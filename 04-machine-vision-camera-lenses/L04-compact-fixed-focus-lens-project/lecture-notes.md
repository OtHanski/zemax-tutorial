# L04 — Project: a compact fixed-focus machine-vision lens

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2 h, tasks ~10–12 h (two weekly sessions)
> **Prerequisites:** [L01](../L01-image-sensors-and-sampling/), [L02](../L02-camera-first-order-design/), [L03](../L03-relative-illumination-and-telecentricity/), [02/L09 — Cooke triplet](../../02-aberrations-classical-design/L09-cooke-triplet/), [02/L10 — double Gauss](../../02-aberrations-classical-design/L10-symmetric-lenses-double-gauss-vignetting/), [03/L04 — merit functions](../../03-image-quality-optimization/L04-merit-function-mastery/), [03/L05 — global search](../../03-image-quality-optimization/L05-optimization-strategies-and-global-search/) · **Next:** [L05 — Wide-angle and distortion mappings](../L05-wide-angle-and-distortion-mappings/)

## Learning objectives
- Write a complete, testable optical specification for a fixed-focus camera lens, derived from the sensor and the application.
- Do the first-order layout (focal length, F/#, field, track budget, back-focus stack with filter and cover glass) before touching glass.
- Choose and justify a design form (triplet, Tessar, triplet + field flattener, double-Gauss derivative) using aperture × field and the "small lenses are easier" scaling argument.
- Build a camera-lens merit function: image quality + first-order constraints + mechanical constraints + CRA, distortion and RI controls.
- Run a staged optimization (aperture/field ramping, element addition, Hammer) and recognise when to change the form rather than the weights.
- Produce the standard analysis set and a one-page design summary that another engineer can review.

## Reading
- **Core:** [Kidger Ch. 10, pp. 199–208] — the triplet: thin-lens Seidel theory, an optimized f = 50 mm F/4 ±22° example whose MTF is "only just acceptable" at F/4, glass choice, vignetting.
- **Core:** [Geary Ch. 30, pp. 343–353] — triplet design philosophy (power split, Petzval sum from equal-and-opposite powers, symmetry; stop near the negative element), image compactness.
- **Revisit:** your own triplet and double-Gauss work in Course 02 L09–L10.
- **Optional:** Edmund Optics, "Understanding Lens Specifications" (PDF; how machine-vision lens specs are written): <https://www.imveurope.com/sites/default/files/EO_Understanding_Lens_Specifications_Oct%2020th_Final.pdf>
- **Optional:** commonlands, lens CRA article (re-read the testing section): <https://commonlands.com/blogs/technical/lens-chief-ray-angle-and-mismatch>

---

## 1. The project

You will design an **M12/S-mount-class, all-glass, fixed-focus lens** for a 1/1.8"-type global-shutter sensor, focused at 1 m — the kind of lens that sits in a compact industrial camera or the colour/texture channel of a 3D camera. It is a realistic first professional design: small, fast, wide-ish, with a real back-focus stack.

### 1.1 Specification (v1.0)

| Item | Requirement | Notes / derivation |
|---|---|---|
| Sensor | 2048 × 1536, $p$ = 3.45 µm, active 7.07 × 5.30 mm, diag 8.83 mm (sensor B of L01) | |
| Image circle | Ø 9.0 mm ($h_\max$ = 4.5 mm) | +0.09 mm radial margin for sensor placement |
| Effective focal length | 8.0 mm ± 2 % | |
| Aperture | F/2.8 (infinity F/#) | light budget, L02 |
| Object distance | 1000 mm from the first lens vertex (design), depth of field 0.77–1.43 m at $c = 2p$ | L02 |
| Wavelengths | 0.486, 0.588, 0.656 µm, weights 1 : 2 : 1 (visible, IR-cut filter in system) | |
| Total track (first vertex → image) | ≤ 20.0 mm | |
| Back-focus stack | last lens vertex → image ≥ 4.0 mm, containing: IR-cut filter 0.30 mm, sensor cover glass 0.50 mm (both modelled as N-BK7 unless the vendor index is known), cover glass 0.40 mm above the die | the filter and cover glass shift focus by 0.102 and 0.170 mm |
| Max lens diameter | ≤ 11 mm clear aperture (fits M12 × 0.5 barrel) | |
| MTF (polychromatic, at the 1 m design focus) | ≥ 0.45 at 72 lp/mm ($\nu_N/2$) on axis; ≥ 0.30 T and S at 72 lp/mm up to 0.9 field; ≥ 0.20 at 145 lp/mm ($\nu_N$) on axis | lens only; the pixel MTF multiplies on top (L01) |
| Distortion | \|F-tan θ distortion\| ≤ 2.0 % over the field | calibrated in software, but must be smooth |
| Relative illumination | ≥ 0.50 at full field (with real apertures, geometric) | L03 |
| CRA | lens CRA within ±5° of sensor CRA (linear, 0° → 15° at 4.42 mm); hence ≤ 20° everywhere | L01, L03 |
| Glass | catalogue glasses from one vendor (SCHOTT), no more than 4 different glass types, avoid glasses with poor climate/stain resistance where possible | |
| Mechanical | centre thickness ≥ 0.8 mm (positive) / ≥ 0.6 mm (negative), edge thickness ≥ 0.6 mm, air gaps ≥ 0.1 mm, no surface with semi-aperture/radius > 0.8 | manufacturability |
| Environment (stretch) | −10 … +50 °C with ≤ 10 µm focus shift relative to the barrel | L07, Course 03 L09 |

A real spec would also cover ghosting, stray light, coatings, weight, cost and tolerances (Course 06). For this project, note them as "TBD in later lessons" — but write the lines, because forgetting them is the most common spec failure.

### 1.2 First-order numbers (verified)
- Magnification at 1 m: $m = 8/992 = 0.00806$; object field 876 × 657 mm; the image moves 0.065 mm behind the infinity focus (L02).
- Full-field half angle: ≈ 29.4° (at infinity, $\arctan(4.5/8)$); at 1 m the object height is 558 mm.
- EPD = 2.857 mm.
- Airy diameter at 0.588 µm, F/2.8: 4.0 µm ≈ 1.2 pixels; diffraction MTF at 72 lp/mm ≈ 0.86 and at 145 lp/mm ≈ 0.72 (L01) — the specification leaves room for ~0.3–0.5 of aberration losses.
- Depth of focus (geometric, $c = p$): ±$N c$ = ±9.7 µm. Fixed-focus assembly must hit focus to ~±5 µm (active alignment, Course 06 L07).

## 2. Choosing the design form

### 2.1 Difficulty measures
Two quick numbers locate a lens on the "difficulty map":

- **Aperture × field**: compare $\tan\theta/N$. Kidger's triplet (F/4, ±22°): 0.10. Our lens (F/2.8, ±29.4°): 0.20 — twice as demanding in this crude metric [Kidger §10.2].
- **Scale**: geometric aberrations scale linearly with the lens size; diffraction does not. Kidger's 50 mm triplet, scaled to 8 mm (×0.16), has spots 0.16 times smaller, so its "just acceptable" MTF at 30 cycles/mm becomes the same MTF at 30/0.16 = 187 lp/mm. **Small lenses are easier** — which is why mobile-phone lenses at F/1.8 ±38° are possible at all.

The two effects partly cancel: a triplet *might* just meet the on-axis spec but will struggle at 0.7–1.0 field (astigmatism, field curvature and lateral colour grow fast with field). Expect to need four or five elements with all-spherical glass.

### 2.2 Candidate forms
1. **Cooke triplet** [Geary Ch. 30; Kidger Ch. 10] — the minimum form that can correct all Seidel aberrations and colour [Geary §30.1]. Start here to learn where it fails.
2. **Tessar** — triplet with the rear positive element replaced by a cemented doublet: better lateral colour and astigmatism.
3. **Triplet + field flattener** — a negative element near the image lowers the Petzval sum and makes the image-side chief rays steeper (bad for CRA!) — watch the CRA spec.
4. **Double-Gauss derivatives** (5–6 elements) — the classic answer at F/2 and below; symmetric around the stop, so coma, distortion and lateral colour are naturally small (Course 02 L10). Compactness and CRA are the difficulty.
5. **Front-stop forms** — stop at or before the first element, like phone cameras: compact and low cost, but CRA is large unless the rear group acts as a field lens; usually needs aspheres (L07).

The **CRA ≤ 20° and track ≤ 20 mm** constraints favour forms with the stop in the *front half* (exit pupil far from the image). The stop-in-the-middle triplet gives CRA ≈ field angle (≈ 29°, L03 Task 3) and will violate the spec unless reshaped. That tension — compactness vs CRA vs correction — is the heart of the project.

## 3. Building the model

### 3.1 System setup
- **Aperture:** Entrance Pupil Diameter 2.857 mm (or Image Space F/# 2.8, but with a finite object EPD is cleaner). Turn **ray aiming** on (Paraxial is enough to start; Real for the final check).
- **Fields:** start with *Object Angle* (0, 10, 20, 25, 29.4°) for speed; switch to *Real Image Height* (0, 1.35, 2.25, 3.15, 4.05, 4.5 mm) in session 2 so that the field is guaranteed to fill the sensor regardless of distortion.
- **Object:** thickness of surface 0 = 1000 mm.
- **Back-focus stack** as explicit surfaces: … last lens → air (variable, ≥ 1.5 mm) → IR filter 0.30 N-BK7 → air 0.5 → cover glass 0.50 N-BK7 → air 0.40 → IMA. Make the gap before the filter the focus variable (or a marginal-ray-height solve).
- Put a **dummy surface** at the front lens vertex reference if the object distance must be measured from a mechanical datum.

### 3.2 Starting point
Use your Course 02 L09 triplet (f = 50 mm, F/4, ±20°). Scale it to f = 8 mm (*Make Focal* or *Scale Lens* tools on the Lens Data Editor/Setup ribbon — location varies by version), then increase field and aperture in steps: (F/4, 20°) → (F/3.5, 24°) → (F/2.8, 29.4°), re-optimizing at each step. This **aperture/field ramping** keeps the optimizer in a sensible basin. Alternative starting points: a scaled Tessar or double Gauss from the OpticStudio samples, or a patent (Course 03 L10).

### 3.3 Merit function
Build it in three blocks:

1. **Image quality** — Optimization Wizard: RMS spot radius, centroid reference, Gaussian quadrature 3 rings × 6 arms, all fields, all wavelengths. (Later switch to RMS wavefront or add MTF operands; spot is robust far from the solution.)
2. **First-order & mechanical** — `EFFL` = 8.0; `TOTR` ≤ 20 (via `OPLT` on TOTR, or TOTR target with a boundary); last-lens-to-filter gap ≥ 1.5 (`CTGT`); glass boundary constraints from the Wizard (min/max centre and edge thickness); `MNCA`/`MNEA` for air gaps; clear aperture ≤ 5.5 mm semi-diameter (e.g. `MXSD` if available in your version, or fixed semi-diameters plus vignetting checks).
3. **Camera-specific** — `DIMX` ≤ 2 % (max distortion; check that its field argument covers the full field); `RAID` on the image surface at Hy = 0.5, 0.7, 1.0 bounded by `OPLT` 20° (later: the ±5° window around the sensor curve, L03); `RELI` at full field ≥ 0.5 (weight low, check-only at first).

Keep a **dashboard block** (weight 0) at the top: EFFL, WFNO, TOTR, EXPP, PMAG, DIMX, RAID at full field, RELI at full field. You will look at it a hundred times.

### 3.4 Optimization strategy
1. Optimize radii only → add thicknesses/air → add glass (model glass or substitution, Course 03 L05) → Hammer.
2. If the merit function stalls with one aberration dominating (look at the Seidel diagram), **change the form**: split the strongest element, cement a doublet for colour, add a field flattener. Adding weight to a dominant operand rarely fixes a form problem.
3. Watch for the classic camera-lens traps: elements shrinking to knife edges, the stop drifting into a lens, the optimizer "solving" CRA by increasing distortion, or "solving" RI by growing elements beyond the barrel.
4. Before declaring victory: re-check with Real Image Height fields, real ray aiming, fixed semi-diameters (+0.2 mm mechanical margin), and the full analysis set.

## 4. The analysis checklist (camera lens)

| # | Analysis | What you check |
|---|---|---|
| 1 | Cross-Section / 3D Layout | form, clearances, ray paths through filter & cover glass |
| 2 | Prescription Data / System Data | EFL, WFNO, pupils, TOTR, glasses |
| 3 | Ray Fan + OPD Fan (all fields) | residual aberration types; vignetting |
| 4 | Standard Spot Diagram (with Airy disc) | spot vs Airy vs pixel |
| 5 | FFT MTF vs frequency (to 145 lp/mm) | spec at 72 and 145 lp/mm |
| 6 | FFT MTF vs field (at 72 and 145 lp/mm) | uniformity, T vs S |
| 7 | Through-Focus MTF at 72 lp/mm | depth of focus, field-curvature balance |
| 8 | MTF at near and far object distance (Multi-Configuration) | depth of field claim (0.77–1.43 m) |
| 9 | Field Curvature / Distortion; Grid Distortion | distortion ≤ 2 %, shape (monotonic, no wiggles) |
| 10 | Lateral Color | ≤ 1 pixel (3.45 µm) over the field |
| 11 | Relative Illumination | ≥ 0.5 |
| 12 | CRA table (RAID) vs sensor curve | within ±5° |
| 13 | Footprint diagram, edge thickness check | manufacturability, apertures |
| 14 | Seidel diagram | which surfaces carry the load (sensitivity hint) |
| 15 | Quick sensitivity look (optional: Tolerance → default tolerances, sensitivity only) | is any surface hopelessly sensitive? (Course 06) |

## 5. Design report (one page + appendix)

1. **Spec vs achieved** table (every line of §1.1, with PASS/FAIL and margin).
2. Layout picture, prescription table (radius, thickness, glass, clear aperture).
3. MTF vs field plot and through-focus summary; distortion, RI and CRA curves vs their spec windows.
4. Design-form rationale (why this form; what you tried and rejected).
5. Risks and next steps: tolerances, thermal focus shift, ghosts from filter/cover glass (L08), cost drivers (glass count, steep surfaces, cemented doublets).

## Worked example — first-order sanity check of the spec

1. $f = 8$ mm, $N = 2.8$ → EPD = 2.857 mm. ✓
2. $h_\max = 4.5$ mm → $\theta_\max = \arctan(4.5/8) = 29.4°$ (infinity) ✓; object field at 1 m: $7.07/0.00806 = 876$ mm × $5.30/0.00806 = 657$ mm.
3. Back-focus: plates add 0.102 (filter) + 0.170 (cover glass) = 0.272 mm of focus shift relative to air; the 4.0 mm minimum stack is physical length, so the *air-equivalent* back focus is ≈ 3.73 mm — use real surfaces, not a reduced air gap, in the model.
4. Diffraction: $\nu_c = 1/(0.5876\,\mu\text{m}\cdot2.8) = 608$ lp/mm; MTF$_\text{diff}$ = 0.85 at 72 lp/mm and 0.70 at 145 lp/mm (d-line). The 0.45 / 0.30 / 0.20 targets therefore demand a lens at roughly 50–70 % of diffraction-limited MTF at mid-field — realistic for 4–6 spherical elements at this scale.
5. CRA: a linear 0 → 15° sensor curve to 4.42 mm with ±5° tolerance means lens CRA at 4.42 mm between 10° and 20°: $d_{XP}$ between $4.42/\tan20° = 12.1$ mm and $4.42/\tan10° = 25.1$ mm from the image. With TTL ≤ 20 mm and a ≥ 4 mm back focus, the exit pupil must sit in the front two thirds of the lens: **put the stop in front of the middle**.

## Key takeaways
- Write the whole spec first, including the lines you will not solve today; derive each number (L01–L03).
- Model the filter and cover glass as real plates from the start; they move focus by ~0.27 mm here.
- Aperture × field ($\tan\theta/N$) and scale tell you the needed complexity: small lenses are easier; wide, fast lenses need more elements.
- Compactness, CRA and correction pull against each other; stop position is the main lever.
- Ramp aperture and field; change the form when one aberration dominates.
- Use a dashboard of zero-weight operands (EFFL, WFNO, TOTR, EXPP, DIMX, RAID, RELI).
- Finish with real image-height fields, real ray aiming, fixed apertures and the full analysis checklist.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| M12 / S-mount | 12 mm × 0.5 mm thread lens mount common for small cameras; focus by thread, no standard flange distance |
| TTL / total track | First lens vertex to image distance (TOTR in OpticStudio) |
| Back-focus stack | Filter, cover glass and air between the last lens and the die |
| IR-cut filter | Interference filter blocking NIR for visible cameras (L08) |
| Aperture/field ramping | Optimizing at reduced aperture and field, then increasing in steps |
| Dashboard operands | Zero-weight operands used only to display key values |
| Design form | The arrangement and number of elements (triplet, Tessar, double Gauss, …) |

## References
1. [Kidger Ch. 10, pp. 199–208] — triplet theory, example, glass choice, vignetting.
2. [Geary Ch. 30, pp. 343–353] — triplet philosophy and design procedure, image compactness.
3. Edmund Optics, "Understanding Lens Specifications" (via Imaging & Machine Vision Europe): <https://www.imveurope.com/sites/default/files/EO_Understanding_Lens_Specifications_Oct%2020th_Final.pdf>
4. commonlands, "Lens chief ray angle and mismatch": <https://commonlands.com/blogs/technical/lens-chief-ray-angle-and-mismatch>
5. Ansys Optics KB KA-01552 (EXPP/RECI, RANG for telecentricity control): <https://optics.ansys.com/hc/en-us/articles/42661811743251>
