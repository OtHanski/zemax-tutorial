# L04 — Tasks: Project — compact fixed-focus machine-vision lens

> Work in `work/` inside this lesson folder. Save each stage as a separate file (`work/L04_S1_triplet_f8.zmx`, `work/L04_S1_ramped.zmx`, `work/L04_S2_final.zmx`, …) so you can go back. Commit after every task with a one-line message saying what changed and the merit-function value.
> Estimated time: ~10–12 h over **two sessions** (Session 1: Tasks 1–3; Session 2: Tasks 4–6).

The specification is §1.1 of the lecture notes. Do not change it silently: if you decide a requirement is impossible, write a "spec deviation" note with the evidence.

---

# Session 1 — Spec, first order and a working starting point

## Task 1 — Spec sheet and first-order check (pen & paper + Python)
**Goal:** Own the spec before designing.
**Steps:**
1. Copy the spec table into `work/spec.md`. For each line add the *reason* (sensor, application, mechanics) and the *verification method* (which analysis/operand).
2. Using `camera.py` (L02), compute: EPD, field angle, object field at 0.77/1.0/1.43 m, image shift from infinity to 1 m, depth of field at $c = p$ and $2p$, diffraction MTF at 72 and 145 lp/mm for 0.486/0.588/0.656 µm.
3. Compute the allowed exit-pupil distance window from the CRA spec.
4. Add a "sensor interface" section from your L01 Task 5 table (cover glass thickness/index from a real datasheet if you have one; otherwise 0.50 mm N-BK7).

**Deliverable:** `work/spec.md` (version 1.0).
**Check yourself:** EPD 2.857 mm; $\theta_\max$ 29.4°; field at 1 m 876 × 657 mm; image shift 0.065 mm; diffraction MTF at 0.588 µm 0.85 / 0.70; $d_{XP}$ window 12.1–25.1 mm.

<details><summary>Hints / solution sketch</summary>

Diffraction MTF at 72 lp/mm: 0.87 (0.486 µm), 0.85 (0.588 µm), 0.83 (0.656 µm). At 145 lp/mm: 0.75, 0.70, 0.67. DOF at focus 1 m, F/2.8: $c = p$: 870–1176 mm; $c = 2p$: 770–1427 mm (focus distance measured from the front principal plane — note the difference to "first vertex" in the spec; a few mm only).
</details>

## Task 2 — Scaled triplet starting point (OpticStudio)
**Goal:** Get a working, correctly-modelled system with the full back-focus stack.
**Given:** your `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx`.
**Steps:**
1. *Save As* `work/L04_S1_triplet_f8.zmx`. Scale to EFL 8 mm (Make Focal / Scale Lens).
2. Set object distance 1000 mm, EPD 2.857 → start at **F/4 (EPD 2.0 mm) and 20°** object-angle fields (0, 10, 14, 20°), wavelengths F, d, C with weights 1:2:1, paraxial ray aiming on.
3. Replace the back focus by: variable air (≥ 1.5 mm) → IR filter 0.30 N-BK7 → 0.50 air → cover glass 0.50 N-BK7 → 0.40 air → IMA.
4. Build the merit function of lecture §3.3 (all three blocks + dashboard). Initially make only radii and the focus air gap variable; then thicknesses.
5. Optimize. Record merit function, RMS spots per field, TOTR, CRA at full field, distortion.

**Deliverable:** `work/L04_S1_triplet_f8.zmx`, a stage log in `work/notes.md`.
**Check yourself:** the scaled F/4 ±20° triplet should give RMS spots of a few µm (≈ 2–6 µm), i.e. near Airy size, TOTR well under 20 mm, CRA at full field close to the field angle (~18–22°).

<details><summary>Hints / solution sketch</summary>

If Make Focal changes the plate thicknesses too, reset them to 0.30/0.50/0.40 afterwards. Check that the stop remains on/near the negative element. If the optimizer drives the focus gap to the 1.5 mm limit, that is fine — compactness usually wants it there.
</details>

## Task 3 — Aperture and field ramping; see where the triplet fails (OpticStudio)
**Steps:**
1. Ramp (F/3.5, 24°) → (F/2.8, 29.4°), re-optimizing (DLS, then 5–10 minutes Hammer) at each step. Save `work/L04_S1_ramped.zmx`.
2. Evaluate against the spec: MTF at 72 lp/mm (T and S) per field, distortion, CRA, RI, TOTR.
3. Open the Seidel Diagram. Which aberration and which surfaces limit the full-field performance?
4. Decide the next form (Tessar, triplet + flattener, 5-element double-Gauss derivative, or "front-stop" form) and write two sentences of justification.

**Deliverable:** spec-vs-achieved table for the triplet, form decision in `notes.md`.
**Check yourself:** typically the triplet at F/2.8 ±29° meets the on-axis MTF but falls below 0.30 at 72 lp/mm toward 0.7–1.0 field (astigmatism/field curvature, lateral colour), and its CRA (≈ 25–30°) exceeds 20°.

---

# Session 2 — Better form, constraints, analysis, report

## Task 4 — Grow the design (OpticStudio)
**Goal:** Meet the specification with 4–6 spherical glass elements.
**Steps:**
1. Implement your chosen form. Suggested routes:
   - **Tessar**: replace the rear element by a cemented doublet (e.g. N-SK16 + F2 or N-LAK9 + N-SF5), optimize.
   - **Front-stop-shifted five-element**: move the stop in front of element 2, add a positive meniscus near the image to pull the exit pupil away (CRA) — watch Petzval.
   - **Double-Gauss derivative**: start from a sample (`Samples\Sequential\Objectives\Double Gauss 28 degree field.zmx`), scale to 8 mm, add the back-focus stack, ramp field to 29.4°.
2. Add the CRA window (±5° around the linear sensor curve) with RAID + OPGT/OPLT, `DIMX` ≤ 2 %, `RELI` ≥ 0.5 at full field, mechanical constraints (centre/edge thickness, air gaps, semi-diameter ≤ 5.5 mm).
3. Switch fields to Real Image Height (0, 1.35, 2.25, 3.15, 4.05, 4.5 mm) and ray aiming to Real. Re-optimize. Consider adding MTF operands (MTFT/MTFS at 72 lp/mm, low weight) in the final polish.
4. Run Hammer/Global for 15–30 minutes with the full merit function. Save `work/L04_S2_final.zmx`.

**Deliverable:** final lens file and stage log.
**Check yourself:** a successful design has 4–6 elements, TOTR 17–20 mm, MTF at 72 lp/mm ≥ 0.3 to 0.9 field, distortion |≤ 2 %|, RI ≥ 0.5, CRA 10–20° at the corner. If you cannot meet all at once, the CRA and the 0.9-field MTF are the usual conflicts — document the trade.

<details><summary>Hints / solution sketch</summary>

- Use `MNCT`/`MXCT` and `MNET` (or the Wizard's glass/air boundary constraints) and check edge thickness in the Prescription Data or with the ETGT/MNET operands.
- Lateral colour at 4.5 mm image height should end up below ~3 µm (1 pixel); if it dominates, the stop is too asymmetric or you need a cemented doublet on the side opposite the dominant lateral-colour contributor.
- If CRA is fine but RI is low, check that apertures are fixed and vignetting factors are cleared (L03) — and look at the footprint on the front element.
- Do not chase the last 0.01 of MTF in the corner: tolerances (Course 06) will eat it. Prefer designs with smaller angles of incidence on surfaces (lower sensitivity).
</details>

## Task 5 — Analysis set (OpticStudio)
**Steps:** produce the 15 analyses of lecture §4. For #8 set up a Multi-Configuration with object distances 770, 1000, 1430 mm (no refocus) and report MTF at 72 lp/mm on axis and at 0.7 field. For #12 produce a table of lens CRA vs sensor CRA at 0, 25, 50, 75, 100 % of 4.42 mm.
**Deliverable:** `work/analysis.md` with each analysis described in one or two lines (and screenshots if you like, saved in `work/`).
**Check yourself:** MTF at 72 lp/mm at 770 and 1430 mm should drop to roughly 60–80 % of the 1000 mm value (defocus ≈ ±25 µm image-side at F/2.8 is ~±2.5 depths of focus).

<details><summary>Hints / solution sketch</summary>

Image-side defocus: $v(770) - v(1000) = 8\cdot770/762 - 8\cdot1000/992 = 8.0840 - 8.0645 = 0.0195$ mm; $v(1000)-v(1430) = 8.0645 - 8.0451 = 0.0194$ mm. Blur disc ≈ 19.5/2.8 ≈ 7 µm ≈ 2 pixels — consistent with $c = 2p$ in the DOF calculation.
</details>

## Task 6 — Design report (writing)
Write `work/report.md` following lecture §5: spec-vs-achieved table with margins, layout, prescription, key curves, design rationale, risks. Maximum two pages plus appendix. Ask a colleague (or your future self in a week) to review it against the spec without opening OpticStudio.

## Stretch tasks
1. **Thermal focus**: set up a two-configuration thermal analysis (Course 03 L09) at −10 and +50 °C with an aluminium barrel (CTE ≈ 23.6 × 10⁻⁶ /K) and compute the focus shift. Is it within ±10 µm?
2. **NIR variant**: change wavelengths to 0.84/0.85/0.86 µm, remove the IR-cut filter (replace by an NIR bandpass of the same thickness), refocus and re-optimize. What happens to MTF at 72 lp/mm and to lateral colour? Keep this file: L08 and L10 use the idea.

## Reflection questions
1. Why did ramping the aperture and field help the optimizer?
2. Which spec line drove your choice of form more: MTF, CRA or track length? Why?
3. Why can a well-corrected lens at 8 mm focal length be impossible to make at 50 mm with the same F/# and field?
4. List three items you would add to the spec for production (Course 06 preview).

<details><summary>Answers</summary>

1. DLS is local; a gradual change keeps the solution in the basin of a good form instead of jumping to a distorted local minimum or failing ray traces.
2. Usually CRA together with track: they fix the stop position and the rear-group power, which then limits what is possible for astigmatism and lateral colour.
3. Geometric aberrations scale with size while the resolution requirement (in lp/mm on the sensor) does not; at 50 mm the same aberration coefficients produce 6× larger blur.
4. Tolerances and as-built MTF yield; focus/assembly method (active alignment, thread focus); ghost/flare requirements; coating spec (reflectance per surface); environmental (temperature, humidity, vibration); cost/glass availability.
</details>
