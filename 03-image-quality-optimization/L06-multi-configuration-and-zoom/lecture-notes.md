# L06 — Multi-configuration systems, focusing and zoom

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~2.5 h, tasks ~6 h
> **Prerequisites:** [L04 — Merit function mastery](../L04-merit-function-mastery/), [L05 — Optimization strategies](../L05-optimization-strategies-and-global-search/), [Course 02 L11 (telephoto)](../../02-aberrations-classical-design/L11-petzval-and-telephoto/) · **Next:** [L07 — Gaussian beams and POP](../L07-gaussian-beams-and-pop/)

## Learning objectives
- Explain what a "configuration" is in OpticStudio and set up the Multi-Configuration Editor (MCE) with the common operands (`THIC`, `CRVT`, `CONN`, `GLSS`, `SDIA`, `PRAM`, `APER`, `WAVE`, `WLWT`, `YFIE`, `FLWT`, `TEMP`, `PRES`, `MOFF`).
- Use configuration pickups and variables in the MCE, and build merit functions that act on all configurations, including custom per-configuration rows with the `CONF` operand.
- Compute first-order cam curves of a two-group mechanically compensated zoom and turn them into a 3-position zoom model.
- Model focusing over object distance (unit focusing vs internal focusing) and design a fixed-focus lens that is optimized over a depth range — a direct model of a 3D camera's working volume.
- Recognise the other uses of multi-configuration: thermal and pressure states, wavelength bands, scanning angles, alternative beam paths, tolerancing.

## Reading
- **Core:** [Kidger §9.4, pp. 193–197] — the telephoto principle (two thin lenses of equal and opposite power, $K = dK_1^2$, zero Petzval sum and zero astigmatism when each component is aplanatic), the f/3 front group in an f/4 system, and the multi-element telephoto prescription (EFL 100, F/4, ±10°). You will use it as the focusing example.
- **Refresh:** [Course 01 L03](../../01-foundations/L03-paraxial-optics-and-ray-tracing/) — power of two separated thin lenses and back focal distance; Newton's equation.
- **Online:** Ansys KB, "Using the Multi-Configuration Editor for optimization, tolerancing and solves" (MC operands as extra variables/parameters; examples with `WAVE`, `APMX`, boundary operands `MCOG`/`MCOL`): <https://optics.ansys.com/hc/en-us/articles/42661753758483>
- **Online:** ZOS-API example 18 (C#): builds multi-configuration files using `THIC`, `CRVT`, `GLSS`, `SDIA`, `TEMP`, `PRES` operands, config pickups and a manual "Make Thermal": <https://developer.synopsys.com/docs/zos-api-interface-2025-r2/page_ex18_cs.xhtml.md> (Ansys optics documentation now lives on Synopsys-hosted pages after the 2025 acquisition; older `developer.ansys.com` links redirect there.)
- **Optional:** Zemax Community, "Vignetting factors for zoom lens with multi-configuration settings": <https://community.zemax.com/got-a-question-7/vignetting-factors-for-zoom-lens-with-multi-configuration-settings-4940>
- **Optional:** Optiland gallery "Multi-Configuration Zoom Lens" (open-source Python, nice for cross-checking cam curves): <https://optiland.readthedocs.io/en/latest/gallery/specialized_lenses/zoom_lens.html>

---

## 1. One lens, several states

Many optical products are not one system but a family of closely related systems:

| Product situation | What changes between states |
|---|---|
| Zoom lens | spacings (and the stop size) |
| Focusing lens (camera at 0.3 m … ∞) | object distance + one or more spacings |
| Fixed-focus 3D camera over a working volume | object distance only (the lens must be good at all of them) |
| Thermal environment (0–45 °C) | temperatures, glass indices, mechanical lengths (L09) |
| Dual-band (visible and 850 nm) | wavelength set and weights, maybe a filter |
| Scanning mirror / galvo | a tilt angle (`PRAM` of a coordinate break) |
| Switchable path (beam splitter, flip mirror) | ignored surfaces, glass, thickness |
| Tolerancing scenarios | perturbed parameters (Course 06) |

OpticStudio handles all of these with one mechanism: a single lens model plus a **Multi-Configuration Editor** table in which each *row* is an MC operand naming a parameter (e.g. "thickness of surface 5") and each *column* is a configuration giving that parameter's value. Everything not listed in the MCE is shared. Analyses evaluate the current configuration (or a chosen one); optimization can evaluate all at once.

## 2. The Multi-Configuration Editor

**Setup → Multi-Configuration Editor** (or the Editors group; location varies by release). Insert configurations (columns) and operands (rows). Common MC operands:

| Operand | Parameter | Typical use |
|---|---|---|
| `THIC` | thickness of surface n | zoom spacings, focus, object distance |
| `CRVT` | curvature of surface n | thermal/pressure (with pickups), adaptive elements |
| `CONN` | conic constant | – |
| `GLSS` | material of surface n | glass swap, filter in/out |
| `SDIA` | semi-diameter | aperture changes, vignetting control |
| `PRAM` | surface parameter n (e.g. coordinate-break tilt, asphere coefficient) | scanning angle, decenter scenarios |
| `APER` | system aperture value | zoom F/# changes |
| `WAVE`, `WLWT` | wavelength value / weight | different bands per state |
| `YFIE`, `XFIE`, `FLWT` | field coordinates / weight | different fields per state (zoom FOV) |
| `TEMP`, `PRES` | system temperature / pressure | thermal analysis (L09) |
| `MOFF` | "off" placeholder row | comment/placeholder |

Each MCE cell can carry a **solve**: *Variable* (optimize this value in this configuration), *Config Pickup* (copy from another configuration, optionally scaled/offset), *Thermal Pickup* (L09). The **Make Thermal** tool (L09) generates a whole thermal MCE automatically. The ZOS-API example cited above builds exactly such tables programmatically.

Practical points:
- The **active configuration** (shown in the title bar; switch with the MCE's next/previous-configuration controls or by double-clicking a column header — keyboard shortcuts exist, see Help) is what the LDE shows and what analyses compute unless told otherwise.
- Most analyses have a *Configuration* setting ("Current", a number, or "All" for overlays such as the Cross-Section / 3D Layout).
- **Vignetting factors** are per field and therefore per configuration when fields change — the Community thread above discusses the pitfalls; prefer real apertures or recompute vignetting for each configuration.
- **Solves in the LDE** are evaluated per configuration. A marginal-ray-height focus solve will refocus each configuration automatically — handy for a focusing study, wrong for a fixed-focus design.

## 3. Merit functions across configurations

### 3.1 Default merit function
In the Optimization Wizard set **Configuration: All**. The wizard then writes one block per configuration, each starting with a `CONF n` row; operands after `CONF n` are evaluated in configuration n until the next `CONF` row. Field and wavelength weights apply per configuration.

### 3.2 Your own rows
Use `CONF` explicitly above DMFS:

```
 1  BLNK  --- focal lengths of the zoom positions ---
 2  CONF  1
 3  EFFL                 target 12.0   weight 1
 4  CONF  2
 5  EFFL                 target 18.0   weight 1
 6  CONF  3
 7  EFFL                 target 30.0   weight 1
 8  BLNK  --- same total track in all positions? (here: monitor only) ---
 9  CONF  1
10  TOTR                               weight 0
11  CONF  3
12  TOTR                               weight 0
13  DIFF  10 12                        weight 0   (track change; constrain with OPLT/OPGT if needed)
```

Rows between `CONF` lines belong to that configuration; math operands (`DIFF`, `SUMM`, `OPGT`, …) can combine values *from different configurations* — e.g. "the image surface must be at the same place in all configurations", "front group travel ≤ 15 mm", or "EFL ratio = zoom ratio". Each `CONF` row costs a model rebuild, so group operands by configuration rather than alternating.

### 3.3 Variables
Mark a variable in the LDE when the parameter is shared by all configurations (a radius), or in the MCE when it is configuration-specific (a zoom spacing). Typical zoom: radii and glass thicknesses are LDE variables (shared), the moving spacings are MCE variables.

## 4. First-order zoom design

### 4.1 The two-group mechanically compensated zoom
Two thin groups, powers $K_1$ and $K_2$, separation $d$. From Course 01 L03:

$$
K = K_1 + K_2 - dK_1K_2,\qquad \text{BFD} = \frac{1 - dK_1}{K} = f\,(1 - dK_1).
$$

Varying $d$ changes $f$; but BFD changes too, so the image moves. To keep the image on the sensor, both groups move along **cam curves** — this is *mechanical compensation*. (In *optical* compensation, groups are linked and move together; the image is fixed only at discrete positions — rare today.)

**Example (negative-lead zoom, like many compact wide-to-normal zooms):** $f_1 = -30$ mm, $f_2 = +20$ mm. Then $K = (10 + d)/600$ mm⁻¹, i.e. $f = 600/(10+d)$, and BFD $= f(1 + d/30)$.

| EFL (mm) | $d$ (mm) | BFD (mm) | Length $d$ + BFD (mm) |
|---|---|---|---|
| 12 | 40.00 | 28.00 | 68.00 |
| 18 | 23.33 | 32.00 | 55.33 |
| 24 | 15.00 | 36.00 | 51.00 |
| 30 | 10.00 | 40.00 | 50.00 |

Zoom ratio 2.5. The rear (positive) group moves monotonically toward the object as focal length grows (BFD 28 → 40 mm), the front (negative) group moves non-monotonically (front-group-to-image distance 68 → 50 → … with a minimum at the long end here; for longer zoom ranges it turns around). Minimizing $L(d) = d + 20(30+d)/(10+d)$ gives $dL/dd = 1 - 400/(10+d)^2 = 0$ at $d = 10$ — the long end. Real zoom design adds: stop location (usually with the rear group, so F/# rises with focal length unless the stop grows), aberration correction of each group *independently* (a group that is corrected by itself stays corrected when it moves — the zoom designer's guiding principle), and the number of groups (3–5 groups for higher ratios, with a "variator" and a "compensator").

### 4.2 Focusing: unit vs internal
Newton's equation $x\,x' = -f^2$ (Course 01 L03) gives the image-side shift needed to refocus from infinity to an object at distance $x$ from the front focal point: $|x'| = f^2/|x|$.
- **Unit focusing** (whole lens moves): for f = 100 mm and an object ≈ 2 m away, $|x'| \approx 100^2/1900 \approx 5.3$ mm extension (approximate; the exact value depends on principal-plane positions). For the 8 mm NIR lens of L04: 0.22, 0.13, 0.065 mm extension for 300, 500, 1000 mm.
- **Internal focusing** (one group moves inside a fixed barrel): length constant, smaller and lighter moving mass, but aberrations change with focus because the ray heights in the groups change — this is the main reason to evaluate it with the MCE. In a telephoto such as Kidger's [§9.4], moving the rear negative group is a classic internal-focus scheme.

### 4.3 Fixed focus over a working volume — the 3D-camera case
A structured-light camera usually has **no focus mechanism**. It must deliver adequate contrast over, say, 0.3–1.0 m object distance. Model it as a multi-configuration system:
- Configurations = object distances (e.g. 300, 450, 600, 1000 mm) via `THIC 0` (object thickness).
- The image distance (sensor position) is **shared** (a normal LDE variable, *not* per configuration) — that is what "fixed focus" means.
- Optimize with the default MF over all configurations, with configuration weighting expressing where in the volume precision matters most.
- Evaluate with Through-Focus MTF per configuration and MTF at the pattern frequency (L02 §6.1).

The optimizer will put the sensor at a compromise "hyperfocal-like" position and balance aberrations so that no configuration is badly defocused. Course 04 L02/L09 build on this with depth-of-field theory and Scheimpflug geometry.

## 5. Other configuration-based tricks
- **Comparing designs** side-by-side in one file (e.g. 3-element vs 4-element) using an ignore-surface MC operand (check the MC operand list in Help) or glass/thickness changes — handy for overlays, but keep separate files as the master copies.
- **Wavelength-switched systems**: a projector at 850 nm and a colour camera in the visible sharing optics; configuration 1 uses NIR wavelengths, configuration 2 visible, with different weights.
- **Scanning systems**: `PRAM` on a coordinate-break tilt for several mirror angles; optimize the F-theta behaviour (Course 02 L05) over all angles.
- **MC operands as extra variables**: the Ansys KB article shows MC operands used even in single-configuration files to expose parameters (e.g. apodization factor `APDF`) to optimization and tolerancing, with `MCOG`/`MCOL` merit-function bounds on MCE values.

## 6. In OpticStudio — workflow and pitfalls
1. Build and optimize **one** configuration first (the hardest one — usually the long-focal-length or nearest-focus state).
2. Add the MCE rows and configurations; fill values from first-order calculation (cam table).
3. Check every configuration's layout (Cross-Section with Configuration = All) and paraxial data before optimizing.
4. Default MF with Configuration = All; custom `CONF` blocks above DMFS; variables in the right editor (shared vs per-configuration).
5. Optimize; then inspect **each** configuration's spot/MTF/distortion. The MF can be dominated by one configuration — use % Contrib grouped by `CONF` block.
6. Pitfalls: forgetting that a LDE solve applies per configuration; vignetting factors that are stale in other configurations; semi-diameters in "automatic" mode growing per configuration (fix them to the maximum over all configurations for mechanical design — the Cross-Section with all configurations shows the envelope); stop size not under control (F/# drifting); sharing a variable that should be configuration-specific (or vice versa).

---

## Worked example — three-position zoom from first order to OpticStudio

**Spec:** EFL 12 / 18 / 30 mm, image-space F/4 at all positions, semi-field: image height 4.0 mm (so 18.4° / 12.5° / 7.6° object-side semi-field), visible F-d-C.

1. **First order** (thin lens): $f_1 = -30$, $f_2 = +20$; spacings from the table: $d$ = 40.00 / 23.33 / 10.00 mm; BFD = 28.00 / 32.00 / 40.00 mm.
2. **Thin-lens model in OpticStudio:** two Paraxial surfaces (focal lengths −30 and +20); MCE rows `THIC` (surface 1 → spacing $d$) and `THIC` (surface 2 → BFD); three configurations with the table values. Aperture: Image Space F/# = 4 (shared). Field: paraxial image height 4.0 (shared) — the object-side field then changes automatically.
3. **Check:** System Data per configuration must show EFL 12.000, 18.000, 30.000 mm and the image at the paraxial focus (marginal ray height ≈ 0 at the image).
4. **Thick lenses:** replace each paraxial group by a cemented doublet (e.g. negative group N-SF5/N-BK7, positive group N-BK7/N-SF5 — your Course 02 L06 achromat scaled), re-solve the spacings with `EFFL` targets in each configuration (custom `CONF` blocks) and an image-position constraint, then optimize everything with Configuration = All.
5. **Expected behaviour:** the short end (widest field) limits field aberrations, the long end limits axial colour and spherical (largest EPD: 30/4 = 7.5 mm vs 3 mm at the short end). A two-doublet zoom will be visibly worse than a fixed-focal lens of the same complexity — zoom lenses pay for flexibility with elements.

---

## Key takeaways
- A configuration = the shared lens + a column of MCE values; MC operands (`THIC`, `CRVT`, `GLSS`, `PRAM`, `APER`, `WAVE`, `YFIE`, `TEMP`, …) name what changes.
- MCE cells can be variables or config/thermal pickups; LDE variables are shared across configurations.
- Default MF with Configuration = All; custom per-configuration rows go between `CONF n` lines; math operands can compare configurations.
- Two-group zoom: $f = 1/(K_1+K_2-dK_1K_2)$, BFD $= f(1-dK_1)$ → cam curves; correct each group on its own.
- Fixed-focus 3D cameras are multi-configuration problems over object distance with a shared sensor position.
- Inspect every configuration; fix semi-diameters to the envelope; watch for per-configuration solves and stale vignetting.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Configuration | One state of a multi-state system, defined by MCE values |
| MC operand | Row in the MCE naming a parameter that differs between configurations |
| Config pickup | Solve copying an MCE value from another configuration (with optional scale/offset) |
| `CONF` operand | MFE row switching subsequent operands to configuration n |
| Mechanical compensation | Zoom groups moving on separate cams to keep the image fixed |
| Variator / compensator | Zoom group that changes focal length / group that keeps focus |
| Unit / internal focusing | Moving the whole lens / one group inside the lens to refocus |
| Cam curve | Group position vs focal length (or object distance) |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, 2002: §9.4, pp. 193–197.
2. Course 01 L03 (this repository) — two-lens power, BFD, Newton's equation.
3. Ansys Optics KB, "Using the Multi-Configuration Editor for optimization, tolerancing and solves": <https://optics.ansys.com/hc/en-us/articles/42661753758483>
4. ZOS-API Interface 2025 R2, Example 18 (multi-configuration and Make Thermal from C#): <https://developer.synopsys.com/docs/zos-api-interface-2025-r2/page_ex18_cs.xhtml.md>
5. Zemax Community, "Vignetting factors for zoom lens with multi-configuration settings": <https://community.zemax.com/got-a-question-7/vignetting-factors-for-zoom-lens-with-multi-configuration-settings-4940>
6. Optiland documentation, "Multi-Configuration Zoom Lens" gallery example: <https://optiland.readthedocs.io/en/latest/gallery/specialized_lenses/zoom_lens.html>
