# L04 — Tasks: Building and editing systems from Python

> Work in your `zlens` repository from L03 (record its path in this lesson's `work/notes.md`). New code goes in `src/zlens/lde.py`, `src/zlens/mfe.py`, `src/zlens/mce.py`, `src/zlens/optimize.py`; scripts in `scripts/`. Generated lens files go in `results/L04/`. Commit after each task.
> Estimated time: ~5 h

---

## Task 1 — Singlet from scratch (Python + hand check)
**Goal:** Build a complete system without touching the GUI and verify it against first-order optics.
**Given / specs:** object at ∞; EPD 20 mm; Angle fields 0, 3.5, 5°; wavelengths F, d, C = 0.4861, 0.5876, 0.6563 µm, d primary; SCHOTT catalogue; N-BK7, $R_1 = 102.7$, $R_2 = -102.7$, $t = 4$ mm; stop on surface 1; comments "L1 front", "L1 rear"; image distance from a marginal-ray-height solve (height 0).
**Steps:**
1. Write `scripts/build_singlet.py` using the patterns in lecture §2–§3. Save to `results/L04/singlet_api.zmx`.
2. Add a zero-weight `EFFL` row (wave = primary) and read its value after `CalculateMeritFunction()`. Read the solved image thickness.
3. Open the file in the GUI: compare System Data (EFL, BFL, F/#) and the LDE.
**Deliverable:** script, saved file, printed numbers.
**Check yourself:** EFFL = 100.03 mm, solved image thickness (paraxial BFD) = 98.70 mm (lecture worked example). Working F/# ≈ 5.0.

<details><summary>Hints</summary>

- New system: `oss.new()` gives object, stop, image. Insert surfaces *before* the image.
- Marginal-ray-height solve: look up `SolveType.MarginalRayHeight` and its `_S_MarginalRayHeight` settings (height, pupil zone) in the Syntax Help.
- If EFFL differs in the 2nd decimal: check that the primary wavelength is d and the material really is N-BK7 (not "BK7" from an older catalogue).
</details>

## Task 2 — Bending study by code (Python)
**Goal:** Use solves, variables and the optimizer from code; reproduce a Course 01/02 result automatically.
**Steps:**
1. Starting from `singlet_api.zmx`: put an `FNumber` solve (5.0) on $R_2$ (this holds f' = 100 mm for EPD 20), make $R_1$ variable.
2. Build the MF with the Wizard from code: RMS spot, centroid, Gaussian quadrature, 3 rings (check which `Ring` index that is by reading back the rows), glass boundaries 2/–/2 mm.
3. Run DLS (automatic). Print start/end MF, $R_1$, $R_2$, shape factor $X = (R_2 + R_1)/(R_2 - R_1)$.
4. Instead of optimizing, sweep $R_1$ from 40 to 300 mm (30 values, log-spaced): for each, set `RadiusCell` value, `CalculateMeritFunction()`, record MF. Plot MF vs $X$; mark the DLS result.
**Deliverable:** `scripts/bending_study.py`, plot `results/L04/bending.png`, numbers.
**Check yourself:** minimum near $X \approx +0.7$ ($R_1 \approx 61$ mm, $R_2 \approx -345$ mm by thin-lens theory for $n = 1.517$); DLS lands at the bottom of your sweep curve. If the sweep curve is jagged, a radius made the solve fail or a ray missed — inspect `oss.get_current_status()`.

<details><summary>Solution sketch</summary>

Thin lens: $c_1 - c_2 = 1/(f(n-1)) = 1/(100 \times 0.5168)$; with $X = (c_1 + c_2)/(c_1 - c_2) = 0.7$: $c_1 = 0.01645$, $R_1 = 60.8$ mm; $c_2 = -0.00290$, $R_2 = -344.5$ mm. The real optimum with thickness, F/5 and the RMS-spot criterion (which balances spherical with defocus) sits close to that.
</details>

## Task 3 — Helper library: find by comment, dashboard reader (Python + pytest)
**Goal:** The helpers every later script will use.
**Steps:**
1. `lde.py`: `surface_by_comment(oss, comment) -> int` (raise on 0 or >1 hits); `get(oss, comment, column)` / `set(oss, comment, column, value)` for Radius/Thickness/Material/Conic/SemiDiameter.
2. `mfe.py`: `dashboard(oss) -> dict[str, float]`: walk the MFE from row 1 until the first row with nonzero weight **or** a `DMFS` row; return `{comment: value}` for zero-weight rows with a comment. Decide how to read a row comment in your version (comment column vs `BLNK` text) and document it.
3. Unit-test the pure logic (comment normalisation, duplicate detection, stopping rule) with fake row objects in `tests/test_helpers.py` — no OpticStudio needed.
4. Integration check: on the Course 04 capstone `designs/capstone.zmx`, print `dashboard(oss)` and the index of "FOCUS COMP", "STOP", "FILTER".
**Deliverable:** modules, tests passing (`pytest -q`), integration printout.
**Check yourself:** the dashboard dict contains the capstone's dashboard items (EFFL, WFNO, TOTR, EXPP, PMAG, DIMX, RAID, RELI — Course 04 L10 §2.2) with values matching the MFE in the GUI after Update.

## Task 4 — Multi-configuration and focus compensator (Python)
**Goal:** MCE manipulation and configuration-aware evaluation.
**Steps:**
1. On a copy of the triplet `designs/L09_T2_triplet.zmx`, change the object to finite: add 3 configurations with `THIC` on surface 0 = 600, 800, 1200 mm (lecture §5).
2. For each configuration: `SetCurrentConfiguration(k)`, run Quick Focus (spot radial, centroid), record the image distance, then restore the original image distance.
3. Compare the Quick-Focus image distances with Newton's equation: $x' = -f'^2/x$ with $x$ the object distance from the front focal point (approximate $x \approx -(d_\text{obj} + \text{small offset})$; use the triplet's front focal distance from Cardinal Points if you want accuracy).
4. Now make the image distance a single variable shared by all configurations (it already is, unless you add a THIC MC row for it) and add the configuration-dependent image-quality block (Wizard, all configurations). Optimize focus only. Report the compromise focus and the per-config RMS spot.
**Deliverable:** `scripts/mc_focus.py`, table of focus per configuration, compromise result.
**Check yourself:** for $f'$ = 50 mm, focus shifts relative to infinity are $\approx f'^2/d$: 4.2 mm (600), 3.1 mm (800), 2.1 mm (1200 mm) — Quick Focus should agree within a few % (principal-plane offsets). The compromise focus lands between the 600 and 1200 mm values, closer to their harmonic mean (in 1/d).

<details><summary>Numbers</summary>

$f'^2/d$: $2500/600 = 4.17$ mm, $2500/800 = 3.13$ mm, $2500/1200 = 2.08$ mm (first-order, measuring $d$ from the front focal point; a more exact value uses $x' = f'^2/(d - f')$-type corrections: $2500/550 = 4.55$, $2500/750 = 3.33$, $2500/1150 = 2.17$ mm if $d$ is measured from the front principal plane). Decide which reference your $d$ uses — that is the point of the exercise.
</details>

## Task 5 — Timed Hammer with logging (Python)
**Goal:** A reusable optimization runner.
**Steps:**
1. `optimize.py`: `run_local(oss, cycles="auto", cores=8) -> dict` and `run_hammer(oss, seconds, cores=8) -> dict` returning start/end MF, wall time, algorithm, variable count (count cells whose solve type is Variable — or record the list before the run), and closing the tool in `finally`.
2. Append each run as a JSON line to `results/L04/runs.jsonl` with git commit and lens SHA-256 (L03 helpers).
3. Run on the triplet: DLS, then Hammer 60 s, then Hammer 300 s. Save each result as `.zmx`.
**Deliverable:** module, `runs.jsonl`, three lens files, a 3-line interpretation (did Hammer find anything better?).
**Check yourself:** MF never increases between runs (each starts from the previous best). If the 300 s Hammer is no better than the 60 s, you're probably in the basin's bottom for this form — the topic of Course 03 L05.

## Stretch task
Write `scripts/rebuild_from_prescription.py` that reads a CSV prescription (surface, radius, thickness, material, conic, comment, stop flag) and builds the lens. Round-trip test: export the capstone's LDE to CSV with your own code, rebuild, and compare EFFL, TOTR and the dashboard to 1e-9 relative.

## Reflection questions
1. Why do the official examples use `RunAndWaitWithTimeout` + `Cancel` for Hammer/Global but `RunAndWaitForCompletion` for local optimization?
2. Give two ways your bending sweep (Task 2 step 4) could silently produce wrong values, and how you'd detect each.
3. Why save the merit function as a separate `.MF` file under git?
4. What would break if you referenced surfaces by index in the capstone report script and a colleague split one element into two?

<details><summary>Answers</summary>

1. Local optimization terminates on its own (convergence or cycle count); Hammer and Global run until stopped, so you must bound them by time.
2. (a) A solve failed or a ray missed → MF evaluates with errors or stale numbers: check status/`RAYE`-equivalents and look for discontinuities. (b) The value was set on the wrong surface (index shift) → assert the comment of the surface you edit. Also: the cell had a solve, so your assignment was overwritten — check the cell's solve type first.
3. It's the specification in executable form; diffs show exactly which constraint changed between design versions, independent of lens-data churn.
4. Every surface index after the split shifts by 2; the script would read and possibly write the wrong surfaces (e.g. move a lens thickness instead of the focus) without any error. Comment-based lookup fails loudly or keeps working.
</details>
