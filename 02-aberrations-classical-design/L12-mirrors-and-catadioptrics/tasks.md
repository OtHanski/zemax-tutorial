# L12 — Tasks: Mirrors and catadioptric systems

> Work in `work/` inside this lesson folder (e.g. save `work/L12_T3_cassegrain.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5–6 h

## Task 1 — Mirror Seidel arithmetic (pen & paper)
**Goal:** Get fluent with $n'=-n$ and conic contributions.
**Given / specs:** concave spherical mirror $R = -400$ mm, EPD 100 mm (F/2), object at infinity, λ = 0.5876 µm.
**Steps:**
1. Compute $f$, $c$, $S_I$ and $W_{040}$ (in µm and waves) of the sphere.
2. Find the conic constant that makes $S_I = 0$. Explain why the answer does not depend on the aperture.
3. Compute the Petzval contribution per $H^2$ (i.e. $P$) and the Petzval radius. Compare with a thin N-BK7 lens ($n=1.5168$) of the same focal length.
4. A positive thin lens ($f=+100$ mm, $n=1.5$) is combined with a concave mirror. What mirror focal length (and radius) makes the total Petzval sum zero?
**Deliverable:** `work/notes.md`.
**Check yourself:** $f = 200$ mm, $c = -0.0025$, $S_I = -2h^4c^3 = 0.1953$ mm, $W_{040} = 24.4$ µm $= 41.5\lambda$; $K = -1$; $P = 2c = -0.005$ mm⁻¹ → Petzval radius $+200$ mm (= $f$, curving away from the lens side), vs. thin lens $P = K/n = 0.0033$, radius $-303$ mm; mirror $f_m = 150$ mm ($R = -300$ mm).

<details><summary>Hints / solution sketch</summary>

$A = hc = -0.125$, $\delta(u/n) = 2hc = -0.25$, $S_I = -A^2h\,\delta = -(0.015625)(50)(-0.25) = 0.1953$. Conic: $\Delta S_I = Kc^3h^4(n'-n) = K(-1.5625\times10^{-8})(6.25\times10^6)(-2) = 0.1953K$ ⇒ $K = -1$; both terms scale as $h^4$, so the aperture cancels. Mirror Petzval $P = -K_{\text{mirror}}$: need $1/(1.5\times100) = 1/f_m$ ⇒ $f_m = 150$ mm.
</details>

## Task 2 — Extend your Seidel script to mirrors and conics (Python)
**Goal:** Verify the Cassegrain/RC formulas yourself.
**Given / specs:** your `seidel.py` from L08; Geary's Cassegrain: $R_1 = -120.598$ cm, $R_2 = -25$ cm, separation −50 cm, EPD 30 cm, semi-field 0.5°.
**Steps:**
1. Add a `K` (conic) array and the contributions $\Delta S_I = Kc^3h^4(n'-n)$, $\Delta S_{II} = (\bar h/h)\Delta S_I$, $\Delta S_{III} = (\bar h/h)^2\Delta S_I$, $\Delta S_V = (\bar h/h)^3\Delta S_I$. Indices: $n = [-1, +1]$ after the two mirrors.
2. Compute EFL, back focus, $m$, $\beta$, the obscuration ratio.
3. Evaluate the Seidel sums for (a) spheres, (b) classical Cassegrain, (c) Ritchey–Chrétien using the lecture formulas. Confirm (b) has $S_I=0$ and (c) has $S_I=S_{II}=0$.
4. Instead of the formula, solve numerically (`scipy.optimize.fsolve`) for $K_1, K_2$ with $S_I = S_{II} = 0$ and compare.
5. Compute $W_{040}$ in waves at 0.55 µm for the all-spherical system.
**Deliverable:** `work/seidel_mirrors.py`, printed table.
**Check yourself:** EFL 342.45 cm, back focus 58.49 cm after the secondary, $m = 5.679$, $\beta = 0.1408$, obscuration 0.171; classic $K_2 = -2.0375$; RC $K_1 = -1.01277$, $K_2 = -2.17123$; spheres: $\Sigma S_I = 0.04649$ cm, $W_{040} = 105.7\lambda$; $\Sigma S_{IV} = 0.001087$ cm for all three variants.

<details><summary>Hints / solution sketch</summary>

```python
dS1 = K*c**3*h**4*(n - n_before)
q = hbar/h
S1 += dS1; S2 += q*dS1; S3 += q**2*dS1; S5 += q**3*dS1
```
With the stop on the primary, $\bar h_1 = 0$, so the primary's conic only affects $S_I$; the secondary sits where $\bar h/h \neq 0$ and its conic moves coma and astigmatism. That is why the RC needs *both* conics changed.
</details>

## Task 3 — Cassegrain → Ritchey–Chrétien in OpticStudio (OpticStudio)
**Goal:** Enter a reflective system correctly and see coma disappear.
**Given / specs:** Geary's Cassegrain (convert to mm: $R_1 = -1205.98$, $R_2 = -250$, separation −500 mm, EPD 300 mm), wavelength 0.55 µm, fields 0°, 0.25°, 0.5°, 1.0°.
**Steps:**
1. LDE: STO = primary (Material MIRROR, thickness −500), secondary (MIRROR, thickness + Marginal Ray Height solve), image. Check EFL and F/# against Task 2.
2. All-spherical: look at the OPD fan and spot diagram (expect ~100 waves of spherical).
3. Classical: primary conic −1, secondary −2.0375. Spot diagram vs. field: what dominates off axis?
4. RC: conics from Task 2. Repeat. Then make both conics variables with `SPHA` = 0 and `COMA` = 0 (Surf 0) and confirm the optimizer reproduces them.
5. Add the hole (primary: Circular Aperture, min radius = secondary semi-diameter) and the obscuration (dummy surface 500 mm in front of the primary, Circular Obscuration). Compare the FFT MTF with and without obscuration.
6. Plot RMS spot radius vs. field (0–1°) for classical and RC (Geary Fig. 26.21) — use the "RMS vs Field" analysis (location varies by version) or a short loop over fields.
**Deliverable:** `work/L12_T3_cassegrain_classic.zmx`, `work/L12_T3_RC.zmx`, plot and notes.
**Check yourself:** on axis both are diffraction-limited; the classical Cassegrain's spot grows linearly with field (coma), the RC's grows roughly quadratically (astigmatism + field curvature) and is much smaller at 0.25–0.5°; the obscured MTF dips at mid frequencies and is slightly higher near cut-off.

<details><summary>Hints / solution sketch</summary>

Negative thickness after a mirror is the most common entry error: if your layout shows the secondary *behind* the primary, the sign is wrong. If the secondary obscuration also clips the reflected beam, you put it on the wrong surface. For a field corrector stretch: add a two-lens fused-silica corrector before focus (Kidger Fig. 13.11) and optimize for a flat field at 1°.
</details>

## Task 4 — Design a Schmidt camera (OpticStudio)
**Goal:** Practise the stop-at-centre-of-curvature principle and the corrector plate.
**Given / specs:** spherical mirror $R = -400$ mm (f = 200 mm), EPD 100 mm (F/2); corrector: N-BK7 plate 5 mm thick, front surface Even Asphere, placed so that its front surface (the stop) is 400 mm in front of the mirror (centre of curvature); fields 0, 3, 5°; wavelength 0.5876 µm first.
**Steps:**
1. Without the asphere: OPD fan on axis and at 5°. Confirm the off-axis fans look like the on-axis ones (no coma/astigmatism).
2. Make the image surface radius variable or set it to −200 mm; confirm the image is a sphere concentric with the mirror.
3. Make the 4th-order coefficient variable; optimize `SPHA` = 0 (or the RMS wavefront default MF). Compare with the formula $a_4 = c^3/(4(n'-n))$.
4. Add F and C wavelengths: quantify spherochromatism (OPD fans per colour, or Chromatic Focal Shift). Then also vary the plate's base radius and the 6th-order term with a polychromatic RMS-wavefront merit function. Where is the neutral zone of your final plate profile (zero local slope)?
5. Replace the curved image with a flat one plus a field-flattening lens close to focus (N-BK7, ~3 mm thick, ~2 mm in front of the image) and re-optimize. What did you gain/lose?
**Deliverable:** `work/L12_T4_schmidt.zmx` (+ flattened variant), notes.
**Check yourself:** $a_4 \approx -7.56\times10^{-9}$ mm⁻³ (on the air→glass front face; sign follows OpticStudio's sag convention), plate edge departure ≈ 47 µm; uncorrected sphere $W_{040} \approx 41.5\lambda$; after correction the residual is mostly 6th-order spherical (a few waves at most at F/2); spherochromatism of order a wave or less between F and C, reduced by the base curvature; neutral zone near 0.87 of the radius after polychromatic optimization.

<details><summary>Hints / solution sketch</summary>

- $a_4 = c^3/(4\Delta n) = (-1/400)^3/(4\times0.5168) = -7.56\times10^{-9}$ mm⁻³; edge sag $= a_4\cdot50^4 = -0.047$ mm. If your optimizer returns the opposite sign, check which plate face carries the asphere ($\Delta n$ changes sign on the glass→air face).
- If off-axis images show coma, your stop is not at the centre of curvature (check the distance plate → mirror = 400 mm, minus nothing for the thin plate's apparent shift — the plate shifts the apparent stop position slightly; that is a second-order effect).
</details>

## Task 5 — Read a catadioptric Seidel table (analysis)
**Goal:** Learn to reason with component-wise Seidel tables.
**Given / specs:** Kidger's Wiedemann Mangin table [Kidger p. 276]: front lens, meniscus (in), mirror, meniscus (out), field lens.
**Steps:**
1. For each component, state which aberration it is mainly there to correct and which it introduces.
2. Why are the two meniscus passes nearly equal in $S_I$ but not identical?
3. Why does the mirror have $C_I = C_{II} = 0$ but the Mangin as a whole needs the front lens for colour?
**Deliverable:** short answers in `notes.md`.
**Check yourself:** compare with the reasoning in Kidger p. 276.

<details><summary>Hints / solution sketch</summary>

Mirror: big positive $S_I$, negative $S_{IV}$. Meniscus passes: large negative $S_I$ (over-correct the mirror) and coma. Field lens: astigmatism/Petzval and residual spherical/coma. Front lens: axial colour of the two glass passes. The two passes differ because the ray heights and angles differ on the way in and out (the beam is converging on the way out).
</details>

## Stretch task(s)
- [Geary Homework 26.7]: turn the Cassegrain into an RC for ±1° purely by optimization, starting from the classic conics.
- [Geary Homework 24.9]: conic constant on a lens surface to null $S_I$ (needs his Ch. 10 singlet).
- **Off-axis parabola collimator** (unobscured): tilt-free off-axis section of a parabola using a decentred aperture or a Coordinate Break; check that on-axis it remains perfect (preview of non-symmetric systems; Seidel analysis is invalid there).

## Reflection questions
1. Why does an aspheric plate at the stop affect only spherical aberration, while the Cassegrain secondary's conic affects coma as well?
2. Why is an RC primary harder to test than a parabola, and what is a null corrector?
3. Give two reasons a machine-vision or projector designer might choose a mirror, and two reasons they usually do not.
4. Why does a Schmidt camera's image lie on a sphere of radius $R/2$?

<details><summary>Answers</summary>

1. Conic contributions scale with $(\bar h/h)^k$; at the stop $\bar h = 0$, so only $\Delta S_I$ survives. At the secondary $\bar h/h \neq 0$.
2. A conic is aberration-free only between its two geometric foci. For a parabola one focus is at infinity, so it can be tested in autocollimation against a large flat; a concave hyperboloid's second focus is virtual, so there is no direct "perfect" test arrangement. In practice both are tested near the centre of curvature with a **null corrector** (lens, mirror or CGH) designed to cancel the mirror's spherical aberration at that conjugate (Kidger p. 267). The HST primary was figured to the wrong conic because its null corrector was mis-spaced (Geary §26.2.2).
3. For: no chromatic aberration (broadband/NIR/UV), folding/compactness, high power handling. Against: obscuration or off-axis complexity, stray light/baffling, tighter tilt tolerances (reflection doubles angular errors), harder testing and mounting.
4. With the stop at the centre of curvature every field point is "on-axis" for the mirror, so the focal points lie on a sphere of radius $f = R/2$ concentric with the mirror.
</details>
