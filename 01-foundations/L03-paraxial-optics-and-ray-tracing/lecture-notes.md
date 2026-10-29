# L03 — Paraxial Optics and Paraxial Ray Tracing

> **Course 01 · Foundations** · Estimated time: lecture ~3 h, tasks ~4–5 h
> **Prerequisites:** [L01](../L01-light-rays-and-opticstudio-tour/), [L02](../L02-surfaces-sign-conventions-aspheres/) · **Next:** [L04 — Stops, pupils and fields](../L04-stops-pupils-fields/)

## Learning objectives
- Derive and apply the paraxial ray-trace equations (refraction $n'u' = nu - y\phi$ and transfer $y_{j+1} = y_j + u'_j t_j$) and fill in a **y–nu table** by hand for a multi-surface lens.
- Compute surface power, thin-lens power, thick-lens power and the power of separated elements; compute EFL, BFL, FFL and the positions of the principal (and nodal) points.
- Use the Gaussian ($n'/l' - n/l = \phi$) and Newtonian ($zz' = ff'$) conjugate equations and compute transverse and longitudinal magnification.
- Represent a paraxial system with 2×2 **ray-transfer (ABCD) matrices** and extract its focal length from the matrix.
- Write a small Python paraxial tracer and verify OpticStudio's System Data, Cardinal Points and Single Ray Trace outputs.
- Explain why paraxial quantities are *exact* definitions (focal length, image position) even though paraxial rays are fictitious.

## Reading
- **Core:** [Geary Ch. 4, pp. 33–42] — the PRTE pair, Gaussian lens formula from the PRTE, the "flat surfaces with power" picture of a lens (Fig. 4.6), derivation of surface power, mirror power $-2nC$, two-element power (Eq. 4.18), principal-plane location, magnification.
- **Core:** [Kidger Ch. 2: §2.1–2.4, pp. 17–25; §2.6–2.7, pp. 30–39] — sign convention, paraxial region, cardinal points (principal and nodal points), the single surface from equal optical paths (Eq. 2.12), paraxial ray tracing, Newton's equation, combination of two lenses, the thick lens with two worked examples, the $\sum y_i K_i / y_1$ formula. Leave §2.5 (Lagrange invariant) and §2.8–2.9 for L04.
- **Core:** [Kenyon §3.3–3.6, pp. 50–58] — refraction at a spherical interface, thin-lens equation, ray sketching rules, Example 3.1 (two lenses), transverse and longitudinal magnification, matrix methods and the equivalent thin lens.
- **Optional:** Geary Homework 4.9 (p. 42) — paraxial trace of his Ch. 1 singlet.

---

## 1. The paraxial idea

Snell's law is nonlinear; exact ray tracing is iterative and messy by hand. If all angles are small ($\sin\theta \approx \tan\theta \approx \theta$) and all surfaces are replaced by their parabolic approximation $z \approx \tfrac12 c r^2$ [Kidger §2.1.2, p. 18], the equations become **linear** in ray height and angle. In that region every object plane is imaged *perfectly* onto an image plane — no aberrations.

Geary's mental picture is very useful: in the paraxial world a lens looks like a set of **flat planes with power**, separated by the real thicknesses [Geary §4.4, Fig. 4.6, p. 35]. Each plane bends rays by an amount proportional to their height; between planes rays travel straight.

Two important facts about paraxial optics:
1. **It defines the first-order properties.** Focal length, back focal length, image position and size, pupil positions and magnification are *defined* paraxially. When OpticStudio reports "Effective Focal Length", it is a paraxial number.
2. **Linearity means scale-free rays.** Because the equations are linear, you can trace a "paraxial" ray at the full aperture height (say $y = 10$ mm) and still get exact first-order results — the ray is fictitious but the ratios are right [Kidger §2.4.1, pp. 24–25]. Comparing this paraxial ray with the *real* ray at the same pupil coordinate is exactly how aberrations are measured.

---

## 2. The paraxial ray-trace equations (PRTE)

### 2.1 Refraction at a single surface
At a spherical surface of curvature $c$ between indices $n$ (left) and $n'$ (right), a ray at height $y$ with slope $u$ leaves with slope $u'$ given by [Geary Eq. 4.1/4.9, pp. 33, 37; Kidger Eq. 2.16, p. 23]

$$
n'u' = n u - y\,\phi, \qquad \phi = (n' - n)\,c .
$$

Derivation sketch (Geary §4.5, pp. 36–37): in the paraxial limit the surface normal at height $y$ is tilted by $yc$ relative to the axis (it points at the centre of curvature). The angles of incidence and refraction measured from that normal are therefore $i = u + yc$ and $i' = u' + yc$ (check: a ray parallel to the axis, $u = 0$, hitting a convex surface at height $y$ has incidence angle $y/R$). Paraxial Snell, $n i = n' i'$, gives $nu + nyc = n'u' + n'yc$, i.e. $n'u' = nu - (n'-n)cy$. Kidger derives the same result from equal optical paths of the axial ray and the ray through height $h$ [Kidger §2.3, pp. 21–23] — Fermat again.

Note the combination $nu$ (index × angle) always appears together; it is called the **reduced angle** or optical direction. Tables therefore carry the column "nu".

**Mirrors.** Put $n' = -n$: $\phi = -2nc$; in air $\phi = -2c = -2/R$ [Geary Eq. 4.10–4.11, p. 37]. A concave mirror facing the light has $R < 0$, so $\phi > 0$: focal length $|R|/2$.

### 2.2 Transfer between surfaces
Between surface $j$ and $j+1$, separated by thickness $t_j$ in index $n'_j$:

$$
y_{j+1} = y_j + t_j\,u'_j = y_j + \frac{t_j}{n'_j}\,(n'_j u'_j).
$$

The quantity $t/n$ is the **reduced thickness**. Written with reduced quantities, the whole paraxial trace uses only $y$, $nu$, $\phi$ and $t/n$ [Kidger §2.4, pp. 23–24; Kenyon §3.6, pp. 55–57].

### 2.3 The y–nu table
Hand traces are laid out as a table: one column per surface, rows for $c$, $t$, $n$, $\phi$, $t/n$, then the rays. Here is the layout for the Course 01 singlet (R = ±102.7, t = 4, N-BK7 $n_d = 1.5168$, stop at surface 1):

| | Surface 1 | | Surface 2 | | Image |
|---|---|---|---|---|---|
| $R$ (mm) | +102.7 | | −102.7 | | |
| $\phi = (n'-n)c$ (mm⁻¹) | 0.0050321 | | 0.0050321 | | |
| $t$ (mm) / $n'$ | | 4 / 1.5168 | | BFL / 1 | |
| $t/n'$ | | 2.63713 | | | |
| **Marginal ray** $y$ | 10.0000 | | 9.86730 | | 0 |
| $nu$ after surface | −0.050321 | | −0.099975 | | |
| **Chief ray (5°)** $\bar y$ | 0 | | 0.23072 | | 8.7511 |
| $n\bar u$ (before S1: 0.087489) | 0.087489 | | 0.086328 | | |

(Full arithmetic in the worked example.) The **marginal ray** starts at the edge of the pupil from the axial object point; the **chief ray** starts from the edge of the field through the centre of the stop. These two rays are the backbone of first-order design; L04 makes them precise.

---

## 3. Focal lengths, focal points and principal points

### 3.1 Effective and back focal length
Trace a ray parallel to the axis ($u_0 = 0$) at height $y_1$. After the last surface $k$ its reduced slope is $n'_k u'_k$. Then [Kidger Eqs. 2.20–2.21, p. 24]

$$
f' = \text{EFL} = -\frac{y_1}{u'_k}\ (\text{image in air}),\qquad \text{BFL} = -\frac{y_k}{u'_k}.
$$

More generally, the system **power** is $\phi = -n'_k u'_k / y_1$ and $f' = n'_k/\phi$, $f = -n/\phi$, so $n'/f' = -n/f = \phi$ [Kidger Eqs. 2.48–2.49, pp. 32–33]. In air front and rear focal lengths are equal in magnitude.

### 3.2 Principal planes and nodal points
Extend the incoming parallel ray forwards and the outgoing ray backwards: they meet on the **rear (second) principal plane** P′ [Kidger §2.2.1, pp. 18–20; Geary Fig. 4.9, p. 39]. The EFL is measured from P′ to the rear focal point F′. Doing the same with a ray parallel in image space gives the front principal plane P. P and P′ are conjugate planes of **unit magnification**.

**Nodal points** N, N′: a ray aimed at N leaves from N′ at the same angle [Kidger §2.2.2, pp. 20–21]. When object and image are in the same medium (usually air), N = P and N′ = P′. (In a camera with a lens in air, the nodal point is where you rotate the camera for a parallax-free panorama — strictly the entrance pupil, see L04.)

Cardinal points = F, F′, P, P′, N, N′. They let you replace *any* paraxial system by an "equivalent thin lens" stretched between P and P′ [Kenyon §3.6.1, p. 58].

Position of P′ relative to the last vertex [Geary Eq. 4.28, p. 41]:

$$
\delta' = \text{BFL} - \text{EFL}\quad(\text{negative} \Rightarrow \text{P}' \text{ lies left of the last vertex}).
$$

### 3.3 Power of combinations
For two powers $\phi_1$, $\phi_2$ separated by distance $d$ in index $n$ [Geary Eq. 4.18, p. 38; Kidger Eq. 2.56, p. 35]:

$$
\phi = \phi_1 + \phi_2 - \frac{d}{n}\,\phi_1\phi_2 .
$$

This one equation covers:
- **Thin lens** ($d = 0$): $\phi = \phi_1 + \phi_2 = (n-1)(c_1 - c_2)$ — the lensmaker's equation [Geary Eq. 4.22, p. 40].
- **Thick lens** ($d = t$ in glass): $\phi = (n-1)\left[c_1 - c_2 + \frac{(n-1)\,t\,c_1 c_2}{n}\right]$ [Kidger Eq. 2.61, p. 36].
- **Two thin lenses in air**: $1/f = 1/f_1 + 1/f_2 - d/(f_1 f_2)$ [Kenyon Eq. 3.39, p. 58].
- **Two mirrors** (Cassegrain) with $\phi_i = -2c_i$ and negative spacing.

The principal planes of the pair, measured from the first and second element respectively [Kidger Eqs. 2.57–2.58, 2.62–2.63]:

$$
\delta = \frac{d}{n}\frac{\phi_2}{\phi}\ (\text{from element 1}),\qquad \delta' = -\frac{d}{n}\frac{\phi_1}{\phi}\ (\text{from element 2}),
$$

for air on both outer sides. Kidger's two examples are worth remembering: for a unit-power plano-convex lens (curved side first, $n = 1.5$, thickness $d$) P sits on the curved vertex and P′ is $d/3$ inside the glass; for an equiconvex lens P and P′ are each $\approx 0.35d$ inside the lens, so the gap PP′ is ≈ $d/3$ in *both* cases [Kidger §2.7.2, pp. 36–37]. Rule of thumb for glass lenses in air: **PP′ ≈ t/3**.

A many-element generalization [Kidger Eq. 2.66, p. 39]:

$$
\phi = \sum_i \frac{y_i}{y_1}\,\phi_i ,
$$

i.e. each element contributes its power weighted by the marginal ray height on it. This is why a field lens near a focus (small $y$) contributes little power, and why lenses near the stop (large $y$) dominate — a key thin-lens predesign insight.

---

## 4. Conjugate equations and magnification

### 4.1 Gaussian (vertex/principal-plane) form
For a single surface, measuring object distance $l$ and image distance $l'$ from the vertex [Kidger Eq. 2.12, p. 22; Kenyon Eq. 3.12, p. 51]:

$$
\frac{n'}{l'} - \frac{n}{l} = (n' - n)c = \phi .
$$

For any system, measuring from the principal planes, the same form holds with the system power [Kidger Eq. 2.50, p. 32]; in air:

$$
\frac{1}{l'} - \frac{1}{l} = \frac{1}{f'} .
$$

Geary derives this directly from the PRTE with $u = -y/l$ and $u' = -y/l'$ [Geary §4.3, p. 35]. Remember the sign convention: a real object to the left has $l < 0$.

### 4.2 Newtonian form
Measure instead from the focal points: $z = l - f$ (object from F), $z' = l' - f'$ (image from F′). Then [Kidger Eq. 2.40, p. 30]:

$$
z\,z' = f f' \quad(\text{in air: } z z' = -f'^2).
$$

Newton's form is handy for small focus shifts: moving a camera's object from infinity to distance $z$ moves the image by $z' = -f'^2/z$. For $f' = 100$ mm and an object 1 m in front of F, the image moves 10 mm — this is the focus travel your lens mount must provide.

### 4.3 Magnification
Transverse magnification [Geary Eq. 4.30, p. 41; Kidger Eq. 2.47, p. 32]:

$$
m = \frac{h'}{h} = \frac{n\,u}{n'\,u'} = \frac{n\,l'}{n'\,l}\quad\left(\text{in air: } m = \frac{l'}{l} = -\frac{z'}{f'} = -\frac{f}{z}\right).
$$

A real image of a real object through a positive lens has $m < 0$ (inverted). **Longitudinal magnification** (for small axial displacements) is $m_L \approx m^2$ in air [Kenyon Eq. 3.21, p. 53]: depth is magnified much more strongly than width when $|m| > 1$, and compressed when $|m| < 1$ — relevant for depth of field in 3D imaging (Course 04).

---

## 5. Matrix (ABCD) formulation

Collect a ray into a column vector of height and reduced angle, $\begin{pmatrix} y \\ nu \end{pmatrix}$. Then refraction and transfer are matrix multiplications:

$$
\mathbf{R}(\phi) = \begin{pmatrix} 1 & 0 \\ -\phi & 1\end{pmatrix},\qquad
\mathbf{T}(t, n) = \begin{pmatrix} 1 & t/n \\ 0 & 1\end{pmatrix}.
$$

A system is the product, rightmost first: $\mathbf{S} = \mathbf{R}_k\mathbf{T}_{k-1}\cdots\mathbf{T}_1\mathbf{R}_1 = \begin{pmatrix} A & B \\ C & D\end{pmatrix}$. Each matrix has unit determinant, so $AD - BC = 1$ (this is the Lagrange invariant in disguise, L04). From the vertex-to-vertex matrix:
- power $\phi = -C$, so $f' = -1/C$ (in air);
- BFL $= -A/C$; FFL (front vertex to F) $= D/C$.

Kenyon uses the same idea with the vector ordered $(n\alpha, y)$, so his matrices look transposed [Kenyon §3.6, pp. 55–58] — always check the ordering in any source. ABCD matrices are also the language of Gaussian-beam propagation (Course 03 L07), so it pays to be fluent.

---

## 6. In OpticStudio

- **System Data report** (Analyze → Reports → System Data): EFL, BFL, F-numbers, paraxial image height and magnification, entrance/exit pupil diameter and position, total track — all paraxial, at the primary wavelength.
- **Cardinal Points report** (Analyze → Reports → Cardinal Points): positions of focal, principal, nodal and anti-principal/anti-nodal planes for the primary wavelength (selectable). Read the report header carefully: object-space positions are given relative to one reference surface and image-space positions relative to another (in current versions the first surface and the image surface, respectively — check your version's header). This is the most common source of "my numbers don't match" confusion.
- **Single Ray Trace** (Analyze → Rays & Spots → Single Ray Trace): traces one ray specified by normalized field $(H_x, H_y)$ and pupil $(P_x, P_y)$ coordinates and prints *both* a real-ray table and a paraxial-ray table (heights and direction tangents per surface) [Geary §4.1, p. 33]. With $H_y = 0, P_y = 1$ you get the paraxial marginal ray; with $H_y = 1, P_y = 0$ the paraxial chief ray. Note that OpticStudio prints direction tangents/cosines per surface rather than $nu$; multiply by the index if you compare with a y–nu table.
- **Paraxial surface type:** a `Paraxial` surface in the LDE is an ideal thin lens with a specified focal length — perfect for first-order system sketches (e.g. a projector + camera triangulation layout) before real lenses exist.
- **Operands** you'll meet in L07: `EFFL` (effective focal length), `PMAG` (paraxial magnification), `PIMH` (paraxial image height).
- **Pitfalls:**
  - EFL/BFL depend on the **primary wavelength**. Change the primary and they change (L05).
  - BFL in System Data is measured from the last *glass* surface to the paraxial focus — not to your image surface, if you have defocused it.
  - OpticStudio's "Front Focal Length" sign follows the Cartesian convention (negative for a positive lens).

---

## Worked example — complete paraxial analysis of the Course 01 singlet

**Prescription:** $R_1 = +102.7$, $R_2 = -102.7$, $t = 4$ mm, $n = 1.5168$, air elsewhere. Stop at surface 1, EPD = 20 mm, field 5°.

**Step 1 — surface powers.**
$\phi_1 = (1.5168 - 1)/102.7 = 0.0050321$ mm⁻¹; $\phi_2 = (1 - 1.5168)/(-102.7) = 0.0050321$ mm⁻¹.

**Step 2 — system power (thick lens).**
$\phi = \phi_1 + \phi_2 - (t/n)\phi_1\phi_2 = 0.0100643 - 2.63713 \times 2.5322\times10^{-5} = 0.0099975$ mm⁻¹ → **EFL = 100.025 mm**.

**Step 3 — marginal ray** ($y_1 = 10$, $u_0 = 0$):
- S1: $n'u' = 0 - 10 \times 0.0050321 = -0.050321$ → $u' = -0.050321/1.5168 = -0.033176$.
- Transfer: $y_2 = 10 + 4 \times (-0.033176) = 9.86730$.
- S2: $n'u' = -0.050321 - 9.86730 \times 0.0050321 = -0.099975$.
- EFL $= -y_1/u'_2 = 10/0.099975 = 100.025$ mm ✓. **BFL** $= -y_2/u'_2 = 9.86730/0.099975 = 98.698$ mm.

**Step 4 — principal planes.**
$\delta' = \text{BFL} - \text{EFL} = 98.698 - 100.025 = -1.327$ mm: P′ is 1.327 mm *inside* the lens from surface 2. By symmetry P is 1.327 mm inside from surface 1 (formula: $\delta = (t/n)\phi_2/\phi = 2.63713 \times 0.0050321/0.0099975 = 1.327$ mm). PP′ = 4 − 2×1.327 = 1.345 mm ≈ $t/3$ ✓.

**Step 5 — chief ray** (5°, through the stop centre): $\bar u_0 = \tan 5° = 0.087489$, $\bar y_1 = 0$.
- S1: $n\bar u' = 0.087489$ (no bending at $y = 0$); $\bar u' = 0.057680$.
- $\bar y_2 = 0 + 4 \times 0.057680 = 0.23072$.
- S2: $n\bar u' = 0.087489 - 0.23072 \times 0.0050321 = 0.086328$.
- At the paraxial image (98.698 mm further): $\bar y' = 0.23072 + 98.698 \times 0.086328 = 8.7511$ mm $= f'\tan 5°$ ✓.

**Step 6 — finite conjugate.** Object 300 mm left of surface 1, i.e. $l = -300 - 1.327 = -301.327$ mm from P. Gaussian: $1/l' = 1/100.025 - 1/301.327$ → $l' = 149.727$ mm from P′, i.e. **148.399 mm after surface 2**. Check by tracing a ray from the axial object: $u_0 = 10/300$, giving the same 148.399 mm. Magnification $m = l'/l = -0.4969$. Newton: $z = l + f' = -201.302$, $z' = l' - f' = 49.702$; $zz' = -10005.0 = -f'^2$ ✓.

**Step 7 — matrix check.** $\mathbf{S} = \mathbf{R}(\phi_2)\mathbf{T}(4, 1.5168)\mathbf{R}(\phi_1) = \begin{pmatrix} 0.98673 & 2.63713 \\ -0.0099975 & 0.98673 \end{pmatrix}$, det = 1. $f' = -1/C = 100.025$ mm, BFL $= -A/C = 98.698$ mm ✓.

**Geary's thin-lens PRTE example** [Geary §4.2, pp. 33–34]: an object 25 units before a thin lens with $\phi = 0.05$, ray at $y = 5$: $u = 5/25 = 0.2$; $u' = 0.2 - 5 \times 0.05 = -0.05$; image at $5/0.05 = 100$ units. Gaussian check: $1/l' = 0.05 - 1/25 = 0.01$ ✓.

---

## Key takeaways
- Paraxial optics linearizes Snell's law: $n'u' = nu - y\phi$ and $y_{j+1} = y_j + t_j u'_j$. Surface power $\phi = (n'-n)c$, mirror power $-2nc$.
- Paraxial results (EFL, BFL, image position, magnification) are exact *definitions*; trace the fictitious paraxial ray at full aperture height without loss of accuracy.
- Two powers separated by $d$: $\phi = \phi_1 + \phi_2 - (d/n)\phi_1\phi_2$ — thin lens, thick lens, two lenses, two mirrors.
- Principal planes are unit-magnification planes; for a glass lens in air PP′ ≈ $t/3$; $\delta' = \text{BFL} - \text{EFL}$.
- Gaussian $1/l' - 1/l = 1/f'$; Newtonian $zz' = -f'^2$ (air); $m = l'/l$; $m_L \approx m^2$.
- ABCD matrices with $(y, nu)$ make long systems easy; $f' = -1/C$.
- OpticStudio: System Data, Cardinal Points (check reference surfaces!), Single Ray Trace (real + paraxial tables).

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Paraxial ray | Fictitious ray obeying the linearized equations |
| PRTE | Paraxial ray-trace equations (refraction + transfer) |
| Reduced angle $nu$ | Index × paraxial slope |
| Reduced thickness $t/n$ | Thickness divided by index |
| Power $\phi$ | Inverse focal length (×index); surface power $(n'-n)c$ |
| EFL $f'$ | Distance from rear principal plane to rear focus |
| BFL | Last vertex to rear focus |
| FFL | Distance from the first vertex to the front focus (negative for a positive lens in the Cartesian convention) |
| Principal planes P, P′ | Conjugate planes with $m = +1$ |
| Nodal points N, N′ | Conjugate points with unit angular magnification |
| Cardinal points | F, F′, P, P′, N, N′ |
| Gaussian equation | $n'/l' - n/l = \phi$ |
| Newtonian equation | $zz' = ff'$ |
| Longitudinal magnification | $\approx m^2$ in air |
| ABCD matrix | 2×2 ray-transfer matrix |
| Marginal ray | Ray from axial object point through edge of stop |
| Chief ray | Ray from field edge through centre of stop |

## References
1. [Geary Ch. 4, pp. 33–42] §4.2 PRTE, §4.3 Gaussian formula, §4.4 PRTE world, §4.5 surface power, §4.6 mirror/two-element/thin lens, §4.7 principal planes, §4.8 magnification, §4.9 homework.
2. [Kidger §2.1–2.4, pp. 17–25] sign convention, paraxial region, cardinal points, single surface, paraxial ray tracing.
3. [Kidger §2.6–2.7, pp. 30–39] Newton's equation, system power, two lenses, thick lens examples, many elements.
4. [Kenyon §3.3–3.6, pp. 50–58] spherical interface, thin lens equation, ray sketching, Example 3.1, magnification, matrix methods, equivalent thin lens.
5. Ansys Optics, "How to design a singlet lens – Part 1: Setup" (shows an F-number solve controlling a radius, a paraxial constraint you'll use in L07): https://optics.ansys.com/hc/jp/articles/42661252179987
