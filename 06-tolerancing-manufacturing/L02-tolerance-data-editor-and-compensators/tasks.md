# L02 — Tasks: The Tolerance Data Editor, compensators and criteria

> Work in `work/` inside this lesson folder (e.g. `work/L02_m12_tol.zmx`). Commit your files and a short `work/notes.md` with answers.
> Estimated time: ~5 h
> Practice lens for L02–L04: your Course 04 fixed-focus lens `../../04-machine-vision-camera-lenses/L04-compact-fixed-focus-lens-project/work/L04_S2_final.zmx` (EFL ≈ 8 mm, F/2.8, image height 4.5 mm, spec MTF at 72 lp/mm). The Course 04 capstone is reserved for L08.

## Task 1 — Prepare the file (OpticStudio)
**Goal:** A lens file that tolerances honestly.
**Steps:**
1. Save As `work/L02_m12_tol.zmx`.
2. Optimize tab → Remove All Variables. List every solve in the LDE in `notes.md` and decide keep/convert/remove (justify each). Convert the image-distance marginal-ray solve (if any) to a fixed value — focus will be a COMP instead.
3. Convert all semi-diameters to Fixed (right-click the column or use the Solve type), rounding up to the next 0.05 mm, and set the stop as the aperture-defining surface.
4. Check ray aiming (Real), and add field points at −y and ±x (or note that you will use XY-symmetric fields in the criterion).
5. Record the nominal RMS wavefront (waves at the primary wavelength) per field and the FFT MTF at 72 lp/mm (T, S) per field: this is the baseline.

**Deliverable:** `work/L02_m12_tol.zmx`, solve list and baseline table in `notes.md`.
**Check yourself:** fixing semi-diameters must not change the nominal performance (if it does, the automatic apertures were clipping rays — find out why).

## Task 2 — Radial decenter statistics (Python)
**Goal:** Understand what independent X and Y tolerances mean for a physical radial clearance.
**Given:** TEDX = TEDY = ±0.010 mm, normal distribution with the limits at ±2σ (OpticStudio default); the physical maximum radial clearance is 0.010 mm.
**Steps:**
1. Draw $10^6$ samples of $(x, y)$ in numpy and compute $r = \sqrt{x^2+y^2}$. Report mean, median, 95th percentile and the fraction with $r > 0.010$ mm.
2. Repeat for uniform X and Y on ±0.010 mm, and for "uniform in the disc" (the physically plausible case for a lens rattling in a bore).
3. Which per-axis normal tolerance reproduces the 95th percentile of the uniform-disc case?

**Deliverable:** script `work/radial.py`, table in `notes.md`.
**Check yourself:** normal ±2σ: σ = 5 µm, $r$ is Rayleigh with mean 6.3 µm, 95th percentile 12.2 µm, and 13.5 % of samples exceed 10 µm. Uniform disc of radius 10 µm: mean 6.7 µm, 95th percentile 9.7 µm.

<details><summary>Hints / solution sketch</summary>

Rayleigh: mean $\sigma\sqrt{\pi/2}$ = 6.27 µm; percentile $p$: $\sigma\sqrt{-2\ln(1-p)}$ → 95 % at 12.24 µm; $P(r>10) = e^{-10^2/(2\cdot5^2)} = e^{-2}$ = 0.135. Uniform disc radius $a$: $P(r<\rho) = (\rho/a)^2$ → mean $2a/3$ = 6.67 µm, 95 % at $a\sqrt{0.95}$ = 9.75 µm. Matching the 95th percentile with a Rayleigh: $\sigma = 9.75/2.448$ = 3.98 µm → per-axis normal tolerance ±7.97 µm at ±2σ, i.e. ≈ ±0.008 mm. The point: per-axis tolerances are a modelling choice; know what radial distribution they imply.
</details>

## Task 3 — Build a realistic TDE (OpticStudio)
**Goal:** Replace the defaults with a precision-grade, mechanically meaningful set.
**Steps:**
1. Run the **Tolerance Wizard** once with its defaults; save the TDE as `work/L02_defaults.tol` (TDE toolbar Save) and note the number of operands.
2. Rerun the wizard with the precision values of the lecture's worked example: TFRN 3 fringes (TWAV 0.6328), CT ±0.05 mm, air spaces ±0.02 mm, surface tilt 0.082° (on one surface per element only — delete the other), no surface decenter, element decenter ±0.010 mm, element tilt ±0.04°, index ±0.0005, Abbe ±0.5 %, TIRR 0.5 fringe.
3. Edit: delete tolerances on the object distance and the last thickness; decide the TTHI adjust surfaces assuming a stacked M12 barrel (all elements and spacers stacked against a front shoulder); add **COMP** on the image distance with range ±0.10 mm; add **TETX/TETY** ±0.1° on the image surface (sensor tilt in the holder). Label every row in the Comment column.
4. Save as `work/L02_precision.tol` and in the lens file.

**Deliverable:** both `.tol` files, operand count, a short list of edits with reasons.
**Check yourself:** expect ~60–90 operands for a 4–6-element lens. If your TTHI Int2 values all equal the next surface, you kept the wizard's "front-face seat" assumption — revisit step 3.

## Task 4 — Compensation modes and field symmetry (OpticStudio)
**Goal:** See how much the analysis settings change the answer.
**Steps:** Tolerancing dialog, mode **Sensitivity**, criterion **RMS Wavefront**, sampling moderate (e.g. 5–7 rings or the default), Monte Carlo runs = 0.
1. Run with Comp = **None**, then **Paraxial Focus**, then **Optimize All (DLS)**. Note for each: the nominal criterion, the estimated change (RSS), and the top-5 worst offenders.
2. With Optimize All, run once with **Y-symmetric** and once with **XY-symmetric** fields. Compare the contribution of TEDX vs TEDY, TETX vs TETY.
3. Explain the differences in two or three sentences each.

**Deliverable:** comparison table in `notes.md`.
**Check yourself:** "None" is dominated by power-type errors (radius, index, CT) that mostly defocus; "Paraxial Focus" removes most of those; "Optimize All" removes more (it can balance spherical against defocus). With Y-symmetric fields, X-decenters/tilts are under-represented — their effect appears smaller than the identical Y-tolerances, which is unphysical.

## Task 5 — Look inside (OpticStudio)
**Goal:** Demystify what the tolerancer does to your lens.
**Steps:**
1. Insert a **SAVE** operand (File # = 1) directly after the TETX of the second element. Run sensitivity. Open the generated `TSAV_MIN_0001.ZMX` / `TSAV_MAX_0001.ZMX` (in the lens-file folder; the exact numbering follows the File # you gave).
2. Identify the inserted coordinate breaks, their solves, and the compensator value. Compare the Merit Function value in the saved file with the criterion listed in the tolerance report for that line.
3. Set Monte Carlo runs = 5, number to save = 5, run, and open `..._MC_T0001.ZMX`. Find the irregularity (TIRR) — what surface type did the standard surfaces become?

**Deliverable:** three screenshots or LDE excerpts with annotations in `notes.md`.
**Check yourself:** the KB article "How to inspect OpticStudio's internal tolerance models" describes the same structure: coordinate-break pairs, a compensating image move, and the criterion merit function inside the file. Irregularity converts standard surfaces into irregular surfaces.

## Task 6 — Criterion choice (OpticStudio)
**Goal:** Choose a criterion that represents the specification, at acceptable speed.
**Steps:** With Optimize All and XY-symmetric fields, run sensitivity with:
(a) RMS Spot Radius (centroid), (b) RMS Wavefront, (c) Diffraction MTF Average at 72 lp/mm, (d) Boresight Error.
1. Record run time and the top-5 worst offenders for each.
2. Which tolerances appear in all top-5 lists? Which only in (d)?
3. Decide which criterion you will use for exploration (L03) and which for the final yield statement, and why.

**Deliverable:** table + decision in `notes.md`.
**Check yourself:** (b) and (c) usually rank similarly for a well-corrected lens; (a) can differ if the spot is near the Airy size; (d) is dominated by element decenters and tilts (and sensor tilt) — the tolerances that move the image of the axis, which for a calibrated 3D camera matter for calibration stability rather than sharpness.

## Reflection questions
1. Why is an F-number solve on the last radius a disaster during tolerancing, while a pickup between two passes of the same surface is required?
2. When would you choose TTHI with Int1 = Int2 rather than the default adjust surface?
3. A colleague runs tolerancing with "Paraxial Focus" and reports excellent yield. What question do you ask?
4. Why might Boresight Error be a sensible *second* criterion for a structured-light camera lens even if it does not appear in the image-quality specification?

<details><summary>Answers</summary>

1. A solve is re-evaluated for every trial: an F-number solve re-shapes the last surface to restore the F-number, i.e. the tolerancer "re-polishes" a lens for each build — an adjustment that does not exist in production. A pickup that expresses physical identity (the same surface met twice) must stay, otherwise the two passes would see different (inconsistent) perturbations.
2. When the element's thickness error really moves everything behind it, e.g. stacked lenses and spacers pushed against one shoulder (typical M12 barrels and many camera modules) — the downstream elements are referenced to this element's rear face, not to their own seat.
3. "Is paraxial focus how your production focuses, and is it the best focus for the criterion?" With spherical aberration or field curvature, the best-MTF focus differs from the paraxial focus; and a real factory focuses on an MTF or contrast criterion, so paraxial-focus compensation can be either optimistic or pessimistic. Also: "what is the compensator range?"
4. Element decenters/tilts and sensor tilt move the image of the optical axis (principal point) and change distortion asymmetry. Calibration absorbs the static value, but the spread across units sets requirements on calibration range and on mechanical stability; boresight sensitivity also predicts sensitivity to shocks and temperature (L05).
</details>
