# L03 — Tasks: Source Modelling — LEDs, Laser Diodes and VCSEL Arrays

> Work in `work/` inside this lesson folder (e.g. save `work/L03_T2_led_dome.zmx`). Commit your designs, scripts and a short `work/notes.md` with answers.
> Estimated time: ~4–5 h

## Task 1 — Datasheet to parameters (Python)
**Goal:** Extend `../L01-radiometry-photometry-etendue/work/radiometry.py` with source-conversion helpers.
**Given / specs:**
- LED-1: 940 nm, FWHM 40 nm, viewing angle 2θ½ = 90°, 0.9 W, emitting area 1 × 1 mm.
- LED-2: same chip with a lens cap, viewing angle 2θ½ = 40°.
- LD: 905 nm, θ∥ = 10°, θ⊥ = 30° FWHM full angles, spectral width 5 nm.
**Steps:**
1. Write `cos_exponent(view_angle_full_deg)`, `gaussian_weights(lam0, fwhm, lams)`, `fwhm_to_e2_half(fwhm_full_deg)`, `coherence_length(lam, dlam)`.
2. Cosine exponents for LED-1 and LED-2. Is LED-1 Lambertian?
3. Weights for 5 system wavelengths at 910, 925, 940, 955, 970 nm (LED-1), and the fraction of the total power each carries.
4. Source Diode divergence inputs ($1/e^2$ half-angles) for the LD.
5. Coherence lengths of LED-1 and LD.
6. Étendue of LED-2? (Careful: the lens cap does not reduce étendue — what does it change?)
**Deliverable:** script + table.
**Check yourself:** $n = 2.0$ (LED-1, *not* Lambertian — a Lambertian die has 2θ½ = 120°), $n = 11.1$ (LED-2); weights 0.210, 0.677, 1, 0.677, 0.210; LD 8.5° (slow) and 25.5° (fast); $L_c$ ≈ 22 µm (LED) and ≈ 0.16 mm (LD).

<details><summary>Hints</summary>

6. Étendue is conserved by the lens cap: what changes is that the light leaves from a larger *apparent* source (the magnified image of the die) into a narrower cone. The product cannot shrink; with imperfect optics it grows. If the datasheet only gives the narrow pattern, you can be fooled into thinking the LED-2 is "brighter" — measure or compute the apparent source size.

</details>

## Task 2 — Bare die vs. domed LED (OpticStudio)
**Goal:** Build a simple geometric LED mini-model and compare its far field and efficiency with a bare Lambertian die.
**Given / specs:** Units mm, Watts, wavelength 0.85 µm.
- Model A (`work/L03_T2_led_bare.zmx`): Source Rectangle 1 × 1 mm (half widths 0.5), Cosine Exponent 1, 1 W, Sobol sampling if available.
- Model B (`work/L03_T2_led_dome.zmx`): same source, placed *inside* a hemispherical silicone dome: a Standard Lens with Radius 1 = 2.5 mm, Radius 2 = 0 (flat base), thickness 2.5 mm, clear semi-diameters 2.5 mm, oriented so the flat face is at the die plane and the curved face faces +Z. Material: a model glass with $n_d = 1.41$, $V_d = 50$ (silicone-like; use a Material Model solve). Set the source's *Inside Of* to the dome object. Below the dome, an absorbing Annulus or Rectangle (`ABSORB`) representing the PCB/package.
- Both: a **Detector Polar** centred on the source, radius 100 mm, maximum angle 90°.
**Steps:**
1. Trace 10⁶ rays in each, polarization on, no splitting. Record total power on the polar detector and plot intensity vs. angle (polar cross-section).
2. Compare the angular pattern of B with $\cos\theta$. Compare the total power with the uncoated-dome Fresnel transmission estimate.
3. Turn on ray splitting in B. Where does the reflected light go? How much reaches the absorbing base?
4. Move the die 0.5 mm off-centre in model B. What happens to the pattern? (Real LED packages are sensitive to die placement — the Ansys source article names die and reflector as the most sensitive components.)
**Deliverable:** two `.zmx` files, intensity plots, a short paragraph.
**Check yourself:** A: 1.000 W on the detector, $I(\theta) \propto \cos\theta$, $I_0 = 0.318$ W/sr. B: the pattern stays close to Lambertian (the die is small compared with the dome, so rays meet the dome near normal incidence), total power ≈ 0.96–0.97 W ($R \approx 2.9$ % at the silicone/air interface, plus a little more at oblique rays near the die corners). With splitting, most of the ~3 % reflected light returns to the base and is absorbed. An off-centre die tilts and distorts the pattern by several degrees.

<details><summary>Hints</summary>

- If you get geometry errors, check *Inside Of* and that the source plane does not coincide exactly with the dome base (offset it by a few µm into the dome).
- The emitted power in model B is 1 W *into the silicone*. In a real LED the dome increases the power that escapes the chip (less TIR at the chip surface), which is not captured by this model: our source already emits 1 W. That is exactly the kind of assumption a geometric model hides — write it down.

</details>

## Task 3 — Laser diode far field (OpticStudio)
**Goal:** Set up a Source Diode and confirm the FWHM ↔ $1/e^2$ conversion.
**Given / specs:** The LD of Task 1 (905 nm, 10° × 30° FWHM). Units mm, W; source power 1 W.
**Steps:**
1. Read the *Source Diode* Help page of your release and note exactly how X/Y divergence are defined (half-angle; which intensity level) and what the super-Gaussian factors do.
2. Enter the divergences from Task 1 (super-Gaussian factors 1 = Gaussian). Emitter size: 3 µm × 1 µm (if the object has width parameters).
3. Detector Polar, radius 500 mm, max angle 60°, fine angular sampling. Trace 10⁶ rays.
4. Measure the FWHM full angles in X and Y from the polar cross-sections. Compare with 10° and 30°.
5. Repeat with a Detector Rectangle 500 mm away and compare the apparent widths — why are they slightly different?
**Deliverable:** `work/L03_T3_diode.zmx`, measured vs. nominal angles.
**Check yourself:** measured FWHM within ~0.5° of 10° and 30° if the inputs are $1/e^2$ half-angles; a Gaussian has its $1/e^2$ points at 8.5° and 25.5° half-angle. On the flat detector, irradiance includes extra $\cos^3\theta$ obliquity/distance factors, so the fast-axis profile looks slightly narrower than the intensity profile.

## Task 4 — Spectral bookkeeping with filter strings (OpticStudio)
**Goal:** Prove that the source's spectrum is sampled as you intended.
**Given / specs:** Model A of Task 2, but with five system wavelengths 0.820, 0.835, 0.850, 0.865, 0.880 µm and weights 0.0625, 0.5, 1, 0.5, 0.0625 (L03 worked example A); source Wavenumber 0.
**Steps:**
1. Save rays to a ZRD. In the Detector Viewer, replay with filters `W1` … `W5` and record the power on the detector for each.
2. Compare with the expected fractions (weight / sum of weights).
3. Change Wavenumber to 3 and retrace. What happens?
**Check yourself:** fractions 2.94 %, 23.5 %, 47.1 %, 23.5 %, 2.94 % (sum of weights 2.125); with Wavenumber 3 all power is at 0.850 µm.

## Task 5 — A small VCSEL array (OpticStudio or ZOS-API-free shortcut)
**Goal:** Model a VCSEL array and see why arrays reduce speckle but keep low étendue.
**Given / specs:** 940 nm; 5 × 5 emitters on a 100 µm pitch; each emitter Gaussian with $1/e^2$ half-angle 10°, 10 µm emitting diameter, 40 mW each (1 W total).
**Steps:**
1. Model the array either with one Source Diode in array mode (if your release has array parameters) or with 25 Source Ellipse/Gaussian objects (copy–paste rows; use *Ref Object* to a dummy "array origin" object so you can move it as one).
2. Detector Rectangle at Z = 0.5 mm (near field) and a Detector Polar (far field). Describe both.
3. Compute the array étendue (use the bounding box of the emitters) and compare with the L01 DMD (7.2 mm² sr).
4. Reflection: each emitter is mutually incoherent with the others. If the camera sees a speckle pattern from each emitter independently, by roughly what factor does averaging 25 independent patterns reduce speckle contrast?
**Deliverable:** `work/L03_T5_vcsel.zmx`, plots, answers.
**Check yourself:** near field: 25 separated spots; far field: one smooth Gaussian lobe (±10°) — at a distance the array looks like a single source. Bounding box 0.41 × 0.41 mm (pitch × 4 + emitter diameter) → $G \approx \pi\cdot0.168\cdot\sin^2 10° \approx 0.016$ mm² sr, ~450× below the DMD étendue. Speckle contrast falls as $1/\sqrt{N}$ for $N$ independent, equal-power patterns: $1/\sqrt{25} = 0.2$.

<details><summary>Solution note</summary>

$0.41^2 = 0.168$ mm²; $\sin^2 10° = 0.0302$; $G = \pi \cdot 0.168 \cdot 0.0302 = 0.0160$ mm² sr. Ratio $7.22/0.016 \approx 450$. The bounding-box area overestimates the "true" étendue (emitters fill only ~1 % of the box), but optics downstream cannot exploit the gaps unless they image each emitter separately — exactly what microlens-based homogenizers do (L04).

</details>

## Stretch task — Import a real ray file
Download a ray file for a real LED from a manufacturer's website (several major LED manufacturers provide them in OpticStudio-readable format, sometimes after registration). Load it in a **Source File** object, check *Randomize?*, ray count and *Maximum Source File Rays in Memory*. Compare its far field (Detector Polar) with the datasheet plot, and its near field (Detector Rectangle 0.1 mm above the emitting surface) with a die photo. Note any discrepancies in `notes.md`.

## Reflection questions
1. When is a point source good enough for an LED, and when is it dangerously optimistic?
2. Why do LED packages with high-index domes emit more total light than bare chips, and what does this do to the étendue?
3. A colleague replaces a 940 nm LED with a 940 nm VCSEL array and narrows the camera bandpass filter from 50 nm to 15 nm. Explain the two physical reasons this works and one new risk.
4. Why might a professional *add* a diffuser in front of a laser source in a structured-light projector?

<details><summary>Answers</summary>

1. Good enough when the optics are many source diameters away and only the angular distribution matters (e.g. scene irradiance at 1 m). Dangerously optimistic for close-coupled optics (condensers, light pipes, DMD illumination): a point source has zero étendue, so it predicts near-100 % coupling and perfectly sharp images of the source.
2. The dome lowers the index step at the chip surface, so less light is trapped by TIR; the extracted light then leaves the dome over an apparent area $n^2$ larger (étendue $\pi n^2 A$) — more flux, more étendue, similar radiance.
3. VCSEL spectra are narrow (~1 nm) and drift less with temperature (< 0.1 nm/K vs. ~0.3 nm/K), so a narrow filter still passes all signal over the operating temperature range while rejecting more ambient light. Risks: speckle, eye-safety classification, and the angle shift of interference filters (the filter centre wavelength moves to the blue at oblique incidence — Course 04 L08).
4. To increase étendue/angular diversity deliberately: lower speckle contrast, lower radiance for eye safety, better fill of the homogenizer/DMD — as long as the increased étendue still fits the downstream acceptance.

</details>
