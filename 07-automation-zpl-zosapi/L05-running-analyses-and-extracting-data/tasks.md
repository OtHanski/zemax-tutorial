# L05 — Tasks: Running analyses and extracting data

> Work in your `zlens` repository from L03/L04 (path recorded in `work/notes.md`). New code goes in `src/zlens/analyses.py` (raw-API extraction + ZOSPy adapters), `src/zlens/reference.py` (perfect-lens formulas), `src/zlens/plots.py`; scripts in `scripts/`; reusable analysis settings files in `config/analyses/`; outputs in `results/L05/`. Use the `opticstudio()` context manager from `connect.py` (L03 Task 4) and the comment lookup from `lde.py` (L04 Task 3). Commit after each task. Answers to questions go in this lesson's `work/notes.md`.
> Lenses used: the triplet `designs/L09_T2_triplet.zmx` (f = 50 mm, F/4, fields 0/14/20°, F-d-C) and the Course 04 capstone `designs/capstone.zmx` (f = 8 mm, F/2.4, 850 nm, configs 1–3 = 0.6 / 0.8 / 1.2 m).
> **API caveat:** member names marked "verify" in the lecture (e.g. `HuygensMtf`, `FieldCurvatureAndDistortion`, `GetTextFile`, data-grid row order) must be checked against your installed version's ZOS-API Syntax Help before you rely on them. Record what you found in `notes.md` — that is part of the deliverable.
> Estimated time: ~5 h

---

## Task 1 — The perfect-lens reference as a tested function (Python, no OpticStudio)
**Goal:** A ground truth that every extracted MTF must respect.
**Given / specs:** incoherent, aberration-free, unobscured circular pupil; $\nu_c = 1/(\lambda N)$; $\text{MTF}(s) = \tfrac{2}{\pi}[\arccos s - s\sqrt{1-s^2}]$ for $s = \nu/\nu_c \le 1$, else 0. Maréchal: $S \approx e^{-(2\pi\sigma)^2}$.
**Steps:**
1. In `reference.py` write `cutoff_lpmm(wl_um, fno)`, `mtf_perfect(nu_lpmm, wl_um, fno)` (vectorised with numpy, returns 0 beyond cutoff, never NaN) and `strehl_marechal(sigma_waves)`.
2. In `tests/test_reference.py`: test the values below to 3 decimals, MTF(0) = 1, MTF(ν ≥ ν_c) = 0, monotonic decrease, and that `mtf_perfect` accepts scalars and arrays.
3. Add `mtf_perfect_poly(nu, wls_um, weights, fno)` = weight-averaged monochromatic MTFs (good enough as a polychromatic reference for an *ideal* lens with the same focus for all colours — write in a docstring why a real lens's polychromatic diffraction limit in OpticStudio may differ slightly).
**Deliverable:** module + passing tests (`pytest -q`).
**Check yourself:**

| Case | $\nu_c$ [lp/mm] | MTF at listed frequencies |
|---|---|---|
| Triplet, 0.5876 µm, F/4 | 425.5 | 30 → 0.910; 50 → 0.851; 80 → 0.762 |
| Capstone, 0.85 µm, F/2.4 | 490.2 | 36.2 → 0.906; 72.5 → 0.812; 144.9 → 0.629 |
| Any lens, $s = 0.5$ | — | 0.391 |
| Maréchal | — | σ = 0.05 → 0.906; 0.07 → 0.824; 0.10 → 0.674 |

<details><summary>Hints</summary>

Use `np.clip(s, 0, 1)` before `arccos`/`sqrt`, then `np.where(s < 1, value, 0.0)`. For the polychromatic triplet reference at 30 lp/mm: F 0.926, d 0.910, C 0.900 → with equal weights ≈ 0.912.
</details>

## Task 2 — Spot diagram and FFT MTF with the raw API (Python + GUI cross-check)
**Goal:** Master the generic pattern, the indexing rules and the data-series layout on a lens you know.
**Given / specs:** triplet `designs/L09_T2_triplet.zmx`; spot diagram referenced to centroid, all fields, all wavelengths; FFT MTF all fields, polychromatic, maximum frequency 100 lp/mm.
**Steps:**
1. Write `dump_results(r)` (lecture §1.5) and run it once on a Standard Spot and once on an FFT MTF result. Paste the output into `notes.md` and answer: how many data series does the FFT MTF return for 3 fields, and what is the shape of each `YData.Data`?
2. In `analyses.py` write `spot_rms(oss, refer_to="centroid") -> pd.DataFrame` returning a tidy table (`field_idx, field_value, wave, rms_um, geo_um, refer_to`). Use **1-based** indices in `GetRMSSpotSizeFor(f, w)`, and decide by experiment which wavelength index returns the polychromatic value in your version (try `w = 0` and compare to the GUI — record the result).
3. Write `fft_mtf(oss, max_freq=100, sampling="64x64") -> pd.DataFrame` with schema `field_idx, field_value, freq_lpmm, orient (T/S), mtf`. Use `net2d_to_numpy` and assert its row/column convention on the first run with a print of a few values next to the GUI's Text tab.
4. Close every window in `finally`. Add `assert oss.Analyses.NumberOfAnalyses == n_before` at the end of the script (member name: verify) to prove you leaked nothing.
5. Open the same analyses in the GUI with the same settings and compare: RMS spot at 0/14/20°, MTF T and S at 30 and 80 lp/mm for the 20° field.
6. Sampling convergence: repeat `fft_mtf` with 32×32, 64×64, 128×128, 256×256 and tabulate MTF(T, 20°, 80 lp/mm) and wall time.
**Deliverable:** `scripts/triplet_spot_mtf.py`, `results/L05/triplet_spot.csv`, `results/L05/triplet_mtf.csv`, comparison table (script vs GUI) and convergence table in `notes.md`.
**Check yourself:** script and GUI numbers agree to all displayed digits when settings match (any difference means different settings — reference, sampling, field/wave selection — not "API noise"). Spot RMS in the ranges you saw in Course 02 L09 (≈ 5–15 µm on axis, 10–30 µm at 20°). Every MTF value is below the Task 1 polychromatic ceiling (0.91 at 30 lp/mm, ≈ 0.77 at 80). Convergence: the change from 128 to 256 should be ≲ 0.01; typically 64×64 is already adequate for this slow (F/4), moderately aberrated lens.

<details><summary>Hints</summary>

- If an MTF exceeds the diffraction ceiling, you are almost certainly reading the X column, a different field, or a single short wavelength.
- If your T and S curves are swapped compared with the GUI, you have the column order of `YData` transposed.
- Wall time for 256×256 grows roughly with the number of pupil samples (×4 per doubling) plus fixed overhead; at 32×32 the fixed overhead dominates.
</details>

## Task 3 — ZOSPy wrappers and your stable schema (Python)
**Goal:** Use the ZOSPy wrappers, isolate yourself from their column names, and check wavefront-grid conventions.
**Given / specs:** triplet; `zp.analyses.mtf.FFTMTF`, `zp.analyses.mtf.HuygensMTF`, `zp.analyses.wavefront.WavefrontMap` (module paths from the ZOSPy API docs; verify against your installed ZOSPy with `help(...)`).
**Steps:**
1. Run `FFTMTF(sampling="64x64", field="All", wavelength="All", maximum_frequency=100.0).run(oss)` and print `type(result.data)`, `result.data.columns`, `result.data.head()`. Write `adapt_fftmtf(df) -> df` that maps it to the **same schema as Task 2**. Assert that it equals your raw-API table to 1e-9.
2. Same for `HuygensMTF` (pick settings matching FFT sampling as closely as possible). Plot FFT vs Huygens for the 20° field. Note the difference at 80 lp/mm in `notes.md`.
3. Wavefront map: run `WavefrontMap(field=3, wavelength=2, sampling="64x64", remove_tilt=True)` (20°, d-line). Convert to a numpy array; mask points outside the pupil (check how they are encoded: 0 or NaN). Compute RMS and P-V over the pupil.
4. Compare your RMS with (a) the RMS printed in the GUI's Wavefront Map text output and (b) the `RWCE` operand (centroid reference) for the same field/wavelength (temporary MFE row or dashboard row; L04).
5. Orientation check: plot the map with `imshow(origin="lower", extent=...)` built from `MinX/Dx/Nx` (or ZOSPy's `get_data_grid(cell_origin=...)`). Compare with the GUI false-colour map: the coma "tail" must point the same way. Document the correct `origin` and whether `MinX` is an edge or a centre in the adapter docstring.
**Deliverable:** `adapt_*` functions with docstrings, comparison plots `results/L05/triplet_fft_vs_huygens.png`, `results/L05/triplet_wfe_20deg.png`, numbers in `notes.md`.
**Check yourself:** FFT and Huygens MTF agree closely (within ~0.01–0.02) for this slow F/4 lens with a flat image plane — Huygens matters for fast beams, large chief-ray angles at the image or tilted image planes (Course 03 L01–L02). Your grid RMS agrees with the GUI text output almost exactly if you mask identically, and with `RWCE` within a few % (different sampling and tilt/centroid conventions). If your RMS is far *smaller* than both, you probably averaged the zeros outside the pupil.

<details><summary>Hints</summary>

- A circular pupil on an N×N grid covers ≈ π/4 ≈ 78.5 % of the points; averaging over the whole square underestimates RMS by roughly √0.785 ≈ 0.89 if the outside is zero-filled (and biases the mean).
- Subtract the pupil mean (piston) before computing RMS.
- Keep the adapters tiny: rename columns, cast types, add `orient`, `freq_lpmm`, and the `zospy`/`opticstudio` version columns — no physics.
</details>

## Task 4 — Field curvature/distortion and settings files (Python + GUI)
**Goal:** Parse an analysis that ZOSPy does not wrap, and reproduce a GUI setup exactly via a `.CFG` file.
**Given / specs:** triplet; Field Curvature/Distortion analysis, d-line, distortion as percent (F-tan(θ) reference, the default).
**Steps:**
1. In the GUI, open Field Curvature/Distortion, set wavelength = 2 (d) and the options you want for the report; save its settings to `config/analyses/fcd_triplet.CFG` (Settings dialog → Save; location varies by version).
2. From Python: `New_Analysis(AnalysisIDM.FieldCurvatureAndDistortion)` (name: verify), `GetSettings().LoadFrom(cfg)`, apply, and `dump_results`. Identify which series is T focus shift, S focus shift and distortion (via `Description`/labels — verify names); write `field_curvature_distortion(oss, cfg) -> pd.DataFrame` with columns `field_deg, sag_mm, tan_mm, dist_pct`.
3. Change one option that is not exposed as a property using `ModifySettings(cfg, KEYWORD, value)` with a keyword from the ZPL `MODIFYSETTINGS` help page for this analysis (e.g. the wavelength or the field-scan density); re-run and confirm the change took effect.
4. Cross-check: distortion at 20° vs the `DIST` operand (check its arguments in the operand help) and the max over field vs `DIMX`; sagittal/tangential focus shift at 20° vs the GUI plot.
5. Fallback path: get the same numbers from the text output (`GetTextFile` — verify; or ZOSPy `get_text_output()` on a wrapper-less run via `zp.analyses.new_analysis`). Write a 20-line parser; keep it only as a test oracle.
**Deliverable:** `.CFG` under git, function + plot `results/L05/triplet_fcd.png` (two panels: field curvature with T solid and S dashed as in the GUI; distortion), cross-check table in `notes.md`.
**Check yourself:** |distortion| at 20° below ~1–2 % (Course 02 L09); field-curvature curves of the same shape as the GUI; `DIST` at 20° equals your series' last point to the displayed digits; the text parser and the series give identical numbers.

<details><summary>Hints</summary>

- If `LoadFrom` seems ignored, check that you call it on the settings object of the *same* analysis type, and that you `ApplyAndWaitForCompletion()` afterwards.
- Field-curvature x/y axis conventions: OpticStudio plots field on the vertical axis and focus shift horizontally; the data series stores field as X data. Don't let the plot orientation confuse the data orientation.
</details>

## Task 5 — Capstone MTF report figure across configurations (Python)
**Goal:** The figure you will reuse in the L08 automated report.
**Given / specs:** `designs/capstone.zmx`; configs 1–3 (0.6 / 0.8 / 1.2 m); fields 0, 0.3, 0.5, 0.7, 0.9, 1.0 of 5.7 mm real image height; FFT MTF at 850 nm, sampling chosen by a convergence check as in Task 2; specs S8 (MTF@36.2 ≥ 0.60 at 0.8 m, ≥ 0.45 at 0.6/1.2 m, 0–0.9 field, T & S) and S9 (MTF@72.5 ≥ 0.45 on axis, ≥ 0.35 to 0.9 field, 0.8 m).
**Steps:**
1. `mtf_vs_field(oss, freqs=(36.2, 72.5), configs=(1,2,3))`: for each config `SetCurrentConfiguration(k)`, run FFT MTF once with all fields, interpolate T/S at the two frequencies (or set max frequency so they are sample points — explain your choice), restore the original configuration in `finally`.
2. Save a tidy CSV `results/L05/capstone_mtf.csv` plus sidecar `capstone_mtf.json` with sampling, max frequency, wavelength, ZOSPy/OpticStudio version, git commit and lens SHA-256 (L03/L04 helpers).
3. `plots.py`: `plot_mtf_vs_field(df, spec)` — one panel per config, same y-limits, T solid / S dashed, diffraction ceiling from Task 1 as dotted lines, spec as grey steps/lines, markers on failing points. Also a classic MTF-vs-frequency plot for config 2 (lecture §5).
4. Print a pass/fail table against S8/S9 with margins (value − spec).
**Deliverable:** script `scripts/capstone_mtf_report.py`, CSV + JSON, `results/L05/capstone_mtf_vs_field.png`, `results/L05/capstone_mtf_cfg2.png`, pass/fail table.
**Check yourself:** every value below the ceilings 0.906 (36.2) and 0.812 (72.5 lp/mm); at the range ends (configs 1 and 3) a perfect lens focused for 0.8 m gives only ≈ 0.73 at 36.2 lp/mm (Course 04 L10), so your values there must be lower still. The pass/fail verdict must match what you concluded in the Course 04 capstone — if not, compare one point in the GUI before trusting either.

## Task 6 — Performance: what actually costs time (Python)
**Goal:** Measure instead of guessing; produce rules for your later loops (L06–L08).
**Steps:**
1. Time 50 evaluations of the triplet's FFT MTF (64×64) in four variants: (a) new window each time and `Close()`; (b) new window each time, never closed (stop if memory grows sharply — note the trend); (c) one window reused, `ApplyAndWaitForCompletion()` each time; (d) a single `MTFT` operand row evaluated with `CalculateMeritFunction()` instead of a window.
2. Repeat (c) in interactive-extension mode with the GUI showing the same analysis, once with lens update mode default and once with `oss.LensUpdateMode` set to `None` (ZOSPy; values per the ZOSPy docs).
3. Make a table of ms/evaluation and write three rules in `notes.md`.
**Deliverable:** `scripts/bench_analyses.py`, timing table, rules.
**Check yourself:** you should find (d) ≪ (c) < (a) per evaluation, and (b) degrading over time; GUI updates in extension mode add noticeable overhead per change. Exact numbers depend on your machine — the ranking is the point.

## Stretch tasks
1. **Fast .NET→numpy:** implement `net2d_to_numpy_fast` with `System.Runtime.InteropServices.Marshal.Copy` (or `System.Buffer.BlockCopy`) into a numpy buffer; test it against `net2d_to_numpy` on a 3×5 array with known values *and* on a Huygens PSF grid; benchmark both at 512×512.
2. **Analysis cache:** decorator `@cached_analysis` keyed on (lens SHA-256, configuration, analysis name, settings dict, ZOSPy/OpticStudio versions) that stores tidy tables as Parquet in `results/cache/`. Prove with a test that changing one thickness invalidates the cache.
3. Compare your Task 5 numbers with a Huygens MTF for the 1.0 field of config 2 — is the fast F/2.4 capstone a case where Huygens and FFT differ more than the triplet did? Explain via the chief-ray angle at the image (RAID, Course 04 L03).

## Reflection questions
1. Why do settings use 0 = "all" while result accessors are 1-based, and which bug does mixing them produce?
2. Your script's RMS spot differs from the GUI by 8 %. List three settings to compare before suspecting anything else.
3. When would you prefer a `.CFG` file over setting properties in code, and what does it give you for reproducibility?
4. Why store results as tidy tables with a sidecar JSON instead of the wrapper's DataFrame as returned?
5. Why is an operand (e.g. `MTFT`) the right tool inside an optimization or tolerancing loop, but the analysis window the right tool for the report?

<details><summary>Answers</summary>

1. Settings mirror the GUI drop-down, where "All" is an extra first entry (index 0); results are indexed by the actual field/wavelength numbers of the system, which start at 1. Mixing them silently returns another field's data (or the polychromatic value instead of a single wavelength) — no exception, wrong number.
2. Reference (centroid vs chief ray), ray density/pattern (and that `RSCE` uses Gaussian quadrature, not the spot-diagram grid), wavelength selection/weights, field selection, configuration, and whether the GUI window was updated after the last lens change.
3. When the analysis exposes options only via the settings file, or when you want *exactly* the GUI setup a colleague uses. The `.CFG` under git is an executable, diffable record of the analysis definition, shared by GUI, ZPL and Python.
4. Wrapper column names change between ZOSPy versions; your own schema keeps downstream code (plots, comparisons, reports) stable, and the sidecar keeps the settings and provenance without which the numbers are uninterpretable later.
5. An operand returns one number with little overhead and is evaluated inside OpticStudio's MF machinery (fast, configurable per row), which is what loops need. A window gives whole curves/maps with the same visual settings a reader expects from the GUI — the right form for documentation, but slower and needing window lifecycle management.
</details>
