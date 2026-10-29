# L06 — Tasks: Real Rays and the Core Analysis Tools

> Work in `work/` inside this lesson folder (e.g. save `work/L06_T3_aberration_zoo.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4–5 h

## Task 1 — A real ray by hand (pen & paper / calculator)
**Goal:** Trace one exact meridional ray through the singlet and see where paraxial optics stops being exact.
**Given / specs:** Course 01 singlet: $R_1 = 102.7$, $R_2 = -102.7$, $t = 4$ mm, $n_d = 1.51680$; image plane at the paraxial focus, 98.698 mm behind S2. Ray parallel to the axis at height $y = 5$ mm.
**Steps:**
1. At S1 compute $I$, $I'$, $U'$, and the sag at the intersection point.
2. Transfer to S2: find the intersection height (solve the ray–sphere intersection, or iterate: guess the height, compute S2's sag there, update).
3. At S2 compute $I$, $I'$, $U'$.
4. Find the ray height at the paraxial image plane (TSA at $\rho = 0.5$) and compare with $\rho^3$ scaling of the marginal value −0.1631 mm from the lecture.
**Deliverable:** your table in notes.
**Check yourself:** TSA(ρ = 0.5) ≈ −0.020 mm (≈ 1/8 of −0.163 mm).

<details><summary>Hints / solution sketch</summary>

S1: $\sin I = 5/102.7$ → $I = 2.790°$, $I' = 1.840°$, $U' = -0.951°$; sag = 0.1218 mm. The ray then reaches S2 at y ≈ 4.938 mm. Exiting angle ≈ −2.87°. The landing height at the paraxial image is −0.0200 mm. If your numbers differ in the 4th digit, check that you transferred along the *real* path length inside the glass (≈ 3.76 mm, not 4 mm, at this height). The vector-method Python of Task 2 is the easiest cross-check.

</details>

## Task 2 — Write a minimal real-ray tracer and spot diagram (Python)
**Goal:** Own the algorithm OpticStudio runs millions of times per second.
**Given / specs:** Spherical surfaces only; prescription format as in L03 `[(R, t, material), ...]`; N-BK7 Sellmeier from L05.
**Steps:**
1. Implement `trace(surfs, lam, P0, D0)`: for each surface, intersect the ray with the sphere (choose the root nearest the vertex), compute the unit normal, apply vector Snell's law $n'\mathbf r' = n\mathbf r + \mathbf a(n'\cos I' - n\cos I)$; finally intersect with the image plane. Return `None` on TIR or a miss.
2. Spot diagram: for a field angle θ, launch rays parallel to $(0, \sin\theta, \cos\theta)$ through a square grid of points on the stop (= S1 vertex plane), radius 10 mm. Compute RMS and GEO radius about the centroid and about the chief ray.
3. Compute for θ = 0° and 5° at the paraxial focus (d-light) and plot the spots with matplotlib.
4. Add a hexapolar pattern (ring $k$ has $6k$ rays at radius $k/N_r$) and compare RMS for $N_r = 6$ and $N_r = 20$ with the square grid.
5. Compare with OpticStudio's Standard Spot Diagram for the same settings (Task 4).
**Deliverable:** `work/raytrace.py`, plots, numbers.
**Check yourself (square grid ~300 rays, d-light, paraxial focus):** on axis RMS ≈ 81 µm, GEO ≈ 163 µm; 5°: RMS ≈ 159 µm about the centroid, ≈ 168 µm about the chief ray; GEO ≈ 419 µm (centroid) / 475 µm (chief). Hexapolar with 6 equal-weight rings: ≈ 100 µm on axis — the rim is over-sampled.

<details><summary>Hints</summary>

For a sphere with centre $C = (0, 0, z_v + R)$ and a ray $P + sD$: with $Q = P - C$, $s = -Q\cdot D \pm \sqrt{(Q\cdot D)^2 - (|Q|^2 - R^2)}$; take the solution whose $z$ is closest to the vertex $z_v$. The normal is $\pm(P_{hit} - C)/R$; orient it so that $\mathbf a\cdot\mathbf D > 0$ before applying Snell. Starting the rays 20 mm before the stop plane and stepping back along $-D$ makes sure they hit the stop grid points.

</details>

## Task 3 — The aberration zoo (OpticStudio)
**Goal:** Recognize aberration signatures in ray fans, spots and through-focus spots.
**Given / specs:** `../L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx`, image at the paraxial focus (M-solve).
**Steps:**
1. **Spherical:** Ray Fan, field 0°, d-light only. Sketch the curve; read TSA at $P_y = 1$ and check it against the lecture (−0.163 mm). Now move the image plane by −0.8 mm (remove solve, edit thickness) and watch the cubic tilt into an "S".
2. **Defocus only:** In a new file put a `Paraxial` surface (f = 100 mm, EPD 20) and image 99 mm behind it. Ray fan = straight lines. Change to 101 mm: slope sign flips.
3. **Coma + astigmatism:** Back in the singlet, field 5°, d-light. Read the tangential and sagittal fans: identify the even (coma) part and the different T/S slopes (astigmatism).
4. **Through Focus Spot** (Analyze → Rays & Spots → Through Focus Spot) at 5°, range ±2 mm: find the tangential and sagittal line foci.
5. **Field curvature & distortion:** open the plot; read the T and S focus shift at 5° and the distortion in %.
6. **Colour:** switch on F, d, C. On axis: different slopes per wavelength (axial colour). At 5°: is there a vertical offset between the colours at $P_y = 0$ (lateral colour)? Why is it small here? (Hint: where is the stop?)
**Deliverable:** six annotated screenshots or sketches + notes; save `work/L06_T3_aberration_zoo.zmx` (the singlet with your final settings).
**Check yourself:** (1) marginal TSA ≈ −0.163 mm; (3) at 5° the tangential fan is strongly asymmetric (coma) while the sagittal fan is close to a straight line; (4) for near-chief (small-aperture) rays the tangential focus lies ≈ 1.3 mm and the sagittal focus ≈ 0.6 mm in front of the paraxial image plane — ≈ 0.7 mm apart (the full-aperture through-focus spots also include coma and spherical, so the line foci look smeared); (5) distortion is tiny (≈ −0.02 % — the real chief ray lands ≈ 2 µm short of 8.751 mm); (6) lateral colour is small because the stop is at the lens: the chief ray passes the lens near its centre where it acts like a thin plate.

## Task 4 — Spot-diagram settings are not cosmetic (OpticStudio)
**Goal:** Learn how pattern, density and reference change the reported numbers.
**Steps:**
1. Singlet at paraxial focus, d-light, fields 0° and 5°. Standard Spot Diagram: record RMS/GEO for Hexapolar with low, default and high ray density; Square; Dithered. Reference = Chief Ray, then Centroid.
2. Compare with your Python numbers from Task 2.
3. Write two sentences on how you will report spot sizes in future (what settings you will state).
**Check yourself:** on-axis numbers converge to ≈ 81 µm RMS and 163 µm GEO as density increases; at 5° centroid-referenced RMS is ≈ 6 % smaller than chief-referenced (the coma "tail" shifts the centroid). If your hexapolar RMS is noticeably larger at low density, that is rim over-sampling.

## Task 5 — From ray fan to wavefront (OpticStudio + pen & paper)
**Goal:** Connect ray and wavefront pictures quantitatively.
**Steps:**
1. Singlet on axis, d-light, paraxial focus. Open an **OPD Fan**. Read the OPD at $P_y = 1$, 0.7071, 0.5. Check the $\rho^4$ scaling.
2. Estimate the edge OPD from the ray fan with $W(1) \approx \text{NA}\cdot|\text{TSA}|/4$ (NA ≈ 0.10).
3. Run Quick Focus with the **Wavefront** criterion and then with **RMS spot radius**. Compare the two focus positions and the OPD fans. Which is closer to the paraxial focus?
**Check yourself:** OPD edge ≈ 6.8 waves at paraxial focus (OpticStudio's sign convention may show it negative); 0.42 waves at 0.5 (∝ ρ⁴). Estimate: 0.10 × 0.163/4 = 0.0041 mm ≈ 7 waves. After refocusing, the peak-to-valley OPD drops to ≈ ¼ of the paraxial-focus value (≈ 1.7 waves) — spherical aberration balanced by defocus. The two Quick Focus criteria land at slightly different planes (the RMS-wavefront optimum for pure ρ⁴ SA is at the "mid-focus", while the RMS-spot optimum sits a bit closer to the marginal focus).

## Task 6 — Footprints for mechanical sizing (OpticStudio)
**Goal:** Use the Footprint Diagram to size lenses and spot vignetting.
**Steps:**
1. Open `../L04-stops-pupils-fields/work/L04_T3_stop_front20.zmx` (stop 20 mm in front of the lens).
2. Footprint Diagram on surface 2 (the rear lens surface), all fields, all wavelengths. Read the beam's maximum radial extent.
3. Choose a clear aperture with a 1 mm margin, and a mechanical diameter with an additional 1 mm for the mount. Set the semi-diameters accordingly and compute the edge thickness (L02).
**Check yourself:** beam extent on S2 ≈ 11.8 mm radius (marginal ray of the 5° field) → clear semi-diameter ≈ 12.8 mm, mechanical ≈ 13.8 mm; edge thickness at r = 13.8 mm is ≈ 2.1 mm (still OK for a 4 mm thick lens).

## Stretch task
Extend your Python tracer to compute OPD relative to a reference sphere at the exit pupil (Kidger §3.5) for the on-axis case, and reproduce the OPD fan values above. Then fit $W(\rho) = W_{020}\rho^2 + W_{040}\rho^4$ to your traced values at a defocused image plane and recover the defocus you applied.

## Reflection questions
1. Why do fast lenses get specified in waves and slow lenses in micrometres?
2. Why is the GEO radius a poor optimization target?
3. A ray fan has a parabola-shaped tangential curve and a flat sagittal curve. What aberration dominates?
4. Why does referencing a spot diagram to the centroid reduce the RMS for coma but not for spherical aberration?
5. Your OPD fan shows 0.1 waves peak-to-valley but the spot diagram shows a 10 µm RMS spot at F/8. Which do you trust, and why?

<details><summary>Answers</summary>

1. $\varepsilon = -(1/\text{NA})\partial W/\partial\rho$: at large NA a given wavefront error produces small ray errors (dominated by diffraction), so wavefront metrics are meaningful; at small NA ray errors are large compared to the Airy disk and spot metrics are meaningful.
2. It is set by one extreme ray — noisy, discontinuous, sensitive to vignetting and sampling; RMS is smooth and statistically meaningful.
3. Coma (odd in wavefront, even in transverse fan).
4. Spherical aberration is rotationally symmetric, so its centroid coincides with the chief ray; coma is asymmetric and its centroid is shifted from the chief ray.
5. Trust the wavefront: at F/8 and 0.55 µm the Airy radius is ≈ 5.4 µm; 0.1 λ P-V is essentially diffraction-limited — the geometric spot is not meaningful when it is comparable to the Airy disk. (If the spot is truly 10 µm RMS geometric while the OPD is 0.1 λ, check sampling/reference settings — those two numbers are inconsistent at F/8.)

</details>
