# L03 — Sensitivity, inverse sensitivity and Monte Carlo

> **Course 06 · Tolerancing and manufacturing** · Estimated time: lecture ~2.5 h, tasks ~5 h
> **Prerequisites:** [L02 — Tolerance Data Editor and compensators](../L02-tolerance-data-editor-and-compensators/); [03/L03 — RSS wavefront budgets](../../03-image-quality-optimization/L03-strehl-wavefront-error-depth-of-focus/) · **Next:** [L04 — Desensitization and as-built performance](../L04-desensitization-and-as-built-performance/)

## Learning objectives
- Explain what the Sensitivity, Inverse Limit and Inverse Increment modes compute, and read the sensitivity section of the tolerance report (worst offenders, compensator values).
- Compute an RSS performance estimate by hand from sensitivity data, and explain when it is optimistic or pessimistic (non-linear criteria, RMS-type criteria with a non-zero nominal, correlated tolerances).
- Set up and interpret a Monte Carlo analysis: statistics (normal ±2σ, uniform, parabolic, user), number of trials, saved files, compensator statistics, cumulative probability and yield.
- Estimate the statistical uncertainty of a Monte Carlo yield and choose the number of trials accordingly.
- Use inverse sensitivity to allocate a performance budget across tolerances, and tighten/loosen tolerances iteratively towards a target yield at minimum cost.

## Reading
- **Core (online):** Ansys Optics KB, "Tolerancing a laser beam expander" — the sections on sensitivity, the RSS estimate, Monte Carlo and inverse sensitivity: <https://optics.ansys.com/hc/en-us/articles/42661666289043>
- **Core (online):** Zemax Community, "Monte Carlo statistics" (normal/uniform/parabolic/user distributions, STAT): <https://community.zemax.com/got-a-question-7/monte-carlo-statistics-171>
- **Online:** Zemax Community, "Another way to understand the RSS performance in the tolerance report" — why the RSS estimate assumes independent, normal errors: <https://community.zemax.com/got-a-question-7/another-way-to-understand-the-meaning-root-mean-square-rss-performance-in-tolernace-report-402>
- **Online:** Ansys Optics KB, tolerancing cache and polynomial option (faster reruns): <https://optics.ansys.com/hc/en-us/articles/43071096218899>
- **Online:** Optimax, "How to use manufacturing statistics when tolerancing a lens system" (fabricator view of real error distributions; listing page): <https://optimaxsi-com.dev.webhost.io/techpaper-tags/brandon-light>
- **Optional:** Apollo Optical Systems, "Sensitivity and tolerance analysis in optical systems": <https://www.apollooptical.com/feeds/blog/sensitivity-tolerance-analysis-optics>
- **Background:** [Geary §38.3, pp. 436–440] (the sensitivity output of his singlet example); [Kidger Ch. 7] will be used in L04.

---

## 1. Three ways to ask the question

With a tolerance set (L02) in place, the Tolerancing dialog offers modes on its Set-Up tab:

| Mode | Question it answers | Output |
|---|---|---|
| **Sensitivity** | "If this one tolerance is at its min or max (all others nominal), how much worse is the criterion?" | ΔC per tolerance, worst offenders, RSS estimate |
| **Inverse Limit** | "How large may this one tolerance be before the criterion reaches the limit $C_\text{lim}$?" | new min/max per tolerance |
| **Inverse Increment** | "How large may this one tolerance be before the criterion *changes by* $\delta$?" | new min/max per tolerance |
| **Skip Sensitivity** | go straight to Monte Carlo | — |

Monte Carlo runs after any of these if the number of runs > 0. Recent versions add speed tools (the tolerancing **cache**, "recompute changed" and a polynomial option), which reuse sensitivity data — use "Recompute All" after any lens change.

## 2. Sensitivity analysis

For each tolerance $i$ OpticStudio builds two systems (at min and at max), optimizes the compensators (per the Comp setting), and evaluates the criterion $C_i^-$, $C_i^+$. With nominal criterion $C_0$:

$$
\Delta C_i^\pm = C_i^\pm - C_0 .
$$

The report lists each tolerance's two values, the compensator values that were needed, and then the **worst offenders** (largest $\Delta C$). It is the most useful page of the whole report: typically 5–10 of 80 tolerances cause most of the degradation, and those are where design effort (L04), tighter grades or compensators go.

Interpreting patterns:
- **$\Delta C^+ \approx \Delta C^-$ and both positive** — the criterion is quadratic in this error (decenters and tilts of a centred system: symmetry makes ±x equivalent). Typical.
- **$\Delta C^+$ and $\Delta C^-$ of opposite sign** — the nominal is not at the optimum for this parameter (often a thickness or radius when the design was not fully optimized for the criterion). A negative ΔC means the perturbed lens is *better*: a hint to re-optimize nominal.
- **Large compensator values** — the tolerance mostly causes defocus; it is cheap if focus is adjusted, expensive if not.

### 2.1 The RSS estimate
After the sensitivity table, OpticStudio estimates the combined effect. Following the KB beam-expander article, for each tolerance the squared changes at min and max are averaged (both cannot occur at once), and the results are added in quadrature:

$$
\delta_i^2 = \tfrac{1}{2}\left[(\Delta C_i^+)^2 + (\Delta C_i^-)^2\right], \qquad
\Delta C_\text{RSS} = \sqrt{\sum_i \delta_i^2}, \qquad
C_\text{est} = C_0 + \Delta C_\text{RSS}.
$$

This is the textbook root-sum-square stack-up: if errors are independent and each contributes linearly, the standard deviations add in quadrature. Its implicit assumptions:
1. tolerances are **independent** (not true for, e.g., X and Y decenter of the same element combined into a radial error, or two surfaces polished against the same test plate);
2. each contribution is **small and linear** — but most criteria are *quadratic* in decenters/tilts, and RMS-type criteria are *not additive*;
3. all errors at their **limits** — real parts are distributed inside the limits.

### 2.2 The trap with RMS criteria
RMS wavefront errors from independent aberrations add in quadrature: $W^2 = W_0^2 + \sum_i w_i^2$, where $w_i$ is the RMS wavefront *contributed* by error $i$. But the sensitivity report gives $\Delta C_i = \sqrt{W_0^2 + w_i^2} - W_0$, which, for $w_i \ll W_0$, is $\approx w_i^2/(2W_0)$ — tiny. RSS-ing those changes **underweights the many small contributors** and depends on how good the nominal is. When the criterion is RMS wavefront (or RMS spot), compute your own estimate from the contributions:

$$
w_i = \sqrt{(C_i)^2 - C_0^2}, \qquad W_\text{all-at-limit} = \sqrt{C_0^2 + \sum_i \bar w_i^2}
$$

(with $\bar w_i^2$ the min/max average), and remember that this is the value *if every error sits at its limit* — pessimistic. The worked example shows the size of the effect. Monte Carlo resolves all of this, which is why it is the arbiter.

## 3. Inverse sensitivity — allocating a budget

Instead of asking "how bad is this tolerance?", inverse modes ask "how loose can it be?". Two flavours:

- **Inverse Limit**: each tolerance alone may degrade the criterion up to $C_\text{lim}$. Simple, but it lets *every* tolerance consume the whole budget — the combined result will miss the target.
- **Inverse Increment**: each tolerance alone may change the criterion by $\delta$. If $N$ similar tolerances combine in quadrature, choose $\delta \approx B/\sqrt{N}$ for a total budget $B$.

In OpticStudio the min/max you entered act as starting values and upper bounds: inverse modes tighten tolerances that are too loose but do not loosen ones you entered tightly (verify in the Help for your version) — so start from a moderately loose set. Nothing is rounded — you must round to shop-friendly values afterwards (3 fringes, ±0.02 mm, ±1′…).

A professional workflow:
1. Start from the vendor's commercial grade.
2. Run sensitivity; identify worst offenders.
3. Run inverse increment with $\delta = B/\sqrt{N}$ to find which tolerances must be tightened; round to the next available grade.
4. Re-run sensitivity + Monte Carlo; check yield; iterate.
5. Where a tolerance must be tighter than "precision", consider a design change (L04) or a compensator (L07) instead.

Inverse modes with RMS criteria suffer from the same non-additivity as §2.2: the per-tolerance increment $\delta$ is a change in $C$, not a contribution in quadrature. Treat the result as a ranking aid and let Monte Carlo decide.

## 4. Monte Carlo analysis

Each Monte Carlo trial draws a random value for **every** tolerance at once, builds the perturbed lens, optimizes compensators and evaluates the criterion. After $N$ trials you have a sample of the as-built distribution. Nothing is linearized: OpticStudio ray-traces each trial system fully.

### 4.1 Statistics
- **Normal (default):** Gaussian with the tolerance limits at ±2σ by default ("four standard deviations between minimum and maximum"); the STAT operand can set a different number of σ. Sampled values are kept inside the min/max range (the Help describes how the tails beyond ±2σ are handled in your version). This is the optimistic choice: most parts near nominal, σ = half the range / 2.
- **Uniform:** any value in the range with equal probability — pessimistic, appropriate for parameters selected from a range (sorted parts, "anything inside spec is shipped").
- **Parabolic:** weighted towards the ends of the range — very pessimistic; models a process that is pushed to the limit (e.g. a polisher who stops as soon as the part is in spec).
- **User-defined** (via STAT): measured histograms from your supplier — the best option once production data exist.

The STAT operand in the TDE applies to all following operands until the next STAT; the dialog setting applies when the TDE gives no specific instruction. A common professional choice: uniform for radius/thickness of polished glass (parts are "in spec" rather than centred), normal for index (melt statistics are centred), normal for assembly errors.

### 4.2 How many trials?
The yield $\hat p$ estimated from $N$ trials has standard error

$$
\sigma_{\hat p} = \sqrt{\frac{\hat p(1-\hat p)}{N}} .
$$

For $\hat p$ = 0.90: $N$ = 100 → ±3.0 %; 200 → ±2.1 %; 500 → ±1.3 %; 1000 → ±0.95 %. To distinguish 90 % from 95 % yield reliably you need several hundred trials. Tail percentiles (98 %, 99 %) need more. The KB beam-expander article suggests a heuristic of at least $n^2$ trials for $n$ tolerances; base the number on the precision you need. Monte Carlo runs are cheap compared with designer time — run 500–1000 overnight for final numbers, 50–100 while iterating.

### 4.3 Saved files and overlays
Set "number of MC files to save" (e.g. 20): files `<lens>_MC_T0001.ZMX`… let you inspect individual builds (L02 Task 5). The **overlay** option draws each trial's curve on open analysis windows (MTF vs field, through-focus MTF) — the best picture of as-built spread for a camera lens. Pick specific trials by their criterion in the report (e.g. one at the 90th percentile) and analyse them fully: is the failure astigmatism from a tilted element (asymmetric MTF across the field), or uniform defocus?

### 4.4 Reading the Monte Carlo summary
The report gives the nominal, best, worst, mean and standard deviation of the criterion, the compensator statistics (mean, σ, min, max of each compensator — check against the mechanical range!), and a **cumulative probability** list: "90 % of trials have criterion ≤ x" (for "smaller is better" criteria) or ≥ x (for MTF). The **yield** at a specification is the fraction of trials meeting it — read it off the cumulative list or compute it from the saved per-trial data (Course 07 automates this).

### 4.5 Yield on what?
The criterion is a single number, usually an *average* over fields (and configurations). A spec like S8 of the Course 04 capstone — "MTF ≥ 0.45 at **every** field point 0–0.9, T and S, at 0.6 m and 1.2 m" — is a *minimum* over fields, not an average. An average criterion can pass while one corner fails (typical for tilted elements). Solutions: a merit function criterion with MTFT/MTFS operands per field and a user script that returns the minimum, or post-processing of saved MC files (Course 07 L07). L08 does this for the capstone.

## 5. Correlations, non-normal parts and other honesty checks
- **Compensator range exceeded:** if the MC compensator max exceeds the real adjustment range, the yield is optimistic — limit the compensator in the TDE and rerun.
- **Correlated errors:** surfaces polished against the same test plate share a radius error; elements from the same melt share an index error. Independent sampling understates the systematic part (it shifts every unit the same way — mostly a focus shift, absorbed by the compensator) and overstates the random part.
- **Batch effects:** production parts arrive in lots with offsets; yield per lot can be worse than the average.
- **Sampling noise:** if the nominal criterion changes by more than ~1 % when the ray sampling is doubled, increase sampling before trusting small ΔC values.

## 6. In OpticStudio

- Tolerance tab → **Tolerancing**. Set-Up: Mode (Sensitivity / Inverse Limit / Inverse Increment / Skip Sensitivity), Cache options. Criterion: criterion, sampling, Comp mode and cycles, Fields, Configuration, and — for inverse modes — the limit or increment. Monte Carlo: number of runs, number to save, statistics, overlay. Display: report content (show the compensator values; "show descriptions").
- The report is a text window — save it, and keep it under git next to the `.zmx` and `.tol` files.
- **Quick Sensitivity** (Tolerance tab) is a fast check with paraxial-focus compensation only; useful during design (L04). Earlier versions ignored element tilts/decenters in Quick Sensitivity; recent ones include them (Zemax Community, "Assessing a toleranced system": <https://community.zemax.com/got-a-question-7/assessing-a-toleranced-system-453>).
- For tail-sensitive specs, export the Monte Carlo data (or use a tolerance script/ZOS-API, Course 07) and compute yield on the exact spec.

## Worked example — RSS vs Monte Carlo for an RMS-wavefront criterion

A lens has nominal RMS wavefront $W_0$ = 0.040 waves. Sensitivity analysis (Optimize All compensation) gives 25 tolerances whose RMS wavefront *contributions* at their limits are $w_i$ = 0.030, 0.025, 0.020, 0.015, 0.010 waves, and twenty at 0.005 waves. Assume symmetric (quadratic) behaviour, so $\Delta C^+ = \Delta C^-$. Specification: $W \le 0.070$ waves (Maréchal, 03/L03).

**(a) What the report shows.** $\Delta C_i = \sqrt{W_0^2+w_i^2} - W_0$ = 0.0100, 0.0072, 0.0047, 0.0027, 0.0012 and 20 × 0.0003. OpticStudio-style RSS: $\Delta C_\text{RSS}$ = 0.0136 → estimated performance **0.0536** waves. Note how the twenty 0.005-wave contributors almost vanish (0.0003 each).

**(b) All errors at their limits, combined physically.** $W = \sqrt{0.040^2 + \sum w_i^2}$ = **0.0660** waves — the pessimistic stack-up.

**(c) Monte Carlo (normal, ±2σ).** Each error contributes $w_i z_i/2$ with $z_i \sim N(0,1)$, so $\langle W^2\rangle = W_0^2 + \sum w_i^2/4$ → RMS-mean 0.0478 waves. A 200 000-trial numpy simulation gives mean 0.0476, median 0.0467, 90th percentile **0.0532**, 98th percentile 0.0590; yield 99.9 % at 0.070 waves and 98.5 % at 0.060. If the normal distribution is *truncated* at the limits (values beyond ±2σ redrawn), the spread shrinks noticeably: mean 0.0461, 90th percentile 0.0502, 98th percentile 0.0530 — another modelling detail worth knowing for your OpticStudio version.

**(d) Monte Carlo (uniform).** Mean 0.0501, 90th percentile 0.0549, yield 99.9 % at 0.060.

**Lessons.** The report's RSS estimate (0.0536) happens to land near the normal-statistics 90th percentile here, but for the wrong reasons (it squashes small contributors and assumes limits). It is not even consistently pessimistic: with a mediocre nominal (0.060 waves) and 80 equal contributors of 0.010 waves, the report-style estimate is 0.0674 while the Monte Carlo mean is 0.0748 (normal) — optimistic; with a near-perfect nominal (0.005 waves) and the same tolerances it is 0.0603 against a Monte Carlo mean of 0.0448 — pessimistic. The all-at-limit stack (0.066) is far too pessimistic for normal statistics. The distribution assumption shifts the 90th percentile by ~3 %. Only Monte Carlo — with statistics that reflect your supplier — gives a defensible yield. All numbers were computed with `python3` (Task 1 reproduces them).

**(e) How many trials?** To quote "yield ≥ 98 %" with ±1 % (1σ) confidence you need $N \ge 0.98\cdot0.02/0.01^2 \approx 196$ trials; for ±0.5 %, ~800.

## Key takeaways
- Sensitivity ranks tolerances; worst offenders are where the money and the design effort go.
- The RSS estimate is a quick heuristic built on independence, linearity and limit values; RMS-type criteria break its additivity.
- Inverse Increment with $\delta \approx B/\sqrt{N}$ is a practical allocation tool — then round to shop grades and verify with Monte Carlo.
- Monte Carlo is the arbiter: choose statistics that match the supplier, enough trials for the precision you claim, and inspect saved trials and compensator statistics.
- Yield must be computed on the actual specification (min over fields, all configurations), not on a convenient average.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Sensitivity | Change in criterion when one tolerance is at its min or max |
| Worst offenders | Tolerances with the largest criterion change |
| RSS estimate | Root-sum-square combination of sensitivity changes, added to the nominal |
| Inverse Limit / Increment | Modes that compute tolerance values producing a given criterion / criterion change |
| Monte Carlo trial | One randomly perturbed system with compensators optimized |
| Cumulative probability | Fraction of trials better than a given criterion value |
| Yield | Fraction of builds meeting the specification |
| STAT | TDE operand setting the statistical distribution for the operands that follow |
| Standard error of yield | $\sqrt{p(1-p)/N}$ — statistical uncertainty of a Monte Carlo yield estimate |

## References
1. Ansys Optics KB, "Tolerancing a laser beam expander: overview of the OpticStudio workflow": <https://optics.ansys.com/hc/en-us/articles/42661666289043>
2. Zemax Community, "Monte Carlo statistics": <https://community.zemax.com/got-a-question-7/monte-carlo-statistics-171>
3. Zemax Community, "STAT command vs Monte Carlo settings": <https://community.zemax.com/got-a-question-7/stat-command-vs-monte-carlo-settings-4596>
4. Zemax Community, "Another way to understand the RSS performance in the tolerance report": <https://community.zemax.com/got-a-question-7/another-way-to-understand-the-meaning-root-mean-square-rss-performance-in-tolernace-report-402>
5. Zemax Community, "Assessing a toleranced system" (Quick Sensitivity): <https://community.zemax.com/got-a-question-7/assessing-a-toleranced-system-453>
6. Ansys Optics KB, "How to use the tolerancing cache": <https://optics.ansys.com/hc/en-us/articles/43071096218899>
7. Optimax, techpapers by B. Light incl. "How to use manufacturing statistics when tolerancing a lens system": <https://optimaxsi-com.dev.webhost.io/techpaper-tags/brandon-light>
8. Apollo Optical Systems, "Sensitivity and tolerance analysis in optical systems": <https://www.apollooptical.com/feeds/blog/sensitivity-tolerance-analysis-optics>
9. [Geary §38.3, pp. 436–440].
