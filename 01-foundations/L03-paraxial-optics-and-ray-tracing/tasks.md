# L03 — Tasks: Paraxial Optics and Paraxial Ray Tracing

> Work in `work/` inside this lesson folder (e.g. save `work/L03_T5_finite_conjugate.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4–5 h

## Task 1 — y–nu table by hand: Geary's biconvex lens (pen & paper)
**Goal:** Do one complete paraxial trace with a calculator so the method is in your fingers.
**Given / specs:** Geary's Ch. 2 lens: $R_1 = +100$ mm, $R_2 = -100$ mm, $t = 10$ mm, $n = 1.5168$, air outside, object at infinity, marginal ray at $y_1 = 20$ mm (EPD 40).
**Steps:**
1. Compute $\phi_1$, $\phi_2$ and the thick-lens power.
2. Fill in a y–nu table for the marginal ray (rows: $c$, $\phi$, $t/n$, $y$, $nu$).
3. Compute EFL, BFL and the position of P′ relative to surface 2, and of P relative to surface 1. What is PP′? Compare with "PP′ ≈ t/3".
**Deliverable:** table in `work/notes.md`.
**Check yourself:** EFL ≈ 98.43 mm, BFL ≈ 95.07 mm (Geary Fig. 2.4: 98.42 and 95.068).

<details><summary>Solution</summary>

- $\phi_1 = \phi_2 = 0.5168/100 = 0.005168$ mm⁻¹; $t/n = 6.59283$; $\phi = 0.010336 - 6.59283 \times 0.005168^2 = 0.0101599$ → EFL = 98.426 mm.
- S1: $nu' = -20 \times 0.005168 = -0.10336$; $u' = -0.068143$; $y_2 = 20 + 10(-0.068143) = 19.3186$.
- S2: $nu' = -0.10336 - 19.3186 \times 0.005168 = -0.203198$.
- EFL $= 20/0.203198 = 98.426$; BFL $= 19.3186/0.203198 = 95.072$ mm.
- $\delta' = 95.072 - 98.426 = -3.354$ mm (P′ 3.354 mm inside from S2); P is 3.354 mm inside from S1 by symmetry. PP′ = 10 − 6.707 = 3.29 mm ≈ $t/3$ ✓.

</details>

## Task 2 — Two separated thin lenses: a telephoto (pen & paper)
**Goal:** Use the two-element power formula and see principal planes leave the lens.
**Given / specs:** Thin lens 1: $f_1 = +50$ mm; thin lens 2: $f_2 = -25$ mm, 30 mm behind lens 1; air.
**Steps:**
1. Compute the system power and EFL with $\phi = \phi_1 + \phi_2 - d\phi_1\phi_2$.
2. Trace a ray $y_1 = 1$, $u = 0$ and find BFL.
3. Locate P′ (relative to lens 2) and P (relative to lens 1). Sketch the system with F′, P′.
4. Compute the *telephoto ratio* = (lens 1 to focus) / EFL.
**Check yourself:** EFL = 250 mm; BFL = 100 mm; telephoto ratio 0.52.

<details><summary>Solution</summary>

$\phi = 0.02 - 0.04 + 30 \times 0.02 \times 0.04 = 0.004$ → EFL = 250 mm. Ray: $u'_1 = -0.02$, $y_2 = 1 - 0.6 = 0.4$, $u'_2 = -0.02 + 0.4 \times 0.04 = -0.004$ → BFL = 0.4/0.004 = 100 mm. $\delta' = 100 - 250 = -150$ mm: P′ is 150 mm *in front of* lens 2 (120 mm in front of lens 1!). $\delta = d\phi_2/\phi = 30 \times (-0.04)/0.004 = -300$ mm: P is 300 mm in front of lens 1. Physical length 30 + 100 = 130 mm vs EFL 250 → ratio 0.52. This is the principle of the telephoto lens (Course 02 L11): the principal planes, and thus the "effective lens position", sit far in front of the hardware.

</details>

## Task 3 — Write a paraxial tracer and compare with OpticStudio (Python + OpticStudio)
**Goal:** Build your own first-order engine and validate OpticStudio's reports against it (and vice versa). You will extend this script in later lessons (pupils in L04, Seidel sums in Course 02).
**Given / specs:**
- Prescription format: a list of surfaces `(R, t, material)` where `t` is the thickness *after* the surface and `material` is the medium *after* it (`None` = air).
- N-BK7 Sellmeier coefficients (SCHOTT): $B_1 = 1.03961212$, $B_2 = 0.231792344$, $B_3 = 1.01046945$, $C_1 = 0.00600069867$, $C_2 = 0.0200179144$, $C_3 = 103.560653$ (µm²), with $n^2 - 1 = \sum B_i\lambda^2/(\lambda^2 - C_i)$, λ in µm.
**Steps:**
1. Write `index(material, lam_um)` (Sellmeier for N-BK7; 1.0 for air).
2. Write `trace(prescription, lam, y0, nu0, obj_dist=inf)` that returns per-surface `y` and `nu` lists, implementing the PRTE.
3. Write `first_order(prescription, lam)` returning EFL, BFL, FFL, positions of P (from S1) and P′ (from last surface), and the system ABCD matrix (check det = 1).
4. Add a finite-object option: given object distance $l$ (negative) from S1, return the image distance from the last surface and the paraxial magnification.
5. Run it for the Course 01 singlet (`[(102.7, 4, 'N-BK7'), (-102.7, 0, None)]`) at λ = 0.5876, 0.4861, 0.6563 µm.
6. In OpticStudio open `../L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx`, and compare with **System Data** (EFL, BFL) and **Cardinal Points** (Analyze → Reports → Cardinal Points). Change the primary wavelength to F and to C and compare again. Note which reference surfaces the Cardinal Points report uses.
**Deliverable:** `work/paraxial.py`, a comparison table in `work/notes.md`.
**Check yourself:**

| λ (µm) | $n$ | EFL (mm) | BFL (mm) |
|---|---|---|---|
| 0.4861 | 1.52238 | 98.962 | 97.639 |
| 0.5876 | 1.51680 | 100.025 | 98.698 |
| 0.6563 | 1.51432 | 100.505 | 99.175 |

Principal planes at d: P 1.327 mm right of S1, P′ 1.327 mm left of S2. Your Python and OpticStudio should agree to ≥ 4 significant figures (OpticStudio uses the same SCHOTT Sellmeier data; tiny differences can come from air index/temperature settings — System Explorer → Environment).

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
SELL = {"N-BK7": ([1.03961212, 0.231792344, 1.01046945],
                  [0.00600069867, 0.0200179144, 103.560653])}
def index(mat, lam):
    if mat is None: return 1.0
    B, C = SELL[mat]; l2 = lam**2
    return np.sqrt(1 + sum(b*l2/(l2 - c) for b, c in zip(B, C)))

def system_matrix(pres, lam):
    S = np.eye(2); n_prev = 1.0
    for i, (R, t, mat) in enumerate(pres):
        n = index(mat, lam); c = 0.0 if np.isinf(R) else 1/R
        S = np.array([[1, 0], [-(n - n_prev)*c, 1]]) @ S      # refraction
        if i < len(pres) - 1:
            S = np.array([[1, t/n], [0, 1]]) @ S              # transfer
        n_prev = n
    return S                                                   # (y, nu) vertex-to-vertex

S = system_matrix([(102.7, 4, "N-BK7"), (-102.7, 0, None)], 0.5876)
A, B, C, D = S.ravel()
efl, bfl, ffl = -1/C, -A/C, D/C
print(efl, bfl, ffl, bfl - efl)   # 100.025 98.698 -98.698 -1.327
```
The ray-by-ray version (`trace`) gives the same numbers and lets you print y–nu tables. For a finite object at distance $l$ (negative) from S1, start the ray with $y_1 = 1$, $u_0 = -1/l$, and the image distance is $-y_k/u'_k$.

The OpticStudio Cardinal Points report lists focal length, focal planes, principal planes, anti-principal planes, nodal and anti-nodal planes for object and image space. If your P′ position appears as ≈ −100 mm, it is being measured from the image surface, not from surface 2 — check the header.

</details>

## Task 4 — Real vs. paraxial rays with Single Ray Trace (OpticStudio)
**Goal:** Read OpticStudio's paraxial tables and see the real-vs-paraxial gap that *is* aberration.
**Given / specs:** `L01_singlet_f100.zmx` with an M-solve on the back thickness (paraxial focus).
**Steps:**
1. Analyze → Rays & Spots → Single Ray Trace. Settings: $H_x = H_y = 0$, $P_x = 0$, $P_y = 1$, wavelength d. This is the marginal ray.
2. Compare the paraxial table with your y–nu table from the lecture (y at S2 = 9.8673 mm; slope after S2 = −0.099975).
3. Read the real-ray Y at the image surface. What is it? (This is the *transverse spherical aberration* of the marginal ray.)
4. Repeat with $P_y = 0.5$ and $P_y = 0.7071$. How does the real-ray image height scale with $P_y$?
5. Set $H_y = 1$, $P_y = 0$ (chief ray): compare paraxial and real image heights (difference = distortion, Course 02 L05).
**Deliverable:** numbers in notes and a one-paragraph interpretation.
**Check yourself:** the real marginal ray crosses the paraxial image plane below the axis (Y ≈ −0.16 mm), and its error grows roughly as the cube of $P_y$ (≈ 1/8 at $P_y = 0.5$) — third-order spherical aberration. The paraxial chief-ray height is 8.751 mm; the real one is ≈ 8.749 mm (≈ 2 µm less — a tiny barrel distortion).

## Task 5 — Finite conjugates (OpticStudio)
**Goal:** Check the Gaussian and Newtonian equations against OpticStudio.
**Given / specs:** Copy of the singlet; set the **object thickness** (OBJ row) to 300 mm. Change Field Type to **Object Height** with fields 0, 10, 15 mm (wavelength d only is fine). Keep EPD = 20 mm and the M-solve.
**Steps:**
1. Read the new back thickness (M-solve) and the paraxial magnification in System Data.
2. Compare with the worked example (148.40 mm, $m = -0.497$).
3. Compute by hand the image height for a 15 mm object and compare with the Cross-Section / System Data paraxial image height.
4. Move the object to 1000 mm. Compute the image shift relative to the infinity focus with Newton's equation, and check in OpticStudio.
**Deliverable:** `work/L03_T5_finite_conjugate.zmx`, notes.
**Check yourself:** 300 mm → back distance 148.40 mm, $m = -0.4969$, image height for a 15 mm object = −7.45 mm. 1000 mm object → image ≈ 11.10 mm beyond the infinity focus (back distance ≈ 109.80 mm).

<details><summary>Hints / solution sketch</summary>

For the 1000 mm case, measure from the **front focal point**, not from the lens: F lies 98.698 mm left of S1 (FFL), so an object 1000 mm left of S1 is $z = -(1000 - 98.698) = -901.30$ mm from F. Then $z' = -f'^2/z = 10005.03/901.30 = 11.10$ mm, and the back distance becomes 98.698 + 11.10 = 109.80 mm. Using the distance from the lens ($z = -1000$) would give 10.0 mm — the most common Newtonian mistake. OpticStudio's M-solve gives ≈ 109.80 mm (a direct paraxial trace from the object gives 109.798 mm).

</details>

## Task 6 — Paraxial surfaces for system sketches (OpticStudio)
**Goal:** Learn the ideal `Paraxial` surface type for first-order layouts.
**Steps:**
1. New file: EPD 10 mm, field angle 0 and 1°, wavelength 0.5876 µm.
2. Build the telephoto of Task 2 with two `Paraxial` surfaces (focal lengths 50 and −25 mm, 30 mm apart), M-solve to the image.
3. Confirm EFL = 250 mm and BFL = 100 mm in System Data, and locate P′ with the Cardinal Points report.
4. Look at the spot diagram. Why is it perfect?
**Deliverable:** `work/L03_T6_paraxial_telephoto.zmx`.
**Check yourself:** EFL 250, BFL 100; spots are points (paraxial surfaces are ideal, aberration-free by construction).

## Stretch task
Extend `paraxial.py` to read a `.zmx` text file (parse `SURF`, `CURV`, `DISZ`, `GLAS` lines) for lenses made only of Standard surfaces with N-BK7/air, and print its first-order data. This is a toy version of what you will do properly with the ZOS-API in Course 07.

## Reflection questions
1. Why can you trace a "paraxial" ray at a height of 10 mm and still get the exact focal length?
2. Why is $\delta' = \text{BFL} - \text{EFL}$ negative for the singlet but $-150$ mm for the telephoto?
3. If the image is in a medium of index $n'$ (e.g. an immersion lens), how do front and rear focal lengths relate?
4. Why does the contribution of an element to total power scale with the marginal ray height on it?
5. You change the primary wavelength from d to C. Which System Data numbers change and why?

<details><summary>Answers</summary>

1. The PRTE are linear: every height and angle scales with $y_1$, so ratios such as $-y_1/u'_k$ are independent of the starting height.
2. For a single biconvex lens P′ lies inside the glass, slightly left of the last surface. In the telephoto the negative rear group pushes P′ far forward, in front of the whole system.
3. $n'/f' = -n/f = \phi$; with $n = 1$ in object space, $f' = -n' f$.
4. Power bends rays in proportion to height ($\Delta(nu) = -y\phi$); the final slope is the sum of these bends, so each element counts with weight $y_i/y_1$ (Kidger Eq. 2.66).
5. EFL, BFL, image height, pupil positions, F-numbers — all paraxial quantities are computed at the primary wavelength, and the index of N-BK7 is lower at C, so the power drops and EFL increases (≈ 100.5 mm).

</details>
