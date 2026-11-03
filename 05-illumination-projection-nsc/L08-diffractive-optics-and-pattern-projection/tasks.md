# L08 — Tasks: Diffractive Optics and Pattern Projection

> Work in `work/` inside this lesson folder (e.g. save `work/L08_T3_fanout_seq.zmx`). Commit your designs, scripts and a short `work/notes.md` with answers.
> Estimated time: ~6–7 h (Task 1 ≈ 2 h, Task 2 ≈ 0.75 h, Task 3 ≈ 1 h, Task 4 ≈ 1.5 h, Task 5 ≈ 1 h, Task 6 ≈ 0.5 h)

Unless stated otherwise, the wavelength is **0.85 µm**, the medium is air, and incidence is normal. Task 1's output (an order-efficiency table) feeds Task 4, and the capstone (L09) reuses `work/doe.py`.

## Task 1 — Design a Dammann fan-out grating and compute its orders by FFT (Python)
**Goal:** Build `work/doe.py`, a small scalar-DOE toolkit. Use it to design 1×3, 1×5 and 1×7 binary Dammann gratings, and to quantify how fabrication and wavelength errors feed the zero order.

**Given / specs:** A symmetric binary 0/π phase cell with period normalised to 1, transitions $0 < x_1 < \dots < x_K < 0.5$ in the half period, transmission $s(x) = +1$ on $[0, x_1)$, $-1$ on $[x_1, x_2)$, …, mirrored about $x = 0$. Fan-out 1×N with N = 2M+1 and target orders −M…+M of equal power.

**Steps:**
1. `cell(x_trans, Ns=2**14)` → sampled $s(x)$ over one period. `orders_fft(t, mmax)` → $\eta_m = |\mathrm{FFT}(t)/N_s|^2$ for $m = -m_\text{max}\dots m_\text{max}$. Test it on a 50 % duty π-grating (one transition at 0.25). Expect $\eta_0 = 0$, $\eta_{\pm1} = 4/\pi^2$, $\eta_{\pm3} = 4/(3\pi)^2$, even orders 0, $\sum\eta = 1$.
2. `orders_analytic(x_trans, mmax)` using the closed-form $c_0, c_m$ of lecture §5.2. Check it agrees with the FFT to < 10⁻⁴. (Sampling error scales as $1/N_s$. Why?)
3. Design: for M = 1, 2, 3 use K = M transitions. Maximise the total efficiency $\eta_\text{tot} = \sum_{|m|\le M}\eta_m$ subject to equal orders. Two practical ways:
   - `scipy.optimize.least_squares` on the residuals $\eta_m - \eta_0$ ($m = 1..M$) from a few thousand random starts, then keep the solution with the largest $\eta_\text{tot}$; or
   - `minimize(..., method='SLSQP')` maximising $\eta_\text{tot}$ with equality constraints.

   Report transitions, $\eta_\text{tot}$, per-order efficiency, and uniformity $U = (\eta_{\max} - \eta_{\min})/(\eta_{\max} + \eta_{\min})$.
4. Plot $\eta_m$ for $|m| \le 11$ (log scale) for your 1×5 design. Which higher order is strongest? Export a table `work/dammann_1x5_orders.csv` with $m$ and $\eta_m$ for $m = -5..5$ (input for Task 4).
5. **Errors.** For a phase depth $\varphi = \pi(1+\varepsilon)$, write $t = A + B\,s(x)$ with $A = (1+e^{i\varphi})/2$ and $B = (1-e^{i\varphi})/2$. Compute $\eta_0$ and $\eta_{\pm1}$ of the 1×5 design for $\varepsilon$ = 0, +2 %, +5 %, and for the 850 nm design used at 940 nm ($\varphi = \pi\cdot 0.85/0.94$, ignoring material dispersion). Repeat for the crossed **2D 5×5** ($t = A + B\,s(x)s(y)$, central dot $|A + Bc_0^2|^2$). Report the ratio (central dot)/(typical dot).
6. Compute the π etch depth in fused silica ($n$ = 1.4525 at 850 nm) and what +5 % means in nm.

**Deliverable:** `work/doe.py`, design table, order plot, CSV, error table in `notes.md`.

**Check yourself:**
- 1×3: one transition at 0.1324 (or the equivalent 0.3676), $\eta_\text{tot}$ = 66.4 %, 22.1 % per spot.
- 1×5: transitions 0.1324, 0.4807; $\eta_\text{tot}$ = 77.4 %, 15.5 % per spot. Strongest unwanted orders are ±5 (3.27 % each); orders up to |m| ≤ 5 hold 84.9 % in total.
- 1×7: best found 0.1229, 0.3448, 0.3954 (or the mirror solution 0.1046, 0.1552, 0.3771); $\eta_\text{tot}$ = 65.5 %, 9.4 % per spot. (Adding transitions did not help in our searches. Report it if you beat this.)
- 2D 5×5: 2.39 % per dot, 59.9 % total.
- Errors, 1D 1×5: $\eta_0$ = 15.5 % (ideal), 15.6 % (+2 %), 16.0 % (+5 %), 17.4 % (at 940 nm), against $\eta_1$ ≈ 15.4 %, 15.4 %, 15.1 %.
- Errors, 2D: central dot 2.49 % / 3.00 % / 4.59 % against ≈ 2.39 % / 2.38 % / 2.34 % for a typical dot.
- Fused-silica π depth 0.939 µm; 5 % = 47 nm.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
def cell(xt, Ns=2**14):
    x = (np.arange(Ns)+0.5)/Ns
    u = np.where(x <= 0.5, x, 1-x)            # mirror symmetry
    k = np.searchsorted(np.sort(xt), u)       # number of transitions passed
    return np.where(k % 2 == 0, 1.0, -1.0)
def orders_fft(t, mmax):
    c = np.fft.fft(t)/t.size
    return {m: abs(c[m % t.size])**2 for m in range(-mmax, mmax+1)}
```
- The analytic and FFT results differ by $O(1/N_s)$ because the sampled edges are quantised to one sample.
- `least_squares(lambda x: eta(x)[1:]-eta(x)[0], x0, bounds=(0, 0.5))` converges in milliseconds. Collect solutions with cost < 1e-16 and sort by $\eta_\text{tot}$. You will see several distinct solution families. For 1×5 there is also a poor one at 48.2 %.
- The 1×5 cell has $c_0 = +0.393$ (positive), so the error term $A$ adds **in phase** to the central order. A cell with $c_0 < 0$ would initially *reduce* it. The sign of the coefficient matters, not just its magnitude.
- Why the 2D central dot is hit harder: in 1D the ideal $c_0^2$ = 15.5 % dwarfs $|A|^2$. In 2D the ideal central amplitude is $c_0^2 = 0.155$ while $|A|$ stays the same, so the relative disturbance roughly doubles.
</details>

## Task 2 — Grating, blaze, hybrid and speckle numbers (pen & paper)
**Goal:** Fluency with the handful of formulas you will use daily.

**Given / specs and questions:**
1. A 1×7 fan-out must cover ±15° at 850 nm. Give the period (µm and lines/µm), the angles of orders 1–3, their positions on a wall at 1 m, and the highest propagating order.
2. The same DOE is used at 940 nm. Where does order 3 go? A VCSEL drifts +0.065 nm/K: by how many mm does order 3 move on the wall for a 40 K warm-up?
3. Blazed kinoform designed for 550 nm, used at 450 and 650 nm: $\eta_{0}, \eta_1, \eta_2$ (ignore dispersion). Same for a design at 850 nm used at 940 nm.
4. 2-, 4-, 8-level staircases: first-order efficiency.
5. Hybrid achromat, $f$ = 100 mm, F/5 (EPD 20 mm), N-BK7 ($\nu_d$ = 64.17, $P_{g,F}$ = 0.5349), diffractive ($\nu$ = −3.453, $P_{g,F}$ = 0.2956): powers of both parts, $A_1$ with $R_\text{norm}$ = 10 mm and $M$ = 1, zone count, minimum zone width, and secondary spectrum. Compare with an N-BK7/N-SF5 doublet ($\nu$ = 32.25, $P_{g,F}$ = 0.5984).
6. Speckle: receiver at working F/2.8, magnification ≈ −0.05, 850 nm. Speckle grain size at the sensor, and compare with a 3.45 µm pixel. Triangulation with $\sin u_\text{obs}$ = 0.02 and $\theta$ = 15°: speckle-limited $\delta z$ for $C$ = 1 and for 16 averaged independent patterns.

**Deliverable:** answers in `notes.md`.

<details><summary>Hints / solution sketch</summary>

1. $d$ = 3(0.85)/sin 15° = 9.852 µm (0.1015 lines/µm); 4.95°, 9.94°, 15.00°; 86.6, 175.2, 267.9 mm; $m_{\max} = \lfloor 9.852/0.85\rfloor$ = 11 (71.6°).
2. sin θ₃ = 3(0.94)/9.852 = 0.2862, so θ₃ = 16.63° and 298.7 mm on the wall. Δλ = 2.6 nm gives Δ(sin θ) = 3(0.0026)/9.852 = 7.92 × 10⁻⁴. Δx = L Δ(sin θ)/cos³θ = 1000(7.92×10⁻⁴)/0.9659³ ≈ **0.88 mm**. The derivative of tan θ with respect to sin θ is 1/cos³θ.
3. 450 nm: α = 1.222, η₀ = 2.8 %, η₁ = 84.8 %, η₂ = 6.9 %. 650 nm: α = 0.846, η₀ = 3.1 %, η₁ = 92.5 %, η₂ = 1.6 %. 940 nm on an 850 nm design: η₁ = 97.0 %, η₀ = 1.1 %, η₂ = 0.7 %.
4. 40.5 %, 81.1 %, 95.0 %.
5. $\phi_d/\phi = 3.453/67.62$ = 0.0511, so $f_d$ = 1958 mm and $f_r$ = 105.4 mm. $A_1 = -\pi(10)^2/(0.5876\times10^{-3}\cdot1958)$ = −273 rad. Zones $r^2/(2\lambda f_d)$ = 43.5. Minimum zone $\lambda f_d/r$ = 115 µm. Secondary spectrum magnitude $f|P_r-P_d|/|\nu_r-\nu_d|$ = 0.354 mm (hybrid) vs 0.199 mm (N-BK7/N-SF5). For reference, an uncorrected N-BK7 singlet has $f/\nu$ = 1.56 mm of primary axial colour.
6. Grain ≈ 2.44(0.85)(2.8)(1.05) = 6.1 µm, about 2 pixels, so the camera fully resolves the speckle. $\delta z = 0.85/(2\pi\cdot0.02\cdot0.2588)$ = 26 µm; with 16 patterns, $C$ = 0.25 and δz ≈ 6.5 µm.
</details>

## Task 3 — Fan-out orders in sequential mode (OpticStudio)
**Goal:** See that the sequential Diffraction Grating surface traces orders exactly as the grating equation says, one order per configuration, and learn the failure mode for evanescent orders.

**Given / specs:** Units mm. Wavelength 0.85 µm. Object at infinity, EPD 2 mm, field 0°. Surfaces:
| # | Type | Notes |
|---|---|---|
| 1 (STO) | Diffraction Grating | flat, 0.1015 lines/µm, order 0, thickness 10 |
| 2 | Paraxial | focal length 100 mm, thickness 100 |
| IMA | Standard | |

**Steps:**
1. Build the file. Confirm with order 0 that the beam focuses on axis.
2. Set the order to 1, 2, 3 and read the chief-ray image height (Single Ray Trace, or the RAYY-type real-ray data in Prescription/Ray Trace). Compare with $f\tan\theta_m$.
3. Use the **Multi-Configuration Editor**: 7 configurations, a PARn row for the grating's Diffraction Order column (check which parameter number that column is), values −3…+3. Show all configs in the 3D Viewer. Save `work/L08_T3_fanout_seq.zmx`.
4. Set the order to 11, then 12. What happens? Read the error message.
5. Change the wavelength to 0.94 µm with the order at 3. Compare with Task 2.2.
6. Replace the paraxial lens by ~1000 mm of air (no lens) and an image surface. Measure the order-3 position and compare with the 267.9 mm of the lecture. Then tilt the beam in **x** by giving a field of 5° in x (Field Type: Angle, X = 5°). Watch order 3 in x–y: why does it no longer lie on the y axis at exactly the same height? (Conical diffraction: the grating equation holds for direction cosines, $\beta_m = \beta_i + m\lambda/d$ with α unchanged.)

**Deliverable:** `.zmx`, table of image heights (computed vs. OpticStudio), answers in `notes.md`.

**Check yourself:** Image heights 8.660, 17.518, 26.796 mm for orders 1–3 (paraxial lens maps $f\tan\theta$ exactly); order 11 at 301.1 mm. Order 12 is evanescent (sin θ = 1.035), so the ray fails with an error. The sign of the height for positive orders follows OpticStudio's convention. Record it, it will matter in NSC.

<details><summary>Hints</summary>

- If the configuration with order 0 and the one with order +1 look identical, you probably edited the lines/µm column instead of the order.
- For the conical case in step 6: with the incident direction cosines $(\alpha_i, \beta_i)$ and grooves parallel to x, order m leaves with $(\alpha_i, \beta_i + m\lambda/d)$. The ray stays on a cone, not in a plane. This is the direction-cosine picture of lecture §2.2.
</details>

## Task 4 — A 5×5 dot projector in NSC with ray splitting by order (OpticStudio NSC)
**Goal:** Model a 2D fan-out with crossed gratings, ray-split by order using **your** efficiencies from Task 1, and check positions (pincushion) and power bookkeeping.

**Given / specs:** New NSC file, units mm, 0.85 µm, source units W.
| Obj | Type | Settings |
|---|---|---|
| 1 | Source Ellipse | Ø 2 mm (half widths 1 mm), collimated, 1 W, Z = 0; layout rays 1, analysis rays 2 × 10⁴ |
| 2 | Diffraction Grating | Z = 5, thin fused-silica plate (e.g. 1 mm thick, semi-aperture 3 mm), 0.1015 lines/µm, grooves along x |
| 3 | Diffraction Grating | Z = 7, same, **rotated 90° about Z** (Tilt Z = 90) |
| 4 | Detector Rectangle | Z = 1000, half widths 300 × 300 mm, 601 × 601 pixels |

**Steps:**
1. Open the sample *Diffraction grating multiple orders.zmx* (Samples → Non-sequential → Diffractives) and inspect **Object Properties → Diffraction** of its grating: which split option is used, and how are the orders and their relative energies specified? Write down the exact labels your version uses.
2. On both gratings, set the split to the table/user-specified option, Start Order −5, Stop Order +5, and enter $\eta_m$ from `dammann_1x5_orders.csv`. (If your version only offers the DLL option for arbitrary energies, use `diff_samp_1.dll` as in the Holo/Or tutorial and note how it defines energies.)
3. Ray Trace with **Split NSC Rays** on (and Use Polarization off). Raise Maximum Segments per Ray if you get warnings.
4. Detector Viewer: count the dots, read the power of the central 5×5 dots (pixel-sum boxes or filter strings), and read the total on the detector. Does OpticStudio renormalise your table if it sums to less than 1? Test this explicitly by also tracing with only orders −2…+2 entered.
5. Measure the positions of order (2,0) and of the corner order (2,2). Compare with $x = L\alpha/\gamma$.
6. Change the wavelength to 0.94 µm (keep the table, since NSC will not recompute efficiencies). Note which numbers changed (positions) and which did not (powers). That is the core lesson of this course on DOEs.
7. Save `work/L08_T4_dots_nsc.zmx`.

**Deliverable:** `.zmx`, detector screenshot, table of positions and powers, and answers in `notes.md`.

**Check yourself:**
- 25 strong dots plus weaker higher orders on the detector. Dots ±5 (3.27 % in 1D) are at sin θ = 0.431 (25.6°, 479 mm on axis), which is outside a 300 mm detector. Enlarge it to see them.
- With a full −5…+5 table, each of the 25 central dots ≈ 23.9 mW (×1 W), central 5×5 total ≈ 0.60 W. Monte-Carlo noise with 2 × 10⁴ rays is a few %, so report ray counts (L02).
- Order (2,0) at 175.2 mm and corner (2,2) at (177.9, 177.9) mm: pincushion of 1.6 %.
- At 0.94 µm, positions scale by about 0.94/0.85 in sin θ, and the powers are unchanged in the trace. In reality the zero order would grow (Task 1.5).

<details><summary>Hints</summary>

- The grating object's default order is used only when not splitting. If you see one dot, the split is off or Split NSC Rays is unchecked.
- Ray count: each grating multiplies the rays by up to 11 orders, so 2 × 10⁴ source rays become up to 2.4 × 10⁶ segments. Keep analysis rays modest.
- Filter strings (L02/L07) help isolate rays by object hit. Use Path Analysis if you want to see order paths ranked by power.
- If the gratings' internal faces produce Fresnel ghost orders, set the faces to uncoated or turn off ray splitting at refractive interfaces for this exercise, so you see the diffraction effect alone. Then put the Fresnel splitting back and look at the ghosts (L07).
</details>

## Task 5 — A hybrid refractive–diffractive achromat (OpticStudio)
**Goal:** Use Binary 2 to colour-correct a singlet and compare it honestly with the Course 02 doublet.

**Given / specs:** $f$ = 100 mm, F/5 (EPD 20 mm), object at infinity, semi-field 1°, wavelengths F, d, C (primary d), plus g = 0.4358 µm with weight 0 for inspection. N-BK7 singlet, centre thickness 4 mm, stop at the lens. Surface 2 (rear) is **Binary 2**: Diffraction Order 1, Normalization Radius 10 mm, 2 terms.

**Steps:**
1. Start with $A_1 = A_2 = 0$, R1 variable, R2 variable, and a marginal-ray-angle solve or variable image distance. MF: EFFL = 100, plus the default RMS-spot (centroid) merit function. Optimise and note the chromatic focal shift (≈ $f/\nu$ ≈ 1.5 mm between F and C).
2. Pre-set $A_1$ = −273 (Task 2.5). Check EFFL changes by only a few %, and in the right direction. If the focal length gets **longer**, your sign convention is flipped. Note it.
3. Make $A_1$, $A_2$ variables and add AXCL = 0 (F vs C). Optimise. Record $A_1$, $A_2$, the refractive radii, and the Chromatic Focal Shift curve. Read the zone count/minimum zone from your own calculation or the `Phases.zpl` macro mentioned in the Ansys Binary 2 article.
4. Open `../../02-aberrations-classical-design/L06-chromatic-aberration-and-achromats/work/L06_T2_achromat.zmx` (or `L06_T3_dmf.zmx`). Compare: radii (how bent?), Chromatic Focal Shift including g, polychromatic RMS spot, Petzval/field curvature at 1° (Seidel Diagram).
5. Efficiency penalty (by hand): the trace assumes 100 % in order +1 at all wavelengths. With a blaze at 0.5876 µm, compute $\eta_1$ at F, d, C, g from $\mathrm{sinc}^2(1-\lambda_0/\lambda)$ and estimate the fraction of light in the 0th and 2nd orders. Where would that light land? (Order 0: an N-BK7 singlet's focus, about 5 % beyond the design focus. Order 2: much shorter focus.)
6. Repeat step 3 for an NIR receiver band 0.84–0.86 µm (primary 0.85). How much $A_1$ is needed now, and is the hybrid worth it compared with an achromat for this narrow band? Save `work/L08_T5_hybrid.zmx` and `work/L08_T5_hybrid_nir.zmx`.

**Deliverable:** both `.zmx` files, comparison table (hybrid vs doublet), efficiency estimate, short verdict in `notes.md`.

**Check yourself:**
- $A_1$ ≈ −270 rad (thin-lens prediction −273; thickness and bending change it by a few %), DOE focal length ≈ 2 m, ~43 zones, minimum zone ≈ 115 µm.
- The refractive part is a nearly plano-convex/best-form singlet with gentle curvature, far weaker than the doublet's crown (R ≈ ±45–60 mm).
- F and C share a focus. The g focus is about 0.35 mm away, roughly twice as far as for the N-SF5 doublet. The hybrid's field curvature is that of an $f$ ≈ 105 mm singlet (the DOE adds no Petzval).
- Blaze efficiencies with λ₀ = 587.6 nm (no material dispersion): F 86.5 %, d 100 %, C 96.4 %, g 66.0 %. At g, 19 % goes into order 2 and 4 % into order 0.

<details><summary>Hints</summary>

- Efficiency check: α = λ₀/λ = 1.2087 (F), 0.8953 (C), 1.3481 (g); $\mathrm{sinc}^2(1-\alpha)$ gives the values above.
- If the optimiser drives $A_1$ positive and bends the glass more, it has found a different local minimum. Reset to the pre-designed $A_1$ and keep EFFL weight high.
- The NIR case needs a much smaller $A_1$ correction for 20 nm of bandwidth. Compute the band "Abbe numbers" as in Course 02 L06 and Task 2.5. Then ask whether the axial colour of a plain singlet over ±10 nm is already within the depth of focus $\pm2\lambda N^2$.
</details>

## Task 6 — Specification of a DOE dot projector (analysis)
**Goal:** Turn the lesson into a one-page spec, the way you would brief a DOE vendor.

**Given:** A 940 nm VCSEL array (300 emitters, 1.5 W optical, ±2 nm part-to-part, 0.07 nm/K) and a collimator with $f$ = 3 mm, followed by a 3×3 tiling DOE covering 60° × 45° full field. 0–50 °C operation.

**Steps:**
1. Compute the DOE periods in x and y (the tile centres at ±20° and ±15°, i.e. a tile pitch equal to one third of the field) and the worst-case wavelength excursion. How far do the outer tiles move on a wall at 1 m?
2. Choose a cell type (binary Dammann 1×3 crossed, or multilevel). Give expected total efficiency and the zero-order fraction at nominal and at worst-case wavelength (use `doe.py`).
3. List the items for the spec sheet: wavelength range, input divergence, fan-out angles, efficiency, uniformity, zero-order maximum (nominal and worst case), higher-order suppression outside FOV, polarisation, AR coating, environmental conditions. Mark each as "you can compute it in OpticStudio", "you can compute it with scalar FFT" or "needs vendor RCWA/measurement".
4. Write 5 bullet points on eye-safety design: brightest dot, fault case (DOE missing/cracked/condensation), and what the optical designer must hand to the laser-safety assessment under IEC 60825-1.

**Deliverable:** `notes.md` section "DOE spec".

<details><summary>Hints / solution sketch</summary>

- $d_x = \lambda/\sin 20^\circ$ = 0.94/0.3420 = 2.75 µm. $d_y = 0.94/\sin 15^\circ$ = 3.63 µm. That is only ~3–4 λ, **below** the ~5 λ scalar-validity rule of thumb. Your scalar efficiencies are optimistic and a vendor would use rigorous models. This is the realistic punchline.
- Wavelength range: ±2 nm part-to-part plus ±1.75 nm thermal (0.07 nm/K × ±25 K about 25 °C), so ±3.75 nm or ±0.40 %. At 20°, Δx = L sin θ (Δλ/λ)/cos³θ ≈ ±1.6 mm on the wall at 1 m (3.3 mm total span). That matters for a calibrated active-stereo system only if the pattern itself is used as a reference. Otherwise it is mainly a uniformity and zero-order issue.
- 1×3 crossed binary Dammann: 66.4 %² = 44.1 % into 9 tiles. Each tile carries the full emitter pattern at about 4.9 % of the power. A multilevel 3×3 cell can approach 80–90 %.
</details>

## Stretch tasks
- **S1 — Continuous-phase fan-out.** Optimise a phase-only cell sampled with 128 points (L-BFGS on the phase samples, analytic gradient of $|c_m|^2$, penalty on non-uniformity) for 1×3, 1×5, 1×7. Expected: 1×3 ≈ 92.6 % (the known optimum "triplicator"), 1×5 ≈ 92 %, 1×7 ≈ 97 %. Then quantise to 4 and 8 levels and recompute. Compare with $\mathrm{sinc}^2(1/N)$ intuition.
- **S2 — IFTA pseudo-random dot cloud.** Use a Gerchberg–Saxton IFTA on a 256 × 256 cell to make a pseudo-random pattern of ~500 dots. Report efficiency, uniformity and the zero order, and plot the far field as $\sin\theta$ coordinates and as positions on a wall (pincushion).
- **S3 — Rigorous vs scalar.** If you have access to Ansys Lumerical (RCWA) or an open RCWA package, compute $\eta_{0}, \eta_{\pm1}$ for a fused-silica binary grating with 50 % duty at periods 20, 10, 5, 2 and 1.2 µm at 940 nm (TE and TM). Find where scalar theory (0 % / 40.5 %) fails by more than 5 percentage points.
- **S4 — Speckle simulation.** Simulate a speckled spot (random phase screen × pupil, FFT to image) and measure centroid jitter versus aperture. Compare with the Dorsch et al. formula.

## Reflection questions
1. Why do the order **directions** depend only on the period, while the **efficiencies** depend on the shape within the period? Answer in Fourier terms.
2. In a DOE dot projector, what sets the size of each dot at 1 m, the DOE or the source/collimator? What would you change to make dots smaller?
3. Why is a hybrid diffractive achromat attractive for an 850 nm VCSEL receiver but questionable for a broadband visible camera?
4. OpticStudio reports 100 % efficiency for a Binary 2 lens. List two analyses whose results are therefore optimistic, and how you would correct them.
5. The zero order of a fan-out DOE is 1 % in the datasheet. Give three reasons it could be 3–5 % in your product.

<details><summary>Answers</summary>

1. The field behind a periodic element is a comb in angle (period → spacing in sin θ) multiplied by the transform of one cell. The cell's transform only weights the comb teeth, so it sets the efficiencies.
2. The beam: each order is a copy of the incident angular spectrum. Dot size at 1 m ≈ beam divergence × distance (plus the emitter-image size for a VCSEL-array projector, set by emitter size / collimator focal length). Better collimation, longer collimator focal length or smaller emitters give smaller dots, at the price of a larger beam on the DOE.
3. Narrow band: the efficiency loss away from the blaze wavelength and the secondary spectrum are negligible, and the colour correction plus zero Petzval come almost for free. Broadband visible: 10–20 % of the light goes into out-of-focus orders (veiling glare), and secondary spectrum is ~2× worse than a glass doublet.
4. MTF/spot/PSF (no veiling glare from orders 0 and 2) and relative illumination/transmission (no efficiency loss, which also varies with field angle). Correct by scalar efficiency per wavelength (weights) and a stray-light NSC model with the ghost orders split out, or better efficiency data (RCWA/measurement).
5. Etch-depth error (sin²(πε/2)), wavelength offset or temperature drift, non-normal or divergent input, polarisation effects in fine features (scalar theory invalid near λ), side-wall slope/rounding, contamination or condensation in the relief, AR-coating mismatch.
</details>
