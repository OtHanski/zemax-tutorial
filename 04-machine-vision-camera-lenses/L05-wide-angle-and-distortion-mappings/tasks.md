# L05 — Tasks: Wide-angle lenses and distortion mappings

> Work in `work/` inside this lesson folder (e.g. save `work/L05_T1_retro_paraxial.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4.5 h

## Task 1 — Retrofocus layout (pen & paper + OpticStudio)
**Goal:** Lay out a two-group retrofocus and see the "wide-angle converter" effect.
**Given / specs:** $f = 4$ mm, BFL = 10 mm (room for a C-mount-like back focus), group separation $d = 8$ mm, stop at the rear group, object at infinity.
**Steps:**
1. Compute $f_1$ and $f_2$ with the thin-lens formulas of §2.1.
2. Paraxially, the chief ray must cross the axis at the rear group. Show that the chief-ray slope between the groups is $u_2 = u_1/(1 - d/f_1)$ and evaluate the ratio.
3. Build it in OpticStudio with two Paraxial surfaces (the second is the stop), field angles 0, 20, 35, 45°, EPD 1.0 mm, λ = 0.55 µm. Save as `work/L05_T1_retro_paraxial.zmx`. Verify EFL and BFL in System Data and the chief-ray angle between the groups with RAED or a Single Ray Trace.
4. Replace the front Paraxial surface by a real N-BK7 negative meniscus (concave toward the stop) of the same focal length and look at the distortion plot. Sign? Size at 45°?

**Deliverable:** numbers, file, two sentences on the distortion you see.
**Check yourself:** $f_1 = -5.33$ mm, $f_2 = 5.71$ mm; ratio $u_2/u_1 = 0.4$: a 45° field arrives at the rear group at $\arctan(0.4\tan45°) = 21.8°$. The real meniscus front adds barrel distortion (negative), typically several percent at 45°.

<details><summary>Hints / solution sketch</summary>

BFL/$f$ = 2.5 → $1 - d/f_1 = 2.5$ → $f_1 = -d/1.5 = -5.333$ mm. Then $1/f = 1/f_1 + (1 - d/f_1)/f_2$ → $0.25 = -0.1875 + 2.5/f_2$ → $f_2 = 5.714$ mm.
Chief ray: $y_2 = y_1 + d u_2 = 0$ and $u_2 = u_1 - y_1/f_1$ ⇒ $u_2 = u_1/(1 - d/f_1)$ = 0.4 $u_1$. The front group is an afocal-like "converter" with angular magnification 0.4 for the stop at the rear group — the same factor 1/2.5 as the retrofocus ratio.
For the meniscus, make the concave side face the stop so that the oblique beams meet both surfaces at moderate incidence; a biconcave lens works paraxially but gives far worse coma and distortion.
</details>

## Task 2 — Mappings and calibration models (Python)
**Goal:** Reproduce the fit-quality table and decide which calibration model to use.
**Steps:**
1. For an ideal f-θ lens ($f = 4$ mm, 3 µm pixels), fit Brown–Conrady radial terms ($k_1$; $k_1,k_2$; $k_1..k_3$) by linear least squares of $r_d - r = k_1r^3 + k_2r^5 + k_3r^7$ with $r = \tan\theta$, for half-fields 30°, 50°, 60°, 70°. Report the maximum residual in pixels.
2. Fit the Kannala–Brandt model $\theta_d = \theta(1 + k_1\theta^2 + \dots)$ to an equisolid lens ($f = 1.59$ mm) out to 90°.
3. Repeat step 1 for a lens with a "wavy" distortion: $r_d = \tan\theta\,(1 - 0.05\,s^2 + 0.08\,s^4 - 0.035\,s^6)$, $s = \theta/\theta_\max$, $\theta_\max = 40°$, $f = 8$ mm, 3.45 µm pixels. Compare with a smooth $r_d = \tan\theta\,(1 - 0.02 s^2)$, which has about *twice* the maximum distortion (−2 % vs −0.95 %).

**Deliverable:** `work/fitmodels.py`, tables, conclusion.
**Check yourself:** step 1 should reproduce ≈ 2.8 / 0.14 / 0.008 px at 30° and ≈ 52 / 8.0 / 1.3 px at 50°; KB with two coefficients fits the equisolid lens to ≈ 0.002 px; step 3: wavy ≈ 9.8 / 5.2 / 1.2 px vs smooth ≈ 3.1 / 0.31 / 0.03 px.

<details><summary>Hints / solution sketch</summary>

Sample θ uniformly (400 points) and use unweighted least squares; your exact residuals will depend slightly on sampling and weighting (real calibrations weight by the number of observed points per radius, which is ∝ $r$). The wavy curve of step 3 has much higher-order content (in $\theta$, and more so in $\tan\theta$), so it needs more coefficients than the smooth one even though its peak distortion is not larger — the reason specs should say "smooth/monotonic", not only "max |D|".
</details>

## Task 3 — Anatomy of a 200° fisheye (OpticStudio)
**Given:** the OpticStudio sample `Wide angle lens 200 degree field` (Sequential samples; find it with the file browser — folder names vary by version). *Save As* `work/L05_T3_fisheye.zos`.
**Steps:**
1. Inspect System Explorer: field type, aperture type, ray-aiming settings. Switch between Robust and Enhanced ray aiming (with/without Advanced Convergence) and note any "cannot determine object coordinates" errors when you add a 102° field.
2. Plot Field Curvature/Distortion with F-Tanθ and with F-θ references. Which is meaningful here?
3. Tabulate real chief-ray image height (REAY) at θ = 0, 10, …, 100°. In Python, compare with $f\theta$, $2f\sin(\theta/2)$, $2f\tan(\theta/2)$, with $f$ = the lens EFL. Which classical mapping is it closest to?
4. Plot Relative Illumination and compare with the ideal RI of the closest mapping (L03 Task 1). Is $\kappa(\theta) > 1$ (pupil growth)?
5. Identify, in the Cross-Section, the front negative menisci and the stop. Note the ratio front-element diameter / stop diameter.

**Deliverable:** file, mapping comparison plot, RI comparison, notes.
**Check yourself:** F-tanθ distortion is meaningless near and beyond 90° (it diverges); F-θ distortion of a few to ~20 % is typical. The front element is many times the stop diameter.

## Task 4 — Distortion stability of your L04 lens (OpticStudio + analysis)
**Goal:** Quantify, in pixels, how the calibration-relevant mapping changes.
**Given:** `../L04-compact-fixed-focus-lens-project/work/L04_S2_final.zmx`. *Save As* `work/L05_T4_stability.zmx`.
**Steps:**
1. Add REAY (image surface, Hy = 0.5, 0.7, 1.0, Px = Py = 0) rows with weight 0.
2. Multi-Configuration: (1) nominal; (2) image plane +20 µm; (3) image plane −20 µm; (4) object at 770 mm; (5) object at 1430 mm; (6) all wavelengths shifted by +10 nm (simulating a different illumination band).
3. For each configuration compute the change of REAY at full field relative to nominal in µm and in pixels (3.45 µm). Which term dominates?
4. Using $d_{XP}$ from EXPP, predict the ±20 µm result as $\delta z\cdot h/d_{XP}$ and compare.
5. Convert the worst term to an equivalent relative focal-length error and to a depth error at 1 m for a triangulation system ($\delta z/z = \delta f/f$).

**Deliverable:** stability table in `notes.md`.
**Check yourself:** with $d_{XP}$ ≈ 12–25 mm (your CRA window from L04), ±20 µm defocus changes the full-field height by ≈ 3.6–7.5 µm (1–2 px). Object-distance changes give much smaller *shape* changes but a scale change through focus; wavelength shifts give sub-pixel changes if lateral colour is corrected.

<details><summary>Hints / solution sketch</summary>

Scale change from defocus: $\delta h = \delta z\,h/d_{XP}$ = 0.020 × 4.5/12 = 7.5 µm (2.2 px) for $d_{XP}$ = 12 mm, 3.6 µm (1.0 px) for 25 mm. As a relative scale: 0.17 % and 0.08 % → depth errors of 1.7 mm and 0.8 mm at 1 m if not compensated. This is why 3D cameras need either a stable focus (athermal mount, L07) or an image-space-telecentric-ish design — or both.
</details>

## Task 5 — Depth error from scale drift (pen & paper)
**Given:** a triangulation camera with $z = 1000$ mm; the receiver lens focal length changes by 12 ppm/K; operating range 15–45 °C, calibrated at 25 °C.
**Steps:** compute the maximum relative depth error and the absolute error at 1 m, assuming no thermal compensation. What would you require of the lens/barrel design?
**Check yourself:** 20 K × 12 ppm/K = 240 ppm → 0.24 mm at 1 m.

## Stretch task
Design (OpticStudio) a 4-element retrofocus with $f = 4$ mm, F/2.8, ±45° field, BFL ≥ 10 mm, for a 1/2.3" sensor, starting from your Task 1 thin-lens layout (two negative menisci in front, a positive group behind the stop with a cemented doublet). Target a smooth barrel mapping between f·tanθ and f·θ, RI ≥ 0.6, and report the Brown–Conrady fit residual of the final mapping with $k_1, k_2$.

## Reflection questions
1. Why do retrofocus lenses have barrel distortion "for free"?
2. When would you deliberately specify an f-θ mapping for a machine-vision camera?
3. A colleague's lens has max |distortion| 0.1 % but the calibration residual at the edge is worse than for a lens with 3 % distortion. How?
4. Why is distortion *stability* more important than magnitude for a 3D camera?

<details><summary>Answers</summary>

1. The front negative group sits far from the stop where the chief ray is high; its distortion contribution is barrel (negative), and it compresses the outer field angles.
2. When the system reasons in angles (ray directions), wants uniform angular resolution, or the field exceeds ~±50°, so that pixels are not wasted and the calibration model is simple (Kannala–Brandt).
3. The 0.1 % lens achieves its small maximum by balancing orders (wavy curve); the residual after a low-order fit is larger than for a smooth 3 % curve that the model represents exactly.
4. Calibration removes whatever static distortion exists; only changes after calibration (focus, temperature, wavelength, mechanics) produce measurement errors.
</details>
