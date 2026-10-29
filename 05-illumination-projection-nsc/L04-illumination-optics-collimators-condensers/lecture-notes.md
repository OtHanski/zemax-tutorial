# L04 — Illumination Optics: Condensers, Köhler Illumination, Homogenizers and TIR Collimators

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3.5 h, tasks ~5 h
> **Prerequisites:** [L01](../L01-radiometry-photometry-etendue/lecture-notes.md) (étendue), [L02](../L02-non-sequential-fundamentals/lecture-notes.md) (NSC basics), [L03](../L03-source-modeling-leds-and-lasers/lecture-notes.md) (sources) · **Next:** [L05 — Projection lens design](../L05-projection-lens-design/lecture-notes.md)

## Learning objectives
- Explain critical and Köhler illumination with a ray diagram, and predict how source non-uniformity appears on the target in each.
- Design a condenser for a given source and target using étendue and the Lagrange invariant: collection angle, magnification, cone angle at the target.
- Size a two-array fly's-eye (lenslet) homogenizer: lenslet pitch and focal length, condenser focal length, acceptance angle, channel count.
- Size a light pipe (integrating rod), including a tapered rod that converts area into angle, and the relay that images its exit face onto a DMD.
- Explain how a TIR collimator works and compute the étendue limit on its output divergence.
- Model these components in OpticStudio NSC (Lenslet Array, Rectangular Volume, Standard Surface/Lens, detectors) and evaluate efficiency and uniformity.

## Reading
- **Core:** [Kenyon §4.4, pp. 81–83] — the microscope condenser and **Köhler illumination**: independent control of illuminated area (field stop) and NA (aperture stop); "light from each point on the source forms a parallel beam at the object", so the illumination is uniform whatever the source brightness variations (his Fig. 4.10).
- **Core:** [Kenyon §4.7–4.8, pp. 92–93] — aspheric condenser lenses (NA up to ~0.75) and Fresnel lenses as cheap large-area condensers.
- **Core (online):** Ansys Optics KB, *Fly's eye array homogenizers for digital projector illumination* — Lenslet Array objects, channel-count rules, uniformity optimization: <https://optics.ansys.com/hc/en-us/articles/42661744169363>
- **Core (online):** Texas Instruments, *DLP System Optics* (DLPA022) — rod vs. fly's-eye integrators, overfill, telecentric vs. non-telecentric DMD illumination, TIR prisms: <https://ti.com/lit/pdf/dlpa022>
- **Optional:** Ansys Optics KB, tutorial on basic operations in Non-Sequential Mode (parabolic reflector + light pipe example): <https://optics.ansys.com/hc/en-us/articles/42661713082899>
- **Optional:** [Kidger Ch. 10] is about photographic objectives, but its discussion of vignetting and illumination of the image corner ([Kidger §10.4, p. 206]) is a useful reminder that the *projection* lens's relative illumination adds to the illumination system's non-uniformity (L05).

---

## 1. What an illumination system must deliver

For a projector the illumination system ("illumination engine") sits between the source and the spatial light modulator (SLM — DMD, LCoS, LCD, or a fixed slide/mask). Its specification is about **where** and **from which directions** light arrives:

1. **Irradiance uniformity** over the SLM (e.g. ≥ 90 % min/max, or ≤ 3 % RMS variation), plus a small **overfill** margin so alignment tolerances do not darken the edges.
2. **Angular distribution** at every SLM point: a cone (or a rectangle) of light with a defined centre direction (the chief ray) and half-angle — matched to the SLM (DMD tilt, L01 §5.4) and to the projection lens's entrance pupil (L05). If the chief-ray direction is the same everywhere, the illumination is **telecentric**.
3. **Efficiency**: flux on the active area divided by source flux. Étendue sets the upper bound (L01); Fresnel losses, absorption, overfill and pupil mismatch set the rest.
4. **Robustness**: insensitive to source-to-source variation (LED binning, die layout) and to alignment.

The two classical layouts differ in which plane of the source is imaged onto the SLM.

## 2. Critical vs. Köhler illumination

```
CRITICAL:   source ──► condenser ──► SLM (= image of source)
            [source structure appears on the SLM]

KÖHLER:     source ──► collector ──► (source image in condenser aperture / projection pupil)
                         field stop ──► condenser ──► SLM (= image of field stop)
            [each source point → parallel beam over the whole SLM]
```

**Critical illumination** images the source onto the target. Simple and efficient when the source shape already matches the target, but every source non-uniformity — electrode pads on an LED die, the gaps between VCSEL emitters, a lamp filament — is reproduced on the SLM and therefore projected onto the scene. It is used when the source itself is uniform (e.g. the exit face of a light pipe is a uniform "source").

**Köhler illumination** images the source into the **pupil** of the condenser (and, through it, into the entrance pupil of the projection lens), while the SLM sits in a plane conjugate to a field stop. Kenyon's microscope description captures the advantages [Kenyon §4.4, pp. 81–83]: the field stop sets the illuminated area, the aperture stop sets the NA, and since every source point produces a parallel beam filling the field, the field is uniform regardless of source structure. In Fourier-optics language: the SLM lies in the Fourier plane of the source, so the *spatial* structure of the source becomes *angular* structure at the SLM — which the projection lens does not image.

Practical consequences:

| | Critical | Köhler |
|---|---|---|
| Source structure on target | yes | no (becomes angular structure) |
| Field and NA separately adjustable | no | yes (field stop, aperture stop) |
| Typical use | rod-exit relays; simple spotlights | microscopes, lithography, fly's-eye projectors |
| Telecentric illumination | needs extra field lens | natural if the aperture stop is at the condenser's front focal plane |

Real projectors combine both: e.g. **LED → collector → light pipe** (the pipe homogenizes) **→ relay imaging the pipe exit onto the DMD** (critical with respect to the pipe exit, which is uniform) — and the relay's aperture is imaged into the projection pupil (Köhler with respect to the LED).

## 3. Condensers and collectors

### 3.1 Collection angle
A Lambertian source emits a fraction $\sin^2\theta$ into a cone of half-angle $\theta$ (L01). An NA 0.5 collector catches 25 %; Kenyon's NA 0.75 aspheric condensers [Kenyon §4.7, p. 92] catch 56 %. To get beyond ~70 % with a refractive collector you need very fast, strongly aspheric elements (often two), or a reflector/TIR approach (§6).

### 3.2 Sizing with étendue (the Lagrange invariant in 2-D)
If a condenser images an emitting area $A_s$ (half-angle $\theta_s$ collected) onto a target area $A_t$ with cone half-angle $\theta_t$, then

$$
n_s^2 A_s\sin^2\theta_s = n_t^2 A_t \sin^2\theta_t \quad\Longrightarrow\quad |m| = \sqrt{A_t/A_s} = \frac{\sin\theta_s}{\sin\theta_t}\ \ (n_s = n_t = 1).
$$

For critical illumination of a 0.3″ DMD (26.9 mm²) with a 1 × 1 mm LED: matching areas needs $|m| \approx 5.2$ (in the long axis 6.9×, short axis 3.9× — a square die cannot fill a 16:9 area without waste); with $\theta_t = 17°$ the collection half-angle is $\arcsin(5.2\cdot\sin17°)$ — impossible, $\sin\theta_s > 1$. With $|m| = 1/\sin 17° = 3.42$ ($\sin\theta_s = 1$, i.e. collect everything), the die image is 3.4 × 3.4 mm: it fills the DMD height (3.89 mm) but only half the width. This is the étendue argument of L01 in geometric form — and the reason projectors put a **homogenizer that also reshapes the beam** between LED and DMD.

### 3.3 Aberrations of condensers
Condensers do not need to form good images, but they are not free of aberration requirements: spherical aberration of a fast collector blurs the source image in the pupil (increasing étendue → losses at the projection pupil), and field-dependent aberrations of the relay blur the edges of the illuminated area (requiring more overfill). Aspheres (Kenyon §4.7) and Fresnel lenses (§4.8: thin, cheap, large, but scattering at the steps) are the usual tools.

## 4. Fly's-eye (lenslet-array) homogenizers

### 4.1 How it works
Two identical lens arrays, LA1 and LA2, separated by the lenslet focal length $f_{LA}$, followed by a condenser of focal length $F$ with the target in its back focal plane:

```
 collimated, non-uniform beam
      │││││
   ┌──┴┴┴┴┴──┐   LA1: each lenslet focuses its part of the beam onto LA2
   └─────────┘
       f_LA
   ┌─────────┐   LA2 (in LA1's focal plane): each lenslet images its LA1 lenslet aperture to infinity
   └─────────┘
        │
   ( condenser F )   superimposes all channel images in its back focal plane
        │
        F
   ═══════════  target (DMD): N overlapping images of a uniformly-filled rectangular lenslet aperture
```

Each channel images **the aperture of an LA1 lenslet** (a uniformly filled rectangle, if the beam is roughly smooth over one lenslet) onto the target; the condenser superimposes all channels. Non-uniformities of the input beam are averaged over the number of channels. This is Köhler illumination replicated N times — the ANSYS article calls LA1 the "objective array" (images the source onto LA2) and LA2 the "field array".

### 4.2 Design equations (paraxial, thin lenses, air)
- **Field size**: a lenslet of pitch $p$ imaged by LA2 + condenser gives a target of size
  $$ D = p\,\frac{F}{f_{LA}} \quad\text{(per axis)}. $$
  So the lenslet aspect ratio must equal the target aspect ratio (16:9 for a 1280 × 720 DMD).
- **Acceptance angle**: the source image formed by an LA1 lenslet must fit inside the corresponding LA2 lenslet, otherwise light crosses into the neighbouring channel and forms ghost fields displaced by $D$ (crosstalk). For an input beam with divergence half-angle $\alpha$:
  $$ f_{LA}\tan\alpha \le p/2 \quad\Longrightarrow\quad \alpha_{\max} = \arctan\frac{p}{2f_{LA}} . $$
- **Illumination cone at the target**: half-angle $\approx \arctan\!\big(D_{\text{array}}/(2F)\big)$, with $D_{\text{array}}$ the illuminated array width — this is a *rectangular* "pupil" made of lenslet-sized source images.
- **Étendue**: the array accepts $G \approx A_{\text{array}}\cdot p_x p_y/f_{LA}^2$ (array area × projected solid angle of the rectangular acceptance cone, small-angle) and delivers exactly the same at the target: $A_{\text{target}}\cdot 4\tan\theta_x\tan\theta_y$. You can check this numerically in the worked example below.
- **Channel count**: Ansys's article recommends roughly 7 to 11 channels per axis as a practical range for lamp-based projectors, with **odd** counts so that a channel sits on axis (an even count can produce a central dip); more channels average better but add more edge scatter and diffraction from lenslet boundaries.
- **Real arrays** are usually molded in glass or plastic with lenslets on both sides of one plate, or on two plates; with the arrays in a medium of index $n$, the physical separation becomes $n f_{LA}$ (the focal length in the medium).

### 4.3 Caveats
- **Coherent sources**: with a laser, the N channels interfere, producing a periodic interference grid on the target (the array is a grating with period $p$). Use a moving or static diffuser, many incoherent emitters (VCSEL arrays), or random/chirped arrays.
- **Collimation**: TI notes that fly's-eye systems need well-collimated input to avoid ghost images, and are less efficient than rods but shorter [TI DLPA022].
- **Diffraction at the lenslet aperture**: for small lenslets (sub-mm) the image of the lenslet edge is softened by diffraction ($\sim\lambda F/\text{(lenslet image NA)}$); ray tracing will not show it.

## 5. Light pipes (integrating rods)

### 5.1 The kaleidoscope
A rectangular rod — solid glass relying on TIR, or a hollow mirror tunnel — scrambles light by multiple reflections. Looking back into the exit face you see a grid of mirror images of the source (a kaleidoscope); the exit face is illuminated by all of them superposed, so it becomes nearly uniform even if the input is a small bright spot. TI recommends enough length to produce roughly a **4 × 5 array of source images** for acceptable uniformity with lamps, more for demanding cases [TI DLPA022].

Rule for length. Inside a solid rod of index $n$, a ray entering with angle $\theta_{\text{air}}$ travels at $\theta_g = \arcsin(\sin\theta_{\text{air}}/n)$. Over length $L$ it moves sideways $L\tan\theta_g$, so the number of source images across a rod of width $w$ visible at angle $\theta_g$ is about $1 + 2L\tan\theta_g/w$. For 5 images: $L \approx 2w/\tan\theta_g$. Because much of a Lambertian source's power is at modest angles, practical solid rods are **5–10 widths long**.

Rod advantages: very high uniformity; the exit face has the target's shape (16:9 rod → 16:9 field), so the **relay simply images the rod exit onto the DMD** (critical illumination of a uniform source). Losses: Fresnel at the faces (AR-coat them), absorption, and rays escaping where TIR fails (dirt, mounts touching the rod — mount at the corners or at the ends only). TI prefers rods (solid or hollow) for single-panel DLP systems; hollow tunnels avoid imaging dust on the exit face.

### 5.2 Étendue in a rod, and tapered rods
A straight rod preserves angles: light enters a 4 × 2.25 mm rod from a 1 × 1 mm LED with ±90° and leaves with ±90°, now spread over 9 mm². The light is uniform over the exit face but **the étendue the next optics must handle is now that of the exit face × full angle** — the rod has diluted the radiance. Hence:

- **Butt-couple a rod whose input face matches the LED**, and use a **tapered rod** (input small, output large) to convert area into angle. For an ideal (long, smooth) taper, $A_{\text{in}}\sin^2\theta_{\text{in}} = A_{\text{out}}\sin^2\theta_{\text{out}}$ (both in air). A taper can also convert a square source to a 16:9 output (TI mentions a 1-D taper for exactly this).
- Then size the relay magnification $m$ so that the rod exit image is slightly larger than the DMD (overfill) and the cone at the DMD fits inside the DMD's acceptance ($\sin\theta_{\text{DMD}} = \sin\theta_{\text{out}}/m$).

## 6. TIR collimators

LED collimators for spotlights, flashlights and some projectors use a solid plastic (PMMA, PC) or silicone part with two light paths:

```
          ┌───────── exit face (flat or lenslets) ─────────┐
         /   ↑     ↑     ↑     ↑     ↑     ↑     ↑     ↑     \
        /    │ TIR │     central asphere     │ TIR │          \   ← outer wall: TIR (no coating)
       /     │     │       (refractive)      │     │           \
      /______│_____│_________________________│_____│____________\
                     cavity: inner cylinder + top asphere
                              ▲ LED (in the cavity)
```

- **Central path (|θ| ≲ 30–45°)**: rays hit the top of an internal cavity and an aspheric lens surface collimates them.
- **Outer path (large θ, up to ~90°)**: rays refract through the cavity side wall, then hit the outer wall — a near-paraboloid shaped so the incidence exceeds the critical angle (PMMA $n \approx 1.49$: $\theta_c = 42°$) — and are reflected by **TIR** (no metallization, ~100 % reflective) into the forward direction.
- **Collection efficiency** can exceed 85–90 % of the LED's flux, versus ~25–55 % for a simple lens.

**The étendue limit on collimation.** No collimator can make the beam more parallel than étendue allows. For a Lambertian source of area $A_s$ and an exit aperture of area $A_e$:

$$
\sin\theta_{\text{out}} \ge \sqrt{\frac{A_s}{A_e}} .
$$

A 1 × 1 mm LED in a Ø 20 mm collimator: $\theta_{\text{out}} \ge 3.2°$. In practice, collimators reach 1.5–2× this limit because the source image varies across the aperture (the central lens magnifies the die less than the TIR wall does). Want a narrower beam? Make the optic bigger or the source smaller — nothing else helps.

## 7. Illuminating a DMD

The DMD adds geometric constraints (TI DLPA022):

- The illumination arrives at $2\theta_t$ (24° or 34°) from the DMD normal in the plane of mirror rotation, so that "on" light leaves along the projection axis; the cone half-angle must be ≲ $\theta_t$ to keep on/off/flat-state light separated (L01 §5.4).
- **Telecentric illumination** (pupil at infinity) usually uses a **TIR prism** to separate the illumination and projection paths: uniform black level, any amount of projection offset; TI recommends a ~10 µm air gap in the prism and quotes ~92–93 % prism transmission.
- **Non-telecentric illumination** uses a **field lens** shared by both paths, needs projection offset, and typically gives the highest contrast but a black level varying across the array; TI notes up to ~10 % extra efficiency loss to integrator-image distortion (overfill).
- The oblique illumination images the rod exit onto a *tilted* plane: the image is keystoned and defocused at the edges unless the relay is tilted (Scheimpflug, [Course 04 L09](../../04-machine-vision-camera-lenses/L09-3d-vision-optics-scheimpflug-stereo/lecture-notes.md)). Budget overfill for this.

In this course's capstone (L09) we simplify the DMD to a flat mask at normal incidence with a reflective "on" region, but keep the étendue constraint.

## 8. In OpticStudio

| Component | NSC objects | Notes |
|---|---|---|
| Condenser lens | Standard Lens; Even Asphere Lens; or import a sequential design (L06) | asphere terms via the lens object's parameters |
| Fresnel lens | Fresnel 1 / Fresnel 2 objects | check the object list in your release |
| Fly's-eye arrays | **Lenslet Array 1**, **Lenslet Array 2**, Hexagonal Lenslet Array | Lenslet Array 1 = rectangular volumes with flat front and curved back face (Ansys KB) |
| Light pipe, taper | **Rectangular Volume** (front and rear half-widths can differ → taper); material N-BK7 or `MIRROR` for hollow-tunnel walls (or 4 Rectangle mirrors) | TIR is automatic; mount contacts can be added as absorbing objects |
| Parabolic reflector | **Standard Surface**, conic −1, `MIRROR` | as in the Ansys NSC tutorial |
| Solid TIR collimator | Part Designer, imported CAD, or rotationally symmetric objects (e.g. combine lens/surface objects) | start with the reflector + lens hybrid; refine to a solid part |
| Uniformity check | Detector Rectangle with as many pixels as your spec grid; Pixel Interpolation for optimization | NSDD Pix# −4 returns the standard deviation of pixel data (L06) |
| Angular check | Detector Rectangle "Radiant Intensity" in far field, or Detector Polar | |

Workflow for a homogenizer study: (1) build with ideal paraxial-like thin parts (e.g. Paraxial Lens objects where available, or simple Standard Lenses); (2) check étendue and channel geometry with a source at ±α; (3) swap in real lenses; (4) evaluate uniformity vs. ray count (L02); (5) optimize (L06).

## Worked example — three homogenizer designs for a 0.3″ DMD

Target: active area 6.912 × 3.888 mm, illumination cone ≲ ±17°.

**A. Fly's-eye.** Choose 16:9 lenslets $p_x \times p_y = 1.6 \times 0.9$ mm, $f_{LA} = 6$ mm.
- Condenser: $F = D f_{LA}/p = 6.912 \cdot 6/1.6 = 25.92$ mm (check: $3.888\cdot6/0.9 = 25.92$ ✓).
- Acceptance: $\alpha_{\max} = \arctan(0.45/6) = 4.29°$ (short axis), $\arctan(0.8/6) = 7.59°$ (long axis). The collimated LED beam must be collimated to better than ±4.3° in the short axis.
- Array 10 × 17 lenslets = 16.0 × 15.3 mm. Cone at the DMD: $\arctan(8/25.92) = 17.2°$ and $\arctan(7.65/25.92) = 16.4°$ — already at the DMD limit along the axes, and the corners of the rectangular pupil exceed it (23° along the diagonal); trim the array corners or use fewer channels.
- Étendue: $A_{\text{array}}\,p_xp_y/f_{LA}^2 = 244.8 \cdot 1.44/36 = 9.79$ mm² sr = $A_{\text{DMD}}\cdot4\tan17.2°\tan16.4° = 9.79$ mm² sr ✓ — the Lagrange invariant in 2-D. (Compare: the DMD's circular F/1.71 acceptance is 7.22 mm² sr — the rectangular pupil overfills it by ~35 %.)

**B. Tapered rod + relay.** LED 1 × 1 mm butt-coupled to a 1.1 × 1.1 mm input face; output face 3.0 × 1.6875 mm (16:9, 5.06 mm²).
- Output angle: $\sin\theta_{\text{out}} = \sqrt{1.21/5.06} = 0.489$ → 29.3° (ideal long taper).
- Relay magnification to fill the DMD width: $m = 6.912/3.0 = 2.304$ (height 1.6875 × 2.304 = 3.888 mm ✓).
- Cone at the DMD: $\sin\theta = 0.489/2.304 = 0.212$ → 12.3° — comfortably within ±17°. Add ~5 % overfill and the cone becomes ~11.7°.

**C. Straight solid rod length.** For a 4 mm wide N-BK7 rod ($n = 1.510$ at 850 nm) and 5 source images across: rays at 30° in air ($\theta_g = 19.3°$) need $L = 2\cdot4/\tan19.3° = 22.8$ mm; rays at 90° in air ($\theta_g = 41.5°$) need only 9.0 mm. A 25–40 mm rod (6–10 widths) is the usual choice.

**D. TIR collimator limit.** 1 × 1 mm Lambertian LED, Ø 20 mm exit: $\theta_{\text{out}} \ge \arcsin\sqrt{1/314.2} = 3.23°$.

## Key takeaways
- Critical illumination images the source onto the target (source structure visible); Köhler images the source into the pupil (uniform field, independent field and NA control).
- Étendue (2-D Lagrange invariant) sizes every illumination component: $A\sin^2\theta$ is conserved, so magnification trades area for angle.
- Fly's-eye: $D = pF/f_{LA}$, acceptance $\arctan(p/2f_{LA})$, lenslet aspect = target aspect, 7–11 (odd) channels per axis; beware coherent interference.
- Light pipes homogenize by kaleidoscopic superposition (aim for ≥ 4 × 5 images; length 5–10 widths); tapers convert area to angle; the relay images the rod exit onto the SLM.
- TIR collimators collect nearly the whole hemisphere, but output divergence is bounded by $\sin\theta_{\text{out}} \ge \sqrt{A_s/A_e}$.
- DMD illumination adds oblique incidence at $2\theta_t$, cone ≤ $\theta_t$, TIR prism vs. field lens, and overfill for keystone and tolerances.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Critical illumination | Source imaged onto the target |
| Köhler illumination | Source imaged into the pupil; target conjugate to a field stop |
| Condenser / collector | Lens(es) collecting source light and directing it to the target |
| Fly's-eye homogenizer | Two lenslet arrays + condenser superimposing many channel images |
| Crosstalk (lenslet) | Light from one LA1 lenslet entering a neighbouring LA2 lenslet → displaced ghost field |
| Light pipe / integrating rod | Rod or mirror tunnel homogenizing by multiple reflections |
| Taper | Rod with different input/output areas, trading area for angle |
| TIR collimator | Solid optic using refraction (centre) and TIR (outer wall) to collimate an LED |
| Overfill | Illuminated area deliberately larger than the SLM active area |
| Telecentric illumination | Same chief-ray direction at every target point (pupil at infinity) |
| TIR prism | Prism pair separating illumination and projection paths at a DMD via TIR at an air gap |

## References
1. [Kenyon §4.4, pp. 81–83] — microscope condenser, Köhler illumination, Fig. 4.10.
2. [Kenyon §4.7–4.8, pp. 92–93] — aspheric condensers, Fresnel lenses.
3. [Kidger §10.4] — illumination of the image field in photographic objectives (relative illumination background).
4. Ansys Optics KB, *Fly's eye array homogenizers for digital projector illumination* — <https://optics.ansys.com/hc/en-us/articles/42661744169363>
5. Texas Instruments, *DLP System Optics*, DLPA022 (July 2010) — <https://ti.com/lit/pdf/dlpa022>
6. Ansys Optics KB, tutorial on basic operations in Non-Sequential Mode (reflector + light pipe) — <https://optics.ansys.com/hc/en-us/articles/42661713082899>
