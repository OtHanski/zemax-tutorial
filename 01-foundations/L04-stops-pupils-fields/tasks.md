# L04 — Tasks: Stops, Pupils, Fields and the Lagrange Invariant

> Work in `work/` inside this lesson folder (e.g. save `work/L04_T3_stop_front20.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Pupils by hand (pen & paper)
**Goal:** Locate pupils with the Gaussian equation and the principal planes from L03.
**Given / specs:** The Course 01 singlet: EFL $f' = 100.025$ mm, P 1.327 mm right of S1, P′ 1.327 mm left of S2, lens thickness 4 mm. Object at infinity.
**Steps:**
1. A stop is placed 10 mm behind S2. Find the position of the entrance pupil (relative to S1) and its magnification relative to the stop.
2. What stop semi-diameter gives EPD = 20 mm?
3. With that stop, compute the Lagrange invariant for a 5° half-field, and the image height.
4. A camera has a sensor with an 11 mm diagonal and a 16 mm EFL lens. What is the half-field angle at the sensor corner?
**Deliverable:** answers in notes.
**Check yourself:** EP ≈ 14.1 mm behind S1; stop semi-diameter ≈ 8.87 mm; H = 0.875 mm; h′ = 8.75 mm; ≈ 19.0°.

<details><summary>Solution</summary>

1. Stop distance from P′: $l' = 10 + 1.327 = 11.327$ mm. $1/l = 1/l' - 1/f' = 1/11.327 - 1/100.025$ → $l = 12.774$ mm from P, i.e. 14.10 mm behind S1 (virtual EP, behind the lens). Magnification stop/EP: $m = l'/l = 0.8868$.
2. Stop semi-diameter $= 10 \times 0.8868 = 8.87$ mm.
3. $H = y_{EP}\tan\theta = 10 \times 0.087489 = 0.875$ mm (independent of where the stop is!). $h' = H/|u'| = 0.875 \times f'/y_{EP} = 8.751$ mm.
4. $\theta = \arctan(5.5/16) = 18.97°$.

</details>

## Task 2 — Extend your paraxial tracer with pupils (Python)
**Goal:** Add stop/pupil handling to `../L03-paraxial-optics-and-ray-tracing/work/paraxial.py`.
**Steps:**
1. Let the prescription mark one surface as the stop (a flat dummy surface with zero power is fine).
2. EP: trace a ray from the stop centre backwards through the surfaces in front of it (or forwards through the reversed front group) and find its axis crossing; trace a ray from the stop edge to get the EP radius. Do the same forwards for the XP.
3. Compute: EP position (from S1) and diameter, XP position (relative to the image plane) and diameter, $m_p$, image-space F/#, paraxial working F/#, Lagrange invariant.
4. Run for the three stop positions in the lecture worked example (A: at S1; B: 20 mm in front; C: 20 mm behind with stop semi-diameter 7.868 mm).
5. Check the Lagrange invariant is the same at every surface (print it per surface).
**Deliverable:** updated script + table.
**Check yourself:**

| Case | EP pos. (from S1) | EPD | XP pos. (from image) | XPD |
|---|---|---|---|---|
| A stop at S1 | 0 | 20.00 | −101.37 | 20.27 |
| B stop 20 mm before S1 | −20 | 20.00 | −127.13 | 25.42 |
| C stop 20 mm after S2 | +28.43 | 20.00 | (XP = stop) −78.70 | 15.74 |

<details><summary>Hints</summary>

A neat trick: the EP is the image of the stop by the front group, so trace the chief ray through the *whole* system in the normal direction but starting at the stop with $\bar y = 0$ and an arbitrary angle, then extrapolate its object-space segment back to the axis. Linearity lets you scale everything afterwards. For case C the XP is the stop itself: 98.698 − 20 = 78.70 mm in front of the image.

</details>

## Task 3 — Stop position in OpticStudio
**Goal:** See pupils, semi-diameters and image height respond (or not) to stop position.
**Given / specs:** Start from `../L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx` (EPD 20, fields 0/3.5/5°, F/d/C, M-solve on the back thickness). Semi-diameters automatic.
**Steps:**
1. Record System Data: EPD, EP position, XP diameter and position, paraxial image height. Compare with case A.
2. Insert a new surface before the lens (above surface 1), make it the stop (surface properties → "Make Surface Stop"), thickness 20 mm to the lens. Save as `work/L04_T3_stop_front20.zmx`. Record System Data again (case B) and the automatic semi-diameters of the lens surfaces.
3. Move the stop behind the lens: delete the front dummy, give surface 2 a thickness of 20 mm, insert a dummy stop surface after it, M-solve on the stop's thickness. Set Aperture Type = **Float By Stop Size** and the stop semi-diameter to 7.868 mm. Save as `work/L04_T3_stop_rear20.zmx`. Check EPD and EP position (case C).
4. For all three, open the Cross-Section and the Standard Spot Diagram. Does the image height change? Do the spots change? (Look at the 5° field.)
**Deliverable:** two `.zmx` files and a table.
**Check yourself:** image height 8.751 mm in all cases; the lens semi-diameter grows to ≈ 11.8 mm in case B; EPD = 20.0 mm in case C with the EP ≈ 28.4 mm behind S1. The off-axis spots *do* change shape and size with stop position — this is the stop-shift effect you will exploit in L08.

## Task 4 — Aperture types and F-numbers (OpticStudio)
**Goal:** Know which aperture type to use and what the F-numbers mean.
**Steps:**
1. In the L01 singlet, switch Aperture Type to **Image Space F/#** = 5. Check EPD in System Data.
2. Set the object distance to 300 mm (object thickness) and change to Field Type Object Height (0, 10, 15 mm). Record Image Space F/#, Paraxial Working F/#, Working F/#, Image Space NA, Object Space NA, and the paraxial magnification.
3. Switch the aperture to **Object Space NA** and enter the object-space NA you just read. Does anything change?
4. Explain why Working F/# ≠ Paraxial Working F/# here.
**Deliverable:** notes.
**Check yourself:** Image Space F/# ≈ 5.0; Paraxial Working F/# ≈ 7.45 (formula $N_\infty(1 - m/m_p)$ with $m = -0.497$, $m_p = 1.013$); object-space NA ≈ $\sin(\arctan(10/300)) \approx 0.033$; Working F/# close to but not equal to 7.45 (real ray angles include aberration).

## Task 5 — Vignetting, apertures and vignetting factors (OpticStudio)
**Goal:** Learn how OpticStudio treats clipping — and verify for yourself how semi-diameters behave.
**Given / specs:** `work/L04_T3_stop_front20.zmx` (stop 20 mm in front of the lens).
**Steps:**
1. Set both lens surfaces' semi-diameters to **10.5 mm** (fixed, `U`). Look at the Cross-Section and the spot diagram for 5°: are rays outside 10.5 mm removed, or merely drawn beyond the lens edge? Write down what you observe — this tells you how your version treats bare semi-diameters.
2. Now add a **circular aperture** (max radius 10.5 mm) to both lens surfaces (surface properties → Aperture), or use the LDE tool that converts semi-diameters to circular apertures. Re-check Cross-Section, spot diagram and a **Footprint Diagram** on surface 2 (Analyze → Rays & Spots → Footprint Diagram).
3. Open Relative Illumination (Analyze → Illumination → Relative Illumination, or search the ribbon). Note the value at 5°.
4. Run **Set Vignetting** (Field Data Editor tools / Setup ribbon — location varies by version) and look at the VDY/VCY values it computes for each field. Re-check the spot diagram.
**Deliverable:** screenshots for yourself, observations in notes.
**Check yourself:** at 5° the beam on S1 spans −8.25…+11.75 mm, so a 10.5 mm aperture clips the upper part of the beam: the footprint becomes a truncated circle, relative illumination drops below 1 (the clipped area of the decentred 5° beam against the two 10.5 mm holes is ≈ 7 % of the pupil, so expect relative illumination ≈ 0.9 at 5°, a little lower once the small cos-type factors are included), and Set Vignetting gives a non-zero VCY/VDY for the 5° field and ≈ 0 on axis.

<details><summary>Hints</summary>

If the spot diagram did not change in step 1, bare semi-diameters are not hard apertures in your version (the usual behaviour in sequential mode). Hard apertures (step 2) vignette real rays in ray-traced analyses; vignetting factors change which rays are *launched*. For optimization with Gaussian quadrature (L07) you want vignetting factors so that launched rays are not lost.

</details>

## Task 6 — A telecentric singlet (OpticStudio)
**Goal:** Make the singlet image-space telecentric and see the price.
**Steps:**
1. From the case-B file, change the stop-to-lens distance to the front focal distance (98.70 mm — or use the FFL from System Data).
2. Use Single Ray Trace for the chief ray ($H_y = 1$, $P_y = 0$) and read its angle at the image surface. Read the XP position in System Data.
3. Note the semi-diameter needed on the lens and compare with case A.
**Deliverable:** `work/L04_T6_telecentric.zmx`, notes.
**Check yourself:** chief-ray angle at the image ≈ 0 (paraxially exactly 0; real ray slightly non-zero due to pupil aberration); XP position huge (≈ infinite); lens semi-diameter ≈ 18.6 mm vs 10 mm in case A.

## Stretch task
Geary Homework 5.7 (p. 49) gives a Cooke triplet (from W. Smith) with a buried stop and asks for its entrance pupil and the starting marginal/chief rays. The scanned figure is hard to read; instead, open an OpticStudio sample Cooke triplet (Samples folder — search for a "Cooke" or triplet sample file in your installation), and compute its entrance pupil position and diameter with your Python tracer from the prescription. Compare with System Data.

## Reflection questions
1. Why does moving the stop not change the image height of a distortion-free lens, but change the image quality?
2. Why is "Float By Stop Size" the right aperture type for a camera lens with a mechanical iris?
3. What does the Lagrange invariant tell you about trying to make a projector both brighter and wider-angle with the same LED?
4. Why might a sensor manufacturer specify the maximum chief-ray angle, and which pupil controls it?
5. When would you turn on ray aiming?

<details><summary>Answers</summary>

1. First-order imaging (focal length, conjugates) does not depend on the stop; the stop selects *which* part of each lens the off-axis beam passes through, which changes off-axis aberrations.
2. The iris has a fixed physical size; with Float By Stop Size the EPD follows from it automatically, so redesigning the optics in front of the stop cannot silently change the iris.
3. $H^2$ (étendue) is conserved: the LED's emitting area × solid angle bounds what the projector can deliver; a wider field at the same pupil needs more étendue than the source provides — you lose light, or you need a bigger source.
4. Microlens/pixel acceptance falls off with angle (colour crosstalk, shading). The exit pupil position (and the field height) sets the CRA.
5. When the real entrance pupil differs noticeably from the paraxial one (pupil aberration > a few %), when the stop is decentred/tilted, and generally for wide-angle and fast lenses with buried stops.

</details>
