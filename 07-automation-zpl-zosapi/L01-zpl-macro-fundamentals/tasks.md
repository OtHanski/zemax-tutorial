# L01 — Tasks: ZPL macro fundamentals

> Work in `work/` inside this lesson folder. Keep your `.ZPL` files in `work/macros/` under git and copy (or symlink) them into your OpticStudio macro folder to run them. Commit the macros, their output files and a short `work/notes.md` with answers.
> Estimated time: ~4.5 h

Test lenses used below:
- **Singlet:** `../../01-foundations/L07-solves-variables-first-optimization/work/` — your optimized 100 mm F/5 N-BK7 singlet (fields 0/3.5/5°, F-d-C). If you don't have it, rebuild: R1 = 102.7, t = 4, N-BK7, R2 = −102.7, EPD 20 mm, marginal-ray-height solve on the last thickness.
- **Triplet:** `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx` (50 mm, F/4, ±20°).

---

## Task 1 — Hello, lens (OpticStudio + ZPL)
**Goal:** Set up the macro workflow and learn to read lens data.
**Steps:**
1. Find your macro folder (Setup → Project Preferences → Folders; location varies by version). Note its path in `notes.md`.
2. Type `hello_lens.ZPL` from lecture §2 into `work/macros/`, copy it to the macro folder, and run it on the triplet.
3. Extend it: print a header line, then one CSV line per surface: `surf,comment,radius,thickness,glass,semidia,conic`. Use `FORMAT` so numbers have 6 decimals. Write it to a file with `OUTPUT` (full path into your `work/` folder) and switch back with `OUTPUT SCREEN`.
4. Load the CSV in Python (`pandas.read_csv`) and compare against Prescription Data (Analyze → Reports → Prescription Data; location varies by version).
**Deliverable:** `work/macros/lens_table.ZPL`, `work/triplet_table.csv`, a 5-line Python check script.
**Check yourself:** row count = `NSUR()` + 1 (object to image); the stop row agrees with System Data; infinite radii appear as 0 curvature (decide how you print them — `RADI()` of a flat surface returns 0 in many versions, which is a trap: print `CURV()` too).

<details><summary>Hints</summary>

- If a function name is rejected, open *About the ZPL → Numeric/String Functions* and search; names occasionally differ (`$GLASS` vs other spellings).
- Strings in CSV: comments can contain commas — wrap them in quotes or replace commas.
</details>

## Task 2 — Chief-ray table and distortion (ZPL)
**Goal:** Real ray tracing with error checking.
**Steps:**
1. Write `chief_table.ZPL` that, for 21 normalized fields $H_y = 0, 0.05, …, 1$ at the primary wavelength, traces the real chief ray and prints `Hy, y_real, angle_deg_at_image, err, vig`, where the angle is the chief-ray angle (CRA) to the axis in image space: $\theta = \arccos(\text{RAYN}(n_{img}))$.
2. Add the paraxial image height for each field (via `OPEV` of a suitable operand — e.g. paraxial chief-ray height `PARY` at the image surface; check the operand definition and `OPEV` signature in Help) and the distortion in % (lecture worked example (b)).
3. Run on the triplet. Compare the 1.0-field distortion with the Field Curvature/Distortion analysis.
4. Deliberately break it: set a too-small semi-diameter (fixed aperture) on surface 2 and re-run. What do `RAYE()`/`RAYV()` report?
**Deliverable:** `chief_table.ZPL`, output CSV, a matplotlib plot of distortion vs $H_y$, answers in notes.
**Check yourself:** distortion from your macro and the analysis window agree to ≤ 0.01 % if you use the same reference (chief ray, primary wavelength, same field normalization). For a symmetric-ish Cooke triplet at ±20° expect |D| ≲ 1–2 %. In step 4 the clipped rays report a non-zero `RAYV()` equal to the clipping surface.

<details><summary>Hints</summary>

- Field type matters: with Angle fields, $H_y=1$ is the max angle; paraxial height $= f\tan\theta$ only for an infinite object.
- Distortion definitions differ (Field Curvature/Distortion uses the paraxial reference height at the same field; "F-Theta" option is different) — match them before comparing.
</details>

## Task 3 — RMS spot by brute force (ZPL + pen & paper)
**Goal:** Pupil sampling and statistics in ZPL; understand why your number differs from OpticStudio's.
**Steps:**
1. Pen & paper: verify the lecture's four-ray example ($r_\text{RMS}$ = 3.54 µm). Then add a fifth ray at (2, 2) µm: compute the new centroid and RMS radius.
2. Write `rms_spot.ZPL(hy, w, n)` (parameters via variables at the top): square grid $n \times n$ over the pupil, skip $P_x^2 + P_y^2 > 1$, trace, skip failed/vignetted rays (count them), accumulate sums, print centroid, RMS radius, number of rays used.
3. Run on the singlet at $H_y$ = 0 and 1 for n = 11, 21, 41, 81. Time each run (note the wall-clock).
4. Compare with Spot Diagram RMS radius (centroid reference, same wavelength) and with the `RSCE` operand (via `OPEV`).
**Deliverable:** `rms_spot.ZPL`, table (n, RMS, rays, time), comparison with Spot Diagram and RSCE.
**Check yourself:** (step 1) centroid (0.4, 0.4) µm, RMS radius 3.36 µm. (Step 3) the RMS converges as n grows (n = 41 is typically within ~1 % of n = 81); run time scales ~ $n^2$. The Spot Diagram default (hexapolar or square grid) and RSCE (Gaussian quadrature) agree with your converged value to a few percent.

<details><summary>Solution sketch (step 1)</summary>

Points (4,0), (−4,0), (0,3), (0,−3), (2,2): $\bar x = 2/5 = 0.4$, $\bar y = 0.4$; $x^2$: 16, 16, 0, 0, 4 → 36; $y^2$: 0, 0, 9, 9, 4 → 22. $\overline{x^2} + \overline{y^2} = 58/5 = 11.6$; minus $\bar x^2 + \bar y^2 = 0.32$ → 11.28 → **3.36 µm**. Note that adding an off-centre ray moved the centroid, so the RMS is *not* simply the old value combined with the new point's radius.
</details>

## Task 4 — Filter angle-of-incidence map (ZPL, Zivid application)
**Goal:** Compute something no single built-in analysis gives you directly.
**Given:** any of your Course 04 NIR camera lenses with a plane filter plate in image space (e.g. `../../04-machine-vision-camera-lenses/L08-filters-cover-glass-nir-and-ghosts/work/` design), surface comment "FILTER" on the filter's front face. If none: add a 1 mm N-BK7 plate 1 mm before the image of the triplet and re-focus.
**Steps:**
1. Find the filter surface **by its comment** (lecture §4.1; look up string comparison or `SURC`/`SRCN`).
2. For fields $H_y = 0, 0.25, 0.5, 0.75, 1$ and a 15 × 15 pupil grid, compute the AOI on the filter front face from the incoming direction cosine: AOI $= \arccos(\text{RAYN}(s_f - 1))$ in degrees.
3. Print max AOI per field and the overall max. Compare with the S7 limit (24°) of the Course 04 capstone.
4. Explain in two sentences why the maximum AOI is usually a marginal ray at full field, not the chief ray.
**Deliverable:** `filter_aoi.ZPL`, output table, explanation.
**Check yourself:** on axis the max AOI equals the image-space marginal-ray angle, $\arcsin(1/(2F/\#_w))$: at F/2.4 that is 12.0°; at F/4 7.2°. Off axis, max AOI ≈ CRA + cone half-angle (as in the Course 04 capstone worked example).

## Task 5 — Change, update, restore (ZPL)
**Goal:** Modify the lens safely.
**Steps:**
1. Write `focus_scan.ZPL`: find the thickness labelled "FOCUS COMP" (on the triplet, add that comment to the last thickness before the image first), store its value, step it from −0.10 to +0.10 mm in 0.02 mm steps with `SURP` + `UPDATE`, and print `delta, RSCE(on-axis), RSCE(full field)` using `OPEV`.
2. Restore the original thickness and `UPDATE` at the end. Verify by re-opening the LDE that nothing changed.
3. Remove the `UPDATE` line inside the loop and re-run. What happens to the printed numbers? Explain.
**Deliverable:** `focus_scan.ZPL`, output, explanation.
**Check yourself:** with `UPDATE`, the on-axis RMS vs delta is roughly V-shaped with its minimum near 0 (if the lens was focused for RMS). Without `UPDATE` the operand values may not change (or change inconsistently), because the lens wasn't recomputed — the bug from lecture §4.2.

## Stretch task
Write `ray_fan.ZPL` that reproduces the tangential Ray Fan data (ey vs Py for three wavelengths) as CSV and plot it in Python alongside an exported Ray Fan text file (Analyze → Ray Fan → Text tab). Agreement should be exact to printed precision; if it isn't, find out why (reference: chief ray of primary wavelength).

## Reflection questions
1. Name two tasks for which you would *still* choose ZPL after finishing this course, and two for which you would not.
2. Why are `RAYX/RAYY/RAYZ` given in local coordinates, and when does that bite you?
3. Your macro gives a CRA that differs from the RAID operand by a few tenths of a degree at full field. List three possible causes.
4. Why is `GETT()` a poor way to get data into a macro that is called from the merit function?

<details><summary>Answers</summary>

1. Still ZPL: a `ZPLM` operand for a cheap custom quantity; a quick one-off ray table while designing; reading/adapting KB macros. Not ZPL: Monte Carlo post-processing with statistics and plots; million-ray distortion maps; anything that must run unattended in a reproducible pipeline.
2. Each surface has its own coordinate system (after coordinate breaks, tilts and decenters). Local coordinates are what aperture/sag calculations need. It bites with tilted filters, Scheimpflug sensors, fold mirrors: you need global coordinates (or the global-coordinate functions) to compare positions across surfaces.
3. Different wavelength; different medium (angle in glass vs in air — RAID is the angle of incidence relative to the surface normal, not necessarily to the axis); field normalization/ray aiming; RAID uses the normal of a curved or tilted image surface; real vs paraxial chief ray.
4. ZPLM macros run on a temporary copy of the lens; GETT reads whatever text window is open on screen, which isn't updated for that copy. Use OPEV or GETTEXTFILE instead.
</details>
