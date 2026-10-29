# L06 — Real Rays and the Core Analysis Tools

> **Course 01 · Foundations** · Estimated time: lecture ~3 h, tasks ~4–5 h
> **Prerequisites:** [L03](../L03-paraxial-optics-and-ray-tracing/), [L04](../L04-stops-pupils-fields/), [L05](../L05-optical-glass-and-dispersion/) · **Next:** [L07 — Solves, variables and first optimization](../L07-solves-variables-first-optimization/)

## Learning objectives
- Trace a real (exact) meridional ray through a spherical surface by hand (trigonometric method) and explain the vector-refraction algorithm used by ray-tracing software.
- Define transverse ray aberration and wavefront aberration (OPD), and use $\varepsilon_y = -\dfrac{1}{n'\sin U'}\dfrac{\partial W}{\partial \rho_y}$ to move between them.
- Read ray fans, OPD fans and spot diagrams: recognize the signatures of defocus, spherical aberration, coma, astigmatism, field curvature, distortion and chromatic aberration.
- Interpret RMS and GEO spot radius, centroid vs. chief-ray reference, pupil sampling patterns, and compare a spot to the Airy disk.
- Use OpticStudio's core analysis windows (Cross-Section/3D Viewer, Ray Fan, OPD Fan, Standard/Through-Focus Spot, Footprint, Field Curvature/Distortion, Longitudinal Aberration, Lateral Color, Single Ray Trace, Prescription/System Data) and set their key options deliberately.

## Reading
- **Core:** [Geary Ch. 7, §7.1–7.3, pp. 65–76] — ray fan and spot diagram protocols; ray-description of defocus, spherical aberration (caustic, minimum blur), coma (the "ice-cream cone"), astigmatism (tangential/sagittal line foci, medial focus), field curvature and distortion. Skim §7.4–7.6 (pp. 77–83: wavefronts, Seidel polynomial, sine condition) — they are the core of Course 02 L01.
- **Core:** [Kidger Ch. 3, §3.1–3.5, pp. 45–57] — trigonometric meridional ray trace, vector Snell's law, direction cosines, the algebraic ray trace, numerical precision, calculation of OPD relative to a reference sphere.
- **Core:** [Kidger §4.1–4.3, pp. 63–70] — the transverse/wavefront relation in relative pupil coordinates, ray-aberration plots (with the "area under the curve = OPD" estimate and the blur → resolution estimate), spot diagrams.
- **Optional online:** Ansys Optics "How to design a singlet lens – Part 2: Analysis" (Cross-Section, Spot Diagram, OPD Fan, Ray Fan, Quick Focus paths).

---

## 1. From paraxial to real rays

Paraxial rays (L03) give first-order *properties*; real rays give *performance*. A real ray obeys Snell's law exactly at the actual surface shape. The difference between where a real ray lands and where the ideal (paraxial/chief-ray) image point is, *is* the aberration.

### 1.1 The trigonometric meridional trace (hand method)
For a ray in the meridional plane crossing the axis at distance $L$ from the vertex of a sphere of radius $R$ at angle $U$ [Kidger §3.2, pp. 46–48]:

$$
\sin I = \frac{(R - L)}{R}\sin U \;\;(\text{or } \sin I = y/R \text{ for a ray parallel to the axis at height } y),\quad
n'\sin I' = n\sin I,\quad U' = U + I - I',\quad L' = R - \frac{R\sin I'}{\sin U'} .
$$

Then subtract the thickness to get $L$ for the next surface. This was the standard for decades but fails for flat surfaces and objects at infinity, handles only meridional rays, and needs three trig functions per surface.

### 1.2 The algebraic (vector) method used by software
Software represents a ray by a point $(x, y, z)$ and **direction cosines** $(L, M, N)$ — the cosines of the angles with the x, y, z axes, $L^2 + M^2 + N^2 = 1$ [Kidger §3.3.1, p. 50]. At each surface:
1. **Transfer:** intersect the straight ray with the surface (closed form for spheres/conics, iterative for aspheres — L02).
2. **Refract:** with unit surface normal $\mathbf{a}$, vector Snell's law [Kidger Eq. 3.15, p. 50]:
$$
n'\mathbf{r}' = n\mathbf{r} + \mathbf{a}\,(n'\cos I' - n\cos I), \qquad \cos I = \mathbf{r}\cdot\mathbf{a},\quad n'\cos I' = \sqrt{n'^2 - n^2(1-\cos^2 I)} .
$$
3. Repeat to the image surface.

If the square root is negative, the ray is totally internally reflected; if the ray misses the surface, it fails — OpticStudio reports "ray miss" or "TIR" errors. Kidger notes that wavefront errors of 0.1 µm in metre-scale systems need ~10⁷ relative precision, so double precision is mandatory [Kidger §3.4.1, pp. 54–55].

### 1.3 Skew rays, meridional and sagittal sections
Rays in the y–z plane are **meridional** (tangential); all others are **skew**. The **sagittal** section is the plane containing the chief ray perpendicular to the tangential plane [Kidger §4.2, p. 67]. Ray fans sample these two sections; spot diagrams sample the whole pupil.

---

## 2. Two languages for aberration

### 2.1 Transverse ray aberration
Trace a ray from a field point; find where it hits the image surface; subtract the reference point (usually the chief-ray intersection). The result $(\varepsilon_x, \varepsilon_y)$ is the **transverse ray aberration (TRA)** [Kidger §3.1, pp. 45–46]. **Longitudinal** aberration is where the ray crosses the axis (or chief ray) relative to the image plane.

### 2.2 Wavefront aberration (OPD)
Let all rays from an object point travel to a **reference sphere** centred on the reference image point, usually placed at the exit pupil. The optical path difference between a ray and the chief ray at that sphere is the **wavefront aberration** $W$ [Kidger §3.5, pp. 55–57; Geary §7.4.3, p. 79]. A perfect system has $W = 0$ everywhere (equal OPL, Fermat — L01).

### 2.3 The bridge
Rays are normals to the wavefront, so a tilted bit of wavefront sends its ray off target. In relative pupil coordinates $\rho_x, \rho_y \in [-1, 1]$ [Kidger Eqs. 4.7–4.8, p. 65; Geary Eq. 7.7, p. 82]:

$$
\varepsilon_y = -\frac{1}{n'\sin U'}\frac{\partial W}{\partial \rho_y}, \qquad
\varepsilon_x = -\frac{1}{n'\sin U'}\frac{\partial W}{\partial \rho_x},
$$

where $n'\sin U'$ is the image-space NA. Consequences:
- A wavefront term in $\rho^4$ (spherical) gives a ray error in $\rho^3$ — hence "fourth-order wave = third-order ray" naming confusion [Geary §7.5 note, p. 82].
- Conversely, the **area under a ray-fan curve** times the NA estimates the OPD [Kidger Eq. 4.9–4.11, pp. 65–68].
- For the same wavefront error, a faster system (larger NA) has *smaller* ray errors. That is why fast lenses are judged in waves, slow ones in micrometres of spot.

---

## 3. Ray fans

**Protocol** [Geary §7.2.1, pp. 65–66; Kidger §4.2, pp. 65–67]: from one field point, trace rays across the pupil along $P_y$ (tangential fan) and along $P_x$ (sagittal fan). Plot TRA (relative to the chief ray) vs. normalized pupil coordinate. OpticStudio plots $e_y$ vs $P_y$ (tangential) and $e_x$ vs $P_x$ (sagittal) for each field, one curve per wavelength.

**Signatures** (pure aberrations, Geary §7.3, pp. 68–76):

| Aberration | Tangential fan $e_y(P_y)$ | Sagittal fan $e_x(P_x)$ | Spot |
|---|---|---|---|
| Defocus | straight line through origin | same slope | uniform disk |
| Spherical (3rd order) | cubic, odd ("S" when balanced with defocus) | same cubic | round, bright core + halo or ring |
| Coma | parabola (even), same sign both ends | $e_x \approx 0$ (sagittal rays are displaced in *y* by 1/3 of the tangential coma, which the $e_x$ plot does not show) | comet / "ice-cream cone" |
| Astigmatism | straight line | straight line, **different** slope | ellipse/line, rotates through focus |
| Field curvature | both fans tilted together, growing with field | | defocus that grows with field |
| Distortion | no blur (fans flat); chief ray misplaced | | sharp points at wrong height |
| Axial colour | curves for different λ have different slopes (on axis) | | colour-fringed disk |
| Lateral colour | curves for different λ offset vertically (off axis) | | colour streak radially |

Reading tips:
- **Slope at the origin = defocus** relative to the plot's image plane. Quick Focus mostly removes the average slope.
- **Odd vs. even** in $P_y$: even shapes (parabola) = coma-like (asymmetric aberrations); odd shapes = spherical/defocus/astigmatism.
- **Scale!** Always read the axis maximum (OpticStudio prints "Maximum Scale: ±… µm"). Two fans that look identical can differ by 100×.
- Kidger's rule of thumb: the full height of the tangential curve (peak-to-peak blur, say 0.06 mm) gives a rough resolution limit ≈ 1/blur (≈ 16 lp/mm) [Kidger §4.2, p. 67].

## 4. OPD fans and wavefront maps
The **OPD Fan** plots $W$ (in waves) along the same two sections; the **Wavefront Map** shows $W(P_x, P_y)$ over the full pupil (Course 02/03). Use them when the lens is close to diffraction-limited: Rayleigh's quarter-wave criterion (peak-to-valley $W \le \lambda/4$) and the Maréchal criterion (RMS $W \le \lambda/14$) are wavefront criteria (Course 03 L03). Kidger: wavefront plots are most useful when the aberrations are a small fraction of a wavelength [Kidger §4.2, p. 68].

## 5. Spot diagrams
Trace many rays (≈ 100 or more) per field, ideally each carrying equal energy, distributed uniformly over the entrance pupil, and plot their image-plane intersections [Kidger §4.3, pp. 69–70; Geary §7.2.2, p. 67].

- **Patterns:** OpticStudio's Standard Spot Diagram offers *hexapolar* (rings, default), *square* and *dithered* (pseudo-random — avoids pattern artifacts) [Geary Fig. 7.4 shows random, square, triangular, polar grids].
- **RMS radius:** $r_{\text{RMS}} = \sqrt{\langle (x - x_0)^2 + (y - y_0)^2\rangle}$ over all rays (and wavelengths, weighted).
- **GEO radius:** the distance to the farthest ray — very sensitive to a few stray rim rays.
- **Reference point** $(x_0, y_0)$: chief ray (default) or **centroid** (better for asymmetric aberrations such as coma — the eye/sensor sees the centroid), or the middle/vertex.
- **Airy circle:** turn it on; compare its radius $1.22\lambda N_w$ with the spot.
- **Caveats:** spot diagrams ignore diffraction; they do not show *what kind* of aberration you have as clearly as fans [Kidger p. 70]; for near-diffraction-limited lenses use FFT/Huygens PSF and MTF.

Variants: *Through Focus Spot* (spots at several focus positions — shows astigmatic line foci and the caustic), *Full Field Spot*, *Matrix Spot* (fields × wavelengths).

## 6. Other first-day analysis tools

| Tool (Analyze tab unless noted) | Answers | Notes |
|---|---|---|
| Cross-Section / 3D Viewer / Shaded Model (System Viewers) | Does it look sane? Ray clipping, lens collisions, negative edges | Cross-Section only for rotationally symmetric systems |
| Footprint Diagram (Rays & Spots) | Beam footprints of all fields on a chosen surface | Size lenses and filters, check vignetting, place a stop |
| Field Curvature / Distortion (Aberrations) | Sagittal & tangential focus vs field; % distortion | Field-dependent focus → Petzval & astigmatism (Course 02 L04) |
| Longitudinal Aberration | Axial focus vs pupil zone per λ | Spherical + axial colour in one plot |
| Lateral Color | Chief-ray height difference vs field | Lateral colour budget vs pixel size |
| Chromatic Focal Shift | Paraxial focus vs λ | Axial colour (L05) |
| Single Ray Trace (Rays & Spots) | Exact numbers for one ray, real & paraxial | Debugging, checking hand calculations |
| Prescription Data / System Data (Reports) | Full tabulation: surfaces, indices, first-order data, Seidels, global coordinates, edge thickness | Read it every time you finish a step |
| Seidel Coefficients / Diagram | Third-order surface contributions | Course 02 L01, L08 |
| RMS vs Field / RMS vs Focus | Spot or wavefront RMS as a function of field or focus | Location varies by version — search the ribbon |

Professional habit: for every design state, look at **(1) layout, (2) ray fans, (3) spots with Airy circle, (4) field curvature/distortion, (5) system data** before believing any number from the merit function.

---

## 7. In OpticStudio — settings that matter

- **Ray Fan settings:** Plot Scale (0 = auto), Number of Rays, Tangential/Sagittal or both, Wavelength(s), Field(s), Use Dashes, "Check Apertures" (whether vignetted rays are drawn). Aberration is referenced to the chief ray (of the primary wavelength, in the usual setting) at the image surface.
- **OPD Fan settings:** reference sphere at the exit pupil centred on the chief ray image point; units of waves at each wavelength; can be referenced to the centroid in some versions/analyses.
- **Standard Spot Diagram:** Pattern (Hexapolar/Square/Dither), Ray Density (rings or grid size), Reference (Chief Ray/Centroid/Middle/Vertex), Show Airy Disk, Show Scale, Configuration/Wavelength/Field selection. The printed RMS/GEO values depend on Reference and Pattern — state them when you report numbers.
- **Image surface:** analyses are evaluated at the image surface as defined in the LDE (after any solve or Quick Focus). A "best focus" spot is meaningless unless you say how focus was chosen.
- **Settings persistence:** "Save" in an analysis' settings stores them as the default for that analysis type (a `.CFG` file — L01). Session files (`.zda`) remember open windows.
- **Text tab:** every analysis has a Text view with the raw numbers — copy it into Python for your own post-processing (or use the ZOS-API in Course 07).

---

## Worked example — spherical aberration of the Course 01 singlet, three ways

Lens: R = ±102.7, t = 4, N-BK7, EPD 20, d-light ($n = 1.51680$), image at the paraxial focus (BFL = 98.698 mm).

**(a) Real marginal ray by hand.** Ray parallel to the axis at $y = 10$:
- S1: $\sin I = 10/102.7$ → $I = 5.588°$; $\sin I' = \sin I/1.5168$ → $I' = 3.681°$. The ray is bent down by $I - I' = 1.907°$: $U'_1 = -1.907°$.
  Vector form: the surface point is at sag 0.4880 mm; direction cosines after refraction $(L, M, N) = (0, -0.033280, 0.999446)$.
- Transfer: the ray travels 3.0355 mm in glass and meets S2 at $y = 9.8990$ mm (S2 sag −0.4782 mm). Compare the paraxial ray: $y_2 = 9.8673$ mm.
- S2: angle of incidence 7.438°; after refraction $M = -0.100939$, $N = 0.994893$ → $U' = -5.793°$.
- At the paraxial image plane the ray lands at $y = -0.1631$ mm: **transverse spherical aberration TSA = −0.163 mm**. It crosses the axis 1.608 mm before the paraxial focus: **longitudinal SA = −1.61 mm** (undercorrected, typical of a positive singlet).

**(b) Ray-fan shape and spot statistics.** Tracing more pupil heights: $\varepsilon_y(0.5) = -0.0200$, $\varepsilon_y(0.7071) = -0.0568$, $\varepsilon_y(1) = -0.1631$ mm. The ratios to the marginal value, 0.122 and 0.349, are close to $\rho^3$ (0.125 and 0.354): mostly third-order spherical aberration, $\varepsilon_y \approx a\rho^3$ with $a = -0.163$ mm.
For a pure $\rho^3$ blur over a uniformly filled circular pupil, the RMS radius is
$$
r_{\text{RMS}} = |a|\sqrt{\int_0^1 \rho^6\,2\rho\,d\rho} = \frac{|a|}{2} = 81.5\ \mu\text{m},\qquad r_{\text{GEO}} = |a| = 163\ \mu\text{m},
$$
matching a dense, uniform-grid ray trace at paraxial focus (≈ 81 / 163 µm). After refocusing to the minimum-RMS plane the RMS drops to ≈ 27 µm.
*Sampling caveat:* a hexapolar pattern with only a few rings, all rays weighted equally, over-represents the rim, where spherical aberration is largest. A Python trace with 6 hexapolar rings gives ≈ 100 µm RMS for the same lens, 87 µm with 20 rings, converging slowly to 81.5 µm. When a spot RMS matters, increase the ray density until the number stops changing, and quote the pattern.

**(c) Wavefront.** Integrating the ray-fan relation, $W(\rho) = -n'\sin U' \int \varepsilon\, d\rho \approx 0.10 \times 0.163 \times \rho^4/4$ mm ≈ 0.0041 mm ≈ **7 waves** at the pupil edge. An exact OPL calculation to a reference sphere at the exit pupil gives 0.00399 mm = 6.78 waves at $\rho = 1$, 1.69 waves at 0.7071 and 0.42 waves at 0.5 (∝ $\rho^4$ ✓). The sign printed by OpticStudio's OPD fan follows its own convention — note it when you do Task 3. Compared with Rayleigh's λ/4, this lens is ~25× too aberrated to be diffraction-limited at F/5 — consistent with L01's conclusion from spot vs Airy.

---

## Key takeaways
- Real ray tracing = repeated (intersection, vector Snell) steps in double precision; aspheres need iteration; failures are TIR or misses.
- Transverse aberration (µm in the image) and wavefront aberration (waves in the pupil) are linked by $\varepsilon = -(1/\text{NA})\,\partial W/\partial\rho$.
- Ray-fan signatures: line = defocus, cubic = spherical, parabola = coma, different T/S slopes = astigmatism, λ-dependent slopes/offsets = colour.
- Spot diagrams give RMS/GEO size; always state pattern, reference (chief/centroid) and focus; compare with the Airy disk.
- For pure third-order SA at paraxial focus, $r_\text{RMS} = \text{TSA}/2$ and $r_\text{GEO} = \text{TSA}$.
- Footprint, field-curvature/distortion, longitudinal and lateral colour plots complete the first-look toolkit; read the Text tab for numbers.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Real (exact) ray | Ray traced with exact Snell's law and surface shapes |
| Direction cosines (L, M, N) | Components of the unit ray direction |
| Meridional / tangential ray | Ray in the y–z plane |
| Skew ray | Ray not in the meridional plane |
| Sagittal section | Plane through the chief ray perpendicular to the tangential plane |
| TRA (transverse ray aberration) | Ray's image-plane offset from the reference point |
| LSA / TSA | Longitudinal / transverse spherical aberration |
| OPD / wavefront aberration $W$ | Optical-path difference to the reference sphere |
| Reference sphere | Sphere centred on the ideal image point, through the exit pupil |
| Ray fan | TRA vs normalized pupil coordinate in one section |
| OPD fan | $W$ vs normalized pupil coordinate |
| Spot diagram | Image-plane intersections of many rays from one field point |
| RMS / GEO radius | RMS distance / maximum distance of rays from the reference |
| Centroid | Mean ray position |
| Caustic | Envelope of crossing rays near focus |
| Footprint diagram | Beam outline on a surface for each field |

## References
1. [Geary Ch. 7, pp. 65–83] Geary, *Introduction to Lens Design*: §7.2 diagnostic plots, §7.3 ray description of aberrations, §7.4 wavefront aberrations, §7.5 image-plane/exit-pupil connection, §7.6 sine condition.
2. [Kidger Ch. 3, §3.1–3.5, pp. 45–57] Kidger, *Fundamental Optical Design*: trigonometric and algebraic ray tracing, vector Snell's law, direction cosines, precision, OPD calculation.
3. [Kidger §4.1–4.3, pp. 63–70] transverse vs wavefront aberrations, ray-aberration plots, spot diagrams.
4. Ansys Optics, "How to design a singlet lens – Part 2: Analysis" — Cross-Section, Standard Spot Diagram, OPD Fan, Ray Fan and Quick Focus: https://optics.ansys.com/hc/en-us/articles/42661948544787
5. Ansys Innovation Space, "Creating a Singlet: Performance Analysis & Optimization" (video lesson covering the same analysis windows): https://innovationspace.ansys.com/courses/?p=85680
