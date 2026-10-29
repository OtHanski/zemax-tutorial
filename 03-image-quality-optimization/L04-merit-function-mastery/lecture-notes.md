# L04 — Merit function mastery

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~3 h, tasks ~6 h
> **Prerequisites:** [Course 01 L07 (solves, variables, first optimization)](../../01-foundations/L07-solves-variables-first-optimization/), [L01–L03 of this course](../L03-strehl-wavefront-error-depth-of-focus/) · **Next:** [L05 — Optimization strategies and global search](../L05-optimization-strategies-and-global-search/)

## Learning objectives
- Write the OpticStudio merit-function formula, compute an MF value and % contributions by hand, and explain why MF values of differently built merit functions cannot be compared.
- Choose every option of the default merit function (type, criterion, reference, pupil integration, rings/arms or grid, symmetry, vignetting, boundaries) deliberately and justify the choice for a given lens.
- Use the main operand families — first-order, aberration, ray, image-quality, boundary/manufacturing, and *math* operands that act on other operands (SUMM, DIFF, PROD, DIVI, ABSO, OPGT, OPLT, …) — to express a written specification as constraints.
- Set weights from tolerances, and diagnose a merit function that is dominated by the wrong operand.
- Build, from a blank editor, a complete custom merit function for a fixed-focus camera lens with packaging, manufacturability and chief-ray-angle constraints.

## Reading
- **Core:** [Geary Ch. 8, pp. 85–95] — M- and F-solves (§8.2–8.3), rings and arms (§8.4), the merit-function definition and a hand computation of MF and % contribution (§8.5, eq. 8.7), RMS spot size (§8.6).
- **Core:** [Geary App. E, pp. 457–458] — short definitions of the operands used in his book (ASTI, AXCL, COMA, DIFF, DIST, DIVI, EFFL, EFLY, FCGS/FCGT, FCUR, LACL, MNCA/MNCG/MXCA/MXCG, OPTH, PARR, PETC/PETZ, PMAG, RAID, SPHA, TOTR, TRAC, TTHI). Translate "Tools → Default Merit Function" to today's **Optimize → Optimization Wizard**.
- **Refresh:** [Course 01 L07 §4](../../01-foundations/L07-solves-variables-first-optimization/lecture-notes.md) — MF definition, why Gaussian quadrature works, boundary basics.
- **Online:** Ansys KB KA-01644, E. Elliott & J. Aiona, "Contrast optimization": <https://optics.ansys.com/hc/en-us/articles/42661802617491> — the Contrast criterion and its `MECS`/`MECT` operands; why it beats direct MTF optimization.
- **Online:** Ansys KB, H. Chen, "Why is the RMS spot size listed in Spot Diagram different than the values reported by RSCE and RSRE operands?": <https://optics.ansys.com/hc/en-us/articles/43071095528979-Why-is-the-RMS-spot-size-listed-in-Spot-Diagram-different-than-the-values-reported-by-RSCE-and-RSRE-operands> — Gaussian quadrature vs rectangular array, centroid vs chief ray.
- **Online:** Ansys KB, singlet design tutorial (Optimization Wizard walk-through, boundary values): <https://optics.ansys.com/hc/en-us/articles/42661700528275>
- **In the software:** Help → the Merit Function Editor operand list (searchable). Treat it as the authoritative dictionary; every operand's Int1/Int2/Hx/Hy/Px/Py/Data columns are defined there.

---

## 1. The merit function is the specification

An optimizer does exactly what the merit function (MF) says and nothing more. A lens that is "optimal" but 2 mm too long, has a 35° chief-ray angle at the sensor, or a 0.3 mm edge thickness is not a design — it is a merit function bug. Professional designers spend more time on the MF than on any other part of the optimization. The mental model:

```
 ┌──────────────────────────────────────────────────────────┐
 │ 1. First-order constraints (EFFL, magnification, F/#)     │  ← prefer solves where possible
 │ 2. Packaging (TOTR, back focus, max diameter)              │
 │ 3. Manufacturability (centre/edge thickness, glass, AOI)   │
 │ 4. Interface/system (CRA, telecentricity, distortion, RI)  │
 │ 5. Monitors (weight 0: Seidels, colour, distortion...)     │
 │ DMFS ─────────────────────────────────────────────────────│
 │ 6. Image quality (default MF: spot / wavefront / contrast) │
 └──────────────────────────────────────────────────────────┘
```

Everything above `DMFS` (Default Merit Function Start) is yours and survives re-running the wizard; everything below is regenerated.

## 2. The arithmetic

OpticStudio defines [Geary eq. 8.7, p. 88; Course 01 L07]

$$
\text{MF}^2 = \frac{\sum_i W_i\,(V_i - T_i)^2}{\sum_i W_i},\qquad \text{contribution}_i = \frac{W_i(V_i-T_i)^2}{\sum_j W_j(V_j-T_j)^2}.
$$

($W_i$ weight, $V_i$ value, $T_i$ target; rows with $W_i = 0$ are computed but ignored.) Consequences that bite:

1. **Only ratios of weights matter** for where the minimum is, but the *value* of MF depends on all weights through the denominator. Adding a constraint row changes the MF number even if the lens is unchanged. Never compare MF values between differently built merit functions; compare physical results (RMS spot, MTF, Strehl, constraints met).
2. **The MF of a pure default MF has meaning.** With RMS/Spot/Centroid and Gaussian quadrature, the weights are the quadrature weights (times field and wavelength weights) and MF = polychromatic, field-weighted RMS spot radius in lens units. Geary computes 40.5 µm for his test singlet by hand from three `TRAC` rows with weights 0.8727, 1.3963, 0.8727 (sum π) [Geary §8.5]. With RMS/Wavefront the MF is the RMS wavefront error in waves.
3. **Units mix.** A row in mm (EFFL), one in waves (OPDX), one in degrees (RAID) all enter the same sum. The weight is what converts "1 unit of error" into "how much I care".

### 2.1 Setting weights from tolerances
A principled starting point: make every operand contribute equally when it is *at its tolerance*. If the image-quality part contributes $\Phi_\text{IQ}$ at the acceptable image quality and operand $i$ has tolerance $\tau_i$, choose

$$
W_i \approx \frac{\Phi_\text{IQ}}{\tau_i^2}.
$$

Example (Geary's singlet, MF built from 3 `TRAC` rows, $\sum W_\text{IQ} = \pi$). Suppose the acceptable RMS spot is 10 µm, so $\Phi_\text{IQ} \approx \pi\times(0.010)^2 = 3.14\times10^{-4}$ mm². For EFFL with tolerance ±0.05 mm: $W = 3.14\times10^{-4}/0.0025 = 0.126$. Contrast this with a careless weight of 1 and an EFFL error of 0.5 mm: MF² = (π·0.0405² + 1·0.5²)/(π + 1) → MF = 0.248 mm and **98%** of the MF is the focal length. With $W = 10^{-4}$ the EFFL error contributes only 0.5% and is essentially ignored. Both extremes are wrong; weight by tolerance, then watch the % Contrib column.

Rules of thumb:
- Hard first-order quantities (focal length, magnification, F/#) → use **solves** when possible (exact, no weight), otherwise high weight.
- Boundary operands (`MNCG`, `MNEG`, `OPGT`, …) can carry large weights because they contribute nothing until violated.
- If one operand holds > 50% of the MF for many cycles, either it conflicts with others (re-think the spec) or its weight is mis-scaled.
- Field weights and wavelength weights (System Explorer) are multiplied into the default-MF weights: set them deliberately — e.g. weight the 0.7 field highest for a camera lens whose corners matter less, or use the measured LED/VCSEL spectrum for wavelength weights.

### 2.2 Lagrange-multiplier (exact) constraints
Besides weighted least squares, OpticStudio can treat an operand as an equality constraint enforced exactly by the optimizer (Lagrange multiplier) — specified, in current versions, by giving the row a **negative weight**. This is useful for a few first-order constraints that cannot be expressed as solves. Use sparingly: too many exact constraints over-determine the problem and the optimizer stalls. (Check the Help section on the Merit Function Editor for the exact behaviour in your release.)

## 3. The default merit function, option by option

Optimize → **Optimization Wizard** (also available from inside the MFE). Course 01 L07 introduced the main choices; here is the professional checklist.

| Group | Option | What it does | When to choose |
|---|---|---|---|
| Optimization function | **Type**: RMS / PTV | RMS minimizes the root-mean-square of ray (or OPD) errors; PTV targets the extreme errors (peak-to-valley) | RMS almost always (smooth, statistically meaningful). PTV when *all* rays must land inside a pixel/fibre core, or to find the minimum-blur focus (L03 Task 3) |
| | **Criterion**: Spot / Wavefront / Contrast / Angular | Transverse ray error (`TRAC`-type rows), OPD (`OPDX` rows), Moore–Elliott contrast (`MECS`/`MECT` pairs at a chosen frequency), angular error for afocal systems | Spot for aberration-limited stages; Wavefront once within a few waves (best Strehl/MTF focus, L03); Contrast for final MTF tuning at a target frequency (Professional/Premium); Angular for afocal/collimators |
| | **Reference**: Centroid / Chief ray (others in some versions) | Error measured from the spot centroid or from the chief-ray intercept | Centroid = what a sensor sees, insensitive to distortion and to pure lateral shift. Chief ray also penalizes coma-like centroid shift and lateral colour — slightly stricter; useful when distortion/lateral colour are not otherwise constrained |
| Pupil integration | **Gaussian quadrature** (rings, arms) | Exact for polynomial aberrations up to degree $2n-1$ in $\rho^2$ with $n$ rings; arms sample azimuth | Default for unvignetted circular/elliptical pupils. Rings 3–4 for ordinary lenses; 5–8 for fast lenses and high-order aspheres. Arms 6; 8–12 if the pupil is strongly asymmetric |
| | **Rectangular array** (grid) | Uniform grid; can delete vignetted rays | Vignetted, obscured, decentred or non-circular pupils; NSC-like apertures. Grid 6×6 to 20×20 |
| | Obscuration | Inner radius of the GQ annulus | Cassegrains etc. (Course 02 L12) |
| Symmetry/vignetting | Assume axial symmetry | Traces only +y fields and half the pupil | On for rotationally symmetric lenses (same MF value, fewer rows) [Geary §8.4]. Off for tilted/decentred systems |
| | Delete vignetted | Drops rays clipped by apertures (RA only) | On when you rely on hard apertures for vignetting |
| | Ignore lateral color | References each wavelength to its own centroid | When lateral colour is corrected electronically or irrelevant; otherwise leave off |
| Boundaries | Glass min/max centre, min edge; Air min/max centre, min edge | Inserts `MNCG`/`MXCG`/`MNEG` and `MNCA`/`MXCA`/`MNEA` rows | Always. Typical small optics: glass centre ≥ 1–2 mm, edge ≥ 0.8–1 mm; air ≥ 0.1–0.5 mm centre and edge |
| Bookkeeping | Start at (row), Overall weight, Configuration (all/current), field and wavelength choice | Where DMFS goes and how the block is weighted | Leave rows above for your operands; set Configuration = All for multi-configuration designs (L06) |

### 3.1 Spot vs wavefront vs contrast — the evolution of a design
A typical design moves through criteria as it improves:

1. **Spot, centroid, GQ 3×6** — robust when aberrations are large; transverse errors are smooth functions of the variables.
2. **Wavefront, centroid** — when RMS spot approaches ~2× the Airy radius; puts the image at the max-Strehl focus and balances aberrations for MTF (L03 §3).
3. **Contrast** at the frequency that matters (e.g. Nyquist/2) — final polishing. The KA-01644 study shows contrast optimization runs about as fast as RMS wavefront and has a smooth minimum where direct MTF operands are flat or noisy; the MF value is *not* the MTF, so evaluate MTF separately afterwards. Avoid frequencies in the spurious-resolution regime (beyond the first MTF zero of a defocused/aberrated system).
4. **Direct MTF operands** (`MTFT`/`MTFS`/`MTFA`, `GMTT`/`GMTS`/`GMTA`, `MTHT`/`MTHS`/`MTHA`; L02) — only for final targeted constraints (e.g. "MTF ≥ 0.3 at 145 cycles/mm at 0.7 field" via `OPGT`), sparingly, because they are slow.

### 3.2 Gaussian quadrature vs rectangular array — the vignetting trap
GQ places rays on fixed rings assuming a full, unvignetted (possibly elliptical, via vignetting factors) pupil. If your lens vignettes by hard apertures and you do not set vignetting factors, GQ traces rays that the real lens blocks — the optimizer then works hard to correct rays that never reach the sensor. Either set vignetting factors (Course 02 L09) and keep GQ, or use RA with "delete vignetted". The same distinction applies to the RMS spot operands: `RSCE`/`RSCH` (GQ, centroid/chief) vs `RSRE`/`RSRH` (rectangular array) — and to why their values differ from a spot-diagram RMS unless ray pattern, density and reference match [Ansys KB, H. Chen].

## 4. The operand toolbox

All operands below exist in current OpticStudio (see Help for arguments). Group them mentally by purpose.

| Purpose | Operands | Notes |
|---|---|---|
| First order | `EFFL` (EFL), `EFLY` (EFL of a surface group), `PMAG` (paraxial magnification), `WFNO` (working F/#), `ISFN` (image-space F/#), `TOTR` (total track), `ENPP`/`EXPP` (entrance/exit pupil position), `EPDI` (EPD) | Many can be replaced by solves (marginal-ray angle / F/# solve, pickups) |
| Seidel / aberration monitors | `SPHA`, `COMA`, `ASTI`, `FCUR`, `DIST`, `PETZ`/`PETC`, `AXCL`, `LACL` | Third-order, waves or lens units; good monitors (weight 0) and good early-stage targets |
| Real rays | `REAX`/`REAY` (real ray x/y at a surface), `RAID` (real angle of incidence), `TRAC` (radial transverse aberration), `OPDX` (OPD), `PARR` (paraxial radial height) | Fields $H_x, H_y$ and pupil $P_x, P_y$ normalized to ±1 |
| Image quality | `RSCE`/`RSCH`/`RSRE`/`RSRH` (RMS spot), MTF families, `ZERN` (Zernike coefficient), `MECS`/`MECT` (contrast), `DIMX` (max distortion), `DISG` (generalized distortion) | Use the default MF for the bulk, these for targeted constraints |
| Manufacturing / geometry | `MNCG`/`MXCG`/`MNEG`, `MNCA`/`MXCA`/`MNEA`, `MNCT`/`MXCT`/`MNET`/`MXET` (any medium), `CTGT`/`CTLT` (centre thickness greater/less than, single surface), `ETGT`/`ETLT` (edge thickness), `TTHI` (sum of thicknesses), `RAID` (limit AOI — coatings, sensitivity) | Boundary operands are one-sided; they cost nothing until violated |
| Glass | `RGLA` (keeps model glasses near real ones), `MNIN`/`MXIN`, `MNAB`/`MXAB`, `MNPD`/`MXPD` (index, Abbe, partial-dispersion bounds) | For model-glass optimization (L05) |
| Bookkeeping | `BLNK` (comment), `DMFS`, `CONF` (switch configuration, L06) | Comments make an MF readable months later |

### 4.1 Operands that act on other operands
These take *row numbers* of other operands as arguments and combine their values. Give the referenced rows **weight 0** (they are ingredients), and put the weight on the combining row.

| Operand | Value |
|---|---|
| `SUMM` | sum of two operands |
| `OSUM` | sum of a range of operands |
| `DIFF` | difference of two operands |
| `PROD` | product |
| `DIVI` | quotient |
| `ABSO` | absolute value of one operand |
| `SQRT` | square root |
| `RECI` | reciprocal |
| `CONS` | a constant (useful as an ingredient) |
| `MAXX` / `MINN` | maximum / minimum of a range of operands |
| `EQUA` | drives a range of operands towards equality (to their average) |
| `OPGT` / `OPLT` | operand greater than / less than target — the generic inequality |

Patterns you will use constantly:

```
# |distortion| ≤ 1% at full field  (DIST evaluated for the max field, all surfaces)
 5  DIST   0  w=1  0 ...                weight 0       (ingredient)
 6  ABSO   5                            weight 0
 7  OPLT   6         target 1.0         weight 10

# Back focal distance ≥ 6 mm (last thickness = surface 9)
 8  CTGT   9         target 6.0         weight 10

# Chief-ray angle at sensor ≤ 20° at full field (image surface = 10)
 9  RAID  10  w=1  Hx=0 Hy=1 Px=0 Py=0  weight 0
10  OPLT   9         target 20          weight 5

# Total track 30 ≤ TOTR ≤ 32
11  TOTR                                weight 0
12  OPLT  11         target 32          weight 10
13  OPGT  11         target 30          weight 10

# Ratio: back focus / EFL ≥ 0.4
14  TTHI   9  9                          weight 0       (thickness after surface 9)
15  EFFL                                 weight 0
16  DIVI  14 15                          weight 0
17  OPGT  16         target 0.4          weight 5
```

(The column layout is schematic: operand name, the Int1/Int2 arguments, then field/pupil coordinates, target, weight. Always check the Help definition of each operand's arguments — for example whether `DIST` reports percent and for which wavelength, or whether `RAID` measures the angle in degrees from the surface normal.)

Watch out: when you insert rows above, the row numbers referenced by `DIFF`, `OPGT`, etc. may no longer point at the intended rows. After editing, verify references (hover or re-read the row values), and keep custom blocks compact and commented with `BLNK` rows.

## 5. Constraint strategy: solves, operands, variables

| Situation | Best tool |
|---|---|
| Exact paraxial relation (F/#, image at paraxial focus, curvature pickup, symmetric thickness) | **Solve** — removes one variable and one equation exactly |
| A physical limit (min thickness, max length, max AOI) | **Boundary / OPGT / OPLT** with generous weight |
| A target with a tolerance (EFL ± 0.5%) | Weighted equality, weight from tolerance |
| Something you want to *see* but not control | Weight 0 monitor row |
| A first-order condition that can't be a solve but must be exact | Lagrange (negative-weight) constraint — sparingly |

And on the variable side: don't make variables of things you will not be allowed to change (catalog-fixed thicknesses, a sensor cover glass), and keep the number of variables ≥ number of *active* constraints + a healthy margin for image quality, or the optimizer will satisfy constraints and ignore aberrations.

## 6. A worked custom merit function

**Specification (fixed-focus NIR receiver lens, used again in L05):** EFL 8.0 mm ± 1%, F/2.0, 940 nm ± 20 nm (three wavelengths 0.920/0.940/0.960 µm), image circle Ø 6.0 mm (1/2.7"-class sensor, full field at image height 3.0 mm), object at 1 m, total track ≤ 16 mm, back focal distance (last lens vertex to image) ≥ 3.0 mm incl. a 0.7 mm cover glass, max CRA at image ≤ 25°, |distortion| ≤ 3%, all elements ≥ 0.8 mm centre and edge thickness (glass), air ≥ 0.1 mm.

A sensible MF (top to bottom):

| Rows | Operands | Weight logic |
|---|---|---|
| 1–3 | `BLNK` "first order"; `EFFL` target 8.0 (tolerance 0.08 → $W \approx \Phi_\text{IQ}/0.08^2$); F/2 by **F/# solve** on the last lens surface (no row needed) | first order |
| 4–7 | `TOTR` + `OPLT` 16; last air thickness `CTGT` 3.0 (or `TTHI` over the back-focus surfaces + `OPGT`) | packaging |
| 8–10 | `RAID` (image surface, $H_y=1$, chief ray) + `OPLT` 25 | sensor interface |
| 11–13 | `DIST` at full field + `ABSO` + `OPLT` 3.0 | calibration-friendly distortion |
| 14–18 | monitors (weight 0): `SPHA`, `COMA`, `ASTI`, `FCUR`, `AXCL` | understanding |
| `DMFS` | Wizard: RMS / Spot / Centroid, GQ 4 rings × 6 arms, fields 0, 0.5, 0.7, 0.85, 1.0 with weights 1, 1, 1.2, 1, 0.8; boundaries glass 0.8/8/0.8, air 0.1/20/0.1 | image quality + manufacturability |

Estimating $\Phi_\text{IQ}$: if a 3 µm RMS spot (≈ the pixel size) is "acceptable", $\sum W_\text{IQ}$ is what the Wizard produced (read it off by summing the weights, or temporarily set one test row) and $\Phi_\text{IQ} \approx \sum W_\text{IQ}\times(0.003)^2$. Then $W_\text{EFFL} \approx \Phi_\text{IQ}/0.08^2$. In practice you round these and adjust after the first runs by looking at % Contrib.

You will build exactly this MF in Task 3 and optimize it in L05 (where the starting point and global search matter).

## 7. In OpticStudio — workflow and pitfalls

- **Optimize → Merit Function Editor**; **Wizards and Operands** panel → Optimization Wizard. Insert rows with the Insert key; operand type from the drop-down or by typing the name.
- The MFE toolbar shows the current MF; the **% Contrib** column is your main diagnostic. Saving the MF separately (`.MF` file) lets you reuse it across designs.
- **Re-running the Wizard** replaces everything below `DMFS`. Put custom rows above it.
- **Ray errors**: if a referenced ray cannot be traced (TIR, misses a surface), the row returns an error and optimization may fail; reduce field/aperture temporarily or add `RAID`/clear-aperture constraints that keep rays well-behaved.
- **Over-constrained MF**: if constraints alone already define the lens, image quality has no freedom. Count variables vs active constraints.
- **Hidden conflicts**: e.g. requiring telecentricity *and* a short total track *and* low distortion with three elements — the optimizer will show you the conflict as a stubborn high-contribution row. That is information for the system engineer, not a reason to keep increasing weights.
- **Speed**: an MF with thousands of rows (many fields × wavelengths × rings × arms × configurations) slows every optimization cycle and Hammer/Global search (L05). Start lean (3 rings, 6 arms, 3 fields), add sampling at the end.

---

## Key takeaways
- The MF *is* the specification; build it in layers (first order, packaging, manufacturing, interface, monitors, image quality).
- MF² = Σ W(V−T)²/ΣW. Weights are relative; set them from tolerances so each operand contributes comparably at its limit; watch % Contrib.
- Default MF choices matter: Spot → Wavefront → Contrast as the design matures; Centroid reference by default; GQ unless vignetting/obscuration demands RA; always set boundaries.
- Math operands (SUMM, DIFF, PROD, DIVI, ABSO, MAXX, MINN, EQUA, OPGT, OPLT…) turn any computed value into an inequality or combined target; the ingredients carry weight 0.
- Prefer solves for exact first-order constraints; use Lagrange-type exact constraints sparingly.
- Keep custom rows above DMFS, comment them, and re-check row references after editing.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| DMFS | Marker row: start of the wizard-generated default merit function |
| % Contrib | Fraction of the MF sum contributed by one row |
| Boundary operand | One-sided constraint that contributes only when violated (MNCG, OPGT, …) |
| Ingredient row | Weight-0 operand whose value is used by a math operand |
| Contrast optimization | Moore–Elliott method using `MECS`/`MECT` OPD differences between sheared rays to maximize MTF at a given frequency |
| Lagrange (exact) constraint | Constraint satisfied exactly by the optimizer rather than in least-squares sense |
| Tolerance weighting | $W_i \propto 1/\tau_i^2$ so operands contribute equally at tolerance |

## References
1. [Geary] J. M. Geary, *Introduction to Lens Design*, 2002: Ch. 8, pp. 85–95; App. E, pp. 457–458.
2. Course 01 L07 lecture notes (this repository): MF definition, Gaussian quadrature, boundaries, DLS.
3. Ansys Optics KB KA-01644, E. Elliott & J. Aiona, "Contrast optimization": <https://optics.ansys.com/hc/en-us/articles/42661802617491>
4. Ansys Optics KB, H. Chen, "Why is the RMS spot size listed in Spot Diagram different than the values reported by RSCE and RSRE operands?": <https://optics.ansys.com/hc/en-us/articles/43071095528979-Why-is-the-RMS-spot-size-listed-in-Spot-Diagram-different-than-the-values-reported-by-RSCE-and-RSRE-operands>
5. Ansys Optics KB, singlet design tutorial (Optimization Wizard and boundary values): <https://optics.ansys.com/hc/en-us/articles/42661700528275>
6. Ansys Optics KB KA-01362, "How to calculate and optimize MTF": <https://optics.ansys.com/hc/en-us/articles/42661772706835>
7. Zemax Community, "Best merit function to use for minimize RMS spot size": <https://community.zemax.com/got-a-question-7/best-merit-function-to-use-for-minimize-rms-spot-size-2941>
