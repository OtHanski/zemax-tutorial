# L05 — Tasks: Optimization strategies and global search

> Work in `work/` inside this lesson folder (e.g. save `work/L05_T3_global_01.zmx`). Commit your designs and a short `work/notes.md` with answers. Keep a **campaign log** (`work/campaign.md`): for every run, file in → file out, algorithm, settings, cores, wall time, MF before/after, one-line comment.
> Estimated time: ~7 h (Tasks 3–4 run in the background; use the time for Task 1)

## Task 1 — Build DLS, OD and a global search (Python)
**Goal:** Understand the optimizers by writing small versions of them.
**Given / specs:** residuals $f(\mathbf x) = (x_1^2-1,\; x_2-0.3,\; 0.3(x_1+x_2))$, MF = Σf².
**Steps:**
1. Implement DLS: finite-difference Jacobian; step from $(J^{\mathsf T}J + \lambda\,\mathrm{diag}(J^{\mathsf T}J))\Delta = -J^{\mathsf T}f$; accept/reject with λ ÷3 / ×4.
2. Run from (0.5, 0), (2, 1), (0.05, −1), (−0.2, 0), (−3, 2). Map the basins: run from a 41×41 grid of starts in [−3, 3]² and colour each start by the minimum reached.
3. Implement a simple derivative-free "orthogonal descent": search along each coordinate direction with step $s$, accept improvements, halve $s$ when no direction improves.
4. Make the MF **noisy/discontinuous**: round every residual to the nearest 0.01 (like a pixelated detector). Compare DLS and your OD from (0.5, 0).
5. Global search: 20 random starts + DLS; count how many reach the global minimum. Then a "hammer": from the local minimum, perturb by Gaussian noise (σ = 0.5), re-optimize, keep if better; 30 trials.
**Deliverable:** `work/optimizers.py`, basin map, results table.
**Check yourself:** local minimum (0.973, 0.195) with Σf² = 0.1366; global (−0.986, 0.357) with Σf² = 0.0396; the basin boundary lies near $x_1 \approx 0$ (slightly shifted by the coupling term). With quantized residuals DLS's finite-difference derivatives are mostly zero or huge and it stalls or jumps erratically; OD still makes progress (to within the quantization). The perturb-and-reoptimize "hammer" escapes the local basin once a perturbation flips the sign of $x_1$.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
res = lambda x: np.array([x[0]**2-1, x[1]-0.3, 0.3*(x[0]+x[1])])
def jac(f, x, h=1e-6):
    f0 = f(x); return np.array([(f(x+h*e)-f0)/h for e in np.eye(len(x))]).T
def dls(x, lam=1e-2, it=100):
    x = np.asarray(x, float)
    for _ in range(it):
        f = res(x); J = jac(res, x); A = J.T@J; g = J.T@f
        while True:
            dx = -np.linalg.solve(A + lam*np.diag(np.diag(A)+1e-12), g)
            if (res(x+dx)**2).sum() < (f**2).sum(): x = x+dx; lam /= 3; break
            lam *= 4
            if lam > 1e8: return x
    return x
```
For the quantized version use a larger finite-difference step (e.g. h = 0.05): it partially restores DLS — the same trick as OpticStudio's pixel interpolation on NSC detectors (Course 05 L06).
</details>

## Task 2 — Many starts, many minima (OpticStudio)
**Goal:** See local minima in a real lens.
**Given / specs:** the NIR receiver lens and MF from L04: `../L04-merit-function-mastery/work/L04_T3_nir_start.zmx` and `work/L04_T3_nir.MF` (EFL 8 mm, F/2, 940 nm band, image height 3.0 mm, TOTR ≤ 16 mm).
**Steps:**
1. Run DLS (Automatic) from the scaled-triplet start. Save as `work/L05_T2_A.zmx`.
2. Create two perturbed starts: (B) reverse the bending of the first element (change signs of $R_1$ and $R_2$ and re-solve focus); (C) move the stop from the middle element to just in front of the first element. Optimize each with DLS.
3. Compare MF, RMS spot per field, CRA, distortion and the lens shapes.
**Deliverable:** three files, a table, one paragraph.
**Check yourself:** at least two of the three runs should end in visibly different forms with different MF values; one may violate a constraint "softly" (check % Contrib). Expect RMS spots of order 5–20 µm for a three-element F/2 lens at this field — not good enough for 3 µm pixels, which motivates Tasks 3–4.

<details><summary>Hints / solution sketch</summary>
If a run produces a lens with an element nearly touching the cover glass or extreme AOIs, add the missing constraints to the MF (and to the `.MF` file) and rerun all three — the MF evolves during a campaign, and every earlier run must be repeated with the final MF for a fair comparison.
</details>

## Task 3 — Global Search for forms (OpticStudio, background run)
**Goal:** Use global search as a form-exploration tool.
**Given / specs:** the best file from Task 2; variables: all radii, all air spaces, glass thicknesses within boundaries. Image-quality block: RMS/Spot/Centroid, GQ 3 rings × 6 arms, 3 fields (0, 0.7, 1.0) for speed.
**Steps:**
1. Version (a) — three elements: run Global Search for a fixed 20–30 minutes (note cores). Keep the 10 saved solutions.
2. Version (b) — four elements: insert a zero-power, 1 mm thick N-BK7 meniscus (R1 = R2 = 20 mm, i.e. nearly zero power) in front of the rear element ("saddle insertion"). Re-run DLS, then Global Search for the same time.
3. Sort all saved solutions into *shape families* (where is the negative element? which elements are menisci? where is the stop?). Sketch each family (Cross-Section screenshots).
4. Local-optimize the best member of each family with a **wavefront** MF and 5 fields.
**Deliverable:** campaign log, a family table (family, best MF, RMS wavefront per field, TOTR, CRA), sketches.
**Check yourself:** Global Search will return several near-duplicate solutions and a few genuinely different forms; the 4-element version should reach a substantially lower MF (often 2× or better) than the best 3-element solution under the same constraints. Results vary between runs — that is expected.

<details><summary>Hints / solution sketch</summary>
If the saved solutions look absurd (huge lenses, elements merging), your boundaries are not active or weights too low — fix the MF, not the solution. Turn off expensive analysis windows while Global Search runs.
</details>

## Task 4 — Hammer with glass substitution (OpticStudio, background run)
**Goal:** Polish the best form, including glass choice.
**Given / specs:** best 4-element solution from Task 3. Glass catalog SCHOTT; allow substitution on all elements, restricted to preferred/standard glasses (exclude obsolete/inquiry glasses); a plastic alternative is out of scope here (Course 04 L07).
**Steps:**
1. Set each glass solve to *Substitute* (restricting to the SCHOTT catalog). Run Hammer for 20–40 minutes.
2. Re-optimize locally with a Contrast MF at Nyquist/2 of a 3.0 µm pixel (83 cycles/mm), keeping your constraint block.
3. Evaluate: FFT MTF (T/S, 5 fields) at 83 and 167 cycles/mm, RMS wavefront, distortion, CRA, TOTR, glass list.
**Deliverable:** final file `work/L05_T4_nir_hammer.zmx`, evaluation table, glass list with a comment on cost/availability.
**Check yourself:** diffraction cutoff at 0.94 µm, F/2 is 532 cycles/mm, so the diffraction-limited MTF at 83 cycles/mm is ≈0.80 and at 167 cycles/mm ≈0.60 — your result must stay below these ceilings. Hammer typically swaps toward high-index, low-dispersion glasses for the positive elements (dispersion matters little over 40 nm, index helps spherical and Petzval).

<details><summary>Hints / solution sketch</summary>
Because the band is narrow (920–960 nm), colour correction is a minor constraint; index and Petzval sum dominate glass choice. Check internal transmittance at 940 nm of any high-index glass you end up with (most are fine in the NIR, unlike in the deep blue).
</details>

## Task 5 — Staging and relaxation (OpticStudio)
**Goal:** Practise two escape techniques on purpose.
**Given / specs:** the Task 2 (A) file.
**Steps:**
1. **Relaxation:** raise the TOTR limit from 16 to 20 mm, optimize; then lower it in steps 19, 18, 17, 16, re-optimizing each time. Compare with a direct optimization at 16 mm.
2. **Criterion staging:** from the same start, compare (i) Contrast MF directly, vs (ii) Spot → Wavefront → Contrast in three stages.
**Deliverable:** table of final MTF at 83 cycles/mm and RMS wavefront for the four end points.
**Check yourself:** the staged/relaxed routes often (not always) end in better minima than the direct routes; when they do not, note it — the landscape decides.

## Reflection questions
1. Why does DLS converge so quickly near a minimum but crawl along a valley?
2. When would you choose OD over DLS for an imaging lens?
3. Global Search returns ten solutions with MFs within 5% of each other. How do you choose?
4. Your three-element design is limited by Petzval sum. Which escape moves are pointless, and which help?
5. What is the risk of letting Hammer substitute glasses freely, and how do you control it?

<details><summary>Answers</summary>

1. Near a minimum the linear (Gauss–Newton) model is accurate and λ→0 gives quadratic-like convergence. Along an ill-conditioned valley the step is limited by the steep cross-valley curvature, so progress along the shallow direction is tiny per cycle.
2. When the MF is noisy or discontinuous: frequent ray failures or vignetting switching during optimization, MTF/encircled-energy operands that are noisy at low sampling, or mixed sequential/NSC models.
3. Group them by form; for the best of each group run a quick sensitivity analysis and Monte Carlo (Course 06); consider manufacturability (element count, thickness, glass cost, aspheres), CRA/telecentricity and mechanical length. Choose the most robust as-built performer.
4. Re-bending, criterion staging and glass swaps among similar indices barely change the Petzval sum. Helpful: higher-index positive glasses, adding a negative element where the marginal ray is low (or a field flattener near the image), splitting positive power into separated groups with a negative between them (triplet logic), or accepting a curved field in the spec.
5. It may choose expensive, hard-to-get, poorly transmitting, soft or stain-prone glasses, or ones with long lead times. Restrict to a preferred-glass list/catalog, add cost/availability judgment afterward, and check transmission at the operating band.
</details>
