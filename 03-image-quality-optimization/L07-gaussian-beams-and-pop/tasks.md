# L07 — Tasks: Gaussian beams and Physical Optics Propagation

> Work in `work/` inside this lesson folder (e.g. save `work/L07_T2_fiber_relay.zmx`). Commit your designs and a short `work/notes.md` with answers. POP is available in Professional/Premium.
> Estimated time: ~6 h

## Task 1 — A Gaussian-beam ABCD library (Python)
**Goal:** Own the q-parameter mathematics before trusting a tool.
**Given / specs:** λ = 0.85 µm unless stated; matrices act on $(y, u)$: free space $\begin{pmatrix}1&d\\0&1\end{pmatrix}$, thin lens $\begin{pmatrix}1&0\\-1/f&1\end{pmatrix}$.
**Steps:**
1. Write `prop(q, M)`, `w_of(q)`, `R_of(q)`, `waist_after(q)` (distance to next waist and its radius). Include an optional $M^2$ (use $\lambda \to M^2\lambda$ in the beam-size formulas).
2. Reproduce the lecture worked example (fibre $w_0 = 2.8$ µm, $f_1 = 10$ mm at its front focal distance, 100 mm, $f_2 = 50$ mm).
3. **Waist shift:** a collimated beam with $w = 0.5$ mm (waist at distance $s$ before an $f = 100$ mm lens). Compute the focused waist position and size for $s = 0$, 100 and 200 mm, and plot waist position vs $s$ from −500 to +1500 mm.
4. **$M^2$:** repeat step 2 with $M^2 = 1.5$ and 4 (same $W_0$ at the fibre). How do the focused spot and its Rayleigh range change?
5. **Truncation:** compute transmitted power for aperture radius $a = w, 1.25w, 1.5w, 2w$.
**Deliverable:** `work/gauss.py` + printed table.
**Check yourself:** step 2: $z_R$ = 29.0 µm, θ = 96.6 mrad, collimated $w$ = 0.966 mm, residual divergence 0.28 mrad, focused waist 14.0 µm at 50.008 mm, $z_R''$ = 0.724 mm. Step 3 ($z_R$ = 924 mm for the 0.5 mm beam): waist 98.84 mm behind the lens for $s = 0$ (1.16 mm *inside* the focal point), exactly 100.00 mm for $s = f$, 101.16 mm for $s = 200$ mm; waist ≈ 54 µm in all three. Step 4: with the same input $W_0$, the far-field divergence and hence the collimated size scale with $M^2$ while the focused spot stays ≈ 5× the input (imaging), but its Rayleigh range shrinks by $M^2$. Step 5: 86.5%, 95.6%, 98.9%, 99.97%.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
lam = 0.85e-3                                        # mm
prop  = lambda q, M: (M[0,0]*q + M[0,1])/(M[1,0]*q + M[1,1])
T = lambda d: np.array([[1, d], [0, 1]]); L = lambda f: np.array([[1, 0], [-1/f, 1]])
w_of = lambda q, M2=1: np.sqrt(-M2*lam/(np.pi*np.imag(1/q)))
def waist_after(q, M2=1):                            # q = z + i zR  ->  waist at -Re(q)
    return -q.real, np.sqrt(M2*lam*q.imag/np.pi)
zR = np.pi*(2.8e-3)**2/lam; q = 1j*zR
for M in (T(10), L(10), T(100), L(50)): q = prop(q, M)
print(waist_after(q))
```
For $M^2 \ne 1$ propagate the embedded Gaussian with $\lambda_\text{eff} = M^2\lambda$: that is exactly the embedded-Gaussian model of Kenyon eq. 14.43.
</details>

## Task 2 — Paraxial Gaussian Beam in OpticStudio
**Goal:** Reproduce Task 1 in the software and learn its conventions.
**Given / specs:** sequential file: object at the fibre tip (object thickness 10 mm), Paraxial surface f = 10 mm (stop, semi-diameter 3 mm), 100 mm air, Paraxial surface f = 50 mm, image at 50 mm. λ = 0.85 µm. Aperture: Object Space NA 0.1 (only for rays).
**Steps:**
1. Save as `work/L07_T2_fiber_relay.zmx`. Open Paraxial Gaussian Beam; set waist 0.0028 mm at the object surface (position 0), $M^2$ = 1.
2. Read beam size, waist, waist location and Rayleigh range at each surface. Compare with Task 1.
3. Insert a `GBPS` operand for the image surface; vary the image distance and confirm the minimum is at the waist location.
4. Set $M^2$ = 4. Compare.
**Deliverable:** table OpticStudio vs Python.
**Check yourself:** agreement to ≥ 4 significant figures (both are exact paraxial calculations). If you are off by a factor √2 or 2, you mixed radius/diameter or 1/e/1/e² conventions — check the analysis' Text tab definitions.

<details><summary>Hints / solution sketch</summary>
The ray-traced spot diagram at the image will show (nearly) a point — rays know nothing about the 14 µm waist. That contrast is the reason this lesson exists.
</details>

## Task 3 — POP: truncation, sampling and the focal spot
**Goal:** Use POP correctly and see effects that neither rays nor paraxial beams show.
**Given / specs:** the Task 2 file.
**Steps:**
1. Open Physical Optics Propagation: Beam type Gaussian Waist, waist X = Y = 0.0028 mm, start surface 1 (object), end surface = image; sampling 256×256; press Auto for the array width. Display: irradiance, and cross-section. Save beam files at all surfaces.
2. Read the Prop Report: propagator chosen at each step (angular spectrum vs Fresnel), pilot-beam data, warnings. Compare the image-plane 1/e² radius with Task 2.
3. **Sampling convergence:** 128, 256, 512, 1024; record peak irradiance and beam radius at the image.
4. **Truncation:** set the semi-diameter of the $f_2$ lens (fixed, "circular aperture") to 0.966, 1.45 and 2.0 mm. Record transmitted power (POP's total power at the image) and the cross-section of the focal spot (look for rings on a log scale).
5. Turn on "Compute Fiber Coupling Integral" with a receiving Gaussian of waist 14.0 µm at the image and record the coupling efficiency for the three apertures.
**Deliverable:** table (sampling vs results; aperture vs power, peak, coupling), log-scale screenshots, short commentary.
**Check yourself:** unclipped image radius ≈ 14.0 µm. Transmitted power ≈ 86.5% / 98.9% / 99.97% for the three apertures (aperture radius = w, 1.5w, ≈2w). Hard clipping at $a = w$ produces visible rings around the focal spot and lowers coupling into the matched 14 µm mode noticeably below the transmitted fraction (the field shape no longer matches); at $a \ge 2w$ coupling ≈ 100%.

<details><summary>Hints / solution sketch</summary>
If the result changes when you double the array *width* (not just the sampling), the array was too small: diffracted light was wrapping around. Clipped beams need a wider array than unclipped ones.
</details>

## Task 4 — An astigmatic edge-emitter collimator (OpticStudio POP + analysis)
**Goal:** Model a realistic laser-diode source.
**Given / specs:** 850 nm edge-emitting diode, divergence 25° (fast) × 10° (slow) FWHM full angle, $M^2$ ≈ 1 in both axes (single-mode for this exercise); collimator: Paraxial f = 4.5 mm with the emitter at its front focal point.
**Steps:**
1. Convert to 1/e² half-angles and to equivalent waists $w_0 = \lambda/(\pi\theta)$ in each axis.
2. Predict the collimated 1/e² radii in x and y and the aspect ratio.
3. In POP use a Gaussian (or Astigmatic Gaussian) beam with different X and Y waists; enable **Separate X, Y**. Propagate 50 mm beyond the collimator. Compare with your prediction.
4. Explain why the fast axis is outside the paraxial regime and what that implies for the real beam size (compare $f\theta$ with $f\tan\theta$).
5. Propose two ways to circularize the beam (anamorphic prism pair, cylindrical telescope) and compute the magnification needed.
**Deliverable:** numbers, a POP screenshot, a paragraph on circularization.
**Check yourself:** θ (1/e² half) = 21.2° (0.371 rad) and 8.49° (0.148 rad); $w_0$ = 0.73 µm and 1.83 µm; collimated radii ≈ 1.67 mm (fast) and 0.67 mm (slow) — aspect ratio ≈ 2.5, so a 2.5× anamorphic magnification of the slow axis (or 0.4× of the fast axis). A 0.73 µm waist is smaller than the wavelength: paraxial Gaussian theory is only approximate here, and the real fast-axis size ($f\tan\theta \approx 1.75$ mm) also depends on collimator aberrations at NA ≈ 0.36 — a real design needs an aspheric collimator and POP (or vector) checks.

<details><summary>Hints / solution sketch</summary>
Kenyon §14.7.1 mentions anamorphic prism pairs for exactly this reshaping. The beam's astigmatism (the two axes' waists at different depths inside the chip) adds a focus offset between axes; datasheets quote it as "astigmatic distance" — include it as a waist position offset between X and Y in POP.
</details>

## Stretch task — VCSEL dot projector budget
A multimode VCSEL emitter has $W_0$ = 4 µm and $M^2$ = 2 at 940 nm. A collimator of f = 3 mm (emitter at front focal point) feeds a DOE that replicates the beam into a dot pattern. (a) Compute the collimated beam radius and the residual divergence (≈ $W_0/f$). (b) What is the 1/e² dot diameter at 1 m (ignoring the DOE's own effects)? (c) How does the dot size compare with a camera pixel footprint at 1 m for an 8 mm lens and 3 µm pixels? (d) Why do dot projectors often use arrays of many emitters, and how does that change speckle?
**Check yourself:** residual divergence 1.33 mrad → dot diameter ≈ 2.7 mm at 1 m (plus the initial beam size); pixel footprint at 1 m ≈ 3 µm × 1000/8 = 0.375 mm, so a dot spans ≈ 7 pixels.

## Reflection questions
1. Why does a Gaussian beam focused by a lens have its waist *inside* the focal point, and when does this matter?
2. A beam has $M^2 = 3$. By how much is its minimum focused spot larger than an ideal beam's, for the same focusing lens and the same collimated beam size?
3. When is the Paraxial Gaussian Beam analysis sufficient, and when must you use POP?
4. What does the POP pilot beam do, and why should you read the Prop Report?
5. Why is laser speckle a problem for structured-light 3D, and how do source choices (VCSEL arrays, LEDs) mitigate it?

<details><summary>Answers</summary>

1. The lens adds curvature to the beam's own wavefront; the resulting q has its waist where the real part vanishes, at $f/[1 + (\lambda f/\pi w^2)^2]$. It matters when $\lambda f/(\pi w^2)$ is not ≪ 1, i.e. weakly focused or small beams (long focal length, small input beam) — laser-line generators, fibre couplers with small beams.
2. With the same collimated 1/e² radius $W$ at the lens, the focused waist is $W_0' = M^2\lambda f/(\pi W)$ — 3× larger than for an ideal beam. Its Rayleigh range $\pi W_0'^2/(M^2\lambda) = M^2\lambda f^2/(\pi W^2)$ is 3× longer. (Put differently: to get the *same* spot size as the ideal beam you would need 3× the input size, and then the depth of focus would be 3× *shorter* than an ideal beam with that spot.)
3. Sufficient for ideal (or $M^2$-scaled) beams through paraxial, unclipped, aberration-free systems. POP for aberrations (fast collimators, off-axis), apertures/clipping, spatial filters, fibre coupling, near-field and non-Gaussian beams.
4. It is the best-fit Gaussian at each surface; POP removes its phase to reduce sampling needs and uses its Rayleigh range to choose the angular-spectrum or Fresnel propagator. Warnings about low pilot-beam sampling at intermediate surfaces do not show in the final plot, so you must read the report and beam files.
5. Speckle is random coherent interference that modulates the imaged pattern, adding noise to fringe phase or dot centroid estimates. Many mutually incoherent emitters (VCSEL arrays), broader spectra (LEDs, multimode), angular diversity and larger collection apertures average speckle down.
</details>
