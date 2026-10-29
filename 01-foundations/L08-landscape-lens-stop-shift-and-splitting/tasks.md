# L08 — Tasks (Mini-Project): The Landscape Lens, Stop Shift and Lens Splitting

> Work in `work/` inside this lesson folder. Use a consistent naming scheme (e.g. `work/L08_A_scan.zmx`, `work/L08_B_WOLR_o02a.zmx`) and commit after every optimization step with a message stating variables, MF and result. Finish with `work/report.md`.
> Estimated time: ~7–8 h (plan two sessions: Parts A–C, then D–E)

**Project specification (Parts A–C)**

| Item | Value |
|---|---|
| Effective focal length | 100 mm (F-number solve on $R_2$, or `EFFL` operand) |
| Aperture | F/15 (EPD 6.667 mm for the rear landscape; Image Space F/# = 15 for the front landscape) |
| Object | infinity |
| Fields | 0°, 10.5°, 15° (angle), equal weights |
| Wavelength | 0.5876 µm (d), single wavelength; F/d/C only in Part C step 5 |
| Glass | SCHOTT N-BK7, centre thickness 5 mm (bounds 2–8 mm when variable) |
| Image | flat; back focus free (variable) |
| Quality metric | RMS spot radius, centroid reference |

## Part A — Stop-shift study (OpticStudio + analysis)
**Goal:** Reproduce Geary's Fig. 6.7 for our lens and see the stop-shift equations at work.
**Steps:**
1. Build the equiconvex lens: dummy STO surface (thickness = stop distance $d$), S1 $R_1 = 103.36$ mm, $t = 5$ mm, N-BK7; S2 radius by F-number solve F/15; back thickness variable. Aperture EPD = 6.667 mm. Semi-diameters automatic.
2. MFE: rows `EFFL`, `SPHA`, `COMA`, `ASTI`, `FCUR`, `DIST` (surface 0, wave 1) with weight 0; `BLNK`; then the default RMS-spot/centroid MF (Gaussian quadrature, 3 rings × 6 arms).
3. For $d$ = 0.5, 10, 20, 30, 40, 50, 60 mm: Quick Focus (or optimize the back thickness only), record SPHA, COMA, ASTI, FCUR, DIST, the MF and the per-field RMS spots, and the lens semi-diameter.
4. Plot (Python) COMA, ASTI and DIST vs $d$, and the MF vs $d$. Fit COMA with a straight line and ASTI with a parabola.
5. Now make $d$ a variable (plus back focus) and let DLS find the best stop position for this fixed bending.
**Deliverable:** `work/L08_A_scan.zmx`, the plots, a table in notes.
**Check yourself:** SPHA and FCUR stay constant as $d$ changes; COMA varies linearly and crosses zero; ASTI is parabolic with its minimum near the coma zero; DIST grows with $d$. The field MF is best at $d \approx 35$–40 mm (≈ 57 µm in the Python model; RMS ≈ 64 / 18 / 73 µm at 0 / 10.5 / 15°), and the lens must grow from ≈ 3.3 mm to ≈ 14 mm semi-diameter as the stop moves out to 40 mm.

<details><summary>Hints</summary>

- The required lens semi-diameter is roughly $d\tan 15° + 3.33$ mm; at $d = 40$ mm that is ≈ 14 mm.
- If COMA does not cross zero within 0–60 mm for your bending, extend the range or check the sign of $R_1$.
- The stop-shift relation predicts $\text{ASTI}(d)$ is quadratic exactly in the chief-ray-height parameter, which itself is close to linear in $d$ for a thin lens — hence a parabola in $d$.

</details>

## Part B — The Wollaston rear landscape lens (OpticStudio)
**Goal:** Combine bending and stop shift; meet local minima.
**Steps:**
1. From the Part A file at $d = 0.5$ mm, make $R_1$, $d$ (air bounds 0.5–80 mm) and the back focus variables; $R_2$ stays on the F/15 solve. Add glass boundaries (min 2, max 8, edge 1). Optimize (DLS, Automatic). Save `L08_B_WOLR_o01a.zmx`. Record shape, $d$, spots, MF.
2. Restart from a meniscus: $R_1 = -40$ mm, $d = 15$ mm. Optimize again. Save `L08_B_WOLR_o02a.zmx`.
3. Compare: which is better? Look at both Cross-Sections. Which one looks like Geary's Fig. 6.9?
4. For the better design: Ray Fan (identify the residual aberrations at 15°), Field Curvature/Distortion (where are the T and S surfaces relative to the flat image? how much distortion?), Standard Spot with Airy circle.
5. Increase the field to ±25° (fields 0, 17.5, 25°) and re-optimize the better design (thickness may need to be 8–12 mm so surfaces don't cross — Geary used 12 mm). Does the meniscus get more strongly bent?
**Deliverable:** two optimized files + the 25° version, notes with a comparison table.
**Check yourself (Python model, d-light, GQ 4×8; OpticStudio will differ by a few %):**

| Start | Converges to | $R_1$ / $R_2$ (mm) | stop $d$ (mm) | RMS 0 / 10.5 / 15° (µm) |
|---|---|---|---|---|
| equiconvex, $d$ = 0.5–30 | plano-convex, flat towards the stop (local minimum) | ≈ ∞ / −51.7 | ≈ 30 | ≈ 27 / 3 / 27 |
| meniscus $R_1 = -40$, $d = 15$ | Wollaston meniscus, concave towards the stop | ≈ −84 / −32.7 | ≈ 19 | ≈ 14 / 9 / 19 |

The meniscus solution is ≈ 30 % better in MF and is the historical form. Its spots are comparable to the F/15 Airy radius (10.8 µm). DLS in OpticStudio varies curvature, so it can cross through a flat surface; whether *your* run from the equiconvex start reaches the plano or the meniscus valley depends on version and settings — note what happens.

## Part C — The front landscape lens (Geary homework 6.6)
**Goal:** Design the "other" landscape form against Geary's targets.
**Steps:**
1. New file: S1 lens front surface, S2 lens rear surface, a dummy STO surface after the lens at distance $d$, then the image. Keep **Aperture Type = Entrance Pupil Diameter = 6.667 mm**: OpticStudio images the rear stop forward to find the entrance pupil and sizes the stop automatically, so F/15 is maintained as the stop moves (Geary's 2002 concern about the stop diameter). Hold the focal length with an F-number solve (F/15) on $R_2$. *Trap:* if you instead choose Aperture Type = Image Space F/# = 15, an F-number solve becomes degenerate (the EPD simply follows whatever EFL results) — in that case make $R_2$ a variable and hold EFL with an `EFFL` = 100 operand.
2. Start: $R_1 = 40$, $R_2 = 60$ mm (meniscus convex to the object), $t = 5$, $d = 10$ mm. Variables $R_1$ (and $R_2$ if it is not on a solve), $d$ (MNCA 2 / MXCA 30 on the lens-to-stop air space), back focus.
3. Optimize. Compare with Geary's targets: RMS 18 / 12 / 20 µm (0 / 10.5 / 15°) at best focus.
4. Remove the MNCA/MXCA constraint and re-optimize. Does the optimizer try to bring the stop back to the lens (Geary's warning)?
5. Switch to F, d, C wavelengths (no re-optimization). How large are the spots now? Compute the axial-colour blur estimate $\Delta f/(2N)$ and compare.
**Deliverable:** `work/L08_C_front_o01a.zmx`, notes.
**Check yourself:** the Python model converges to $R_1 \approx 18.6$, $R_2 \approx 26.4$ mm (strong meniscus, X ≈ 5.8), stop ≈ 10 mm behind the lens, RMS ≈ 17 / 12 / 20 µm — on Geary's targets. If the stop distance is unconstrained and starts near zero, the optimizer can get stuck with the stop against the lens and an MF ≈ 3× worse. In white light the spots grow to several tens of µm: axial colour blur ≈ 1.54/30 ≈ 0.05 mm diameter dominates.

## Part D — Lens splitting (Geary Ch. 9)
**Goal:** Quantify the power of splitting.
**Given / specs:** EFL 100 mm, F/4 (EPD 25), on axis only, d-light, N-BK7; element thickness 7 mm, air gaps 1 mm; stop at the first surface.
**Steps:**
1. **Singlet:** start equiconvex (±103.36 mm). Variables: $R_1$ and the back focus; $R_2$ by F/4 solve. MF: monitor `SPHA` (weight 0) + default RMS spot (centroid, GQ 4 rings). Optimize. Record SPHA (waves), RMS spot, shape.
2. **Doublet:** two equiconvex elements ±206.72 mm, 1 mm apart. Variables: three radii + back focus; last radius by F/4 solve. Optimize. Record element powers (from System Data or by hand).
3. **Triplet:** three elements ±310.08 mm. Variables: five radii + back focus. Optimize.
4. Plot SPHA and RMS spot vs. number of elements, and compare with Kidger's $1/k^2$ prediction. Compare the triplet spot with the Airy disk (diameter 2.44 λN = 5.73 µm).
5. Open the Seidel Coefficients (or Seidel Diagram) for the triplet and identify which surfaces contribute most spherical aberration. Compare angles of incidence (`RAID` operand, or Single Ray Trace) on the last surface before and after optimization.
**Deliverable:** three files, plot, notes.
**Check yourself:**

| Elements | Geary $W_{040}$ (waves) | Python model: best-focus RMS (µm) | element powers (mm⁻¹) |
|---|---|---|---|
| 1 | 9.64 | ≈ 34 ($R_1 \approx 60$, $R_2 \approx -361$) | 0.0100 |
| 2 | 2.04 | ≈ 6.5 | ≈ 0.0050 / 0.0051 (front weaker) |
| 3 | 0.514 | ≈ 3 | front weakest |

A rough $W_{040}$ estimate from the marginal TSA ($\text{NA}\cdot|\text{TSA}|/4$) gives ≈ 11, 2.1 and ≈ 1 wave in the Python model (this simple estimate includes higher-order terms, so it differs from the Seidel `SPHA` value). The triplet's RMS spot is about the Airy radius (2.87 µm) — near diffraction-limited on axis. Expect your OpticStudio powers to show the same trend as Geary's (0.004796 / 0.005253 for the doublet; 0.003298 / 0.003355 / 0.003429 for the triplet); a 5-variable optimization can settle in slightly different local minima.

## Part E — Design report
Write `work/report.md` (1–2 pages) as if for a colleague:
1. **Specification** (table above).
2. **Approach**: starting points, solves, variables, merit function, constraints, optimization sequence (with file names / commit hashes).
3. **Results**: final prescriptions (radii, thickness, stop position, back focus, semi-diameters "squared up"), spot table vs. field, ray fans, field curvature/distortion, comparison rear vs. front landscape, lens-splitting table.
4. **Limitations**: what cannot be fixed with one glass and one element (axial colour, Petzval), and what you would try next (achromat, field flattener — Course 02).
5. **Lessons learned**: local minima, constraints, sampling.

## Stretch tasks
- **Fizeau transmission sphere** (Geary Homework 9.5, p. 101): 4-inch diameter, F/7.8, 0.6328 µm, BK7 → N-BK7, element thickness 0.5″, spacing 0.2″. Split until the on-axis spot fits inside the Airy disk. Make the last surface concentric with the focus (rays normal to it — "aplanatic/normal" condition) using a curvature solve, monitor `RAID` on the last surface, and use `OPTH`/`DIFF` (or a simpler EFL/BFL constraint) as Geary suggests.
- **Stop-shift equations by hand**: from your Part A data, take SPHA, COMA, ASTI at $d = 0.5$ mm; fit the scale factor $\bar q(d)$ from the COMA line, and predict ASTI($d$) with $S_{III}^* = S_{III} + 2\bar q S_{II} + \bar q^2 S_I$. Compare with OpticStudio.

## Reflection questions
1. Why can't stop shift reduce spherical aberration?
2. Why does the optimum stop distance coincide (approximately) with zero coma and minimum astigmatism?
3. Why is the meniscus bent concave towards the stop in the rear landscape lens?
4. Why does splitting a lens into $k$ elements reduce spherical aberration by about $k^2$, and why does the optimizer make the front element weakest?
5. A colleague wants a ±15° camera lens at F/2.8 from a single element for a 3D sensor. Using what you learned, explain why it won't work and what the minimum change would be.

<details><summary>Answers</summary>

1. Spherical aberration depends only on the marginal ray, which is unchanged when the stop moves at constant NA ($S_I^* = S_I$).
2. Astigmatism after a shift is $S_{III} + 2\bar qS_{II} + \bar q^2S_I$, minimal where its derivative $2(S_{II} + \bar qS_I) = 2S_{II}^*$ vanishes, i.e. where coma is zero.
3. With the stop in front, the off-axis beam strikes the lens off-centre; a meniscus concave to the stop makes the chief ray meet both surfaces at small angles (nearly concentric about the stop), which reduces coma/astigmatism and lets the remaining astigmatism flatten the field.
4. $S_I \propto h^4K^3$ per element; $k$ elements of power $K/k$ give $k \cdot (K/k)^3 = K^3/k^2$. The marginal ray converges through the system, so later elements see smaller $h$ and tolerate more power; equalizing the contributions makes the front element weakest.
5. Spherical aberration grows as the cube of the aperture: going from F/15 to F/2.8 multiplies the ray errors by ≈ (15/2.8)³ ≈ 150, while axial colour blur grows ≈ 5×; the result is spots of hundreds of µm. Minimum change: an achromatic doublet for colour plus splitting/more elements (triplet-class design) for field aberrations — Course 02.

</details>
