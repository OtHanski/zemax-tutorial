# L06 — Chromatic Aberration and Achromats

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3.5 h, tasks ~5 h
> **Prerequisites:** [L01](../L01-wavefront-and-transverse-aberrations/)–[L03](../L03-coma-astigmatism-and-symmetry/); Course 01 [L05 optical glass](../../01-foundations/L05-optical-glass-and-dispersion/) · **Next:** [L07 — Secondary spectrum and apochromats](../L07-secondary-spectrum-apochromats/)

## Learning objectives
- Compute axial colour of a thin lens ($\delta f = -f/V$) and of a system from the Seidel chromatic sums $C_L$, $C_T$; explain why lateral colour of a thin lens at the stop is zero and how it appears with a stop shift.
- Derive and apply the thin-lens achromat power split $K_1 = KV_1/(V_1-V_2)$, $K_2 = -KV_2/(V_1-V_2)$, and compute radii of a cemented doublet for a chosen bending.
- Use thin-lens Seidel theory to map spherical aberration (parabola) and coma (line) versus bending, and decide from that map whether a given glass pair can be an **aplanat**.
- Design a 100 mm F/5 cemented achromat in OpticStudio from the thin-lens pre-design, correcting axial colour, spherical aberration and coma, and interpret Chromatic Focal Shift, Longitudinal Aberration and Lateral Color plots.
- Explain why the "best" doublet leaves some third-order spherical aberration to balance fifth order, and what spherochromatism and secondary spectrum are.
- Define colour correction for a non-visible band (e.g. NIR) with an appropriate Abbe-like number.

## Reading
- **Core:** [Geary Ch. 16, pp. 175–183] — primary axial colour, $C_L$, the wavefront colour term and the thin-lens achromat (§16.5).
- **Core:** [Geary Ch. 17, pp. 185–194] — bending the achromat in ZEMAX, two zero-spherical solutions, higher-order spherical, spherochromatism, the aplanat (§17.7) and lateral colour (§17.8).
- **Core:** [Kidger Ch. 5, §5.1–5.1.4, pp. 91–97] — dispersion, V-number, secondary spectrum (preview), lateral colour.
- **Core:** [Kidger §8.1–8.2.3, pp. 167–177] — Seidel analysis of doublets, what a doublet can and can't correct (Table 8.1), the cemented doublet, crown-first (Fraunhofer) and flint-first (Steinheil) examples with full Seidel tables.
- **Optional:** [Kidger §5.2, pp. 97–100] — Conrady's $D-d$ method for chromatic aberration from real rays. [Kidger §7.2.6–7.2.7, §7.3.7] — thin-lens colour formulas.
- **Optional online:** SCHOTT optical glass data sheets / catalogue (Sellmeier coefficients, $n_d$, $V_d$, $P_{g,F}$) — available from schott.com; OpticStudio ships the same data in its SCHOTT.AGF catalogue.

---

## 1. Chromatic aberration of a single lens

The index of every transparent material falls with wavelength (normal dispersion), so a positive lens is stronger in blue than in red: blue focuses closer [Kidger §5.1.1, Fig. 5.2; Geary §16.2]. For a thin lens $K = (n-1)(c_1-c_2)$, so

$$
\delta K = \delta n\,(c_1-c_2) = \frac{K}{V},\qquad V = \frac{n_d - 1}{n_F - n_C},\qquad
\delta f = f_F - f_C = -\frac{f}{V}.
$$

**The axial colour of a thin singlet is its focal length divided by its Abbe number — independent of its shape.** For an N-BK7 lens ($V_d = 64.17$) of $f = 100$ mm, the F and C foci are 1.56 mm apart; Geary's 400 mm example gives 6.23 mm [Geary §16.4, p. 180]. At F/5 the diffraction depth of focus is only ±0.029 mm. Colour is not a subtle effect.

### 1.1 Seidel chromatic sums
Per surface [Kidger Eqs. 6.49–6.50]:

$$
C_L = A\,y\,\Delta\!\left(\frac{\delta n}{n}\right),\qquad C_T = \bar A\,y\,\Delta\!\left(\frac{\delta n}{n}\right),\qquad \delta n = n_F - n_C ,
$$

and for a thin lens at the stop $C_L = h^2K/V$, $C_T = 0$ [Kidger Eqs. 7.18, 7.20]. These are **first-order** chromatic aberrations (paraxial focus and magnification change with wavelength). In wavefront form $W_{020}^{chr} = C_L/2$ (axial colour, a defocus) and $W_{111}^{chr} = C_T$ (lateral colour, a tilt ∝ field) — the "W020/W111" lines of the OpticStudio Seidel report (L01). Longitudinal: $\delta z_{F-C} = -C_L/(n'u'^2)$; transverse lateral colour at full field: $C_T/(n'u')$.

> **Sign alert.** Kidger/Welford's convention (used in our `seidel.py`) gives $C_L = +h^2K/V > 0$ for a positive lens. OpticStudio's Seidel report shows the **opposite sign**: Geary's ZEMAX listing of a positive 400 mm singlet gives CLA = −0.01558 [Geary Fig. 16.5], whose magnitude equals $h^2K/V = 20^2\cdot0.0025/64.17 = 0.01558$. Compare magnitudes, and check the sign on a singlet before trusting a convention.

### 1.2 Lateral colour
With the stop at a thin lens the chief ray passes through the centre: no prism effect, $C_T = 0$. Move the stop and the chief ray passes through the lens off-centre — a thin prism — and the image of an off-axis point is spread into a spectrum radially [Geary §17.8]. The stop-shift equation (L03):

$$
C_T^* = C_T + \chi\,C_L .
$$

So **a system corrected for axial colour has stop-independent lateral colour** [Kidger §7.3.1.6]. Lateral colour is a wavelength-dependent *magnification*: it can't be refocused away and it grows linearly with field. In colour cameras it shows up as coloured fringes at edges toward the corners; in a multi-wavelength 3D sensor (e.g. pattern projected in one band, texture captured in another) it is a wavelength-dependent *distortion* that calibration must handle per band.

## 2. The thin-lens achromat

Two thin lenses in contact, glasses with $V_1$ (crown, high $V$) and $V_2$ (flint, low $V$). Require total power $K$ and zero axial colour [Kidger Eqs. 5.6–5.8; Geary §16.5]:

$$
K_1 + K_2 = K,\qquad \frac{K_1}{V_1} + \frac{K_2}{V_2} = 0
\quad\Longrightarrow\quad
K_1 = \frac{V_1}{V_1-V_2}K,\qquad K_2 = -\frac{V_2}{V_1-V_2}K .
$$

Lessons from these two lines:
- The element powers scale as $1/(V_1 - V_2)$. A large Abbe difference keeps the elements weak (shallow curves, less higher-order aberration). Typical: $V_1 \approx 60$, $V_2\approx36$ gives $K_1 = 2.5K$, $K_2 = -1.5K$ [Kidger §8.1.1] — the "+2.5/−1.5" rule.
- Both elements carry **more** power than the whole doublet. Monochromatic aberrations of the doublet are therefore a delicate cancellation between two stronger lenses.
- **Petzval gets slightly worse:** $P = K_1/n_1 + K_2/n_2$. For N-BK7/N-SF5 (below) $Pf = 0.72$, vs. $0.66$ for an N-BK7 singlet of the same power. Correcting Petzval and colour together would need $n_1/n_2 = V_1/V_2$ — not available among visible glasses at sensible powers [Kidger §8.1.4]. A doublet cannot flatten its field (Kidger Table 8.1: it can correct $S_I$, $S_{II}$, $C_L$; not $S_{III}$, $S_{IV}$; $S_V$ and $C_T$ are zero at the stop).

### 2.1 Bending the cemented doublet
Once the powers are fixed and the doublet is cemented ($c_2$ shared), **one free parameter** remains: the overall shape, e.g. $c_1$. Bending keeps both powers, hence colour correction, unchanged [Geary §17.3]. As with the singlet:
- $S_I(c_1)$ is a **parabola** — but now, thanks to the negative flint, its minimum can be below zero, giving **two** zero-spherical bendings ("left-hand" and "right-hand" solutions, [Geary §17.3, Fig. 17.5]).
- $S_{II}(c_1)$ is a **straight line** — one coma-free bending.
- An **aplanat** ($S_I = S_{II} = 0$) needs the zero of the line to fall on a zero of the parabola. Whether that happens depends only on the **glass pair** [Kidger §8.2, Fig. 8.2]. With the wrong pair you must give up something — Geary shows that forcing $S_I = S_{II} = 0$ with three radii and fixed glasses costs colour correction [Geary §17.7].

## 3. Worked example — a 100 mm F/5 cemented achromat

**Specification:** $f = 100$ mm, F/5 (EPD 20 mm, $h = 10$ mm, $u' = -0.1$), object at infinity, semi-field 1°, wavelengths F, d, C (d primary), crown first, stop at the first surface. Glass data computed from SCHOTT Sellmeier coefficients:

| Glass | $n_F$ | $n_d$ | $n_C$ | $V_d$ | $P_{g,F}$ |
|---|---|---|---|---|---|
| N-BK7 | 1.52238 | 1.51680 | 1.51432 | 64.17 | 0.5349 |
| F2 | 1.63208 | 1.62004 | 1.61503 | 36.37 | 0.5828 |
| N-SF5 | 1.68750 | 1.67271 | 1.66664 | 32.25 | 0.5984 |

### 3.1 Which flint? A thin-lens Seidel scan
For each pair, compute the powers, then scan $c_1$ with $c_2 = c_1 - K_1/(n_1-1)$, $c_3 = c_2 - K_2/(n_2-1)$, and evaluate $S_I$, $S_{II}$ with `seidel.py` (thin lenses, stop at the doublet, 1° field):

**N-BK7 / F2:** $K_1 = 0.023081$ ($f_1 = 43.33$ mm), $K_2 = -0.013081$ ($f_2 = -76.45$ mm).
- Zero coma at R = 62.20 / −34.98 / −133.56 mm, but there $S_I = -0.0082$ mm ($W_{040} = -1.75$ waves, *over*corrected).
- Zero spherical at two bendings: R = 46.37 / −43.30 / −500.1 ($S_{II} = +0.00164$) and R = 101.05 / −28.76 / −73.16 ($S_{II} = -0.00185$).
- → **not an aplanatic pair** (crown-first): you choose between zero spherical with some coma, or zero coma with overcorrected spherical.

**N-BK7 / N-SF5:** $K_1 = 0.020105$ ($f_1 = 49.74$ mm), $K_2 = -0.010105$ ($f_2 = -98.96$ mm) — weaker elements, thanks to the larger $V$ difference (31.9 vs 27.8).

| $c_1$ (mm⁻¹) | R1 / R2 / R3 (mm) | $S_I$ (mm) | $S_{II}$ (mm) | $W_{040}$ (waves) |
|---|---|---|---|---|
| 0.0100 | 100.0 / −34.60 / −72.04 | 0.00966 | −0.00196 | 2.06 |
| 0.0150 | 66.67 / −41.84 / −112.6 | 0.00071 | −0.00046 | 0.15 |
| **0.01652** | **60.54 / −44.67 / −135.8** | **0.00041** | **0** | **0.09** |
| 0.0180 | 55.56 / −47.84 / −170.0 | 0.00120 | +0.00045 | 0.26 |
| 0.0200 | 50.00 / −52.90 / −257.6 | 0.00397 | +0.00105 | 0.85 |

The parabola's minimum (≈ +0.0004 mm) sits almost exactly at the coma-free bending: **N-BK7/N-SF5 is (very nearly) an aplanatic pair** at F/5 — the residual 0.09 wave of third-order spherical is negligible. This is the professional way to choose a glass pair: a 20-line thin-lens scan *before* opening the optimiser.

### 3.2 Thick lens
Give the crown 5 mm and the flint 2.5 mm centre thickness (edge thicknesses ≈ 2.8 mm and ≈ 3.3 mm at 10.5 mm semi-diameter — manufacturable). Re-solve the three curvatures for EFL = 100 mm, F and C paraxial foci coincident, and $S_{II} = 0$ (exact thick-lens paraxial optics + Seidel sums):

**Design A ("Seidel aplanat"):** R1 = 60.702, R2 = −43.117, R3 = −129.742 mm; BFL = 96.446 mm. $S_I = 0.00020$ mm ($W_{040}$ = 0.04 wave), $S_{II} = 0$, $S_{III} = 0.00029$, $S_{IV} = 0.00022$ mm.

Now the real rays (exact meridional trace at d, image at paraxial d focus): the marginal ray lands at **+8.3 µm** — *over*corrected, although the Seidel prediction is −1.0 µm. The difference is **fifth-order spherical aberration**, generated mostly at the steep cemented interface. The on-axis wavefront is still excellent: RMS after refocus ≈ 0.026 wave; RMS spot radius 1.7 µm at best focus vs Airy radius $1.22\lambda N = 3.6$ µm.

**Design B ("real-ray balanced"):** replace $S_{II} = 0$ by "real marginal ray at the paraxial focus = 0": R1 = 54.046, R2 = −47.083, R3 = −177.001 mm. Now $S_I = +0.0015$ mm ($W_{040} = 0.32$ wave of *under*correction deliberately left to cancel the fifth order), the 0.707-zone error is −1.4 µm, on-axis RMS wavefront ≈ 0.004 wave — but $W_{131} = 0.49$ wave of coma at 1°.

This is exactly what Kidger's published Fraunhofer doublet shows (S-SK11/S-SF19: $S_I = 0.0019$, $S_{II} \approx 0$, [Kidger §8.2.2, p. 172]) and what Geary demonstrates with TRAC vs SPHA [Geary §17.4]: **the best real design leaves some third-order spherical to balance higher orders**, and the optimiser — not the Seidel sum — decides how much. With a merit function over 0°, 0.7° and 1°, OpticStudio will land between A and B (Task 3).

### 3.3 Secondary spectrum and spherochromatism
With F and C at a common focus, other wavelengths are not: from the thick design, the d focus lies **0.051 mm closer** to the lens than the common F/C focus, the e focus 0.058 mm closer, and the g focus (435.8 nm) **0.195 mm farther** away (0.246 mm behind the d focus). The thin-lens estimate is

$$
\delta f_{d} = f\,\frac{P_{F,d}^{(1)} - P_{F,d}^{(2)}}{V_1 - V_2} = 100\times\frac{0.6924 - 0.7090}{31.92} = -0.052\ \text{mm},\qquad P_{F,d} = \frac{n_F - n_d}{n_F-n_C}.
$$

That's the **secondary spectrum** (L07): ≈ $f/2000$ for ordinary crown/flint pairs — larger than the ±29 µm depth of focus at F/5 once you include the blue end. In addition, spherical aberration itself varies with wavelength (**spherochromatism**): the F-light ray fan has more spherical than d or C [Geary §17.5, Fig. 17.10; Kidger §8.2.2]. Both are visible in OpticStudio's **Longitudinal Aberration** plot (curves for each wavelength, with different slopes and offsets).

## 4. Colour correction outside the visible

The F, d, C Abbe number is a *visible-band* quantity. For another band, define the analogue with the band's edges and centre [Kidger §5.1.2 advises generating a glass map for your own wavelengths]:

$$
V_{band} = \frac{n_{\text{centre}} - 1}{n_{\text{short}} - n_{\text{long}}}.
$$

Examples (computed from SCHOTT Sellmeier data):

| Glass | $V$(800/850/900 nm) | $V$(450/600/850 nm) |
|---|---|---|
| N-BK7 | 286 | 33.4 |
| F2 | 202 | 19.3 |
| N-SF5 | 181 | 17.1 |

- **Narrow NIR band** (an 850 nm LED with ±50 nm bandwidth): $V$ is ~4× larger than in the visible, so a singlet's axial colour is $f/286$ — still 42 µm for a 12 mm lens, vs. a depth of focus of ±10 µm at F/2.4 and 850 nm. Broadband LEDs need achromatization even in the NIR; a narrow laser/VCSEL source usually doesn't.
- **Visible + NIR** (450–850 nm, e.g. a camera that sees both a blue projected pattern and NIR illumination): the effective $V$ values collapse (33 for N-BK7, 17 for N-SF5) and secondary spectrum becomes the limiting factor → apochromatic glass choices (L07) or deliberate focus-per-band strategies.
- In OpticStudio, define the wavelengths of *your* band (System Explorer → Wavelengths, with weights from the source spectrum × sensor QE) and let AXCL/LACL and the merit function work on those — the catalog $V_d$ is only a pre-design guide.

## 5. In OpticStudio

**Setup.** System Explorer → Wavelengths: preset "F, d, C (Visible)", d primary. Material column: N-BK7, N-SF5 (SCHOTT catalogue loaded under System Explorer → Material Catalogs). A cemented doublet is three surfaces: R1 (N-BK7), R2 (N-SF5), R3 (air). Stop on surface 1, EPD 20 mm.

**Analyses.**
- **Chromatic Focal Shift** — paraxial focus vs wavelength; F and C coincident means achromatized; the parabola's vertex depth is the secondary spectrum. The plot also shows the "diffraction-limited range" for reference [Geary §16.4–16.5].
- **Longitudinal Aberration** — real marginal focus vs pupil zone for each wavelength (spherical + axial colour + spherochromatism in one plot).
- **Lateral Color** — chief-ray height differences between wavelengths vs field, often with the Airy disk for reference.
- **Ray Fan with all wavelengths** — same slope at the origin for F and C means colour-corrected; different curvature = spherochromatism.
- **Seidel Coefficients** — SPHA, COMA, CLA (axial), CTR (lateral) per surface; mind the CLA sign convention (§1.1).

**Operands.** **EFFL** (focal length), **AXCL** (axial colour: paraxial focus difference between the two specified wavelengths, Geary §16.4), **LACL** (lateral colour), **SPHA**, **COMA** (Seidel, by surface or sum), **EFLY** (focal length of a surface range — Geary uses it to read the element focal lengths of a doublet with a tiny air gap, §17.2), and the default merit function (RMS spot or wavefront, centroid or chief ray, Gaussian quadrature rings/arms).

**Optimisation recipe (follow Geary Ch. 17 in spirit):**
1. Enter the thin-lens radii with real thicknesses; the EFL and colour will be slightly off.
2. Variables: R1, R2, R3. MF: EFFL = 100, AXCL = 0 (wavelengths 1 & 3 = F & C). Optimise → colour and focal length restored.
3. Add SPHA = 0 (sum). Optimise → one of the two zero-spherical bendings (which one depends on the start). Add COMA = 0 → aplanat if the glass pair allows it; otherwise watch what is sacrificed.
4. Replace the Seidel operands by the default merit function (RMS wavefront, 3 fields, 3 wavelengths) + EFFL. Compare: the real-ray optimum keeps a little third-order spherical (§3.2).
5. If the pair can't make an aplanat, let a glass vary: **Glass Solve → Substitute** (catalog glasses, used by Hammer optimisation) or **Model** glass with $n_d$, $V_d$ as variables, then pick a real glass near the result [Kidger §8.2.1]. (More in L07.)

**Pitfalls.** Thicknesses are poor variables for doublets [Kidger §8.2.1]; fix them at manufacturable values (edge thickness ≥ ~1.5–2 mm for this size, check with the Lens Data Editor's edge thickness or the CTGT/ETGT-type operands). Don't forget the cemented interface must be identical on both sides (it is a single surface in OpticStudio, so it automatically is).

## Key takeaways
- Thin-lens axial colour: $\delta f_{F-C} = -f/V$ regardless of shape; $C_L = h^2K/V$; lateral colour is zero at the stop and appears with stop shift: $C_T^* = C_T + \chi C_L$.
- Achromat: $K_1 = KV_1/(V_1-V_2)$, $K_2 = -KV_2/(V_1-V_2)$; bigger $\Delta V$ → weaker elements. Doublets correct $S_I$, $S_{II}$, $C_L$ — not astigmatism or Petzval.
- Bending a cemented doublet: $S_I$ parabola (two zeros possible), $S_{II}$ line; the glass pair decides whether an aplanat exists. N-BK7/N-SF5 ≈ aplanatic; N-BK7/F2 is not (crown-first).
- Real fast-ish doublets leave some undercorrected third-order spherical to balance fifth order; optimise on real rays.
- Secondary spectrum ≈ f/2000 for normal glasses; spherochromatism makes spherical wavelength-dependent.
- Outside the visible, define your own band $V$; NIR broad sources still need colour correction.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Axial (longitudinal) colour | Wavelength dependence of focus position; $C_L$ |
| Lateral (transverse) colour | Wavelength dependence of image height/magnification; $C_T$ |
| Achromat | Lens with two wavelengths (usually F and C) brought to a common focus |
| Crown / flint | Low-dispersion (high $V$) / high-dispersion (low $V$) glass |
| Fraunhofer / Steinheil doublet | Crown-first / flint-first cemented doublet |
| Aplanat | System free of spherical aberration and coma |
| Secondary spectrum | Residual focus difference of the other wavelengths after achromatization |
| Spherochromatism | Variation of spherical aberration with wavelength |
| Band Abbe number | $(n_c - 1)/(n_s - n_l)$ for a user-defined band |

## References
1. [Geary] Ch. 16 "Axial Color and Achromats" pp. 175–183; Ch. 17 "Bending Achromats" pp. 185–194.
2. [Kidger] §5.1–5.1.4 pp. 91–97; §5.2 pp. 97–100; §6.2.5 pp. 111–112; §7.2.6–7.2.7 pp. 145–146; §8.1–8.2.3 pp. 167–177.
3. SCHOTT AG, Optical Glass data sheets / catalogue (Sellmeier coefficients used here for N-BK7, F2, N-SF5). Also available inside OpticStudio (SCHOTT.AGF) and via refractiveindex.info.
