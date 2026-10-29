# L13 — Eyepieces, afocal systems, field lenses, relays and windows

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~5–6 h
> **Prerequisites:** [Course 01 L04 (stops, pupils, Lagrange invariant)](../../01-foundations/L04-stops-pupils-fields/), [L08 (Seidel)](../L08-seidel-surface-contributions/), [L10 (symmetry)](../L10-symmetric-lenses-double-gauss-vignetting/), [L11 (field flatteners)](../L11-petzval-and-telephoto/) · **Next:** Course 03 — [L01 Diffraction and the PSF](../../03-image-quality-optimization/L01-diffraction-and-the-psf/)

## Learning objectives
- Compute the first-order layout of a Keplerian and a Galilean afocal system: angular magnification, exit-pupil size and position (eye relief), and field angles in object and eye space.
- Explain the role of a field lens (redirecting the chief ray without changing the marginal ray) and size one for an eyepiece or a relay train.
- Describe the classic eyepiece family (Ramsden, Kellner, Plössl, Erfle) and why eyepieces cannot exploit the symmetry principle; design one "in reverse".
- Compute the focus shift and the Seidel aberrations of a plane-parallel plate in a converging beam, including a tilted plate's astigmatism, and decide when a window, filter or cover glass must be part of the design.
- Use OpticStudio's **Afocal Image Space** mode, angular aberration units, the **Paraxial** surface (ideal lens / model eye), `AMAG`, and coordinate breaks for tilted plates.

## Reading
- **Core:** [Kidger Ch. 11, pp. 209–229] — eyepiece specifications (focal length, field, pupil, eye relief, prisms, pupil spherical aberration, distortion, Petzval), Ramsden/Kellner/Plössl/Erfle with Seidel sums, design of a complete binocular telescope with angular aberration plots, Galilean telescopes, biocular magnifiers.
- **Core:** [Geary Ch. 22, pp. 239–247] — first-order eyepiece layout for a 400 mm F/10 telescope, the field lens (§22.4), Ramsden and Kellner (§22.5), Paraxial-surface eye model (§22.6), Ramsden design in reverse with `AMAG` (§22.7).
- **Core:** [Geary Ch. 23, pp. 249–259] — field lenses in relay systems (periscope), windows: wavefront quality, focus shift (§23.4.1), Seidel spherical of a perfect window (§23.4.2), simple window Seidel formulas (§23.4.3), tilted windows with coordinate breaks (§23.5), effect on axial colour (§23.6).
- **Optional:** [Kenyon Ch. 4] — optical instruments (magnifier, microscope, telescope) from the physics side.
- **Online:** Ansys Optics KB on designing afocal systems with *Afocal Image Space* (beam expander and cylinder-lens examples): <https://optics.ansys.com/hc/en-us/articles/42661707601683>; community thread on angular spot-diagram units in afocal mode: <https://community.zemax.com/got-a-question-7/angular-spot-diagram-units-afocal-image-space-935>

---

## 1. Afocal systems

An **afocal** system takes a collimated beam in and gives a collimated beam out: object and image at infinity, total power zero. The two-lens versions:

- **Keplerian** (astronomical) telescope: positive objective $f_o$, positive eyepiece $f_e$, separation $f_o + f_e$, real intermediate image (where a field stop or reticle can sit), inverted output.
- **Galilean**: positive objective, negative eye lens, separation $f_o - |f_e|$, no real intermediate image, upright output, shorter.

**Angular magnification.** $M = \tan\theta'/\tan\theta = -f_o/f_e$ (Keplerian: $M<0$, image inverted). Because the Lagrange invariant is conserved, $H = n\,y_{\text{pupil}}\tan\theta$ is the same in object and eye space, so the beam diameter shrinks by $|M|$:

$$
D_{\text{exit pupil}} = \frac{D_{\text{entrance pupil}}}{|M|},\qquad \tan\theta' = M\tan\theta .
$$

Example [Kidger p. 210]: 8×30 binoculars have a 30/8 = 3.75 mm exit pupil. Practical eye-side constraints [Kidger §11.1]: eye pupil 3–7 mm, eye relief ~20 mm (more for spectacle wearers), eye-space semi-field 20–30° (larger is hard), eyepiece focal lengths ~25 mm.

**Exit pupil and eye relief.** With the stop at the objective, the eyepiece images the objective to the exit pupil at distance $l' = f_e(1 + f_e/f_o)$ behind the eyepiece (thin lenses). Geary's 400 mm F/10 objective with a 4 mm iris gives $f_e = 40$ mm ($M = 10$) and $l' = 44$ mm [Geary §22.2].

**Beam expanders** are afocal systems used backwards: a laser beam enters the "eyepiece" and leaves the objective $|M|$ times wider and $|M|$ times less divergent. The Galilean form (no internal focus — no air breakdown with high-power lasers) is preferred for high power. For a Zivid-type projector, an afocal expander/anamorphic pair can shape a laser or VCSEL beam before a DOE (Course 05 L08).

**Which aberrations are measured how?** In an afocal system the image is at infinity, so ray errors are **angles** (ray angle minus chief-ray angle, in radians or arc-minutes), and the wavefront is referenced to a *plane*, not a sphere [Kidger p. 221; Ansys KB]. Defocus becomes **vergence** in dioptres: Kidger's simple binocular has ~0.002 rad of marginal-ray angular error over a 2 mm pupil radius, i.e. rays diverging from ~1 m in front of the eye = 1 dioptre of deliberate defocus to balance field curvature [p. 221].

## 2. Field lenses

A **field lens** sits at (or near) an intermediate image. There the marginal ray height is ~0, so the lens hardly changes the axial beam ($u' = u - hK$ with $h = 0$) — but the chief ray passes at full field height, so it is bent strongly [Geary §22.4]. A field lens therefore:

- **steers the off-axis beams** into the next element's aperture, reducing vignetting and the size of downstream optics (Geary's ±1° → ±2° example: the field lens doubles in diameter but the eye lens grows only modestly);
- **relocates the pupil**: by choosing its power you image the objective's aperture onto the next relay lens (relay trains) or set the eye relief (eyepieces) [Geary Fig. 22.7: $R = -25$ mm puts the beam crossing behind the eye lens; flatter radii push the eye point further out];
- adds almost no spherical aberration, coma or axial colour (the L08 "$h=0$" zero condition), but **does add Petzval** ($S_{IV} = H^2K/n$ regardless of $h$) and some distortion and lateral colour.

Sizing: to image a pupil at distance $a$ before the field lens onto a lens at distance $b$ after it, $1/f_{FL} = 1/a + 1/b$ (thin lens, both distances positive here). Because dust and scratches on a field lens at the image are in focus, real field lenses sit slightly away from the image (Kidger §6.6; L11).

## 3. Relays

A **relay** re-images an intermediate image with (usually) unit magnification — periscopes, endoscopes, rifle scopes (erecting relay), and illumination/projection trains [Geary §23.2]. Typical forms:

- **4f relay:** two identical lenses of focal length $f$ separated by $2f$, the stop midway: symmetric at $m=-1$, so coma, distortion and lateral colour cancel (L10). Each lens can be a doublet.
- **Relay train:** relay–field lens–relay–field lens… Without field lenses each relay vignettes the off-axis beam more; with a field lens at every intermediate image, the pupil is re-imaged onto every relay aperture and the illumination stays uniform (Geary Figs. 23.1–23.3, submarine periscope). Even aberrations (spherical, Petzval, axial colour) **accumulate** through the train, which is why rod-lens endoscopes use thick glass rods (higher $n$, lower NA in glass) and dedicated Petzval-correcting elements.

## 4. Eyepieces

An eyepiece works with a finite object (the intermediate image) and an image at infinity, with the **aperture stop outside the lens** (the eye pupil, or the objective imaged there) [Kidger §11.1]. Two consequences:

1. **No symmetry principle.** The stop is external, so odd aberrations (coma, distortion, lateral colour) are not cancelled automatically and must be fought element by element.
2. **Large field, small aperture.** Eye-space semi-fields of 20–30° at ~F/7–F/10 make astigmatism, Petzval, lateral colour and distortion the main problems; spherical aberration is minor (but **pupil spherical aberration** matters — if beams from different field points don't overlap at the eye, the user sees "kidney-bean" blackouts).

**Design in reverse.** Trace from the eye pupil (now the entrance pupil, collimated input at the eye-space field angles) to the intermediate image, so the merit function deals with a finite image [Kidger Fig. 11.2; Geary §22.7]. Then reverse it (OpticStudio has a reverse-elements tool in the Lens Data Editor; location varies by version) or, better, put objective and eyepiece together in afocal mode.

| Eyepiece | Construction | Typical semi-field | Notes (Kidger §11.2) |
|---|---|---|---|
| Ramsden | two plano-convex singlets, curved sides facing | ~15° | cheap; lateral colour, spherical, Petzval uncorrectable; reticle possible |
| Kellner | Ramsden with achromatized eye lens | ~20° | eye relief short (9.4 mm in Kidger's example) |
| Plössl (symmetric) | two cemented doublets | ~20° | much better; Petzval balanced by astigmatism |
| Erfle | 3 groups (with a concave surface near the image) | ~30° | longer eye relief, lower Petzval; lateral colour left for the prism |

**Petzval in eyepieces.** All simple eyepieces are positive, so Petzval is positive and uncorrectable. Unlike a camera lens, a visual system should *not* trade it for astigmatism, because the eye can accommodate for defocus (curvature) but not for astigmatism [Kidger p. 212]. One dioptre of residual field curvature/astigmatism over most of the field is generally acceptable [p. 220].

**Distortion.** Afocal visual systems are better designed so that object- and eye-space chief-ray angles are proportional ($\theta' \propto \theta$, like an f-θ lens) rather than $\tan\theta' \propto \tan\theta$ [Kidger p. 212].

**Same-glass achromatic separation.** Two thin lenses of the same glass separated by $d = (f_1 + f_2)/2$ have a focal length independent of wavelength (set $\partial K/\partial n = 0$ in $K = K_1 + K_2 - dK_1K_2$ with $K_i \propto n-1$). This is the classical Huygens-eyepiece rule, and the reason the Ramsden's lens spacing is tied to its colour behaviour.

## 5. Windows and plane-parallel plates

Plane plates are everywhere in real cameras: protective windows, IR-cut and bandpass filters, polarizers, the sensor cover glass, beam splitters, prisms (unfolded, a prism is a thick plate). A perfect plate in **collimated** light has no effect on image quality (only its surface flatness and homogeneity matter — Geary's interferograms show how a "window" with defocus- or astigmatism-like OPD ruins an image [§23.3]). In a **converging** beam it is a lens element with zero power but non-zero aberrations [Geary §23.4]:

**Focus shift** (paraxial):

$$
\Delta z = t\,\frac{n-1}{n}\quad(\approx t/3 \text{ for } n\approx1.5).
$$

Geary: 20 mm of BK7 behind a 100 mm F/3.3 achromat pushes focus back 6.81 mm.

**Seidel terms** of a plate (both surfaces together, in air), with marginal and chief ray slopes $u$, $\bar u$ in the beam where the plate sits:

$$
N = -\frac{t(n^2-1)}{n^3},\qquad S_I = Nu^4,\quad S_{II} = Nu^3\bar u,\quad S_{III} = Nu^2\bar u^2,\quad S_{IV} = 0,\quad S_V = Nu\bar u^3
$$

[Geary Table 23.1 and eq. 23.14, after Mahajan]. They depend on the beam *angles*, not on where the plate is — a plate anywhere in the same converging cone gives the same Seidel aberrations. $N<0$ means **overcorrected** (negative) spherical aberration: the steeper marginal rays are displaced further back than the paraxial ones. Colour: a plate also adds **axial colour** (the focus shift depends on $n(\lambda)$) — re-optimize the lens with the plate present [Geary §23.6].

**Tilted plate** (filters at an angle, beam splitters, misaligned windows). Tilting by $\theta$ is equivalent (to third order) to a chief-ray angle $\bar u = \tan\theta$ even on axis, so an *on-axis* point acquires coma and astigmatism. For a thin bundle the exact tangential–sagittal focal separation (from the Coddington equations at two plane surfaces) is

$$
\Delta_{T-S} = \frac{t\,(\sin^2\theta - \sin^2\theta_g)}{n\cos^3\theta_g},\qquad \sin\theta_g = \sin\theta/n,
$$

plus a lateral image shift $t\sin\theta\big(1 - \cos\theta/\sqrt{n^2-\sin^2\theta}\big)$. A 45° plate beam splitter in a converging beam is therefore a strong astigmatism generator — use cube splitters, or put plate splitters in collimated space, or compensate with a second plate tilted in the orthogonal plane.

**Zivid/practice angle.** The sensor cover glass and any filter between the last lens and the sensor sit in the converging beam: they must be in the design from day one (Course 04 L08). A front protective window sits in object space, where the beam from each object point is nearly collimated (object at 0.5–2 m): its focus effect is small but its *wavefront quality* (flatness, wedge, stress birefringence of plastic windows) is not — specify it with a transmitted wavefront spec. Interference filters tilted to tune or to avoid ghosts add astigmatism *and* shift their passband (angle-of-incidence blue shift).

## 6. In OpticStudio

- **Afocal Image Space:** a checkbox in System Explorer (under Aperture in current versions; the Ansys KB article also mentions the Units section — location varies by version). Image-space analyses then report **angles** (units selectable in System Explorer → Units → Afocal mode units, e.g. mrad or arc-min), OPD is referenced to a plane wave, Spot Diagram becomes an angular spot (ray angle minus chief-ray angle), and the default merit function offers an *Angular* criterion. Relative illumination is not meaningful in afocal mode. The `AFOC` multi-configuration operand can switch the mode per configuration and the `IMSF` operand can change the image surface used inside a merit function (both per the Ansys article).
- **Paraxial surface:** an ideal thin lens with a *Focal Length* parameter — use it as a perfect eye (f ≈ 17–25 mm; Geary uses 25.4 mm and lets the retina radius vary [§22.6]) or as a perfect objective/collimator to test one half of a system. It has its own OPD-mode settings; read its Help page before trusting wavefront or MTF results through it.
- **Angular magnification:** `AMAG` (Geary designs a 10× Ramsden in reverse with `AMAG` = 0.1 and `EFFL` = 40 [§22.7]).
- **Tilted plates:** sandwich the plate between two **Coordinate Break** surfaces (tilt about X, then the negative tilt to restore the axis) [Geary §23.5], or use the Tilt/Decenter tab of the surface properties; view in the 3D Viewer. Seidel analysis is invalid for tilted systems — use real-ray analyses (Spot Diagram, Field Curvature, Zernike).
- **Prisms** in sequential mode: model as an unfolded glass block of the correct path length (Kidger's binocular uses an 85 mm BK7 block) unless you need the actual reflections.

## Worked example

**(a) Telescope first order (Geary §22.2).** Objective $f_o = 400$ mm, F/10 ($D = 40$ mm), desired exit pupil 4 mm ⇒ $|M| = 10$, $f_e = 40$ mm. Eye relief (thin lens) $= f_e(1 + f_e/f_o) = 44$ mm. A plano-convex N-BK7 eye lens: $R = (n-1)f_e = 0.5168\times40 = 20.67$ mm. At 1° object-space semi-field, the eye sees $\tan\theta' = 10\tan1^\circ$ → 9.9°.

**(b) Plate in a converging beam (Geary §23.4).** 20 mm N-BK7 ($n = 1.5168$) in the F/3.3 beam ($u = -0.15$) of a 100 mm achromat:
- $\Delta z = 20 \times 0.5168/1.5168 = 6.81$ mm.
- $N = -20(1.5168^2 - 1)/1.5168^3 = -7.454$ mm; $S_I = Nu^4 = -0.003774$ mm, i.e. $W_{040} = S_I/8 = -0.47$ µm $= -0.80\lambda$ at 587.6 nm — almost a wave of spherical aberration from a "perfect" window. Surface by surface (Kidger's formulas, checked with the L08 script): the air→glass face gives $-0.016012$ and the glass→air face $+0.012238$; they partly cancel.
- With a 10° chief ray (or a 10° tilt): $S_{II} = +0.004436$, $S_{III} = -0.005215$, $S_V = +0.006130$ mm.

**(c) Tilted filters.** A 3 mm N-BK7 filter tilted 10° in a converging beam: T–S separation 0.034 mm (the Seidel estimate $t(n^2-1)\theta^2/n^3$ gives 0.035 mm), lateral image shift 0.18 mm. A 1 mm plate beam splitter at 45°: 0.27 mm of T–S separation — at F/4 that is a geometric blur of ~0.27/(2·4) ≈ 34 µm, i.e. several pixels on a modern sensor.

## Key takeaways
- Afocal: $M = -f_o/f_e$, exit pupil $= D/|M|$, field angles multiply by $M$; aberrations are angular (dioptres for defocus), wavefront referenced to a plane.
- A field lens at an intermediate image steers chief rays and relocates pupils with almost no effect on the axial beam — but it adds Petzval.
- Relay trains need a field lens at every intermediate image; even aberrations accumulate, odd ones cancel in symmetric relays.
- Eyepieces have an external stop (no symmetry help), large fields and positive Petzval; visual systems prefer field curvature to astigmatism.
- Plates in converging beams shift focus by $t(n-1)/n$ and add overcorrected spherical aberration and, when tilted or used off axis, coma and astigmatism; filters and cover glass must be in the design.
- Use Afocal Image Space, Paraxial surfaces and Coordinate Breaks to model these systems correctly in OpticStudio.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Afocal system | Zero total power; collimated in, collimated out |
| Angular magnification $M$ | $\tan\theta'/\tan\theta = -f_o/f_e$ |
| Keplerian / Galilean telescope | Positive / negative eyepiece; real / no intermediate image |
| Eye relief | Distance from last eyepiece surface to the exit pupil |
| Field lens | Lens at an intermediate image that redirects chief rays |
| Relay | Optics that re-image an intermediate image (often at $m=-1$) |
| Pupil spherical aberration | Spherical aberration of the pupil imaging; causes beam wander at the eye |
| Dioptre | Vergence unit, 1/m; used for defocus in visual systems |
| Afocal Image Space | OpticStudio mode with angular image-space units and a plane reference wave |
| Paraxial surface | OpticStudio ideal thin lens defined by focal length |
| Coordinate Break | OpticStudio surface that tilts/decentres the coordinate system |
| Plane-parallel plate | Zero-power element; shifts focus and adds aberration in non-collimated light |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE Press 2002 — Ch. 11, pp. 209–229; §6.6 (field lens near the image).
2. [Geary] J. M. Geary, *Introduction to Lens Design*, Willmann-Bell 2002 — Ch. 22, pp. 239–247; Ch. 23, pp. 249–259 (Table 23.1 after V. Mahajan, *Aberration Theory Made Simple*, SPIE TT6).
3. [Kenyon] I. R. Kenyon, *The Light Fantastic*, OUP 2008 — Ch. 4 (optical instruments).
4. Ansys Optics KB, designing afocal systems with Afocal Image Space: <https://optics.ansys.com/hc/en-us/articles/42661707601683>
5. Zemax community, "Angular spot diagram units — afocal image space": <https://community.zemax.com/got-a-question-7/angular-spot-diagram-units-afocal-image-space-935>
