# L03 — Tasks: Coma, Astigmatism and the Symmetry Principle

> Work in `work/` inside this lesson folder (e.g. save `work/L03_T2_landscape.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4–5 h

## Task 1 — Stop-shift equations in Python (Python)
**Goal:** Verify the stop-shift equations numerically and find the natural stop position.

**Given / specs:** thin N-BK7 lens ($n = 1.5168$), $f = 100$ mm, shape factor $B = -3$ (R1 = −51.68 mm, R2 = −25.84 mm, thickness 0), F/10 (EPD 10 mm), object at infinity, semi-field 10°, λ = 587.6 nm.

**Steps:**
1. With your `seidel.py` from L01, compute $S_I \ldots S_V$ with the stop at the lens.
2. Compute $\chi_0 = -S_{II}/S_I$ and the stop distance $d = \chi_0 h/\bar u$ in front of the lens.
3. Predict $S_{III}^*$ and $S_V^*$ from the stop-shift equations.
4. Re-run `seidel.py` with the chief ray launched so that it crosses the axis $d$ mm in front of the lens ($\bar y_{\text{lens}} = \bar u d$) and compare.
5. Repeat steps 1–3 for $B = -1, -2, -5, -10$ and tabulate $S_{III}^*/S_{IV}$. What value would give a flat tangential field?

**Deliverable:** `work/stopshift.py` and a table in `notes.md`.

**Check yourself:** stop at lens: $S_I = 0.02025$, $S_{II} = -0.01355$, $S_{III} = 0.007773$, $S_{IV} = 0.005124$, $S_V = 0$ (mm). $\chi_0 = 0.669$, $d = 18.97$ mm. $S_{III}^* = -0.001289$, $S_V^* = 0.006904$ — direct recomputation agrees to all printed digits. Flat T field needs $S_{III}^*/S_{IV} = -1/3$; the scan gives 0.00 (B=−1), −0.19 (B=−2), −0.25 (B=−3), −0.29 (B=−5), −0.30 (B=−10) — it never quite reaches −1/3.

<details><summary>Hints</summary>

- In the stop-at-lens case the chief ray has $\bar y = 0$ at the lens; just launch $\bar y_1 = \bar u d$ instead (thin lens, object at infinity: the chief ray in object space is a straight line through the stop centre).
- $S_{III}^*/S_{IV}$ at $B=-3$: $-0.001289/0.005124 = -0.252$.
</details>

## Task 2 — Landscape lens: coma and astigmatism vs stop position (OpticStudio)
**Goal:** See the stop-shift equations in action on a real (thick) lens and read coma/astigmatism off the analysis windows.

**Given / specs:** N-BK7 meniscus, R1 = −51.68 mm, R2 = −25.84 mm, centre thickness 3 mm (then re-scale R1/R2 or use an EFFL operand to restore EFL = 100 mm). EPD 10 mm, fields 0°, 7°, 10°, wavelength 0.5876 µm. Surface 1: dummy STOP surface with thickness $d$ (start at 0); surface 2–3: the lens; image at paraxial focus (marginal-ray height solve).

**Steps:**
1. Build the lens and save `work/L03_T2_landscape.zmx`. Confirm System Aperture is *Entrance Pupil Diameter* (so moving the stop keeps the F/#).
2. For $d$ = 0, 5, 10, 15, 20, 25, 30 mm, record COMA (S2), ASTI (S3), FCUR (S4), DIST (S5) sums from **Seidel Coefficients**. Plot them vs $d$ in Python. Fit S2 (should be linear in $d$) and S3 (quadratic) and compare with the stop-shift equations using $\chi = \bar u d/h$.
3. At the zero-coma position: open **Ray Fan** (full field) and **Field Curvature/Distortion**. Identify the T and S curves; read the distortion at 10°.
4. Add a merit function with COMA (surf 0, target 0) and make $d$ variable; optimize. Compare the optimum with step 2.
5. Now also make R1 variable, constrain EFFL = 100, and add FCGT at the 10° field (target 0) to flatten the tangential field (as Geary does in §12.5). How close do you get with zero coma? What does the spot diagram look like on axis?

**Deliverable:** `.zmx`, plots of S2/S3/S5 vs $d$, short discussion.

**Check yourself:** S2 linear and S3 quadratic in $d$ with zero coma near $d \approx 19$ mm (thickness shifts it a few mm); distortion at the natural stop is barrel of a few tenths of a percent; T field much flatter than with the stop at the lens. Flattening T exactly costs either some coma or a stronger meniscus; the axial spot grows because spherical aberration is uncorrected (≈ 4 waves at F/10) — landscape lenses were used at F/11–F/16 for a reason.

## Task 3 — Periscopic lens and the symmetry principle (OpticStudio)
**Goal:** Use pickup solves to build a symmetric lens, verify that odd aberrations vanish at $m=-1$, then break symmetry for an object at infinity. (Follows [Geary Ch. 12] with modern UI and N-BK7.)

**Given / specs:** two identical N-BK7 elements, 4 mm thick, separated by 20 mm with the stop exactly in the middle (10 mm + 10 mm air). System EFL 100 mm, F/10 (image-space F/#), fields 0°, 10.5°, 15°, λ = 0.5876 µm. Start with equiconvex elements: each element focal length ≈ 189.4 mm → R ≈ ±195.8 mm (thin-lens estimate from $\Phi = 2\Phi_1 - t\Phi_1^2$).

**Steps:**
1. Front element radii R1, R2 variable; rear element radii by **pickup solves**: R4 = −R2, R5 = −R1 (scale −1); air space after stop = pickup of air space before stop (scale +1); rear thickness = pickup of front thickness.
2. **Unit magnification:** set object distance finite and variable, add PMAG (target −1) and EFFL (target 100). Optimize. Open Seidel Coefficients: check COMA, DIST and CTR sums (add F, C wavelengths for CTR). Save `work/L03_T3_perisc_m1.zmx`.
3. **Object at infinity:** set object at infinity, remove PMAG, use the default merit function (RMS spot, centroid, 3 rings) + EFFL = 100; variables = front curvatures and the stop air space (rear follows via pickups). Make the image distance variable too (or Quick Focus). Record RMS spots at the three fields and the Seidel sums. Save `work/L03_T3_perisc_inf.zmx`.
4. **Break symmetry:** remove all pickups, make all four curvatures and both air spaces variable, re-optimize. Record RMS spots again. Save `work/L03_T3_perisc_asym.zmx`.

**Deliverable:** three `.zmx` files and a table: case | RMS spot (0°, 10.5°, 15°) | S2 | S3 | S5.

**Check yourself:** at $m=-1$ the COMA, DIST (and lateral colour) sums are zero to numerical precision while SPHA and ASTI are not. At infinity the symmetric lens bends into two menisci concave toward the stop (the classical periscopic form). Breaking symmetry should reduce the off-axis spots substantially — Geary reports a dramatic improvement (from tens of µm to below 10 µm) for his F/10, 200 mm version. If the asymmetric optimisation gets stuck, stage it (Geary's cautionary note, §12.7): first unslave the curvatures, then the air spaces.

## Task 4 — Coma and astigmatism by hand (pen & paper)
**Given:** a thin plano-convex N-BK7 lens, curved side to the object, at the stop, $f = 50$ mm, object at infinity, λ = 587.6 nm.

1. At F/4 and 5° semi-field, compute $S_{II}$, $S_{III}$, $W_{131}$ and $W_{222}$ in waves.
2. Compute the tangential and sagittal coma lengths in µm.
3. At what field angle are $W_{131}$ and $W_{222}$ equal at F/4?
4. A lens with $S_I = 0$, $S_{II} = 0$ but $S_{III} \ne 0$: what happens to $S_{III}$ and $S_V$ if you move the stop?

<details><summary>Solution</summary>

$h = 6.25$ mm, $K = 0.02$, $\bar u = \tan5° = 0.08749$, $H = -\bar u h = -0.5468$ mm, $u' = -0.125$, $\sigma_{II} = \frac{n+1}{n(n-1)}(1) + \frac{2n+1}{n}(-1) = 3.2107 - 2.6593 = 0.5514$.
1. $S_{II} = -\frac{h^2K^2H}{2}\sigma_{II} = -\frac{39.06\cdot4\times10^{-4}\cdot(-0.5468)}{2}\cdot0.5514 = 2.356\times10^{-3}$ mm → $W_{131} = S_{II}/2 = 1.178\times10^{-3}$ mm = 2.00 waves. $S_{III} = H^2K = 0.29899\cdot0.02 = 5.980\times10^{-3}$ mm → $W_{222} = 2.990\times10^{-3}$ mm = 5.09 waves.
2. Tangential coma $3S_{II}/(2n'u') = 3\cdot2.356\times10^{-3}/(-0.25) = -28.3$ µm; sagittal $-9.4$ µm.
3. $\bar u = \sigma_{II}/(4N) = 0.5514/16 = 0.0345$ rad = 1.97°.
4. Both are unchanged by a stop shift: $S_{III}^* = S_{III} + 2\chi S_{II} + \chi^2S_I = S_{III}$; $S_V^* = S_V + \chi(3S_{III}+S_{IV})$ — **distortion does change** (unless $3S_{III}+S_{IV}=0$). Only $S_{IV}$ and $S_{III}$ are invariant here.
</details>

## Stretch task
Compute the **offence against the sine condition** for the best-form singlet of L02 (`work/L02_T2_bending.zmx`): trace real rays at $P_y$ = 0.25, 0.5, 0.75, 1.0 (Ray Trace analysis or the REAY/RANG operands — check the help for the exact operand name returning the ray angle) and compute $y/\sin U'$ vs the EFL. Relate the trend to the coma you see at a 1° field. Then bend the lens to the coma-free shape ($B = 0.83$) and repeat.

## Reflection questions
1. Why does adding more positive thin lenses at the stop never help astigmatism?
2. A colleague moves the aperture stop of a well-corrected triplet by 2 mm for mechanical reasons and finds coma barely changes but distortion does. Explain with the stop-shift equations.
3. Why might a metrology engineer care more about coma than about the same RMS wavefront of astigmatism?
4. Why does the symmetry principle not cancel spherical aberration?

<details><summary>Answers</summary>

1. For thin lenses at the stop $S_{III} = H^2\sum K_i$ — fixed by the total power. Only separating elements (different chief-ray heights) or moving the stop changes it.
2. In a corrected lens $S_I\approx0$, so $\Delta S_{II} = \chi S_I \approx 0$ and $\Delta S_{III}\approx 0$; but $\Delta S_V = \chi(3S_{III}+S_{IV})$ is not zero if the field is curved/astigmatic (it usually has $S_{IV}\ne0$).
3. Coma is asymmetric: it shifts the light centroid relative to the chief ray by an amount that varies with field and aperture, biasing position measurements; astigmatism is symmetric about the chief ray and leaves the centroid in place (to first order).
4. Spherical aberration is even in the pupil coordinate, so the contributions of the two halves have the same sign and add; symmetry only cancels terms that are odd in $\rho\cos\theta$.
</details>
