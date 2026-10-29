# L03 — Coma, Astigmatism and the Symmetry Principle

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~4–5 h
> **Prerequisites:** [L01](../L01-wavefront-and-transverse-aberrations/), [L02](../L02-spherical-aberration-and-bending/); Course 01 [L08 landscape lens](../../01-foundations/L08-landscape-lens-stop-shift-and-splitting/) · **Next:** [L04 — Field curvature, Petzval and flatteners](../L04-field-curvature-petzval-flatteners/)

## Learning objectives
- Describe the image-plane signatures of coma (comatic circles, 60° flare, tangential = 3 × sagittal) and astigmatism (two focal lines, medial focus), and recognise them in ray fans, spot diagrams and Field Curvature plots.
- Compute thin-lens coma and astigmatism for a lens at the stop and find the coma-free bending.
- Derive and apply the Seidel **stop-shift equations**, and use them to find the "natural" (coma-free) stop position and the resulting astigmatism.
- Explain why astigmatism of a thin lens at the stop is shape-independent and can only be controlled by stop position (or by several separated elements).
- Explain the **symmetry principle** (odd aberrations cancel in a symmetric system at unit magnification) and use it to design a periscopic lens in OpticStudio.
- Estimate at what field angle astigmatism overtakes coma for a given F/#.

## Reading
- **Core:** [Kidger §6.2.2, pp. 107–108] — off-axis Seidel surface formulas.
- **Core:** [Kidger §6.3–6.3.1, pp. 115–120] — stop-shift effects and their derivation (Kidger uses the "eccentricity" $E$; we use the equivalent $\chi$ below).
- **Core:** [Kidger §7.2.2–7.2.3 and §7.3.2–7.3.3, pp. 142–145, 152–154] — thin-lens coma and astigmatism, their correction.
- **Core:** [Kidger §7.7.2, pp. 165–166] — front-to-back symmetry.
- **Core:** [Geary Ch. 13, pp. 147–156] — coma and astigmatism from Seidel sums and thin-lens form, coma vs bending, coma vs astigmatism as a function of F/# and field.
- **Core:** [Geary Ch. 12, pp. 135–145] — the periscopic lens step by step in ZEMAX (Task 3 follows it).
- **Optional:** [Kidger §4.4.2.2–4.4.2.3, pp. 76–79] — wavefront pictures and through-focus spots for coma and astigmatism.

---

## 1. Coma

### 1.1 What it looks like
Coma is the term $W_{131}H\rho^3\cos\theta$: linear in field, cubic in aperture, odd in the meridional pupil coordinate. Physically, different annular zones of the pupil have slightly different **magnification**: each zone of radius $\rho$ images the point as a small circle (the *comatic circle*) whose radius grows as $\rho^2$ and whose centre is displaced from the chief-ray image by an amount also $\propto\rho^2$. Superimpose the circles from all zones and you get the characteristic comet: a bright head at the chief ray and a flare enclosed by two lines at ±30° from the meridional direction (a 60° wedge).

Differentiating the wavefront (L01 §3) gives, at full aperture and field:

$$
\varepsilon_y^{\text{tan}} = \frac{3S_{II}}{2n'u'} \quad\text{(tangential coma, length of the comet)},\qquad
\varepsilon_y^{\text{sag}} = \frac{S_{II}}{2n'u'}\quad\text{(sagittal coma)}.
$$

So **tangential coma is three times sagittal coma** [Kidger Eq. 6.89; OpticStudio's TTCO and TSCO columns]. In the ray fan:
- tangential fan $\varepsilon_y(P_y)$: a **parabola** ($\propto P_y^2$) — both edge rays land on the same side;
- sagittal fan: $\varepsilon_x(P_x) = 0$ — but the sagittal rays still have $\varepsilon_y \ne 0$ (which the standard sagittal ray fan, plotting only $\varepsilon_x$, does not show!). Don't be fooled by a "flat" sagittal fan.

Coma is the most important off-axis aberration at **small** fields because it is the only one linear in $H$ [Kidger §4.4.2.2, p. 77]. It is also very visible: the asymmetric flare shifts the **centroid** away from the chief ray, which biases any measurement based on spot centroids — a direct problem in metrology and structured-light triangulation, where you measure feature positions to sub-pixel precision.

### 1.2 Coma and the sine condition
Abbe's **sine condition** says that for an on-axis-corrected system to be free of coma for small fields, $n\sin U/(n'\sin U')$ must equal the paraxial magnification for every zone; for an object at infinity, $y/\sin U' = f$ for all ray heights [Geary §7.6, p. 83; Kidger §7.6]. Coma is the "offence against the sine condition" (OSC). An aplanat is a lens corrected for spherical aberration *and* satisfying the sine condition (L06). The OSC is a quick real-ray diagnostic: trace a marginal ray, compare $y/\sin U'$ with the EFL.

### 1.3 Coma of a thin lens at the stop
For a thin lens at the stop [Kidger Eq. 7.6]:

$$
S_{II} = -\frac{h^2K^2H}{2}\left[\frac{(n+1)B}{n(n-1)} + \frac{(2n+1)C}{n}\right],
$$

with $h$ = marginal height, $K$ = power, $H$ = Lagrange invariant, $B$ and $C$ = shape and conjugate factors (L02). Coma is **linear** in $B$, so there is always a coma-free bending:

$$
B_{\text{coma}=0} = -\frac{(2n+1)(n-1)}{n+1}\,C .
$$

For N-BK7 ($n = 1.5168$), object at infinity ($C=-1$): $B = 0.8283$ [Geary §13.4, p. 154 gets the same number]. Compare $B = 0.7397$ for minimum spherical: **the best-form singlet is very nearly coma-free** — that's why plano-convex/best-form lenses at the stop are good small-field objectives.

At $C = 0$ (1:1 imaging) the coma-free shape is $B=0$ (equiconvex) — a first hint of the symmetry principle.

## 2. Astigmatism

### 2.1 What it looks like
Astigmatism $W_{222}H^2\rho^2\cos^2\theta$ is a defocus that exists only in the tangential section. An off-axis beam therefore has two line foci [Kidger §4.4.2.3, pp. 77–79]:
- the **tangential (T) focus**: a line perpendicular to the meridional plane (rays in the tangential fan converge, sagittal ones don't yet);
- the **sagittal (S) focus**: a line in the meridional (radial) direction;
- between them a circular blur (the "medial" focus).

In the ray fans: both fans are straight lines through the origin with **different slopes**. In OpticStudio's **Field Curvature** plot you see two curves (T and S) versus field; their separation is the astigmatism and their average curvature is the field curvature (L04).

Longitudinal positions relative to the paraxial image plane (object at infinity, air):

$$
\delta z_T = -\frac{3S_{III}+S_{IV}}{2n'u'^2},\qquad \delta z_S = -\frac{S_{III}+S_{IV}}{2n'u'^2},
\qquad \delta z_T - \delta z_S = -\frac{S_{III}}{n'u'^2}.
$$

### 2.2 Astigmatism of a thin lens at the stop is fixed
For a thin lens at the stop, the chief ray passes through the centre, and the result is remarkably simple [Kidger Eqs. 7.10, 7.12]:

$$
S_{III} = H^2K,\qquad S_{IV} = \frac{H^2K}{n},\qquad S_V = 0 .
$$

Neither depends on the shape! **No amount of bending changes the astigmatism of a thin lens at the stop**, and adding more thin lenses at the stop just adds up their powers: $S_{III} = H^2\sum K_i$. A positive system with all lenses near the stop has inward-curving, astigmatic fields — you need **stop position** (stop shift) or **separated** positive and negative elements to control astigmatism. This is one of the deepest structural facts in lens design: it explains landscape lenses, symmetrical lenses, the Cooke triplet (L09) and why fast wide-angle lenses are long.

### 2.3 Coma vs astigmatism: which dominates?
With the stop at the lens and object at infinity, $W_{131} \propto \sigma_{II}/N^3 \cdot \bar u$ and $W_{222} \propto \bar u^2/N^2$ (Geary's "difference factor" analysis, §13.5). For a plano-convex lens the two are equal at roughly

$$
\bar u \approx \frac{\sigma_{II}}{4N},\qquad \sigma_{II} = \frac{n+1}{n(n-1)}B + \frac{2n+1}{n}C
$$

— for N-BK7 PC ($\sigma_{II} = 0.551$) at F/5 that's $\bar u\approx 0.028$ rad ≈ 1.6°; at F/10 ≈ 0.8°. (Checked against an exact Seidel computation.) Beyond a degree or two of field, **astigmatism**, not coma, is what limits a singlet. Fast lenses (low $N$) push the crossover outward — coma dominates longer in fast systems.

## 3. Stop shift

### 3.1 The stop-shift equations
Move the stop along the axis while keeping the marginal ray (the F/#) unchanged. The chief ray changes: at every surface its height changes by an amount proportional to the marginal ray height,

$$
\bar y^{*} = \bar y + \chi\,y,\qquad \chi = \text{same constant at all surfaces}
$$

(because both rays obey the same linear transfer and refraction equations — any linear combination of solutions is a solution). Consequently $\bar A^{*} = \bar A + \chi A$ at every surface, and substituting into the Seidel formulas gives [Kidger Eqs. 6.63–6.70, with $\chi = H\Delta E$]:

$$
\begin{aligned}
S_I^* &= S_I\\
S_{II}^* &= S_{II} + \chi S_I\\
S_{III}^* &= S_{III} + 2\chi S_{II} + \chi^2 S_I\\
S_{IV}^* &= S_{IV}\\
S_V^* &= S_V + \chi(3S_{III}+S_{IV}) + 3\chi^2S_{II} + \chi^3 S_I\\
C_L^* &= C_L,\qquad C_T^* = C_T + \chi C_L
\end{aligned}
$$

These are exact within third-order theory, valid for whole systems as well as single surfaces, and also hold for aspheres [Kidger §6.3.1, p. 120].

How to get $\chi$: if the stop is moved to a plane where the marginal-ray height is $y_s$ and the old chief ray had height $\bar y_s$ there, the new chief ray must pass through the centre of the new stop: $0 = \bar y_s + \chi y_s$ → $\chi = -\bar y_s/y_s$. For an object at infinity and a thin lens, moving the stop a distance $d$ **in front** of the lens gives $\bar y_{\text{lens}} = \bar u\,d$, i.e. $\chi = \bar u d/y$.

### 3.2 What the equations tell you
1. **If a system is free of a given aberration and all "lower" ones, a stop shift can't introduce it.** A system with $S_I = 0$ has stop-independent coma; with $S_I = S_{II} = 0$, stop-independent astigmatism; corrected axial colour → stop-independent lateral colour [Kidger §7.3.1.6, p. 152].
2. **Spherical aberration is the lever for coma** (and coma for astigmatism): an *uncorrected* $S_I$ lets you choose coma at will by moving the stop. That's the trick of the landscape lens (Course 01 L08).
3. **The natural stop position** $\chi_0 = -S_{II}/S_I$ makes coma zero, and there the astigmatism takes its minimum-possible value for that lens:

$$
S_{III}^{*}\big|_{\text{coma}=0} = S_{III} - \frac{S_{II}^2}{S_I} = \frac{S_IS_{III}-S_{II}^2}{S_I}.
$$

The combination $S_IS_{III} - S_{II}^2$ is **invariant under stop shift**; bending the lens changes it. So the design problem for a single-element lens with a remote stop becomes: choose the bending so that the coma-free stop position also gives the astigmatism you want (e.g. flat tangential field $3S_{III}^*+S_{IV}=0$, or $S_{III}^*=0$).
4. **Distortion appears** when the stop moves away from the lens ($S_V^*$ picks up $\chi(3S_{III}+S_{IV})$): stop in front of a positive lens → **barrel**, behind → **pincushion** (L05).

## 4. The symmetry principle

If a system is mirror-symmetric about its stop and works at unit magnification ($m=-1$), every ray through the front half has a mirror-image partner in the back half; their optical paths are identical, so the wavefront can only contain terms **even** in the pupil coordinate [Kidger §7.7.2, pp. 165–166]. All **odd** aberrations — **coma, distortion and lateral colour** — vanish identically, to all orders. Spherical aberration, astigmatism, field curvature and axial colour of the two halves *add*.

At other magnifications the cancellation is imperfect but usually still substantial, and a small asymmetry fixes the remainder. This is why so many classic designs are (nearly) symmetric: the **periscopic lens** (Steinheil, 1865 — two meniscus singlets around a central stop) [Geary Ch. 12], the Rapid Rectilinear, Dagor, double Gauss (L10), and many 1:1 relay and copy lenses. In machine vision, **near-symmetric** designs are common for finite-conjugate lenses (macro lenses, line-scan lenses at 0.2–1× magnification) because they give low distortion "for free".

Practical OpticStudio idiom: enforce symmetry with **pickup solves** (radius of surface *k* = −1 × radius of its mirror surface; thickness pickups for the air spaces), vary only the front half, and constrain magnification with PMAG. Geary's periscopic walk-through does exactly this, then shows that **breaking** the symmetry (unslaving everything) for an object at infinity improves RMS spot sizes from ~40–70 µm to < 10 µm in his example [Geary §12.7, p. 143]. Symmetry is a starting point, not a religion.

## 5. In OpticStudio

- **Stop position.** In the Lens Data Editor, any surface can be made the stop (Surface Properties → Type → "Make Surface Stop", or the STOP column/flag, depending on version). To scan stop position, insert a dummy plane surface for the stop and vary the thicknesses before/after it with a pickup or a fixed sum (e.g. thickness before = variable, thickness after = solve "pickup" with scale −1 plus offset, or simply keep total length constant manually). Keep **System Aperture = Entrance Pupil Diameter or Image Space F/#** so the marginal ray stays the same while you move the stop — "Float by Stop Size" would change the F/#.
- **Seidel Coefficients / Seidel Diagram:** watch COMA (S2) and ASTI (S3) as you move the stop; check the stop-shift equations with the numbers. The transverse table gives TSCO/TTCO (sagittal/tangential coma) and the longitudinal table LSFC/LTFC-type field-curvature terms (column names vary slightly by version).
- **Ray Fan** at full field: tangential parabola = coma; different T/S slopes = astigmatism. Use **Spot Diagram** with the *chief ray* reference to see the comet tail clearly; the *centroid* reference hides the coma offset.
- **Field Curvature/Distortion**: T and S curves; their difference is astigmatism.
- **Through-focus spots** (Spot Diagram → Through Focus, or *Analyze → Rays & Spots → Through Focus Spot*): look for the two line foci.
- Operands: **COMA**, **ASTI** (Seidel, by surface or summed with Surf = 0), **FCGT / FCGS** (real-ray tangential/sagittal field curvature at a given field — Geary uses them in §12.5), **PMAG** (paraxial magnification), **EFFL**. Always confirm units by comparing an operand value with the Seidel report.

## Worked example — a thin N-BK7 singlet, then a landscape stop shift

**Given:** thin N-BK7 lens ($n=1.5168$), $f=100$ mm, F/10 ($h = 5$ mm, $u' = -0.05$), semi-field 10° ($\bar u = 0.17633$), object at infinity, λ = 587.6 nm. Lagrange invariant $H = n(u\bar y - \bar u y) = -\bar u h = -0.8816$ mm.

**(a) Stop at the lens.** From Kidger's formulas (and confirmed by exact paraxial Seidel sums with `seidel.py` with $t\to0$):

| Shape $B$ | $S_I$ (mm) | $S_{II}$ (mm) | $S_{III} = H^2K$ | $S_{IV} = H^2K/n$ |
|---|---|---|---|---|
| −1 (flat side first) | 0.005384 | −0.006469 | 0.007773 | 0.005124 |
| 0 (equiconvex) | 0.002021 | −0.002931 | 0.007773 | 0.005124 |
| 0.7397 (min SA) | 0.001279 | −0.000313 | 0.007773 | 0.005124 |
| **0.8283 (zero coma)** | 0.001289 | **0** | 0.007773 | 0.005124 |
| 1 (plano-convex) | 0.001370 | +0.000608 | 0.007773 | 0.005124 |

Note how $S_{III}$ and $S_{IV}$ don't change at all. Tangential field: $\delta z_T = -(3S_{III}+S_{IV})/(2u'^2) = -0.02844/0.005 = -5.69$ mm; sagittal $\delta z_S = -0.01290/0.005 = -2.58$ mm (both toward the lens). At F/10 the depth of focus is only $\pm 2\lambda N^2 \approx \pm0.12$ mm — the 10° image is hopelessly blurred by field curvature and astigmatism, even though the axis is fine.

**(b) Meniscus with a remote stop (rear landscape lens).** Bend to $B = -3$ (meniscus concave toward the object: R1 = −51.68 mm, R2 = −25.84 mm) and keep the stop at the lens: $S_I = 0.02025$, much worse spherical (4.3 waves at F/10), but spherical aberration is what lets a stop shift control coma. Natural stop position: $\chi_0 = -S_{II}/S_I = 0.669$, i.e. the stop sits $d = \chi_0 h/\bar u = 18.97$ mm in front of the lens. There:

$$
S_{II}^* = 0,\quad S_{III}^* = -0.001289,\quad S_{IV} = 0.005124,\quad S_V^* = +0.0069 .
$$

Tangential field $\delta z_T = -(3S^*_{III}+S_{IV})/(2u'^2) = -0.25$ mm (23× flatter than in (a)); sagittal $\delta z_S = -0.77$ mm. Distortion: $S_V^*/(2H) = 0.0069/(2\times-0.8816) = -0.39\%$ (**barrel**, as expected for a front stop).

**(c) A limit of the single lens.** Scanning $B$ from −1 to −50 in this thin-lens model, the ratio $S_{III}^*/S_{IV}$ at the coma-free stop never gets below about −0.30, so a *perfectly* flat tangential field ($S_{III}^* = -S_{IV}/3$) with zero coma is just out of reach for $n = 1.517$; real landscape lenses accept a little coma or use lens thickness (which the thin model ignores) to get there. Exactly the kind of insight a 20-line Python script gives you before you touch the optimizer.

## Key takeaways
- Coma ($\propto H\rho^3$) gives a 60° comet; tangential coma = 3 × sagittal coma; it shifts the centroid — bad for metrology.
- Coma of a thin lens is linear in bending; zero at $B = 0.83$ for BK7 at infinity, close to the minimum-spherical shape.
- Astigmatism and Petzval of a thin lens at the stop are **shape-independent**: $S_{III}=H^2K$, $S_{IV}=H^2K/n$.
- Stop shift: $S_{II}^* = S_{II}+\chi S_I$, $S_{III}^* = S_{III}+2\chi S_{II}+\chi^2S_I$; uncorrected spherical is the lever. At the natural stop, $S_{III}^* = (S_IS_{III}-S_{II}^2)/S_I$.
- Corrected aberrations are stop-shift invariant; a remote stop introduces distortion (front stop → barrel).
- Symmetric systems at 1:1 have zero coma, distortion and lateral colour; near-symmetry is a powerful starting point, but break it for infinite conjugates.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Comatic circle / flare | Image of one pupil zone under coma; the superposition forms a 60° comet |
| Tangential / sagittal coma | Length of the comet / radius offset of the sagittal ray pair; ratio 3:1 |
| Sine condition, OSC | $y/\sin U' = f$ for all zones (object at ∞); offence against it measures coma |
| Tangential / sagittal focus | Line foci of an astigmatic off-axis beam |
| Medial focus | Midway between T and S foci; circular blur |
| Stop shift, $\chi$ | Moving the stop at constant F/#; $\bar y^* = \bar y + \chi y$ at every surface |
| Natural stop position | Stop location giving zero coma, $\chi_0 = -S_{II}/S_I$ |
| Symmetry principle | Mirror symmetry about the stop at $m=-1$ cancels odd aberrations |
| Periscopic lens | Two meniscus singlets symmetric about a central stop (Steinheil 1865) |

## References
1. [Kidger] §4.4.2.2–4.4.2.3 pp. 76–79; §6.2.2 pp. 107–108; §6.3–6.3.1 pp. 115–120; §7.2.2–7.2.3 pp. 142–145; §7.3.1.6–7.3.3 pp. 152–154; §7.6 pp. 162–164; §7.7.2 pp. 165–166.
2. [Geary] §7.6 p. 83; Ch. 12 "Symmetry and the Periscopic Lens" pp. 135–145; Ch. 13 "Coma and Astigmatism" pp. 147–156.
3. J. Sasián, OPTI 517 "Aberration coefficients" (stop-shift relations in $W_{klm}$ form): <https://wp.optics.arizona.edu/jsasian/wp-content/uploads/sites/33/2016/02/L4-OPTI-517-Aberration-Coefficients.pdf>
