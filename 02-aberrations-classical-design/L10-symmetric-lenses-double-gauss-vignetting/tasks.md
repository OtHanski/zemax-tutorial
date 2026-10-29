# L10 — Tasks: Symmetric lenses, the Celor, the double Gauss and deliberate vignetting

> Work in `work/` inside this lesson folder (e.g. save `work/L10_T2_celor_sym.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~6–7 h

## Task 1 — Celor rear-half predesign (Python, pen & paper)
**Goal:** Derive and solve the Celor quadratic yourself.
**Given / specs:** flint (a) $n_a=1.60562$, $V_a=43.93$; crown (b) $n_b=1.61272$, $V_b=58.63$.
**Steps:**
1. Starting from the three constraints (power, axial colour, Petzval) in the lecture, eliminate $y_b/y_a$ and $\phi_b$ to obtain the quadratic in $\phi_a$. Show your algebra.
2. Code `celor(na,Va,nb,Vb,phi,phiP)` returning both roots, $\phi_b$ and $t$.
3. Reproduce Geary's example (10-inch rear half: $\phi = 0.1$ in⁻¹, $\phi_P = 0.03$ in⁻¹) and the $\phi_P=0$ variant.
4. Solve for the 50 mm lens of Task 2: rear half $\phi = 0.01$ mm⁻¹ and $\phi_P \in\{0, 0.002, 0.003, 0.004\}$ mm⁻¹. Tabulate $f_a$, $f_b$, $t$. Which trend do you see?
5. Compute thin-lens radii (equi-concave / equi-convex) for $\phi_P = 0.003$.
**Deliverable:** derivation + table in `work/notes.md`; `work/celor.py`.
**Check yourself:** Geary: $\phi_a=-0.4614$, $\phi_b=0.5118$ in⁻¹, $t=0.210$ in; with $\phi_P=0$: $f_a=-1.578$, $f_b=1.571$, $t=0.241$ in. Metric $\phi_P=0.003$: $f_a=-21.68$, $f_b=19.54$, $t=2.10$ mm; equi radii $R_a = 2(n_a-1)f_a = -26.25$ mm (i.e. surfaces −26.25/+26.25), $R_b = 2(n_b-1)f_b = 23.94$ mm (+23.94/−23.94).

<details><summary>Hints / solution sketch</summary>

From power: $y_b/y_a = (\phi-\phi_a)/\phi_b$. Colour: $\phi_a/V_a + (y_b/y_a)^2\phi_b/V_b=0 \Rightarrow y_b/y_a = -\phi_aV_b/[V_a(\phi-\phi_a)]$. Combine with $\phi_b = n_b(\phi_P-\phi_a/n_a)$:
$-V_a(\phi-\phi_a)^2 = n_bV_b\phi_a(\phi_P-\phi_a/n_a)$, which rearranges to
$(V_a - \tfrac{n_b}{n_a}V_b)\phi_a^2 + (n_bV_b\phi_P - 2V_a\phi)\phi_a + V_a\phi^2 = 0$.
Lowering $\phi_P$ (flatter Petzval) strengthens both elements and widens the gap: a typical "Petzval costs power" trade-off. $(n-1)$ values: 0.60562 and 0.61272.
</details>

## Task 2 — Celor in OpticStudio: half → symmetric → asymmetric (OpticStudio)
**Goal:** Practise Geary's design-by-halves workflow with pickups.
**Given / specs:** full lens $f = 50$ mm, F/6 (EPD 8.33 mm), object at infinity, fields 0°, 10°, 15°, wavelengths F, d, C. Glasses: SCHOTT **N-BAF4** (flint, element a) and **N-SK4** (crown, element b) — catalogue values differ slightly from Task 1's; that is fine. Stop gap (between the halves) ≥ 4 mm.
**Steps:**
1. *Rear half* (f = 100 mm, EPD 8.33 → F/12): stop, 1 mm air, element a (1.5 mm thick), gap $t$, element b (3.5 mm thick), image. Start from Task 1 radii; optimize `EFFL`=100, `AXCL`=0 with radii pickups keeping equi-shapes; then bend for `SPHA`=0 while holding element powers with `EFLY`.
2. Add 5° field and a stop 3 mm in front; remove astigmatism with `ASTI`=0 or three `FCGT` operands; ignore coma.
3. *Symmetric system:* insert the mirrored front half before the stop. Make every rear radius a **pickup** of its mirror surface with scale −1 and every rear thickness a pickup of its mirror thickness. Optimize `EFFL` = 50 and `AXCL`, then add the default RMS-spot merit function (centroid), `MNCA` ≥ 2 mm on each stop gap, and walk the field 5° → 10° → 15°.
4. *Break symmetry* in at least two different orders (e.g. (i) free rear positive radii only; (ii) free all rear radii and the rear gap; (iii) everything plus a dummy image-plane thickness) and record the RMS spot at 0/0.7/1 field for each.
**Deliverable:** `work/L10_T2_celor_half.zmx`, `..._sym.zmx`, `..._asym.zmx`; a table like Geary's Table 28.1.
**Check yourself:** The symmetric 15° design should show small coma/lateral colour in the Seidel Diagram (mirror-image bars of opposite sign in $S_{II}$, $S_V$, $C_{II}$) and similar bars in $S_I$, $S_{III}$, $S_{IV}$. Symmetry breaking typically improves full-field RMS spot by ~1.5–2× (Geary: 45 → 23 µm for his 5-inch lens; your 50 mm lens is ~2.5× smaller, so expect proportionally smaller spots, roughly 10–25 µm symmetric).

<details><summary>Hints / solution sketch</summary>

- Pickup bookkeeping: label the front half surfaces 1–4 (1–2 = positive crown b, 3–4 = negative flint a, i.e. the mirror image of the rear half), stop = 5, rear surfaces 6–9 (6–7 = flint a, 8–9 = crown b). Radii: $R_6=-R_4$, $R_7=-R_3$, $R_8=-R_2$, $R_9=-R_1$ (pickup with scale −1). Thicknesses: $t_5$ (stop→6) $= t_4$ (4→stop), $t_6=t_3$, $t_7=t_2$, $t_8=t_1$. Draw it before typing.
- If `TRAC`/RMS spot "slams" elements together (Geary Fig. 28.9a), remove the negative-element radii from the variable list for one run, as Geary does, or tighten `MNCA`/`MNEA`.
</details>

## Task 3 — Prove the symmetry principle numerically (OpticStudio)
**Goal:** See odd aberrations vanish at unit magnification.
**Given / specs:** your symmetric Celor from Task 2 (pickups still active).
**Steps:**
1. Change the object to a finite distance and add `PMAG` = −1 (paraxial magnification) with the object distance as the only variable (and the image distance on a marginal-ray-height solve). Use an object height field type (Object Height) so the field is defined in object space.
2. Open the Seidel Coefficients text. Record the sums of $S_{II}$, $S_V$ and lateral colour (`CTR`).
3. Run the Grid Distortion or Field Curvature/Distortion analysis. What is the real-ray distortion?
4. Return to the infinite conjugate and compare.
**Deliverable:** numbers in `notes.md`.
**Check yourself:** at $m=-1$, $\Sigma S_{II}$, $\Sigma S_V$, $\Sigma C_{II}$ are zero to numerical precision (~1e-10 or smaller), real-ray distortion is 0.000% at all fields, and lateral colour is zero, while the even sums $S_I$, $S_{III}$, $S_{IV}$ are the sum of two equal, same-sign half contributions (compare front-half and rear-half surface sums: they are identical). At infinity the odd terms reappear (small but non-zero).

<details><summary>Hints / solution sketch</summary>

Make sure the image-side distance equals the object distance (check the paraxial image distance). If $S_{II}$ is not ~0, a pickup has the wrong scale sign or you mirrored thicknesses in the wrong order.
</details>

## Task 4 — Double Gauss sample: anatomy, apertures and vignetting (OpticStudio)
**Goal:** Learn to read a professional starting point and model vignetting honestly.
**Given / specs:** `{Zemax}\Samples\Sequential\Objectives\Double Gauss 28 degree field.zmx`. *Save As* `work/L10_T4_dg.zmx` before editing.
**Steps:**
1. Record the system specs (EFL, F/#, field, wavelengths), glasses, and whether the sample uses vignetting factors and/or fixed apertures (Field Data Editor; semi-diameter solve column).
2. Seidel Diagram: identify the surfaces with the biggest $S_{IV}$ (Petzval) contributions and their sign. Which surfaces are they physically (concave toward the stop?). Identify mirror-image pairs in $S_{II}$ and $S_V$.
3. Clear any vignetting factors (**Clear Vignetting**) and let semi-diameters float: note the element diameters needed for zero vignetting.
4. Put a **hard circular aperture** on the stop at the axial semi-diameter and fix all lens semi-diameters at the sample's values; run Vignetting Plot and Relative Illumination. Then **Set Vignetting** and compare spot diagrams and MTF at full field before/after.
5. Compute AWRMS (RMS spot, centroid) over the sample's fields using annular zones with boundaries halfway between adjacent field heights (use image heights).
**Deliverable:** annotated notes with numbers; `work/L10_T4_dg.zmx`.
**Check yourself:** You should find large negative Petzval contributions from the strongly concave surfaces facing the stop, positive ones from the outer convex surfaces; relative illumination at full field typically well below $\cos^4(14^\circ) = 0.886$ once real apertures clip the oblique beam; AWRMS dominated by the outer zones.

<details><summary>Hints / solution sketch</summary>

- The file name refers to a 28° *full* field (±14°) — verify in the Field Data Editor rather than trusting the name.
- If Relative Illumination does not change when you add apertures, you probably set apertures on the wrong surfaces or semi-diameters are still in Automatic mode.
- AWRMS weights: for fields at image heights $y_1 < y_2 < \dots < y_N = 1$ (normalized), boundary $b_i = (y_i+y_{i+1})/2$; weight $A_i = b_i^2 - b_{i-1}^2$, with $b_0=0$, $b_N=1$.
</details>

## Task 5 — The thick meniscus principle (pen & paper + OpticStudio)
**Goal:** Feel why thick menisci flatten fields.
**Given / specs:** N-BK7 ($n_d = 1.5168$) meniscus with $R_1 = R_2 = 20$ mm, centre thickness $t = 10$ mm, in air.
**Steps:**
1. Compute its focal length and its Petzval contribution $\sum c\,\delta(1/n)$.
2. Compare with a thin N-BK7 lens of the same focal length: Petzval sum $K/n$.
3. Enter it in OpticStudio and confirm EFL; check `FCUR`/Seidel $S_{IV}$ is zero.
**Deliverable:** numbers in `notes.md`.
**Check yourself:** $K = t(n-1)^2/(nR^2) = 10\times0.5168^2/(1.5168\times400) = 0.004402$ mm⁻¹ → $f = 227.2$ mm, Petzval contribution exactly 0; a thin lens of the same power has $P = K/n = 0.002902$ mm⁻¹ (Petzval radius −344.6 mm).

<details><summary>Hints / solution sketch</summary>

Thick-lens power $K = K_1 + K_2 - (t/n)K_1K_2$ with $K_1 = (n-1)/R$, $K_2 = -(n-1)/R$ gives $t(n-1)^2/(nR^2)$. Petzval: $S_{IV} \propto c_1(1/n - 1) + c_2(1 - 1/n) = (c_1-c_2)(1/n-1) = 0$ for $c_1=c_2$.
</details>

## Stretch task(s)
- **Rapid Rectilinear:** do [Geary Homework 25.10] (10-inch F/8, ±20°, LF1/F1 — use current SCHOTT equivalents, e.g. N-LF… / F… as available, and say which you chose).
- **Celor homework:** [Geary Homework 28.8] — 10-inch F/6, ±20°, BAF4/SK4, ≥ 1 inch stop gap.
- **Double Gauss re-optimization for NIR:** change the sample's wavelengths to 850 nm only and re-optimize; how much does the RMS spot improve, and why (spherochromatism and colour no longer matter)?

## Reflection questions
1. Why does symmetry cancel coma but double spherical aberration?
2. Your symmetric lens works at infinity. Why is it still worth starting symmetric before breaking symmetry?
3. A colleague's double Gauss shows excellent MTF at full field in OpticStudio, but the prototype is visibly dark and soft in the corners. What two modelling errors are most likely?
4. Why do long stop air spaces worsen relative illumination?

<details><summary>Answers</summary>

1. Coma (and distortion, lateral colour) are odd in the field–pupil product; the mirrored half sees the partner ray with the sign of that product reversed, so contributions cancel. Spherical aberration is even — both halves add the same sign.
2. Symmetry gives a well-conditioned start where odd aberrations are already small; the optimizer then needs only small asymmetric changes, and you avoid local minima where one half does all the work (Geary's ASYM1 "window" solution).
3. Floating (non-physical) apertures — the model passed rays the real barrel blocks — and stale/absent vignetting factors or no relative-illumination check; also possible: ignoring mechanical stop clearance.
4. The further the outer elements are from the stop, the more the oblique beam walks across them, so finite apertures clip it sooner (more vignetting), and the off-axis pupil appears smaller/obliquely foreshortened.
</details>
