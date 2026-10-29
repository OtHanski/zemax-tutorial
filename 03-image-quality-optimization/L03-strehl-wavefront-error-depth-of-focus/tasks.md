# L03 — Tasks: Strehl ratio, wavefront error budgets and depth of focus

> Work in `work/` inside this lesson folder (e.g. save `work/L03_T3_geary_mirror.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — How good is the Maréchal approximation? (Python)
**Goal:** Know exactly when RMS wavefront predicts Strehl.
**Given / specs:** balanced aberrations $W_{040}(\rho^4-\rho^2)$, $W_{131}(\rho^3-\tfrac23\rho)\cos\theta$, $W_{222}(\rho^2\cos^2\theta-\tfrac12\rho^2)$.
**Steps:**
1. Numerically compute the RMS (area-weighted, piston removed) of each unbalanced and balanced form for unit coefficient and compare with the closed forms in lecture §2.
2. For σ = 0.05, 0.0714, 0.1, 0.15, 0.2 waves scale each aberration to that σ and compute the exact Strehl at the reference point, $S = |\langle e^{2\pi iW}\rangle|^2$ (a 2-D pupil average; no FFT needed).
3. Compare with $e^{-(2\pi\sigma)^2}$, $1-(2\pi\sigma)^2$ and $(1-(2\pi\sigma)^2/2)^2$.
4. Reproduce Geary's mirror: $W_{040} = 3.05/0.55$ waves balanced with $W_{020} = -W_{040}$. Compute σ, the exponential estimate and the exact Strehl.
**Deliverable:** `work/strehl.py`, table in `notes.md`.
**Check yourself:** RMS factors 0.2887, 0.2981 / 0.0745, 0.3536 / 0.1179, 0.25 / 0.2041. Exact S at σ = 0.1: 0.668 (SA), 0.670 (coma), 0.673 (astig) vs exp 0.674. Geary mirror: σ = 0.413 waves, exp estimate 0.0012, exact ≈ 0.13.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
r = np.linspace(0, 1, 801); t = np.linspace(0, 2*np.pi, 721, endpoint=False)
R, T = np.meshgrid(r, t); A = R                 # area weight rho*drho*dtheta
avg = lambda f: (f*A).sum()/A.sum()
def rms(W): m = avg(W); return np.sqrt(avg((W-m)**2))
def strehl(W): return abs(avg(np.exp(2j*np.pi*W)))**2
Wc = (R**3 - 2/3*R)*np.cos(T); print(rms(Wc), 1/np.sqrt(72))
```
The exact Strehl being nearly independent of aberration type for σ ≤ 0.15 λ is the practical justification for optimizing RMS wavefront.
</details>

## Task 2 — Axial intensity and depth of focus (Python)
**Goal:** See how spherical aberration shifts and shrinks the depth of focus.
**Given / specs:** $W = W_{040}\rho^4 + W_{020}\rho^2$ (waves); $W_{040} = 0, 0.5, 1.0$.
**Steps:**
1. For a rotationally symmetric pupil, $S = |\int_0^1 e^{2\pi i W(x)}dx|^2$ with $x=\rho^2$ (Geary's substitution, eq. 32.10). Implement it.
2. Plot S vs $W_{020}$ from −2.5 to +1.5 waves for the three cases. Verify the perfect case against $\mathrm{sinc}^2(\pi W_{020})$.
3. For each case find the peak S, the $W_{020}$ at the peak, and the $W_{020}$ range where S ≥ 0.8.
4. Convert to focus shift in µm for N = 2.8, λ = 0.85 µm ($\delta = 8N^2W_{020}\lambda$).
**Deliverable:** plot + table.
**Check yourself:** perfect: S ≥ 0.8 for $|W_{020}| \le 0.257$ waves → ±13.7 µm (the ±2λN² = ±13.3 µm rule uses 0.81 at exactly ¼ wave). $W_{040} = 0.5$: peak 0.946 at $W_{020} = -0.5$, S ≥ 0.8 from −0.726 to −0.274 (width 0.45 waves ≈ 24 µm, centred 26.7 µm from paraxial focus). $W_{040} = 1.0$: peak 0.80 — the S ≥ 0.8 depth of focus has collapsed to zero.

<details><summary>Hints / solution sketch</summary>
`x = np.linspace(0,1,20001); S = abs(np.trapezoid(np.exp(2j*np.pi*(a*x**2 + d*x)), x))**2`. For pure spherical the curve is symmetric about $W_{020} = -W_{040}$, so the best-Strehl plane is exactly where Geary's variance analysis puts it.
</details>

## Task 3 — Geary's mirror: three "best" foci (OpticStudio)
**Goal:** Show that the optimizer's best focus depends on the merit function.
**Given / specs:** spherical concave mirror R = −800 mm (f = 400 mm), EPD 100 mm (F/4), object at infinity, on-axis only, λ = 0.55 µm. Mirror is the stop. After the mirror: a dummy surface at the paraxial focus (thickness −400 mm from mirror), then the image surface with a variable thickness (start 0).
**Steps:**
1. Build and save as `work/L03_T3_geary_mirror.zmx`. Check $W_{040}$: Seidel Coefficients should give $W_{040} \approx 3.05$ µm (≈ 5.55 waves).
2. Optimization Wizard: Wavefront, RMS, Centroid; optimize. Record the image-surface thickness and the MF value.
3. Repeat with Spot, RMS, Centroid; then Spot, PTV, Centroid. Record thicknesses.
4. At each of the three foci read the Huygens PSF Strehl and the Zernike Standard Coefficients' RMS and estimated Strehl.
**Deliverable:** table (criterion → focus shift, RMS wavefront, Strehl Huygens, Strehl estimate).
**Check yourself:** focus shifts of magnitude 0.390 mm (wavefront), 0.521 mm (RMS spot), 0.586 mm (PTV spot) [Geary pp. 360–362]; the signs follow OpticStudio's mirror convention (Geary discusses this — the thicknesses after the mirror are negative). Wavefront MF ≈ 0.41 waves. Huygens Strehl ≈ 0.1 order (exact pupil calculation 0.13), while the Zernike-based estimate is ~0.001 — a striking demonstration of lecture §1.

<details><summary>Hints / solution sketch</summary>
Because the light travels right-to-left after reflection, "towards the mirror" is a *positive* change of the (negative) image distance — be careful when reading signs. If the RMS-spot and PTV results coincide, check that the wizard actually changed the criterion (look at the operands: `TRAC` vs `OPDX`, and the PTV variant uses different operand weighting).
</details>

## Task 4 — Wavefront error budget (pen & paper / Python)
**Goal:** Practise allocating a diffraction-limited budget.
**Given / specs:** a 940 nm receiver lens, working F/2.4, must reach polychromatic Strehl ≥ 0.75 on axis over 0–45 °C. Known: nominal design σ = 0.035 λ; fabrication Monte Carlo (Course 06) predicts σ = 0.040 λ (90th percentile); alignment σ = 0.030 λ.
**Steps:**
1. Convert the Strehl target to a total RMS using the exponential form.
2. Compute the remaining allocation for focus (thermal + mechanical).
3. Convert that allocation into an allowed defocus $\delta$ (µm).
4. Compare with the diffraction DOF ±2λN².
**Deliverable:** worked numbers in `notes.md`.
**Check yourself:** S = 0.75 → σ_tot = $\sqrt{-\ln0.75}/(2\pi) = 0.0854\lambda$. Used: $\sqrt{0.035^2+0.040^2+0.030^2} = 0.0610\lambda$. Focus allocation $\sqrt{0.0854^2-0.0610^2} = 0.0598\lambda$ → $W_{020} = 0.0598\sqrt{12} = 0.207\lambda$ → $\delta = 8N^2 W_{020}\lambda = 8\times5.76\times0.207\times0.94 = 8.97$ µm, i.e. about ±9 µm vs the ±10.8 µm diffraction DOF.

<details><summary>Hints / solution sketch</summary>
Note how little focus margin remains even with a modest design residual: in fast NIR systems the thermal focus shift (L09) is often the single largest term, so designers make the lens *athermal* first and only then polish the nominal design.
</details>

## Task 5 — Measuring DOF in OpticStudio (OpticStudio)
**Goal:** Use RMS vs Focus as a DOF tool on a paraxial and a real lens.
**Given / specs:** (a) the L02 paraxial lens `../L02-mtf-theory-and-practice/work/L02_T3_paraxial_f25.zmx` (F/2.8, 850 nm); (b) the achromat `../../02-aberrations-classical-design/L06-chromatic-aberration-and-achromats/work/L06_T2_achromat.zmx` with a single wavelength 0.5876 µm, on axis.
**Steps:**
1. RMS vs Focus, Data = Strehl Ratio, range ±0.03 mm (a) and ±0.06 mm (b). Find the S ≥ 0.8 range.
2. For (b), switch to polychromatic F-d-C and repeat. Explain the change.
3. For (b), compute the diffraction DOF ±2λN² and compare.
**Deliverable:** two plots, three numbers, short interpretation.
**Check yourself:** (a) ≈ ±13.7 µm (S = 0.8 points, cf. Task 2). (b) mono: ±2λN² = ±2 × 0.5876 × 25 = ±29.4 µm if the lens is near-perfect on axis; a residual of spherical or a slightly wrong focus shifts and narrows the range. Polychromatic: lower peak and a narrower S ≥ 0.8 range (or none) because F and C focus differently (secondary spectrum).

<details><summary>Hints / solution sketch</summary>
If the polychromatic Strehl never reaches 0.8, the achromat is not diffraction-limited in white light even though it is at one wavelength — a common surprise; Course 02 L07's apochromats are the cure for visible imaging, narrow-band NIR illumination is the cure for 3D cameras.
</details>

## Stretch task — Polishing ripple: PV vs RMS
In Python add a mid-spatial-frequency ripple $W_r = a\cos(2\pi\cdot 8\rho)$ (8 cycles across the radius) to a perfect pupil. Find $a$ such that PV = λ/4 and compute RMS and Strehl. Then compute the PSF (L01 code) and the encircled energy at 3 Airy radii. Explain why opticians specify RMS (and slope) for such errors, and where the lost energy goes (hint: rings at a radius proportional to the ripple frequency — a "grating" in the pupil).

## Reflection questions
1. Why is the Strehl ratio nearly independent of aberration type for small RMS wavefront errors?
2. A colleague reports "1.2 waves of spherical aberration" on a lens and calls it unusable. What two questions do you ask?
3. Why does the diffraction depth of focus scale with N² while the Airy radius scales with N?
4. You optimize a nearly diffraction-limited lens with the RMS spot merit function. Why might the MTF at high frequency be lower than after an RMS wavefront optimization?
5. In a wavefront error budget, why should the design residual be the smallest allocation?

<details><summary>Answers</summary>

1. For small W, $|\langle e^{ikW}\rangle|^2 \approx 1 - k^2\mathrm{Var}(W)$: only the second moment of the phase enters, not its shape. Shape matters only at higher order (fourth moments) — visible for σ ≳ 0.15 λ.
2. (i) Is it PV or RMS, and is it measured relative to the best-fit focus (balanced) or paraxial focus? Balanced, 1.2 waves of $W_{040}$ is σ = 0.089 λ, S ≈ 0.73 — only slightly worse than diffraction-limited. (ii) At what wavelength (waves at 633 nm vs 850 nm differ by 1.34×)?
3. The Airy radius is $\propto \lambda/\sin u'$ (lateral). Defocus $W_{020} = \delta\sin^2u'/2$, so the focal shift that produces a fixed W scales as $1/\sin^2u' \propto N^2$ — the longitudinal extent of the focal volume falls faster with NA than its width.
4. RMS spot puts the image plane at $W_{020} = -\tfrac43W_{040}$ and weights the pupil edge (where transverse errors are largest) heavily; RMS wavefront picks $W_{020} = -W_{040}$, which maximizes Strehl and keeps the MTF closest to the diffraction ceiling at mid/high frequencies.
5. Because fabrication, alignment and environmental errors are random and large, and adding them in quadrature means that reducing an already small term barely changes the total. Design effort is better spent on making the design *less sensitive* (Course 06 L04) than on driving the nominal residual to zero.
</details>
