# L09 — Tasks: Capstone — structured-light projector

> Work in `work/` inside this lesson folder. Keep everything under git, one commit per milestone, with the commit message stating the milestone and the headline number (e.g. `M2: DMD CV 2.4 % ± 0.3 %, spill 6 %`). **Commit your paper predictions (Task 1) before you trace anything** — the grading checks the history.
> Estimated time: ~18–22 h (three weekly sessions: M0–M2, M3–M5, M6–M7).

The specification is §2 of the [lecture notes](lecture-notes.md) (P1–P18). Default path: **Track A source (850 nm LED)**, and you choose **architecture A** (collimator + fly's-eye) or **B** (tapered rod + relay) in Task 1. The VCSEL track and the visible track are stretch tasks.

**Files from earlier lessons you will reuse** (paths relative to this lesson folder):

| File | From | Used in |
|---|---|---|
| `../L01-radiometry-photometry-etendue/work/radiometry.py` | L01 Task 1 (extended in L03 Task 1) | Task 1 |
| `../L03-source-modeling-leds-and-lasers/work/L03_T2_led_bare.zmx`, `L03_T2_led_dome.zmx`, `L03_T5_vcsel.zmx` | L03 | Tasks 2, Stretch 1 |
| `../L04-illumination-optics-collimators-condensers/work/L04_T3_flyseye.zmx`, `L04_T5_reflector.zmx`, your L04 Task 4 taper model | L04 | Tasks 2–3 |
| `../L05-projection-lens-design/work/projector.py`, `dof.py`, `L05_T5_projlens.zmx` | L05 | Tasks 1, 6 |
| `../L06-hybrid-mixed-mode-and-nsc-optimization/work/L06_T4_flyseye_opt.zmx`, `L06_T5_collimator_opt.zmx`, `noise.py` | L06 | Tasks 2–3 |
| `../L07-stray-light-scattering-ghosts/work/straylight.py`, `L07_T3_proj_nsc_C.zmx` (and `_B`), `L07_T4_barrel_M1.zmx` … | L07 | Tasks 5, 7 |
| `../L08-diffractive-optics-and-pattern-projection/work/doe.py`, `L08_T4_dots_nsc.zmx` | L08 | Stretch 2 |
| `../../04-machine-vision-camera-lenses/L10-capstone-machine-vision-lens/work/capstone.zmx` | Course 04 | Task 6 (optional), reflection |

If a file is missing because you skipped a task, the hint in each milestone says what minimal substitute is acceptable. Note the substitution as a deviation.

Common NSC settings unless stated: lens units mm; wavelengths 0.82/0.835/0.85/0.865/0.88 µm with weights 0.0625/0.5/1/0.5/0.0625 (L03); *Use Polarization* on; *Split NSC Rays* **off** for flux/uniformity runs and **on** for ghost runs; detectors `ABSORB` unless stated as transparent (material blank).

---

## Task 1 — M0: specification, predictions and budget (Python, pen & paper)
**Goal:** Own the spec and predict every graded metric before tracing.
**Given / specs:** Lecture §2–§3 and the worked example.
**Steps:**
1. Copy the spec into `work/spec.md`. For each line P1–P18 add: origin, derivation (formula + numbers), verification method (which model, which detector/operand), and the noise you will need to resolve the margin.
2. Write `work/budget.py` that imports `radiometry.py` (L01) and the functions of `projector.py`/`dof.py` (L05) and `straylight.py` (L07) — copy them if importing across folders is awkward — and prints:
   a. the étendue table (LED, VCSEL, DMD at F/1.71, lens at F/2.0 and F/2.4);
   b. the shape-loss figure $G_{\text{round}}$ for architecture A and the cone at the DMD for architecture B;
   c. the flux budget for both architectures (links as in the worked example, as a list you will later overwrite with measured values) and the scene irradiance at 0.5/1.0/1.5 m;
   d. the defocus/modulation table for 8/16/32-px fringes at 0.5/0.75/1.0/1.5 m for F/2.0 full fill and for your architecture's $\sigma$;
   e. the tilt-geometry margins (P15) for your chosen cone and F/#;
   f. the ghost sum $s = \binom{N}{2}R^2$, checkerboard contrast and modulation factor for $R$ = 1 % and 0.25 % with your lens's actual number of air–glass faces $N$.
3. Choose architecture A or B with a short written argument (efficiency, uniformity robustness, size, cost, how much you can reuse). Either is acceptable; the argument is graded.
4. Commit: `M0: predictions`.

**Deliverable:** `work/spec.md`, `work/budget.py`, its printed output in `work/notes.md`, the architecture decision.
**Check yourself:** étendues 3.14 / 0.045 / 7.22 / 5.28 / 3.66 mm² sr; $G_{\text{round}}$ = 2.47 mm² sr (79 % of the LED); rod cone 12.25°, $\sigma$ = 0.85; budgets 0.335 (A) and 0.475 (B) with the planning links; irradiance at 1.5 m 0.455 / 0.646 W/m²; modulation at the range ends (F/2.0, full fill) 0.69 / 0.91 / 0.98; tilt margin 5.0° at F/2.0 with a 14.48° cone; ghost sums 9.1 × 10⁻³ and 5.7 × 10⁻⁴ for $N$ = 14.

<details><summary>Hints</summary>

- Image area at distance $L$ (from the lens): $(W m)(H m)$ with $m = (L-f)/f$; $f$ = 8.23 mm. Use your *actual* L05 focal length if it differs, and propagate.
- Balanced focus: $x'(L) = f^2/(L-f)$; $x'_f$ = mean of the end values; $\delta$ = half their difference (46.2 µm).
- Partial fill blur: $b = 2\delta\sin\theta_c$; full fill: $b = \delta/N$ (identical when $\sin\theta_c = 1/(2N)$).
- $G_{\text{round}} = \pi(\pi R^2)\sin^2\alpha_y$ with $R = F\tan\theta_{\text{lens}}$, $\tan\alpha_y = H/(2F)$ — show algebraically that $F$ drops out.

</details>

---

## Task 2 — M1: source and collector (OpticStudio NSC)
**Goal:** Measure the first link of the budget — how much LED flux enters the homogenizer's acceptance — and see the étendue-shape loss.

**Architecture A — collimator into a fly's-eye.**
**Given / specs:** Start from `../L06-hybrid-mixed-mode-and-nsc-optimization/work/L06_T5_collimator_opt.zmx` (substitute: `../L04-illumination-optics-collimators-condensers/work/L04_T5_reflector.zmx`). Keep its Ø 20 mm exit. To accept a Ø 20 mm beam while still giving a 14.48° cone at the DMD, the fly's-eye must be rescaled: condenser $F = 10/\tan14.48° = 38.73$ mm, lenslets 1.6 × 0.9 mm with $f_{LA} = F\cdot1.6/6.912 = 8.965$ mm, acceptance ±2.87° (short axis) × ±5.10° (long axis).
**Steps:**
1. Save as `work/L09_M1_collector.zmx`. Source: 1 × 1 mm, cosine exponent 1, 1.2 W, five wavelengths as above (or the domed LED of `L03_T2_led_dome.zmx` if you want to see what the dome does to étendue — record which).
2. Put a transparent Detector Rectangle (Ø 20 mm equivalent: 20 × 20 mm, 100 × 100 px) at the planned array position and use its angle-space display (or a Detector Polar behind a Ø 20 mm aperture) to measure the power inside the rectangular acceptance ±2.87° × ±5.10° — export the angular data and integrate in Python if the viewer cannot do a rectangular window.
3. Compute the capture fraction = (power inside acceptance and inside Ø 20 mm)/(source power). Compare with the étendue-shape limit 0.79 × your collimator's own efficiency from L06.

**Architecture B — tapered rod.**
**Given / specs:** Your L04 Task 4 model: LED butt-coupled (0.05 mm gap) to an N-BK7 rod, input 1.1 × 1.1 mm, output 3.0 × 1.6875 mm. Length: the L04 result that approached the ideal output angle (≥ 40 mm; try 50 mm).
**Steps:**
1. Save as `work/L09_M1_rod.zmx`. Detector at the exit face (3.0 × 1.6875 mm, 60 × 34 px) with angle-space display.
2. Measure: power at the exit face / source power; irradiance CV over 20 × 12 px; fraction of power inside $\sin\theta \le 0.489$ (29.3°) in air.
3. Add AR on the end faces (`I.995`) and repeat. Which loss dominates — Fresnel, side-wall escape, or the gap?

**Deliverable:** file(s), measured capture/transmission with noise estimate, updated first rows of the budget.
**Check yourself:**
- A: a realistic collimator gives a capture fraction around 0.55–0.7 into the acceptance window; it cannot exceed ~0.79 even if perfect. If you get more, check that you are measuring the *rectangular* acceptance and the beam *inside* Ø 20 mm.
- B: exit-face power 0.85–0.93 of the source with AR ends; the CV at the exit face should already be a few % for a ≥ 40 mm rod (L04); the angular distribution is nearly flat-topped up to ~29° with a soft tail.

<details><summary>Hints</summary>

- Rescaled lenslets in N-BK7 at 850 nm: $R = f_{LA}(n-1) = 8.965\times0.5098 = 4.57$ mm; with 1.5 mm thick arrays the starting gap is $g = f_{LA} - 2t/n = 6.98$ mm (L06 worked example (a)). About 218 channels fit inside Ø 20 mm — plenty.
- The shape-loss limit is the same (0.79) as with the Ø 13.4 mm array and $F$ = 25.92 mm in the lecture: $F$ drops out. You just verified the lecture's invariant numerically.

</details>

---

## Task 3 — M2: illumination at the DMD (OpticStudio NSC + optimization)
**Goal:** Deliver P7 and P8: a uniform, telecentric, ≤ 14.5° illumination of the DMD active area with little spill.
**Given / specs:** Your M1 file + homogenizer + condenser/relay. Unfolded geometry: illumination axis along +Z, DMD plane perpendicular to it, centred on the illumination axis. Ignore the TIR prism here (scalar 0.92 later). Detectors at the DMD plane:
- D1: 6.912 × 3.888 mm, 20 × 12 px, transparent (CV);
- D2: 0.01 mm behind D1, 8.29 × 4.67 mm (1.2×), 240 × 135 px, `ABSORB` (spill and pictures);
- angular check: D2's angle-space display, or a Detector Polar 1 mm behind a 6.912 × 3.888 mm opening, half-angle range 30°.

**Steps:**
1. Build the chain. A: two Lenslet Array objects (L04 Task 3 / L06 Task 4 style) + condenser at $F$ = 38.73 mm from array 2 (a Paraxial-like thin lens first if your release has one, then a real N-BK7 or N-LAK9 singlet/doublet); B: relay of magnification 2.304 from the rod exit face to the DMD, image-side telecentric (aperture stop at the relay's front focal point).
2. Trace 10⁶ rays; record power on D1, D2, CV(D1), min/max(D1), spill = 1 − P(D1)/P(D2), cone half-angle containing 95 % of the power in x and y, and the mean ray angle (chief-ray proxy) at the four corners of the active area (restrict with small detectors or export the angle data per region).
3. Optimize (L06): variables = array gap (A) or relay spacing/focus (B), condenser/relay position; MF = CV(D1) (via `NSDD` pixel code −4 divided by mean, as in L06) + `NSDD` power on D1 ≥ 0.9 × starting value. Use orthogonal descent or Hammer with 10⁵–10⁶ rays per evaluation; *never* DLS on a noisy merit (L06 §5).
4. Verify at 10⁷ rays. Save `work/L09_M2_illum.zmx`.
5. Fit a source description for later tasks: a cosine exponent $n$ whose angular profile matches your measured DMD-plane distribution best (L03), and the value of $\sigma = \sin\theta_{95}/\sin14.48°$.

**Deliverable:** `work/L09_M2_illum.zmx`, D1/D2 pictures, angular plot, a P7/P8 table with noise, fitted $n$ and $\sigma$.
**Check yourself:**
- Noise floor of CV on 240 px: ≈ $\sqrt{240/N_{\text{det}}}$ = 1.5 % at 10⁶ rays, 0.5 % at 10⁷ (L06). A measured CV of 2–3 % at 10⁷ rays is real.
- Fly's-eye: flat-top with sharp edges, spill 3–10 % (edge blur from lenslet aberrations), cone ≈ rectangle ±arctan(10/38.73) clipped to the circle of the beam: ≤ 14.5°. Rod + relay: cone ≈ 12–13°, edges softer, uniformity depends on rod length.
- Corner chief-ray angles ≲ 1–2° if the condenser/relay is telecentric; if they are 5°+, the array/stop is not at the condenser's front focal plane.

<details><summary>Hints</summary>

- Spill is the cheapest efficiency to buy back: lenslet aberrations (A) or relay distortion/defocus (B) blur the edge. Aspherize the condenser or bend it before adding elements.
- A real DMD's illumination is oblique (34°) and keystoned (L04 §7); you are modelling the unfolded, ideal-telecentric equivalent. Note this as a model limitation, and budget ~5 % extra overfill for the real build.

</details>

---

## Task 4 — M3: tilt geometry and DMD reality check (pen & paper, optional NSC sketch)
**Goal:** Close P15 and turn the DMD's hidden physics into explicit risks.
**Steps:**
1. Draw (ASCII is fine) the on, off and flat-state directions for illumination at +34°, with your measured illumination cone $\theta_c$ and the lens acceptance 14.48°. Compute the margins: illumination ↔ on-state cone, on-state ↔ flat-state, lens acceptance ↔ flat-state cone, lens acceptance ↔ off-state cone.
2. Repeat for F/1.71 with $\theta_c$ = 17°. What fails?
3. DMD as a grating: at 850 nm and 5.4 µm pitch, list the diffraction-order directions (relative to the on-state direction, assume the blaze centres the envelope on it) that fall within ±14.48° along one axis. Repeat at 550 nm. One paragraph: why is $\eta_{\text{DMD}}$ wavelength-dependent, and what will you ask the vendor?
4. *(Optional NSC sketch, `work/L09_M3_fold.zmx`)*: place a flat Rectangle `MIRROR` tilted 17° at the DMD, illumination arriving at 34° to the array normal, and a Detector Polar where the lens would be. Confirm the on-state bundle leaves along the normal. Then set the tilt to 0° (flat state) and see where the light goes. State clearly why this model cannot be used for imaging (a single tilted plane is out of focus by about $\pm\tfrac{W}{2}\sin17°$ ≈ ±1.0 mm across the array — ~20× the depth of focus).

**Deliverable:** angle diagram, margin table, order list, vendor question list in `notes.md`.
**Check yourself:** F/2.0, $\theta_c$ = 14.48°: lens ↔ flat-state margin 5.0°; F/2.0 with a 17° cone: 2.5°; F/1.71 with 17°: 0.0°. Order spacing $\arcsin(\lambda/p)$ = 9.06° at 850 nm, 5.85° at 550 nm: within ±14.48° along one axis you get orders 0, ±1 at 850 nm (3 orders) and 0, ±1, ±2 at 550 nm (5 orders).

<details><summary>Discussion</summary>

With few orders inside the pupil, a small mismatch between the tilt-defined blaze direction and the order grid moves a large fraction of the light into orders the lens does not collect. Visible DMDs are characterized for visible light; at 850 nm ask the vendor for: diffraction efficiency into your F/# vs wavelength, window AR band and reflectance at 850 nm, mirror reflectance at 850 nm, and whether an NIR-optimized device exists for your array size.

</details>

---

## Task 5 — M4: unfolded end-to-end system (OpticStudio NSC)
**Goal:** Measure P9, P10, P11 and turn the planning budget into a measured one.
**Given / specs:** Combine `work/L09_M2_illum.zmx` with `../L07-stray-light-scattering-ghosts/work/L07_T3_proj_nsc_C.zmx` (lens converted to NSC, `I.9975`, prism block and window plates included). Substitute: if you have no L07 file, convert `L05_T5_projlens.zmx` yourself (L06 Task 2).
**Steps:**
1. Save as `work/L09_M4_system.zmx`. Delete L07's half-field source and the DMD mirror. Create Null Objects "LENS ORIGIN", "DMD CENTRE" (at the DMD plane, offset by $s$ = 1.944 mm from the lens axis as in your L05 file) and reference the whole illumination chain to "DMD CENTRE", placed *behind* the DMD plane (unfolded).
2. DMD aperture: four `ABSORB` Rectangles forming a frame around the 6.912 × 3.888 mm active area (outer size ≥ the spill footprint). Keep D1 (transparent) for bookkeeping.
3. Scene detectors at 500, 750, 1000, 1500 mm from the lens front vertex (same convention as your L05 configurations), each sized to the projected image + 10 % (centre them where the image actually lands — 100 % offset puts it on one side of the axis), 160 × 90 px. Make the first three transparent and the last `ABSORB`, or trace each in a separate configuration.
4. Trace 10⁷ rays (splitting off, polarization on). Record the power on: source, collector exit (transparent detector), D1, each scene detector *inside the image area*.
5. Build the measured budget: each link = ratio of consecutive powers; multiply in the two scalars $\tau_{\text{prism}}$ = 0.92 and $\eta_{\text{DMD}}$ = 0.65 (or your vendor value). Compare with Task 1 link by link; explain every discrepancy > 5 %.
6. Uniformity at 1.0 m: rebin the central 90 % × 90 % of the image to 16 × 9 cells; compute min/max and CV. Compare with the product (DMD irradiance map) × (lens Relative Illumination from the sequential L05 file). Where does the falloff come from?
7. Irradiance in W/m² at 0.5, 1.0, 1.5 m (detector power ÷ image area, then multiply by the two scalars).

**Deliverable:** `work/L09_M4_system.zmx`, scene maps (four distances), measured budget table next to the predicted one, P9–P11 results with noise.
**Check yourself:**
- Lens transmission measured with polarization on should be near $0.9975^{14}$ ≈ 0.966 (a little lower for oblique fields).
- Scene power should be (within noise) independent of distance — only the area changes. If the 0.5 m and 1.5 m powers differ by more than a few %, a detector is too small or misplaced.
- Uniformity at 1.0 m is usually limited by the lens's relative illumination at the image corners (32° field): expect min/max ≈ 0.6–0.8 for a telecentric retrofocus lens; the DMD CV contributes only a few %.
- End-to-end source → scene ≈ 0.3–0.35 (A) or 0.4–0.48 (B) with the planning scalars.

<details><summary>Hints</summary>

- Filter strings (L02, L07) give link powers without extra detectors: e.g. replay the ZRD with `H<D1>` for rays that reached the DMD plane, and `H<D1> & H<scene>` for rays that made it all the way. Check the operator syntax in the Help (*The Filter String*).
- If ray counts get slow, trace the illumination once, save rays at the DMD plane to a ZRD, and check in the Help whether your release can convert it into a Source File for the projection-only model — that is the professional "relay the rays" workflow. If not, use the fitted cosine-exponent Source Rectangle from Task 3 step 5 and note the approximation.

</details>

---

## Task 6 — M5: fringe modulation versus depth (sequential + NSC + Python)
**Goal:** Measure P12 two ways and see the effect of the real pupil fill.

**Part A — sequential (σ = 1 worst case).**
1. Copy `../L05-projection-lens-design/work/L05_T5_projlens.zmx` to `work/L09_M5_projlens_mc.zmx`. Ensure configurations at 500, 750, 1000, 1500 mm (add 1000 mm if missing).
2. For each configuration: FFT MTF at the field corresponding to the DMD centre ($y$ = 1.944 mm in DMD coordinates, i.e. 0.374 of $r_{\max}$) and at 0.7 $r_{\max}$; read the **sagittal** MTF at 5.79, 11.57, 23.15 c/mm (vertical fringes vary along $x$, perpendicular to the $y$-field meridian). Optionally add `MTFS` operands to the MFE dashboard for all four configs.
3. Table: MTF vs distance × frequency × field. Compare with the Task 1 defocus prediction × the 750 mm nominal MTF.

**Part B — NSC with the real pupil fill.**
1. New file `work/L09_M5_fringes.zmx` from `L09_M4_system.zmx` minus the illumination. Replace it by **bright bars**: 10 Source Rectangles at the DMD plane, each half width = half a bar (16-px period → bar 8 px = 43.2 µm wide, pitch 86.4 µm; height 0.2 mm), centred on the DMD centre; cosine exponent = the value fitted in Task 3 step 5; total 1 W. (Alternative: one source behind a **Slide** object with a bitmap of the fringes — check in the Help how the Slide maps bitmap colour to transmission at an NIR wavelength before trusting it. A ZOS-API script that writes the rows is a fine Course 07 preview.)
2. Strip detectors at 500, 750, 1000, 1500 mm, centred on the bars' image, width = 10 periods × magnification (51.6, 77.9, 104.1, 156.6 mm), height 0.2 mm × magnification, 400 × 4 px.
3. Trace ≥ 2 × 10⁶ rays *on each detector* (estimate the launch count from the lens transmission and stop clipping you observe).
4. `work/modulation.py`: load each detector's text export, average the 4 rows, keep the central 6 periods, least-squares fit $a_0 + a_1\cos(2\pi x/\Lambda) + b_1\sin(2\pi x/\Lambda)$ with the known period $\Lambda$, and report $M_1 = \sqrt{a_1^2+b_1^2}/a_0$. For a 50 % duty binary input the fundamental's modulation is $4/\pi$ times the system MTF, so **MTF = $M_1/(4/\pi)$**. Estimate the fit noise by splitting the data in halves.
5. Repeat for 8-px and 32-px periods (bars 21.6 µm and 86.4 µm wide).
6. **Defocused PSF picture:** one Source Rectangle the size of one DMD pixel (5.4 × 5.4 µm), same exponent; detector at 500 mm, 40 × 40 px over ~8 projected pixels. For architecture A you should see the structure of the pupil fill (a grid of lenslet images, cropped by the stop); for B a smoother blob. Explain what this does to the MTF curve.

**Deliverable:** both tables, `work/modulation.py`, PSF pictures, P12 verdict, and a recommendation for the pattern sequence (which periods over which depth range; whether binary codes finer than 16 px are usable at 0.5 and 1.5 m).
**Check yourself:**
- Part A at the range ends: 16-px ≈ 0.91 × (nominal MTF at 11.6 c/mm), 32-px ≈ 0.98 × nominal. At 750 mm the defocus factor is 1 and the lens alone sets the number.
- Part B with σ < 1 should come out *above* Part A at the range ends (smaller blur) — e.g. 8-px ≈ 0.77 vs 0.69 (defocus factor only) for σ = 0.85 — and about equal at 750 mm. If B is *below* A at 750 mm, your bars are too few, the fit window includes edge periods, or the ray count is too low.
- Geometric NSC cannot show diffraction: at 8 px (23 c/mm) the F/2.0 diffraction limit at 850 nm is $1 - $ a few %, so this is a small effect — but say so.

<details><summary>Hints</summary>

- Diffraction cutoff at F/2.0, 850 nm: $1/(\lambda N)$ = 588 c/mm; 23 c/mm is 4 % of it, so the diffraction MTF is ≈ 0.95 there — smaller than the defocus effect at the range ends but not negligible when you compare A and B at best focus.
- Link to depth noise: at 1.0 m a 16-px period is 10.4 mm on the scene and $p_z$ ≈ 69 mm (lecture (e)); phase noise scales with 1/modulation, so compare $p_z/M$ across periods to find which period gives the lowest depth noise at each distance.

</details>

---

## Task 7 — M6: stray light, ghosts and spill (OpticStudio NSC + Python)
**Goal:** Close P14 and find where the light you lost actually goes.
**Given / specs:** `../L07-stray-light-scattering-ghosts/work/L07_T3_proj_nsc_C.zmx` (folded ghost model: half-field source at the DMD + `MIRROR` DMD with `I.35`), and, if you did L07 Task 4, your best barrel variant (`L07_T4_barrel_*.zmx`).
**Steps:**
1. Save as `work/L09_M6_ghost.zmx`. Replace L07's cosine exponent 20 by the exponent fitted in Task 3 (your real illumination cone). Keep 1 W in the bright half.
2. Ray Trace Control: polarization on, splitting on, Minimum Relative Ray Intensity 10⁻⁹; save a ZRD; ≥ 10⁶ launched rays.
3. Measure on the 750 mm (and 1500 mm) detector: signal (`!G0` → straight path; check your release's filter syntax), ghosts (`X_GHOST(0,2)` …), ghosts involving the DMD; ghost/signal ratio; half-field contrast (bright-half mean / dark-half mean, excluding 10 % of the width each side of the boundary).
4. Path Analysis: top-5 paths with % of detected power; identify the faces. Compare with L07 Task 3 — did the real illumination cone change the ranking?
5. Find the **peak** ghost irradiance relative to the local signal (a focused ghost matters more than a diffuse one); with `straylight.py` convert it to a phase error and a depth error at 1 m ($p_z$ = 69 mm for 16-px fringes).
6. Spill and clipped light: in `L09_M4_system.zmx` replay with filters for rays that hit the DMD frame and for rays absorbed at the lens stop/barrel. Report each as % of the source. In the real projector, where would each go (flat-state at −34°? barrel walls?)? If you have the L07 barrel model, estimate the scattered fraction that reaches the scene with the M2 numbers.
7. Propose and, if time allows, test one fix (coating on a specific face, a stop/baffle, a curvature change against a focused ghost).

**Deliverable:** `work/L09_M6_ghost.zmx`, P14 table, top-5 paths, depth-error estimate, spill/clip destinations, one fix with before/after.
**Check yourself:** with `I.9975` on all lens faces, ghost/signal typically 10⁻⁴–10⁻³ and half-field contrast in the hundreds to thousands; DMD–lens double bounces (scaling with $R$, not $R^2$) usually top the list. A focused ghost with peak relative amplitude 10⁻³ gives $\delta z = \arcsin(10^{-3})/(2\pi)\times69.3$ mm ≈ 11 µm — right at the P14 limit; diffuse ghosts are far below.

<details><summary>Hints</summary>

- The folded ghost model still has a flat DMD mirror; real on-state mirrors are tilted, so part of the DMD-reflected ghost light goes elsewhere. Your result is a conservative (pessimistic) estimate — say so in the report.
- If half-field contrast is unexpectedly low, check that the dark half is not lit by direct source rays leaking around a mis-sized source or by the source's own back-emission.

</details>

---

## Task 8 — M7: report, review and hand-off
**Steps:**
1. Write `work/projector_report.md` following lecture §7. Every number must be traceable to a file, a ray count and a script.
2. Fill the compliance table P1–P18: value, margin, noise, PASS/FAIL/DEVIATION. Each FAIL or DEVIATION gets a proposal (what to change, what it costs, what you expect).
3. Review: give the report to a colleague (an optical or a 3D-vision engineer is ideal), or review it yourself after three days with the grading checklist below. Record findings and responses in `work/review.md`.
4. Hand-off: save the final system models as `work/projector_system.zmx` (unfolded, M4 state), `work/projector_ghost.zmx` (M6), `work/projector_lens_mc.zmx` (M5 sequential). Put dashboard operands (power on D1, CV, scene power, MTFs) at the top of each MFE with comments. Write `work/HANDOFF.md`: files, configurations, object naming (origins, detectors), scalars applied in post-processing, known model limitations.
5. Commit: `M7: report v1.0`.

**Deliverable:** report, review, three final files, `HANDOFF.md`.

---

## Grading checklist (100 points; pass ≥ 70 with no block at zero)

| Block | Points | Full marks when… |
|---|---|---|
| **Spec & predictions** | 15 | `spec.md` has origin/derivation/verification for all 18 lines (5); predictions committed before the first trace (git) (5); étendue value *and* shape analysed for the chosen architecture (5) |
| **Illumination (M1–M2)** | 15 | P7/P8 measured at ≥ 10⁷ rays with noise (6); telecentricity and σ reported (4); architecture choice argued with numbers (5) |
| **System (M4)** | 15 | scene maps at four distances, P9–P11 with noise (6); measured vs predicted budget link by link, every > 5 % discrepancy explained (9) |
| **Patterns (M5)** | 15 | sequential table (5); NSC fringe fit with noise and the 4/π correction (6); defocused-PSF picture interpreted and a pattern-sequence recommendation (4) |
| **Stray light (M3, M6)** | 15 | ghost/signal, half-field contrast and top paths (6); depth-error estimate from the peak ghost (4); tilt margins and DMD-diffraction risk documented (5) |
| **Report** | 15 | compliance table complete and honest (6); each model's blind spots stated (4); reproducible: files, ray counts, seeds, scripts (5) |
| **Engineering judgement** | 10 | top risks ranked with a mitigation each; a clear "what I would do next" (vendor data, prototype measurement, tolerancing) |

Automatic deductions: −5 for any NSC number quoted without a noise estimate; −5 for a "PASS" whose margin is smaller than its noise; −10 if the predictions were written after the measurements.

---

## Stretch tasks
1. **Track B — VCSEL source.** Replace the LED by an 850 nm VCSEL array (0.8 × 0.6 mm, 2 W, ±10° per emitter; build it as in `../L03-source-modeling-leds-and-lasers/work/L03_T5_vcsel.zmx`). The illumination now has far too *little* étendue to fill the lens: design a homogenizer (fly's-eye or diffuser + condenser) for σ ≈ 0.3–0.5, redo M2, M4 and M5 (Part B). Quantify: depth of field gain, efficiency, and speckle contrast estimate ($G/\lambda^2$ modes, $1/\sqrt{M}$ within one camera pixel's footprint — make your assumptions explicit). Which would you build for a bin-picking camera and why?
2. **DOE alternative.** Compare the DMD projector with a fixed-pattern DOE projector built from `../L08-diffractive-optics-and-pattern-projection/work/doe.py` and `L08_T4_dots_nsc.zmx`: efficiency, depth of field, flexibility of codes, zero-order eye-safety issue. One page.
3. **Track V — visible.** Re-optimize the L05 lens for 0.45–0.65 µm with a white LED; what breaks first (lateral colour in pixels, MTF at Nyquist, coatings)? Recompute the budget photometrically (lm, lux).
4. **Automate.** Using Course 07 (L03–L06) or ZOSPy, script Task 6 Part B: generate bars for any period, run the trace, fit modulation, loop over distances. Compare run time and noise with your manual results.
5. **Thermal reality.** LED output and peak wavelength drift with junction temperature (typ. −0.3 %/K power and ~0.2–0.3 nm/K shift for NIR LEDs — check your datasheet). Over 25–60 °C junction, what happens to scene irradiance and to lateral colour? Which spec line is first at risk?

## Reflection questions
1. Which single decision (architecture, F/#, cone angle, coatings) moved the end-to-end efficiency the most, and which moved fringe modulation at the range ends the most? Were they the same?
2. Your sequential MTF and your NSC fringe modulation disagree at 0.5 m. Name three legitimate physical reasons and one modelling mistake that could cause it.
3. Why is a projector with an F/2.0 lens on a ±17° DMD not "wasting" the DMD's étendue, and when would it be?
4. A colleague proposes replacing the 1 × 1 mm LED by a 2 × 2 mm LED "for 4× the power". What do you answer, with numbers?
5. Which of your results would you trust least on a real prototype, and what measurement would you make first?

<details><summary>Guidance</summary>

1. Typically efficiency is dominated by the collection/étendue-shape link (A) or by $\eta_{\text{DMD}}$ (both), while modulation at the range ends is dominated by the pupil fill / F/# (defocus), not by coatings. Different knobs — which is why the spec has both lines.
2. Physical: partial pupil fill (σ < 1) in NSC vs full fill in sequential; NSC includes ghosts/veil; non-uniform pupil illumination (fly's-eye grid) changes the defocus MTF shape. Modelling mistakes: detector not at the same distance convention, too few periods/rays, forgetting the 4/π factor, wrong MTF orientation (tangential vs sagittal).
3. The lens's étendue (5.28 mm² sr) is still larger than the LED's (3.14), so all the light that can be collected is collected; the DMD's extra acceptance would matter only for a source with $G > 5.28$ mm² sr, or if you needed the extra cone to push more flux from a large source — then F/1.71 would help efficiency but cost flat-state margin and depth of field.
4. 2 × 2 mm: $G$ = 12.6 mm² sr vs a 5.28 mm² sr lens → at most 42 % of its light can pass; the delivered flux rises by only ≈ 5.28/3.14 ≈ 1.7× (if radiance is equal and shapes match) — and the excess becomes stray light and heat. Better: a higher-radiance 1 × 1 mm die, or the VCSEL track.
5. Usually $\eta_{\text{DMD}}$ at 850 nm and the ghost level (coatings as built, the real tilted DMD). First measurement: total scene power and an all-on/all-off/half-field image with a calibrated camera at 1.0 m.

</details>
