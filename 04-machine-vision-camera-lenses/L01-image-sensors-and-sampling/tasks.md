# L01 — Tasks: Image sensors and sampling

> Work in `work/` inside this lesson folder (e.g. save `work/L01_T3_paraxial_camera.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Sensor sheet in Python (Python)
**Goal:** Build a small reusable `sensor.py` you will import in every lesson of this course.
**Given / specs:** these sensors (all monochrome, 100 % fill factor assumed):

| Name | $N_x \times N_y$ | $p$ (µm) |
|---|---|---|
| A | 1920 × 1200 | 5.86 |
| B | 2048 × 1536 | 3.45 |
| C | 4096 × 3000 | 3.45 |
| D | 4024 × 3036 | 1.85 |
| E | 1440 × 1080 | 3.45 |

**Steps:**
1. Write a `Sensor` dataclass with `nx, ny, pitch_um` and properties `width_mm, height_mm, diag_mm, nyquist_lpmm`.
2. Add a function `mtf_pixel(nu, a_um)` (sinc) and `mtf_diff(nu, lam_um, fno)` (circular-pupil diffraction MTF).
3. Print a table of W, H, D, $\nu_N$ for A–E, and guess each sensor's "optical format" name from the diagonal (≈16 mm per inch).
4. For sensor B, plot `mtf_diff × mtf_pixel` at $\nu_N$ versus F/# from 1.4 to 8 for λ = 0.55, 0.85 and 0.94 µm.

**Deliverable:** `work/sensor.py`, the table and plot, a two-line conclusion in `notes.md`.
**Check yourself:** at F/2.8 and 0.55 µm the product for B is ≈ 0.46; at 0.94 µm ≈ 0.34.

<details><summary>Hints / solution sketch</summary>

| Sensor | W (mm) | H (mm) | D (mm) | $\nu_N$ (lp/mm) | format |
|---|---|---|---|---|---|
| A | 11.25 | 7.03 | 13.27 | 85.3 | 1/1.2" |
| B | 7.07 | 5.30 | 8.83 | 144.9 | ~1/1.8" |
| C | 14.13 | 10.35 | 17.52 | 144.9 | 1.1" |
| D | 7.44 | 5.62 | 9.33 | 270.3 | ~1/1.7" |
| E | 4.97 | 3.73 | 6.21 | 144.9 | ~1/2.9" |

Diffraction MTF at 145 lp/mm, F/2.8: 0.718 (0.55 µm), 0.526 (0.94 µm). Times 0.637 → 0.457 and 0.335. Sensor D at Nyquist (270 lp/mm) needs a very fast, very good lens: at F/2.8, 0.55 µm, $s = 0.416$ and MTF$_\text{diff}$ ≈ 0.48 even before the pixel. Conclusion to draw: small pixels plus NIR push you toward F/2 or faster, and NIR systems should specify at $\nu_N/2$ rather than $\nu_N$.
</details>

## Task 2 — Format traps (pen & paper)
**Goal:** Avoid the most common lens-procurement error.
**Given:** A catalog M12 lens is specified "for 1/2.3-inch sensors, image circle 7.8 mm, CRA < 12°". You want to use it on (a) sensor B above, (b) sensor E above, (c) a sensor with a 25° linear CRA spec.
**Steps:**
1. For (a) and (b) decide whether the image circle covers the sensor diagonal; if not, what fraction of the diagonal is covered?
2. For (c) explain what you would see in a flat-field image.
3. A colleague says "1/2.3 inch is 11 mm diagonal". Correct him in one sentence.

**Deliverable:** answers in `notes.md`.

<details><summary>Hints / solution sketch</summary>

1. (a) Sensor B diagonal 8.83 mm > 7.8 mm: the corners are outside the image circle (dark/vignetted corners); coverage 7.8/8.83 = 88 % of the diagonal. (b) Sensor E (6.21 mm) is covered with margin.
2. A lens with CRA < 12° on a sensor whose microlenses are shifted for 25° at the corner: mismatch ~13° at the corner → strong corner shading (and colour shading on a Bayer sensor); the effect grows toward the corners. A low-CRA lens on a high-CRA sensor is just as bad as the reverse.
3. "The inch name is a vidicon-tube legacy ≈ 1.5 × the diagonal; a 1/2.3-inch sensor is about 7.7 mm diagonal."
</details>

## Task 3 — A paraxial camera with cover glass and CRA readout (OpticStudio)
**Goal:** See CRA follow from stop position, and see the cover-glass focus shift.
**Given / specs:** object at infinity; field type Real Image Height, fields 0, 1.65, 2.75, 3.85, 5.5 mm; wavelength 0.55 µm only; Paraxial surface with focal length 8 mm; EPD 2.857 mm (F/2.8); cover glass N-BK7, 0.5 mm thick, followed by 0.3 mm air to the image.
**Steps:**
1. Build: OBJ (infinity) → STO (Paraxial, f = 8 mm) → air gap (use a marginal-ray-height solve or Quick Focus) → plate 0.5 mm N-BK7 → 0.3 mm air → IMA. Save as `work/L01_T3_paraxial_camera.zmx`.
2. First, set the plate material to blank (air) and note the paraxial back focus. Then set N-BK7 and Quick Focus again: by how much did the lens-to-sensor distance increase?
3. Add five RAID rows to the Merit Function Editor (surface = image, Hy = 0, 0.3, 0.5, 0.7, 1.0, Px = Py = 0, weight 0). Record CRA vs image height.
4. Now insert a dummy surface 8 mm *in front of* the paraxial lens, make it the stop, and adjust so that the system is image-space telecentric. Repeat the RAID table.
5. Switch the wavelength to 0.85 µm and Quick Focus; note the new shift.

**Deliverable:** file, CRA tables for both stop positions, focus shifts in `notes.md`.
**Check yourself:** stop at lens: CRA ≈ 11.7°, 19.0°, 25.7°, 34.5° at 30/50/70/100 % field (tan CRA = h/8). Stop at front focal point: CRA ≈ 0° everywhere. Plate shift ≈ 0.171 mm at 0.55 µm and 0.169 mm at 0.85 µm.

<details><summary>Hints / solution sketch</summary>

- With the stop on the paraxial lens, the exit pupil is at the lens, 8 mm (+ plate shift) from the image: $\tan\text{CRA} = h/8$ gives 11.65°, 18.97°, 25.70°, 34.51°. The plate does not change the CRA in air.
- With the stop in the front focal plane, the exit pupil is at infinity: chief rays leave parallel to the axis. This is the "telecentric limit" — note that the paraxial lens must now be large (semi-diameter grows to roughly $h + \text{EPD}/2$).
- $\Delta z = t(1-1/n)$ with $n_{0.55} = 1.5185$: 0.1707 mm; $n_{0.85} = 1.5098$: 0.1688 mm.
- If RAID returns 0 everywhere in step 3, check that you put the image surface number and Px = Py = 0.
</details>

## Task 4 — NIR photon budget (Python)
**Goal:** Feel the 850 nm vs 940 nm trade.
**Given:** image irradiance $E = 0.05$ W/m² (in-band, from the projector), exposure 2 ms, $p = 3.45$ µm, temporal dark noise 3 e⁻; QE 0.30 at 850 nm, 0.15 at 940 nm.
**Steps:**
1. Compute photons, electrons and SNR at each wavelength.
2. What exposure gives SNR = 50 at each wavelength (same irradiance)?
3. List two system reasons (not sensor reasons) why one might still pick 940 nm.

**Deliverable:** numbers and reasoning in `notes.md`.
**Check yourself:** SNR ≈ 39 (850 nm) and ≈ 29 (940 nm).

<details><summary>Hints / solution sketch</summary>

$N_\gamma = E p^2 t \lambda/(hc)$: 5093 photons at 850 nm, 5632 at 940 nm. Electrons: 1528 and 845. SNR $= N_e/\sqrt{N_e+9}$: 39.0 and 28.9. SNR = 50 needs $N_e \approx 2509$ e⁻ → 3.3 ms at 850 nm, 5.9 ms at 940 nm. System reasons for 940 nm: a deep atmospheric water absorption band reduces solar background outdoors; less visible red glow from the projector; some VCSEL/laser availability. Reasons for 850 nm: QE, more projector efficiency options, smaller diffraction (L02).
</details>

## Task 5 — Read a real datasheet (analysis)
**Goal:** Practise extracting optical-interface requirements.
**Steps:**
1. Pick a sensor used (or considered) in your products, or a public one (e.g. a Sony Pregius/Pregius S or onsemi global-shutter sensor). Find: pixel pitch, active area, CRA specification (and whether several microlens variants exist), cover glass thickness and material/index, QE at 850 and 940 nm, temporal dark noise, saturation capacity (EMVA 1288 if available).
2. Write these into a "sensor interface" table in `notes.md` — you will reuse it as the sensor section of the L04 and L10 specification.

**Deliverable:** the table, with sources.

## Stretch task
Simulate aliasing: in Python, render a sinusoidal bar target of frequency 0.8 $\nu_N$, 1.0 $\nu_N$ and 1.3 $\nu_N$ (slightly rotated) through a diffraction-limited F/2.8 PSF at 0.55 µm, integrate over 3.45 µm pixels, and display the sampled images. Observe the moiré at 1.3 $\nu_N$ and the phase sensitivity of contrast at exactly $\nu_N$.

## Reflection questions
1. Why is "MTF at Nyquist" a fragile specification, and what would you specify alongside it?
2. A BSI sensor tolerates larger CRA. Does that mean CRA no longer matters for your lens? Why or why not?
3. Why does the cover glass shift focus but not change the CRA measured in air?
4. Why does sensor MTF in the NIR tend to be lower than in the visible even with identical pixel geometry?

<details><summary>Answers</summary>

1. Contrast at exactly $\nu_N$ depends on the phase between pattern and pixel grid (0 to full contrast), and aliasing begins there; specify also at $\nu_N/2$ and give field and focus conditions.
2. It still matters: larger acceptance reduces but does not remove shading/crosstalk; QE still falls with angle, and fast lenses deliver wide cones around the chief ray. Match within the vendor's tolerance anyway.
3. A parallel plate refracts the ray in and back out by the same angle (Snell twice with parallel faces), so the exit angle equals the entrance angle; the ray is displaced laterally and the focus moves by $t(1-1/n)$.
4. NIR photons are absorbed deep in the silicon; the carriers diffuse laterally before collection and can be collected by a neighbouring pixel (electrical crosstalk), widening the pixel's effective response.
</details>
