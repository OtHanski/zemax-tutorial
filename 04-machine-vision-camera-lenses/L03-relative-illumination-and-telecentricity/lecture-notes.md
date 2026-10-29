# L03 — Relative illumination and telecentricity

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2.5 h, tasks ~4 h
> **Prerequisites:** [L01](../L01-image-sensors-and-sampling/), [L02](../L02-camera-first-order-design/), [01/L04 — stops, pupils, vignetting](../../01-foundations/L04-stops-pupils-fields/), [02/L10 — vignetting](../../02-aberrations-classical-design/L10-symmetric-lenses-double-gauss-vignetting/) · **Next:** [L04 — Compact fixed-focus lens project](../L04-compact-fixed-focus-lens-project/)

## Learning objectives
- Derive the cos⁴ law from radiometry, and state the assumptions under which it holds (and why it is "not a law").
- Write a general relative-illumination formula that includes image mapping (distortion) and pupil-area change, and use it to explain why wide-angle and retrofocus lenses can beat cos⁴.
- Distinguish natural fall-off, mechanical vignetting, pupil aberration and sensor angular response, and know which one OpticStudio's Relative Illumination analysis includes.
- Define image-space telecentricity, compute the CRA from the exit-pupil position, and quantify the image-scale error caused by defocus in a non-telecentric lens.
- Put a sensor CRA specification and a relative-illumination target into a merit function with RAID, RELI, EXPP/RECI and related operands.
- Explain the design trade (size, cost, distortion) between low CRA and compactness.

## Reading
- **Core:** [Geary §25.7, pp. 282–283] — relative illumination fall-off, Fig. 25.19 derivation of cos⁴, "this law has nothing to do with vignetting".
- **Core:** [Kidger §10.4, pp. 206–208] — vignetting in a triplet; typical 60 % full-field beam width; corner illumination ~40 % of axis.
- **Core:** [Kenyon §1.7, pp. 22–25] — radiometric terms (irradiance, radiance, Lambertian sources, Eq. 1.34). Note: Kenyon writes Lambert's law as $L(\theta) = L(0)\cos\theta$; the usual statement is that *radiance is constant* and the *intensity* (per steradian, from a fixed area) falls as $\cos\theta$. His integral $E = \pi L$ (Eq. 1.34) is the standard result.
- **Online:** Ansys Optics KB, "How to create image-space telecentric lenses" (KA-01552): <https://optics.ansys.com/hc/en-us/articles/42661811743251>
- **Online:** Zemax Community, "Why vignetting factors should be removed when calculating relative illumination and MTF": <https://community.zemax.com/got-a-question-7/why-vignetting-factors-should-be-removed-when-calculating-relative-illumination-and-mtf-121>
- **Online:** Zemax Community, "How to calculate relative illuminance through integration" (how OpticStudio integrates the exit pupil; points to Rimmer's paper): <https://community.zemax.com/got-a-question-7/how-to-calculate-relative-illuminance-through-integration-1581>
- **Optional:** M. P. Rimmer, "Relative illumination calculations", Proc. SPIE 655 (1986) — the method behind OpticStudio's analysis.

---

## 1. Why uniformity matters for a measurement camera

A machine-vision image is data. Fall-off of irradiance toward the corners means:
- **lower SNR in the corners** (shot noise $\propto\sqrt{N_e}$) — the 3D point cloud gets noisier toward the edges of the field;
- **less usable dynamic range**: you expose so the centre does not saturate and the corners starve (Geary's warning, [Geary §25.7]);
- **calibration burden**: flat-field correction fixes the *mean* but not the *noise*.

A Zivid-type camera also has a projector whose own fall-off multiplies the camera's: if both have 50 % corner illumination, the corner signal is 25 % of the centre. Relative illumination (RI) is therefore a first-class spec item — typically "RI ≥ 50–70 % at full field (including vignetting, at the design F/#)" for machine-vision lenses.

## 2. Radiometry of an image point: the cos⁴ law

Consider a perfect thin lens with entrance pupil area $A$ looking at a uniform Lambertian object of radiance $L$ at infinity. For the image point at field angle $\theta$ [Geary Fig. 25.19]:

1. The pupil, seen obliquely from the object direction, has projected area $A\cos\theta$ → one factor $\cos\theta$.
2. The distance from the pupil to the image point grows as $1/\cos\theta$ (along the chief ray), so the solid angle subtended by the pupil falls as $\cos^2\theta$ → two more factors. (Equivalently: the image area corresponding to a given object solid angle grows.)
3. The light arrives obliquely at the image plane, spreading over an area larger by $1/\cos\theta$ → the fourth factor.

So, for a distortion-free lens without vignetting or pupil aberrations,

$$
\mathrm{RI}(\theta) = \frac{E(\theta)}{E(0)} = \cos^4\theta .
$$

| $\theta$ | 10° | 20° | 25° | 30° | 35° | 40° | 45° |
|---|---|---|---|---|---|---|---|
| $\cos^4\theta$ | 0.94 | 0.78 | 0.67 | 0.56 | 0.45 | 0.34 | 0.25 |

A 70° diagonal FOV lens ($\theta = 35°$) that obeys cos⁴ has only 45 % corner illumination *before* any vignetting. "cos⁴ is not a law, it is the result you get for a simple system with no aberration" ([Zemax Community FAQ on relative illumination](https://community.zemax.com/got-a-question-7/faq-about-relative-illumination-1006)) — real lenses do better or worse.

The on-axis irradiance itself, for a lens of transmittance $T$ and working F/# $N_w$ (aplanatic, small-angle), is

$$
E_0 = \pi T L \sin^2 u' \approx \frac{\pi T L}{4 N_w^2},
$$

which is the formula used in L02.

## 3. A general relative-illumination formula

Energy bookkeeping gives a more useful form. For an object at infinity, the flux from the scene element of solid angle $d\Omega = \sin\theta\,d\theta\,d\phi$ that enters the entrance pupil is $L\,A\,\kappa(\theta)\cos\theta\,d\Omega$, where $\kappa(\theta)$ is the ratio of the *real* entrance-pupil area at field $\theta$ to the axial one (pupil aberration and vignetting). It lands on the image area $h\,dh\,d\phi$ (rotational symmetry, radial mapping $h(\theta)$). Therefore

$$
E(\theta) \propto \frac{\kappa(\theta)\cos\theta\,\sin\theta}{h\,(dh/d\theta)}
\quad\Longrightarrow\quad
\mathrm{RI}(\theta) = \kappa(\theta)\,\cos\theta\,\frac{f^2\sin\theta}{h\,h'(\theta)}
$$

(normalised so that RI(0) = 1; $h' = dh/d\theta$, and the obliquity at the sensor is already accounted for because $h\,dh\,d\phi$ is the *sensor-plane* area).

Check: for $h = f\tan\theta$, $h\,h' = f^2\tan\theta/\cos^2\theta$ and RI $= \kappa\cos^4\theta$ ✓.

This formula shows the three ways out of cos⁴:

- **Barrel distortion** (image compressed at the edge, $h < f\tan\theta$) concentrates the energy on a smaller area: an equidistant ("f-θ") mapping $h = f\theta$ gives RI $= \kappa\cos\theta\sin\theta/\theta$ — 0.83 at 30° and 0.64 at 45° instead of 0.56 and 0.25. Fisheye and wide-angle lenses exploit this (L05).
- **Pupil growth** ($\kappa > 1$): in retrofocus/wide-angle lenses the front negative group images the stop with strong *pupil coma*: the entrance pupil seen from oblique directions is larger and tilted toward the viewer. This is the "Slyusarev effect"; modern wide-angle lenses use it deliberately.
- **Vignetting** ($\kappa < 1$) works the other way; it is used to cut off badly aberrated rim rays [Kidger §10.4], at the cost of RI.

Kidger's triplet example puts numbers on the conventional case: a full-field beam ~60 % of the axial width combined with cos⁴ leaves the corner at ~40 % [Kidger §10.4].

**Image-space view.** Equivalently, the irradiance at an image point is $\pi T L'\,\Omega_\text{proj}$ where $\Omega_\text{proj}$ is the *projected solid angle of the exit pupil* seen from that image point. This is exactly what OpticStudio integrates (Section 6) and it gives the most useful intuition for camera lenses: **if every image point sees the same exit-pupil cone, RI is flat.** An image-space telecentric lens with a well-behaved exit pupil does that; the object-space bookkeeping then balances through pupil aberration and/or distortion.

## 4. Four different "fall-offs" — keep them apart

| Effect | Cause | Shows up in |
|---|---|---|
| Natural fall-off | cos⁴-type geometry, modified by mapping and pupil aberrations | RI analysis, even without apertures |
| Mechanical vignetting | clear apertures clip the off-axis beam | Footprint diagram, RI analysis, shortened ray fans |
| Transmission fall-off | coatings, filters and bulk absorption vary with angle | RI with polarization/transmission enabled, or a separate calculation |
| Sensor angular response | microlens/CRA mismatch, QE vs angle | **not** in OpticStudio — your own model from the sensor's angular-response data |

The total flat-field profile the customer sees is the product. A design review should show all four (Task 4 builds that product).

## 5. Image-space telecentricity and the CRA

### 5.1 Definition
A lens is **image-space telecentric** when its exit pupil is at infinity: every chief ray reaches the image parallel to the axis (CRA = 0). Optically this means the aperture stop is in the **front focal plane** of the optics that follow it. To first order (L01),

$$
\tan\text{CRA}(h) = \frac{h}{d_{XP}},
$$

with $d_{XP}$ the distance from the exit pupil to the image. Example: a compact lens with the exit pupil 12 mm before a 2/3" sensor ($h = 5.5$ mm) has CRA = 24.6° at the corner; to get 15° you need $d_{XP} = 20.5$ mm; to get 0° you need $d_{XP} = \infty$.

### 5.2 Why telecentricity in image space matters
1. **Sensor matching:** global-shutter machine-vision sensors are often designed for low CRA (0–10°); see L01.
2. **Focus-insensitive scale:** if the sensor is defocused by $\delta z$, the image point moves laterally by $\delta z\tan\text{CRA}$, i.e. the image scale changes by the fraction $\delta z/d_{XP}$. With $d_{XP} = 12$ mm, a 20 µm focus change (thermal drift!) changes the magnification by 0.17 % — at the corner (5.5 mm) that is 9.2 µm ≈ 2.7 pixels of 3.45 µm. For a 3D camera that has been calibrated at the factory, this is a direct calibration error. With CRA = 10° the shift is 3.5 µm (1 pixel); with CRA ≈ 0 it is essentially zero.
3. **Filters:** interference filters shift with angle of incidence; a telecentric image space gives every field point the same cone of angles (L08).
4. **Relative illumination:** as argued above, it tends to flatten RI.

### 5.3 The price
- The last group must be at least as large as the image diagonal plus the beam footprint: a 2/3" image (11 mm) needs a rear element of ~14–16 mm clear aperture.
- Total track grows (the stop must sit a focal length in front of the rear group).
- Distortion and pupil aberrations are harder to control; the rear group is a strong positive "field lens" near the image, which also makes the design sensitive to dust on that element.

So real camera lenses aim for a CRA that is "telecentric enough": matching the sensor's CRA curve within a few degrees and keeping the defocus-induced scale change within the calibration budget.

### 5.4 CRA curve matching
The sensor CRA spec is a *curve* (L01): often linear in image height, sometimes non-linear. The lens CRA curve depends on pupil aberrations: real CRA is not exactly $\arctan(h/d_{XP})$ and can even peak at 70–80 % field. Match at several heights, not just the corner.

## 6. In OpticStudio

### 6.1 Relative Illumination analysis
*Analyze → (Image Quality / Illumination group) → Relative Illumination* (location varies by version — search the ribbon). It computes RI vs field by integrating the effective exit-pupil area (projected solid angle) seen from each image point, on a grid in direction-cosine space — the method of Rimmer (1986) ([Zemax Community](https://community.zemax.com/got-a-question-7/how-to-calculate-relative-illuminance-through-integration-1581)). It therefore *includes* vignetting by real apertures, pupil aberrations, distortion and image-plane obliquity. Settings to know:
- **Ray density** — increase until the curve stops changing.
- **Use polarization** (if available in your version) — includes coating/Fresnel transmission; leave it off to see geometry only.
- The analysis uses real clear apertures: set **fixed** semi-diameters (or explicit apertures) on the lens surfaces before trusting it. Automatic semi-diameters grow to pass every ray, which hides vignetting.
- **Remove vignetting factors** (VDX/VDY/VCX/VCY) before evaluating RI and MTF; vignetting factors approximate the clipped beam and shift the chief ray, which can make RI wrong — even *higher* ([Zemax Community](https://community.zemax.com/got-a-question-7/why-vignetting-factors-should-be-removed-when-calculating-relative-illumination-and-mtf-121)). Use ray aiming and real apertures instead.

The merit-function operand **RELI** returns the relative illumination for a given wavelength and field (field number from the field list). Use it as an inequality: e.g. `RELI` at the full-field point with an `OPGT` bound, or target 0.6 with low weight.

### 6.2 CRA and telecentricity operands
- **RAID** — real ray angle of incidence (degrees) at a surface, for normalized field (Hx, Hy) and pupil (Px, Py). With the image surface and Px = Py = 0 it is the CRA. It is an angle magnitude; for a sign-sensitive check use **REAB** (real ray y-direction cosine after the surface, i.e. $\sin$ of the angle to z in the y–z plane for a y-field).
- **RAED** — real ray angle of exitance (after refraction) at a surface; useful inside the lens.
- **RANG** — ray angle with respect to the z axis (radians); the Ansys KA-01552 article uses RANG on the last powered surface to drive the chief ray to zero ([KA-01552](https://optics.ansys.com/hc/en-us/articles/42661811743251)).
- **EXPP** — exit-pupil position relative to the image surface. To force telecentricity, KA-01552 recommends computing EXPP with zero weight and targeting its reciprocal (**RECI**) to zero — numerically better than asking EXPP to become huge.
- A curvature solve on the last powered surface can drive the chief ray angle to zero (also in KA-01552).

**CRA-curve matching recipe** (sensor with linear CRA, 12° at $h_\text{max}$):

```
RAID  surf=IMA  Hx=0 Hy=0.3 Px=0 Py=0   target 3.6   weight 1
RAID  surf=IMA  Hx=0 Hy=0.5 Px=0 Py=0   target 6.0   weight 1
RAID  surf=IMA  Hx=0 Hy=0.7 Px=0 Py=0   target 8.4   weight 1
RAID  surf=IMA  Hx=0 Hy=1.0 Px=0 Py=0   target 12.0  weight 1
```

(If fields are in Real Image Height, Hy is proportional to image height; otherwise convert the sensor curve to your field normalisation first.) In practice a ±tolerance is better than an exact target: use the operand with weight 0 and bound it with `OPGT`/`OPLT` rows referencing it, so the optimizer is free inside the window.

### 6.3 Image-space telecentricity checks
- *System Data / Prescription* reports the exit-pupil position; $d_{XP} \to$ very large ⇒ telecentric.
- Defocus test: shift the image surface ±0.02 mm and compare chief-ray heights (REAY) — the change divided by 0.04 mm is $\tan$CRA.
- OpticStudio's *Image Space Telecentric* flag does not exist as a system setting; *Object Space Is Telecentric* does (System Explorer → Aperture) — that is for L06.

## Worked example — RI and CRA budget for a compact 2/3" lens

**Given:** $f = 8$ mm, rectilinear, F/2.8, 2/3" sensor ($h_\text{max} = 5.5$ mm), exit pupil 12 mm before the image; full-field object angle $\theta = \arctan(5.5/8) = 34.5°$; sensor CRA spec: linear, 15° at the corner, ±3°; focus drift budget ±20 µm.

1. **Natural fall-off:** cos⁴(34.5°) = 0.46 if the lens had no pupil aberration or distortion.
2. **CRA at the corner:** $\arctan(5.5/12) = 24.6°$ → 9.6° above the sensor spec; fails the ±3° window.
3. **Scale error from defocus:** lateral shift at the corner $= 0.020\tan24.6° = 9.2$ µm (2.7 pixels). With the CRA reduced to 10°: 3.5 µm.
4. **What to change:** move the exit pupil back to $d_{XP} \ge 5.5/\tan 18° = 16.9$ mm (to meet 15° − 3° … 15° + 3° at the corner you need $12° \le$ CRA $\le 18°$, i.e. $16.9 \le d_{XP} \le 25.9$ mm). In lens terms: move the stop forward or add a positive rear element that acts as a field lens — at the cost of a larger rear diameter and longer track (L04 project).
5. **Image-space RI:** with $d_{XP} = 20.5$ mm (CRA 15°), image-space $\cos^4(15°) = 0.87$ — the exit-pupil view suggests RI ~0.8–0.9 is reachable with modest pupil aberration, much better than the 0.46 of the object-space cos⁴ estimate. The real RI analysis decides.

## Key takeaways
- cos⁴ is the fall-off of an ideal, distortion-free, unvignetted lens: 0.45 at 35°, 0.25 at 45°.
- RI $= \kappa\cos\theta\,f^2\sin\theta/(h\,h')$: barrel distortion and pupil growth beat cos⁴; vignetting makes it worse.
- RI is best understood as the projected solid angle of the exit pupil from each image point — the quantity OpticStudio integrates.
- Remove vignetting factors and set real apertures before trusting RI or MTF.
- Image-space telecentricity (stop at the front focal plane of the rear optics, $d_{XP}\to\infty$) gives CRA ≈ 0, focus-insensitive scale, filter-friendly angles and flatter RI, at the cost of size.
- Defocus $\delta z$ changes image scale by $\delta z/d_{XP}$ — a calibration error for 3D cameras.
- Match the sensor CRA as a *curve*, with RAID rows (or REAB) bounded by OPGT/OPLT, and use RELI for an RI floor.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Relative illumination (RI) | Off-axis image irradiance / on-axis irradiance for a uniform Lambertian object |
| cos⁴ law | RI of an ideal rectilinear lens without vignetting or pupil aberration |
| Natural vignetting | Older name for cos⁴-type fall-off |
| Mechanical vignetting | Clipping of off-axis beams by lens apertures |
| Pupil aberration / pupil coma | Imperfect imaging of the stop into the entrance/exit pupil, changing the pupil size/shape with field |
| Projected solid angle | $\int\cos\alpha\,d\Omega$ of the exit pupil seen from an image point; proportional to irradiance |
| Image-space telecentric | Exit pupil at infinity, chief rays normal to the image |
| CRA | Chief-ray angle at the image surface |
| Telecentricity error | Residual CRA (deg) or scale change per unit defocus |

## References
1. [Geary §25.7, pp. 282–283] — relative illumination, cos⁴ derivation (Fig. 25.19), effect of vignetting (Figs. 25.20–25.21).
2. [Kidger §10.4, pp. 206–208] — vignetting in triplets, corner illumination.
3. [Kenyon §1.7, pp. 22–25] — radiometric terminology and Lambertian sources.
4. Ansys Optics KB KA-01552, "How to create image-space telecentric lenses" (curvature solve, EXPP+RECI, RANG; object-space telecentric flag): <https://optics.ansys.com/hc/en-us/articles/42661811743251>
5. Zemax Community, "Why vignetting factors should be removed when calculating relative illumination and MTF": <https://community.zemax.com/got-a-question-7/why-vignetting-factors-should-be-removed-when-calculating-relative-illumination-and-mtf-121>
6. Zemax Community, "How to calculate relative illuminance through integration": <https://community.zemax.com/got-a-question-7/how-to-calculate-relative-illuminance-through-integration-1581>
7. Zemax Community, "FAQ about relative illumination": <https://community.zemax.com/got-a-question-7/faq-about-relative-illumination-1006>
8. M. P. Rimmer, "Relative illumination calculations", Proc. SPIE 655 (1986).
9. commonlands, "Lens chief ray angle and mismatch": <https://commonlands.com/blogs/technical/lens-chief-ray-angle-and-mismatch>
