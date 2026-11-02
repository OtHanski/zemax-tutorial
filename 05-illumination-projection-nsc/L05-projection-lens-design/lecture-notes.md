# L05 — Projection Lens Design: DMD Imaging, Offset, Telecentricity and Depth of Focus

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3.5 h, tasks ~6 h
> **Prerequisites:** [L01](../L01-radiometry-photometry-etendue/lecture-notes.md) (étendue, DMD acceptance), [L04](../L04-illumination-optics-collimators-condensers/lecture-notes.md) (DMD illumination, TIR prisms); Course 02 [L05 distortion](../../02-aberrations-classical-design/L05-distortion/lecture-notes.md), [L13 windows & plates](../../02-aberrations-classical-design/L13-eyepieces-afocal-relays-windows/lecture-notes.md); Course 03 [L02 MTF](../../03-image-quality-optimization/L02-mtf-theory-and-practice/lecture-notes.md), [L03 depth of focus](../../03-image-quality-optimization/L03-strehl-wavefront-error-depth-of-focus/lecture-notes.md), [L06 multi-configuration](../../03-image-quality-optimization/L06-multi-configuration-and-zoom/lecture-notes.md); Course 04 [L03 telecentricity](../../04-machine-vision-camera-lenses/L03-relative-illumination-and-telecentricity/lecture-notes.md), [L05 retrofocus](../../04-machine-vision-camera-lenses/L05-wide-angle-and-distortion-mappings/lecture-notes.md) · **Next:** [L06 — Hybrid/mixed mode and NSC optimization](../L06-hybrid-mixed-mode-and-nsc-optimization/lecture-notes.md)

## Learning objectives
- Set up a projection lens in OpticStudio's sequential mode **in reverse** (screen as object, DMD as image) and explain which numbers then appear in DMD pixels; also set up the forward (DMD-as-object, telecentric object space) version for checking.
- Compute the first-order layout of a projector from DMD size, throw ratio and offset: focal length, image-circle radius, maximum field angle, F/# from the micromirror tilt, projected pixel size.
- Explain DMD geometry (±12°/±17° tilt, on/off/flat-state bundles), why the projection F/# is tied to the tilt angle, and why telecentric DMD illumination with a TIR/RTIR prism forces a long back focal length and a retrofocus lens form.
- Model the prism and DMD window as plane-parallel plates and estimate the spherical aberration they introduce in the converging beam.
- Quantify keystone for a tilted projector and explain why offset (lens shift) is preferred, especially for structured light.
- Write a projection-lens specification in pixels: MTF at the DMD Nyquist frequency, distortion and lateral-colour budgets, telecentricity — and translate it into merit-function operands.
- Compute the DMD-side defocus over a 0.5–1.5 m structured-light working range, choose the focus distance and F/#, and predict the contrast of projected fringes of a given period at the range ends.

## Reading
- **Core:** [Geary §20.3, p. 223] and [Geary §22.7, p. 247] — designing "from the long conjugate to the short conjugate", i.e. in reverse to the way the system is used; exactly what we do with a projection lens.
- **Core:** [Geary Ch. 23, §23.3–23.6, pp. 251–259] — windows and plane-parallel plates in converging beams: focus shift $t(n-1)/n$, spherical aberration, tilted windows, axial colour. Your TIR prism and DMD window are such plates.
- **Core:** [Kidger §4.4.2.4.1, pp. 79–80] — distortion in the finite-conjugate case (real vs paraxial chief-ray height), which is how projector distortion is defined; [Kidger §6.11, pp. 136–137] — conjugate-shift changes of the Seidel aberrations (why a projection lens designed at 1 m changes slightly at 0.5 m).
- **Core:** [Kidger Ch. 10, pp. 199–208] — triplet-family design and vignetting; read §10.4 (p. 206) on corner illumination. Note Kidger's remark that fast, aspheric, medium-field lenses "are used as television projection lenses" [Kidger §6.6, p. 128].
- **Core (online):** Texas Instruments, *DLP System Optics* (DLPA022) — tilt angle sets the usable NA, telecentric vs non-telecentric architectures, TIR prism air gap, and concrete projection-lens image-quality targets (MTF at Nyquist, lateral colour, distortion): <https://ti.com/lit/pdf/dlpa022>
- **Core (online):** Texas Instruments, *TI DLP® System Design: Optical Module Specifications* (DLPA078) — definitions of throw ratio and offset: <https://ti.com/lit/dlpa078>
- **Optional:** [Geary Ch. 32, §32.2.2, p. 370] — diffractive depth of focus; Texas Instruments, *Geometric Optics for DLP* (DLPA044) — throw ratio, offset and projected pixel size for the LightCrafter kits: <https://edgeworker.ti.com/lit/pdf/dlpa044>
- **Optional (Ansys KB):** *Making image-space telecentric lenses* (curvature solve, RANG, EXPP + RECI): <https://optics.ansys.com/hc/en-us/articles/42661811743251>; *Reversing an entire sequential system with the Reverse Elements tool* (KA-01408): <https://optics.ansys.com/hc/en-us/articles/42661794180115>; community thread on modelling a DMD (US_MEMS.DLL user-defined surface and the MEMS NSC object): <https://community.zemax.com/got-a-question-7/ti-dlp-dmd-projector-model-736>
- **Optional:** Optics for Hire blog, *Projection lens design* — a short practitioner's overview of offset, telecentricity and trade-offs: <https://www.opticsforhire.com/blog/projection-lens-design/>

---

## 1. A projection lens is a camera lens run backwards

A projector images a small, bright object — the spatial light modulator (SLM: DMD, LCoS, or a fixed mask) — onto a large, distant "screen". For Zivid-type structured-light cameras the screen is the 3-D scene itself, anywhere from ~0.5 to ~1.5 m away. Geometrically this is a camera lens with light reversed: the long conjugate (scene) and the short conjugate (SLM, a few µm per pixel) are swapped.

Because ray paths are reversible, **image quality is identical in both directions**: a lens that images a 5.4 µm DMD pixel into a 0.65 mm patch on a wall also images a 0.65 mm patch on the wall into a 5.4 µm spot on the DMD. Designers therefore almost always **design in reverse**: object = screen (long conjugate, left), image = DMD (short conjugate, right). Geary does exactly this for microscope objectives and eyepieces — "the design will proceed from the long conjugate to the short conjugate" [Geary §20.3, p. 223; §22.7, p. 247].

Why reverse?

1. **All image-space numbers are on the DMD, in µm.** Spot radii, MTF frequencies (cycles/mm), lateral colour and distortion are evaluated at the DMD, so you can compare them directly with the pixel pitch $p$: Nyquist $=1/(2p)$, "one pixel of lateral colour" = $p$. In the forward direction, the same numbers come out at the screen in mm and depend on the throw distance.
2. **The default merit function works.** It minimizes spot or wavefront at the image; at the screen that is a 1 m away, huge image the RMS-spot numbers are large and poorly conditioned.
3. **Telecentricity on the DMD side** is image-space telecentricity — easy to constrain with a chief-ray-angle operand.

When is the forward direction useful? To **verify** (e.g. a Geometric Image Analysis or an NSC/mixed-mode simulation of the whole projector, L06/L09), when the illumination side defines the pupil, and for keystone/tilt studies where the screen is tilted. OpticStudio's System Explorer has a **Telecentric Object Space** option (Aperture tab) for exactly this case: the object (DMD) is telecentric, the entrance pupil is at infinity. Ansys's KB notes the restrictions: ray aiming and angle-type fields cannot be used with it, and the stop is best on surface 1 (see the telecentric KB article in Reading).

**Conventions in this lesson.** OpticStudio standard: light left → right, distances positive to the right, radii positive when the centre of curvature is to the right. In the reverse model the screen is surface 0, the lens follows, then the prism/window plates, then the DMD as the image surface. "Field" means DMD height $h$ (mm) measured from the lens axis; "offset" is a vertical displacement of the DMD (or the image) relative to that axis. Signs of aberrations follow Kidger: undercorrected spherical aberration = positive $S_1$ [Kidger §6.7, p. 128].

## 2. DMD geometry — what the lens sees

### 2.1 Micromirror tilt and the F/# ceiling
A DMD is an array of square micromirrors (pitch e.g. 5.4, 7.56, 10.8 µm) that tilt about their diagonal (or, for "tilt-and-roll" pixels, about two axes) to **±θ_t**: ±12° for most older and many industrial parts, ±17° for many newer ones (e.g. the 0.47″ 1080p DLP4710, 5.4 µm pitch: <https://www.ti.com/product/dlp4710>). TI's DLPA022 describes the 12° family; check each device's datasheet.

Reflection doubles angles. With the on-state mirror tilted by $+\theta_t$:

```
            projection lens axis (normal to DMD)
                      ▲  on-state light (reflected along the normal)
                      │
   illumination ──►   │   incident at 2θt from the normal
        ╲             │
          ╲    2θt    │       flat-state (θ=0) reflection leaves at −2θt
            ╲         │       off-state (−θt) reflection leaves at −4θt
  ──────────────────[DMD]──────────────────────
     θt = 12°:  illumination 24°, flat 24°, off 48°
     θt = 17°:  illumination 34°, flat 34°, off 68°
```

Each bundle is a cone. If the on-state cone half-angle exceeds $\theta_t$, it overlaps the flat-state bundle (light scattered from the window, the mirror gaps and the via/hinge structure) and the off-state light starts entering the lens: **contrast collapses**. Hence TI's statement that "the device tilt angle sets the maximum useful numerical aperture" (DLPA022):

$$
\mathrm{NA}_{\max} = \sin\theta_t,\qquad N_{\min} = \frac{1}{2\sin\theta_t}
$$

where $N$ is the (image-space, DMD-side) F-number. Numbers: $\theta_t = 12°$ → NA 0.208, **F/2.40**; $\theta_t = 17°$ → NA 0.292, **F/1.71**. TI notes the limit can be "stretched" with performance trade-offs, and that a projection aperture slower than the illumination aperture raises contrast at the cost of lumens.

### 2.2 Telecentric vs non-telecentric illumination
Two architectures, from DLPA022 and L04 §7:

| | Telecentric | Non-telecentric |
|---|---|---|
| Illumination/projection separation | in glass, by a **TIR or RTIR prism** at ≈ 2θ_t + margin | in air (sometimes with a field lens) |
| Projection-lens pupil (seen from DMD) | at infinity → chief rays ⊥ DMD | at a short finite distance; must coincide with the illumination exit pupil |
| Offset | free: anything including 0 % | fixed by geometry (TI: "reducing offset is not an option") |
| Back working distance | long (prism glass) | shorter |
| Lens complexity | higher (telecentric + long BFL → retrofocus) | lower, cheaper |

For structured light (and any good projector) the telecentric route is attractive: the illumination angle is the same at every mirror, so brightness and contrast do not vary over the field, and the magnification does not change with focus (pupil at infinity on the DMD side). The price is in the lens.

### 2.3 The prism and window are plane-parallel plates
In the projection path the TIR (or RTIR) prism pair looks, to the projection lens, like a thick **plane-parallel glass block** (typically 10–25 mm of glass for small DMDs) plus a thin air gap at the TIR hypotenuse; the DMD package adds a cover window (~1 mm; take the exact value and glass from the datasheet). DLPA022: the prism "is basically a flat glass plate", the TIR air gap should be ≈ 10 µm to avoid astigmatism in the projection path, and the window must be included in the design.

In the converging beam on the DMD side, a plate of thickness $t$, index $n$ [Geary §23.4, pp. 253–257]:
- shifts focus by $\Delta z = t\,(n-1)/n$ (≈ t/3 for crown glass);
- adds **overcorrected** (negative $S_1$) spherical aberration, growing with $u^2$;
- adds axial colour (focus shift varies with $n(\lambda)$);
- if tilted (the TIR air gap is a tilted thin plate!), adds astigmatism and lateral shift.

Exact focus shift of a ray with angle $u$ in air ($\tan u_g = \sin u/\sqrt{n^2-\sin^2 u}$ inside the glass):

$$
\Delta z(u) = t\left(1-\frac{\tan u_g}{\tan u}\right)\;\xrightarrow{u\to0}\; t\,\frac{n-1}{n},
\qquad
\mathrm{LSA}\approx t\,\frac{(n^2-1)\,u^2}{2n^3}.
$$

For a 12 mm N-BK7 block at 850 nm ($n = 1.5098$) and an F/1.71 cone ($\tan u = 0.292$): paraxial shift 4.05 mm; marginal–paraxial LSA ≈ 0.18 mm; transverse aberration of the marginal ray at paraxial focus ≈ 54 µm (10 pixels); even at best focus the blur circle is ≈ 27 µm — about **5 pixels** — if the lens were designed without the plate. Lesson: **the plate is part of the lens**. Put it in the Lens Data Editor from the very first sketch. Because the beam is telecentric, every field sees the same plate aberration, so the lens can compensate it with its own (undercorrected) spherical aberration.

### 2.4 Consequence: long back focal length → retrofocus
The physical distance from the last lens to the DMD must hold prism + window + air: say 2 mm air + 12 mm prism + 1.1 mm window. Its *air-equivalent* ("reduced") length is $2 + 12/1.51 + 1.1/1.51 \approx 10.7$ mm. For a short-focal-length lens ($f \approx 8$ mm in the worked example) that means **BFL/f ≈ 1.3**, which a symmetric or triplet form cannot provide. Add the telecentric condition (stop at the front focal plane of the rear group) and you arrive at the classic DLP projection-lens form: **negative front group – stop – positive rear group**, i.e. a retrofocus (inverted telephoto, Course 04 L05) with a strongly positive, telecentric rear group, typically 6–10 elements and often one or two aspheres. Small pico/industrial projectors trade some of this for cost.

## 3. First-order layout: throw ratio, offset, image circle

### 3.1 Throw ratio and focal length
TI defines the **throw ratio** as distance $D$ from the lens to the screen divided by the projected image width $W_s$ (DLPA078): $T = D/W_s$. With magnification $m = W_s/W$ ($W$ = DMD active width) and a thin lens, $D = f(1+m)$, so

$$
f = \frac{D}{1+m} = T\,W\,\frac{m}{1+m}\;\approx\; T\,W .
$$

For a 0.3″ 720p DMD ($W = 1280 \times 5.4\ \mu\text{m} = 6.912$ mm) and $T = 1.2$: $f \approx 8.3$ mm (8.23 mm exactly at $D = 1$ m). Projected pixel size $= p\,m$ — 0.65 mm at 1 m. Shorter throw = wider field = harder lens: horizontal half-angle at zero offset is $\arctan\left(1/(2T)\right)$, 22.6° at $T = 1.2$, 34.9° at $T = 0.6$.

### 3.2 Offset (lens shift)
**Offset** describes where the image sits relative to the lens axis. TI's convention (DLPA078): 0 % = image centred on the axis; **100 % = the bottom edge of the image is on the axis**. Equivalently

$$
\text{offset} = \frac{2\,s}{H}\times100\ \%,
$$

with $s$ the vertical distance of the DMD centre from the lens axis and $H$ the DMD active height. 100–120 % is common for table-top projectors so the image clears the table; 0 % gives the thinnest module. (Conventions differ between vendors — some quote the fraction of the image above the axis — so always confirm with a sketch.)

Offset costs **image circle**. The lens must cover the farthest DMD corner:

$$
r_{\max} = \sqrt{\left(\tfrac{W}{2}\right)^2 + \left(s+\tfrac{H}{2}\right)^2}.
$$

0.3″ 720p: $r_{\max} = 3.97$ mm at 0 % offset, **5.20 mm** at 100 % ($s = 1.944$ mm); with $f = 8.23$ mm the corner field grows from 25.7° to **32.3°**. The lens is rotationally symmetric and designed over the full circle, but only part of it is used: with 100 % offset the DMD occupies the upper half of the circle. Weight your field points accordingly (§6).

```
   0 % offset              100 % offset (DMD below axis → image above axis)
   ┌──────────┐            ┌──────────┐  image on screen
   │    ●     │ axis       │          │
   └──────────┘            │          │
                           ●──────────┘ ← bottom edge on axis
   image circle r = 3.97   image circle r = 5.20 mm (at the DMD)
```

### 3.3 Why not just tilt the projector? Keystone
To raise the image without offset you could tilt the projector up by $\alpha$. The image plane (DMD conjugate) is then no longer parallel to the screen and the image becomes a trapezoid — **keystone**. For a pinhole projector with vertical half-field $\beta$ tilted by $\alpha$, a horizontal row at field angle $\varphi$ (relative to the projector axis) lands at a distance along the axis proportional to $1/\cos(\alpha+\varphi)$, so the top-to-bottom width ratio is

$$
\frac{W_{\text{top}}}{W_{\text{bottom}}} = \frac{\cos(\alpha-\beta)}{\cos(\alpha+\beta)} .
$$

Reproducing a 100 % offset image by tilt needs $\alpha = \beta$: for $T = 1.2$, 16:9, $\beta = 13.2°$ and the ratio is **1.116** — the top is 11.6 % wider than the bottom.

Why offset beats tilt:
1. **Rectangular image, uniform pixel footprint.** Digital keystone correction can square the image only by not using mirrors: the top rows would use 1/1.116 = 90 % of their columns, and the pattern is resampled. For structured light, resampling binary or phase-shifted patterns introduces interpolation errors and aliasing — exactly what you do not want in a measurement pattern.
2. **Focus plane stays parallel to the screen.** A tilted projector has its best-focus plane tilted relative to the wall (Scheimpflug, Course 04 L09), so top and bottom are at different focus.
3. **Uniform brightness.** Irradiance falls off with the extra path length on the far side.
4. In a triangulation system the projector–camera overlap over the depth range can also be achieved by toe-in; calibration absorbs the geometry, but points 1–2 still apply. Many 3-D sensors use offset (shift) rather than toe-in for these reasons — at the cost of a larger image circle in both lenses.

The cost of offset is only optical: a bigger field to correct (32° instead of 26° corner field above).

## 4. Image-quality specification in pixels

A projection-lens spec is most useful when written in DMD pixels; the reverse design makes this natural.

### 4.1 MTF at the DMD Nyquist frequency
The finest pattern a DMD can display is alternating on/off columns: period $2p$, frequency $\nu_N = 1/(2p)$ — **92.6 cycles/mm** for 5.4 µm, 46.3 cycles/mm for 10.8 µm. (Strictly, square-wave patterns contain harmonics above $\nu_N$; the lens acts as the low-pass filter that turns them into near-sinusoids.)

TI's DLPA022 targets for display lenses, a good default starting point:
- ≥ **40 % MTF at Nyquist**, average of sagittal and tangential, everywhere in the field;
- sagittal and tangential within **20 %** of each other at any field point;
- design nominal **10–20 % higher** to leave room for tolerances (Course 06).

The diffraction ceiling at $\nu_N$ is far above that for typical F/#s: with $\nu_c = 1/(\lambda N)$ the diffraction-limited MTF at 92.6 c/mm is 0.83 at 850 nm F/1.71, 0.76 at 850 nm F/2.4, 0.91 at 450 nm F/1.71. The 40 % target is therefore an aberration budget, not a diffraction limit — and NIR projectors pay ~10 % more than visible ones.

For structured light, ask what the patterns actually need. Phase-shifting fringes typically have periods of 8–32 pixels (5.8–23 c/mm at 5.4 µm); only the finest Gray-code or binary-edge patterns approach Nyquist. Often **depth of focus (§5) dominates** over nominal in-focus MTF.

### 4.2 Distortion
Kidger's finite-conjugate definition is what OpticStudio reports [Kidger §4.4.2.4.1, pp. 79–80]: real vs paraxial chief-ray height, relative to the paraxial height. In pixels: 1 % at the image-circle edge $r_{\max} = 5.20$ mm is 52 µm = **9.6 pixels** (the farthest pixel of a 100 %-offset 720p DMD is 963 pixels from the axis, versus 734 for 0 % offset).

- Display projectors: TI quotes ±1 % maximum, or 2 % total if there are no inflections (DLPA022).
- Structured light: the projector is calibrated like an inverse camera (Brown–Conrady-type models), so a few per cent is acceptable **if** the distortion is low-order, monotonic (no inflection, which calibration models fit poorly) and stable (temperature, focus). A practical design target is ≤ 1–2 % with a smooth curve; what matters more is that it does not change after calibration.
- Distortion also changes with conjugate [Kidger §6.11, pp. 136–137]: check it at 0.5, 0.75 and 1.5 m (multi-configuration) — small, but it is a systematic error that the calibration volume must cover.

### 4.3 Lateral colour
Lateral colour displaces the image of a pixel by wavelength. DLPA022 asks for **< 1 pixel** from 430 to 670 nm for RGB display. For a structured-light projector:
- Broadband white LED → lateral colour at the field edge smears pattern edges across the camera's spectral response; budget ≈ 0.5 pixel (2.7 µm at 5.4 µm pitch) over the effective band.
- Narrowband source (single-colour LED, 30–50 nm FWHM, or a laser) → lateral colour inside the band is small; the issue becomes the **difference between the calibration wavelength and the operating wavelength** (e.g. a lens designed for blue but used with an NIR source: its distortion is different at 850 nm). Design and calibrate at the wavelength you use.

### 4.4 Telecentricity and relative illumination
With telecentric illumination the chief ray at every mirror is along the normal. If the lens is not telecentric on the DMD side, the reflected cone at the field edge is displaced in the lens pupil → vignetting, brightness roll-off, lost contrast. A useful rule of thumb: keep the DMD-side chief-ray angle small compared with the cone half-angle — a degree or two against 12–17°. Relative illumination (cos⁴ plus vignetting, Course 04 L03; [Kidger §10.4, p. 206]) adds to the illumination system's non-uniformity (L04); product specs usually ask for a corner-to-centre ratio well above the 40 % that Kidger quotes for a photographic triplet — check your spec, there is no universal number.

## 5. Depth of focus over a structured-light working range

A display projector focuses on one screen. A structured-light projector must put a usable pattern on objects from, say, 0.5 to 1.5 m. Work on the DMD side with Newton's equation [Course 01 L03]: a scene plane at distance $L$ (from the lens) is conjugate to a DMD-side plane displaced by

$$
x'(L) = \frac{f^2}{L-f}
$$

from the rear focal point. Over a range $L_1 \dots L_2$, the DMD (fixed) is best placed midway between $x'(L_1)$ and $x'(L_2)$, which corresponds to focusing at the **harmonic mean** $L_f \approx 2L_1L_2/(L_1+L_2)$ — 0.75 m for 0.5–1.5 m, not 1.0 m. The residual defocus at the range ends is

$$
\pm\delta = \pm\tfrac12\left[x'(L_1)-x'(L_2)\right]\approx \pm\tfrac12 f^2\left(\frac1{L_1}-\frac1{L_2}\right),
$$

and, since a cone of F-number $N$ has a full angle of about $1/N$, the geometric blur diameter on the DMD side is $b \approx \delta/N$.

For $f = 8.23$ mm, 0.5–1.5 m: $\delta = 46\ \mu$m. At F/1.71, $b = 27\ \mu$m = **5.0 pixels**; at F/2.4, 3.6 pixels. Keeping the blur to one pixel would need F/8.5 — throughput $(1.71/8.5)^2 \approx 4$ % of the F/1.71 lens. Compare the diffraction depth of focus $\pm2\lambda N^2$ [Geary §32.2.2, p. 370]: ±5 µm at 850 nm F/1.71 — the geometric term dominates by an order of magnitude.

Scaling law (useful in architecture trade-offs): with $f \approx T\,N_{px}\,p$ ($N_{px}$ = pixels across),

$$
b_{\text{px}} = \frac{b}{p} \approx \frac{T^2 N_{px}^2\, p}{2N}\left(\frac1{L_1}-\frac1{L_2}\right).
$$

For fixed pixel count and throw ratio, **a smaller DMD (smaller $p$) has less blur in pixels** — the 0.47″ 1080p DMD (f ≈ 14.3 mm at T = 1.4) blurs ~15 pixels at the range ends at F/1.71 (tasks). That is one reason structured-light projectors use small DMDs and moderate throw ratios.

What does a 5-pixel blur do to a pattern? A uniform defocus disc of diameter $b$ has geometric MTF $2J_1(\pi b\nu)/(\pi b\nu)$. With $b = 27\ \mu$m:

| Pattern period (pixels) | ν at DMD (c/mm) | Contrast at range ends |
|---|---|---|
| 2 (Nyquist) | 92.6 | ≈ 0.05 (gone) |
| 8 | 23.1 | 0.59 |
| 16 | 11.6 | 0.88 |
| 32 | 5.8 | 0.97 |

This is the physics behind structured-light pattern design: **sinusoidal fringes of 8–32 pixels survive defocus** (a defocused sinusoid is still a sinusoid of the same phase, just with lower contrast — the phase, which carries depth, is preserved), while fine binary codes do not. Beyond the first zero of the defocus MTF, contrast even reverses sign (phase flips by π) — a nasty failure for phase decoding. Projection-lens design for structured light is therefore a **joint optimization of F/#, focus distance, pattern period and lens MTF** — and the in-focus Nyquist MTF matters less than the through-focus MTF at the pattern frequencies.

## 6. In OpticStudio

### 6.1 Reverse (design) model
**System Explorer**
- *Aperture:* **Paraxial Working F/#** = 1.71 (or 2.4) — this is defined on the image (DMD) side, exactly the quantity tied to the mirror tilt. (Image Space F/# assumes an infinite object; at $m \approx 1/120$ the difference is ~1 %.)
- *Fields:* **Real Image Height** (or Paraxial Image Height while sketching) — enter DMD heights in mm: e.g. 0, 0.3, 0.5, 0.7, 0.85, 1.0 × $r_{\max}$. With 100 % offset you may add weight to the zone 0–$(s+H/2)$ that covers the vertical extent, since the outer zone is only used at the corners.
- *Wavelengths:* the source band (e.g. 0.83, 0.85, 0.87 µm for an 850 nm LED; or 0.45/0.55/0.62 µm for RGB). Weight by the source spectrum (L03).
- *Ray aiming:* on (Paraxial or Real) for a wide-angle retrofocus front group.

**Lens Data Editor** (surface 0 to image):
`OBJ (screen, thickness 750 mm) → front negative group → STOP → rear positive group → air gap → prism (plate, N-BK7 or the prism glass, t) → air (≈ 0.5–1 mm) → window (plate) → small air gap → IMA (DMD)`.
Put a **Marginal Ray Height = 0** solve on the last air thickness while sketching; later make it a variable (it is the projector's focus adjustment).

**Analyses** — all at the DMD, in µm:
- Standard Spot Diagram with the Airy disc and a 5.4 µm reference; **FFT MTF** to 100 c/mm, and **FFT Through Focus MTF** at 11.6/23.1/92.6 c/mm.
- **Field Curvature/Distortion** and **Grid Distortion** (the grid covers the square field; read the DMD rectangle out of it, or define x–y field points at the DMD corners).
- **Lateral Color** (in µm; compare with $p$), **Chromatic Focal Shift**.
- **Relative Illumination**; Footprint Diagram on the prism faces to size the prism.

**Merit Function** — start with the default (RMS spot or wavefront, centroid, rectangular array) and add:
- `EFFL` (first-order, from the throw ratio) or let the object distance and a magnification target do it;
- telecentricity: `RANG` (real ray angle in radians w.r.t. the z axis) of the chief ray ($P_x = P_y = 0$) at the image surface for the edge fields, target 0 — or, as in the Ansys KB, `EXPP` (weight 0) + `RECI` of it targeted to 0, which drives the exit pupil to infinity;
- distortion: `DIMX` (maximum distortion) target ≤ 1–2 %;
- lateral colour: `LACL` (lens units, so mm at the DMD) bounded with `OPLT` to ± ½ pixel;
- MTF: `MTFA` (average of sagittal and tangential) at 92.6 c/mm with `OPGT` 0.5 at each field — add it late in the optimization, it is expensive and non-smooth (Course 03 L04);
- physical: `CTGT`/`ETGT`/`MNCT` etc. for glass, a minimum back working distance with `TTHI` across the prism-side air gaps, `TOTR` for length.

**Multi-Configuration Editor** (Course 03 L06): configurations for object distance 500 / 750 / 1500 mm (operand `THIC` on surface 0), with the DMD position held fixed. Optimize the through-range performance, not only the nominal.

### 6.2 Forward (verification) model
Either use **Reverse Elements** (select all surfaces between OBJ and IMA; the KB article KA-01408 lists the extra thickness and aperture steps) or rebuild: OBJ = DMD; Aperture **Object Space NA** = 0.292 (= sin 17°); **Telecentric Object Space** checked; fields as **Object Height** (mm on the DMD, positive y for the offset region); image at the screen distance. Use **Geometric Image Analysis** or **Image Simulation** with a fringe bitmap to see the projected pattern at 0.5/0.75/1.5 m. Tilted-projector (keystone) studies are easiest here: tilt the image surface with a Coordinate Break before the IMA (or tilt the lens group), then look at Grid Distortion — the trapezoid appears directly.

### 6.3 The DMD itself
For the lens, the DMD is just a flat image (reverse) or object (forward) plane. If you need the mirrors — e.g. off-state light or diffraction from the mirror array — OpticStudio provides a sequential **User Defined surface (US_MEMS.DLL)** and an NSC **MEMS** object, with sample files `MEMS DLL Sample.zmx` and `MEMS device.zmx` (per the Zemax community thread in Reading; locations vary by version — search the Samples folder). The sequential DLL bends rays as on a flat substrate, so it is fine for geometric results but not for wavefront-accurate work. Whole-projector simulation is L06 and the L09 capstone.

### 6.4 Common pitfalls
- Designing without the prism/window plates, then "adding them later": 5+ pixels of spherical aberration and the wrong BFL.
- Forgetting that offset enlarges the field: optimizing to $r = 3.97$ mm and then using the lens at 100 % offset.
- Optimizing at one distance and finding at 0.5 m that the edge MTF has collapsed (field curvature and astigmatism change with conjugate).
- Using telecentric illumination with a non-telecentric lens: edge vignetting and contrast loss that look like an illumination problem.
- Specifying "F/1.7" for a ±12° DMD: the lens collects flat-state light and contrast drops.
- Mixing up offset conventions with a supplier: draw the axis and image in the spec.

## Worked example — first-order design of an NIR structured-light projector lens

**Given:** 0.3″ 720p DMD, 1280 × 720 mirrors, $p = 5.4\ \mu$m, ±17° tilt, telecentric illumination via a TIR prism (12 mm N-BK7 glass path), 1.1 mm window (assume N-BK7), 850 nm LED. Throw ratio 1.2 defined at 1 m; 100 % offset; working range 0.5–1.5 m.

1. **DMD:** $W = 6.912$ mm, $H = 3.888$ mm, diagonal 7.93 mm. Nyquist 92.6 c/mm.
2. **Image at 1 m:** $W_s = 1000/1.2 = 833.3$ mm, $H_s = 468.75$ mm; $m = 120.6$; projected pixel 0.651 mm (0.32 mm at 0.5 m, 0.97 mm at 1.5 m).
3. **Focal length:** $f = D/(1+m) = 8.23$ mm (rule of thumb $T W = 8.29$ mm).
4. **F/#:** $1/(2\sin17°) = 1.71$; entrance pupil diameter $f/N = 4.81$ mm.
5. **Offset & field:** 100 % → $s = H/2 = 1.944$ mm; $r_{\max} = \sqrt{3.456^2 + 3.888^2} = 5.20$ mm; corner field $\arctan(5.20/8.23) = 32.3°$ (25.7° without offset).
6. **Back focal length:** reduced length $2 + 12/1.5098 + 1.1/1.5098 = 10.7$ mm → BFL/f ≈ 1.3: retrofocus needed. Plate focus shift $13.1\times(0.5098/1.5098) = 4.4$ mm.
7. **Plate spherical aberration (if uncompensated):** 12 mm block at F/1.71: marginal transverse aberration ≈ 54 µm (≈ 10 pixels), minimum blur ≈ 27 µm (≈ 5 pixels) → must be balanced by the lens.
8. **Image-quality budget (DMD side):** MTF$_{avg}$(92.6 c/mm) ≥ 50 % nominal (≥ 40 % as built) at 0.75 m; diffraction ceiling 0.83. Distortion ≤ 1 % at $r_{\max}$ (≤ 9.6 pixels), monotonic. Lateral colour 830–870 nm ≤ 0.5 pixel (2.7 µm). Chief-ray angle at DMD ≤ 2°.
9. **Focus and depth:** focus at $L_f = 0.75$ m; DMD-side defocus at 0.5 and 1.5 m ±46 µm → blur 27 µm = 5.0 pixels at F/1.71. Defocus MTF at range ends: 8-pixel fringes 0.59, 16-pixel fringes 0.88 → choose ≥ 12–16-pixel fringes for the coarse-to-fine phase sequence, keep fine binary codes for the middle of the range or drop them.
10. **Keystone alternative:** tilting by 13.2° instead of 100 % offset gives a 1.116 top/bottom width ratio; correcting it digitally wastes ~10 % of the columns at the top and resamples the pattern — rejected.

These ten numbers are the spec you would hand to the optimizer (Task 4–5).

## Key takeaways
- Design projection lenses **in reverse** (screen → DMD): every image-space number is then in DMD µm and directly comparable with the pixel pitch; verify forward with Telecentric Object Space or in NSC.
- The micromirror tilt sets the F/# ceiling: $N_{\min} = 1/(2\sin\theta_t)$ — F/2.4 for 12°, F/1.71 for 17°; going faster costs contrast.
- Telecentric DMD illumination + TIR/RTIR prism ⇒ thick plates in the converging beam (include them from the start; they add overcorrected spherical and focus shift) and a long BFL ⇒ retrofocus, telecentric rear group.
- First order: $f \approx T\,W$; offset $= 2s/H$; offset enlarges the image circle ($r_{\max} = \sqrt{(W/2)^2+(s+H/2)^2}$) but keeps the image rectangular and in focus — tilting creates keystone $\cos(\alpha-\beta)/\cos(\alpha+\beta)$.
- Spec in pixels: MTF ≥ 40 % (as built) at $1/(2p)$, distortion ~1 % (monotonic for calibration), lateral colour < ½–1 pixel, small DMD-side chief-ray angle.
- For structured light the depth of focus dominates: focus at the harmonic mean of the range; blur $b = \delta/N$ with $\delta \approx \tfrac12 f^2(1/L_1-1/L_2)$; choose fringe periods whose defocus MTF stays high at the range ends.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Reverse design | Modelling a projection lens with the screen as object and the SLM as image |
| DMD | Digital micromirror device; array of bistable tilting mirrors (TI DLP) |
| Tilt angle θ_t | Micromirror on/off tilt (±12°, ±17°); sets maximum NA = sin θ_t |
| On/off/flat-state bundle | Light reflected by on-state mirrors (to the lens), off-state mirrors (to a dump), and flat structures (window, gaps) |
| TIR / RTIR prism | Prism pair that separates illumination and projection paths by total internal reflection at a thin air gap (RTIR: reverse TIR variant) |
| Throw ratio T | Lens-to-screen distance / image width |
| Offset | Image position relative to the lens axis; 100 % = image edge on the axis |
| Lens shift | Moving the lens (or DMD) perpendicular to the axis to change offset |
| Keystone | Trapezoidal image distortion from a projector tilted relative to the screen |
| Image circle | Circle at the DMD the lens must cover; grows with offset |
| Telecentric object space | OpticStudio option: entrance pupil at infinity, chief rays parallel to the axis at the object |
| Nyquist (DMD) | $1/(2p)$, the frequency of an on/off column pattern |
| Harmonic-mean focus | Focus distance $2L_1L_2/(L_1+L_2)$ that balances defocus over a depth range |

## References
1. [Geary §20.3, p. 223] — designing from the long to the short conjugate (microscope objective).
2. [Geary §22.7, p. 247] — designing an eyepiece in reverse.
3. [Geary Ch. 23, §23.3–23.6, pp. 251–259] — windows and plates in converging beams: focus shift, spherical aberration, tilt, axial colour.
4. [Geary Ch. 32, §32.2.2, p. 370] — diffractive depth of focus.
5. [Kidger §4.4.2.4.1, pp. 79–80] — distortion, finite-conjugate definition.
6. [Kidger §6.6–6.7, p. 128] — projection lenses mentioned; under/overcorrected sign convention.
7. [Kidger §6.11, pp. 136–137] — conjugate-shift effects.
8. [Kidger Ch. 10, pp. 199–208] — triplets; §10.4 vignetting and corner illumination.
9. Texas Instruments, *DLP System Optics*, DLPA022 — <https://ti.com/lit/pdf/dlpa022>
10. Texas Instruments, *TI DLP® System Design: Optical Module Specifications*, DLPA078 — <https://ti.com/lit/dlpa078>
11. Texas Instruments, *Geometric Optics for DLP*, DLPA044 — <https://edgeworker.ti.com/lit/pdf/dlpa044>
12. Texas Instruments, DLP4710 product page (0.47″ 1080p, 5.4 µm, ±17°) — <https://www.ti.com/product/dlp4710>
13. Ansys Optics KB, image-space telecentric lenses (solve, RANG, EXPP/RECI; Telecentric Object Space) — <https://optics.ansys.com/hc/en-us/articles/42661811743251>
14. Ansys Optics KB, reversing an entire sequential system (KA-01408) — <https://optics.ansys.com/hc/en-us/articles/42661794180115>
15. Zemax Community, *TI DLP DMD projector model* (US_MEMS.DLL and MEMS NSC object) — <https://community.zemax.com/got-a-question-7/ti-dlp-dmd-projector-model-736>
16. Optics for Hire, *Projection lens design* — <https://www.opticsforhire.com/blog/projection-lens-design/>
