# L06 — Tasks: Telecentric metrology lenses

> Work in `work/` inside this lesson folder (e.g. save `work/L06_T3_bitele_paraxial.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4.5 h

## Task 1 — Perspective vs telecentric error (pen & paper)
**Goal:** Feel the size of perspective error.
**Given:** a gauging task: measure the diameter (nominally 20 mm) of parts whose height on the conveyor varies by ±1.5 mm.
**Steps:**
1. Entocentric lens with the entrance pupil 250 mm from the part: what is the diameter error range?
2. Telecentric lens with slope $\theta_t = 0.08°$ at the edge of the part (worst case, both edges sloping outward): what is the error range of the measured *diameter*?
3. What slope would you need for ±2 µm diameter error?

**Check yourself:** (1) ±0.12 mm (±0.6 %); (2) ±4.2 µm; (3) ≤ 0.038°.

<details><summary>Hints / solution sketch</summary>

1. $\delta D/D = \delta s/s = 1.5/250 = 0.6\,\%$ → ±0.120 mm.
2. Each edge moves by $\delta s\tan\theta_t = 1.5\tan0.08° = 2.09$ µm; if both edges slope outward, the diameter changes by twice that: ±4.2 µm.
3. $2\cdot1.5\tan\theta_t \le 0.002$ mm → $\tan\theta_t \le 6.7\times10^{-4}$ → 0.038°.
</details>

## Task 2 — First-order bi-telecentric design (Python)
**Goal:** Size a gauging lens from requirements and see the NA conflict.
**Given:** sensor B (7.07 × 5.30 mm, 3.45 µm), $|m| = 0.5$, λ = 0.55 µm, required depth of field ≥ 0.5 mm total with $c = 2p$; working distance ≈ 120 mm.
**Steps:**
1. Compute the object field. Then compute the *minimum* working F/# $N_w$ (i.e. the maximum object-side NA) that still gives the required DOF.
2. Compute the Airy radius on the object and compare with the object-space pixel; compute diffraction MTF at the sensor Nyquist.
3. Choose $f_1 = 120$ mm, $f_2 = 60$ mm. Compute thin-lens length, stop diameter, front-lens minimum diameter.
4. Write two sentences: can this lens resolve one pixel *and* hold 0.5 mm DOF? What would you change?

**Check yourself:** field 14.1 × 10.6 mm; $N_w = 9.06$, NA = 0.0276; Airy radius 12.2 µm on the object vs 6.9 µm object pixel; MTF at Nyquist ≈ 0.17; length 360 mm; stop Ø 6.6 mm; front lens ≥ 24.3 mm.

<details><summary>Hints / solution sketch</summary>

$N_w = \text{DOF}\,m^2/(2c) = 0.5\cdot0.25/(2\cdot0.0069) = 9.06$; NA $= m/(2N_w) = 0.0276$. Diffraction at $N_w = 9.06$: $s = 145\cdot0.55\times10^{-3}\cdot9.06 = 0.72$ → MTF ≈ 0.17. The lens cannot deliver full-pixel resolution over 0.5 mm depth; either relax DOF (fixture the parts better), accept ~2-pixel edge resolution (sub-pixel edge fitting still gives µm-level repeatability), or use larger pixels / lower magnification.
</details>

## Task 3 — Paraxial bi-telecentric in OpticStudio
**Goal:** Build, verify and break telecentricity.
**Given / specs:** two Paraxial surfaces $f_1 = 200$ mm and $f_2 = 50$ mm, separated by 250 mm with the stop at 200 mm behind lens 1; object 200 mm in front of lens 1; Object Height fields 0, 11, 22 mm; λ = 0.55 µm.
**Steps:**
1. Build OBJ → (200) → Paraxial f=200 → (200) → STO → (50) → Paraxial f=50 → (50) → IMA. Set *Object Space Is Telecentric* and aperture *Object Space NA* = 0.02. Save as `work/L06_T3_bitele_paraxial.zmx`. Check PMAG and image distance.
2. Turn the telecentric flag **off**, set aperture to *Float By Stop Size* with stop semi-diameter 4 mm. Confirm that the chief rays in object space are still parallel (RANG on surface 1 or RAED on surface 0, Hy = 1).
3. Multi-Configuration: object thickness 199, 200, 201 mm (no refocus). Record REAY at Hy = 1. Then also move the image plane ±0.05 mm. What changes?
4. Now move the stop 5 mm toward lens 2 (keep the total spacing 250 mm). Predict the object-space chief-ray angle at H = 22 mm and the REAY change for ±1 mm object displacement, then measure.

**Deliverable:** file, tables, predictions vs measurements.
**Check yourself:** PMAG = −0.25; REAY unchanged (to numerical noise) for object ±1 mm and for image ±0.05 mm when the stop is at the common focus. With the stop 5 mm off: entrance pupil $f_1^2/\delta = 8000$ mm from the front focal plane; slope ≈ 22/8000 rad = 0.158°; object-scale shift 2.75 µm per mm, i.e. REAY changes by ≈ 0.69 µm per mm (×0.25).

<details><summary>Hints / solution sketch</summary>

Newton's equation for lens 1: a stop at $x' = \delta$ beyond the rear focal point images to $x = -f_1^2/\delta$ before the front focal point. The object sits in the front focal plane, so the chief ray from height $H$ points at (or away from) a pupil 8 m away: angle $H/8000$. Whether the image grows or shrinks with displacement depends on the side to which you moved the stop — check the sign in your table. Moving the stop also breaks image-space telecentricity (stop no longer at the front focal point of lens 2).
</details>

## Task 4 — A real bi-telecentric with cemented doublets (OpticStudio)
**Goal:** See what pupil aberrations do to telecentricity.
**Steps:**
1. Replace each Paraxial surface by a cemented doublet (N-BK7 crown + N-SF5 flint as a starting pair; start with the crown facing the stop-distant side) with the same focal length. Get a first shape from a quick optimization of each doublet alone (object at infinity, f = 200 and f = 50).
2. Assemble with the stop at the common focus, object-space NA 0.02, fields 0, 11, 15.5, 22 mm, wavelengths F, d, C.
3. Merit function: default RMS spot; PMAG = −0.25; telecentricity: RAED (or RANG) of the chief ray leaving the object surface at Hy = 0.7 and 1.0 targeted to 0; image-side RAID at Hy = 0.7 and 1.0 targeted to 0; DIMX ≤ 0.1 %.
4. Optimize; report telecentric slope per field and wavelength (object and image side), distortion, MTF at 145 lp/mm on the sensor, and the multi-configuration REAY change for ±1 mm.
5. Save as `work/L06_T4_bitele_doublets.zmx`.

**Check yourself:** with only two doublets, residual object-side slopes of a few hundredths of a degree and distortion below ~0.1–0.3 % are realistic; slopes differ between F, d and C (pupil lateral colour) — exactly the colour dependence Edmund warns about.

<details><summary>Hints / solution sketch</summary>

If the optimizer kills telecentricity to improve spots, raise the telecentricity weights or turn them into hard constraints with OPLT/OPGT bands (e.g. |slope| < 0.05°). The stop-side curvatures of both doublets control pupil spherical aberration; the outer curvatures control field aberrations. Expect field curvature to be the main residual — a bi-telecentric made of two positive groups has an uncorrected Petzval sum.
</details>

## Task 5 — Where telecentric optics fit in a 3D-camera company (analysis)
Write half a page in `notes.md`: (a) why a structured-light 3D camera for bin picking cannot use a telecentric receiver; (b) three places in development or production where a telecentric lens is the right tool (e.g. measuring a projector mask/DOE pattern, gauging a lens barrel, a calibration-target inspection station); (c) what you would specify for one of them (field, $m$, NA, DOF, slope, distortion).

## Stretch task
Design an image-space-only telecentric C-mount lens (f = 25 mm, F/4, 2/3" sensor) and compare its scale sensitivity to sensor defocus with your L04 lens. Use KA-01552's EXPP + RECI method.

## Reflection questions
1. Why must the front lens of an object-space telecentric lens be larger than the object field?
2. Why is magnification of a bi-telecentric lens independent of sensor position, while an object-space-only telecentric lens's is not?
3. Why is object-side NA, rather than F/#, the natural aperture spec for gauging lenses?
4. What does a wavelength-dependent telecentric slope mean for the choice of illumination?

<details><summary>Answers</summary>

1. Chief rays are parallel to the axis, so the beam from each object point reaches the front lens at the same height as the point; the lens must span the field plus the cone footprint.
2. In the bi-telecentric lens image-side chief rays are parallel to the axis, so defocusing the sensor does not move chief-ray positions; with an object-only telecentric lens they arrive obliquely and the image scale changes with sensor position.
3. The object field, DOF and object-space resolution are all set by NA and $m$; F/# at infinity is meaningless when the entrance pupil is at infinity.
4. Measurements depend on the colour; use narrow-band (monochromatic) illumination at the design wavelength, as Edmund recommends.
</details>
