# L04 — Field Curvature, the Petzval Sum and Field Flatteners

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~4 h
> **Prerequisites:** [L01](../L01-wavefront-and-transverse-aberrations/)–[L03](../L03-coma-astigmatism-and-symmetry/) · **Next:** [L05 — Distortion](../L05-distortion/)

## Learning objectives
- Explain the Petzval surface physically (the concentric-stop mirror/ball lens picture) and compute the Petzval sum $P = \sum K_i/n_i$ and Petzval radius for a system of thin lenses.
- Relate $S_{III}$ and $S_{IV}$ to the sagittal, tangential and medial image surfaces ($PT = 3\,PS$) and choose an astigmatism balance (flat T, flat medial, crossing S/T) on purpose.
- Apply Coddington's equations to find the T and S foci along the chief ray, and explain what OpticStudio's **Field Curvature** plot actually computes.
- Explain the three ways to reduce the Petzval sum (index contrast, separated positive/negative lenses, thick meniscus) and design a thin field flattener.
- Translate a sensor depth-of-focus budget into a maximum permissible Petzval sum.
- Use FCUR/PETC/FCGT/FCGS-type operands and the Field Curvature plot in OpticStudio to control the image surface.

## Reading
- **Core:** [Kidger §6.9.3–6.9.4, pp. 132–135] — Petzval sum, Petzval surface, image-surface diagrams for various $S_{III}$, $S_{IV}$.
- **Core:** [Kidger §7.3.4, pp. 153–156] — the three ways to correct Petzval curvature.
- **Core:** [Geary Ch. 14, pp. 157–165] — Petzval wavefront coefficient, Petzval radius in ZEMAX, field-flattener theory.
- **Core:** [Geary Ch. 29, pp. 329–340] — Coddington's equations, oblique power, and how the ZEMAX field-curvature plot is computed (§29.9).
- **Optional:** [Geary Ch. 27, pp. 301–314] — relating defocus, astigmatism and field curvature in Cartesian pupil coordinates; image sizes at the T and S foci.
- **Optional:** [Kidger §4.4.3.3, pp. 85–86] — balancing higher-order astigmatism and field curvature.

---

## 1. The Petzval surface

Imagine a spherical mirror with the stop at its centre of curvature (Geary's Fig. 14.2). Every chief ray hits the mirror along a radius, so every off-axis beam sees exactly the same geometry as the on-axis beam: no coma, no astigmatism. But the focus for each field angle lies at distance $R/2$ along *its own* chief ray, so the images lie on a sphere of radius $R/2$ — concentric with the mirror. This curved image is the **Petzval surface**, and the mirror is the rare case where you can actually observe it [Geary §14.2, pp. 157–159]. The same picture applies to a glass ball lens with a central stop (the "monocentric" lens, Kidger §7.7.1, p. 165).

In general the Petzval curvature is a *property of the powers and indices alone*, independent of bending, stop position or spacing:

$$
S_{IV} = -H^2\sum_{\text{surfaces}} c\,\Delta\!\left(\frac1n\right),\qquad
P \equiv \frac{S_{IV}}{H^2} = \sum_{\text{surfaces}} c\left(\frac1n - \frac1{n'}\right) = \sum \frac{\phi_{\text{surf}}}{n\,n'} .
$$

For a thin lens in air, $P = K/n$; for several thin lenses, $P = \sum K_i/n_i$ [Kidger Eqs. 6.94, 7.31–7.32; Geary Eq. 14.5]. The Petzval surface has curvature $c_P = -P$ for an image in air, i.e. radius

$$
R_P = -\frac{1}{P}\quad(\text{image in air}),
$$

and the Seidel longitudinal departure of the Petzval surface from the paraxial plane at image height $h'$ is $\delta z_P = -S_{IV}/(2n'u'^2) = -h'^2P/2$ [Kidger Eq. 6.97]. A positive lens ($P > 0$) has $R_P < 0$: an image surface **concave toward the lens** (curving back toward it at the edge). OpticStudio prints the **Petzval radius** in the header of the Seidel Coefficients report — Geary verifies it by hand for his silica singlet (−71.54 cm) [Geary §14.6, pp. 161–162].

Why it matters: *you cannot bend, stop-shift, or aspherize your way out of Petzval curvature.* Only the arrangement of positive and negative powers (and indices) changes $P$. Every flat-field camera lens is, structurally, a negotiation between the positive power you need and the negative power you must add to cancel $P$.

## 2. Petzval, sagittal and tangential surfaces

Astigmatism splits the image into the T and S surfaces about the Petzval surface. From L01/L03 (object at infinity, image in air):

$$
\delta z_S = -\frac{S_{III}+S_{IV}}{2u'^2},\qquad
\delta z_T = -\frac{3S_{III}+S_{IV}}{2u'^2},\qquad
\delta z_P = -\frac{S_{IV}}{2u'^2}.
$$

So $\delta z_T - \delta z_P = 3(\delta z_S - \delta z_P)$: **the tangential surface is always three times as far from the Petzval surface as the sagittal surface, on the same side** ($PT = 3\,PS$) [Kidger Eq. 6.100]. Useful special cases [Kidger §6.9.4, pp. 133–134]:

| Choice of $S_{III}$ (given $S_{IV}>0$) | Result |
|---|---|
| $S_{III} = 0$ | S = T = P (curved, anastigmatic) |
| $S_{III} = -S_{IV}/3$ | **flat tangential** surface; S still curved inward |
| $S_{III} = -S_{IV}/2$ | **flat medial** surface: S and T symmetric about the image plane |
| $S_{III} = -S_{IV}$ | flat sagittal, T strongly curved (worst choice) |
| $S_{III} > 0$ (singlet, doublet) | both inward, T worse |

For third order alone, with $S_{IV}\neq0$ you can flatten one surface but not both. Real lenses with several separated elements use **fifth-order astigmatism** of opposite sign so that S and T curves bend back and **cross** at 0.7–0.85 of full field, leaving small residuals across the field [Kidger §6.9.4, p. 134; §4.4.3.3]. When you look at the Field Curvature plot of a good camera lens and see S and T curves wiggling around zero and crossing, that's what you're seeing — and the residual Petzval sum is small but not zero.

**Which surface should be flat?** Old practice flattened the tangential field [Geary §12.5]; Geary shows that this makes RMS spots worse than simply minimising RMS spot. Modern practice: optimise the image-quality metric (RMS spot/wavefront, or MTF at the relevant frequency, often split into sagittal and tangential MTF) and let the optimiser find the balance — but *know* which balance it chose, because S/T separation means **orientation-dependent resolution**: line patterns along the radial direction are imaged differently from tangential ones. For a structured-light system projecting stripes, this matters: stripes in one orientation will lose contrast faster toward the field edge.

## 3. Coddington's equations: what the Field Curvature plot really shows

Seidel theory gives the third-order positions. The exact positions of the T and S foci along a real chief ray come from **Coddington's equations**, a "paraxial optics around the chief ray". At a refracting surface with radius $R$, chief-ray incidence and refraction angles $I$, $I'$, and distances $t, t'$ (tangential) and $s, s'$ (sagittal) measured along the chief ray from the surface:

$$
\frac{n'\cos^2 I'}{t'} - \frac{n\cos^2 I}{t} = \frac{n'\cos I' - n\cos I}{R},\qquad
\frac{n'}{s'} - \frac{n}{s} = \frac{n'\cos I' - n\cos I}{R}.
$$

The right-hand side is the **oblique power** of the surface; the extra $\cos^2$ factors in the tangential equation are the root of astigmatism. For a thin lens at the stop and an object at infinity, Geary derives [Geary §29.4–29.6, pp. 331–334]

$$
\phi_{\text{obl}} = (n\cos U' - \cos U)(c_1-c_2),\qquad s' = \frac{1}{\phi_{\text{obl}}},\qquad t' = \frac{\cos^2 U}{\phi_{\text{obl}}},\qquad s' - t' = \frac{\sin^2U}{\phi_{\text{obl}}},
$$

with $U$ the field angle and $U'$ the internal chief-ray angle ($\sin U = n\sin U'$). Note these are *exact* for an infinitely narrow beam around the chief ray — there's no third-order approximation.

**OpticStudio's Field Curvature plot** is computed exactly this way: for each field, it traces real rays very close to the chief ray in the tangential and sagittal planes and finds where they cross; it then plots the distance of those crossings from the **paraxial image plane, measured along the optical axis** (not along the chief ray) [Geary §29.9, p. 335]. Consequences:
- The plot contains **all orders** of astigmatism and field curvature but **no aperture effects** — it's for a vanishingly small pupil around the chief ray. A lens with lots of oblique spherical or coma can have nice-looking field curves and still produce bad off-axis spots.
- It's relative to the **paraxial** image plane. If you've refocused (image distance not at the paraxial solve), the curves are referenced to the paraxial plane, not your detector — check the plot settings and remember to subtract your defocus mentally.

## 4. Reducing the Petzval sum

Kidger lists three structural techniques [Kidger §7.3.4.1–7.3.4.3]:

1. **Index contrast.** Positive lenses of high index, negative lenses of low index: $P = K_1/n_1 + K_2/n_2$ is reduced while the power $K_1 + K_2$ stays positive. Kidger's example: $K_1 = 4$, $n_1=1.8$; $K_2=-3$, $n_2=1.5$ → $P = 0.222$ vs 0.555 for a single $n=1.8$ lens of the same power. It requires strong elements, so alone it is rarely sufficient — but it is why modern camera lenses use **high-index lanthanum crowns for the positive elements** (N-LAK, N-LASF families) and lower-index glasses for negatives (and why the "new achromat" pairs in L06 have high-index crowns).
2. **Separated positive and negative lenses.** Two thin lenses $+K_1$ and $-K_1$ separated by $d$ have $P = 0$ but power $K = dK_1^2 > 0$, whichever comes first [Kidger Eq. 7.34]. The negative lens works where the marginal ray is low (little power penalty) and still subtracts its full $K/n$ from the Petzval sum. This is *the* mechanism of the Cooke triplet (L09), the Petzval lens with field flattener (L11), the telephoto and the retrofocus.
3. **Thick meniscus.** A meniscus with $c_1 = c_2$ has zero Petzval contribution (its surface powers cancel) but positive power $K = (n-1)^2dc_1^2/n$ [Kidger Eq. 7.35]. Double-Gauss inner menisci exploit this (L10).

### 4.1 The field flattener
The extreme form of technique 2: put a **negative lens at (or very near) the image**. There the marginal-ray height is ≈ 0, so the flattener adds almost no power, spherical aberration, coma or axial colour — but its Petzval contribution $K_{ff}/n_{ff}$ is undiminished, because Petzval doesn't depend on ray heights at all. To cancel a Petzval sum $P$:

$$
\frac{K_{ff}}{n_{ff}} = -P \quad\Longrightarrow\quad f_{ff} = -\frac{1}{n_{ff}P}.
$$

For a single lens of index $n$ and focal length $f$, a flattener of the **same glass** needs $f_{ff} = -f$. Geary develops the flattener from a different angle: a plano-concave plate whose thickness varies with height shifts the focus by $t(n-1)/n$, chosen to equal the Petzval sag at each height [Geary §14.7, pp. 163–165].

Side effects: the chief ray is high at the flattener, so it introduces **distortion and lateral colour**, and (being near focus) any dust, scratch or bubble on it is imaged sharply. In cameras, the sensor cover glass and filters also occupy the space just in front of the sensor, so a flattener usually sits a few mm in front and accepts some power penalty. Petzval portrait lenses (L11), and many projector and microscope designs use one; many mobile-phone lenses use a strongly aspheric last element that partly acts as a field flattener.

### 4.2 Curved image surfaces
If you control the detector, the alternative is to **curve the image surface** to match the field (photographic film in old box cameras was curved; Schmidt cameras use curved plates; research curved CMOS sensors exist). In OpticStudio you can give the image surface a radius and make it a variable — useful for diagnostics ("how good would this lens be if the field were allowed to curve?"), and occasionally a real design freedom (e.g. fibre bundles, some line-scan or scanning systems).

## 5. Depth of focus sets the field-curvature budget

A useful professional habit: convert your sensor and F/# into an allowed image-surface departure. The diffraction-based depth of focus (±¼ wave of defocus) is

$$
\Delta z = \pm 2\lambda N^2 .
$$

For a Zivid-style NIR receiver at 850 nm and F/2.8: $\Delta z = \pm 2(0.85)(2.8)^2 = \pm13$ µm. If the image half-diagonal is $h' = 5.5$ mm (2/3" sensor), a pure Petzval field must satisfy $h'^2|P|/2 < 13$ µm → $|P| < 8.8\times10^{-4}$ mm⁻¹, i.e. $|R_P| > 1.14$ m. For a 16 mm focal length lens that's $|P| f < 0.014$ — compared with $1/n \approx 0.66$ for a singlet. **A flat-field fast camera lens needs ~98% of its positive Petzval contribution cancelled by negative elements.** That single number explains why machine-vision lenses have 5–8 elements including strong negatives.

## 6. In OpticStudio

- **Seidel Coefficients:** FCUR (S4) per surface and sum; W220P (Petzval), W220S/M/T; the **Petzval radius** in the header.
- **Field Curvature/Distortion** analysis (*Analyze → Aberrations → Field Curvature and Distortion*, location varies by version): T and S curves vs field (real near-chief rays, Coddington-like, along the axis from the paraxial image plane). Use it with one wavelength first; then all wavelengths to see chromatic variation of field curvature.
- **Operands:** FCUR (Seidel S4/Petzval contribution; check units against the report), **PETC** (Petzval curvature in inverse lens units, as Geary uses in §12.3; PETC = 1/Petzval radius), **FCGT/FCGS** (real tangential/sagittal field-curvature at a specified field, Geary §12.5), and of course the default merit function. A Petzval-sum constraint (e.g. keep PETC within a band) is a classic way to stop an optimizer from producing a lens that looks good on axis but whose field you can never fix later.
- **Image surface curvature:** type a radius on the IMA surface (or make it variable) to see how much of the off-axis blur is "just" field curvature.
- **Pitfall:** the default merit function with a *flat* image will push S and T to straddle the image plane — the Field Curvature plot will show crossing curves, not zero curves. That's correct behaviour.

## Worked example — singlet field curves, Coddington check, and a flattener

**Given:** thin N-BK7 lens ($n=1.5168$), $f = 100$ mm, at the stop, F/10 ($h=5$ mm, $u'=-0.05$), object at infinity, semi-field 10° (image height $h' = 100\tan10° = 17.63$ mm), λ = 587.6 nm. From L03: $S_{III} = H^2K = 0.007773$ mm, $S_{IV} = H^2K/n = 0.005124$ mm.

**Seidel image surfaces** (from the paraxial plane, negative = toward the lens):
$\delta z_P = -S_{IV}/(2u'^2) = -1.025$ mm; $\delta z_S = -(S_{III}+S_{IV})/(2u'^2) = -2.58$ mm; $\delta z_T = -(3S_{III}+S_{IV})/(2u'^2) = -5.69$ mm. Check: $PT = 4.66$ mm $= 3\times PS = 3\times1.55$ mm ✓.

**Petzval radius:** $P = K/n = 0.01/1.5168 = 6.593\times10^{-3}$ mm⁻¹ → $R_P = -151.7$ mm. Sag at $h' = 17.63$ mm: $h'^2P/2 = 1.025$ mm ✓ (same as $\delta z_P$).

**Coddington (exact, thin lens at stop):** $\sin U' = \sin10°/1.5168 = 0.11448$, $\cos U' = 0.99343$. Oblique power factor $(n\cos U' - \cos U)/(n-1) = (1.50683 - 0.98481)/0.5168 = 1.0101$ → $s' = 99.00$ mm, $t' = s'\cos^2U = 96.01$ mm along the chief ray; $s'-t' = 2.99$ mm. Projected on the axis: S at $99.00\cos10° - 100 = -2.50$ mm, T at $-5.44$ mm. Compare Seidel: −2.58 and −5.69 mm — third order overestimates slightly; the remainder is higher-order astigmatism/field curvature.

**Flattener:** an N-BK7 thin lens of $f_{ff} = -100$ mm placed 95 mm behind the main lens (5 mm before the old focus) makes $P = 0.01/n - 0.01/n = 0$ exactly. The system power becomes $K = K_1 + K_2 - dK_1K_2 = 0.01 - 0.01 + 95\times10^{-4} = 0.0095$ mm⁻¹ ($f = 105.3$ mm) and the back focal distance 5.26 mm; the marginal ray is at only 5% of its height there, so the flattener adds little spherical aberration. But the chief ray at 10° is ≈ 16.8 mm high at the flattener — expect noticeable distortion and lateral colour. (Task 2 builds this in OpticStudio; the remaining astigmatism then has to be handled with the stop position, as in L03.)

## Key takeaways
- Petzval sum $P = \sum K_i/n_i$ (thin lenses) depends only on powers and indices; $R_P = -1/P$ in air. Bending, stop shift and aspheres cannot change it.
- T and S surfaces lie on the same side of the Petzval surface with $PT = 3PS$; flat T at $S_{III} = -S_{IV}/3$, flat medial at $-S_{IV}/2$.
- Coddington's equations give exact narrow-beam T/S foci along the chief ray; OpticStudio's Field Curvature plot uses this (no aperture effects; axial distance from the paraxial plane).
- Reduce $P$ with index contrast (high-index positives), separated positive/negative lenses, or thick menisci; a negative field flattener near the image cancels $P$ with almost no power penalty but adds distortion/lateral colour.
- Depth of focus $\pm2\lambda N^2$ sets the budget: a fast flat-field camera lens needs almost all of its Petzval sum cancelled.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Petzval sum $P$ | $\sum K_i/n_i$ (thin lenses); curvature of the Petzval surface is $-P$ (image in air) |
| Petzval surface / radius | Image surface in the absence of astigmatism; radius $R_P = -1/P$ |
| Tangential / sagittal image surface | Loci of T and S line foci vs field |
| Medial surface | Mean of S and T surfaces |
| Coddington's equations | Exact narrow-beam focusing equations for T and S fans along the chief ray |
| Oblique power | $(n'\cos I' - n\cos I)/R$; power of a surface for an oblique beam |
| Field flattener | Negative element near the image that cancels Petzval sum with little power |
| Anastigmat | Lens corrected for astigmatism with a reasonably flat field |

## References
1. [Kidger] §6.9.3–6.9.4 pp. 132–135; §7.3.4 pp. 153–156; §7.7.1 p. 165; §4.4.3.3 pp. 85–86.
2. [Geary] Ch. 12 §12.5 pp. 140–141; Ch. 14 pp. 157–165; Ch. 27 pp. 301–314; Ch. 29 pp. 329–340.
3. Ansys/Zemax community, "Any difference between FCGS/FCGT and the Field Curvature/Distortion analysis plot?" — how the operands relate to the plot: <https://community.zemax.com/people-pointers-9/any-difference-between-fcgs-fcgt-and-the-field-curvature-distortion-analysis-plot-2854>
