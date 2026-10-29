# L10 — Symmetric lenses, the Celor, the double Gauss and deliberate vignetting

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~6–7 h
> **Prerequisites:** [L03 (symmetry principle, periscopic lens)](../L03-coma-astigmatism-and-symmetry/), [L06 (achromats)](../L06-chromatic-aberration-and-achromats/), [L08 (Seidel surface contributions)](../L08-seidel-surface-contributions/), [L09 (Cooke triplet)](../L09-cooke-triplet/) · **Next:** [L11 — Petzval lens and telephoto](../L11-petzval-and-telephoto/)

## Learning objectives
- State and prove (in words and with ray paths) the front-to-back symmetry principle, and list which aberrations it removes exactly at unit magnification and approximately at infinite conjugate.
- Derive the Celor rear-half thin-lens equations (power, axial colour, Petzval) and solve them for given glasses, focal length and Petzval target.
- Run Geary's "rear half → symmetric system with pickups → break symmetry" workflow in OpticStudio using pickup solves.
- Explain the architecture of the double Gauss (why thick menisci around the stop flatten the field), load a credible starting point, and analyse it with the Seidel Diagram.
- Distinguish floating (paraxial) stop size from a hard aperture, and use hard apertures, vignetting factors, Vignetting Plot and Relative Illumination correctly; compute an area-weighted RMS spot.

## Reading
- **Core:** [Kidger §7.7, pp. 164–166] — monocentric systems and front-to-back symmetry (short but fundamental).
- **Core:** [Geary Ch. 25, pp. 271–285] — symmetric achromat ("achromatic periscopic"), design by rear half, breaking symmetry, area-weighted RMS (§25.4), vignetting and hard apertures (§25.6), relative illumination and $\cos^4$ (§25.7), Rapid Rectilinear (§25.8).
- **Core:** [Geary Ch. 28, pp. 315–327] — the Celor (symmetric dialyte): generalized power, the three constraints, the Celor quadratic, and the full ZEMAX procedure with symmetry breaking.
- **Core:** [Kidger §10.4, pp. 206–208] — vignetting in a triplet (re-read with this lesson's eyes).
- **Optional:** Ansys "Getting Started with OpticStudio — Sequential Mode" tutorial, which uses the shipped double Gauss sample `{Zemax}\Samples\Sequential\Objectives\Double Gauss 28 degree field.zmx`: <https://optics.ansys.com/hc/en-us/articles/42661713256723>
- **Optional:** S. Gangadhara, Ansys KB article on vignetting factors: <https://optics.ansys.com/hc/en-us/articles/42661826659347>

---

## 1. The symmetry principle

Consider a lens whose rear half is the mirror image of its front half about the stop, used at **unit magnification** ($m=-1$, object and image at equal distances). Take any ray from an off-axis object point. By symmetry there is a partner ray that traverses the rear half exactly as the first ray traverses the front half, reversed [Kidger §7.7.2, Fig. 7.17]. Consequences:

- The chief ray leaves the lens at the same angle it entered ⇒ **no distortion**.
- The ray-pair argument makes the wavefront aberration contributions of the two halves *equal for even terms* and *equal and opposite for odd terms* in the field-pupil product ⇒ **coma, distortion and lateral colour vanish exactly** (all orders) at $m=-1$.
- Even aberrations — spherical, astigmatism, Petzval, axial colour — **double**. Symmetry does nothing for them; they must be corrected inside each half.

In Seidel language: for the front half, $\bar A/A$ at each surface is mirrored with opposite sign at the corresponding rear surface, so odd terms ($S_{II}$, $S_V$, $C_{II}$) cancel pairwise.

At infinite conjugate the symmetry is broken by the conjugates themselves, so the odd aberrations are only *small*, not zero, and the classic practice is to finish by slightly breaking the lens symmetry [Kidger p. 166; Geary §25.5]. This is why almost every high-performance camera lens with a central stop (Celor, Dagor, Rapid Rectilinear, Plasmat, double Gauss, Biogon-type wide angles) is *nearly* symmetric.

**Degrees-of-freedom bookkeeping.** For the symmetric achromat Geary counts 5 variables (3 radii, one air space, image position) against 7 targets; at unit magnification three of the targets vanish by symmetry, leaving 5 for 5 — a good match [Geary §25.5, pp. 277–278].

### A cousin: monocentric lenses
If *every* surface is concentric with the stop, every chief ray is a "local axis", so off-axis imagery equals on-axis imagery with a narrower beam: coma, astigmatism and lateral colour vanish, but the image surface is a sphere concentric with the lens [Kidger §7.7.1]. Monocentric lenses reappear today in wide-field imagers coupled to curved sensors or fibre bundles.

## 2. Designing by halves: the symmetric achromat and the Rapid Rectilinear

Geary's procedure for a 10-inch F/8, ±20° symmetric achromat [§25.2–25.3, pp. 271–276] is the template for all of this lesson's designs:

1. **Rear half first, at twice the focal length** (two halves of power $\phi/2$ each combine to roughly $\phi$; the separation shifts it a bit). Design it as a thin-lens achromat (L06), then thicken it.
2. **Choose the right bending branch.** An achromat has two zero-spherical bendings; choose the one whose meniscus faces the stop (Geary's "left-hand solution").
3. **Control astigmatism with the stop position**, not the bending (L08: for an achromat with $S_I\approx 0$, bending barely changes $S_{III}$, but moving the stop does if coma is present). Geary uses `FCGT` (tangential field-curvature operand) at several fields to flatten the tangential field. Coma is *ignored* at this stage — symmetry will remove most of it.
4. **Mirror the half** about the stop. In OpticStudio make the rear radii **pickup solves** of the front radii with scale factor −1, and the rear thicknesses pickups of the front ones (in reversed order).
5. Optimize the symmetric system (`EFFL`, `AXCL`, then RMS spot/`TRAC`).
6. **Break symmetry** gradually — free the rear radii, then the air spaces — and re-optimize. The order matters: different release sequences lead to different local minima (Geary's ASYM1–ASYM4 series shows lenses ranging from "front half acting as a window" to a good balanced solution).

Key practical constraint: the stop air space must hold an **iris and shutter**; Geary insists on 0.4–1 inch in his 10-inch designs. In a modern machine-vision lens the analogue is an iris ring or a fixed aperture plate — still a few millimetres.

**Rapid Rectilinear (Dallmeyer, 1866)** — two identical cemented meniscus achromats around a stop. Its trick was glasses with *similar Abbe numbers but different indices*, which lets each half be achromatic with weak, compact menisci and gives flatter illumination [Geary §25.8]. (Geary's homework uses LF1 and F1, $\Delta V\approx 7$.)

## 3. The Celor (symmetric dialyte)

The Celor (von Hoegh, Goerz 1899) replaces each cemented half by an **air-spaced** negative + positive pair [Geary Ch. 28]. The air space is a new degree of freedom: separating the elements requires stronger individual powers to keep the colour correction, and that can be exploited to reduce the Petzval sum.

### The rear-half equations
Let element *a* (negative, flint) be first with marginal height $y_a$, element *b* (positive, crown) second with $y_b$; object at infinity, half power $\phi$, target Petzval $\phi_P$. The three constraints [Geary §28.3] are

$$
\phi = \phi_a + \frac{y_b}{y_a}\phi_b,\qquad
\frac{y_a^2\phi_a}{V_a} + \frac{y_b^2\phi_b}{V_b} = 0,\qquad
\frac{\phi_a}{n_a}+\frac{\phi_b}{n_b} = \phi_P .
$$

The first is the *generalized power* equation (power of thin lenses weighted by relative marginal-ray height — the same as Kidger eq. 2.66 used for the triplet). Eliminating $y_b/y_a$ and $\phi_b$ gives a quadratic in the negative power [Geary eqs. 28.13–28.15; my own re-derivation gives the identical coefficients]:

$$
\Big(V_a - \frac{n_b}{n_a}V_b\Big)\phi_a^2 + \big(n_bV_b\phi_P - 2V_a\phi\big)\phi_a + V_a\phi^2 = 0 .
$$

Take the negative root, then $\phi_b = n_b(\phi_P - \phi_a/n_a)$ and the separation from $\phi = \phi_a+\phi_b - t\phi_a\phi_b$:

$$
t = \frac{\phi_a + \phi_b - \phi}{\phi_a\phi_b}.
$$

Because $n_bV_b\phi_P \ll 2V_a\phi$ for a sensible low Petzval target, Geary notes you may simply set $\phi_P = 0$ for a first start (it changes the answer only moderately).

### Celor procedure in OpticStudio (Geary §28.6, modernized)
1. Thin-lens rear half from the equations; equi-concave negative, equi-convex positive (radius pickups with −1); verify with `EFFL` and `EFLY` (single-element focal length operands, used by Geary to monitor element powers).
2. Thicken; re-optimize with `EFFL`, `AXCL`.
3. Bend each element to zero spherical (`SPHA` target 0) while holding element powers with `EFLY` targets.
4. Add a stop in front, 5° field; remove astigmatism with `ASTI` = 0 *or* with `FCGT` at three fields; ignore coma.
5. Assemble the symmetric system with pickups; re-establish `EFFL` and colour; then turn on `TRAC`/RMS spot and let the stop air space vary — but **with a minimum** (`MNCA`) so the halves do not crash.
6. Walk the field out gradually (5° → 10° → 15°), re-generating the default merit function each time.
7. Break symmetry (Geary's CELO109–1012 sequence). His table shows RMS spot at full field dropping from 45 µm (best symmetric) to 23 µm (fully asymmetric) — the typical factor ~2 gain from symmetry breaking at infinite conjugate [Geary Table 28.1].

The Celor is also the conceptual bridge to the triplet: merge the two central negative elements of a Celor into one and you have a Cooke triplet — exactly how Geary teaches the triplet [Geary §30.3].

## 4. The double Gauss

The double Gauss (Clark 1888; Rudolph's Zeiss Planar 1896; Lee's Taylor-Hobson Opic 1920 made it practical) is the most successful high-aperture normal lens: typically **F/1.4–F/2, ±20–25°**, six (sometimes seven) elements in four groups:

```
   L1        L2+L3        STOP       L4+L5        L6
  (+)    (+ cemented −)    |     (− cemented +)   (+)
 meniscus thick meniscus   |     thick meniscus  meniscus
   )          ))           |          ((            (
```

How it works, in the language of the previous lessons:
- **Near symmetry about the stop** ⇒ small coma, distortion, lateral colour.
- **Two thick negative menisci concave toward the stop.** Their strongly curved inner surfaces sit where the marginal ray is low and the beam converges/diverges strongly; they carry large negative $S_{IV}$ contributions (Petzval depends only on curvature and index, not on ray height) while their effect on power is moderated. This is the "thick meniscus" principle: a meniscus with *equal* radii has zero Petzval contribution but positive power $K = (n-1)^2t/(nR^2)$ — power without field curvature.
- **Cemented flint–crown interfaces** inside the menisci correct axial colour and, with a refractive-index step, provide a "buried surface" for higher-order spherical and spherochromatism control.
- Residual problem: **oblique spherical aberration and sagittal flare** at large apertures and fields — the rim rays of the off-axis beam. Practical double Gauss lenses therefore vignette substantially at the field edge (often 40–60% of the axial beam remains at full field).

### Where to get a starting point (be realistic)
- **OpticStudio sample files.** OpticStudio ships with `{Zemax}\Samples\Sequential\Objectives\Double Gauss 28 degree field.zmx` (used by Ansys's own getting-started tutorial and by the ZOSPy examples). Browse the same `Objectives` folder for other classic forms. The `{Zemax}` folder is your *Documents\Zemax* data folder (set under Setup → Project Preferences / Folders; location varies by version).
- **Books.** Kingslake, *Lens Design Fundamentals*, and W. J. Smith, *Modern Lens Design*, tabulate many double Gauss prescriptions scaled to f = 100 (not in our corpus — check a library).
- **Patents.** Search Google Patents for "Gauss type" or "photographic objective" with six elements; expired patents give real, manufacturable prescriptions. Always check the units (some old patents normalize f = 1) and the glass names (convert old glass codes to current equivalents with the Glass Catalog or Glass Compare tools).
- Never trust a starting point blindly: re-optimize for *your* wavelengths, sensor and conjugate.

## 5. Vignetting, hard apertures and relative illumination

### Floating stop vs. hard aperture
By default OpticStudio's stop semi-diameter **floats**: it is computed from the system aperture (e.g. EPD) for the axial beam, and other surfaces' semi-diameters grow automatically to pass every ray of every field. Geary shows that, in this mode, the stop semi-diameter even *grows* when you add field (0.47 → 0.62 inch in his example) — a real iris does not do that [Geary §25.6, pp. 280–281]. To model hardware you must:

1. Put a **hard aperture** on the stop (Surface Properties → Aperture → Circular Aperture, maximum radius = the axial value), or fix the stop semi-diameter (*Fixed* solve).
2. Fix or aperture-limit the element clear apertures as the mechanical design will.
3. Inspect with the **Vignetting Plot** (fraction of unvignetted rays vs. field; Geary's "Analysis > Illumination > Vignetting Plot" — in current versions look in the Analyze tab, location varies by version) and **Relative Illumination**.

Then decide: either *accept* physical clipping and let vignetting factors (L09) tell the optimizer which rays survive, or *enlarge* apertures. Vignetting factors and hard apertures should agree; after big design changes, re-run **Set Vignetting**.

### Relative illumination is more than vignetting
For a Lambertian object and a perfect thin lens, irradiance falls as $\cos^4\theta$ even with *no* vignetting [Geary §25.7, Fig. 25.19]: one $\cos$ from the apparent source area, one from the apparent pupil area, two from the inverse square of the longer oblique path. Pupil distortion and image distortion modify it: wide-angle retrofocus lenses enlarge their off-axis entrance pupil and beat $\cos^4$; long stop air spaces (Celor-type) make it worse [Geary p. 283]. Steep fall-off saturates the centre and starves the corners of a sensor — for a Zivid camera, it maps directly to corner depth noise.

### One number for the whole field: area-weighted RMS
Averaging spot sizes over field points equally over-weights the centre. Geary's **area-weighted RMS** gives each field point the area of the annular image zone it represents [§25.4, eq. 25.1]:

$$
\text{AWRMS} = \frac{1}{A_{\text{tot}}}\sum_i A_i\,\text{RMS}_i .
$$

With zone boundaries halfway between field heights, the edge field typically carries ~30% of the weight and the axis only ~10% (see worked example). This is the right mindset for camera lenses: most pixels are off-axis.

## 6. In OpticStudio

- **Pickup solves:** in a radius or thickness cell, Solve Type → *Pickup*, From Surface, Scale Factor (−1 for mirrored radii), Offset. For a symmetric lens about surface S, surface S+k picks up radius of S−k+1 with scale −1 (check on paper first — off-by-one errors here are the classic mistake). Thicknesses pick up in reverse order.
- **Element-power monitoring:** `EFLY` (focal length of a surface range) as Geary uses, or `EFFL` for the system; `AXCL` for axial colour; `FCGT`/`FCGS` for generalized tangential/sagittal field curvature; `SPHA`/`COMA`/`ASTI` (waves, L08) for Seidel monitoring.
- **Spacing protection:** `MNCA`, `MNEA`, `MNCG`, `MNEG` (min centre/edge air and glass) — set the stop gap minimum for the iris.
- **Analyses:** Seidel Diagram (look for mirror-image bars in the two halves), Field Curvature/Distortion, Lateral Colour, Relative Illumination, Vignetting Plot, Footprint Diagram.
- **Sample files** are read-only templates: *Save As* into your work folder before editing.

## Worked example

**(a) Celor rear half, scaled to a 50 mm lens.** Glasses as in Geary: flint $n_a=1.60562$, $V_a=43.93$ (BaF4-type); crown $n_b=1.61272$, $V_b=58.63$ (SK4-type). Full lens $f=50$ mm, so the rear half is designed at $f_{1/2}=100$ mm: $\phi=0.01$ mm⁻¹, Petzval target $\phi_P = 0.003$ mm⁻¹ (i.e. $\phi_P f_{1/2} = 0.3$).

Coefficients: $a = 43.93 - (1.61272/1.60562)\times58.63 = -14.959$; $b = 1.61272\times58.63\times0.003 - 2\times43.93\times0.01 = -0.5949$; $c = 43.93\times10^{-4} = 0.004393$.

Roots: $\phi_a = -0.04614$ or $+0.00637$ mm⁻¹ → take $\phi_a = -0.04614$ ($f_a = -21.68$ mm). Then $\phi_b = 1.61272\,(0.003 + 0.04614/1.60562) = 0.05118$ ($f_b = 19.54$ mm), and $t = (-0.04614+0.05118-0.01)/(-0.04614\times0.05118) = 2.10$ mm. These are exactly Geary's inch results (−2.168 in, 1.954 in, 0.210 in for a 10-inch half) scaled by 10 — a good check. With $\phi_P=0$: $f_a=-15.78$, $f_b=15.71$, $t=2.41$ mm (stronger elements).

**(b) Thick meniscus.** $n=1.5$, $R_1=R_2=20$ mm, $t=10$ mm: $K = 10\times0.25/(1.5\times400) = 1/240$ mm⁻¹ → $f=240$ mm, Petzval contribution 0.

**(c) AWRMS.** Fields 0°, 14°, 20° (image heights ∝ tan θ: 0, 0.685, 1). Zone boundaries at 0.3425 and 0.8425 of full height give area weights 0.117, 0.593, 0.290. With RMS spots 20, 30, 50 µm: AWRMS $= 0.117(20)+0.593(30)+0.290(50) = 34.6$ µm (vs. a simple mean of 33.3 µm). The difference grows when the edge is much worse than the centre.

## Key takeaways
- Front-to-back symmetry about the stop cancels odd aberrations (coma, distortion, lateral colour) exactly at unit magnification and approximately at infinity; even aberrations must be corrected within each half.
- Design by halves: optimize a rear half at twice the focal length, mirror it with pickups, optimize symmetric, then break symmetry in controlled steps.
- The Celor's air space adds a degree of freedom used to reduce Petzval; its rear half follows from a quadratic in the negative power.
- The double Gauss flattens the field with thick negative menisci around the stop and controls colour with cemented interfaces; its limit is oblique spherical / sagittal flare, handled partly by vignetting.
- Model real hardware with hard apertures; floating stops silently grow. Keep vignetting factors consistent with apertures.
- Relative illumination ≈ $\cos^4\theta$ × vignetting × pupil effects; use AWRMS to rate a whole field.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Symmetry principle | Mirror-symmetric lens at $m=-1$ has zero odd aberrations |
| Symmetric achromat / Rapid Rectilinear | Two cemented meniscus achromats around a stop |
| Celor (symmetric dialyte) | Two air-spaced − + pairs symmetric about the stop |
| Double Gauss | Six-element (+, ++−, stop, −+, +) near-symmetric high-aperture objective |
| Pickup solve | Parameter set equal to (scale × another parameter + offset) |
| Hard aperture | Physical aperture on a surface that blocks rays |
| Floating stop | Stop semi-diameter computed from the system aperture |
| Vignetting Plot | Fraction of unvignetted rays vs. field |
| Relative illumination | Off-axis/on-axis image irradiance |
| AWRMS | Area-weighted average RMS spot over the image |
| Monocentric lens | All surfaces concentric with the stop |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE Press 2002 — §7.7, pp. 164–166; §10.4, pp. 206–208; eq. 2.66, p. 39.
2. [Geary] J. M. Geary, *Introduction to Lens Design*, Willmann-Bell 2002 — Ch. 25, pp. 271–285; Ch. 28, pp. 315–327; §30.3, pp. 344–345.
3. Ansys Optics, "Getting Started with OpticStudio — Sequential Mode" (uses `Double Gauss 28 degree field.zmx`): <https://optics.ansys.com/hc/en-us/articles/42661713256723>
4. ZOSPy example that loads the same sample via `SamplesDir / "Sequential/Objectives/Double Gauss 28 degree field.zmx"`: <https://zospy-cn.readthedocs.io/zh-cn/latest/examples/%E5%8F%8C%E9%AB%98%E6%96%AF%E9%95%9C%E5%A4%B4%E5%85%89%E7%BA%BF%E8%BF%BD%E8%B8%AA/raytrace_double_gauss.html>
5. S. Gangadhara, Ansys KB, vignetting factors: <https://optics.ansys.com/hc/en-us/articles/42661826659347>
6. R. Kingslake, *Lens Design Fundamentals*; W. J. Smith, *Modern Lens Design* — prescription sources (not in corpus).
