# L10 — Tasks: Capstone — receiver lens for a structured-light 3D camera

> Work in `work/` inside this lesson folder. The final design **must** be saved as `work/capstone.zmx` (text .zmx) — Course 06 L08 and Course 07 L08 start from it. Keep versions (`work/capstone_v01.zmx`, …) under git with one-line commit messages stating the merit-function value and what changed.
> Estimated time: ~16–20 h (Session A: Tasks 1–3; Session B: Tasks 4–5; Session C: Tasks 6–7).

The specification is §1.3 of the lecture notes (S1–S19). Do not edit it silently: record deviations in `work/deviations.md`.

---

## Task 1 — Specification and budget sheet (Python + writing)
**Goal:** A spec you can defend line by line.
**Steps:**
1. Copy the spec into `work/spec.md`. For every line add: origin (sensor, projector, mechanics, calibration, environment), derivation (formula + numbers), verification method.
2. With your course tools (`sensor.py`, `camera.py`, `ri.py`, filter and depth-noise scripts from L01–L09), compute and tabulate: FOV and object pixel at 0.6/0.8/1.2 m; range-end defocus and blur; diffraction × defocus MTF at 18.1/36.2/72.5 lp/mm; $d_{XP}$ needed for CRA 8° and 12°; filter AOI budget; filter centre/FWHM proposal for the LED (L08 Task 5 method); depth noise at 0.6/1.0/1.2 m for $\delta d$ = 0.05 and 0.1 px.
3. Add a "photon budget" paragraph: what irradiance at the sensor gives SNR 50 at 1 ms with QE 0.3 at 850 nm (L01)?

**Deliverable:** `work/spec.md` v1.0.
**Check yourself:** FOV at 0.6 m 625 × 523 mm; blur at range ends 11.3 µm; perfect-lens MTF at 36.2 lp/mm at range ends 0.73; $d_{XP}$ ≥ 39.1 mm (8°) / 25.9 mm (12°); depth noise at 1 m 0.144 mm ($\delta d$ = 0.05 px).

<details><summary>Hints / solution sketch</summary>

Photon budget: SNR 50 with read noise ~3 e⁻ needs ≈ 2509 e⁻ → 8363 photons at QE 0.3; one 3.45 µm pixel, 1 ms, 850 nm: $E = N_\gamma hc/(\lambda p^2 t) = 8363\cdot2.337\times10^{-19}/(1.19\times10^{-11}\cdot10^{-3}) \approx 0.16$ W/m². Compare with the projector's delivered irradiance (Course 05) — that comparison is the system-level check for F/2.4.
</details>

## Task 2 — Form study (pen & paper + OpticStudio paraxial)
**Goal:** Choose the design form from first-order properties.
**Steps:**
1. Sketch two candidate forms: (A) front negative meniscus + stop + positive core with one cemented doublet + positive rear field element (5–6 elements); (B) a double-Gauss derivative with a rear positive field element.
2. Model each with Paraxial surfaces (one per group) in OpticStudio: EFL 8 mm, F/2.4, object 800 mm, fields to 5.7 mm. Adjust group powers and spacings to meet EFL, BFL ≥ 4 mm (plus filter and cover glass as real plates), CRA ≤ 8° at 5.5 mm, TTL ≤ 30 mm.
3. Tabulate for each: group powers, exit-pupil distance, rear-group clear diameter, front-group clear diameter, Petzval sum estimate (thin lens, assumed glass indices).
4. Choose one; write the rationale (half a page).

**Deliverable:** `work/capstone_paraxial_A.zmx`, `work/capstone_paraxial_B.zmx`, comparison table, decision.
**Check yourself:** a low-CRA solution needs the stop in the front half and a strong positive rear group; expect rear clear diameters of ~13–16 mm (image circle 11.4 mm plus beam) — check against the Ø 16 mm limit early.

## Task 3 — Starting point and first optimization (OpticStudio)
**Steps:**
1. Replace the paraxial groups by real glass elements (start with thin-lens bendings from Course 02 rules, or adapt a patent/sample with a similar form; scale to f = 8 mm).
2. Build the full system: object at 800 mm (config 2), configs for 600 and 1200 mm, wavelengths S4, filter and cover glass, Real Image Height fields 0/1.7/2.85/4.0/5.1/5.7 mm, ray aiming on.
3. Build the merit function per lecture §2.2 (blocks 1–5). Use ramping (start F/3.5, 4.0 mm image height).
4. Optimize to a first feasible design; save `work/capstone_v01.zmx`.

**Deliverable:** v01 file, stage log in `work/notes.md`.
**Check yourself:** at v01 you should have EFL, TTL, BFL and CRA under control and image quality within a factor ~2 of the spec; if CRA and BFL fight constantly, revisit the form (Task 2).

<details><summary>Hints / solution sketch</summary>

- Keep the image distance (or the gap before the filter) as a single focus variable shared by all configurations — the camera is fixed-focus.
- If RAID constraints dominate the merit function, check that the rear element has enough positive power and that the stop is not drifting rearward; temporarily constrain the stop position.
- The 835–865 nm band is narrow; colour correction is mostly about lateral colour at the field edge (S15).
</details>

## Task 4 — Full optimization (OpticStudio)
**Steps:**
1. Ramp to F/2.4 and the full field. Add the filter-AOI constraint (S7), RI (S11), distortion (S12), mechanics (S17).
2. Hammer/Global for 30–60 min; try at least one glass substitution run (constrained to your vendor and to good climate resistance).
3. Polish with MTF operands at 36.2 lp/mm in configs 1 and 3 and at 72.5 lp/mm in config 2.
4. Save `work/capstone_v02.zmx` (and further versions).

**Deliverable:** best design, merit-function history.
**Check yourself:** a successful design meets S1–S12 and S15, S17–S18 with margins; S8 at the range ends is usually the tightest image-quality line.

## Task 5 — Full analysis set vs spec (OpticStudio + Python)
**Steps:** produce the evidence for every spec line:
1. Layout, Prescription Data (glass list, clear apertures).
2. FFT MTF vs field at 36.2 and 72.5 lp/mm for configs 1–3; through-focus MTF at 36.2 lp/mm; spot diagrams.
3. Field Curvature/Distortion; REAY table at 20 field points → Python Brown–Conrady fit ($k_1,k_2$) and residual in pixels (S12).
4. Relative Illumination (fixed apertures, no vignetting factors) (S11).
5. CRA vs image height (RAID) against the sensor spec (S10); filter AOI map (RAID at the filter for chief and marginal rays) and resulting spectral shifts per field (L08 code) (S7).
6. Lateral colour (S15).
7. Focus stability: configs with ±15 µm image shift; REAY change at full field in pixels (S13).
8. Thermal: TEMP configurations 0 and 45 °C with aluminium barrel; best-focus shift and EFL change (S14).
9. Ghosts: Ghost Focus Generator double-bounce; top-5 list; relative irradiance of the worst image ghost (S16).
10. Sensitivity preview: default tolerances, sensitivity mode, criterion MTF at 36.2 lp/mm, compensator = focus (S19).

**Deliverable:** `work/analysis/` with saved outputs/screenshots and an evidence table (spec line → result → PASS/FAIL → margin).

## Task 6 — Design report and review
**Steps:**
1. Write `work/capstone_report.md` following the template in lecture §3 (≤ 6 pages plus appendix).
2. Hold a review: give the report (not the file) to a colleague — or, if working alone, wait three days and review it yourself with this checklist:
   - Every spec line has evidence; every number in the report can be regenerated from `capstone.zmx`.
   - The deviation list is honest and has proposals.
   - The first-order derivations agree with the final file (EFL, F/#, FOV, CRA).
   - The report states what is *not yet* known (tolerances, stray light from mechanics, coating designs).
3. Record review findings and your responses in `work/review.md`.

## Task 7 — Hand-off (OpticStudio)
**Steps:**
1. Apply the conventions of lecture §4: surface comments, configuration order, "FOCUS COMP" label, dashboard rows with comments at the top of the MFE.
2. Save as `work/capstone.zmx` (text). Open it in a fresh OpticStudio session to verify that it loads with all catalogues (if you used non-default catalogues, also save a `.zar` archive).
3. Write `work/HANDOFF.md`: file list, configuration meanings, compensator, operand rows that scripts will read, known issues.

**Deliverable:** `work/capstone.zmx`, `work/HANDOFF.md`.

## Stretch tasks
1. **Visible variant:** re-optimize for 0.45–0.65 µm (colour texture camera) with the same mechanics; what breaks first?
2. **Hybrid aspheric variant:** replace two glass elements with one precision-molded glass asphere (L07 stretch); quantify element-count saving vs sensitivity.
3. **Depth-noise map:** combine your MTF results (Task 5) with the L09 phase-noise model to produce a predicted depth-noise map over the field at 0.6/0.8/1.2 m.

## Reflection questions
1. Which spec line constrained the design most, and would you push back on it with the system architect? With what argument?
2. Which robustness check (focus, thermal, ghosts, sensitivity) gave you the biggest surprise?
3. If you could change one system input (sensor, F/#, baseline, wavelength, volume), which would improve 3D performance most per unit cost?
4. What will the tolerancing engineer (Course 06 L08) worry about first when opening your file?

<details><summary>Guidance</summary>

There are no unique answers. Strong answers quantify: e.g. "S10 (CRA ≤ 8°) forced a Ø 15.6 mm rear element and cost 0.08 MTF at the range ends; relaxing to 12° would allow … at the price of a 3 nm wider filter". A good capstone is judged by the traceability from requirement to evidence, not only by the MTF numbers.
</details>
