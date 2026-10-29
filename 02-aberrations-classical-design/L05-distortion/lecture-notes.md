# L05 — Distortion

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~2.5 h, tasks ~4 h
> **Prerequisites:** [L01](../L01-wavefront-and-transverse-aberrations/), [L03 (stop shift)](../L03-coma-astigmatism-and-symmetry/), [L04](../L04-field-curvature-petzval-flatteners/) · **Next:** [L06 — Chromatic aberration and achromats](../L06-chromatic-aberration-and-achromats/)

## Learning objectives
- Define distortion for finite, infinite and afocal conjugates, compute percent distortion from real and paraxial chief rays, and name barrel vs pincushion correctly.
- Relate third-order distortion to $S_V$ and $W_{311}$ ($D = S_V/(2H)$) and compute $S_V$ with the formula that survives $A = 0$.
- Predict how distortion changes with stop position (stop-shift equation) and explain why symmetric lenses are distortion-free at 1:1.
- Compare image-height mappings (f·tanθ, f·θ, equisolid, stereographic, orthographic) and explain why scanners need f-θ and fisheyes don't fight their barrel distortion.
- Use OpticStudio's Field Curvature/Distortion and Grid Distortion analyses and distortion operands (DIMX, DISG) correctly, including the "calibrated" vs. paraxial reference.
- Connect lens-design distortion to the radial distortion coefficients used in camera calibration ($k_1, k_2, \ldots$), and state what a machine-vision customer actually needs.

## Reading
- **Core:** [Geary Ch. 15, pp. 167–173] — wavefront tilt, distortion as field-dependent tilt, worked example (400 mm F/10 lens) reproduced in this lesson.
- **Core:** [Kidger §4.4.2.4, pp. 79–82] — definitions for finite, infinite and afocal conjugates, effect of defocus and pupil aberrations, f-θ lenses, curved objects.
- **Core:** [Kidger §6.2.3, pp. 108–109] — the alternative distortion formula that avoids division by zero.
- **Core:** [Kidger §6.3.1, pp. 116–120] — stop-shift change of distortion (Eq. 6.69).
- **Optional:** [Kidger §4.4.3.4, p. 86] — balancing distortion with higher orders.
- **Optional online:** e-con Systems, "A beginner's guide to lens distortion parameters: F-Theta, F-Tan Theta and TV distortion" — practical camera-industry vocabulary: <https://www.e-consystems.com/blog/camera/tag/ftheta/amp/>

---

## 1. What distortion is (and isn't)

Distortion is a **field-dependent magnification error**: each point is imaged sharply, but at the wrong place [Geary §15.1]. In wavefront terms it is the term $W_{311}H^3\rho\cos\theta$ — a **tilt** whose size grows as $H^3$ [Geary §15.3]. A tilt of the wavefront does not blur the image (no OPD relative to the *real* chief ray), which is why distortion is invisible in the OPD fan and spot diagram and only appears when you compare the real chief-ray position with the ideal one.

### 1.1 Definitions
For a finite object and a plane image (the "natural" case), trace the real and the paraxial chief ray from the same object point [Kidger Eq. 4.20]:

$$
D = \frac{\eta'_{\text{real}} - \eta'_{\text{paraxial}}}{\eta'_{\text{paraxial}}}\times100\%.
$$

For an object at infinity at field angle $\theta$, the reference is the paraxial chief ray with slope $\tan\theta$: $\eta'_{\text{par}} = f'\tan\theta$ (an ordinary camera lens is an "**f-tan θ**" lens) [Kidger §4.4.2.4.2]. For afocal systems (binoculars, beam expanders) the natural requirement is angle-to-angle proportionality, $\theta' = m\theta$ [Kidger §4.4.2.4.3].

**Sign:** $D>0$ means real images are too far out → **pincushion**; $D<0$ → **barrel**. Third-order distortion is $\propto H^2$ when expressed as a percentage ($\delta\eta' \propto H^3$, divided by $\eta'\propto H$).

### 1.2 Third order
From L01: $W_{311} = S_V/2$, transverse error $\delta\eta' = S_V/(2n'u')$ at full field, and fractional distortion

$$
D_{3} = \frac{\delta\eta'}{\eta'} = \frac{S_V}{2H}\qquad\text{[Kidger Eq. 6.93]},
$$

with $H$ the Lagrange invariant (same sign convention as in L01; check the sign of your $H$). Geary writes the transverse version as $T = -2N\,W_{311}$ (object at infinity, $H=1$) [Geary Eq. 15.12] — the same "slope × 2N" rule you used for every other aberration.

### 1.3 Computing $S_V$ safely
The surface formula $S_V = (\bar A/A)(S_{III}+S_{IV})$ fails when $A = 0$ (marginal ray normal to the surface — e.g. a plane surface in a collimated beam, very common!). Kidger gives an equivalent form without the division [Kidger Eq. 6.37]:

$$
S_V = -\bar A^3\,y\,\Delta\!\left(\frac{1}{n^2}\right) + \bar y\,\bar A\,(2y\bar A - \bar y A)\,c\,\Delta\!\left(\frac1n\right).
$$

Use this one in your `seidel.py` (Task 1). OpticStudio of course handles it internally.

## 2. Distortion and the stop

From the stop-shift equations (L03, [Kidger Eq. 6.69]):

$$
S_V^* = S_V + \chi(3S_{III} + S_{IV}) + 3\chi^2S_{II} + \chi^3S_I .
$$

For a thin lens at the stop $S_V = 0$ (the chief ray passes through the centre undeviated). Moving the stop **in front** of a positive lens ($\chi>0$ in our convention) gives $\Delta S_V \approx \chi(3S_{III}+S_{IV}) > 0$ and with $H<0$ in our convention, $D = S_V/(2H) < 0$: **barrel**. Stop **behind** → **pincushion**. Mnemonic: for a positive lens, "front stop: barrel; rear stop: pincushion"; reverse both for a negative lens. Intuition: with a front stop, the chief ray crosses the lens off-centre, on the same side as its image point; a positive spherical lens is undercorrected (it bends rays far from its centre more than the paraxial approximation says), so the chief ray is bent toward the axis too much and the image lands inward — barrel. With a rear stop the chief ray crosses the lens on the opposite side of the axis and the same excess bending pushes the image outward — pincushion.

**Symmetry kills distortion.** A system symmetric about the stop at $m = -1$ has $S_V = 0$ to all orders (L03): the barrel of the front half cancels the pincushion of the rear half. This is why the periscopic lens, the Rapid Rectilinear ("rectilinear" = straight lines stay straight) and later symmetric anastigmats were invented — the photographers of the 1860s were tired of bent architecture. Near-symmetric designs remain the go-to choice when you need low distortion at moderate field angles; extremely low distortion at high field angles (aerial mapping, lithography) requires many elements and careful higher-order balancing.

**Wide-angle lenses.** Retrofocus and fisheye lenses have a strong negative front group (stop well behind it), so they naturally produce **barrel** distortion; correcting it to near zero at 60°+ half-field is expensive and often not wanted (§3).

## 3. Mapping functions: choosing the "right" distortion

"Zero distortion" means the image obeys the rectilinear mapping $\eta' = f\tan\theta$. Other mappings are often more useful:

| Mapping | Image height | Used for | Distortion vs f·tanθ at 20° / 45° / 60° |
|---|---|---|---|
| Rectilinear | $f\tan\theta$ | normal cameras, metrology | 0 |
| **f-θ (equidistant)** | $f\theta$ | laser scanners (galvo), many fisheyes | −4.1% / −21.5% / −39.5% |
| Equisolid angle | $2f\sin(\theta/2)$ | fisheyes (equal-area) | −4.6% / −23.5% / −42.3% |
| Stereographic | $2f\tan(\theta/2)$ | some fisheyes (conformal) | −3.1% / −17.2% / −33.3% |
| Orthographic | $f\sin\theta$ | rarely for imaging (shown for completeness) | −6.0% / −29.3% / −50.0% |

(Percentages computed from the formulas.) An **f-θ lens** is required for laser scanning: a galvo mirror rotating at constant angular speed must move the spot at constant linear speed on the work surface [Kidger §4.4.2.4.5]. Relative to f·tanθ, the f-θ mapping is about $-\tan^2\theta/3$ of "barrel" at small angles — i.e. a scan lens is a lens *designed* with a specific amount of third-order barrel distortion.

For a wide-angle machine-vision lens, the rectilinear mapping wastes pixels at the edge (the image of a constant angular increment grows as $\sec^2\theta$) and makes the lens hard to build; a controlled, smooth barrel distortion is often the better engineering choice — it's removed in software anyway.

## 4. Distortion and camera calibration (the Zivid angle)

In machine vision and 3D cameras, distortion is **measured and removed by calibration**. The standard radial model (Brown–Conrady, used by OpenCV and most calibration toolboxes) writes the distorted normalized image coordinates as

$$
x_d = x\,(1 + k_1r^2 + k_2r^4 + k_3r^6) + \ldots,\qquad r^2 = x^2+y^2,\quad x = X/Z,\ y = Y/Z
$$

(plus tangential terms $p_1, p_2$ for decentering). Comparing with lens design: the fractional distortion at normalized radius $r = \tan\theta$ is $D(r) = k_1r^2 + k_2r^4 + \ldots$ So **third-order (Seidel) distortion is exactly $k_1$**: $k_1 \approx D_{\max}/\tan^2\theta_{\max}$ for a lens dominated by third order. Fifth-order distortion maps to $k_2$, etc.

What the calibration engineer cares about, and therefore what you should specify and design for:
1. **Smoothness/low order.** A distortion curve that's monotonic and well described by 2–3 coefficients calibrates robustly. A "wavy" curve (strong high-order balancing, often a by-product of pushing the *maximum* distortion to zero) needs more parameters and degrades calibration accuracy at the field edge. Specify "distortion < x% *and* well fit by a k1, k2 model", not just "< 0.1%".
2. **Stability.** Calibration removes the distortion you had at calibration time. Changes with **focus** (distortion depends on image distance unless the lens is image-space telecentric — [Kidger §4.4.2.4.4]; Course 04 L06), **temperature** (Course 03 L09), **wavelength** (lateral colour = wavelength-dependent magnification, L06) and mechanical shifts are what actually hurt 3D accuracy.
3. **Decentering/tilt** in manufacturing produces asymmetric distortion (the $p_1, p_2$ terms) — a tolerancing issue (Course 06).
4. **Projectors too.** In a structured-light system the projector lens's distortion warps the projected pattern; it is calibrated like a camera (an "inverse camera"), with the same smoothness and stability requirements.

## 5. In OpticStudio

- **Field Curvature/Distortion** (*Analyze → Aberrations → Field Curvature and Distortion*; location varies by version): right panel = percent distortion vs field. Its settings let you choose the **distortion reference**: F-Tan(θ) (the standard rectilinear definition), F-θ, and "calibrated" variants that use a best-fit focal length instead of the paraxial one (exact option names vary by version — check the settings dialog). Use F-θ when designing scan lenses; use a calibrated reference when only the *shape* of the distortion matters (machine vision).
- **Grid Distortion** (*Analyze → Aberrations → Grid Distortion*): shows the distorted image of a square grid vs. the ideal grid and reports maximum distortion and "keystone"/"smile" information — the analysis to use for anamorphic, tilted or decentred systems where radial distortion is not enough.
- **Seidel Coefficients:** DIST (S5) per surface — find the surfaces that create the distortion (usually those far from the stop where the chief ray is high).
- **Operands:** **DIMX** (maximum distortion in percent over the field — handy as a constraint), **DISG** (generalised distortion at a specified field/pupil coordinate, in percent), and the Seidel-based **DIST** (Geary's ZEMAX version returned the percent value [Geary §15.4, Fig. 15.10]; check the current Help for its definition before using it). Real-ray chief-ray positions via **REAY** combined with paraxial **PARY** give fully custom distortion definitions.
- **Pitfalls:**
  - Distortion is measured relative to the **paraxial** chief ray of the *primary wavelength* — check which wavelength is primary.
  - For wide-angle or fast lenses turn on **Ray Aiming** (System Explorer → Ray Aiming: Paraxial or Real) so that real chief rays actually pass through the centre of the stop; pupil aberrations otherwise corrupt the distortion values [Kidger §4.4.2.4.4].
  - Distortion values depend on where the image plane is if the exit pupil is not at infinity (non-telecentric).
  - Don't confuse distortion with **keystone** from a tilted object plane — that's geometry, not an aberration [Kidger §4.4.2.4.2].

## Worked example — Geary's 400 mm F/10 lens

**Given** [Geary §15.4, pp. 171–172]: N-BK7 singlet ($n_d = 1.5168$), R1 = 799.31 mm, R2 = −277.42 mm, thickness 12 mm; stop 151.56 mm **in front** of the lens; EFL ≈ 400 mm, F/10 (EPD 40 mm); field 5°; λ = 587.6 nm.

**Seidel sums** (our `seidel.py`): $S_I = 0.01316$, $S_{II} = -0.00003$ (the stop is at the coma-free position — this is a landscape lens), $S_{III} = 0.00123$, $S_{IV} = 0.00507$, $S_V = 0.01040$ mm. $H = -\bar u y = -\tan5°\times20 = -1.750$ mm.

- $W_{311} = S_V/2 = 0.00520$ mm $= 8.85$ waves (Geary: 8.86).
- Transverse: $\delta\eta' = S_V/(2n'u') = 0.01040/(2\times(-0.05)) = -0.104$ mm (Geary: −2N·W311 = −104 µm).
- Percent: $D = S_V/(2H) = 0.01040/(-3.4997) = -0.297\%$ — **barrel**, as expected for a front stop.
- **Real rays** (exact trace): real chief ray at 34.893 mm, paraxial at 34.997 mm → $\delta\eta' = -0.1038$ mm, $D = -0.297\%$. Geary's ZEMAX listing gives −0.1032 mm and −0.296%. Third order is essentially exact at 5°.

**Stop position experiment** (EPD fixed at 40 mm, third order):

| Stop | $S_{II}$ | $S_V$ | $D$ |
|---|---|---|---|
| 151.56 mm in front | −0.00003 | +0.01040 | **−0.30%** (barrel) |
| at the lens | −0.00875 | +0.00073 | −0.02% |
| 151.56 mm behind | −0.02344 | −0.07957 | **+2.27%** (pincushion) |

The lens itself is unchanged; only the chief-ray path differs. (The rear-stop case also has large coma — moving the stop away from the natural position costs image quality.)

## Key takeaways
- Distortion is a field-dependent wavefront tilt ($W_{311}H^3\rho\cos\theta$): sharp images in the wrong place; $D_3 = S_V/(2H) \propto H^2$.
- $D>0$ pincushion, $D<0$ barrel; positive lens with front stop → barrel, rear stop → pincushion; symmetric at 1:1 → zero.
- Use Kidger's alternative $S_V$ formula when $A=0$.
- "Zero distortion" depends on the mapping: f·tanθ for cameras, f·θ for scanners, equisolid/stereographic for fisheyes.
- For calibrated machine vision, smooth low-order and *stable* distortion beats minimal but wavy distortion; Seidel distortion ≈ calibration $k_1$.
- In OpticStudio check the distortion reference (paraxial vs calibrated, F-tanθ vs F-θ) and enable ray aiming for wide fields.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Distortion $D$ | $(\eta'_{\text{real}} - \eta'_{\text{ref}})/\eta'_{\text{ref}}$ of the chief-ray image height |
| Barrel / pincushion | $D<0$ / $D>0$; straight lines bow outward / inward at the edges |
| Rectilinear (f·tanθ) | Distortion-free mapping for a plane object |
| f-θ lens | Lens with $\eta' = f\theta$, for constant-speed laser scanning |
| Equisolid / stereographic / orthographic | Fisheye mappings $2f\sin(\theta/2)$, $2f\tan(\theta/2)$, $f\sin\theta$ |
| Calibrated distortion | Distortion relative to a best-fit (not paraxial) focal length |
| Grid distortion | 2D map of real vs ideal positions of a grid of field points |
| $k_1, k_2, k_3$ | Radial distortion coefficients of the Brown–Conrady calibration model |
| Keystone | Trapezoidal image of a tilted object plane (geometry, not aberration) |

## References
1. [Geary] Ch. 15 "Distortion", pp. 167–173 (§15.2 wavefront tilt p. 167–169; §15.4 example pp. 171–172); Ch. 12 (symmetry) pp. 135–145.
2. [Kidger] §4.4.2.4 pp. 79–82; §4.4.3.4 p. 86; §6.2.3 pp. 108–109; §6.3.1 pp. 116–120; §6.9.2 Eq. 6.93 p. 131; §7.7.2 pp. 165–166.
3. e-con Systems blog, "A beginner's guide to lens distortion parameters: F-Theta, F-Tan Theta and TV distortion" — <https://www.e-consystems.com/blog/camera/tag/ftheta/amp/>
4. Avantier case study, "Distortion correction with F-theta lens" — application context for scan lenses: <https://avantierinc.com/resources/case-study/case-study-distortion-correction-with-f-theta-lens/>
