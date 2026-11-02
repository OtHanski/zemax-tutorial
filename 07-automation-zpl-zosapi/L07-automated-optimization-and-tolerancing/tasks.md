# L07 — Tasks: Automated optimization and tolerancing

> Work in your `zlens` repository from L03–L06 (path recorded in `work/notes.md`). New code goes in:
> - `src/zlens/optimize.py`: extend L04 with `open_tool`, `run_local`, `run_timed`, `count_variables`.
> - `src/zlens/jobs.py`: job spec, canonical JSON, job id, seeds.
> - `src/zlens/db.py`: SQLite schema, claim/finish, metrics.
> - `src/zlens/runner.py`: worker loop and supervisor.
> - `src/zlens/glass.py`: AGF parser.
> - `src/zlens/stats.py`: Wilson interval, starts needed. Pure numpy, **no OpticStudio imports**.
> - `src/zlens/tolerance.py`: tolerancing run, ZTD → Parquet.
>
> Scripts go in `scripts/`, tests in `tests/`, outputs in `results/L07/`, with one run directory per job: `results/L07/runs/<job_id>/`. Use the `opticstudio()` context manager (L03), the comment lookup and `dashboard()` (L04), and the sidecar/provenance helpers (L05). Add `pyarrow` and `psutil` to your pinned dependencies. Commit after each task. Answers go in this lesson's `work/notes.md`.
>
> **Lenses:**
> - The triplet `designs/L09_T2_triplet.zmx`: f = 50 mm, F/4 (EPD 12.5 mm), fields 0/14/20°, F-d-C, N-SK16 / F2 / N-SK16.
> - The Course 04 capstone `designs/capstone.zmx`: f = 8 mm, F/2.4, 850 nm, configs 1–3 = 0.6 / 0.8 / 1.2 m.
> - The C06 L08 tolerancing files, if you finished them: the tolerancing copy of the capstone with its TDE, `aa_station_capstone.MF`, `eval_capstone.MF`, `tier1.TOP`. Copy them into `designs/tol/` and commit.
>
> **API caveat:** everything marked *(verify)* in the lecture must be checked against your installed version's ZOS-API Syntax Help: `IsRunning`, the return type of `RunAndWaitWithTimeout`, the `OptimizationCycles`/`OrthogonalDescent` members, `SolveType.Variable`, `Criterions.MeritFunction`, `SetupModes.Inverse…`, the `ITolerancing` cores/seed properties, the TDE load method, the MC file naming, `MonteCarloData.Values` Rows/Cols orientation, `GetMetadata`, and the application version properties. Keep a table "name → exists? → exact spelling" in `notes.md`. It is a deliverable.
>
> Estimated time: ~7 h (+ stretch)

## Task 1 — Optimizer wrappers and a determinism test (Python + OpticStudio)
**Goal:** Wrappers you can trust in unattended runs, plus measured facts about what is re-executable in *your* version.
**Given / specs:** triplet; its existing MF and variables (all radii; air spaces, if you made them variable in C02 L09).
**Steps:**
1. Implement `open_tool`, `run_local`, `run_timed` (lecture §2.2) and `count_variables(oss) -> list[tuple[int, str]]` (surface, column) by walking the LDE cells' solve types. `run_local`/`run_timed` must raise if the variable list is empty.
2. **Leak test:** call `run_local` on a design you corrupt deliberately so the call raises inside the `with` block (e.g. a callback that raises after the run starts, or a `KeyboardInterrupt` simulated with `raise`). Then immediately call `oss.Tools.OpenLocalOptimization()`: it must **not** return `None`.
3. **Determinism (local):** from the same freshly loaded file, run `run_local(cores=c)` twice for each of c = 1, 4, 8 (or your machine's physical core count). Record `mf_end` with `repr()` (all digits) and the radius of surface 1. Compute the max relative difference within the same `c` and between different `c`.
4. **Determinism (Hammer):** twice `run_timed("hammer", seconds=60, cores=8)` from the same start. Record `mf_end` and the end prescription fingerprint (lecture §4.2: hash of radius/thickness/material rounded to 1e-6 mm).
5. **Global:** one `run_timed("global", seconds=120)` on a copy in `results/L07/runs/global_test/`. List the files that appear in that folder, and record their naming pattern and which one is the best.
**Deliverable:** `optimize.py`, `tests/test_optimize_smoke.py` (marked `@pytest.mark.opticstudio`), determinism table and Global file list in `notes.md`.
**Check yourself:** within the same core count, local DLS should repeat to the last printed digit (if it does not, the start was not identical: check that you reloaded the file). Across core counts, expect identical results or differences at the 1e-10…1e-6 relative level. Hammer repeats should give **different** fingerprints, with MFs typically within a few %. After the leak test the next tool opens normally.

<details><summary>Hints</summary>

- Get the solve type of a cell via `row.GetCellAt(col).GetSolveData().Type` (or ZOSPy's helpers). Compare against the `SolveType` enum member for Variable *(verify)*. Radius, thickness, conic and material (for substitute glasses) are the usual columns.
- If `count_variables` finds variables but the MF does not move, check that the MF has no rows with weight 0 only, and that `DMFS` actually created operands (L04 Task 3).
- For the fingerprint use `json.dumps([[round(r, 6), round(t, 6), m] for …])` → SHA-256. Rounding before hashing is what makes it robust to the last-digit noise you measured in step 3.
</details>

## Task 2 — Multi-start on the air-spaced doublet: finding Kidger's two basins (Python + OpticStudio)
**Goal:** Reproduce the local-minimum story of [Kidger §8.3.2] with statistics, and size a multi-start study.
**Given / specs:** built entirely by script (`scripts/build_doublet.py`, L04 patterns):
- System: f = 100 mm, EPD 20 mm (F/5), fields 0°, 1.0°, 1.5° (Angle), wavelengths F, d, C (d primary), object at infinity.
- Lens 1: SCHOTT N-BK7, centre thickness 4.0 mm. Air gap 0.5 mm. Lens 2: SCHOTT F2, centre thickness 2.5 mm. Stop on surface 1.
- Image distance: marginal-ray height solve = 0.
- Variables: the four curvatures.
- MF: Optimization Wizard RMS spot radius, centroid, 3 rings × 6 arms, plus `EFFL` target 100 weight 1. Glass min centre/edge 1.0 mm, air min centre 0.3 mm, min edge 0.3 mm.

**Steps:**
1. `jobs.py`: `make_job(...)` → dict, `job_id(job)` = first 16 hex digits of SHA-256 of `json.dumps(job, sort_keys=True, separators=(",", ":"))`. Unit test: changing key order does not change the id, and changing any value does.
2. Seeds: `seeds = [int(s.generate_state(1)[0]) for s in np.random.SeedSequence(2026).spawn(40)]`. Store them in the jobs. Write `perturb_curvatures(c, sigma, seed)` (lecture §3.4) as a pure function, with a test that the same seed gives identical output.
3. Run 40 jobs with σ = 0.3 (start = a lens with all four curvatures equal to those of an equi-convex/plano-concave thin-lens achromat — work them out with your C02 L06 code, or just use ±0.01 mm⁻¹ and let `EFFL` pull). For each job: reload the start, perturb, `run_local` (Automatic cycles), save `results/L07/runs/<job_id>/doublet.zmx`, store the MF and the four curvatures in the DB (a simple SQLite file is enough for now; Task 3 formalises the schema).
4. Cluster: same basin if |ΔMF|/MF < 1 % **and** max |Δc|/c̄ < 0.02. Print the clusters with count, best MF and the shape (sign of each curvature). Open one representative of each in the GUI (Cross-Section).
5. `stats.py`: `wilson(k, n, z=1.96)` and `starts_needed(p, P)`. From your counts, compute $\hat p$ for the best basin, its Wilson interval, and the starts needed for 95 % confidence using the lower bound.
**Deliverable:** `build_doublet.py`, `jobs.py`, `stats.py` with tests, `scripts/doublet_multistart.py`, cluster table, sizing calculation in `notes.md`.
**Check yourself:** you should find at least two clusters with clearly different shapes. One has a biconvex crown and a nearly plano or negative-meniscus flint (Fraunhofer-like). The other has both elements bent as menisci in the same direction (Gauss-like). The Fraunhofer-like solution should have the lower MF, as Kidger argues. Unit-test values for `stats.py`: `wilson(455, 500)` = (0.8817, 0.9321); `wilson(6, 40)` = (0.0706, 0.2907); `wilson(50, 50)` = (0.9286, 1.0); `starts_needed(0.15, 0.95)` = 19.

<details><summary>Hints</summary>

- If all 40 starts land in one basin, increase σ to 0.5. If many fail (ray errors, negative edge thickness), lower it, or reject starts that violate the boundary rows before optimizing, and *count the rejections*. A rejected start is still a sample of your start distribution.
- The F2 element is thin. Fixed thicknesses keep the comparison clean: only the bending differs between basins.
- `starts_needed(p, P) = ceil(log(1 - P) / log(1 - p))`. Guard p = 0 and p = 1.
</details>

## Task 3 — Results database and the triplet flint sweep (Python + OpticStudio)
**Goal:** A real study: which flint for the triplet's centre element, with a database that will carry L08.
**Given / specs:** triplet; flint candidates from your installed `SCHOTT.AGF` with status standard or preferred, $1.60 \le n_d \le 1.76$, $25 \le V_d \le 40$; 3 multi-start starts per glass (σ = 0.15, seeds from `SeedSequence(7)`), plus the unperturbed start; local DLS, Automatic; variables as in Task 1.
**Steps:**
1. `glass.py`: `read_agf(path) -> pd.DataFrame` (name, formula, nd, vd, status, …), handling UTF-8 and UTF-16 (BOM). Write the test against a small synthetic `.AGF` snippet whose `NM` lines you copy from two real entries of your file (so the format is right for your version).
2. `db.py`: the schema of lecture §4.1 (`jobs`, `runs`, `metrics`), WAL mode, `claim_job(con, worker)`, `finish_job(con, job_id, run_row, metrics)` (one transaction), `fail_job(con, job_id, err)`. Test with an in-memory database: two claims never return the same job.
3. Provenance: `provenance(zos)` returns OpticStudio version, ZOSPy, pythonnet, numpy, Python versions, host, `git describe --always --dirty`, and the SHA-256 of the glass catalogue files the system uses. Store it in every `runs` row. The runner must refuse to start with a dirty tree unless `--allow-dirty` is given.
4. Job payload: copy the design into its run directory, set L2's material, perturb (unless start 0), optimize, save `triplet.zmx` via a temp name + rename, hash it, compute metrics: MF, `dashboard()` rows, RMS spot per field (L05), and the L04 variable count.
5. Run the study with **one worker** (Task 4 adds parallelism). Then kill the Python process half-way (Ctrl+C or Task Manager) and restart. The study must resume, rerun only the unfinished jobs, and end with exactly one `runs` row per job.
6. Analysis: best-of-4 MF per glass; scatter on the $(V_d, n_d)$ plane coloured by MF; table of the top 5 with dashboard values. Mark F2 (the C02 L09 baseline). How much does the spread between the 4 starts of one glass compare with the spread between glasses?
**Deliverable:** `glass.py`, `db.py`, `runner.py` (single worker), `scripts/study_triplet_flint.py`, `results/L07/results.sqlite`, `results/L07/triplet_flint.png`, top-5 table, resume-test log excerpt.
**Check yourself:**
- The F2 row (start 0) must reproduce the MF of `L09_T2_triplet.zmx` after a re-optimization, to the precision you found in Task 1.
- Expect the best flints to sit at lower $V_d$ than the crowns by a healthy margin. Higher-index flints usually help Petzval and therefore the 20° field.
- If start-to-start spread within a glass is comparable to the glass-to-glass differences, a single-start sweep would have been noise. This is the main lesson of the task.

<details><summary>Hints</summary>

- `NM` line fields: name, formula number, MIL code, nd, Vd, exclude, status, melt frequency (lecture §3.2; verify on your file). Skip glasses with an exclude flag set.
- Material edits for names not in the loaded catalogues fail. Check that `SCHOTT` is in the system's catalogue list (L04 §8) and log the status after every edit.
- For the resume test, the claim/finish must be idempotent: on restart, set every `running` job whose worker no longer exists back to `pending` before claiming.
- `pd.read_sql("SELECT r.job_id, r.mf_end, j.spec_json FROM runs r JOIN jobs j USING(job_id)", con)`, then `json_normalize` the spec column.
</details>

## Task 4 — Parallel runner, timeouts and crash recovery; F/# sweep as payload (Python + OpticStudio)
**Goal:** Throughput measured within your licence and core limits, and a runner that survives hangs and crashes.
**Given / specs:** triplet; F/# ∈ {3.0, 3.5, 4.0, 4.5, 5.6} (via EPD = 50/F#: 16.667, 14.286, 12.5, 11.111, 8.929 mm, or via image-space F/# if your file uses it); for each F/#: (a) **cold**: 8 multi-starts from the F/4 design; (b) **continuation**: one chain F/5.6 → F/3, each step starting from the previous optimum. Total 5 × 8 + 5 = 45 jobs, the continuation chain being sequential (dependency: store `depends_on` in the spec).
**Steps:**
1. **Licence/instance test:** start 1, 2, 3, 4 workers (each `opticstudio()` once) and log `LicenseStatus`/`IsValidLicenseForAPI` at connect. Record the maximum number of simultaneous standalone instances you can run. Ask your licence administrator whether that is allowed for long runs.
2. **Supervisor:** `runner.py --workers N --cores-per-worker M`, using `multiprocessing` with the spawn context. Workers heartbeat at every step. The supervisor kills a worker whose heartbeat is older than `job.budget_s + 60 s` (kill the **process tree** with `psutil`), marks the job `pending` (attempt < 3) or `failed`, and starts a replacement worker. At start, warn about stray OpticStudio processes.
3. **Fault injection** (behind a `--fault` flag): job kinds `raise` (Python exception), `hang` (`time.sleep(10**6)` inside the payload) and `kill_os` (you terminate the worker's OpticStudio process from Task Manager during a job). Each must end with the study finishing and the faulty job `failed` after 3 attempts (or `done`, for `kill_os` on retry).
4. **Throughput:** run the 40 cold jobs with (workers × cores) = 1×8, 2×4, 4×2 (within your licence). Record wall time, jobs/min, and peak memory per instance.
5. **Result:** plot best MF vs F/# for cold and continuation. Mark F/#s where they disagree by > 5 %, and open both designs at that F/# in the GUI.
**Deliverable:** `runner.py` (multi-worker), fault-injection log, throughput table, `results/L07/fno_sweep.png`, discussion in `notes.md`.
**Check yourself:** with short jobs, 4×2 should beat 1×8 in throughput (lecture worked example 3: 2.6× there; your ratio depends on MF size). If 4×2 is *slower*, check for oversubscription (cores per worker × workers > physical cores) or memory paging. The MF should rise steeply toward F/3. Continuation is usually smoother but can be stuck in a worse family at the fast end. After fault tests, no `OpticStudio.exe` processes remain when the study ends.

<details><summary>Hints</summary>

- Windows has no `fork`: everything a worker needs must be importable at module level, and the worker connects to OpticStudio **inside** the worker function, never in the parent.
- `psutil.Process(pid).children(recursive=True)` → `kill()` each child, then the parent. Before relying on this, find out in Task Manager whether the standalone instance appears as a child of `python.exe` in your version (lecture §7). Record it.
- Heartbeats: a single `UPDATE jobs SET heartbeat=? WHERE job_id=?` in its own short transaction. Never keep a transaction open across an OpticStudio call.
- A continuation job whose predecessor failed should be marked `failed` with reason "dependency", not run from the wrong start.
</details>

## Task 5 — Scripted tolerancing and yield extraction (Python + OpticStudio)
**Goal:** A tolerance run you can repeat with one command, whose trial table lands in Parquet and whose yield carries an interval.
**Part A — triplet, default tolerances:**
1. On a copy of the triplet in `results/L07/runs/<job_id>/`, apply the tolerance wizard as in ZOS-API example 14 with: radius ±0.1 mm (or fringes, if your wizard default is fringes; record which), thickness ±0.05 mm, surface decenter ±0.02 mm, surface tilt ±0.02°, element decenter ±0.02 mm, element tilt ±0.02°, index ±0.0005, Abbe ±0.5 %, irregularity 0.25 fringe. Compensator: back focus (the wizard default). Save the TDE to a file and commit it.
2. Run **sensitivity + Monte Carlo**: criterion RMS spot radius, sampling 3, `OptimizeAll_DLS`, cycles 2, 200 trials, save 10 MC files, `OutputFile`, `SaveTolDataFile`/`TolDataFile`. Time it.
3. **File smoke test:** assert that the report, the `.ZTD` and 10 MC lens files exist in the run directory. Record their exact names.
4. Close the tolerancing tool, open the **Tolerance Data Viewer** on the `.ZTD`, extract the MC table into a DataFrame with column names from the metadata, save `mc.parquet`, and store summary metrics (mean, σ, p90 of the criterion, compensator range) in the DB.
5. Cross-check: open the same `.ZTD` in the GUI viewer and compare three trials and the 90 % line of the text report.
6. Yield vs threshold: for RMS-spot thresholds from the nominal value to 3× nominal, plot $\hat y$ with Wilson 95 % bands (`stats.py`). How many trials would you need for ±2 % at the threshold where $\hat y \approx 0.9$?
7. **Repeatability:** run step 2 again with identical settings. Do the trial tables agree exactly (OpticStudio reseeds identically), only statistically, or not at all? Record the answer. It decides whether MC results in L08 are re-executable or archived.

**Part B — capstone (if C06 L08 is done):** put the C06 L08 route (b) into the runner. A tolerance job runs the tier-1 settings (set explicitly in code from `tier1.TOP`'s values, recorded in the spec) with 500 trials and saves all trials. Each trial is then evaluated by a separate **evaluation job** (`mc_extract` logic: load trial, load `eval_capstone.MF`, read commented rows), in parallel across workers. The evaluation results form one Parquet table. Compute the joint yield with Wilson bounds and compare with your C06 L08 numbers.
**Deliverable:** `tolerance.py`, `scripts/tol_triplet.py`, `results/L07/runs/<id>/mc.parquet`, yield plot, repeatability finding, (B) capstone evaluation Parquet and yield table.
**Check yourself:** the nominal criterion in the report matches the nominal RMS spot of the design (same sampling). The MC trial count in Parquet is 200 (plus nominal rows, if your version includes them: identify and drop them). The Python yield at the report's "90 %" threshold should come out close to 0.90 (exactly, if you use the same percentile definition). Part B's trial-0 row reproduces the C06 L08 baseline, as in its Task 3 check.

<details><summary>Hints</summary>

- If `OpenToleranceDataViewer()` returns `None`, the tolerancing tool is still open (one tool at a time).
- `.NET double[,]` → numpy: `np.array([[d[i, j] for j in range(d.GetLength(1))] for i in range(d.GetLength(0))])` is fine for 200 × 50. Verify that the shape matches `Rows`/`Cols` and transpose if necessary.
- Wilson at 180/200 = 0.90: interval (0.851, 0.934). ±2 % at 0.9 needs ≈ 864 trials.
- If no MC files appear (the 2020 community report), try setting `NumberToSave` before `NumberOfRuns`, check that the lens was *saved* in the run directory before opening the tool, and record the outcome. Fallback for evaluation: save trials via a `SAVE` operand, or perturb in Python yourself (stretch 1).
</details>

## Stretch tasks
1. **Post-cure on every trial** (C06 L08 stretch 2): for each saved capstone trial, draw 5 post-cure perturbations of the AA coordinate break (`TUTX/TUTY` ±0.01°, `TUDX/TUDY` ±0.002 mm, gap ±0.002 mm, uniform; seeded with `SeedSequence`), apply them via the LDE (comment lookup), evaluate with `eval_capstone.MF`, restore. Report the as-shipped yield with Wilson bounds and compare with C06 L08's median/p90 approximation.
2. **Global vs multi-start at equal wall time:** for the doublet and the triplet, give Global the same wall time as your Task 2/3 multi-start. Compare best MF found and number of distinct basins seen (cluster the 10 saved Global solutions).
3. **LHS system study:** Latin hypercube of 30 points over (F/# 3–5.6, semi-field 14–24°, total track ±10 %) for the triplet, each with 4 starts. Fit a quadratic surrogate of best MF and report main effects.
4. **Version drift guard:** a script that reruns 5 "golden" re-executable jobs and fails if any metric differs by more than your Task 1 tolerance. Run it after the next OpticStudio update.

## Reflection questions
1. Your flint sweep ranks glass A first with one start per glass, and glass C first with four. Which result do you trust, and what does that tell you about every single-start sweep you have seen?
2. Why is the job id computed from the job spec but not from the git commit? When must you change the spec anyway after a code change?
3. A colleague proposes to speed up the study by running 16 threads in one Python process against one OpticStudio instance. What happens, and what would you do instead?
4. Your Monte Carlo trial tables differ between two identical runs. Is the tolerance analysis wrong? How do you make the L08 report reproducible anyway?
5. 455 of 500 trials pass. Marketing wants "≥ 90 % yield". Write the one sentence you would put in the report.

<details><summary>Answers / guidance</summary>

1. Trust the four-start result, as long as the within-glass spread was comparable to the between-glass differences: the one-start ranking was partly ranking starting points. Any sweep that re-optimizes per point inherits basin noise. Either use several starts per point, or check that the spread is small compared with the effect you care about.
2. The id identifies the *recipe*. Including the commit would invalidate every cached result on each commit, even for refactors that change nothing. The commit goes into the result's provenance. When a code change alters results (a new metric definition, a different perturbation scheme), bump `recipe_version` in the spec so that old and new results do not mix.
3. The API allows one connection per process, and the instance runs one tool at a time, so threads would serialize at best and corrupt state or deadlock at worst. Use several processes, each with its own standalone instance, within the licence limit, and set cores per optimizer so that workers × cores ≈ physical cores.
4. Not necessarily. If OpticStudio's MC draws are not seeded identically, two runs are two samples, and their statistics should agree within the Wilson/SE bands. Treat the MC output as an archived artifact: keep the `.ZTD`, the trial Parquet and the MC files with hashes, and have the report read them rather than regenerate them. Your own Python perturbations are seeded and re-executable.
5. Something like: "Monte Carlo yield 91.0 % (455/500); 95 % one-sided lower confidence bound 88.7 %. The ≥ 90 % target is not demonstrated at 95 % confidence. Approximately 860 trials would be needed for a ±2 % interval." (Numbers: Wilson, z = 1.645 → 0.887.)
</details>
