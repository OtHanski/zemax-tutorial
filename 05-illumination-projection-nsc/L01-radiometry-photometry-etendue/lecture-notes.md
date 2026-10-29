# L01 — Radiometry, Photometry and Étendue

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3 h, tasks ~4 h
> **Prerequisites:** [Course 01 L04 — stops, pupils, fields, Lagrange invariant](../../01-foundations/L04-stops-pupils-fields/lecture-notes.md) · **Next:** [L02 — Non-sequential fundamentals](../L02-non-sequential-fundamentals/lecture-notes.md)

## Learning objectives
- Name the four radiometric quantities (flux, intensity, irradiance, radiance), their SI units and their photometric twins (lm, cd, lx, nit), and convert between radiometric and photometric quantities using $V(\lambda)$ and 683 lm/W.
- Explain what "Lambertian" means precisely (constant radiance, $I = I_0\cos\theta$, $\Phi = \pi L A$), and compute the fraction of a Lambertian source's flux inside a cone of half-angle $\theta$ ($\sin^2\theta$).
- Compute the irradiance a small source produces on a plane, including the $\cos^4$-type falloff for an off-axis point.
- State the radiance theorem ($L/n^2$ is conserved in a lossless system) and explain why no passive optics can make a source "brighter".
- Compute étendue $G = n^2 A\Omega_{\text{proj}} = \pi n^2 A\sin^2\theta$ for a source and a spatial light modulator (DMD), and decide whether a given LED can fill a given DMD efficiently.
- Relate étendue to the Lagrange invariant of sequential optics.
- Predict which OpticStudio detector quantity (irradiance, intensity, radiance; W or lm) answers a given engineering question.

## Reading
- **Core:** [Kenyon §1.7, pp. 22–25] — radiation terminology, $V(\lambda)$, lumen/candela/lux/nit, Lambert's law and $E = \pi L$ (note the remark on Kenyon's convention in §2 below).
- **Core:** [Kenyon §4.2.2, pp. 77–79] — étendue $T = n^2\Omega A$, invariance through a lens, the law of conservation of radiance.
- **Optional:** [Kenyon §1.8, pp. 26–27] — black-body radiation and Kirchhoff's law (useful background for thermal sources and for understanding why "brightness" has an upper bound).
- **Optional:** [Kenyon §6.9.2, p. 143] — étendue of a grating spectrometer: the same bookkeeping applied to an instrument.
- **Online:** TI, *DLP System Optics* (DLPA022) — how DMD tilt angle sets the usable NA and why lamp étendue should match system étendue: <https://ti.com/lit/pdf/dlpa022>
- **Online:** TI E2E, *DMD etendue* (short PDF from TI's DLP forum) — DMD vs. source étendue, F/2.4 ↔ ±12°: <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/94/DMDEtendue.pdf>

---

## 1. Why a new set of quantities?

Courses 01–04 were about *imaging*: where do rays from one object point go, and how tightly do they meet? The figure of merit was a spot size, a wavefront error or an MTF. In illumination and projection the question changes: **how much light arrives where, from which directions?** A structured-light projector at Zivid has to put a known pattern onto a scene with enough irradiance to beat ambient light and camera noise, with acceptable uniformity, without wasting the LED's output, and without stray light that washes out the dark fringes. None of that is captured by a spot diagram. We need radiometry.

Radiometry is accounting for energy flow. Every quantity is "power per something": per area, per solid angle, or per both. Get comfortable with solid angle first.

### 1.1 Solid angle
A solid angle $\Omega$ (steradian, sr) is the area a cone cuts out of a unit sphere. A full sphere is $4\pi$ sr, a hemisphere $2\pi$ sr. For a right circular cone of half-angle $\theta$:

$$
\Omega = 2\pi(1-\cos\theta) \approx \pi\theta^2 \quad(\theta \ll 1).
$$

A small area $dA$ at distance $r$, tilted by $\theta$ from the line of sight, subtends $d\Omega = dA\cos\theta / r^2$.

We will also need the **projected solid angle**, which weights each direction by $\cos\theta$ (the obliquity of the receiving or emitting surface):

$$
\Omega_{\text{proj}} = \int \cos\theta\, d\Omega = \int_0^{2\pi}\!\!\int_0^{\theta_{\max}} \cos\theta\sin\theta\, d\theta\, d\phi = \pi\sin^2\theta_{\max}.
$$

For a full hemisphere $\Omega_{\text{proj}} = \pi$ (not $2\pi$!). This $\pi$ is where all the $\pi$'s in Lambertian formulas come from.

## 2. Radiometric and photometric quantities

| Radiometric | Symbol | Unit | Definition | Photometric twin | Unit |
|---|---|---|---|---|---|
| Radiant flux (power) | $\Phi_e$ | W | total power | Luminous flux $\Phi_v$ | lumen (lm) |
| Radiant intensity | $I_e$ | W/sr | $d\Phi/d\Omega$ from a (small) source in a direction | Luminous intensity $I_v$ | candela (cd = lm/sr) |
| Irradiance (incident) / exitance (emitted) | $E_e$ / $M_e$ | W/m² | $d\Phi/dA$ on/from a surface | Illuminance $E_v$ | lux (lx = lm/m²) |
| Radiance | $L_e$ | W/(m² sr) | $d^2\Phi/(dA\cos\theta\, d\Omega)$ | Luminance $L_v$ | cd/m² (= nit) |

Notes that save confusion later:

- **"Intensity" is overloaded.** Physicists (and Kenyon §1.7) often say "intensity" for W/m². In radiometry and in OpticStudio, *intensity* means W/sr, and W/m² is *irradiance*. When you read OpticStudio's detector output "Radiant Intensity", it is W/sr; "Incoherent Irradiance" is W/m² (or lm/m² = lux in photometric mode).
- **Intensity only makes sense for a source that is small compared with the viewing distance** (far field). For an LED viewed from 1 m it is fine; for a diffuser 50 mm away from your detector it is not — use radiance.
- **Radiance is the fundamental quantity.** It describes a single "ray bundle": how much power flows through a small area into a small cone. Everything else is an integral of radiance over area and/or angle. The $\cos\theta$ in the definition means radiance is per unit *projected* area perpendicular to the ray.
- **Spectral quantities** carry a "per wavelength" subscript: $\Phi_{e,\lambda}$ in W/nm, $L_{e,\lambda}$ in W/(m² sr nm), and the total is $\Phi_e = \int\Phi_{e,\lambda}d\lambda$ [Kenyon eqn 1.29].

### 2.1 Photometry: weighting by the eye
Photometric quantities are radiometric quantities weighted by the CIE photopic luminous efficiency function $V(\lambda)$, which peaks at 555 nm with value 1:

$$
\Phi_v = 683\ \tfrac{\text{lm}}{\text{W}} \int \Phi_{e,\lambda}(\lambda)\,V(\lambda)\,d\lambda .
$$

The constant 683 lm/W is the definition of the lumen (1 W at 555 nm ≡ 683 lm) [Kenyon §1.7, p. 23]. Kenyon folds the 683 into his $V_\lambda$ (his Fig. 1.18 is plotted in lm/W); most standards keep $V$ dimensionless and write the 683 explicitly. Night (scotopic) vision has its own curve peaking near 507 nm (Kenyon quotes ~1700 lm/W).

**Why this matters at Zivid:** $V(\lambda)$ is essentially zero beyond ~750 nm. An 850 nm or 940 nm projector LED with 1 W optical output has *zero* lumens — photometric units are meaningless for NIR projectors. For visible (e.g. blue/white) projectors, datasheets often quote lumens or candela, and you must convert back to watts to do a camera SNR budget, since your sensor counts photons, not lumens. Always work in **watts (and photons)** for machine vision; use photometric units only when talking to people who think in lumens, or when eye-safety/glare for human operators matters.

A quick photon conversion: the photon energy is $hc/\lambda$, so 1 W at 850 nm is $1/(6.626\times10^{-34}\cdot 2.998\times10^{8}/850\times10^{-9}) = 4.28\times10^{18}$ photons/s.

### 2.2 Relations for a small source
For a small source of intensity $I(\theta)$, the irradiance on a surface at distance $r$, whose normal makes angle $\alpha$ with the line to the source, is the **inverse-square / cosine law**:

$$
E = \frac{I(\theta)\cos\alpha}{r^2}.
$$

The total flux is $\Phi = \int I\, d\Omega$; for an isotropic point source $\Phi = 4\pi I$ [Kenyon eqn 1.32 and text].

## 3. Lambertian sources

A **Lambertian** (perfectly diffuse) emitter or reflector has **radiance independent of direction**: it looks equally bright from every angle. Because the projected area of the emitter shrinks as $\cos\theta$, its intensity falls off as

$$
I(\theta) = I_0\cos\theta, \qquad I_0 = L A,
$$

where $A$ is the emitting area. Integrating over the forward hemisphere with the projected solid angle from §1.1:

$$
\Phi = L A\,\pi = \pi I_0, \qquad M = \Phi/A = \pi L .
$$

> **Convention warning.** Kenyon writes Lambert's law as $L_v(\theta) = L_v(0)\cos\theta$ [Kenyon eqn 1.33]. There "luminance" is being taken per unit *emitting-surface* area rather than per unit projected area, so his $L_v(\theta)$ behaves like our intensity per unit area. His result $E_v = \pi L_v(0)$ [eqn 1.34] — which he labels illuminance but which is really the luminous *exitance* (flux leaving unit area of the source) — agrees with $M = \pi L$ above. In this course (and in OpticStudio) radiance is per unit projected area, so a Lambertian source has **constant** radiance and **cosine** intensity.

Good real-world approximations: matte white surfaces (Spectralon, white paint), opal diffusers, and the bare die of many LEDs (planar surface emitters are close to Lambertian; domed or lensed LEDs are not — their intensity patterns are in the datasheet and we model them in [L03](../L03-source-modeling-leds-and-lasers/lecture-notes.md)).

### 3.1 How much of a Lambertian source can a lens collect?
The flux inside a cone of half-angle $\theta$ about the normal is

$$
\frac{\Phi(\theta)}{\Phi_{\text{total}}} = \frac{\pi L A\sin^2\theta}{\pi L A} = \sin^2\theta .
$$

This one formula explains a lot of illumination design:

| Collection half-angle | 17° | 30° | 45° | 60° | 90° |
|---|---|---|---|---|---|
| Fraction of Lambertian flux | 8.5 % | 25 % | 50 % | 75 % | 100 % |

A condenser lens working at F/1 collects only 20–25 % of a bare Lambertian LED (20 % if you take the paraxial definition $N = 1/(2\tan\theta)$, i.e. $\theta = 26.6°$; 25 % if you use the aplanatic definition $N = 1/(2\sin\theta)$, i.e. $\theta = 30°$ — illumination engineers usually mean the latter, and so does TI when it quotes DMD F-numbers below). That is why LED collimators are TIR "cups" or very fast aspheric condensers (half-angles of 60–80°) — topic of [L04](../L04-illumination-optics-collimators-condensers/lecture-notes.md).

### 3.2 Irradiance on a plane from a Lambertian source facing it
Put a small Lambertian source at height $d$ above a plane, facing it. A point on the plane at angle $\theta$ off-axis is at distance $r = d/\cos\theta$, sees intensity $I_0\cos\theta$, and is hit at obliquity $\cos\theta$:

$$
E(\theta) = \frac{I_0\cos\theta\cdot\cos\theta}{(d/\cos\theta)^2} = \frac{I_0}{d^2}\cos^4\theta .
$$

This is the illumination cousin of the cos⁴ law you meet for camera relative illumination in [Course 04 L03](../../04-machine-vision-camera-lenses/L03-relative-illumination-and-telecentricity/lecture-notes.md). At 30° it is 56 %, at 60° only 6 %: a bare LED is a terrible way to illuminate a flat scene uniformly.

## 4. Conservation of radiance

Follow a thin bundle of rays through a lossless optical system. In medium $n_1$ it passes area $dA_1$ into projected solid angle $d\Omega_1$; after the system it passes $dA_2$ into $d\Omega_2$ in medium $n_2$. Two facts:

1. Energy is conserved: $d\Phi_1 = d\Phi_2$ (minus absorption/reflection losses).
2. The geometric quantity $n^2\, dA\, d\Omega_{\text{proj}}$ is invariant along the bundle (this is Liouville's theorem / the Lagrange invariant in two dimensions — shown for paraxial imaging in [Kenyon §4.2.2, pp. 78–79]).

Dividing, the **basic radiance** $L/n^2$ is invariant:

$$
\frac{L_1}{n_1^2} = \frac{L_2}{n_2^2}\quad\text{(lossless)}, \qquad \frac{L_2}{n_2^2} \le \frac{L_1}{n_1^2}\quad\text{(real)}.
$$

Consequences you will use constantly:

- **A lens cannot increase brightness.** The image of an LED die has (at most) the radiance of the die. A lens can *concentrate flux onto a smaller area* only by spreading it into a larger angle — and that angle is limited (by 90°, or by the acceptance of the next component).
- **Image irradiance depends only on radiance and the cone angle:** an image of a Lambertian object of radiance $L$ formed by a cone of half-angle $\theta'$ has irradiance $E' = \pi L\,\tau\sin^2\theta'$ ($\tau$ = transmission). In F-number terms $E' \approx \pi L\tau/(4N^2)$ — the camera exposure equation in disguise.
- Kenyon's "white cliffs of Dover" example [Kenyon §1.7, p. 25]: an extended object looks equally bright at any distance, because the area seen and the solid angle collected scale oppositely.
- For a **point** (unresolved) source étendue is undefined and "bigger aperture is always better" [Kenyon §4.2.2, p. 79]. Lasers are the practical near-point source: tiny étendue, which is why laser projectors can use small, slow optics (see [L03](../L03-source-modeling-leds-and-lasers/lecture-notes.md)).

## 5. Étendue

### 5.1 Definition
The **étendue** (French: "extent"; also throughput, geometric extent, *T* in Kenyon) of a beam is

$$
G = n^2\int\!\!\int \cos\theta\, dA\, d\Omega = n^2 A\,\Omega_{\text{proj}} .
$$

For a flat aperture of area $A$ accepting a uniform circular cone of half-angle $\theta$ at every point:

$$
\boxed{G = \pi n^2 A\sin^2\theta = \pi A\,\mathrm{NA}^2}
$$

Units: mm² sr (most common in illumination). Kenyon writes $T = n^2\Omega A$ and, for small angles, $T = \pi\,\mathrm{NA}^2 A$ [Kenyon eqns 4.11–4.13]. The exact projected-solid-angle form uses $\sin^2\theta$ and is exact at any angle for a Lambertian-filled cone; using the geometric solid angle $2\pi(1-\cos\theta)$ instead is a common (small) error at large angles. For a Lambertian emitter into the full hemisphere ($\theta = 90°$): $G = \pi A$.

Total flux through a system is $\Phi = L\,G$ (for uniform radiance) [Kenyon eqn 4.14] — étendue is literally the "size of the pipe", and radiance is the "pressure".

### 5.2 Étendue is conserved — so it is a budget
In a lossless system étendue cannot decrease (it can increase through scattering, diffusers, aberrations and mismatch — like entropy). Every component has an **acceptance étendue**: the DMD, the projection lens, a light pipe, a fibre. Rules of thumb:

- If $G_{\text{source}} \le G_{\text{system}}$, a well-designed condenser can (in principle) collect nearly all the light.
- If $G_{\text{source}} > G_{\text{system}}$, the best possible efficiency is roughly $G_{\text{system}}/G_{\text{source}}$; a *bigger* LED does not help once you are étendue-limited — only a *higher-radiance* one does.
- Matching shapes matters: a round cone into a rectangular DMD, or a square LED into a 16:9 DMD, wastes étendue unless the illumination optics reshape it (light pipes and fly's-eye homogenizers do this, [L04](../L04-illumination-optics-collimators-condensers/lecture-notes.md)).

### 5.3 Link to the Lagrange invariant
In [Course 01 L04](../../01-foundations/L04-stops-pupils-fields/lecture-notes.md) you met the Lagrange invariant $H = n u \bar{y} - n\bar{u}y$; at an image plane $H = n u h$ (marginal-ray angle × image height). For a circular field of radius $h$ and a cone of (paraxial) half-angle $u$:

$$
G = \pi h^2 \cdot \pi (n u)^2 = \pi^2 H^2 .
$$

So étendue is the squared Lagrange invariant (per two transverse dimensions). A projection lens, a condenser and a camera lens all have an étendue; it is the single number that says how much light the system *can* handle, independent of focal length.

### 5.4 Étendue of a DMD
A DMD micromirror tilts by ±$\theta_t$ (12°, 14.5° or 17° depending on the device). The "on" light is deflected by $2\theta_t$ from the "off"/flat-state light, so to keep the illumination cone, the on-state projection cone and the off-state cone from overlapping, each cone's half-angle must be ≲ $\theta_t$. TI's application notes tie the native illumination F-number to the tilt: ±12° ↔ F/2.4, ±17° ↔ F/1.7 [TI DLPA022; TI DLPA083]. Check: $N = 1/(2\sin\theta_t)$ gives $N = 2.40$ for 12° and $1.71$ for 17°.

The DMD acceptance étendue is therefore

$$
G_{\text{DMD}} \approx \pi\, A_{\text{DMD}}\,\sin^2\theta_t .
$$

TI frames this as "Matching the lamp etendue to the system etendue is the goal for maximum efficiency" [TI DLPA022 §3.1.1]. Using a larger cone (faster than the native F/#) gives more light but reduces contrast, because off-state and flat-state light start to leak into the projection pupil — a trade you will quantify in [L09](../L09-capstone-structured-light-projector/lecture-notes.md).

### 5.5 Étendue at the other end: the projection lens and the scene
The same budget runs forward. The projection lens images the DMD onto the scene at magnification $|m| \gg 1$; the image area grows by $m^2$ while the cone half-angle shrinks so that $\pi A\sin^2\theta$ is unchanged. Two practical consequences for a structured-light projector:

1. **Lens speed is fixed by the DMD, not chosen freely.** The projection lens must accept at least the DMD's on-state cone (F/1.7 for a ±17° device). Making it faster does not add light (the illumination does not fill a bigger cone) but does admit more flat-state and off-state stray light, lowering contrast (TI DLPA022 discusses exactly this trade).
2. **Scene irradiance is a flux budget, not an étendue problem.** Once the light is on the DMD, scene irradiance is simply $E_{\text{scene}} \approx \Phi_{\text{on DMD}}\,\tau_{\text{DMD}}\,\tau_{\text{lens}}/A_{\text{scene}}$, with $A_{\text{scene}}$ the projected-image area. Doubling the working distance quarters the irradiance (inverse-square in disguise: $A_{\text{scene}}\propto z^2$).

### 5.6 From watts to photo-electrons
Machine-vision budgets end in electrons. For a Lambertian scene of reflectance $\rho$ under irradiance $E$, the scene radiance is $L = \rho E/\pi$; the camera image irradiance is $E' = \pi L\tau/(4N^2) = \rho E\tau/(4N^2)$ (paraxial, on-axis, ignoring $\cos^4$). A pixel of area $a_p$ integrating for time $t$ collects
$$
N_e = \eta\,\frac{E' a_p t}{hc/\lambda}
$$
electrons, where $\eta$ is the quantum efficiency. You will do this calculation at the end of [Task 1](tasks.md) and again in the capstone [L09](../L09-capstone-structured-light-projector/lecture-notes.md); it is the link between this course and the sensor material in [Course 04 L01](../../04-machine-vision-camera-lenses/L01-image-sensors-and-sampling/lecture-notes.md).

## 6. In OpticStudio

How these concepts map to the software (details in [L02](../L02-non-sequential-fundamentals/lecture-notes.md)):

- **Units.** *Setup → System Explorer → Units*: source units (Watts, Lumens, Joules) and analysis units (W/cm², W/m², etc.). Pick watts and mm/m consistently. Photometric output for an NIR source is zero by definition — if your detector shows 0 lm for an 850 nm source, that is physics, not a bug.
- **Sources** in the Non-Sequential Component Editor are specified by *# Layout Rays*, *# Analysis Rays* and **Power (W)** (or lm). Power is the total emitted flux, not intensity. Many NSC sources (Source Ellipse, Source Rectangle, …) have a *Cosine Exponent* parameter: cosine exponent 1 gives a Lambertian intensity $I\propto\cos\theta$; higher exponents give narrower $\cos^n$ patterns (L03).
- **Detectors.** *Detector Rectangle* records incoherent irradiance (W/area) and can also display radiant intensity (W/sr, far-field angular data). *Detector Polar* records intensity vs. angle on a sphere — the natural tool for "what is the LED's $I(\theta)$". The *Detector Viewer* (Analyze tab) shows these; radiance-type outputs exist on some detectors (check *Show Data* options in your version). Ansys's introductory article on detectors notes the default 100 × 100 pixels, that results accumulate from traced rays, and that statistical noise per pixel scales as $1/\sqrt{N_{\text{rays/pixel}}}$ — e.g. 10 × 10 pixels with 100 000 rays ≈ 3 % noise ([Ansys Optics: detectors in illumination systems](https://optics.ansys.com/hc/en-us/articles/42661774340243)).
- **Edition note.** Everything non-sequential (NSC Editor, sources, detectors, Ray Database) needs a Professional or Premium licence (it is not in the Standard edition); with Premium every NSC feature used in this course is available.
- **Étendue is not a button.** OpticStudio has no "étendue" analysis; you compute it by hand from source area and angular distribution, or verify it numerically by putting detectors in space and angle (task 4).
- **Pitfall — the "intensity" of an extended source.** A Detector Rectangle placed 50 mm from a 5 mm diffuser and switched to "Radiant Intensity" shows the angular distribution of rays hitting it, which is only the source intensity in the far field. Put the detector far away (≥ 10× the source size is a common rule of thumb) or use a polar detector.

## Worked example

### Part A — a white LED (photometric)
A white LED emits $\Phi_v = 100$ lm from a 1 mm × 1 mm Lambertian die.

- On-axis intensity: $I_0 = \Phi/\pi = 31.8$ cd.
- Luminance: $L = I_0/A = 31.8/(10^{-6}\ \text{m}^2) = 3.18\times10^{7}$ cd/m² — about 3000× a sunlit white wall (~10⁴ cd/m², Kenyon p. 24).
- Illuminance 1 m away on axis: $E = 31.8$ lx (dim indoor level — bare LEDs do not illuminate distant scenes well).

### Part B — an 850 nm NIR LED (radiometric)
Same 1 mm² die, $\Phi_e = 1.0$ W at 850 nm.

- $I_0 = 1/\pi = 0.318$ W/sr. Radiance $L = 0.318$ W/(mm² sr) = $3.18\times10^5$ W/(m² sr).
- Irradiance on a plane 0.5 m away, facing the LED: $E(0°) = 0.318/0.25 = 1.27$ W/m²; at 30° off-axis: $1.27\cos^4 30° = 0.72$ W/m²; at 60°: 0.080 W/m².
- Luminous flux: 0 lm ($V(850\text{ nm}) \approx 0$).

### Part C — can this LED fill a DMD?
DMD: TI DLP3010-class, 0.3-inch, 1280 × 720 mirrors at 5.4 µm pitch, ±17° tilt ([TI DLP3010 product page](https://www.ti.com/product/DLP3010)).

- Active area: $6.912 \times 3.888$ mm = 26.87 mm² (diagonal 7.93 mm ✓ "0.3 inch").
- Native illumination F/#: $1/(2\sin17°) = 1.71$.
- DMD étendue: $G_{\text{DMD}} = \pi\cdot 26.87\cdot\sin^2 17° = \pi\cdot26.87\cdot0.0855 = 7.22$ mm² sr.
- LED étendue (Lambertian, full hemisphere): $G_{\text{LED}} = \pi\cdot A$.

| LED die | $G_{\text{LED}}$ (mm² sr) | Best-case efficiency $\min(1, G_{\text{DMD}}/G_{\text{LED}})$ |
|---|---|---|
| 1 × 1 mm | 3.14 | 100 % (étendue-wise; real losses still apply) |
| 2 × 2 mm | 12.57 | 57 % |
| 3 × 3 mm | 28.27 | 26 % |

The largest Lambertian emitting area this DMD can in principle accept is $7.22/\pi = 2.30$ mm². Note how a 3 × 3 mm "more powerful" LED delivers, at best, only $9 \times 0.26 \approx 2.3$ times the flux of the 1 mm² LED... and only if it has the same radiance. In practice the shape mismatch (square LED, 16:9 DMD, circular pupil) loses another 10–30 %, which is why the 1 mm² case will not reach 100 % either.

Reproduce every number in this example yourself in [Task 1](tasks.md) — it is a ten-line Python script.

## Key takeaways
- Radiance $L$ (W m⁻² sr⁻¹) is the fundamental quantity; flux, intensity and irradiance are integrals of it. In OpticStudio, "intensity" means W/sr.
- Photometric = radiometric × 683 lm/W × $V(\lambda)$; NIR sources have zero lumens. Do machine-vision budgets in watts/photons.
- Lambertian = constant radiance, $I = I_0\cos\theta$, $\Phi = \pi L A$, fraction into a cone = $\sin^2\theta$.
- $L/n^2$ is conserved; passive optics cannot make a source brighter, only trade area for angle.
- Étendue $G = \pi n^2 A\sin^2\theta$ is conserved (or grows); it equals $\pi^2 H^2$ (Lagrange invariant squared).
- A DMD's étendue is set by its area and its mirror tilt (native F/# = $1/(2\sin\theta_t)$); once the source étendue exceeds it, extra LED area buys nothing.
- Statistical noise in Monte-Carlo NSC detectors scales as $1/\sqrt{N}$ rays per pixel — choose pixel count and ray count together.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Radiant flux $\Phi$ | Total optical power, W |
| Radiant intensity $I$ | Power per unit solid angle from a small source, W/sr |
| Irradiance $E$ / exitance $M$ | Power per unit area incident on / leaving a surface, W/m² |
| Radiance $L$ | Power per unit projected area per unit solid angle, W/(m² sr) |
| Lumen, candela, lux, nit | Photometric units of flux, intensity, illuminance, luminance |
| $V(\lambda)$ | CIE photopic luminous efficiency function (peak 1 at 555 nm) |
| Lambertian | Radiance independent of direction; $I\propto\cos\theta$ |
| Projected solid angle | $\int\cos\theta\,d\Omega$; $\pi\sin^2\theta$ for a cone, $\pi$ for a hemisphere |
| Étendue $G$ | $n^2\int\cos\theta\,dA\,d\Omega$; "size" of a beam in phase space, mm² sr |
| Basic radiance | $L/n^2$, invariant along a lossless ray bundle |
| DMD tilt angle | Mirror rotation (±12°, ±17° …) that sets the DMD's native F/# |

## References
1. [Kenyon §1.7, pp. 22–25] — radiation terminology, photometry, Lambert's law.
2. [Kenyon §1.8, pp. 26–27] — black-body radiation, Kirchhoff's law.
3. [Kenyon §4.2.2, pp. 77–79] — étendue and conservation of radiance.
4. [Kenyon §6.9.2, p. 143] — étendue of a grating spectrometer.
5. Texas Instruments, *DLP System Optics*, application report DLPA022 — <https://ti.com/lit/pdf/dlpa022> (tilt angle ↔ maximum NA, étendue matching, contrast vs. illumination angle).
6. Texas Instruments, *DMD Optical Efficiency for Visible Wavelengths* (DLPA083), on-state fill factor table with native F/# per tilt — <https://ti.com/document-viewer/lit/html/DLPA083B/GUID-A957AE9D-7027-4283-93A6-86CF18D0D65A>
7. TI E2E forum attachment, *DMD etendue* — <https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/94/DMDEtendue.pdf>
8. Texas Instruments, DLP3010 product page (array size, pitch, tilt) — <https://www.ti.com/product/DLP3010>
9. Ansys Optics, introductory article on detectors in illumination systems (Detector Rectangle, ray-count noise) — <https://optics.ansys.com/hc/en-us/articles/42661774340243>
10. Edmund Optics, *Illumination Design Using Ansys Zemax OpticStudio* (application note, overview of NSC illumination workflow) — <https://www.edmundoptics.com/knowledge-center/application-notes/illumination/illumination-design-using-ansys-zemax-opticstudio/>
