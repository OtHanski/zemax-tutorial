# L05 — Tasks: Opto-mechanics and CAD integration

> Work in `work/` inside this lesson folder (e.g. save `work/L05_mech.zmx`). Commit your files, scripts and a short `work/notes.md` with answers.
> Practice lens: the same Course 04 fixed-focus lens used in L02–L04, i.e. `../L02-tolerance-data-editor-and-compensators/work/L02_m12_tol.zmx` with `../L02-tolerance-data-editor-and-compensators/work/L02_precision.tol`.
> Estimated time: ~5 h
> Confidentiality: if you use a real Zivid barrel or housing CAD model in Task 4, keep it out of any public repository.

## Task 1 — A barrel stack-up calculator (Python)
**Goal:** Turn a mechanical drawing into element tolerances you can type into the TDE. You will reuse `work/stackup.py` in the capstone (L08).
**Given / specs (drop-in aluminium barrel, assembled at 20 °C):**
- Element L1: N-BK7, OD Ø9.000 0/−0.010 mm; barrel bore Ø9.000 +0.012/0 mm; bore runout (coaxiality to the barrel datum axis) Ø0.008 mm.
- L1 seat: shoulder squareness 0.003 mm and spacer face parallelism 0.004 mm, both measured over the contact diameter Ø7.5 mm.
- Axial chain from the front shoulder to the front vertex of the last element: 3 spacers at ±0.010 mm and 2 lens centre thicknesses at ±0.025 mm, all independent.
- CTE: aluminium 6061 23.6 × 10⁻⁶/K, N-BK7 7.1 × 10⁻⁶/K; for a polycarbonate holder use 65 × 10⁻⁶/K (a typical datasheet value — use your supplier's number in real work). Storage −40…+85 °C.

**Steps:**
1. Worst-case radial decenter of L1 (half the maximum diametral clearance + radial runout).
2. Monte Carlo ($10^6$ samples): OD and bore uniform in their tolerance bands, lens position uniform in the clearance disc, runout uniform in its disc, random directions. Report mean and 95th percentile of the radial decenter, and the per-axis TEDX/TEDY value (normal, limits at ±2σ — OpticStudio's default) that reproduces that 95th percentile (L02 Task 2 did the Rayleigh algebra).
3. Seat tilt of L1 from the spacer alone, then shoulder + spacer combined worst case and RSS.
4. Axial position of the last element: worst case, RSS of the tolerance limits, and Monte Carlo 95th percentile of |error| with uniform parts.
5. Change in diametral clearance of L1 at −40 °C and +85 °C for an aluminium and a polycarbonate holder. What minimum clearance at 20 °C avoids squeezing the lens at −40 °C?

**Deliverable:** `work/stackup.py` (functions, not a flat script), table in `notes.md` with the TDE values you will use in Task 2.
**Check yourself:** worst-case decenter 0.015 mm; MC mean ≈ 0.0045 mm, 95th percentile ≈ 0.0088 mm → TEDX = TEDY ≈ ±0.0072 mm; tilt 0.031° (spacer), 0.053° WC, 0.038° RSS; axial stack ±0.080 mm WC, ±0.039 mm RSS, MC 95 % ≈ 0.044 mm; clearance change for Al −8.9 µm / +9.7 µm, for PC −31 µm / +34 µm.

<details><summary>Hints / solution sketch</summary>

- Decenter WC: $(0.012+0.010)/2 + 0.008/2 = 0.015$ mm. Uniform in a disc of radius $c$: $r = c\sqrt{U}$.
- Per-axis tolerance: $T = 2\sigma$ with $\sigma = r_{95}/\sqrt{-2\ln 0.05} = 0.00879/2.448 = 0.00359$ mm → ±0.0072 mm.
- Tilts: $0.004/7.5$ rad = 0.0306°; WC $(0.004+0.003)/7.5$ = 0.0535°; RSS $\sqrt{0.004^2+0.003^2}/7.5 = 0.005/7.5$ = 0.0382°.
- Axial: WC $3(0.010)+2(0.025) = 0.080$; RSS $\sqrt{3\cdot0.010^2+2\cdot0.025^2} = 0.0394$. For uniform parts σ = RSS/√3 = 0.0227 mm and the sum is nearly normal, so the 95 % two-sided value ≈ 1.92σ ≈ 0.044 mm — note it is *larger* than the "RSS of limits" because RSS-of-limits silently assumes each limit is ~2σ (normal parts), whereas uniform parts put more mass near the limits.
- Thermal: $\Delta c = D(\alpha_\text{h}-\alpha_\text{g})\Delta T$: Al $9\times16.5\times10^{-6}\times60$ = 8.9 µm closing at −40 °C, $\times65$ K = 9.7 µm opening at +85 °C; PC $9\times57.9\times10^{-6}$ → 31.3 µm / 33.9 µm. Minimum diametral clearance ≥ 9 µm with Al — which is close to the whole tolerance band you were given, so either accept that some lenses are lightly squeezed at −40 °C storage (check stress) or use a radially compliant feature (RTV ring, three-pad seat). The PC holder opens by 34 µm when hot: decenter can grow to ~17 µm unless the lens is glued or clamped axially.
</details>

## Task 2 — A mechanically structured tolerance model (OpticStudio)
**Goal:** Replace "one TEDX per element" with a hierarchy that mirrors the hardware, and see what MPVT changes.
**Given:** `L02_m12_tol.zmx` + `L02_precision.tol`; your Task 1 numbers.
**Steps:**
1. Save As `work/L05_mech.zmx`. Sketch the barrel in `notes.md` (ASCII is fine): which element sits on the shoulder, which spacers, where the retainer is, where the lens holder meets the sensor PCB.
2. Reorganize the TDE in three labelled blocks (Comment column):
   - **Barrel/holder:** TETX/TETY over all lens surfaces ±0.10° (barrel tilt in the holder), TEDX/TEDY over all lens surfaces ±0.020 mm (holder-to-sensor decenter), sensor tilt as in L02.
   - **Elements:** TEDX/TEDY per element from Task 1 (±0.0072 mm for the drop-in elements; keep L02's values for the others), TETX/TETY per element ±0.038°.
   - **Fabrication:** wedge as TSTX/TSTY (or TIRX/TIRY) on *one* surface per spherical element; both TSDX/TSDY and TSTX/TSTY on aspheric surfaces.
   Check that TTHI adjust surfaces still match a stacked or drop-in barrel (decide which you are modelling and say so).
3. Sensitivity run (criterion RMS wavefront, Optimize All (DLS) on the focus COMP, XY-symmetric fields). Save `work/L05_sens_frontvertex.txt`.
4. Insert **MPVT** before the barrel-tilt rows with Pivot At = Rear Mechanical Edge (3) — the barrel is held at its rear flange. Rerun and save `work/L05_sens_rearedge.txt`. (MPVT needs Premium/Enterprise; in Professional build the pivot with coordinate breaks and tolerance them with TUTX/TUTY instead.)
5. Pen & paper: for a 15 mm long barrel tilted 0.10° about its rear flange, how far does the front element move sideways? Compare with your element decenter tolerance.
6. Run a 200-trial Monte Carlo with both pivot settings; report mean and 90 % criterion.

**Deliverable:** `work/L05_mech.zmx`, `work/L05_mech.tol`, the two sensitivity reports, a table of the barrel-tilt rows' contributions and MC results.
**Check yourself:** step 5: $15\times0.10\times\pi/180$ = 0.026 mm — larger than any element decenter tolerance. With a focus-only compensator the extra decenter shows up mainly as image shift (boresight) and some asymmetric field blur; the RMS-wavefront change is usually modest because decentering the *whole* lens relative to the sensor is nearly harmless, but the image-position (principal-point) shift is not — which a camera-calibration engineer at Zivid cares about. If the two runs give identical numbers, MPVT is not placed *before* the rows it should affect.

<details><summary>Hints</summary>

- To see the boresight effect explicitly, add a second criterion run with a merit function that tracks the chief-ray image position (e.g. REAY/REAX of the chief ray at the field points) — the criterion "RMS wavefront" is blind to pure image shifts.
- Keep the barrel-level rows' pivot in mind when you compare with mechanical drawings: the mechanical engineer thinks about the flange, not the first vertex.
</details>

## Task 3 — Element vs surface errors: what is actually different? (pen & paper + OpticStudio)
**Goal:** Build intuition for TEDX/TETX vs TSDX/TSTX.
**Steps:**
1. Pen & paper: a spherical surface of radius $R$ = 10 mm decentered by $\delta$ = 0.005 mm is geometrically identical to the same sphere tilted by what angle about its centre of curvature? Express it in degrees.
2. In `work/L05_mech.zmx`, pick the element with the strongest meniscus shape. In a copy (`work/L05_T3.zmx`) add only four operands: TEDX 0.010 mm on the element; TSDX 0.010 mm on its rear surface; TSTX of the angle equivalent to step 1 (for that surface's actual $R$ and 0.010 mm) on the rear surface; TETX 0.04° on the element.
3. Sensitivity with focus compensator. For the max-perturbation case of each, open the saved file (SAVE operand, as in L02 Task 5) and look at the coordinate breaks the tolerancer inserted.
4. Explain why TSDX and the equivalent TSTX give (nearly) the same change, and why TEDX gives a smaller change than TSDX for this meniscus.

**Deliverable:** table of the four changes + three-sentence explanation in `notes.md`.
**Check yourself:** step 1: $\delta/R$ = 0.0005 rad = 0.0286°. TSDX and the equivalent TSTX should agree to within a few percent (they differ only by a piston/vertex-position effect that the focus compensator absorbs). TEDX moves both surfaces together, so the large, opposite aberration contributions of a meniscus's two surfaces stay matched (L04, reflection Q1); TSDX breaks that balance — expect the surface (wedge) error to be clearly worse.

## Task 4 — Export to CAD and bring the barrel back into NSC (OpticStudio)
**Goal:** Close the optical–mechanical loop once by hand.
**Steps:**
1. In `work/L05_mech.zmx`: set fixed mechanical semi-diameters 0.3–0.5 mm larger than the clear apertures, add edge flats where an element will sit on a spacer, and set the **Global Coordinate Reference** to the image (sensor) surface.
2. **File tab → Export → CAD Files:** export STEP of all lens surfaces with an XY-fan of rays (all fields, all wavelengths) → `work/L05_lens.step`. Also export STL without rays and note the difference in file content.
3. Open the STEP in any CAD viewer (FreeCAD is free) and check: units, origin at the sensor, element edges as solids, ray envelope. Measure the closest approach of the marginal rays to the element edges.
4. Make a simple barrel: either (a) a STEP from CAD (a tube with a front shoulder whose inner diameter clears the ray envelope by 0.2 mm, and spacer rings), or (b) in **Part Designer** (saved as `work/L05_barrel.ZPO`) or from built-in NSC primitives (e.g. annulus/cylinder-pipe objects).
5. Convert a copy of the lens to non-sequential (Convert to NSC Group; location varies by version) → `work/L05_nsc.zmx`. Insert the barrel as **CAD Part: STEP/IGES/SAT** (copy the file into `…\Zemax\Objects\CAD Files`) or **CAD Part: Zemax Part Designer**. Give the barrel a black-anodized-like property (absorbing, or Lambertian scatter with ~5 % reflectance, as in Course 05 L07).
6. Add a source that fills the entrance pupil at the edge field and a detector at the sensor. Compare detected power with and without the barrel (vignetting check), and with Ray Splitting + scatter on, look for flux that has hit the barrel or spacers on its way to the detector.

**Deliverable:** `work/L05_lens.step`, barrel file, `work/L05_nsc.zmx`, a screenshot-free description in `notes.md` of the clearances and the stray-light paths found.
**Check yourself:** with a 0.2 mm clearance the barrel should cost < 1 % of the detected power at the traced field (otherwise a semi-diameter or the barrel position is wrong — most often a units or origin mismatch). Spacer inner edges near the stop are the classic stray-light offenders: light grazing a spacer bore scatters directly towards the sensor. If the STEP import fails to trace, check that the solid is closed (IGES often arrives as loose faces).

## Task 5 — A poor-man's STOP analysis (pen & paper + OpticStudio)
**Goal:** Understand what STAR would give you, and do the rigid-body part by hand.
**Given (steady state, assembled at 20 °C):** an image sensor heats the lens holder; the 5.0 mm of aluminium holder that sets the lens-to-sensor distance has a mean temperature of 52 °C; the barrel's internal air spaces (total 3.0 mm of aluminium spacers) average 42 °C. Lens at F/2.8, visible (λ = 0.5876 µm) and NIR (0.85 µm) variants.
**Steps:**
1. Compute the axial growth of the back-focal holder length and of the total spacer length (the glass and its $dn/dT$ are handled in step 3).
2. Compare with the diffraction depth of focus $\pm 2\lambda N^2$ at both wavelengths. Repeat step 1 for a polycarbonate holder (65 × 10⁻⁶/K).
3. In OpticStudio, add two configurations to a copy `work/L05_T5_thermal.zmx` using the 03/L09 approach (TEMP and thermal pickups), but with *different* temperatures per part — since the built-in thermal model assumes one uniform temperature per configuration, set the holder/spacer thicknesses directly with THIC operands in the MCE using your computed values, and the glass temperature via TEMP at the mean lens temperature (≈ 42 °C). Evaluate MTF at 72 lp/mm with and without the focus compensator.
4. Write down which effects your hand model misses and which STAR would capture (radial gradients inside the glass, mount-induced surface deformation, time-dependent warm-up).
5. If your licence includes STAR (look for the STAR tab), open the KB smartphone STOP example (Reading) and identify the Load FEA Data, Fit Assessment and System Viewer steps. If not, note how you would get the same data from the mechanical team (rigid-body motions + Zernike-fitted surface sag + temperature per element).

**Deliverable:** numbers, `work/L05_T5_thermal.zmx`, the effect list in `notes.md`.
**Check yourself:** Al holder: $23.6\times10^{-6}\times5\times32$ = 3.8 µm; spacers: $23.6\times10^{-6}\times3\times22$ = 1.6 µm. Depth of focus ±9.2 µm (0.5876 µm) and ±13.3 µm (0.85 µm), so the aluminium holder uses ~40 % of the visible budget; the PC holder grows 10.4 µm — more than the whole visible depth of focus. The fixed-focus lens without compensator should show a visible MTF drop in the PC case; a professional answer is an athermalized holder (material pairing) or factory focus at operating temperature.

## Stretch tasks
1. **Preload sanity check:** for a threaded retainer with thread pitch diameter 10 mm, use $P \approx Q/(0.2\,D_T)$ to find the torque that gives 20 N preload (enough to hold a ~1 g lens at a few hundred g of shock with margin). Then compute the glass contact stress for a sharp-corner contact (look up the formula in Yoder) — is it below ~7 MPa (a commonly used conservative limit for glass)?
2. **Dynamic CAD link:** if you have Creo or Inventor, link a parametric barrel (CAD Part: Creo Parametric / Autodesk Inventor), expose its inner diameter and optimize it with an NSC merit function to the minimum diameter that keeps detected power within 0.5 % of the no-barrel case.

<details><summary>Stretch 1 hint</summary>

$Q = 0.2\,D_T P = 0.2\times0.010\,\text{m}\times20\,\text{N} = 0.04$ N·m — a few cN·m, far below what a technician applies "by feel". Specify torque on the assembly drawing.
</details>

## Reflection questions
1. Why is a lens's wedge (fabrication) a *surface* tolerance, while its seat in the barrel is an *element* tolerance? Give one case where the two are physically linked.
2. Your mechanical colleague says "bore Ø9 H7, lens Ø9 g6". What do you need to do before those fits become TDE numbers?
3. Why can a whole-barrel decenter of 20 µm be harmless for MTF but unacceptable for a calibrated 3D camera?
4. When is uniform-temperature thermal analysis (03/L09) enough, and when do you need FEA/STAR?
5. Why should the Global Coordinate Reference be a mechanical datum when exporting to CAD?

<details><summary>Answers</summary>

1. Wedge is how the optical axis of the part relates to its own edge — a property the part carries anywhere you put it, so it is modelled by tilting/decentering one surface relative to the other. The seat is how the part's edge/surfaces relate to the barrel axis — the whole element moves. Linked case: when a lens is located by its curved surfaces (self-centring between spacers) rather than its OD, its wedge directly sets how it tilts in the barrel.
2. Convert ISO fit codes into limits (look up the H7/g6 deviations for Ø9 in an ISO 286 table), compute the radial clearance range plus runout, choose a statistical model (Task 1), and translate into per-axis TEDX/TEDY with a stated distribution. Also check the cold-end clearance.
3. Shifting the whole lens relative to the sensor barely changes the wavefront (the lens is used slightly off-axis) — but it moves the principal point by ~20 µm, i.e. several pixels. If it happens *after* calibration (shock, temperature, glue creep), the 3D reconstruction is biased. Stability matters more than the absolute value.
4. Uniform temperature is enough when the whole module soaks to one temperature (environmental spec, slow changes) and parts are free to expand. FEA/STAR is needed for gradients (sensor, LED/laser drivers near the lens, absorbed light in a projector), for mount-induced deformation (bonding, clamping, preload changes) and for transients during warm-up.
5. So that the exported solids land in the mechanical assembly at the right place without manual re-positioning — and so both teams talk about positions in the same frame (e.g. distances from the sensor plane or barrel flange), avoiding sign/origin mistakes.
</details>
