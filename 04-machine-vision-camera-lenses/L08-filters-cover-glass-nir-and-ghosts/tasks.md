# L08 — Tasks: Filters, cover glass, NIR design and ghosts

> Work in `work/` inside this lesson folder (e.g. save `work/L08_T3_nir940.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4.5 h

## Task 1 — Plates by hand (pen & paper + Python)
**Goal:** Quantify focus shift and plate spherical aberration.
**Steps:**
1. Verify Geary's window example: $t = 20$ mm, $n = 1.5168$.
2. For a 0.5 mm N-BK7 cover glass at 940 nm ($n$ = 1.50837), compute the paraxial focus shift and the exact focus shift of the marginal ray at F/2.8, F/2.0 and F/1.4 using Snell's law ($\Delta z(U) = t\,[1 - \tan U'/\tan U]$, $\sin U' = \sin U/n$). The difference is the plate's longitudinal spherical aberration.
3. Compare with the third-order estimate $\delta z_\text{SA} \approx t\,(n^2-1)\,U^2/(2n^3)$.
4. Compare each result with the depth of focus $\pm2\lambda N^2$ at 940 nm. When does the plate's SA matter?

**Check yourself:** Geary: 6.81 mm. Cover glass: paraxial 168.5 µm; marginal minus paraxial ≈ 2.9 µm (F/2.8), 5.7 µm (F/2.0), 11.2 µm (F/1.4); third-order estimate 2.9 µm at F/2.8. Depth of focus ±14.7 µm (F/2.8), ±7.5 µm (F/2), ±3.7 µm (F/1.4): the plate matters at F/2 and faster.

<details><summary>Hints / solution sketch</summary>

$U = \arctan(1/2N)$: 10.12° at F/2.8. The SA is overcorrected (marginal focus further away than paraxial). Since the optimizer can compensate a known plate, the real message is: include the plate *before* optimization; if the plate thickness changes later (another sensor package), the lens must be re-balanced.
</details>

## Task 2 — Filter response over the cone (Python)
**Goal:** Compute what each pixel "sees" through a band-pass filter.
**Given:** filter transmission at normal incidence $T_0(\lambda) = \exp[-\ln2\,(2(\lambda-\lambda_c)/W)^8]$ with $\lambda_c$ = 940 nm, $W$ = 20 nm; $n_\text{eff}$ = 1.8; F/2.8 cone; CRA = 0°, 3° and 15°.
**Steps:**
1. Implement the angle shift and the cone average: sample ray directions uniformly over the cone's solid angle (or uniformly over the circular pupil), tilt the cone by the CRA, compute each ray's AOI and shifted spectrum, and average.
2. Plot the effective spectra for CRA = 0, 3, 15° and report the centre shift and peak transmission.
3. Find the normal-incidence centre wavelength you should order so that, for the CRA = 3° lens, the effective passband is centred on 940 nm.

**Check yourself:** mean shifts ≈ −2.25 nm (CRA 0°), −2.64 nm (3°), −11.8 nm (15°); the 15° case also broadens strongly (edge rays up to −26.5 nm). Order ≈ 942.6 nm for the low-CRA lens.

<details><summary>Hints / solution sketch</summary>

For a uniform cap of half-angle α around direction CRA: $\cos t$ uniform in $[\cos\alpha, 1]$, azimuth uniform; rotate by CRA about x; AOI = arccos of the z-component. Mean of $\sin^2(\text{AOI})$ ≈ $\sin^2\text{CRA} + \alpha^2/2$ for small angles, which explains why the shift grows so fast with CRA.
</details>

## Task 3 — A 940 nm version of your lens (OpticStudio)
**Goal:** Convert a visible design to a narrow-band NIR receiver.
**Given:** `../L04-compact-fixed-focus-lens-project/work/L04_S2_final.zmx` (or your L04 NIR stretch file). *Save As* `work/L08_T3_nir940.zmx`.
**Steps:**
1. Change wavelengths to 0.930, 0.940, 0.950 µm (weights 1:2:1). Replace the IR-cut filter by a 0.5 mm band-pass filter substrate (N-BK7 or fused silica — e.g. F_SILICA in the SCHOTT/MISC catalogue; name varies) placed 0.5 mm in front of the cover glass.
2. Before re-optimizing: Quick Focus and note the focus change from the visible design. Then re-optimize.
3. Add RAID rows at the filter's first surface for the chief ray and for marginal rays (Py = ±1, Px = ±1) at 0, 0.7, 1.0 field; export and compute the per-field AOI range and filter shift (Task 2 code).
4. Evaluate MTF at 72 lp/mm, distortion, RI. What got better or worse vs visible?
5. Repeat with a VCSEL-like single wavelength 0.940 and multi-configurations at 0.9365 and 0.9435 µm (±50 K × 0.07 nm/K): how much does the focus/EFL move?

**Deliverable:** file, AOI table, filter-shift table, comparison notes.
**Check yourself:** the visible-to-940 nm refocus is of order 0.1–0.2 mm for an 8 mm lens; within 930–950 nm the chromatic spread is a few µm; MTF at 72 lp/mm is lower than visible mainly due to diffraction (diffraction MTF at 72 lp/mm, F/2.8: 0.85 at 0.588 µm vs 0.76 at 0.94 µm); VCSEL drift changes focus by far less than 1 µm.

<details><summary>Hints / solution sketch</summary>

Diffraction MTF at 72.5 lp/mm and F/2.8: $s = 72.5\cdot0.94\times10^{-3}\cdot2.8 = 0.191$ → MTF ≈ 0.76. If AOI at the filter exceeds ~20° anywhere, the passband will split by polarization at the field edge — a reason to keep the CRA low.
</details>

## Task 4 — Ghost hunting (OpticStudio)
**Given:** `work/L08_T3_nir940.zmx`.
**Steps:**
1. Run the Ghost Focus Generator in double-bounce mode with a realistic reflector coating (or 0.5 % reflectance if your version allows a simple setting). List the 5 ghosts that focus closest to the image plane.
2. For the worst ghost, open its saved ghost lens file and run a Geometric Image Analysis (or spot diagram) to estimate its size and relative irradiance at the sensor.
3. Identify the filter/cover-glass ghosts. Estimate by hand the halo diameter of the "sensor → cover glass top surface → sensor" ghost (cover glass 0.5 mm, $n$ = 1.51, air gap to die 0.4 mm, F/2.8).
4. Propose two design changes that reduce the worst image ghost, and implement one (e.g. change the curvature of the offending surface, or use GPIM in the merit function while holding MTF).

**Deliverable:** ranked ghost table and before/after numbers.
**Check yourself:** sensor/cover-glass ghost: air-equivalent round trip $2(0.4 + 0.5/1.51) = 1.46$ mm → halo ≈ 1.46/2.8 ≈ 0.52 mm diameter (≈ 150 pixels of 3.45 µm). Surfaces concave toward the image near the back of the lens often produce the most focused lens ghosts.

## Task 5 — Bandwidth budget (pen & paper)
**Given:** an LED-based 850 nm system: LED centre 850 ± 5 nm, FWHM 30 nm, drift 0.25 nm/K over 0–50 °C (calibrated at 25 °C); receiver CRA ≤ 5°, F/2.0; filter $n_\text{eff}$ = 2.0, centre tolerance ±3 nm.
**Steps:** derive a reasonable filter centre and FWHM; explain why LED-based systems need much wider filters than VCSEL-based ones, and what that costs in ambient-light rejection.
**Check yourself:** drift ±6.25 nm; cone at F/2 (α = 14.0°) plus CRA 5° → worst edge-ray AOI 19.0°, shift ≈ −11.4 nm with $n_\text{eff}$ = 2.0; a FWHM of ~60 nm is needed to pass most of the LED spectrum over temperature — roughly 3× the VCSEL case.

<details><summary>Hints / solution sketch</summary>

Edge-ray AOI = 5° + 14.0° = 19.0°: shift $= 850[\sqrt{1-(\sin19.0°/2)^2}-1] = -11.4$ nm with $n_\text{eff}$ = 2.0 (−19.0 nm if $n_\text{eff}$ were 1.55 — $n_\text{eff}$ matters; ask the vendor). The cone-averaged centre shift is roughly half the edge-ray value. Add half-widths: LED spectrum ±15, LED tolerance ±5, drift ±6.25, filter ±3, angle ≈ −6 (centre) to −11 (edge) → order a centre ≈ 855 nm and FWHM ≈ 60 nm. A 3× wider passband admits ~3× more broadband ambient light, i.e. √3 more ambient shot noise.
</details>

## Stretch task
Model the band-pass filter as an NSC object with a coating file (or table coating) in a non-sequential version of your lens (Course 05 L02/L06 preview), launch a 940 nm source with an angular distribution matching your field, and compare transmitted power at the image centre and corner with your Task 2 prediction.

## Reflection questions
1. Why does a plate in collimated space not affect image quality, while the same plate in a converging beam does?
2. Why is the image-space position preferred for a narrow NIR band-pass filter, and what lens property makes it work well?
3. Why are flat surfaces near the sensor ghost-prone?
4. You must use one lens for a visible colour camera and an NIR structured-light camera. What are your options?

<details><summary>Answers</summary>

1. In collimated space all rays of a field point cross the plate at the same angle, so they are displaced equally (no path-difference variation across the pupil); in a converging beam the displacement depends on ray angle → focus shift and aberrations.
2. The AOI range is set by CRA + cone half-angle and is the same for all field points if the CRA is small; low CRA (near image-space telecentricity) is the enabling property.
3. Their reflections return almost on themselves with little defocus (small round-trip distance), so the ghost is relatively concentrated; and the sensor itself is a strong reflector.
4. Dual-band correction (apochromat-like glass choice) with a dual-band filter; or two focus positions (motorized or two variants); or separate lenses; or accept reduced performance in one band — decide with an MTF budget per band.
</details>
