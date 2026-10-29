# Curriculum map

Seven courses, 66 lessons. Each lesson folder contains `lecture-notes.md` and `tasks.md`.
Book abbreviations used everywhere: **[Geary]**, **[Kidger]**, **[Kenyon]** — see [`references/README.md`](references/README.md).

Time estimates assume ~6–8 h per lesson (reading + lecture notes + tasks). At roughly one lesson per week, the full programme fits in ~12–15 months; Courses 01–03 are the core, Courses 04–07 are the professional specialisation tracks and can be taken in any order once Course 03 is done (Course 06 L08 and Course 07 L08 build on the Course 04 capstone).

```
01 Foundations ──► 02 Aberrations & classical design ──► 03 Image quality & optimization
                                                              │
              ┌───────────────┬───────────────┬───────────────┤
              ▼               ▼               ▼               ▼
      04 Machine vision  05 Illumination  06 Tolerancing  07 Automation
         camera lenses     & projection    & manufacturing  (ZPL / ZOS-API)
```

---

## Course 01 — Foundations: geometrical optics and OpticStudio basics (`01-foundations`)

| # | Lesson folder | Topic | Core reading |
|---|---|---|---|
| L01 | `L01-light-rays-and-opticstudio-tour` | Light as rays & waves, Snell, Fermat; tour of OpticStudio (ribbon, System Explorer, LDE, analysis windows), first singlet | Kenyon Ch. 1.2, 2.1; Kidger §1.1–1.5; Geary Ch. 1–2 |
| L02 | `L02-surfaces-sign-conventions-aspheres` | Sign conventions, curvature, shape factor, sag, conics, even aspheres | Geary Ch. 3; Kidger §1.7, §3.6 |
| L03 | `L03-paraxial-optics-and-ray-tracing` | Paraxial ray trace equations (y–nu), power, cardinal points, thick lens, Gaussian/Newtonian imaging, ABCD matrices | Geary Ch. 4; Kidger Ch. 2; Kenyon §3.3–3.6 |
| L04 | `L04-stops-pupils-fields` | Aperture stop, entrance/exit pupils, marginal & chief rays, F/#, NA, Lagrange invariant, field definitions & vignetting basics | Geary Ch. 5; Kidger §1.6, §2.5 |
| L05 | `L05-optical-glass-and-dispersion` | Refractive index, dispersion formulas, Abbe number, partial dispersion, glass map, catalogs, practical glass choice | Geary §6.2; Kidger §5.1; Kenyon §1.6, §11.5 |
| L06 | `L06-real-rays-and-analysis-tools` | Real (exact) ray tracing, ray fans, spot diagrams, OPD fans, footprint, layout, prescription data | Geary Ch. 7; Kidger Ch. 3, §4.1–4.3 |
| L07 | `L07-solves-variables-first-optimization` | Solves (marginal-ray height/angle, F/#, pickups), variables, Merit Function Editor, default merit function, DLS | Geary Ch. 8, App. E; Kidger Foreword (history of DLS) |
| L08 | `L08-landscape-lens-stop-shift-and-splitting` | Mini-project: Wollaston landscape lens, stop shift, lens splitting | Geary §6.3–6.4, Ch. 9; Kidger §6.3, §7.3.5 |

## Course 02 — Aberrations and classical lens design (`02-aberrations-classical-design`)

| # | Lesson folder | Topic | Core reading |
|---|---|---|---|
| L01 | `L01-wavefront-and-transverse-aberrations` | Wavefront vs. transverse aberration, aberration polynomial (W_klm), Seidel sums, Zernike polynomials, how OpticStudio reports them | Geary §7.4–7.6; Kidger §4.1, §4.4, §6.1, §6.9 |
| L02 | `L02-spherical-aberration-and-bending` | Spherical aberration, lens bending, aberration balancing with defocus, higher-order spherical | Geary Ch. 10–11; Kidger §6.2.1, §7.3.1, §4.4.3.1 |
| L03 | `L03-coma-astigmatism-and-symmetry` | Coma & astigmatism, stop-shift equations, symmetry principle, periscopic lens | Geary Ch. 12–13; Kidger §6.2.2, §6.3, §7.7.2 |
| L04 | `L04-field-curvature-petzval-flatteners` | Petzval sum, sagittal/tangential fields, Coddington equations, field flatteners | Geary Ch. 14, 27, 29; Kidger §6.9.3–6.9.4, §7.3.4 |
| L05 | `L05-distortion` | Distortion, its stop dependence, F-theta & F-tan mapping, grid distortion analysis | Geary Ch. 15; Kidger §4.4.2.4, §6.2.3 |
| L06 | `L06-chromatic-aberration-and-achromats` | Axial & lateral color, thin-lens achromat, cemented doublet design, bending the achromat, aplanat | Geary Ch. 16–17; Kidger Ch. 5, §8.1–8.2 |
| L07 | `L07-secondary-spectrum-apochromats` | Partial dispersion, secondary spectrum, air-spaced achromats, apochromatic triplets, glass substitution | Geary Ch. 18, 19, 21; Kidger §5.1.3, §8.3 |
| L08 | `L08-seidel-surface-contributions` | Seidel surface coefficients by hand and in OpticStudio (Seidel Coefficients / Diagram), stop & conjugate shift, aplanatic surfaces | Kidger §6.2–6.6, §6.10–6.11; Geary §13.3 |
| L09 | `L09-cooke-triplet` | Cooke triplet: thin-lens predesign, optimization, image compactness, glass choice | Geary Ch. 30; Kidger Ch. 10 |
| L10 | `L10-symmetric-lenses-double-gauss-vignetting` | Symmetric achromats, Celor, double Gauss, deliberate vignetting | Geary Ch. 25, 28; Kidger §7.7.2, §10.4 |
| L11 | `L11-petzval-and-telephoto` | Petzval portrait lens, field flattener, telephoto ratio | Geary Ch. 33; Kidger Ch. 9 |
| L12 | `L12-mirrors-and-catadioptrics` | Conic mirrors, Cassegrain/RC, Schmidt corrector, catadioptric field correctors | Geary Ch. 24, 26; Kidger Ch. 13; Kenyon §8.2–8.3 |
| L13 | `L13-eyepieces-afocal-relays-windows` | Afocal systems, eyepieces, field lenses, relays, windows & plane-parallel plates | Geary Ch. 22–23; Kidger Ch. 11; Kenyon Ch. 4 |

## Course 03 — Image quality, optimization and physical optics (`03-image-quality-optimization`)

| # | Lesson folder | Topic | Core reading |
|---|---|---|---|
| L01 | `L01-diffraction-and-the-psf` | Fraunhofer diffraction, Airy disk, FFT vs. Huygens PSF, diffraction-limited criteria | Kenyon Ch. 6 (§6.1–6.7, 6.10); Geary Ch. 31 |
| L02 | `L02-mtf-theory-and-practice` | OTF/MTF/PTF, Fourier optics view, geometric vs. diffraction MTF, through-focus MTF, MTF vs. field | Kenyon Ch. 7; Kidger §4.5; Geary Ch. 34 |
| L03 | `L03-strehl-wavefront-error-depth-of-focus` | Strehl ratio, Maréchal criterion, RMS wavefront budgets, axial intensity, depth of focus | Geary Ch. 31–32 |
| L04 | `L04-merit-function-mastery` | Default merit function options, operand toolbox, weights, boundary constraints, custom MF design | Geary Ch. 8, App. E; Ansys docs |
| L05 | `L05-optimization-strategies-and-global-search` | DLS, orthogonal descent, Hammer & Global search, local minima, design forms exploration | Kidger Foreword, Ch. 7; Ansys docs |
| L06 | `L06-multi-configuration-and-zoom` | Multi-Configuration Editor, zoom lenses, multiple conjugates, configuration-dependent operands | Kidger §9.4 (telephoto) ; Ansys docs |
| L07 | `L07-gaussian-beams-and-pop` | Gaussian beam optics, M², Paraxial Gaussian Beam tool, Physical Optics Propagation | Kenyon §6.15, Ch. 14 (laser background) |
| L08 | `L08-polarization-and-coatings` | Fresnel equations, coatings (AR, thin-film stacks), polarization ray tracing, transmission | Kenyon §9.5–9.7, Ch. 10 |
| L09 | `L09-thermal-and-environmental-analysis` | dn/dT, CTE, thermal pickups, athermalization, pressure | Kidger §12.5.2; Ansys docs |
| L10 | `L10-starting-points-and-design-strategy` | Starting points (patents, LensView-type sources, sample files), scaling, specification-to-design workflow | Geary Ch. 1, 37–38; Kidger Ch. 7 |

## Course 04 — Machine-vision & camera lens design (`04-machine-vision-camera-lenses`)

| # | Lesson folder | Topic | Core reading |
|---|---|---|---|
| L01 | `L01-image-sensors-and-sampling` | Pixel pitch, Nyquist, sensor formats, CRA, microlenses, QE, noise basics | Kenyon §15.7; online sensor docs |
| L02 | `L02-camera-first-order-design` | Focal length / FOV / working distance, magnification, depth of field, hyperfocal, F/# vs. diffraction | Kenyon §4.5; Geary Ch. 32 |
| L03 | `L03-relative-illumination-and-telecentricity` | cos⁴ law, vignetting, relative illumination, image-space telecentricity & CRA matching | Kidger §10.4; Kenyon §1.7 |
| L04 | `L04-compact-fixed-focus-lens-project` | Project (2 sessions): M12-style fixed-focus lens for a 1/2.3"–2/3" sensor | Kidger Ch. 10; Geary Ch. 30 |
| L05 | `L05-wide-angle-and-distortion-mappings` | Retrofocus/wide-angle, fisheye mappings, distortion budgets, calibration-friendly distortion | Kidger §4.4.2.4; Geary Ch. 15 |
| L06 | `L06-telecentric-metrology-lenses` | Object-space & double-telecentric lenses, depth of field, measurement accuracy | Kidger §1.6; online |
| L07 | `L07-plastic-optics-and-molded-aspheres` | Optical polymers, molded aspheres, thermal behaviour, high-order aspheres & Q-type | Kidger §7.5; online |
| L08 | `L08-filters-cover-glass-nir-and-ghosts` | Cover glass, IR-cut / bandpass filters, NIR design, angle-of-incidence shift, ghost analysis | Kenyon §9.7; Geary Ch. 23 |
| L09 | `L09-3d-vision-optics-scheimpflug-stereo` | Optics for 3D: triangulation geometry, Scheimpflug, stereo baselines, depth-range focus | online sources |
| L10 | `L10-capstone-machine-vision-lens` | Capstone: specification → design → analysis → report for a 3D-camera receiver lens | all of the above |

## Course 05 — Illumination, projection and non-sequential design (`05-illumination-projection-nsc`)

| # | Lesson folder | Topic | Core reading |
|---|---|---|---|
| L01 | `L01-radiometry-photometry-etendue` | Radiometric/photometric quantities, Lambertian sources, étendue conservation | Kenyon §1.7–1.8 |
| L02 | `L02-non-sequential-fundamentals` | NSC Editor, objects, sources, detectors, ray splitting, Ray Database | Ansys docs |
| L03 | `L03-source-modeling-leds-and-lasers` | Source types, LED source files, spectra, laser diodes & VCSEL arrays | Kenyon Ch. 14–15 |
| L04 | `L04-illumination-optics-collimators-condensers` | Condensers, Köhler vs. critical illumination, TIR collimators, lenslet homogenizers | Kenyon §4.4 |
| L05 | `L05-projection-lens-design` | Sequential projection lens design (reverse ray trace), DMD/LCoS imaging, telecentricity, keystone | Kidger Ch. 10; online |
| L06 | `L06-hybrid-mixed-mode-and-nsc-optimization` | Sequential-in-NSC, NSC optimization operands (NSDD, NSTR…), freeform/illumination optimization | Ansys docs |
| L07 | `L07-stray-light-scattering-ghosts` | Scatter models (Lambertian, ABg), importance sampling, path analysis, ghost reflections | Kenyon Ch. 11 |
| L08 | `L08-diffractive-optics-and-pattern-projection` | Gratings, DOEs, binary/diffractive surfaces, dot-pattern generators | Kenyon §6.5, §6.8, §7.7 |
| L09 | `L09-capstone-structured-light-projector` | Capstone: structured-light projector (source → illumination → projection lens → scene) | all of the above |

## Course 06 — Tolerancing and manufacturing (`06-tolerancing-manufacturing`)

| # | Lesson folder | Topic | Core reading |
|---|---|---|---|
| L01 | `L01-manufacturing-processes-and-tolerances` | Grinding/polishing, molding, metrology (interferometry), typical tolerance grades | Geary §9.4; Kenyon §5.7 |
| L02 | `L02-tolerance-data-editor-and-compensators` | TDE operands, default tolerances, compensators, criteria | Ansys docs |
| L03 | `L03-sensitivity-and-monte-carlo` | Sensitivity, inverse sensitivity, Monte Carlo statistics, yield | Ansys docs |
| L04 | `L04-desensitization-and-as-built-performance` | Desensitizing designs, high-order aberration awareness, tolerance-aware optimization | Kidger Ch. 7 |
| L05 | `L05-opto-mechanics-and-cad-integration` | Element mounting, decenters/tilts, CAD export, STAR / structural-thermal coupling | Ansys docs |
| L06 | `L06-drawings-iso10110-and-vendor-handoff` | ISO 10110 drawings, test-plate fitting, melt data, vendor communication | Geary §6.2.5; online |
| L07 | `L07-alignment-and-active-alignment` | Alignment strategies, compensators in production, camera active alignment | online |
| L08 | `L08-capstone-tolerancing-the-camera-lens` | Capstone: full tolerance analysis of the Course 04 capstone design | all of the above |

## Course 07 — Automation with ZPL and the ZOS-API (`07-automation-zpl-zosapi`)

| # | Lesson folder | Topic | Core reading |
|---|---|---|---|
| L01 | `L01-zpl-macro-fundamentals` | ZPL language, keywords, ray tracing from macros, output | Ansys docs |
| L02 | `L02-user-defined-operands-and-analyses` | ZPLM operand, UDOC/UDOP, user analyses | Ansys docs |
| L03 | `L03-zos-api-architecture-and-python-setup` | Standalone vs. interactive extension, pythonnet, ZOSPy | ZOSPy docs |
| L04 | `L04-building-and-editing-systems-from-python` | LDE/MFE/MCE manipulation, solves, files | ZOSPy docs |
| L05 | `L05-running-analyses-and-extracting-data` | Analyses (spot, MTF, wavefront), results parsing, plotting | ZOSPy docs |
| L06 | `L06-batch-ray-tracing-and-custom-metrics` | Batch ray trace (normalized unpolarized), custom metrics, vectorized post-processing | ZOS-API docs |
| L07 | `L07-automated-optimization-and-tolerancing` | Scripted optimization loops, design-of-experiments, scripted tolerancing / Monte Carlo files | ZOS-API docs |
| L08 | `L08-capstone-automated-design-report` | Capstone: reproducible design-report pipeline under git | — |
