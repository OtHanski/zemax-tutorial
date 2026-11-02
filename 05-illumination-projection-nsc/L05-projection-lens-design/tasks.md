# L05 — Tasks: Projection Lens Design

> Work in `work/` inside this lesson folder (e.g. save `work/L05_T4_skeleton.zmx`). Commit your designs, scripts and a short `work/notes.md` with answers.
> Estimated time: ~6 h (Tasks 1–4 ≈ 3 h; Task 5 ≈ 3 h or more — it is a real design)

All tasks use OpticStudio conventions (light left → right; in the *reverse* model the screen is the object and the DMD is the image). N-BK7 at 0.85 µm: $n = 1.50984$.

## Task 1 — First-order projector calculator (Python)
**Goal:** Turn a DMD datasheet and a throw-ratio/offset requirement into the numbers a lens designer needs.
**Given / specs:** DLP4710-class DMD: 1920 × 1080 mirrors, pitch $p = 5.4\ \mu$m, ±17° tilt, telecentric illumination. Throw ratio $T = 1.4$ defined at $D = 1000$ mm lens-to-screen; **100 % offset** (TI convention: image bottom edge on the lens axis); thin-lens model.
**Steps:**
1. Write `projector_first_order(Nx, Ny, p, T, D, offset_pct, tilt_deg)` returning: DMD $W$, $H$, diagonal; image $W_s$, $H_s$; magnification $m$; focal length $f = D/(1+m)$ and the rule-of-thumb $TW$; DMD-centre shift $s$; image-circle radius at 0 % and at the given offset; corner field angle for both; minimum F/# from the tilt; entrance-pupil diameter; projected pixel size at 0.5, 1.0, 1.5 m; DMD Nyquist frequency.
2. Run it for the specs above and for the lecture worked example (0.3″ 720p, $T = 1.2$) to check the function against the lecture numbers.
3. How much larger (in %) is the image-circle *area* the lens must correct at 100 % offset than at 0 %?
**Deliverable:** script `work/projector.py` + table in `notes.md`.
**Check yourself:** $W = 10.368$, $H = 5.832$ mm (diag 11.90 mm); $W_s = 714.3$, $H_s = 401.8$ mm; $m = 68.9$; $f = 14.31$ mm ($TW = 14.52$); $s = 2.916$ mm; $r_{\max}$ = 5.95 mm (0 %) → 7.80 mm (100 %); corner field 22.6° → 28.6°; F/1.71; EPD 8.37 mm; projected pixel 0.183 / 0.372 / 0.561 mm; Nyquist 92.6 c/mm.

<details><summary>Hints / solution sketch</summary>

- $r_{\max} = \sqrt{(W/2)^2 + (s+H/2)^2}$ with $s = (\text{offset}/100)\cdot H/2$.
- Projected pixel at distance $L$: $p\,(L-f)/f$ (from Newton/thin lens, distances from the lens).
- Area ratio $(7.80/5.95)^2 = 1.72$ → 72 % more field area; the lens is a different, harder lens.
- The worked example should reproduce $f = 8.23$ mm, $r_{\max} = 5.20$ mm, corner 32.3°.

</details>

## Task 2 — Depth-of-focus and fringe-contrast budget for 0.5–1.5 m (Python)
**Goal:** Decide focus distance, F/# and minimum fringe period for a structured-light projector.
**Given / specs:** The Task 1 lens ($f = 14.31$ mm, $p = 5.4\ \mu$m), working range $L$ = 500–1500 mm (from the lens), geometric (thin-lens, defocus-disc) model; diffraction neglected except in step 5.
**Steps:**
1. Compute the DMD-side conjugate offset $x'(L) = f^2/(L-f)$ at 500, 750, 1000, 1500 mm.
2. Find the focus distance $L_f$ that balances the defocus at the two ends (DMD placed midway). Compare with 1000 mm and with the harmonic mean $2L_1L_2/(L_1+L_2)$.
3. Residual defocus $\pm\delta$ and blur $b = \delta/N$ (µm and pixels) at F/1.71, F/2.4, F/4. What F/# gives a 1-pixel blur, and what fraction of the F/1.71 throughput would remain?
4. For each F/#, compute the defocus-disc MTF $2J_1(\pi b\nu)/(\pi b\nu)$ at the range ends for fringe periods of 2, 4, 8, 16 and 32 pixels. Flag negative values (contrast reversal).
5. Compare $\delta$ with the diffraction depth of focus $\pm 2\lambda N^2$ at 850 nm.
6. Compare with the lecture's 0.3″ 720p example (blur 5 pixels at F/1.71). Explain the difference using the scaling law $b_{px} \propto T^2 N_{px}^2 p / N$.
**Deliverable:** `work/dof.py`, a table in `notes.md`, and a one-paragraph recommendation (F/#, focus distance, minimum fringe period).
**Check yourself:** $x'$ = 0.421, 0.278, 0.208, 0.138 mm; balanced focus ≈ 746 mm (harmonic mean 750 mm); $\delta = \pm 142\ \mu$m; blur 83 µm = 15.4 px (F/1.71), 59 µm = 10.9 px (F/2.4), 35 µm = 6.6 px (F/4); 1-pixel blur needs ≈ F/26 (≈ 0.4 % throughput). Contrast at the range ends for 16-px / 32-px fringes: 0.22 / 0.74 (F/1.71), 0.52 / 0.86 (F/2.4), 0.81 / 0.95 (F/4); 8-px fringes are reversed (negative) at F/1.71 and F/2.4. Diffraction DOF at F/2.4, 850 nm: ±9.8 µm ≪ 142 µm.

<details><summary>Solution sketch / discussion</summary>

- Balanced focus: $x'_f = \tfrac12[x'(500)+x'(1500)] = 0.2796$ mm → $L_f = f + f^2/x'_f = 746$ mm.
- The 1080p, $T = 1.4$ projector has $(1.4/1.2)^2 (1920/1280)^2 = 3.06$× the pixel blur of the 720p, $T = 1.2$ one for the same F/# and range — 15.4 vs 5.0 pixels. More pixels across a fixed working volume means each pixel is smaller in the scene, and the defocus blur (set by the pupil and the range) does not shrink with it.
- A reasonable recommendation: F/2.4 (also gives more contrast on a ±17° DMD), focus ≈ 0.75 m, fringe periods ≥ 24–32 pixels for the full range — or accept a smaller range for the finest patterns. Many systems instead change focus or use fewer, larger pixels; both are system-level decisions you can now quantify.

</details>

## Task 3 — Keystone vs offset (Python, optional OpticStudio check)
**Goal:** Quantify what tilting the projector instead of using offset costs.
**Given / specs:** Task 1 projector, screen (wall) vertical at 1000 mm horizontal distance. Option A: 100 % offset, lens axis horizontal. Option B: 0 % offset, projector tilted up by $\alpha = \beta$ (vertical half-field), giving the same bottom edge on the horizontal axis.
**Steps:**
1. Compute $\beta$ and the top/bottom width ratio $\cos(\alpha-\beta)/\cos(\alpha+\beta)$.
2. Height of the image on the wall in option B vs A.
3. If the image is digitally squared to the bottom width, which fraction of the columns is used in the top row?
4. Distances along the projector axis to the top and bottom edges of the image in option B, and the corresponding difference in DMD-side focus $x'$ (µm). Compare with $\delta$ from Task 2.
5. (Optional, OpticStudio) In a forward paraxial model (Task 4 reversed, or a Paraxial surface with object = DMD), tilt the image surface by 11.36° about x with Coordinate Breaks and look at **Grid Distortion** — the trapezoid should match step 1.
**Deliverable:** numbers + a 3-line argument for offset in `notes.md`.
**Check yourself:** $\beta = 11.36°$; ratio 1.084; height 418.7 mm (B) vs 401.8 mm (A); 92.2 % of columns used in the top row; axial distances 1062.9 mm (top) and 980.4 mm (bottom) → $\Delta x' \approx 17\ \mu$m — small compared with the ±142 µm range defocus, so for structured light the keystone's main cost is the non-rectangular, non-uniform pixel grid, not focus.

<details><summary>Hint</summary>

A row at projector field angle $\varphi$ lands at elevation $\alpha+\varphi$; its distance along the projector axis is $D\cos\varphi/\cos(\alpha+\varphi)$, and its width scales with that distance.

</details>

## Task 4 — Reverse paraxial skeleton with prism and window (OpticStudio)
**Goal:** Build the reverse model correctly, verify first order and telecentricity, and *see* the plate spherical aberration.
**Given / specs:** Units mm; wavelength 0.85 µm only; Aperture **Paraxial Working F/#** = 1.71; Field type **Real Image Height** (or Paraxial Image Height): 0, 2.916, 5.832, 7.803 mm.

| Surf | Type | Comment | Thickness | Glass |
|---|---|---|---|---|
| 0 | Standard | screen (OBJ) | 985.692 | |
| 1 (STOP) | Standard | front focal plane | 14.3075 | |
| 2 | Paraxial, focal length 14.3075 | ideal lens | 2.0 | |
| 3 | Standard | prism (as plate) | 20.0 | N-BK7 |
| 4 | Standard | | 1.0 | |
| 5 | Standard | DMD window | 1.1 | N-BK7 |
| 6 | Standard | | solve: Marginal Ray Height = 0 | |
| 7 | IMA | DMD | | |

**Steps:**
1. Enter the system; open the Cross-Section (it will be very long — set the layout to start at surface 1).
2. Verify: paraxial magnification (`PMAG` in the MFE or Prescription Data); object height for the 7.803 mm field; real chief-ray angle at the DMD for all fields (`RANG`, $P_x = P_y = 0$) and exit-pupil position (`EXPP`). Where is the stop relative to the paraxial lens and why does that make the DMD side telecentric?
3. Set the plate thicknesses (surfaces 3 and 5) to 0 and record the image distance from the solve; restore them and record again. Compare the change with $t(n-1)/n$.
4. With the plates in, open the Ray Fan and Spot Diagram. Record the marginal transverse aberration at paraxial focus; then use Quick Focus and record the RMS spot. Is it the same for all fields?
5. Change to F/2.4 and repeat step 4.
6. Save as `work/L05_T4_skeleton.zmx`. Keep it: the Paraxial surface will be replaced by real groups in Task 5.
**Deliverable:** table (magnification, CRA, image distances, TSA at F/1.71 and F/2.4) + screenshot of the ray fan.
**Check yourself:**
- $m = -0.01452$ (= −1/68.9; inverted), object height for 7.803 mm ≈ 537.6 mm; chief-ray angle ≈ 0 at every field; `EXPP` very large (exit pupil at infinity) — the stop is at the lens's front focal point.
- Image distance increases by 7.125 mm $= 21.1\times0.50984/1.50984$ when the plates are added.
- Marginal transverse aberration at paraxial focus ≈ 95 µm at F/1.71 (≈ 18 pixels!) and ≈ 35 µm at F/2.4, **identical at all fields** (telecentric beam through a plate). Sign: opposite to the undercorrected spherical of the singlets in Course 02 L02 (plates are overcorrecting). After Quick Focus the RMS spot is still several pixels at F/1.71.
- If the spot with zero-thickness plates is not essentially perfect, check the Paraxial surface's OPD/ray settings in the Help (behaviour can depend on version).

<details><summary>Why these numbers</summary>

Paraxial working F/1.71 sets $\tan u = 0.2924$ in air. In glass $\tan u_g = \sin u/\sqrt{n^2-\sin^2u}$; the ray's focus shift is $t(1-\tan u_g/\tan u) = 7.450$ mm vs the paraxial 7.125 mm, so LSA = 0.324 mm and TSA = LSA·tan u = 94.7 µm. At F/2.4: LSA 0.167 mm, TSA 34.8 µm. Scale: ∝ $t\,u^3$.

</details>

## Task 5 — Design a telecentric retrofocus projection lens (OpticStudio)
**Goal:** Go from the lecture worked example's spec to a real, optimized projection lens.
**Given / specs (lecture worked example):** 0.3″ 720p DMD, $p = 5.4\ \mu$m; reverse model; screen at 750 mm (nominal focus) with multi-configs at 500 and 1500 mm; target $f = 8.23$ mm (throw ratio 1.2 at 1 m); 100 % offset → fields (Real Image Height) 0, 1.56, 2.60, 3.64, 4.42, 5.20 mm; wavelengths 0.83, 0.85, 0.87 µm (weights 1, 2, 1); Paraxial Working F/# 2.0 first, then 1.71 as a stretch; prism 12 mm N-BK7 + 1.0 mm air + 1.1 mm N-BK7 window + 0.5 mm air to the DMD; at least 2.3 mm air between the last lens and the prism.

**Steps:**
1. **Thin-lens predesign (pen & paper):** two groups, front $f_1 = -20$ mm, rear $f_2$, separation $d$. Require $f = 8.23$ mm and an *air-equivalent* BFL of 13 mm (2.3 mm air + reduced prism/window/air path $12/n + 1.0 + 1.1/n + 0.5 \approx 10.2$ mm → ≈ 12.5; round up to 13). Use $f_{BFL} = f(1-d\varphi_1)$ and $\varphi = \varphi_1+\varphi_2-d\varphi_1\varphi_2$ to get $d$ and $f_2$. Where must the stop be for DMD-side telecentricity?
2. **Paraxial check:** copy the Task 4 file, replace the single Paraxial surface by two Paraxial surfaces ($f_1$, $f_2$, spacing $d$), put the stop at the front focal point of the rear group, set the plate thicknesses above, and confirm EFFL, BFL and CRA ≈ 0.
3. **Real elements:** replace the front group by a negative meniscus (convex to the screen, e.g. N-SF5 or N-LAK9) and the rear group by four elements, e.g. positive N-LAK9 – (cemented N-SF6 negative + N-LAK9 positive or N-PSK53A-type positive) – positive N-LAK9 near the prism (any reasonable high-index crowns/flints from the SCHOTT catalog). Start with all elements 2–4 mm thick, air gaps ≥ 0.5 mm, radii from the thin-lens powers with equi-convex/meniscus shapes; Quick Focus.
4. **Merit function:** Optimization Wizard (RMS spot, centroid, rectangular array, glass/air boundary constraints: centre ≥ 1.0 mm glass, edge ≥ 0.8 mm, air ≥ 0.3 mm), then add `EFFL` = 8.23, `RANG` of the chief ray at the image for fields 3–6 with a target 0 (≈ ±2° allowed: weight it moderately or bound with OPLT/OPGT), `DIMX` ≤ 1.5 %, `LACL` bounded to ±2.7 µm, `TTHI` ≥ 2.3 mm for the last air gap, and a total-track limit (`TOTR` ≤ 60 mm). Variables: all radii, air gaps, then glasses (substitution) once the form is stable.
5. **Multi-configuration:** configs 500 / 750 / 1500 mm (`THIC` on surface 0), DMD position fixed (no per-config focus). Optimize all three; then add `MTFA` at 92.6 c/mm with `OPGT` 0.5 for the 750 mm config and ≥ 0.3 for the end configs (or use the default merit function across configs and check MTF afterwards — faster).
6. **Evaluate:** FFT MTF at 750 mm (to 100 c/mm), FFT Through Focus MTF at 11.6 and 23.1 c/mm, Field Curvature/Distortion, Lateral Color (in µm), Relative Illumination, Footprint Diagram on the prism entrance face (prism aperture size). Check Seidel/Zernike for which aberration limits the edge field.
7. Push to F/1.71. What fails first? Try one even asphere on the element nearest the stop.
**Deliverable:** `work/L05_T5_projlens.zmx`, a one-page summary in `notes.md`: layout, MTF plot, distortion and lateral colour in pixels, CRA, relative illumination, and whether it meets the worked-example budget.
**Check yourself:**
- Predesign: $d = 11.59$ mm, $f_2 = 9.21$ mm; the stop lies 9.21 mm in front of the rear group, i.e. ≈ 2.4 mm behind the front lens.
- After step 4–5 at F/2.0 with six spherical elements, expect: CRA within ~±2°, distortion within ±1–2 % (retrofocus forms tend to barrel), lateral colour ≪ 1 pixel over 830–870 nm (the NIR band is narrow), MTF at 92.6 c/mm roughly 40–70 % at 750 mm depending on field (the 32° corner is the hard part), noticeably lower at 500 mm. Total track 40–60 mm. If the corner MTF is far below 40 %, the field is too wide for the element count — add an element or reduce the offset to 50 % and see how much it helps.
- At F/1.71 spherical aberration and oblique spherical/coma at the edge rise; an asphere near the stop usually recovers much of it.

<details><summary>Hints</summary>

- Predesign algebra: $13 = 8.23(1 + d/20)$ → $d = 11.59$; $1/8.23 = -0.05 + \varphi_2(1 + 11.59/20)$ → $\varphi_2 = 0.1086$, $f_2 = 9.21$ mm.
- If the optimizer pulls the stop out of position, remember telecentricity is enforced only by the `RANG` targets; a curvature solve on the last powered surface targeting the chief-ray angle is an alternative (Ansys KB, Reading).
- Ray aiming (Paraxial) on; for the 500 mm config the object height is smaller — fields are image heights, so this is automatic.
- Weighting: if 100 % offset, the region $r > 3.888$ mm is used only towards the corners; it is legitimate to lower the weights of the 4.42 and 5.20 mm fields somewhat. Do not drop them.

</details>

## Stretch tasks
- **Forward verification.** Use Reverse Elements (Ansys KB KA-01408) or rebuild your Task 5 lens with OBJ = DMD, **Object Space NA** = 0.25 (F/2.0), **Telecentric Object Space** on, fields as Object Height. Run Image Simulation (or Geometric Image Analysis) with a bitmap of 16-pixel vertical fringes at 500, 750 and 1500 mm. Does the fringe contrast follow your Task 2 prediction (scaled to this lens)?
- **Offset sensitivity.** Re-optimize Task 5 for 50 % and 0 % offset (fields up to 4.42 and 3.97 mm). Plot corner MTF vs offset — the price of offset in one curve.
- **12° DMD.** Repeat Task 5 for a ±12° device (F/2.4). How much easier is it, and what does it cost in étendue (L01)?

## Reflection questions
1. Why do we design projection lenses in reverse, and which analysis outputs would be awkward in the forward direction?
2. A colleague proposes F/1.5 "for more light" on a ±17° DMD. What happens to contrast, and why?
3. Why must the TIR prism be in the model from the first sketch, and why does telecentricity make its aberration easier to correct?
4. For a structured-light projector, why might the through-focus MTF at the fringe frequency be a better merit target than the in-focus MTF at Nyquist?
5. Give two reasons to prefer offset over tilt that matter specifically for structured light.

<details><summary>Answers</summary>

1. The DMD is the short conjugate: designing with it as the image gives spots, MTF (cycles/mm), lateral colour and distortion in DMD µm, directly comparable with the pixel pitch; the default merit function is well conditioned; telecentricity is a simple image-space constraint. Forward, the "image" is a metre away and hundreds of mm wide.
2. The cone half-angle (19.5° at F/1.5) exceeds the 17° tilt: the on-state cone overlaps the flat-state bundle (window/gap scatter) and approaches the off-state light → black level rises, contrast falls; some on-state light near the flat-state direction must be rejected anyway (TI DLPA022).
3. A 10–20 mm glass block in an F/1.7–2.4 converging beam adds tens of µm of overcorrected spherical aberration and several mm of focus shift; adding it afterwards ruins the design. In a telecentric beam every field sees the same aberration, so it is a single, field-independent term the lens can balance with its own undercorrected spherical.
4. The patterns are mostly 8–32-pixel fringes and the object can be anywhere in 0.5–1.5 m: what decides measurement quality is fringe contrast (and absence of contrast reversal) across the range, which depends on F/#, focus and field curvature — not the in-focus Nyquist MTF that no pattern uses.
5. (i) Rectangular, uniform pixel grid without digital keystone resampling of the patterns (no interpolation/aliasing errors, all mirrors used); (ii) the focus plane stays parallel to the reference plane, so defocus is symmetric over the field; also uniform irradiance.

</details>
