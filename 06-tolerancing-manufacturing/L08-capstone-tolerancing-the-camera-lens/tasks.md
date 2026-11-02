# L08 — Tasks: Capstone — tolerancing the camera lens

> Work in `work/` inside this lesson folder. Keep everything under git (`.zmx`, `.tol`, `.MF`, `.TOP`, `.tsc`, reports as `.txt`, scripts, CSVs); one-line commit messages stating what changed and the resulting yield.
> **Input (read-only):** `../../04-machine-vision-camera-lenses/L10-capstone-machine-vision-lens/work/capstone.zmx` (configs 1/2/3 = 0.6/0.8/1.2 m; "FOCUS COMP" thickness; dashboard rows with comments at the top of the MFE) and its `HANDOFF.md`. Never edit it here — copy it.
> **Reused scripts:** `../L01-manufacturing-processes-and-tolerances/work/tolconv.py`, `../L03-sensitivity-and-monte-carlo/work/mcyield.py`, `../L05-opto-mechanics-and-cad-integration/work/stackup.py`, `../L06-drawings-iso10110-and-vendor-handoff/work/iso_translate.py`, `../L07-alignment-and-active-alignment/work/aa_fit.py` and `drift.py`; reused OpticStudio work: `../L07-alignment-and-active-alignment/work/aa_crit.MF` (as a pattern), `../L06-drawings-iso10110-and-vendor-handoff/work/RFQ_package.md` (as a pattern). Import scripts via `sys.path` or copy them into `work/lib/` with a note of the source commit.
> Estimated time: ~20–24 h — Session A: Tasks 1–3; Session B: Tasks 4–5; Session C: Tasks 6–8. The 500-trial Monte Carlo runs overnight.

The as-built specification P1–P11 (and goal G1) is lecture §1.1. Do not change it silently: deviations go into `work/deviations.md` with evidence.

---

## Task 1 — Baseline audit and the as-built specification (OpticStudio + writing)
**Goal:** Know exactly what you received and what you must prove.
**Steps:**
1. Copy `capstone.zmx` to `work/tol_capstone.zmx`. Open it; check that all catalogues load, ray aiming is on, and the hand-off conventions hold (surface comments "L1 front"…"STOP", "FILTER", "COVER"; "FOCUS COMP"; MFE dashboard rows). Note anything missing in `work/notes.md` — you are the receiving engineer, so missing conventions are findings.
2. **Fix all semi-diameters** (Fixed solve, rounded up to 0.05 mm) and set mechanical semi-diameters ≥ clear SD + 0.5 mm (L02 §2, L06). Tolerancing with floating apertures changes vignetting per trial.
3. **Fields for tolerancing** (lecture §7): change the field type to **Object Angle** and enter the 13 fields. First-pass angles $\theta = \arctan(h/f)$ with $f$ = 8 mm, entered as (θx, θy):
   - F1 centre (0, 0); F2/F3 ±x (±22.90°, 0); F4/F5 ±y (0, ±19.47°);
   - F6–F9 AA corners (±22.90°, ±19.47°) → target image (±3.38, ±2.83) mm;
   - F10–F13 S8 corners (±26.19°, ±22.37°) → target image (±3.93, ±3.29) mm.
   Then check with REAX/REAY of the chief rays (config 2) and adjust the angles until each image point is within 0.05 mm of its target (your barrel distortion of a few % will shift the corners by 0.1–0.2 mm at first). Save the angle table in `notes.md`.
4. **Baseline numbers** (nominal, config 1/2/3): MTFT/MTFS at 36.2 lp/mm at all 13 fields; at 72.5 lp/mm on axis and at the AA corners; EFFL; chief-ray REAX/REAY of F1. Put them in a table and compute the **nominal margin** of each block against P2–P4 (minimum row − limit).
5. Write `work/requirements_asbuilt.md`: P1–P11 and G1 from the lecture, each with origin, derivation and verification method (which file/report/script proves it). Add `work/production_concept.md` (½ page): update your L01 Task 4 process plan (`../L01-manufacturing-processes-and-tolerances/work/capstone_process_plan.md`), the barrel concept (L05), the AA concept (L07), volume 10⁴/year.

**Deliverable:** `work/tol_capstone.zmx` (fields changed, apertures fixed), baseline table and margins in `notes.md`, `requirements_asbuilt.md`, `production_concept.md`.
**Check yourself:** the diagonal AA corner is at $r$ = 4.41 mm = 0.8 × 5.51 mm (half-diagonal of 8.45 × 7.07 mm); the S8 corners at 5.13 mm = 0.9 × 5.7 mm. If the nominal minimum MTF at 36.2 lp/mm in config 2 is below ~0.58 (margin < 0.08 over P2) or a range-end block has margin < 0.05, expect Task 5 to fail — read Task 5's branch now and consider talking to "the designer" early.

<details><summary>Hints</summary>

- The as-built limits are 0.85 × S8/S9 (rounded): 0.60 → 0.50 (0.51 rounded down to keep a clean number below the factor), 0.45 → 0.38, 0.35 → 0.30. Write down that this rounding is a choice.
- Your Course 04 design MF uses Real Image Height field numbers; once you change the field type, its field-dependent rows are meaningless. That is fine in the tolerancing copy: you will replace the MF by the station criterion in Task 3. Keep the dashboard rows.
- If your Course 04 file ended with a deviation (e.g. S8 not met at 1.2 m), carry it here: P3 then cannot be met at 90 % and the deviation must be propagated, not hidden.
</details>

## Task 2 — Mechanics and the tolerance model (Python + OpticStudio)
**Goal:** A TDE in which every row has a physical source, a grade, a statistic and a comment.

**Given (capstone barrel, aluminium 6061, assembled at 20 °C):**
- Element bores +0.012/0 mm, element OD 0/−0.010 mm, bore runout Ø0.010 mm to the barrel datum axis; doublet seated as one part.
- Spacer face parallelism 0.004 mm, shoulder squareness 0.003 mm, both over a contact diameter = 0.8 × element OD.
- Spacers ±0.010 mm; CT ±0.025 mm; lens→filter seat in the holder ±0.020 mm.
- CTE: Al 23.6 ppm/K, glass 7.1 ppm/K (use your actual glasses' values from the catalogue in the final version). Operation 0–45 °C, storage −40…+85 °C.
- Holder: tilt ±0.3°, decenter ±0.05 mm (AA lets you buy a cheap holder, L07 Task 4 B). Sensor die tilt in package ±0.1°. Filter: tilt in holder ±0.3°, thickness ±0.05 mm, wedge 1′.
- Shop grade (start): precision — TFRN 3 fr, TIRR 0.5 fr at TWAV 0.6328 µm, wedge drawn as `4/1'` (radial), TIND ±0.0005, TABB ±0.5 %; cemented-element relative decenter ±0.005 mm.

**Steps:**
1. Write `work/capstone_stackup.py` that imports your L05 `stackup.py` and prints, per element of *your* design (ODs from Prescription Data): radial decenter (WC, MC mean, p95) and per-axis TEDX/TEDY (normal ±2σ); spacer tilt, WC and RSS tilt; diametral clearance change at 0 °C, 45 °C, −40 °C, +85 °C.
2. **Thermal conflict:** the given bore has zero minimum clearance. Recompute for a bore +0.008/+0.020 mm. Write the trade (decenter per axis vs clearance at 0 °C and −40 °C) in `notes.md`; choose one and justify (you may revisit it in Task 4).
3. Per-axis wedge from the drawing: `4/1'` radial → per axis ±1′/1.224 = ±0.817′ = **±0.0136°** (use `iso_translate.peraxis_from_radial`).
4. **Insert the AA model** (L07 Task 3): Coordinate Break "AA" after the filter rear surface, in front of the cover glass; the filter→CB thickness is the AA gap (comment "AA GAP"). Leave "FOCUS COMP" in place but it is now a holder dimension (TTHI ±0.020 mm, *no* COMP).
5. Build the TDE (Tolerance Wizard for structure, then edit — L02 §4): blocks as in lecture §3 in this order, each preceded by its STAT operand (uniform for surfaces/CT/wedge, normal for index, Abbe and assembly): surfaces → thicknesses → materials → cementing → barrel (with `MPVT` Rear Mechanical Edge before the holder tilt rows) → holder/filter → sensor → compensators (`COMP` on AA GAP ±0.050 mm; `CPAR` on the AA CB, Par 3 and Par 4, ±0.5°). Delete what has no physical meaning (L02 §4 step 2). Comment every row ("E2 S2 wedge X", "E3-4 bore decenter Y", "Holder tilt X"…).
6. Set the TTHI adjust surfaces from your barrel (front-shoulder drop-in: the following air space absorbs a CT change).
7. Save `work/tol_v1.tol`, and export the TDE as a table (copy cells → `work/tde_v1.tsv`, or read it via ZOS-API; Course 07). Generate `work/tolerance_budget.md` v1 (row, value, unit, grade, source, statistic).

**Deliverable:** `capstone_stackup.py` + output table, thermal-conflict decision, `tol_capstone.zmx` with AA model, `tol_v1.tol`, `tde_v1.tsv`, `tolerance_budget.md` v1.
**Check yourself:** decenter WC 0.016 mm, MC mean ≈ 0.0049 mm, p95 ≈ 0.0094 mm → **±0.0077 mm** per axis; with bore +0.008/+0.020: WC 0.020, p95 ≈ 0.0128 → **±0.0104 mm**. Spacer tilt over 0.8 × OD: Ø12 → 0.024° (WC 0.042°, RSS 0.030°), Ø16 → 0.018° (WC 0.031°, RSS 0.022°). Clearance closure Ø16 mm: 5.3 µm at 0 °C, 15.8 µm at −40 °C; Ø12 mm: 4.0 / 11.9 µm. Expect ~100–150 TDE rows for 6 elements + filter.

<details><summary>Hints / solution sketch</summary>

- Decenter model (L05 Task 1): bore and OD uniform in their bands, lens position uniform in the clearance disc ($r = c\sqrt U$), runout uniform in its disc, random directions; per-axis $T = 2\,r_{95}/\sqrt{-2\ln 0.05} = r_{95}/1.224$.
- Tilt: $\theta = \delta/D_c$; for Ø12, $D_c$ = 9.6 mm: 0.004/9.6 rad = 0.0239°; WC (0.004 + 0.003)/9.6; RSS $\sqrt{0.004^2+0.003^2}/9.6$.
- Thermal: $\Delta(\text{clearance}) = D(\alpha_\text{Al}-\alpha_\text{glass})\Delta T$ = 16 × 16.5 × 10⁻⁶ × 20 = 5.3 µm.
- Doublet: TEDX/TETX over both elements = barrel error; a separate TEDX/TEDY on the *second* element only = cementing error.
- Holder tilt rows with MPVT: in Professional, build the pivot with coordinate breaks and TUTX/TUTY (L05).
- Do not tolerance the AA GAP thickness with TTHI — it is the compensator; the cover-glass thickness and the cover→die gap are sensor-vendor tolerances (small, mostly focus) and can be one TTHI row each.
</details>

## Task 3 — Criteria and AA emulation (OpticStudio)
**Goal:** A criterion that behaves like the station, and an evaluation that measures the real spec.
**Steps:**
1. **Station MF** `work/aa_station_capstone.MF` (pattern: L07 `aa_crit.MF`): `CONF 2`; `MTFT` and `MTFS` at 36.2 lp/mm, polychromatic, for F1–F9; weight 2 on F1, 1 elsewhere, target 1. Choose the MTF sampling: evaluate nominal at two samplings and keep the lower one only if all rows agree within 0.005.
2. **Evaluation MF** `work/eval_capstone.MF` (all weight 0, every row commented `C{config}_F{field:02d}_{T|S}_{freq}`):
   - `CONF 2`: MTFT/MTFS at 36.2 lp/mm, F1–F13 (26 rows); at 72.5 lp/mm, F1 and F6–F9 (10 rows); `EFFL`; `REAX`/`REAY` of F1 chief ray at the image;
   - `CONF 1` and `CONF 3`: MTFT/MTFS at 36.2 lp/mm, F1–F13 (2 × 26 rows);
   - `MINN` rows over each block (comment `C2_MIN36`, `C1_MIN36`, `C3_MIN36`, `C2_MIN72AX`, `C2_MIN72C`) — if MINN is not available in your version, compute minima in Python.
   Total: 88 MTF rows.
3. **Tier-1 settings** (save as `work/tier1.TOP`): Criterion RMS Wavefront, Comp Optimize All (DLS), cycles 3, fields **User Defined/XY** with all 13 fields, configuration 2 (also run once with "All" to see the difference).
4. **Tier-2 settings** (save as `work/tier2.TOP`): Criterion Merit Function = `aa_station_capstone.MF`, Optimize All (DLS), **cycles 3** (fixed, finite station), compensator ranges as in the TDE.
5. **Emulation test** (L07 Task 3 step 5): put a `SAVE` operand after the holder tilt X row; run tier-2 sensitivity on that row only (a small TDE copy). Open the saved MIN/MAX files: the CPAR tilt should be close to equal and opposite to the *effective image-plane* tilt, and the corner MTF recovers substantially but not fully (a tilted lens also sees an asymmetric object field). Do the same for the sensor die tilt row: recovery should be almost complete.
6. **Timing:** run tier-2 Monte Carlo with 10 trials and measure the time per trial. Estimate the 500-trial runtime; adjust sampling/cycles if it exceeds a night.
7. **Evaluation route:** choose (a) a tolerance script (`.tsc`) that reports the `eval_capstone.MF` rows per trial (Ansys KB "How to get any optimization operand value in the tolerance report", lecture Reading; command names from Help → Tolerance Scripts), or (b) saving all trial files and evaluating them with `work/mc_extract.py` (sketch below; Course 07 L03–L05 for the API details). Test the chosen route on the 10-trial run; output `work/mc_rows_test.csv` with one row per trial and one column per comment.

```python
# work/mc_extract.py — sketch; verify property names against Course 07 L04 / ZOSPy docs
import csv, glob, sys
import zospy as zp
zos = zp.ZOS()
oss = zos.connect("standalone")
files = sorted(glob.glob(sys.argv[1]))           # e.g. r"C:\...\work\mc\tol_capstone_MC_T*.ZMX"
out = []
for f in files:
    oss.load(f)
    oss.MFE.LoadMeritFunction(sys.argv[2])       # eval_capstone.MF (absolute path)
    oss.MFE.CalculateMeritFunction()
    rec = {"file": f}
    for i in range(1, oss.MFE.NumberOfOperands + 1):
        op = oss.MFE.GetOperandAt(i)
        if op.Comment:
            rec[op.Comment] = op.Value
    out.append(rec)
with open(sys.argv[3], "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
zos.disconnect()
```

**Deliverable:** `aa_station_capstone.MF`, `eval_capstone.MF`, `tier1.TOP`, `tier2.TOP`, emulation-test notes, timing estimate, `mc_rows_test.csv`.
**Check yourself:** the trial-0 (nominal) row of your CSV must reproduce the Task 1 baseline table to within sampling noise — if not, fields, configurations or sampling differ between the two files. For the pure sensor-tilt row the station criterion should come back to nominal within ~0.005; if the CPARs do not move, your fields are still symmetric or the CB sits after the image surface.

<details><summary>Hints</summary>

- MTF frequencies: ν_N = 1/(2 × 3.45 µm) = 144.9 lp/mm; 36.2 = ν_N/4 (8-pixel fringes), 72.5 = ν_N/2.
- Why the station MF contains config 2 only: the station focuses on one target distance. If you let the compensator see configs 1 and 3, the tolerancer aligns better than the factory does — optimistic (L02 §5.3). Configs 1/3 are *consequences*, evaluated afterwards.
- No CPAR on CB Par 1/2 (decenter): degenerate for MTF with object-space fields (L07 §6.1). Lateral position is boresight, monitored by REAX/REAY.
</details>

## Task 4 — Sensitivity, allocation and cost drivers (Python + OpticStudio)
**Goal:** Find the few rows that matter and buy yield cheaply.

**Part A — warm-up on the lecture's illustrative table (Python).** Write `work/costdrivers.py`:
- input: a TSV with columns `group, n_rows, w_limit, stat (n|u), grade`; cost points 0/1/3 for commercial/precision/high precision;
- output: variance shares (Var(u) = 1/3 uniform, 0.25 × 0.7737 truncated normal), RSS-at-limits, Monte Carlo of $W=\sqrt{W_0^2+\sum (w_iu_i)^2}$ (reuse `mcyield.simulate`), mean, p90, yield at a threshold, total cost points;
- scenario mode: apply multipliers to groups and re-evaluate.
Reproduce the lecture worked example ($W_0$ = 0.050 λ, threshold 0.077 λ).
**Check yourself (Part A):** RSS-at-limits 0.122 λ; A: mean 0.0753, p90 0.0815, yield ≈ 65.8 %, 83 points; top two shares 19.4 % (doublet decenter) and 18.8 % (E2 wedge); D: yield ≈ 98.2 %, 66 points; E: ≈ 90.4 %, 60 points (±0.3 % Monte Carlo noise with 4 × 10⁵ samples).

**Part B — your lens (OpticStudio).**
1. Tier-1 sensitivity (`tier1.TOP`, Mode Sensitivity, MC 0). Save `work/sens_t1_v1.txt`. Transfer the per-row ΔC to `work/sens_v1.tsv`; convert to quadrature contributions $w_i = \sqrt{(C_0+\Delta C_i)^2 - C_0^2}$ (use the larger of the min/max sides).
2. Run `costdrivers.py` on your data: Pareto, cumulative share plot (`work/pareto_v1.png`), and the **S19/P9 check** (no row > 50 % of the variance).
3. Tier-2 sensitivity on the top 15 rows only (a TDE copy) — confirm that the MTF criterion ranks them the same way. Note disagreements.
4. **Diagnose** the top 3 rows physically: which aberration do they create after AA (open the SAVE files: Zernike coma? astigmatism? field tilt that AA removes?), and why that element (ray angles on steep surfaces, [Kidger p. 192]; the doublet, [Kidger pp. 182–183]).
5. **Calibrate the proxy:** from the 10-trial test (Task 3) and a 100-trial tier-2 run, plot the per-trial `C2_MIN36` against the tier-1 RMS wavefront of the same trial (run tier-1 on the saved files or record both via the script). Fit a monotonic line; read the RMS-WFE threshold that corresponds to P2 = 0.50. This threshold makes tier-1 iterations meaningful.
6. **Scenarios:** using the calibrated threshold, evaluate at least four scenarios like the lecture (A all precision; B all high precision; C targeted tighten; D targeted + loosen; plus your own, e.g. "active centring of the doublet replaces its bore decenter by ±0.002 mm" or "bore +0.008/+0.020"). Implement the chosen scenario as `work/tol_v2.tol`.
7. Optional (L03): Inverse Limit on the top 5 rows with the station criterion to see how far each could be loosened.

**Deliverable:** `costdrivers.py`, `sens_t1_v1.txt`, `sens_v1.tsv`, `pareto_v1.png`, `work/cost_drivers.md` (Pareto table, physical diagnosis, proxy calibration plot, scenario table with yield and cost points, decision), `tol_v2.tol`.
**Check yourself:** typically 3–6 rows carry > 50 % of the variance and they are decenters/wedges of the elements nearest the stop or with the steepest surfaces; index, Abbe and most radius rows carry < 1 % each. If the holder or sensor tilt rows are near the top *with* AA compensators active, your AA model is not working (back to Task 3).

<details><summary>Hints</summary>

- Use the side of the sensitivity table that worsens the criterion; for decenters and tilts both sides are ≈ equal (L03 reflection 1).
- Quadrature is a model: it works well for RMS wavefront and poorly for MTF directly — which is why the proxy is calibrated against MTF per trial.
- Cost points are a placeholder for prices. If you have access to the Cost Estimator (L01 Task 5) or a vendor quote, replace them for the elements that change grade.
</details>

## Task 5 — Monte Carlo yield on the real spec (OpticStudio + Python)
**Goal:** The yield claim, with confidence and failure modes.
**Steps:**
1. Tier-2 Monte Carlo with `tol_v2.tol`: N = 500, number of files to save = 500 (route b) or the script route (a). Statistics as in the TDE (STAT rows). Save `work/MC_v2.txt`. Run overnight.
2. Extract `work/mc_rows_v2.csv` (88 MTF columns + minima + EFFL + boresight).
3. Write `work/yield.py`:
   - per-requirement pass flags (P2, P3, P4, P5, P6) and the **joint** pass flag (P2 ∧ P3 ∧ P4);
   - yields with standard error and one-sided 95 % Wilson lower bound;
   - failure-mode Pareto: for failing trials, which row is the minimum (field, T/S, config) — group by "corner T", "corner S", "range end 0.6 m", …;
   - histograms of `C2_MIN36`, `C1_MIN36`, `C3_MIN36`; boresight scatter (REAX, REAY);
   - compensator statistics from `MC_v2.txt` (mean, σ, min, max of AA GAP and both tilts) against P7.
4. Compare with the yield of the plain average-criterion (L03 Task 5): what would you have reported if you had stopped there?
5. **Decide:** if P1 passes, go to Task 6. If not, return to Task 4 with the failure-mode Pareto (cheap fix?) — at most two loops. If P1 still fails within P10, do the **desensitization branch**:
   - list the options with expected effect: mechanics (active centring of the doublet as an internal compensator — L07 §3; tighter bore by selective assembly), design (HYLD re-optimization, L04 §4.1, of a copy `capstone_r1.zmx` with the full Course 04 MF; or a TOLR-based run), or spec (negotiate P3 at the range ends with the system architect, with numbers);
   - implement one; re-verify Course 04 S1–S18 on the new design (re-run your 04/L10 Task 5 evidence script or analyses) and log it in `deviations.md`;
   - repeat Tasks 4–5 for the new design.

**Deliverable:** `MC_v2.txt`, `mc_rows_v2.csv`, `yield.py`, `work/yield_summary.md` (table P1–P7 with value, CI, PASS/FAIL), plots, and — if needed — the desensitization record.
**Check yourself:** `yield.py` on a synthetic test: 465 passes of 500 → 93.0 %, SE 1.14 %, Wilson lower bound 0.909 (PASS); 460/500 → 92.0 %, lower bound 0.898 (FAIL); 93/100 → lower bound 0.876 — the same 93 % with 100 trials proves nothing. Expect the joint yield to be set mainly by one block (often the 1.2 m or 0.6 m range end, or the S8 corners F10–F13, which the station does not see). Expect the AA GAP spread (σ) of order 10–20 µm and tilt compensations of order 0.1–0.3° with a ±0.3° holder; if any tilt trial reaches ±0.5°, the station range is limiting.

<details><summary>Hints / solution sketch</summary>

Wilson bound (one-sided 95 %, $z$ = 1.645):

$$
p_\text{low} = \frac{\hat p + \frac{z^2}{2N} - z\sqrt{\frac{\hat p(1-\hat p)}{N} + \frac{z^2}{4N^2}}}{1 + \frac{z^2}{N}} .
$$

- Number of trials: to separate a true 93 % from 90 % with 95 % one-sided confidence you need $N \gtrsim z^2 \hat p(1-\hat p)/(0.03)^2 \approx 196$; 500 gives room for a lower true yield.
- If the failing trials are dominated by the S8 corners F10–F13 while the AA corners pass, the station recipe (ROIs at 0.8 of the half-diagonal) is not representative of the spec: either add outer ROIs to the station (a production-process change — note it) or accept and document.
- A large *mean* AA GAP (not just spread) means the nominal "FOCUS COMP" design value is not the as-built average focus (e.g. from systematic CT or index offsets); adjust the holder nominal so the glue gap is centred.
</details>

## Task 6 — As-shipped performance: post-cure, thermal, drift (OpticStudio + Python)
**Goal:** Prove P8 and quantify G1.
**Steps:**
1. From the Task 5 files pick the trials nearest the median and the 90th percentile of the *joint minimum margin* (min over all rows of value − limit). Save as `work/unit_med.zmx`, `work/unit_p90.zmx` (compensators frozen).
2. **Post-cure** (L07 Task 5): in each, a TDE with only `TUTX`/`TUTY` on the AA CB ±0.01°, `TUDX`/`TUDY` ±0.002 mm, `TTHI` on AA GAP ±0.002 mm; Comp = None; criterion = station MF; Monte Carlo 200 runs, extract the evaluation rows (same route as Task 5). Save `work/postcure_med.txt`, `work/postcure_p90.txt` and CSVs.
3. **Thermal:** add the Course 04 thermal configurations (0 °C and 45 °C, aluminium barrel via thermal pickups; 03/L09) to `unit_p90.zmx` (keep the AA state from 25 °C). Report best-focus shift (Quick Focus in a copy) and the P2 rows at 0/45 °C without refocusing. Compare with S14 (±5 µm) and with the L07 focus budget.
4. **Drift → depth error:** run `drift.py` (L07) with the boresight change from step 2 (TUDX/TUDY rows, Criterion Boresight or REAX/REAY) and from step 3 (chief-ray shift of F1 between 25 °C and 45 °C). Compare with G1: lateral drift ≤ 0.17 µm keeps the depth error at 1 m below the 0.144 mm depth noise ($\delta z = z^2\delta x/(fb)$).
5. **Calibration check:** for the p90 unit, repeat your Course 04 Brown–Conrady fit (REAY table, $k_1, k_2$) — residual ≤ 0.1 px (S12)? Per-unit calibration absorbs the distortion change, but the *model* must still fit.

**Deliverable:** two unit files, post-cure reports and yields, thermal table, drift table, calibration-fit check, a P8/G1 paragraph in `yield_summary.md`.
**Check yourself:** ±0.01° tilt gives 0.8 µm corner defocus at 4.41 mm — the median unit should lose at most a few hundredths of MTF, the p90 unit more (smaller margin). Lateral TUDX/TUDY does not change MTF but shifts the image 1:1: 0.5 µm → 0.42 mm depth error at 1 m (L07), i.e. G1 is very hard to meet with glue creep alone — that is a finding for the system architect (recalibration strategy, or an athermal/creep-resistant joint), not a lens tolerance.

## Task 7 — Drawings package and test specification (OpticStudio + Python + writing)
**Goal:** Production documents that are the same numbers as the tolerance model (P11).
**Steps:**
1. Export the final TDE (`tol_final.tol`) to `work/tde_final.tsv`. Write `work/make_callouts.py` using `iso_translate.py`: for every element surface, generate 3/A(B) at the drawing wavelength you choose (e.g. 546.07 nm — round *down*), 4/σ radial from per-axis tilts (×1.224), thickness ± from TTHI, material $n_d$/$\nu_d$ tolerances from TIND/TABB; write `work/drawings/callouts.md` (one table per element) and flag any row that has no drawing equivalent (TEDX/TETX → barrel/assembly drawing; holder, sensor → interface drawing).
2. In OpticStudio, create **ISO Element Drawings** (Tolerance tab → Manufacturing Drawings and Data) for each singlet, the cemented doublet and the filter: Reset from TDE, then type 0/–2/, 5/, 6/, coatings (850 nm AR, ≤ 0.5 % per surface — S16 assumption), chamfers. Save PDFs/PNGs to `work/drawings/`.
3. **Consistency check** (P11): `make_callouts.py --check` compares every value you typed/saw on the OpticStudio drawings (transcribe into `drawings/drawing_values.tsv`) with the generated callouts; no drawing value may be looser than the TDE-derived value. Fix and record discrepancies — the ISO drawing shows per-axis tilts as 4/ angles; decide whether that is the radial value you mean (L06 §7).
4. **Assembly & interface summary** `work/drawings/interface.md`: barrel bore/OD fits (Task 2 decision), spacer and retainer specs, holder geometry, nominal glue gap and its tolerance from P7 compensator statistics (mean ± 3σ + margin), AA tilt range, filter seat, keep-out zones, datum scheme.
5. **Test spec** `work/test_spec.md` (L06 §6.1): source/filter (850 nm LED, FWHM ≤ 40 nm), target distance (0.8 m or an equivalent collimator + relay), the 9 ROIs and frequency, the station figure of merit, **limits with guard band** (use the lecture Part 2 method with *your* MC distribution and a measured or assumed σ_m = 0.02), EFL, boresight, sampling plan, golden-sample correlation.
6. Update `RFQ_package.md` (pattern from L06 Task 5) for the capstone: 11 sections, N/A with reasons.

**Deliverable:** `drawings/` (PDF/PNG per element + filter, `callouts.md`, `drawing_values.tsv`, `interface.md`), `make_callouts.py`, `test_spec.md`, `RFQ_package.md`.
**Check yourself:** 3 fr at 632.8 nm = 3.48 fr at 546.07 nm → `3/3.4(0.5)` for TFRN 3, TIRR 0.5 when rounded down; per-axis ±0.0136° → radial 4/1′; guard-band example from the lecture: spec 0.50, mean 0.585, σ 0.045, σ_m 0.02 → test limit 0.50 passes 95.8 % with 0.77 % escapes among shipped units; limit 0.52 passes 90.7 % with 0.19 %.

<details><summary>Hints</summary>

- Guard band in Python: simulate true values ~ your MC distribution (or resample `mc_rows_final.csv` directly — better than a normal fit), add measurement noise, and tabulate pass rate, false rejects (good units failing) and escapes (bad units passing) for several limits.
- The test measures *at the AA ROIs only* — the S8 corners F10–F13 and the 0.6/1.2 m performance are guaranteed by design + statistics, not by test. Say so in the test spec; it is a deliberate decision.
</details>

## Task 8 — Tolerance report and review (writing)
**Goal:** A report that a production engineer, a vendor and a reviewer can audit.
**Steps:**
1. Write `work/tolerance_report.md` with the template below (≤ 10 pages + appendices). Every number must be regenerable from files in `work/` (state the file and the script).
2. Review it with the grading checklist (below) — with a colleague, or yourself after three days. Record findings and responses in `work/review.md`.
3. Leave the Course 04 `HANDOFF.md` untouched (it describes the design revision); write `work/HANDOFF_tolerancing.md` here: file list, which `.TOP`/`.MF`/`.tol` reproduce which result, row-comment conventions (Course 07 L07/L08 scripts will read them), known issues.

### Tolerance report template
```markdown
# Tolerance report — <lens name> rev <x> (design file <capstone.zmx, git hash>)
## 1. Summary (½ page)
- Production concept in one paragraph; yield claim: "<p̂> (95 % lower bound <p_low>) of units meet P2–P4 after AA, N = <N>".
- PASS/FAIL table P1–P11, G1; top-3 risks; decisions requested (e.g. barrel clearance, test limit).
## 2. Inputs
- Design revision, spec references (Course 04 S1–S19 → P1–P11 derivation), production concept, volumes.
## 3. Tolerance model
- Table by block (surfaces, thickness, materials, cementing, barrel, holder/filter, sensor): value, unit, grade, source (shop table / stack-up / datasheet), statistics.
- Modelling decisions: wedge as tilt, pivots (MPVT), TTHI adjust surfaces, AA CB position, thermal clearance decision.
## 4. Compensators and process emulation
- AA model, ranges, cycles, station MF; evidence of the emulation test (Task 3.5).
## 5. Criteria and yield definition
- Tier 1/tier 2; evaluation MF rows; sampling check; proxy calibration.
## 6. Sensitivity results
- Top-15 rows with ΔC and variance share; S19/P9 check; physical diagnosis of the top 3.
## 7. Monte Carlo results
- Yield table with SE and Wilson bound per requirement and joint; histograms; failure-mode Pareto; compensator statistics vs P7; comparison with average-criterion yield.
## 8. As-shipped
- Post-cure (median, p90), thermal, drift → depth error, calibration fit.
## 9. Cost drivers and decisions
- Scenario table (yield, cost points or quotes); chosen scenario and why; rows loosened.
## 10. Production documents
- Drawing list, callout consistency check result, interface summary, test spec with guard band.
## 11. Risks, deviations, open issues
- With owners and proposed actions.
## Appendices
- A: full TDE (tsv) · B: tolerance settings (.TOP) · C: reports (.txt) · D: scripts and versions · E: review log.
```

### Grading checklist (100 points; items marked ★ are must-pass gates)
| # | Item | Points |
|---|---|---|
| 1 ★ | As-built spec P1–P11 written before results; every limit derived (origin + formula) | 8 |
| 2 ★ | Design file untouched; tolerancing on a copy; any design change versioned and re-verified vs S1–S18 | 5 |
| 3 | Fields in object space; 13 fields land within 0.05 mm of targets; apertures fixed | 5 |
| 4 ★ | Every TDE row commented and traceable to a source (shop grade, stack-up, datasheet) | 10 |
| 5 | Wedge/decenter degeneracy, pivots (MPVT), adjust surfaces and STAT choices stated and justified | 6 |
| 6 ★ | AA model: old focus COMP removed; COMP + 2 CPAR with physical ranges; finite cycles; emulation test shown | 10 |
| 7 | Sampling-noise check and runtime estimate documented | 3 |
| 8 | Sensitivity Pareto with variance shares; tier-1 vs tier-2 ranking compared; top-3 diagnosed physically | 8 |
| 9 ★ | Yield computed on the minimum over all 88 rows and 3 distances, with SE and Wilson bound; N ≥ 500 for the claim | 12 |
| 10 | Compensator statistics checked against ranges (P7); glue-gap nominal derived | 4 |
| 11 | Cost-driver scenarios (≥ 4) with yield and cost; decision avoids "everything tighter"; P10 met or deviation | 8 |
| 12 | Post-cure, thermal and drift on real units; G1 discussed honestly | 6 |
| 13 ★ | Drawings generated from the TDE; consistency check passes (P11); assembly-only rows routed to interface drawing | 7 |
| 14 | Test spec with ROIs, focus procedure, guard-banded limits and false-reject/escape numbers | 4 |
| 15 | Report reproducible: every number traceable to a file + script; hand-off notes for Course 07 | 4 |
| | **Total** | **100** |

Pass: ≥ 70 points **and** all ★ gates. Distinction: ≥ 85 and a demonstrated cost reduction versus the all-precision reference at equal or better yield.

**Deliverable:** `tolerance_report.md`, `review.md`, `HANDOFF_tolerancing.md`.

---

## Stretch tasks
1. **Melt and test-plate re-tolerance (L06):** fit the design to a vendor test-plate list and to one melt sheet per glass; re-run Task 5 with TIND/TABB replaced by melt residuals. How much yield does melt matching buy, and is it worth the logistics?
2. **Scripted post-cure on every trial:** extend `mc_extract.py` to apply random post-cure perturbations to the AA CB of each saved trial (several draws per trial) before evaluating — a full as-shipped yield instead of the median/p90 approximation (Course 07 L07).
3. **Station recipe study:** add the S8 corners as AA ROIs with weight 0.5, or switch the station MF to maximise the minimum ROI (`MINN` row as the only weighted row). Compare yield, compensator statistics and runtime.
4. **Projector twin:** sketch how the same flow applies to the Course 05 capstone projection lens (05/L09): what replaces the AA station, what is the criterion (pattern contrast over depth), which errors are calibrated away?

## Reflection questions
1. Your joint yield is 91 % (N = 500) and the Wilson bound is 0.887. The project manager says "91 is more than 90, ship it." What do you reply, and what are your two cheapest ways to make the claim solid?
2. The top sensitivity row is the doublet's bore decenter. List three different ways to reduce its impact (tolerance, process, design) and the cost/risk of each.
3. Why must the station criterion not include the 0.6 m and 1.2 m configurations, even though the spec does?
4. Thermal clearance argued for a looser bore; yield argued for a tighter one. Who should make that decision, and what evidence from your work should they see?
5. Which result from this capstone would change your *design* approach next time (Course 04 L10 → Course 06 L04)?

<details><summary>Answers / guidance</summary>

1. The claim at 95 % confidence is not demonstrated: 91 % ± 1.3 % (SE) is consistent with a true 88–89 %. Cheapest fixes: (a) run more trials only if the point estimate is likely to stay ≥ ~92.5 % (more trials narrow the interval but do not raise the estimate); (b) a targeted tightening of the top failure mode from the Pareto (often a single wedge or decenter), which moves the whole distribution; (c) loosen-elsewhere to keep cost flat. Never "improve" yield by making compensators or cycles unrealistic.
2. Tolerance: tighter bore/OD fit or selective assembly (cost per part, thermal risk). Process: active centring of the doublet in the barrel (L07 §3; adds a station step, but replaces a tight tolerance by a measurement). Design: reduce the doublet's contribution (bending, lower ray angles, HYLD — L04), at some nominal performance or length cost; requires re-verifying the whole Course 04 spec.
3. The station aligns at one target. Letting the tolerancer optimize compensators on all distances gives it information and freedom the factory does not have, so the yield is optimistic (L02 §5.3). The range-end performance is a consequence of the alignment at 0.8 m and must be evaluated, not optimized.
4. A joint decision of mechanical and optical engineering (and quality, for storage-damage risk), owned by whoever owns the product spec. They need: the decenter-vs-clearance numbers (Task 2), the yield of both variants (Task 4/5), the storage temperature requirement and its origin, and the alternatives (compliant mount, active centring) with cost.
5. Typical answers: design-time sensitivity control (HYLD/TOLR or a sensitivity check per design iteration), keeping the stop-adjacent elements' ray angles low, budgeting nominal MTF margin explicitly (≥ 0.08 above the as-built limit), and putting the as-built criterion — not just the nominal spec — into the design review.
</details>
