# L08 — Filters, cover glass, NIR design and ghosts

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2.5 h, tasks ~4.5 h
> **Prerequisites:** [02/L13 — windows & plates](../../02-aberrations-classical-design/L13-eyepieces-afocal-relays-windows/), [03/L08 — coatings](../../03-image-quality-optimization/L08-polarization-and-coatings/), [L01](../L01-image-sensors-and-sampling/), [L03](../L03-relative-illumination-and-telecentricity/), [L04](../L04-compact-fixed-focus-lens-project/) · **Next:** [L09 — 3D-vision optics](../L09-3d-vision-optics-scheimpflug-stereo/)

## Learning objectives
- Compute the focus shift and the aberrations a plane-parallel plate (cover glass, filter, window) introduces in a converging beam, and model plates correctly in OpticStudio.
- Compute the blue shift of an interference filter with angle of incidence, $\lambda(\theta) = \lambda_0\sqrt{1-(\sin\theta/n_\text{eff})^2}$, and the broadening caused by a cone of rays.
- Choose a filter position (front window, near the stop, in the image-space cone, coated on a lens) and derive the required filter bandwidth from source drift, angles and tolerances.
- Design for NIR (850/940 nm): glass and coating choices, chromatic correction over a narrow band, focus offset between visible and NIR, diffraction penalty.
- Find and rank ghost paths with the Ghost Focus Generator and estimate ghost irradiance; know when to escalate to non-sequential analysis.

## Reading
- **Core:** [Geary Ch. 23, §23.3–23.6, pp. 251–259] — windows: focus shift $\Delta z = t(n-1)/n$ (Eq. 23.9), spherical aberration of a window in a converging beam (Seidel calculation), tilted windows, axial colour.
- **Core:** [Kenyon §9.7, pp. 249–254] — interference filters: multilayer transfer matrices, quarter-wave stacks, bandwidth of a high-reflector (Eq. 9.104), Fabry–Perot band-pass structure $(HL)^mHH(LH)^m$.
- **Online:** Syron Optics FAQ, "How can the effects of angle of incidence and half-cone angle on the transmission spectrum be calculated?" — the AOI formula, cone averaging, polarisation splitting above ~20°: <https://syronoptics.com/blogs/faqs/how-can-the-effects-of-angle-of-incidence-aoi-and-half-cone-angle-on-the-transmission-spectrum-be-calculated>
- **Online:** Edmund Optics, "Optical Filter Orientation": <https://www.edmundoptics.com.tw/knowledge-center/application-notes/optics/optical-filter-orientation/>
- **Online:** Ansys Optics KB, Ghost Focus Generator workflow (single/double-bounce ghosts, ghost lens files, GPIM optimization): <https://optics.ansys.com/hc/en-us/articles/43071067483795>
- **Optional:** Laser Focus World, "Optical analysis software automates ghost busting": <https://laserfocusworld.com/software-accessories/software/article/16547529/optical-analysis-software-automates-ghost-busting>

---

## 1. Plates in a converging beam

Every camera has at least one plane-parallel plate in the image-space cone: the sensor **cover glass**; usually also a **filter** (IR-cut for visible cameras, band-pass for NIR structured light), sometimes a **window** in front of the lens. In collimated space a perfect plate does nothing to image quality; in a converging beam it does [Geary §23.4]:

1. **Focus shift** (paraxial):

$$
\Delta z = t\,\frac{n-1}{n} = t\left(1-\frac1n\right)
$$

[Geary Eq. 23.9]. Geary's example: $t = 20$ mm of BK7 shifts focus by 6.81 mm. For camera plates: 0.5 mm cover glass → 0.17 mm; 0.3 mm filter → 0.10 mm.
2. **Spherical aberration** (overcorrected, positive $S_I$ in a converging beam) growing with $t$ and with the cone angle — Geary computes it surface by surface from the paraxial trace [Geary §23.4.2–23.4.3]. For a 0.5 mm plate at F/2.8 it is small but not negligible against a ±10 µm depth of focus at F/2; for thick windows in fast beams it dominates.
3. **Astigmatism and lateral colour** for off-axis beams, which cross the plate obliquely (CRA ≠ 0); a tilted plate adds astigmatism and coma even on axis [Geary §23.5].
4. **Axial colour**: $\Delta z$ depends on $n(\lambda)$ [Geary §23.6].

**Rule:** model every plate with its real thickness and material in the lens file *before* optimizing; let the optimizer correct its aberrations. Never "fold it into the back focus" with a shortened air gap — that corrects focus but not the aberrations, and the mechanical drawing will be wrong.

## 2. Interference filters and angle of incidence

### 2.1 How they work
A dielectric interference filter is a stack of quarter-wave layers of high- and low-index materials; reflection amplitudes from the interfaces add in phase, giving high reflectance over a band whose relative width for one pair type is $\Delta\lambda/\lambda_0 = \sin^{-1}[(u-u')/(u+u')]$ (Kenyon's notation for the layer admittances) [Kenyon §9.7.1, Eq. 9.104]. A **band-pass** filter is a Fabry–Perot cavity: two reflectors separated by a half-wave spacer, $(HL)^mHH(LH)^m$, transmitting a narrow band at the cavity resonance [Kenyon §9.7.1]. Real NIR band-pass filters stack several cavities for steep edges and add blocking layers for out-of-band suppression (OD 3–6).

### 2.2 The angle shift
At oblique incidence the phase thickness of every layer decreases ($\propto n_i d_i\cos\theta_i$), so the whole spectrum shifts **to shorter wavelengths**. For a collimated beam at angle $\theta$ (in air),

$$
\lambda(\theta) = \lambda_0\sqrt{1-\left(\frac{\sin\theta}{n_\text{eff}}\right)^2},
$$

where $n_\text{eff}$ is the filter's **effective index** (typically 1.45–2.1; higher for filters with high-index spacers) ([Syron Optics](https://syronoptics.com/blogs/faqs/how-can-the-effects-of-angle-of-incidence-aoi-and-half-cone-angle-on-the-transmission-spectrum-be-calculated)). Above ~20° the s and p polarisations shift by different amounts and the passband splits/broadens.

Shift of a 940 nm filter (nm):

| $\theta$ | 5° | 10° | 15° | 20° | 25° | 30° | 35° |
|---|---|---|---|---|---|---|---|
| $n_\text{eff}$ = 1.5 | −1.6 | −6.3 | −14.1 | −24.8 | −38.1 | −53.8 | −71.4 |
| $n_\text{eff}$ = 1.8 | −1.1 | −4.4 | −9.8 | −17.1 | −26.3 | −37.0 | −49.0 |
| $n_\text{eff}$ = 2.0 | −0.9 | −3.6 | −7.9 | −13.9 | −21.2 | −29.9 | −39.5 |

### 2.3 Cones
In a converging beam each image point receives a cone of half-angle $\alpha \approx \arctan(1/2N)$ (10.1° at F/2.8) centred on its CRA. The filter response is the average over the cone (weighted by the pupil illumination; for a uniformly filled circular pupil, by solid angle). The result: the passband **shifts blue, broadens, its edges soften and peak transmission drops**. Rule of thumb for a cone centred on normal incidence: the centre shift is roughly half the edge-ray shift.

## 3. Where to put the filter

| Position | AOI seen by the filter | Pros | Cons |
|---|---|---|---|
| **Front window** (object space) | full field angle (±30–45°) per image point, collimated per field | protects lens; easy to swap; no focus impact | large; huge spectral shift across the field → needs wide passband or the image edge is cut off |
| **Near the stop** (inside the lens) | each field point: one angle ≈ chief-ray angle at the stop (≈ field angle × pupil magnification⁻¹) | small diameter | spectrum varies across the field; needs space at the stop; the plate in a non-collimated space adds aberration |
| **Image-space cone** (in front of the sensor) | CRA ± cone half-angle | small, standard; with near-telecentric image space every pixel sees the **same** cone → uniform spectrum | focus shift; ghosts with sensor; dust shadows near focus |
| **Coated onto a lens surface** | local AOI varies with surface slope and field | no extra surfaces, compact | coating uniformity on curved surfaces; AOI hard to control; expensive to change |

For a narrow band-pass NIR camera, the image-space position with **low CRA** (L03) is the usual professional choice: the filter sees angles 0 → CRA + α, the same everywhere if CRA ≈ 0.

**Bandwidth budget** for a band-pass filter (half-widths, add linearly for worst case):
1. Source centre tolerance and spectral width (LED FWHM ~30–50 nm; VCSEL ~1–2 nm).
2. Source thermal drift: LEDs ~0.2–0.3 nm/K, VCSELs ~0.06–0.07 nm/K (check datasheets) → over 0–50 °C, ~10–15 nm (LED) vs ~3.5 nm (VCSEL).
3. Filter angle shift over the maximum AOI (§2.2, with cone broadening).
4. Filter manufacturing tolerance on centre wavelength (±2–5 nm typical for good NIR filters) and its own (small) temperature drift.
Make the passband just wide enough: every extra nanometre admits ambient light (sunlight, factory lighting), which reduces the pattern contrast.

## 4. Designing for the NIR

- **Glass dispersion is lower in the NIR**: for N-BK7 the focal shift of an $f = 8$ mm singlet across 840–860 nm is only 5.6 µm, versus 125 µm across F–C. A narrow-band NIR lens needs little colour correction — but it is **not** focused where the visible design is: the same singlet's focus moves by 0.136 mm from 0.55 to 0.85 µm. A lens corrected in the visible must be refocused (and re-optimized) for 850 nm; a lens that must work at both (e.g. a colour texture channel and an NIR pattern channel through the same optics) needs explicit dual-band correction with an apochromat-like glass strategy (Course 02 L07).
- **Diffraction is worse** (L01–L02): Airy diameter ∝ λ; at 940 nm the same F/# delivers ~70 % more blur than at 550 nm. NIR systems need faster lenses or bigger pixels for the same MTF.
- **Coatings**: specify the AR band to include the operating line; a visible-optimised broadband AR can reflect noticeably more at 850–940 nm, increasing ghosts and losses. With ~6–12 air–glass surfaces, 1 % vs 0.25 % per surface changes total transmission by ~5–8 % and ghost levels by an order of magnitude (ghost ∝ product of two reflectances).
- **Glass choice**: internal transmission of most optical glasses is excellent at 850–940 nm; some high-index lanthanum/titanium glasses and cements have reduced transmission or bulk absorption features — check the catalogue transmission data at your thickness. Plastics: check C–H overtone absorption (L07).
- **Sensor**: QE falls (L01), pixel crosstalk grows (MTF falls), and CRA sensitivity may change — validate the sensor-lens pairing at the operating wavelength.
- **Wavelength set in OpticStudio**: e.g. 0.840, 0.850, 0.860 µm with weights from (source spectrum × filter × QE); for a VCSEL, a single wavelength plus ±(drift) configurations.

## 5. Ghosts

### 5.1 What makes a ghost harmful
A ghost is light reflected twice (or an even number of times) at surfaces and then reaching the sensor. Its harm depends on how much energy and how **concentrated** it is at the sensor:
- Energy fraction ≈ $R_iR_j$ for the two bouncing surfaces (e.g. 0.5 % × 0.5 % = 2.5 × 10⁻⁵ for good AR; 4 % × 4 % = 1.6 × 10⁻³ for uncoated glass).
- A ghost that **focuses near the image plane** concentrates that energy into a small spot → visible artefact (bright point, false structured-light feature). A ghost that is strongly defocused spreads into a faint veiling glare.
- **Flat surfaces near focus** (filter, cover glass, sensor) are dangerous: the sensor itself reflects several percent or more. A ghost bouncing sensor → filter → sensor is defocused by twice the gap: blur diameter ≈ $2d/N$; with $d$ = 1 mm at F/2.8, a 0.71 mm diameter halo around every bright point.
- Curved surfaces concave toward the image can refocus ghosts near the sensor — the Ghost Focus Generator finds these.

For a structured-light 3D camera, ghosts are particularly nasty: a projected pattern stripe reflected from a shiny part makes a bright spot whose ghost can create a false pattern feature and thus a false 3D point.

### 5.2 Ghost Focus Generator (sequential)
*Analyze → (Reports/Tools; location varies by version) → Ghost Focus Generator*. It converts pairs of refracting surfaces to reflecting ones and traces the resulting ghost systems for single- or double-bounce ghosts, reporting for each surface pair where the ghost focuses (near the pupil = pupil ghost; near the image = image ghost), and can save each ghost path as a separate lens file for further analysis ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/43071067483795)). Workflow from the KB:
1. Run in double-bounce mode; sort by ghost focus distance from the image; flag pairs whose ghost focuses within a few mm of the image or has a small spot there.
2. Open the worst ghost files and run a Geometric Image Analysis to estimate ghost irradiance relative to the main image (with the ghost reflector coating set to your real AR).
3. Fix by changing curvatures of the offending surfaces (the GPIM operand can push ghost image distances away during optimization, while you watch MTF), by coatings, or by tilting the filter slightly (a few degrees moves its ghost off-axis but adds astigmatism and spectral shift).
Limitations: coordinate breaks and some special surfaces are not handled, and all surfaces are assumed to have the same coating ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/43071067483795)).

### 5.3 When to go non-sequential (Premium)
For multiple bounces, TIR, mechanical scatter (barrel walls, spacers, flanges), real coatings per surface and the sensor's reflectance, convert the lens to NSC (Course 05 L06–L07) and trace with ray splitting and path analysis. This is the professional standard for final stray-light sign-off of a camera.

## 6. In OpticStudio

- **Plates:** two Standard surfaces with the plate material; keep them as separate surfaces even if thin. Use the real vendor index if known (cover glass glasses such as D 263 T eco or similar; if missing in your catalogue, use a *Model glass* with the vendor's $n_d$, $V_d$ — Course 01 L05).
- **Filter spectral behaviour:** sequential ray tracing ignores filter spectra unless you attach a coating. Options: an ideal/table coating with angle-dependent transmission on the filter surface, then *Polarization → Transmission* or the coating analyses (*Transmission vs. Angle / vs. Wavelength*; location varies by version) — or do the AOI → wavelength shift calculation in Python from a table of real-ray AOIs. To get the AOIs, use **RAID** at the filter surface for the chief ray and for marginal rays (Px, Py = ±1) at several fields.
- **Wavelength weights** from source × filter × QE.
- **Ghosts:** Ghost Focus Generator (sequential); NSC with ray splitting for final checks.
- **NIR multi-config:** wavelength configurations for source drift; focus compensator check between visible and NIR builds.

## Worked example — choosing filter position and bandwidth for a 940 nm structured-light camera

**Given:** VCSEL projector at 940 nm ± 2 nm (production), drift 0.07 nm/K over 0–50 °C (calibrated at 25 °C); filter $n_\text{eff}$ = 1.8, centre tolerance ±3 nm; receiver lens F/2.8 (cone half-angle α = 10.1°), full field ±30° in object space; two lens options: (A) CRA up to 15°, (B) near-telecentric CRA ≤ 3°.

1. **Front-window filter:** edge of field at 30° → shift −37.0 nm (and s/p splitting). The passband would need to be ~40+ nm wide → lets in a lot of ambient light. Rejected.
2. **Image-space filter, lens A:** worst-case AOI = 15° + 10.1° = 25.1° → edge-ray shift −26.5 nm; centre field: up to 10.1° → −4.5 nm. Spectral response differs between centre and edge of the image: the corners see a broader, bluer, weaker passband.
3. **Image-space filter, lens B:** max AOI ≈ 13.1° → edge-ray shift ≈ −7.5 nm; nearly uniform across the field. (On axis, the cone-averaged shift is ≈ −2.2 nm — half the −4.5 nm of the edge ray, as the rule of thumb says.)
4. **Bandwidth for lens B** (half-widths): source ±2 + drift ±1.75 (25 ± 25 K × 0.07) + filter ±3 + angle (averaged over the cone, the effective centre shifts by ≈ −2.3 nm on axis and ≈ −2.6 nm at CRA 3°, and the blue side broadens): specify a normal-incidence centre ≈ 2.5 nm to the red of 940 nm and a FWHM of roughly 20 nm. (Exact design: average the filter curve over the cone at each field — Task 2.)
5. **Lesson:** telecentric-ish image space buys a narrower filter → better ambient-light rejection → better 3D data outdoors and under factory lights. CRA is a *system* parameter, not only a sensor-matching detail.

## Key takeaways
- A plate in a converging beam shifts focus by $t(1-1/n)$ and adds spherical aberration (and astigmatism off-axis); model it explicitly.
- Interference filters shift blue with angle: $\lambda = \lambda_0\sqrt{1-(\sin\theta/n_\text{eff})^2}$; cones broaden and soften the passband; s/p split above ~20°.
- Put narrow band-pass filters where the AOI range is small and uniform — in the image-space cone of a low-CRA lens.
- Budget the passband: source tolerance + thermal drift + angle shift + filter tolerance; no wider than needed.
- NIR: little chromatic spread within a narrow band, but a large focus offset from the visible; diffraction and coatings must be re-checked at the NIR line.
- Ghost harm = energy × concentration; flat surfaces near the sensor and surfaces concave toward the image are the usual suspects; use Ghost Focus Generator, then NSC.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Cover glass | Protective window of the sensor package |
| IR-cut filter | Short-pass filter blocking NIR for visible imaging |
| Band-pass filter | Transmits a narrow band (e.g. 940 ± 10 nm); Fabry–Perot cavity stack |
| Effective index $n_\text{eff}$ | Single index describing a filter's angle shift |
| Blue shift | Shift of a filter's spectrum to shorter wavelengths with AOI |
| Half-cone angle | $\arctan(1/2N)$, angular half-width of the image-side beam |
| Ghost (image/pupil) | Even-bounce reflection reaching the sensor, focused near the image/pupil |
| Veiling glare | Low-level diffuse light from defocused ghosts and scatter |
| GPIM | Merit-function operand for ghost image location (used to push ghosts away) |

## References
1. [Geary Ch. 23, §23.3–23.6, pp. 251–259] — windows: focus shift, spherical aberration, tilted windows, axial colour.
2. [Kenyon §9.7, pp. 249–254] — interference filters, multilayer analysis, Fabry–Perot band-pass.
3. Syron Optics, AOI and half-cone angle effects on filter spectra: <https://syronoptics.com/blogs/faqs/how-can-the-effects-of-angle-of-incidence-aoi-and-half-cone-angle-on-the-transmission-spectrum-be-calculated>
4. Edmund Optics, "Optical Filter Orientation": <https://www.edmundoptics.com.tw/knowledge-center/application-notes/optics/optical-filter-orientation/>
5. Ansys Optics KB, Ghost Focus Generator workflow: <https://optics.ansys.com/hc/en-us/articles/43071067483795>
6. Laser Focus World, "Optical analysis software automates ghost busting": <https://laserfocusworld.com/software-accessories/software/article/16547529/optical-analysis-software-automates-ghost-busting>
