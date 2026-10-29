# L01 — Tasks: Wavefront and Transverse Aberrations

> Work in `work/` inside this lesson folder (e.g. save `work/L01_T2_kidger_triplet.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

You will build a small Python Seidel calculator (`work/seidel.py`) in Task 1. **Keep it** — every lesson of Course 02 reuses it.

## Task 1 — A Seidel calculator in Python (Python)
**Goal:** Implement the paraxial marginal + chief ray trace and the seven Seidel surface sums, and validate against a published table.

**Given / specs:** Kidger's Kingslake triplet [Kidger §6.2.7, p. 113]: object at infinity, EPD 22.2222 mm (F/4.5), semi-field 20°, λ = 587.6 nm.

| Surf | R (mm) | thickness after (mm) | n after | $V_d$ |
|---|---|---|---|---|
| 1 | 42.98790 | 4.00000 | 1.620408 | 60.30 |
| 2 | −248.07740 | 10.51018 | 1 | |
| 3 | −38.21035 | 2.50000 | 1.616589 | 36.61 |
| 4 | 43.95894 | 0.95798 | 1 | |
| STOP | ∞ | 8.91148 | 1 | |
| 5 | 656.66349 | 4.50000 | 1.620408 | 60.30 |
| 6 | −33.50754 | 86.48643 | 1 | |

(Kidger's printed chief-ray data correspond to the stop lying 0.958 mm behind surface 4; with that placement the book's table is reproduced. Treat the stop as a plane surface with no power — it contributes zero to all sums.)

**Steps:**
1. Write `trace(surfs, y0, u0)` using $n'u' = nu - yc(n'-n)$ and $y_{k+1} = y_k + u'_k t_k$ (slope convention, $u$ = tan of the angle, positive climbing).
2. Marginal ray: $y_1 = 11.1111$, $u_1 = 0$. Chief ray: $\bar u_1 = \tan 20°$; find $\bar y_1$ such that $\bar y = 0$ at the stop (trace twice with two trial heights and interpolate — the trace is linear).
3. Compute $A, \bar A, \Delta(u/n), H$ and $S_I \ldots S_V$, $C_L$, $C_T$ per surface (formulas in the lecture notes §5.1; use $\delta n = (n_d - 1)/V_d$).
4. Print a table like Kidger's and the sums.
5. Add a function that converts sums to $W_{040}\ldots W_{311}$ in waves and to transverse aberrations.

**Deliverable:** `work/seidel.py` and its printed table in `work/notes.md`.

**Check yourself:** sums $S_I = 0.01143$, $S_{II} = 0.01033$, $S_{III} = -0.02837$, $S_{IV} = 0.06216$, $S_V = -0.05921$, $C_L = 0.000963$, $C_T = 0.000871$ mm; $H = -4.044$ mm; $W_{040} = 2.43$ waves; surface 3 has $S_I = -0.2568$ (the negative flint is the only strong source of *over*correction).

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
def seidel(surfs, y, u, yb, ub, dn=None):
    """surfs: list of (c, t_after, n_before, n_after); dn: list of (dn_before, dn_after)."""
    H = surfs[0][2]*(u*yb - ub*y)
    out = []
    for k, (c, t, n, n2) in enumerate(surfs):
        A, Ab = n*(u + y*c), n*(ub + yb*c)
        u2  = (n*u  - y *c*(n2-n))/n2
        ub2 = (n*ub - yb*c*(n2-n))/n2
        d = u2/n2 - u/n
        S1, S2, S3 = -A*A*y*d, -A*Ab*y*d, -Ab*Ab*y*d
        S4 = -H*H*c*(1/n2 - 1/n)
        S5 = (Ab/A)*(S3+S4) if A != 0 else 0.0   # (for A=0 use the alternative formula, Kidger §6.2.3)
        if dn:
            dd = dn[k][1]/n2 - dn[k][0]/n
            CL, CT = A*y*dd, Ab*y*dd
        else:
            CL = CT = 0.0
        out.append((S1, S2, S3, S4, S5, CL, CT))
        y, yb, u, ub = y + u2*t, yb + ub2*t, u2, ub2
    return np.array(out), H
```
The stop surface has $c=0$ and equal indices, so all its terms are 0 — but **$A$ may be nonzero there, fine**. The image-space slope after surface 6 should be $u' = -0.11111$ and the marginal height at the image ≈ 0 (the last thickness is the paraxial back focus).
</details>

## Task 2 — The same triplet in OpticStudio (OpticStudio)
**Goal:** Compare hand-computed Seidels with OpticStudio's report and with real-ray fans; see where third-order theory stops being accurate.

**Given / specs:** Table of Task 1. Glasses: use **Model** glass (Glass Solve → Model) with $n_d$, $V_d$ as given (Kidger used S-SK16 / S-F4-type glasses; the model glass avoids catalog-name issues). System Explorer: Aperture = Entrance Pupil Diameter 22.2222; Fields = Angle, 0°, 14°, 20°; Wavelengths F, d, C with d primary. Stop on the dummy surface.

**Steps:**
1. Enter the lens, check EFL (Prescription Data or the status bar) ≈ 99.996 mm. Save as `work/L01_T2_kidger_triplet.zmx`.
2. Open **Seidel Coefficients**. Compare SPHA…CTR surface by surface with your Python table. Record the W040…W311 lines and the W220S/M/T lines.
3. Open the **Ray Fan** (primary wavelength only). Read the on-axis tangential $\varepsilon_y$ at $P_y = 1$ and compare with $S_I/(2n'u') = -51$ µm.
4. At 20°: read the tangential ray fan at $P_y = \pm1$. The average of $\varepsilon_y(+1)$ and $\varepsilon_y(-1)$ isolates the even-in-$\rho_y$ part (coma); compare with $3S_{II}/(2n'u') = -139$ µm (beware: the ray fan is relative to the *real* chief ray, and higher-order terms are large at 20°).
5. Open the **OPD Fan** on axis. Note the sign OpticStudio shows at the pupil edge for this undercorrected lens and write it in your notes (you will need this convention all year).
6. Open **Field Curvature/Distortion**. Compare the max distortion with the +0.73% Seidel prediction.

**Deliverable:** `work/L01_T2_kidger_triplet.zmx`; in `notes.md` a 3-column table "Python Seidel | OpticStudio Seidel | real-ray value" for spherical, tangential coma, distortion.

**Check yourself:** Seidel sums agree to ~4 significant figures (small differences come from model-glass dispersion for $C_L$/$C_T$; expect OpticStudio's CLA/CTR to have the **opposite sign** to the Kidger-convention values — see L06 §1.1). On axis, the real spherical error is of the order of the Seidel estimate but not equal (fifth-order spherical is present). At 20°, real-ray coma/distortion differ more noticeably — this is the point: Seidels are a *diagnostic*, not a final answer.

<details><summary>Hints</summary>

- If the EFL is off, check that you set Model glass index at d, and that the stop surface is a plane with air on both sides.
- The Seidel report always uses the maximum field. To get Seidels "at 14°", scale: coma ×0.685 (= tan14°/tan20°), astigmatism ×0.469, distortion ×0.321 (third order only).
- If OpticStudio's DIST sign or percentage differs from your Python, check which reference (paraxial chief ray) and which sign convention (positive = pincushion in OpticStudio's Field Curvature/Distortion plot).
</details>

## Task 3 — Seidel ↔ Zernike bookkeeping (Python + OpticStudio)
**Goal:** Convert Seidel wavefront coefficients into Fringe and Standard Zernike coefficients, and verify against OpticStudio.

**Steps:**
1. In Python, sample $W(\rho,\theta) = W_{040}\rho^4 + W_{131}\rho^3\sin\theta + W_{222}\rho^2\sin^2\theta$ (θ from the $x$-axis, field on $+y$) on a unit disk; least-squares fit the first 9 Fringe polynomials and the first 11 Standard polynomials (definitions in lecture notes §6). Use $W_{040}=1$, $W_{131}=0$, $W_{222}=0$ first, then each term alone.
2. Confirm: Fringe Z9 = $W_{040}/6$, Z4 = $W_{040}/2$; Standard Z11 = $W_{040}/(6\sqrt5) = 0.0745\,W_{040}$; coma alone → Fringe **Z8** = $W_{131}/3$; astigmatism alone → Fringe **Z5** = $-W_{222}/2$.
3. In OpticStudio on the Task 2 triplet, open **Zernike Fringe Coefficients** on axis at 587.6 nm (reference to chief ray). Using $W_{040} = 2.43$ waves from the Seidel report, predict Z9 ($\approx 0.41$ wave) and compare. Then open **Zernike Standard Coefficients** and find the spherical term (Z11). Confirm Standard Z11 ≈ Fringe Z9/√5.

**Deliverable:** `work/zernike_fit.py`; table of predicted vs. reported coefficients in `notes.md`.

**Check yourself:** Agreement in *order of magnitude and sign* for Z9 — exact agreement is not expected because the real wavefront contains $\rho^6$ (fifth-order) spherical, which projects onto Z9 too (and onto Fringe Z16). The ratio Standard/Fringe for the spherical term is exactly $1/\sqrt5 = 0.447$ only if you compare like-for-like terms.

<details><summary>Hints</summary>

Fringe: $Z_1=1, Z_2=\rho\cos\theta, Z_3=\rho\sin\theta, Z_4=2\rho^2-1, Z_5=\rho^2\cos2\theta, Z_6=\rho^2\sin2\theta, Z_7=(3\rho^3-2\rho)\cos\theta, Z_8=(3\rho^3-2\rho)\sin\theta, Z_9=6\rho^4-6\rho^2+1$.
Standard (Noll): multiply by $\sqrt{2(n+1)}$ for $m\ne0$ and $\sqrt{n+1}$ for $m=0$; order Z4 defocus, Z5 sin2θ, Z6 cos2θ, Z7 sinθ coma, Z8 cosθ coma, Z9/Z10 trefoil, Z11 spherical.
Use `np.linalg.lstsq` on ~10⁵ random points uniformly in the disk ($\rho=\sqrt{U}$).
</details>

## Task 4 — Read the aberration from the fan (analysis, pen & paper)
**Goal:** Practise identifying aberrations and their scaling.

**Given:** A lens at F/4, 0.55 µm, field ±15°, has $W_{040} = 0.5\,\lambda$, $W_{131} = 0.8\,\lambda$ (at full field), $W_{222} = 0.3\,\lambda$ (at full field), no other aberrations, image in air.

**Questions:**
1. Marginal transverse spherical error (µm)?
2. Tangential coma length $3S_{II}/(2n'u')$ in µm at full field and at 7.5°?
3. If the client wants F/2.8 instead, by what factor does each wavefront coefficient grow (third-order only)?
4. Sketch the tangential and sagittal ray fans at full field.
5. Which of the three is cheapest to "remove" by refocusing? Which by changing the reference to the centroid?

<details><summary>Solution</summary>

$u' = -1/(2N) = -0.125$, so $1/(n'u') = -8$.
1. $\varepsilon = \frac{1}{n'u'}\cdot 4W_{040} = -8\cdot 4\cdot 0.5\cdot0.55 = -8.8$ µm.
2. $S_{II} = 2W_{131}$, so $3S_{II}/(2n'u') = 3W_{131}/(n'u') = -8\cdot3\cdot0.8\cdot0.55 = -10.56$ µm at full field; coma ∝ H → −5.28 µm at 7.5° (third order, using $H \approx \tan$ ratio ≈ 0.49 gives −5.2 µm).
3. Aperture ratio $4/2.8 = 1.4286$: $W_{040}\times1.4286^4 = 4.16$, $W_{131}\times1.4286^3 = 2.92$, $W_{222}\times1.4286^2 = 2.04$.
4. T fan: cubic (SA) + parabola (coma) + straight line slope (astig $\tfrac{3}{2}$-factor); S fan: cubic + smaller straight line; the S fan's $\varepsilon_x$ has no coma.
5. Defocus removes part of spherical (best RMS when $W_{020} = -W_{040}$) and the *mean* astigmatic defocus; centroid reference removes the tilt part of coma. None removes them completely (lecture §6.1 residuals).
</details>

## Stretch task
Using your Task 2 file, run the **OPD Fan** at 0°, 10°, 14°, 20°, and fit in Python $W(H,\rho_y) = a\rho_y^4 + bH\rho_y^3 + cH^2\rho_y^2$ (+ $\rho_y^6$ and $H\rho_y^5$ terms) to the tangential OPD fans (export the text with the "Text" tab of each analysis). Compare $a, b, c$ with $W_{040}, W_{131}, W_{222}+W_{220}$ from the Seidel report and comment on the size of the fifth-order terms. (Hint: OPD fans are relative to the real chief ray, so $W_{311}$ distortion does not appear.)

## Reflection questions
1. Why can Seidel coefficients be added surface by surface, while fifth-order coefficients cannot?
2. A colleague says "S1 = 0.002 mm, that's only 3.4 waves at 587 nm, fine". What's wrong?
3. Why is distortion invisible in an OPD fan or spot diagram but visible in Grid Distortion?
4. For a structured-light projector imaging a pattern onto a scene, which W term matters for *depth accuracy* even though it does not blur the pattern?

<details><summary>Answers</summary>

1. Third-order contributions depend only on paraxial ray data, which are unaffected by aberrations of earlier surfaces; higher orders contain "induced" cross-terms where one surface's aberration changes the ray heights/angles at later surfaces [Kidger §6.2, p. 102].
2. $W_{040} = S_I/8$: 0.002 mm/8 = 0.00025 mm = 0.25 µm = 0.43 waves at 587.6 nm; the colleague overestimated the wavefront error by 8×.
3. Distortion is $W_{311}$, a pure tilt of the wavefront ∝ $H^3$: the whole bundle is displaced, so relative to the real chief ray there is no OPD and no blur. Grid distortion compares chief-ray positions to the paraxial (ideal) grid.
4. Distortion (and lateral colour for multi-wavelength systems): a displaced pattern feature biases triangulation; it must be calibrated or kept small and stable.
</details>
