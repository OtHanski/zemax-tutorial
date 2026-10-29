# L08 — Tasks: Polarization, Fresnel losses and thin-film coatings

> Work in `work/` inside this lesson folder (e.g. save `work/L08_T3_nir_coated.zmx` and your coating file `work/L08_coatings.DAT` — the working copy lives in your Zemax Coatings folder). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — Fresnel curves (Python)
**Goal:** Reproduce Kenyon's Figs. 9.12, 9.14 and 9.15 numerically and learn the key angles.
**Given / specs:** N-BK7, $n_d = 1.5168$; air $n = 1$.
**Steps:**
1. Implement $r_s, r_p, t_s, t_p$ (Kenyon eqs. 9.71–9.74) and $R$, $T$ (with the $n_2\cos\theta_t/n_1\cos\theta_i$ factor). Check $R + T = 1$.
2. Plot $R_s$, $R_p$ vs AOI for air→glass and glass→air. Mark Brewster's and the critical angle.
3. For glass→air beyond the critical angle, plot the phases of $r_s$ and $r_p$ and their difference. At what AOI does the difference reach 45° (Fresnel rhomb condition)?
4. Compute the Sellmeier index of N-BK7 at 0.94 µm and the normal-incidence reflectance there.
**Deliverable:** `work/fresnel.py`, plots, numbers.
**Check yourself:** $R_0$ = 4.22% (d-line), 4.11% at 940 nm ($n$ = 1.5084); at 45°: $R_s$ = 9.60%, $R_p$ = 0.92%; $\theta_B$ = 56.60°; $\theta_c$ = 41.25°; TIR phase difference at 45° = 39.75°; it reaches 45° at two angles, ≈ 47.9° and ≈ 55.2° for n = 1.5168 (the maximum is ≈ 46.4° at 51.1°, so N-BK7 *just* works as a Fresnel-rhomb glass).

<details><summary>Hints / solution sketch</summary>
Phase difference on TIR: $\tan(\delta/2) = \cos\theta\sqrt{\sin^2\theta - 1/n^2}/\sin^2\theta$ (n = glass index, exit into air). Solve $\delta(\theta) = 45°$ numerically with `brentq` on the two sides of the maximum. Be careful with the sign conventions for $r_p$ — use reflectances and phase *differences*, which are convention-independent.
</details>

## Task 2 — Thin-film calculator and a NIR V-coat (Python)
**Goal:** Build the characteristic-matrix method and design a real coating.
**Given / specs:** substrate N-BK7 (Sellmeier); MgF₂ $n$ = 1.38; SiO₂ $n$ = 1.45; Ta₂O₅ $n$ = 2.07 (take constant over 850–1000 nm for this exercise).
**Steps:**
1. Implement `R(lam, layers, n0, ns, theta, pol)` with the matrix of lecture §4.1 (s and p admittances).
2. Quarter-wave MgF₂ at 550 nm on N-BK7: R at 450/550/650/850 nm and vs AOI 0–45° (s and p).
3. V-coat for 940 nm: glass | Ta₂O₅ ($d_H$) | SiO₂ ($d_L$) | air. Find $(d_H, d_L)$ giving R = 0 at 940 nm (choose the thinnest solution). Plot R from 880 to 1000 nm.
4. V-coat vs AOI: R_s, R_p and the average at 0°, 20°, 30°.
5. Two-quarter-wave design: what inner-layer index would make MgF₂/X/glass a perfect AR at 940 nm?
**Deliverable:** `work/thinfilm.py`, plots, table.
**Check yourself:** MgF₂: 1.64 / 1.28 / 1.46 / 2.11% at 450/550/650/850 nm; at 45°: R_s 4.05%, R_p 0.14%. V-coat: $d_H$ ≈ 41.5 nm, $d_L$ ≈ 207.6 nm; R ≈ 0.03% at 920 and 960 nm, ≈ 0.12–0.16% at 900/980 nm. At AOI 20°: R_s ≈ 0.07%, R_p ≈ 0.05%; at 30°: R_s ≈ 0.38%, R_p ≈ 0.21% (avg ≈ 0.30%). Two-QW inner index ≈ 1.38·√1.508 = 1.69.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
def R(lam, layers, n0=1.0, ns=1.5168, th0=0.0, pol='s'):
    s0 = n0*np.sin(th0)
    def eta(n):
        c = np.sqrt(1 - (s0/n)**2 + 0j); return n*c if pol == 's' else n/c
    M = np.eye(2, dtype=complex)
    for n, d in layers:                       # layers listed from the incident side
        c = np.sqrt(1 - (s0/n)**2 + 0j); phi = 2*np.pi*n*d*c/lam; e = eta(n)
        M = M @ np.array([[np.cos(phi), 1j*np.sin(phi)/e], [1j*e*np.sin(phi), np.cos(phi)]])
    B, C = M @ np.array([1, eta(ns)]); e0 = eta(n0)
    return abs((e0*B - C)/(e0*B + C))**2
```
Use `scipy.optimize.minimize` from a grid of starting points; there are several solutions (adding a half-wave to either layer gives another), prefer the thinnest — more robust to thickness errors and cheaper.
</details>

## Task 3 — Coatings in OpticStudio on the NIR receiver lens
**Goal:** Define, apply and verify coatings; build a transmission budget.
**Given / specs:** your NIR lens `../L05-optimization-strategies-and-global-search/work/L05_T4_nir_hammer.zmx` (920/940/960 nm).
**Steps:**
1. Libraries → Coating Tools → Edit Coating File → save as a copy (e.g. `MYCOAT.DAT`). Add `MATE` entries for `TA2O5` (n = 2.07, k = 0 at 0.8 and 1.1 µm) and `SIO2X` (n = 1.45), and a `COAT V940` with absolute thicknesses (µm) from Task 2 (`is_absolute` = 1). Add an ideal coating with T = 0.9975 for budgeting (see Help for the `IDEAL` line syntax). Select the file in System Explorer → Files; Reload.
2. Coatings analysis (R vs wavelength and R vs angle) for one coated surface: compare with Python Task 2 (remember the actual glass at that surface may not be N-BK7).
3. Turn on polarization (System Explorer → Polarization: Unpolarized). Run the Transmission analysis for: (a) no coatings, (b) a visible MgF₂ quarter-wave coating (the default file's AR-type coating — check its definition), (c) V940 on all air–glass surfaces, (d) the ideal coating.
4. Add the cover glass (if not yet) and a filter modeled as an ideal coating with T = 0.92. Build the transmission budget table at 0, 0.7 and full field.
**Deliverable:** coating file copy in `work/`, `work/L08_T3_nir_coated.zmx`, transmission table, 4–6 sentence comparison.
**Check yourself:** with ~10 air–glass surfaces + 2 cover-glass surfaces: uncoated ≈ 0.6 × filter, visible MgF₂ ≈ 0.77–0.8 × filter, V940 ≈ 0.97 × filter (lecture worked example). Transmission falls slightly toward the field edge because AOIs grow. If the Transmission analysis shows ~100% with coatings off, check that polarization is enabled and the analysis is not set to ignore surfaces.

<details><summary>Hints / solution sketch</summary>
A relative (waves) thickness is tied to the system *primary* wavelength; with 940 nm primary, 0.25 waves of MgF₂ is a 940 nm quarter-wave — not the visible coating you intended. For the visible MgF₂ case either set absolute thickness 0.0996 µm (550 nm/(4·1.38)) or check what the default file's coating actually contains.
</details>

## Task 4 — Polarization across the pupil (OpticStudio)
**Goal:** See diattenuation and retardance in a fast lens and judge whether they matter.
**Given / specs:** Task 3 lens, (a) uncoated, (b) V940.
**Steps:**
1. Polarization Pupil Map at full field with x-linear input: observe the ellipse orientation and ellipticity at the pupil edge.
2. Polarization Ray Trace for a marginal ray at full field: list s/p transmission per surface; find the surface with the largest diattenuation (compare with the largest `RAID` from the footprint).
3. FFT MTF at full field with and without "Use Polarization". Is the difference significant at 83 cycles/mm?
**Deliverable:** screenshots + 3–5 sentences.
**Check yourself:** uncoated surfaces at 30–40° AOI produce visible diattenuation (s/p transmission differences of a few %); the V-coat reduces it. The MTF change is small (≲ 1–2% absolute) for an F/2 lens — polarization effects are second-order for imaging quality but first-order for transmission, ghosts and any polarization-based optics.

## Task 5 — Cross-polarized imaging (pen & paper)
**Goal:** Quantify a common 3D-scanning trick.
**Given / specs:** a projector emits linearly polarized light (x). A shiny metal part reflects specularly (polarization preserved) and a matte part scatters diffusely (fully depolarized). The camera has a linear analyser. Assume an ideal polarizer with 0.5% leakage for the crossed state (extinction ratio 200:1).
**Steps:**
1. Use Jones matrices to compute the camera signal for specular and diffuse light with the analyser parallel (x) and crossed (y).
2. Compute the specular-to-diffuse contrast improvement from crossing.
3. If the projector was unpolarized (LED) and needed its own polarizer, what overall light penalty does the cross-polarized setup cost for the diffuse signal?
**Deliverable:** numbers and a sentence on when the trick is worth it.
**Check yourself:** parallel: specular ×1, diffuse ×0.5; crossed: specular ×0.005, diffuse ×0.5 → specular/diffuse ratio reduced by 200×. With an unpolarized source: 0.5 (source polarizer) × 0.5 (analyser on depolarized light) = 0.25 of the original diffuse signal, i.e. 2 stops.

## Reflection questions
1. Why is the reflectance at normal incidence the same for s and p, but the sign of $r_p$ relative to $r_s$ apparently opposite (Kenyon Fig. 9.13)?
2. Why is a quarter-wave MgF₂ coating not ideal on crown glass, and why does it perform better on high-index glass?
3. Why do interference filters shift to shorter wavelengths at oblique incidence, and what does that imply for placing a 940 nm bandpass filter in a camera with a 30° CRA?
4. When must you turn on polarization in OpticStudio, and when can you ignore it?
5. Why do cemented interfaces rarely need AR coatings?

<details><summary>Answers</summary>

1. At normal incidence s and p are physically identical; the apparent sign difference is purely the convention used to define positive field directions for the reflected p-wave. Reflectances, which are what you measure, agree.
2. The ideal single-layer index is $\sqrt{n_s}$ (≈1.23 for crown glass), lower than MgF₂'s 1.38, leaving ≈1.3%. For $n_s ≈ 1.9$, $\sqrt{n_s} = 1.38$ exactly, so MgF₂ is a near-perfect single-layer AR on high-index glass.
3. The phase thickness of each layer scales with $\cos\theta$ inside the layer, so the whole spectral response moves to shorter λ as AOI grows ($\lambda \approx \lambda_0\sqrt{1-(\sin\theta/n_\text{eff})^2}$). With 30° CRA plus the cone angle, the passband at the sensor corner shifts by tens of nm; either widen the filter, place it where AOIs are small (front of the lens, or in a telecentric space), or design the lens for low CRA.
4. Turn it on for transmission/relative-illumination budgets with coatings, ghost analysis, polarization optics (polarizers, PBS, wave plates, LCoS), TIR prisms, birefringent materials and high-NA PSFs. For aberration-limited image-quality optimization of ordinary lenses it can be off (faster).
5. Index differences between cemented glasses are small (e.g. 1.517/1.673 → R = 0.24%), and cement layers are thin; the reflectance is already at "AR-coated" levels.
</details>
