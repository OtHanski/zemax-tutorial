# L03 — Tasks: Relative illumination and telecentricity

> Work in `work/` inside this lesson folder (e.g. save `work/L03_T2_stopshift_cra.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — RI for different mappings (Python)
**Goal:** Make the general RI formula concrete.
**Steps:**
1. Implement `ri(theta, h, dh, kappa=1)` $= \kappa\cos\theta\,f^2\sin\theta/(h\,h')$ (normalise numerically so RI(0) = 1).
2. Evaluate for 0–60° for the mappings $h = f\tan\theta$, $f\theta$, $2f\sin(\theta/2)$ (equisolid), $2f\tan(\theta/2)$ (stereographic), $f\sin\theta$ (orthographic). Plot all on one graph.
3. Derive closed forms for each mapping by hand and check them against your numbers.
4. Add a function `scale_error(dz, cra_deg, h)` returning the lateral shift $dz\tan(\text{CRA})$.

**Deliverable:** `work/ri.py`, the plot, closed forms in `notes.md`.
**Check yourself:** at 30°: rectilinear 0.563, f-θ 0.827; at 45°: 0.250 and 0.637.

<details><summary>Hints / solution sketch</summary>

Closed forms (with $\kappa = 1$): rectilinear $\cos^4\theta$; equidistant $\cos\theta\,\sin\theta/\theta$; equisolid $\cos\theta$ (because $h\,h' = f^2\sin\theta$); stereographic $\cos\theta\cos^4(\theta/2)$; orthographic $1$ (!). The orthographic result shows how strongly the mapping alone controls illumination. L05 returns to these mappings.
</details>

## Task 2 — CRA versus stop position (OpticStudio)
**Goal:** See the exit pupil move and CRA follow, with numbers you can predict.
**Given / specs:** object at infinity; field type Angle, fields 0°, 12°, 24°, 34.51° (34.51° gives 5.5 mm image height at $f = 8$ mm); EPD 2.857 mm; wavelength 0.55 µm; a Paraxial surface with $f = 8$ mm; a separate stop surface a distance $d$ in front of it.
**Steps:**
1. Build OBJ → STO (dummy) → (thickness $d$) → Paraxial ($f = 8$) → (thickness 8 mm, or Quick Focus) → IMA. Save as `work/L03_T2_stopshift_cra.zmx`.
2. Add EXPP and RAID (image surface, Hy = 1, Px = Py = 0) rows, weight 0.
3. For $d$ = 0, 4, 6, 8 mm record EXPP, the CRA at full field, and the image height (REAY).
4. Derive the formula for $d_{XP}$ and CRA as functions of $d$ and confirm.

**Deliverable:** table and derivation in `notes.md`.
**Check yourself:** $d_{XP} = f^2/(f-d)$: 8, 16, 32 mm, ∞; CRA = 34.5°, 19.0°, 9.75°, 0°. The image height stays 5.50 mm for every $d$ (the paraxial surface maps $f\tan\theta$ regardless of stop position).

<details><summary>Hints / solution sketch</summary>

The stop at distance $d < f$ in front of the lens is imaged by the lens to a virtual exit pupil $df/(f-d)$ in front of the lens, so $d_{XP} = f + df/(f-d) = f^2/(f-d)$. The chief ray reaches the lens at height $d\tan\theta$ and goes to $f\tan\theta$ over distance $f$: $\tan\text{CRA} = (f-d)\tan\theta/f = h(f-d)/f^2$. OpticStudio reports EXPP measured from the image surface (sign depends on side); compare magnitudes. Note how large the paraxial lens's semi-diameter must become as $d \to f$: that is the telecentric "price" in its simplest form.
</details>

## Task 3 — Relative illumination of a real lens (OpticStudio)
**Goal:** Learn to trust (or distrust) the RI analysis.
**Given / specs:** your Cooke triplet `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx` (f = 50 mm, F/4, ±20°). *Save As* `work/L03_T3_triplet_ri.zmx`.
**Steps:**
1. With automatic semi-diameters and no vignetting factors, plot Relative Illumination (increase ray density until it converges). Compare with $\cos^4$ of the field angle.
2. Convert all semi-diameters to *fixed* at 90 % of their automatic values (simulating a cheaper, smaller lens). Re-plot RI and the Footprint Diagram on the last surface.
3. Run *Set Vignetting* and re-plot RI. Then *Clear Vignetting* again. Which result is physically right, and why?
4. Tabulate CRA at 0, 0.5, 0.7, 1.0 field (RAID on the image) and EXPP.
5. Defocus test: move the image plane by +0.05 mm, record the change of the full-field chief-ray height (REAY), and compare with $0.05\tan\text{CRA}$.

**Deliverable:** `work/L03_T3_triplet_ri.zmx`, RI curves (described), CRA table, defocus test in `notes.md`.
**Check yourself:** $\cos^4 20° = 0.78$; the unvignetted triplet should be near (often slightly different from) cos⁴; with 90 % apertures the full-field RI drops noticeably. The triplet's CRA at 20° is close to 20° (its exit pupil is near the middle of the lens, far from telecentric). The REAY change should equal $0.05\tan(\text{CRA})$ to within a few %.

<details><summary>Hints / solution sketch</summary>

- The RI analysis traces real rays through real apertures; vignetting factors only approximate the clipped beam and shift the chief ray, which can distort RI (sometimes upward). The "Clear Vignetting + fixed apertures + ray aiming" result is the physical one.
- If RI equals 1.000 everywhere, you probably have the object-space telecentric flag on, or the field type is wrong.
- A CRA near 20° at 18 mm image height means $d_{XP} \approx 18.2/\tan20° \approx 50$ mm — a classic "symmetric" lens has its exit pupil about one focal length from the image.
</details>

## Task 4 — Optimizing for a CRA specification (OpticStudio)
**Goal:** Feel the cost of low CRA.
**Given / specs:** start from `work/L03_T3_triplet_ri.zmx` (semi-diameters back to automatic); requirement: CRA ≤ 10° at full field, ≤ 7° at 0.7 field; keep EFFL = 50 mm, F/4, same glasses.
**Steps:**
1. Add RAID rows (weight 0) for Hy = 0.7 and 1.0 and bound them with `OPLT` rows (or target them directly with modest weight). Keep the default RMS-spot merit function and the EFFL constraint.
2. Make all radii, thicknesses and the stop position variable (keep thickness bounds sensible: centre ≥ 2 mm, edge ≥ 1 mm).
3. Optimize (DLS, then Hammer for a few minutes). Record: total track (TOTR), largest clear aperture, RMS spot per field, distortion, RI at full field.
4. Alternatively try the KA-01552 trick: EXPP with weight 0, RECI of it targeted to 0.

**Deliverable:** before/after table, Cross-Section described, three sentences on the cost of telecentricity.
**Check yourself:** expect the stop to move toward the front and the rear element(s) to grow; total track and rear diameter increase; image quality at full field typically worsens unless you add an element. Full-field RI usually *improves*.

<details><summary>Hints / solution sketch</summary>

Three elements are not enough to be both well corrected and telecentric at ±20°. A professional fix would add a positive field-lens element near the image. The lesson: CRA is a design-form decision made at the start, not a constraint you add at the end.
</details>

## Task 5 — Full flat-field budget (pen & paper)
**Goal:** Combine optical RI with the sensor's angular response.
**Given:** an (illustrative) sensor relative response vs incidence angle: 1.00 at 0°, 0.97 at 10°, 0.90 at 20°, 0.75 at 30° (linear in between). Lens A: corner RI = 0.62 and CRA = 24.6°. Lens B: corner RI = 0.70 and CRA = 15°.
**Steps:** compute the corner signal relative to the centre for both lenses. Which would you choose, and what additional data would you request from the sensor vendor?
**Check yourself:** A: 0.62 × 0.831 = 0.52; B: 0.70 × 0.935 = 0.65.

<details><summary>Hints / solution sketch</summary>

Interpolate: 24.6° → 0.90 − 0.46 × 0.15 = 0.831; 15° → 0.935. Choose B (25 % more corner signal → ~12 % better shot-noise SNR). Ask for angular response at your wavelength (850/940 nm), for both x and y directions (pixel response is often asymmetric), and with the cone of your F/# rather than a collimated beam.
</details>

## Stretch task
Build a ZPL macro or Python (ZOSPy) script that sweeps the stop position of the triplet in 1 mm steps, re-optimizes, and plots CRA(full field), RI(full field), total track and RMS spot vs stop position. You will build such tools properly in Course 07.

## Reflection questions
1. Why can a wide-angle lens have *better* relative illumination than cos⁴ of its field angle?
2. Why should vignetting factors be removed before computing RI and MTF?
3. A 3D camera is calibrated at 20 °C and runs at 45 °C with a 15 µm focus shift. Why does a near-telecentric image space help?
4. Your lens meets the sensor's CRA at the corner but not at 70 % field. Can this happen and why does it matter?

<details><summary>Answers</summary>

1. Barrel distortion compresses the outer image (less area per solid angle) and pupil coma enlarges the oblique entrance pupil ($\kappa > 1$).
2. They approximate the clipped beam by rescaling the pupil, which shifts the chief ray and can over- or under-clip; RI integrates the actual exit-pupil solid angle, so real apertures with ray aiming give the true answer.
3. Defocus changes image scale by $\delta z/d_{XP}$; with $d_{XP}\to\infty$ the calibration (pixel → ray direction) is insensitive to the thermal focus shift.
4. Yes: real CRA curves are non-linear because of pupil aberrations and can peak inside the field. Mismatch at 70 % field affects a large image area (the 70 % zone covers more pixels than the corners).
</details>
