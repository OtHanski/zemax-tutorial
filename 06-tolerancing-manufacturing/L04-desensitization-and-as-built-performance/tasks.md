# L04 — Tasks: Desensitization and as-built performance

> Work in `work/` inside this lesson folder. Use the same tolerance model (`../L02-tolerance-data-editor-and-compensators/work/L02_precision.tol`, adapted per design) and the same Tolerancing settings for every comparison — save them once as `work/L04_compare.TOP` and reuse.
> Estimated time: ~6 h (Task 4 and 5 run unattended for a while)

## Task 1 — The decenter–coma rule (Python)
**Goal:** Verify the lecture's formula and get a feel for its size.
**Steps:**
1. On a 801 × 801 unit-pupil grid compute $\Delta W = W_{040}(|\boldsymbol\rho+\boldsymbol\varepsilon|^4 - \rho^4)$, remove piston, x/y tilt and defocus by least squares, and compute the RMS. Compare with $4|W_{040}|\varepsilon/(3\sqrt8)$ for $\varepsilon$ = 0.001…0.3 and $W_{040}$ = 1 wave.
2. Where does the linear formula deviate by more than 5 %? What aberration appears at second order?
3. Tabulate the decenter $\delta$ (mm) that produces 0.01 waves RMS for $h$ = 1.67 mm and $W_{040}$ = 1, 3, 10 waves.

**Deliverable:** `work/decenter_coma.py`, plot, table.
**Check yourself:** the linear rule holds to < 0.5 % for ε ≤ 0.05 and reaches 5 % only near ε ≈ 0.19 (realistic decenters are ε < 0.02); $\delta$ for 0.01 waves: 0.0354 mm ($W_{040}$ = 1), 0.0118 mm (3), 0.0035 mm (10). Second-order terms ($\propto\varepsilon^2$): astigmatism and defocus (defocus removed by the fit, astigmatism remains).

<details><summary>Hints</summary>

$\delta = 0.01\cdot3\sqrt8\,h/(4W_{040})$. Expand $(\rho^2+2\varepsilon\rho\cos\theta+\varepsilon^2)^2$: the $\varepsilon^2$ terms are $4\varepsilon^2\rho^2\cos^2\theta + 2\varepsilon^2\rho^2$ → astigmatism + defocus.
</details>

## Task 2 — Read the sensitivity map before tolerancing (OpticStudio + Python)
**Goal:** Predict worst offenders from the Seidel table and check against L03.
**Given:** `../L02-tolerance-data-editor-and-compensators/work/L02_m12_tol.zmx` and your L03 sensitivity report `../L03-sensitivity-and-monte-carlo/work/L03_sens.txt`.
**Steps:**
1. Analyze → Aberrations → **Seidel Coefficients** (text). Copy the per-surface $W_{040}$ and $W_{131}$ (waves) and the marginal ray heights (from a paraxial ray trace or the Seidel output) into a Python table.
2. Predict for each element the RMS axial coma for element decenter 0.010 mm, and for each surface the RMS coma for surface decenter 0.005 mm (lecture §1.1).
3. Rank your predictions and compare with the TEDX/TEDY and TSDX/TSTX ranking in the L03 report (on-axis field, or the RMS wavefront change). Discuss agreements and misses.

**Deliverable:** prediction-vs-report table in `notes.md`.
**Check yourself:** the ranking of element decenters should largely agree (the rule is first-order and on-axis only). Misses typically involve elements far from the stop, where field-dependent effects (coma → astigmatism) dominate, and elements whose decenter mainly moves the image (boresight) rather than blurring it.

## Task 3 — Cemented vs air-spaced doublet (OpticStudio)
**Goal:** Test Kidger's claim on a lens you can design in an hour.
**Given / specs:** EFL 100 mm, F/4 (EPD 25 mm), field 0, 1.4, 2° (object at infinity), wavelengths F, d, C; glasses N-BK7 (crown) + N-SF5 (flint), crown first. Fixed semi-diameters 13 mm after optimization.
**Steps:**
1. Design A: cemented doublet (3 radii + crown CT 6 mm, flint CT 3 mm). Optimize RMS wavefront (default MF, EFL = 100, image distance as variable).
2. Design B: air-spaced doublet (4 radii, air gap ≥ 0.5 mm variable). Optimize the same MF. B should be nominally better.
3. Apply the same TDE to both: TFRN 3 fr, TIRR 0.5 fr, TTHI ±0.05 (glass) / ±0.02 (air), TEDX/Y ±0.02 mm per element, TETX/Y ±0.05° per element, TIND ±0.0005, TABB ±0.5 %; COMP on image distance ±1 mm. For A, the two elements of the cemented pair can still decenter relative to each other (cementing error) — use ±0.005 mm for that relative decenter and ±0.02 mm for the pair in the barrel.
4. Sensitivity + Monte Carlo (300, normal), criterion RMS wavefront (XY-symmetric fields).
5. Tabulate nominal, RSS estimate, MC mean, 90 % for both; list the worst offenders of B.

**Deliverable:** `work/L04_T3_cemented.zmx`, `work/L04_T3_airspaced.zmx`, comparison table.
**Check yourself:** B wins nominally; A typically wins (or ties) as built, and B's worst offenders include the central air space and the decenter of one element relative to the other — exactly Kidger's point. If B still wins as built, check that you gave A's internal cementing decenter a realistic (small) value.

## Task 4 — HYLD weight scan (OpticStudio)
**Goal:** Map the trade between nominal and as-built performance.
**Given:** your Course 04 M12 design `L02_m12_tol.zmx` (re-enable the variables you removed — use a copy, `work/L04_hyld.zmx`, with the original Course 04 merit function).
**Steps:**
1. In the Optimization Wizard, enable **Improve Manufacturing Yield** with weight 0 (reference), 3, 10, 30; for each weight re-optimize (DLS to convergence + 10 min Hammer), save `work/L04_hyld_w{w}.zmx`.
2. For each file: nominal MTF at 72 lp/mm (0, 0.7, 0.9 field), the spec checks from Course 04 (TOTR, CRA, distortion), and a Monte Carlo (200 runs, the L03 final TDE, criterion RMS wavefront or MTF average at 72 lp/mm).
3. Plot nominal criterion and MC 90 % criterion vs HYLD weight. Identify the knee.

**Deliverable:** four files, plot, recommendation.
**Check yourself:** nominal degrades slowly with weight; the 90 % value improves then saturates (or degrades if the nominal suffers too much). Constraint violations (CRA, TOTR) appearing at high weight mean the HYLD term is overpowering your design constraints — reduce the weight.

## Task 5 — Choosing among Global Search candidates by as-built performance (OpticStudio)
**Goal:** Practise the professional selection step.
**Steps:**
1. From the M12 design, run **Global Search** for 30–60 min with the full merit function (variables re-enabled) and keep the 5 best saved files.
2. Apply the identical TDE and tolerancing settings (`L04_compare.TOP`) to all five. Monte Carlo 200 runs each.
3. Rank by MC 90 % criterion and by yield at the Course 04 MTF spec. Is the best nominal also the best as built?
4. For the winner and the loser, compare their Seidel $|W_{040}|$ sums $\sum_j |W_{040,j}|$ and their maximum angle of incidence (RAID over surfaces, marginal ray at full field). Do these simple metrics predict the ranking?

**Deliverable:** table + 1 paragraph in `notes.md`.
**Check yourself:** it is common that the nominal ranking and the as-built ranking differ; a lower $\sum|W_{040}|$ and lower max AOI usually go with better as-built results, but not always (tilt sensitivity, air-space sensitivity).

## Stretch tasks
1. **TOLR:** save your tolerancing setup as `TOLR001.TOP` in `{Zemax}/Configs`, add `TOLR` (file 1, data 2) with modest weight to the M12 merit function, remove insignificant tolerances, and run 5–10 DLS cycles. Compare with the HYLD result of Task 4 at equal nominal performance.
2. **Perturbed multi-config:** take the top-3 worst offenders (e.g. element decenters), build 4 extra configurations with ± perturbations in x via coordinate breaks (keep a focus variable per configuration), and re-optimize. Compare Monte Carlo yield with the original.

## Reflection questions
1. Why does a wedge (surface decenter) tolerance often matter more than an element decenter tolerance for a strongly bent meniscus element?
2. Why do field-flattener elements near the image usually tolerate decenter well but not tilt?
3. A desensitized design has 5 % lower nominal MTF but 20 % better 90th-percentile MTF. Under which business conditions would you still choose the more sensitive design?
4. Why is it dangerous to optimize only the RSS estimate (TOLR data 0) without the nominal term?

<details><summary>Answers</summary>

1. A strongly bent meniscus has large, opposite-sign $W_{040}$ on its two surfaces that nearly cancel (small element total). Element decenter moves both together and sees only the small total; a wedge shifts one surface relative to the other and exposes the large individual contribution.
2. Near the image the beam for each field point is small (small $h$ per field relative to the element), so a lateral shift mostly moves the image slightly (distortion/boresight) and causes little blur. A tilt changes the effective thickness and incidence angle across the field and tilts the image surface — producing asymmetric field curvature across the sensor.
3. Very low volumes with individual alignment/testing (each unit is adjusted anyway), when a hard nominal spec cannot be met otherwise, or when the sensitive parameters can be compensated cheaply in production (e.g. active alignment absorbs the dominant errors, L07). For mass production with fixed processes, the robust design normally wins.
4. The optimizer can reduce the estimated *change* by making the nominal bad — a lens that is uniformly poor is insensitive. Always optimize nominal + change (data 2) or keep the nominal criterion in the merit function.
</details>
