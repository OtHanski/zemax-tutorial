# L06 — Hybrid (Mixed-Mode) Systems and Non-Sequential Optimization

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3.5 h, tasks ~6 h
> **Prerequisites:** [L02](../L02-non-sequential-fundamentals/lecture-notes.md) (NSC basics, ray-count noise), [L04](../L04-illumination-optics-collimators-condensers/lecture-notes.md) (homogenizers, collimators), [Course 03 L04–L05](../../03-image-quality-optimization/L05-optimization-strategies-and-global-search/lecture-notes.md) (merit functions, DLS vs. orthogonal descent) · **Next:** [L07 — Stray light, scattering and ghosts](../L07-stray-light-scattering-ghosts/lecture-notes.md)

## Learning objectives
- Explain what a **Non-Sequential Component (NSC) surface** does in a sequential file, what its **entry and exit ports** are, and which analyses still work in **mixed mode**.
- Convert a sequential lens (or part of one) with **File › Convert to NSC Group**, and check the conversion quantitatively (geometry, transmission, image quality).
- Decide between pure sequential, mixed mode and pure NSC for a given engineering question, and justify the choice.
- Build a non-sequential merit function from **NSDD** (clear / read detectors) and **NSTR** (trace), including total-power, efficiency and uniformity terms, and know where **NSRA** fits.
- Estimate the Monte-Carlo noise of a detector metric and of its finite-difference derivative, and explain why noise breaks DLS; choose ray count, pixel count, pixel interpolation and optimizer accordingly.
- Set up and optimize a parametric illumination component (lenslet homogenizer spacing, aspheric/reflector collimator) for uniformity or collimation with an efficiency constraint.

## Reading
- **Core (online):** Ansys Optics KB, *How to optimize non-sequential optical systems* — pixel interpolation, aggregated detector data (centroid, RMS width) instead of single pixels, orthogonal descent vs. DLS, an LED + freeform (Extended Polynomial) mirror example optimized from ~23 cd to ~254 cd on axis: <https://optics.ansys.com/hc/en-us/articles/42661692035475-How-to-optimize-non-sequential-optical-systems>
- **Core (online):** Ansys Optics KB, *Using the OpticStudio NSC Optimization Wizard* — what the wizard writes into the MFE (always a detector-clearing NSDD first), minimum-flux constraint, spatial-uniformity criterion on the fly's-eye projector sample, Bitmap Wizard: <https://optics.ansys.com/hc/en-us/articles/42661763574419>
- **Core (online):** Ansys Optics KB, article on converting sequential systems to non-sequential mode (Cooke 40° triplet, Double Gauss, off-axis parabola examples; ports, Design Lockdown, Critical Ray Tracer): <https://optics.ansys.com/hc/en-us/articles/42661773116435>
- **Optional (online):** Ansys Optics KB, confocal fluorescence microscope built in sequential + non-sequential mode (a realistic "design sequentially, then convert part of it" workflow): <https://optics.ansys.com/hc/en-us/articles/42712682220691>
- **Optional (online):** Ansys Optics KB, *Fly's eye array homogenizers for digital projector illumination* (uniformity with NSDD pixel −4): <https://optics.ansys.com/hc/en-us/articles/42661744169363>
- **Optional:** [Kidger, Foreword] and Course 03 L05 for the background of damped least squares — this lesson is largely about when its assumptions fail.

The books in our corpus predate practical NSC optimization; this lesson relies on the Ansys documentation and community threads, which are cited inline. When a parameter table matters (NSDD pixel codes!), **the OpticStudio Help topic on NSC operands in your installed release is the authority** — Task 3 makes you verify the codes empirically.

---

## 1. Three ways to trace one system

By now you have seen both tracers:

| | Sequential (LDE) | Non-sequential (NSC Editor) |
|---|---|---|
| Ray path | fixed order of surfaces, one path per ray | any order, splitting, TIR, scatter, multiple hits |
| Primary output | aberrations, wavefront, MTF, spot | flux/irradiance/intensity on detectors |
| Source | fields × pupil (points at infinity or object) | physical sources with power, extent, angular distribution |
| Optimization | smooth, analytic-ish, fast (DLS works beautifully) | Monte-Carlo, noisy, slow |
| Typical runtime per MF evaluation | ms | 0.1 s – minutes |

The third option is **mixed mode**: a sequential file in which a range of surfaces is replaced by one **Non-Sequential Component** surface. Sequential rays reach the NSC surface, enter the non-sequential group at its **entry port**, wander through whatever objects are in the group (prisms with TIR, light pipes, lenslet arrays, corner cubes, CAD parts), leave through the **exit port**, and continue sequentially. The KB conversion article puts it as: rays are traced sequentially outside the group but can follow non-sequential paths inside it [online: KB conversion article].

### 1.1 Anatomy of the NSC surface and its ports

```
 sequential ... ─► [ NSC surface ]  ──────── group of NSC objects ────────  [exit port] ─► next sequential surface
                   entry port at the                                          defined relative to the
                   NSC surface vertex                                          entry port by the NSC surface's
                   (aperture = its semi-dia)                                   exit-location / exit-tilt parameters
```

- The **entry port** sits at the local coordinate system of the NSC surface, with the surface's aperture. Rays outside it never enter.
- The **exit port** is placed by parameters of the NSC surface (exit location X/Y/Z and exit tilts — names as shown in the LDE parameter columns; see the Help topic *How to use NSC with ports*, which the KB article refers to). The thickness of the NSC surface is then measured **from the exit port** to the next sequential surface.
- Inside the group, object positions are relative to the entry port coordinate system (or to a reference object, L02).
- Sequential rays that miss the exit port, or are absorbed, are simply lost to the sequential analyses — just as vignetted rays are.

**What still works in mixed mode:** the sequential analyses (spot, ray fans, MTF, wavefront...) because the rays that leave the exit port are ordinary sequential rays. The KB notes two practical restrictions: the **2-D Layout is blank** — use the 3D Viewer / Shaded Model — and the **stop** concept exists only in the sequential part, so the system stop must be a sequential surface *before* the NSC group (insert a dummy surface and make it the stop if needed) [online: KB conversion article].

**What you must remember:** a sequential ray entering a port is still one ray asking "where do I end up?". It does not split into a reflected and a transmitted child the way an NSC-source ray does with *Split NSC Rays* on (L02 §4); it follows one path through the group (check the Help topic for the exact rule in your release). Ghosts and scatter inside the group are therefore *not* represented in sequential analyses. Energy-type questions (efficiency, ghosts, stray light) belong to NSC **sources and detectors** — which you can also place inside the same group and trace with *Ray Trace Control* (L02) — not to the sequential spot diagram.

### 1.2 When to use which

A practical decision rule:

1. **Is the question about image quality (MTF, distortion, wavefront) and does every ray follow the same order of surfaces?** → pure sequential. Keep it there as long as possible; it is 100–1000× faster to optimize.
2. **Is it an imaging question but one component cannot be described sequentially** (a TIR prism, a total-internal-reflection light pipe, a lenslet array, a roof/corner reflector, an imported CAD window with a lip)? → **mixed mode**: the awkward part goes into an NSC group with ports, you keep sequential optimization of everything else.
3. **Is the question about energy** — efficiency, irradiance uniformity, intensity distributions, ghosts, stray light, extended sources with real angular distributions? → **pure NSC**, often after building and optimizing the imaging parts sequentially and converting them.

For a Zivid-style projector this gives a natural split (cf. L04, L05):

| Sub-system | Mode | Why |
|---|---|---|
| Projection lens (DMD → scene) | sequential (L05) | MTF, distortion, telecentricity |
| Projection lens + DLP **TIR prism** | mixed mode (prism in an NSC group) | the prism has a TIR face; still want sequential MTF through it |
| LED/laser → collector → homogenizer → DMD | pure NSC | uniformity, efficiency, angular fill; extended source |
| Whole projector for stray light / contrast | pure NSC (converted lens + illumination) | ghosts, scatter (L07), capstone L09 |
| Camera lens + cover window ghosts | NSC (or mixed for quick checks) | L07 |

## 2. Converting a sequential design: Convert to NSC Group

**Where:** File tab › **Convert to NSC Group** [online: KB conversion article; KB microscope article]. The dialog lets you choose the **first and last surface** to convert, and has an option to **convert the whole file to non-sequential mode** (all sequential surfaces removed; only the NSC Editor contents remain).

**What it does:** most common sequential surface types (Standard, Even Asphere, Coordinate Break, apertures...) become NSC objects; surfaces without a direct equivalent become **Grid Sag Surface** objects. For a full-file conversion of a focal system it adds Source Ellipse(s) and Detector Rectangle(s) so you can immediately trace; for finite conjugate systems it adds a source DLL, a Slide object and a Detector Color to check imaging [online: KB conversion article].

**Prepare before converting** (KB recommendations, plus experience):

1. **Fix semi-diameters** (change solves to *Fixed*, "U" in the LDE). In NSC, a lens object's clear aperture is a physical edge; an automatic semi-diameter that later changes is meaningless.
2. Make sure the **stop** is a sequential surface that will *stay* sequential (for partial conversion).
3. Consider **Design Lockdown** (Production tools; it turns on ray aiming, converts to physical apertures and object-based fields, fixes semi-diameters, removes solves and rounds thicknesses) — essentially "freeze this design as a manufacturable object".
4. Add mechanical edges: a lens with a 0.5–1 mm flat bevel beyond the clear aperture behaves very differently from an ideal lens once rays can hit the edge (L07).
5. Premium: the **Critical Rayset Generator / Critical Ray Tracer** writes a set of reference rays from the sequential file that you can retrace in the converted model to prove the geometry is identical [online: KB conversion article].

**After converting, verify** — never trust a conversion until you have checked:

- **Geometry:** the NSC Shaded Model overlaid on the sequential 3D layout; vertex positions from the NSC Editor vs. the LDE thicknesses (sum them in a spreadsheet or a Python script).
- **Image quality:** in mixed mode, the sequential spot diagram/MTF *through the NSC group* should match the original to the plotting precision.
- **Transmission:** in pure NSC, power on the image detector will be *lower* than "100 % of unvignetted rays" because NSC applies Fresnel reflection at every uncoated face (and absorption in the bulk if the glass data has it). For an uncoated N-BK7 singlet at 850 nm ($n = 1.5098$), each face transmits $1-R$ with $R = \left(\frac{n-1}{n+1}\right)^2 = 0.0412$; a 4-face doublet with air gap transmits $\approx (1-0.0412)^4 = 0.845$. If you see 100 %, polarization/Fresnel is off; if you see much less, rays are hitting edges or mounts.
- **Reference objects:** the converter places objects relative to the group; if you will later move elements independently (tolerancing, focus), set **reference objects** so that each element moves with the previous one, as done in the KB microscope example.

**Partial conversion pattern.** A useful idiom from the microscope KB article: convert just the lenses you need in a scratch copy, then **copy-paste the converted objects** into your main NSC model. This is how you will bring the L05 projection lens into the L09 capstone projector.

## 3. Non-sequential optimization: the operand toolbox

In NSC, every merit function evaluation is a **ray trace**. The MFE has to (1) clear detectors, (2) trace, (3) read detector results. The order matters because operands are evaluated top to bottom [online: community thread *How to retrieve data from NSDD operand*].

### 3.1 NSDD — Non-Sequential Detector Data

Syntax in the MFE: `NSDD  Surf  Det#  Pix#  Data  #Ignored` [online: KB *How to optimize NSC systems*].

- **Surf** — the surface number of the NSC group: **1 in a pure NSC file**; the NSC surface number in mixed mode.
- **Det#** — detector object number. **Det# = 0 clears all detectors** (the operand then returns 0 and contributes nothing); **a negative number clears only that detector**, e.g. −3 clears detector 3 [online: community *Peak irradiance in merit function*; community *NSDD parameter definition*].
- **Pix#** — a positive integer reads that pixel; zero or negative values return **aggregate statistics** of the whole detector. Codes verified in Ansys/community sources:

| Pix# | Returns | Source |
|---|---|---|
| > 0 | value of that single pixel | community *NSDD parameter definition* |
| 0 | **sum over all pixels** (total flux on the detector, or summed data) | community *Peak irradiance in MF* |
| −4 | **standard deviation** of the pixel data — the usual uniformity metric | community *How to check standard deviation...*; KB fly's-eye article |
| −6, −7 | centroid x, y of the distribution (used with angular data for an intensity centroid) | KB *How to optimize NSC systems* |
| −9 … −13 | RMS widths (second moments) about the centroid — i.e. RMS spot size or angular width; −9/−10/−11 recommended for RMS spot size | community *Nseq: question about NSDD*; Ansys forum reply on RMS spot size in NSC |

  Other negative codes (e.g. peak and minimum pixel values, ray count) exist but **look them up in the Help table of your release** before use — and verify them as in Task 3. Never guess.

- **Data** — 0 = flux, 1 = flux/area (irradiance), 2 = flux/solid angle (intensity, needs a detector with an angular range), 3 = normalized flux (for the bitmap merit function, positive Pix# only), 4/5 = absorbed flux, absorbed flux/area (for volume detectors) [online: community *How to retrieve data from NSDD operand*; *NSDD parameter definition*].
- **#Ignored** — number of pixels at the **edge** of the detector to ignore. Raising it lets you compute uniformity on the flat top of a distribution without the steep edges dominating the standard deviation — a forum user had to set it to 40 to get a meaningful comparison [online: community *How to evaluate the uniformity... using NSDD*].

### 3.2 NSTR — Non-Sequential Trace

`NSTR` launches the ray trace. Its parameters select the NSC surface, which source (0 = all), and the trace flags you know from Ray Trace Control: **split**, **polarization**, **ignore errors** (check the columns in your release; the KB fly's-eye projector wizard example uses Split, Use Polarization and Ignore Errors on [online: KB NSC Optimization Wizard]). The ray count is **not** an NSTR parameter: it is each source's *# Analysis Rays*. The canonical skeleton:

```
 #  Type   Surf Det# Pix# Data #Ign   Target  Weight    comment
 1  NSDD    1    0                                      clear ALL detectors
 2  NSTR    1   (src 0 = all, split, pol, ignore err)    trace
 3  NSDD    1    7    0    0    0      -       0         total flux on det 7 (monitor)
 4  NSDD    1    7   -4    0    0      -       0         std dev of pixel flux (monitor)
 5  ...  arithmetic operands build the actual targets (see §4)
```

Rule: **every** NSC MF begins with clear + trace; if you forget the clear, energy accumulates over successive evaluations and the merit function drifts upward forever. The Optimization Wizard always inserts the clearing NSDD at the top [online: KB NSC Optimization Wizard].

### 3.3 NSRA — single-ray data, and other helpers

**NSRA** is the *non-sequential single ray trace* operand: it traces one ray from a source and returns data about one **segment** of its path (coordinates, direction cosines, optical path length — e.g. data 17 is the optical path [online: community *Optical path length in non-sequential mode*]). It is the NSC analogue of REAY/REAX: deterministic, noise-free, cheap. Its mixed-mode counterpart is **NSST** (a single ray through an NSC group with ports) [online: community *Feature request: Data 40 for NSRA*]. Use NSRA to:

- constrain a chief or edge ray of a source (e.g. "the ray from the LED edge at 60° must hit the reflector, not miss it"),
- target exit directions of a few representative rays in a collimator as a **noise-free pre-optimization**, before switching to detector-based terms.

Look up NSRA's parameter list (source, split, polarization, segment number, data code, ...) in the Help before use; the data codes are numerous.

**Geometry constraints:** the NSC object-position operands **NPZV** (target a Z position), **NPZG/NPZL** (Z greater/less than) keep objects from colliding or flying away [online: community *Focusing and collimating light sources in NSC*]. Put such constraints *before* any wizard-generated block.

**Variables:** in the NSC Editor you make any numeric object parameter or position a variable exactly as in the LDE (Ctrl+Z on the cell, or the solve dialog). Pickup solves work between objects (e.g. array 2 = array 1 radius).

### 3.4 The NSC Optimization Wizard

Optimize tab › Optimization Wizard, NSC mode. It writes the clear/trace block and then operands for criteria such as **spatial uniformity** (target std dev = 0), **RMS angular radius** (collimation), **RMS spot radius**, **minimum flux**, and a **Bitmap** target (one operand per pixel — a 306 × 306 grey image needs 93,636 operands) [online: KB NSC Optimization Wizard]. Good practice: let the wizard build the block, **then read every operand it wrote** and learn the codes from it. Always add the **minimum flux** criterion: the cheapest way to make a detector "perfectly uniform" is to put no light on it.

## 4. Merit functions for illumination

### 4.1 Total power and efficiency

Efficiency $\eta = \Phi_{\text{det}}/\Phi_{\text{src}}$, with $\Phi_{\text{det}}$ = NSDD Pix# 0, Data 0. Total power is the **least noisy** detector number (it averages over all rays reaching the detector: relative noise $\approx \sqrt{(1-\eta)/(\eta N)}$ for $N$ launched rays — binomial statistics). Use it as an inequality (OPGT on the NSDD line, or via a separate operand) rather than as a target to maximize when uniformity is the main goal.

### 4.2 Uniformity metrics

Common definitions over the $M$ pixels of the region of interest with values $E_i$:

$$
\text{CV} = \frac{\sigma_E}{\bar E} = \frac{\sqrt{\tfrac{1}{M}\sum_i (E_i-\bar E)^2}}{\tfrac{1}{M}\sum_i E_i},
\qquad
U_{\min/\max} = \frac{E_{\min}}{E_{\max}},
\qquad
U_{\min/\text{avg}} = \frac{E_{\min}}{\bar E}.
$$

CV (coefficient of variation, "RMS/mean") is what the optimizer should see: it uses every pixel, so it is smooth and relatively noise-robust. Min/max is what the *specification* usually states (projector datasheets, ANSI-style 9- or 13-point measurements), but it is a pair of extreme order statistics — the noisiest numbers you can extract from a Monte-Carlo detector, and biased (noise always lowers min/max). Optimize CV; *report* min/max from a high-ray-count verification trace.

**Build CV from NSDD.** Pix# −4 gives $\sigma$ in the detector's data units; Pix# 0 gives $\sum E_i$. With $M$ pixels (minus ignored edges), $\bar E = \Sigma/M$:

```
 6  NSDD  1  7  -4  1  2          σ of irradiance, 2 edge pixels ignored
 7  NSDD  1  7   0  1  2          Σ of irradiance (same ignore)  [check in your release whether
                                                                 #Ignored also applies to Pix# 0]
 8  CONS  value = M               number of evaluated pixels
 9  DIVI  7  8                    mean
10  DIVI  6  9      target 0  weight 1     → CV
11  NSDD  1  7   0  0  0   with OPGT/ a separate OPGT operand on it  → flux ≥ Φ_min
```

Why normalize? $\sigma$ alone can be reduced by *dimming* the detector; CV is scale-free, so the optimizer cannot cheat that way. (One subtlety to check in Task 3: whether −4 includes zero-valued pixels. If the detector is larger than the lit area, a "uniform" spot with dark surroundings has a large σ — which is exactly why the detector should be sized to the **target region**, with #Ignored trimming the transition band.)

### 4.3 Shape and angle targets

- **Collimation:** RMS angular width (NSDD with an angular detector and an RMS-width pixel code; let the wizard's *RMS Angular Radius* write it) + minimum flux. The KB LED example obtained a 10× gain in on-axis intensity not by targeting the central pixel but by targeting **centroid and RMS width** — aggregated data is better conditioned than single pixels [online: KB *How to optimize NSC systems*].
- **Arbitrary target pattern:** Bitmap Wizard (one operand per pixel; keep the image low-resolution).
- **Rectangular flat-top on a DMD/target:** CV over a detector the size of the active area + flux on the active area ≥ X % + flux on a slightly larger "overfill" detector ≤ Y %.

## 5. Noise, and why it breaks damped least squares

### 5.1 Noise on the merit function

From L02: a pixel that collects $k$ rays has relative error $\approx 1/\sqrt{k}$. If the true irradiance has coefficient of variation $\text{CV}_0$, the **measured** CV is approximately

$$
\text{CV}_{\text{meas}} \approx \sqrt{\text{CV}_0^2 + \frac{1}{k}}, \qquad k = \frac{N_{\text{det}}}{M},
$$

where $N_{\text{det}}$ is the number of rays reaching the $M$ evaluated pixels. Noise adds in quadrature — it **biases** the CV upward *and* makes it fluctuate from trace to trace. An optimizer can only see design improvements larger than both.

### 5.2 Noise on the derivative

DLS (Course 03 L05) builds the Jacobian by finite differences: it perturbs each variable by a small $\delta$, retraces and computes $\partial F/\partial x \approx [F(x+\delta)-F(x)]/\delta$. If each evaluation of $F$ carries independent noise $\sigma_F$, the derivative error is

$$
\sigma_{\partial F/\partial x} \approx \frac{\sqrt{2}\,\sigma_F}{\delta}.
$$

With $\sigma_F = 0.01$ and $\delta = 10^{-3}$ mm, the derivative noise is $\approx 14$ per mm — while a typical true sensitivity of a CV to a lens spacing is $O(0.1\text{–}1)$ per mm. The Jacobian is garbage, the damped step points in a random direction, and DLS "converges" immediately or wanders. Two further problems: (i) pixelation makes the MF **piecewise constant** in the variables — a small move changes no ray's pixel, so the derivative is exactly zero, until it jumps; (ii) noise can create spurious local minima.

### 5.3 The remedies (use all of them)

1. **Orthogonal Descent (OD).** OD does not compute numerical derivatives; it samples along orthogonalized search directions with finite steps, which tolerates noise and discontinuity. Ansys recommends it for NSC; in the KB LED example OD reached 254 cd versus 238 cd for DLS in comparable time, and Hammer (OD) was used only as a final check for local minima [online: KB *How to optimize NSC systems*]. DLS can still work on smooth, high-ray-count problems — try both (community advice, thread *How to use optimization function to collimate light in NSC*).
2. **Pixel Interpolation** (detector Object Properties › Type): each ray's energy is shared among neighbouring pixels according to where it lands, so the MF changes *continuously* when rays move [online: KB *How to optimize NSC systems*]. Turn it on for any detector in a merit function. (Viewer *smoothing* is a display post-process; do not assume NSDD sees it.)
3. **Fewer, larger pixels.** Use the pixel count of the *specification* (e.g. 20 × 12 for a 16:10 DMD region, or the 9/13-point grid), not the visualization resolution (L02 §3).
4. **More rays — and the right kind.** Choose $N$ so that $1/\sqrt{k}$ is a few times below the CV improvement you want to resolve (worked example below). **Sobol sampling** on the source gives better signal-to-noise per ray [online: KB *How to optimize NSC systems*; L02].
5. **Aggregated, smooth operands:** totals, centroids, RMS widths, CV — not single pixels or min/max.
6. **Noise-free pre-optimization:** do the first-order design sequentially (Hui Chen's advice in the collimation thread: design and optimize sequentially first, then convert), or target a handful of **NSRA** rays, then refine on detector data.
7. **Staged ray counts:** optimize at $10^4$–$10^5$ rays to find the basin; re-optimize at $10^6$; verify at $10^7$ with a different seed. If the "optimum" moves when the seed changes, you are fitting noise.
8. **Hardware:** NSC tracing is multi-threaded; LightningTrace is available in the wizard for some detector types and is much faster for rectangle/color/polar data [online: KB NSC Optimization Wizard].

## 6. Parametric illumination components

The optimizer can only change **numbers in the NSC Editor**, so choose objects whose parameters are the design degrees of freedom:

| Component | Object(s) | Typical variables |
|---|---|---|
| Aspheric condenser / collimating lens | **Even Asphere Lens** (or Standard Lens) | front/back radius, conic, a few even-asphere terms, thickness, Z position |
| Reflector cup | **Standard Surface** with conic, material MIRROR (L02/L04) | radius, conic, length/aperture |
| Freeform mirror or lens surface | **Extended Polynomial Surface** (conic base + polynomial terms; the KB example varied 22 terms) | radius, conic, low-order xy terms first |
| Fly's-eye arrays | **Lenslet Array 1/2** (L04) | lenslet radius, array thickness, gap, condenser position |
| Light pipe / taper | **Rectangular Volume** | length, exit half-widths |
| Solid TIR collimator | Part Designer part, imported CAD, or a combination of rotationally symmetric objects (L04 §6) | profile parameters exposed by the part (check what your release exposes as editable object parameters) |

Strategy for a TIR-type collimator: optimize the *central refractive lens* and the *reflector profile* as separate simple objects first (lens + conic mirror "hybrid", as in L04 Task 5), against RMS angular width with a flux constraint; once it works, build the monolithic solid part from those profiles and verify. Always compare the result to the **étendue limit** (L01, L04): a 1 × 1 mm Lambertian LED into a Ø 20 mm exit cannot be collimated better than $\arcsin\sqrt{1/(\pi\cdot 10^2)} = 3.23°$ half-angle; an "optimum" far above that has room left, one at the limit is done — and one *below* it means your detector or metric is wrong.

## 7. In OpticStudio — quick reference

| Task | Where / what |
|---|---|
| Sequential → mixed / pure NSC | File › Convert to NSC Group (first/last surface; "convert file to non-sequential mode" option) |
| Freeze before conversion | Fixed semi-diameters; Design Lockdown (Production tools); Critical Rayset Generator (Premium) |
| Mixed-mode view | 3D Viewer / Shaded Model (2D Layout is blank) |
| Port placement | NSC surface parameters (exit location / tilt); Help: *How to use NSC with ports* |
| NSC MF skeleton | `NSDD 1 0` (clear) → `NSTR` → `NSDD` reads → arithmetic (DIVI, CONS, ...) |
| Uniformity | NSDD Pix# −4 (σ) ÷ mean (Pix# 0 / M); #Ignored for edges |
| Collimation | Wizard "RMS Angular Radius" + minimum flux |
| Deterministic ray constraints | NSRA (pure NSC), NSST (mixed mode) |
| Object position limits | NPZV, NPZG, NPZL |
| Optimizer | Orthogonal Descent; Hammer (OD) for a final basin check |
| Smooth detector | Pixel Interpolation (Object Properties › Type) |
| Source sampling | Sobol sampling (source properties) |

Common pitfalls:
- **No clear at the top** → MF creeps upward each cycle.
- **Detector bigger than the target** → σ dominated by edges; use a target-sized detector or #Ignored.
- **No flux floor** → optimizer "solves" uniformity by vignetting everything.
- **Optimizing min/max** → chasing noise.
- **Ray count changed between "before" and "after"** → the improvement is partly a change of noise bias (§5.1). Compare designs at the same high ray count.
- **Mixed mode used for ghost/efficiency questions** → sequential rays don't split; use NSC sources and detectors.

## Worked example — tuning a fly's-eye homogenizer at 850 nm

Take the L04 fly's-eye design: lenslet focal length $f_{LA} = 6$ mm, condenser $F = 25.92$ mm, DMD active area 6.912 × 3.888 mm, now for an 850 nm NIR LED.

**(a) Starting value of the variable (paraxial).** Two identical plano-convex N-BK7 lenslet arrays, curved face of array 1 toward the source, curved face of array 2 toward the condenser, flat faces facing each other, each array $t = 1.5$ mm thick. N-BK7 at 850 nm: $n = 1.5098$ (Sellmeier). For $f_{LA} = 6$ mm, $R = f_{LA}(n-1) = 6 \times 0.5098 = 3.059$ mm. Array 1 focuses a collimated beam at a *reduced* distance $f_{LA}$ behind its curved vertex. Reduced path to array 2's curved face (where the focus should lie so array 2 acts as a field lens, L04 §4): $t/n + g + t/n = f_{LA}$, hence

$$
g = f_{LA} - \frac{2t}{n} = 6 - \frac{2 \times 1.5}{1.5098} = 4.013\ \text{mm}.
$$

This is the starting air gap; aberrations of the lenslets and the finite source divergence will move the uniformity optimum by a fraction of a millimetre, which is exactly what the optimizer should find.

**(b) Ray budget.** Uniformity spec: CV ≤ 3 % over a 20 × 12 = 240-pixel detector on the DMD. Rays reaching the detector per pixel and resulting noise:

| Rays on detector $N_{\text{det}}$ | $k = N_{\text{det}}/240$ | Noise $1/\sqrt{k}$ | Measured CV if true CV = 3 % |
|---|---|---|---|
| $10^5$ | 417 | 4.9 % | 5.7 % |
| $10^6$ | 4,167 | 1.55 % | 3.4 % |
| $10^7$ | 41,667 | 0.49 % | 3.04 % |

(A quick Monte-Carlo of a perfectly uniform 20 × 12 detector gives CV = 4.9 % at $10^5$ rays and 1.5 % at $10^6$ — the formula holds.) With $10^5$ rays the noise is larger than the effect being optimized; use $10^5$ only to find the basin, $10^6$ to optimize, $10^7$ to verify. If the illumination efficiency to the detector is ~60 %, launch $N \approx N_{\text{det}}/0.6$.

**(c) Why DLS fails here.** At $10^6$ rays, run-to-run σ of the CV is of order 0.1–0.2 % (estimate it yourself in Task 1 by retracing with different seeds). With a finite-difference step $\delta = 1$ µm on the gap, the derivative noise $\sqrt{2}\cdot 0.0015/0.001 \approx 2$ per mm, larger than the true slope near the optimum. OD with steps of ~0.05–0.2 mm sees the real trend.

**(d) Merit function.** Variables: gap $g$, condenser Z position, lenslet radius (pickup array 2 = array 1). MF: clear, trace, CV on the DMD-sized detector (target 0, weight 1), flux on DMD detector ≥ 0.9 × starting flux, NPZG/NPZL keeping the condenser between 20 and 35 mm from array 2.

## Key takeaways
- Mixed mode = sequential file + NSC group with entry/exit ports; it keeps sequential image analyses through components that are not sequential (TIR prisms, rods, lenslet arrays). The stop must be sequential and before the group; use the 3D viewer.
- Sequential rays in mixed mode follow one path: energy questions (efficiency, ghosts, uniformity) need NSC sources and detectors.
- File › Convert to NSC Group converts part or all of a design; fix semi-diameters first, add edges, then **verify** geometry, image quality and transmission (expect Fresnel losses, ~4 % per uncoated face).
- The NSC MF pattern is always: **clear (NSDD Det# 0) → trace (NSTR) → read (NSDD) → arithmetic**. Pix# 0 = total, −4 = σ, −6/−7 centroid, −9…−13 RMS widths; verify any other code in Help.
- Optimize **CV with a flux floor**, report min/max from a high-ray verification run.
- Monte-Carlo noise biases and randomizes the MF and destroys finite-difference derivatives: use OD, pixel interpolation, spec-sized pixels, Sobol sampling, staged ray counts, and noise-free pre-optimization.
- Always check optimized illumination optics against the étendue limit.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Mixed mode | Sequential file containing one or more Non-Sequential Component surfaces |
| NSC surface | LDE surface type that hosts an NSC object group inside a sequential system |
| Entry / exit port | Planes where sequential rays enter and leave an NSC group |
| Convert to NSC Group | File-tab tool turning a surface range (or the whole file) into NSC objects |
| Design Lockdown | Production tool that freezes a design (fixed apertures, no solves, rounded thicknesses) |
| NSDD | Operand that clears detectors or returns detector pixel data/statistics |
| NSTR | Operand that runs an NSC ray trace inside the merit function |
| NSRA / NSST | Single-ray NSC trace operands (pure NSC / mixed mode), noise-free |
| CV | Coefficient of variation σ/mean — the preferred uniformity merit |
| Pixel Interpolation | Detector option distributing a ray's energy over neighbouring pixels for a continuous MF |
| Orthogonal Descent | Derivative-free local optimizer recommended for NSC |
| Sobol sampling | Quasi-random source sampling with lower noise per ray |

## References
1. Ansys Optics KB, *How to optimize non-sequential optical systems* (pixel interpolation, aggregated data, OD vs DLS, LED freeform example) — <https://optics.ansys.com/hc/en-us/articles/42661692035475-How-to-optimize-non-sequential-optical-systems>
2. Ansys Optics KB, *Using the OpticStudio NSC Optimization Wizard* — <https://optics.ansys.com/hc/en-us/articles/42661763574419>
3. Ansys Optics KB, converting sequential systems to non-sequential mode (Convert to NSC Group, ports, Design Lockdown, Critical Ray Tracer) — <https://optics.ansys.com/hc/en-us/articles/42661773116435>
4. Ansys Optics KB, confocal fluorescence microscope in sequential and non-sequential mode (partial conversion, reference objects) — <https://optics.ansys.com/hc/en-us/articles/42712682220691>
5. Ansys Optics KB, *Fly's eye array homogenizers for digital projector illumination* — <https://optics.ansys.com/hc/en-us/articles/42661744169363>
6. Zemax Community, *How to retrieve data from NSDD operand* (clear → trace → read; data codes 0–5) — <https://community.zemax.com/got-a-question-7/how-to-retrieve-data-from-nsdd-operand-1842>
7. Zemax Community, *NSDD parameter definition* (Data 0–3, Det# 0 clears) — <https://community.zemax.com/got-a-question-7/nsdd-parameter-definition-5058>
8. Zemax Community, *Peak irradiance in merit function* (Pix# 0 total flux, Det# −n clears one detector) — <https://community.zemax.com/got-a-question-7/peak-irradiance-in-merit-function-888>
9. Zemax Community, *How to check standard deviation of results from detector viewer* (Pix# −4) — <https://community.zemax.com/got-a-question-7/how-to-check-standard-deviation-of-results-from-detector-viewer-1827>
10. Zemax Community, *How to evaluate the uniformity of the light spot using NSDD operands* (#Ignored edges) — <https://community.zemax.com/got-a-question-7/how-to-evaluate-the-uniformity-of-the-light-spot-using-nsdd-operands-5345>
11. Zemax Community, *Nseq: Question about NSDD operand* (Pix# −9…−13 are RMS widths about the centroid) — <https://community.zemax.com/got-a-question-7/nseq-question-about-nsdd-operand-264>
12. Ansys Innovation Space forum, *RMS spot size in non-sequential method* — <https://innovationspace.ansys.com/forum/forums/reply/397582/>
13. Zemax Community, *Optical path length in non-sequential mode* (NSRA data 17) — <https://community.zemax.com/got-a-question-7/optical-path-length-in-non-sequential-mode-739>
14. Zemax Community, *Feature request: add Data 40 to NSRA* (NSRA pure NSC vs NSST mixed mode) — <https://community.zemax.com/zpl-13/feature-request-add-data-40-to-nsra-to-report-the-face-number-3943>
15. Zemax Community, *Focusing and collimating light sources in NSC with merit functions* (RMS angular radius, minimum flux, NPZV/NPZG/NPZL) — <https://community.zemax.com/got-a-question-7/focusing-and-collimating-light-sources-in-nsc-with-merit-functions-1200>
16. Zemax Community, *How to use optimization function to collimate light in NSC mode* (OD vs DLS; design sequentially first) — <https://community.zemax.com/got-a-question-7/how-to-use-optimization-function-to-collimate-light-in-nsc-mode-412>
17. [Kidger, Foreword] — history and assumptions of damped least squares (background for §5).
