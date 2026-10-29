# L09 — Optics for 3D vision: triangulation, stereo baselines and Scheimpflug

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~3 h, tasks ~5 h
> **Prerequisites:** [L01](../L01-image-sensors-and-sampling/)–[L05](../L05-wide-angle-and-distortion-mappings/), [L08](../L08-filters-cover-glass-nir-and-ghosts/); coordinate breaks from Course 02/03 · **Next:** [L10 — Capstone](../L10-capstone-machine-vision-lens/)

## Learning objectives
- Derive the triangulation depth equation $z = fb/d$ and the depth-resolution law $\delta z \approx z^2\,\delta d/(fb)$, and use it to size baseline, focal length and pixel pitch for a depth-accuracy target.
- Explain the structured-light camera as "a stereo pair in which one camera is a projector", and relate phase-shifting depth noise to pattern contrast — and hence to the MTF of *both* the projector and camera lenses.
- Compute the field-of-view overlap, occlusion and toe-in geometry for a given baseline and working range.
- State the Scheimpflug condition ($\tan\theta_i = m\tan\theta_o$; object, lens and image planes meet in a line) and say when a 3D sensor needs it (laser-line triangulation) and when it does not (area structured light).
- Model a tilted object or image plane in OpticStudio (Tilted surface type, coordinate breaks with ray aiming) and optimize the image-plane tilt.
- Specify focus and depth of field of camera and projector over a depth range in terms of pattern contrast rather than "sharpness".

## Reading
- **Core (online):** Teledyne FLIR, "How is depth determined from a disparity image?" — $Z = fB/d$ and the depth error from a disparity error; 0.2 px matching-error rule of thumb: <https://www.teledynevisionsolutions.com/support/support-center/technical-guidance/iis/how-is-depth-determined-from-a-disparity-image/>
- **Core (online):** L. Keselman et al., "Intel RealSense Stereoscopic Depth Cameras" (arXiv:1705.05548) — a clear engineering treatment of stereo depth error, baseline and sub-pixel disparity: <https://arxiv.org/pdf/1705.05548>
- **Core (online):** Zemax Community, "How to tilt object plane in Scheimpflug setup" — Tilted surface type vs coordinate breaks + ray aiming: <https://community.zemax.com/got-a-question-7/how-to-tilt-object-plane-in-scheimpflug-setup-5208>
- **Online:** Ansys Optics KB, coordinate breaks (pickup and position solves, order flag, Tilt/Decenter Elements tool): <https://optics.ansys.com/hc/en-us/articles/42661737698451>; tilting about a pivot point: <https://optics.ansys.com/hc/en-us/articles/43071140327187>
- **Online:** Edmund Optics glossary, "Scheimpflug condition": <https://www.edmundoptics.co.uk/knowledge-center/glossary/scheimpflug-condition/>
- **Optional:** "Noise in structured-light stereo depth cameras: modeling and its applications" (arXiv:1505.01936): <https://arxiv.org/pdf/1505.01936>
- **Optional:** J. Geng, "Structured-light 3D surface imaging: a tutorial", Advances in Optics and Photonics 3, 128–160 (2011) — the standard overview of coding strategies.
- **Background:** [Kenyon §4.5, pp. 83–85] (camera depth of field) and your L02 notes.

---

## 1. Triangulation

### 1.1 Stereo geometry
Two cameras (or a camera and a projector) with parallel optical axes separated by the **baseline** $b$, both with focal length $f$ (in the same units as image coordinates). A point at depth $z$ images at $x_L$ and $x_R$; the **disparity** $d = x_L - x_R$ satisfies, by similar triangles,

$$
z = \frac{f\,b}{d}.
$$

(With $f$ in pixels and $d$ in pixels, $z$ comes out in the units of $b$ — the form used in the Teledyne FLIR note.) Differentiating:

$$
\delta z = -\frac{f b}{d^2}\,\delta d = -\frac{z^2}{f\,b}\,\delta d .
$$

**Depth error grows with the square of distance**, and falls with focal length, baseline and disparity precision. With $\delta d$ in pixels and pitch $p$: $\delta z \approx z^2\,(\delta d\cdot p)/(f b)$.

### 1.2 Numbers
$f = 8$ mm, $p = 3.45$ µm, sub-pixel correspondence precision $\delta d = 0.05$ px:

| $b$ \ $z$ | 0.5 m | 1.0 m | 1.5 m | 2.0 m |
|---|---|---|---|---|
| 100 mm | 0.054 mm | 0.216 mm | 0.485 mm | 0.863 mm |
| 150 mm | 0.036 mm | 0.144 mm | 0.323 mm | 0.575 mm |
| 250 mm | 0.022 mm | 0.086 mm | 0.194 mm | 0.345 mm |

What the optical designer controls in this formula: $f$ (field of view trade), the pixel scale $p$ (sensor choice), and — most directly — $\delta d$, the correspondence precision, which depends on **image contrast, SNR and the stability of the calibration** (L05). A typical stereo matcher achieves ~0.1–0.2 px; phase-shifted structured light reaches a few hundredths of a pixel when contrast is good.

### 1.3 Structured light = active stereo
Replace one camera by a **projector**: it is an "inverse camera" whose pixels (or pattern phase) label rays in space. The camera measures, for each pixel, which projector ray illuminated that scene point (decoded from a sequence of patterns, e.g. Gray codes plus phase-shifted sinusoids). Triangulating the camera ray with the projector ray gives depth by the same geometry; the projector's focal length and pixel pitch play the role of the second camera's, and the projector lens's distortion must be calibrated like a camera's.

With $K$-step phase shifting of a sinusoidal fringe pattern, a common noise model is $\sigma_\phi \approx \sqrt{2/K}\,\sigma_I/B$, where $B$ is the fringe *modulation amplitude* (in electrons) at the camera and $\sigma_I$ the intensity noise. A phase error translates into a correspondence error $\delta d = (P/2\pi)\,\sigma_\phi$, with $P$ the fringe period in camera pixels. Example: $K = 4$, $\sigma_I = 25$ e⁻, $B = 400$ e⁻, $P = 16$ px → $\sigma_\phi = 0.044$ rad, $\delta d = 0.11$ px → $\delta z = 0.32$ mm at 1 m ($f = 8$ mm, $b = 150$ mm).

**This is where lens design enters 3D accuracy directly:** $B$ is the projected fringe modulation multiplied by the projector lens MTF (at the fringe frequency on the object) *and* the camera lens MTF (at the fringe frequency on the sensor), plus the sensor MTF. Halving the system MTF at the fringe frequency halves $B$ and **doubles the depth noise**. The relevant spec is MTF at the pattern frequency over the full depth range — not MTF at Nyquist at best focus.

### 1.4 Baseline trade-offs
Larger $b$ → better depth resolution, but:
- **Occlusion/shadowing:** surfaces seen by the camera but not lit by the projector (or not seen by the second camera) produce holes; grows with $b/z$ and with object relief (bins, boxes).
- **Overlap:** with parallel axes and half horizontal FOV $\theta$, the two fields start to overlap at $z_\text{min} = b/(2\tan\theta)$ and the overlap fraction at depth $z$ is $1 - b/(2z\tan\theta)$. With $\theta = 27.8°$ (8 mm lens, 2/3" sensor): $z_\text{min}$ = 142 mm for $b = 150$ mm; at 1 m the two fields overlap over 86 % of the width. **Toe-in** (converging axes) centres the overlap at the working distance but makes the epipolar geometry non-parallel (handled by rectification) and tilts the depth-of-field regions relative to each other.
- **Size, mass, thermal stability** of the baseline: a bracket that grows by 23.6 ppm/K (aluminium) changes $b$ and therefore the depth scale by the same fraction — mechanics is part of the optical budget (L05 §4.3).

## 2. Focus over a depth range — camera and projector

Area 3D cameras work at fixed focus over a depth range (L02). The question is not "is it sharp?" but "is the **pattern contrast** high enough everywhere?":

- Camera side: blur disc at the range ends $b_c \approx \delta'_c/N_c$ (L02 §5.1); contrast loss at sensor frequency $\nu_s$: $\text{MTF}_\text{defocus} = 2J_1(\pi b_c\nu_s)/(\pi b_c\nu_s)$.
- Projector side: the projector lens defocuses the *projected* pattern on the object in the same way; its blur on the object scales with its own F/# and focus.
- System: $B(z) \propto \text{MTF}_\text{proj}(z)\cdot\text{MTF}_\text{cam}(z)\cdot\text{MTF}_\text{sensor}$ at the pattern frequency.

Example: fringe period 16 px on a 3.45 µm sensor ($\nu_s$ = 18.1 lp/mm). A 9.7 µm camera defocus disc (F/2.8 at the ends of a 0.6–1.2 m range, L02) keeps 96 % contrast at that frequency; even a 30 µm disc keeps 68 %. Coarse patterns tolerate defocus well; the depth-of-field limit is then set by the *finest* pattern used, and by the projector, which usually has the larger aperture (brightness!). This is why pattern design and lens design must be done together.

## 3. The Scheimpflug condition

### 3.1 When the object is a tilted plane
If the plane you need in focus is tilted with respect to the lens — a laser light sheet viewed obliquely, a conveyor belt viewed from the side, a projector throwing onto a floor at an angle — a sensor perpendicular to the optical axis can only be in focus along one line. **Scheimpflug's rule:** the object plane, the lens (principal) plane and the image plane must intersect in a common line. For a thin lens with magnification $m$, if the object plane is tilted by $\theta_o$ from the perpendicular to the axis, the image plane must be tilted by

$$
\tan\theta_i = m\,\tan\theta_o
$$

(in the same rotational sense; verified numerically in the scratch calculation behind Task 1: $f$ = 25 mm, object at 250 mm, $\theta_o$ = 60° → $m$ = 0.111, $\theta_i$ = 10.9°, and both planes cross the lens plane at the same height, 144.3 mm). At small magnification the required image tilt is small even for steep object planes; at $m \approx 1$ it equals the object tilt.

Consequences:
- The magnification varies across the tilted image (keystone/anamorphic distortion) — calibration absorbs it.
- The depth of field becomes a wedge around the object plane (Merklinger's hinge rule describes how the wedge pivots); the CRA at the tilted sensor is asymmetric — check the sensor's CRA acceptance on one side.
- Tilting the sensor (or the lens) needs mechanical design: Scheimpflug adapters, tilted sensor boards.

### 3.2 Where 3D sensors use it
- **Laser-line (sheet-of-light) profilers:** the laser plane is fixed; the camera views it at 20–45°. A Scheimpflug-tilted sensor puts the *entire laser plane* in focus at full aperture — essential for their speed and precision.
- **Area structured-light cameras** (projector + camera with overlapping fields, measuring a volume): there is no single plane to bring into focus, so Scheimpflug is generally *not* used; instead the design relies on depth of field (§2), toe-in, and calibration.
- **Projectors aimed obliquely** at a known plane (e.g. projecting onto a table from the side) can use a tilted pattern panel — the projection version of the same rule (Course 05 L05).

## 4. In OpticStudio

### 4.1 Tilted image plane
- Insert a **Coordinate Break** immediately before the image surface; make its *Tilt About X* a variable (or set it from $\tan\theta_i = m\tan\theta_o$). The image surface then lies in the tilted coordinate system. Turn **ray aiming** on; paraxial calculations ignore coordinate breaks, so judge with real-ray analyses (spot diagram, FFT/Huygens MTF, Field Curvature does not apply to tilted planes — use spot/MTF per field) ([Zemax Community](https://community.zemax.com/got-a-question-7/how-to-tilt-object-plane-in-scheimpflug-setup-5208)).
- Check placement with *Prescription Data → Global Vertex* ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/42661737698451)).

### 4.2 Tilted object plane
- The simplest way is the **Tilted** surface type for the object (or image) surface, which defines a plane tilted about the local axes without coordinate breaks and does not need ray aiming. Note that field heights are then defined in the *projected* (untilted) coordinates, so the actual heights on the tilted plane differ — scale accordingly ([Zemax Community](https://community.zemax.com/got-a-question-7/how-to-tilt-object-plane-in-scheimpflug-setup-5208)).
- Alternative: coordinate breaks after the object with ray aiming; at large object distances you may need to enter approximate pupil-shift values in the ray-aiming settings to help it converge (same thread).

### 4.3 Coordinate-break hygiene
Two CBs per tilted element (tilt, then return), pickup solves to reverse the decenters/tilts, a position solve to keep them co-located, and attention to the *order flag* when combining tilts ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/42661737698451)). The *Tilt/Decenter Elements* tool automates this.

### 4.4 Modelling a triangulation pair
For geometry studies (overlap, ray angles, depth from disparity), the simplest approach is two sequential files or a Multi-Configuration with the camera position as a coordinate break (configuration 1: left camera, configuration 2: right camera, both looking at the same object points). For a projector + camera with a real object scene, non-sequential mode (Course 05 L09) is the natural tool.

## Worked example — sizing a structured-light camera for ±0.15 mm at 1 m

**Target:** depth noise (1σ) ≤ 0.15 mm at $z$ = 1 m. Camera: 2/3" sensor, $p$ = 3.45 µm, $f$ = 8 mm (FOV ≈ 1.05 × 0.88 m at 1 m, L02).

1. **Required $fb/\delta d$:** $\delta z = z^2\,\delta d\,p/(fb)$ → $b/\delta d = z^2 p/(f\,\delta z) = 10^6 \cdot 0.00345/(8 \cdot 0.15) = 2875$ mm/px.
2. **With $\delta d$ = 0.05 px** → $b$ = 144 mm. With $\delta d$ = 0.11 px (the phase-shifting example above, 400 e⁻ modulation) → $b$ = 316 mm — too large for a compact camera.
3. **Lever on $\delta d$:** $\delta d \propto 1/B$. Raising the modulation from 400 to 880 e⁻ (better projector/camera MTF at the fringe frequency, more light, faster lens) brings $\delta d$ to 0.05 px and $b$ back to ~144 mm. Equivalently, a lens whose MTF at the fringe frequency is 0.9 instead of 0.45 halves the required baseline.
4. **Overlap:** $b$ = 150 mm with parallel axes → $z_\text{min}$ = 142 mm, overlap at 1 m = 86 % of the width; toe-in by $\arctan(75/1000) = 4.3°$ per unit to centre the overlap at 1 m.
5. **Thermal:** an aluminium baseline over ±20 K changes $b$ by ±470 ppm → ±0.47 mm depth-scale error at 1 m unless compensated (calibration over temperature, low-CTE bracket, or a thermal model).

## Key takeaways
- $z = fb/d$; $\delta z = z^2\,\delta d/(fb)$ — depth error grows as $z^2$.
- In structured light, $\delta d$ is set by phase noise, $\sigma_\phi \approx \sqrt{2/K}\,\sigma_I/B$, and $B$ is proportional to the product of projector and camera MTF at the pattern frequency — lens MTF converts directly into depth noise.
- Baseline buys resolution but costs occlusion, overlap, size and thermal stability.
- Specify focus over depth in terms of pattern contrast; coarse patterns tolerate defocus, the finest pattern sets the limit.
- Scheimpflug: object, lens and image planes meet in a line; $\tan\theta_i = m\tan\theta_o$. Essential for laser-line profilers, rarely used for area structured light.
- In OpticStudio: CB before the image (ray aiming on, judge with real-ray analyses) or the Tilted surface type; check with Global Vertex.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Baseline $b$ | Distance between the two viewpoints (camera–camera or camera–projector) |
| Disparity $d$ | Difference of image positions of a point in the two views |
| Triangulation | Depth from intersecting two rays from known viewpoints |
| Phase shifting | Projecting $K$ shifted sinusoidal fringes to measure phase per pixel |
| Fringe modulation $B$ | Amplitude of the sinusoidal signal at the camera, in electrons |
| Occlusion / shadowing | Points visible to one view but not the other |
| Toe-in | Converging the optical axes of the two views |
| Scheimpflug condition | Object, lens and image planes intersect in one line |
| Hinge rule | Describes the pivot line of the plane of focus when the lens is tilted |
| Tilted surface | OpticStudio surface type for a tilted plane without coordinate breaks |

## References
1. [Kenyon §4.5, pp. 83–85] — camera depth of field (background for §2).
2. Teledyne FLIR, "How is depth determined from a disparity image?": <https://www.teledynevisionsolutions.com/support/support-center/technical-guidance/iis/how-is-depth-determined-from-a-disparity-image/>
3. L. Keselman, J. I. Woodfill, A. Grunnet-Jepsen, A. Bhowmik, "Intel RealSense Stereoscopic Depth Cameras", arXiv:1705.05548: <https://arxiv.org/pdf/1705.05548>
4. "Noise in structured-light stereo depth cameras: modeling and its applications", arXiv:1505.01936: <https://arxiv.org/pdf/1505.01936>
5. J. Geng, "Structured-light 3D surface imaging: a tutorial", Adv. Opt. Photon. 3, 128–160 (2011).
6. Zemax Community, "How to tilt object plane in Scheimpflug setup": <https://community.zemax.com/got-a-question-7/how-to-tilt-object-plane-in-scheimpflug-setup-5208>
7. Ansys Optics KB, coordinate breaks: <https://optics.ansys.com/hc/en-us/articles/42661737698451> and <https://optics.ansys.com/hc/en-us/articles/43071140327187>
8. Edmund Optics, "Scheimpflug condition" (glossary): <https://www.edmundoptics.co.uk/knowledge-center/glossary/scheimpflug-condition/>
