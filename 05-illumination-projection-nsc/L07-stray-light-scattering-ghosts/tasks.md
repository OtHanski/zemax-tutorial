# L07 — Tasks: Stray Light — Scattering, Ghosts and Baffling

> Work in `work/` inside this lesson folder (e.g. save `work/L07_T2_brdf.zmx`). Commit your designs, scripts and a short `work/notes.md` with answers.
> Estimated time: ~6–7 h (Task 1 ≈ 1 h, Task 2 ≈ 1.5 h, Task 3 ≈ 2 h, Task 4 ≈ 1.5 h, Task 5 ≈ 1 h)

All OpticStudio tasks use a single wavelength of **0.85 µm** unless stated. Always record the number of traced rays next to every number you report (L02/L06: Monte-Carlo noise).

## Task 1 — A stray-light calculator (Python)
**Goal:** Build `work/straylight.py`, a small library you will reuse in the capstone (L09) together with `../L01-radiometry-photometry-etendue/work/radiometry.py`.

**Given / specs:** functions to implement (numpy/scipy):
1. `fresnel_R(n1, n2)` — normal-incidence reflectance.
2. `ghost_budget(R_list)` — returns the list of all double-bounce pairs $(i,j,R_iR_j)$ sorted by strength and their sum.
3. `abg_bsdf(x, A, B, g)` and `abg_tis(A, B, g)` — TIS at normal incidence by numerical integration over $s = \sin\theta_s \in [0,1]$; check against the closed form $\pi A\ln(1+1/B)$ for $g = 2$.
4. `tis_roughness(sigma_nm, lam_nm, theta_deg=0)` — $(4\pi\sigma_h\cos\theta/\lambda)^2$.
5. `lambert_into_cone(rho, alpha_deg)` — $\rho\sin^2\alpha$.
6. `fringe_metrics(s, eps, p_z_mm)` — modulation factor $1/(1+s)$, phase error $\arcsin\varepsilon$, depth error $\delta z$.
7. `fit_abg(x, bsdf)` — fit $A, B, g$ to data (log-space least squares).

**Steps:**
1. Implement and unit-test against the lecture worked example (all values listed there).
2. Fit this synthetic BRDF (normal incidence, $|x| = \sin\theta_s$):

   | $|x|$ | 0.001 | 0.003 | 0.01 | 0.03 | 0.1 | 0.3 | 0.7 |
   |---|---|---|---|---|---|---|---|
   | BSDF (sr⁻¹) | 0.1471 | 0.1311 | 0.06649 | 0.01489 | 0.001869 | 2.615 × 10⁻⁴ | 5.699 × 10⁻⁵ |

   First by the "engineer's method" from the Ansys ABg-fitting article (straight line through the large-$|x|$ points on log–log → $g$ and $A$; then $B = A/\text{BSDF}(x\to0)$), then by nonlinear least squares in log space. Compute the TIS of both fits.
3. Plot BSDF vs $|x|$ on log–log axes with the data and both fits; mark the knee $B^{1/g}$.

**Deliverable:** `work/straylight.py`, the plot, a table of fitted parameters and TIS in `notes.md`.

**Check yourself:** N-BK7 at 850 nm ($n$ = 1.5098): $R$ = 0.04126. Worked-example ABg ($A$ = 2.266 × 10⁻⁵, $B$ = 10⁻³, $g$ = 2): TIS = 4.918 × 10⁻⁴ numerically and analytically. Synthetic data: the nonlinear fit recovers $A = 3.0\times10^{-5}$, $B = 2.0\times10^{-4}$, $g$ = 1.80, TIS = 5.69 × 10⁻⁴; knee at $|x|$ = 0.0088 (0.50°).

<details><summary>Hints / solution sketch</summary>

- Integration: `scipy.integrate.quad(lambda s: 2*np.pi*A*s/(B+s**g), 0, 1, points=[B**(1/g)])` — giving the knee as a breakpoint helps accuracy when $B$ is tiny.
- The engineer's fit through the last four points ($|x| \ge 0.03$) gives roughly $g \approx 1.77$, $A \approx 3.1\times10^{-5}$, $B \approx 2.1\times10^{-4}$, TIS ≈ 5.5 × 10⁻⁴ — close, but the straight-line fit is biased because the 0.03 point still feels the knee. Drop it, or use the nonlinear fit.
- `scipy.optimize.least_squares` on residuals $\ln(\text{model}) - \ln(\text{data})$ with parameters $(\ln A, \ln B, g)$ keeps $A, B > 0$ automatically.
- With real data, also check TIS < 1 — OpticStudio rejects ABg profiles whose TIS exceeds 1 (Ansys fitting article).

</details>

## Task 2 — A virtual BRDF goniometer: verify the scatter models (OpticStudio)
**Goal:** Learn exactly what each scatter model does in OpticStudio and confirm it against hand numbers; meet importance sampling.

**Given / specs:** New NSC file `work/L07_T2_brdf.zmx`, units mm, wavelength 0.85 µm.
- Object 1: **Source Rectangle** at Z = 0, half widths 0.5 × 0.5 mm, collimated along +Z, 1 W, 10⁵ analysis rays.
- Object 2: **Detector Rectangle** at Z = 50 mm, half widths 50 × 50 mm, 101 × 101 pixels, material **blank** (transparent, so the incident beam passes through it — L02).
- Object 3: **Rectangle** at Z = 100 mm, half widths 10 × 10 mm, material `MIRROR` (the sample, facing −Z — the beam hits it at normal incidence).
- System Explorer → Non-Sequential: Minimum Relative Ray Intensity $10^{-10}$.

**Steps:**
1. Trace with no scatter (Split, Scatter, Polarization on). Open the Detector Viewer: what total power does the detector report, and why? (Incident and reflected beams both cross it.) Now apply filter `S3` (scattered at object 3): nothing — no scatter is defined yet.
2. **Lambertian:** Object 3 Properties → Coat/Scatter → face of the rectangle: Lambertian, Scatter Fraction 0.1, Number of Rays 5. Trace. Detector Viewer with filter `S3`: total power and the irradiance shape. Repeat with *angle space* display (radiant intensity) if your detector settings offer it.
3. **Gaussian:** σ = 0.1, fraction 0.1. Compare the spot size on the detector with $50\ \text{mm}\times\tan(5.74°)$ (1/e radius).
4. **ABg:** create a user ABg data file (copy the format of `ABG_DATA.DAT` in `{Zemax}\ABg_Data` into e.g. `MY_ABG.DAT`), add a profile `ROUGH850` with $A$ = 0.01, $B$ = 0.01, $g$ = 2 at 0.85 µm, select it for the face. Trace; read `S3` and `!S3` totals. Use your Task 1 code to predict both.
5. **Importance sampling:** go back to Lambertian (fraction 0.1) and shrink the detector to half widths 2 × 2 mm, 21 × 21 pixels. Trace once without importance sampling: note detector power and number of rays hitting it (Detector Viewer text tab or Ray Database Viewer). Then Object 3 → **Scatter To** → importance sampling: target object 2, Size 3 mm (slightly larger than the detector's 2.83 mm corner radius), default Limit, for the scattered ray number(s) you use. Trace again with the same source ray count.

**Deliverable:** table in `notes.md` (model, predicted power on detector, measured `S3` power, rays on detector) + screenshots of the four irradiance maps.

**Check yourself:**
- Step 1: unfiltered ≈ 2 W (1 W incident + 1 W reflected through a transparent detector) — a reminder to filter.
- Lambertian, 100 × 100 mm square at 50 mm from the sample: fraction of Lambertian power = 0.554 (view factor) → **0.0554 W** with `S3`; `!S3` reflected specular = 0.9 W (plus the 1 W incident on the way in).
- Gaussian σ = 0.1: essentially all 0.1 W lands on the detector (fraction > 0.999); the halo's 1/e radius ≈ 5.0 mm.
- ABg (0.01, 0.01, 2): TIS = $\pi\cdot0.01\cdot\ln 101$ = **0.145**; power on the 100 × 100 mm detector 0.127 W; specular 0.855 W. No Scatter Fraction was entered — the 1 − TIS specular share is automatic.
- Importance sampling: expected power on the 4 × 4 mm detector = 0.1 × 0.00203 = **2.0 × 10⁻⁴ W** in both runs (within noise). Without IS only ~0.2 % of scattered rays hit (≈ 10³ of 5 × 10⁵); with IS (nearly) every IS ray hits — hundreds of times more rays, much lower noise. If the IS run shows *zero* power, your Minimum Relative Ray Intensity is too high.

<details><summary>Hints</summary>

- The ABg data-file line layout is version-specific: copy an existing entry's `NM`/`WV`/`DT` lines and change the numbers; keep names upper-case if you later use an `.ABGF` file.
- The ABg file's wavelength must cover your trace wavelength (one `WV` value at 0.85 µm is fine).
- For the importance-sampling table, the "Ray" column selects which of the *Number of Rays* scattered rays is importance-sampled; with Number of Rays = 5 you can sample one or more of them. Read the Help on *Scatter To* for your release.
- Measured numbers will differ from predictions by a few % because of noise (≈ $1/\sqrt{N_{\text{hits}}}$) — quote the hit counts.

</details>

## Task 3 — Ghosts in the projection lens and half-field contrast (OpticStudio)
**Goal:** Quantify ghost stray light of your L05 projection lens in NSC, rank the paths, and see what coatings buy.

**Given / specs:** Start from `../L05-projection-lens-design/work/L05_T5_projlens.zmx` (if you did not finish it, any 5–6-element lens of similar size works — e.g. your Cooke triplet NSC file `../L06-hybrid-mixed-mode-and-nsc-optimization/work/L06_T2_cooke_nsc.zmx`).
1. Save a copy, fix all semi-diameters, and **Convert to NSC Group** with "convert file to non-sequential mode" (L06 Task 2). Save as `work/L07_T3_proj_nsc.zmx`. Delete the converter's source(s) and detector(s).
2. **Source (the "white" half of the DMD):** Source Rectangle at the DMD plane, emitting toward the lens, X half width 1.728 mm centred at X = +1.728 mm, Y half width 1.944 mm centred where the DMD centre is in your L05 offset geometry; Cosine Exponent 20 (half-power half-angle ≈ 14.6°, i.e. about the F/2.0 cone — the overfill will hit mechanics later in Task 4); 1 W; 10⁶ analysis rays.
3. **DMD as a reflector:** a Rectangle (DMD active area, half widths 3.456 × 1.944 mm) 0.01 mm *behind* the source plane, material `MIRROR`, coating `I.35` (≈ 65 % reflectance — a crude flat-mirror worst case; real micromirrors are tilted, so their return goes partly elsewhere).
4. **Detector:** Detector Rectangle at the 750 mm screen, sized to the projected image plus 10 % margin, 200 × 120 pixels, `ABSORB`.
5. Ray Trace Control: Use Polarization, Split NSC Rays on; Save Rays to `L07_T3.ZRD` with filter `H<det>`. Minimum Relative Ray Intensity $10^{-9}$.

**Steps:**
1. **Configuration A — uncoated:** no coatings on any lens/window face. Trace. In the Detector Viewer (log scale) look at the image of the "black" half.
2. Replay the ZRD with filters: `!G0` (signal), `X_GHOST(0,2)` (double-bounce ghosts), `X_GHOSTN(0,4,0)` or `X_GHOST(0,4)` (fourth-order), `H<dmd> & X_GHOST(0,2)` (ghosts involving the DMD). Record total powers.
3. **Half-field contrast:** mean irradiance in the bright half / mean irradiance in the dark half, using regions that exclude 10 % of the image width on each side of the boundary (export the detector text and compute in Python).
4. **Path Analysis** (Analyze → Raytrace Analysis → Path Analysis) on the ZRD: list the top 10 paths with % of total. Identify which objects/faces produce the strongest ghosts; show the strongest with filter `_2` (or whichever path number) in the Shaded Model. For a face-resolved check use `X_HITFACE2(n,f,2) & Gn`.
5. **Configuration B — 1 % AR:** coating `I.99` on all lens and window faces. **Configuration C — NIR V-coat:** `I.9975`. Repeat steps 1–4 (a Multi-Configuration Editor with the coating per face is elegant but optional — copies of the file are fine).
6. Compare with the lecture estimate $s \approx \binom N2 R^2$ and $\text{CR} \approx (1+s/2)/(s/2)$ (though your source is only half-field, so convert accordingly).

**Deliverable:** `work/L07_T3_proj_nsc.zmx` (+ B, C variants), a table (config, signal, ghost power, ghost/signal, half-field contrast, top-3 paths), log-scale detector images.

**Check yourself:**
- Path 1 must be the straight-through design path with most (typically ≥ 80 %) of the detected power (uncoated: Fresnel losses on ~14 surfaces cost ~45 % if all were at normal incidence — $0.9587^{14}$ = 0.55 — so expect the uncoated signal to be noticeably lower than with I.99, which gives $0.99^{14}$ = 0.87).
- Ghost/signal on the detector: uncoated typically 10⁻²–10⁻¹; I.99 typically 10⁻³–10⁻² ; I.9975 typically 10⁻⁴–10⁻³. Each step should scale roughly as $R^2$ (×16 between 1 % and 0.25 %) unless the DMD ghost dominates — the DMD reflects 65 %, so DMD–lens ghosts scale only with $R$, not $R^2$, and often top the list once the lens is coated.
- Half-field contrast should rise roughly as $1/R^2$ (or $1/R$ if DMD ghosts dominate); for a well-coated NIR projection lens several hundred to a few thousand to one.

<details><summary>Hints</summary>

- If the converter produced Standard Lens objects, faces are 1 (front), 2 (back) and 0 (edge). Do not forget the window/prism faces.
- Ghosts that leave the system backwards are not on the detector; that's fine — the `H<det>` save filter keeps the ZRD small.
- 10⁶ rays with splitting can produce very large ZRDs; start with 10⁵, look at the paths, then scale.
- The "DMD ghost" (lens surface → back to the DMD → forward again) re-images the bright half onto itself (or mirrored) slightly defocused — a structured ghost. Discuss in `notes.md` what that means for fringe phase (lecture §7).

</details>

## Task 4 — Barrel, vanes and NIR-reflective "black" (OpticStudio)
**Goal:** Add mechanics to the Task 3 model, find the scatter paths, and test baffle measures.

**Given / specs:** Start from `work/L07_T3_proj_nsc_C.zmx` (the I.9975 configuration).
- Add a **Cylinder Pipe** (or Cylinder Volume) barrel coaxial with the lens: inner radius 0.5 mm larger than the largest element semi-diameter, running from the window to 2 mm beyond the front element. Material `MIRROR`.
- Add **Annulus** objects as retaining rings/spacers at each element (inner radius = element clear semi-diameter, outer = barrel radius), same surface treatment.
- Surface treatments (Coat/Scatter of every mechanical face):
  - **M1 "black anodise, visible"**: coating `I.95`, Lambertian, Scatter Fraction 0.9 (→ 4.5 % Lambertian + 0.5 % specular, as in Ansys KB Part 3).
  - **M2 "black anodise at 850 nm"**: coating `I.70`, Lambertian, fraction 0.9 (27 % Lambertian + 3 % specular — a pessimistic but realistic NIR case).
  - **M3 "bare machined aluminium"**: coating `I.30` (70 % reflectance), Gaussian σ = 0.3, fraction 0.5.
- Number of Rays = 3 on all mechanical faces; Scatter NSC Rays on.

**Steps:**
1. Trace M1, M2, M3. Separate the families with filters: `F0` (scattered anywhere — the Help documents `F0` and `G0` as "any object"), `X_SCATTER(0,1)` (exactly one scatter event), `X_SCATTER(0,2)` (two), and per-object `S<barrel>`, `S<ring k>`; combine each with `H<det>` if your ZRD was not already saved with that filter.
2. Path Analysis: which mechanical part is worst? Is it the barrel bore between the DMD window and the stop, or a ring near the stop?
3. Turn on **importance sampling** on the worst part, targeting the next lens element toward the screen (target Size ≈ that element's semi-diameter + 0.5 mm). Compare scatter power on the detector and its noise with and without IS (same ray count). Lower Minimum Relative Ray Intensity if IS rays vanish.
4. **Fix it:** add 4–6 **vanes** (Annuli, inner radius just outside the beam footprint — check with the Footprint/Layout) along the worst bore, or reduce the bore section's diameter as a field stop. Re-trace in M2.
5. Compute the half-field contrast for M1/M2/M3 and M2 + vanes.

**Deliverable:** `work/L07_T4_barrel_M1.zmx` … `M2_vanes.zmx`, a table of scatter power on the detector (by path family) and contrast, one paragraph of conclusions for a mechanical engineer ("specify NIR reflectance of the anodise ≤ x % at 850 nm", "add vanes at …").

**Check yourself:** Scatter power should scale roughly with the Lambertian reflectance: M2/M1 ≈ 27/4.5 = 6× for single-scatter paths, ≈ 36× for double-scatter. M3's Gaussian specular-ish behaviour often produces **structured** stray light (rings, arcs — cf. the arc in KB Part 2) instead of a smooth veil. Vanes should reduce the bore contribution by several × if their inner edges are not themselves lit. With 0.25 % AR coatings, mechanical scatter in M2 can rival or exceed the lens ghosts — the reason "black" must be specified in the NIR.

<details><summary>Hints</summary>

- Cylinder Pipe is an open tube (no end caps): good for a bore. Its parameters include front radius, length and rear radius — use equal radii for a straight bore.
- Lens edges: assign the converted lenses' edge faces (face 0) a Lambertian fraction too (ground, un-inked edge: e.g. `I.90`-like treatment with Lambertian 1.0 inside glass is hard to model exactly — try Lambertian fraction 1 on face 0 and compare with an "inked" edge, coating `I.95`).
- With multiple-scatter trees, keep Number of Rays small and use importance sampling only after you know where to aim.

</details>

## Task 5 — Glint ghosts in the camera and the depth error they cause (OpticStudio + analysis)
**Goal:** Connect a ghost level in the receiver to a 3D error.

**Given / specs:** Start from your NIR camera lens `../../04-machine-vision-camera-lenses/L08-filters-cover-glass-nir-and-ghosts/work/L08_T3_nir940.zmx` (940 nm; keep its wavelength). Convert to NSC (full conversion). Model the **sensor** as a Detector Rectangle (`ABSORB`) with a thin, *transparent* Rectangle 0.001 mm in front of it carrying coating `I.90` (10 % sensor reflectance — verify in a one-ray test that an IDEAL coating on a blank-material Rectangle really reflects 10 % in your release; if not, use a thin N-BK7 Rectangular Volume with a `TABLE`/`IDEAL` coating instead).

**Steps:**
1. **Glint:** a Source Point (or a small Source Ellipse, radius 0.1 mm) at the working distance at 70 % field, emitting a cone that fills the entrance pupil (no wider — use the source's cone/angle parameters, or a far-field Gaussian). 10⁶ rays, split on.
2. Detector Viewer (log scale): main image vs ghost spots/halos. Filter `!G0` vs `X_GHOST(0,2)`. Find the brightest ghost: its peak irradiance relative to the main spot peak ($\eta_{\text{peak}}$), and its location/size. Path Analysis: which surfaces form it? (Expect sensor ↔ filter/cover-glass ghosts and a lens-surface pair or two — compare with your Ghost Focus Generator ranking from Course 04 L08 Task 4.)
3. **Depth error estimate (pen & paper):** a glint $G$ = 300× brighter than diffuse surfaces at the same exposure, with the ghost landing on a diffuse region. If the glint image spot covers ~4 pixels and the ghost halo covers $M$ pixels, the ghost's irradiance relative to the diffuse signal is $\varepsilon \approx G\cdot P_{\text{ghost}}/P_{\text{main}}\cdot 4/M$. Compute $\varepsilon$ from your simulated $P_{\text{ghost}}/P_{\text{main}}$ and halo size; then $\delta\phi = \arcsin\varepsilon$ (if $\varepsilon < 1$) and $\delta z$ with $p_z$ = 69.3 mm (lecture worked example).
4. Repeat 1–3 with all lens AR coatings changed from your current setting to `I.99` and to `I.9975`.

**Deliverable:** detector images, a table (coating, $P_{\text{ghost}}/P_{\text{main}}$, halo size, $\varepsilon$, $\delta z$), and a recommendation for the receiver coating spec.

**Check yourself:** For a single pair, $P_{\text{ghost}}/P_{\text{main}} \approx R_iR_j$: 10⁻⁴ for two 1 % surfaces, 10⁻³ for sensor (10 %) × 1 % filter. Example: $P_{\text{ghost}}/P_{\text{main}} = 10^{-3}$, halo of $M$ = 400 pixels → $\varepsilon = 300\cdot10^{-3}\cdot4/400 = 3\times10^{-3}$ → $\delta\phi$ = 3.0 mrad → $\delta z = 0.0030/(2\pi)\cdot69.3$ = 0.033 mm. A focused lens ghost with $M$ ≈ 10 and $10^{-4}$ gives $\varepsilon$ = 0.012 → 0.13 mm. Sensor–cover-glass ghosts are dim per pixel because of their large halos (Course 04 L08: ≈ 0.5 mm diameter); concentrated lens-pair ghosts are the dangerous ones.

<details><summary>Hints</summary>

- `arcsin` needs $\varepsilon < 1$; for $\varepsilon \ge 1$ the ghost dominates and the phase at that pixel is simply the glint's phase — a gross outlier, not a small error.
- The ghost carries the *glint's* fringe phase to a different pixel, so the phase offset $\Delta$ between ghost and local signal is essentially random — use the worst case $\arcsin\varepsilon$.
- If the sensor reflector placement confuses the detector (double counting), use a filter: `L<det>` (last segment hit the detector) counts each branch's final arrival.

</details>

## Stretch task(s)
- **VGI simulation (ISO 9358-style):** with the Task 5 camera, put a large Lambertian Source Ellipse (field-filling) in object space with a small absorbing disk (`ABSORB` Ellipse) at its centre; measure irradiance at the centre of the disk's image with and without the disk. VGI = ratio in %. Compare M1 vs M2 barrel treatments (add a barrel as in Task 4).
- **GSF:** point source at 0°, detector 10× the image size with log display; plot the azimuthally averaged GSF down to 10⁻⁶ and identify the regions dominated by diffraction, lens-surface scatter (add the lecture ABg with $A$ = 2.27 × 10⁻⁵, $B$ = 10⁻³, $g$ = 2 to every lens face), and ghosts.
- **Scripted ZRD analysis:** in Python (ZOSPy / ZOS-API Ray Database Reader — preview of Course 07), read `L07_T3.ZRD` and compute ghost power per surface pair; reproduce the Path Analysis top 10.

## Reflection questions
1. Why is a "4 % per surface" ghost estimate an upper bound for the light reaching the detector, and in which situations can a single ghost still be worse than this simple product suggests?
2. You switched a black anodised barrel from the visible to an 850 nm system and stray light rose 6×. Which number in your NSC model captures this, and what would you ask the supplier for?
3. Why must the importance-sampling target be an object the scatter point can see directly, and why do importance-sampled rays need a lower Minimum Relative Ray Intensity?
4. For a structured-light camera, why is a 10⁻⁴ ghost potentially more harmful than a 10⁻² uniform veil?
5. Path Analysis says path 2 carries 0.8 % of the detected power and is "lens 3 face 2 ↔ lens 5 face 1". List three design levers, in order of cost, to reduce it.

<details><summary>Answers</summary>

1. The product $R_iR_j$ ignores transmission losses on the way and assumes all ghost light reaches the detector area; many ghosts are vignetted or leave the field. But a ghost can be *locally* far worse: if it focuses near the detector its irradiance (power per area) can approach a sizeable fraction of the source image's; and very bright scene points (glints, the DMD ON-state) multiply it. Highly reflective elements (sensor, DMD) make some ghosts scale with $R$ instead of $R^2$.
2. The coating on the MIRROR material (`I.95` → `I.70`, i.e. reflectance 5 % → 30 %) together with the Lambertian fraction. Ask for hemispherical (total and diffuse) reflectance — ideally BRDF — of the finish at the operating wavelength (850/940 nm), not only "black" in the visible; consider NIR-black finishes or paints.
3. Importance sampling aims rays at the target and weights them by the BSDF averaged over the target's solid angle; if the target is not directly visible (e.g. a detector behind a lens), the aimed rays are blocked or the weighting is wrong. The weighted rays carry small power (∝ BSDF × solid angle / Number of Rays), often below the default 10⁻⁶ relative threshold, so they are terminated before arriving.
4. A uniform veil reduces modulation by $1/(1+s)$ — 1 % for $s = 10^{-2}$ — costing only a little depth precision. A ghost carries pattern phase from elsewhere; multiplied by scene dynamic range (glints 100–1000×) and concentration, it can reach $\varepsilon$ ~ 10⁻²–1, giving systematic depth errors of 0.1–several mm, which look like real geometry.
5. (a) Improve the AR coating on those two faces (cheapest if the coating run exists; ghost ∝ $R_3R_5$); (b) change curvature/spacing slightly so the ghost focuses far from the image (sequential re-optimization with GPIM, Course 04 L08), keeping MTF; (c) add a field stop or baffle that blocks the ghost path if it is geometrically separate from the image beam. Also check whether the path involves a mechanical surface you can blacken.

</details>
