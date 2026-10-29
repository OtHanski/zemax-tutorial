# L05 — Tasks: Distortion

> Work in `work/` inside this lesson folder (e.g. save `work/L05_T2_geary400.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Distortion from Seidel sums and real rays (Python)
**Goal:** Make your Seidel calculator robust and reproduce a published example.

**Given / specs:** Geary's example [Geary §15.4]: N-BK7 ($n_d = 1.5168$) lens, R1 = 799.31 mm, R2 = −277.42 mm, centre thickness 12 mm; stop 151.56 mm in front; EPD 40 mm; object at infinity; field 5°; image at paraxial focus; λ = 587.6 nm.

**Steps:**
1. Add Kidger's alternative distortion formula (lecture §1.3) to `seidel.py` and use it for every surface (check it gives identical results to $(\bar A/A)(S_{III}+S_{IV})$ on the L01 triplet).
2. Compute $S_I \ldots S_V$, $W_{311}$ (waves), the transverse distortion $S_V/(2n'u')$ and $D = S_V/(2H)$.
3. Trace the real chief ray (your meridional tracer from L04 Task 3) and compute the exact distortion at 1°, 2°, 3°, 4°, 5° and 10°. Plot $D(\theta)$ and the third-order prediction $D_3(\theta) = D_3(5°)\cdot(\tan\theta/\tan5°)^2$.
4. Repeat step 2 with the stop at the lens and with the stop 151.56 mm behind the lens (keep the EPD at 40 mm, i.e. the marginal ray enters at 20 mm).

**Deliverable:** updated `work/seidel.py` (copy), `work/distortion.py`, plot, table.

**Check yourself:** EFL 400.01 mm; $S_V = 0.01040$ mm, $W_{311} = 8.85$ waves; $\delta\eta' = -0.104$ mm; $D = -0.297\%$ (barrel); exact chief ray: 34.893 vs paraxial 34.997 mm. Stop at lens: $D \approx -0.02\%$; stop behind: $D \approx +2.27\%$ (pincushion).

## Task 2 — Distortion analyses in OpticStudio (OpticStudio)
**Goal:** Learn the distortion analyses and their reference options.

**Steps:**
1. Enter the Task 1 lens (stop on a dummy surface 151.56 mm in front; Field = Angle 0, 3.5°, 5°; wavelength d). Save `work/L05_T2_geary400.zmx`.
2. Open **Field Curvature/Distortion**; read the distortion at 5°. Switch the distortion reference between F-Tan(θ), F-θ and a calibrated option (if present in your version) and explain each value.
3. Open **Grid Distortion** (increase the field to ±15° for a visible effect). Note the reported maximum distortion and the grid shape.
4. Open **Seidel Coefficients**: which surface contributes most DIST? Why?
5. Add operands to the Merit Function Editor (weight 0, just to read): DIMX, DISG at full field, and REAY / PARY of the chief ray at the image surface. Reproduce the percentage from REAY and PARY.
6. Move the stop behind the lens (151.56 mm, adjust the image distance) and repeat step 2.

**Deliverable:** `.zmx` + `notes.md` table of reported values for each reference.

**Check yourself:** −0.30% at 5° (F-Tan θ) with the front stop; with the F-θ reference the number changes by roughly $+\tan^2\theta/3 \approx +0.25\%$ at 5° (because $f\theta < f\tan\theta$), i.e. the F-θ distortion is only ≈ −0.04%; pincushion of a couple of percent with the rear stop. Surface 2 (R2 = −277 mm, high chief ray, strong curvature) dominates DIST.

<details><summary>Hints</summary>

- PARY = paraxial ray y-coordinate, REAY = real ray y-coordinate; both take surface, wavelength, Hx, Hy, Px, Py. Use Hy = 1, Px = Py = 0 at the image surface.
- If the F-θ reading surprises you, write out $D_{f\theta} = (\eta'_{real} - f\theta)/(f\theta)$ and evaluate with $\theta$ in radians.
</details>

## Task 3 — An f-θ scan lens (OpticStudio)
**Goal:** Design for a *specified* distortion rather than zero distortion.

**Given / specs:** galvo-scanned laser at 850 nm (structured-light line projector / laser marker style). Entrance beam diameter 4 mm; the galvo mirror is the stop, 25 mm in front of the lens. Scan half-angle 20° (one axis is enough: use y-fields 0°, 10°, 15°, 20°). EFL 100 mm. Flat image. One or two N-BK7 (or N-SF11) elements, thickness 4–6 mm.

**Steps:**
1. Start with a plano-convex N-BK7 lens, convex side to the image. Check its F-θ distortion at 20° (should be several %).
2. Variables: curvatures, the lens–image distance, and (optionally) the stop distance. Merit function: default RMS spot (wavelength 0.85 µm, centroid) + EFFL = 100 + DISG or a custom chief-ray-height constraint at each field so that $\eta' = f\theta$ (REAY targets: 17.453 mm at 10°, 26.180 mm at 15°, 34.907 mm at 20°).
3. Optimise. If one element is not enough, split it into a meniscus + positive pair.
4. Report: f-θ linearity error (%) vs field, RMS spot vs Airy radius ($1.22\lambda N$ with $N = 100/4 = 25$ → 25.9 µm), and the image-surface curvature (Field Curvature plot).

**Deliverable:** `work/L05_T3_ftheta.zmx`, short report.

**Check yourself:** the target heights are $f\theta$: $100\times(10°, 15°, 20°$ in rad$) = 17.453, 26.180, 34.907$ mm. A meniscus concave toward the galvo is the classic single-element answer. At this slow F/25 beam the spot can be near diffraction-limited across the scan with one or two elements; f-θ linearity well below 1% is achievable — field curvature is usually the harder residual.

## Task 4 — From lens design to calibration coefficients (Python)
**Goal:** Connect design distortion to the $k_1, k_2$ of calibration models.

**Steps:**
1. Using your Task 1 real-ray data (or OpticStudio's distortion text output) for the Geary lens at fields 0–15° (stop in front), fit $D(r) = k_1r^2 + k_2r^4$ with $r = \tan\theta$.
2. Compare $k_1$ with the Seidel prediction $k_1 \approx D_3/\tan^2\theta$.
3. Do the same for the L01 Cooke triplet (`../L01-wavefront-and-transverse-aberrations/work/L01_T2_kidger_triplet.zmx`, fields 0–20°). Which lens needs $k_2$?
4. In two sentences: what would you put in a lens specification for a calibrated 3D-camera lens regarding distortion?

**Check yourself:** Geary lens: $k_1 \approx -0.00297/\tan^2 5° = -0.388$ (third-order); the real-ray fit should give a similar $k_1$ and small $k_2$. The triplet at 20° has noticeable higher-order distortion (from L01: Seidel +0.73% at 20°); compare it to OpticStudio's real value.

## Reflection questions
1. Why is distortion invisible in a spot diagram referenced to the chief ray?
2. Why does a symmetric lens lose its zero-distortion property when used with an object at infinity?
3. A customer asks for "< 0.05% distortion" on a 90° FOV machine-vision lens. What would you ask them back?
4. Why should a structured-light projector lens be stable in distortion versus temperature, even if its absolute distortion is calibrated?

<details><summary>Answers</summary>

1. Distortion is a pure tilt of the whole wavefront for that field point — all rays shift together, so relative to the (real) chief ray there is no spread.
2. Symmetry cancels odd aberrations exactly only if the ray paths in the two halves mirror each other, which requires $m=-1$; at infinite conjugates the front half works from infinity and the rear half to a finite image, so the chief-ray paths are no longer mirror images and the cancellation is only partial.
3. Whether they calibrate (then smoothness, stability and low-order description matter more than the absolute value); which mapping is meant (rectilinear at 90° FOV costs elements and relative illumination); over which wavelength band and focus range; and whether "calibrated" or paraxial reference.
4. The calibration is a snapshot: a temperature-induced change in focal length, element spacing or decentre changes the mapping, which directly biases the triangulated depth; stability (athermal design, Course 03 L09) is what preserves accuracy.
</details>
