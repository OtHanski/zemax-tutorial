# L02 — Surfaces, Sign Conventions, Sag, Conics and Aspheres

> **Course 01 · Foundations** · Estimated time: lecture ~2.5 h, tasks ~4 h
> **Prerequisites:** [L01](../L01-light-rays-and-opticstudio-tour/) · **Next:** [L03 — Paraxial optics and ray tracing](../L03-paraxial-optics-and-ray-tracing/)

## Learning objectives
- Apply the Cartesian sign convention used by OpticStudio (and Kidger/Geary) to radii, curvatures, thicknesses, distances and ray angles — including after a mirror.
- Compute the curvatures of a thin lens of given power and **shape factor** (bending), and recognize plano-convex, equiconvex, convex-plano and meniscus shapes by their shape factor.
- Compute the **sag** of a spherical surface exactly and with the parabolic approximation, and use sag to find the **edge thickness** of a lens.
- Write the conic surface equation, relate the conic constant $k$ to eccentricity and surface type, and name the classic "perfect" conic surfaces (parabolic mirror, hyperbolic plano-convex lens).
- Describe the **even asphere** polynomial, explain why aspheres do not change paraxial properties (as long as no $r^2$ term is used), and estimate the **departure from the best sphere** a manufacturer needs to know.
- Enter Standard (conic) and Even Asphere surfaces in the OpticStudio LDE and check a surface's sag.

## Reading
- **Core:** [Geary Ch. 3, pp. 21–28] — sign conventions (§3.2), shape factor (§3.3), sag (§3.4), the conic equation and table of conic constants (§3.5), departure from sphere with the F/1.25 parabola example (§3.6). The homework (§3.7, pp. 28–31) is an excellent ZEMAX bending/asphere exercise — we do a modern version in L07.
- **Core:** [Kidger §1.7, pp. 8–15] — sphere equation in the numerically stable form, power series of the sag, quadrics of revolution, oblate ellipsoid, hyperboloid, axicon.
- **Core:** [Kidger §3.6, pp. 57–60] — the asphere equation and how ray tracers find the intersection with an asphere iteratively.
- **Optional:** [Kidger §2.1.1, pp. 17–18] — the sign convention for ray heights and angles (needed in L03).

---

## 1. Why sign conventions matter

Every formula in lens design (paraxial ray trace, Seidel sums, thick-lens power) contains signs. Optics textbooks historically used several conventions ("real-is-positive", "New Cartesian", etc.), and Kidger remarks that the subject "has not been helped" by this [Kidger §2.1.1, p. 17]. OpticStudio uses a **Cartesian** convention, which is also the one used by Kidger and Geary. Learn it once, use it everywhere, and when you read another source, check its convention before trusting a sign.

---

## 2. The Cartesian sign convention

Light travels left → right (+z) in object space. Then [Geary §3.2, p. 21; Kidger §2.1.1, pp. 17–18]:

| Quantity | Positive when… | Example |
|---|---|---|
| Distance along z (thickness, object/image distance) | measured left → right | image 100 mm right of lens: $l' = +100$ |
| Ray height $y$ | above the axis | |
| Radius of curvature $R$ | centre of curvature is to the **right** of the vertex | front face of a biconvex lens |
| Curvature $c = 1/R$ | same sign as $R$ | flat surface: $c = 0$, $R = \infty$ |
| Ray angle $u$ | the ray slopes **upwards** going left → right (counter-clockwise from +z) | a ray converging to the axis from above has $u < 0$ |
| Refractive index | positive; changes sign after a reflection in the classical convention | |

Consequences you should be able to recite:
- **Biconvex lens:** $R_1 > 0$, $R_2 < 0$. **Biconcave:** $R_1 < 0$, $R_2 > 0$.
- A **meniscus** has both radii of the same sign.
- An object at a finite distance to the *left* of a lens has a **negative** object distance; a real image to the right has a **positive** image distance [Geary §3.2, p. 21]. Front focal length is negative, rear focal length positive.
- Ray angles do not depend on direction of travel: Kidger points out that a ray retraced right-to-left along the same line has the same slope and therefore the same sign [Kidger §2.1.1, p. 18].

### 2.1 Mirrors in OpticStudio
After a reflection light travels right → left. OpticStudio handles this by making **thicknesses after an odd number of mirrors negative**: a concave mirror with focal length 100 mm facing the incoming light has $R = -200$ mm (centre of curvature to the left of the vertex) and the image surface sits at thickness $-100$ mm. You type `MIRROR` in the Material column; you do *not* flip indices manually. (Kidger's alternative device of $n' = -n$ [Kidger §1.3, p. 3] is what goes on internally in many formulas.)

```
           incoming light  ───►
                                 )  concave mirror, R = -200 (centre at left)
   image  ◄───  thickness = -100 ┘
```

### 2.2 What OpticStudio stores
The LDE shows **radius**, but the `.zmx` file stores **curvature** (`CURV` keyword) — because a flat surface is simply $c = 0$, and because curvature is what enters the ray-trace equations linearly (power $\phi = (n'-n)c$). Optimizers also vary curvature internally, which avoids the singularity at $R = \infty$. Keep that in mind when you script things in Course 07.

---

## 3. Curvature, power and the shape factor

### 3.1 Surface power (preview of L03)
A spherical refracting surface of curvature $c$ between indices $n$ and $n'$ has (paraxial) power

$$
\phi = (n' - n)\,c .
$$

A thin lens in air of index $n$ has power

$$
\phi = (n-1)(c_1 - c_2) = \frac{1}{f}.
$$

Only the *difference* of the curvatures sets the power. The *sum* is free — and that freedom is called **bending**.

### 3.2 Shape factor
Geary defines the shape factor [Geary §3.3, Eq. 3.1, p. 21]

$$
X = \frac{c_1 + c_2}{c_1 - c_2} = \frac{R_2 + R_1}{R_2 - R_1}.
$$

(This is often called the Coddington shape factor; some books use $q$ or $B$.) Given the power $\phi$ and shape factor $X$, the curvatures are

$$
c_1 = \frac{\phi\,(X+1)}{2(n-1)}, \qquad c_2 = \frac{\phi\,(X-1)}{2(n-1)}.
$$

(Check: $c_1 - c_2 = \phi/(n-1)$ ✓ and $(c_1+c_2)/(c_1-c_2) = X$ ✓.)

```
   X < -1        X = -1        X = 0          X = +1        X > +1
  meniscus    plano-convex   equiconvex   convex-plano    meniscus
  (concave   (flat side to   R1 = -R2     (curved side    (convex
   to object)  object)                     to object)      to object)
     ((           |)            ()            (|              ))
```

All five have the same focal length but very different **aberrations** [Geary Fig. 3.2, p. 22]. Bending also moves the principal planes relative to the glass (L03). For a collimated input beam, the minimum spherical aberration of an $n \approx 1.5$ singlet occurs near $X \approx +0.7$ — very close to convex-plano with the curved side towards the distant object. That is why every catalogue plano-convex lens comes with the instruction "curved side towards the collimated beam". You will see this numerically in the tasks; Course 02 L02 derives it.

---

## 4. Surface sag

The **sag** $z(r)$ is the axial depth of the surface at radial distance $r$ from the axis, measured from the vertex tangent plane [Geary §3.4, pp. 22–23]. For a sphere of radius $R$ through the origin [Kidger Eqs. 1.12–1.15, pp. 8–9]:

$$
z = R - \sqrt{R^2 - r^2} \;=\; \frac{c\,r^2}{1 + \sqrt{1 - c^2 r^2}} .
$$

The second form is the one software uses: it is numerically stable (no difference of two large numbers when $R \gg r$), and it works for $c = 0$ (flat surface). The sign of $z$ follows the sign of $c$.

The power-series expansion [Kidger Eq. 1.17, p. 10]:

$$
z = \tfrac{1}{2}c r^2 + \tfrac{1}{8}c^3 r^4 + \tfrac{1}{16}c^5 r^6 + \dots
$$

The first term is the **parabolic approximation** $z \approx r^2/(2R)$ [Geary Eq. 3.5, p. 23]. The paraxial region of L03 is exactly the region where only this first term matters [Kidger §2.1.2, p. 18].

### 4.1 Why sag matters in practice
- **Metrology:** opticians check a radius with a spherometer, which measures sag over a known ring diameter [Geary §3.4, p. 22].
- **Edge thickness.** For a lens with centre thickness $t$ and surfaces with sags $z_1(r)$ and $z_2(r)$ at the rim radius $r$:
$$
t_{\text{edge}} = t - z_1(r) + z_2(r).
$$
A positive lens gets thinner at the edge; if $t_{\text{edge}}$ approaches zero the lens is unmanufacturable (knife edge). A common shop rule: edge thickness ≥ ~1 mm (or ~5–10 % of the diameter) for small glass lenses — you will make this a constraint in L07.
- **Mechanical design:** sag determines spacer shapes and whether two lenses collide in an air gap.

---

## 5. Conic surfaces

### 5.1 The equation
Rotating a conic section (ellipse, parabola, hyperbola) about the optical axis gives a **conicoid**. With vertex curvature $c = 1/R$ and **conic constant** $k$ [Kidger Eq. 1.22, p. 11; Geary §3.5, pp. 23–26]:

$$
z(r) = \frac{c\,r^2}{1 + \sqrt{1 - (1+k)\,c^2 r^2}} .
$$

The conic constant is related to the eccentricity $e$ by $k = -e^2$ (for prolate ellipsoids and hyperboloids) [Kidger Eq. 1.23, p. 11]:

| $k$ | Surface | Notes |
|---|---|---|
| $k > 0$ | oblate ellipsoid | ellipse rotated about its *minor* axis [Kidger §1.7.3] |
| $k = 0$ | sphere | |
| $-1 < k < 0$ | prolate ellipsoid | two foci on the axis; images one focus perfectly onto the other |
| $k = -1$ | paraboloid | images an infinitely distant on-axis point perfectly (as a mirror) |
| $k < -1$ | hyperboloid | Cassegrain secondary; axicon in the limit of very large $c$ [Kidger §1.7.5] |

**Convention trap.** Some authors (e.g. Kingslake) use $P = 1 + k$ instead of $k$; Kidger uses $\varepsilon = 1 + k$ in derivations. Geary and OpticStudio use $k$ [Geary §3.5, p. 24]. When you copy a conic from a paper or patent, check which constant is meant — a parabola is $k = -1$ but $P = 0$.

Expanding [Kidger Eq. 1.24, p. 11]:

$$
z = \tfrac{1}{2}c r^2 + \tfrac{1}{8}(1+k)c^3 r^4 + \tfrac{1}{16}(1+k)^2 c^5 r^6 + \dots
$$

The $r^2$ term — and hence all **paraxial properties** — is independent of $k$ [Geary §3.5, p. 24]. The conic only changes the $r^4$ and higher terms, i.e. only the *aberrations*. To leading order the conic departs from the sphere of the same vertex radius by

$$
\Delta z \approx \frac{k\,c^3 r^4}{8}.
$$

### 5.2 Perfect conics worth remembering
These follow from Fermat's principle (equal optical path to the focus):
1. **Parabolic mirror ($k = -1$)**: perfect on-axis image of a star. The classical Newtonian and Cassegrain primary [Geary §3.5, pp. 26–27].
2. **Ellipsoidal mirror ($-1 < k < 0$)**: perfect imaging between its two foci.
3. **Hyperbolic mirror ($k < -1$)**: a ray aimed at one focus is redirected to the other — the Cassegrain secondary [Geary Fig. 3.6–3.7, pp. 26–27].
4. **Plano-hyperbolic lens**: collimated light entering a flat face, leaving through a hyperboloid with $k = -n^2$, focuses perfectly (on axis, at one wavelength).
5. **Ellipsoidal refracting surface with $k = -1/n^2$**: collimated light in air focuses perfectly *inside* glass of index $n$.

"Perfect" always means: one conjugate, on axis, one wavelength. Off axis and in white light the aberrations return — as you will see in the tasks.

---

## 6. General aspheres

### 6.1 The even asphere
A conic offers one extra parameter. For more freedom, add a polynomial in $r^2$ [Kidger Eq. 3.48, p. 57]:

$$
z(r) = \frac{c\,r^2}{1 + \sqrt{1 - (1+k)c^2 r^2}} + \alpha_4 r^4 + \alpha_6 r^6 + \alpha_8 r^8 + \dots
$$

Only even powers appear so that the surface is smooth and rotationally symmetric on the axis. Kidger notes that the series is rarely taken beyond $r^{10}$ in classical designs [Kidger §3.6, p. 58]; molded plastic camera lenses often go to $r^{16}$ or more (Course 04 L07).

**OpticStudio's Even Asphere** surface uses exactly this form, plus an $\alpha_2 r^2$ term ("2nd order term"). Leave $\alpha_2 = 0$: an $r^2$ term duplicates the curvature, *changes the paraxial power*, and makes curvature and $\alpha_2$ degenerate variables in optimization. Coefficients carry units (mm$^{-3}$, mm$^{-5}$, …), so they change when you scale a lens — another reason modern designs use normalized forms (Q-type polynomials, Course 04 L07).

### 6.2 How a ray tracer handles an asphere
A ray–sphere intersection is a quadratic equation with a closed-form solution. For a general asphere there is no closed form: the tracer starts from a nearby point (intersection with the vertex plane or the base sphere), computes the surface point with the same $(x, y)$, intersects the ray with the tangent plane there, and iterates until the change is tiny (Kidger quotes ~λ/1000, typically ~5 iterations) [Kidger §3.6, pp. 58–60]. In practice: aspheres trace slightly slower, and a wild polynomial can make the iteration fail — OpticStudio then reports a ray-trace error for that ray.

### 6.3 Departure from sphere — talk to the shop
Spheres are cheap: any small patch of a sphere fits the sphere everywhere, so lapping/polishing with a large tool naturally produces spheres. Aspheres need deterministic sub-aperture polishing, diamond turning or molding, and special metrology (null optics or CGH interferometry, profilometers) [Geary §3.6, pp. 27–28]. Geary's advice: aspheres only when there is no other way or a trade study shows they pay off; and always quote **departure from (best-fit) sphere** to the vendor.

Geary's example: an F/1.25 parabola with $R = 625$ mm and semi-aperture 125 mm departs from the vertex sphere by about 0.128 mm ≈ 200 waves at 632.8 nm [Geary §3.6, p. 28] — far too much for a standard interferometer test without a null lens. A small molded asphere in a machine-vision lens might depart by tens of micrometres: easy for a mould, hard for a classical polishing shop.

For a Zivid-type product the practical rule is: glass spheres for low volumes and tight thermal stability; molded aspheres (glass or polymer) when volume is high and the element count or package must shrink.

---

## 7. In OpticStudio

- **Surface Type column (LDE):** `Standard` = sphere or conic (has a *Conic* column). `Even Asphere` adds parameter columns for the 2nd, 4th, 6th… order terms. Change the type by clicking the Surface Type cell (or via the surface properties panel that opens from the arrow at the left of each row). Other types you will meet: `Odd Asphere`, `Toroidal`, `Biconic`, `Paraxial` (ideal thin lens), `Coordinate Break`, Q-type and Zernike surfaces.
- **Radius sign:** type it exactly by the Cartesian convention. If your Cross-Section shows a lens that looks like a negative meniscus when you expected a biconvex, flip a sign.
- **Semi-diameter vs. clear aperture.** The *Semi-Diameter* column is the clear radius used for drawing and edge-thickness calculations. Newer versions also show *Chip Zone* and *Mech Semi-Dia* columns — the extra rim for bevels and mounting (Course 06).
- **Sag:** an Analyze-tab surface sag plot or sag table exists (look in the Surface group of the Analyze tab; location varies by version). The Prescription Data report and the *Edge Thickness* information in the LDE/reports also help.
- **Tools you'll use with bending:** *Reverse Elements* (in the LDE toolbar — reverses a range of surfaces, flipping a lens around) and *Make Focal* / *Scale Lens* (scale to a new focal length). Exact locations vary by version; hover over LDE toolbar icons.
- **Pitfalls:**
  - Entering the conic as $P = 1 + k$ from an old reference.
  - Forgetting that an Even Asphere's $r^2$ term changes the focal length.
  - Aspheric coefficients from a design in inches used in a design in mm (coefficients scale as $L^{1-n}$ for the $r^n$ term).
  - A "flat" surface in OpticStudio is `Infinity` in the Radius column; typing `0` is interpreted as… also infinity (curvature 0). Be explicit: type `Infinity` (or `inf`).

---

## Worked example — bending, sag and edge thickness of the Course 01 singlet

**Given:** thin lens, $f = 100$ mm, N-BK7 ($n_d = 1.5168$), semi-aperture of the beam $y = 10$ mm (F/5), lens rim $r = 12.5$ mm (25 mm diameter), centre thickness 4 mm.

**(a) Curvatures for several bendings.** $\phi/(2(n-1)) = 0.01 / 1.0336 = 0.0096749$ mm$^{-1}$.

| $X$ | $c_1$ (mm⁻¹) | $c_2$ (mm⁻¹) | $R_1$ (mm) | $R_2$ (mm) | Shape |
|---|---|---|---|---|---|
| −1 | 0 | −0.019350 | ∞ | −51.68 | plano-convex (flat to object) |
| 0 | 0.0096749 | −0.0096749 | 103.36 | −103.36 | equiconvex |
| +1 | 0.019350 | 0 | 51.68 | ∞ | convex-plano |
| +2 | 0.029025 | 0.0096749 | 34.45 | 103.36 | positive meniscus |

With 4 mm thickness the true EFL departs slightly from 100 mm (e.g. 100.66 mm for the equiconvex form, 100.00 mm for both plano forms); our L01 lens used 102.7 mm radii to bring the equiconvex EFL back to 100.0 mm.

**(b) Sag of the L01 surfaces ($R = 102.7$ mm).**
- At $r = 10$: exact $z = 102.7 - \sqrt{102.7^2 - 100} = 0.48801$ mm; parabolic $r^2/2R = 0.48685$ mm. Difference 1.2 µm (≈ $c^3r^4/8$).
- At $r = 12.5$: exact 0.76355 mm; parabolic 0.76071 mm.

**(c) Edge thickness at $r = 12.5$:** $t_\text{edge} = 4 - 0.76355 + (-0.76355) = 2.473$ mm. At $r = 15$ (30 mm diameter) it drops to 1.80 mm.

**(d) A perfect plano-hyperbolic lens.** For the X = −1 form ($R_2 = -51.68$ mm), the conic that removes on-axis spherical aberration is $k = -n_d^2 = -2.3007$. Its departure from the base sphere is approximately $k c^3 r^4/8$:
$$
\Delta z(10) \approx \frac{(-2.3007)(-1/51.68)^3(10^4)}{8} = +0.0208\ \text{mm} \approx 21\ \mu\text{m}
$$
(the exact value is 20.7 µm; $\approx 43$ µm at $r = 12$). A Python ray trace confirms the on-axis d-light spot is essentially zero (nm level) at the paraxial focus — but the polychromatic on-axis RMS radius is still ≈ 49 µm (axial colour), and at 5° field the d-light RMS radius is ≈ 129 µm (coma/astigmatism). One aspheric surface fixes one aberration, at one wavelength, on axis.

**(e) Geary's parabola.** $R = 625$ mm, $r = 125$ mm. Sphere sag $= 625 - \sqrt{625^2 - 125^2} = 12.6276$ mm; parabola sag $= r^2/2R = 12.5000$ mm; departure 0.1276 mm = 201.6 waves at 632.8 nm (Geary: 127.5 µm ≈ 201 λ from the first two series terms, 0.125 + 0.0025 mm) [Geary §3.6, p. 28].

---

## Key takeaways
- OpticStudio uses a Cartesian convention: distances left→right positive, $R > 0$ if centre of curvature is to the right, upward-sloping rays have $u > 0$, thickness negative after a mirror.
- Lens power depends on $c_1 - c_2$; the shape factor $X = (c_1+c_2)/(c_1-c_2)$ describes the bending, which changes aberrations but not (thin-lens) power.
- Sag $z = cr^2/(1+\sqrt{1-(1+k)c^2r^2})$; parabolic approximation $r^2/2R$; edge thickness $t - z_1 + z_2$.
- Conic constant $k = -e^2$: 0 sphere, −1 parabola, < −1 hyperbola, between −1 and 0 prolate ellipse, > 0 oblate. Watch for $P = 1+k$ conventions.
- Conics and higher aspheric terms change only $r^4$ and higher terms → aberrations, not paraxial properties (unless you use an $r^2$ term).
- Aspheres cost money and metrology effort; always quote departure from sphere. One asphere typically corrects one aberration at one conjugate/wavelength.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Vertex | Point where a surface crosses the optical axis |
| Curvature $c$ | $1/R$; zero for a flat surface |
| Shape factor $X$ | $(c_1+c_2)/(c_1-c_2)$; describes lens bending |
| Bending | Changing $c_1$ and $c_2$ together at constant power |
| Meniscus | Lens whose two radii have the same sign |
| Sag | Axial depth of a surface at radius $r$ from the vertex plane |
| Edge thickness | Glass thickness at the rim: $t - z_1 + z_2$ |
| Conic constant $k$ | Shape parameter of a conicoid; $k = -e^2$ |
| Eccentricity $e$ | Conic-section parameter; 0 for circle, 1 for parabola |
| Even asphere | Conic plus a polynomial in even powers of $r$ |
| Departure from sphere | Difference between asphere and (vertex or best-fit) sphere |
| Spherometer | Instrument that measures radius via sag |

## References
1. [Geary Ch. 3, pp. 21–28] Geary, *Introduction to Lens Design*: §3.2 sign conventions, §3.3 shape factor, §3.4 surface sag, §3.5 aspheric surfaces (Table 3.1), §3.6 departure from sphere; §3.7 homework pp. 28–31.
2. [Kidger §1.7, pp. 8–15] Kidger, *Fundamental Optical Design*: spheres, quadrics of revolution, oblate ellipsoid, hyperbola, axicon.
3. [Kidger §2.1.1–2.1.2, pp. 17–18] sign convention for paraxial rays; definition of the paraxial region.
4. [Kidger §3.6, pp. 57–60] ray tracing through aspheric and toroidal surfaces.
5. Ansys Optics, "How to design a singlet lens – Part 1: Setup" (radius solves and the singlet setup used as a reference throughout Course 01): https://optics.ansys.com/hc/jp/articles/42661252179987
