# L05 — Wide-angle lenses and distortion mappings

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2.5 h, tasks ~4.5 h
> **Prerequisites:** [02/L05 — Distortion](../../02-aberrations-classical-design/L05-distortion/) (read its §3–4 again), [02/L11 — telephoto](../../02-aberrations-classical-design/L11-petzval-and-telephoto/), [L03 — RI & telecentricity](../L03-relative-illumination-and-telecentricity/), [L04 — project](../L04-compact-fixed-focus-lens-project/) · **Next:** [L06 — Telecentric metrology lenses](../L06-telecentric-metrology-lenses/)

## Learning objectives
- Explain why short-focal-length lenses with long back focus need the retrofocus (inverted-telephoto) form, and lay out a two-group retrofocus by thin-lens formulas.
- Compare the rectilinear, equidistant (f-θ), equisolid, stereographic and orthographic mappings by image size, angular resolution across the field, and relative illumination; pick one for a given application.
- Express distortion budgets in pixels and in calibration-model terms (Brown–Conrady $k_i$, Kannala–Brandt for fisheyes), and quantify how well a model fits a lens mapping.
- Explain why a calibrated 3D camera cares more about distortion *stability* (focus, temperature, wavelength, mechanics) than about its magnitude, and estimate stability terms in pixels and in depth error.
- Set up wide-angle and fisheye systems in OpticStudio (field types, enhanced ray aiming, distortion references) and extract a mapping table for calibration studies.

## Reading
- **Core:** [Kidger §4.4.2.4, pp. 79–82] — distortion definitions for finite, infinite and afocal conjugates; effect of pupil aberrations and defocus (§4.4.2.4.4); f-θ lenses (§4.4.2.4.5).
- **Core:** [Kidger §9.4, pp. 193–198] — the telephoto principle; the retrofocus is the same two-group arithmetic turned around.
- **Core:** [Geary Ch. 15, pp. 167–173] — distortion as a wavefront tilt; plus [Geary Ch. 1, p. 6], the chart of design forms by field and aperture (fisheye and retrofocus at the wide-field end).
- **Online:** Ansys Optics KB, "Setting up a wide-angle or fisheye lens in OpticStudio" (Enhanced vs Robust ray aiming; supported field types): <https://optics.ansys.com/hc/en-us/articles/42661958377491>
- **Online:** OpenCV documentation, fisheye camera model (Kannala–Brandt): <https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html>
- **Optional:** Wikipedia, "Angénieux retrofocus" (history of the form): <https://en.wikipedia.org/wiki/Ang%C3%A9nieux_retrofocus>
- **Optional:** "Surround-view fisheye optics in computer vision and simulation: survey and challenges" (arXiv 2402.12041) — fisheye models as used by vision engineers: <https://arxiv.org/pdf/2402.12041>

---

## 1. Why wide-angle lenses look the way they do

A machine-vision camera that must see a large object field at a short working distance (bin picking from 0.5 m, robot cells, logistics) needs a short focal length. Two constraints then shape the lens:

1. **Back focus.** C-mount lenses have a flange focal distance of 17.526 mm, CS-mount 12.526 mm; the sensor stack (filter, cover glass) and the camera housing need space. A 4–6 mm focal-length lens with a simple symmetric form would have its rear vertex ~3–5 mm from the sensor, inside the camera. The lens must have a **back focal length larger than its focal length**.
2. **Field angle.** Beyond about ±35–40°, cos⁴ fall-off (L03), astigmatism and the sheer size of the rectilinear image ($h = f\tan\theta$ grows without bound) push the design toward **controlled barrel distortion** or a fisheye mapping.

Geary's chart of design forms [Geary Ch. 1, p. 6] places retrofocus and fisheye lenses at the wide-field end, at modest apertures — the domain of most 3D-camera receivers with 60–90° fields.

## 2. The retrofocus (inverted telephoto)

### 2.1 Thin-lens layout
A telephoto has a positive front group and a negative rear group, giving an overall length shorter than $f$ [Kidger §9.4]. Reverse it: a **negative front group** of focal length $f_1 < 0$, separated by $d$ from a **positive rear group** $f_2$. Then

$$
\frac1f = \frac1{f_1}+\frac1{f_2}-\frac{d}{f_1f_2},\qquad
\text{BFL} = f\left(1-\frac{d}{f_1}\right).
$$

With $f_1 < 0$, BFL > $f$: the principal plane has moved behind the rear group. The **retrofocus ratio** BFL/$f$ is set by $d/|f_1|$: e.g. BFL = $2f$ needs $d = |f_1|$.

**Example.** $f = 6$ mm with BFL = 12 mm and $d = 10$ mm: $1 - d/f_1 = 2 \Rightarrow f_1 = -10$ mm; then $1/6 = -1/10 + 1/f_2 + 10/(10f_2) = -0.1 + 2/f_2 \Rightarrow f_2 = 7.5$ mm. Check: $f = 6.0$ mm, BFL = 12.0 mm.

### 2.2 What the negative front group does to aberrations
- **The front group acts as a "wide-angle converter"**: it reduces the field angle that the rear group must handle (object chief rays at 45° may hit the rear group at ~20–25°), which is why it works at all.
- It is **far from the stop**, where the chief ray is high: it is the main source of **barrel distortion** and **lateral colour**. Retrofocus lenses therefore naturally have barrel distortion — good for RI and sensible for calibrated cameras, bad for "zero-distortion" specs.
- It introduces strong **pupil aberration**: the entrance pupil seen from oblique angles grows and tilts toward the viewer (the RI "bonus" of L03, $\kappa > 1$).
- The asymmetry (negative front, positive rear) makes **coma and lateral colour** hard; designs add a cemented doublet behind the stop and split the front negative into two menisci concave toward the stop (to keep incidence angles low).
- Large front elements: the front group must pass the full field at full aperture — its diameter, not the rear element, sets the lens size and cost.

## 3. Mappings: what each one gives you

Course 02 L05 tabulated the five classical mappings. Here we look at them as an engineer choosing one:

| Mapping | $h(\theta)$ | $dh/d\theta$ (radial resolution) | Relative illumination (ideal, L03) | $f$ for $h = 2.25$ mm at 90° |
|---|---|---|---|---|
| Rectilinear | $f\tan\theta$ | $f\sec^2\theta$ — grows, ∞ at 90° | $\cos^4\theta$ | impossible |
| Equidistant (f-θ) | $f\theta$ | $f$ — constant | $\cos\theta\sin\theta/\theta$ | 1.43 mm |
| Equisolid | $2f\sin(\theta/2)$ | $f\cos(\theta/2)$ — 0.71 f at 90° | $\cos\theta$ | 1.59 mm |
| Stereographic | $2f\tan(\theta/2)$ | $f\sec^2(\theta/2)$ — 2 f at 90° | $\cos\theta\cos^4(\theta/2)$ | 1.125 mm |
| Orthographic | $f\sin\theta$ | $f\cos\theta$ — 0 at 90° | 1 | 2.25 mm |

(The RI column is the pure mapping effect with $\kappa = 1$; derivations in L03 Task 1.)

How to choose:
- **Rectilinear** when straight lines must stay straight in the raw image (measurement without calibration, human viewing) and the half-field is below ~45°.
- **Equidistant / f-θ**: equal angular resolution everywhere — natural for angle-measuring systems (scanners, star trackers, many 3D sensors that reason in ray directions anyway).
- **Equisolid**: equal *area* per solid angle — every pixel sees the same solid angle; good for radiometric uniformity (sky cameras).
- **Stereographic**: conformal (preserves local shapes), enlarges the edge — good when objects at the edge must be recognised.
- In a **calibrated 3D camera**, the mapping is a *design variable* — choose the one that best spends pixels where the application needs resolution, then calibrate. A "rectilinear" spec for a 120° lens wastes pixels in the centre and needs an enormous image circle.

Modern wide-angle machine-vision lenses (90–120°) are usually "between" rectilinear and f-θ: barrel distortion of −10 % to −30 % at the edge, deliberately chosen.

## 4. Distortion budgets in pixels and in calibration terms

### 4.1 Size in pixels
Express distortion in pixels at the sensor edge: −2 % at 4.5 mm with 3.45 µm pixels is 90 µm = 26 pixels. Calibration routinely removes hundreds of pixels; the question is **how well** and **how stably**.

### 4.2 Calibration models
**Brown–Conrady** (OpenCV's standard model) maps undistorted normalized coordinates $(x, y) = (X/Z, Y/Z)$, $r^2 = x^2 + y^2$, to distorted ones:

$$
x_d = x\,(1 + k_1r^2 + k_2r^4 + k_3r^6) + 2p_1xy + p_2(r^2+2x^2),
$$
$$
y_d = y\,(1 + k_1r^2 + k_2r^4 + k_3r^6) + p_1(r^2+2y^2) + 2p_2xy,
$$

then pixel coordinates via the focal length in pixels and the principal point. $k_1, k_2, k_3$ describe radial distortion (relative to rectilinear, since $r = \tan\theta$); $p_1, p_2$ describe decentering (assembly errors, Course 06). Because the reference is $\tan\theta$, which diverges at 90°, the model needs ever more coefficients as the field grows.

**Kannala–Brandt** (OpenCV's *fisheye* model) uses the angle directly:

$$
\theta_d = \theta\,(1 + k_1\theta^2 + k_2\theta^4 + k_3\theta^6 + k_4\theta^8),\qquad r_d \propto \theta_d,
$$

i.e. an f-θ reference with polynomial corrections ([OpenCV fisheye docs](https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html)). It represents all classical fisheye mappings with a few terms.

**Fit quality matters.** Fitting Brown–Conrady to an ideal f-θ lens ($f = 4$ mm, 3 µm pixels; residual = worst-case model error):

| Half-field | $k_1$ only | $k_1, k_2$ | $k_1..k_3$ |
|---|---|---|---|
| 30° | 2.8 px | 0.14 px | 0.008 px |
| 50° | 52 px | 8.0 px | 1.3 px |
| 60° | 176 px | 41 px | 10.6 px |

whereas Kannala–Brandt with two coefficients fits an equisolid lens out to 90° to 0.002 px (Task 2). **Design rule:** pick the lens mapping and the calibration model together. A design whose distortion curve has "wiggles" (high-order balancing used to push the maximum distortion to zero) may need more coefficients than the calibration pipeline has — smooth and monotonic wins.

### 4.3 Why stability beats magnitude in 3D cameras
A structured-light or stereo 3D camera converts pixel positions into ray directions using the factory calibration. Any change of the lens mapping *after* calibration becomes a 3D error:

| Source | Mechanism | Typical size |
|---|---|---|
| Focus shift (thermal, mechanical creep) | image scale changes by $\delta z/d_{XP}$ (L03) | 20 µm at $d_{XP}$ = 15 mm → 0.13 % → 1.7 px at 4.5 mm (3.45 µm pixels) |
| Focal-length change with temperature | $dn/dT$, CTE of glass and barrel | ~5–30 ppm/K glass, ~100 ppm/K plastics (L07) |
| Distortion shape change with object distance | pupil aberrations; distortion depends on conjugate | small for $m \ll 1$, check with Multi-Config |
| Wavelength change | lateral colour = magnification vs λ; LED/VCSEL drift ~0.06–0.3 nm/K | sub-pixel if lateral colour is corrected |
| Mechanical (shock, tilt of lens vs sensor) | decentre → $p_1,p_2$; tilt → keystone | Course 06 |

For triangulation (L09), depth is $z \approx f b/d$ (baseline $b$, disparity $d$): a relative change of the effective focal length gives the same relative change in depth. 300 ppm (e.g. 10 ppm/K over 30 K) at 1 m is 0.3 mm of depth error — comparable to the accuracy spec of a high-end 3D camera. Hence the professional priority list: **(1) stable, (2) smooth/low-order, (3) small**.

## 5. In OpticStudio

- **Fields for wide angles:** with the object at infinity use *Angle* (or *Theodolite Angle* for fields defined by azimuth/elevation); for finite objects, *Object Height* with ray angles below 90°. These are the combinations supported by Enhanced Ray Aiming ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/42661958377491)). *Real Image Height* is convenient below ~60° but can fail to converge on fisheyes.
- **Ray aiming:** wide-angle and fisheye lenses have large pupil aberrations — without ray aiming the chief ray does not pass through the stop centre and distortion/RI are wrong. Use *Enhanced Ray Aiming* first (with *Advanced Convergence* if needed); try *Robust Ray Aiming* only if Enhanced fails (the two are mutually exclusive). Spikes in the Field Curvature/Distortion plot and "Cannot determine object coordinates" errors are the symptoms ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/42661958377491)).
- **Sample file:** the samples include a 200° field wide-angle lens (`Wide angle lens 200 degree field.zos` in the Sequential samples; folder name varies by version) — the KB article uses it.
- **Distortion reference:** the Field Curvature/Distortion analysis can report F-Tanθ or F-θ distortion (and calibrated variants; Course 02 L05). For a fisheye, F-θ distortion is the meaningful number.
- **Mapping table for calibration studies:** add REAY rows (weight 0) for chief rays at many field angles, or use the Grid Distortion analysis text output, and export to Python (Course 07 automates this). Fit Brown–Conrady or Kannala–Brandt and report residuals in pixels.
- **Controlling the mapping in optimization:** to target an f-θ mapping, constrain chief-ray heights: `REAY` at Hy = 0.25, 0.5, 0.75, 1.0 with targets $f\theta$ (or use the F-θ distortion option with DIMX if your version offers it — check Help). For a generic "smooth barrel" target, constrain REAY at several fields to a chosen polynomial.
- **Stability checks:** Multi-Configuration with (a) image plane ±20 µm, (b) object distance near/far, (c) temperature (Course 03 L09), (d) wavelength shifted by ±5 nm; compare REAY at full field across configurations and convert to pixels.

## Worked example — choosing a mapping for a 140° bin-picking camera

**Given:** a 1/2.3"-type sensor used with a circular image of diameter 4.5 mm ($h_\max = 2.25$ mm) at 3.0 µm pixels; required full field 140° (θ_max = 70°).

1. **Rectilinear:** $f = 2.25/\tan70° = 0.82$ mm. Radial resolution at the centre $f$ = 0.82 mm/rad, i.e. 0.82/3.0e-3 = 273 px/rad = 4.8 px/deg; at the edge $f\sec^2 70° = 7.0$ mm/rad → 41 px/deg. The centre is starved, the edge oversampled, and RI = cos⁴70° = 0.014. Not sensible.
2. **Equidistant:** $f = 2.25/1.2217 = 1.84$ mm → 613 px/rad = 10.7 px/deg everywhere — more than twice the rectilinear centre resolution. RI ≈ $\cos70°\sin70°/1.2217 = 0.26$ (before pupil effects).
3. **Equisolid:** $f = 2.25/(2\sin35°) = 1.96$ mm; centre 11.4 px/deg, edge $\cos35°$ × that = 9.4 px/deg; RI = cos 70° = 0.34.
4. **Calibration:** Brown–Conrady with 3 coefficients fails at 70° (tens of px residual even for an ideal f-θ lens, Table §4.2); use Kannala–Brandt.
5. **Choice:** equidistant or equisolid; prefer equisolid if radiometric uniformity matters, equidistant if angular resolution should be uniform.

## Key takeaways
- Short focal length + long back focus ⇒ retrofocus: negative front group, BFL $= f(1 - d/f_1) > f$.
- The front negative group creates barrel distortion, lateral colour and pupil growth — use them, don't fight them blindly.
- Mappings differ in resolution distribution and RI: rectilinear wastes the centre at wide angles; f-θ is uniform in angle; equisolid is uniform in solid angle.
- Choose the calibration model with the lens: Brown–Conrady to ~50° half-field, Kannala–Brandt for fisheyes; demand smooth, low-order distortion.
- For 3D cameras, distortion *stability* (focus, temperature, wavelength, mechanics) is the real spec; 300 ppm of scale ≈ 0.3 mm depth error at 1 m.
- In OpticStudio: angle fields, enhanced ray aiming, F-θ distortion reference, REAY tables exported for calibration fits.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Retrofocus / inverted telephoto | Negative front group + positive rear group, BFL > EFL |
| Retrofocus ratio | BFL / EFL |
| Fisheye | Lens with ≥ ~150° field using a non-rectilinear mapping |
| Mapping function | $h(\theta)$: image height vs field angle |
| Equidistant (f-θ) | $h = f\theta$ |
| Equisolid | $h = 2f\sin(\theta/2)$, equal area per solid angle |
| Stereographic | $h = 2f\tan(\theta/2)$, conformal |
| Brown–Conrady model | Radial ($k_i$) + tangential ($p_i$) polynomial distortion model in $r = \tan\theta$ |
| Kannala–Brandt model | Polynomial in $\theta$ (OpenCV fisheye) |
| Enhanced / Robust ray aiming | OpticStudio ray-aiming algorithms for difficult wide-field systems |

## References
1. [Kidger §4.4.2.4, pp. 79–82] — distortion definitions, pupil aberrations and defocus, f-θ lenses.
2. [Kidger §9.4, pp. 193–198] — telephoto lenses (two-group arithmetic).
3. [Geary Ch. 15, pp. 167–173] — distortion; [Geary Ch. 1, p. 6] — design-form chart.
4. Ansys Optics KB, "Setting up a wide-angle or fisheye lens in OpticStudio": <https://optics.ansys.com/hc/en-us/articles/42661958377491>
5. OpenCV, "Fisheye camera model" (calib3d fisheye): <https://docs.opencv.org/3.4/db/d58/group__calib3d__fisheye.html>
6. Wikipedia, "Angénieux retrofocus": <https://en.wikipedia.org/wiki/Ang%C3%A9nieux_retrofocus>
7. "Surround-view fisheye optics in computer vision and simulation: survey and challenges", arXiv:2402.12041: <https://arxiv.org/pdf/2402.12041>
