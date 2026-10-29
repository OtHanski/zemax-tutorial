# L02 — Tasks: Camera first-order design

> Work in `work/` inside this lesson folder (e.g. save `work/L02_T3_paraxial_dof.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — A first-order camera calculator (Python)
**Goal:** Extend `../L01-image-sensors-and-sampling/work/sensor.py` into `camera.py` with the functions you will use for the rest of the course.
**Steps:**
1. Implement `focal_for_field(s, W, Wo)`, `magnification(f, s)`, `image_distance(f, s)`, `hyperfocal(f, N, c)`, `dof(f, N, c, s) -> (near, far)`, `n_opt(delta_img, lam)`.
2. Reproduce the L02 worked-example tables (FOV vs distance; DOF at 1000 mm for $c = p$ and $2p$).
3. Recompute Kenyon's DSLR example with his Eq. 4.21: $f = 50$ mm, $c = 8$ µm, $s = 3$ m, f/8. Compare with the exact near/far formulas.

**Deliverable:** `work/camera.py`, printed tables, a sentence on the Kenyon example in `notes.md`.
**Check yourself:** focus 1000 mm, F/2.8, $c = 3.45$ µm → 870–1176 mm. Kenyon's formula gives $\Delta s = 8\cdot(3000/50)^2\cdot0.008 = 230$ mm (one side), not 8 cm.

<details><summary>Hints / solution sketch</summary>

Exact limits for the Kenyon case: $H = 50^2/(8\cdot0.008)+50 = 39\,113$ mm; near = 3000·39063/(39113+3000−100) = 2789 mm, far = 3000·39063/(39113−3000) = 3245 mm. So the depth of field is about −211 / +245 mm, consistent with ≈230 mm from the approximate formula. Moral: always recompute book examples.
</details>

## Task 2 — Spec to focal length (pen & paper)
**Goal:** Practise the "field at nearest distance" rule.
**Given:** sensor B from L01 (2048 × 1536, 3.45 µm: 7.07 × 5.30 mm). The object field must be at least 500 mm × 400 mm at the nearest working distance of 400 mm (measured from the front principal plane).
**Steps:**
1. Which sensor direction limits the magnification? Compute $m$ and $f$.
2. What object field do you actually get at 400 mm and at 800 mm?
3. What is the object-space pixel size at 400 mm and 800 mm?
4. If the camera's front principal plane is 15 mm behind the front window, what working distance (from the window) corresponds to 400 mm?

**Deliverable:** answers in `notes.md`.

<details><summary>Hints / solution sketch</summary>

1. Horizontal needs $m \le 7.066/500 = 0.01413$; vertical needs $m \le 5.299/400 = 0.01325$. Vertical limits: $m = 0.01325$, $f = 400\cdot0.01325/1.01325 = 5.23$ mm.
2. At 400 mm: 533 × 400 mm. At 800 mm: $m = 5.23/794.8 = 0.00658$ → ≈ 1074 × 805 mm.
3. 0.26 mm at 400 mm, ≈ 0.52 mm at 800 mm.
4. 385 mm from the window. Write both numbers in a spec.
</details>

## Task 3 — Depth of field with the Multi-Configuration Editor (OpticStudio)
**Goal:** See the depth-of-field geometry in a paraxial model and match it to your formulas.
**Given / specs:** Paraxial surface (stop) with focal length 8 mm; aperture type Image Space F/# = 2.8; field type Object Height: 0, 200, 400 mm; wavelength 0.55 µm; object distance 800 mm.
**Steps:**
1. Build OBJ (thickness 800) → STO (Paraxial, f = 8) → IMA. Quick Focus. Check with PMAG and image distance that $v_0 = 8.0808$ mm. Save as `work/L02_T3_paraxial_dof.zmx`.
2. Open the Multi-Configuration Editor; add THIC for surface 0 with configurations 800, 600, 1200 mm. **Do not** refocus configurations 2 and 3.
3. For each configuration and for F/2, F/2.8, F/4, record the on-axis geometric spot diameter and RMS radius (Standard Spot Diagram).
4. Add an FFT MTF (0.55 µm, maximum frequency 145 lp/mm) for configurations 2 and 3 at F/2.8 and F/4. Compare with your intuition from Section 5.1.
5. Repeat step 4 at 0.85 µm.

**Deliverable:** table of spot sizes vs configuration and F/#; short comment on which F/# you would choose for this range in the visible and in the NIR.
**Check yourself:** for configurations 2 and 3 the defocus blur is a uniform disc of diameter ≈ $\delta'/N$ with $\delta' \approx 27$ µm: ≈ 13.6 / 9.7 / 6.8 µm at F/2 / 2.8 / 4; RMS radius = disc radius/√2 ≈ 4.8 / 3.4 / 2.4 µm. Configuration 1 is a point (paraxial lens).

<details><summary>Hints / solution sketch</summary>

- Image-side shifts: $v(600) - v(800) = 27.3$ µm and $v(800)-v(1200) = 27.1$ µm — equal by construction of the harmonic-mean focus.
- If your spots are much smaller, check that you set Image Space F/# (not Object space NA) and that configuration 2/3 did not get refocused.
- In the MTF you should see the defocus MTF dropping quickly with frequency at F/2, while at F/4 the curve is lower near the diffraction cutoff but better at mid frequencies over the whole range. In the NIR, the diffraction term grows by 0.85/0.55 = 1.55× and the optimum shifts to a faster aperture (~F/3.6 vs ~F/4.5).
</details>

## Task 4 — CoC from the projected pattern (pen & paper + Python)
**Goal:** Replace "1 pixel" with a measurement-driven blur budget.
**Given:** A structured-light pattern whose finest period on the sensor is 12 pixels ($p = 3.45$ µm); you require ≥ 50 % geometric defocus MTF at that frequency; $f = 8$ mm, F/2.8, focus at 800 mm.
**Steps:**
1. Compute the pattern frequency $\nu_\text{pat}$ (lp/mm).
2. The MTF of a uniform blur disc of diameter $b$ is $2J_1(\pi b\nu)/(\pi b\nu)$. Find (numerically) the largest $b$ with MTF ≥ 0.5 at $\nu_\text{pat}$.
3. Convert to an image-side focus tolerance $\pm\delta' = \pm bN$ and then to near/far object distances.

**Deliverable:** numbers and a one-paragraph comment comparing with the 1-pixel DOF of the worked example.
**Check yourself:** $\nu_\text{pat} = 24.2$ lp/mm; $b \le 29$ µm; $\delta' = \pm 82$ µm; sharp from ≈ 402 mm to beyond infinity.

<details><summary>Hints / solution sketch</summary>

$2J_1(x)/x = 0.5$ at $x = 2.215$ → $b\nu = 0.705$ → $b = 0.705/24.15$ mm = 29.2 µm. $\delta' = 29.2 \times 2.8 = 81.7$ µm. Near: $v = 8.0808 + 0.0817 = 8.1625$ mm → $s = vf/(v-f) = 402$ mm. Far: $v = 7.9991 < f$ → beyond infinity. For coarse patterns, depth of field is not the limit — the finest pattern frequency and the diffraction/aberration MTF are. This is why structured-light systems choose pattern periods with the depth range in mind (L09).
</details>

## Task 5 — Optimum F/# for an NIR close-range camera (pen & paper)
**Given:** $f = 6$ mm; depth range 300–600 mm; wavelengths 0.85 µm and 0.94 µm.
**Steps:** compute the harmonic-mean focus, $\delta'$, $N_\text{opt}$ and the minimum RSS blur at both wavelengths. Compare with the pixel size of a 2.74 µm sensor.
**Check yourself:** $s_0 = 400$ mm, $\delta' = 30.9$ µm, $N_\text{opt} = 3.9$ (0.85 µm) and 3.7 (0.94 µm), blur ≈ 11.3 and 11.9 µm (≈ 4 pixels of 2.74 µm).

<details><summary>Hints / solution sketch</summary>

$v(300) = 6.1224$, $v(600) = 6.0606$ mm → $\delta' = 0.0309$ mm. $N_\text{opt} = \sqrt{0.0309/(2.44\lambda)}$. Blur $= \sqrt2\,\delta'/N_\text{opt}$. Small pixels do not help here: the depth range, not the sensor, limits resolution at the range ends.
</details>

## Stretch task
Plot, in Python, the RSS blur $b_\text{tot}(N)$ at the range ends for the worked example (600–1200 mm, $f = 8$ mm) at 0.55, 0.85 and 0.94 µm, together with the relative exposure $\propto 1/N^2$. Mark the F/# that maximises "exposure subject to $b_\text{tot} \le 3p$". This "light vs sharpness" plot is a standard slide in a camera design review.

## Reflection questions
1. Why is there more depth of field behind the focus distance than in front of it?
2. Your customer specifies FOV as "60° diagonal". Why is that ambiguous for a machine-vision camera used at 0.5 m, and what would you ask?
3. Why does the optimum F/# for a given depth range decrease in the NIR?
4. A colleague proposes to fix the depth-of-field problem by using a smaller pixel sensor with the same lens. What happens?

<details><summary>Answers</summary>

1. Object distance is a $1/v$-like function of image distance: equal image-side defocus corresponds to a larger object-space interval on the far side ($\Delta s \propto s^2$).
2. The angle is defined from the entrance pupil, and the useful quantity is object field at specific distances; also whether it is rectilinear/including distortion and whether it is the sensor diagonal or the image circle. Ask for the field size at the nearest distance and the distance reference.
3. Diffraction blur grows with $\lambda$, while defocus blur does not; balancing them moves the optimum to a smaller $N$ ($N_\text{opt}\propto\lambda^{-1/2}$).
4. The blur in µm is unchanged, so it covers more pixels: Nyquist rises but the delivered resolution at the range ends does not; you gain only near best focus (and lose light per pixel).
</details>
