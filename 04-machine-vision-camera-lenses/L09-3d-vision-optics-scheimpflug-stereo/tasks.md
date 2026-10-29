# L09 — Tasks: Optics for 3D vision — triangulation, stereo baselines and Scheimpflug

> Work in `work/` inside this lesson folder (e.g. save `work/L09_T4_scheimpflug.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — Scheimpflug geometry in Python
**Goal:** Verify the Scheimpflug rule numerically and see the size of the defocus it removes.
**Given:** thin lens $f = 25$ mm; object plane crosses the axis at $u = 250$ mm and is tilted by $\theta_o = 60°$ from the perpendicular to the axis; F/4.
**Steps:**
1. Image three points of the tilted object plane (at heights −20, 0, +20 mm) with the thin-lens equation; fit the image line and compute its tilt $\theta_i$.
2. Check $\tan\theta_i = m\tan\theta_o$ and that the object line and image line meet the lens plane at the same height.
3. With an *untilted* sensor focused for the axial point, compute the defocus and the blur diameter at the ±20 mm points (use the working F/# $N_w = N(1+m)$).
4. Plot $\theta_i$ versus $\theta_o$ for $m$ = 0.05, 0.1, 0.5, 1.

**Deliverable:** `work/scheimpflug.py`, numbers, plot.
**Check yourself:** $m = 0.111$, $\theta_i = 10.9°$, both lines meet the lens plane at 144.3 mm; untilted sensor: image-side defocus −0.37 mm / +0.51 mm, blur ≈ 83 µm and 114 µm at $N_w$ = 4.44 — tens of pixels.

<details><summary>Hints / solution sketch</summary>

Object point at height $y$ on the plane lies at distance $s = u - y\tan\theta_o$; image distance $v = sf/(s-f)$, image height $-vy/s$. The sign of $\theta_i$ depends on your axis convention; the magnitude matches $\arctan(m\tan\theta_o)$. The object plane meets the lens plane at $y = u/\tan\theta_o$ = 144.3 mm.
</details>

## Task 2 — Baseline sizing tool (Python)
**Goal:** Build the system-level calculator you would use in a concept review.
**Given:** target depth noise 0.10 mm (1σ) at $z = 1.5$ m; sensor 4096 × 3000, $p$ = 2.74 µm; $f$ = 12 mm; correspondence precision 0.05 px.
**Steps:**
1. Compute the required baseline. Compute the horizontal half-FOV and the parallel-axis overlap start $z_\text{min}$ and the overlap fraction at 0.8, 1.5 and 2.5 m.
2. Plot $\delta z(z)$ from 0.5 to 2.5 m for your baseline and for 0.6× and 1.5× of it.
3. Compute the depth-scale error from a 30 K temperature change of an aluminium baseline.
4. Write a short paragraph: what would you change (f, p, b, δd) if the baseline must be ≤ 150 mm?

**Check yourself:** $b$ ≈ 257 mm; half-FOV 25.1°; $z_\text{min}$ ≈ 275 mm; thermal: 708 ppm → ≈ 1.06 mm at 1.5 m.

<details><summary>Hints / solution sketch</summary>

$b = z^2\,p\,\delta d/(f\,\delta z) = 1500^2\cdot0.00274\cdot0.05/(12\cdot0.1) = 256.9$ mm. Half-FOV $= \arctan(11.22/2/12) = 25.06°$. $z_\text{min} = b/(2\tan25.06°) = 274.6$ mm. Overlap fraction $1 - b/(2z\tan\theta)$: 0.66 at 0.8 m, 0.82 at 1.5 m, 0.89 at 2.5 m. Thermal: 30 × 23.6 = 708 ppm. To halve $b$ you must halve $\delta d$ (twice the fringe modulation: more light, better MTF at the fringe frequency) or double $f$ (half the field) — or accept 2× worse depth noise.
</details>

## Task 3 — From lens MTF to depth noise (pen & paper)
**Goal:** Connect the optics spec to the 3D spec.
**Given:** 4-step phase shifting, fringe period $P$ = 16 camera pixels; intensity noise 25 e⁻; fringe modulation before optics losses 600 e⁻ (i.e. with perfect projector and camera MTF); $f$ = 8 mm, $b$ = 150 mm, $p$ = 3.45 µm, $z$ = 1 m. Two camera lens options at the fringe frequency (18.1 lp/mm on the sensor), averaged over the depth range: lens A MTF 0.85, lens B MTF 0.55; projector MTF at the corresponding frequency 0.8; sensor MTF at 18 lp/mm ≈ 0.98.
**Steps:** compute the modulation, phase noise, disparity noise and depth noise for both lenses.
**Check yourself:** A: $B$ = 400 e⁻, $\sigma_\phi$ = 0.044 rad, $\delta d$ = 0.113 px, $\delta z$ ≈ 0.32 mm; B: $B$ = 259 e⁻, $\delta z$ ≈ 0.50 mm.

<details><summary>Hints / solution sketch</summary>

$B = 600\cdot0.85\cdot0.8\cdot0.98 = 399.8$ (A), $600\cdot0.55\cdot0.8\cdot0.98 = 258.7$ (B). $\sigma_\phi = \sqrt{2/4}\cdot25/B$: 0.0442 and 0.0683 rad. $\delta d = 16\sigma_\phi/2\pi$: 0.1126 and 0.174 px. $\delta z = (10^6/1200)\cdot\delta d\cdot0.00345$: 0.324 and 0.500 mm. A 35 % lower MTF costs 55 % more depth noise.
</details>

## Task 4 — A Scheimpflug laser-line camera (OpticStudio)
**Goal:** Model a tilted object plane and optimize the sensor tilt.
**Given / specs:** start with a Paraxial lens $f$ = 25 mm, F/4 (EPD 6.25 mm), λ = 0.66 µm (red laser); object plane 250 mm in front, tilted 60° about x; object-height fields along y: −20, −10, 0, 10, 20 mm (on the tilted plane).
**Steps:**
1. Make surface 0 a *Tilted* surface with the tilt (or use CBs after the object with ray aiming — try both and compare which field heights you actually get). Save `work/L09_T4_scheimpflug.zmx`.
2. With the image surface perpendicular, Quick Focus and record RMS spot per field.
3. Insert a Coordinate Break before the image; make *Tilt About X* variable; optimize (default RMS spot, chief-ray centroid) with the focus distance and tilt as variables. Compare the resulting tilt with $\arctan(m\tan60°)$ and record RMS spots.
4. Replace the Paraxial lens by a real lens: the sample `Double Gauss 28 degree field` scaled to $f$ = 25 mm (F/4). Repeat step 3. How does the real lens's field curvature change the optimum tilt?
5. Look at the CRA at the tilted sensor at both ends of the line (RAID). Is it symmetric?

**Deliverable:** file(s), table of spot sizes (untilted vs tilted), tilt angles.
**Check yourself:** paraxial: untilted spots at ±20 mm are tens of µm (cf. Task 1: blur 80–115 µm diameter); with the optimized tilt ≈ 10.9° they collapse to near zero. The real lens's optimum tilt differs slightly (field curvature and distortion of the lens), and the CRA becomes asymmetric between the two ends.

<details><summary>Hints / solution sketch</summary>

If you get "cannot find rays" errors with CBs on the object side, enable ray aiming and enter approximate pupil shifts, or use the Tilted surface (no ray aiming needed). Remember that paraxial data (EFL, image height in System Data) ignore coordinate breaks — judge only with real-ray analyses.
</details>

## Task 5 — Pattern contrast over the depth range (OpticStudio)
**Given:** your NIR receiver `../L08-filters-cover-glass-nir-and-ghosts/work/L08_T3_nir940.zmx`. *Save As* `work/L09_T5_depth_contrast.zmx`.
**Steps:**
1. Multi-Configuration with object distances 600, 800, 1000, 1200 mm (no refocus; image plane fixed at the 1000 mm focus or re-chosen at the harmonic mean — decide and justify).
2. Compute polychromatic FFT MTF at 18.1 lp/mm and 36.2 lp/mm (fringe periods of 16 and 8 pixels) at 0, 0.7 and 1.0 field for each configuration.
3. Plot MTF vs object distance. Which fringe period would you use as the finest pattern for this lens?
4. Repeat with the focus at the harmonic mean of 600 and 1200 mm. Does it help?

**Deliverable:** plots/tables, recommendation.
**Check yourself:** at 18 lp/mm the MTF should stay high (≈ 0.8+) over the whole range; at 36 lp/mm the range ends drop more, and the harmonic-mean focus equalizes near and far.

## Stretch task
Write a small Python simulation: a sinusoidal fringe (period 16 px) on a plane at depths 0.6–1.2 m is blurred by the projector (defocus disc for an F/2 projector focused at 0.9 m, $f_p$ = 12 mm, pixel pitch on the DMD 7.6 µm) and the camera (your lens's MTF from Task 5), sampled, noise added (shot + read), phase decoded with 4-step phase shifting; plot the depth noise vs depth and compare with the closed-form model of Task 3.

## Reflection questions
1. Why does depth noise grow with $z^2$, and what are the three optical levers to fight it?
2. Why is MTF at the fringe frequency over the depth range a better lens spec for structured light than MTF at Nyquist at best focus?
3. Why do laser-line profilers use Scheimpflug while area structured-light cameras usually don't?
4. What happens to the depth calibration if the baseline bracket expands with temperature?

<details><summary>Answers</summary>

1. $z = fb/d$ ⇒ $\delta z = z^2\delta d/(fb)$. Levers: longer $f$ (narrower field), better disparity precision (MTF, SNR, calibration stability), smaller pixels at constant precision in pixels; the baseline is a mechanical lever.
2. Depth noise ∝ 1/fringe modulation, which is ∝ system MTF at the fringe frequency, everywhere in the measurement volume; Nyquist at best focus says little about either.
3. The laser line lies in a single known plane — tilting the sensor brings all of it into focus at full aperture; an area camera measures a volume with no single plane to focus.
4. Depth scales with $b$: a relative change $\delta b/b$ gives the same relative depth error (e.g. 23.6 ppm/K for aluminium) unless compensated.
</details>
