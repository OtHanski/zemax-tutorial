# L02 — Spherical Aberration and Lens Bending

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~4 h
> **Prerequisites:** [L01 — Wavefront and transverse aberrations](../L01-wavefront-and-transverse-aberrations/) (and your `seidel.py`) · **Next:** [L03 — Coma, astigmatism and symmetry](../L03-coma-astigmatism-and-symmetry/)

## Learning objectives
- Explain physically why a spherical refracting surface produces spherical aberration, and name the three conditions under which a single surface is free of it.
- Use the thin-lens shape factor $B$ (Geary's $X$) and conjugate factor $C$ (Geary's $Y$) to compute $S_I$ for a singlet, and find the bending for minimum spherical aberration — by hand and in Python.
- Predict the best-focus shift for spherical aberration for each criterion (minimum RMS wavefront, minimum RMS spot, minimum blur circle) and the improvement each brings.
- Balance third-order against fifth-order spherical aberration and recognise the zonal residual it leaves.
- Set up a bending study in OpticStudio (curvature variables with an EFL constraint, Quick Focus, Seidel Coefficients, Ray Fan/OPD Fan) and compare it with thin-lens theory.
- Estimate the F-number at which a best-form singlet becomes diffraction limited.

## Reading
- **Core:** [Geary Ch. 10, pp. 103–116] — Seidel $W_{040}$ from a paraxial trace and the thin-lens structural coefficient $\sigma_I$; read §10.1–10.6, skim the derivation in §10.7.
- **Core:** [Geary Ch. 11, pp. 117–134] — bending, focus shift, and balancing spherical aberration against defocus (§11.3–11.6 are the heart of this lesson).
- **Core:** [Kidger §7.1–7.3.1, pp. 139–152] — shape and conjugate factors, thin-lens Seidel formulas, minimum-spherical bending and the effect of refractive index and conjugates.
- **Core:** [Kidger §6.2.1, pp. 102–107] — spherical aberration of a single surface; the zero conditions.
- **Core:** [Kidger §4.4.3.1, pp. 82–83] — balancing fifth-order spherical with third-order and defocus.
- **Optional:** [Kidger §6.5, pp. 122–126] — the aplanatic surface (revisited in L08).

---

## 1. Physics: why a sphere is the wrong shape

A spherical surface is easy to make (two spheres in rubbing contact wear each other into spheres — that's why 95% of glass optics are spherical), but it is not the shape that focuses a plane wave perfectly. For a refracting surface the ideal shape is a Cartesian oval (a conic for object at infinity); for a mirror it's a paraboloid. Compared with that ideal shape, a convex sphere is "too steep at the edge": rays far from the axis meet the surface at larger angles of incidence and, because Snell's law is $n\sin I = n'\sin I'$ and not $nI = n'I'$, they are bent *more* than the paraxial approximation predicts. A positive lens therefore brings marginal rays to a focus *closer* to the lens than paraxial rays: **undercorrected spherical aberration**, $S_I > 0$.

The deviation of $\sin I$ from $I$ is $I^3/6$, so the extra bending grows as the cube of the ray height: transverse error $\propto \rho^3$, wavefront error $\propto\rho^4$. That's $W_{040}$.

### 1.1 The single surface and its zero conditions
From L01, the surface contribution is

$$
S_I = -A^2\,y\,\Delta\!\left(\frac{u}{n}\right),\qquad A = n(u + yc) = n i.
$$

$S_I$ vanishes when any factor vanishes [Kidger §6.2.1, §6.6]:
1. **$y = 0$** — the surface is at an image (field lenses, L04/L13).
2. **$A = 0$** — the ray hits the surface normally: the object/image point is at the **centre of curvature** (concentric surface). No refraction, no aberration.
3. **$\Delta(u/n) = 0$**, i.e. $u'/n' = u/n$ — the **aplanatic** condition. It occurs for object distance $l = R(n+n')/n$; the surface is then free of spherical aberration *and* coma to all orders. This is how microscope objectives get to NA 0.9+ (L08).

Everything else produces spherical aberration, and the sign follows the sign of $y\,\Delta(u/n)$: in a positive lens both surfaces usually contribute positive $S_I$; a negative lens contributes negative $S_I$. **Correction of spherical aberration therefore requires either negative elements, aspheres, or aplanatic/concentric surfaces.** Kidger notes that with low-index glass you need four positive BK7 lenses to cancel spherical aberration without any negative element [Kidger §7.3.1.4, p. 151] — in practice, designers combine positive and negative lenses (L06).

### 1.2 How big is it, and how does it scale?
For a thin lens of power $K = 1/f$ at the stop, with marginal-ray height $h$ (Kidger's notation; $h = y$ = EPD/2):

$$
S_I = \frac{h^4K^3}{4}\left[\left(\frac{n}{n-1}\right)^2 + \frac{n+2}{n(n-1)^2}\left(B + \frac{2(n^2-1)}{n+2}C\right)^2 - \frac{n}{n+2}C^2\right]
\qquad\text{[Kidger Eq. 7.5]}
$$

with the **shape factor** and **conjugate factor**

$$
B = \frac{c_1 + c_2}{c_1 - c_2},\qquad C = \frac{u_1 + u_2'}{u_1 - u_2'} = \frac{m+1}{m-1},
$$

where $c_1, c_2$ are the two curvatures, $u_1$ the marginal-ray slope entering, $u_2'$ leaving, $m$ the transverse magnification. $B = +1$: plano-convex with the curved side facing the object; $B = 0$: equiconvex; $B=-1$: convex-plano with the flat side facing the object. Object at infinity → $C = -1$; unit magnification ($m = -1$) → $C = 0$.

> **Notation alert.** Geary writes the same formula as $S_I = \tfrac14 y^4\Phi^3\sigma_I$, $\sigma_I = aX^2 - bXY + cY^2 + d$, with shape factor $X = B$ and "magnification factor" $Y = (1+M)/(1-M) = -C$ [Geary Eq. 10.9–10.13, Table 10.1]. For an object at infinity Geary has $Y=+1$ where Kidger has $C=-1$. The coefficients are $a = \frac{n+2}{n(n-1)^2}$, $b = \frac{4(n+1)}{n(n-1)}$, $c = \frac{3n+2}{n}$, $d = \frac{n^2}{(n-1)^2}$. Expanding Kidger's square reproduces Geary's polynomial exactly.

The prefactor $h^4K^3$ is the scaling law: at a fixed focal length, $S_I \propto h^4 \propto 1/N^4$; at a fixed F-number, $S_I \propto h^4K^3 = f/(16N^4)$ — spherical aberration *in mm* scales linearly with focal length. Since the diffraction blur at fixed $N$ doesn't scale with $f$, **long focal lengths are harder to make diffraction-limited at the same F/#.** (The reason many big telescopes are slow and why scaling a design up is not free — Course 03 L10.)

## 2. Bending for minimum spherical aberration

Changing $B$ at constant power ("bending") doesn't change the paraxial ray paths, so the rest of the system doesn't notice [Kidger §7.1, p. 139]. It does change $S_I$, which is a parabola in $B$. Setting $dS_I/dB = 0$:

$$
B_{\text{opt}} = -\frac{2(n^2-1)}{n+2}\,C
\qquad\Longrightarrow\qquad
S_{I,\min} = \frac{h^4K^3}{4}\left[\left(\frac{n}{n-1}\right)^2 - \frac{n}{n+2}C^2\right].
$$

For an object at infinity ($C=-1$): $B_{\text{opt}} = 2(n^2-1)/(n+2)$. For $n = 1.5168$ (N-BK7 at d): $B_{\text{opt}} = 0.7397$ — Geary gets the same number [Geary §11.3, p. 120].

| $n$ | $B_{\text{opt}}$ ($C=-1$) | $S_{I,\min}$ relative to $n=1.5$ |
|---|---|---|
| 1.5 | 0.71 | 1.00 |
| 1.7 | 1.02 | 0.63 |
| 2.0 | 1.50 | 0.41 |
| 3.0 | 3.20 | 0.19 |
| 4.0 (Ge) | 5.00 | 0.13 |

(Computed from the formula. Kidger's table [§7.3.1.2, p. 150] prints 2.25 for $n = 2$; the formula gives 1.50 — a nice example of why you should recompute book tables.)

Lessons:
- The best singlet for an object at infinity is **nearly plano-convex, curved side toward the collimated beam**, biconvex for $n<1.69$ and meniscus above. Plano-convex ($B=1$) is only ~7% worse than optimum at $n \approx 1.5$ — this is why catalog "best-form" lenses exist but plano-convex lenses dominate catalogs.
- **The wrong way round is 4× worse.** A plano-convex lens with the *flat* side toward infinity ($B=-1$) has ~4× the spherical aberration. Rule: "the curved side faces the collimated (or the longer conjugate) beam" — share the bending between the two surfaces.
- **High index helps.** $S_{I,\min}$ drops by 37% from $n=1.5$ to $1.7$, and by almost 8× for germanium in the LWIR.
- **Conjugates matter.** At 1:1 ($C=0$) the best shape is equiconvex. In a finite-conjugate machine-vision lens (working distances of 0.3–2 m), $C$ is close to $-1$ but not equal, and the optimum shifts slightly.
- **Splitting helps.** Two thin lenses of half power each, both bent for minimum, give roughly $2\cdot(1/2)^3 = 1/4$ of the spherical aberration [Kidger Eq. 7.29]. That's the lens-splitting trick from Course 01 L08.

## 3. Balancing spherical aberration with defocus

You can't remove $S_I$ from a singlet, but you can choose where to put the detector. Moving the reference sphere along the axis adds $W_{020}\rho^2$ (L01 §2). With $W = W_{040}\rho^4 + W_{020}\rho^2$, the transverse error is $\varepsilon \propto 4W_{040}\rho^3 + 2W_{020}\rho$ — a cubic with an added straight line, which is exactly what you see when you refocus a ray fan [Kidger §4.4.3.1; Geary §11.6].

Let LSA $= S_I/(2u'^2)$ be the paraxial-to-marginal focus distance (L01). Expressed as a fraction $k$ of LSA measured from the paraxial focus toward the marginal focus:

| Criterion | $W_{020}$ | Focus position $k$ | Residual |
|---|---|---|---|
| paraxial focus | 0 | 0 | P–V $W = W_{040}$, RMS $= 0.298\,W_{040}$ |
| **min RMS wavefront** (≈ max Strehl for small aberrations) | $-W_{040}$ | 1/2 | P–V $= W_{040}/4$, RMS $= W_{040}/(6\sqrt5) = 0.0745\,W_{040}$ |
| **min RMS spot radius** (geometric) | $-\tfrac43 W_{040}$ | 2/3 | RMS spot $= \tfrac13$ of paraxial RMS spot |
| **min blur circle** ("circle of least confusion") | $-\tfrac32 W_{040}$ | 3/4 | blur radius $= |\text{TSA}|/4$ |
| marginal focus | $-2W_{040}$ | 1 | |

(Each row checked by direct minimisation; Geary derives the 3/2 result from the caustic [Geary §11.6–11.7, pp. 123–125].) The defocus that corresponds to a given $W_{020}$ is $\delta z = 8N^2 W_{020}$ in magnitude for an object at infinity in air [Geary Eq. 11.15].

The practical meaning: **"best focus" depends on the criterion**, and the three positions differ by a quarter of the LSA. Kidger warns that the circle of least confusion "does not correspond to any useful criterion of image quality" [Kidger §4.4.2.1, p. 76]. For machine vision you usually care about MTF at a specific frequency, which typically lands near (but not exactly at) the minimum RMS-wavefront focus for well-corrected lenses, and nearer the min-RMS-spot focus for heavily aberrated ones. OpticStudio's **Quick Focus** lets you choose the criterion (RMS spot radius/x/y, or wavefront) — try them all in Task 3.

## 4. Higher-order spherical and zonal aberration

A real lens has $W = W_{040}\rho^4 + W_{060}\rho^6 + \ldots$ Fifth-order spherical $W_{060}$ is usually of opposite sign to the corrected third-order in a well-designed fast lens, and it can't be removed by bending once the third order has been used up [Kidger §4.4.3.1]. The designer's move is to **balance**: deliberately leave some third-order of opposite sign, and refocus. The RMS-optimal balance for a given $W_{060}$ is

$$
W_{040} = -\tfrac32 W_{060},\qquad W_{020} = +0.6\,W_{060},\qquad \sigma = \frac{W_{060}}{20\sqrt7} = 0.0189\,W_{060},
$$

which is the Fringe Zernike $Z_{16} = 20\rho^6 - 30\rho^4 + 12\rho^2 - 1$ pattern. With $W_{040} = -\tfrac32W_{060}$, the *marginal* ray is also exactly corrected ($\partial W/\partial\rho = 0$ at $\rho=1$ ignoring defocus), and the residual longitudinal aberration is largest at the **0.707 zone**: the classic "zonal spherical aberration" curve on the Longitudinal Aberration plot, which bulges out between axis and edge and comes back to zero at the edge. When you see that curve, the designer has done exactly this balance. Why this matters for tolerancing: a design that relies on balancing two large opposite terms is sensitive — small radius or thickness errors break the balance (Course 06 L04).

## 5. Singlets, F-number and the diffraction limit

Using the thin-lens result, a best-form N-BK7 singlet with $f=100$ mm at F/5 has $W_{040} \approx 4.3$ waves (worked example below). After optimal refocus the RMS wavefront is $0.0745 \times 4.35 \approx 0.32$ waves — Strehl ~0.02, far from diffraction-limited. The Maréchal criterion (RMS ≤ λ/14 ≈ 0.071 wave, Course 03 L03) needs $W_{040} \le 0.94$ wave. Since $W_{040} \propto 1/N^4$ at fixed $f$, the singlet becomes diffraction-limited on axis at about

$$
N \approx 5\left(\frac{4.35}{0.94}\right)^{1/4} \approx 7.3 .
$$

That's a useful rule: **a 100 mm best-form crown singlet is diffraction-limited on axis (monochromatically) at about F/7 or slower** (and the threshold F/# grows as $f^{1/4}$). Chromatic aberration is a different story (L06). For an 850 nm structured-light or laser application, the same lens has $\approx 4.30 \times 587.6/850 \approx 3.0$ waves at F/5 — slightly better in waves (the index of BK7 also drops a little in the NIR, which pushes the other way only slightly).

## 6. In OpticStudio

**Setting up a bending study.**
1. *System Explorer → Aperture:* Entrance Pupil Diameter (or Image Space F/#). *Fields:* on-axis only for now. *Wavelengths:* d (0.5876 µm) only for monochromatic work.
2. *Lens Data Editor:* surface 1 = STOP (put the stop on the front surface for a thin lens "at the stop"), radius R1, thickness = centre thickness, material N-BK7; surface 2 radius R2, thickness with a **Marginal Ray Height** solve (height 0) to put the image at paraxial focus.
3. To bend at constant power: make R1 a variable and give R2 an **F/# solve** (Geary's "F-solve", Course 01 L07) — it adjusts the last curvature to hold the paraxial F/# and hence the EFL. Alternatively, vary both curvatures and add **EFFL** with a target in the Merit Function.
4. To scan $B$ manually: use **Quick Adjust** or simply type a series of R1 values and log the Seidel SPHA sum. For an automated scan use the **Universal Plot** (1D, X = surface 1 curvature, Y = a merit operand such as SPHA or an RMS spot operand). (Universal Plot location: Analyze tab → Universal Plot; varies by version.)

**Reading the result.**
- **Seidel Coefficients:** SPHA (S1) per surface and the sum; W040 in waves. In a bending scan, watch how S1 moves from surface 2 to surface 1 as the lens is bent.
- **Ray Fan:** cubic. Its slope at the origin tells you where you are focused (zero slope = paraxial focus).
- **OPD Fan:** quartic at paraxial focus; after Quick Focus (wavefront criterion) it becomes the "W"-shaped $\rho^4-\rho^2$ curve with P–V ≈ $W_{040}/4$.
- **Longitudinal Aberration:** marginal-focus position vs pupil zone — parabola for pure third order, zonal bulge if fifth order is balanced.
- **Spot Diagram:** compare RMS radius at paraxial focus vs after Quick Focus; ratio ~3 for pure third-order spherical.

**Merit-function operands useful here:** SPHA (Seidel spherical of a surface or, with surface 0, the sum — check units against the Seidel report), EFFL (effective focal length), TRAY/TRAX (real transverse ray aberration for a specified pupil/field coordinate), OPDC (OPD relative to chief ray), ZERN (Zernike coefficient). The default merit function (RMS spot or wavefront, centroid/chief) already captures spherical aberration; SPHA is mainly for *guiding* a pre-design toward a desired Seidel balance.

**Pitfalls.**
- A marginal-ray height solve puts you at **paraxial** focus, which is not best focus. Either add a variable image-surface thickness (or a dummy surface) and include it in the optimization, or run Quick Focus — but never compare designs "at paraxial focus" if they'll be used at best focus.
- Thickness matters: the thin-lens $B_{\text{opt}}$ is close to but not exactly the thick-lens optimum (Worked example).
- Seidel W040 is third-order only. Compare its prediction for TSA with the real Ray Fan; the difference is the higher-order content.

## Worked example — best-form N-BK7 singlet, f = 100 mm, F/5

**Given:** N-BK7, $n_d = 1.5168$, $f = 100$ mm, EPD = 20 mm ($h = 10$ mm, $u' = -0.1$), object at infinity ($C = -1$), λ = 587.6 nm.

**Thin lens.** $K = 0.01$ mm⁻¹. Prefactor $h^4K^3/4 = 10^4\cdot10^{-6}/4 = 0.0025$ mm.
$(n/(n-1))^2 = (1.5168/0.5168)^2 = 8.614$; $(n+2)/(n(n-1)^2) = 3.5168/(1.5168\cdot0.26708) = 8.681$ (Geary's $a$); $n/(n+2) = 0.4313$.

$B_{\text{opt}} = 2(n^2-1)/(n+2) = 2(1.30068)/3.5168 = 0.7397$.

$S_{I,\min} = 0.0025\,(8.614 - 0.4313) = 0.02046$ mm → $W_{040} = 0.02046/8 = 0.002557$ mm $= 4.35$ waves.

Curvatures: $c_1 - c_2 = K/(n-1) = 0.019350$ mm⁻¹; $c_1 = 0.019350(B+1)/2$, $c_2 = 0.019350(B-1)/2$ →

| Shape | $B$ | R1 (mm) | R2 (mm) | $S_I$ (mm) | $W_{040}$ (waves) | TSA = $S_I/(2u')$ (mm) | LSA (mm) |
|---|---|---|---|---|---|---|---|
| convex-plano, flat side first | −1 | ∞ | −51.68 | 0.0861 | 18.3 | −0.431 | 4.31 |
| equiconvex | 0 | 103.36 | −103.36 | 0.0323 | 6.88 | −0.162 | 1.62 |
| **best form** | **0.740** | **59.41** | **−397.1** | **0.02046** | **4.35** | **−0.102** | **1.02** |
| plano-convex, curved side first | 1 | 51.68 | ∞ | 0.02193 | 4.66 | −0.110 | 1.10 |

**Thick lens check (centre thickness 4 mm, EFL held at 100 mm, image at paraxial focus).** Computing exact paraxial Seidel sums with `seidel.py`: the minimum moves slightly to $B \approx 0.727$ (R1 ≈ 59.6, R2 ≈ −378 mm), $S_I = 0.02023$ mm, $W_{040} = 4.30$ waves. For $B = 0.74$, a real (exact) marginal ray lands at $-0.1038$ mm vs the Seidel prediction $-0.1012$ mm — third order is accurate to ~3% at F/5. At $B=-1$ the real error is −0.454 mm vs −0.431 Seidel (5% higher-order).

**Refocusing** the thick best-form lens ($S_I = 0.02023$): LSA = 1.012 mm. Best RMS-wavefront focus is 0.506 mm inside paraxial focus, min-RMS-spot focus 0.675 mm, least-confusion 0.759 mm. RMS spot radius drops from 50.6 µm (paraxial) to 16.9 µm (best). Diffraction-limited only at ~F/7.3 (§5).

## Key takeaways
- Spherical aberration arises because $\sin I \ne I$; a positive spherical surface is undercorrected ($S_I>0$). Zero only for $y=0$, concentric ($A=0$) or aplanatic ($\Delta(u/n)=0$) surfaces.
- Thin-lens $S_I$ is a parabola in shape factor $B$; minimum at $B_{\text{opt}} = -2(n^2-1)C/(n+2)$ (≈ 0.74 for BK7 at infinity). Plano-convex, curved side to the long conjugate, is within ~7%.
- $S_I \propto h^4K^3$: at fixed F/#, spherical in mm grows with $f$. Higher index, splitting and negative elements reduce it.
- Best focus is criterion-dependent: ½ (RMS wavefront), ⅔ (RMS spot), ¾ (blur circle) of the LSA from paraxial focus.
- Fifth-order spherical is balanced with $W_{040} = -1.5W_{060}$, leaving a 0.707-zone residual — balanced designs are tolerance-sensitive.
- A 100 mm best-form singlet is monochromatically diffraction-limited on axis only at ≈ F/7 or slower.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Undercorrected / overcorrected SA | Marginal focus closer to / farther from the lens than paraxial focus ($S_I>0$ / $<0$) |
| Shape factor $B$ (Geary $X$) | $(c_1+c_2)/(c_1-c_2)$; describes the bending of a lens at fixed power |
| Conjugate factor $C$ (Geary $Y=-C$) | $(u_1+u_2')/(u_1-u_2') = (m+1)/(m-1)$; −1 for object at infinity |
| Bending | Changing the shape at constant power; leaves paraxial rays unchanged |
| Best form | Bending that minimises spherical aberration |
| LSA / TSA | Longitudinal / transverse spherical aberration of the marginal ray |
| Aberration balancing | Deliberately combining terms (defocus, third and fifth order) to minimise a quality metric |
| Zonal aberration | Residual at an intermediate zone (typ. 0.707) after the marginal ray is corrected |
| Aplanatic surface | Surface with $\Delta(u/n)=0$: free of spherical aberration and coma |

## References
1. [Geary] Ch. 10 "Spherical Aberration", pp. 103–116 (esp. §10.3–10.5, Table 10.1 p. 111); Ch. 11 "Lens Bending and Aberration Balancing", pp. 117–134 (§11.3 p. 119–120; §11.4–11.6 pp. 120–124; §11.7 p. 124–125).
2. [Kidger] §4.4.2.1 pp. 74–76; §4.4.3.1 pp. 82–83; §6.2.1 pp. 102–107; §6.5–6.6 pp. 122–127; §7.1–7.3.1 pp. 139–152.
3. J. Sasián, OPTI 517 "Aberration coefficients" lecture notes, Univ. of Arizona — <https://wp.optics.arizona.edu/jsasian/wp-content/uploads/sites/33/2016/02/L4-OPTI-517-Aberration-Coefficients.pdf>
