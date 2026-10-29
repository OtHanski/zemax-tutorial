# L03 — Source Modelling: LEDs, Laser Diodes and VCSEL Arrays

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3 h, tasks ~4–5 h
> **Prerequisites:** [L01 — Radiometry, photometry and étendue](../L01-radiometry-photometry-etendue/lecture-notes.md), [L02 — Non-sequential fundamentals](../L02-non-sequential-fundamentals/lecture-notes.md); [Course 03 L07 — Gaussian beams and POP](../../03-image-quality-optimization/L07-gaussian-beams-and-pop/lecture-notes.md) is useful for §4 · **Next:** [L04 — Illumination optics](../L04-illumination-optics-collimators-condensers/lecture-notes.md)

## Learning objectives
- Explain how LEDs, edge-emitting laser diodes and VCSELs generate light, and what that implies for their spatial size, angular distribution, spectrum, coherence and étendue.
- Choose the right level of source model (point, analytic surface source, measured ray file, geometric "mini-model", physics model) for a given design stage and justify it.
- Translate a datasheet into OpticStudio source parameters: power, cosine exponent or angular data, emitting area, spectrum (system wavelengths and weights), and laser-diode divergences (FWHM → 1/e² half-angles).
- Set up Source Rectangle/Ellipse, Source Radial, Source File, Source Diode and Polar-detector checks; know which sources are Premium-only (Radiant Source models).
- Compare the radiance and étendue of an LED, a laser diode and a VCSEL array, and explain the speckle/étendue trade-off for structured-light projectors.

## Reading
- **Core:** [Kenyon §14.7–14.7.1, pp. 408–414] — semiconductor junctions, LEDs as incoherent sources, double-heterostructure lasers, threshold, mode spacing, the elliptical, astigmatic diode beam; Table 14.2 (alloys vs. wavelength).
- **Core:** [Kenyon §14.8–14.8.1, pp. 416–420] — quantum-well lasers and **vertical-cavity surface-emitting lasers (VCSELs)**: circular low-divergence beams, $M^2$ a little above 1, arrays straight from the wafer.
- **Core:** [Kenyon §14.4.5, p. 397] — laser speckle; [Kenyon p. 414, eqn 14.43] — the $M^2$ beam-quality factor.
- **Core (online):** Ansys Optics KB, *Light sources in illumination systems* — modelling approaches (geometric, radiance, system, physical emission) and the list of OpticStudio source objects: <https://optics.ansys.com/hc/en-us/articles/42661687233939>
- **Core (online):** Ansys Optics KB, *How to model LEDs and other complex sources* — Source Radial, Source File, Radiant Source Models (Premium), geometric LED mini-models: <https://optics.ansys.com/hc/en-us/articles/42661737780371-How-to-model-LEDs-and-other-complex-sources>
- **Optional:** Ansys Optics KB, *Polar detector and IESNA/EULUMDAT import/export* — verify a source's far field, export it, re-import it: <https://optics.ansys.com/hc/en-us/articles/42661958873235>
- **Optional:** Ansys Zemax community thread on Source Diode divergence definitions (half-angles; relation to FWHM): <https://community.zemax.com/got-a-question-7/laser-diode-astigmatism-845>

---

## 1. Why the source model decides the answer

In imaging design the "source" is a field point and you rarely think about it. In illumination, the source *is* the design: the condenser and homogenizer you build in L04 are matched to the source's size, angular spread and spectrum, and your efficiency and uniformity predictions are only as good as the source model. Ansys's source article lists the data every ray needs — position $(x,y,z)$, direction cosines $(l,m,n)$, power, wavelength — and frames the job as deciding **how much of the real emitter's structure matters for the optics at hand**:

- **Far from the source** (optics ≫ source size away; e.g. a scene 1 m from a 1 mm LED) a point source with the right angular distribution is enough.
- **Close to the source** (a condenser 2 mm from a die, a light pipe touching the dome) you need the source's real extent, its near-field radiance distribution, and often its package geometry — reflections back into the LED package matter.
- **Re-check as the design matures.** Start simple; replace the source with a measured model before you trust efficiency numbers.

The four modelling approaches named by Ansys:

| Approach | What it is | Pros / cons |
|---|---|---|
| Geometric model | Die, reflector cup, wire bonds, dome built as NSC objects, with an emitting surface/volume source inside | Can be tolerance-analysed and captures re-incident light; emission and material properties are guessed |
| Radiance model | Goniometric measurement of the real part, imported as a ray file (Source File) or radiance data (Radiant Source, Premium) | Accurate for that sample at those conditions; ignores light returning into the source; costly to measure |
| System model | Measured radiance on a surface + geometric package around it | Best of both; non-trivial to set up |
| Physical emission | Phosphor absorption/emission/quantum yield + Mie bulk scatter (Volume Physics) | Most faithful for phosphor-converted white LEDs; slow |

## 2. LEDs

### 2.1 Physics in one paragraph
A forward-biased p–n junction in a direct-band-gap semiconductor injects electrons and holes that recombine radiatively, emitting photons near the band-gap energy [Kenyon §14.7, p. 411]. GaAs has $E_g = 1.43$ eV ≈ 865 nm [Kenyon p. 409]; AlGaAs covers ~0.68–0.92 µm and InGaN 0.36–0.60 µm [Kenyon Table 14.2]. Without a resonant cavity the emission is **spontaneous**: incoherent, broadband (tens of nm), emitted in all directions inside the chip. Two consequences for optics:

- **Light extraction.** The semiconductor index is high (the Ansys source article quotes $n > 2.5$; GaAs is ≈ 3.6 [Kenyon p. 412]). The critical angle into air is only $\arcsin(1/3.6) = 16°$, so most light is trapped by TIR. Packages use textured surfaces, high-index encapsulant domes and reflectors to get it out — which is why the package is part of the source.
- **Surface emitters are near-Lambertian.** A thin, flat, top-emitting die (most high-power LEDs) has nearly constant radiance across angle: $I \approx I_0\cos\theta$, the $n = 1$ case of L01 Task 2. A domed or lensed package reshapes this into a narrower $\cos^n$-like or "bat-wing" pattern.

### 2.2 The datasheet, decoded
A typical high-power NIR LED datasheet gives:

| Datasheet item | What you do with it in OpticStudio |
|---|---|
| Radiant flux (mW or W) at a test current and temperature, with binning range | Source **Power**; check the bin, derate for your current, duty cycle and junction temperature |
| Peak / centroid wavelength and spectral FWHM (e.g. 850 nm, 30 nm) | System wavelengths and weights (§2.3) or a spectrum file |
| Radiation pattern plot, "viewing angle 2θ½" | Cosine exponent $n = \ln 0.5/\ln\cos\theta_{1/2}$, or a tabulated $I(\theta)$ in **Source Radial**, or a measured ray file |
| Emitting area / die size | Source half widths (Source Rectangle) |
| Ray files (often on request or via the manufacturer's website) | **Source File** object |
| Wavelength temperature coefficient (typically a few tenths of nm/K for AlGaAs LEDs) | Multi-configuration or wavelength-set variants to check filters and dispersion |

Datasheet "radiance" is rarely quoted for LEDs; compute it ($L \approx \Phi/(\pi A)$ for a Lambertian die) because it decides the étendue-limited performance (L01).

### 2.3 Spectra in OpticStudio
Each source has a *Wavenumber* parameter: 0 = use all system wavelengths, with the system **weights** apportioning power; $k$ = only wavelength $k$. The simplest polychromatic LED model is therefore a set of system wavelengths sampling the LED spectrum, weighted by its relative spectral power. For a Gaussian spectrum of centre $\lambda_0$ and FWHM $\Delta\lambda$, $\sigma = \Delta\lambda/2.3548$ and

$$
w(\lambda) = \exp\!\left[-\frac{(\lambda-\lambda_0)^2}{2\sigma^2}\right].
$$

Object Properties (Sources tab) also offers source-colour options such as spectrum files, blackbody and colour-temperature spectra, and CIE-coordinate definitions — the exact list varies by release; use them for white LEDs and multi-colour projectors, together with a *Detector Color*. Each launched ray carries one wavelength chosen according to the spectrum, so spectral effects (dispersion in the condenser, filter transmission vs. wavelength and angle) are captured automatically.

For a machine-vision projector, spectral modelling matters for: chromatic aberration of the projection lens across the LED bandwidth (an 850 nm LED with 30 nm FWHM spans ~820–880 nm), **bandpass filters on the camera** (the receiver filter must pass the whole projector spectrum at all angles — [Course 04 L08](../../04-machine-vision-camera-lenses/L08-filters-cover-glass-nir-and-ghosts/lecture-notes.md)), and the temperature drift of the peak wavelength.

### 2.4 OpticStudio LED source options, simplest to best
1. **Source Rectangle / Source Ellipse** with the die size and a cosine exponent. Good for first-order condenser design.
2. **Source Two Angle** — different cone angles in X and Y.
3. **Source Radial** — tabulated intensity vs. angle (spline-fitted), uniform over a flat rectangular/elliptical area; the angular data can even be made variable for optimization. Ansys's LED article uses it for a Luxeon emitter.
4. **Source IESNA File / Source EULUMDAT File** — import photometric files (relative intensity on an angular grid). Point-like: no spatial information.
5. **Source File** — a manufacturer **ray file** (millions of rays with position, direction, power, wavelength) captured on a surface or volume around the real LED. Captures near-field spatial structure (die pattern, electrode shadows). Parameters include *Randomize?*, # Layout Rays and # Analysis Rays; when randomizing, *System Explorer → Non-Sequential → Maximum Source File Rays in Memory* must exceed the file's ray count. Do not trace more rays than the file contains without understanding what reuse does to your noise.
6. **Radiant Source Model** (RSMX, Premium only) — calibrated radiance measurements from which rays are generated on demand (*Libraries → Radiant Source Models*).
7. **Geometric mini-model** — die (Source Volume Rectangle or a surface source), encapsulant dome (Standard Lens or Even Asphere Lens of silicone), reflector cup, all as NSC objects. OpticStudio ships an example, `led_model.zmx`, referenced in the Ansys article.

Whatever you choose, **verify it**: put a **Detector Polar** (far field, full hemisphere or more) around the source and compare $I(\theta)$ with the datasheet plot; put a Detector Rectangle very close to the emitting surface and compare with the die photo/near-field. You can even export the polar data to IES/LDT and re-import it (Ansys polar-detector article).

## 3. Edge-emitting laser diodes

### 3.1 Physics
Add a Fabry–Perot cavity (cleaved facets, $R \approx 0.32$ for GaAs/air) and confine carriers and light in a thin **double heterostructure** and you get a laser [Kenyon §14.7.1]. The active stripe is ~0.1–0.2 µm thick and a few µm wide, ~0.3 mm long. Above threshold (~10 mA in Kenyon's example) the output rises with a slope efficiency of order 0.5 W/A, and the spectrum collapses to one or a few longitudinal modes (mode spacing $\Delta\lambda = \lambda^2/2nL \approx 0.35$ nm for a 0.3 mm GaAs cavity).

Diffraction from the tiny, rectangular exit aperture produces a **wide, elliptical, astigmatic** beam [Kenyon p. 413]:

- **Fast axis** (perpendicular to the junction): from the ~1 µm-scale aperture, divergence typically 20–40° FWHM, nearly diffraction-limited ($M^2 \approx 1$).
- **Slow axis** (parallel to the junction): from the wider stripe, divergence typically 6–12° FWHM; multimode (broad-area) diodes have $M^2 \gg 1$ in this axis.
- **Astigmatism**: the two axes have different apparent waist positions (a few µm for index-guided, more for gain-guided diodes).
- **Polarization**: strongly linear (TE), which matters for coatings and polarization-sensitive elements.

### 3.2 Datasheet → OpticStudio
Datasheets quote **full-angle FWHM** divergences. A Gaussian far field with $1/e^2$ half-angle $\theta_e$ has FWHM full angle $2\theta_e\sqrt{\ln 2/2}$, so

$$
\theta_{e} = \frac{\text{FWHM}_{\text{full}}}{2\sqrt{\ln 2/2}} = 0.849\ \text{FWHM}_{\text{full}} .
$$

The **Source Diode** object takes X and Y *divergence half-angles* (confirmed by Ansys staff in the community thread above; another user describes them as "0.85 × FWHM", consistent with the $1/e^2$ half-angle relation), super-Gaussian shape factors, emitter widths, astigmatism and array parameters (number and spacing of emitters). Check the Help page *Source Diode* in your release for the exact definitions — they were revised in 21.2. Note also that OpticStudio reports **RMS** angular widths in some analyses: for a Gaussian, the RMS radius per axis is half the $1/e^2$ radius, so do not compare RMS and $1/e^2$ numbers directly.

For **coherent** propagation (beam waist, focusing to a few µm), use sequential mode with the Paraxial Gaussian Beam tool or Physical Optics Propagation ([Course 03 L07](../../03-image-quality-optimization/L07-gaussian-beams-and-pop/lecture-notes.md)); for illumination (power through a homogenizer, onto a DMD) NSC with Source Diode/Gaussian is appropriate.

## 4. VCSELs and VCSEL arrays

A **VCSEL** emits perpendicular to the wafer through a top window; the very short (~1 µm) cavity is closed by two distributed-Bragg-reflector (DBR) mirrors and supports a single longitudinal mode [Kenyon §14.8.1, pp. 418–419]. Kenyon lists the advantages that made VCSELs the dominant NIR source for consumer 3-D sensing:

- **Circular, low-divergence beams** — aperture 10–1000 µm² so divergence is much smaller than an edge emitter's fast axis; $M^2$ "usually a little above unity" for single-mode devices (larger multimode apertures are common in illumination arrays, with typically 15–30° full divergence).
- **Arrays straight from the wafer** — hundreds to thousands of emitters on a regular or pseudo-random grid; on-wafer testing.
- **Low threshold** (~1 mA), ~20 % wall-plug efficiency in Kenyon's numbers (modern high-power 940 nm arrays are considerably better).
- **Small wavelength drift** — the DBR cavity sets the wavelength, so the temperature coefficient (typically < 0.1 nm/K) is several times smaller than an LED's; this allows narrow camera bandpass filters, a big ambient-light advantage.

In a dot-pattern projector (L08) a VCSEL array is imaged to the scene and replicated by a diffractive element; in a "flood" illuminator it passes a diffuser. Model it with **Source Diode** set up as an array, or with a grid of Source Ellipse/Gaussian objects (the ZOS-API makes generating 500 sources trivial — Course 07), or with a manufacturer ray file.

### 4.1 Coherence, speckle and étendue
Lasers are high-radiance, low-étendue sources: a single-mode beam has étendue of order $\lambda^2$ ($7\times10^{-7}$ mm² sr at 850 nm — seven orders of magnitude below a 0.3″ DMD). That is the good news: tiny, slow optics collect everything. The bad news is **speckle** [Kenyon §14.4.5]: coherent light scattered from a rough scene interferes, producing a granular pattern with feature size set by the *camera's* aperture ($\sim\lambda/\text{NA}$ at the sensor). For a structured-light 3-D camera, speckle is noise on exactly the quantity you measure (fringe phase or edge position). Speckle contrast is reduced by **adding diversity** — many mutually incoherent emitters (VCSEL arrays), spectral width, angular diversity (deliberately *increasing* étendue with a diffuser), time averaging (moving diffusers), polarization diversity. Professionals therefore often degrade a laser's étendue on purpose, up to what the downstream optics accept.

Coherence length $L_c \approx \lambda^2/\Delta\lambda$ gives a feel: an 850 nm LED with 30 nm FWHM has $L_c \approx 24$ µm; a multimode diode with 1 nm spectrum, ≈ 0.7 mm; a single-frequency laser, metres.

## 5. Comparing sources for a projector

| | Lambertian LED, 1 × 1 mm, 1.2 W | Edge-emitting LD, single mode | VCSEL array, 0.8 × 0.6 mm, 2 W, ±10° |
|---|---|---|---|
| Étendue | $\pi A = 3.14$ mm² sr | ~$\lambda^2$ ≈ 10⁻⁶ mm² sr | $\pi A\sin^2 10° = 0.045$ mm² sr |
| Radiance | 0.38 W/(mm² sr) | enormous | ≈ 44 W/(mm² sr) (array average) |
| Spectrum | 20–40 nm | < 1 nm | ~1 nm |
| Temperature drift | ~0.3 nm/K (typ.) | ~0.3 nm/K (typ., GaAs) | < 0.1 nm/K (typ.) |
| Speckle | negligible | severe | reduced by many incoherent emitters |
| Fits a 0.3″ DMD (7.2 mm² sr)? | yes, with room | trivially | trivially |

The VCSEL array has ~100× the radiance of the LED in this example; for a DMD-based projector whose étendue is much larger than either source, radiance alone is not the deciding factor — total flux, cost, speckle, eye safety and filter bandwidth are. For a pattern projector based on a small DOE or for long throw distances, low étendue becomes decisive.

**Eye safety.** Laser and high-radiance LED projectors fall under IEC 60825-1 (lasers) and IEC 62471 (lamps/LEDs). Optical design choices (diffusers that increase apparent source size, pulse duty cycle, exit pupil size) directly change the hazard classification — involve your laser-safety specialist early.

## 6. In OpticStudio — checklist for a source model

1. **Units and power:** System Explorer → Units (Watts for NIR); source Power = optical (radiant) flux at your operating point, not electrical power.
2. **Spatial extent:** half widths of Source Rectangle/Ellipse = half the die size; for a domed LED the *apparent* size from outside is larger (magnified by the dome).
3. **Angular distribution:** Cosine Exponent, Gx/Gy, Source Radial table, Source Diode divergences, or a ray file.
4. **Spectrum:** system wavelengths + weights, or a spectrum in the source's Object Properties.
5. **Position inside packaging:** use *Inside Of* if the source sits within a volume (e.g. silicone dome), otherwise geometry errors (L02).
6. **Verify:** Detector Polar for $I(\theta)$; near-field Detector Rectangle; total emitted power on a closed detector "box" = source power.
7. **Sampling:** use Sobol sampling where available for smooth, low-noise results with fewer rays; for Source File, mind *Randomize?* and the number of rays in the file.

## Worked example — from datasheets to source objects

**A. NIR LED.** Datasheet: 1.2 W radiant flux at 850 nm, FWHM 30 nm, Lambertian pattern (2θ½ = 120°), emitting area 1 × 1 mm.

- Source Rectangle, half widths 0.5 × 0.5 mm, Power 1.2 W, Cosine Exponent 1.
- Check: $\theta_{1/2} = \arccos(0.5^{1/1}) = 60°$ ✓; on-axis intensity $I_0 = 1.2/\pi = 0.382$ W/sr; radiance 0.382 W/(mm² sr).
- Spectrum: $\sigma = 30/2.3548 = 12.74$ nm. Five system wavelengths 820, 835, 850, 865, 880 nm with weights 0.0625, 0.5, 1, 0.5, 0.0625 (the Gaussian evaluated at ±15 and ±30 nm — conveniently exactly $2^{-4}$ and $2^{-1}$ because 15 nm is half the FWHM). Coherence length ≈ 24 µm.

**B. Edge-emitting laser diode.** Datasheet: 850 nm, θ∥ = 8°, θ⊥ = 25° (FWHM, full angles).

- $1/e^2$ half-angles: 0.849 × 8 = 6.8° (slow), 0.849 × 25 = 21.2° (fast) → Source Diode X/Y divergence (after checking the Help definition).
- If the fast axis is diffraction-limited, its waist radius is $w_0 = \lambda/(\pi\tan\theta_e) = 0.85/(\pi\cdot0.388) = 0.70$ µm — consistent with a sub-µm active layer. A diffraction-limited slow axis would need $w_0 = 2.3$ µm; a broad-area emitter with a 50 µm stripe and the same divergence has $M^2 \approx 25/2.3 \approx 11$ in that axis.

**C. VCSEL array.** 940 nm, 2 W, 0.8 × 0.6 mm emitting region, per-emitter divergence ±10° ($1/e^2$).

- Étendue: $\pi\cdot0.48\cdot\sin^2 10° = 0.045$ mm² sr; array-average radiance $2/0.045 = 44$ W/(mm² sr), ~115× the LED of part A.
- A Gaussian angular distribution puts $1 - e^{-2} = 86.5$ % of the power inside the $1/e^2$ cone — so a collector sized exactly to ±10° loses 13.5 %. Size optics to ~1.3–1.5× the $1/e^2$ angle.

## Key takeaways
- The source model must resolve whatever the downstream optics can "see": point + angular distribution for far-away optics, full spatial/angular (ray file or geometric) model for close-coupled optics.
- LEDs: incoherent, broadband, near-Lambertian die, package-dependent pattern; model with Source Rectangle (cos^n), Source Radial, IES/LDT, Source File, Radiant Source (Premium) or a geometric mini-model.
- Spectra: system wavelengths with weights (or a spectrum file) — essential for filters, dispersion and temperature drift.
- Edge-emitting LDs: elliptical, astigmatic, polarized; convert FWHM full angles to $1/e^2$ half-angles (× 0.849) for Source Diode.
- VCSEL arrays: circular, low-divergence, low-drift, array-friendly; the 3-D sensing workhorse at 850/940 nm.
- Lasers have tiny étendue (easy optics) but speckle; diversity (many emitters, diffusers, spectral width) trades étendue for lower speckle.
- Always verify a source model with polar and near-field detectors before trusting system-level numbers.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Direct band gap | Semiconductor in which electron–hole recombination emits a photon efficiently (GaAs, InGaN) |
| Light extraction | Getting photons out of a high-index chip despite TIR |
| Ray file | List of rays (position, direction, power, wavelength) measured around a real source |
| Source Radial / Source File / Radiant Source | OpticStudio sources from tabulated angular data / ray files / calibrated radiance models (Premium) |
| Double heterostructure (DH) | Laser structure confining carriers and light in a thin active layer |
| Fast / slow axis | Laser-diode axes perpendicular / parallel to the junction; large / small divergence |
| VCSEL | Vertical-cavity surface-emitting laser; DBR mirrors, circular beam, arrays |
| $M^2$ | Beam-quality factor: divergence × waist relative to an ideal Gaussian |
| Speckle | Random interference pattern from coherent light on rough surfaces |
| Coherence length | $\approx\lambda^2/\Delta\lambda$; path difference over which light still interferes |

## References
1. [Kenyon §14.7–14.7.1, pp. 408–414] — semiconductors, LEDs, DH lasers, divergence and astigmatism, Table 14.2.
2. [Kenyon §14.8–14.8.1, pp. 416–420] — quantum-well lasers and VCSELs.
3. [Kenyon §14.4.5, p. 397] — laser speckle; [Kenyon §14.7.1, p. 414, eqn 14.43] — $M^2$.
4. Ansys Optics KB, *Light sources in illumination systems* — <https://optics.ansys.com/hc/en-us/articles/42661687233939>
5. Ansys Optics KB, *How to model LEDs and other complex sources* — <https://optics.ansys.com/hc/en-us/articles/42661737780371-How-to-model-LEDs-and-other-complex-sources>
6. Ansys Optics KB, *Polar detector and IESNA/EULUMDAT import/export* — <https://optics.ansys.com/hc/en-us/articles/42661958873235>
7. Ansys Zemax community, *Laser diode astigmatism* (Source Diode divergence definitions) — <https://community.zemax.com/got-a-question-7/laser-diode-astigmatism-845>
8. Ansys Zemax community, *How to determine elliptical Gaussian source in NSC* (Gx, Gy of Source Ellipse) — <https://community.zemax.com/got-a-question-7/how-to-determine-elliptical-gaussian-source-in-nsc-3534>
