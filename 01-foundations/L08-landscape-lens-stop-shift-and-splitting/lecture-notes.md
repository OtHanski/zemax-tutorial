# L08 — Mini-Project: The Landscape Lens, Stop Shift and Lens Splitting

> **Course 01 · Foundations** · Estimated time: lecture ~2 h, project tasks ~7–8 h (two sessions)
> **Prerequisites:** L01–L07 of this course · **Next:** [Course 02 — L01 Wavefront and transverse aberrations](../../02-aberrations-classical-design/L01-wavefront-and-transverse-aberrations/)

## Learning objectives
- Explain why moving the aperture stop changes coma, astigmatism, distortion and lateral colour but not spherical aberration, and state the Seidel stop-shift relations qualitatively and in formula form.
- Design a Wollaston (rear) landscape lens and a front landscape lens in OpticStudio by combining **bending** and **stop shift**, using solves, variables, boundary constraints and the default merit function.
- Recognize and escape a **local minimum** by changing the starting point.
- Explain the Petzval limit of a singlet and how the landscape lens "flattens" its field with deliberately introduced astigmatism.
- Reduce spherical aberration by **lens splitting** and predict the improvement from the $h^4K^3$ scaling.
- Write a short, professional design report (spec → approach → results → limitations).

## Reading
- **Core:** [Geary §6.3–6.6, pp. 58–64] — stop shifting with SPHA/COMA/ASTI monitoring (Fig. 6.7), the Wollaston rear landscape lens optimization (WOLR files), the meniscus shape at 25° (Fig. 6.9), history, and the front-landscape homework with target spot sizes.
- **Core:** [Geary Ch. 9, pp. 95–101] — lens splitting: 100 mm F/4 singlet → doublet → triplet, $W_{040}$ 9.64 → 2.04 → 0.514 waves, power redistribution, per-surface contributions (Table 9.1), lithography lenses, Fizeau transmission-sphere homework.
- **Core:** [Kidger §6.3, pp. 115–120] — stop-shift effects (Fig. 6.5) and the Seidel stop-shift equations (Eqs. 6.63–6.70).
- **Core:** [Kidger §7.3.5, p. 156] — reduction of spherical aberration by splitting a lens ($S_1 \propto h^4K^3$); [Kidger §7.3.6, pp. 157] — lateral colour of a thin lens away from the stop.
- **Optional:** [Geary §2.6, pp. 17–18] — file-naming discipline; you'll need it for this project.

---

## 1. Why a landscape lens?

The single positive lens in front of a flat film was the first photographic objective. Wollaston (1812) noticed that a **meniscus** lens with the **stop placed in front of it** at the right distance gives a much flatter, sharper field than a biconvex lens with the stop at the lens [Geary §6.5, p. 62]. Such lenses served photography for decades at apertures around F/11–F/16 and fields up to ±25°.

It is the perfect first project because a singlet has only three "knobs" — bending, stop position, focus — and each one has a clear physical role:

| Knob | Changes | Does not change |
|---|---|---|
| Bending (shape factor X) | spherical aberration, coma, astigmatism (through coma) | power, Petzval curvature |
| Stop position | coma, astigmatism, distortion, lateral colour | spherical aberration, axial colour, Petzval curvature, power |
| Focus | balances everything against defocus | — |

What *cannot* be fixed by any of these: **axial colour** (one glass, L05) and **Petzval curvature** (depends only on powers and indices, Course 02 L04). The landscape lens is thus a monochromatic or slow-aperture design — a lesson in working *with* an unfixable aberration.

---

## 2. Stop shift

### 2.1 Physical picture
Kidger's Fig. 6.5 [§6.3, pp. 115–116]: a lens transmits a fan of rays 1–4 from an off-axis point; the emerging wavefront has some shape. A stop at position "a" selects rays 1–3; at "b" it selects rays 2–4. The lens surfaces are untouched, but the *portion* of the aberrated wavefront that forms the image differs, so the off-axis aberrations differ. Two consequences [Kidger p. 116]:
1. If the system had **no** aberrations, moving the stop introduces none.
2. Moving the stop leaves the **marginal** (axial) ray untouched — so spherical aberration and axial colour are unchanged — while the **chief** ray now crosses each surface at a different height.

When you move the stop you must keep the system NA (or F/#) constant; unless the stop sits in collimated space, that means changing the stop diameter [Kidger p. 116]. In OpticStudio, keep the aperture type as *Entrance Pupil Diameter* or *Image Space F/#* (not Float By Stop Size) during a stop-shift study.

### 2.2 The Seidel stop-shift relations
Let $S_I \dots S_V$ be the Seidel sums (spherical, coma, astigmatism, Petzval, distortion) and $C_I, C_{II}$ the axial and lateral colour sums. Moving the stop changes the chief-ray height at every surface by an amount proportional to the marginal-ray height there; call the proportionality constant $\bar q$ (Kidger writes it as $H\Delta E$). Then [Kidger Eqs. 6.63–6.70, pp. 118–120]:

$$
\begin{aligned}
S_I^* &= S_I \\
S_{II}^* &= S_{II} + \bar q\, S_I \\
S_{III}^* &= S_{III} + 2\bar q\, S_{II} + \bar q^{\,2} S_I \\
S_{IV}^* &= S_{IV} \\
S_V^* &= S_V + \bar q\,(3S_{III} + S_{IV}) + 3\bar q^{\,2} S_{II} + \bar q^{\,3} S_I \\
C_I^* &= C_I, \qquad C_{II}^* = C_{II} + \bar q\, C_I .
\end{aligned}
$$

These are exact within third-order theory (not limited to small shifts) and hold for aspheric surfaces too [Kidger p. 120]. Read them like this:
- **Coma is linear** in stop position: as long as $S_I \ne 0$ there is a stop position where coma is zero — Geary's Fig. 6.7 shows COMA crossing zero linearly [Geary §6.3, pp. 59–60].
- **Astigmatism is quadratic** in stop position, with its extremum where $S_{II}^* = 0$ (minimize $S_{III}^*$ over $\bar q$: $dS_{III}^*/d\bar q = 2S_{II} + 2\bar q S_I = 2S_{II}^* = 0$). Hence "astigmatism goes through a minimum at about the same place where coma is zero" [Geary p. 60].
- **Lateral colour of a thin lens away from the stop** is $C_{II} \propto \bar y\, y\,K/V$: zero at the stop, growing with chief-ray height [Kidger Eq. 7.37, p. 157].
- The sign of the needed $\bar q$ (stop in front of or behind the lens) depends on the bending — which is why there are *two* landscape forms.

### 2.3 Field curvature: the part you cannot remove
A singlet's Petzval curvature is $1/R_P = -\phi/n$ (in air), i.e. the Petzval surface has radius $R_P = -nf$: for $f = 100$ mm N-BK7, $R_P \approx -152$ mm. At a 15° field (image height 26.8 mm) the Petzval surface lies $26.8^2/(2 \times 152) \approx 2.4$ mm in front of the flat image plane. Bending and stop shift cannot change that. The landscape trick is to introduce **astigmatism of the opposite sign** so that the tangential (or medial) image surface is bent back towards the flat film, accepting some astigmatic blur that is small at F/15. This is "artificial field flattening"; the proper cure (a negative element / field flattener) is in Course 02 L04.

---

## 3. Two landscape forms

```
 Rear landscape (Wollaston)                 Front landscape (Chevalier type)
   stop     meniscus                          meniscus    stop
    |       ((        ---->  image             ))         |      ---->  image
    |  d    concave towards stop               convex to   d
                                               the object
```

- **Rear landscape** (Geary's naming: the lens is at the *rear*, stop in front): the meniscus is **concave towards the stop** (both radii negative in our convention). Geary's WOLR runs [§6.3–6.4, pp. 58–62]: at a small field the optimizer keeps a near-equiconvex lens; when the field grows to 25° the optimum becomes the classical meniscus (Fig. 6.9).
- **Front landscape**: the lens is in front, the stop behind it; the meniscus is **convex towards the object** (both radii positive). Geary's homework (EFL 100, F/15, ±15°, d-light, BK7): target RMS spots with best focus ≈ 18 / 12 / 20 µm at 0 / 10.5 / 15° [Geary §6.6, pp. 62–64]. With the stop behind the lens its diameter must change as the stop moves to keep F/15 — so define the aperture by the entrance pupil (or F-number), not by the stop size, and constrain the stop distance (MNCA/MXCA) so the optimizer cannot slide back to the rear-landscape solution [Geary p. 64].

### 3.1 Local minima are real here
Bending passes through flat surfaces (curvature 0) and changes sign; the landscape problem has at least two valleys (plano-convex-like and meniscus-like). A Python model of the rear landscape (F/15, ±15°, d-light, 5 mm N-BK7, focus free) shows:
- starting from the **equiconvex** lens, local optimization converges to a **plano-convex** lens (flat side towards the stop, R₁ → ∞, R₂ ≈ −51.7 mm, stop ≈ 30 mm in front) with field RMS ≈ 27 / 3 / 27 µm (MF ≈ 22 µm);
- starting from a **meniscus** (e.g. R₁ = −40 mm, stop 15 mm in front), it converges to R₁ ≈ −84 mm, R₂ ≈ −32.7 mm, stop ≈ 19 mm in front, with RMS ≈ 14 / 9 / 19 µm (MF ≈ 15 µm) — the classical Wollaston meniscus, clearly better.

Same merit function, same variables, different answer: the starting point chooses the valley (Geary Fig. 8.4 and his remark that "starting points also matter" [§6.4, p. 61]).

---

## 4. Lens splitting

Spherical aberration of a thin lens at a given bending scales as $S_I \propto h^4K^3$ [Kidger Eq. 7.26, p. 156]. Replace one lens of power $K$ by $k$ lenses of power $K/k$ (same $h$):

$$
S_I \propto k\,h^4\left(\frac{K}{k}\right)^3 = \frac{h^4K^3}{k^2},
$$

a factor 4 for two elements and 9 for three [Kidger Eq. 7.36, p. 156]. Physically: each surface bends the rays less, angles of incidence shrink, and Snell's $\sin I - I$ nonlinearity (L01) falls off much faster than linearly. Geary's numbers for a 100 mm F/4 BK7 lens (7 mm elements, 1 mm gaps, EFFL + SPHA merit function): $W_{040}$ = 9.64 → 2.04 → 0.514 waves [Geary §9.2, pp. 95–97] — ×4.7 and ×4. The optimizer also **redistributes power**: the front element becomes weakest, the last strongest, and the shapes evolve from biconvex at the front to meniscus (bent towards the image) at the back [Geary pp. 96–97]. Geary's Table 9.1 shows why: after optimization the glass-to-air surfaces carry much smaller angles of incidence.

Lens splitting is everywhere in high-performance optics: lithography lenses (dozens of gently curved elements, Geary Fig. 9.5), Fizeau transmission spheres (Geary §9.4–9.5), fast camera and projector lenses. For a Zivid-type projector lens at F/2, splitting the positive power over several elements is a standard first move before reaching for an asphere.

---

## 5. In OpticStudio — project workflow

1. **Monitor operands.** Put `SPHA`, `COMA`, `ASTI`, `FCUR`, `DIST` (surface 0 = system total; wavelength = primary) at the top of the MFE with weight 0, plus `EFFL` (weight 0 when an F-number solve holds EFL). Their values are in waves (Seidel wavefront coefficients). Keep them throughout the project — they make stop-shift trends visible.
2. **Stop as a dummy surface.** Insert a flat surface in front of the lens, *Make Surface Stop*, give it the stop distance as thickness. For the front landscape put the dummy stop after the lens.
3. **Aperture type.** Entrance Pupil Diameter = EFL/15 = 6.667 mm works for both forms: for the rear landscape the stop *is* the EP; for the front landscape OpticStudio images the stop forward to locate the EP and resizes the stop automatically as it moves. (Image Space F/# = 15 is an alternative, but then an F-number solve on $R_2$ is degenerate — use an `EFFL` operand instead.) Avoid Float By Stop Size during stop-shift studies.
4. **Semi-diameters floating** (automatic) during optimization [Geary p. 59]; "square up" at the end (both faces of the lens same diameter) [Geary §6.6 practical note, p. 64].
5. **Variables:** $R_1$, stop distance, back focus (last thickness). $R_2$ by F-number solve. Later free $R_2$ and use `EFFL` instead, to see the difference.
6. **Merit function:** default RMS spot, centroid, Gaussian quadrature (3–4 rings, 6 arms), fields 0/10.5/15°, d-light; glass boundaries (min 2, max 8, edge 1); air bounds on the stop distance (`MNCA`/`MXCA` or the wizard's air settings).
7. **Optimize** (DLS, Automatic), then **analyze**: Cross-Section, Ray Fan, Spot (with Airy circle), Field Curvature/Distortion, Seidel Diagram (preview of Course 02).
8. **Version control:** `L08_WOLR_o01b.zmx` / `..._o01a.zmx` or git commits per step; write what changed in `notes.md` [Geary §2.6].

---

## Worked example — stop-shift scan of the equiconvex lens

Spec for the project: EFL = 100 mm, **F/15** (EPD 6.667 mm), fields 0, 10.5, 15°, d-light, N-BK7, centre thickness 5 mm, flat image, focus free. Start: equiconvex, $R_1 = 103.36$, $R_2$ by F/15 solve (−101.66 mm, EFL = 100.00).

**Stop at the lens.** At the paraxial focus the RMS spots are 3 / 111 / 229 µm (0 / 10.5 / 15°): on axis F/15 is nearly harmless (spherical ∝ $h^3$), off-axis is terrible. With the best flat focus (≈ 4.5 mm towards the lens — that's the Petzval/astigmatic field curvature pulling the compromise focus inwards) the spots are 103 / 38 / 126 µm.

**Stop in front, scanned** (focus re-optimized at each step, Python model, GQ 4 rings × 8 arms):

| Stop distance (mm) | Best-focus shift (mm) | RMS 0° / 10.5° / 15° (µm) | Field MF (µm) |
|---|---|---|---|
| 0.5 | −4.49 | 103 / 38 / 126 | 96.5 |
| 10 | −3.71 | 85 / 29 / 101 | 77.9 |
| 20 | −3.16 | 72 / 22 / 83 | 64.7 |
| 30 | −2.86 | 65 / 19 / 74 | 57.7 |
| 40 | −2.81 | 64 / 18 / 73 | 56.7 |
| 60 | −3.50 | 80 / 26 / 96 | 73.7 |

The optimum stop distance for *this* bending is ≈ 35–40 mm, where coma vanishes and astigmatism is smallest — the same behaviour as Geary's Fig. 6.7 (his 400 mm F/10 lens has its coma zero near 160 mm). Note the on-axis spot gets *worse* at large stop distances in this table only because the focus is a compromise over the field.

**Then bend + shift together** (variables $R_1$, stop distance, focus): the Wollaston meniscus ($R_1 \approx -84$, $R_2 \approx -32.7$ mm, stop ≈ 19 mm in front) reaches ≈ 14 / 9 / 19 µm — a 4× improvement over the best equiconvex stop shift and comparable to the F/15 Airy radius (1.22 λN = 10.8 µm). The front-landscape form reaches ≈ 17 / 12 / 20 µm with $R_1 \approx 18.6$, $R_2 \approx 26.4$ mm, stop ≈ 10 mm behind the lens — matching Geary's homework targets (18 / 12 / 20 µm).

**Colour reality check.** In white light (F, d, C) the singlet's axial colour (Δf ≈ 1.54 mm) gives a blur diameter of about $1.54/(2 \times 15) \approx 0.05$ mm at F/15 — larger than all the monochromatic residuals above. Historic landscape lenses lived with this (and later became achromatized: the Chevalier lens, Geary §19.5). You'll fix it in Course 02.

---

## Key takeaways
- Stop shift changes off-axis aberrations only: coma linearly, astigmatism quadratically (minimum where coma is zero), distortion cubically, lateral colour linearly; spherical, axial colour and Petzval are untouched.
- Bending + stop shift + focus are the three knobs of a singlet; together they produce the landscape lens with spots near the diffraction limit at F/15 over ±15° (monochromatic).
- Petzval curvature of a singlet ($R_P = -nf$) cannot be removed by bending or stop shift; landscape lenses trade it against deliberate astigmatism.
- The landscape problem has multiple local minima; the starting shape chooses the solution.
- Lens splitting reduces spherical aberration roughly as $1/k^2$ for $k$ elements; optimized splits redistribute power (front weaker) and reduce angles of incidence.
- Good project hygiene: monitor Seidel operands at weight 0, float semi-diameters, constrain spacings, version every optimization.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Landscape lens | Single meniscus lens with a separated stop, for moderate fields at small aperture |
| Rear / front landscape | Stop in front of / behind the lens |
| Stop shift | Moving the aperture stop along the axis at constant NA |
| Stop-shift equations | Seidel relations giving the change of off-axis aberrations with stop position |
| Petzval surface | Image surface of a system free of astigmatism; radius $-nf$ for a singlet |
| Artificial field flattening | Using astigmatism to bend the tangential/medial surface towards a flat image |
| Lens splitting | Replacing one element by several of lower power |
| Seidel operands | SPHA, COMA, ASTI, FCUR, DIST (waves) |
| Squaring up | Making semi-diameters consistent for manufacture after optimization |

## References
1. [Geary §6.3–6.6, pp. 58–64] Geary, *Introduction to Lens Design*: stop shifting and aberration control, Wollaston rear landscape lens, history, front landscape homework.
2. [Geary Ch. 9, pp. 95–101] lens splitting (single, double, triple elements), micro-lithography, Fizeau interferometry and transmission-sphere homework.
3. [Geary Ch. 8, Fig. 8.4, p. 89] local vs. global minima.
4. [Kidger §6.3, pp. 115–120] Kidger, *Fundamental Optical Design*: stop-shift effects and Seidel stop-shift equations.
5. [Kidger §7.3.5–7.3.6, pp. 156–157] splitting lenses; thin lens not at the stop, lateral colour.
6. Ansys Optics, "How to design a singlet lens – Part 3: Optimization" (variables, Optimization Wizard and boundary values used throughout the project): https://optics.ansys.com/hc/en-us/articles/42661700528275
