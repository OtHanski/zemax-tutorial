# L04 — Tasks: Merit function mastery

> Work in `work/` inside this lesson folder (e.g. save `work/L04_T3_nir_start.zmx` and `work/L04_T3_nir.MF`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~6 h

## Task 1 — MF arithmetic and tolerance weights (pen & paper / Python)
**Goal:** Be able to predict what a weight does before you type it.
**Given / specs:** Geary's three `TRAC` rows [Geary Table 8.2, p. 88]: weights 0.87266, 1.3963, 0.87266; values 0.0031, 0.0286, 0.0678 mm; targets 0.
**Steps:**
1. Compute the MF and the % contribution of each row.
2. Add an `EFFL` row with error 0.5 mm and weight 1. Recompute MF and contributions.
3. Using tolerance weighting with an acceptable RMS spot of 10 µm and an EFL tolerance of ±0.05 mm, compute the EFFL weight. With that weight, what is the EFFL contribution at errors of 0.05 mm and 0.5 mm?
4. Explain in two sentences why the MF value changed in step 2 even for rows you did not touch.
**Deliverable:** `work/mf_math.py` + answers.
**Check yourself:** MF = 0.04054 mm (40.5 µm); contributions 0.16%, 22.1%, 77.7%. With EFFL (W = 1): MF = 0.248 mm, EFFL = 98.0%. Tolerance weight $W = \pi(0.010)^2/0.05^2 = 0.126$; contribution 5.8% at 0.05 mm error (the spot is 4× its acceptable value here), 86% at 0.5 mm.

<details><summary>Hints / solution sketch</summary>
$\sum W_\text{IQ} = \pi$ for one field/wavelength with 3 rings and axial symmetry, so $\Phi_\text{IQ} = \pi\cdot0.010^2 = 3.14\times10^{-4}$ mm². The denominator $\sum W$ grows with every row added, so the MF *value* is a weighted average whose normalization depends on the whole editor.
</details>

## Task 2 — Same lens, four merit functions (OpticStudio)
**Goal:** See how the default-MF criterion and reference change the optimum.
**Given / specs:** the triplet `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx` (50 mm, F/4, ±20°, F-d-C). Keep your variables (six radii, air spaces, back focus) and your `EFFL` row above DMFS. Boundaries glass 1.0/–/1.0, air 0.5/–/0.5.
**Steps:**
1. Make four copies and optimize each (DLS, automatic) with: (A) RMS/Spot/Centroid GQ 3×6; (B) RMS/Spot/Chief ray; (C) RMS/Wavefront/Centroid; (D) Contrast at 72 cycles/mm (if your licence offers it; it does in Premium).
2. For each, record: RMS spot (0/14/20°), RMS wavefront (0/14/20°), polychromatic FFT MTF at 36 and 72 cycles/mm (T and S, three fields), distortion at 20°, lateral colour, and the back focal distance.
3. Overlay the four lens drawings (or list radii). Which parameters moved most?
**Deliverable:** comparison table + 6–10 sentence interpretation in `notes.md`.
**Check yourself:** (B) should show smaller lateral colour/coma-type centroid shift than (A) at a small cost in RMS spot; (C) should place the image plane slightly differently from (A) (lecture L03 §3) and typically gives the best on-axis MTF at mid frequency; (D) should be best at 72 cycles/mm but not necessarily best elsewhere. The differences are small (often 5–20%) — and that is the lesson: the criterion fine-tunes a design, it doesn't rescue a bad form.

<details><summary>Hints / solution sketch</summary>
Run each variant from the *same* starting file to compare like with like. If (D) is unavailable or slow, set the contrast sampling lower first. Never compare the MF numbers across A–D (different operands, different units); compare the physical metrics.
</details>

## Task 3 — Build the NIR receiver merit function (OpticStudio)
**Goal:** Translate a written spec into a complete, readable MF. (L05 will optimize it.)
**Given / specs:** the specification of lecture §6: EFL 8.0 mm ± 1%, F/2.0, wavelengths 0.920/0.940/0.960 µm (weights 1/2/1), object at 1000 mm, fields as *paraxial image height* 0, 1.5, 2.1, 2.55, 3.0 mm, TOTR ≤ 16 mm, back focal distance ≥ 3.0 mm, 0.7 mm N-BK7 cover glass 0.4 mm in front of the image, CRA ≤ 25°, |distortion| ≤ 3%, glass ≥ 0.8 mm centre/edge, air ≥ 0.1 mm.
**Starting point:** scale your L09 triplet to f = 8 mm (Lens Data Editor → Make Focal / scale lens tool; location varies by version — search "Scale" or "Make Focal" in the ribbon), set EPD 4.0 mm, keep its glasses, add the cover glass.
**Steps:**
1. Save as `work/L04_T3_nir_start.zmx`. Note EFL, TOTR, CRA, distortion before optimization.
2. Build the custom rows above DMFS exactly as in the lecture table, with `BLNK` comments for each block. Use an F/# solve for F/2 (marginal ray angle solve on the last lens surface).
3. Run the Wizard for the image-quality block (RMS/Spot/Centroid, GQ 4×6, field weights 1, 1, 1.2, 1, 0.8; boundaries as specified).
4. Set variables (radii, air spaces, image distance). Run **one** DLS optimization (automatic). Do not try to make it good yet — check that every constraint row behaves (is it active? satisfied? contributing?).
5. Deliberately violate each constraint once (e.g. set the TOTR limit to 10 mm) and confirm it starts to dominate % Contrib.
6. Save the MF (`.MF` file) for reuse.
**Deliverable:** `work/L04_T3_nir_start.zmx`, `work/L04_T3_nir.MF`, a screenshot/text dump of the MF, and a list of which constraints were active after one optimization.
**Check yourself:** at the start, a scaled visible triplet at F/2 will have a large RMS spot (tens of µm) and possibly CRA close to the field angle (~20°). After one DLS run all packaging/manufacturing constraints should be met or nearly met; image quality will still be poor (a triplet at F/2, ±20.6° is a stretch — L05 will explore better forms).

<details><summary>Hints / solution sketch</summary>
- Half field angle in object space ≈ atan(3/8) = 20.6°.
- CRA: `RAID` on the image surface for the chief ray ($H_y=1$, $P_x=P_y=0$), then `OPLT` 25. Because the cover glass is plane, you could equally evaluate the angle in air just before it.
- Distortion: `DIST` reports percent; wrap it with `ABSO` + `OPLT` 3.
- If the scaled triplet's air gaps become < 0.1 mm after scaling, relax the boundary temporarily or increase spacings by hand before optimizing.
</details>

## Task 4 — GQ vs rectangular array with vignetting (OpticStudio)
**Goal:** See the vignetting trap and the operand/spot-diagram mismatch.
**Given / specs:** `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T4_vignetted.zmx` (your deliberately vignetted triplet).
**Steps:**
1. Remove all vignetting factors (Setup → System Explorer → Fields → clear/"Remove vignetting factors"; location varies by version) but keep the hard apertures.
2. Insert `RSCE` and `RSRE` rows for the 20° field (polychromatic), weight 0. Compare with the Standard Spot Diagram RMS (centroid reference) with square and hexapolar ray patterns at density 20 and 50.
3. Re-apply vignetting factors (Set Vignetting) and repeat.
4. Build two default MFs: GQ 3×6 without vignetting factors, and RA 10×10 with "delete vignetted". Optimize copies of the lens with each and compare the resulting full-field spot and MTF.
**Deliverable:** table and explanation.
**Check yourself:** without vignetting factors, `RSCE` traces the full GQ pupil and reports the error of rays that the apertures actually block — it disagrees with `RSRE` and the spot diagram. With vignetting factors (or RA + delete vignetted) the numbers converge. Optimizing with the wrong sampling wastes freedom correcting rays that never reach the sensor.

<details><summary>Hints / solution sketch</summary>
The Ansys KB note on RSCE/RSRE vs spot diagram (lecture reference 4) lists exactly the settings to align: ray pattern square, sufficient density, same reference.
</details>

## Task 5 — Operand gymnastics (OpticStudio)
**Goal:** Fluency with math operands.
**Given / specs:** any optimized copy of the triplet from Task 2.
**Steps (each a small block above DMFS, weight 0 except where noted):**
1. Make the RMS spot radii at 0°, 14° and 20° *equal* (field-uniform image quality): three `RSCE` rows (one per field) + `EQUA` over them with weight 1. Optimize; compare spot vs field with the unconstrained version.
2. Constrain the ratio TOTR/EFFL ≤ 1.1 with `TOTR`, `EFFL`, `DIVI`, `OPLT`.
3. Limit the maximum angle of incidence on any surface for the marginal ray at full field to 35° using `RAID` rows and `MAXX` + `OPLT`.
4. Monitor `SUMM` of `SPHA` + `COMA` + `ASTI` (weight 0) and explain why such a sum is a poor optimization target.
**Deliverable:** the four blocks in a saved file `work/L04_T5_gym.zmx` with comments; one-line result per block.
**Check yourself:** (1) spots become more uniform but the on-axis spot grows; (2)–(3) constraints active or not depending on your design — confirm by tightening them; (4) signed aberrations can cancel in a sum, so minimizing the sum does not minimize any of them.

<details><summary>Hints / solution sketch</summary>
`EQUA` acts on a *range* of operands (Int1 to Int2 rows). For `MAXX`, the ingredient rows must be contiguous. Insert rows *below* existing blocks to avoid shifting row references, or re-check them afterwards.
</details>

## Reflection questions
1. Why does adding a weight-1 constraint row change the MF value even when the lens is unchanged? What should you compare instead?
2. When would you choose the chief-ray reference over the centroid reference?
3. Your MF has `TOTR` + `OPLT` contributing 70% for 20 cycles while image quality stagnates. List three possible causes and what you would do.
4. Why is Gaussian quadrature both more efficient and more dangerous than a rectangular array?
5. Why is the Contrast criterion better behaved than direct MTF operands early in a design?

<details><summary>Answers</summary>

1. MF² is divided by ΣW; any new weight changes the normalization. Compare physical metrics (spot, wavefront, MTF, constraint violations), not MF numbers across MF definitions.
2. When distortion and lateral colour (centroid shift between wavelengths/fields) matter and are not constrained separately — e.g. metrology lenses or calibration-sensitive 3D cameras — because chief-ray reference penalizes centroid displacement.
3. (a) The length limit conflicts with the form (too few elements / too slow for that track) — revisit spec or form; (b) the weight is far too high relative to tolerance — re-scale; (c) a variable that would shorten the lens is missing or fixed (e.g. back focus, a solve holding a thickness). Also check that the constraint is physically achievable given min thickness constraints.
4. GQ is exact for polynomial aberrations with very few rays, but it assumes an unvignetted circular/elliptical pupil; with hard-aperture vignetting and no vignetting factors it samples rays that are blocked, so the optimizer optimizes the wrong thing.
5. Contrast optimization uses OPD differences between rays sheared by the frequency-dependent pupil shift — smooth, quadratic in the aberrations, and cheap. Direct MTF is flat/noisy when aberrations are large (inside the caustic), may be non-monotonic (spurious resolution), and is expensive to compute (KA-01644).
</details>
