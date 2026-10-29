# L03 — Tasks: Sensitivity, inverse sensitivity and Monte Carlo

> Work in `work/` inside this lesson folder. Start from `../L02-tolerance-data-editor-and-compensators/work/L02_m12_tol.zmx` with the precision TDE (`L02_precision.tol`). Commit your files, saved tolerance reports (`.txt`) and a short `work/notes.md`.
> Estimated time: ~5 h

## Task 1 — A Monte Carlo yield model in Python
**Goal:** Own the statistics before trusting OpticStudio's.
**Steps:**
1. Write `work/mcyield.py` with a function `simulate(W0, w, dist, N, rng)` returning $N$ samples of $W = \sqrt{W_0^2 + \sum_i (w_i u_i)^2}$, where $u_i$ is the normalized error (normal with σ = 1/2 truncated to [−1, 1], or uniform on [−1, 1]).
2. Reproduce the lecture's worked example (a)–(d) with $W_0$ = 0.040, $w$ = [0.030, 0.025, 0.020, 0.015, 0.010] + 20 × [0.005].
3. Plot the cumulative distributions (normal vs uniform) and mark the spec 0.060 and 0.070 waves.
4. Repeat 200 independent Monte Carlo runs of size $N$ = 50, 100, 500 and plot the spread of the estimated 90th percentile and of the yield at 0.055 waves. Compare the yield spread with $\sqrt{p(1-p)/N}$.

**Deliverable:** script + two plots + numbers in `notes.md`.
**Check yourself:** OpticStudio-style RSS estimate 0.0536; all-at-limit 0.0660; normal (untruncated): mean ≈ 0.0476, 90th percentile ≈ 0.053; normal truncated to ±2σ: mean ≈ 0.0461, 90th percentile ≈ 0.050; uniform: 90th percentile ≈ 0.055. Yield at 0.055 waves: ≈ 99.6 % (truncated normal) vs ≈ 91 % (uniform). The spread of the yield estimate follows $\sqrt{p(1-p)/N}$: about ±0.9 % at $N$ = 50 for $p$ ≈ 0.996, but ±3 % at $N$ = 100 for $p$ ≈ 0.9 — Monte Carlo with 20 trials says almost nothing.

<details><summary>Hints</summary>

```python
def u_normal(rng, shape):
    u = rng.normal(0, 0.5, shape)
    bad = np.abs(u) > 1
    while bad.any():
        u[bad] = rng.normal(0, 0.5, bad.sum()); bad = np.abs(u) > 1
    return u
```
For the yield at 0.055 waves the uniform model gives a noticeably lower value than the normal model — a reminder that the distribution choice is a modelling decision you must state in the report.
</details>

## Task 2 — Sensitivity run and your own RSS (OpticStudio + Python)
**Goal:** Read a real sensitivity report and recompute its estimate.
**Steps:**
1. Tolerancing: mode Sensitivity, criterion RMS Wavefront, Comp = Optimize All (DLS), XY-symmetric fields, Monte Carlo runs = 0. Save the report as `work/L03_sens.txt`.
2. Write the top-10 worst offenders in `notes.md` with their compensator values. Classify each: power-type (focus-compensated), decenter/tilt-type (quadratic, asymmetric images), irregularity.
3. Parse the report in Python (copy the sensitivity table into a CSV if parsing is awkward). Compute (a) OpticStudio's RSS estimate (check it matches the report), (b) the contributions $w_i = \sqrt{C_i^2-C_0^2}$ and the all-at-limit physical stack $\sqrt{C_0^2+\sum \bar w_i^2}$.
4. Which tolerances have $\Delta C^+$ and $\Delta C^-$ of opposite sign? What does that tell you about the nominal design?

**Deliverable:** `work/L03_sens.txt`, `work/rss.py`, table in `notes.md`.
**Check yourself:** your (a) must equal the report's estimated change to the printed precision; (b) will be larger. Typically 5–10 tolerances carry > 70 % of $\sum \bar w_i^2$, and element tilts/decenters of the elements next to the stop are among them.

## Task 3 — Monte Carlo, properly (OpticStudio)
**Goal:** A defensible as-built prediction.
**Steps:**
1. Monte Carlo runs = 500, number to save = 20, statistics **Normal**, overlay on: open an FFT MTF vs Field window (72 lp/mm) and a Through-Focus FFT MTF window before running. Criterion RMS Wavefront.
2. Record: nominal, mean, σ, best, worst, the cumulative-probability list, and the compensator statistics. Compare the compensator max with your ±0.10 mm range from L02.
3. Repeat with statistics **Uniform**. Compare the 90 % values.
4. Identify the trial closest to the 90th percentile; open its saved `MC_T00xx` file (or re-run with a fixed seed and more saved files) and diagnose the dominant failure (field asymmetry? defocus? astigmatism?) with Field Curvature and MTF vs field.

**Deliverable:** both reports, overlay screenshots, diagnosis paragraph.
**Check yourself:** uniform statistics give a worse 90 % value than normal (expect several percent to tens of percent worse in RMS wavefront, depending on how dominated the budget is by a few tolerances). Asymmetric MTF across ±x / ±y fields in the overlay is the signature of element tilt/decenter.

## Task 4 — Inverse increment budgeting toward a target yield (OpticStudio)
**Goal:** Allocate a budget, round to shop grades, verify.
**Given:** Course 04 spec for this lens: MTF at 72 lp/mm ≥ 0.30 to 0.9 field. Use as criterion **Diffraction MTF Average at 72 lp/mm** (slower — reduce sampling to the lowest that gives a stable nominal), Optimize All with the image-distance compensator. Target: ≥ 90 % yield.
**Steps:**
1. Start from a deliberately loose "commercial" TDE (L01 table: CT ±0.10, 5 fringes, wedge 0.05 mm ETD → convert to degrees, element decenter ±0.025 mm, tilt ±0.1°, index ±0.001, Abbe ±0.8 %).
2. Choose a total allowed MTF *drop* $B$ (nominal minus 0.30, minus a margin), count tolerances $N$, set $\delta = B/\sqrt N$, run **Inverse Increment**.
3. Round every changed tolerance to the next *standard* grade (commercial/precision/high-precision values from L01). Count how many tolerances ended at each grade.
4. Run Monte Carlo (300 runs). If yield < 90 %, tighten the top-3 worst offenders one grade and repeat; if > 98 %, try loosening the cheapest-to-loosen ones.
5. Record the iteration history (yield vs number of precision/high-precision tolerances).

**Deliverable:** iteration table, final `.tol`, cost discussion in `notes.md`.
**Check yourself:** You should end with most tolerances at commercial/precision and a handful (decenter/tilt of 1–3 elements, perhaps one radius) at precision or high precision. If more than ~5 tolerances need high precision, the design is too sensitive — that is the motivation for L04.

## Task 5 — Yield on the real spec (OpticStudio, stretch)
**Goal:** Avoid the average-criterion trap.
**Steps:**
1. Build a merit function `work/crit_minMTF.zmx`-style MF (save it as `work/crit.MF`) with MTFT and MTFS at 72 lp/mm for fields 0, 0.5, 0.7, 0.9 (±x and ±y for the off-axis ones), weight 1, target 1 — and one row that computes the minimum via operands (e.g. MINN over the MTF rows, if available in your version; otherwise use the full list and post-process).
2. Use "Merit Function" as criterion with this MF loaded, Monte Carlo 300 runs, saved files 300 (or use the ZOS-API in Course 07 to read each trial).
3. Compute the yield as the fraction of trials in which *every* MTF row ≥ 0.30, and compare with the yield from the average-MTF criterion.

**Deliverable:** both yields with their standard errors.
**Check yourself:** the min-over-fields yield is lower — sometimes much lower — than the average-criterion yield. This is the number that belongs in a report.

## Reflection questions
1. Why do decenters and tilts usually show $\Delta C^+ \approx \Delta C^-$, while radius and thickness tolerances can show opposite signs?
2. Your Monte Carlo with 50 trials gives 94 % yield. Your manager wants "≥ 95 %". What do you say?
3. When is uniform statistics the right model, and when is normal?
4. Why can the RSS estimate in the report be *lower* than the Monte Carlo mean for an RMS criterion with a mediocre nominal and many comparable tolerances, yet *higher* for a near-perfect nominal?

<details><summary>Answers</summary>

1. A centred system is symmetric: decentering by +x or −x produces mirror-image systems with the same criterion (even function, quadratic near zero). Radius and thickness errors are not symmetric: one sign may move the design toward a better balance of aberrations (if the nominal was not exactly optimal for this criterion), giving a negative ΔC on one side.
2. With $N$ = 50 the standard error at 94 % is $\sqrt{0.94\cdot0.06/50}$ = 3.4 % — the result is consistent with anything from ~87 % to ~100 %. Run ≥ 500 trials, use statistics matched to the supplier, and compute yield on the actual spec before answering.
3. Uniform when the process only guarantees "inside spec" (parts sorted, process pushed to the limit, unknown supplier), or as a conservative bound. Normal when the process is centred and capable (Cpk well above 1), e.g. melt index data, molded parts after mold correction, good machining. Measured data beat both.
4. For $w_i \ll C_0$ the report's ΔC is ≈ $w_i^2/(2C_0)$. The RSS of $N$ such terms grows like $\sqrt N\,w^2/(2C_0)$, but the true mean degradation (normal ±2σ) grows like $N\,w^2/(8C_0)$ — for more than ~16 comparable tolerances the true value wins and the RSS is optimistic (lecture: 0.0674 vs 0.0748 for 80 tolerances on a 0.060-wave nominal). With a near-perfect nominal ($C_0$ → 0), ΔC ≈ $w_i$ (full contribution at the limit), and the RSS of limit values exceeds what normally distributed errors produce (mean contribution about half) — pessimistic.
</details>
