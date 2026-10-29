# L02 — Tasks: Spherical Aberration and Lens Bending

> Work in `work/` inside this lesson folder (e.g. save `work/L02_T2_bending.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Thin-lens bending curve (pen & paper + Python)
**Goal:** Build intuition for $S_I(B)$ and verify the minimum-spherical bending.

**Given / specs:** N-BK7, $n_d = 1.5168$; $f = 100$ mm; EPD 20 mm; object at infinity; λ = 587.6 nm.

**Steps:**
1. By hand: compute $B_{\text{opt}}$, R1, R2, $S_{I,\min}$ and $W_{040}$ (waves) using Kidger Eq. 7.5 (lecture §1.2).
2. In Python, plot $W_{040}$ (waves) vs $B \in [-2, 3]$ for $n = 1.5168$ (N-BK7), $1.7174$ (N-SF1 at d), $1.8040$ (N-LASF44 at d — check the value in the SCHOTT catalog) and mark each minimum.
3. Repeat step 1 for magnification $m = -1$ (1:1 relay, $C = 0$) and $m = -0.1$ (a machine-vision lens imaging a field 10× larger than the sensor; $C = (m+1)/(m-1)$).
4. Recompute Kidger's refractive-index table [Kidger §7.3.1.2, p. 150] and report any entry you disagree with.

**Deliverable:** `work/bending.py`, plot `work/bending.png`, numbers in `notes.md`.

**Check yourself:** N-BK7 at infinity: $B_{\text{opt}} = 0.7397$, R1 = 59.41 mm, R2 = −397.1 mm, $S_I = 0.02046$ mm, $W_{040} = 4.35$ waves. Plano-convex ($B=1$) 4.66 waves; reversed ($B=-1$) 18.3 waves.

<details><summary>Hints / solution sketch</summary>

- $C=0$: $B_{\text{opt}} = 0$ (equiconvex), $S_{I,\min} = 0.0025\cdot(n/(n-1))^2 = 0.0025\cdot8.614 = 0.02154$ mm — but careful: at 1:1 the marginal-ray height on the lens for the same F/# on the image side is different, so compare at equal *lens* aperture $h$, as the formula assumes.
- $m=-0.1$: $C = (-0.1+1)/(-0.1-1) = -0.818$; $B_{\text{opt}} = 2(n^2-1)(0.818)/(n+2) = 0.605$ for N-BK7.
- Kidger's table: the formula gives $B_{\text{opt}} = 1.50$ at $n=2.0$ (book prints 2.25). The other rows agree to rounding.
</details>

## Task 2 — Bending study in OpticStudio (OpticStudio)
**Goal:** Reproduce the bending curve with real thick lenses and compare with thin-lens theory.

**Given / specs:** EPD 20 mm, field 0°, wavelength 0.5876 µm only. Surface 1 = STOP, N-BK7, centre thickness 4 mm. Image surface at paraxial focus via a marginal-ray-height solve on the last thickness. EFL held at 100 mm.

**Steps:**
1. Build the lens with R1 = 59.41, R2 = −397.1. Give R2 an **F/# solve** (paraxial F/# = 5) so that bending R1 keeps EFL ≈ 100 mm. Check EFL in Prescription Data.
2. Record SPHA (sum) and W040 from **Seidel Coefficients**, and $\varepsilon_y$ at $P_y = 1$ from the **Ray Fan**, for R1 = 40, 50, 59.4, 70, 100, 200 mm and for R1 = ∞ (convex side to the image). Also flip the best-form lens (swap and negate the radii) and record again.
3. Plot (Python) Seidel $W_{040}$ vs shape factor $B$ computed from the actual R1, R2; overlay your thin-lens curve from Task 1.
4. Make R1 a variable, build a merit function containing only SPHA (surface 0, target 0, weight 1) and EFFL (target 100) and optimize. Does it reach zero? Where does it stop? Save as `work/L02_T2_bending.zmx`.

**Deliverable:** `.zmx`, plot, and a short paragraph comparing thin vs thick lens.

**Check yourself:** Thick-lens minimum near $B \approx 0.73$ (R1 ≈ 59.6, R2 ≈ −378) with W040 ≈ 4.3 waves; real marginal TSA ≈ −0.104 mm vs Seidel −0.101 mm. The SPHA-only optimisation stalls at the minimum of the parabola (it cannot reach zero) — DLS will settle at the same bending. The flipped lens is ~4× worse.

<details><summary>Hints</summary>

- If the F/# solve is not available on your version's curvature solve list, instead set both curvatures variable and add EFFL = 100 to the merit function.
- Shape factor from radii: $B = (1/R_1 + 1/R_2)/(1/R_1 - 1/R_2) = (R_2 + R_1)/(R_2 - R_1)$.
- Remember the Seidel report is *paraxial focus*; the Ray Fan is at whatever the image surface is (here also paraxial focus), so they are comparable.
</details>

## Task 3 — Where is "best focus"? (OpticStudio + analysis)
**Goal:** See that best focus depends on the criterion, and verify the ½, ⅔, ¾ rules.

**Given:** your best-form lens from Task 2 (paraxial focus).

**Steps:**
1. Record the paraxial-focus RMS spot radius (Standard Spot Diagram) and RMS wavefront (OPD Fan → or Zernike/Wavefront Map RMS).
2. Replace the marginal-ray-height solve with a fixed value and use **Quick Focus** three times with different criteria: RMS spot radius, RMS wavefront. Record the focus shift relative to paraxial each time.
3. Open **Longitudinal Aberration** and read the marginal-focus LSA.
4. Compute the predicted shifts ($k$ = ½, ⅔ × LSA) and residuals from the lecture table and compare.
5. Run a **Through-Focus Spot Diagram** (or vary the image thickness by ±1 mm in 0.25 mm steps) and sketch where the spot looks like a sharp core with a halo vs a ring — compare with Kidger Fig. 4.10.

**Deliverable:** table in `notes.md`: criterion | predicted shift | OpticStudio shift | residual.

**Check yourself:** LSA ≈ 1.0 mm (a little more with higher order); RMS-wavefront focus ≈ 0.5 mm inside paraxial; RMS-spot focus ≈ 0.67 mm; RMS spot radius ≈ 50 µm at paraxial and ≈ 17–18 µm at best focus; RMS wavefront ≈ 1.3 waves at paraxial (0.298 × 4.3) and ≈ 0.32 waves at best.

<details><summary>Hints</summary>

Sign: "inside" = toward the lens = the thickness to the image *decreases*. If your shift has the wrong sign, check whether you started from the paraxial position.
</details>

## Task 4 — When does a singlet become diffraction-limited? (Python + OpticStudio)
**Goal:** Connect wavefront error to F/# scaling.

**Steps:**
1. From lecture §5, predict the F/# at which the best-form N-BK7 $f = 100$ mm singlet reaches RMS wavefront ≤ 0.07 wave after refocus (λ = 587.6 nm).
2. In OpticStudio, change the EPD to give F/6, F/7, F/8, F/10, re-bend (re-optimize R1 against RMS wavefront using the default merit function with *Wavefront, Centroid*, and the image distance as variable) and record the RMS wavefront and Strehl (Huygens PSF or FFT PSF report).
3. Repeat the prediction for $f = 25$ mm (typical machine-vision focal length): at what F/# is a 25 mm best-form singlet diffraction-limited on axis?

**Check yourself:** ≈ F/7.3 for $f = 100$ mm. For $f = 25$ mm, $S_I$ in mm scales with $f$ at fixed $N$, so $N \propto f^{1/4}$: $7.3\times(0.25)^{1/4} \approx 5.2$. OpticStudio values will be slightly worse because of higher-order spherical at the faster settings.

## Stretch task — Balancing fifth-order spherical
Design an air-spaced pair of N-BK7 lenses (both positive, total $f = 100$ mm, F/3, 1 mm air gap, 5 mm centre thickness each) and optimise for minimum RMS wavefront with variable curvatures and image distance. Then:
1. Read SPHA (third-order) from the Seidel report and convert to W040.
2. Fit $W(\rho) = W_{020}\rho^2 + W_{040}\rho^4 + W_{060}\rho^6$ in Python to the exported on-axis OPD Fan text.
3. Check whether the optimiser chose $W_{040} \approx -1.5\,W_{060}$, $W_{020} \approx 0.6\,W_{060}$ (lecture §4), and identify the zonal bulge in the Longitudinal Aberration plot.

## Reflection questions
1. Why does the optimum singlet shape change from biconvex to meniscus as the index rises?
2. A vendor sells a "best-form" lens and a cheaper plano-convex lens of the same focal length. For a collimated 850 nm laser beam of 5 mm diameter and $f = 50$ mm, does the difference matter? Estimate.
3. Why is the circle of least confusion a poor criterion for a machine-vision camera?
4. You must use a singlet at F/4. Which two parameters (other than bending) would you change first to reduce spherical aberration, and why?

<details><summary>Answers</summary>

1. The $B^2$ coefficient $\propto (n+2)/(n(n-1)^2)$ falls quickly with $n$ while the linear term's centre $2(n^2-1)/(n+2)$ grows; physically, with high index the surfaces need less curvature for the same power, and sharing the deviation between the surfaces favours a stronger first surface bent toward the image — a meniscus.
2. $h = 2.5$ mm, $K=0.02$: $h^4K^3/4 = 39.06\cdot8\times10^{-6}/4 = 7.8\times10^{-5}$ mm; with $n\approx1.51$ at 850 nm the bracket is $(8.77 - 0.43) \approx 8.34$ → $S_I \approx 6.5\times10^{-4}$ mm, $W_{040} \approx 8.1\times10^{-5}$ mm ≈ 0.10 wave at 850 nm. Plano-convex is ~7% worse: ≈ 0.10–0.11 wave, and after refocus the RMS is < 0.01 wave. Irrelevant — buy the plano-convex (but mount it curved side toward the collimated beam!).
3. It minimises the maximum ray error, which over-weights the few outermost rays; MTF/contrast at the relevant spatial frequency (or RMS wavefront for near-diffraction-limited lenses) correlates better with what the image-processing algorithm sees.
4. Higher index glass (reduces $S_{I,\min}$ by ~37% from 1.5 to 1.7) and splitting into two elements (~¼); or an aspheric surface (removes it entirely, see Course 04 L07). Reducing aperture is "cheating" the spec.
</details>
