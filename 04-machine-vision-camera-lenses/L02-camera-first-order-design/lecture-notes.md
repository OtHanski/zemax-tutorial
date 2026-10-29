# L02 — Camera first-order design

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2.5 h, tasks ~4 h
> **Prerequisites:** [L01 — Image sensors and sampling](../L01-image-sensors-and-sampling/), [01/L03 — paraxial optics](../../01-foundations/L03-paraxial-optics-and-ray-tracing/), [01/L04 — stops & pupils](../../01-foundations/L04-stops-pupils-fields/), [03/L03 — depth of focus](../../03-image-quality-optimization/L03-strehl-wavefront-error-depth-of-focus/) · **Next:** [L03 — Relative illumination and telecentricity](../L03-relative-illumination-and-telecentricity/)

## Learning objectives
- Compute the focal length needed for a given sensor and field of view, both for an object at infinity and at a finite working distance.
- Compute magnification, object-space pixel footprint and working F/# at a finite conjugate, and find them in OpticStudio (PMAG, WFNO, EFFL).
- Derive and apply the near/far depth-of-field and hyperfocal-distance formulas with a circle of confusion tied to the pixel size.
- Choose an F/# that balances defocus blur over a required depth range against diffraction, at visible and NIR wavelengths.
- Turn an application requirement (field at distance, resolution, depth range, exposure) into a first-order lens specification.
- Set up a paraxial "camera model" in OpticStudio with multiple object distances (Multi-Configuration Editor).

## Reading
- **Core:** [Kenyon §4.5, pp. 83–85] — cameras: diffraction-limited resolution $\Delta t = 1.22\lambda(f/\#)$ (Eqs. 4.17–4.19) and depth of field (Eqs. 4.20–4.21).
- **Core:** [Geary Ch. 32, §32.2.2–32.2.3, pp. 370–372] — diffractive vs geometric depth of focus; "in imaging arrays the box should be about the pixel size".
- **Optional:** Edmund Optics, "Depth of Field and Depth of Focus": <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/depth-of-field-and-depth-of-focus/>
- **Optional:** commonlands, "Depth of field in machine vision": <https://commonlands.com/blogs/technical/depth-of-field-machine-vision>
- **Refresh:** Course 01 L03 (Gaussian and Newtonian imaging) and L04 (pupils, F/#, NA).

---

## 1. The first-order skeleton of every camera

Before any glass is chosen, a camera lens is fully described to first order by five numbers: **focal length** $f$, **F-number** $N$, **field** (sensor size or field angle), **object distance** (working distance) and the **pupil positions** (which set CRA, L03). Most project disasters in machine vision are first-order mistakes — a field of view that does not cover the part at the shortest working distance, a depth of field that is half of what was promised, a lens that is diffraction limited at a resolution the sensor cannot see — so do this layer carefully, by hand and in Python, before opening OpticStudio.

Throughout, we use thin-lens/principal-plane formulas with the object distance $s > 0$ measured from the front principal plane to the object (a *magnitude*), image distance $v > 0$ from the rear principal plane, and $1/s + 1/v = 1/f$. (In the signed convention of Course 01, the object distance is negative; we drop the sign here because cameras always image a real object to a real image.) The magnification magnitude is $m = v/s$.

## 2. Focal length from field of view

### 2.1 Object at infinity
For a distortion-free ("rectilinear", $h = f\tan\theta$) lens, an image height $h$ corresponds to field angle $\theta$:

$$
\theta = \arctan\frac{h}{f},\qquad \text{FOV} = 2\arctan\frac{h_{\max}}{f}.
$$

Use the half-width, half-height or half-diagonal of the sensor to get horizontal, vertical or diagonal FOV. Example: a 2/3" sensor ($D/2 = 5.51$ mm) and a 60° diagonal FOV need $f = 5.51/\tan 30° = 9.54$ mm. Wide-angle lenses deviate from $f\tan\theta$ (L05), so for FOV > ~70° compute with the real mapping.

### 2.2 Finite working distance
Machine-vision cameras look at objects 0.2–3 m away, where "field of view" means the **size of the object field** $W_o$ covered by a sensor of width $W$:

$$
m = \frac{W}{W_o} = \frac{f}{s-f}\quad\Longrightarrow\quad f = \frac{s\,m}{1+m}.
$$

Example: a 2/3" sensor ($W = 8.45$ mm) must see $W_o = 700$ mm at $s = 1000$ mm: $m = 0.01207$, $f = 11.92$ mm. Note how close this is to $s\,m = 12.07$ mm: at $m \ll 1$ the thin-lens result barely differs from the infinity result, but the *image distance* changes by $v - f = f^2/(s-f)$ — here 0.144 mm, i.e. ~7 depths of focus. You must focus for the working distance, and that refocus is part of the mechanical design (fixed focus, L04).

**Working distance vs object distance.** Customers quote "working distance" from the front of the camera (or the front lens vertex), not from the front principal plane. For a 10 mm lens the difference is a few mm to a few cm — negligible at 1 m, important at 100 mm. State in the spec which one you mean.

### 2.3 Object-space resolution
The object-space footprint of one pixel is $p/m$. With $f = 8$ mm and $p = 3.45$ µm: 0.26 mm at 0.6 m, 0.43 mm at 1.0 m, 0.51 mm at 1.2 m. For a triangulation 3D camera this lateral sampling, together with the baseline, sets the depth resolution (L09).

## 3. F-number, working F-number and light

The F-number for an object at infinity is $N = f/D_{EP}$ ($D_{EP}$ = entrance-pupil diameter). At finite conjugates the cone that actually reaches the image is narrower; the **working F-number** is

$$
N_w = \frac{1}{2\,n'\sin u'} \approx N\left(1 + \frac{m}{m_p}\right),
$$

with $m_p$ the pupil magnification (exit/entrance pupil diameter). For $m \approx 0.01$ the correction is ~1 %, so camera lenses at 1 m behave like infinity lenses; for close-up and metrology lenses ($m \sim 0.1$–1) it matters a lot (L06).

**Image irradiance** on axis for a Lambertian scene of radiance $L$ is

$$
E_0 = \frac{\pi\,T\,L}{4N_w^2}\quad(\text{small angles}),
$$

with $T$ the lens transmittance (derived in L03). Halving $N$ → 4× more light. For a structured-light camera, where the projector's optical power is limited by eye safety and heat, every F-stop is worth a factor of 2 in projector power or exposure time. That is the force pushing toward F/1.8–F/2.8; diffraction and depth of field (below) push back.

## 4. Depth of field

### 4.1 Geometry
Focus the lens on distance $s$. A point at distance $s_1 \ne s$ images at $v_1 \neq v$, so on the sensor it is a blur disc (an image of the pupil) of diameter

$$
b = D_{XP}\frac{|v_1 - v|}{v_1} \approx \frac{|v_1 - v|}{N_w},
$$

[Geary Eq. 32.30; Kenyon Fig. 4.11]. The **depth of field** is the range of $s_1$ for which $b \le c$, the acceptable **circle of confusion** (CoC). Combining with the longitudinal magnification $\Delta s \approx \Delta v\,(s/v)^2$ [Kenyon §4.5] gives Kenyon's one-sided estimate $\Delta s \approx N (s/f)^2 c$ [Kenyon Eq. 4.21], valid when $s$ is well below the hyperfocal distance. (Recompute Kenyon's DSLR example — $f = 50$ mm, $c = 8$ µm, $s = 3$ m, f/8 — yourself in Task 1; his own formula gives about 23 cm, so the 8 cm printed in the text appears to be an arithmetic slip.)

### 4.2 Exact thin-lens formulas and the hyperfocal distance
Define the **hyperfocal distance**

$$
H = \frac{f^2}{N c} + f .
$$

Then the near and far limits of acceptable sharpness for focus distance $s$ (all distances from the front principal plane) are

$$
s_{\text{near}} = \frac{s\,(H-f)}{H + s - 2f},\qquad
s_{\text{far}} = \frac{s\,(H-f)}{H - s}\quad (s<H;\ s_{\text{far}}=\infty \text{ for } s\ge H).
$$

For $s \gg f$ these reduce to $s_\text{near} \approx Hs/(H+s)$ and $s_\text{far}\approx Hs/(H-s)$. Focusing at $s = H$ gives sharpness from $H/2$ to infinity — the classic fixed-focus trick used by inexpensive cameras. Note the asymmetry: more depth behind the focus than in front.

### 4.3 Choosing the circle of confusion
Photographers use $c$ = 0.03 mm for 35 mm film (viewing-based). In machine vision the CoC must come from the **measurement**:

- For edge detection / gauging at full resolution: $c \approx 1$–2 pixels ($p$ to $2p$).
- For colour (Bayer) sensors: $c \approx 2p$ (one colour "super-pixel").
- For a structured-light camera, the relevant question is how much *contrast* of the projected pattern survives at the pattern's spatial frequency $\nu_\text{pat}$ on the sensor. A uniform defocus disc of diameter $b$ has MTF $2J_1(\pi b\nu)/(\pi b\nu)$, which falls to 0 at $\nu = 1.22/b$. Requiring, say, MTF ≥ 0.5 at $\nu_\text{pat}$ gives $b \lesssim 0.7/\nu_\text{pat}$ — a more meaningful "CoC" than a pixel count (Task 4).

### 4.4 Diffraction depth of focus
Even a perfect lens has a finite depth of focus. With Rayleigh's quarter-wave criterion, the image-side depth of focus is

$$
\delta z' = \pm 2\lambda N_w^2
$$

[Geary §32.2.2, Eq. 32.27]. At F/2.8, 0.85 µm: ±13.3 µm. Compare with the geometric depth of focus $\pm N_w c$ [Geary Eq. 32.30 with $c = 2w$]: for $c = 3.45$ µm at F/2.8 that is ±9.7 µm. Both are tiny: the focus tolerance of a fixed-focus F/2.8 camera lens is ±10–15 µm on the sensor side, which drives the mechanical design (active alignment, Course 06 L07) and the thermal design (L07, Course 03 L09).

## 5. F-number versus diffraction and pixel size

The Airy-disc diameter (first zero) is $d_A = 2.44\lambda N$ [Kenyon Eqs. 4.17–4.19]. Rules of thumb:

- If $d_A \lesssim 2p$, the lens can (in principle) deliver good contrast at Nyquist. For $p = 3.45$ µm: $N \lesssim 5.1$ at 0.55 µm, $N \lesssim 3.3$ at 0.85 µm, $N \lesssim 3.0$ at 0.94 µm.
- The L01 table of MTF$_\text{diff}$ at Nyquist is the better tool: decide what MTF you need at Nyquist (or at the pattern frequency) and read off the maximum $N$.

### 5.1 The optimum F-number for a depth range
Suppose the camera must image sharply from $s_n$ to $s_f$. Focus at the **harmonic mean** $s_0 = 2s_ns_f/(s_n+s_f)$ (this splits the image-space defocus evenly). The image-side defocus at both ends is then $\delta' \approx (v_n - v_f)/2$. The total blur at the ends is approximately the root-sum-square of the defocus disc and the diffraction spot:

$$
b_\text{tot}(N) \approx \sqrt{\left(\frac{\delta'}{N}\right)^2 + (2.44\lambda N)^2},
$$

which is minimised when the two terms are equal:

$$
N_\text{opt} = \sqrt{\frac{\delta'}{2.44\,\lambda}},\qquad b_\text{tot,min} = \sqrt{2}\,\frac{\delta'}{N_\text{opt}} .
$$

This is a crude but very useful design rule (RSS of a uniform disc and an Airy spot is only an approximation — verify with through-focus MTF). Note: $N_\text{opt}$ *decreases* with wavelength — an NIR camera wants a faster lens for the same depth range.

## 6. From requirement to first-order specification

A senior engineer's first-order checklist:

1. **Sensor** (L01): $p$, $W\times H$, CRA spec, cover glass.
2. **Field**: object field $W_o \times H_o$ at the *nearest* working distance where the full field is needed (the field grows with distance for a fixed lens). Add margin (5–10 %) for mounting tolerances and distortion.
3. **Focal length**: $f = s\,m/(1+m)$.
4. **Resolution**: object-space pixel $p/m$ at near and far distances; required MTF at $\nu_N$ or the pattern frequency.
5. **Depth range**: $s_n$ to $s_f$ → focus distance, $\delta'$, $N_\text{opt}$ at each wavelength.
6. **Light**: required $N_e$ (SNR) → exposure × irradiance → maximum $N$.
7. **Reconcile**: the light requirement wants a small $N$; depth wants a large $N$; diffraction wants a small $N$. If no $N$ satisfies all three, the requirement must change (shorter $f$ i.e. wider FOV, smaller depth range, larger pixels, more projector power) — better to find this on day one.
8. **Envelope**: total track, diameter, mount/back focus, mass.

## 7. In OpticStudio

**A paraxial camera model.** Before designing real glass, build the system with a *Paraxial* surface (focal length $f$) as the stop: Surface 0 thickness = object distance $s$; field type *Object Height* (in mm) or *Real Image Height* (preferred for sensors); aperture type *Image Space F/#* or *Entrance Pupil Diameter*. Then:

- **System Data / Prescription Data** shows EFL, working F/#, image-space F/#, paraxial magnification, entrance/exit pupil positions.
- Merit-function operands: **EFFL** (effective focal length), **PMAG** (paraxial magnification), **WFNO** (working F/#), **ISFN** (image-space F/#), **EXPP**/**ENPP** (exit/entrance pupil position), **TOTR** (total track). Use them with weight 0 as a "dashboard" in every camera design.
- **Multiple object distances**: in the Multi-Configuration Editor add a THIC operand for surface 0 with configs 600, 800, 1200 mm (near, focus, far). Keep the image distance fixed across configurations. Then the Spot Diagram or FFT MTF of config 1 and 3 show the defocus blur at the depth-range ends directly — the real-lens version of Section 5.1.
- **Through-focus**: the *Through Focus MTF* and *Through Focus Spot* analyses (Analyze → MTF / Rays & Spots groups; location varies by version) show the depth of focus on the image side.
- **Quick Focus** (on the Optimize tab, or Ctrl+Q) focuses for the current configuration only — don't Quick-Focus each configuration separately when you are studying depth of field.

**Pitfall:** with the object at a finite distance, a field type of *Angle* refers to object-space angles at the entrance pupil, and "F/#" in System Data is still the infinity F/#. Use WFNO for exposure and diffraction calculations at close range.

## Worked example — a 3D-camera receiver at 0.6–1.2 m

**Given:** 2/3" sensor, 2448 × 2048, $p = 3.45$ µm ($W = 8.45$ mm, $H = 7.07$ mm); $f = 8$ mm; depth range $s_n = 600$ mm to $s_f = 1200$ mm; wavelengths 0.55 µm and 0.85 µm.

1. **Field of view** ($m = f/(s-f)$):

| $s$ (mm) | 600 | 800 | 1000 | 1200 |
|---|---|---|---|---|
| $m$ | 0.01351 | 0.01010 | 0.00806 | 0.00671 |
| $W_o \times H_o$ (mm) | 625 × 523 | 836 × 699 | 1047 × 876 | 1258 × 1053 |
| pixel footprint (mm) | 0.26 | 0.34 | 0.43 | 0.51 |

2. **Focus distance:** $s_0 = 2\cdot600\cdot1200/1800 = 800$ mm. Image distances: $v_n = 8.1081$, $v_0 = 8.0808$, $v_f = 8.0537$ mm → $\delta' = 27.2$ µm on each side.
3. **Defocus blur at the range ends:** $b = \delta'/N$ = 13.6 µm (F/2), 9.7 µm (F/2.8), 6.8 µm (F/4) — i.e. 2–4 pixels.
4. **Optimum F/#:** $N_\text{opt} = \sqrt{0.0272/(2.44\cdot0.00055)} = 4.5$ at 0.55 µm; $\sqrt{0.0272/(2.44\cdot0.00085)} = 3.6$ at 0.85 µm. The minimum total blur is ≈ 8.5 µm (visible) and ≈ 10.6 µm (NIR): 2.5–3 pixels at the ends of the range.
5. **Conclusion:** a 2:1 depth range at $f = 8$ mm cannot be held to "1-pixel sharpness". Either accept that structured-light patterns use spatial frequencies well below Nyquist (typical: periods of 8–30 pixels), or reduce the range, the focal length, or the pixel count. At F/2.8 (chosen for light), the blur at the range ends is ≈ 2.8 pixels from defocus alone.
6. **Classic DOF for comparison** (focus 1000 mm, F/2.8): with $c = p$: $H = 6633$ mm, sharp from 870 to 1176 mm; with $c = 2p$: $H = 3321$ mm, 770 to 1427 mm.

## Key takeaways
- $f = s\,m/(1+m)$ with $m = W/W_o$; at $m \ll 1$ the focal length is almost the infinity value but focus must still be set for the working distance.
- Use working F/# ($N_w \approx N(1+m/m_p)$) for exposure and diffraction at close range.
- Hyperfocal $H = f^2/(Nc) + f$; near/far limits follow from $H$; depth behind focus exceeds depth in front.
- In machine vision, choose $c$ from the measurement (pixel size, or MTF at the pattern frequency), not from photographic conventions.
- Depth of focus on the sensor side is ±(10–15) µm at F/2.8: fixed-focus lenses need precise, thermally stable focus.
- $N_\text{opt} = \sqrt{\delta'/(2.44\lambda)}$ balances defocus and diffraction; NIR wants a faster lens.
- Do the first-order budget (field, resolution, depth, light) before any glass — it reveals impossible specs early.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Working distance | Distance from the camera/lens front to the object (state the reference!) |
| Magnification $m$ | Image size / object size ($= f/(s-f)$ for a thin lens) |
| Working F/# $N_w$ | $1/(2n'\sin u')$ for the actual conjugate |
| Circle of confusion $c$ | Largest acceptable blur diameter on the sensor |
| Depth of field | Object-space range with blur ≤ $c$ |
| Depth of focus | Image-space range of acceptable focus (geometric $\pm N_w c$, diffractive $\pm2\lambda N_w^2$) |
| Hyperfocal distance $H$ | Focus distance giving sharpness from $H/2$ to infinity |
| Harmonic-mean focus | $s_0 = 2s_ns_f/(s_n+s_f)$, splits image-side defocus equally |

## References
1. [Kenyon §4.5, pp. 83–85] — cameras, diffraction limit (Eqs. 4.17–4.19), depth of field (Eqs. 4.20–4.21, Fig. 4.11).
2. [Geary Ch. 32, §32.2.2–32.2.3, pp. 370–372] — diffractive and geometric depth of focus.
3. Edmund Optics, "Depth of Field and Depth of Focus": <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/depth-of-field-and-depth-of-focus/>
4. Edmund Optics, "Imaging Lab: f-number" (PDF): <https://www.edmundoptics.co.uk/ViewDocument/imaging-lab-f-number.pdf>
5. commonlands, "Depth of field in machine vision": <https://commonlands.com/blogs/technical/depth-of-field-machine-vision>
