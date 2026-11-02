# L07 — Tasks: Alignment and active alignment

> Work in `work/` inside this lesson folder. Practice lens: the Course 04 M12 lens as toleranced in L05 — `../L05-opto-mechanics-and-cad-integration/work/L05_mech.zmx` with `../L05-opto-mechanics-and-cad-integration/work/L05_mech.tol` (if you skipped L05, use `../L02-tolerance-data-editor-and-compensators/work/L02_m12_tol.zmx` with `L02_precision.tol`). Commit your files, saved tolerance reports (`.txt`), scripts and a short `work/notes.md` with answers.
> Sensor of that lens (04/L04): 7.07 × 5.30 mm, $p$ = 3.45 µm, F/2.8, object at 1000 mm, MTF spec at 72 lp/mm.
> Estimated time: ~6 h

## Task 1 — An active-alignment station in 60 lines (Python)
**Goal:** Own the AA algorithm (through-focus → peak → plane fit) and learn what limits its accuracy.
**Given:** ROIs at the centre and at $(\pm3.380, \pm2.828)$ mm; true best-focus positions (µm) centre 12.00, top-right 12.93, top-left −0.59, bottom-left 5.07, bottom-right 18.59 (the lecture's worked example). Model each ROI's through-focus MTF as $M(z) = 0.6\,\exp[-(z-z_i)^2/(2w^2)] + \text{noise}$ with $w$ = 12 µm, Gaussian noise of standard deviation σ.
**Steps:**
1. Write `work/aa_fit.py`: scan $z$ from −40 to +40 µm in steps $\Delta$; for each ROI find the peak by a parabola fit to the 5 samples around the maximum; fit the plane $z = z_0 + a x + b y$ with `numpy.linalg.lstsq`; convert $a, b$ to tilt angles in degrees.
2. Noise-free: reproduce $z_0$ = 9.60 µm, 0.115° and −0.057°, and the residuals (+2.4 µm centre, −0.6 µm corners).
3. Monte Carlo (2000 repeats): standard deviation of $z_0$ and of both tilts for (Δ, σ) = (5 µm, 0.01) and (5 µm, 0.02).
4. Now use Δ = 2 µm with the same 5-point parabola. Explain the result.
5. Convert the tilt noise into corner defocus at the sensor corner ($r$ = 4.42 mm for the M12 sensor) and compare with the depth of focus $\pm N\cdot 2p$ at F/2.8.

**Deliverable:** script, a table of the Monte Carlo results, two sentences on step 4 in `notes.md`.
**Check yourself:** (5 µm, 0.01): σ($z_0$) ≈ 0.1 µm, σ(tilt) ≈ 0.002°; (5 µm, 0.02): ≈ 0.2 µm and ≈ 0.004–0.005° (exact values depend on the random seed). With Δ = 2 µm and 5 points the parabola only spans ±4 µm of a curve that is 12 µm wide: it sees almost a flat top, so noise moves the vertex a lot — expect several times *worse* results (and occasional outliers). Depth of focus at F/2.8, $c$ = 2p: ±19.3 µm; 0.005° at 4.42 mm is 0.4 µm — the algorithm is not the limit; the cure is.

<details><summary>Hints</summary>

```python
def peak(zs, m):
    k = np.clip(np.argmax(m), 2, len(zs) - 3)
    c = np.polyfit(zs[k-2:k+3], m[k-2:k+3], 2)
    return -c[1] / (2 * c[0])
```
The fit window should cover roughly ±1 width ($w$) of the through-focus curve. Real stations fit more samples or a model of the through-focus MTF, and use several frequencies; the principle is the same. Note that a real ROI also has *separate* tangential and sagittal peaks (astigmatism) — the station must decide which to use.
</details>

## Task 2 — Centering numbers and the centering lens (pen & paper / Python)
**Goal:** Convert between centering quantities and pick an alignment compensator.
**Given / specs:**
- (a) A surface with $R$ = 20 mm is measured in reflection on a rotating spindle; the instrument reports a centre-of-curvature runout (radius) $e$ = 5 µm. The lens is N-BK7-like ($n$ = 1.52), Ø10 mm.
- (b) A lens of $f$ = 10 mm is decentered by 2 µm relative to the spindle axis. Transmission test.
- (c) An objective has six independent decenter/wedge tolerances that each produce on-axis $y$-coma (at their tolerance limit) of 0.040, 0.030, 0.025, 0.020, 0.015, 0.010 waves. Candidate centering lenses: L2 with $s$ = 0.008 waves/µm, L3 with 0.003 waves/µm, L4 with 0.0015 waves/µm. The set screws give an adjustment resolution of 2 µm.

**Steps:**
1. (a) Surface tilt in arcsec; the beam deviation of the lens in transmission if all the error is in this surface; the equivalent wedge expressed as ETD over the diameter.
2. (b) Beam deviation in arcsec.
3. (c) RSS coma; travel each candidate needs to cancel it; a design range with 50 % margin; residual coma after adjustment due to the 2 µm resolution (half a step). Which would you choose, and what else would you check in OpticStudio before deciding (lecture §3.2)?

**Deliverable:** numbers and choice in `notes.md`.
**Check yourself:** (a) 2.5×10⁻⁴ rad = 51.6″; deviation (n−1)ε = 26.8″; ETD = 2.5 µm. (b) 2×10⁻⁴ rad = 41.3″. (c) RSS 0.062 waves; travel 7.8 / 20.7 / 41.4 µm; range ±11.6 / ±31 / ±62 µm; resolution residual 0.008 / 0.003 / 0.0015 waves.

<details><summary>Discussion</summary>

L2 needs the least travel but its 2 µm steps leave 0.008 waves — still small compared with the 0.062 waves it removes, so L2 is acceptable *if* its side effects are small. L4 is the gentlest knob but needs ±60 µm, which may exceed the radial clearance of a compact barrel (and large decenters create their own field-dependent asymmetry). L3 is a typical compromise. In OpticStudio check: (i) MTF at the edge of the field after compensation (does fixing axial coma tilt the image or add astigmatism?), (ii) boresight change per µm (it will be large for a strong element — fine before calibration, critical if it can move later), (iii) mechanical feasibility (access for set screws, glue).
</details>

## Task 3 — Build the AA model (OpticStudio)
**Goal:** A lens file whose tolerancing behaves like a 5-axis AA station.
**Steps:**
1. Save As `work/L07_aa.zmx` (with its TDE). Insert a **Coordinate Break** directly in front of the sensor cover glass (lecture §6.1; if the IR filter sits in the lens holder, the CB goes after it). The air gap is the thickness of the surface in front of the CB; the CB thickness is 0. Label it "AA".
2. Fields: change to **Object Angle** (or Object Height at 1000 mm) and define 9 fields: on-axis; ±x and ±y at the ROI positions; four diagonal corners at about $(\pm2.83, \pm2.12)$ mm on the sensor (0.8 of the half-diagonal). For a first pass use $\theta \approx \arctan(h/f)$ with $f$ = 8 mm: 19.5° in $x$, 14.8° in $y$ for the corners (≈ 23.8° diagonal); then check with a Footprint or spot diagram that the image points land within ~0.1 mm of the targets, adjusting if your distortion is large.
3. Build the AA criterion merit function and save it as `work/aa_crit.MF`: `MTFT` and `MTFS` at 72 lp/mm (= $\nu_N/2$) for all 9 fields (target 1, weight 1; centre weight 2 if you want to mimic a centre-priority recipe). Keep sampling as low as gives a stable value (compare two samplings at nominal).
4. TDE: remove the old focus COMP; add `COMP` on the air gap (range ±0.050 mm — a glue gap), `CPAR` on the AA coordinate break, parameter 3 (Tilt About X) and parameter 4 (Tilt About Y), range ±0.5° each. Keep the sensor die tilt (TETX/TETY on the image surface, ±0.1°) and the barrel/holder tilts from L05; increase the holder tilt to ±0.3° (with AA you can afford a cheaper holder).
5. Use a SAVE operand (L02 Task 5) after one holder-tilt row and run a quick sensitivity with Criterion = Merit Function (loaded `aa_crit.MF`), Comp = Optimize All (DLS), cycles = a small fixed number (e.g. 3–5). Open the saved file: check that the CPAR values on the AA CB are approximately equal and opposite to the effective image tilt you introduced.

**Deliverable:** `work/L07_aa.zmx`, `work/aa_crit.MF`, `work/L07_aa.tol`, a screenshot of the saved file's LDE around the AA CB.
**Check yourself:** for a pure image-surface tilt row, the AA tilt compensator should cancel it almost exactly (the criterion recovers to the nominal within sampling noise). For holder/barrel tilt rows the compensator cancels the image-plane tilt but not the full damage (a tilted lens also sees an asymmetric object field). If the compensators hardly move, your fields are probably still Y-symmetric or the CB is after the image surface.

<details><summary>Hints</summary>

- The CB column headers in the LDE show which parameter is which; CPAR's Int2 is the parameter number.
- Do not add CPAR on parameters 1/2 (decenter): with object-space fields it is degenerate for an MTF criterion (lecture §6.1). Task 5 handles $x, y$ through boresight.
- If the tolerancer complains about ray aiming with the tilted sensor, make sure ray aiming is on (L02 §2).
</details>

## Task 4 — Passive vs active: what does AA buy? (OpticStudio)
**Goal:** Quantify the yield and the compensator ranges of three production scenarios.
**Steps:** With Monte Carlo 300 runs, statistics Normal, criterion = `aa_crit.MF`, and the yield computed as in L03 Task 5 (every MTF row ≥ 0.30 at 72 lp/mm), run:
- **A — passive:** only the focus COMP (thread, ±0.10 mm), no tilt compensators, holder tilt ±0.1° (L05 value).
- **B — AA, cheap holder:** COMP (gap) + both CPAR tilts, holder tilt ±0.3°.
- **C — AA with a finite station:** as B, but cycles reduced to 1–2 and the tilt CPAR ranges reduced to ±0.15°.

Save the reports as `work/L07_MC_A.txt`, `..._B.txt`, `..._C.txt`. Tabulate yield, mean and 90 % criterion, and for B and C the compensator statistics (mean, σ, max of the gap COMP and the two tilts).
**Deliverable:** table + interpretation in `notes.md`: which tolerances still dominate after AA (look at the sensitivity worst offenders with AA compensators active), and what glue gap and stage range you would specify.
**Check yourself:** B should beat A clearly in the corner MTF (tilt-type errors, including the field tilt generated by element decenters, are removed) even with the 3× looser holder. What remains in B is lens-internal asymmetry — element decenters/wedges near the stop (axial coma), astigmatism — the lecture's §1 table in action. In C, any trial whose required tilt exceeds ±0.15° hits the limit; the compensator max in B tells you whether that happens. Expect the gap COMP spread to be a few tens of µm — compare with the ±0.050 mm range, and use mean ± 3σ plus margin to size the nominal glue gap.

## Task 5 — Post-cure shift and post-calibration drift (OpticStudio + Python)
**Goal:** Apply errors *after* the compensators, and turn image shifts into depth errors.
**Steps:**
1. From scenario B, save 20 MC files (Monte Carlo "number to save"). Pick the trial nearest the median criterion and the one nearest the 90th percentile. Save each as `work/L07_unit_med.zmx` and `work/L07_unit_p90.zmx`.
2. In each, create a new TDE containing only post-cure errors on the AA coordinate break: `TUTX`/`TUTY` ±0.01°, `TUDX`/`TUDY` ±0.002 mm, and `TTHI` on the air gap ±0.002 mm (axial shrink spread). **Comp = None.** Run Monte Carlo (200 runs) with the AA criterion. Save `work/L07_postcure_med.txt` and `..._p90.txt`.
3. Find, by repeating step 2 with scaled values, the post-cure tilt and axial spread at which the p90 unit still meets 0.30 in ≥ 90 % of the runs. This is the **specification you give to the process/adhesive engineer**.
4. Rerun step 2 on the median unit with **Criterion = Boresight Error** (lecture §6.3) and only the TUDX/TUDY rows. Record the image shift in µm (or, if your version reports boresight as an angle, convert it).
5. Write `work/drift.py`: for $f$ = 8 mm, $b$ = 150 mm, $p$ = 3.45 µm, compute the depth error $\delta z = z^2\,\delta x/(f b)$ at $z$ = 0.6, 1.0, 1.2 m for lateral image drifts δx = 0.25, 0.5, 1, 2 µm, and the scale error of an axial drift of 1 and 2 µm at a 5.5 mm corner. Compare with the depth noise from 04/L09 (0.144 mm at 1 m for δd = 0.05 px).

**Deliverable:** two post-cure reports, the allowed post-cure spec, `drift.py` and its table.
**Check yourself:** at ±0.01° tilt (corner defocus 0.8 µm at 4.42 mm) and ±2 µm axial spread the post-cure loss should be small (a few hundredths in MTF at most) for the median unit and larger for the p90 unit, whose margin is smaller. Lateral TUDX/TUDY changes MTF essentially not at all but boresight 1:1 — that is the point. `drift.py`: δx = 1 µm gives 0.30 mm (0.6 m), 0.83 mm (1.0 m), 1.20 mm (1.2 m); δx = 0.5 µm gives 0.42 mm at 1 m; axial 2 µm gives 250 ppm = 1.4 µm (0.40 px) at 5.5 mm.

<details><summary>Hints</summary>

- In a single tolerancing run every TDE perturbation is applied *before* the compensators are optimized, so post-cure errors in the same TDE would be "aligned away". The two-stage approach (or a tolerance script / ZOS-API loop, Course 07 L07) is the honest model.
- The saved MC file contains the compensator values as plain numbers — exactly the "glued" state.
</details>

## Task 6 — Calibration-aware error budget for a projector–camera pair (analysis)
**Goal:** Decide which alignment errors matter for a calibrated 3D camera.
**Given:** the Course 04 capstone geometry (receiver $f$ = 8 mm, F/2.4, $p$ = 3.45 µm, baseline 150 mm, working range 0.6–1.2 m) and a projector on the same aluminium bracket (20 mm thick, $\alpha$ = 23 ppm/K).
**Steps:** For each item below decide (i) absorbed by factory calibration, (ii) not absorbed — affects image quality, or (iii) not absorbed — drift after calibration; and give a number where the lecture's formulas allow:
1. Lens decentered 30 µm relative to the sensor at assembly.
2. Sensor tilted 0.08° relative to the best-focus surface after AA.
3. Projector pointing error 0.5° (toe-in) at assembly.
4. Fringe pattern rolled 1° relative to the epipolar direction.
5. A 1 K front-to-back temperature difference through the bracket during operation.
6. Lens–sensor glue creep of 0.5 µm laterally over the first 1000 h.
7. Holder thermal expansion moving focus 5 µm between 20 and 45 °C.

**Deliverable:** a classified table in `notes.md` with numbers and one-line mitigations.
**Check yourself:** 1 → (i) principal point shift 30 µm = 8.7 px; 2 → (ii) corner defocus 7.7 µm at 5.5 mm (≈ half the ±16.6 µm depth of focus — MTF loss, and a keystone that *is* calibrated); 3 → (i) for geometry, but check coverage: 8.7 mm shift of the projected field at 1 m; 4 → (i), depth sensitivity changes by 1 − cos 1° = 0.015 %; 5 → (iii) 173 µrad relative rotation → ≈ 1.15 mm at 1 m, 0.41 mm at 0.6 m; 6 → (iii) 0.42 mm at 1 m; 7 → (ii) and (iii): defocus 5 µm plus scale change 5/8000 = 625 ppm → 3.4 µm (1.0 px) at a 5.5 mm corner.

## Stretch tasks
- **Emulate the station in the tolerancer.** Replace the MTF criterion by a tolerance script or a ZOS-API loop (Course 07 L07) that, for each MC trial, computes through-focus MTF at the 5 ROIs, finds the peaks, fits the plane (your `aa_fit.py`), sets the CB tilts and gap to the fitted values (not the optimizer's), adds peak-finding noise and post-cure errors, and evaluates the spec. Compare the yield with Task 4 B.
- **Centering lens in the TDE.** Put a coordinate-break pair around the element you chose in Task 2 (with a pickup on the second CB), add `CPAR` on the first CB's decenter X/Y with your range, and a criterion that includes on-axis coma (`ZERN` Fringe terms 7/8 at the on-axis field) plus MTF. Show which worst offenders disappear.
- **Projector AA.** In your Course 05 L09 projector, model the light-modulator tilt as a CB with CPAR compensators and evaluate pattern contrast at the fringe frequency at near and far range. Does the optimum tilt differ from the one that maximizes MTF at the mid distance?

## Reflection questions
1. Your Monte Carlo with 6-axis AA shows 70 % yield, limited by on-axis MTF asymmetry. Your manager proposes buying a better AA station. What do you answer?
2. Why should the AA criterion in the tolerancer be the *same* figure of merit the factory station uses, even if another criterion gives a higher predicted yield?
3. Why is it acceptable for a calibrated 3D camera to have a 30 µm principal-point offset, but not a 0.5 µm change of it?
4. Why do adhesive suppliers emphasize "consistent" shrinkage rather than "low" shrinkage? How does a station exploit consistency?
5. Why are the lens–sensor $x, y$ compensators degenerate in an MTF-only tolerancing criterion, and how would you model them meaningfully?

<details><summary>Answers</summary>

1. AA moves the lens rigidly relative to the sensor; it corrects focus, image tilt and centre position, not lens-internal asymmetric aberrations (axial coma, axial astigmatism) from element decenters and wedges. A better station will not help. Options: tighter element centering for the 2–3 worst offenders (cementing on a centering machine, better seats), a centering lens adjusted in the barrel, or desensitizing the design (L04).
2. The compensator finds the optimum of *its* criterion. If the model optimizes a different figure of merit (e.g. average MTF) than the station (e.g. maximize the minimum corner), it predicts alignments the factory never produces, and therefore an optimistic yield. Model what is done, then judge with the spec.
3. Calibration measures and stores the static offset; the 3D reconstruction uses it. A change *after* calibration is unknown to the model and becomes a systematic triangulation error: 0.5 µm ≈ 0.42 mm at 1 m for $f$ = 8 mm, $b$ = 150 mm.
4. A known, repeatable shrinkage is pre-compensated (pre-offset); only its *variation* remains as error. Stations even learn the offset adaptively from the measured before/after shift of recent units. An adhesive with lower but erratic shrinkage leaves a larger residual.
5. With object-space fields, translating the sensor laterally only shifts where the image lands; the criterion (MTF at fixed object fields) does not change, so the optimizer has a flat direction. Model $x, y$ as an alignment-accuracy tolerance on boresight (Boresight Error criterion or REAX/REAY of the on-axis chief ray), or as a compensator with a boresight target in the merit function if the station centres the optical axis on the sensor.
</details>
