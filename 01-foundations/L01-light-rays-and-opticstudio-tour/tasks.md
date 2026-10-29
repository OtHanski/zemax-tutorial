# L01 — Tasks: Light, Rays and a First Tour of OpticStudio

> Work in `work/` inside this lesson folder (e.g. save `work/L01_singlet_f100.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Snell's law warm-up (pen & paper)
**Goal:** Get fluent with refraction numbers before the software does them for you.
**Given / specs:** N-BK7, $n_d = 1.5168$; $\lambda_d = 587.6$ nm; $c = 2.998\times10^8$ m/s.
**Steps:**
1. Compute the speed of light and the wavelength of d-light inside N-BK7.
2. A ray in air strikes a flat N-BK7 surface at $I = 30°$. Find $I'$.
3. Find the critical angle for N-BK7 → air.
4. Compute the relative error of the paraxial approximation $\sin I \approx I$ at 5°, 10°, 20°, 30°. At which angle does it exceed 1 %?
**Deliverable:** numbers in `work/notes.md`.
**Check yourself:** $I' \approx 19°$; critical angle a little above 41°.

<details><summary>Hints / solution sketch</summary>

1. $v = c/n = 1.976\times10^8$ m/s; $\lambda/n = 387.4$ nm (frequency is unchanged).
2. $\sin I' = 0.5/1.5168 = 0.3296 \Rightarrow I' = 19.25°$.
3. $I_c = \arcsin(1/1.5168) = 41.25°$.
4. 0.13 %, 0.51 %, 2.06 %, 4.72 %. The 1 % level is crossed at about 14° (error ≈ $I^2/6$ → $I = \sqrt{0.06} = 0.245$ rad ≈ 14°).

</details>

## Task 2 — Fermat's principle numerically (Python)
**Goal:** See Snell's law emerge from "minimize optical path length".
**Given / specs:** Point A in air ($n_1 = 1$) at height $h_1 = 10$ mm above a flat interface; point C in N-BK7 ($n_2 = 1.5168$) at depth $h_2 = 10$ mm below it; horizontal separation $X = 20$ mm.
**Steps:**
1. Write $L(x) = n_1\sqrt{x^2 + h_1^2} + n_2\sqrt{(X-x)^2 + h_2^2}$ where $x$ is the crossing point measured horizontally from A's foot.
2. Minimize $L(x)$ with `scipy.optimize.minimize_scalar` (or a brute-force grid with numpy).
3. Compute $\theta_1 = \arctan(x/h_1)$, $\theta_2 = \arctan((X-x)/h_2)$ and compare $n_1\sin\theta_1$ with $n_2\sin\theta_2$.
4. Plot $L(x)$ for $0 \le x \le 20$. How "flat" is the minimum? Compute $L$ at the straight-line crossing $x = 10$.
**Deliverable:** `work/fermat.py` and a plot `work/fermat.png` (not committed if you prefer; record the numbers in notes).
**Check yourself:** the two products agree to at least 6 decimals.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
from scipy.optimize import minimize_scalar
n1, n2, h1, h2, X = 1.0, 1.5168, 10.0, 10.0, 20.0
L = lambda x: n1*np.hypot(x, h1) + n2*np.hypot(X - x, h2)
x = minimize_scalar(L, bounds=(0, X), method="bounded").x
t1, t2 = np.arctan(x/h1), np.arctan((X - x)/h2)
print(x, np.degrees(t1), np.degrees(t2), n1*np.sin(t1), n2*np.sin(t2))
```
Expected: $x \approx 13.707$ mm, $\theta_1 \approx 53.89°$, $\theta_2 \approx 32.18°$, both sides ≈ 0.80786. $L_{\min} \approx 34.889$ mm vs. $L(10) \approx 35.593$ mm. The minimum is quadratic (flat): moving the crossing point by 1 mm changes $L$ only by a few hundredths of a mm — that "stationarity" is what makes wavefront error insensitive to small ray-position errors.

</details>

## Task 3 — Your first session: the Course 01 reference singlet (OpticStudio)
**Goal:** Set up, analyze, focus and save the lens you will reuse in L02–L07.
**Given / specs:**
- Object at infinity; Aperture Type = Entrance Pupil Diameter = 20 mm (F/5).
- Fields (angle, degrees): 0, 3.5, 5; weights 1.
- Wavelengths: F, d, C preset (0.4861, 0.5876, 0.6563 µm), primary = d.
- Lens: STO radius +102.7 mm, thickness 4 mm, material N-BK7; surface 2 radius −102.7 mm, thickness 95 mm (initial guess). Semi-diameters automatic.
**Steps:**
1. Follow lecture §6.2 steps 1–9. Take a screenshot (for yourself) of the Cross-Section with 95 mm back distance.
2. Put a **Marginal Ray Height** solve (height 0) on the thickness of surface 2. Note the new thickness.
3. Open Analyze → Reports → System Data. Record: EFL, BFL, Image Space F/#, Paraxial Working F/#, Working F/#, Paraxial Image Height, Total Track, Entrance Pupil Position, Exit Pupil Position and Diameter.
4. Open a Standard Spot Diagram (default settings, plus "Show Airy Disk"). Record RMS and GEO radius for each field.
5. Remove the solve (Solve Type → Fixed). Run Quick Focus (RMS Spot Radius, Use Centroid). Record the new back thickness and the new RMS radii.
6. Save as `work/L01_singlet_f100.zmx`. Close OpticStudio, re-open the file and confirm the spot diagram window re-appears (this is the `.zda` session file at work). Look in the folder and identify the `.zda` file.
**Deliverable:** `work/L01_singlet_f100.zmx` (+ its `.zda`), a table of the recorded numbers in `work/notes.md`.
**Check yourself:**
- EFL ≈ 100.0 mm, BFL (M-solve) ≈ 98.70 mm, Image Space F/# ≈ 5.0, paraxial image height ≈ 8.75 mm, total track ≈ 102.7 mm.
- Spots at paraxial focus: on axis the polychromatic RMS radius is of order 100 µm; at 5° it is larger (~150–200 µm). Airy radius ≈ 3.6 µm — the Airy circle is a tiny dot.
- After Quick Focus the back distance shortens by roughly 1.5–2 mm (≈ 97 mm) and the RMS spots shrink to roughly 60–90 µm across the field. Exact values depend on Quick Focus and spot-diagram sampling settings.

<details><summary>Hints / solution sketch</summary>

- If your EFL is −100 mm, you swapped the radius signs (biconvex = $R_1 > 0$, $R_2 < 0$).
- The three F-numbers: Image Space F/# = EFL/EPD = 5.00; the paraxial working F/# also ≈ 5.0 (object at infinity); the real-ray "Working F/#" differs slightly because it uses $1/(2\sin U')$ of the real marginal ray.
- The stop is on the first lens surface, so the entrance pupil is at the first surface (position 0) with diameter 20 mm.
- Quick Focus moves the image *towards* the lens: the rim rays of a positive singlet focus short of the paraxial focus (spherical aberration), and the "best compromise" plane lies between marginal and paraxial foci.

</details>

## Task 4 — Reproduce Geary's 2002 first session in modern OpticStudio
**Goal:** Practise translating old ZEMAX instructions into the ribbon UI — you will do this throughout the course.
**Given / specs:** [Geary §2.2–2.4, pp. 11–17]: OBJ; surface 1 dummy, thickness 25 mm; STO thickness 0; surface 3 radius 100, thickness 10, glass BK7 (use **N-BK7** — the modern lead-free equivalent with practically the same $n_d$); surface 4 radius −100, Marginal Ray Height solve; semi-diameters 25 mm on surfaces 3 and 4; EPD = 40 mm; fields 0°, 7.07°, 10°; wavelengths F, d, C (primary d).
**Steps:**
1. Enter the system. Note: Geary's "Gen" dialog = System Explorer → Aperture; "Fie" = Field Data Editor; "Wav" = Wavelength settings; "Lay" = Cross-Section; "Sys" = System Data report; "Spt" = Standard Spot Diagram; "Pre" = Prescription Data report.
2. Compare your System Data with Geary Fig. 2.4: EFL, BFL, Image Space F/#.
3. Open a Ray Fan (Analyze → Aberrations → Ray Fan), Spot Diagram and Field Curvature/Distortion, i.e. Geary's Fig. 2.6. Arrange them side by side.
4. Open Analyze → Reports → Prescription Data and find the refractive index of N-BK7 at the three wavelengths (Geary §2.7 says this needed the "Index Data" setting; in current versions the index table is part of the report — look for it).
5. Save as `work/L01_geary_biconvex.zmx`.
**Deliverable:** saved file; a short comparison table in notes.
**Check yourself:** EFL ≈ 98.43 mm, BFL ≈ 95.07 mm, F/# ≈ 2.46 (Geary: 98.42, 95.068, 2.46). On-axis polychromatic RMS spot ≈ 0.7 mm (Geary prints ≈ 740 µm). Indices: ≈ 1.5224 (F), 1.5168 (d), 1.5143 (C).

<details><summary>Hints / solution sketch</summary>

The tiny differences from Geary come from old BK7 vs. N-BK7 data and from sampling. A Python trace with a square pupil grid gives on-axis RMS ≈ 733 µm and ≈ 1.05 mm and 1.38 mm at 7.07° and 10° — compare with Geary's spot diagram (≈ 740 µm, 1.1 mm, 1.4 mm). This lens is F/2.5 with a 10° field: an aberration disaster, which is exactly the point of Geary's Fig. 1.6.

</details>

## Task 5 — Is it diffraction-limited? (analysis)
**Goal:** Build the reflex of comparing geometric spot to the Airy disk.
**Steps:**
1. For your Task 3 lens after Quick Focus, compute the ratio (on-axis RMS spot *diameter*) / (Airy diameter).
2. Change the aperture to EPD = 2 mm (F/50) and Quick Focus again. Repeat the comparison. Look at the spot diagram with the Airy circle.
3. Explain in two or three sentences which analyses you would trust for each case.
**Deliverable:** notes.
**Check yourself:** at F/5 the ratio is ~15–20 (aberration-limited). At F/50 the Airy diameter is 2.44 × 0.5876 × 50 ≈ 72 µm while the geometric spot is now only a few µm (spherical aberration scales with the cube of the aperture; axial colour with the aperture) — diffraction-limited.

<details><summary>Hints / solution sketch</summary>

At F/50 the ray-traced spot is much smaller than the Airy disk; the "real" image of a point is the Airy pattern, so ray spot diagrams overstate sharpness. Use wavefront/OPD, Strehl and FFT MTF/PSF there (Course 03). At F/5 geometric metrics describe the blur well. Restore EPD = 20 mm afterwards (do not overwrite your saved file).

</details>

## Stretch task — git-friendly workflow
Create a git repository for your course work (if you haven't). Commit `L01_singlet_f100.zmx`. Change the thickness of the lens to 6 mm, save, and run `git diff`. Identify the lines in the `.zmx` text file that changed (look for `DISZ`, `CURV`, `GLAS` keywords). Note: `CURV` stores curvature $1/R$, not radius — a preview of L02. Revert the change.

## Reflection questions
1. Why do two lenses with the same focal length produce images of the same size but different quality?
2. A colleague says "this lens has 20 µm RMS spots, so it can resolve 10 µm features". What else would you want to know before agreeing?
3. Why is the field point at 0.7 of the maximum field a sensible choice for a "middle" field?
4. Why does Quick Focus move the image plane towards the lens for a simple positive singlet?
5. Which file(s) would you email to a colleague who must open your design on another PC with a custom glass catalogue?

<details><summary>Answers</summary>

1. Image size is set by focal length (first-order optics); quality is set by aberrations, which depend on shapes, glasses and spacings, not on focal length alone [Geary §1.2.1].
2. The wavelength and F-number (is the Airy disk larger than 20 µm?), the field position, the pixel pitch / detector sampling, and whether the spot is representative of MTF at the frequency of interest (Course 03).
3. A radius of $1/\sqrt{2} \approx 0.707$ splits a circular field (or pupil) into an inner disk and outer annulus of equal area [Geary §2.8.2].
4. Undercorrected spherical aberration: rays through the rim of the lens focus closer to it than paraxial rays; the minimum-RMS plane lies between paraxial and marginal foci.
5. A `.zar` archive (File → Create Archive) — it bundles catalogues, coatings and other dependencies with the lens file.

</details>
