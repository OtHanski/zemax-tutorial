# L06 — Tasks: Chromatic Aberration and Achromats

> Work in `work/` inside this lesson folder (e.g. save `work/L06_T2_achromat.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — Thin-lens achromat pre-design (pen & paper + Python)
**Goal:** Do the classic pre-design by hand, then use your Seidel code to choose the glass pair and bending.

**Given / specs:** $f = 100$ mm, F/5 (EPD 20 mm), object at infinity, semi-field 1°, F/d/C, crown first, stop at the doublet. Glasses: SCHOTT N-BK7 with F2, and N-BK7 with N-SF5. Use the catalog $n_d$, $V_d$ (N-BK7 1.51680/64.17, F2 1.62004/36.37, N-SF5 1.67271/32.25) or compute them from the Sellmeier coefficients in OpticStudio's Glass Catalog window (Libraries → Materials Catalog).

**Steps:**
1. By hand: element powers and focal lengths for both pairs. Petzval sum $Pf$ for both, compared with an N-BK7 singlet.
2. By hand: radii for an **equiconvex crown** for both pairs (Geary's pre-design choice).
3. In Python (`seidel.py`, thin lenses): scan $c_1$ from 0 to 0.03 mm⁻¹ with $c_2 = c_1 - K_1/(n_1-1)$, $c_3 = c_2 - K_2/(n_2-1)$; plot $S_I(c_1)$ and $S_{II}(c_1)$ for both pairs. Find the coma-free bending and the zero-spherical bendings.
4. Decide which pair can make an aplanat.

**Deliverable:** `work/achromat_thin.py`, plot `work/bending_doublet.png`, numbers in `notes.md`.

**Check yourself:**
- N-BK7/F2: $f_1 = 43.33$, $f_2 = -76.45$ mm. N-BK7/N-SF5: $f_1 = 49.74$, $f_2 = -98.96$ mm. $Pf$ = 0.72 (N-BK7/N-SF5) vs 0.66 (singlet).
- N-BK7/N-SF5 coma-free bending: R = 60.54 / −44.67 / −135.8 mm with $S_I = +0.0004$ mm (≈ 0.09 wave): ≈ aplanat.
- N-BK7/F2: coma-free at R = 62.20 / −34.98 / −133.6 mm but $S_I = -0.0082$ mm; zero-spherical bendings at R = 46.37 / −43.30 / −500.1 and 101.05 / −28.76 / −73.16 mm (with coma $S_{II}$ = +0.0016 and −0.0018 mm).

<details><summary>Hints / solution sketch for step 2</summary>

Equiconvex crown: $c_1 = -c_2 = K_1/(2(n_1-1))$.
N-BK7/N-SF5: $c_1 = 0.020105/(2\cdot0.5168) = 0.019451$ → R1 = 51.41, R2 = −51.41 mm; flint: $c_3 = c_2 - K_2/(n_2-1) = -0.019451 + 0.010105/0.67271 = -0.004430$ → R3 = −225.7 mm.
N-BK7/F2: $c_1 = 0.023081/1.0336 = 0.022331$ → R1 = 44.78 = −R2; $c_3 = -0.022331 + 0.013081/0.62004 = -0.001234$ → R3 = −810 mm.
</details>

## Task 2 — The achromat in OpticStudio, Geary-style (OpticStudio)
**Goal:** Turn the pre-design into a real, colour-corrected aplanatic doublet.

**Given / specs:** as Task 1, N-BK7/N-SF5, crown 5 mm, flint 2.5 mm thick, stop on surface 1, fields 0°, 0.7°, 1°.

**Steps:**
1. Enter the equiconvex pre-design from Task 1. Note EFL, AXCL and the Chromatic Focal Shift plot (colour is slightly off because of the real thicknesses). Save `work/L06_T2_start.zmx`.
2. Variables R1, R2, R3 (image distance with a marginal-ray-height solve). MF: EFFL = 100 (weight 1), AXCL (wave 1 = F, wave 3 = C) = 0. Optimise.
3. Add SPHA (surf 0) = 0. Optimise. Record radii, COMA, the Ray Fan (3 wavelengths). Which zero-spherical solution did you land on?
4. Replace SPHA by COMA = 0 (keep EFFL, AXCL). Optimise. Save `work/L06_T2_achromat.zmx`. Compare radii with Design A of the lecture (60.70 / −43.12 / −129.74 mm).
5. Read: Seidel SPHA, COMA, CLA, CTR; Ray Fan on axis (real marginal error, d); Chromatic Focal Shift (secondary spectrum); Longitudinal Aberration (spherochromatism); Spot Diagram with Airy disk at 1°.

**Deliverable:** `.zmx`, screenshots or text exports, table in `notes.md`.

**Check yourself:** Design A: EFL 100.00, BFL ≈ 96.45 mm; real on-axis marginal error ≈ +8 µm at d (fifth-order overcorrection, though Seidel SPHA ≈ 0); RMS spot on axis well inside the Airy radius (3.6 µm) after Quick Focus; d focus ≈ 0.05 mm inside the common F/C focus; g focus ≈ 0.25 mm behind d (add g = 0.4358 µm as a 4th wavelength to see it). CLA sign: compare with your Python (lecture §1.1).

## Task 3 — Real-ray optimisation vs Seidel targets (OpticStudio + analysis)
**Goal:** See why the final design leaves some third-order spherical.

**Steps:**
1. From `L06_T2_achromat.zmx`, delete SPHA/COMA and use the **default merit function**: RMS wavefront, centroid, 3 rings × 6 arms, all three fields and wavelengths, + EFFL = 100 + AXCL = 0 (low weight). Make the image distance a variable (or remove the solve and run Quick Focus between optimisations). Optimise. Save `work/L06_T3_dmf.zmx`.
2. Compare with Design A and Design B (lecture §3.2: B has R = 54.05 / −47.08 / −177.0 mm). Tabulate: R1–R3, SPHA, COMA, on-axis RMS wavefront, 1° RMS wavefront, polychromatic RMS spot at 0° and 1°.
3. Repeat step 1 with the field increased to 3°. What happens to the balance between spherical and coma? Which aberration now dominates at 3°, and can the doublet fix it? (Kidger Table 8.1.)

**Check yourself:** The DMF optimum has SPHA > 0 (some undercorrected third order) and a small COMA — between A and B. At 3° astigmatism and field curvature ($S_{III} = H^2K$, $S_{IV} \approx 0.72H^2K$) dominate off axis and no bending fixes them.

## Task 4 — Lateral colour and the stop (pen & paper + OpticStudio)
**Given:** a thin N-BK7 singlet, best form ($B = 0.74$), $f = 100$ mm, F/5, semi-field 10°, stop 30 mm in front.

1. Compute $C_L$, the stop-shift parameter $\chi$, $C_T^*$, and the transverse lateral colour $C_T^*/(n'u')$ at full field.
2. Replace the singlet with your Task 2 achromat (same stop position). Predict $C_T^*$.
3. Verify both in OpticStudio with the **Lateral Color** plot (thin lens → use 0.1 mm thickness).

<details><summary>Solution</summary>

1. $C_L = h^2K/V = 100\cdot0.01/64.17 = 0.01558$ mm; $\chi = \bar u d/h = \tan10°\cdot30/10 = 0.529$; $C_T^* = \chi C_L = 0.00824$ mm; transverse $= 0.00824/(-0.1) = -82$ µm (F vs C chief-ray separation; sign per our convention — OpticStudio may show the opposite sign). Exact thin-lens Seidel trace: 0.008244 mm ✓.
2. $C_L \approx 0$ for the achromat → $C_T^* \approx C_T \approx 0$ regardless of the stop. (Residual from finite thickness and secondary spectrum.)
</details>

## Stretch task — An NIR achromat for a 3D-camera receiver
Re-design the doublet for 800/850/900 nm (850 primary), $f = 25$ mm, F/2.8, semi-field 10°. Use the band Abbe numbers from lecture §4 to pre-design N-BK7/N-SF5 powers, then optimise in OpticStudio with the DMF (RMS spot). Compare with an N-BK7 singlet of the same focal length: is the achromat worth it if the source is (a) an 850 nm VCSEL (±1 nm), (b) an 850 nm LED (±30 nm FWHM)? Give a quantitative answer using the depth of focus $\pm2\lambda N^2$.

## Reflection questions
1. Why does the axial colour of a thin singlet not depend on its shape, while its spherical aberration does?
2. Why can't a cemented doublet correct astigmatism, however you bend it?
3. You must make an aplanatic cemented doublet but the optimiser can't reach SPHA = COMA = 0 with your glasses. What are your options, in order of preference?
4. Why is the Fraunhofer (crown-first) form usually preferred over the Steinheil (flint-first) form?

<details><summary>Answers</summary>

1. $\delta K = \delta n(c_1-c_2) = K/V$ depends only on the curvature difference (the power), not the curvature sum (shape); spherical aberration depends on angles of incidence, which change with shape.
2. For thin lenses at the stop $S_{III} = H^2\sum K_i = H^2K$ — fixed by the total power. Only stop shift or separated elements change it.
3. (a) Change one glass (Glass Substitute / Model glass, then choose a real glass) to move the $S_I$ parabola relative to the $S_{II}$ line [Kidger §8.2.1]; (b) accept a little coma or spherical (often fine for small fields); (c) split into an air-spaced doublet (an extra variable, L07); (d) thicknesses — least effective [Kidger §8.2.1].
4. Shallower cemented-surface curvature in the usual solutions → more lenses per polishing block, cheaper, and usually less higher-order aberration [Kidger §8.2.3].
</details>
