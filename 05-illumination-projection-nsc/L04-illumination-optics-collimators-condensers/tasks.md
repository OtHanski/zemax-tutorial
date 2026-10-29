# L04 — Tasks: Illumination Optics — Condensers, Köhler, Homogenizers, TIR Collimators

> Work in `work/` inside this lesson folder (e.g. save `work/L04_T2_rod.zmx`). Commit your designs, scripts and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — Size a fly's-eye homogenizer (pen & paper / Python)
**Goal:** Practise the design equations of §4.2.
**Given / specs:** DMD 0.2″-class: 854 × 480 mirrors at 5.4 µm (active area 4.6116 × 2.592 mm), ±17° tilt. Lenslets 0.80 × 0.45 mm, $f_{LA} = 4.0$ mm (thin lenses in air). Design target: illumination cone ≤ ±12° along each axis (leaving margin below 17° for the diagonal of the rectangular pupil).
**Steps:**
1. Condenser focal length from each axis. Why do the two values differ slightly?
2. Maximum input divergence (each axis) to avoid crosstalk.
3. Largest **odd** number of lenslets per axis that keeps the cone ≤ ±12°, and the resulting cone half-angles.
4. Étendue accepted by the array and delivered to the DMD; compare with the DMD's circular F/1.71 acceptance (3.21 mm² sr, L01 Task 4).
5. The input beam is a collimated LED: 1 × 1 mm die at the focus of a 40 mm collimator. Is its divergence within the acceptance?
**Deliverable:** numbers in `notes.md` (add a `flyseye()` function to your radiometry script).
**Check yourself:** $F = 23.06$ mm (x) and 23.04 mm (y) — the DMD aspect 1.7792 is not exactly 16/9 = 1.7778; acceptance ±3.2° (short axis), ±5.7° (long axis); 11 × 21 lenslets → ±10.8° × ±11.6°; étendue ≈ 1.87 mm² sr both ways (well inside 3.21); collimated-LED divergence ±0.72° ✓.

<details><summary>Solution sketch</summary>

$F = Df_{LA}/p$: 4.6116·4/0.8 = 23.06; 2.592·4/0.45 = 23.04. $N_{\max} = 2F\tan12°/p$ = 12.25 → 11 (x); 21.78 → 21 (y). Cones: $\arctan(11\cdot0.8/(2\cdot23.06)) = 10.8°$, $\arctan(21\cdot0.45/(2\cdot23.06)) = 11.6°$. $G = (8.8\cdot9.45)\cdot(0.8\cdot0.45)/4^2 = 1.871$ mm² sr; at the DMD $11.95\cdot4\cdot0.1908\cdot0.2049 = 1.870$ ✓. Collimator: $\arctan(0.5/40) = 0.72°$.

</details>

## Task 2 — Light pipe length vs. uniformity (OpticStudio)
**Goal:** See kaleidoscopic homogenization and measure the efficiency of a solid rod.
**Given / specs:** Units mm, W, wavelength 0.85 µm.
- Source Rectangle 1 × 1 mm (half widths 0.5), Lambertian (Cosine Exp 1), 1 W, Sobol sampling if available, at Z = 0.
- Rectangular Volume, N-BK7, front face at Z = 0.1 mm, cross-section 4.0 × 2.25 mm (half widths 2.0 × 1.125, same front and back), length $L$.
- Detector Rectangle `ABSORB` 0.05 mm after the rod exit, 4.0 × 2.25 mm, 32 × 18 pixels.
- A second large transparent detector just in front of the source (Z = −0.05 mm, 20 × 20 mm) to catch back-reflected light.
**Steps:**
1. Trace 10⁶ rays with polarization on, no splitting, for $L$ = 5, 10, 20, 40 mm. Save as `work/L04_T2_rod_L<L>.zmx` (or use a multi-configuration with $L$ as an operand — Course 03 L06).
2. For each, record total power on the exit detector and the uniformity: min/max and σ/mean over the pixels (export the text data and compute in Python; ignore nothing — the field edges matter for a DMD).
3. Show the exit detector for $L$ = 5 and 40 mm side by side. Count the source "images" you can identify by looking back into the rod in the 3D Layout with a few layout rays (optional).
4. Turn on ray splitting for $L$ = 20 mm: where does the reflected light go?
**Deliverable:** table (L, power, min/max, σ/mean), two detector images.
**Check yourself:** power ≈ 0.83 W for every length (Fresnel at entrance and exit faces for a Lambertian input: hemispherically averaged transmission ≈ 0.907 per face → ≈ 0.83 for both; TIR on the walls is lossless, and every ray that enters is inside the TIR condition: internal angles ≤ 41.5° hit the side walls at ≥ 48.5°). Uniformity improves strongly with length: a bright central patch at 5 mm, σ/mean of a few per cent (approaching the ray-noise floor of ~1/√(830 000/576) ≈ 2.6 %) by 40 mm.

<details><summary>Hints</summary>

- The ~0.1 mm gap between LED and rod is realistic (LEDs have a dome or a window); try 0.5 mm and see power drop as grazing rays miss the rod face.
- The noise floor: 576 pixels, ~830 000 rays reaching them → ~1440 rays/pixel → 2.6 % noise. You cannot claim better uniformity than that without more rays.

</details>

## Task 3 — Fly's-eye homogenizer in NSC (OpticStudio)
**Goal:** Build the worked-example homogenizer A (0.3″ DMD) with Lenslet Array objects and compare with "no homogenizer".
**Given / specs:** Units mm, W, 0.85 µm.
- Source: Source Rectangle 1 × 1 mm Lambertian, 1 W, at Z = 0.
- Collimator: Standard Lens N-BK7, plano-convex, curved side away from the LED, chosen for $f \approx 40$ mm (use $R = -(n-1)\cdot 40 = -20.39$ mm on the second face, first face flat, 6 mm thick, clear semi-diameter 12 mm, edge thickness ≈ 2.1 mm); put its flat face at Z = 36.0 mm (the front focal distance from the flat face is $f - t/n$ = 40 − 6/1.51 = 36.0 mm), then fine-tune Z until the beam after the lens looks best collimated in the layout.
- LA1 and LA2: **Lenslet Array 1** objects, 10 × 17 lenslets of 1.6 × 0.9 mm, focal length 6 mm (set the lenslet radius from $R = (n-1)f$ for the material you use — e.g. PMMA or N-BK7 — and use thin arrays), separated so that LA2 sits in LA1's focal plane. Hover over the parameter headers to map pitch, count and radius to the object's parameters.
- Condenser: focal length 25.92 mm (a Paraxial Lens object if available in your release, otherwise a Standard Lens of $f \approx 26$ mm), 5 mm after LA2.
- Detector Rectangle 8 × 5 mm (half widths 4 × 2.5), 80 × 50 pixels, at the condenser's back focal plane.
**Steps:**
1. Build and save as `work/L04_T3_flyseye.zmx`. First trace with the arrays' material set to blank (i.e. ignored as air) — this is "no homogenizer". What do you see on the detector?
2. Set the arrays to their material and trace 2 × 10⁶ rays. Record: size of the illuminated field, edge sharpness, uniformity (σ/mean inside the central 6.9 × 3.9 mm), and the power inside 6.912 × 3.888 mm vs. total on the detector.
3. Move LA2 by ±1 mm from LA1's focal plane. What happens to the field edges?
4. Replace the 1 × 1 mm LED by a 2 × 2 mm one. What appears around the main field, and why?
**Deliverable:** `.zmx`, detector images for steps 1, 2, 4; a table.
**Check yourself:** (1) without arrays the condenser forms an image of the far field of the collimated LED — a blurry spot, not a rectangle. (2) with arrays: a rectangle ≈ 6.9 × 3.9 mm with fairly sharp edges and σ/mean of a few % (noise-limited); most of the power on the detector falls inside the DMD rectangle, minus edge blur and Fresnel losses. (3) defocusing LA2 blurs the field edges (the lenslet apertures are no longer sharply imaged). (4) a 2 × 2 mm LED has ±1.4° divergence after the collimator — still within the ±4.3° acceptance, so the field stays clean; if you shorten the collimator focal length to ~10 mm you will exceed it and see displaced "ghost fields" from crosstalk.

<details><summary>Hints</summary>

- Arrays made of real lenslets have aberrations and the collimator is not perfect: expect some light in a soft border around the rectangle. That is the overfill you budget for.
- If nothing reaches the detector, check the array orientation (curved face direction) and that the condenser's focal plane coincides with the detector.

</details>

## Task 4 — Tapered rod: area-to-angle conversion (OpticStudio + pen & paper)
**Goal:** Verify $A\sin^2\theta$ conservation through a taper.
**Given / specs:** Worked example B: LED 1 × 1 mm Lambertian butt-coupled (0.05 mm gap) to an N-BK7 Rectangular Volume with front half widths 0.55 × 0.55 mm and rear half widths 1.5 × 0.84375 mm. Detector Rectangle right after the exit face, 3.0 × 1.6875 mm, with angular (radiant intensity) display.
**Steps:**
1. Predict the maximum output angle in air for an ideal taper.
2. Trace for taper lengths 5, 15, 40 mm. Read the angular extent of the output from the detector's radiant-intensity view (or put a polar detector right after the exit, centred on it).
3. Explain why the short taper does not reach the ideal.
4. What relay magnification puts the exit face onto the 0.3″ DMD, and what cone results there?
**Deliverable:** table + explanation.
**Check yourself:** ideal output half-angle 29.3° ($\sin\theta = \sqrt{1.21/5.06} = 0.489$); long tapers approach it (with a soft tail), short tapers leave a large fraction of light at large angles (some rays reflect only once or not at all and keep their large input angle; some even exit through the side walls). Relay $m = 2.304$; cone at DMD ≈ 12.3°.

## Task 5 — Collimator étendue limit (OpticStudio)
**Goal:** Confirm that no collimator beats $\sin\theta_{\text{out}} \ge \sqrt{A_s/A_e}$.
**Given / specs:** Parabolic reflector: Standard Surface, conic −1, `MIRROR`, vertex radius of curvature 5 mm (focal length 2.5 mm), aperture semi-diameter 10 mm (Ø 20 mm), with the 1 × 1 mm Lambertian LED at its focus facing the opening. Far-field Detector Polar (or a Detector Rectangle at 5 m in intensity mode).
**Steps:**
1. Trace and measure the far-field FWHM half-angle and the fraction of power within ±3.2°, ±6.4°, ±10°.
2. Add a central lens (Standard Lens, f ≈ 15 mm) to catch the direct light that escapes without hitting the reflector. What happens to the efficiency within ±10°?
3. Change the LED to 0.5 × 0.5 mm. How does the beam change?
**Deliverable:** `work/L04_T5_reflector.zmx`, numbers, a paragraph comparing with the étendue limit (3.2° for 1 × 1 mm, 1.6° for 0.5 × 0.5 mm into Ø 20 mm).
**Check yourself:** first, most of the light never touches the reflector: from the focus the rim is at $\arctan(10/7.5) = 53°$, so $\sin^2 53° = 64$ % of the Lambertian flux leaves directly as a wide, uncollimated cone. The reflected 36 % forms a beam far wider than the étendue limit near the axis (the reflector sees the die at very different distances: near the vertex the die subtends ~±11°, at the rim only ~±2–3°), so the power within ±3.2° is a modest fraction; halving the die size roughly halves the divergence. This is why TIR collimators combine a central lens with a TIR wall — and why they still end up at 1.5–2× the étendue limit.

<details><summary>Hints</summary>

At the vertex of a parabola with focal length $f_p$ the distance to the focus is $f_p$; at the rim of semi-diameter $h$ it is $f_p + h^2/(4f_p)$ = 2.5 + 100/10 = 12.5 mm. A 1 mm die (±0.5 mm) subtends $\pm\arctan(0.5/2.5) = \pm11.3°$ at the vertex and $\pm\arctan(0.5/12.5) = \pm2.3°$ at the rim.

</details>

## Stretch task — Köhler vs. critical, side by side
Take a source with structure: two 0.4 × 0.8 mm Source Rectangles side by side with a 0.2 mm gap (an LED with a central electrode). (a) Critical: image it with a single lens at magnification 3 onto a detector. (b) Köhler: put the source at the front focal plane of a collector, a field stop (Annulus or rectangular aperture) after it, and a condenser that images the field stop onto the detector. Compare the detector images. Then put a second detector in the condenser's pupil plane in (b) — where did the source structure go?

## Reflection questions
1. Why does Köhler illumination produce a uniform field even from a structured source, and where does the structure end up?
2. A fly's-eye homogenizer works beautifully with an LED but shows a fine grid pattern with a laser. Explain and propose two fixes.
3. Your rod-based illuminator has excellent uniformity but 15 % less flux than predicted. List three loss mechanisms to check first.
4. Marketing wants a "narrower beam" from the same LED collimator without making it bigger. What do you tell them?

<details><summary>Answers</summary>

1. Each source point produces a collimated beam that covers the whole field; all points add, so the field irradiance is the integral over the source and source structure maps to angle (it appears in the pupil, i.e. in the projection lens aperture — invisible in the image, but it affects which parts of the pupil carry light).
2. The array is periodic and the laser coherent: the channels interfere like a grating, producing fringes of period ≈ $\lambda F/p$. Fixes: diffuser (static or moving) before the arrays, a random/chirped lenslet array, multiple mutually incoherent emitters (VCSEL array), wavelength or polarization diversity.
3. Fresnel losses at uncoated rod faces (≈ 9 % each for Lambertian light), rod mounts or dirt frustrating TIR, overfill larger than planned (light outside the DMD), mismatch between the relay pupil and the projection pupil, absorption in the glass at your wavelength, LED binning/temperature.
4. Divergence is bounded by étendue: $\sin\theta \ge \sqrt{A_s/A_e}$. Only a smaller (or higher-radiance) source or a larger exit aperture narrows the beam.

</details>
