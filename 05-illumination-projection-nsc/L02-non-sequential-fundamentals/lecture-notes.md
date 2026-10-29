# L02 — Non-Sequential Fundamentals

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3 h, tasks ~4–5 h
> **Prerequisites:** [L01 — Radiometry, photometry and étendue](../L01-radiometry-photometry-etendue/lecture-notes.md); [Course 01 L06 — real rays and analysis tools](../../01-foundations/L06-real-rays-and-analysis-tools/lecture-notes.md) · **Next:** [L03 — Source modelling: LEDs and lasers](../L03-source-modeling-leds-and-lasers/lecture-notes.md)

## Learning objectives
- Explain what changes when OpticStudio switches from sequential to non-sequential ray tracing, and decide which mode a given problem needs.
- Build a non-sequential system in the Non-Sequential Component Editor (NSCE) from a source, a lens object and a detector, using global coordinates and reference objects correctly.
- Distinguish layout rays from analysis rays, and choose ray counts and detector pixel counts from a target noise level ($\sigma/\mu \approx 1/\sqrt{N_{\text{rays/pixel}}}$).
- Predict and verify the energy bookkeeping of a ray trace with and without *Use Polarization* and *Split NSC Rays*, including Fresnel losses and ghost rays.
- Read the Detector Viewer correctly (total power, peak irradiance, hits, units) and identify lost energy from thresholds and errors.
- Save rays to a Ray Database (.ZRD) and isolate ray families with filter strings (`Hn`, `Gn`, `X_GHOST`, path filters).

## Reading
- **Core:** Ansys Optics knowledge base, tutorial on basic operations in Non-Sequential Mode (N.-H. Kim) — the canonical "first NSC system" walkthrough (parabolic reflector, filament source, light pipe, detector): <https://optics.ansys.com/hc/en-us/articles/42661713082899>
- **Core:** Ansys Optics, *Detectors in illumination systems* — pixel count vs. ray count vs. noise: <https://optics.ansys.com/hc/en-us/articles/42661774340243>
- **Core:** OpticStudio Help, *The Filter String* (complete list of filter flags): <https://ansyshelp.ansys.com/public////////Views/Secured/Zemax/v25101/en/OpticStudio_User_Guide/OpticStudio_Help/topics/The_Filter_String.html>
- **Core (physics):** [Kenyon §9.6, pp. 245–248] — Fresnel equations; the 4 % reflectance of an uncoated glass surface at normal incidence is the origin of every "ghost" ray in this lesson. [Kenyon §2.2, p. 37] — total internal reflection, which NSC handles automatically.
- **Optional:** Ansys Optics, *How to locate geometry errors* (part I) — reading error messages, *Create Error Ray*, Ray Database Viewer: <https://optics.ansys.com/hc/en-us/articles/42661758842387>
- **Optional:** Ansys Optics, *Not enough segments or intersections allocated* — why ray splitting explodes memory: <https://optics.ansys.com/hc/en-us/articles/42661833236755>
- **Optional:** Ansys Optics article on filter strings with ray databases (KA-01508, scatter/wavelength filters): <https://optics.ansys.com/hc/en-us/articles/42661949492755>

---

## 1. Why a second ray tracer?

Everything you did in Courses 01–04 was **sequential**: rays visit surfaces 1, 2, 3, … in the order of the Lens Data Editor rows, exactly once each. That assumption is what makes sequential tracing fast and makes pupils, fields, aberration theory and derivative-based optimization possible. It is also exactly wrong for:

- **Illumination optics** — light pipes and TIR collimators, where a ray may reflect off the side walls 0, 3 or 11 times depending on where it started.
- **Stray light and ghosts** — the 4 % reflection from each uncoated surface goes *backwards*, possibly reflects again, and reaches the sensor by a path no LDE could describe.
- **Scatter** — a ray hitting a rough housing spawns a fan of scattered rays in random directions.
- **Extended, real sources** — an LED die with a phosphor layer and a dome, a filament, a VCSEL array; these are not "fields" with a "pupil".
- **Complex mechanical geometry** — mounts, baffles, the DMD package window, CAD parts.

In **non-sequential (NSC)** mode, objects are placed in 3-D space and each ray simply goes to whatever it hits next. The software intersects each ray with every object (accelerated by spatial partitioning), decides what happens at the interface (refraction, reflection, TIR, absorption, scatter, diffraction, splitting), and continues until the ray leaves the system, is absorbed, or falls below an energy threshold. Rays carry **power**, and detectors accumulate it — the bookkeeping of L01 becomes an explicit Monte-Carlo simulation.

| | Sequential | Non-sequential |
|---|---|---|
| Ray order | fixed by surface number | determined by geometry |
| Unit of description | surfaces (LDE rows) | 3-D objects (NSCE rows), possibly CAD |
| Rays | defined by field and pupil coordinates | launched by sources with a spatial & angular distribution, random or quasi-random |
| Typical output | aberrations, MTF, spot | irradiance, intensity, radiance, colour, power on detectors |
| Speed | very fast; analytic derivatives possible | slow; results are noisy (Monte Carlo) |
| Optimization | DLS, smooth merit functions | noisy merit functions; orthogonal descent preferred (L06) |

A professional uses both: design the imaging lens sequentially, then import it into an NSC model (or a *mixed-mode* model, L06) to study illumination, stray light and ghosts with the real mechanics around it.

**Edition note.** NSC is in the Professional and Premium editions. Premium adds, among other things, the advanced stray-light and illumination tools you will use later in this course; you have everything needed.

## 2. Anatomy of the Non-Sequential Component Editor

Switch a new file to non-sequential mode (Setup tab → *Non-Sequential* mode; the KB tutorial phrases it *Setup → System → Non-Sequential*). The Lens Data Editor is replaced by the **Non-Sequential Component Editor (NSCE)**. Each row is an **object**. The first columns are common to all objects:

| Column | Meaning |
|---|---|
| Object Type | Standard Lens, Standard Surface, Rectangular Volume, Annulus, Source Ellipse, Detector Rectangle, … (double-click the cell, or the object-properties panel at the top) |
| Comment | free text — name things ("LED", "Condenser", "DMD plane") |
| Ref Object | the object whose local coordinate system this object's position is relative to (0 = global; −1 = the previous object) |
| Inside Of | which object a source or object is embedded in (e.g. an LED die inside a silicone dome) |
| X, Y, Z Position; Tilt About X, Y, Z | placement in the reference coordinate system (lens units, degrees) |
| Material | blank = the surrounding medium (air), a glass name (N-BK7), `MIRROR`, or `ABSORB` |
| Par 1 … Par n | object-specific parameters (radii, thicknesses, ray counts, pixel counts) — hover over the column header to see each parameter's name |

Points that trip up every newcomer:

- **Positions are absolute, not thicknesses.** There is no "thickness to next surface". A lens at Z = 10 and a detector at Z = 111.7 are 101.7 mm apart regardless of the lens thickness. Use *Ref Object* to build assemblies that move together (e.g. reference the detector to the lens), and **pickup solves** to tie parameters together (the KB tutorial ties a detector's Z position to a light-pipe length this way).
- **Object order in the editor does not matter for tracing** — except that sources must be defined before they are used and that nesting rules apply when volumes overlap: if two volumes overlap, the object with the *higher* row number takes precedence in the overlap region (OpticStudio's nesting rule; check *Object Properties* in Help for details). Most of the time, simply avoid overlapping solids.
- **Objects have faces.** A Standard Lens has a front face, back face and edge (face numbers 1, 2, 0 in typical use); coatings, scatter and filter strings can be assigned per face (Object Properties → *Coat/Scatter*).
- **Volumes vs. surfaces.** A Standard Lens or Rectangular Volume is a closed solid with a material inside. A Standard Surface or Annulus is a single surface with no volume; use `MIRROR` or `ABSORB` on it, or leave it blank to make it "invisible" except for detectors and filter strings.
- **Detector material.** A detector with blank material is transparent: rays pass through and are recorded. With `ABSORB` it records and stops them. Choose deliberately — a transparent detector placed in front of a lens records both the forward light and the light reflected back by the lens.

### 2.1 Sources (preview of L03)
Every source shares the first parameters: **# Layout Rays**, **# Analysis Rays**, **Power** (in source units: W or lm), **Wavenumber** (0 = polychromatic using all system wavelengths and weights; *k* = only wavelength *k*), and **Color #** (for drawing). The rest describe the spatial and angular emission:

- *Source Point*, *Source Ellipse*, *Source Rectangle* — the workhorses. Source Ellipse and Source Rectangle emit from an area; their angular distribution is set by *Source Distance* (apparent point source behind or in front of the emitting area; per Ansys staff, a source distance of 0 with the default distribution parameters gives a collimated beam), *Cosine Exponent* ($I \propto \cos^n\theta$, n = 1 Lambertian — L01 Task 2) and Gaussian angular parameters *Gx, Gy*.
- *Source Gaussian*, *Source Diode* (laser diodes, L03), *Source Filament*, *Source File* / *Source Radial* / *Radiant Source* (measured LED data, L03), *Source Two Angle*, and many more.

### 2.2 Detectors
- **Detector Rectangle** — the main tool. Parameters: X/Y half width, # X/Y pixels, data type. It records in **space** (irradiance: W/area, or lux in photometric units) *and* simultaneously in **angle** (radiant intensity in W/sr for rays crossing it; this is meaningful only if the detector is in the far field of the source — see L01 §6). It also stores coherent amplitude data if you need it.
- **Detector Color** — like Detector Rectangle with spectral/colour data (CIE coordinates, true-colour display). Use it for multi-LED visible projectors.
- **Detector Polar** — a spherical "dome" in angle space: intensity vs. (θ, φ). Use it to characterise a source or a collimator's far field.
- **Detector Volume** — 3-D voxels recording absorbed or incident flux (e.g. heating inside a lens).
- **Detector Surface** — wrap a detector over the shape of another object's surface.

## 3. Rays: layout vs. analysis, and Monte-Carlo noise

Each source has two ray counts:

- **# Layout Rays** — drawn in the NSC 3D Layout / Shaded Model only. A dozen to a few hundred.
- **# Analysis Rays** — traced when you run a ray trace from *Ray Trace Control*. Only analysis rays deposit energy on detectors (the KB tutorial is emphatic: layout rays never affect the Detector Viewer).

Each analysis ray starts with power $P/N$ ($P$ = source power, $N$ = number of analysis rays). A detector pixel receiving $k$ rays reports $kP/(N\,A_{\text{pix}})$. Because $k$ is Poisson-like, the relative noise is

$$
\frac{\sigma}{\mu} \approx \frac{1}{\sqrt{k}}, \qquad k \approx \frac{N\,\eta_{\text{det}}}{N_{\text{pix,lit}}}
$$

where $\eta_{\text{det}}$ is the fraction of rays reaching the detector and $N_{\text{pix,lit}}$ the number of illuminated pixels. Ansys's detector article gives the canonical example: a 10 × 10 detector needs ~10⁵ rays for ~3 % noise; going to 100 × 100 pixels needs 100× more rays for the same noise; ~2 % is about as well as you can measure in the lab anyway.

Design consequences:

- **Choose pixels for the question.** A uniformity spec over a 20 × 12 grid needs 20 × 12 pixels, not 500 × 500.
- **Total power on a detector is very precise** (it averages over all pixels); peak irradiance is noisy and biased *upwards* by noise — never optimize on a single pixel without interpolation/smoothing (L06).
- **Sobol (quasi-random) sampling** is available on many sources and converges faster than pure random for smooth distributions; the NSC optimization KB article uses it for the best signal-to-noise per ray.
- **Multi-core**: the ray trace is parallel; ray counts of 10⁶–10⁸ are routine on a workstation.

## 4. What happens at an interface: polarization, Fresnel and ray splitting

At an uncoated air–glass interface at normal incidence the power reflectance is [Kenyon §9.6, pp. 245–248]

$$
R = \left(\frac{n_2-n_1}{n_2+n_1}\right)^2 ,
$$

4.1 % for N-BK7 at 850 nm ($n = 1.5098$), rising with angle of incidence and different for s and p polarization. How OpticStudio treats this depends on two switches in the *Ray Trace Control* dialog (Analyze → Ray Trace):

| *Use Polarization* | *Split NSC Rays* | Behaviour |
|---|---|---|
| off | off | No Fresnel losses: refractive surfaces transmit 100 %. Rays follow the "most likely" path: refraction, or TIR if beyond the critical angle. Fast; fine for layout and first-order illumination checks. |
| on | off | Fresnel/coating transmission and bulk absorption are computed and the ray's energy is reduced accordingly; the reflected energy is simply discarded. Correct throughput, no ghosts. |
| on | on | At each interface the ray **splits** into a reflected and a transmitted child, each carrying its share of power. Ghosts, back-reflections and multiple reflections appear. Slowest, but the only way to see stray light. |
| off | on | Rays still split; Help describes how the split ratios are computed in this case — prefer polarization on whenever you split. |

Splitting creates trees. If every interface splits a ray in two, after $n$ intersections a single launched ray has produced $2^{n+1}-1$ segments [Ansys KB, *Not enough segments…*]. With 8 surfaces that is 511 segments per launched ray. OpticStudio keeps this under control with stopping rules set in *System Explorer → Non-Sequential*:

- **Minimum Relative Ray Intensity** / **Minimum Absolute Ray Intensity** — child rays below this fraction of the launched power (or below this absolute power) are terminated. Their energy is reported as *lost to threshold*. A relative value of 10⁻³–10⁻⁴ is typical for illumination; stray-light work may need 10⁻⁶ or lower (and much longer traces).
- **Maximum Intersections Per Ray** and **Maximum Segments Per Ray** — hard limits on tree size. Hitting them is an error you must not ignore: rays are traced depth-first, so a truncated tree can miss *high-energy* branches, not only weak ones (Ansys KB). Raise the limit as needed (each segment costs ~140 bytes of RAM).
- **Glue Distance** — tolerance for deciding that two surfaces touch (e.g. a cemented doublet built from two lens objects).

(Exact labels can vary slightly between releases; all live in the Non-Sequential section of System Explorer.)

### 4.1 Where did the energy go? Lost energy
After a trace, the energy launched by the sources must equal: energy absorbed by objects (including `ABSORB` detectors) + energy that left the system without hitting anything ("lost" into space) + energy lost to thresholds + energy lost to errors. OpticStudio reports threshold and error losses in absolute units (W). Rules:

- **Error energy should be ~0.** Geometry errors (rays that cannot be traced — invalid object placement, sources straddling a volume boundary, unclosed CAD solids) are logged; *Setup → Create Error Ray* reproduces a failing ray as a *Source Ray* object so you can see it (Ansys KB, geometry errors part I).
- **Threshold energy** should be small compared with the effects you care about. If you are studying 10⁻⁴-level ghosts, a 10⁻³ threshold is meaningless.
- **Rays that miss everything** are usually most of the "loss" in an early model — put a big transparent detector (or an absorbing "box" around the system) to see where it goes.

### 4.2 Total internal reflection
TIR needs no switch: if Snell's law has no real solution the ray reflects with 100 % efficiency. This is what makes light pipes, TIR collimators and prisms work (L04) — and what traps light inside an LED chip (L03).

## 5. Ray Database files and filter strings

A ray trace can save every ray segment to a **Ray Database** (`.ZRD`) file (*Save Rays* in Ray Trace Control). A ZRD records for each segment: which object and face it hit, position, direction, power, wavelength, and flags (reflected, transmitted, scattered, diffracted, ghost, …). You can:

- **Inspect it** with the *Ray Database Viewer* (Analyze tab) — every segment of every ray, with an asterisk marking where a ray terminated.
- **Replay it** into the Detector Viewer with a **filter string**, so that the detector shows only a family of rays, without re-tracing. The KB recommends: save *all* rays, filter afterwards; filtering during the trace makes a smaller file but throws data away permanently.
- **Script it**: ZPL keyword `ZRDPLAYBACK` and the ZOS-API *Ray Database Reader* (Course 07) give programmatic access.

### 5.1 Filter-string grammar
A filter string is a Boolean expression of **flags** joined with `&` (and), `|` (or), `^` (xor), `!` (not) and parentheses. From the OpticStudio Help page *The Filter String* (n = object number, optional .f = face):

| Flag | Selects rays that … |
|---|---|
| `Hn` | hit object n |
| `Mn` | missed object n |
| `Ln` | had their *last* segment hit object n |
| `Gn` | were ghost-reflected from object n (reflections from refractive objects, with splitting on) |
| `Rn`, `Tn` | reflected / transmitted at object n (but use `Gn` to isolate reflected *branches* when splitting) |
| `Sn`, `Fn` | scattered at object n (on the ray / on the split child) |
| `Dn`, `En` | diffracted at object n |
| `On` | originated at source n |
| `Wn` | started with wavelength n |
| `X_GHOST(n,b)` | ghosted exactly b times and hit object n (n = 0: any object) |
| `X_HIT(n,b)` | hit object n exactly b times |
| `X_SCATTER(n,b)` | scattered exactly b times and hit object n |
| `X_TIR(n,v)` | TIR'd at object n v times |
| `~007018009` | path filter: source 7 → object 18 → object 9 (3-digit object numbers) |

Examples you will use: `H5` (everything reaching the condenser, object 5), `!G2` (exclude ghosts from the lens, object 2), `X_GHOST(0,2)` (all second-generation ghosts — the classic two-reflection ghost image), `H3 & !G2` (rays reaching detector 3 that were never ghost-reflected by object 2). Test every string on a simple model before trusting it. Filter strings fail silently if typed with non-ASCII spaces (a reported gotcha with non-English keyboard layouts).

In Premium, **Path Analysis** (L07) automates this by listing every unique path rays took and its power — the natural next step after hand-written filters.

## 6. The Detector Viewer

Open it from the Analyze tab (*Detectors → Detector Viewer*). Settings worth knowing:

- **Detector** — which detector object; **Show As** — greyscale/false colour/cross-section/text.
- **Show Data** — incoherent irradiance (spatial), radiant intensity (angular), coherent irradiance/phase, radiance (position or angle space) — not all detectors offer all types.
- **Smoothing** and **Ray Database** / **Filter** fields (to replay a ZRD).
- The text below the plot (or the *Text* tab) lists **Peak Irradiance**, **Total Power** and **Total Hits** (rays) — read these every time. Total Hits divided by lit pixels is your $k$ in §3.

In the 3D Layout or Shaded Model, *Color Pixels By Last Analysis* paints detector results onto the detector object — a nice sanity check that the light lands where you think.

**Units.** *System Explorer → Units* sets source units (Watts, Lumens, Joules) and analysis units (e.g. W/cm² or W/m²). Many first models are "off by 10⁴" because of cm² vs m².

## 7. A sane workflow for every NSC model

1. **Sketch the system and decide the question**: throughput? uniformity? stray light? Each needs different detectors and switches.
2. **Units and wavelengths first** (System Explorer).
3. **Build geometry with layout rays only**; look at the NSC 3D Layout and Shaded Model from several angles. Are the rays doing what you expect?
4. **Add detectors** sized for the question, and **name everything** in the Comment column.
5. **First analysis trace** with polarization off, no splitting, ~10⁵ rays. Check total power on detectors against a hand estimate (L01).
6. **Turn on polarization**, then splitting, raise ray counts, check the lost-energy report.
7. **Save rays to a ZRD** whenever you will want to ask "where did this light come from?"
8. **Converge**: double the ray count; if the answer changes more than your tolerance, you did not have enough rays.

## 8. In OpticStudio — quick reference

| Task | Where |
|---|---|
| Switch to NSC | Setup tab → Non-Sequential mode |
| Units, wavelengths | Setup → System Explorer → Units / Wavelengths |
| NSC stopping rules | System Explorer → Non-Sequential |
| Insert/edit objects | Non-Sequential Component Editor (Insert key adds a row) |
| Object faces, coatings, scatter, draw options | Object Properties (button at top of NSCE) |
| Layout | Analyze → NSC 3D Layout; Shaded Model |
| Ray trace | Analyze → Ray Trace (Ray Trace Control: Clear & Trace, Use Polarization, Split NSC Rays, Scatter NSC Rays, Ignore Errors, Save Rays, Filter) |
| Detector results | Analyze → Detector Viewer |
| Ray-by-ray inspection | Analyze → Ray Database Viewer |
| Error ray | Setup → Create Error Ray |

(Menu groupings move between releases; if a command is not where this table says, use the ribbon search box.)

## Worked example — energy bookkeeping through an uncoated singlet

**System.** Wavelength 850 nm, units mm, source units W.

| # | Object | Settings |
|---|---|---|
| 1 | Source Ellipse | X/Y half width 10 mm (Ø 20 mm), collimated (Source Distance 0, Cosine Exp 0), Power 1 W, Z = 0 |
| 2 | Standard Lens, N-BK7 | Z = 10; Radius 1 = 50.98 mm, Radius 2 = 0 (flat), Thickness 5 mm, clear semi-diameters 12.5 mm |
| 3 | Detector Rectangle, ABSORB | Z = 10 + 5 + 96.69 = 111.69 mm (paraxial focus), half widths 0.5 mm, 101 × 101 pixels |

**Hand calculation.**

1. $n_{\text{N-BK7}}(0.85\ \mu\text{m}) = 1.50984$ (Sellmeier, SCHOTT coefficients). A plano-convex lens with the curved side to the collimated beam has $f = R_1/(n-1)$, so $R_1 = 0.50984 \times 100 = 50.98$ mm for $f = 100$ mm.
2. Back focal distance from the flat face: $f - t/n = 100 - 5/1.50984 = 96.69$ mm.
3. Real rays: a marginal ray at $y = 10$ mm crosses the axis 100.56 mm behind the front vertex instead of 101.69 mm (exact trace in Python) — 1.13 mm of longitudinal spherical aberration. The geometric blur radius at the paraxial focus is therefore ≈ 1.13 × (10/100) ≈ 0.11 mm, so a 1 mm detector is big enough, and the best focus lies ~0.5–0.8 mm in front of the paraxial focus.
4. Fresnel reflectance per surface (normal incidence): $R = (0.50984/2.50984)^2 = 4.13\ \%$. Transmission through two surfaces: $(1-R)^2 = 91.9\ \%$. A double-bounce ghost (reflect at back face, reflect again at front face, then go forward) carries $R^2 = 0.17\ \%$ of the power.

**What OpticStudio should report on detector 3 (total power):**

| Ray trace settings | Expected total power on detector |
|---|---|
| Polarization off, no splitting | ≈ 1.000 W (all rays refracted, 100 % transmission) |
| Polarization on, no splitting | ≈ 0.919 W (slightly less: off-axis rays at the curved face see a little more than 4.13 %) |
| Polarization on, splitting on | ≈ 0.919 W **plus** a small part of the 0.17 % double-bounce ghost that happens to land on the 1 mm detector (the ghost is strongly defocused there, so only a tiny fraction does) |

And the remaining ≈ 8 %? It is reflected backwards, mostly by the first surface, and leaves the system: with no object to hit, it is counted as lost into space. Put a large transparent Detector Rectangle at Z = 5 between source and lens and you will see the back-reflected 8 % — that is the experiment of Task 3.

**Noise budget.** With 10⁶ analysis rays and the spot covering a disc of ~0.1 mm radius on 10 µm pixels (~300 lit pixels), each lit pixel gets ~3000 hits: 2 % noise. Doubling the pixel count per axis would cost 4× the rays for the same noise.

## Key takeaways
- NSC ray tracing follows physics, not a surface list: it is the tool for illumination, stray light, ghosts, scatter and real sources — at the price of Monte-Carlo noise and slower tracing.
- Objects are placed by absolute position (or relative to a *Ref Object*); there are no thicknesses. Name objects, use pickups and reference objects to keep assemblies consistent.
- Only analysis rays reach detectors. Noise per pixel ≈ $1/\sqrt{\text{hits per pixel}}$; choose pixel count for the question and ray count for the noise.
- *Use Polarization* gives correct Fresnel/coating losses; *Split NSC Rays* adds the reflected branches (ghosts). Splitting grows as $2^{n+1}-1$ segments — control it with intensity thresholds and segment limits.
- Always check the energy bookkeeping: detector totals vs. hand estimates, lost energy to thresholds and errors (errors should be ~0).
- Save rays to a ZRD and use filter strings (`Hn`, `Gn`, `X_GHOST`, path filters) to ask "where did this light come from?".

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Non-sequential (NSC) ray tracing | Rays interact with whatever object they hit next, any number of times, in any order |
| NSCE | Non-Sequential Component Editor: one row per object |
| Ref Object / Inside Of | Coordinate reference object / enclosing object for nested sources or volumes |
| Layout rays / Analysis rays | Rays drawn in layouts / rays traced to accumulate detector data |
| Ray splitting | Creating reflected and transmitted child rays at each interface |
| Ghost | Light that reaches a detector after unintended (Fresnel) reflections |
| Minimum Relative Ray Intensity | Threshold below which child rays are terminated |
| Lost energy | Energy not accounted for on objects: to thresholds, errors, or leaving the system |
| ZRD | Ray Database file of all traced ray segments |
| Filter string | Boolean expression of flags selecting ray families from a trace or ZRD |
| Detector Viewer | Analysis window showing detector data (irradiance, intensity, radiance, colour) |

## References
1. [Kenyon §9.6, pp. 245–248] — Fresnel equations, normal-incidence reflectance.
2. [Kenyon §2.2, p. 37] — total internal reflection.
3. Ansys Optics KB, tutorial on basic operations in Non-Sequential Mode — <https://optics.ansys.com/hc/en-us/articles/42661713082899>
4. Ansys Optics KB, *Detectors in illumination systems* — <https://optics.ansys.com/hc/en-us/articles/42661774340243>
5. OpticStudio Help, *The Filter String* — <https://ansyshelp.ansys.com/public////////Views/Secured/Zemax/v25101/en/OpticStudio_User_Guide/OpticStudio_Help/topics/The_Filter_String.html>
6. Ansys Optics KB, filter strings with Ray Database files, scatter & wavelength filters (KA-01508) — <https://optics.ansys.com/hc/en-us/articles/42661949492755>
7. Ansys Optics KB, *How to locate geometry errors* (part I) — <https://optics.ansys.com/hc/en-us/articles/42661758842387>
8. Ansys Optics KB, *Not enough segments or intersections allocated* — <https://optics.ansys.com/hc/en-us/articles/42661833236755>
9. Ansys Optics KB, *Using ZRDPLAYBACK to filter non-sequential ray data* — <https://optics.ansys.com/hc/en-us/articles/43071100384787>
10. Ansys Zemax community, *How to separate ghost rays* (practical `X_HIT`/`Gn` filter examples) — <https://community.zemax.com/got-a-question-7/how-to-separate-ghost-rays-3251>
