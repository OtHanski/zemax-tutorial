# L06 — Tasks: Multi-configuration systems, focusing and zoom

> Work in `work/` inside this lesson folder (e.g. save `work/L06_T2_zoom_paraxial.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~6 h

## Task 1 — Cam curves of a two-group zoom (Python)
**Goal:** Do the first-order zoom design before touching the software.
**Given / specs:** thin groups $f_1 = -30$ mm, $f_2 = +20$ mm; focal-length range 12–30 mm; image plane fixed.
**Steps:**
1. Derive $d(f)$ and BFD$(f)$ from $K = K_1 + K_2 - dK_1K_2$ and BFD $= f(1-dK_1)$.
2. Plot the positions of both groups relative to the fixed image plane vs $f$ (the cam curves).
3. Find the focal length at which the overall length (front group to image) is minimum, analytically and numerically.
4. Repeat for $f_1 = -25$, $f_2 = +20$ and comment on the change in group travel.
5. With the stop at the rear group and a fixed stop diameter of 5 mm, compute the F/# at 12, 18, 30 mm (entrance pupil ≈ image of the stop through group 1). What happens to F/# across the zoom?
**Deliverable:** `work/zoom_cams.py`, plots, table.
**Check yourself:** $f = 600/(10 + d)$; $d$ = 40.00, 23.33, 15.00, 10.00 mm and BFD = 28.00, 32.00, 36.00, 40.00 mm at f = 12, 18, 24, 30 mm; length 68.00, 55.33, 51.00, 50.00 mm; minimum where $(10+d)^2 = 400$, i.e. $d = 10$, f = 30 mm (the long end of this range).

<details><summary>Hints / solution sketch</summary>
For step 5 trace a paraxial marginal ray backwards from the stop edge through group 1 (or simply build it in OpticStudio in Task 2 and read the EPD per configuration). With a fixed physical stop the F/# is not constant; a real zoom either accepts a "variable aperture" (e.g. F/3.5–5.6) or changes the stop size with an MC operand (`SDIA` of the stop, or `APER` with "float by stop size" off).
</details>

## Task 2 — A paraxial three-position zoom (OpticStudio)
**Goal:** Learn the MCE mechanics with no aberrations in the way.
**Given / specs:** lecture worked example: two Paraxial surfaces f = −30 and +20 mm; stop on the second; aperture Image Space F/# = 4; field Paraxial Image Height 4.0 mm (0, 2.8, 4.0); λ = d only.
**Steps:**
1. Build the lens with configuration-1 values ($d$ = 40, BFD = 28). Save as `work/L06_T2_zoom_paraxial.zmx`.
2. Open the MCE; add two `THIC` rows (surface 1, surface 2) and three configurations with the Task 1 values for f = 12, 18, 30 mm.
3. In each configuration read EFL, EPD, object-side semi-field, and confirm the image is at paraxial focus.
4. Cross-Section with Configuration = All (overlay). Add a dummy surface at a fixed distance in front of group 1 if you want the overlay to show the front group moving relative to a fixed image.
5. Now break the cam: set configuration 2's BFD to 30 mm instead of 32 mm and compute how far out of focus the image is (in µm) and what the RMS spot is. Then make that MCE cell a *Variable* and write a 6-row custom MF: `CONF 2`, `EFFL` target 18, and a focus condition (use the default MF Spot for configuration 2 only, or `REAY` of a marginal ray at the image with target 0). Optimize and confirm it returns to 32 mm.
**Deliverable:** file, table of EFL/EPD/semi-field per configuration, a note on step 5.
**Check yourself:** EFL 12.000 / 18.000 / 30.000; EPD 3.0 / 4.5 / 7.5 mm (F/4); semi-field 18.4° / 12.5° / 7.6°. A 2 mm BFD error at F/4 gives a geometric blur diameter ≈ 2/4 = 0.5 mm.

<details><summary>Hints / solution sketch</summary>
For a paraxial system the default spot MF in configuration 2 is zero only at exact focus, so optimization with BFD variable recovers 32.000 mm. If EFL targets are off, check that the image-space F/# aperture setting is shared (not in the MCE).
</details>

## Task 3 — Unit vs internal focusing of Kidger's telephoto (OpticStudio)
**Goal:** Compare two focusing schemes with the MCE.
**Given / specs:** Kidger's multi-element telephoto [Kidger §9.4, p. 196], EFL 100 mm, F/4 (EPD 25), ±10°, F-d-C. Enter it with modern SCHOTT equivalents:

| Surf | Radius | Thickness | Glass (SCHOTT) |
|---|---|---|---|
| 1 | 53.72645 | 5.00000 | N-LAK7 |
| 2 | 205.54068 | 0.25000 | |
| 3 | 34.32911 | 7.00000 | N-SK14 |
| 4 | −227.00584 | 2.00000 | N-SF5 |
| 5 | 41.32751 | 16.42940 | |
| 6 (stop) | ∞ | 31.38080 | |
| 7 | −16.44330 | 2.00000 | N-BK7 |
| 8 | 46.38767 | 8.00000 | N-LAK22 |
| 9 | −30.50036 | 18.80042 | |
| image | ∞ | | |

**Steps:**
1. Enter, check EFL ≈ 100 mm (glass substitution changes it slightly — re-optimize lightly with radii variable and EFFL = 100 if needed). Total track ≈ 90.9 mm → telephoto ratio ≈ 0.91. Save `work/L06_T3_tele.zmx`.
2. Add configuration 2 with object distance 2000 mm (`THIC` 0). **Unit focusing:** make `THIC` 9 variable in configuration 2 only; MF: `CONF 2` + default spot MF for configuration 2. Record the extension and image quality at 2 m.
3. Configuration 3, object at 2000 mm, **internal focusing**: make `THIC` 6 variable in configuration 3 and constrain the total track to equal configuration 1 (`CONF 1` + `TOTR`, `CONF 3` + `TOTR`, `DIFF` with target 0, high weight). Back focus `THIC` 9 is also variable in configuration 3.
4. Compare configurations 2 and 3: group motion, RMS spot at 0/7/10°, distortion, EFL (focal length changes in internal focus!).
**Deliverable:** file with three configurations, a comparison table, 4–6 sentences.
**Check yourself:** unit focusing needs ≈ 5 mm extension (Newton: $f^2/x \approx 100^2/1900 = 5.3$ mm, exact value depends on principal-plane positions); internal focusing moves the rear group by a comparable but different amount with constant length, and the effective focal length at 2 m is no longer 100 mm. Image quality differences are modest at 2 m but grow at closer distances.

<details><summary>Hints / solution sketch</summary>
Keep the image-surface position fixed relative to the first lens vertex for internal focusing: that is what the TOTR equality enforces. Which way must the rear group move? Try a ±1 mm change of `THIC` 6 by hand (with `THIC` 9 compensating to keep the track) and watch where best focus goes, then explain the direction with a thin-lens sketch of the telephoto (Kidger Fig. 9.11) before letting the optimizer finish the job.
</details>

## Task 4 — Fixed focus over a working volume (OpticStudio + analysis)
**Goal:** Model a 3D camera's depth range and discover its first-order limits.
**Given / specs:** your NIR lens `../L05-optimization-strategies-and-global-search/work/L05_T4_nir_hammer.zmx` (f = 8 mm, F/2, 940 nm). Pixel 3.0 µm.
**Steps:**
1. Pen & paper first: with Newton's equation, compute the image-side focus positions for objects at 300, 450, 600 and 1000 mm, the half-range of focus shift, and the geometric blur diameter ($c \approx \delta/N$) at the ends if the sensor sits in the middle, for F/2 and F/4. Repeat for a 500–1000 mm range. Compare with the diffraction DOF ±2λN².
2. Build four configurations (`THIC` 0 = 300, 450, 600, 1000 mm); image distance shared (LDE variable).
3. Optimize with the default MF over all configurations (Wavefront or Spot, your choice — justify it), radii and spacings variable.
4. Evaluate MTF at 83 cycles/mm (Nyquist/2) in each configuration. Then change the aperture to F/4 and repeat.
**Deliverable:** pen-and-paper table, MTF table per configuration for F/2 and F/4, conclusion.
**Check yourself:** image shifts 0.219, 0.145, 0.108, 0.065 mm (300→1000 mm); half-range ±77 µm → blur ≈ 39 µm at F/2 (13 pixels!), ≈ 19 µm at F/4; F/# ≈ 13 would be needed for a 2-pixel (6 µm) blur. For 500–1000 mm: ±33 µm → 16 µm (F/2), 8 µm (F/4). Diffraction DOF at F/2, 940 nm is only ±7.5 µm. The optimizer cannot beat first-order geometry: fixed-focus 3D cameras trade aperture (light, speckle) against depth range, use longer working distances, or rely on low-frequency patterns (L02 Task 5).

<details><summary>Hints / solution sketch</summary>
The optimizer will place the sensor near the focus for an object around the harmonic mean of the distances (where image shifts are symmetric), and may slightly "spread" focus through field curvature or spherical aberration — an extended-depth-of-focus effect at the cost of peak contrast.
</details>

## Stretch task — From paraxial to real zoom
Replace the paraxial groups of Task 2 by two cemented doublets (scale your Course 02 L06 achromat to f = −30 and +20 mm; the negative group with the flint first). Optimize all three configurations with `EFFL` targets in custom `CONF` blocks, shared radii, configuration-specific spacings, and the default MF with Configuration = All. Report RMS spot vs field in each configuration and identify which configuration limits the design.

## Reflection questions
1. Which parameters should be LDE variables (shared) and which MCE variables in a zoom lens? In a fixed-focus depth-range design?
2. Why is it good practice to correct each zoom group independently?
3. A merit function with Configuration = All is dominated (80%) by configuration 1. What do you do?
4. Why does internal focusing change the effective focal length while unit focusing does not?
5. Give two non-zoom uses of the MCE relevant to a structured-light 3D camera.

<details><summary>Answers</summary>

1. Zoom: radii, glass, centre thicknesses shared; group spacings (and possibly stop size) per configuration. Fixed-focus depth design: everything shared, only the object distance differs per configuration — the sensor position must be shared.
2. A group whose own aberrations are small does not change the overall balance much when ray heights and conjugates change with zooming; residual aberrations then stay small at all positions instead of cancelling only at one.
3. Check whether configuration 1 is genuinely the hardest (often yes) and whether its weights/field definitions are comparable; consider re-weighting configurations, adding degrees of freedom that help that state, or accepting it as the limiting case. Look at physical metrics per configuration, not just the MF share.
4. In unit focusing the lens is unchanged; only its position changes. Internal focusing changes a separation inside the lens, which changes the combined power ($K = K_1+K_2-dK_1K_2$).
5. Thermal states (0–45 °C) with `TEMP`/`PRES` and thermal pickups (L09); object-distance states for a fixed-focus working volume; wavelength states (850 vs 940 nm variants); tolerance/alignment scenarios; projector and camera sharing a model.
</details>
