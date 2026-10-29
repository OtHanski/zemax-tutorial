# L04 — Stops, Pupils, Fields and the Lagrange Invariant

> **Course 01 · Foundations** · Estimated time: lecture ~3 h, tasks ~4 h
> **Prerequisites:** [L03 — Paraxial optics](../L03-paraxial-optics-and-ray-tracing/) · **Next:** [L05 — Optical glass and dispersion](../L05-optical-glass-and-dispersion/)

## Learning objectives
- Identify the aperture stop and field stop of a system and locate the **entrance and exit pupils** as images of the stop, by paraxial trace.
- Define and trace the **marginal ray** and **chief ray**, and use them to compute F-number, numerical aperture, image height and pupil positions.
- Distinguish the F-numbers OpticStudio reports (Image Space F/#, Paraxial Working F/#, Working F/#) and use $N_w \approx N_\infty(1 - m/m_p)$ for finite conjugates.
- Compute the **Lagrange invariant** $H$, use it to get image height and magnification, and interpret it as a measure of throughput and information capacity.
- Set up the system aperture (EPD, Image Space F/#, Object Space NA, Float By Stop Size…), field type (angle, object height, image height) and ray aiming in OpticStudio, and recognize vignetting and when to use vignetting factors.
- Explain what telecentricity is and how stop position produces it.

## Reading
- **Core:** [Geary Ch. 5, pp. 43–49] — stops (§5.2), entrance/exit pupils for front, rear and buried stops (Figs. 5.2–5.9), marginal and chief rays (§5.3), locating a buried stop's pupils with the PRTE (§5.4), F-number from the paraxial marginal-ray angle (§5.5), the Lagrange invariant with a Galilean-telescope example (§5.6).
- **Core:** [Kidger §1.6, pp. 6–8] — aperture stop, marginal/chief rays, entrance/exit pupils, field stops.
- **Core:** [Kidger §2.5, pp. 25–30] — Lagrange invariant: proof of invariance on refraction and transfer, transverse magnification, afocal systems and angular magnification (binocular example).
- **Optional online:** Ansys Optics knowledge base, "Ray Aiming in OpticStudio: when to use Off, Paraxial or Real", and "How to use vignetting factors" (links in References).

---

## 1. Every system has an aperture stop

Some aperture always limits the cone of light from an axial object point: a lens rim, an iris, a mount. That aperture is the **aperture stop** [Kidger §1.6, p. 6; Geary §5.2, p. 43]. The stop does two jobs:

1. It sets the **light-gathering power** (F-number, NA) and hence image irradiance and diffraction blur.
2. Its **position** decides which part of each lens the off-axis beams use — so it is one of the most powerful aberration-control knobs you have. Moving the stop does not change focal length, but changes coma, astigmatism, distortion and lateral colour (stop-shift, L08 and Course 02 L03).

A **field stop** limits the *extent* of the image (or object): the sensor edge in a camera, a reticle in an eyepiece [Kidger §1.6.3, p. 8]. In a Zivid-type camera the sensor active area is the field stop.

### 1.1 Finding the stop
For a given axial object point, trace a paraxial ray at an arbitrary height and compute, at every surface/aperture $j$, the ratio $|\text{(semi-aperture)}_j / y_j|$. The aperture with the *smallest* ratio limits the beam first: it is the stop. (In OpticStudio you *declare* which surface is the stop — `STO` — and the aperture setting then sizes the beam; real apertures elsewhere can additionally vignette off-axis beams.)

---

## 2. Pupils: what the stop looks like from outside

- **Entrance pupil (EP):** the image of the stop formed by all optics *in front of* it (seen from object space).
- **Exit pupil (XP):** the image of the stop formed by all optics *behind* it (seen from image space).

[Geary §5.2, pp. 43–45; Kidger §1.6.2, pp. 7–8]

Three cases (Geary Figs. 5.2–5.9):

```
 (a) stop in front           (b) stop behind            (c) buried stop
   |      (lens)               (lens)    |               (L1) | (L2)
  STOP = EP                    STOP = XP                 EP = image of stop through L1
  XP = image of stop           EP = image of stop        XP = image of stop through L2
       through the lens             through the lens (backwards)
```

Rays from object space are *aimed at* the entrance pupil; in image space they *appear to come from* the exit pupil. Pupils are often **virtual** (located where no hardware is) and can lie far from the lens.

Why a camera designer cares about each pupil:
- **EP position** = perspective centre of the camera (the point you'd rotate about for parallax-free panoramas; the projection centre in a pinhole camera model used in 3D calibration).
- **XP position** sets the **chief-ray angle (CRA)** at the sensor; sensors with microlenses need CRA within limits (Course 04 L01/L03). XP at infinity = image-space telecentric.
- **Pupil size** sets the F-number and the NA.

### 2.1 Locating pupils with paraxial rays (Geary §5.4)
1. Trace a ray from the **centre of the stop** backwards (towards object space) through the optics in front of the stop. Where it (or its extension) crosses the axis is the EP location.
2. Trace a ray from the **edge of the stop** the same way; its height at the EP plane is the EP radius.

Same idea forwards through the rear optics gives the XP. Equivalently, use the Gaussian equation on the stop as an "object" (L03).

---

## 3. Marginal and chief rays

- **Marginal ray:** from the **axial** object point to the **edge** of the stop (edge of EP) [Kidger §1.6.1, p. 7; Geary §5.3, p. 46].
- **Chief ray:** from the **edge of the field** through the **centre** of the stop (centre of EP, centre of XP). Geary distinguishes "chief ray" (maximum field) from "principal ray" (any field); OpticStudio and most modern texts use "chief ray" for any field point.

By convention the chief-ray quantities carry a bar: $\bar y$, $\bar u$. They obey the same PRTE [Geary Eqs. 5.1–5.2, p. 46].

What these two rays tell you:

| Where | Marginal ray | Chief ray |
|---|---|---|
| Height zero | at object & image (focus) | at stop & pupils |
| Height at a lens | beam radius → lens size, power contribution | beam offset → off-axis aberrations, lens size |
| Angle in image space | $u'$ → F-number, NA | $\bar u'$ → CRA, telecentricity |

The ratio $\bar y / y$ at a surface measures how "off-axis" that surface is used; it is the lever arm for stop-shift effects (Course 02 L03, L08).

---

## 4. F-number and numerical aperture

### 4.1 Definitions
For an object at infinity [Geary Eq. 5.7, p. 48]:

$$
N = F/\# = \frac{f'}{D_{EP}} = \frac{-1}{2 u'} \quad(\text{paraxial marginal ray, } u' < 0).
$$

The image-space **numerical aperture** is $\text{NA} = n'\sin U'$ with $U'$ the real marginal-ray angle. For an aplanatic system in air, $N_w = 1/(2\,\text{NA})$.

OpticStudio lists three F-numbers [Geary §2.8.1, p. 19]:

| Name | Definition | Use |
|---|---|---|
| Image Space F/# | $f'/D_{EP}$ (infinite-conjugate value) | catalogue "F-number" of a lens |
| Paraxial Working F/# | $1/(2n'|u'|)$ for the actual conjugate, paraxial | radiometry, depth of focus at finite conjugates |
| Working F/# | $1/(2n'\sin U')$ from real rays | real cone angle; diffraction (Airy size uses this) |

### 4.2 Finite conjugates
When the object comes closer, the image moves away and the cone angle at the image shrinks:

$$
N_w = N_\infty\left(1 - \frac{m}{m_p}\right),
$$

where $m$ is the (negative) magnification and $m_p = D_{XP}/D_{EP}$ the pupil magnification. For a symmetric lens ($m_p \approx 1$) at 1:1 ($m = -1$), $N_w \approx 2N_\infty$ — a macro lens at F/2.8 behaves like F/5.6 for exposure and diffraction. Machine-vision lenses at short working distance are a typical case.

### 4.3 Typical values
- Machine-vision / 3D camera lenses: F/1.8–F/8 (fast for light-starved NIR, stopped down for depth of field).
- Projector lenses (structured light): F/1.5–F/3 to collect LED/laser étendue.
- Photographic primes: F/1.4–F/2.8; telescopes: F/4–F/15; microscope objectives: NA 0.1–1.4.

---

## 5. The Lagrange invariant

Trace the marginal ray $(y, u)$ and the chief ray $(\bar y, \bar u)$. Then at every surface and in every space [Kidger Eq. 2.24, p. 26; Geary Eq. 5.11, p. 49]

$$
H = n(\bar u\,y - u\,\bar y) = \text{constant}.
$$

(Geary writes it as $n(\bar y u - y\bar u)$ — the opposite sign. Only the magnitude matters in most uses; just be consistent.) Kidger's proof: eliminate the surface power between the refraction equations of the two rays (invariant on refraction), then eliminate the thickness between the two transfer equations (invariant on transfer) [Kidger §2.5, pp. 25–27].

Evaluate $H$ where it's easy:
- **At the object** ($y = 0$, $\bar y = h$): $H = -n u h$.
- **At the image** ($y' = 0$, $\bar y' = h'$): $H = -n' u' h'$.
- **At the stop/EP** ($\bar y = 0$): $H = n\bar u\, y_{EP}$ = (EP radius) × (field angle) for an object at infinity.

Consequences:
1. **Magnification:** $m = h'/h = nu/(n'u')$ [Kidger Eq. 2.33, p. 28].
2. **Image height from field angle:** $h' = H/(-n'u')$; for infinity, $h' = y_{EP}\,\bar u / (-u') = f'\tan\theta$.
3. **Afocal systems:** angular magnification $= \bar u'/\bar u = n y_{EP}/(n' y_{XP})$. Kidger's binocular: 30 mm EP, 8× → 3.75 mm exit pupil [Kidger §2.5.2, p. 30].
4. **Throughput:** $H^2$ is proportional to the energy a lens can transmit from a uniformly radiating object [Kidger p. 27] — the paraxial form of **étendue** (Course 05 L01). You cannot increase both field and aperture of a beam through a passive optical system. For a structured-light projector this is *the* law that limits brightness from a given LED.
5. **Information capacity:** the Airy radius is $0.61\lambda/(n'|u'|)$; the image radius is $H/(n'|u'|)$; their ratio $H/(0.61\lambda)$ is the number of diffraction-limited resolution elements along a radius [Kidger p. 27 mentions this link]. A bigger $H$ is a more "capable" (and harder to design) lens.

---

## 6. Fields

### 6.1 How fields are specified
- **Angle** (object at infinity): half-field angle $\theta$; image height $h' = f'\tan\theta$ for a distortion-free lens.
- **Object height** (finite object).
- **Paraxial image height** or **Real image height**: specify the image directly — natural when the sensor is fixed (e.g. a sensor's half-diagonal), but note that "real image height" makes OpticStudio iterate to find the object point, and it interacts with distortion.

A design spec usually gives the sensor and the desired FOV; the half-diagonal of the sensor is the full field. Geary: the half-field angle is taken at the *corner* of the format [Geary §1.2.4, pp. 6–7]. Sample at least 0, 0.7 and 1.0 of the full field (equal-area zones, L01), more for wide-angle designs.

### 6.2 Normalized coordinates
OpticStudio describes any ray by **normalized field** $(H_x, H_y)$ (fraction of the maximum field; $|H| \le 1$) and **normalized pupil** $(P_x, P_y)$ (fraction of the EP radius; $P_x^2 + P_y^2 \le 1$). The marginal ray is $H = 0, P_y = 1$; the chief ray is $H_y = 1, P = 0$. These coordinates appear in Single Ray Trace, ray fans and merit-function operands (e.g. `REAY` real ray y-coordinate takes $H_x, H_y, P_x, P_y$). OpticStudio also offers radial vs. rectangular field normalization (System Explorer → Fields); keep the default radial normalization unless you design for a rectangular sensor field.

### 6.3 Vignetting
Off-axis beams can be clipped by apertures *other* than the stop — lens rims, spacers. This is **vignetting**: the off-axis image gets darker and the effective pupil becomes a "cat's eye". Designers sometimes vignette *on purpose* to cut off the worst aberrated rim rays of off-axis beams (double Gauss, Course 02 L10).

In OpticStudio:
- **Semi-diameters** in the LDE are used for drawing, edge thickness and mechanical sizing. A semi-diameter alone does not generally act as a hard clipping aperture; to clip rays you add a **surface aperture** (e.g. circular aperture in the surface properties; the LDE tools can also convert semi-diameters into circular apertures). Verify the behaviour in your version with Task 5.
- **Vignetting factors** (VDX, VDY, VCX, VCY, TAN in the Field Data Editor) *decenter and compress* the pupil per field so that the rays OpticStudio launches already represent the unvignetted beam. The **Set Vignetting** tool computes them from the apertures. This matters for optimization: the default merit function's Gaussian-quadrature sampling assumes all launched rays reach the image; with hard apertures you either use vignetting factors or the rectangular-array sampling with "delete vignetted" (L07).
- Relative illumination (Analyze → Illumination → Relative Illumination) quantifies the darkening including the $\cos^4$-type effects (Course 04 L03).

### 6.4 Telecentricity
If the stop is placed at the **front focal plane**, the exit pupil is at infinity and every chief ray leaves the lens parallel to the axis: **image-space telecentric**. Stop at the rear focal plane → entrance pupil at infinity → **object-space telecentric** (magnification independent of object distance — the metrology lens of Course 04 L06). Telecentricity costs lens diameter: the last (or first) element must be at least as large as the field.

---

## 7. In OpticStudio

- **System Explorer → Aperture → Aperture Type:**
  - *Entrance Pupil Diameter* (default; good for infinite objects).
  - *Image Space F/#* (OpticStudio sizes the EPD to give $f'/D_{EP}$).
  - *Object Space NA* (finite objects, microscopes).
  - *Float By Stop Size* (the stop surface's semi-diameter defines the aperture — best when the physical stop size is fixed, e.g. a camera iris).
  - *Paraxial Working F/#*, *Object Cone Angle* for special cases.
- **Stop surface:** make a surface the stop from its surface properties (Type tab, "Make Surface Stop") or by inserting a dummy surface for an iris.
- **System Explorer → Aperture → Telecentric Object Space** for object-space telecentric systems (entrance pupil at infinity — EPD cannot be used then; use NA).
- **Ray Aiming (System Explorer → Ray Aiming: Off / Paraxial / Real).** With Off, OpticStudio aims rays at the *paraxial* entrance pupil. If the real entrance pupil is aberrated or shifted (wide-angle lenses, buried stops with strong front groups), real rays then miss the stop edge. Paraxial ray aiming iterates so that real rays hit the stop where the paraxial marginal ray would. Check with Analyze → Aberrations → Pupil Aberration: more than a few percent → turn ray aiming on. Ray aiming slows ray tracing (factor ~2–8) [Ansys KB, Ray Aiming].
- **System Data:** Entrance Pupil Diameter/Position, Exit Pupil Diameter/Position (positions are relative to the first surface and to the image surface respectively), all F-numbers, image-space NA.
- **Pitfalls:**
  - Putting the stop on the wrong surface (the `STO` label is on surface 1 by default).
  - Using EPD for a lens whose stop is an iris of known size, then changing the front lens: the actual iris size changes silently. Use Float By Stop Size.
  - Field type "Real Image Height" + optimization of distortion can fight each other; use angle or paraxial image height while learning.
  - Forgetting that a decentered or tilted stop requires ray aiming.

---

## Worked example — pupils of the Course 01 singlet for three stop positions

Lens: $R = \pm102.7$ mm, $t = 4$ mm, $n = 1.5168$, EFL 100.025 mm, BFL 98.698 mm, P and P′ 1.327 mm inside the lens. Field 5°, EPD 20 mm.

**(A) Stop at surface 1 (our L01 set-up).**
- EP = stop: at S1, diameter 20 mm.
- XP = image of the stop through surface 2. Chief ray: $\bar y_2 = 0.23072$, $n\bar u'_2 = 0.086328$ (L03). It crosses the axis at $-\bar y_2/\bar u'_2 = -2.673$ mm from S2 (inside the lens, i.e. 101.37 mm before the paraxial image). Marginal ray at that plane: $y = 9.8673 + (-0.099975)(-2.6726) = 10.134$ mm → **XP diameter 20.27 mm**, pupil magnification $m_p = 1.013$.
- Lagrange invariant: $H = n\bar u\,y_{EP} = 1 \times 0.087489 \times 10 = 0.87489$ mm. Image height $= H/|u'| = 0.87489/0.099975 = 8.751$ mm ✓.
- F/# $= 100.025/20 = 5.00$; $-1/(2u') = 1/(2 \times 0.099975) = 5.00$ ✓.

**(B) Stop 20 mm in front of the lens (EP = stop).**
- The chief ray now hits S1 at $\bar y_1 = 20\tan 5° = 1.750$ mm. The full-field beam occupies $-8.25$ to $+11.75$ mm on S1, so the lens must have a clear semi-diameter ≥ 11.75 mm (vs. 10.0 mm on axis) or the beam will vignette.
- XP: chief ray crosses the axis 28.43 mm *before* S2 → XP is virtual, 127.1 mm before the image; XP diameter 25.42 mm.
- Image height is unchanged (8.751 mm): stop position does not change first-order imaging, only *which rays* form the image.

**(C) Stop 20 mm behind the lens (XP = stop).**
- EP = image of the stop seen through the lens from the front. Using P′: the stop is $l' = 20 + 1.327 = 21.327$ mm from P′; $1/l = 1/21.327 - 1/100.025$ → $l = 27.107$ mm from P, i.e. **28.43 mm behind S1** (a virtual EP inside/behind the lens), magnification $21.327/27.107 = 0.787$.
- For EPD = 20 mm the physical stop must have semi-diameter $10 \times 0.787 = 7.87$ mm (check: the paraxial marginal ray $y_1 = 10$ arrives at the stop plane at 7.87 mm ✓). In OpticStudio, with *Float By Stop Size* and stop semi-diameter 7.87 mm you would get EPD = 20 mm.

**(D) Telecentric stop.** Put the stop at the front focal plane, 98.70 mm in front of S1. The chief ray then hits S1 at $\bar y_1 = 8.63$ mm and leaves the lens with $\bar u' = 0$: image-space telecentric. The lens would need a semi-diameter ≈ 18.6 mm (8.63 + 10) — telecentricity is paid for in glass.

**(E) Finite conjugate F-number.** With the object 300 mm in front of S1 (L03, $m = -0.497$), tracing the marginal ray from the axial object to the EP edge gives $n'u' = -0.06708$ → paraxial working F/# $= 1/(2 \times 0.06708) = 7.45$. Formula: $N_\infty(1 - m/m_p) = 5.001 \times (1 + 0.497/1.013) = 7.45$ ✓.

**(F) Resolution elements.** $H/(0.61\lambda) = 0.87489/(0.61 \times 0.5876\times10^{-3}) \approx 2440$ Airy radii from centre to edge of the field — if the lens were diffraction-limited. (It isn't: the singlet's ~60 µm spots give only ~150 resolvable spots per field radius. That gap is what lens design closes.)

---

## Key takeaways
- The aperture stop limits the axial beam; the field stop limits the image size. Stop position is a major aberration-control parameter.
- Entrance pupil = stop imaged by front optics; exit pupil = stop imaged by rear optics; both are found by paraxial trace and are often virtual.
- Marginal ray (axial object → stop edge) gives F/#, NA, beam size; chief ray (field edge → stop centre) gives image height, pupils, CRA.
- $N = f'/D_{EP} = -1/(2u')$; at finite conjugates $N_w = N_\infty(1 - m/m_p)$.
- The Lagrange invariant $H = n(\bar u y - u\bar y)$ is conserved; it fixes magnification and image height, and $H^2$ measures throughput (étendue).
- In OpticStudio choose the aperture type that matches the physical constraint (EPD, F/#, NA, Float By Stop Size); use ray aiming when pupils are aberrated; handle vignetting with apertures + vignetting factors.
- Stop at front focal plane → image-space telecentric.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Aperture stop | Aperture limiting the axial beam |
| Field stop | Aperture limiting the field (e.g. sensor edge) |
| Entrance pupil (EP) | Image of the stop in object space |
| Exit pupil (XP) | Image of the stop in image space |
| Pupil magnification $m_p$ | $D_{XP}/D_{EP}$ |
| Marginal ray | Axial object point → edge of stop |
| Chief ray | Field point → centre of stop |
| Working F/# | $1/(2n'\sin U')$ at the actual conjugate |
| Numerical aperture (NA) | $n\sin U$ |
| Lagrange invariant $H$ | $n(\bar u y - u\bar y)$, conserved through the system |
| Étendue | Geometric throughput; ∝ $H^2$ |
| Vignetting | Clipping of off-axis beams by non-stop apertures |
| Vignetting factors | VDX, VDY, VCX, VCY, TAN: per-field pupil decenter/compression |
| Ray aiming | Iterating launched rays to hit the real stop correctly |
| Telecentric | Pupil at infinity; chief rays parallel to axis in that space |
| Normalized coordinates | $H_x, H_y$ (field) and $P_x, P_y$ (pupil), each in [−1, 1] |

## References
1. [Geary Ch. 5, pp. 43–49] Geary, *Introduction to Lens Design*: §5.2 stop and pupils, §5.3 marginal and chief rays, §5.4 pupils via PRTE, §5.5 F-number, §5.6 Lagrange invariant, §5.7 homework (triplet pupils).
2. [Geary §2.8.1, p. 19] three F-numbers in ZEMAX; [Geary §1.2.4, pp. 5–7] field angle at the format corner.
3. [Kidger §1.6, pp. 6–8] Kidger, *Fundamental Optical Design*: stops, pupils, marginal/chief rays, field stops.
4. [Kidger §2.5, pp. 25–30] Lagrange invariant, transverse magnification, afocal systems and angular magnification.
5. Ansys Optics knowledge base, "Ray Aiming in OpticStudio: when to use Off, Paraxial, or Real" — pupil aberration check, Float By Stop Size, speed trade-off: https://optics.ansys.com/hc/en-us/articles/42661778056083
6. Ansys Optics knowledge base, "How to use vignetting factors" — VDX/VDY/VCX/VCY/TAN, Set Vignetting, Gaussian quadrature vs. rectangular array: https://optics.ansys.com/hc/en-us/articles/42661826659347
7. Zemax Community, "How do vignetting factors affect my ray trace?" — intuitive picture of decentering/compressing the pupil: https://community.zemax.com/got-a-question-7/how-do-vignetting-factors-affect-my-ray-trace-87
