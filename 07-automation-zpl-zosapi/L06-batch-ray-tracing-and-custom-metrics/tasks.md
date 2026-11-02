# L06 — Tasks: Batch ray tracing and custom metrics

> Work in your `zlens` repository from L03–L05 (path recorded in `work/notes.md`). New code: `src/zlens/raytrace.py` (batch tracing: reference loop + fast path), `src/zlens/metrics.py` (pure numpy: grids, centroids, RMS, CRA, Brown–Conrady fit; **no OpticStudio imports**), plots in `src/zlens/plots.py`; scripts in `scripts/`; tests in `tests/`; outputs in `results/L06/`. Use the `opticstudio()` context manager (`connect.py`, L03), the comment lookup (`lde.py`, L04) and the tidy-table + sidecar-JSON helpers (L05). Commit after each task. Answers go in this lesson's `work/notes.md`.
> Lenses: the triplet `designs/L09_T2_triplet.zmx` (f = 50 mm, F/4, fields 0/14/20°, F-d-C) and the Course 04 capstone `designs/capstone.zmx` (f = 8 mm, F/2.4, 850 nm, Real Image Height fields to 5.7 mm, ray aiming on, configs 1–3 = 0.6 / 0.8 / 1.2 m; sensor 2448 × 2048, 3.45 µm, 8.45 × 7.07 mm).
> **API caveat:** names marked *verify* in the lecture (`OPDMode` members, `RaysType.Paraxial`, `SetFieldType` and the field-type enum, `Marshal.Copy` overloads, the `RayTrace.dll` classes) must be checked against your installed version's ZOS-API Syntax Help. Record what you found in `notes.md`; that record is part of the deliverable.
> Estimated time: ~6 h (+ stretch)

## Task 1 — Reference batch tracer and its validation (Python + OpticStudio)
**Goal:** A slow but trustworthy `trace_norm_unpol` that every faster version will be tested against.
**Given / specs:** triplet; image surface; wavelength 2 (d).
**Steps:**
1. Implement `trace_norm_unpol(oss, hx, hy, px, py, wave, to_surface=None, opd_mode="None_")` as in lecture §2.3: broadcasting inputs, 1-based ray-number mapping, `err`/`vig` arrays, `try/finally: tool.Close()`.
2. Trace these 6 rays: $(H_y, P_y)$ = (0, 1), (0.7, 0), (1, 0), (1, 1), (1, −1), and $(H_x, P_x)$ = (1, 1) with the other coordinates 0. Compare $Y$ (or $X$) with weight-0 `REAY`/`REAX` rows at the image surface (scratch MF, L04) and with the GUI Single Ray Trace for one ray.
3. Trace a ray you know must fail: $P_y$ = 1.5 at $H_y$ = 1. Record `err`/`vig` and look up which surface the code points to in the LDE. Then do the same in ZPL (`RAYTRACE 0, 1, 0, 1.5, 2` → `RAYE()`, `RAYV()`) and confirm that the codes agree.
4. Trace to an intermediate surface (the stop) with `to_surface` and check one ray against `REAY` on that surface.
5. Write `tests/test_raytrace_smoke.py` (marked `@pytest.mark.opticstudio`, skipped when OpticStudio is not available) that asserts agreement with the stored `REAY` values to 1e-9 mm.
**Deliverable:** `raytrace.py`, smoke test, comparison table in `notes.md` (ray, batch Y, REAY, GUI).
**Check yourself:** batch and `REAY` agree to ~1e-12 mm (same tracer), and differences at the 1e-6 level mean you are on a different wavelength, configuration or field normalization. The over-filled-pupil ray returns non-zero `vig` (or `err`) and the same codes as ZPL.

<details><summary>Hints</summary>

- `REAY` arguments are surface, wavelength, $H_x$, $H_y$, $P_x$, $P_y$. Check the operand help for the order in your version.
- If the tool comes back `None`, another tool (often an optimizer you forgot to close in a previous crashed run) is still open. Close it, or restart the standalone instance.
- Ray numbers in results are 1-based (`output[1] - 1` in example 22).
</details>

## Task 2 — Where the time goes, and a fast path (Python + C# or DLL + ZPL)
**Goal:** Measured per-ray costs for every option, and a fast tracer that passes the Task 1 oracle.
**Steps:**
1. **Measure the reference.** Time `trace_norm_unpol` for $N$ = 10², 10³, 10⁴, 10⁵ random rays (uniform in the unit field and pupil disks; fixed seed) in standalone mode. Separate the time for (a) the `AddRay` loop, (b) `RunAndWaitForCompletion`, (c) the `ReadNextResult` loop. Repeat $N$ = 10⁴ in interactive-extension mode.
2. **ZPL baseline.** Write `macros/L06_rays.ZPL` that traces the same 10⁴ rays (read them from a text file, or regenerate with the same formula) with `RAYTRACE`, writes `hx hy px py x y err vig` per line with `OUTPUT`, and prints the elapsed time. Load the file with `np.loadtxt` and assert equality with the batch result to 1e-9.
3. **Fast path — choose one:**
   - (B) Download `RayTrace.dll` from the Ansys KB article (lecture [2]), unblock the zip, load it with `clr.AddReference`, and reproduce the forum's normalized-unpolarized example (lecture [3]). Record the exact class/method names that work in your version.
   - (C) Build your own `FastTrace` class library (lecture §3.1): reference `ZOSAPI.dll` and `ZOSAPI_Interfaces.dll` from the OpticStudio folder with Copy Local = False, and target the runtime OpticStudio uses (find it from the DLL's properties or the install's `*.runtimeconfig.json`/`*.config` files; record it). Pass arrays with `np_to_net_double` and read results back with `net_double_to_np`.
4. Write `tests/test_fasttrace.py`: 2000 random rays, fast path vs `trace_norm_unpol`, all 11 outputs + codes equal (allow NaN = NaN for failed rays).
5. Timing table (ms per 10⁴ rays) for: reference standalone, reference extension, ZPL, fast path standalone. Add three "rules for my loops" to `notes.md`.
**Deliverable:** `macros/L06_rays.ZPL`, `raytrace.py` with `trace_norm_unpol_fast`, C# project (if C) under `tools/fasttrace/`, tests, timing table.
**Check yourself:** the add/read loops dominate the reference timing, and `RunAndWaitForCompletion` is a small fraction for 10⁴ rays. Extension mode is several times slower per ray than standalone. The fast path should be ≥ 10× faster than the reference at 10⁴–10⁵ rays (the KB article reports up to 40× vs MATLAB loops). ZPL lands between the two. If your fast path is *not* faster, you are probably still converting arrays element by element.

<details><summary>Hints</summary>

- Use `time.perf_counter()` and report the median of 5 runs. The first call includes JIT and warm-up.
- A broadcast-friendly random disk: `r = sqrt(U)`, `φ = 2πV` gives uniform area density.
- The DLL's `AddRay` in the forum example takes Python lists. If lists are slow at 10⁵, try passing `System.Double[]` built with `np_to_net_double`.
- Keep the ZPL macro dumb: read, trace, write. Parsing belongs in Python.
</details>

## Task 3 — Full-field distortion map and Brown–Conrady fit (Python, then capstone)
**Goal:** The S12 calibration-residual metric, done properly, with a demonstration of the field-type trap.
**Part A — pure Python (no OpticStudio):**
1. In `metrics.py` write `fit_brown_conrady(x, y, u, v, radial=2, tangential=True, principal_point=True)` → dict with `F, k1, k2, p1, p2, cu, cv` and residual arrays. Use one linear `lstsq` on the stacked $u$/$v$ equations (lecture §5.1).
2. Reproduce the worked example: radial mapping $r = 8x(1 - 0.09x^2 + 0.02x^4 - 0.02x^6)$ mm at θ = 0, 7, …, 35°, with $p$ = 3.45 µm. Unit tests: $F$ = 7.9985 mm, $k_1$ = −0.0864, $k_2$ = 0.0036 (3 decimals / 4 significant figures), node residual max 0.049 px, dense (351 angles) residual max of the 6-point fit 0.121 px.
3. Add synthetic decentering ($p_1$ = 2e-4, $c_u$ = 3 px) to a 2D grid and check that the fit recovers it.

**Part B — capstone:**
1. **Show the trap.** On the capstone as delivered (Real Image Height), trace chief rays on a 21×21 grid $H_x \in [-0.741, 0.741]$, $H_y \in [-0.620, 0.620]$ (the sensor rectangle: 4.225/5.7 and 3.535/5.7), config 2, to the image. Plot landing points minus $(H_x, H_y)\cdot 5.7$ mm. Explain the result in two sentences.
2. **Scratch copy, object-space field.** Save to `results/L06/capstone_objfield.zmx`. Switch to Object Height (`SetFieldType`, *verify* the enum) and choose $Y_{max}$ so that the $H=1$ chief ray lands beyond the 5.5 mm sensor corner (lecture §5.1 step 1). Record $Y_{max}$, $T_0$ and `ENPP`.
3. Trace a 41×41 grid covering the sensor (adjust the $H$ range so landing points cover the full 8.45 × 7.07 mm with ~3 % margin), compute $x = X/d_E$, $y = Y/d_E$, $u,v$ in px, and fit with $k_1,k_2$ (+ $p_1,p_2,c_u,c_v$ as a check).
4. Validate on an independent 101×101 grid (same range, interleaved points). Report max and RMS residual (px) and a quiver plot of residuals ×1000.
5. Cross-check: radial distortion along +Y vs `DIST` and the Field Curvature/Distortion plot (paraxial reference); one or two grid points vs the Grid Distortion text output.
**Deliverable:** `metrics.py` + `tests/test_metrics.py` (Part A), `scripts/capstone_distortion_map.py`, `results/L06/capstone_distortion_map.csv` (+ JSON sidecar), `capstone_bc_residuals.png`, S12 verdict with numbers.
**Check yourself:** Part B.1 shows residuals at round-off level, so the trap is real. The fitted $F$ lies close to (not equal to) the paraxial EFL expressed in px (~2300 px for f ≈ 8 mm). $p_1, p_2, c_u, c_v$ come out ≈ 0 for the nominal design. Barrel distortion of a few % at the corner gives negative $k_1$. If the dense residual exceeds the node residual by 2× or more, your fit points are too sparse. Use the dense grid for the fit and keep the interleaved grid for validation.

<details><summary>Hints</summary>

- Design matrix for $u$: columns $[x,\ x r^2,\ x r^4,\ 2xy,\ r^2+2x^2,\ 1,\ 0]$; for $v$: $[y,\ y r^2,\ y r^4,\ r^2+2y^2,\ 2xy,\ 0,\ 1]$; unknowns $[F, Fk_1, Fk_2, Fp_1, Fp_2, c_u, c_v]$.
- Worked-example values, from `numpy.linalg.lstsq` on columns $[x, x^3, x^5]$: F = 7.99851, k1 = −0.08639, k2 = 0.00359; node residuals (px) 0, 0.0386, 0.0115, −0.0490, 0.0269, −0.0044.
- Inverted image: either let $F$ be negative or flip $u, v$. Be consistent with how your calibration code (e.g. OpenCV) defines the pixel axes.
- If `SetFieldType` changes but the field values stay in mm of *image* height, you must re-enter them in object mm. Check one chief ray by hand.
</details>

## Task 4 — CRA vs image height and the S13 consistency check (Python + OpticStudio)
**Goal:** The full CRA curve against the sensor spec, and a spec conflict you can quantify.
**Given / specs:** capstone, config 2; sensor CRA 0° ± 10° acceptance; S10 goal ≤ 8°, limit ≤ 12°; S13 ≤ 0.5 px for ±15 µm sensor shift.
**Steps:**
1. `cra(X, Y, L, M, N)` in `metrics.py`, returning signed and unsigned CRA (lecture §5.2), with a unit test on synthetic rays (e.g. a ray at ρ = 5 mm with L = 0, M = sin 10°: signed CRA = +10°; flip M: −10°).
2. Trace chief rays at $H$ = 0…1 (51 points) along azimuths 0°, 45°, 90°, 135°, 180° (Real Image Height file is fine here: why?). Plot CRA vs ρ, with the sensor's ±10° band and the 8°/12° lines.
3. Validate three points against `RAID` at the image surface.
4. Find the maximum CRA and where it occurs. Is the curve monotonic?
5. **S13 by ray trace.** In the scratch copy, change the image-surface position by +15 µm and −15 µm (thickness of the last gap, or a dummy surface just before the image), retrace, and compute landing shifts in px. Compare with $\Delta z\tan(\text{CRA})$ point by point.
6. In `notes.md`: does your design satisfy S13 at the corner? Compare the CRA limit $\arctan(0.5 \times 3.45/15)$ = 6.6° with your S10 numbers and propose a consistent spec pair.
**Deliverable:** `scripts/capstone_cra.py`, `results/L06/capstone_cra.png`, S13 table (field, CRA, predicted shift, traced shift), spec recommendation.
**Check yourself:** CRA ≈ 0 on axis, rising roughly like $\arctan(\rho/d_{XP})$. 8.0° at 5.5 mm corresponds to $d_{XP}$ ≈ 39 mm (Course 04 L03). Traced shifts match $\Delta z\tan$CRA to a few % (the difference is real-ray curvature). A corner CRA of 8° gives 0.61 px, which fails S13.

<details><summary>Hints</summary>

- Why Real Image Height is fine for CRA: you want CRA as a function of *image* height, so a field definition on the image side is exactly right here.
- `RAID` returns degrees and is unsigned. Compare it with `degrees(arccos(|N|))`.
- Shifting the image surface: change only the last thickness and restore it in `finally`. Better still, do it on the scratch copy.
</details>

## Task 5 — RMS spot from your own pupil grid vs `RSCE` and the spot diagram (Python + OpticStudio)
**Goal:** A convergence-checked RMS spot that you can trust and explain.
**Steps:**
1. **Pure test first.** `rms_spot(x, y, w, ref="centroid"|"chief", chief=None)` and `pupil_grid(n, kind="cell"|"edge")` in `metrics.py`. Reproduce the worked-example table ($r_{RMS}/a$ for n = 8…128, both grid kinds) with the synthetic defocus $\epsilon = a(P_x,P_y)$, and assert $|r_{RMS}/a - 1/\sqrt2| < 0.003$ at $n$ = 64 (cell).
2. Triplet, polychromatic (F, d, C with the file's weights), fields 0, 14, 20°: compute RMS (centroid reference) with cell-centred grids $n$ = 16, 32, 64, 128. Use the vectorized layout of lecture §6, so there is a single batch per $n$.
3. Compare with `RSCE` (polychromatic, centroid; choose rings/arms per the operand help) and with the Standard Spot RMS (L05 Task 2 values) at default and high ray density.
4. Repeat for the capstone at the 1.0 field in configs 1–3 (monochromatic 850 nm). Is the RMS spot at 0.6 m consistent with defocus alone? Use the worked example (c) ($a/\sqrt2$ ≈ 4 µm for 27 µm defocus at F/2.4) as the yardstick.
**Deliverable:** convergence table (n, rays, RMS per field, % vs `RSCE`), `results/L06/triplet_rms_convergence.png`, capstone 3-config table.
**Check yourself:** at $n$ = 64 your RMS agrees with `RSCE` to ≲ 0.5 %. The Standard Spot at default density may differ by 1–3 %. Edge-inclusive grids converge from below. For the capstone at 0.6 m, the RMS spot is at least of the order of the 4 µm defocus-only value. If it is much smaller, check that the configuration really changed.

<details><summary>Hints</summary>

- Polychromatic weights: weight per ray = wavelength weight / (rays traced at that wavelength), which is identical if every wavelength gets the same grid.
- The centroid comes from *all* wavelengths together. Do not average per-wavelength RMS values.
- If `RSCE` and your grid disagree by a constant ~5–10 %, check vignetting factors, the reference (centroid vs chief), and whether you included rays with `vig ≠ 0`.
</details>

## Task 6 — Depth-dependent image-point shift across configurations (Python + OpticStudio)
**Goal:** The Zivid-specific metric: how much the image of a fixed line of sight moves between 0.6, 0.8 and 1.2 m, compared with your calibration tolerance.
**Steps:**
1. On the Object Height scratch copy from Task 3, choose 9×7 normalized directions $(x, y)$ spanning the sensor. For each config $k$: set the configuration, compute $d_{E,k} = T_{0,k} + z_E$ (`ENPP` per config), convert to object coordinates $X = d_{E,k}x$, then to $H = X/Y_{max,k}$ (with the per-config max field from the MCE or a fixed $Y_{max}$ large enough for 1.2 m), and trace chief rays.
2. Compute $\Delta_k$ = landing(config k) − landing(config 2) in px. Plot quiver maps for k = 1, 3 and max $|\Delta|$ vs field radius.
3. Repeat with `RaysType.Paraxial` (*verify*). The paraxial shifts must be ≈ 0. If not, your object placement or pupil distance is wrong.
4. Repeat with *centroids* from a 32×32 cell-centred pupil grid instead of chief rays, and report how much the centroid shift differs from the chief-ray shift at the corner (coma and defocus asymmetry).
5. Interpret in `notes.md`: is the shift ≪, ≈ or ≫ the S12 residual (0.1 px)? If it is comparable, your calibration must be depth-aware (Brown 1971 style), or the 0.8 m-only calibration error shows up in 3D (Course 04 L09).
**Deliverable:** `scripts/capstone_depth_shift.py`, `results/L06/capstone_depth_shift.csv` + sidecar, quiver plots, interpretation.
**Check yourself:** shifts are zero on axis and grow with field. Paraxial shifts vanish to round-off. Real shifts at the corner for a well-corrected 8 mm lens are typically fractions of a pixel. A value of several pixels almost always means the line of sight was not held fixed (wrong $d_E$ or a forgotten `SetCurrentConfiguration`).

<details><summary>Hints</summary>

- Hold the *direction from the paraxial entrance pupil* fixed, which is what a pinhole calibration assumes. Then everything that remains is the lens's deviation from the pinhole model at that depth.
- Assert the current configuration inside the loop (`oss.MCE.CurrentConfiguration`, *verify*) and restore the original in `finally`.
</details>

## Stretch tasks
1. **Wavefront from rays.** Trace a 64×64 pupil grid with `OPDMode.CurrentAndChief` (chief ray first), validate five points against `OPDC`, then fit Fringe Zernikes by least squares in numpy and compare with the Zernike Fringe Coefficients analysis (L05). Resolve the OPD units/sign question from lecture §2.4 and document it.
2. **Encircled energy in pixels.** From the Task 5 rays, compute the fraction of ray weight that lands in the 3×3 pixel neighbourhood of the centroid pixel (with sub-pixel centroid offsets 0, 0.25, 0.5 px) for the capstone 1.0 field, configs 1–3. Discuss what this means for sub-pixel fringe decoding.
3. **UDOC.** Port the S13 metric (max landing shift for ±15 µm) to a C# UDOC (L02) using your `FastTrace` code, add it to the capstone MF with weight 0, and time one MF evaluation.
4. **Tolerance-aware map.** Run your Task 3 script on 10 Monte Carlo files from Course 06 L03/L08 (if you have them) and plot the distribution of fitted $p_1, p_2, c_u, c_v$.

## Reflection questions
1. Why does a Real Image Height field type make a field-grid distortion map meaningless, and why is the same field type perfectly fine for a CRA curve?
2. Your batch result disagrees with `REAY` by 3 µm. List four settings you would check, in order.
3. Why are per-ray `AddRay`/`ReadNextResult` calls slow even though OpticStudio traces millions of rays per second, and what are the two ways to avoid them without leaving Python?
4. Why does a fit residual evaluated at the fitting points understate the model error, and how does batch tracing fix that cheaply?
5. Paraxially, a fixed line of sight lands on the same pixel at any depth. Name three real effects that break this, and the metric from this lesson that exposes each.

<details><summary>Answers</summary>

1. With Real Image Height, OpticStudio solves for the object point whose chief ray lands at $H\cdot h_{max}$, so landing points equal the input grid by construction and the distortion is hidden in the (unreported) object coordinates. A CRA curve is a function of image height, so an image-side field definition samples it directly.
2. Wavelength number → configuration → field type/normalization (radial vs rectangular) → ray aiming and vignetting factors (and the surface number/local frame of the target surface).
3. The cost is in the interop: two .NET calls per ray, each boxing ~14 arguments and returning a tuple, plus a process boundary in extension mode. Avoid it by (a) a compiled helper that loops in .NET (Ansys `RayTrace.dll` or your own C# class) with bulk array copies, or (b) letting OpticStudio loop internally via a ZPL macro (or a UDOC when the metric lives in the MF).
4. Least squares minimizes the error at the fitting points, so between sparse points the model can deviate more (worked example: 0.049 px at 6 nodes vs 0.121 px densely). Batch tracing makes dense, independent validation grids cheap.
5. Pupil aberration (field-dependent projection centre) → depth-shift map with chief rays (Task 6). Conjugate-dependent distortion and coma → chief-ray vs centroid shift across configs (Task 6.4). Image-side focus or sensor shifts with non-zero CRA → $\Delta z\tan$CRA (Task 4).
</details>
