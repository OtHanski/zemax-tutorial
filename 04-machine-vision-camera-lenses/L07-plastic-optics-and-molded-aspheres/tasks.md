# L07 — Tasks: Plastic optics and molded aspheres

> Work in `work/` inside this lesson folder (e.g. save `work/L07_T2_cop_asphere.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — Thermal and chromatic power budget (Python)
**Goal:** See why plastic achromats don't athermalize and what a hybrid does.
**Given:** thin lenses in contact, total $f = 6$ mm. Use $\gamma$ (ppm/K): N-BK7 4.0, PC 263.6, COP 267.2, PMMA 311.4; $V_d$: N-BK7 64.17, PC 30.0, COP 56.0.
**Steps:**
1. Write `gamma(alpha, dndT, n)` and reproduce the table of lecture §3.
2. Two-element achromats ($\sum\phi_i = \phi$, $\sum\phi_i/V_i = 0$): compute element focal lengths and $\gamma_\text{sys}$ for COP + PC and for N-BK7 + PC.
3. Three elements N-BK7 + PC + COP: solve power, achromatism and athermal focus for an aluminium barrel ($\gamma_\text{sys} = 23.6$ ppm/K).
4. Comment on the element powers you get (manufacturability, sensitivity).

**Deliverable:** `work/thermal_budget.py`, results in `notes.md`.
**Check yourself:** COP + PC: $f_1 = 2.79$, $f_2 = -5.20$ mm, $\gamma_\text{sys} ≈ +271$ ppm/K. N-BK7 + PC: $f_1 = 3.19$, $f_2 = -6.83$ mm, $\gamma_\text{sys} ≈ -224$ ppm/K. Three-element: $f$ ≈ 6.39 (N-BK7), −5.91 (PC), 5.57 (COP) mm.

<details><summary>Hints / solution sketch</summary>

Achromat: $\phi_1 = \phi V_1/(V_1-V_2)$, $\phi_2 = -\phi V_2/(V_1-V_2)$; $\gamma_\text{sys} = (\phi_1\gamma_1+\phi_2\gamma_2)/\phi$. COP and PC have nearly equal $\gamma$, so the achromat inherits $\gamma \approx 270$ ppm/K. N-BK7 + PC is the opposite: the negative PC element dominates and the pair is strongly *negative*. The three-equation linear system ($3\times3$) gives a solution with element powers each about as strong as the whole lens — workable but sensitive. Real designs add air spaces and more elements and verify with thermal multi-configuration analysis; the polymer $dn/dT$ uncertainty (±10–20 %) must be part of the tolerance budget.
</details>

## Task 2 — From sphere to asphere to Q-type (OpticStudio)
**Goal:** Learn asphere workflow and see coefficient conditioning.
**Given / specs:** singlet, object at infinity, EPD 3.0 mm, f = 6 mm (F/2), wavelength 0.85 µm, on-axis plus fields 0, 10, 20°; material COP (e.g. E48R from the ZEON catalog — name varies by version) — if unavailable, use PMMA and say so; centre thickness 2.5 mm; stop on surface 1.
**Steps:**
1. Spherical singlet: optimize radii (default RMS spot, EFFL = 6). Record spot sizes. Save `work/L07_T2_sphere.zmx`.
2. Make surface 1 *Even Asphere*: free the conic, then 4th, 6th, 8th, 10th order in turn, re-optimizing each time. Record the coefficients and RMS spots. Save `work/L07_T2_cop_asphere.zmx`.
3. Make both surfaces aspheric. What improves now, and why (think $\bar h/h$, Kidger §7.5)?
4. Convert surface 1 to *Q-Type Asphere* (Qcon) with normalization radius = clear semi-aperture, refit/re-optimize with the same number of terms. Compare coefficient magnitudes and the optimizer's convergence.
5. Check the edge slope and the thickness ratio (centre vs edge incl. a 0.8 mm flange).

**Deliverable:** table of coefficients and spots per step; notes on conditioning.
**Check yourself:** on axis the asphere removes spherical aberration almost completely (spot ≪ Airy; Airy radius at F/2, 0.85 µm ≈ 2.1 µm). Off-axis (20°) is limited by coma/astigmatism with one asphere at the stop; the second asphere (away from the stop) helps the field. Even-asphere coefficients come out with alternating signs and widely varying magnitudes; Qcon coefficients are of similar size (µm-level departures).

<details><summary>Hints / solution sketch</summary>

Airy radius $1.22\lambda N = 1.22\cdot0.85\cdot2 = 2.07$ µm. With the stop on surface 1, $\bar h/h \approx 0$ there: its asphere acts on $S_1$ only. Surface 2 is 2.5 mm away, where $\bar h/h \ne 0$, so its asphere also changes $S_2, S_3$ ([Kidger Eq. 7.43]). If the Q-type surface optimizes to the same performance with smaller, smoother coefficients, you have seen its main benefit.
</details>

## Task 3 — Hybrid version of your L04 lens (OpticStudio)
**Goal:** Trade element count against thermal robustness.
**Given:** `../L04-compact-fixed-focus-lens-project/work/L04_S2_final.zmx`. *Save As* `work/L07_T3_hybrid.zmx`.
**Steps:**
1. Replace one weak element (or a cemented pair) by a single COP element with two aspheric surfaces; try to remove one element in total. Add moldability constraints (centre thickness 0.8–3 mm, edge ≥ 0.6 mm, thickness ratio ≤ 3, slope ≤ 50° at the clear aperture).
2. Re-optimize to the L04 spec.
3. Set up a thermal Multi-Configuration at −10, 20, 50 °C with an aluminium barrel (Course 03 L09 method; check that the plastic material has thermal data). Record focus shift (with fixed sensor distance), EFL change and MTF at 72 lp/mm.
4. Compare with the all-glass L04 lens under the same conditions.

**Deliverable:** comparison table and two-paragraph recommendation: would you ship the hybrid in an industrial 3D camera?
**Check yourself:** the hybrid usually reaches the spec with one element fewer at 20 °C; its thermal focus shift is typically several times larger than the all-glass lens unless the plastic element has little power or its power is balanced.

## Task 4 — Moldability and birefringence numbers (pen & paper)
**Steps:**
1. A spherical surface of radius 3.0 mm has a clear semi-aperture of 1.8 mm. What is the surface slope at the edge? Is it moldable/measurable comfortably?
2. A molded lens has residual birefringence $\Delta n = 1\times10^{-5}$ over a 2 mm path. Compute the retardance (nm) and the phase at 850 nm. If linearly polarized light enters at 45° to the stress axes, what fraction ends up in the orthogonal polarization (and would leak through a crossed analyser)?
3. A design has centre thickness 3.2 mm and edge thickness 0.9 mm (flange 1.0 mm). Does it meet a 3:1 rule? What would you change?

**Check yourself:** (1) 36.9° (fine); (2) 20 nm, 0.148 rad (8.5°), $\sin^2(\delta/2) = 0.55\,\%$; (3) 3.56:1 — fails; thin the centre or thicken the edge/flange.

<details><summary>Hints / solution sketch</summary>

(1) $\sin\theta = r/R = 0.6$. (2) Retardance $= \Delta n\,t = 10^{-5}\cdot2\times10^{6}$ nm $= 20$ nm; $\delta = 2\pi\cdot20/850 = 0.148$ rad; leakage $\sin^2(\delta/2) = 0.0055$. In a polarisation-filtered structured-light camera, 0.5 % leakage of specular glare may matter; in a plain intensity camera it does not. (3) 3.2/0.9 = 3.56.
</details>

## Stretch task
Rebuild your Task 2 COP singlet as an aspheric *glass* singlet using a precision-moldable glass from a vendor catalogue (e.g. a low-$T_g$ glass such as those offered for PGM by SCHOTT/OHARA/HOYA/CDGM — check your catalogue for availability) and compare thermal focus shift over 40 K with the COP version.

## Reflection questions
1. Why do phone cameras use all-plastic lenses while many industrial 3D cameras use glass or hybrids?
2. Why does an asphere far from the stop affect astigmatism and distortion but not Petzval curvature?
3. What is the practical advantage of Q-type over even-asphere coefficients?
4. Where would birefringence in a molded lens hurt in a structured-light system?

<details><summary>Answers</summary>

1. Phones autofocus and recalibrate continuously, are produced in huge volumes and are space-limited; industrial 3D cameras are fixed-focus, factory-calibrated and must hold calibration over temperature — plastics' thermal coefficients (~300 ppm/K) make that hard.
2. Its stop-shift contributions scale with $\bar h/h$ (Kidger Eq. 7.43), while Petzval depends only on surface curvatures and indices, which the aspheric terms (higher than $r^2$) do not change.
3. Orthogonality: coefficients are independent, physically meaningful (µm of departure/slope), better conditioned for optimization and easier to tolerance and communicate.
4. Anywhere polarisation is used: polariser-based glare suppression, polarisation cameras, laser/DOE projectors (efficiency and speckle are polarisation-dependent).
</details>
