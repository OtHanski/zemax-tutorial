# L02 — Tasks: Surfaces, Sign Conventions, Sag, Conics and Aspheres

> Work in `work/` inside this lesson folder (e.g. save `work/L02_T3_bend_X+1.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Sign-convention drill (pen & paper)
**Goal:** Make the Cartesian convention automatic.
**Given:** Light travels left → right.
**Steps:** For each item give the sign (+/−) of the requested quantity.
1. $R_1$ and $R_2$ of a biconcave lens.
2. $R_1$ and $R_2$ of a positive meniscus whose convex side faces the object.
3. The object distance $l$ of a real object 300 mm to the left of a lens; the image distance $l'$ of a real image to the right.
4. The angle $u'$ of the paraxial marginal ray after a positive lens (ray started parallel to the axis at height $y > 0$).
5. The radius of a concave mirror facing the incoming light, and the thickness from the mirror to its focus.
6. Shape factor $X$ of: (a) plano-convex with the flat facing the object; (b) the meniscus in item 2; (c) a lens with $R_1 = 60$, $R_2 = -120$.
**Deliverable:** answers in `work/notes.md`.

<details><summary>Solution</summary>

1. $R_1 < 0$, $R_2 > 0$.
2. Both positive, with $R_1 < R_2$ (front surface more strongly curved).
3. $l < 0$, $l' > 0$.
4. $u' < 0$ (ray descends towards the axis).
5. $R < 0$ (centre of curvature to the left); thickness to the focus is negative.
6. (a) $c_1 = 0 \Rightarrow X = -1$. (b) $X > +1$. (c) $c_1 = 1/60$, $c_2 = -1/120$: $X = (1/60 - 1/120)/(1/60 + 1/120) = (1/120)/(3/120) = 1/3 \approx 0.333$.

</details>

## Task 2 — Sag, edge thickness and aspheric departure (Python)
**Goal:** Build a reusable `sag()` function — you will reuse it in L06 and in Course 07.
**Given / specs:** Standard/even-asphere sag formula from the lecture.
**Steps:**
1. Write `sag(r, R, k=0.0, A=())` returning $z$ for radius $R$ (use `np.inf` for flat), conic $k$ and coefficients `A = (a4, a6, ...)`. Use the stable form $cr^2/(1+\sqrt{1-(1+k)c^2r^2})$.
2. For $R = 102.7$ mm compute exact and parabolic sag at $r = 5, 10, 12.5$ mm.
3. Compute the edge thickness of the L01 lens (R = ±102.7, t = 4) for diameters 20, 25, 30, 35 mm. At what diameter would the edge reach 1.0 mm?
4. Plot the departure $z_{\text{conic}} - z_{\text{sphere}}$ for $R = -51.68$, $k = -2.3007$ over $0 \le r \le 12.5$ mm, in µm. Overlay the approximation $k c^3 r^4 / 8$.
5. Reproduce Geary's parabola departure (R = 625 mm, r = 125 mm) and express it in waves at 632.8 nm.
**Deliverable:** `work/sag.py`, plot, numbers in notes.
**Check yourself:** sag at r = 10: 0.48801 mm (exact) vs 0.48685 mm (parabolic). Edge thickness at Ø25: 2.473 mm. Departure at r = 10: ≈ 20.7 µm. Parabola: ≈ 0.1276 mm ≈ 202 waves.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
def sag(r, R, k=0.0, A=()):
    c = 0.0 if np.isinf(R) else 1.0/R
    z = c*r**2/(1 + np.sqrt(1 - (1+k)*c**2*r**2))
    for i, a in enumerate(A):
        z += a*r**(4 + 2*i)
    return z
def edge(t, R1, R2, r):
    return t - sag(r, R1) + sag(r, R2)
```
Edge thickness: Ø20 → 3.024 mm, Ø25 → 2.473 mm, Ø30 → 1.797 mm; solving `edge(...) = 1` (e.g. with `scipy.optimize.brentq`) gives a diameter of ≈ 35.0 mm (Ø35 → edge ≈ 1.00 mm). The departure plot rises as $r^4$: tiny (1.3 µm) at r = 5 but ~43 µm at r = 12.

</details>

## Task 3 — Bending the reference singlet (OpticStudio)
**Goal:** See with your own eyes that shape (not just power) controls image quality.
**Given / specs:** Start from `../L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx` (EPD 20 mm, fields 0/3.5/5°, F/d/C). For this task set **a single wavelength 0.5876 µm** and **a single field 0°** (keep a copy; do not overwrite the L01 file). Thickness 4 mm, N-BK7, Marginal Ray Height solve on the back thickness.
**Steps:**
1. Enter the four bendings from the worked example: $X = -1$ (∞ / −51.68), $X = 0$ (103.36 / −103.36), $X = +1$ (51.68 / ∞), $X = +2$ (34.45 / 103.36). Save each as `work/L02_T3_bend_X<value>.zmx`.
2. For each: record EFL (System Data), then remove the solve, run Quick Focus (RMS spot radius, centroid), and record the on-axis RMS spot radius and the focus shift relative to the paraxial BFL.
3. Use the LDE **Reverse Elements** tool on the X = +1 lens and confirm it turns into the X = −1 lens.
4. Plot RMS spot vs. X (a quick Python/Excel plot is fine). Where is the minimum?
**Deliverable:** four `.zmx` files and a table/plot.
**Check yourself:** (Python ray trace, d-light, on axis, best focus, square pupil sampling — expect ~10 % differences from OpticStudio)

| X | EFL (mm) | best-focus RMS radius (µm) |
|---|---|---|
| −1 | 100.00 | ≈ 75 |
| 0 | 100.66 | ≈ 27 |
| +1 | 100.00 | ≈ 19 |
| +2 | 98.06 | ≈ 47 |

The minimum is between X = 0.5 and 1 (≈ 17 µm near X ≈ 0.7) — the convex-plano orientation is ~4× better than the reversed plano-convex.

<details><summary>Hints / solution sketch</summary>

- The EFL changes slightly with bending because of the 4 mm thickness (thick-lens term, L03). For the plano forms EFL = 100.00 mm exactly because one surface has zero power.
- The flat-first plano-convex lens refracts all the power at one strongly curved surface with large angles of incidence — Snell's nonlinearity at work (L01 §3.4).
- This is a monochromatic, on-axis comparison. Off-axis, the best bending for coma differs slightly; the stop position matters too (L08).

</details>

## Task 4 — Conic and even-asphere singlet (OpticStudio)
**Goal:** Use a conic to remove spherical aberration, then emulate it with an even-asphere term, and see the limits.
**Given / specs:** The X = −1 lens from Task 3 (flat first, $R_2 = -51.68$ mm), d-light, on-axis.
**Steps:**
1. Set the Conic of surface 2 to $k = -n_d^2 = -2.3007$. Keep the M-solve (paraxial focus). Look at the spot diagram and ray fan. Save `work/L02_T4_hyperbolic.zmx`.
2. Restore the 3 wavelengths (F, d, C) and the fields 0/3.5/5°. Record the RMS spot for each field. Which aberrations are still there?
3. Back to d-light on axis. Change surface 2 to **Even Asphere**, set conic 0 and the 4th-order term to $\alpha_4 = k c^3/8 = 2.0835\times10^{-6}$ mm⁻³ (with $c = -1/51.68$). Compare the spot with step 1.
4. Check the paraxial EFL in System Data for steps 1 and 3. Did it change relative to the spherical lens?
**Deliverable:** saved files; notes with RMS values and answers.
**Check yourself:**
- Step 1: on-axis d-light spot collapses to (numerically) zero — well inside the Airy circle.
- Step 2: polychromatic on-axis RMS ≈ 50 µm (axial colour); at 5° the d-light RMS is ≈ 130 µm (coma and astigmatism).
- Step 3: the $r^4$ term alone leaves a small residual (≈ 1 µm RMS at paraxial focus) because the conic also contributes $r^6, r^8, \dots$ terms.
- Step 4: EFL = 100.00 mm in all cases — aspheric terms do not change paraxial properties.

<details><summary>Hints / solution sketch</summary>

In OpticStudio the Even Asphere parameter columns are labelled by order ("2nd Order Term", "4th Order Term", …). Leave the 2nd order term at 0. If you put a value in it, re-check the EFL: it will change.

</details>

## Task 5 — A mirror and negative thicknesses (OpticStudio)
**Goal:** Practise the mirror convention.
**Given / specs:** New file. EPD 20 mm, field 0° and 1°, wavelength 0.5876 µm. STO: Radius −200, Thickness −100, Material MIRROR. Image after it.
**Steps:**
1. Enter the system. Look at the Cross-Section (light goes back to the left).
2. Record the on-axis spot (RMS) for $k = 0$ (sphere) and $k = -1$ (paraboloid), at the paraxial focus.
3. Compare with the Airy radius ($1.22\lambda N$ with $N = 5$). Is a spherical F/5 mirror good enough on axis?
**Deliverable:** `work/L02_T5_mirror.zmx`, notes.
**Check yourself:** sphere ≈ 6 µm RMS at paraxial focus (≈ 2 µm at best focus) vs. Airy radius 3.6 µm — marginal; paraboloid ≈ 0 on axis but ≈ 4 µm RMS at 1° (coma — the paraboloid is perfect *only* on axis).

## Stretch task — the axicon
Following [Kidger §1.7.5, pp. 14–15], model an axicon in OpticStudio as a hyperboloid with very large curvature (e.g. $R = 0.01$ mm) and $k = -1/\cos^2\theta$ for a cone half-angle $\theta = 30°$ (so $k = -1.3333$). Send a collimated beam (EPD 10 mm) through a flat-backed N-BK7 axicon and look at the Cross-Section and a spot/footprint at several distances: you should see a line focus along the axis (the "Bessel beam" zone). Note any ray-trace errors at the apex.

## Reflection questions
1. Why do optical programs store curvature rather than radius?
2. Why does a conic constant not change the effective focal length?
3. A vendor quotes "asphere departure 150 µm". Why does this number matter to them?
4. Your design has a plano-convex lens used with collimated light. Which way round should it be mounted, and why?
5. What goes wrong if you copy "P = 0.36" from an older text into OpticStudio's Conic column?

<details><summary>Answers</summary>

1. A flat surface is $c = 0$ (no infinity), curvature enters paraxial power linearly, and optimization in $c$ is better behaved.
2. The paraxial region only sees the $\tfrac12 cr^2$ term, which does not depend on $k$ (Kidger Eq. 1.24).
3. It sets the manufacturing process (how much material to remove), tool size, cycle time and the test method (null optics/CGH for large departures).
4. Curved side towards the collimated beam (X ≈ +1): the bending is shared between two surfaces with smaller angles of incidence, giving ~4× less spherical aberration than the reverse.
5. $P = 1 + k$, so $P = 0.36$ means $k = -0.64$ (a prolate ellipsoid). Typing 0.36 gives an oblate ellipsoid — the aberration correction goes the wrong way.

</details>
