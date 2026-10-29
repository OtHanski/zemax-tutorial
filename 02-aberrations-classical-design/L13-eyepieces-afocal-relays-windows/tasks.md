# L13 — Tasks: Eyepieces, afocal systems, field lenses, relays and windows

> Work in `work/` inside this lesson folder (e.g. save `work/L13_T3_telescope.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5–6 h

## Task 1 — Afocal first-order layouts (pen & paper)
**Goal:** Fluency with angular magnification, pupils and eye relief.
**Given / specs:**
- (a) 8×30 binocular (one side), objective $f_o = 120$ mm, object-space semi-field 3.75°.
- (b) Galilean 2.5× with $f_o = 100$ mm.
- (c) Laser beam expander: 1 mm beam in, 10 mm out, total length ≤ 120 mm, both forms.
**Steps:**
1. (a) Compute $f_e$, the exit pupil diameter, the eye relief (thin lenses, stop at the objective) and the eye-space semi-field.
2. (b) Compute $f_e$ and the lens separation. Where is the exit pupil? What limits the field of view?
3. (c) Give Keplerian and Galilean solutions (focal lengths, separations). Which would you use for a 5 W laser, and why?
4. Verify the Lagrange invariant is the same in object and eye space for (a).
**Deliverable:** `work/notes.md`.
**Check yourself:** (a) $f_e = 15$ mm, exit pupil 3.75 mm, eye relief 16.9 mm, eye-space semi-field 27.7° (a demanding eyepiece — compare Kidger's 20–30° range). (b) $f_e = -40$ mm, separation 60 mm; no real exit pupil near the eye — the objective's clear aperture limits the field [Kidger p. 224]. (c) e.g. Keplerian $f_1 = 10$, $f_2 = 100$, $d = 110$; Galilean $f_1 = -10$, $f_2 = 100$, $d = 90$ — Galilean for high power (no internal focus).

<details><summary>Hints / solution sketch</summary>

$|M| = f_o/f_e$; exit pupil $= D/|M|$; eye relief $l' = f_e(1+f_e/f_o)$ from imaging the objective (distance $f_o + f_e$) through the eyepiece. $\tan\theta' = 8\tan3.75^\circ = 0.524$. Lagrange: $H = (D/2)\tan\theta = 15\times0.0655 = 0.983$ mm; eye side $1.875\times0.524 = 0.983$ mm ✓.
</details>

## Task 2 — Plates in converging beams (pen & paper + Python)
**Goal:** Quantify what cover glasses, filters and splitters do.
**Given / specs:** N-BK7 ($n = 1.5168$), λ = 587.6 nm.
**Steps:**
1. Reproduce Geary's window: 20 mm plate in an F/3.33 beam ($u = -0.15$): focus shift, $N$, $S_I$, $W_{040}$ in waves. Then $S_{II}$, $S_{III}$, $S_V$ for a 10° chief ray.
2. A machine-vision camera: 0.7 mm cover glass in an F/2 beam ($u = -0.25$). Focus shift and $W_{040}$. Is it negligible? Does the answer change at F/1.4?
3. Write a Python function for the exact T–S separation and lateral shift of a tilted plate and tabulate them for $t = 1$ mm, $\theta = 0$–45°. Compare the T–S separation with the Seidel estimate $t(n^2-1)\theta^2/n^3$.
4. Convert the 45° value into a geometric blur at F/4 and into pixels for a 3.45 µm pixel sensor.
**Deliverable:** `work/plates.py` and numbers in `notes.md`.
**Check yourself:** (1) 6.81 mm, $N = -7.454$ mm, $S_I = -0.003774$ mm, $W_{040} = -0.80\lambda$; $S_{II} = 0.004436$, $S_{III} = -0.005215$, $S_V = 0.006130$ mm. (2) Δz = 0.239 mm, $S_I = -0.00102$ mm, $W_{040} = -0.22\lambda$ at F/2 — not negligible for a near-diffraction-limited lens, and it scales as $u^4$ (≈ 4× more at F/1.4). (3) 10°: 0.0115 mm per mm of thickness; 45°: 0.269 mm, lateral shift 0.334 mm. (4) ≈ 34 µm ≈ 10 pixels.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
def tilted_plate(t, theta_deg, n=1.5168):
    th = np.radians(theta_deg); g = np.arcsin(np.sin(th)/n)
    dTS = t*(np.sin(th)**2 - np.sin(g)**2)/(n*np.cos(g)**3)
    lat = t*np.sin(th)*(1 - np.cos(th)/np.sqrt(n**2 - np.sin(th)**2))
    return dTS, lat
```
Derivation: Coddington at a plane surface: sagittal $s' = s\,n'/n$, tangential $t' = t\,n'\cos^2\theta'/(n\cos^2\theta)$ (distances along the chief ray); apply at both faces with the glass path $t/\cos\theta_g$ in between and subtract.
</details>

## Task 3 — Ramsden eyepiece and a complete telescope in afocal mode (OpticStudio)
**Goal:** Design an eyepiece in reverse, then evaluate a full afocal system the right way.
**Given / specs (Geary §22.7):** reversed eyepiece: stop (eye pupil) 4 mm diameter, eye relief 10 mm, eye-space semi-field 10° (20° full field), two N-BK7 plano-convex lenses 5 mm thick (plano sides outward), initial separation 32 mm, eye lens convex radius −22 mm (so it focuses just in front of the field lens), field lens convex radius 40 mm, field lens plano face 2 mm from the image plane; F, d, C.
**Steps:**
1. Enter the reversed eyepiece. Variables: both convex radii and the separation. Merit function: `EFFL` = 40, RMS spot default merit function. (Geary also uses `AMAG`; read its Help definition first and decide whether it is meaningful in your set-up.)
2. Examine lateral colour and Field Curvature. Why can't this design correct its lateral colour or Petzval?
3. **Model eye:** add a Paraxial surface (f = 25.4 mm) at the eye pupil in a *forward* copy of the system and let the image (retina) radius vary, as Geary does in §22.6.
4. **Complete telescope:** objective = a 400 mm F/10 achromat (from your L06 work, or a Paraxial surface f = 400 mm as a stand-in), stop at the objective, intermediate image, then your eyepiece reversed (forward direction). Turn on **Afocal Image Space**; choose angular units (arc-min or mrad). Fields: 0, 0.7°, 1.0°.
5. Read the angular ray fans and angular spot diagrams; convert the on-axis marginal angular error into dioptres of defocus ($D = \Delta\alpha / r_{\text{pupil}}$). Adjust the eyepiece spacing to put 0 to −1 dioptre on axis and see the field balance (Kidger's 1-dioptre trick [p. 221]).
**Deliverable:** `work/L13_T3_ramsden_rev.zmx`, `work/L13_T3_telescope_afocal.zmx`, notes.
**Check yourself:** optimized Ramsden radii in the −20 to −25 mm (eye lens) and 35–45 mm (field lens) range with ~30–37 mm separation (Geary's optimized listing shows an eye-lens radius of −22.93 mm and a separation of 37.18 mm; his field-lens radius is illegible in our scan); in the full telescope the exit pupil is ≈ 4 mm and lies near the 10 mm eye relief you designed for, *provided* the objective sits where the reversed design's chief rays cross the axis (otherwise the pupil moves — check it); strong lateral colour at the field edge.

<details><summary>Hints / solution sketch</summary>

- 1 mrad of marginal angular error at a 2 mm pupil radius corresponds to 0.5 dioptre (vergence = angle / height = 0.001/0.002 m = 0.5 m⁻¹).
- If the afocal analyses look nonsensical, check that the last surface before the image is where the eye pupil is and that the system really is afocal (marginal ray angle after the eyepiece ≈ 0).
</details>

## Task 4 — Field lenses in a relay train (OpticStudio)
**Goal:** See vignetting disappear when field lenses are added.
**Given / specs:** three identical relay lenses, each a Paraxial surface of $f = 50$ mm, working at $m = -1$ (object 100 mm → lens → image 100 mm); lens clear semi-diameter 6 mm (set as fixed apertures); object height ±4 mm; object-space NA such that the axial beam just fills the first lens (marginal ray to lens edge: $u = 6/100$); single wavelength.
**Steps:**
1. Build object → L1 → image 1 → L2 → image 2 → L3 → image 3. Plot Relative Illumination / Vignetting Plot at the final image.
2. Add Paraxial field lenses at images 1 and 2 with $1/f_{FL} = 1/a + 1/b$ chosen to image the previous relay lens onto the next one. Repeat the plots.
3. Replace the field-lens focal lengths by ±30% and observe what happens to vignetting.
4. Replace the Paraxial relay lenses with real cemented doublets (any reasonable achromat) and check how Petzval curvature accumulates over three relays (Field Curvature plot).
**Deliverable:** `work/L13_T4_relay.zmx`, before/after plots, notes.
**Check yourself:** $a = b = 100$ mm ⇒ $f_{FL} = 50$ mm. Without field lenses the edge-of-field transmission collapses after the second relay (much of the oblique beam misses L2 and L3); with them the vignetting is essentially gone. Petzval curvature roughly triples over three identical relays.

<details><summary>Hints / solution sketch</summary>

Place the field lenses exactly at the paraxial images first (the lecture's "$h=0$" case) — then move them 1 mm away and confirm the change is small. The field lenses add Petzval: with real lenses you can see the trade-off between pupil steering and field curvature.
</details>

## Task 5 — Filters and cover glass in a real lens (OpticStudio)
**Goal:** Make "plates must be in the design" concrete.
**Given / specs:** your optimized triplet from [L09 Task 2](../L09-cooke-triplet/) (50 mm F/4); add a 1.0 mm N-BK7 IR-cut filter 3 mm in front of the image and a 0.7 mm N-BK7 cover glass 0.5 mm in front of the image (adjust the air gaps; keep the image on a solve).
**Steps:**
1. Before re-optimizing: record the paraxial focus shift, RMS spot and Chromatic Focal Shift. Compare the focus shift with $t(n-1)/n$.
2. Re-optimize the lens with the plates present (radii and spaces variable). How much performance did you recover?
3. Tilt the IR filter by 10° about X with two Coordinate Breaks (or the surface Tilt/Decenter tab). Record the astigmatism on axis (Field Curvature at 0° or OPD fan/Zernike coefficients) and the lateral image shift. Compare with Task 2.
**Deliverable:** `work/L13_T5_triplet_plates.zmx` (+ tilted variant), table.
**Check yourself:** total plate thickness 1.7 mm ⇒ paraxial focus shift ≈ 0.58 mm; re-optimization recovers nearly all performance (plates add a little negative spherical and axial colour); the 10° tilt produces ~0.011 mm T–S separation per mm of filter on axis and a lateral shift of ~0.06 mm for 1 mm — small at F/4, but not at F/1.4 with small pixels.

<details><summary>Hints / solution sketch</summary>

For the tilt, the second coordinate break must undo the first (negative angle) *after* the filter's second face, with the thickness solve placed on that coordinate break so the image stays at the right distance (Geary §23.5). Seidel coefficients are not valid once you tilt anything.
</details>

## Stretch task(s)
- **Plössl in reverse:** design a 25 mm Plössl (two identical cemented N-BK7/N-SF2 doublets) for ±20° eye-space field, 4 mm pupil, eye relief ≥ 18 mm; compare with Kidger's Seidel sums (p. 217).
- **Galilean beam expander for 850 nm:** 5× expander with ≤ 60 mm length using two singlets; evaluate in Afocal Image Space at 850 nm; minimize the output RMS wavefront with an aspheric surface.
- [Geary Homework 23.7]: window in the converging beam of the Ch. 3 singlet.

## Reflection questions
1. Why does a field lens at an intermediate image barely change the axial beam but strongly change the off-axis beam? What aberration does it still add?
2. Why can't eyepieces exploit the symmetry principle, and which aberrations suffer as a result?
3. Why should a visual instrument prefer field curvature to astigmatism, while a camera lens often balances them?
4. A protective window sits 20 mm in front of your camera lens (object at 1 m). Do you need to include it in the optical design? What specification matters most?

<details><summary>Answers</summary>

1. At the image the marginal ray height is ~0, so $u' = u - hK \approx u$ for the axial beam; the chief ray is at full height and is bent by $\bar hK$. It still adds Petzval ($S_{IV} = H^2K/n$) and some distortion/lateral colour.
2. The aperture stop is outside (the eye pupil), so the ray paths are not symmetric about the stop; coma, distortion and lateral colour are not automatically cancelled.
3. The eye can accommodate defocus (curvature) as it scans the field but cannot accommodate astigmatism; a camera sensor is flat and fixed, so a balanced T/S (flat mean field) gives the best average MTF.
4. In object space each object point sends a nearly collimated pencil through the window (cone half-angle ≈ (EPD/2)/1000), so its Seidel contribution is tiny, but its transmitted wavefront error (flatness, wedge, inhomogeneity, stress birefringence for plastic) adds directly to the lens's wavefront error and must be specified. Include it in the model anyway (and in stray-light/ghost analyses: AR coatings!).
</details>
