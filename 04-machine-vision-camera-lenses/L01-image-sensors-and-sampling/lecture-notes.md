# L01 — Image sensors and sampling

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2.5 h, tasks ~4 h
> **Prerequisites:** Courses 01–03, in particular [01/L04 — stops, pupils, fields](../../01-foundations/L04-stops-pupils-fields/), [02/L13 — windows & plates](../../02-aberrations-classical-design/L13-eyepieces-afocal-relays-windows/), [03/L02 — MTF](../../03-image-quality-optimization/L02-mtf-theory-and-practice/) · **Next:** [L02 — Camera first-order design](../L02-camera-first-order-design/)

## Learning objectives
- Compute the Nyquist frequency of a sensor from its pixel pitch and convert between lp/mm, cycles/pixel and object-space resolution.
- Decode a sensor "optical format" (1/2.3", 1/1.8", 2/3", 1.1") into real active-area dimensions, and explain why the inch number is not a diagonal.
- Explain what the sensor's chief-ray-angle (CRA) specification and microlens shift mean, and what goes wrong when the lens CRA does not match.
- Estimate the photon budget, shot-noise-limited SNR and the effect of NIR quantum efficiency for a pixel, and know which numbers an EMVA 1288 datasheet gives you.
- Write an MTF-at-Nyquist specification that combines lens MTF, pixel-aperture MTF and margins, at visible and NIR wavelengths.
- Model a sensor cover glass correctly in OpticStudio and predict its focus shift.

## Reading
- **Core:** [Kenyon §15.7, pp. 461–466] — imaging arrays: CCD structure, quantum efficiency and colour (Bayer), microlens arrays, shot noise and dynamic range, CMOS arrays. Read it for the device physics; the numbers there (CCD-era, 10 µm pixels) are older than today's 2–6 µm CMOS pixels.
- **Core:** commonlands, "The Definition of Lens Chief Ray Angle and the dreaded CRA mismatch" — a clear, practical discussion of lens vs sensor CRA: <https://commonlands.com/blogs/technical/lens-chief-ray-angle-and-mismatch>
- **Core:** STMicroelectronics AN6472, "Lens CRA matching recommendations for optimal colorization" — a real sensor vendor's CRA spec and its ±5° guidance: <https://www.st.com/resource/en/application_note/an6472-lens-cra-matching-recommendations-for-optimal-colorization-stmicroelectronics.pdf>
- **Optional:** EMVA 1288 Release 4.0 (General and Linear) — the standard for characterising and reporting camera/sensor performance: <https://emva.org/wp-content/uploads/EMVA1288General_4.0Release.pdf>, <https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf>
- **Optional:** Edmund Optics application notes "Resolution" and "Pixel sizes and optics" (Imaging Resource Guide): <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/resolution/>, <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/pixel-sizes-and-optics/>
- **Optional:** Wikipedia, "Optical format" — the origin of the inch names: <https://en.wikipedia.org/wiki/Optical_format>

---

## 1. Why a lens designer must understand the sensor

In Courses 01–03 the image surface was a mathematical plane and "good" meant small spots or high MTF. In a camera the image is **sampled** by a grid of pixels, each of which integrates light over its area, sits under a microlens and a colour or NIR filter stack, and converts photons to electrons with a wavelength-dependent efficiency. Four consequences dominate everyday machine-vision lens design:

1. **Resolution is bounded by sampling.** There is no point correcting the lens far beyond what the pixel grid can record — but the lens must deliver contrast *at* the sampling limit, or the expensive pixels are wasted.
2. **The pixel accepts light only within a limited cone of angles.** Microlenses make CMOS sensors efficient, but only for rays that arrive at the angle the microlens was designed for. This couples the lens's exit-pupil position (its chief-ray angle) to the sensor.
3. **Photons are scarce.** Machine-vision cameras run short exposures (motion, eye-safe projector power, ambient-light suppression). F/# is chosen as a compromise between light, depth of field and diffraction (L02).
4. **There is glass in front of the sensor.** Cover glass and filters sit in a converging beam; they shift focus and can add aberration and ghosts (L08).

For a structured-light 3D camera such as Zivid's, add: the image is used for **measurement**, not for viewing. Contrast of the projected pattern at the relevant spatial frequency, geometric stability and signal-to-noise matter more than "pleasing" rendering.

## 2. Sensor architecture in one page

Kenyon describes the CCD in detail [Kenyon §15.7, pp. 461–466]; modern machine-vision cameras almost all use **CMOS active-pixel sensors**, where each pixel has its own transistors for charge-to-voltage conversion [Kenyon §15.7.4]. Two architecture distinctions matter for optics:

- **Front-side illuminated (FSI) vs back-side illuminated (BSI).** In FSI pixels the metal wiring sits between the microlens and the photodiode, forming a "well" a few µm deep; light must go down this tunnel, so angular acceptance is limited. BSI sensors put the photodiode on top (the wafer is thinned and illuminated from the back), giving higher QE and wider angular acceptance. Kenyon shows the factor-of-two QE gain of thinned back-illuminated CCDs [Kenyon §15.7.1, Fig. 15.21]; Sony's Pregius S global-shutter family (2.74 µm pixels) is a current BSI example and is marketed as tolerating higher incidence angles ([Teledyne FLIR, "Sony Pregius S"](https://www.teledynevisionsolutions.com/learn/learning-center/machine-vision/pregius-s/)).
- **Global vs rolling shutter.** Global-shutter pixels need an in-pixel storage node shielded from light, which eats area and makes microlenses essential [Kenyon §15.7.2 and p. 466]. Structured-light cameras typically need global shutter (the pattern and the exposure must be synchronised across the whole frame).

**Microlenses** concentrate light from the full pixel area onto the smaller photosensitive area [Kenyon p. 466]. Each microlens is a tiny lens with its own (small) acceptance cone. Light arriving too obliquely is focused onto the metal or into the neighbouring pixel: signal is lost (shading) and leaks into neighbours (crosstalk, which in a Bayer sensor becomes colour error).

**Fill factor** is the fraction of the pixel area that is effectively photosensitive (after microlenses, often close to 100 % for BSI). It determines the pixel-aperture MTF (Section 4).

## 3. Pixels, formats and the inch-name quirk

### 3.1 Pixel pitch and active area
The **pixel pitch** $p$ is the centre-to-centre spacing (usually equal in x and y). Typical values today: 1.0–2.0 µm (mobile), 2.2–3.45 µm (mainstream machine vision), 4.5–9 µm (high-sensitivity, high-dynamic-range sensors). Active area is simply

$$
W = N_x\,p,\qquad H = N_y\,p,\qquad D = \sqrt{W^2+H^2},
$$

with $N_x, N_y$ the pixel counts. Example: a 2448 × 2048 sensor with $p = 3.45$ µm (the IMX250 class) has $W = 8.45$ mm, $H = 7.07$ mm, $D = 11.0$ mm — a "2/3-inch" sensor.

The lens designer cares about the **image circle**: the lens must cover at least $D$ (plus a margin for sensor placement tolerance, typically 0.1–0.3 mm on the radius). In OpticStudio the full field is therefore normally specified as a real image height $D/2$ (Section 7).

### 3.2 The "optical format" naming
Sensor sizes are named like "1/2.3-inch" or "2/3-inch". These names come from the outer glass diameter of the **vidicon camera tubes** of the 1950s; the usable image on the tube's target was only about two thirds of that diameter. The convention survived into solid-state sensors: the nominal format is roughly 3/2 × the actual diagonal ([Wikipedia, "Optical format"](https://en.wikipedia.org/wiki/Optical_format)). In practice the industry uses **≈16 mm of diagonal per "inch"** for formats ≥ 1/2", and somewhat more (≈18 mm/inch) for small formats. Hence:

| Format name | Typical active area W × H (mm) | Diagonal (mm) | Notes |
|---|---|---|---|
| 1/2.3" | 6.17 × 4.55 | 7.7 | compact cameras, many M12 lenses |
| 1/2" | 6.4 × 4.8 | 8.0 | classic 4:3 |
| 1/1.8" | 7.18 × 5.32 | 8.9 | |
| 2/3" | 8.8 × 6.6 | 11.0 | classic machine-vision format |
| 1/1.2" | 11.25 × 7.03 | 13.3 | e.g. 16:10 global-shutter sensors |
| 1" | 12.8 × 9.6 | 16.0 | |
| 1.1" | ~14.1 × 10.3 | ~17.5 | 12 MP-class, 3.45 µm sensors |

These are *typical*; always take $W$ and $H$ from the actual datasheet ($N_x \cdot p$), never from the format name. A "1/2.3-inch" sensor has a diagonal of 7.7 mm, not 25.4/2.3 = 11.0 mm — the factor-of-1.4 confusion is a classic specification error when buying an off-the-shelf lens.

**Lens mount and back focus.** Machine-vision lenses use C-mount (flange focal distance 17.526 mm), CS-mount (12.526 mm) or S-mount/M12 (no standard flange; focus by thread). The mount constrains the mechanical back focal length and hence the lens form (L04, L05).

## 4. Sampling: Nyquist and what MTF "at Nyquist" means

### 4.1 Nyquist frequency
A grid of pitch $p$ can represent spatial frequencies up to

$$
\nu_N = \frac{1}{2p},
$$

the **Nyquist frequency** — one line pair (one bright plus one dark line) per two pixels. With $p$ in µm, $\nu_N\,[\text{lp/mm}] = 1000/(2p)$:

| $p$ (µm) | 1.55 | 2.0 | 2.74 | 3.45 | 5.86 |
|---|---|---|---|---|---|
| $\nu_N$ (lp/mm) | 323 | 250 | 182 | 145 | 85 |

In image-processing units Nyquist is 0.5 cycles/pixel. Frequencies above $\nu_N$ that the lens passes are **aliased**: they reappear as false low-frequency patterns (moiré). Machine-vision cameras rarely have an optical low-pass filter; the lens MTF and the pixel aperture are the only anti-aliasing.

### 4.2 Pixel-aperture MTF
A pixel integrates light over its sensitive width $a$ (with $a = p$ for 100 % fill factor). Integration over a rectangle is convolution with a rect function, so the pixel contributes an MTF factor

$$
\text{MTF}_\text{pix}(\nu) = \left|\frac{\sin(\pi a \nu)}{\pi a \nu}\right| .
$$

At Nyquist with $a = p$: $\text{MTF}_\text{pix}(\nu_N) = \sin(\pi/2)/(\pi/2) = 2/\pi = 0.637$. Even a perfect lens therefore delivers at most 64 % contrast at Nyquist after the pixel. In the NIR, photo-generated carriers are created deep in the silicon and diffuse sideways before being collected, which lowers the sensor MTF further (lateral diffusion / electrical crosstalk). Expect the effective pixel MTF at 850–940 nm to be noticeably below 0.64 at Nyquist; sensor vendors rarely publish it, so measure it (slanted edge).

### 4.3 Cascading MTFs
To first order, independent blurs multiply in frequency space:

$$
\text{MTF}_\text{system}(\nu) \approx \text{MTF}_\text{lens}(\nu)\cdot\text{MTF}_\text{pix}(\nu)\cdot\text{MTF}_\text{other}(\nu),
$$

where "other" includes motion, vibration, demosaicing and focus error. A common professional way to write a lens spec is **"lens polychromatic MTF ≥ X at $\nu_N$ (or $\nu_N/2$) over Y % of the field, at best focus and over the focus/temperature range"**. Typical targets for machine-vision lenses: MTF ≥ 0.3–0.5 at $\nu_N/2$ across the field, MTF ≥ 0.15–0.3 at $\nu_N$ on axis. Specifying at $\nu_N/2$ as well as $\nu_N$ is wise: contrast at Nyquist is fragile (it depends on phase between the pattern and the pixel grid), whereas $\nu_N/2$ is where measurement algorithms usually operate.

### 4.4 Diffraction sets a floor
From Course 03 L02, a diffraction-limited circular pupil has cutoff frequency $\nu_c = 1/(\lambda N)$ (image-space working F/# $N$) and MTF

$$
\text{MTF}_\text{diff}(\nu) = \frac{2}{\pi}\left[\arccos s - s\sqrt{1-s^2}\right],\qquad s = \nu/\nu_c .
$$

For $p = 3.45$ µm ($\nu_N = 145$ lp/mm):

| $\lambda$ | F/2.0 | F/2.8 | F/4 | F/5.6 |
|---|---|---|---|---|
| 0.55 µm | 0.80 | 0.72 | 0.60 | 0.45 |
| 0.85 µm | 0.69 | 0.57 | 0.40 | 0.20 |
| 0.94 µm | 0.66 | 0.53 | 0.34 | 0.13 |

Two lessons: (1) in the NIR diffraction bites much sooner — a lens that is "fast enough" at 550 nm may be diffraction-starved at 940 nm; (2) small pixels force fast lenses. L02 develops this into an F/# selection rule.

## 5. Chief-ray angle (CRA) and microlens shift

### 5.1 Lens CRA
The **lens CRA** at image height $h$ is the angle between the real chief ray and the surface normal of the (flat) image plane. To first order, if the exit pupil is a distance $d_{XP}$ in front of the image,

$$
\tan\text{CRA}(h) \approx \frac{h}{d_{XP}} .
$$

A distant exit pupil (image-space near-telecentric lens) gives small CRA; a compact lens with the stop near the sensor gives large CRA. Mobile-phone lenses have 25–35° CRA at the image corner; classic C-mount machine-vision lenses typically 0–15° ([commonlands](https://commonlands.com/blogs/technical/lens-chief-ray-angle-and-mismatch)). Real CRA curves are often non-linear and can peak *before* the corner, so always ask for (or compute) the full CRA-vs-image-height curve.

### 5.2 Sensor CRA (microlens shift)
To accept oblique light efficiently, sensor makers **shift each microlens** (and the colour filter) toward the array centre by an amount that grows with image height. The design value is published as the sensor's CRA specification: e.g. "0°" (centred microlenses, intended for telecentric lenses), "linear to 12° at the corner", or a vendor curve. The same silicon is often sold in several microlens-shift variants. The ST application note shows a sensor optimised for a linear CRA reaching 30° at the corner, with an acceptance band around it ([ST AN6472](https://www.st.com/resource/en/application_note/an6472-lens-cra-matching-recommendations-for-optimal-colorization-stmicroelectronics.pdf)).

Geometry gives a feel for the shift: if the microlens sits a height $t_s$ above the photodiode in a stack of index $n_s$, a ray at angle CRA in air is refracted to $\theta_s = \arcsin(\sin\text{CRA}/n_s)$ and lands displaced by $t_s\tan\theta_s$. With $t_s = 3$ µm, $n_s = 1.6$ and CRA = 25°: $\theta_s = 15.3°$, displacement 0.82 µm — a quarter of a 3.45 µm pixel. That is why mismatch matters.

### 5.3 Consequences of mismatch
- **Shading**: extra fall-off of signal toward the corners on top of the lens's own relative illumination (L03).
- **Colour shading / crosstalk**: on Bayer sensors, typically pink or green corners; worse in the red/NIR because crosstalk is wavelength dependent.
- **Lower corner MTF**: crosstalk spreads signal into neighbours.

Vendor guidance varies: ST recommends a lens within ±5° of the sensor CRA ([AN6472](https://www.st.com/resource/en/application_note/an6472-lens-cra-matching-recommendations-for-optimal-colorization-stmicroelectronics.pdf)); lens suppliers screen for roughly ±3° and stress that it is a screening rule, not an acceptance limit ([commonlands](https://commonlands.com/blogs/technical/lens-chief-ray-angle-and-mismatch)). Note that CRA is only the *centre* of the ray cone: a fast lens (F/1.8) delivers a cone of half-angle ≈ 15.5°, so the extreme rays are far off-axis even when the chief ray matches. Mismatch tolerance is therefore smaller at low F/#, and must be checked at the operating wavelength — an NIR pairing can behave differently from a visible one.

**Professional habit:** before designing, get the sensor's CRA curve and angular-response data (QE vs angle) from the vendor under NDA, and make "CRA within ±x° of sensor curve over 0–100 % field" a line in the spec (L03 shows how to put it into the merit function).

## 6. Photons, QE and noise — just enough

### 6.1 Quantum efficiency
**QE** $\eta(\lambda)$ is the fraction of incident photons that become collected electrons. Silicon absorbs blue light within a fraction of a µm [Kenyon §15.7.1] but NIR light needs tens of µm: the absorption length is ~20 µm at 850 nm and several tens of µm at 940 nm. A typical 3–5 µm-thick photodiode therefore loses much of the NIR. Typical numbers: peak QE 60–80 % (green), 20–40 % at 850 nm and 10–25 % at 940 nm for standard sensors; "NIR-enhanced" sensors (thicker epi, deep trench isolation, light-trapping pyramids) reach roughly double that. Always read the actual QE curve; it drives the choice between 850 nm (better QE) and 940 nm (less sunlight, invisible) illumination.

### 6.2 Photon budget and shot noise
The number of photons reaching a pixel of area $A_p = p^2$ in exposure time $t$ under image irradiance $E$ (W/m²) is

$$
N_\gamma = \frac{E\,A_p\,t\,\lambda}{hc},
$$

and the signal is $N_e = \eta N_\gamma$ electrons. Photon arrival is Poisson, so the **shot noise** is $\sqrt{N_e}$ [Kenyon §15.7.3]. With read (temporal dark) noise $\sigma_d$ electrons, the SNR is

$$
\text{SNR} = \frac{N_e}{\sqrt{N_e + \sigma_d^2}} .
$$

Image irradiance scales as $1/N^2$ (L02, L03), so halving the F/# quadruples $N_e$ and doubles the shot-limited SNR. For a structured-light camera, where projector power is limited by eye safety and thermal budget, this is a central system trade.

### 6.3 What EMVA 1288 gives you
The EMVA 1288 standard defines how to measure and report: quantum efficiency (at stated wavelengths), temporal dark noise (e⁻), saturation capacity (e⁻), absolute sensitivity threshold, dynamic range, dark current and its temperature dependence, and spatial non-uniformities (DSNU, PRNU) ([EMVA 1288 Release 4.0](https://emva.org/wp-content/uploads/EMVA1288General_4.0Release.pdf)). These are the numbers you need for the photon budget above; ask suppliers for EMVA 1288 data at your wavelength rather than marketing QE curves.

## 7. In OpticStudio

**Field definition.** For a camera lens with the object at a finite distance (e.g. 1 m), use *Real Image Height* fields (System Explorer → Fields) with the maximum equal to half the sensor diagonal plus margin; e.g. 0, 0.3, 0.5, 0.7, 0.85, 1.0 of $D/2$. Real Image Height requires ray aiming and iteration; it guarantees you design for the sensor, independent of distortion. For a first pass, *Paraxial Image Height* or *Object Angle* is faster; switch later. (If you want x/y asymmetric fields matching the 4:3 rectangle, add field points at the corners and on the x and y edges — Course 03 discusses field weighting.)

**MTF to Nyquist.** In the FFT MTF settings set "Maximum Frequency" to $\nu_N$ (or slightly above), and add $\nu_N/2$ as a reference. The lens MTF reported by OpticStudio does **not** include the pixel aperture — multiply by $\text{MTF}_\text{pix}$ yourself (Task 3) or use Image Simulation, which can include a pixel grid (location varies by version — search the ribbon for "Image Simulation"). In the merit function, MTFT/MTFS/MTFA (tangential/sagittal/average) target modulation at a given frequency and field.

**Cover glass.** The sensor package window (typically 0.4–0.7 mm of borosilicate glass, e.g. SCHOTT D 263 T eco, or N-BK7-like glasses) must be in the model: insert two surfaces before the image, set thickness and material, and leave the air gap to the die. A plate of thickness $t$ and index $n$ in a converging beam moves the paraxial focus *away* from the lens by

$$
\Delta z = t\left(1-\frac{1}{n}\right)
$$

[see Course 02 L13 on plane-parallel plates]. For $t = 0.5$ mm, $n = 1.517$: $\Delta z = 0.170$ mm — enormous compared with a depth of focus of ±10–20 µm. The plate also adds a little spherical aberration and (in fast, wide-angle beams) astigmatism, so it must be in the model *before* optimization, not added afterwards. If your catalog lacks the exact cover glass material, use the vendor's index or a near equivalent and note it.

**CRA readout.** The real chief-ray angle on the image surface is the merit-function operand **RAID** (real ray angle of incidence at a surface, in degrees, for given normalized field Hx, Hy and pupil Px = Py = 0). Put RAID rows at several field heights with zero weight to tabulate CRA; OpticStudio also has an incidence-angle-vs-image-height style analysis (location varies by version — search the ribbon / Help for "incident angle"). Remember to evaluate CRA at the *image surface* (after the cover glass the angle in air is the same as before the plate, because the plate is parallel).

**Wavelengths.** For a monochrome NIR camera use e.g. 0.84, 0.85, 0.86 µm (LED/VCSEL band) with weights matching the source spectrum × QE; for a visible camera F, d, C or a sensor-weighted set. Course 04 L08 treats bandwidth in detail.

## Worked example — what does a 2/3" 5 MP sensor demand from the lens?

**Given:** 2448 × 2048 pixels, $p = 3.45$ µm, 100 % fill factor, monochrome; lens F/2.8, used either at 0.55 µm or at 0.85 µm; scene at $z = 1$ m with a lens of $f = 8$ mm.

1. **Active area:** $W = 8.45$ mm, $H = 7.07$ mm, $D = 11.01$ mm → image circle ≥ 11.0 mm (design to e.g. 11.4 mm with placement margin).
2. **Nyquist:** $\nu_N = 1000/(2\cdot3.45) = 144.9$ lp/mm.
3. **Diffraction MTF at Nyquist (perfect lens):** $\nu_c = 1/(0.55\times10^{-3}\cdot2.8) = 649$ lp/mm → $s = 0.223$ → MTF$_\text{diff}$ = 0.718. At 0.85 µm: $\nu_c = 420$ lp/mm, MTF = 0.570.
4. **With the pixel:** $0.718 \times 0.637 = 0.457$ (visible), $0.570\times0.637 = 0.363$ (NIR, before carrier-diffusion losses). A real lens at 70–80 % of diffraction-limited MTF then gives a system MTF at Nyquist of only ~0.25–0.35 — this is why Nyquist-level specs need care.
5. **Object-space pixel footprint at 1 m:** magnification $m \approx f/(z-f)$, so one pixel sees $3.45\,\mu\text{m}\times(1000-8)/8 = 0.43$ mm on the object.
6. **Photon budget:** assume image irradiance $E = 0.1$ W/m², $t = 1$ ms. At 0.55 µm: $N_\gamma = 3.29\times10^3$, with $\eta = 0.65$, $N_e = 2141$ e⁻, $\sigma_d = 2.5$ e⁻ → SNR = 46. At 0.85 µm (same irradiance): $N_\gamma = 5.09\times10^3$ (more photons per joule), but with $\eta = 0.25$, $N_e = 1272$ e⁻ → SNR = 35.6.
7. **Cover glass:** 0.5 mm with $n = 1.517$ shifts focus by 0.170 mm; it must be in the lens file.

## Key takeaways
- Nyquist $\nu_N = 1/(2p)$; a 3.45 µm pixel samples to 145 lp/mm, a 2.74 µm pixel to 182 lp/mm.
- Format names ("2/3-inch") are vidicon-era labels ≈ 1.5 × the diagonal; take sizes from $N\cdot p$ on the datasheet.
- Even a perfect lens plus a 100 %-fill pixel gives at most 0.64 × MTF$_\text{diff}$ at Nyquist; NIR wavelengths lose more to diffraction and carrier diffusion.
- The sensor's CRA spec (microlens shift) is an optical interface requirement: match the lens CRA curve within a few degrees, at the operating wavelength and F/#.
- QE in the NIR is typically a third or less of the visible peak; photon budgets and F/# follow from it.
- Ask for EMVA 1288 data and the sensor CRA curve before starting a design.
- Always model the cover glass (and later the filter): a 0.5 mm plate moves focus by ~0.17 mm.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Pixel pitch $p$ | Centre-to-centre spacing of pixels |
| Nyquist frequency | $1/(2p)$, highest frequency a sampling grid can represent without aliasing |
| Aliasing / moiré | False low-frequency patterns from frequencies above Nyquist |
| Optical format | Legacy "inch" size name ≈ 1.5 × sensor diagonal |
| Fill factor | Effective photosensitive fraction of the pixel area |
| Microlens (shift) | On-chip lenslet per pixel, displaced toward the centre to accept oblique chief rays |
| CRA | Chief-ray angle of incidence at the image plane (lens) or the angle the microlenses are designed for (sensor) |
| QE | Quantum efficiency: collected electrons per incident photon |
| Shot noise | Poisson noise $\sqrt{N_e}$ of the photo-electron count |
| Temporal dark noise | Read-out noise, in electrons (EMVA 1288 term) |
| BSI / FSI | Back-/front-side illuminated pixel architecture |
| Global shutter | All pixels exposed simultaneously |
| EMVA 1288 | Standard for measuring and reporting camera/sensor performance |

## References
1. [Kenyon §15.7, pp. 461–466] — imaging arrays, QE and colour, CCD readout, noise and dynamic range, CMOS arrays, microlens arrays.
2. [Kenyon §15.7.1, p. 463, Fig. 15.21] — QE of front- vs back-illuminated silicon arrays.
3. commonlands, "The Definition of Lens Chief Ray Angle and the dreaded CRA mismatch" — lens vs sensor CRA, typical values, testing: <https://commonlands.com/blogs/technical/lens-chief-ray-angle-and-mismatch>
4. STMicroelectronics AN6472, "Lens CRA matching recommendations for optimal colorization" — a sensor CRA curve and ±5° matching rule: <https://www.st.com/resource/en/application_note/an6472-lens-cra-matching-recommendations-for-optimal-colorization-stmicroelectronics.pdf>
5. EMVA 1288 Release 4.0 General: <https://emva.org/wp-content/uploads/EMVA1288General_4.0Release.pdf> and Linear: <https://www.emva.org/wp-content/uploads/EMVA1288Linear_4.0Release.pdf> — how sensor QE, noise and saturation are defined and measured.
6. Teledyne FLIR, "Sony Pregius S Global Shutter CMOS" — BSI global shutter with 2.74 µm pixels: <https://www.teledynevisionsolutions.com/learn/learning-center/machine-vision/pregius-s/>
7. Edmund Optics, "Resolution" and "Pixel sizes and optics" application notes: <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/resolution/>, <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/pixel-sizes-and-optics/>
8. Wikipedia, "Optical format": <https://en.wikipedia.org/wiki/Optical_format>
9. Zemax Community, "Matching the lens CRA with imaging sensor CRA" (RAID for CRA, incident-angle analysis): <https://community.zemax.com/got-a-question-7/matching-the-lens-cra-with-imaging-sensor-cra-1584>
