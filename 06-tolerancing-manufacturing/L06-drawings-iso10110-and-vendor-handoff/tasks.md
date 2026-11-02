# L06 — Tasks: Drawings, ISO 10110 and vendor hand-off

> Work in `work/` inside this lesson folder (e.g. `work/iso_translate.py`, `work/L06_tpfit.zmx`). Commit your files and a short `work/notes.md` with answers.
> Practice lens: the mechanically structured M12 lens from L05, `../L05-opto-mechanics-and-cad-integration/work/L05_mech.zmx` with `../L05-opto-mechanics-and-cad-integration/work/L05_mech.tol` (itself derived from `../L02-tolerance-data-editor-and-compensators/work/L02_m12_tol.zmx`; EFL ≈ 8 mm, F/2.8, F/d/C wavelengths, spec MTF ≥ 0.30 at 72 lp/mm to 0.9 field). Reuse `../L01-manufacturing-processes-and-tolerances/work/tolconv.py`.
> Estimated time: ~5–6 h
> Confidentiality: if you practise on a real Zivid lens or real vendor documents, keep them out of any public repository.

## Task 1 — A TDE ↔ ISO 10110 translator (Python)
**Goal:** Make the mapping of lecture §3 executable, so drawings and tolerance files can never drift apart. You will reuse `iso_translate.py` in the capstone (L08).
**Given / specs:** element E2 of the worked example — N-SK16, R1 = 12.50 mm (Ø7.0 clear aperture), R2 = −30.00 mm (Ø7.4), TDE: TFRN 3 and TIRR 0.5 on both surfaces, TWAV 0.6328 µm; TSTX/TSTY ±0.02° on S2; TSDX/TSDY ±0.005 mm on S1 (as an alternative model of S1 centring).
**Steps:**
1. Write `work/iso_translate.py` (import `sag`, `dR_from_fringes` from `tolconv.py`) with functions:
   - `form_callout(N_power, N_irr, lam_tde, lam_drawing)` → string like `3/3.5(0.6); λ = 546.07 nm` (round *down* to one decimal unless told otherwise — explain why down is the safe direction);
   - `radial_from_peraxis(T, p=0.95)` and `peraxis_from_radial(sigma, p=0.95)` for normal statistics with limits at ±2σ (Rayleigh: factor $\sqrt{-2\ln(1-p)}/2$);
   - `tilt_from_decenter(d, R)` returning arcmin;
   - `radius_tol_from_fringes(R, N, D, lam)` (exact sag).
2. Produce the drawing callouts for E2 at 632.8 nm and at 546.07 nm, and the equivalent ΔR for each surface.
3. Inverse: the vendor proposes `3/5(1); 4/2'; λ = 546.07 nm` on S2. What TFRN/TIRR (with TWAV = 0.6328) and per-axis TSTX/TSTY must you put into the TDE to evaluate that proposal?
4. Verify `radial_from_peraxis` with a $10^6$-sample numpy Monte Carlo.

**Deliverable:** `work/iso_translate.py`, a table in `notes.md`.
**Check yourself:** 1 fringe at 632.8 nm = 1.159 fringes at 546.07 nm; S1/S2 at 546.07 nm: `3/3.4(0.5)` if rounded down (3.48, 0.58), ΔR = 0.0228 mm (S1) and 0.124 mm (S2); radial 95 % of ±1.2′ per axis = 1.47′; TSDX 0.005 mm on R = 12.5 → 1.38′. Vendor proposal: TFRN 5/1.159 = 4.31, TIRR 0.86 fringes at 632.8 nm (or simply set TWAV = 0.54607 and enter 5 and 1); per-axis tilt ±1.63′ = ±0.0272°.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
LAM633, LAM546 = 632.8e-6, 546.07e-6        # mm
def rescale(N, lam_from, lam_to): return N*lam_from/lam_to
def radial_from_peraxis(T, p=0.95): return np.sqrt(-2*np.log(1-p))*T/2
def peraxis_from_radial(s, p=0.95): return s/(np.sqrt(-2*np.log(1-p))/2)
def tilt_from_decenter(d, R): return np.degrees(d/abs(R))*60   # arcmin
```
- Rounding: rounding a tolerance *down* tightens it (safe vs your model); rounding *up* loosens it. With 3.48 → 3.5 the loosening is 0.6 % — acceptable if you say so (the lecture did); 3.4 is the strictly safe value.
- Why ΔR differs so much between S1 and S2 for the same 3 fringes: the fringe count scales as $\Delta R\,D^2/R^2$ — the flatter S2 tolerates a larger radius error for the same sag change.
- Monte Carlo: `r = np.hypot(rng.normal(0,T/2,N), rng.normal(0,T/2,N)); np.percentile(r,95)` → 1.224 T.
</details>

## Task 2 — An ISO element drawing from the TDE (OpticStudio)
**Goal:** Use the ISO Element Drawing tool and audit what it produces.
**Given:** `L05_mech.zmx` + `L05_mech.tol` (fabrication rows: TFRN/TIRR, TSTX/TSTY or TIRX-type wedge rows, TTHI, TIND/TABB).
**Steps:**
1. Save As `work/L06_drawings.zmx`. Make sure the TDE contains a TWAV row and that all semi-diameters are fixed (L02 Task 1). Add a mechanical semi-diameter (≥ clear SD + 0.5 mm, rounded) to the element closest to the stop, if missing.
2. Tolerance tab → Manufacturing Drawings and Data → **ISO Element Drawing**. General tab: first surface = front surface of the element nearest the stop; type = Singlet. Press **Reset from TDE**.
3. List in `notes.md` which fields were filled automatically and with which values. Compare the 3/ and 4/ entries with `iso_translate.py`. Is the 4/ value the per-axis number or a radial number? Decide what you want written and overwrite it (uncheck "Automatic").
4. Fill by hand (Material and Codes 5–6 tabs): `0/20`, `1/3×0.16`, `2/1;1`, `5/3×0.16; L1×0.010; E0.3` on both surfaces, coating "AR, $R_\text{avg} \le 0.5\,\%$, 420–680 nm, AOI 0–30°" (use the max AOI from your L05 ray trace instead of 30° if you know it), protective chamfers 0.2 × 45°, test wavelength on the drawing.
5. Repeat for one more element (prefer one with a cemented interface if your lens has a doublet — type Doublet).
6. Save/print the drawings (PDF printer or screenshot → `work/L06_E_stop.pdf` / `.png`) and, for the singlet, save the XML from the General tab.
7. Inhomogeneity check (pen & paper): with `2/1` the PV index variation can be 20 × 10⁻⁶. What PV wavefront does that allow through your element's centre thickness, in waves at 587.6 nm? Is class 1 good enough for the element at the stop, given your L03 RMS-wavefront budget?

**Deliverable:** `work/L06_drawings.zmx`, two drawings, XML, audit table and answers in `notes.md`.
**Check yourself:** TEDX/TETX rows do **not** appear (assembly tolerances); untoleranced parameters show nothing (zero). For a 2.8 mm element, class 1 allows 56 nm = 0.095 waves PV at 587.6 nm — comparable to a whole-lens RMS budget once PV/RMS ≈ 3–5 is considered, so ask the vendor what their glass actually achieves (usually much better), or specify class 2 for the stop element.

<details><summary>Hints</summary>

- If "Reset from TDE" shows radius tolerances but no 3/ power, your TDE uses TRAD (mm) rather than TFRN — both are legitimate; write either "R ± ΔR" with `3/–(B)` or the fringe form, not an inconsistent mixture.
- If the tool's location differs in your version, search the ribbon for "ISO". The Ansys KB singlet example (lecture reading) walks through the dialog.
- The drawing is only as good as the TDE: if your wedge is modelled as TSTX on S1 *and* S2 of the same element, the drawing will show centring on both surfaces — decide which surface is the reference (datum) first.
</details>

## Task 3 — Test-plate fitting (OpticStudio)
**Goal:** Snap radii to a vendor's test plates and measure the cost in performance and tolerance yield.
**Given:** `work/L06_drawings.zmx`; any vendor test-plate list shipped with your OpticStudio (choose one; note its name).
**Steps:**
1. Pen & paper warm-up (worked example (c)): design R = 24.37 mm, Ø9 mm, plates 24.20/24.40/24.50 mm. Fringe offset of each at 632.8 nm; which would you use; what ΔR corresponds to 3 fringes here?
2. Save As `work/L06_tpfit.zmx`. Record the baseline: merit function value, EFL, MTF at 72 lp/mm (T/S) at 0, 0.7, 0.9 field, distortion at full field.
3. Make all spherical radii variable (not aspheres, not the stop, not flat surfaces). Keep the L04 merit function including thickness constraints, with the image distance free.
4. Open **Test Plate Fitting** (location varies by version — search the ribbon/Help for "Test Plate"). Choose the vendor list, run with at least two different fitting orders, and keep the better result.
5. Make the remaining radii **fixed** — all radii are now plate radii — and re-optimize air spaces and thicknesses only.
6. Compare with the baseline. Then re-run the L03 sensitivity analysis (RMS wavefront criterion, focus compensator) and a 200-trial Monte Carlo with `L05_mech.tol`. Did the 90 % value move?
7. Write the list of (surface, design R, plate R, fringes offset before re-optimization) in `notes.md`.

**Deliverable:** `work/L06_tpfit.zmx`, comparison table, MC numbers.
**Check yourself:** step 1: 9.5, 1.66 and 7.1 fringes; use 24.40 mm; 3 fringes ↔ ΔR = 0.054 mm. In steps 4–6, a lens with 8–10 spherical surfaces and a dense vendor list typically loses little nominal MTF (a few points at the edge of the field at most) after re-optimizing air spaces; if one surface has no plate within a few percent of its radius, expect a visible change — consider leaving that radius for interferometric testing. If the 90 % Monte Carlo value gets clearly worse, the fitted design is in a more sensitive region: try another fitting order.

<details><summary>Hints / solution sketch</summary>

- Step 1 uses `tolconv.fringes_from_dR(24.37, Rp-24.37, 9.0)`.
- The tool needs radii to be variables; it fixes each fitted radius as it goes. If it reports "no suitable plate", check the plate diameters against your clear apertures and the convex/concave sense.
- Short radii on small lenses are the hardest to match: a plate set is typically spaced by a fixed percentage, and the fringe consequence of a given % offset rises with D²/R.
</details>

## Task 4 — Melt-data fitting and refocus (Python + OpticStudio)
**Goal:** Turn a melt sheet into a usable catalog glass and quantify its effect.
**Given:** a lot of N-SK16 with test report $n_d$ = 1.62010, $\nu_d$ = 60.50 (catalogue: 1.62041, 60.32). Catalogue Sellmeier coefficients for N-SK16 (SCHOTT): B1 = 1.34317774, B2 = 0.241144399, B3 = 0.994317969, C1 = 0.00704687339, C2 = 0.0229005, C3 = 92.7508526 (µm²) — check them against your OpticStudio catalogue.
**Steps:**
1. Write `work/meltfit.py`: compute catalogue $n_d$, $\nu_d$; fit $\Delta n(\lambda) = a + b/\lambda^2$ to the melt; print the melt indices at F, d, C, 850 and 940 nm; classify the lot in SCHOTT tolerance steps.
2. Generate a `.IND` style list of 13 (λ, n) pairs from 0.40 to 1.00 µm with the corrected formula.
3. Libraries → Materials Catalog: create a user catalog `MYMELT.AGF`, use **Fit Index Data** / the Glass Fitting tool (Sellmeier 1) on your points, save the glass as `NSK16_LOT1`. Check the fit residual (should be ≲ 1 × 10⁻⁶). (Alternatively use OpticStudio's melt-data fitting feature if your version has it; glasses it creates are flagged "Melt".)
4. Save `work/L06_tpfit.zmx` As `work/L06_melt.zmx`; replace the N-SK16 element(s) (or, if your lens has no N-SK16, the element with the largest TIND sensitivity in your L03 table, with an analogous Δ) by the melt glass. Quick Focus only: record the focus shift and MTF change. Then re-optimize air spaces only.
5. Pen & paper: how large is the focus shift of an 8 mm thin lens made entirely of this lot, at the d-line? Compare with the d-line depth of focus at F/2.8.

**Deliverable:** `work/meltfit.py`, `MYMELT.AGF` (copy into `work/`), `work/L06_melt.zmx`, notes.
**Check yourself:** catalogue $\nu_d$ = 60.32; $a = -2.567\times10^{-4}$, $b = -1.838\times10^{-5}$ µm²; $\Delta n$ = −0.000335 (F), −0.000310 (d), −0.000299 (C), −0.000282 (850 nm), −0.000278 (940 nm). Lot class: $n_d$ off by 0.00031 → step 3 (outside step 2's ±0.0003), $\nu_d$ +0.29 % → step 2. Thin-lens focus shift +4.0 µm vs ±$2\lambda N^2$ = ±9.2 µm: the focus compensator absorbs it; MTF after refocus essentially unchanged. Generated points include $n$(0.85) = 1.611437.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
B=[1.34317774,0.241144399,0.994317969]; C=[0.00704687339,0.0229005,92.7508526]
n=lambda l: np.sqrt(1+sum(b*l*l/(l*l-c) for b,c in zip(B,C)))
lF,ld,lC=0.4861327,0.5875618,0.6562725
nd=n(ld); dFC=n(lF)-n(lC); ndm,vdm=1.62010,60.50
b=((ndm-1)/vdm-dFC)/(1/lF**2-1/lC**2); a=(ndm-nd)-b/ld**2
```
- With more than two measured lines (a full melt sheet), solve the same model by least squares (`np.linalg.lstsq` on columns [1, 1/λ²]) and look at the residuals: if they are > 2 × 10⁻⁶, the 2-term model is not enough — add a $\lambda^2$ term or refit the full Sellmeier.
- The focus shift sign: lower index → weaker positive lens → longer focal length → image moves away from the lens (+).
- Production view: this lot is fine for a focus-compensated M12 lens. Melt-fitting a *design* to it would only make sense if every lens for the product's life came from this lot.
</details>

## Task 5 — The RFQ package and MTF acceptance spec (writing + OpticStudio)
**Goal:** Produce the document set a lens vendor would quote from — the professional output of Course 06 so far.
**Given:** your files from L02–L06, the Course 04 spec (`../../04-machine-vision-camera-lenses/L04-compact-fixed-focus-lens-project/work/spec.md`), your L03 Monte Carlo (`../L03-sensitivity-and-monte-carlo/`).
**Steps:**
1. Write `work/RFQ_package.md` with the 11 sections of lecture §6 (prescription; element drawings or per-element tolerance table in drawing units; interface drawing summary; tolerance report summary; performance & test spec; coatings; environmental; cosmetic; materials incl. allowed equivalents; packaging/traceability; quality process). Keep it to what *this* lens needs — mark items "N/A" with a reason rather than inventing content.
2. **MTF test spec:** run a 500-trial Monte Carlo with criterion MTF at 72 lp/mm (focus compensator = the image distance, same as the production focus procedure you will write), saving the MTF per field point (use the overlay or a merit function with MTFT/MTFS rows at 0, 0.5, 0.7, 0.9 field and ±y/±x azimuths). From the distribution choose limits that give ≥ 95 % yield at nominal tolerances, and write the spec: source/filter, conjugate, cover glass, focus definition, field points & azimuths, frequencies, T/S limits, max opposite-azimuth difference.
3. Add measurable non-MTF items with tolerances: EFL, flange focal distance/back focus, distortion at full field, relative illumination at 0.9 field, boresight (image-centre offset) — take ranges from the Monte Carlo where possible.
4. Add a short "co-design" variant: which sections would you hand over if the vendor produces the element drawings, and what would you ask to approve?

**Deliverable:** `work/RFQ_package.md`.
**Check yourself:** every limit in the test spec is traceable to an analysis (file + numbers); the focus procedure in the spec is the same as the compensator used in the Monte Carlo; the test spec includes the sensor cover glass in the measurement path; the spec contains at least one asymmetry check (opposite azimuths), because averaged MTF hides tilt/decenter.

<details><summary>Hints</summary>

- A useful pattern for limits: take the 5th percentile of the MC distribution at each field point, subtract a bench-correlation allowance (e.g. 0.03–0.05 MTF), and round down. Then check that the nominal design passes with margin.
- Boresight: in a calibrated 3D camera the principal point is calibrated, but its *range* still matters for the sensor's usable area and for the projector–camera overlap — specify it.
- Environmental and coating durability methods: name the standard your company uses (ISO 9022 parts, ISO 9211-4, or MIL-style); do not invent test parameters you have not agreed with mechanics/quality.
</details>

## Stretch task(s)
- **Scratch–dig translation.** A legacy drawing says "60-40 per MIL-PRF-13830B" for a Ø9 mm element. Write the ISO 10110-7:2017 dimensional and visibility equivalents you would propose, explain the approximation (dig 40 = 0.40 mm diameter → equal-area grade 0.354 → R5 grade 0.4 or 0.25), and draft the e-mail question to the vendor ("which method do your inspectors use?").
- **ZOS-API preview (Course 07).** Write a Python script that reads the TDE of `L06_drawings.zmx` (ZOSPy or plain pythonnet) and prints, for each element, the drawing callouts produced by `iso_translate.py`. This is the seed of an automated "drawings consistent with tolerances" check.
- **Cost curve.** Use the Cost Estimator (Tolerance tab) on one element with `3/5(1)`, `3/3(0.5)` and `3/1(0.25)`, and with `4/3'`, `4/1'`, `4/0.5'`. Plot price vs tolerance (prototype quantities only — say so).

## Reflection questions
1. Why must the test wavelength be written on every surface-form callout, and what happens if a drawing made for 632.8 nm testing is inspected with an old-default 546.07 nm interpretation?
2. Your TDE has TSTX/TSTY = ±0.02° per axis. A colleague writes `4/1.2'` on the drawing. Is that tighter or looser than your model, and by how much at the 95 % level?
3. Why are TEDX/TETX not on the element drawing, and where must they appear instead?
4. When is melt fitting worth doing for a Zivid-type mass-produced lens, and when is specifying a tighter glass step the better choice?
5. Why can test-plate fitting make a design *worse* in Monte Carlo even when the nominal MTF is unchanged?

<details><summary>Answers</summary>

1. Fringes are counted in units of λ/2 of the test light, so the number of fringes for the same physical error depends on λ. 3 fringes at 632.8 nm is 3.48 fringes at 546.07 nm; inspected as "3 fringes at 546.07", the part is held 14 % tighter than you intended (a cost issue); the reverse mistake (a 546.07-nm drawing read at 632.8 nm) loosens it by 16 % (a performance issue). The current ISO 10110-5 requires stating λ; old editions defaulted to 546.07 nm.
2. Your model's radial tilt has a 95th percentile of 1.224 × 1.2′ = 1.47′, so `4/1.2'` is tighter than the model — every part is inside 1.2′. That is safe for performance but may cost more; `4/1.5'` matches the model at 95 %. (If the vendor's distribution piles up at the limit, the drawing value and the model's 95 % value should be matched with the uniform-disc model instead.)
3. They describe how the element sits in the barrel (clearances, seat squareness, runout — L05), which the lens shop that makes the element cannot control or inspect. They belong on the barrel/spacer drawings and the assembly specification, and in the tolerance report.
4. Worth it when glass rows dominate the yield and there is no compensator that absorbs them (EFL-critical, no refocus, apochromatic or very fast designs), and when one lot covers the production quantity, or when you re-fit per lot with adjustable spacers. For focus-compensated M12-type lenses over years of production, a tighter step (and a supplier who controls it) is simpler and robust to lot changes.
5. Fitting moves radii and the optimizer compensates with other variables; the new solution can rely on larger mutual cancellation between surfaces (higher-order balancing), which increases sensitivity to decenters and tilts — the nominal is the same but the derivatives are larger. Always re-tolerance after fitting.
</details>
