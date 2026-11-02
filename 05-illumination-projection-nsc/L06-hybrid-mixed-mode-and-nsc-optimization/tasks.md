# L06 — Tasks: Hybrid (Mixed-Mode) Systems and Non-Sequential Optimization

> Work in `work/` inside this lesson folder (e.g. save `work/L06_T2_cooke_mixed.zmx`). Commit your designs, scripts and a short `work/notes.md` with answers.
> Estimated time: ~6 h

## Task 1 — Noise budget and why DLS fails (Python)
**Goal:** Feel Monte-Carlo noise in a uniformity metric and in its finite-difference derivative before you meet it in OpticStudio.

**Given / specs:** A detector of 20 × 12 pixels. A "design" irradiance on it $E(x) = 1 + a\,x^2$ with $x \in [-1, 1]$ across the long axis, uniform across the short axis; the design variable is $a$ (think: condenser defocus). Rays are drawn from $E$ by rejection sampling.

**Steps:**
1. Write `work/noise.py`: for $N_{\text{det}} \in \{10^4, 10^5, 10^6\}$ and $a = 0$, trace 20 independent "runs" (different seeds) and record the measured CV. Compare the mean with $1/\sqrt{N_{\text{det}}/240}$.
2. For $a = 0.10$ compute the true CV analytically or with $10^8$ samples on the 20-pixel grid; then the measured CV at the three ray counts; check $\text{CV}_{\text{meas}} \approx \sqrt{\text{CV}_0^2 + 1/k}$.
3. Finite-difference derivative: estimate $d\,\text{CV}/da$ at $a = 0.10$ with steps $\delta = 10^{-3}, 10^{-2}, 10^{-1}$, using independent seeds for the two evaluations (as OpticStudio does when the random sequence advances) and then *the same seed* (common random numbers). Tabulate mean and std of the derivative over 20 repeats.
4. Implement a 1-D "DLS-like" step (Newton step using your noisy derivative) and a derivative-free golden-section or simple pattern search on $a \in [-0.3, 0.3]$ at $N_{\text{det}} = 10^5$. Which finds $a \approx 0$ more reliably?

**Deliverable:** `noise.py`, a table and a 5-line conclusion in `notes.md`.

**Check yourself:** at $a = 0$: CV ≈ 15.5 % ($10^4$), 4.9 % ($10^5$), 1.55 % ($10^6$). With independent seeds and $\delta = 10^{-3}$ the derivative is pure noise (std of order $\sqrt2\,\sigma_{\text{CV}}/\delta$, i.e. tens to hundreds), with $\delta = 0.1$ it is usable. Common random numbers dramatically reduce derivative noise — a lesson for your own ZOS-API loops (Course 07).

<details><summary>Hints / solution sketch</summary>

- Sampling: draw $x$ uniform in $[-1,1]$, accept with probability $E(x)/E_{\max}$; draw $y$ uniform. `np.histogram2d(x, y, bins=(20, 12), range=[[-1,1],[-1,1]])`.
- True CV for $a = 0.1$ on 20 bins: compute bin averages of $1 + 0.1x^2$ exactly (integrate over each bin) — the result is ≈ 2.8 %. So at $10^5$ rays (noise 4.9 %) the design signal is *smaller* than the noise; at $10^6$ (1.55 %) it is visible; at $10^7$ clear.
- True derivative $d\,\text{CV}/da$ near $a = 0.1$ is ≈ 0.28 (CV is ≈ linear in $a$ for small $a$). Compare it with your noise.
- Common random numbers: use the same uniform draws for both evaluations; only the acceptance threshold changes, so most rays land in the same pixel and the difference is dominated by the real change.

</details>

## Task 2 — Mixed mode from a sequential lens (OpticStudio)
**Goal:** Use Convert to NSC Group for a partial and a full conversion and verify both.

**Given / specs:** Sample file `Cooke 40 degree field.zmx` (Samples › Sequential › Objectives; location may vary by release — search the samples folder). Keep the wavelengths as given.

**Steps:**
1. Save a copy as `work/L06_T2_cooke_seq.zmx`. Fix all semi-diameters (make them *Fixed*). Note the stop surface. Record: RMS spot radius at the three fields, MTF at 50 lp/mm, and the image-space F/#.
2. **Partial conversion:** File › Convert to NSC Group, converting **only the last element** (its two surfaces). Do *not* tick "convert file to non-sequential mode". Save as `work/L06_T2_cooke_mixed.zmx`.
3. Inspect the new NSC surface in the LDE (parameter columns: port drawing and exit location/tilt) and the objects in the NSC Editor. Open the 3D Viewer (the 2D layout is blank — confirm). Turn on port drawing.
4. Re-run the spot diagram and MTF. They should match step 1 to plotting precision. If not, find out why (stop, aperture, exit port position).
5. Move the exit port 1 mm too far (or change the NSC surface thickness by 1 mm) and observe what changes. Undo.
6. **Full conversion:** from the sequential copy, convert all surfaces with "convert file to non-sequential mode". Save as `work/L06_T2_cooke_nsc.zmx`. Look at the source(s) and detector(s) the converter added.
7. Trace $10^6$ rays (polarization on, split off, then split on). Compare the detector total power with the source power. Then compute by hand the expected uncoated transmission of 6 air–glass faces using the glass indices at the primary wavelength.

**Deliverable:** three `.zmx` files; table in `notes.md`: sequential vs mixed vs NSC (spot, MTF, transmission); one paragraph on what the NSC model tells you that the sequential one cannot.

**Check yourself:** mixed-mode image quality is identical; NSC transmission is ≈ 70–78 % for an uncoated triplet (six faces at ~4.3–5.6 % each; all six at $n = 1.62$ gives 0.71), not 100 %. With splitting on, the total energy accounted for (detector + lost) should still be ≈ source power.

<details><summary>Hints / solution sketch</summary>

- Each face: $R = ((n-1)/(n+1))^2$. For $n = 1.62$ (typical of the Cooke's crown/flint pair), $R \approx 0.056$; for $n = 1.52$, 0.043. Six faces at ~0.05 → $0.95^6 \approx 0.74$; the exact number depends on the glasses — compute it with the actual indices.
- If the full-NSC spot looks very different from the sequential one, check that the detector is at the paraxial image plane and that the source fills the same pupil — the converter's source is an approximation of the field/pupil definition.
- Partial-conversion mismatch is almost always the stop or an aperture: the stop must be sequential and before the NSC group.

</details>

## Task 3 — Verify the NSDD codes yourself (OpticStudio + Python)
**Goal:** Never trust an operand code you have not checked: reproduce NSDD statistics from exported detector data.

**Given / specs:** Pure NSC file. Source Rectangle 10 × 10 mm, 1 W, 850 nm, collimated (cosine exponent large or a small angular range), $10^6$ analysis rays, Sobol sampling if available. Detector Rectangle 20 × 20 mm, 20 × 20 pixels, 50 mm away. Insert a Standard Lens (N-BK7, R1 = 100 mm, flat back, 4 mm thick) halfway to get a non-trivial distribution.

**Steps:**
1. MFE: `NSDD 1 0` (clear), `NSTR`, then NSDD on the detector with Pix# 0, −4, −6, −7, −9 and, after looking them up in the Help, the peak and minimum codes. Data = 0 and Data = 1. Then #Ignored = 0 and 2.
2. Run the same trace from Ray Trace Control and export the Detector Viewer data as text (Text tab › save). Load it in Python (`work/nsdd_check.py`) and compute sum, std (population and sample), std over non-zero pixels only, centroid, RMS width.
3. Match each NSDD value to your Python number. Establish: does −4 include zero pixels? Population or sample std? Does #Ignored apply to Pix# 0?
4. Turn Pixel Interpolation on and repeat: which numbers change?

**Deliverable:** `nsdd_check.py`; a table "NSDD code → definition (verified)" in `notes.md`. Keep it — you will reuse it in L07–L09 and Course 07.

**Check yourself:** Pix# 0, Data 0 ≈ detector total power (≈ 0.9 W after two Fresnel faces); your Python numbers agree with NSDD to the number of decimals shown (both come from the same trace, so there is no noise between them).

<details><summary>Hints / solution sketch</summary>

- Run the MFE evaluation and the Ray Trace Control trace with the same ray count; with Sobol sampling both traces are identical; with random sampling, export after the MF evaluation (the MF trace leaves data in the detectors — verify by opening the Detector Viewer after updating the MFE without retracing).
- Two uncoated faces at $n = 1.5098$: $T = (1-0.0413)^2 = 0.919$.
- If your sample/population or zero-pixel test is ambiguous, make the lit area half the detector: then "all pixels" and "non-zero pixels" statistics differ strongly.

</details>

## Task 4 — Optimize a fly's-eye homogenizer for uniformity (OpticStudio)
**Goal:** Run a real NSC optimization with a uniformity + efficiency merit function; compare DLS and OD and the effect of ray count and pixel interpolation.

**Given / specs:** Start from `../L04-illumination-optics-collimators-condensers/work/L04_T3_flyseye.zmx`. Change the wavelength to 0.85 µm. Lenslet focal length 6 mm (N-BK7: $R = 3.059$ mm at 850 nm), both arrays 1.5 mm thick, curved faces outward, condenser $F \approx 25.9$ mm, detector 6.912 × 3.888 mm with **20 × 12 pixels** at the DMD plane (the DMD active area). Optional: check overfill afterwards in a copy with a larger detector.
**Starting point:** deliberately detune: gap $g = 3.0$ mm (paraxial optimum 4.013 mm), condenser 3 mm too far.

**Steps:**
1. Turn on Pixel Interpolation on the DMD detector. Set source rays to $10^5$.
2. MFE: clear, NSTR (polarization on, split off for speed), CV block from the lecture (§4.2: NSDD −4 / (NSDD 0 / M)), flux ≥ 0.9 × starting flux on the DMD detector, NPZG/NPZL to keep the condenser 20–35 mm from array 2.
3. Variables: gap, condenser Z, lenslet radius (array 2 picks up array 1).
4. Run **DLS** for 5 cycles; record MF, CV and time. Reload the start file and run **Orthogonal Descent** for the same wall-clock time.
5. Repeat step 4 with $10^6$ rays, and with Pixel Interpolation off.
6. Verify each final design at $10^7$ rays (same for all): CV, min/max, efficiency. Save the best as `work/L06_T4_flyseye_opt.zmx`.

**Deliverable:** a 2 × 2 × 2 results table (optimizer × ray count × interpolation) with verified CV, min/max, efficiency, time; final design file; detector images before/after.

**Check yourself:** OD should reach a gap within a few tenths of a mm of 4.0 mm and CV of a few % (the fly's-eye diffraction-free geometric limit is good; residual non-uniformity comes from lenslet aberrations and edge roll-off). DLS at $10^5$ rays without interpolation often stalls near the start. Remember §5.1: compare only the $10^7$-ray verified numbers.

<details><summary>Hints / solution sketch</summary>

- Gap formula: $g = f_{LA} - 2t/n = 6 - 3/1.5098 = 4.013$ mm.
- If the optimizer changes the lenslet radius a lot, it is trading the field-lens function of array 2 against the edge sharpness — check that the illuminated rectangle still matches the DMD (overfill ~5 %).
- Typical runtime: a $10^6$-ray trace of this system takes about a second or two on a modern workstation; OD needs tens to a few hundred evaluations — a few minutes.

</details>

## Task 5 — Collimator against the étendue limit (OpticStudio)
**Goal:** Optimize a parametric hybrid collimator for minimum divergence with a flux constraint, and judge the result against étendue.

**Given / specs:** Start from `../L04-illumination-optics-collimators-condensers/work/L04_T5_reflector.zmx` (LED 1 × 1 mm Lambertian, conic reflector, Ø 20 mm exit). Add a central **Even Asphere Lens** (N-BK7, Ø 8 mm) that collimates the forward cone the reflector does not catch. Far-field angular detector (Detector Rectangle with angular data, or Detector Polar) of ±20°.
**Steps:**
1. Use the NSC Optimization Wizard: criterion RMS Angular Radius = 0 + minimum flux = 70 % of source power. Read every operand the wizard wrote and annotate it in `notes.md`.
2. Variables: reflector radius and conic, lens radii, conic and 4th/6th-order terms, lens Z. Constrain positions with NPZG/NPZL.
3. Optional noise-free pre-step: use NSRA on 3–5 representative rays from the LED edge to target zero exit angle, optimize, then switch to the detector-based MF.
4. Optimize with OD at $10^5$ rays, then $10^6$. Verify at $10^7$: RMS angular radius, FWHM, fraction of flux within ±5°.
5. Compare with the étendue limit $\theta_{\min} = \arcsin\sqrt{A_{\text{LED}}/(\pi r_{\text{exit}}^2)}$.

**Deliverable:** `work/L06_T5_collimator_opt.zmx`, wizard annotation, a paragraph comparing the result with 3.23°.

**Check yourself:** $\theta_{\min} = \arcsin\sqrt{1/(\pi\cdot 100)} = 3.23°$. A good hybrid gets an RMS angular radius within a factor of ~1.5–3 of this; a result *below* the limit means the metric or detector is wrong (e.g. the detector ignores rays outside its angular range).

<details><summary>Hints / solution sketch</summary>

- The étendue limit uses the full ±90° Lambertian emission; if you count only 70 % of the flux, the limit for that fraction is somewhat smaller — the comparison is a ballpark.
- If the optimizer shortens the reflector to raise "collimation", the flux floor is not active — check the OPGT line.

</details>

## Stretch task — Mixed-mode DLP TIR prism
Insert a two-prism DLP TIR prism (two Polygon/Rectangular-volume-type objects or CAD; 0.5–1 mm air gap at the TIR face) in an NSC group between the DMD plane and the first element of your projection lens `../L05-projection-lens-design/work/L05_T5_projlens.zmx`, in **mixed mode**. Re-optimize the sequential lens with the prism in place (the prism is a thick glass block in the convergent beam: spherical aberration and astigmatism appear). Then build the same prism in a pure NSC copy with an LED source tilted at the DMD illumination angle and check whether any illumination light leaks into the projection path (preview of L07).

## Reflection questions
1. Why can't the spot diagram of a mixed-mode file reveal a ghost created inside the NSC group?
2. You halve the detector pixel size at fixed ray count. What happens to the measured CV of a truly uniform field, and why might the optimizer "prefer" a different design?
3. Why is total detector flux almost noise-free while min/max uniformity is the noisiest number in the model?
4. When is DLS acceptable for an NSC problem?
5. Your optimized collimator reports a divergence 20 % below the étendue limit. List three possible causes.

<details><summary>Answers</summary>

1. Sequential rays entering a port follow a single path and do not split; ghost energy exists only for NSC source rays with splitting on, recorded on detectors.
2. $k$ per pixel halves along each axis → 4× fewer rays per pixel → noise 2× larger, CV inflates; since noise adds in quadrature, designs that put more light on the detector (higher $k$) look "more uniform", biasing the optimizer toward efficiency rather than true uniformity. Compare designs at fixed, high ray count.
3. Total flux averages all $N\eta$ rays (relative error $\sqrt{(1-\eta)/(\eta N)}$); min and max are extreme order statistics of ~240 noisy pixels, and noise always pushes max up and min down.
4. When the MF is smooth on the scale of the finite-difference step: many rays (or common random numbers/Sobol), pixel interpolation, aggregated operands, few variables — or when the operands are deterministic (NSRA-based).
5. The angular detector clips rays outside its range (they are not counted); the flux floor is inactive so most light is discarded; wrong source size (emitter smaller than 1 × 1 mm, or a point source); the metric is FWHM/RMS of a peaked distribution while the étendue limit is an edge angle — definitions differ.

</details>
