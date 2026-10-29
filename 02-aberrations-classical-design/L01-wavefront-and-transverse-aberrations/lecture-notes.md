# L01 — Wavefront and Transverse Aberrations

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~4 h
> **Prerequisites:** Course 01 (especially [L03 paraxial optics](../../01-foundations/L03-paraxial-optics-and-ray-tracing/), [L04 stops & pupils](../../01-foundations/L04-stops-pupils-fields/), [L06 real rays & analysis tools](../../01-foundations/L06-real-rays-and-analysis-tools/)) · **Next:** [L02 — Spherical aberration and bending](../L02-spherical-aberration-and-bending/)

## Learning objectives
After this lesson you should be able to:
- Explain what a wavefront aberration $W$ is (OPD against a reference sphere centred on the ideal image point) and how it relates to the transverse ray error you see in a ray fan.
- Write down the aberration polynomial in Hopkins $W_{klm}$ notation and name every term up to fourth order ($W_{020}, W_{111}, W_{040}, W_{131}, W_{222}, W_{220}, W_{311}$), including its pupil and field dependence.
- Convert between Seidel sums $S_I\ldots S_V$ (plus $C_L$, $C_T$) and wavefront coefficients, transverse ray errors and longitudinal errors — by hand and in Python.
- Compute Seidel sums from a paraxial marginal + chief ray trace (Python), and compare with OpticStudio's **Seidel Coefficients** report.
- Decompose a Seidel wavefront into Fringe and Standard Zernike coefficients, and avoid the three classic pitfalls (ordering, normalization, $x$ vs $y$ angle reference).
- Recognise the "signature" of each primary aberration in a ray fan, OPD fan and spot diagram.

## Reading
- **Core:** [Kidger §4.1, pp. 63–65] — the derivative relation between wavefront and transverse aberration, relative pupil coordinates.
- **Core:** [Kidger §4.4–4.4.2, pp. 70–81] — the symmetry argument that produces the aberration polynomial, and a tour of each Seidel term with ray-fan and through-focus pictures. Read carefully; this lesson is built on it.
- **Core:** [Kidger §6.1–6.2.7, pp. 101–115] — skim the derivation; study the summary of Seidel surface coefficients (pp. 112–113) and the numerical triplet example (pp. 113–115). Task 1 reproduces that table.
- **Core:** [Kidger §6.9.1–6.9.2, pp. 130–132] — the Seidel ↔ wavefront ↔ transverse conversion formulas.
- **Core:** [Geary §7.4–7.6, pp. 77–83] — a gentle, picture-based introduction to wavefronts, the reference sphere, the Seidel polynomial and the sine condition.
- **Optional:** [Geary §37.8, pp. 430–432] — Zernike polynomials from the optical-testing angle. [Kidger §4.4.3, pp. 87–92] — balancing with higher orders (preview of L02/L03).
- **Optional online:** J. Sasián, *OPTI 517 lecture 4: Aberration coefficients* (Univ. of Arizona) — compact slides on $W_{klm}$ and Seidel sums: <https://wp.optics.arizona.edu/jsasian/wp-content/uploads/sites/33/2016/02/L4-OPTI-517-Aberration-Coefficients.pdf>

---

## 1. Why we need a language for aberrations

In Course 01 you learned to trace exact rays and look at ray fans and spot diagrams. Those plots tell you **what** the image looks like, but not **why**, and not **what to change**. Kidger makes the point bluntly: ray tracing gives "virtually no diagnostic information" about the cause of the aberrations [Kidger §6.1, p. 101]. The aberration polynomial and the Seidel sums are the diagnostic language: they split the total error into a handful of named terms with known dependence on aperture and field, and — crucially — they can be computed *surface by surface* from just two paraxial rays. A professional lens designer reads a Seidel bar chart the way you read a profiler: which surface is hot, what kind of aberration it produces, and which other surface can cancel it.

There are three ways to describe the same error, and you must be fluent in all three:

| Description | Measured where | Unit (typical) | OpticStudio plots |
|---|---|---|---|
| **Wavefront aberration** $W$ (OPD) | exit pupil, along the ray, relative to a reference sphere | waves (λ) | OPD Fan, Wavefront Map, Zernike coefficients |
| **Transverse ray aberration** $\varepsilon_x, \varepsilon_y$ | image plane, relative to the chief ray (or centroid) | µm | Ray Fan, Spot Diagram |
| **Longitudinal aberration** $\delta z$ | along the axis | mm | Longitudinal Aberration, Field Curvature, Chromatic Focal Shift |

## 2. The wavefront aberration

A perfect imaging system turns the diverging spherical wave from an object point into a converging spherical wave centred on the ideal image point: every ray from object to image then has the same optical path length (OPL) [Geary §7.4.2, p. 78]. In a real system the emerging wavefront is not quite spherical.

To quantify this we put a **reference sphere** in the exit pupil: vertex on the axis of the exit pupil (in practice where the chief ray crosses the exit pupil), centre at the ideal image point (usually where the *chief ray* hits the image surface). The **wavefront aberration** $W(x,y)$ is the optical path difference between the real wavefront and the reference sphere, measured along the ray [Geary §7.4.3, p. 79; Kidger §4.1, p. 63]. Because it is an optical path, it already contains the refractive index; because it is a phase, we quote it in **waves** of the working wavelength.

```
          exit pupil                         image plane
              |   reference sphere (centre at ideal image point P')
              |  .-'
   aberrated  | /    ray (normal to the real wavefront)
   wavefront -+/------------------------------.  lands at P' + ε
              |\                               \
              | '-.                             * P'  (chief ray)
              |    '-.
          W(x,y) = OPD between the two surfaces, along the ray
```

Key facts:
- $W = 0$ at the pupil centre **by definition** (the chief ray is the reference). That is why Kidger's constant terms ${}_2w_{00}\eta^2$, ${}_4w_{00}\eta^4$ are dropped [Kidger §4.4.1, p. 73].
- Rays are normals to the wavefront (theorem of Malus–Dupin). So a *tilted* patch of wavefront means a ray that misses the ideal image point — this is the bridge to transverse aberration.
- The reference sphere's centre is a *choice*. Move it along the axis and you add defocus ($\rho^2$); move it sideways and you add tilt ($\rho\cos\theta$). That is exactly what OpticStudio does when you change "Reference" in an OPD/wavefront analysis (Chief Ray vs. Centroid) or refocus.

## 3. Transverse ray error = slope of the wavefront

If the ray makes a small angle $\delta U'$ with the normal to the reference sphere of radius $R$, it misses the reference centre by $\varepsilon_y \approx R\,\delta U'$. The angle between ray and reference normal equals the angle between wavefront and reference sphere, which is the slope of $W$ divided by $n'$ (because $W$ is an optical path). Hence [Kidger Eq. 4.3; Geary Eq. 7.7]

$$
\varepsilon_y = -\frac{R}{n'}\frac{\partial W}{\partial y}, \qquad \varepsilon_x = -\frac{R}{n'}\frac{\partial W}{\partial x}.
$$

($R$ = reference-sphere radius, $n'$ = image-space index, $x, y$ = coordinates on the reference sphere.) The overall sign depends on how a book signs $R$ and $W$; in this course we use the form that is consistent with the Seidel formulas in Kidger §6.9.2 and with OpticStudio's Seidel output. With **normalized pupil coordinates** $\rho_x = x/y_m$, $\rho_y = y/y_m$ (OpticStudio's $P_x, P_y$) and the **signed** paraxial marginal-ray slope in image space $u'$ ($u'<0$ for a ray converging to the axis from above),

$$
\boxed{\;\varepsilon_y = \frac{1}{n'u'}\,\frac{\partial W}{\partial \rho_y}, \qquad \varepsilon_x = \frac{1}{n'u'}\,\frac{\partial W}{\partial \rho_x}\;}
$$

For an object at infinity in air, $u' \approx -1/(2N)$ with $N$ the working F-number, so

$$
\varepsilon_y \approx -2N\,\frac{\partial W}{\partial \rho_y}.
$$

Two practical consequences:
1. **The ray fan is the derivative of the OPD fan.** A quartic OPD (spherical aberration) gives a cubic ray fan; a quadratic OPD (defocus) gives a straight-line ray fan. Conversely the OPD is the *area under* the ray fan [Kidger Eq. 4.9].
2. **The same wavefront error produces a bigger blur at higher F/#.** One wave of $W_{040}$ at λ = 0.55 µm gives a marginal-ray error of $|\varepsilon| = 2N\cdot 4W_{040} = 2\cdot5\cdot4\cdot0.55 = 22$ µm at F/5. The Airy radius at F/5 is $1.22\lambda N = 3.4$ µm. In waves, the system is "1 wave" bad; in microns, the geometric blur is 6× the Airy radius. That is why for slow, near-diffraction-limited systems you should judge by OPD/RMS wavefront, and for fast, aberration-dominated systems by spot size (L03 of Course 03 formalises this).

Geary notes the naming confusion this derivative creates: the Seidel terms are **fourth order** in the wavefront but **third order** in transverse ray error [Geary §7.5, p. 82]. "Third-order aberration", "primary aberration" and "Seidel aberration" all mean the same five terms.

## 4. The aberration polynomial ($W_{klm}$ notation)

### 4.1 Where the terms come from (symmetry)
For a rotationally symmetric (centred) system we can, without loss of generality, put the object point on the $y$-axis at normalized height $H$ (OpticStudio's $H_y$; Kidger calls it $\eta$, Geary $h$). A ray is then labelled by $H$ and its normalized pupil position $(\rho, \theta)$. Rotational symmetry plus mirror symmetry about the meridional plane forces $W$ to depend only on the three invariants [Kidger §4.4, pp. 71–72]

$$
H^2, \qquad \rho^2, \qquad H\rho\cos\theta,
$$

where **$\theta$ is measured from the $y$-axis** (the meridional direction), so $\rho\cos\theta = \rho_y$. Expanding $W$ as a power series in these invariants gives the **aberration polynomial** (Hopkins notation):

$$
W(H,\rho,\theta) = \sum_{j,m,n} W_{klm}\,H^k\rho^l\cos^m\theta, \qquad k = 2j+m,\; l = 2n+m .
$$

The subscripts are simply the powers of $H$, $\rho$ and $\cos\theta$ [Geary Eq. 7.3; Kidger Eq. 4.15 writes the same coefficient as ${}_kw_{lm}$]. The **order** of a term is $k+l$ in the wavefront.

### 4.2 The terms you must know

| Coefficient | Term | Name | Wavefront order | Ray-fan signature |
|---|---|---|---|---|
| $W_{020}$ | $\rho^2$ | defocus | 2 | straight line through origin, same slope tangential & sagittal |
| $W_{111}$ | $H\rho\cos\theta$ | tilt (magnification / lateral shift) | 2 | constant offset ∝ $H$ |
| $W_{040}$ | $\rho^4$ | spherical aberration | 4 | cubic, same T and S, independent of field |
| $W_{131}$ | $H\rho^3\cos\theta$ | coma | 4 | T fan: parabola ($\propto\rho_y^2$), ∝ $H$; S fan: $\varepsilon_x = 0$ but $\varepsilon_y\ne0$ |
| $W_{222}$ | $H^2\rho^2\cos^2\theta$ | astigmatism | 4 | straight lines with **different** T and S slopes, ∝ $H^2$ |
| $W_{220}$ | $H^2\rho^2$ | field curvature (sagittal; $=W_{220P}+\tfrac12W_{222}$) | 4 | straight line, same T and S slope, ∝ $H^2$ |
| $W_{311}$ | $H^3\rho\cos\theta$ | distortion | 4 | constant offset ∝ $H^3$ (spot is sharp, but misplaced) |
| $W_{060}, W_{151}, W_{242}, W_{333},\ldots$ | | fifth-order (sixth in $W$) | 6 | higher-order wiggles; see L02–L03 |

Read across a row and you can predict how the term scales: doubling the aperture multiplies spherical aberration ($\rho^4$) by 16, coma by 8, astigmatism by 4; doubling the field multiplies coma by 2, astigmatism/field curvature by 4, distortion by 8. This is the single most useful scaling table in lens design — e.g. when a client asks to go from F/4 to F/2.8, the spherical aberration wavefront goes up by $(4/2.8)^4 \approx 4.2\times$.

Defocus and tilt are "first-order" (they only move or rescale the perfect image). In OpticStudio's Seidel report the labels **W020** and **W111** are reused for the *chromatic* versions — the wavefront change of focus and of image size between the extreme wavelengths (axial and lateral colour). Keep that in mind when you read the report.

### 4.3 Field curvature and astigmatism: S, T, P
$W_{222}$ only defocuses the tangential section; $W_{220}$ defocuses both. Combining them, the effective defocus (in $\rho^2$) at field $H$ is

- sagittal: $W_{220S} = W_{220} + \tfrac12 W_{222}$ (using $W_{220} = W_{220P}$ below),
- tangential: $W_{220T} = W_{220P} + \tfrac32 W_{222}$,
- medial (between S and T): $W_{220M} = W_{220P} + W_{222}$,

where $W_{220P}$ is the pure **Petzval** curvature term. These are exactly the "W220S/W220M/W220T" lines OpticStudio prints. Note that the coefficient of $H^2\rho^2$ in the raw polynomial (Kidger's ${}_2w_{20}$) is the *sagittal* one, $(S_{III}+S_{IV})/4$, because the astigmatism term vanishes along the sagittal direction ($\cos\theta = 0$); along the tangential direction ($\cos\theta=1$) the astigmatism term adds a further $W_{222}$. The ratio 3:1 of the distance Petzval→T to Petzval→S [Kidger Eq. 6.100] follows from the $\tfrac32$ vs $\tfrac12$ factors. L04 develops this fully.

## 5. Seidel sums and how they map to $W_{klm}$

### 5.1 Computing them
Seidel's insight: to third order, each surface's contribution can be computed from **two paraxial rays** — the marginal ray (height $y$, slope $u$) and the chief ray ($\bar y$, $\bar u$). At each surface with curvature $c$, indices $n\to n'$:

$$
A = n(u + yc), \qquad \bar A = n(\bar u + \bar y c)\quad\text{(refraction invariants, } A = ni\text{)}
$$

$$
\Delta\!\left(\frac{u}{n}\right) = \frac{u'}{n'} - \frac{u}{n},\qquad \Delta\!\left(\frac{1}{n}\right) = \frac{1}{n'}-\frac{1}{n},\qquad H = n(u\bar y - \bar u y)\ \text{(Lagrange invariant)}
$$

$$
\begin{aligned}
S_I &= -A^2\, y\, \Delta(u/n) && \text{spherical}\\
S_{II} &= -A\bar A\, y\, \Delta(u/n) && \text{coma}\\
S_{III} &= -\bar A^2\, y\, \Delta(u/n) && \text{astigmatism}\\
S_{IV} &= -H^2 c\, \Delta(1/n) && \text{Petzval}\\
S_V &= \frac{\bar A}{A}\,(S_{III}+S_{IV}) && \text{distortion}\\
C_L &= A\,y\,\Delta(\delta n/n), \quad C_T = \bar A\,y\,\Delta(\delta n/n) && \text{axial / lateral colour}
\end{aligned}
$$

with $\delta n = n_F - n_C$ [Kidger §6.2.6, Eqs. 6.27–6.31, 6.49–6.50]. Here $u$ is the slope (tangent) of the paraxial ray with the usual sign: positive when the ray climbs going left→right; this is the OpticStudio and Kidger convention (Kidger Fig. 2.1, p. 18). The **system Seidel sum** is the plain sum over surfaces — that additivity is what makes Seidel analysis so powerful. (Fifth- and higher-order terms are *not* simply additive [Kidger §6.2, p. 102].)

The units of $S$ are the lens units (mm). A positive $S_I$ means **undercorrected** spherical aberration — the normal state of a positive singlet: marginal rays focus too close to the lens.

### 5.2 Mapping to wavefront, transverse and longitudinal errors
At full aperture ($\rho=1$) and full field ($H=1$) [Kidger §6.9.1–6.9.2, pp. 130–132]:

| Seidel | Wavefront coefficient | Max transverse error (marginal ray) |
|---|---|---|
| $S_I$ | $W_{040} = S_I/8$ | $\varepsilon_y = S_I/(2n'u')$ |
| $S_{II}$ | $W_{131} = S_{II}/2$ | tangential coma $= 3S_{II}/(2n'u')$; sagittal coma $= S_{II}/(2n'u')$ |
| $S_{III}$ | $W_{222} = S_{III}/2$ | — |
| $S_{IV}$ | $W_{220P} = S_{IV}/4$ | — |
| $S_{III}, S_{IV}$ | $W_{220} = (S_{III}+S_{IV})/4$ (sagittal) | $\varepsilon_y = (3S_{III}+S_{IV})/(2n'u')$ (T); $\varepsilon_x = (S_{III}+S_{IV})/(2n'u')$ (S) |
| $S_V$ | $W_{311} = S_V/2$ | $\varepsilon_y = S_V/(2n'u')$ (chief-ray displacement); fractional distortion $= S_V/(2H)$ |
| $C_L$ | $W_{020}^{\text{chrom}} = C_L/2$ | $C_L/(n'u')$ |
| $C_T$ | $W_{111}^{\text{chrom}} = C_T$ | $C_T/(n'u')$ |

Longitudinal versions follow from $\delta z = -\varepsilon_y/u'$ (paraxial). E.g. longitudinal spherical $= -S_I/(2n'u'^2)$.

Notice the factor $\tfrac18$ in $W_{040} = S_I/8$: a Seidel sum is **not** a wavefront error. Many people compare an $S_I$ value directly with "a quarter wave" and are off by 8×. (This is also why the OpticStudio Seidel *Diagram*, which plots $S$ in lens units, can look scarier than the wavefront it represents.)

## 6. Zernike polynomials — and how OpticStudio reports them

Seidel/$W_{klm}$ coefficients are the designer's language: they are defined at the *paraxial* reference and organised by field dependence. **Zernike polynomials** are the tester's language: an orthogonal basis over the unit circle for *one* field point's wavefront, fitted to real ray-traced (or interferometer) OPD [Geary §7.4.3, p. 80, §37.8]. Orthogonality means each coefficient is independent of how many terms you fit and the coefficients add in quadrature to the RMS.

OpticStudio offers both **Zernike Fringe Coefficients** and **Zernike Standard Coefficients** (and Zernike Annular) under *Analyze → Wavefront → Zernike …* (exact sub-menu varies by version — search "Zernike" in the ribbon/Help). They differ in **ordering** and **normalization**:

| | Fringe (Univ. Arizona / "Fringe" ordering, 37 terms) | Standard (Noll ordering, unlimited terms) |
|---|---|---|
| Normalization | peak-normalised: each polynomial has value ±1 at the edge | RMS-normalised: each polynomial has RMS = 1 over the unit disk |
| Coefficient meaning | ≈ peak contribution | **RMS contribution** directly |
| Piston | Z1 = 1 | Z1 = 1 |
| Tilt | Z2 = ρcosθ (x), Z3 = ρsinθ (y) | Z2 = 2ρcosθ, Z3 = 2ρsinθ |
| Defocus | Z4 = 2ρ²−1 | Z4 = √3(2ρ²−1) |
| Primary astigmatism | Z5 = ρ²cos2θ, Z6 = ρ²sin2θ | Z5 = √6ρ²sin2θ, Z6 = √6ρ²cos2θ |
| Primary coma | Z7 = (3ρ³−2ρ)cosθ, Z8 = (3ρ³−2ρ)sinθ | Z7 = √8(3ρ³−2ρ)sinθ, Z8 = √8(3ρ³−2ρ)cosθ |
| Primary spherical | **Z9** = 6ρ⁴−6ρ²+1 | **Z11** = √5(6ρ⁴−6ρ²+1) |

**Pitfalls (each has cost real projects real money):**
1. **Ordering.** "Z9" is spherical aberration in Fringe but trefoil-family in Standard. Always state which set. Interferometer software (e.g. MetroPro-style) usually exports Fringe; OpticStudio's Zernike *surfaces* exist in both flavours (Zernike Fringe Sag / Zernike Standard Sag) — check the community thread on importing Fringe sag data in the reading list.
2. **Normalization.** A Fringe Z9 of 0.1 wave and a Standard Z11 of 0.1 wave are *not* the same amount of spherical: Standard Z11 = Fringe Z9 / √5. To get RMS from Fringe coefficients you must multiply each by its normalisation factor.
3. **Angle reference.** In Zernike conventions $\theta$ is measured **from the $x$-axis**, whereas the $W_{klm}$ polynomial measures it **from the $y$-axis**. OpticStudio puts field points on $+y$ by default, so meridional coma shows up in the **sinθ** term (Fringe Z8, Standard Z7), not Z7/Z8 as you might guess, and $W_{222}$ appears as a *negative* $\cos 2\theta$ astigmatism term (Fringe Z5, Standard Z6).
4. **Reference and units.** Zernike coefficients in OpticStudio are in waves at the chosen wavelength and depend on the reference (chief ray vs centroid) and on whether the fit includes higher-order content. They describe *one* field point and *one* wavelength.

### 6.1 Converting Seidel terms to Zernike
Because $\rho^4$, $\rho^3\cos\theta$, $\rho^2\cos^2\theta$ are not orthogonal to lower terms, each Seidel term spills into lower Zernikes:

$$
W_{040}\rho^4 = W_{040}\left[\tfrac16 Z_9^{F} + \tfrac12 Z_4^{F} + \tfrac13\right]
$$

$$
W_{131}\rho^3\sin\theta_x = W_{131}\left[\tfrac13 Z_8^{F} + \tfrac23 Z_3^{F}\right],\qquad
W_{222}\rho_y^2 = W_{222}\left[-\tfrac12 Z_5^{F} + \tfrac14 Z_4^{F} + \tfrac14\right]
$$

(superscript F = Fringe; $\theta_x$ measured from $x$, so $\rho\sin\theta_x = \rho_y$). The leftover RMS after removing piston, tilt and defocus — i.e. what a refocus/recentre *cannot* fix — is

$$
\sigma_{SA} = \frac{W_{040}}{6\sqrt5} = 0.0745\,W_{040},\qquad
\sigma_{coma} = \frac{W_{131}}{\sqrt{72}} = 0.118\,W_{131},\qquad
\sigma_{astig} = \frac{W_{222}}{\sqrt{24}} = 0.204\,W_{222}.
$$

(Without the defocus removal, pure $\rho^4$ has RMS $\sqrt{4/45}\,W_{040} = 0.298\,W_{040}$ — balancing with defocus improves RMS spherical by 4×. That is the topic of L02.) These numbers were checked by Monte-Carlo integration over the unit disk.

## 7. In OpticStudio

**Seidel Coefficients** (*Analyze → Image Quality → Aberrations → Seidel Coefficients*, location varies slightly by version). A text report that lists, surface by surface and summed:
- Seidel sums **SPHA (S1), COMA (S2), ASTI (S3), FCUR (S4), DIST (S5), CLA (CL), CTR (CT)** in lens units;
- wavefront coefficients in waves: **W040, W131, W222, W220P, W311, W020, W111**, and the derived **W220S, W220M, W220T**;
- transverse and longitudinal aberration coefficients (lens units), e.g. transverse spherical, sagittal/tangential coma, sagittal/tangential field curvature, distortion, axial and lateral colour (column names such as TSPH, TSCO, TTCO, LSPH… — check the exact set in your version).

Conditions and pitfalls:
- **Sign of the colour terms:** our formulas follow Kidger/Welford, where a positive lens has $C_L>0$; OpticStudio's CLA/CTR columns use the opposite sign (Geary's ZEMAX listing of a positive singlet shows a negative CLA, [Geary Fig. 16.5]). Compare magnitudes; see L06 §1.1.
- Computed at the **primary wavelength** and for the **maximum field** (normalised $H=1$) and full pupil. Colour terms use the shortest and longest wavelengths in the Wavelength list.
- Valid only for rotationally symmetric systems with paraxial-meaningful surfaces. Tilts/decenters, non-sequential components, freeforms: ignore the Seidels.
- They are **paraxial** third-order numbers. Fast or wide-angle lenses have large higher-order content; the real ray fan can differ substantially (Task 2 shows this).
- Merit operands **SPHA, COMA, ASTI, FCUR, DIST** return the Seidel contribution of a surface (Surf = 0 for the sum), and are reported in **waves** per the Ansys community discussion in the reading list; **always cross-check the operand's value against the Seidel report** before relying on the unit. They are useful for guiding early optimization (L02, L06), but don't optimise to zero Seidels on a fast lens — you'll trade them for higher orders.
- The **Seidel Diagram** shows the same S values as a bar chart per surface. Get used to reading it: tall bars of opposite sign on adjacent surfaces = "fighting" surfaces = sensitive to tolerances (Course 06).

**OPD Fan / Ray Fan.** OPD fan = $W$ along $P_y$ (tangential) and $P_x$ (sagittal) in waves; Ray Fan = $\varepsilon_y(P_y)$, $\varepsilon_x(P_x)$ in µm. Check the derivative relationship yourself: a ray fan that is a cubic must sit next to an OPD fan that is a quartic. Note the sign convention for OPD in OpticStudio (positive or negative for an undercorrected singlet) — verify it empirically in Task 2 rather than assuming.

**Wavefront Map, Zernike Fringe/Standard Coefficients** — per field and wavelength; the coefficient report also prints P–V and RMS wavefront "to chief" and "to centroid".

## Worked example — Kidger's Cooke triplet, from Seidel sums to everything else

Kidger tabulates the surface Seidel coefficients for a Kingslake triplet: EFL 100 mm, F/4.5, semi-field 20° [Kidger §6.2.7, pp. 113–115]. Re-computing the sums with the formulas above (our Python, Task 1) gives

$$
S_I = 0.011435,\; S_{II} = 0.010332,\; S_{III} = -0.028370,\; S_{IV} = 0.062162,\; S_V = -0.059214,\; C_L = 0.000963,\; C_T = 0.000871\ \text{mm},
$$

matching the book's sums to the last printed digit. Image-space data: $n' = 1$, $u' = -0.11111$ (F/4.5), Lagrange invariant $H = -4.044$ mm, paraxial image height $h' = H/(n'u') = 36.40$ mm $= 100\tan20°$. λ = 587.6 nm.

**Wavefront coefficients** ($\lambda = 0.0005876$ mm):

| | value (mm) | waves |
|---|---|---|
| $W_{040} = S_I/8$ | 0.001429 | **2.43** |
| $W_{131} = S_{II}/2$ | 0.005166 | 8.79 |
| $W_{222} = S_{III}/2$ | −0.014185 | −24.1 |
| $W_{220P} = S_{IV}/4$ | 0.015540 | 26.4 |
| $W_{220S},\ W_{220M},\ W_{220T}$ | | 14.4, 2.3, −9.8 |
| $W_{311} = S_V/2$ | −0.029607 | −50.4 |
| $W_{020}^{chr} = C_L/2$ | 0.000482 | 0.82 |
| $W_{111}^{chr} = C_T$ | 0.000871 | 1.48 |

**Transverse errors** at full aperture/field ($2n'u' = -0.22222$):
- spherical: $S_I/(2n'u') = -0.0515$ mm (−51 µm; negative = marginal ray lands below the axis = undercorrected);
- tangential coma $3S_{II}/(2n'u') = -0.139$ mm, sagittal coma $-0.046$ mm;
- tangential field $(3S_{III}+S_{IV})/(2n'u') = +0.103$ mm, sagittal $(S_{III}+S_{IV})/(2n'u') = -0.152$ mm;
- distortion: $S_V/(2n'u') = +0.266$ mm, i.e. $0.266/36.4 = +0.73\%$ (= $S_V/(2H)$, pincushion).

**Longitudinal spherical:** $|{-S_I/(2u'^2)}| = 0.46$ mm, marginal focus in front of paraxial focus.

**Interpretation.** Large-looking astigmatism and Petzval wavefronts (tens of waves) are actually *balanced*: the medial surface is only 2.3 waves from the paraxial plane, and the triplet has been designed so that S and T fields straddle the image plane. This is the Cooke-triplet strategy you will meet in L09. Distortion of 50 waves sounds huge but only means 0.7% image-shape error — distortion does not blur the image.

## Key takeaways
- $W$ is OPD against a reference sphere centred on the ideal image point; the transverse ray error is its slope: $\varepsilon_y = (1/n'u')\,\partial W/\partial\rho_y \approx -2N\,\partial W/\partial\rho_y$.
- The aberration polynomial is forced by symmetry; $W_{klm}$ subscripts give the powers of field, pupil and $\cos\theta$, so scaling with aperture and field can be read off directly.
- Seidel sums are additive surface contributions computed from two paraxial rays. $W_{040}=S_I/8$, $W_{131}=S_{II}/2$, $W_{222}=S_{III}/2$, $W_{220P}=S_{IV}/4$, $W_{311}=S_V/2$.
- Positive $S_I$ = undercorrected spherical (normal for positive lenses).
- Zernike Fringe vs Standard differ in ordering *and* normalization; Standard coefficients are RMS contributions. Field along $+y$ puts coma into the sinθ term.
- Seidel numbers are third-order and paraxial: excellent for diagnosis and pre-design, insufficient for final performance of fast/wide lenses.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Wavefront aberration $W$ / OPD | Optical path difference between the actual wavefront and the reference sphere, along the ray, in waves |
| Reference sphere | Sphere in the exit pupil centred on the ideal image point; zero-OPD reference |
| Transverse ray aberration | Image-plane miss distance of a ray relative to the chief ray (or centroid) |
| $W_{klm}$ | Coefficient of $H^k\rho^l\cos^m\theta$ in the aberration polynomial (Hopkins notation) |
| Seidel sums $S_I$–$S_V$ | Third-order surface contributions summed over the system: spherical, coma, astigmatism, Petzval, distortion |
| $C_L$, $C_T$ | First-order axial and lateral colour Seidel sums |
| Refraction invariant $A$ | $A = n i = n(u + yc)$; same on both sides of a surface |
| Lagrange invariant $H$ | $n(u\bar y - \bar u y)$; constant through the system |
| Fringe / Standard Zernikes | Two orderings/normalizations of Zernike circle polynomials; Standard (Noll) is RMS-normalised |
| Primary / third-order aberration | Synonyms for the five Seidel aberrations |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE Press, 2002: §2.1.1 (sign convention, pp. 17–18); §4.1 (pp. 63–65); §4.4–4.4.2 (pp. 70–81); §4.4.3 (pp. 87–92); §6.1–6.2.7 (pp. 101–115); §6.9 (pp. 130–134).
2. [Geary] J. M. Geary, *Introduction to Lens Design with Practical ZEMAX Examples*, Willmann-Bell, 2002: §7.4–7.6 (pp. 77–83); §37.8 (pp. 430–432).
3. J. Sasián, OPTI 517 Lecture 4 "Aberration coefficients", Univ. of Arizona — <https://wp.optics.arizona.edu/jsasian/wp-content/uploads/sites/33/2016/02/L4-OPTI-517-Aberration-Coefficients.pdf>
4. Ansys/Zemax community, "Seidel diagram and values in merit function operand" — discussion of S vs W units and the 8× / 2× factors: <https://community.zemax.com/got-a-question-7/seidel-diagram-and-values-in-merit-function-operand-5121>
5. Ansys/Zemax community, "Importing Zernike Fringe sag data from MetroPro and correct normalization radius" — practical normalization pitfalls: <https://community.zemax.com/got-a-question-7/importing-zernike-fringe-sag-data-from-metropro-and-correct-normalization-radius-602>
6. ray-optics (Python) third-order module source — an open implementation of Seidel sums you can compare your code against: <https://ray-optics.readthedocs.io/en/latest/_modules/rayoptics/parax/thirdorder.html>
