# L05 — Optimization strategies and global search

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~3 h, tasks ~7 h
> **Prerequisites:** [L04 — Merit function mastery](../L04-merit-function-mastery/), [Course 01 L07 §5 (DLS)](../../01-foundations/L07-solves-variables-first-optimization/), [Course 01 L08 (local minima, lens splitting)](../../01-foundations/L08-landscape-lens-stop-shift-and-splitting/) · **Next:** [L06 — Multi-configuration and zoom](../L06-multi-configuration-and-zoom/)

## Learning objectives
- Explain damped least squares (DLS) at the level of the normal equations, including damping, finite-difference derivatives, scaling and why it converges to the bottom of the *nearest* valley.
- Contrast DLS with Orthogonal Descent (OD) and state when each is the better local optimizer.
- Describe what OpticStudio's Global Search and Hammer optimizers do, how to configure and stop them, and how to combine them with local optimization in a design campaign.
- Apply at least six practical techniques for escaping local minima (perturbing the start, element splitting, saddle-point insertion, constraint relaxation, criterion staging, model glasses and substitution, aspheres).
- Choose a sensible design form for a given F/# and field, and use global search to explore forms rather than to replace thinking.
- Run a reproducible optimization campaign (versioned files, logs, run times) on the NIR receiver lens of L04.

## Reading
- **Core:** [Kidger Foreword, pp. xiii–xvi] — the Imperial College group (Wynne, Hopkins, Welford) and Kidger's 1963 FORTRAN rewrite of their damped-least-squares program; and the **Preface, pp. xvii–xviii**, especially the point that understanding *why* a lens works matters more than hoping the optimizer finds a miracle, and that third-order correctability is necessary but not sufficient.
- **Core:** [Kidger Ch. 7, pp. 139–166] — thin-lens design strategies: shape-dependent vs shape-independent aberrations (§7.4), splitting lenses (§7.3.5), aspheric surfaces (§7.5), monocentric systems and front-to-back symmetry (§7.7). These are the "moves" that take a design from one valley to a better one.
- **Core:** [Geary §8.5, pp. 88–89, Fig. 8.4] — local minima: start at Z, end at B, never see A.
- **Online:** Zemax Community, "What is the difference between the Global and Hammer optimization options?": <https://community.zemax.com/got-a-question-7/what-is-the-difference-between-the-global-and-hammer-optimization-options-414?postid=176>
- **Online:** Zemax Community, "OD vs DLS": <https://community.zemax.com/got-a-question-7/od-vs-dls-464>
- **Online:** Ansys KB (A. Arora), NSC optimization example comparing DLS, OD, Global and Hammer: <https://optics.ansys.com/hc/en-us/articles/42661692035475>
- **Optional:** I. P. Agurok, "Multi-extremum optimization in lens design: navigation through merit function valleys maze", arXiv:1907.08676: <https://arxiv.org/pdf/1907.08676> — valleys, saddle points and networks of minima.

---

## 1. The landscape

A lens with $n$ variables defines an $n$-dimensional landscape whose height is the merit function. Three facts shape everything in this lesson:

1. **It has many minima.** Already a two-element system has several distinct solutions (the two zero-spherical bendings of the cemented achromat in Course 02 L06; front vs rear landscape lens of Course 01 L08). Real lenses with 10–40 variables have hundreds or thousands. Bociort and co-workers mapped the minima of simple systems such as the Cooke triplet and found they form a *network* connected through saddle points (F. Bociort, E. van Driel, A. Serebriakov, "Networks of local minima in optical system optimization", *Optics Letters* 29(2), 2004); Agurok describes the same structure as a maze of valleys (arXiv:1907.08676).
2. **Minima are long, flat valleys, not round bowls.** Many parameter combinations trade against each other (bending one lens vs. the next), so the Hessian is ill-conditioned: steep across the valley, nearly flat along it. Agurok's observation that a "minimum" is really a region several millimetres of radius wide is typical. Practical consequence: two designs with nearly equal MF may look different; choose among them by *tolerance sensitivity* and manufacturability (Course 06).
3. **The landscape is changed by the merit function.** Change the criterion (spot → wavefront), weights, or constraints and minima move, merge or appear. Constraint surfaces create new minima where the unconstrained valley meets a boundary (Agurok).

## 2. Local optimization in depth

### 2.1 Damped least squares
Write the MF as $\Phi = \sum_i w_i f_i^2$ with residuals $f_i = V_i - T_i$ (L04) and variables $\mathbf x$. Linearize: $\mathbf f(\mathbf x+\Delta) \approx \mathbf f + J\Delta$, $J_{ij} = \partial f_i/\partial x_j$. Minimizing the linearized $\Phi$ plus a penalty on the step gives

$$
\big(J^{\mathsf T}WJ + \lambda D\big)\,\Delta = -J^{\mathsf T}W\mathbf f ,
$$

with $W$ the diagonal weight matrix, $D$ a diagonal scaling matrix (often $\mathrm{diag}(J^{\mathsf T}WJ)$, Marquardt's choice) and $\lambda$ the **damping factor**. Small $\lambda$ → Gauss–Newton step (fast near a minimum where the linear model is good); large $\lambda$ → a short step along the scaled steepest descent (safe when nonlinearity is strong). Each cycle adjusts $\lambda$: if the MF fell, reduce it; if it rose, increase it and retry.

Implementation facts worth knowing:
- **Derivatives by finite differences.** One full MF evaluation per variable per cycle (plus the step evaluations). Cost ∝ (#variables) × (#rays in the MF). Lean MFs (L04 §7) matter.
- **Smoothness required.** Ray failures, TIR, vignetting that switches on/off, and pixelated detector data create discontinuities that make derivatives meaningless.
- **Scaling.** A curvature (≈0.05 mm⁻¹) and a 10th-order aspheric coefficient (≈10⁻¹⁰ mm⁻⁹) differ by many orders of magnitude; the damping term's diagonal scaling helps, but normalized aspheres (Q-type, Course 04 L07) and sensible units help more.
- **It goes downhill to the bottom of the nearest valley.** That is a feature (fast, reliable) and the limitation this lesson is about.

**History.** Damped least squares came to lens design in the late 1950s–1960s; at Imperial College the Wynne–Hopkins–Welford group used it, and Kidger rewrote the group's DLS software in FORTRAN on an IBM 7090 in 1963, later porting it to HP desktop computers and commercializing it as SIGMA [Kidger Foreword, pp. xiii–xiv]. It is still the default local optimizer in OpticStudio and in essentially every lens design code.

### 2.2 Orthogonal Descent
OD orthonormalizes the variables and searches along these directions by sampling discrete points, **without derivatives** [Community "OD vs DLS"; Ansys KB Arora]. It is better than DLS when the MF is noisy or discontinuous — non-sequential/illumination merit functions with pixelated detectors (Course 05 L06), merit functions with occasional ray failures, or the first rough cycles of a wild starting point. DLS is generally recommended for imaging systems with smooth MFs and many variables. In tolerancing (Course 06) compensator optimization uses one or two cycles of either.

### 2.3 Running local optimization well
- Optimize → **Optimize!**: choose algorithm, cycles (Automatic, or 1/5/10/50), cores; watch Initial and Current MF; stop manually if progress stalls.
- **Save before every run** (`_o01b`, `_o01a` pattern from Geary, or a git commit). Undo is not a version-control system.
- After each run *look at the lens* (Cross-Section) and at the % Contrib column. A drop in MF caused by a constraint slipping out of bounds is not progress.
- If DLS makes tiny improvements per cycle for many cycles you are crawling along a flat valley: that is the moment to stop and change strategy (§4), not to run 500 more cycles.

## 3. Global optimizers in OpticStudio

Both global tools are in the **Optimize** tab (Global Search, Hammer); availability is edition-dependent — they are included in Professional and Premium.

### 3.1 Global Search
Global Search combines generated/random starting points with local optimization to find regions of low MF across the whole variable space, and **keeps the best solutions (ten)** found so far as separate files, updating them as it runs [Community #414; Ansys KB Arora]. It is a *form-exploration* tool:
- Use it early, after first-order constraints and boundaries are solid (otherwise it happily returns absurd lenses).
- Give it the freedom you want explored (all radii, spacings, possibly model glasses), but keep the MF lean: it will evaluate it many thousands of times.
- Let it run for a fixed time budget (minutes to hours), then inspect the saved solutions as *candidate forms*: group them by shape (where the negative lens sits, which elements are menisci), not by MF alone.
- It is stochastic: two runs will not give the same list. Record settings and run time.

### 3.2 Hammer
Hammer searches **around the current design**, repeatedly perturbing it and re-optimizing, keeping improvements. It is a polishing tool for the final stages, especially effective when glass choice is part of the problem (glasses set to *Substitute*, restricted to a preferred catalog) [Community #414]. Typical use: run Hammer for 10–60 min on the best Global candidate after local optimization; stop when the MF has not improved for a long time.

### 3.3 A design campaign

```mermaid
flowchart LR
  A["Spec & first-order layout"] --> B["Starting point<br/>(thin-lens, patent, sample)"]
  B --> C["Local DLS, spot MF,<br/>solid constraints"]
  C --> D["Global Search<br/>lean MF, time-boxed"]
  D --> E["Pick 2–4 forms by shape"]
  E --> F["Local DLS each,<br/>wavefront MF"]
  F --> G["Hammer with glass substitution"]
  G --> H["Contrast/MTF polishing"]
  H --> I["Tolerance check (Course 06)<br/>→ choose the robust one"]
```

Choosing between final candidates is not done on MF alone: run a quick sensitivity/tolerance analysis (Course 06 L03) and pick the design whose *as-built* performance is best. A slightly worse nominal design with half the sensitivity is almost always the better product.

## 4. Escaping local minima — the designer's toolkit

| Move | What it does | Reference |
|---|---|---|
| **Perturb the starting point** | Change a bending sign, swap the position of a negative element, scan the stop position | Course 01 L08 (stop-shift scan, front vs rear landscape) |
| **Split a lens** | Replace one strongly curved element by two weaker ones; reduces spherical and higher orders, adds variables | [Kidger §7.3.5]; Course 01 L08 |
| **Saddle-point insertion** | Insert a zero-thickness, zero-power meniscus (or a thin plane-parallel plate) and grow it; the design moves across a saddle into a new valley with one more element | Bociort et al. (2004); Agurok |
| **Constraint relaxation ("annealing")** | Temporarily loosen TOTR, thickness or distortion limits, optimize, then tighten progressively | L04 §5 |
| **Criterion staging** | Spot → wavefront → contrast; each stage reshapes the landscape | L04 §3.1 |
| **Model glasses then substitution** | Make glass a continuous variable (index, Abbe number), optimize, then snap to real catalog glasses (Hammer with Substitute, or Glass Substitution tools) | [Kidger Ch. 5, §8.3] (glass maps) |
| **Use symmetry** | Impose front-back symmetry (pickups) to kill odd aberrations, then break it slightly | [Kidger §7.7.2]; Course 02 L10 |
| **Add an asphere** | One well-placed asphere removes a spherical-aberration-type limit (near the stop) or field aberrations (far from the stop) | [Kidger §7.5]; Course 01 L02 |
| **Change the form** | If a triplet can't do F/2 at ±20°, no optimizer will make it; go to a Tessar/double-Gauss/4–6 element form | §5 |

Two attitudes matter more than any tool:
- **Diagnose before you search.** Look at the Seidel diagram (Course 02 L08): which aberration and which surface limits you? If Petzval sum is the limit, no amount of bending will help — you need negative power or a field flattener.
- **Use global search to explore, not to think for you.** Kidger's preface makes the same point: the codes are the tools, understanding is the craft.

## 5. Choosing a form

A rough map for refractive imaging lenses in the visible/NIR (orientation only; modern aspheric and plastic designs push every boundary):

| Semi-field ↓ / Aperture → | Slow (F/8 and slower) | Moderate (F/4–F/5.6) | Fast (F/2–F/2.8) | Very fast (≤ F/1.4) |
|---|---|---|---|---|
| Narrow (≤ 5°) | Singlet / landscape | Cemented doublet | Air-spaced doublet / Petzval | Petzval with flattener, microscope-objective forms |
| Medium (10–25°) | Landscape, periscopic | Cooke triplet, Tessar | Double Gauss, Tessar with asphere, 4–5 element | Double Gauss + extra elements |
| Wide (30–45°) | Symmetric (Hypergon-like) | Retrofocus / reverse telephoto | Retrofocus with aspheres, 6+ elements | specialized |
| Very wide (> 60°) | Fisheye | Fisheye | Fisheye with aspheres | — |

Machine-vision specifics change the picture: sensors want low CRA (or telecentric) images (Course 04 L03), compact M12 lenses use molded plastic aspheres (Course 04 L07), and NIR narrowband light removes most colour correction burden — so for a narrowband 940 nm receiver a fast 4-element form with one or two aspheres is often enough where a broadband visible lens would need 6–7 glass elements.

## 6. In OpticStudio — practical settings and habits

- **Optimize!** (local): DLS default; OD for noisy/NSC; set cores; Automatic cycles.
- **Global Search** and **Hammer**: set number of cores, choose to save best solutions (Global keeps 10), "Stop after" or stop manually. Leave a lean MF and remove expensive operands (MTF, many configurations) during the global stage.
- **Glass substitution**: set glass solve to *Substitute* (optionally restricted to a catalog and to a preferred-glass list), then Hammer. Or use model glasses (Model solve: $n_d$, $V_d$, $\Delta P_{g,F}$ as variables) with `RGLA` or index/Abbe bounds (`MNIN`/`MXIN`/`MNAB`/`MXAB`), then convert to the nearest real glass.
- **Reproducibility**: record OpticStudio version, MF file, variables, run time, cores and random behaviour in `notes.md`; keep the candidate files. Course 07 L07 automates such campaigns via the ZOS-API.
- **Watch for**: designs that "win" by violating something you forgot to constrain (a lens 0.2 mm from the sensor, a 70° AOI surface, glass you cannot buy). Global Search finds every loophole in your MF.

---

## Worked example — a two-valley toy problem

A 2-variable "lens" with residuals $f = (x_1^2 - 1,\; x_2 - 0.3,\; 0.3(x_1 + x_2))$ has two minima:

| Start $(x_1, x_2)$ | DLS result | Σf² |
|---|---|---|
| (0.5, 0) | (0.973, 0.195) | 0.1366 |
| (2, 1) | (0.973, 0.195) | 0.1366 |
| (0.05, −1) | (0.973, 0.195) | 0.1366 |
| (−0.2, 0) | (−0.986, 0.357) | **0.0396** |
| (−3, 2) | (−0.986, 0.357) | **0.0396** |

DLS (Marquardt damping, finite-difference Jacobian) always converges, quickly, to the minimum of the basin it starts in — the sign of $x_1$ at the start decides. A "global search" of 20 random starts in [−3, 3]² followed by DLS finds the deeper minimum in about half the starts (10/20 in the run used for these notes). Real lenses differ in scale (many variables, many basins), not in kind. You will implement this in Task 1 and then watch OpticStudio do the same thing on a real lens.

---

## Key takeaways
- DLS solves $(J^{\mathsf T}WJ + \lambda D)\Delta = -J^{\mathsf T}W\mathbf f$ each cycle; it is fast and reliable but strictly local, and crawls along ill-conditioned valleys.
- OD is derivative-free — better for noisy, discontinuous (NSC) merit functions; DLS is the default for imaging.
- Global Search explores forms (keeps the best 10); Hammer polishes around the current design (excellent with glass substitution). Combine: local → global → local → Hammer.
- Escape local minima by design moves (splitting, saddle insertion, symmetry, aspheres, form change) and by staging criteria/constraints — guided by Seidel diagnosis.
- Pick among near-equal minima by tolerance sensitivity and manufacturability, not by nominal MF.
- Keep a reproducible log of every optimization campaign.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Damping factor λ | Weight on step size in DLS; trades Gauss–Newton speed vs steepest-descent safety |
| Jacobian | Matrix of derivatives of residuals with respect to variables |
| Ill-conditioning | Very different curvatures in different directions; long flat valleys |
| Orthogonal Descent | Derivative-free local optimizer using orthonormalized variable directions |
| Global Search | OpticStudio's global optimizer exploring many starting points, keeps 10 best |
| Hammer | OpticStudio's optimizer that perturbs and re-optimizes around the current design |
| Saddle-point construction | Inserting a null element at a saddle to move into a new valley |
| Model glass | Glass defined by continuous parameters ($n_d$, $V_d$, ΔP) for optimization |
| Substitute solve | Lets Hammer swap catalog glasses |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE 2002: Foreword pp. xiii–xvi; Preface pp. xvii–xviii; Ch. 7, pp. 139–166.
2. [Geary] J. M. Geary, *Introduction to Lens Design*, 2002: §8.5, pp. 88–89.
3. F. Bociort, E. van Driel, A. Serebriakov, "Networks of local minima in optical system optimization," *Optics Letters* 29(2), 189–191 (2004).
4. I. P. Agurok, "Multi-extremum optimization in lens design: navigation through merit function valleys maze," arXiv:1907.08676: <https://arxiv.org/pdf/1907.08676>
5. Zemax Community, "What is the difference between the Global and Hammer optimization options?": <https://community.zemax.com/got-a-question-7/what-is-the-difference-between-the-global-and-hammer-optimization-options-414?postid=176>
6. Zemax Community, "OD vs DLS": <https://community.zemax.com/got-a-question-7/od-vs-dls-464>
7. Ansys Optics KB, A. Arora, NSC optimization with DLS/OD/Global/Hammer: <https://optics.ansys.com/hc/en-us/articles/42661692035475>
