# L01 — Tasks: Manufacturing processes and tolerances

> Work in `work/` inside this lesson folder (e.g. `work/tolconv.py`, `work/L01_T3_singlet_perturbed.zmx`). Commit your files and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — A tolerance unit converter (Python)
**Goal:** Never again be confused by fringes, %, ETD and arc-minutes. You will reuse this module in L02, L06 and L08.
**Given / specs:** test wavelength 632.8 nm (double-pass fringes: 1 fringe = λ/2 surface height); N-BK7 $n_d$ = 1.5168.
**Steps:**
1. Write `work/tolconv.py` with functions:
   - `sag(R, r)` — exact spherical sag;
   - `fringes_from_dR(R, dR, D, lam=0.6328e-3)` and its inverse `dR_from_fringes(R, N, D, lam)` (use `scipy.optimize.brentq` on the exact sag, and also return the small-sag approximation $\Delta R \approx 4\lambda R^2 N/D^2$);
   - `wedge_from_etd(etd, D)`, `beam_dev(wedge, n)`, `decenter_from_dev(dev, f)`;
   - `wfe_from_irregularity(N, n, lam_test, lam_use)` returning transmitted-wavefront PV in waves at the use wavelength.
2. Reproduce the three parts of the lecture's worked example.
3. Make a table: for $R$ = 10, 20, 50, 100, 500 mm and $D$ = 12 mm, the $\Delta R$ (mm and %) corresponding to 3 fringes.

**Deliverable:** `work/tolconv.py`, table in `work/notes.md`.
**Check yourself:** $R$ = 20, $D$ = 12: ±0.1 % → 3.05 fr; 3 fr → $\Delta R$ = 0.0197 mm exact (0.0211 mm approximate). $R$ = 100: 3 fr → 0.529 mm. ETD 0.010 mm on Ø12 → 2.86′ wedge, 1.48′ beam deviation. 0.5 fr irregularity → 0.096 waves PV at 850 nm.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
from scipy.optimize import brentq
def sag(R, r): return R - np.sign(R)*np.sqrt(R*R - r*r)
def fringes_from_dR(R, dR, D, lam=0.6328e-3):
    r = D/2; return abs(sag(R+dR, r) - sag(R, r))/(lam/2)
def dR_from_fringes(R, N, D, lam=0.6328e-3):
    f = lambda d: fringes_from_dR(R, d, D, lam) - N
    return brentq(f, 1e-9, abs(R)*0.5), 4*lam*R**2*N/D**2
```
The %-equivalent of 3 fringes grows roughly in proportion to $R$ (since $\Delta R/R \propto R/D^2$): 0.038 % at $R$ = 10, 0.098 % at 20, 0.26 % at 50, 0.53 % at 100 and 2.7 % at 500 mm (the small-sag approximation is 39 % off at $R$ = 10, where the surface is nearly a hemisphere over Ø12). Moral: specify long radii in fringes (the test plate measures them easily), steep radii in % or mm.
</details>

## Task 2 — Reading interferograms (pen & paper)
**Goal:** Connect what the polisher sees to the tolerance numbers.
**Given:** A convex surface $R$ = 30 mm, Ø 15 mm, tested against a test plate with the 546.1 nm mercury line.
**Steps:**
1. The polisher sees 4 circular rings across the aperture, with the centre dark and the fringes moving *outward* when she presses gently on the centre of the plate. What is the sag error, and (using `tolconv.py`) the radius error? Is the surface too steep or too flat? (Pressing at the centre closes the gap there — fringes moving outward mean the gap is smallest at the centre.)
2. Another part shows 2 rings in the horizontal direction and 3 in the vertical (elliptical fringes). Express this as power and irregularity. (Hint: shops usually quote power as the average and irregularity as the difference.)
3. Explain why an irregularity of "0.5 fringe" on a lens surface close to the aperture stop is more harmful than the same irregularity on a field lens next to the sensor.

**Deliverable:** answers in `work/notes.md`.

<details><summary>Hints / solution sketch</summary>

1. 4 fringes × 0.546/2 µm = 1.09 µm of sag difference over Ø15. With exact sag: $\Delta R \approx$ 0.033 mm (≈ 0.11 %). Gap smallest at the centre of a convex part under a concave plate means the part is *more* curved than the plate at the centre relative to the edge → the part's radius is shorter (steeper) than the plate's. (In practice shops tell this from fringe motion; do not worry if you get the sign wrong the first time — every polisher has.)
2. Power ≈ 2.5 fringes (mean), irregularity ≈ 1 fringe (astigmatic difference). ISO 10110 notation (L06) would be e.g. 3/2.5(1).
3. Near the stop every field point's beam covers almost the whole surface, so the full PV is in every field's wavefront; near the image each field point uses a small sub-aperture, over which a low-order irregularity is mostly tilt and a little defocus (distortion and local focus) — small wavefront error.
</details>

## Task 3 — Manual tolerancing of the Course 01 singlet (OpticStudio + Python)
**Goal:** Reproduce, in modern OpticStudio, what Geary does by hand in §38.3 — and see that a "simple" tolerance is about focus, not image quality.
**Given:** `../../01-foundations/L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx` (R = ±102.7 mm, t = 4 mm, N-BK7, EPD 20 mm, F/5, EFL ≈ 100.0 mm, BFL ≈ 98.70 mm).
**Steps:**
1. Copy to `work/L01_T3_singlet.zmx`. Put **EFFL** in the MFE with weight 0 as a dashboard; read the paraxial BFL from System Data.
2. Compute with Python (thick-lens formula) and then in OpticStudio by editing the LDE by hand, the EFL change for:
   (a) $R_1$ changed by the radius error equivalent to 3 fringes over Ø 20 mm;
   (b) CT + 0.05 mm;
   (c) $n_d$ + 0.0005 (precision-grade index; in OpticStudio use the glass "Model" solve or a MIL glass — or simply note that TIND will do this for you in L02).
3. Compare each EFL change with the diffraction depth of focus $\pm 2\lambda N^2$ at 587.6 nm, F/5.
4. Combine the four effects (both radii, CT, index) by root-sum-square and decide: does this lens need a focus adjustment in production?

**Deliverable:** table (Python vs OpticStudio) in `work/notes.md`.
**Check yourself:** 3 fringes over Ø20 mm ↔ $\Delta R$ = 0.199 mm (0.19 %) → $\Delta f$ ≈ ±0.096 mm; CT +0.05 mm → $\Delta f$ ≈ +0.008 mm; $\Delta n$ = +0.0005 → $\Delta f$ ≈ −0.096 mm; DOF = ±0.029 mm; RSS ≈ 0.17 mm ≈ 6× the depth of focus — yes, focus must be adjusted (or the image distance becomes the compensator, L02).

<details><summary>Hints / solution sketch</summary>

Thick lens: $\Phi = (n-1)(c_1-c_2) + (n-1)^2 t c_1 c_2/n$. Index error behaves like a radius error ($\Delta f/f \approx -\Delta n/(n-1)$ = −0.097 %). CT barely matters for a thin biconvex lens. This is the general pattern: individual element *power* errors mostly defocus the image, and a single focus compensator removes most of their effect. What a compensator cannot remove — decenters, tilts, irregularity, and the higher-order consequences of power errors — is what L02–L03 are about.
</details>

## Task 4 — Choosing processes and grades for the capstone lens (writing)
**Goal:** Practise the manufacturing judgement you will need in L08.
**Given:** your Course 04 capstone (`../../04-machine-vision-camera-lenses/L10-capstone-machine-vision-lens/work/capstone.zmx`): Ø ≤ 16 mm elements, ≤ 6 glass elements, EFL 8 mm, F/2.4, ~10⁴ units/year.
**Steps:**
1. For each element, write a line: process (polished sphere / PGM / plastic not allowed by S18), likely shop grade for radius, CT, irregularity, centering, and why (position relative to stop, beam footprint, steepness).
2. Use the lecture's conversion of 1 arcmin beam deviation to decenter for an 8 mm focal length (2.3 µm) to argue which elements will need precision centering.
3. Identify the one element you expect to be most sensitive (you will check this guess in L03 and L08).

**Deliverable:** `work/capstone_process_plan.md` (half a page).

## Task 5 — Seeing the cost–tolerance curve (OpticStudio, optional if your licence/region lacks the Cost Estimator)
**Goal:** Put a price on "precision".
**Steps:**
1. Open the singlet from Task 3. On the Tolerance tab, open the **ISO Element Drawing** for surfaces 1–2 (singlet) and look at what is filled in automatically (codes 3/, 4/ — empty or zero until you have tolerance operands; L06 explains).
2. If the **Cost Estimator** is available (Tolerance tab; requires registering with a provider — see the Ansys KB article in References), request estimates for the same lens at commercial, precision and high-precision values from the §5 table (quantity 10).
3. Plot price vs grade.

**Deliverable:** screenshot/table in `work/notes.md`.
**Check yourself:** expect a mild increase from commercial to precision and a sharp increase to high precision (individual processing). Exact prices depend on the provider and date; the shape is the lesson.

## Reflection questions
1. Why are test-plate fringes "double pass", and what would change if a shop reported irregularity as surface height in waves instead?
2. A molded plastic lens has radius tolerance ±1 % but CT tolerance ±0.015 mm — the opposite pattern from polished glass. Why?
3. Why must an asphere's centration be specified with both tilt and decenter, while a sphere's can be described by wedge alone?
4. You can buy precision irregularity (λ/4) on every surface for +30 % element cost, or redesign to reduce the sensitivity of the two worst surfaces. What information do you need to decide?

<details><summary>Answers</summary>

1. The test light crosses the air gap (test plate) or reflects off the surface (Fizeau) and therefore accumulates twice the height difference; one fringe = λ/2 height. Reporting height in waves would halve the number for the same surface — a factor-two ambiguity that must be resolved on the drawing (ISO 10110 uses fringes = λ/2, at a stated wavelength).
2. In molding, thickness is set by the mold cavity and press stroke (very repeatable), while radius is affected by shrinkage and cooling (less predictable, corrected iteratively in the mold). In polishing, CT is set by measured material removal (moderate accuracy) while radius is matched to a test plate (very accurate).
3. A sphere has no unique axis — any line through its centre of curvature is an axis — so only the line connecting the two centres of curvature matters, and its tilt relative to the edge is the wedge. An asphere's axis is fixed in the surface, so it can be both laterally displaced and tilted relative to the other surface independently.
4. The sensitivity table (which surfaces dominate), the cost of a redesign (time, schedule, performance loss), production volume (redesign is a one-off cost, tolerance cost is per part), and the yield model (L03). With volume in the tens of thousands, a redesign almost always wins.
</details>
