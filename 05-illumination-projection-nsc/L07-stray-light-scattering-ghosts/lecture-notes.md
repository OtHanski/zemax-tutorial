# L07 — Stray Light: Scattering, Ghosts and Baffling

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3.5 h, tasks ~6–7 h
> **Prerequisites:** [L02](../L02-non-sequential-fundamentals/lecture-notes.md) (ray splitting, ZRD, filter strings), [L05](../L05-projection-lens-design/lecture-notes.md) (projection lens), [L06](../L06-hybrid-mixed-mode-and-nsc-optimization/lecture-notes.md) (Convert to NSC Group, Monte-Carlo noise), [Course 04 L08](../../04-machine-vision-camera-lenses/L08-filters-cover-glass-nir-and-ghosts/lecture-notes.md) (sequential ghost analysis, Ghost Focus Generator), [Course 03 L08](../../03-image-quality-optimization/L08-polarization-and-coatings/lecture-notes.md) (Fresnel equations, coatings) · **Next:** [L08 — Diffractive optics and pattern projection](../L08-diffractive-optics-and-pattern-projection/lecture-notes.md)

## Learning objectives
- Define **BSDF/BRDF/BTDF**, **TIS** and the **projected solid angle**, and use them to estimate by hand how much scattered power from a surface reaches a detector or pupil.
- Write down the **Lambertian, Gaussian and ABg** scatter models as OpticStudio implements them, explain what $A$, $B$, $g$ and $\sigma$ do, compute the TIS of an ABg profile, and relate surface roughness to TIS.
- Set up surface scatter on NSC object faces (Coat/Scatter tab, Scatter Fraction, Number of Rays), use **Scatter To** and **importance sampling**, and explain why importance-sampled rays need a lower *Minimum Relative Ray Intensity*.
- Model Fresnel and coating-driven **ghost reflections** with ray splitting, count and rank ghost paths, and isolate them with ZRD filter strings (`Gn`, `X_GHOST`, `X_HITFACE2`, `Sn`, `X_SCATTER`) and **Path Analysis**.
- Translate stray light into metrics that matter for a structured-light 3D camera: fringe modulation loss, phase/depth error from a ghost, projector checkerboard (ANSI-type) contrast and camera **veiling glare index**.
- Run a practical stray-light workflow: sequential ghost screening → NSC model with coatings and black housings → path ranking → fixes (coatings, curvatures, baffles, vanes, blackening) → re-verify.

## Reading
- **Core:** [Kenyon §11.1–11.4, pp. 297–303] — physical origin of scattering: Rayleigh ($\propto\lambda^{-4}$), Mie (size ≈ λ, forward-peaked lobes), and the extinction law $I = I_0 e^{-(\beta_s+\beta_a)z}$ (eq. 11.10). Read for intuition about *why* rough surfaces, dust and paints scatter, and why bulk scatter in OpticStudio is parametrised by a mean free path.
- **Core:** [Kenyon §9.6, eq. 9.79–9.80, p. 247] (normal-incidence Fresnel reflectance, "4 % per glass surface") and [Kenyon §9.7, p. 252] (single-layer MgF₂ AR: 4 % → 1.4 %). These two numbers are the ghost budget's raw material.
- **Core (online):** Ansys Optics KB, *Introduction to stray light analysis – Part 2* (ghosts, filter strings, Minimum Relative Ray Intensity, Path Analysis, `{#50}` and `_n` path filters): <https://optics.ansys.com/hc/en-us/articles/42661744883091>
- **Core (online):** Ansys Optics KB, *Introduction to stray light analysis – Part 3* (CAD housings in single-surface mode, `I.95` on MIRROR + 0.9 Lambertian fraction, Path Analysis of retaining-ring scatter): <https://optics.ansys.com/hc/en-us/articles/42661774807955>
- **Core (online):** Ansys Optics KB, summary of scatter models (KA-01415: Lambertian, Gaussian, ABg, tabular BSDF, K-correlation, bulk scatter): <https://optics.ansys.com/hc/en-us/articles/42661773980563>
- **Core (online):** Ansys Optics KB, *Scatter To and Importance Sampling*: <https://optics.ansys.com/hc/en-us/articles/43071055638419>
- **Optional:** [Kenyon §2.2.2, p. 39] — the groove cut across Porro prisms to kill glancing-angle scatter: a two-line lesson in baffling.
- **Optional (online):** fitting ABg to measured BRDF (<https://optics.ansys.com/hc/en-us/articles/43071132421395>); several ABg profiles in one `.ABGF` file (<https://optics.ansys.com/hc/en-us/articles/43071068163347>); tabular BSDF data (<https://optics.ansys.com/hc/en-us/articles/43071089490451>); K-correlation roughness model (<https://optics.ansys.com/hc/en-us/articles/43071070893971>).
- **Optional (books, not in corpus):** E. Fest, *Stray Light Analysis and Control* (SPIE Press, 2013); J. C. Stover, *Optical Scattering: Measurement and Analysis* (SPIE Press). The standard references if stray light becomes part of your job.

---

## 1. What stray light is, and why a 3D camera cares

**Stray light** is any light that reaches the detector by a path the designer did not intend. In imaging optics it shows up as reduced contrast, veiling glare, flare, ghost images; in a projector as raised black level and pattern copies. The mechanisms are few:

| Mechanism | Physics | Typical source in a Zivid-type system |
|---|---|---|
| **Ghosts** | Specular Fresnel reflections at refracting surfaces, even number of bounces | lens surfaces, DMD window, TIR prism, filter, cover glass, sensor |
| **Surface scatter from optics** | Residual roughness, digs, contamination | polished/molded lens surfaces, dust on the front window |
| **Scatter from mechanics** | Diffuse/specular reflection off housings, retainers, lens edges | barrel bore, spacers, threads, edge of lenses (ground but not blackened) |
| **Direct/sneak paths** | Light that bypasses the optics | LED light leaking around the condenser; projector light leaking into the camera inside a shared housing |
| **Bulk scatter / fluorescence** | Inclusions, bubbles, polymers | plastic lenses, diffusers |
| **Out-of-band / out-of-field light** | Sources outside the FOV or wavelength band | sunlight, factory lights, bright parts just outside the FOV |

For structured light the consequences are concrete. The projector paints fringes; the camera measures their **phase**. Anything that adds a **uniform** offset reduces fringe **modulation** (worse SNR, more depth noise). Anything that adds a **structured** copy of the pattern — a ghost image of the DMD, or a ghost of a specular glint in the camera — adds a component with the *wrong phase* and therefore a **systematic depth error**. The second kind is far more dangerous per watt, and the worked example quantifies this.

A professional mental model, from the stray-light literature (Fest; Breault), is the product

$$
\Phi_{\text{det}} \;\approx\; \Phi_{\text{src}}\cdot \text{BSDF}\cdot \Omega_{p}
$$

— power on a "critical" surface × how strongly it scatters × the **projected solid angle** of the next aperture as seen from that surface. Each factor can be attacked separately: keep light off surfaces that the detector can see (baffles, stops), make the seen surfaces scatter less (black, smooth, tilted), and shrink what each surface sees (vanes, apertures). The Monte-Carlo trace in OpticStudio is just a careful way to evaluate the product over every path.

## 2. Scatter physics in one page

### 2.1 Microscopic origin (Kenyon Ch. 11)
Kenyon builds scattering from oscillating dipoles: a particle much smaller than λ scatters with cross-section $\sigma \propto a^6/\lambda^4$ (Rayleigh, eq. 11.7); particles from ~λ/10 to ~100 λ are in the **Mie** regime with lobed, increasingly forward-peaked angular distributions (for a 5λ sphere the forward/backward ratio is ~2000:1) and a cross-section tending to the geometric area [Kenyon §11.2–11.3, pp. 298–302]. A perfectly homogeneous medium scatters coherently only into the forward direction — that coherent forward scatter *is* the refractive index [§11.2.1, pp. 300–301]. Light is lost from a beam only through **inhomogeneities**: density fluctuations, inclusions, surface height variations.

For optical engineering this gives three take-home points:
1. **Surface roughness and contamination** dominate the scatter of good optics (bulk scatter of optical glass is tiny). Polished-glass roughness (~0.5–2 nm RMS) is ≪ λ, so it scatters mostly at **small angles** around the specular direction.
2. **Particulates** (dust, ~1–100 µm) are Mie scatterers: strong, forward-peaked, roughly wavelength-independent in the visible/NIR.
3. **Bulk scatter** follows the extinction law $I(z) = I_0 e^{-(\beta_s+\beta_a)z}$ [Kenyon eq. 11.10, p. 303]; OpticStudio's bulk-scatter models are parametrised by the **mean free path** $M = 1/\beta_s$ (scatter probability $1-e^{-x/M}$ over path length $x$) [KA-01415].

### 2.2 BSDF, TIS and projected solid angle
Let a surface element receive irradiance $E_i$ (W/m²) from direction $\hat k_i$. It scatters radiance $L_s(\theta_s,\phi_s)$ (W m⁻² sr⁻¹). The **bidirectional scattering distribution function** is

$$
\text{BSDF}(\theta_i,\phi_i;\theta_s,\phi_s) = \frac{dL_s(\theta_s,\phi_s)}{dE_i(\theta_i,\phi_i)}\quad[\text{sr}^{-1}],
$$

called BRDF for reflection and BTDF for transmission. Integrating over the hemisphere with the projected-solid-angle weight $\cos\theta_s\,d\Omega_s$ gives the **total integrated scatter**:

$$
\text{TIS}(\theta_i) = \int_{\text{hemi}} \text{BSDF}\,\cos\theta_s\,d\Omega_s = \int_0^{2\pi}\!\!\int_0^{\pi/2}\text{BSDF}\,\cos\theta_s\sin\theta_s\,d\theta_s\,d\phi_s ,
$$

the fraction of incident power scattered (as opposed to specular, absorbed or transmitted).

**Lambertian** surface: BSDF constant $= \rho/\pi$, so TIS $= (\rho/\pi)\cdot\pi = \rho$ (the hemispherical reflectance). Radiance is constant; intensity $\propto\cos\theta_s$ (L01).

**Projected solid angle.** The power that a Lambertian patch sends into an aperture is $\rho\,\Phi_{\text{inc}}\,\Omega_p/\pi$, where $\Omega_p = \int\cos\theta\,d\Omega$ over the aperture. For a circular aperture of half-angle $\alpha$ centred on the patch normal, $\Omega_p = \pi\sin^2\alpha$, so the fraction is simply $\rho\sin^2\alpha$. This little formula is the stray-light engineer's best friend.

**Smooth-surface TIS from roughness.** For a surface with RMS roughness $\sigma_h \ll \lambda$, the classic (Davies/Bennett–Porteus) result for reflection is

$$
\text{TIS} \approx \left(\frac{4\pi\sigma_h\cos\theta_i}{\lambda}\right)^2 .
$$

(For transmission through a glass surface the prefactor is smaller, roughly $[2\pi\sigma_h(n-1)/\lambda]^2$ — about 16× less for $n=1.5$; use the reflective form as a conservative upper bound.) With $\sigma_h$ = 1.5 nm at 850 nm: TIS ≈ 4.9 × 10⁻⁴; the same surface at 550 nm scatters 1.2 × 10⁻³. **NIR helps**: scatter from smooth surfaces falls as $\lambda^{-2}$.

### 2.3 The Harvey (direction-cosine) picture
Most practical scatter models are written in **direction-cosine space**. Project the specular direction and the scatter direction onto the surface plane: $\vec\beta_0$ and $\vec\beta$ (each with length $\sin\theta$). Their difference $\vec x = \vec\beta - \vec\beta_0$ has $|\vec x| \le 2$. Harvey observed that for many polished surfaces the BSDF depends (approximately) only on $|\vec x|$ — it is **shift-invariant**: the same "scatter halo" rides along with the specular ray whatever the angle of incidence. OpticStudio's built-in Gaussian and ABg models use exactly this variable [KA-01415; ABg fitting article].

## 3. Scatter models in OpticStudio

All are set per **object face**: Object Properties → **Coat/Scatter** tab, choose the face, then *Scatter Model* and its parameters [L02 §2; KA-01415].

### 3.1 Lambertian
$$\text{BSDF} = \frac{1}{\pi}\ \ (\text{normalised}),$$
scaled so that the scattered power is the **Scatter Fraction** of whatever power the face reflects (or transmits). Use it for black paints, anodising, bead-blasted metal, diffusers, and as a conservative "pessimistic" model of any mechanical surface.

### 3.2 Gaussian
$$\text{BSDF}(\vec x) = A\,\exp\!\left(-\frac{|\vec x|^2}{\sigma^2}\right),$$
with $\sigma$ the width in direction-cosine space ($\sigma$ = 0.1 → 1/e half-width ≈ 5.7° around the specular ray at small angles). $A$ is computed internally from the normalisation; you set $\sigma$ and the Scatter Fraction. OpticStudio limits $\sigma$ to 5 — larger values are practically Lambertian [KA-01415; Turner, U. Arizona stray-light notes]. Use it for "satin" or lightly-etched surfaces, and for engineered diffusers when you only know an FWHM.

### 3.3 ABg (Harvey–Shack-type)
$$\text{BSDF}(\vec x) = \frac{A}{B + |\vec x|^{g}} .$$

- For $|\vec x| \ll B^{1/g}$ the BSDF is flat at $A/B$ (the near-specular plateau).
- For $|\vec x| \gg B^{1/g}$ it falls as a straight line of slope $-g$ on a log–log plot ($\log\text{BSDF}$ vs $\log|\vec x|$); $A$ sets the line's height. The **knee** is at $|\vec x| = B^{1/g}$.
- Constraints in OpticStudio: $A \ge 0$, $B \ge 10^{-12}$ unless $g = 0$ [KA-01415].
- Polished optics typically have $g$ ≈ 1.5–2.5 and small $B$; black paints have $g$ ≈ 0 (Lambertian-like: BSDF $= A/(B+1)$ = constant).

**TIS of ABg.** At normal incidence $|\vec x| = \sin\theta_s$; substituting $s = \sin\theta_s$ ($ds = \cos\theta_s d\theta_s$):
$$
\text{TIS} = 2\pi\int_0^1 \frac{A\,s}{B+s^{g}}\,ds \;\overset{g=2}{=}\; \pi A\,\ln\!\left(1+\frac{1}{B}\right).
$$
A $g=2$ profile has a logarithmically "fat" tail: with $B=10^{-3}$ only ~31 % of the TIS lies within 5° of specular (worked example), which is why such surfaces still light up baffles far from the beam.

**The important behavioural difference.** For Lambertian and Gaussian (and tabular BSDF, where you normally set Scatter Fraction = 1 [tabular BSDF article]), *you* decide how much scatters via the Scatter Fraction. For ABg there is **no fraction input**: the TIS follows from $A$, $B$, $g$, and OpticStudio "automatically adds specular rays with the weight of all non-scattered energy (1 − TIS)" [ABg fitting article]. Consequences: (i) a fitted ABg with TIS slightly above 1 is rejected; (ii) absorption must come from a coating (e.g. `IDEAL`/`TABLE`), not from the ABg numbers; (iii) the specular part is $1-\text{TIS}$, so a black paint fitted with TIS ≪ 1 would wrongly reflect most light specularly unless you add absorption. (A Zemax staff answer puts the ABg specular level as "just A/B" — i.e. you cannot set it separately [community thread].)

**ABg data files.** Profiles live in ASCII `.DAT` files in the `ABg_Data` folder of your Zemax data directory (`{Zemax}\ABg_Data`); the default is `ABG_DATA.DAT`, but Ansys recommends a **user file** so updates do not overwrite your data. Each profile has a name line (`NM`), wavelength line (`WV`) and data line(s) (`DT`) [multi-ABg article] — open the shipped file in a text editor and copy an entry's layout for the exact column order in your release. An `.ABGF` file can sum or average up to 20 named profiles (first line: number of profiles and a flag, 0/omitted = weighted average, non-zero = sum; names in upper case) — useful when one ABg cannot fit both the near-specular peak and a contamination tail.

### 3.4 Other options
- **BSDF (tabular)**: measured data in the Zemax tabular BSDF format; inspect with the Scatter Function Viewer / Scatter Polar Plot first; no extrapolation, so missing azimuths scatter nothing [tabular BSDF article].
- **User-defined DLLs** shipped as samples: K-correlation (roughness-based: $\sigma_h$, correlation length), two-Gaussian, Gaussian_XY; and bulk scatter (Angle, Henyey–Greenstein, Rayleigh, Mie) set on the **Volume Physics** tab with a mean free path [KA-01415].

### 3.5 Scatter Fraction, Number of Rays, and how energy is split
On the Coat/Scatter tab you also set **Number of Rays**: with *Scatter NSC Rays* (and *Split NSC Rays*) on in Ray Trace Control, each hit spawns that many scattered child rays that share the scattered power equally [tabular BSDF article], plus the specular child carrying $1-$fraction. Keep it small (1–5) for surfaces hit by many rays, larger for the few critical surfaces — the tree grows geometrically with multiple scatter. Without splitting, OpticStudio follows one path per ray and chooses between specular and scattered probabilistically (check the Help topic *Scattering* for the exact rule in your release).

**Black surfaces done right.** The robust pattern (Ansys KB Part 3 and staff answers) is: material **`MIRROR`**, an **IDEAL coating** to set reflectance — `I.95` means T = 0.95, R = 0.05; on a mirror the "transmitted" part is absorbed — and a Lambertian scatter fraction for how much of that 5 % is diffuse. KB Part 3 uses `I.95` + fraction 0.9: 4.5 % Lambertian + 0.5 % specular — a fair model of black anodised aluminium in the visible. In the NIR many black anodise dyes become *much* more reflective (often tens of percent at 850–940 nm); ask the supplier for NIR reflectance or measure it — this is a classic NIR camera trap.

## 4. Getting scattered rays where they matter: Scatter To and importance sampling

A Lambertian surface sends a fraction $\Omega_p/\pi = \sin^2\alpha$ of its rays into an aperture of half-angle $\alpha$. For $\alpha$ = 5.7°, 1 % — so 99 % of your traced scattered rays are wasted, and the detector result is noisy (L06 §5: relative noise $\approx 1/\sqrt{N_{\text{hits}}}$).

OpticStudio offers two fixes on the **Scatter To** tab of Object Properties [importance sampling article]:

1. **Scatter To list** — scattered rays are only *kept* if they will hit listed objects. Saves tracing time downstream; does not create more useful rays.
2. **Importance sampling** — for a chosen scattered ray, OpticStudio aims the ray at a **target sphere** centred on a target object's local origin with radius **Size**, and weights its power by the BSDF averaged over the solid angle the sphere subtends ("each importance-sampled ray targeting a specific object contains the same flux"). **Limit** caps that solid angle so the BSDF does not vary too much inside it.

Rules from the KB and community:
- Make the target sphere **slightly larger** than the object you aim at, centred on its local origin (move the object's reference if needed).
- **Target an object the scatter point can actually see**, not the detector behind a lens: aim at the first lens/aperture of the receiving optics (the KB telescope example targets a corrector lens, not the detector).
- Importance-sampled rays carry **little power**, so they may fall below *Minimum Relative Ray Intensity* (System Explorer → Non-Sequential; default $10^{-6}$) and silently die. Lower it (e.g. to $10^{-9}$–$10^{-12}$) — the community answer for "no rays are scattered when I use importance sampling".
- Importance sampling **biases nothing** if set up right (total power at the target is correct), but it shows *only* the targeted direction — do not use it when you want the scatter everywhere (e.g. to see which baffle is hot).

Expected gain ≈ $\pi/\Omega_p$ more useful rays per traced ray: ×100 for $\alpha$ = 5.7°, ×800 for $\alpha$ = 2°.

## 5. Ghost reflections in NSC

### 5.1 Physics and counting
At normal incidence each uncoated air–glass surface reflects $R_0 = (n-1)^2/(n+1)^2$ [Kenyon eq. 9.79, p. 247]: 4.13 % for N-BK7 at 850 nm ($n$ = 1.5098). A single MgF₂ quarter-wave cuts it to ~1.4 % in the visible [Kenyon §9.7, p. 252]; a good NIR V-coat reaches 0.1–0.25 % at its design wavelength. A **double-bounce ghost** from surfaces $i$ and $j$ carries $\approx R_iR_j$ of the beam; with $N$ reflecting surfaces there are $\binom{N}{2} = N(N-1)/2$ such ghosts (66 for 12 surfaces, 91 for 14; a 21-surface system gives 210). Triple-bounce paths do not return toward the detector in a simple forward system (odd number of reflections goes backwards); 4-bounce ghosts scale as $R^4$ and matter only with uncoated surfaces or very bright sources.

Remember from Course 04 L08: ghost harm is **energy × concentration**. A ghost that focuses near the detector is a bright copy; a defocused one is a faint veil. And the **sensor** (several % to >10 % reflectance), the DMD (micromirrors are mirrors!), and flat windows near focus are the usual dominant reflectors.

### 5.2 Modelling ghosts in OpticStudio
1. Convert the sequential lens to NSC (L06 §2) or build it in the NSC Editor.
2. **Coatings** on each face (Coat/Scatter tab): none (bare Fresnel), `I.995` (0.5 % R), a `TABLE` coating, or a real multilayer from a coating file — Course 03 L08. Uncoated refractive faces get Fresnel reflection computed with the actual angle and polarization.
3. Ray Trace Control: **Use Polarization** and **Split NSC Rays** on (in current releases ticking Split also forces polarization — the Fresnel coefficients need it). The children of a reflection at a refractive face carry the `G` (ghost) flag.
4. System Explorer → Non-Sequential: **Minimum Relative Ray Intensity** sets which branches are pruned. Default $10^{-6}$ keeps $R^2$ ghosts of uncoated ($1.7\times10^{-3}$) and of 0.25 % coatings ($6\times10^{-6}$) — but a 0.1 % coating pair ($10^{-6}$) is right at the threshold. Set it at least 10× below the smallest path you care about. Also check *Maximum Intersections/Segments Per Ray* if you get truncation warnings.
5. **Save Rays** to a ZRD with a filter such as `H<detector>` so only rays that end up where you look are stored (KB Part 3 uses `H15`).

The KB Part 2 trick for a *first look*: temporarily raise Minimum Relative Ray Intensity to e.g. 0.005 so only the strongest ghost branches survive in the 3D Layout; then use Path Analysis for the real ranking.

### 5.3 Filter strings for stray light (verified against the Help page *The Filter String*)
Syntax: object `n`, optional face `.f`; `&` and, `|` or, `^` xor, `!` not, parentheses for precedence. Selection most useful here:

| Flag | Meaning |
|---|---|
| `Hn.f` / `Mn.f` | hit / missed object n (face f) |
| `Ln` | last segment of the branch hit n |
| `Gn.f` | ghost-reflected at n.f (split children of reflections at refractive objects; `G0` = any object) |
| `Sn.f` | scattered at n.f; `Fn.f` scattered (split child); `Bn` bulk scattered |
| `X_GHOST(n.f,b)` | ghosted exactly b times and hit n.f at least once (n = 0 → any) |
| `X_GHOSTN(n.f,n1,n2)` | ghosted at n.f between n1 and n2 times |
| `X_SCATTER(n.f,b)` | scattered exactly b times and hit n.f |
| `X_HITFACE2(n,f,b)` | hit face f of object n exactly b times |
| `X_TIR(n.f,v)` | TIR at n(.f) v times |
| `X_IRGT(n.f,v)` | intensity relative to launch > v on n.f |
| `~007018009[#]` | exact object sequence (3-digit numbers) |
| `_k` | path *k* of the last Path Analysis |
| `{#50} …` | keep only the first 50 rays passing the filter (layout readability) |
| `SEQ[a:b]` | sequences from the Sequence Selector (Premium/Enterprise) |

Useful patterns for a detector `D`:
- signal only: `HD & !G0 & !F0` ("never ghosted, never scattered" — `F0`/`G0` mean *any object* and are set on split children, so splitting must be on)
- all double-bounce ghosts: `HD & X_GHOST(0,2)`
- one surface's contribution: `X_HITFACE2(7,1,2) & G7` (rays that hit face 1 of lens 7 twice and were ghosted there — staff suggestion for ranking surfaces in a many-surface lens)
- housing scatter: `HD & S12` (object 12 = barrel), or single-scatter only `HD & X_SCATTER(0,1)`

Filter strings are mostly **order-independent** (they test "did this happen", not "in which order") — use path filters (`~…`), `X_SEQ`, or Path Analysis when order matters.

### 5.4 Path Analysis (and the Sequence Selector)
*Analyze → Raytrace Analysis → Path Analysis* reads the ZRD and lists every **unique path** (sequence of objects) with its power and share of the total, sorted by flux, together with counts of ghost/scatter/split events [KB Parts 2–3]. You can enter a filter (e.g. only rays that hit the detector) before analysing. Then:
- Path 1 should be the **design path** (no ghosts/scatter) — if it is not, something is very wrong.
- Read the next 10–20 paths: which objects/faces appear, how many ghost or scatter events.
- Display one path in the Shaded Model/Layout or Detector Viewer with filter `_k` (KB Part 2 uses `&_1` appended to a filter).

The **Sequence Selector** (Premium and Enterprise; Analyze tab) generates, edits and groups sequences from a ZRD/PAF or Path Analysis, saves them as `.nseq`, and exposes them as `SEQ[...]` filters [Sequence Selector article] — handy when 210 ghost paths need grouping ("all ghosts involving the window").

## 6. Mechanical stray light: housings, baffles, vanes

The sequential designer thinks in clear apertures; the stray-light designer thinks in **critical** and **illuminated** surfaces:
- **Critical surfaces**: those the detector can "see" through the optics (trace *backwards* from the detector — in OpticStudio, put a source at the detector and see what it illuminates).
- **Illuminated surfaces**: those the source (or out-of-field light) hits directly.
- A surface that is **both** is a first-order stray-light path. The design goal is that no surface is both. Then everything needs at least two scatters ($\propto\text{BSDF}^2\Omega_p^2$, typically 10⁻³–10⁻⁴ lower).

Tools, in order of effectiveness:
1. **Geometry**: field stops, aperture stops at pupil images, and a **Lyot-type stop** block light without touching image light. In a projector, a field mask at the DMD and the projection lens aperture stop are your two first lines of defence; in a camera, a tight hood/front aperture and a field stop near the image.
2. **Vanes and threads** on long bores (barrel interiors): they turn a grazing-incidence surface (which scatters strongly forward — glossy at grazing angle even when black at normal incidence) into a sequence of small faces seen nearly at normal incidence, each shadowing the next. Kenyon's Porro-prism groove [§2.2.2, p. 39] is the same idea.
3. **Blackening**: black anodise, black paints (Lambertian 2–5 % in the visible; check NIR), ink-blackened **lens edges** (ground edges are bright diffuse scatterers inside the glass and feed TIR paths).
4. **Coatings** on optics (ghosts) and **tilting** flats (filters, windows) by a few degrees so their ghosts leave the field.
5. **Cleanliness** (particulate scatter on the front window often dominates in field).

In OpticStudio: CAD barrels can be imported (STEP/IGES/SAT/STL) and set to **single-surface mode** so one coating/scatter assignment covers all faces (Object Properties → CAD → *Use single surface*) [KB Part 3]. For learning, native objects — **Cylinder Pipe**, **Cylinder Volume**, **Annulus** — are faster and fully parametric (vane spacing as an editor parameter you can sweep).

## 7. Metrics for structured light and camera glare

**Fringe modulation with a uniform veil.** A sinusoidal pattern $I(x) = \bar I\,[1 + C_0\cos\phi(x)]$ plus a uniform stray irradiance $s\bar I$ has modulation $C = C_0/(1+s)$. In shot-noise-limited phase-shifting, phase noise $\propto \sqrt{\bar I(1+s)}/(C\bar I)$ — a veil of a few % costs a few % of depth precision. Uniform veil is a nuisance, rarely a disaster.

**Projector contrast.** Projector datasheets quote full on/off ("sequential") contrast — limited by DMD off-state and flat-state light leaking into the lens pupil — and **ANSI-type checkerboard contrast** (white/black ratio measured on a 4×4 checkerboard) — limited by ghosts and scatter in the projection path. If stray light spreads a fraction $s$ of the mean power uniformly, a 50 % checkerboard gives $\text{CR} \approx (1 + s/2)/(s/2) \approx 2/s$: 1 % stray light ↔ CR ≈ 200:1.

**Ghost as a structured error.** If a ghost deposits at pixel *q* a component of relative modulated amplitude $\varepsilon$ whose fringe phase differs by $\Delta$, the measured phase is $\arg(1 + \varepsilon e^{i\Delta})$, with maximum error $\arcsin\varepsilon \approx \varepsilon$ rad. Depth error $\delta z = (\delta\phi/2\pi)\,p_z$, with $p_z$ the depth change per fringe period. Small $\varepsilon$ only matters when multiplied by large **dynamic range** — a specular glint 100–1000× brighter than diffuse neighbours.

**Camera veiling glare.** ISO 9358 defines the **veiling glare index (VGI)** as the ratio of the irradiance at the centre of the image of a small, perfectly black patch on a uniform bright field, to the irradiance there without the patch, in % [Optikos note on ISO 9358]; the **glare spread function** (GSF) is the image of a small source normalised to unit flux, measurable to ~10⁻⁵. In OpticStudio, a GSF is a point/small source at a field angle and a large detector with a log-scale display; a VGI simulation is a field-filling Lambertian source with a central obscuring disk (Task 5 stretch).

## 8. In OpticStudio — workflow and quick reference

A practical workflow (consistent with Ansys' *Stray Light Analysis Overview*):

1. **Sequential screening** — Ghost Focus Generator (Course 04 L08); move ghost foci away from the image with curvature changes/GPIM; decide which surfaces need premium AR.
2. **NSC model** — Convert to NSC Group (L06); fix coatings per face; add **mechanics** (barrel, spacers, retainers, stops, housing, the window), each with a scatter model; add the **real source** (DMD-sized source with the illumination NA for the projector; for the camera, scene sources including bright glints and out-of-field sources).
3. **Trace** — Split + Scatter + Polarization on; Minimum Relative Ray Intensity low enough; Save Rays with an `H<det>` filter; 10⁶–10⁷ rays.
4. **Rank** — Path Analysis; filter strings to separate ghosts (`G`), scatter (`S`), and specific surfaces; Detector Viewer in log scale.
5. **Fix** — biggest path first; coatings, curvatures, baffles/vanes, blackening, tilts. Use importance sampling once you know which scatter surfaces matter and you need quantitative numbers at the detector.
6. **Verify** — metrics: ghost-to-signal ratio, ANSI/half-field contrast, VGI/GSF, fringe phase error; document the top paths.

| Task | Where |
|---|---|
| Scatter model per face | Object Properties → Coat/Scatter (Scatter Model, Scatter Fraction, Number of Rays) |
| Importance sampling | Object Properties → Scatter To |
| Bulk scatter | Object Properties → Volume Physics |
| Coating per face | Object Properties → Coat/Scatter (coating name, `I.x`, `TABLE`, `IDEAL` from the coating file) |
| Ray splitting, scatter, polarization, ZRD | Analyze → Ray Trace (Ray Trace Control) |
| Pruning thresholds | System Explorer → Non-Sequential (Minimum Relative/Absolute Ray Intensity, Max Intersections/Segments per Ray) |
| Path ranking | Analyze → Raytrace Analysis → Path Analysis; Sequence Selector |
| Inspect a BSDF | Scatter Function Viewer / Scatter Polar Plot (location varies — search the ribbon) |
| ZRD inspection | Ray Database Viewer; Detector Viewer with a ZRD + filter |

Common pitfalls:
- Treating a surface as "black" with `ABSORB` everywhere: optimistic by orders of magnitude. Real black surfaces reflect 2–10 % (more in NIR).
- Forgetting the **lens edges** and **flat annuli** of lenses (the converter gives you the faces you need; assign them coatings/scatter too).
- Too high a Minimum Relative Ray Intensity: ghosts and importance-sampled rays vanish silently.
- Detector with `ABSORB` material inside the beam path when you want to see what happens after it (L02).
- Reading a single noisy pixel: use detector totals or regions, and quote ray counts.

## Worked example — stray-light budget for an 850 nm fringe projector

**Setup.** The L05 projection lens: 6 singlets (12 air–glass surfaces) plus a 2-surface DMD-side window → $N$ = 14 reflecting surfaces, glass $n$ = 1.5098 at 850 nm. Fringe period on the object 10.4 mm (16 DMD pixels of 0.65 mm at 1 m, L05), camera–projector baseline 150 mm at 1 m working distance.

**(a) Fresnel and ghost count.** $R_0 = (0.5098/2.5098)^2 = 0.04126$. Pairs: $\binom{14}{2} = 91$. Each double-bounce ghost carries $R_iR_j$:

| Coating per surface | $R$ | one ghost $R^2$ | sum of 91 ghosts $s$ | checkerboard CR $=(1+s/2)/(s/2)$ |
|---|---|---|---|---|
| uncoated | 4.13 % | 1.70 × 10⁻³ | 0.155 | ≈ 14 |
| visible broadband AR used at 850 nm | 1.0 % | 1.0 × 10⁻⁴ | 9.1 × 10⁻³ | ≈ 221 |
| NIR V-coat | 0.25 % | 6.25 × 10⁻⁶ | 5.7 × 10⁻⁴ | ≈ 3500 |

(Upper bound: assumes all ghost light lands in the image area spread uniformly and neglects transmission losses.) Fringe modulation with the 1 % AR: $C/C_0 = 1/1.0091 = 0.991$; uncoated: 0.866. Coatings are clearly necessary; whether 1 % or 0.25 % is needed depends on the *structured* errors below.

**(b) Structured error from a focused ghost.** Triangulation angle $\theta = \arctan(150/1000) = 8.53°$; depth per fringe period $p_z = 10.4/\tan\theta = 69.3$ mm. A ghost that re-images the DMD on the scene nearly in focus with relative amplitude $\varepsilon = R^2$:
- 1 % AR: $\delta\phi = \arcsin(10^{-4}) = 10^{-4}$ rad → $\delta z = 10^{-4}/(2\pi)\times 69.3 = 1.1\ \mu$m — negligible.
- uncoated: $\varepsilon = 1.70\times10^{-3}$ → $\delta z = 19\ \mu$m — visible in metrology-grade data.

**(c) The camera side with a glint.** Now the ghost source is a specular highlight $G = 300\times$ brighter than diffuse surfaces, and the camera lens ghost from it lands on a diffuse neighbour (assume the ghost is about as concentrated as the glint image, a worst case):
- 1 % AR: $\varepsilon = 300\times10^{-4} = 0.03$ → $\delta\phi = 0.030$ rad → $\delta z = 0.33$ mm.
- uncoated: $\varepsilon = 0.51$ → $\delta\phi = \arcsin 0.51 = 0.536$ rad → $\delta z = 5.9$ mm.
- 0.25 % V-coat: $\varepsilon = 1.9\times10^{-3}$ → $\delta z = 0.021$ mm.
This is why NIR-optimised coatings and ghost-focus control on the **receiver** pay off: the dynamic range of real scenes multiplies every ghost.

**(d) Barrel scatter.** Suppose 2 % of the illumination overfills the lens and hits a barrel wall patch 10 mm in front of a 4 mm-radius aperture (roughly facing it). Fraction of the patch's Lambertian scatter entering: $\sin^2\alpha = 4^2/(4^2+10^2) = 0.138$. Stray fraction $= 0.02\times\rho\times0.138$: black anodise ($\rho$ = 5 %) → 1.4 × 10⁻⁴; bare bead-blasted aluminium ($\rho \approx$ 30 %) → 8.3 × 10⁻⁴. Either is small compared with the 1 % AR ghost sum — but if the anodise reflects 30 % at 850 nm, blackening "on paper" is worth nothing. Measure NIR reflectance.

**(e) Lens-surface scatter (ABg).** Surfaces polished to $\sigma_h$ = 1.5 nm: TIS = $(4\pi\cdot1.5/850)^2 = 4.92\times10^{-4}$ each (conservative reflective formula). Fit an ABg with $g = 2$, $B = 10^{-3}$ (knee at $\arcsin\sqrt{B}$ = 1.8°): $A = \text{TIS}/[\pi\ln(1+1/B)] = 2.27\times10^{-5}$ sr⁻¹; plateau $A/B$ = 0.0227 sr⁻¹; BSDF at 10° = 7.3 × 10⁻⁴ sr⁻¹, at 30° = 9.0 × 10⁻⁵ sr⁻¹. Numerically integrating confirms TIS = 4.92 × 10⁻⁴, of which only 31 % lies within 5° of specular (3.8 % within 1°). Over 12 surfaces ≈ 0.6 % scattered — comparable to the 1 % AR ghost sum, but spread into a halo around bright features rather than uniform.

**(f) Simulation cost.** To see (d) without importance sampling: 10⁶ source rays → 2 × 10⁴ wall hits → 2 × 10⁵ scattered rays (10 per hit) → 13.8 % of them, ≈ 2.8 × 10⁴, enter the aperture: ≈ 0.6 % noise on the *total*, but spread over a 100 × 100-pixel detector that is ~3 rays per pixel — useless as an image. Importance sampling toward the aperture gains only π/Ω_p ≈ 7× here (the aperture is large as seen from the wall); it pays off for small targets (×100 at α = 5.7°, ×800 at 2°) and for surfaces many scatters deep.

## Key takeaways
- Stray light = unintended paths; the physics is BSDF × projected solid angle × incident power, evaluated over all paths — OpticStudio does this by Monte-Carlo ray splitting.
- Lambertian (BSDF = ρ/π), Gaussian (σ in direction-cosine space) and ABg ($A/(B+|x|^g)$) cover most needs; for ABg the TIS follows from $A,B,g$ (no scatter fraction), for the others you set the fraction.
- Smooth-surface scatter falls as $(\sigma_h/\lambda)^2$; NIR helps, but NIR also makes many "black" anodised parts reflective.
- Ghosts: $\binom N2$ double-bounce paths, each ≈ $R_iR_j$; coatings move ghost levels by orders of magnitude. Harm = energy × concentration × scene dynamic range.
- Uniform veil costs modulation ($C_0/(1+s)$); structured ghosts cost **phase**, up to $\arcsin\varepsilon$ — the critical failure for structured light.
- Workflow: sequential ghost screening → NSC with coatings and mechanics → ZRD + Path Analysis → fix the top paths → verify with contrast/VGI/phase metrics.
- Importance sampling makes scatter quantitative at small targets; lower Minimum Relative Ray Intensity, target a visible object slightly larger than it.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| BSDF / BRDF / BTDF | Scattered radiance per unit incident irradiance (sr⁻¹); for reflection / transmission |
| TIS | Total integrated scatter: fraction of incident power scattered into the hemisphere |
| Projected solid angle $\Omega_p$ | $\int\cos\theta\,d\Omega$; $\pi\sin^2\alpha$ for a cone of half-angle α; π for a hemisphere |
| Direction-cosine space, $\vec\beta-\vec\beta_0$ | Projection of scatter minus specular directions onto the surface; argument of Gaussian/ABg models |
| ABg model | $\text{BSDF} = A/(B+|x|^g)$: plateau $A/B$, knee at $B^{1/g}$, log–log slope $-g$ |
| Importance sampling | Aiming scattered rays at a target sphere and weighting them by the averaged BSDF |
| Scatter To | List of objects scattered rays must hit to be kept |
| Ghost | Specular, even-bounce reflection path from refractive surfaces reaching the detector |
| Path Analysis | Ranking of unique ray paths by power from a ZRD |
| Critical / illuminated surface | Surface seen by the detector / lit by the source; both → first-order stray path |
| Vane | Baffle fin inside a bore that blocks grazing-angle scatter |
| VGI | Veiling glare index (ISO 9358): black-patch image irradiance ratio, % |
| GSF | Glare spread function: normalised image of a small source including stray light |
| ANSI (checkerboard) contrast | White/black ratio on a 4×4 checkerboard; probes projector stray light |

## References
1. [Kenyon §11.1–11.4, pp. 297–303] — Rayleigh, Mie, coherent scattering, extinction law (eq. 11.10).
2. [Kenyon §9.6, eqs. 9.79–9.80, p. 247] — normal-incidence Fresnel reflectance; [Kenyon §9.7, p. 252] — single-layer MgF₂ AR coating.
3. [Kenyon §2.2.2, p. 39] — Porro prisms and the scatter-absorbing groove.
4. Ansys Optics KB, *Introduction to stray light analysis – Part 2* (ghosts, filter strings, Path Analysis) — <https://optics.ansys.com/hc/en-us/articles/42661744883091>
5. Ansys Optics KB, *Introduction to stray light analysis – Part 3* (mechanical scatter, CAD single-surface mode, `I.95` + Lambertian) — <https://optics.ansys.com/hc/en-us/articles/42661774807955>
6. Ansys Optics KB, introductory stray-light article (N. Herringer; why stray light is done in NSC) — <https://optics.ansys.com/hc/en-us/articles/43071117166867>
7. Ansys Optics KB, scatter models summary KA-01415 (formulas and limits for Lambertian, Gaussian, ABg, K-correlation, bulk) — <https://optics.ansys.com/hc/en-us/articles/42661773980563>
8. Ansys Optics KB, *Scatter To and Importance Sampling* (Size, Limit, target choice, efficiency) — <https://optics.ansys.com/hc/en-us/articles/43071055638419>
9. Ansys Optics KB, fitting the ABg model to partial BRDF data (1−TIS specular, fit procedure) — <https://optics.ansys.com/hc/en-us/articles/43071132421395>
10. Ansys Optics KB, multiple ABg profiles with `.ABGF` files (`ABG_DATA.DAT`, NM/WV/DT) — <https://optics.ansys.com/hc/en-us/articles/43071068163347>
11. Ansys Optics KB, tabular BSDF scatter data (Scatter Fraction = 1, Number of Rays, no extrapolation) — <https://optics.ansys.com/hc/en-us/articles/43071089490451>
12. Ansys Optics KB, K-correlation surface scatter model vs ABg — <https://optics.ansys.com/hc/en-us/articles/43071070893971>
13. OpticStudio Help, *The Filter String* — <https://ansyshelp.ansys.com/public////////Views/Secured/Zemax/v25101/en/OpticStudio_User_Guide/OpticStudio_Help/topics/The_Filter_String.html>
14. Ansys Optics KB, *How to Use Sequence Selector* (Premium/Enterprise, `SEQ[...]` filters) — <https://optics.ansys.com/hc/en-us/articles/49350853430163-How-to-Use-Sequence-Selector>
15. Ansys Optics KB, *Stray Light Analysis Overview* (OpticStudio → Speos workflow) — <https://optics.ansys.com/hc/en-us/articles/45146457845395-Stray-Light-Analysis-Overview>
16. Ansys Optics KB, smartphone-camera stray-light example (I.995 AR, spacer fix, SNR before/after) — <https://optics.ansys.com/hc/en-us/articles/9273272641555>
17. Ansys Optics KB, Ghost Focus Generator workflow — <https://optics.ansys.com/hc/en-us/articles/43071067483795>
18. Ansys Zemax community, *Absorptive and scattering surfaces in NSC* (MIRROR + IDEAL coating + Lambertian fraction; ABg specular) — <https://community.zemax.com/got-a-question-7/absorptive-and-scattering-surfaces-in-nsc-985>
19. Ansys Zemax community, *No rays are scattered when I use importance sampling* (lower Minimum Relative Ray Intensity) — <https://community.zemax.com/got-a-question-7/no-rays-are-scattered-when-i-use-importance-sampling-661>
20. Ansys Zemax community, *Filter string for ghost analysis* (`X_HITFACE2` per-face ghost filters) — <https://community.zemax.com/got-a-question-7/filter-string-for-ghost-analysis-3690>
21. M. Turner, *Stray light* lecture notes, Part 3, U. Arizona (BSDF, TIS, Lambertian 1/π, Gaussian σ ≤ 5) — <https://wp.optics.arizona.edu/jsasian/wp-content/uploads/sites/33/2019/10/Straylight-Part-3-Mary-Turner.pdf>
22. Optikos, *Stray Light Measurement* (ISO 9358 VGI and GSF definitions) — <https://www.optikos.com/wp-content/uploads/2020/07/Stray-Light-Measurement_07.01.2020.pdf>
23. E. Fest, *Stray Light Analysis and Control*, SPIE Press, 2013; J. C. Stover, *Optical Scattering: Measurement and Analysis*, SPIE Press — standard textbooks (not in corpus).
