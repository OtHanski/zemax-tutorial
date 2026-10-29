# L07 — Tasks: Solves, Variables and Your First Optimization

> Work in `work/` inside this lesson folder (e.g. save `work/L07_T3_o01a.zmx`). Commit your designs and a short `work/notes.md` with answers. Commit *before* and *after* every optimization run (Geary's b/a naming, or git).
> Estimated time: ~5 h

## Task 1 — Solves and merit functions on paper (pen & paper)
**Goal:** Know exactly what the software computes.
**Steps:**
1. A lens ends with a surface of index $n = 1.5168$ in front and air behind. The paraxial marginal ray (EPD 20 mm, object at infinity) arrives at the last surface with $y = 9.8673$ mm and $nu = -0.050321$. Compute the last curvature that gives F/4, F/5 and F/6.
2. For F/5 compute the M-solve thickness (back focal distance).
3. An MFE has three operands with (value, target, weight): EFFL (100.8, 100, 1); TRAC (0.030, 0, 2); MNCG (1.5, 2.0, 1) where the MNCG is violated. Compute the MF and the % contributions. (Treat the MNCG contribution as (1.5 − 2.0)².)
4. If you double the weight of EFFL, what happens to its % contribution?
**Check yourself:** F/5 → $R = -102.65$ mm; BFL ≈ 98.67 mm; MF ≈ 0.472.

<details><summary>Solution</summary>

1. $c = (nu - u')/(y(1-n))$ with $u' = -1/(2N)$: F/4: $u' = -0.125$, $c = 0.074679/(-5.09942) = -0.014645$ → $R = -68.28$ mm. F/5: $c = 0.049679/(-5.09942) = -0.0097421$ → $R = -102.65$ mm. F/6: $u' = -0.08333$, $c = 0.033012/(-5.09942) = -0.0064737$ → $R = -154.47$ mm.
2. $t = -y/u' = 9.8673/0.1 = 98.673$ mm.
3. $\sum W(V-T)^2 = 1(0.8)^2 + 2(0.03)^2 + 1(0.5)^2 = 0.64 + 0.0018 + 0.25 = 0.8918$; $\sum W = 4$; MF $= \sqrt{0.8918/4} = 0.472$. Contributions: EFFL 71.8 %, TRAC 0.2 %, MNCG 28.0 %.
4. Its share rises to $1.28/(1.28 + 0.0018 + 0.25) = 83.6$ %, and ΣW becomes 5. Weights are relative: what matters is the ratio between weighted squared errors.

</details>

## Task 2 — Solves in OpticStudio
**Goal:** Practise the three key solve types.
**Given / specs:** `../L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx`.
**Steps:**
1. On the radius of surface 2 put an **F Number** solve with F/# = 5. Read $R_2$ and EFL (System Data).
2. Replace it with a **Marginal Ray Angle** solve with angle −0.1. Same result? Why?
3. Replace it with a **Pickup** solve from surface 1, scale −1. Now change $R_1$ to 80 mm: what happens to $R_2$ and to the EFL?
4. Restore the F-number solve. Change $R_1$ to 60 mm (a near "best-form" bending): EFL should stay 100 mm. Read $R_2$.
5. Put a Marginal Ray Height solve on the back thickness with pupil zone 0 and then with pupil zone 0.7 (a real-ray zone, if your version offers it). How far apart are the two image positions?
**Deliverable:** `work/L07_T2_solves.zmx` (final state: $R_1 = 60$, F/5 solve), numbers in notes.
**Check yourself:** (1) $R_2 \approx -102.65$ mm, EFL = 100.00; (2) identical — for an object at infinity F/# = −1/(2u′); (3) with $R_1 = 80$, $R_2 = -80$, EFL drops to ≈ 78 mm; (4) $R_2 \approx -364$ mm; (5) the 0.7-zone real ray crosses the axis ≈ 0.78 mm in front of the paraxial focus (≈ half of the full-aperture LSA of −1.61 mm: longitudinal SA ∝ ρ²).

## Task 3 — Your first real optimization (OpticStudio)
**Goal:** Optimize the singlet properly and compare with the lecture's reference run.
**Given / specs:** From `L07_T2_solves.zmx`, set $R_1 = 102.7$ again (F/5 solve on $R_2$), fields 0/3.5/5°, F/d/C, stop at S1, EPD 20.
**Steps:**
1. Remove the M-solve from the back thickness; make **$R_1$** and the **back thickness** variables (Ctrl+Z).
2. Optimize → Optimization Wizard: Image Quality **Spot**, Reference **Centroid**, **Gaussian Quadrature** 3 rings / 6 arms, Assume Axial Symmetry on, Glass boundaries: min 2, max 8, edge 1; Air: min 0.5, max 1000, edge 0.5. Apply. Insert an `EFFL` line above the DMFS line with target 100 and weight 0 (monitor only).
3. Record the initial MF, then Optimize! (DLS, Automatic). Record final MF, $R_1$, $R_2$, back thickness, shape factor $X$, and the per-field RMS spot (Standard Spot Diagram, centroid, high ray density).
4. Save as `work/L07_T3_o01a.zmx` (the starting state as `..._o01b.zmx`).
5. Now also make the centre thickness variable. Optimize again. What happens to the thickness? Save `work/L07_T3_o02a.zmx`.
**Check yourself:** start MF ≈ 0.145 mm at paraxial focus; after step 3 MF ≈ 0.059 mm with $R_1 \approx 58$ mm, $R_2 \approx -460$ mm ($X \approx 0.78$), back focus ≈ 96.3 mm; per-field RMS ≈ 60/51/66 µm. In step 5 the thickness runs to the 8 mm bound and the MF improves only slightly (≈ 0.0586). Your OpticStudio numbers may differ by a few % (sampling, version) — but the bending and trends should match.

<details><summary>Hints</summary>

- If the optimizer does nothing: check that the back thickness is really a variable (V), not still an M-solve.
- If $R_2$ stays at −102.65 while $R_1$ changes, the F-number solve is working: EFL is locked.
- Look at % contributions: which field and wavelength dominate? (The 5° field and the F/C wavelengths — colour is the limit.)

</details>

## Task 4 — Pitfall gallery (OpticStudio)
**Goal:** Break things on purpose so you recognize the symptoms later.
**Steps:**
1. **Locked focus:** start from `..._o01b.zmx`, keep the M-solve on the back thickness, vary only $R_1$. Optimize. Compare the MF with Task 3.
2. **Runaway thickness:** delete the boundary operands (MNCG/MXCG/MNEG) from the Task 3 MF, vary $R_1$, back thickness and centre thickness. Optimize. Look at the Cross-Section.
3. **Drifting focal length:** replace the F-number solve on $R_2$ by a plain variable; optimize with only the default MF. What happens to EFL? Then give the `EFFL` operand weight 1 (or 10) and optimize again.
4. **Wrong sampling:** in the Task 3 file, put a circular aperture of radius 9 mm on surface 1 (smaller than the 10 mm beam). Compare the GQ-based MF value with the Spot Diagram RMS. Rebuild the MF with Rectangular Array and "delete vignetted" and compare again.
**Deliverable:** one paragraph per case in notes (symptom → cause → fix).
**Check yourself:** (1) the MF stays far above Task 3 because best focus is not the paraxial focus; (2) the lens becomes a ~100 mm long glass cylinder (MF ≈ 0.044 in the Python model) — absurd; (3) EFL drifts away from 100 mm (spot size scales with focal length, so the optimizer happily trades focal length for smaller spots) until EFFL is weighted; (4) GQ ignores the hard aperture and reports a misleading MF; RA with vignetting deletion agrees with the spot diagram.

## Task 5 — Spot vs. wavefront, centroid vs. chief ray, mono vs. poly (OpticStudio)
**Goal:** See how merit-function choices change the "optimum".
**Steps:**
1. From `..._o01b.zmx` run four optimizations (vary $R_1$ + back focus): (a) Spot/Centroid; (b) Spot/Chief ray; (c) Wavefront/Centroid; (d) Spot/Centroid with d-light only.
2. Tabulate $R_1$, $X$, back focus, per-field RMS spot (polychromatic) and on-axis OPD P-V for each.
3. Which design would you choose for a sensor with 5 µm pixels? (Hint: none of them is good enough — why, and what would you change in the *design form*?)
**Check yourself:** all four land near $X \approx 0.7$–0.8 ($R_1 \approx 55$–62 mm). The monochromatic optimization (d) gives a much lower MF (≈ 0.038 mm in d-light) but is no better in white light. Chief-ray referencing shifts the balance slightly towards smaller coma at 5°. Wavefront optimization focuses a little differently (L06 Task 5). With ~50–65 µm RMS spots versus 5 µm pixels, a singlet is hopeless: you need an achromat (two glasses) to kill axial colour and more surfaces to fix field aberrations — Course 02.

## Task 6 — Write a tiny damped-least-squares optimizer (Python)
**Goal:** Demystify DLS by implementing it.
**Given / specs:** Your ray tracer from `../L06-real-rays-and-analysis-tools/work/raytrace.py`.
**Steps:**
1. Residual vector $\mathbf f(\mathbf x)$: for each field (0, 3.5, 5°), wavelength (F, d, C) and Gaussian-quadrature ray (3 rings at ρ = 0.3357, 0.7071, 0.9420 with weights 5/18, 8/18, 5/18; 6 arms), the x and y image errors relative to that field's centroid, multiplied by $\sqrt{w}$. Variables $\mathbf x = (c_1, t_{\text{back}})$; $c_2$ from the F/5 solve formula.
2. Jacobian by forward differences (step 1e-6 in curvature, 1e-4 mm in thickness).
3. Iterate $\Delta = -(\mathbf J^\mathsf T\mathbf J + \lambda\,\mathrm{diag}(\mathbf J^\mathsf T\mathbf J))^{-1}\mathbf J^\mathsf T\mathbf f$; accept the step and divide λ by 10 if the MF decreased, otherwise multiply λ by 10 and retry.
4. Start from $R_1 = 102.7$, $t_{\text{back}} = 98.67$. Plot MF vs iteration.
5. Start from $R_1 = -60$ (a lens bent the "wrong" way, $X < -1$ meniscus). Where does it converge? Local minimum?
**Deliverable:** `work/dls.py`, plot.
**Check yourself:** converges in ~5–15 iterations to $R_1 \approx 58$ mm, back focus ≈ 96.3 mm, MF ≈ 0.059 mm (same as Task 3). From a very different start it may stall at a worse bending or need much larger λ — that's the "local" in local optimization.

## Stretch task — Geary's Chapter 3 homework, modernized
Do Geary Homework 3.7 (pp. 28–31) with OpticStudio: his singlet is f = 400 mm, F/10 (EPD 40), d-light, fields 0/3.5/5°, BK7 → use N-BK7, thickness 4 mm. Follow his steps (F-solve, bending for minimum `SPHA`, zero `COMA`, zero `ASTI`, conic on surface 2, default MF, dummy-surface focus, thickness constraints `MNCG`/`MXCG`). Keep `SPHA`, `COMA`, `ASTI`, `DIST`, `PETC` lines at weight 0 as monitors. Note in your notes which steps produce unusable lenses and why.

## Reflection questions
1. Why is it better to control EFL with a solve than with an `EFFL` operand?
2. Why does Gaussian quadrature with 3 rings reproduce the dense-spot RMS of a lens dominated by third-order spherical aberration exactly?
3. Why did the optimizer make the lens 100 mm thick when allowed to?
4. What does "% contribution" tell you that the MF value alone does not?
5. When would you use Orthogonal Descent instead of DLS?

<details><summary>Answers</summary>

1. A solve is exact and removes a degree of freedom; an operand is only a weighted wish that competes with image quality (and costs a variable).
2. The squared ray error of third-order SA plus defocus is a polynomial of degree ≤ 3 in $x = \rho^2$; 3-node Gauss–Legendre integrates degree ≤ 5 exactly.
3. Nothing in the MF penalized it; a very thick lens changes the principal-plane positions and ray heights in a way that reduces the targeted aberrations. Optimizers exploit every freedom; boundaries encode manufacturability.
4. Which operands (fields, wavelengths, constraints) dominate — where to focus design effort, and whether a constraint is fighting image quality.
5. Noisy/discontinuous MFs (non-sequential detectors, many vignetted rays), and small compensator adjustments in tolerancing.

</details>
