# L08 — Tasks: Capstone — a reproducible automated design report

> Work in your `zlens` repository from L03–L07 (path recorded in this lesson's `work/notes.md`). New code goes in the package `src/zlens/report/` (`__main__.py`, `collect.py`, `evaluate.py`, `rules.py`, `render.py`, `compare.py`, `templates/`). Spec files go in `specs/`, accepted baselines in `baselines/`, imported evidence (ghost report, sensitivity table, MC Parquet, spot-check notes) in `evidence/`, and reports in `results/report/<git-describe>/`. Unit tests go in `tests/`. Commit after each task. Answers and the review go in this lesson's `work/notes.md`.
> **Input lens:** copy `../../04-machine-vision-camera-lenses/L10-capstone-machine-vision-lens/work/capstone.zmx` (and its `HANDOFF.md`) to `designs/capstone.zmx` if you have not already done so in L05. Conventions: configs 1/2/3 = 0.6/0.8/1.2 m (config 2 nominal), further configs (thermal 0/45 °C, focus ±15 µm) after these; the focus thickness has the comment "FOCUS COMP"; dashboard operands with row comments at the top of the MFE; surface comments "L1 front" … "STOP", "FILTER", "COVER".
> **Optional inputs:** C06 L08 tolerance files in `designs/tol/` and the L07 Part B evaluation Parquet (`results/L07/runs/<id>/…`).
> **API code** in this lesson that did not appear (tested) in L03–L07 is marked *(verify)*. Verify it against your installed version's ZOS-API Syntax Help (Help tab) or the ZOSPy API reference before relying on it.
> Estimated time: ~14–18 h (Tasks 1–3 one session, Tasks 4–5 one session, Task 6 and the review one session).

## Task 1 — The specification as data, the evaluator and the conflict rules (Python, no OpticStudio)
**Goal:** Everything downstream of `results.json` is pure Python and unit-tested before you open OpticStudio.
**Given / specs:** Course 04 L10 lecture §1.3 (S1–S19) and §1.1–1.2 (pixel 3.45 µm, F/2.4, 850 nm, ±27.2 µm range-end defocus, sensor corner 5.5 mm, full image circle 5.7 mm).
**Steps:**
1. Write `specs/capstone_v1.0.yaml` with one entry per spec row S1–S19 (split rows with several conditions into `S8a/S8b/S8c`, `S9a/S9b`, `S14a/S14b`, `S17a…`). Fields: `id`, `what`, `metric` (key or glob), `reduce` (`min|max|maxabs|value`), `limit`, optional `goal`, `unit`, `verification` (how, from C04 L10), `evidence` (for imported rows: S16, S19). Transcribe; do not "fix" anything yet.
2. `evaluate.py`: `evaluate(spec, metrics) -> list[Verdict]` with the four verdicts (PASS, GOAL-MISSED, FAIL, NOT-EVALUATED), signed margin, and the arg-min/arg-max key for reduced rows. Operators: `<=`, `>=`, `within` (absolute or relative tolerance), `monotonic` (for S12's "monotonic", applied to a list-valued metric).
3. `rules.py`, static rules (lecture §4.1), each returning `{rule, rows, severity: conflict|warning|ok, message, numbers}`:
   - **R1** S13 ⇒ CRA bound: $\theta_\text{max} = \arctan(0.5\,p/\Delta z)$; compare with S10 limit and goal. Message must contain the three alternatives (tighten S10, relax S13 to the value matching the S10 goal, reduce $\Delta z$ to $0.5p/\tan\theta_\text{goal}$).
   - **R2** S7 vs S10: CRA allowance $= 24^\circ - u'$, with $u'$ both $\arctan(1/2N)$ and $\arcsin(1/2N)$; `warning` if the S10 limit lies within that band or within 0.5° of it.
   - **R3** feasibility ceilings: diffraction MTF $\frac{2}{\pi}\left(\arccos x - x\sqrt{1-x^2}\right)$, $x=\nu\lambda N$, and the range-end ceiling 0.73 from C04 L10 (store it in the spec file as a cited constant, do not recompute defocus here). `conflict` if a threshold ≥ its ceiling, `warning` if ≥ 0.85 × ceiling.
   - **R4** S13 vs S14: corner shift $\Delta z_\text{thermal}\tan(\theta_\text{goal})$ in px for the S14 ±5 µm focus budget; `ok` if ≤ 0.5 px. Rules that confirm consistency are reported too.
4. `tests/test_rules.py` and `tests/test_evaluate.py`: the numbers below; plus a missing metric → NOT-EVALUATED (never PASS), a glob that matches nothing → NOT-EVALUATED, a reduced row reports the right arg-min.

**Deliverable:** `specs/capstone_v1.0.yaml`, `evaluate.py`, `rules.py`, tests passing (`pytest -m "not opticstudio"`).
**Check yourself:**
- R1: $\theta_\text{max}$ = 6.560°; S10 limit 12° and goal 8° both exceed it → `conflict`. Alternatives: S13 relaxed to 0.611 px (for 8°), or $\Delta z \le$ 12.27 µm (for 8°).
- R2: allowance 11.98° (arcsin) … 12.23° (arctan); S10 limit 12° inside the band → `warning`.
- R3: diffraction ceilings at F/2.4, 850 nm: 0.906 (36.2 lp/mm), 0.812 (72.5 lp/mm); cutoff 490.2 lp/mm. S9a 0.45 < 0.85 × 0.812 = 0.690 → `ok`; S8 range ends 0.45 vs 0.73 → `ok`; S8a nominal 0.60 vs 0.906 → `ok`.
- R4: 5 µm × tan 8° = 0.70 µm = 0.20 px → `ok`.

<details><summary>Hints</summary>

- Keep the YAML loader strict: unknown fields are an error. A typo like `limt:` must not silently remove a limit.
- Margin: for `<=` use $(L - v)/|L|$; for `>=` use $(v - L)/|L|$; for `within` use $1 - |v - c|/\text{tol}$ (1 at centre, 0 at the edge).
- Glob expansion: `fnmatch` on the metric keys after expanding `{a,b}` braces yourself (fnmatch does not do braces).
- R1 check in Python: `math.degrees(math.atan(0.5*3.45/15))` → 6.5602.
</details>

## Task 2 — The collector: from `capstone.zmx` to `results.json` (OpticStudio + Python)
**Goal:** One function that loads the lens, runs every analysis once with recorded settings, and writes the data contract.
**Steps:**
1. `collect.py`: `collect(lens: Path, out: Path, *, allow_dirty=False, with_tolerance=None) -> Path`. Inside one `opticstudio()` context (L03):
   - Refuse a dirty tree unless `allow_dirty`; hash the lens bytes (SHA-256) **before** loading; copy the lens to `out/scratch/capstone.zmx`; load the copy; never write to `designs/`.
   - **Assert conventions** and fail loudly if any is missing: surfaces "STOP", "FILTER", "COVER", "FOCUS COMP" found by comment lookup (L04); config count ≥ 3; object thickness of configs 1/2/3 ≈ 600/800/1200 mm. Read the object distance per configuration via `SetCurrentConfiguration(k)` *(verify the exact accessor on `oss.MCE`)* and the surface-0 thickness. Missing conventions are findings for `HANDOFF.md`.
2. Sections, each a function returning a `dict` of flat metric keys (lecture §2) plus tidy tables saved next to `results.json`:
   - `prescription()`: per surface: index, comment, type, radius, thickness, material, semi-diameter, conic (and aspheric terms if any). Row access via `oss.LDE.GetSurfaceAt(i)` (L04). The property names `Radius`, `Thickness`, `Material`, `SemiDiameter`, `Conic`, `Comment` are what you used in L04; re-check them *(verify)*. Also store the canonical prescription fingerprint (L07).
   - `first_order()`: `dashboard()` (L04) in each of configs 1–3 → `first_order.c{k}.{comment}`; plus `first_order.efl_mm` from config 2.
   - `mtf()`: L05 Task 5 logic: FFT MTF, configs 1–3, fields 0/0.3/0.5/0.7/0.9/1.0, T & S, 36.2 and 72.5 lp/mm, sampling from your L05 convergence study.
   - `distortion()`: L06 Task 3, object-space field scratch copy, 41×41 fit / 101×101 validation; store $F, k_1, k_2, p_1, p_2, c_u, c_v$, max/RMS residual px, and the radial distortion curve (list → S12 monotonic test).
   - `cra()`: L06 Task 4, CRA vs ρ along 5 azimuths, `cra.max_deg`, and its location; plus `s13.max_shift_px` traced (±15 µm), and `s13.predicted_max_shift_px` = $\Delta z\tan$CRA.
   - `filter_aoi()`: max AOI at the "FILTER" surface over pupil and field (L06 or the L02 UDOC).
   - `relative_illumination()`: RI at the 6 fields, config 2, as specified in S11 (real apertures, no vignetting factors). Use `RELI` rows in an evaluation MF, or the Relative Illumination analysis via ZOSPy/raw API *(verify that a wrapper exists in your ZOSPy version; otherwise use the operand)*.
   - `lateral_colour()`: chief-ray landing difference 835 vs 865 nm at full field, in µm and px.
   - `thermal()`: identify the thermal configurations by their `TEMP` value in the MCE (not by index). For each, compute EFL and the best-focus shift relative to the sensor: on the scratch copy, sweep "FOCUS COMP" by ±10 µm in 2 µm steps, evaluate on-axis MTF at 36.2 lp/mm, fit a parabola, and report peak position minus the nominal value (Course 03 L09). Restore in `finally`.
   - `provenance()`: L07 function plus SHA-256 of spec file, MF files, analysis-settings files and every `evidence/` file referenced by the spec.
3. Write `results.json` with sorted keys and a stable float format. Time each section and store `timing.*` **outside** `metrics`.
4. **Idempotence test:** run `collect` twice on the same commit. `metrics` must be byte-identical. If not, find out which section is non-deterministic and why (multi-threaded analysis? random ray grids?). Record the answer.

**Deliverable:** `collect.py`, `results/report/<describe>/results.json` + tidy tables, timing table and idempotence finding in `notes.md`.
**Check yourself:** EFL = 8.00 mm ± 1 %; MTF values below the ceilings 0.906/0.812, and at the range ends below 0.73; CRA ≈ 0 on axis rising roughly like $\arctan(\rho/d_{XP})$; traced S13 shift equals $\Delta z\tan$CRA to a few %; $k_1 < 0$ for barrel distortion; fitted $F$ ≈ 2300 px. The pipeline should take a few minutes, dominated by MTF and the distortion grid. If it takes much longer, check L05's sampling and L06's batch path.

<details><summary>Skeleton (verify API members marked)</summary>

```python
# src/zlens/report/collect.py — skeleton
import hashlib, json, shutil, time
from pathlib import Path
from zlens.connect import opticstudio            # L03
from zlens.lde import surface_by_comment         # L04
from zlens.mfe import dashboard                  # L04
from zlens.jobs import provenance                # L07 (wherever you put it)

SECTIONS = ["prescription", "first_order", "mtf", "distortion", "cra",
            "filter_aoi", "relative_illumination", "lateral_colour", "thermal"]

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def collect(lens: Path, out: Path, allow_dirty=False, with_tolerance=None) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    lens_sha = sha256(lens)
    scratch = out / "scratch" / lens.name
    scratch.parent.mkdir(exist_ok=True)
    shutil.copy2(lens, scratch)
    metrics, timing = {}, {}
    with opticstudio() as (zos, oss):
        prov = provenance(zos)
        if prov["dirty"] and not allow_dirty:
            raise SystemExit("dirty tree: commit or pass --allow-dirty")
        oss.load(str(scratch.resolve()))          # absolute path (L03)
        check_conventions(oss)                    # raises with a clear message
        for name in SECTIONS:
            t0 = time.perf_counter()
            metrics.update(globals()[name](oss, out))
            timing[name] = time.perf_counter() - t0
    doc = {"schema": "zlens.report/1",
           "provenance": {**prov, "lens_sha256": lens_sha},
           "metrics": metrics, "timing_s": timing}
    path = out / "results.json"
    path.write_text(json.dumps(doc, sort_keys=True, indent=1))
    return path
```

`check_conventions` uses `surface_by_comment` for the four labels and the MCE to read the object distance per configuration.
</details>

## Task 3 — Renderer: Markdown + HTML report with plots (Python, no OpticStudio)
**Goal:** The C04 L10 §3 report template, generated from `results.json` + `verdicts.json`.
**Steps:**
1. `render.py` with a Jinja template (or plain f-strings if you prefer zero dependencies) `templates/report.md.j2`. Convert to HTML with a Markdown library of your choice, or have pandoc do it if installed. Pin whichever you use.
2. Mandatory section order:
   1. **Header**: lens name, design tag (`git describe`), spec version, date (UTC), DIRTY watermark if applicable.
   2. **Summary**: counts of PASS / GOAL-MISSED / FAIL / NOT-EVALUATED; regression summary (Task 4); exit code with its decoded bits.
   3. **Cross-spec conflicts and warnings** (Task 1 rules plus the design-based rules of lecture §4.2).
   4. **Spec compliance table**: id, requirement, value, limit, goal, margin, verdict, arg-min location, evidence/source.
   5. **Prescription table** and **first-order data** per config.
   6. **MTF vs field** per config (one figure, three panels or three line styles; T solid / S dashed; the spec thresholds drawn as horizontal lines; diffraction ceiling as a dotted line).
   7. **Distortion**: radial distortion curve, Brown–Conrady coefficients, residual quiver plot (×1000), max/RMS residual in px.
   8. **CRA curve**: CRA vs ρ, 5 azimuths, sensor ±10° band, S10 goal/limit lines, **and the R1 line at 6.56°**; S13 table (predicted vs traced shift).
   9. **Relative illumination**, **filter AOI**, **lateral colour**, **thermal check** (EFL ppm and focus shift per thermal config vs S14).
   10. **Tolerance / MC yield** (optional, Task 6).
   11. **Imported evidence** list with file hashes and the lens hash each was computed for.
   12. **Provenance block** (all of lecture §5's table) and timing.
3. Figures: `fig/*.png` at fixed size and dpi, sans-serif, no titles that repeat the caption. Every figure caption names its data key(s) and analysis settings. Pass `metadata=` to `savefig` to drop what you can (see the matplotlib docs for your backend), but do **not** rely on byte-identical PNGs.
4. `evaluate`, `render` and `compare` must work from a copied `results.json` on a machine without OpticStudio. Prove it: run them in a fresh venv without ZOSPy/pythonnet installed (or on WSL/Linux).

**Deliverable:** `render.py`, templates, `results/report/<describe>/report.md`, `report.html`, `fig/`. Screenshot-free: the report is the evidence.
**Check yourself:** the compliance table lists every row S1–S19. Rows you have not produced evidence for are NOT-EVALUATED with a reason, not missing. The conflicts section shows R1 as a conflict for spec v1.0. Re-rendering from the same JSON gives an identical `report.md`.

## Task 4 — Baseline and regression check (Python; OpticStudio for the experiment)
**Goal:** A CI gate that catches "worse than before", with tolerances that you measured.
**Steps:**
1. `compare.py`: `compare(current, baseline, tolerances) -> list[Delta]` with classes `same / better / worse / new / missing` (lecture §6). The direction comes from the spec operator; for info metrics use a `direction:` field in `specs/tolerances.yaml`.
2. **Measure the noise.** Run the collector once with your production settings and once with a finer setting: MTF sampling ×2, distortion grid 61×61 instead of 41×41, CRA 101 instead of 51 points. Per metric family, record the max |Δ|. Set `tol = max(floor, 3 × max|Δ|)` and write `specs/tolerances.yaml` with a comment saying how each value was derived. Families: `first_order.*` (relative 1e-6), `mtf.*`, `distortion.*`, `cra.*`, `s13.*`, `ri.*`, `thermal.*`.
3. Exit codes as a bit mask (1 limit FAIL, 2 worse/missing, 4 NOT-EVALUATED/stale, 8 cross-spec conflict). `python -m zlens.report designs/capstone.zmx --baseline baselines/capstone.json` must print the decoded bits and return the integer.
4. Accept the current report as baseline: `--update-baseline` copies the `metrics` block (and the provenance, for reference) to `baselines/capstone.json`. Commit it on its own with a message that names the tag.
5. **Planted regressions** on a scratch branch (do not merge):
   - (a) change "FOCUS COMP" by +10 µm and save as `designs/capstone.zmx`; re-run; which rows regress? Is any spec row now FAIL?
   - (b) change the MTF sampling setting only (the lens is unchanged): what should the comparison say, and what does it say? A settings change must be visible through the settings hash in provenance, even if all values are `same`.
   - (c) delete the CRA section from `SECTIONS`: the run must exit with bit 2 (`missing`) and bit 4 (S10, S13 NOT-EVALUATED).
6. `tests/test_compare.py`: synthetic dictionaries for each class, including the lecture worked example (b): baseline 0.512, current 0.497, tol 0.005, `>=` row → `worse`; margin vs S8 range-end limit 0.45 = +10.4 %.

**Deliverable:** `compare.py`, `specs/tolerances.yaml` with derivations, `baselines/capstone.json`, the three planted-regression outputs (exit code + diff table) in `notes.md`.
**Check yourself:** for (a), a +10 µm image shift is about a third of the ±27.2 µm range-end defocus, so expect MTF at one range end to improve and at the other to degrade, with the nominal config 2 degrading slightly. Find out which end improves from the sign convention of your "FOCUS COMP" thickness, and explain it. The CRA hardly changes, and S13 traced values change only slightly. Paraxial EFL does not change at all (`same`), which is a good sanity check that the comparator does not flag unchanged quantities.

<details><summary>Hints</summary>

- Compare only `metrics`; never compare `provenance.utc`, `timing_s` or the host name.
- For lists (radial distortion curve, CRA curve) compare element-wise max |Δ| and report the location.
- `--update-baseline` should refuse when the tree is dirty or the report has exit bit 1 set, unless `--force`. Accepting a failing design as baseline must be a conscious act.
</details>

## Task 5 — Git workflow: tags, a design revision, and a report diff (OpticStudio + git)
**Goal:** The full loop: the report flags the S10/S13 conflict, you resolve it by a spec change plus a design revision, and the review artefact is a diff of two reports.
**Steps:**
1. Tag the current state `capstone-v1.0` (annotated; message: verdict counts and exit code). Generate the report **at the tag** (`git describe` must print exactly `capstone-v1.0`). Archive `results/report/capstone-v1.0/` (commit or release asset).
2. Branch `cra-fix`. Write `specs/capstone_v1.1.yaml`: S10 goal ≤ 6.5° (so R1 becomes `ok`), and keep S10 limit 12° but add a note that S13 now governs. Record the change and rationale in `specs/CHANGELOG.md` (one paragraph citing R1's numbers). This is the "designer negotiates the spec" step of [Geary §1.2.4].
3. Re-optimize the design in OpticStudio for CRA ≤ 6.5° at the corner (add `RAID` targets at the image for several $H_y$, as in C04 L10 §2.2, with S17's Ø ≤ 16 mm and TTL ≤ 30 mm still active). Save as `designs/capstone.zmx`, commit with the MF value in the message. If you cannot reach 6.5° within S17, stop at the best compromise and write a deviation (C04 L10 practice). Either outcome is valid; the report must show it honestly.
4. Run the report against spec v1.1 and the v1.0 baseline. Then write `python -m zlens.report.diff capstone-v1.0 capstone-v1.1`: it loads both `results.json` files (from the tagged folders) and prints only rows whose class is not `same`, plus verdict changes and spec-version changes.
5. Merge, tag `capstone-v1.1`, regenerate at the tag, update the baseline in its own commit.
6. **CI for the pure stages:** add a workflow (GitHub Actions, GitLab CI or a local `pre-commit` hook) that runs `pytest -m "not opticstudio"` and `evaluate + render + compare` on the committed `results.json` of the latest tag. Optional: a self-hosted Windows runner that also runs `collect`. Get licence clearance first (L07 Task 4) and record the answer.

**Deliverable:** tags `capstone-v1.0`, `capstone-v1.1`; both report folders; `specs/capstone_v1.1.yaml` + `CHANGELOG.md`; the diff table in `notes.md`; CI config file and one green run (screenshot or log excerpt in `notes.md`).
**Check yourself:** exit code at v1.0 includes bit 8 (R1 conflict) and probably bit 1 if your corner CRA is above 6.56° (S13 FAIL). At v1.1 bit 8 is gone. Getting from ~8° to 6.5° at 5.5 mm needs the exit pupil moved from ~39 mm to ~48 mm from the image ($5.5/\tan\theta$), which is usually paid for with a larger rear element and some MTF at the range ends. Your diff should show exactly these trade-offs.

## Task 6 — Tolerance/MC yield section and the final review (Python; data from L07 / C06 L08)
**Goal:** Close the loop to Course 06 without re-running hours of Monte Carlo in every report.
**Steps:**
1. `--with-tolerance PATH` reads an evaluation Parquet (L07 Part B) or the C06 L08 `mc_rows_v2.csv`, plus a small JSON sidecar giving the lens SHA-256 the run was made on, the trial count, the TDE file hash and the criterion definition.
2. **Staleness rule:** if the sidecar's lens hash ≠ current lens hash → section shows "STALE: computed for <tag/hash>", rows S19 / P-rows NOT-EVALUATED, bit 4 set. Test it by running v1.1's report with v1.0's MC data.
3. Yield table per C06 L08 spec rows: $k/n$, $\hat y$, Wilson two-sided 95 % interval, one-sided 95 % lower bound, and the joint yield. Use `stats.wilson` (L07). Add a histogram of the worst MTF row with its threshold.
4. Regression of yields: compare with the baseline yield via interval overlap, not point values (lecture worked example (c)).
5. **Self-review.** Hand the v1.1 `report.html` to yourself a week later (or to a colleague) with only the grading checklist below. Write the reviewer's findings into `notes.md` and fix what you can.

**Deliverable:** yield section in the v1.1 report (or the STALE message with a plan), staleness test, review notes.
**Check yourself (pen & paper):** 455/500 → $\hat y$ = 0.910, Wilson 95 % [0.882, 0.932], one-sided lower bound 0.887; 462/500 → 0.924, [0.897, 0.944], lower bound 0.902. The two revisions are statistically indistinguishable (`same`). Only the second supports "≥ 90 % at 95 % confidence".

## Grading checklist (definition of done for the capstone)

| # | Criterion | Points |
|---|---|---|
| 1 | One command (`python -m zlens.report designs/capstone.zmx [--baseline …]`) produces `results.json`, `report.md`, `report.html`, `fig/` in a folder named by `git describe` | 10 |
| 2 | Spec file covers S1–S19 with limits/goals/reductions/sources; no row silently missing; NOT-EVALUATED has a reason | 10 |
| 3 | Unit tests for evaluate/rules/compare pass on a machine without OpticStudio | 10 |
| 4 | Cross-spec rules R1–R4 implemented with correct numbers; R1 flags S10 vs S13 with the three alternatives; design-based rule checks traced vs predicted S13 shift | 10 |
| 5 | Report contains: prescription, first-order per config, compliance table with margins, MTF vs field per config, distortion + Brown–Conrady residuals, CRA curve with S10/R1 lines, RI, filter AOI, lateral colour, thermal check | 15 |
| 6 | Provenance complete (git describe, dirty refusal, lens/spec/settings/evidence SHA-256, OpticStudio/ZOSPy/Python versions, seeds); evidence staleness detected | 10 |
| 7 | Idempotence: two runs on one commit give identical `metrics` (or a documented, understood exception) | 5 |
| 8 | Regression check with measured tolerances, bit-mask exit codes, three planted regressions documented | 10 |
| 9 | Git: annotated tags v1.0 and v1.1, reports generated at the tags, baseline updates in separate commits, report diff table | 10 |
| 10 | Spot checks against the GUI (lecture §8) recorded in `evidence/spotcheck_<tag>.md` and hashed | 5 |
| 11 | Optional yield section with Wilson bounds and staleness test | +5 bonus |
| 12 | Write-up: does the report change a decision? One paragraph in `notes.md` | 5 |

Pass: ≥ 70 points with items 1, 2, 4 and 6 at full marks. Those four are what make a report trustworthy rather than merely automatic.

## Stretch tasks
1. **Generality test:** run the pipeline on the Course 02 L09 triplet (`designs/L09_T2_triplet.zmx`) with a small `specs/triplet.yaml`. Every capstone-specific assumption that breaks (850 nm, three configs, "FOCUS COMP") should become a spec-file or config parameter, not an `if` in the code.
2. **Sensitivity of the verdicts:** for every PASS row with margin < 5 %, re-evaluate on the 10 worst MC trials (L07). Which rows flip first? Add a "fragile rows" list to the summary.
3. **Calibration hand-off file:** export `calibration_seed.json` (Brown–Conrady $F,k_1,k_2,p_1,p_2,c_u,c_v$ per config, CRA curve, RI curve) with the report's provenance block for the 3D-camera calibration team. Validate it against your calibration code (e.g. OpenCV's model) on a synthetic grid.
4. **PDF output** via pandoc or a headless browser, with the provenance block in the page footer of every page.
5. **ZPL cross-check:** a short macro (L01) that prints EFL, WFNO and the "FOCUS COMP" thickness for configs 1–3. The report compares its text output with `results.json` as an independent oracle.

## Reflection questions
1. Why is it wrong for the collect stage to run Quick Focus or a local optimization "to make sure the lens is in focus"?
2. Spec S10 has a goal of ≤ 8° and S13 implies ≤ 6.56°. Who should resolve this conflict, and what evidence should the report give them?
3. Your regression check says `same` for all metrics, but the provenance shows a different OpticStudio release than the baseline. Is the baseline still valid? What would you do?
4. Why must a missing metric be NOT-EVALUATED and not PASS, even if the requirement "obviously" holds?
5. When is it acceptable to accept a `worse` regression into the baseline?

<details><summary>Answers</summary>

1. The report must describe the file whose hash it prints. Any modification during collection means the analysed lens is not the committed lens, and optimizers can be non-deterministic across core counts (L07). Focus is a design decision: make it in OpticStudio, commit it, then report it.
2. The spec owner (system/calibration engineers together with the optical designer), not the optics script. The report gives R1's numbers ($\arctan(0.5p/\Delta z)$ = 6.56°), the measured CRA and S13 shift of the current design, and the cost of each alternative: tighter CRA needs exit pupil ≈ 48 mm instead of ≈ 39 mm, a larger rear element and some MTF; relaxing S13 to 0.61 px affects calibration stability; reducing the focus budget to 12.3 µm tightens assembly/thermal tolerances.
3. Formally the baseline was made with other software and the comparison is between two variables at once. With all metrics `same`, it is probably fine. Record the release change, re-baseline in a dedicated commit ("re-baseline on OpticStudio <version>, no metric changes beyond tolerance"), and keep the old report for traceability. If metrics changed, investigate with an unchanged lens before attributing anything to the design.
4. A report is evidence. A row without evidence is an untested claim. Defaulting to PASS hides pipeline failures, such as a crashed section or a renamed key, which are exactly what automation is prone to.
5. When the change buys something that matters more and the spec rows still pass with acceptable margin, as with the CRA fix costing range-end MTF. The acceptance is then documented by the separate baseline-update commit, whose message states the trade-off. Never accept it silently or by default.
</details>
