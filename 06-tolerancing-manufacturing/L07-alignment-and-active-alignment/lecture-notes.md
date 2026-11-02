# L07 — Alignment and active alignment

> **Course 06 · Tolerancing and manufacturing** · Estimated time: lecture ~2.5 h, tasks ~6 h
> **Prerequisites:** [L02 — TDE and compensators](../L02-tolerance-data-editor-and-compensators/), [L03 — sensitivity and Monte Carlo](../L03-sensitivity-and-monte-carlo/), [L05 — opto-mechanics](../L05-opto-mechanics-and-cad-integration/); helpful: [04/L09 — 3D-vision optics](../../04-machine-vision-camera-lenses/L09-3d-vision-optics-scheimpflug-stereo/), [04/L10 — capstone spec](../../04-machine-vision-camera-lenses/L10-capstone-machine-vision-lens/) · **Next:** [L08 — Capstone: tolerancing the camera lens](../L08-capstone-tolerancing-the-camera-lens/)

## Learning objectives
- Explain the difference between **passive** assembly (accuracy from parts) and **active** alignment (accuracy from measurement + adjustment + fixing), and decide which errors each can remove.
- Describe how a lens surface's centering error is measured in **reflection** (autocollimator focused on the centre of curvature, rotating spindle) and in **transmission** (beam deviation), and convert between wobble radius, surface tilt, wedge and beam deviation.
- Choose an alignment **compensator** in a multi-element lens (which element to center, which spacer to grind) from a sensitivity analysis, and estimate the travel it needs.
- Describe the 5/6-axis **active alignment** (AA) of a camera module — lens vs sensor in $x, y, z$, tip, tilt (and roll) — including through-focus SFR/MTF on several regions of interest, the focus-plane fit, and the UV-cure shrink / post-cure shift budget.
- Build an AA model in OpticStudio: a coordinate break in front of the sensor with **CPAR** compensators on its tilts, **COMP** on the lens–sensor gap, an MTF-based merit-function criterion at centre and corners — and a second stage that applies post-cure errors *after* compensation.
- Explain **boresight / principal-point** errors, why a calibrated 3D camera absorbs static alignment errors but not drift after calibration, and estimate the depth error caused by micrometre-level lens–sensor or projector–camera drift.

## Reading
- **Core:** [Geary §37.5, pp. 424–425] — modelling a decentered and a tilted element with a pair of coordinate breaks (the same construction you will use for the sensor in §6). Ignore the old dialog names.
- **Core:** [Geary §37.7, pp. 426–429] — a decentered aperture in a beam with spherical aberration "sees" coma and astigmatism: the physical reason why decentering one element can *cancel* axial coma created elsewhere (the principle of the centering compensator, §3).
- **Core:** [Kidger §3.7, pp. 60–61] — how a ray trace handles decentrations $d_x, d_y, d_z$ and rotations; useful to understand that a coordinate break is just a change of the local frame.
- **Optional:** [Kidger §8.4, p. 182] — why a cemented doublet is mechanically preferable to a split one: the air space of a split doublet is a sensitive parameter and "subject to loss of alignment" under shock and vibration.
- **Online (core):** Commonlands, "Active alignment for camera modules" — a clear practitioner overview: 6 DOF, centre + four-corner through-focus scoring, the tilt/depth-of-focus arithmetic, UV-cure process: <https://commonlands.com/blogs/technical/active-alignment-for-camera-modules>
- **Online (core):** TRIOPTICS, "Centration measurement" — reflection vs transmission centering measurement, multi-surface measurement, bonding/cementing alignment: <https://www.trioptics.com/applications/alignment-and-testing-of-lens-systems/centration-measurement>
- **Online:** Henkel, "Active alignment" adhesive white paper — the adhesive requirements (fast UV fix, low and *consistent* shrinkage, post-cure) with shrinkage and bond-line-stability data for two commercial adhesives: <https://dm.henkel-dam.com/is/content/henkel/active-alignment-whitepaper-landscape>
- **Online:** Laser Focus World, "Adaptive software eases camera lens-to-sensor alignment" (vendor-written, Kasalis): 6-DOF AA with ISO 12233 SFR-derived MTF, multi-point through-focus, and *adaptive* pre-offset of the lens against the measured cure shrinkage: <https://www.laserfocusworld.com/software-accessories/software/article/16557046/software-design-for-manufacturing-adaptive-software-eases-camera-lens-to-sensor-alignment>
- **Online:** Zemax Community, "How to set the image surface tilt and decenter as compensator" (staff answer: CPAR on a coordinate break in front of the image, COMP for $z$): <https://community.zemax.com/got-a-question-7/how-to-set-the-image-surface-tilt-and-decenter-as-compensator-4289>; and "Decenter of a lens as compensator" (CPAR on a coordinate-break pair; finite compensator resolution; tolerance scripts): <https://community.zemax.com/got-a-question-7/decenter-of-a-lens-as-compensator-2183>

---

## 1. Alignment philosophy: passive vs active

Every assembled optical system answers one question: **where does the accuracy come from?**

- **Passive (mechanical) alignment.** Accuracy comes from the parts. Lenses drop into a bore, stack on spacers, the barrel screws into a holder, the holder is screwed to the sensor PCB. The final error is the stack-up of part tolerances (L05). Cheap, fast, no metrology per unit — but every micrometre must be paid for in machining, and no part can be better than its worst interface.
- **Active alignment.** Accuracy comes from a **measurement of the optical function** during assembly. A part is held loosely (in adhesive, on a sliding seat, with a set screw), the system is operated (light goes through, an image is analysed), the part is moved until the measured signal is optimal, and then the position is **frozen** (UV-cured adhesive, clamp, laser weld, potting). Parts can be looser, because their errors are measured and cancelled — but you now depend on the measurement, the motion system, and the stability of the fixing step.

In between are **semi-active** steps that every lens designer uses without thinking of them as alignment: focusing an M12 lens by turning its thread while watching the image; selecting a spacer from a set of thicknesses after a test ("select-on-test"); grinding a spacer to measured length; centring a cemented doublet before the cement cures.

In tolerancing language (L02 §5) every active or semi-active step is a **compensator**: a parameter adjusted *after* the errors exist, to optimize a *measured* criterion, within a *limited range* and with a *finite resolution*, and followed by a fixing step that adds its own error. Those four qualifiers — criterion, range, resolution, fixing error — are what this lesson is about. A compensator modelled without them is optimistic.

**What can a compensator remove?** Only errors that it maps onto. A rule that saves a lot of confusion:

| Adjustment | Removes (to first order) | Cannot remove |
|---|---|---|
| Lens–sensor $z$ (focus) | power errors, thickness/spacing errors, index errors, mean field curvature shift | astigmatism, coma, lateral colour |
| Lens–sensor tip/tilt | **tilt of the best-focus surface** (from sensor tilt in its package, holder tilt, *and* the field-linear focus tilt created by decentered elements) | asymmetric blur inside the lens (axial coma, axial astigmatism) |
| Lens–sensor $x, y$ | position of the optical centre on the sensor (principal point, shading symmetry, CRA symmetry) | nothing image-quality related in a rotationally symmetric lens |
| Lens–sensor roll ($\theta_z$) | image rotation relative to pixel rows — relevant for stereo/epipolar alignment, Scheimpflug and anamorphic systems | anything else |
| Decenter/tilt of one *element* inside the lens | **axial coma** (and partially field-dependent asymmetry) caused by the other elements' decenters/wedges | spherical aberration, power errors |
| Axial position of one element / spacer selection | a chosen aberration balance (e.g. spherical vs field curvature) + focus | asymmetric errors |

The key professional insight: **camera-module active alignment moves the lens as a rigid body relative to the sensor. It fixes "where the image surface is", not "what the image is like".** If your Monte Carlo shows that the yield is limited by on-axis coma, a 6-axis AA station will not save you; centring inside the lens (§2–3) or tighter element tolerances will.

## 2. Centering of elements

### 2.1 What "centred" means
A spherical surface is defined by its centre of curvature $C$. A lens (two spherical surfaces) has an optical axis: the line through $C_1$ and $C_2$. It is **centred** relative to a reference axis (its own edge, a barrel bore, a spindle, another lens) if that line coincides with the reference. Errors come in two flavours: a **tilt** of the optical axis and a **decenter** (lateral offset). For a single spherical surface the two are degenerate (L02 §3.2): all that matters is the lateral distance $e$ of $C$ from the reference axis, giving a surface tilt angle

$$
\varepsilon = \frac{e}{R},
$$

with $R$ the radius of curvature. For an asphere the vertex position and the axis direction are independent, so an asphere has *two* centering errors (L01).

### 2.2 Measuring in reflection (autocollimation)
The workhorse of centering metrology is the **autocollimator focused on the centre of curvature** with the part rotating on a precise spindle (air bearing). The instrument projects a reticle image to the point $P$ on the spindle axis where the nominal $C$ lies. A sphere reflects any point $P$ near its centre of curvature into its mirror image through $C$: $P' = 2C - P$. If $C$ is a distance $e$ off-axis, the returned image is displaced by $2e$; as the part rotates, it runs on a circle. Instruments report the circle centre (the rotation axis) and its radius converted back to $e$ (the factor 2 is part of the calibration — read the manual of your instrument). The TRIOPTICS page in Reading describes exactly this: "the circle radius equals the distance from the centre of curvature to the reference axis", expressed as an angle it is the surface tilt.

For surfaces *inside* an assembled lens, the autocollimator looks at the image of $C_k$ formed by all the surfaces in front of it. The measurement software ray-traces the nominal design (it needs the prescription — this is one reason a vendor asks for your lens data) to back-calculate the true position of each $C_k$. Instruments of this type measure 20 or more surfaces of a complete objective from one or both sides, with micrometre-level accuracy (TRIOPTICS quotes ~1 µm typical).

### 2.3 Measuring in transmission
Collimated light through the lens focuses at a point; if the lens is rotated about a reference axis, a decentered lens makes the focus run on a circle. The result is a **beam deviation** $\delta$. For a thin lens decentered by $d$: $\delta \approx d/f$ (L01). For a single lens, a surface tilt $\varepsilon$ produces a wedge and therefore a deviation

$$
\delta = (n-1)\,\varepsilon,
$$

which is the relation quoted by TRIOPTICS ($T = (n-1)R$). Transmission cannot tell *which* surface is wrong and can show a "centred" result for a lens that is tilted and decentered in compensating ways; reflection identifies individual surfaces. Use both when it matters.

**Cheap alternatives** for single elements: edge-thickness difference (ETD) with a dial gauge while rotating on the edge; wedge $\approx$ ETD/$D$ (L01, L06).

### 2.4 Centering *processes*
- **Edging with bell chucks or optical centering** (L01): grinds the edge concentric with the optical axis — sets the element's wedge.
- **Cementing on a centering machine.** The first element is mounted on the spindle and its axis aligned to the rotation axis (watching the reflected images of its surfaces). The second element is placed on uncured cement and pushed laterally (and tilted) until the reflected images of *its* surfaces stop wobbling; then a UV tack cure freezes it, followed by a full cure. Achievable: a few µm and some arcseconds; vendors of automated bonding/cementing stations advertise ~1 µm and a few arcsec including adhesive shrinkage. In the TDE this sets the *relative* TEDX/TETX of the two elements of a doublet (L02 §3.3, L05 §2).
- **Bonding in a cell + alignment turning.** An element is aligned on the spindle in an oversized cell (floating in adhesive), cured, and then the *cell* outer diameter and seat faces are turned concentric to the measured optical axis on a precision lathe ("alignment turning"). The cell then drops into the barrel with the accuracy of a turned diameter (a few µm). This is how high-end lenses (microscope objectives, lithography, aerospace) reach sub-µm effective centring with commercial-grade glass centering.
- **Centering a whole objective.** The assembled lens is measured surface by surface; one designated element (the **centering lens**, §3) is moved laterally by set screws or in a floating cell until the measured residual is minimized, then glued.

### 2.5 Typical numbers
Order-of-magnitude values (always confirm with your vendor):

| Process | Typical residual |
|---|---|
| Drop-in, metal barrel, commercial | 10–50 µm decenter, 1–5 arcmin tilt (L01 §6) |
| Precision drop-in (fits ≈ H7/g6, good spacers) | 5–10 µm, ~1 arcmin (L05) |
| Cementing on a centering machine | 1–5 µm, a few to ~30 arcsec |
| Alignment turning of cells | 1–3 µm, a few arcsec |
| Camera-module lens–sensor AA (tilt) | ~0.01°–0.02° residual; z a few µm after cure |

## 3. Aligning a multi-element system — choosing the compensator

### 3.1 Why one element can compensate many
Each decentered or wedged element contributes, to first order, three asymmetric image errors that grow *linearly* with the decenter (nodal aberration theory makes this precise; here we only need the linearity):

1. **Boresight / image shift** (the image moves sideways),
2. **Axial (on-axis) coma** — a constant coma over the field,
3. **Image-plane tilt** — the best-focus surface tilts (a field-linear focus term), and, to second order, field-asymmetric astigmatism.

Because the effects are linear and add like vectors (an $x$ and a $y$ component each), a single adjustable element with a strong *and different* lever on these terms can cancel the sum of many small errors. Geary's "Arthur" story [Geary §37.7] shows the mechanism: an off-axis piece of a beam that carries spherical aberration contains coma. An element working in a beam with a lot of its own (or upstream) spherical aberration is therefore a powerful coma knob when decentered.

### 3.2 How to pick it in OpticStudio
1. Build a merit function that measures the target asymmetry: on-axis coma via **ZERN** (Zernike Fringe terms 7 and 8 are the $x$ and $y$ third-order coma; set the field to the on-axis field and check the operand's parameter columns in the MFE), and the image tilt via the focus at ±x and ±y fields (e.g. through-focus MTF peaks, or **REAY** of marginal rays at symmetric fields).
2. For each element $k$, decenter it by a small amount (e.g. 10 µm) — manually with a coordinate-break pair, or by a sensitivity run with only TEDY rows and the criterion = this merit function — and record the coma per µm, $s_k$, and the side effects (MTF loss at the edge of the field, boresight change).
3. The ideal compensator has **a large $s_k$** (small travel needed, coarse adjustment resolution suffices) but **a small side effect per unit of coma correction**. Very sensitive elements make poor compensators *if* their adjustment resolution (screw pitch, operator) cannot follow; very insensitive ones need impossible travel.
4. The travel needed is the expected coma from all other errors divided by $s_k$. With sensitivities $a_i$ (coma per unit error) and tolerances $t_i$, the RSS coma is $\sqrt{\sum_i (a_i t_i)^2}$ (per axis), so

$$
\Delta_{\text{comp}} \approx \frac{\sqrt{\sum_i (a_i t_i)^2}}{s_k}.
$$

5. Model the result in the TDE: a coordinate-break pair around the element, **CPAR** compensators on the decenter parameters of the first coordinate break (with a pickup on the second so the lens is decentered as a body), with a realistic range — see the community thread in Reading. In Premium you can alternatively write a **tolerance script** that emulates the factory sequence (measure → adjust this element → fix) — the scripting language is documented in Help ("Tolerance Scripts"); Course 07 L07 does the same via the ZOS-API.

### 3.3 Other compensators
- **Air-space compensator** (a spacer ground to measured length, or a threaded focusing group): best chosen as the air space with the largest effect on the aberration you need to balance (often spherical/field curvature) and *least* effect on focus — otherwise it is just a second focus.
- **Focus** remains the universal compensator; L02 set it up with COMP on the image distance.
- Avoid **degenerate pairs**: two compensators that do the same thing (e.g. sensor $x$ and lens $x$; or decenter and tilt of a sensor in a model where field points move with it) make the optimizer wander and inflate the compensator statistics without improving the criterion.

## 4. Active alignment of camera modules

### 4.1 The station
A modern camera-module AA station holds the **sensor** (on its PCB, powered, streaming images) fixed and holds the **lens** (barrel or lens holder) in a gripper on a 5- or 6-axis stage: $x, y, z$, tip $\theta_x$, tilt $\theta_y$, and optionally roll $\theta_z$. Adhesive is dispensed on the holder's bond surface; the lens hovers in the wet adhesive with a gap that is deliberately larger than the expected correction. A chart (for finite conjugate) or a set of collimators with targets (for infinity or, with a relay, a simulated finite distance) is imaged onto the sensor so that one target lands in the centre and one in each corner region, often additional ones at mid-field.

```
            chart / collimators (targets at centre + 4 corners)
                         │  │  │
                    ┌────▼──▼──▼────┐
   gripper ───────► │     LENS      │  ◄── 6-axis stage: x, y, z, θx, θy, (θz)
                    └───┬───────┬───┘
                 glue   │  gap  │  glue      (UV adhesive, 50–150 µm typical)
                    ┌───┴───────┴───┐
                    │ holder + PCB  │  ◄── sensor fixed, live images to the PC
                    │ ▓▓▓ sensor ▓▓▓│
                    └───────────────┘
```

### 4.2 The algorithm
1. **Coarse:** centre the optical axis on the sensor ($x, y$ from the image of a centre target or from relative-illumination symmetry); coarse focus.
2. **Through-focus scan:** step $z$ through focus (e.g. 2–5 µm steps over ±30–50 µm). At each step compute, for every region of interest (ROI), the **SFR** (slanted-edge spatial frequency response, ISO 12233) and from it the MTF at one or two frequencies — commonly $\nu_N/4$ and $\nu_N/2$, where $\nu_N = 1/(2p)$. For $p$ = 3.45 µm: $\nu_N$ = 144.9 lp/mm, $\nu_N/4$ = 36.2 lp/mm, $\nu_N/2$ = 72.5 lp/mm.
3. **Peak finding:** fit each ROI's through-focus curve (parabola or Gaussian around its maximum) to find its best-focus $z_i$, separately for tangential and sagittal edges if desired.
4. **Plane fit:** fit $z_i = z_0 + a\,x_i + b\,y_i$ over the ROI positions $(x_i, y_i)$ on the sensor. The slopes give the tilts that make the sensor parallel to the best-focus surface, $\theta \approx a$ and $\theta \approx b$ (radians, with $a, b$ in µm/µm); $z_0$ is the best average focus. (Signs depend on the station's axis definitions.)
5. **Correct and iterate** (usually 1–3 iterations), then optionally a fine search maximizing a figure of merit (e.g. maximize the *minimum* corner MTF while keeping the centre above a threshold).
6. **Pre-offset and cure:** move $z$ (and possibly tilt) by the expected cure shrinkage in the opposite direction, UV-cure (seconds), release, re-measure; thermal post-cure in an oven (tens of minutes); final through-focus test.

The field-curvature term is not a plane: with a centre and four symmetric corners, a least-squares plane absorbs the mean of centre and corners into $z_0$ and leaves the curvature as a residual. AA can only *balance* field curvature, not remove it — that remains the designer's job.

### 4.3 Why it matters: the tilt–depth-of-focus arithmetic
A sensor tilted by $\theta$ relative to the best-focus surface puts a corner at radius $r$ out of focus by

$$
\Delta z \approx r\,\theta .
$$

The geometric depth of focus for a blur circle $c$ at working F-number $N$ is $\pm N c$; the diffraction depth of focus (λ/4 wavefront criterion) is $\pm 2\lambda N^2$ (03/L03). For the Course 04 capstone (F/2.4, $p$ = 3.45 µm, corner $r$ = 5.5 mm):

- depth of focus $\pm N\cdot 2p$ = ±16.6 µm; $\pm 2\lambda N^2$ at 850 nm = ±9.8 µm;
- a 0.1° tilt (a typical *passive* holder-tilt tolerance, L02/L05) gives $\Delta z$ = 9.6 µm at one corner and 19.2 µm between diagonal corners — the entire focus budget;
- 0.01° (a good AA residual) gives 1.0 µm.

Add the M12 thread: 0.5 mm pitch = 500 µm per turn, so 10 µm of focus is a 7.2° turn of the lens — feasible by hand, but a thread has play and tilts in its own clearance. This is why fast lenses on small pixels (≲ 2–3 µm pixel, ≲ F/2) are glued by AA almost universally, and why it is increasingly common for industrial cameras with larger pixels when the lens is fast.

### 4.4 Adhesive, cure and the post-cure shift budget
The adhesive gap replaces the thread: it must be thick enough to absorb the full correction range, yet every micrometre of glue is a micrometre that can shrink, swell or creep. Facts to plan around (Henkel and Kasalis sources in Reading):

- UV acrylates and UV/thermal **dual-cure** epoxies are used; a short UV exposure "tacks" the position in seconds, a thermal post-cure completes cross-linking (and reaches shadowed glue).
- **Volume shrinkage** of AA adhesives is around 1–1.5 % (Henkel quotes 1.0 % and 1.4 % for two products). The vendor of AA systems reports cure shrinkage "typically a few microns", enough to affect focus. What matters most is that shrinkage is **consistent**, so it can be pre-compensated; the residual is the unit-to-unit *variation* of the shift.
- **Long-term stability**: Henkel's data show bond-line thickness changes of −0.7 % to +0.3 % after 1000 h of heat or damp-heat storage on a 650 µm bead (that is up to 4.6 µm!), and ~0.1 % on a 100 µm bond line (0.1 µm). **Thin, uniform bond lines are stable bond lines.**
- **Differential shrinkage → tilt.** When AA corrects a tilt, the glue gap becomes wedge-shaped; unequal glue thickness shrinks unequally and tilts the lens a little back. Example: a 0.25° correction over a 12 mm bond diameter makes the gap differ by 52 µm side to side; at 1 % linear shrinkage of the thickness this is a 0.52 µm difference → 0.0025° of tilt → 0.24 µm of corner defocus at 5.5 mm. Small — but at 2–3 % shrinkage, large corrections or larger lever arms it is not, which is one reason stations iterate tilt *after* the UV tack or pre-tilt.
- **Glue CTE** (~25 ppm/K below $T_g$ for the products cited) over a 100 µm gap and 40 K gives 0.1 µm — negligible compared with the barrel and holder (03/L09); the *holder* material between lens and sensor dominates thermal focus shift.

A **post-cure shift budget** therefore looks like this (example values, to be replaced by qualification data):

| Contribution (focus, at the image) | ±µm |
|---|---|
| AA residual (peak-finding noise, stage resolution) | 2 |
| UV-cure shrink after pre-offset (unit-to-unit) | 1 |
| Thermal post-cure + early aging | 2 |
| Tilt residual (as corner defocus) | 1 |
| Thermal focus shift over 0–45 °C (holder/barrel) | 5 |
| Design residual field curvature/astigmatism | 4 |
| **RSS** | **7.1** |
| (worst case, sum) | (15) |

against a depth of focus of ±16.6 µm ($c = 2p$) or ±9.8 µm (diffraction, 850 nm) for the F/2.4 capstone: comfortable at $c = 2p$, tight at the diffraction criterion — and note that thermal drift is already the largest single term.

### 4.5 Projector modules
A structured-light projector has the same problem in reverse: the projection lens must image the pattern generator (DMD, LCD/LCoS, mask, or a VCSEL/DOE arrangement) sharply onto the scene over the working volume. Projector AA mounts the light modulator (or the lens) on a stage, projects a test pattern on a screen or into a camera-based measurement head, and focuses and tilts for uniform pattern contrast across the field — the same through-focus and plane-fit logic, with the reverse ray trace of 05/L05. Two differences: the "sensor" is a hot, optically loaded component (heat flow during operation changes focus — do the final AA at operating temperature if you can), and the quantity that matters for 3D is **pattern contrast at the fringe frequency** across the depth range, not peak MTF at one distance.

## 5. Boresight, pointing and calibration

### 5.1 What calibration absorbs
A 3D camera is **calibrated** after assembly: intrinsic parameters of the camera (focal length, principal point $(c_x, c_y)$, distortion coefficients — often also tilt terms) and of the projector, and the extrinsic pose (rotation + translation) between them (04/L09). Any *static* alignment error that is a smooth, low-order geometric mapping is therefore absorbed:

- lens decenter relative to the sensor → **principal point** offset (a lateral image shift of the whole image, the **boresight error**);
- sensor tilt → small keystone (tilt) distortion, absorbed by a tilted-sensor model or by the distortion polynomial;
- focal-length error → focal length;
- projector pointing and roll relative to the camera → extrinsic rotation.

**What calibration does not absorb:**
1. **Blur.** MTF lost to tilt or residual aberration is lost — it reduces fringe contrast and therefore increases depth noise ($\delta d$ in 04/L09). AA is first of all an MTF tool.
2. **Anything that changes after calibration**: thermal expansion of the holder and bracket, adhesive creep and humidity swelling, shock and vibration. A lateral image shift of $\Delta x$ after calibration is a pure pointing error $\Delta\theta \approx \Delta x / f$.
3. **Coverage.** Calibration cannot create light where the projector does not illuminate: projector–camera field-of-view overlap over the full working range is a mechanical alignment tolerance.

### 5.2 How big is a micrometre?
For a triangulating system with baseline $b$, focal length $f$, pixel $p$, the depth error from a disparity error $\delta x$ (in length units on the sensor, along the baseline) is (04/L09)

$$
\delta z \approx \frac{z^2\,\delta x}{f\,b}
$$

equivalently $\delta z \approx z^2 \delta\theta / b$ for an angular pointing change $\delta\theta = \delta x/f$. For $f$ = 8 mm, $b$ = 150 mm, $z$ = 1 m:

- **1 µm** of lens–sensor lateral drift = 0.29 px = 125 µrad (26 arcsec) → $\delta z \approx$ **0.83 mm** — about six times the 0.144 mm depth noise of the capstone at $\delta d$ = 0.05 px. The error is systematic (a depth-dependent offset/warp of the point cloud), not noise, so it survives averaging.
- **Axial drift** changes image scale for a non-telecentric lens by $\Delta v/v$: 2 µm on an 8 mm lens = 250 ppm → 1.4 µm (0.4 px) radial shift at a 5.5 mm corner — a "zoom" error that calibration at another temperature would have assigned to the focal length.
- **Bracket bending.** A 1 K temperature difference through a 20 mm thick aluminium bracket ($\alpha$ = 23 ppm/K) bends it with curvature $\alpha\,\Delta T/t$; over a 150 mm baseline the projector and camera rotate relative to each other by $\alpha\,\Delta T\,L/t$ = 173 µrad → $\delta z \approx$ 1.15 mm at 1 m (0.41 mm at 0.6 m).

The conclusions a 3D-camera optical engineer draws: (1) after calibration, the *relative* pose of lens, sensor, projector and bracket must be stable to **micrometres and tens of microradians** over temperature and life; (2) adhesive joints with thin, symmetric bond lines and materials with matched CTE are part of the optical design; (3) residual thermal drift is handled by thermal design, temperature-dependent calibration models, or in-field correction — but each of these needs the drift to be *repeatable*, which glued AA joints with creep are not unless qualified; (4) the boresight criterion of the tolerancer (L02 §6) is the right tool to quantify *how much* image shift a given perturbation (e.g. a thermal or shock-induced element shift) produces.

### 5.3 Projector–camera relative alignment
Tolerances for the relative alignment are set by:
- **Overlap:** the projected field must cover the camera field at the near and far ends of the working range with margin. A 0.5° pointing error moves the projected field by 8.7 mm at 1 m — compare with the margin you designed in.
- **Roll** of the fringe pattern relative to the epipolar direction: for phase-shifted fringes the depth sensitivity scales with $\cos\psi$ — a 1° roll costs 0.015 %, i.e. nothing; calibration takes care of the geometry. Roll matters more for line or dot patterns decoded along epipolar lines.
- **Focus** of each unit over the shared depth range (§4.4, §4.5).
- **Stability** (§5.2) — almost always the binding requirement.

## 6. In OpticStudio — simulating active alignment

### 6.1 The model
Start from your tolerancing file (e.g. L05's `L05_mech.zmx`). The AA moves the lens relative to the sensor; in the model it is easier to move the **sensor package** (cover glass + image) relative to the lens — for distant objects the two are equivalent up to a decenter and a negligible change of object distance.

1. Insert a **Coordinate Break** surface directly in front of the sensor package (in front of the cover glass; if the IR filter is glued to the holder and moves with the lens, put the CB after it). The surface in front of it carries the air gap; the CB has zero thickness.
2. The CB parameters (check the column headers in your LDE): Par 1 Decenter X, Par 2 Decenter Y, Par 3 Tilt About X, Par 4 Tilt About Y, Par 5 Tilt About Z, Par 6 Order. Leave them at 0 nominally. The pivot of the tilts is the CB vertex — the cover-glass front centre, within ~1 mm of the die; the small extra decenter that a different pivot would cause is irrelevant for MTF.
3. In the TDE add the **compensators**:
   - `COMP` on the air-gap thickness (the surface in front of the CB) with the glue-gap range (e.g. ±0.05 mm), *replacing* the thread-focus COMP of L02;
   - `CPAR` on the CB, parameter 3 and parameter 4 (tilts) with the stage/glue range (e.g. ±0.5°);
   - **not** CPAR on Par 1/2 (decenter) for an MTF criterion — with fields defined in object space, sensor $x, y$ changes nothing the criterion sees, so it is a degenerate compensator. Treat $x, y$ separately (boresight, below).
4. The **errors** stay as in L05 (element and barrel tolerances), plus those the AA must fix: sensor die tilt in its package (TETX/TETY on the image surface, L02), holder tilt.
5. **Fields:** AA scores centre and corners. Use object-space fields (Object Angle or Object Height, not Real Image Height, whose solve for the field point would move with the perturbed lens) at the on-axis point, ±x, ±y and **the four diagonal points** at the ROI positions, e.g. 0.8 of the half-diagonal. Field weights mimic the station's figure of merit.
6. **Criterion:** a **merit function** with `MTFT` and `MTFS` at the AA frequency (e.g. $\nu_N/4$ or $\nu_N/2$) for each field (target 1, weight 1; centre weight per the station recipe), optionally `MTFA`. Load it as the criterion (Criterion = Merit Function), with **Optimize All (DLS)**, a fixed small number of **cycles** (to mimic finite search effort — the community thread notes that "Automatic" lets the optimizer keep perfecting the compensator), and XY-symmetric/user fields so that the corners are evaluated.
7. Run sensitivity, then Monte Carlo. Read the **compensator statistics**: the tilt CPARs must stay well inside the stage and glue-gap range; the COMP mean and spread define the nominal glue gap.

### 6.2 Errors after compensation: the post-cure shift
In a standard tolerancing run OpticStudio applies **all** perturbations and *then* adjusts the compensators — so any error you add to the TDE is compensated. Post-cure shift happens *after* the AA. Model it in a second stage:

- **Two-stage run.** Save Monte Carlo files from stage 1 (the `MC_T####.ZMX` files, L02/L03). Open one (or several, e.g. the median and the 90th-percentile unit), convert the compensator values to fixed numbers (they already are in the saved file), and run a second tolerancing with **Comp = None** (no compensators) and only the post-cure errors: `TUTX`/`TUTY` on the same AA coordinate break (the TU operands work only on coordinate breaks, Ansys KB in References), `TUDX`/`TUDY` if lateral shift matters for boresight, and `TTHI` on the air gap for the axial shrink. The resulting distribution is the *as-shipped* performance.
- **Tolerance script.** Emulate the factory sequence in one run: perturb, compensate, perturb again, evaluate. The scripting language and commands are in Help ("Tolerance Scripts"); the community thread in Reading discusses the idea. Course 07 L07 does the same with the ZOS-API, which is often simpler for complex sequences (e.g. emulate peak-finding noise and the plane fit of §4.2).

### 6.3 Boresight and lateral alignment
- To quantify image shift, use the **Boresight Error** criterion (L02 §6) or a merit function with `REAX`/`REAY` of the chief ray of the on-axis field ($P_x = P_y = 0$). `BSER` is the boresight-error merit operand in recent versions (chief-ray radial coordinate on the image divided by the EFL, per the Help) — check the operand list in your version before relying on it.
- Run sensitivity with this criterion and **Comp = None** on the *drift* tolerances you expect after calibration (thermal element shifts, glue creep, holder deformation from STAR in L05). The output, in µm or µrad, feeds the depth-error formula of §5.2.

### 6.4 Pitfalls
- Leaving the old thread-focus COMP *and* adding the AA z COMP: two degenerate focus compensators.
- Compensating with unlimited range or unlimited cycles — the "perfect AA" that no station delivers.
- Criterion = average MTF while the station maximizes the *minimum* corner — the tolerancer will pick a different, better-looking alignment than the factory (L02 §5.3, L03 Task 5).
- Forgetting the corners: with Y-symmetric fields the tilt compensators have nothing to work on (and asymmetric errors look harmless).
- Expecting the AA compensators to fix on-axis coma: check the worst offenders *after* AA — what remains are the lens-internal asymmetries (§1, §3).

## Worked example — plane fit, tilt correction and focus budget for the capstone receiver

**Given:** sensor 8.45 × 7.07 mm, $p$ = 3.45 µm, F/2.4. ROIs at the centre and at 0.8 of the half-diagonal: $(x, y)$ = (±3.380, ±2.828) mm, $r$ = 4.41 mm. The through-focus scan gives peak positions (µm, positive = sensor should move away from the lens):

| ROI | $x$ (mm) | $y$ (mm) | $z_i$ (µm) |
|---|---|---|---|
| centre | 0 | 0 | 12.00 |
| top right | +3.380 | +2.828 | 12.93 |
| top left | −3.380 | +2.828 | −0.59 |
| bottom left | −3.380 | −2.828 | 5.07 |
| bottom right | +3.380 | −2.828 | 18.59 |

**Plane fit.** With symmetric ROIs the least-squares solution decouples:

$$
z_0 = \overline{z_i} = 9.60\ \mu\text{m},\quad
a = \frac{\sum x_i z_i}{\sum x_i^2} = 2.00\ \mu\text{m/mm},\quad
b = \frac{\sum y_i z_i}{\sum y_i^2} = -1.00\ \mu\text{m/mm}.
$$

(Check $a$: $\sum x_i z_i = 3.38\,(12.93 + 0.59 - 5.07 + 18.59) = 3.38 \times 27.04 = 91.40$ and $\sum x_i^2 = 4 \times 3.38^2 = 45.70$, so $a = 2.000$. Task 1 does the general case with `numpy.linalg.lstsq`.)

**Corrections.** Slope 2.00 µm/mm = $2.0\times10^{-3}$ rad = **0.115°** about the $y$-axis, and −1.00 µm/mm = **−0.057°** about the $x$-axis; move focus by **+9.6 µm**. The residuals after the correction are +2.4 µm at the centre and −0.6 µm at each corner: that is the design's **field curvature** (3 µm centre–corner), which AA balances but cannot remove.

**Was it worth it?** Before correction, at the best average focus the bottom-right corner was +9.0 µm and the top-left corner −10.2 µm from focus — the latter beyond the ±9.8 µm diffraction depth of focus at 850 nm, and the two diagonal corners 19 µm apart. After: all within ±2.4 µm.

**Glue.** The larger tilt component across a 12 mm bond diameter is $12 \tan(0.115°)$ = 24 µm of gap difference — inside a 100 µm nominal gap. At 1 % shrinkage, the differential is 0.24 µm → 0.0012° → 0.1 µm corner defocus. The axial shrink of ~1 µm is pre-compensated; its unit-to-unit spread enters the budget table of §4.4 (RSS ±7.1 µm vs ±16.6 µm depth of focus at $c = 2p$).

**After calibration.** If the same joint later creeps laterally by 0.5 µm (0.14 px), the depth error at 1 m with $b$ = 150 mm is $10^6 \cdot 0.0005/(8 \cdot 150)$ = **0.42 mm** — three times the capstone's depth noise. The glue joint that was perfectly adequate for *focus* is the critical element for *metrology*. That is the 3D-camera twist on active alignment.

## Key takeaways
- Every alignment step is a compensator with a criterion, a range, a resolution and a fixing error; model all four, or the tolerancing is optimistic.
- Rigid lens-vs-sensor AA fixes focus, image-surface tilt and optical-centre position — not lens-internal asymmetries such as axial coma. Those need element centering (one well-chosen centering lens) or tighter element tolerances.
- Centering is measured in reflection (autocollimator on each centre of curvature, rotating spindle; $\varepsilon = e/R$) and in transmission (beam deviation, $\delta = (n-1)\varepsilon$ for a single lens).
- Camera AA = through-focus SFR/MTF at centre + corners → per-ROI peak → plane fit → tip/tilt/z correction → pre-offset → UV tack → thermal post-cure. Tilt matters because corner defocus is $r\theta$: 0.1° costs ~10 µm at a 5.5 mm corner.
- Adhesives shrink ~1–1.5 % by volume; consistency matters more than size; thin, uniform bond lines are the stable ones.
- In OpticStudio: CB in front of the sensor package, CPAR on its tilt parameters, COMP on the gap, merit-function criterion with MTFT/MTFS at centre and corners, finite cycles; post-cure errors need a second stage or a tolerance script because all TDE errors are applied before compensation.
- Calibration absorbs static geometry, not blur and not drift: for a triangulating camera, 1 µm of lens–sensor drift after calibration is ~0.8 mm of depth error at 1 m ($f$ = 8 mm, $b$ = 150 mm).

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Passive alignment | Accuracy from part tolerances alone (stack-up) |
| Active alignment (AA) | Position set by measuring the optical function during assembly, then fixed (glue, clamp) |
| Centering error | Offset/tilt of a surface's centre of curvature or an element's optical axis from a reference axis |
| Autocollimator (centering) | Instrument that projects a reticle to a surface's centre of curvature and observes the reflected image's wobble while the part rotates |
| Beam deviation | Angular deviation of a transmitted axial beam caused by wedge/decenter |
| Alignment turning | Turning a cell's outer diameter and faces concentric to the measured optical axis of the bonded lens |
| Centering lens | Element designated to be moved laterally during assembly to cancel axial coma |
| SFR | Spatial frequency response from a slanted-edge target (ISO 12233); gives MTF per region |
| ROI | Region of interest on the sensor (centre, corners) used by the AA algorithm |
| Through-focus scan | Sequence of images at stepped lens–sensor distances; each ROI's MTF peak gives its best focus |
| Pre-offset | Deliberate offset of the lens before curing to cancel the expected cure shrinkage |
| Post-cure shift | Movement of the aligned part during/after cure and aging |
| Boresight error | Lateral shift of the image of the axial point (line of sight); for a calibrated camera, a principal-point shift |
| Bond line | Thickness of the adhesive layer |

## References
1. [Geary §37.5, pp. 424–425] — lens decentration and tilt with coordinate breaks.
2. [Geary §37.7, pp. 426–429] — aberrations induced by decentration (coma and astigmatism from a decentered aperture in an aberrated beam).
3. [Kidger §3.7, pp. 60–61] — ray tracing through decentered and tilted surfaces.
4. [Kidger §8.4, p. 182] — cemented vs split doublets: manufacturing tolerances and loss of alignment in service.
5. Commonlands, "Active alignment for camera modules" (camera module assembly guide): <https://commonlands.com/blogs/technical/active-alignment-for-camera-modules>
6. TRIOPTICS, "Centration measurement": <https://www.trioptics.com/applications/alignment-and-testing-of-lens-systems/centration-measurement>; product page "OptiCentric — lens centration and alignment": <https://www.trioptics.com/products/opticentric-lens-centration-and-alignment>
7. Henkel, active-alignment adhesives white paper: <https://dm.henkel-dam.com/is/content/henkel/active-alignment-whitepaper-landscape>; and "Camera modules and dual-cure adhesives": <https://dm.henkel-dam.com/is/content/henkel/whitepaper-1015-camera-modules-and-dual-cure-adhesives>
8. Laser Focus World, "Adaptive software eases camera lens-to-sensor alignment": <https://www.laserfocusworld.com/software-accessories/software/article/16557046/software-design-for-manufacturing-adaptive-software-eases-camera-lens-to-sensor-alignment>
9. Zemax Community, "How to set the image surface tilt and decenter as compensator": <https://community.zemax.com/got-a-question-7/how-to-set-the-image-surface-tilt-and-decenter-as-compensator-4289>
10. Zemax Community, "Decenter of a lens as compensator": <https://community.zemax.com/got-a-question-7/decenter-of-a-lens-as-compensator-2183>
11. Ansys Optics KB, "How to tolerance for tilts and decenters of a double pass system" (TUDX/TUDY/TUTX/TUTY/TUTZ work only on coordinate breaks): <https://optics.ansys.com/hc/en-us/articles/43071118693139>
12. Ansys Optics KB, "How to inspect OpticStudio's internal tolerance models" (SAVE operand, saved MC files): <https://optics.ansys.com/hc/en-us/articles/43071088477587>
