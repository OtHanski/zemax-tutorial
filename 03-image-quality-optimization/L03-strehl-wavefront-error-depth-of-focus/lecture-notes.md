# L03 — Strehl ratio, wavefront error budgets and depth of focus

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~2.5 h, tasks ~5 h
> **Prerequisites:** [L01 — Diffraction and the PSF](../L01-diffraction-and-the-psf/), [L02 — MTF](../L02-mtf-theory-and-practice/), [Course 02 L01 (Zernikes)](../../02-aberrations-classical-design/L01-wavefront-and-transverse-aberrations/), [Course 02 L02 (spherical aberration & defocus balancing)](../../02-aberrations-classical-design/L02-spherical-aberration-and-bending/) · **Next:** [L04 — Merit function mastery](../L04-merit-function-mastery/)

## Learning objectives
- Define the Strehl ratio and compute it from an RMS wavefront error with the Maréchal/exponential approximations — and know where those approximations fail.
- Compute the RMS of common aberrations (defocus, spherical, coma, astigmatism) with and without balancing, and convert a Strehl or RMS target into allowed Seidel/Zernike coefficients.
- Build an RSS wavefront-error budget (design, manufacture, assembly, environment) for a diffraction-limited system.
- Derive the axial intensity $\mathrm{sinc}^2$ law and the diffraction depth of focus $\pm2\lambda N^2$, and contrast it with geometric depth of focus $\pm N c$.
- Find "best focus" under different criteria (minimum blur, minimum RMS spot, maximum Strehl) for spherical aberration, and reproduce Geary's mirror example in OpticStudio.
- Use OpticStudio's Strehl-related outputs (Huygens PSF, Zernike Standard Coefficients, RMS vs Field/Focus) and the wavefront form of the default merit function.

## Reading
- **Core:** [Geary Ch. 31, pp. 355–364] — Strehl definition (eq. 31.2), exponential form (31.3) and its small-aberration expansion (31.5–31.6), wavefront variance (31.7–31.9), the defocus + spherical calculation (§31.2.3), the 400 mm F/4 mirror example (§31.2.4–31.2.6), variance of coma and astigmatism (Table 31.3).
- **Core:** [Geary Ch. 32, pp. 365–376] — axial intensity by the Fourier–Hankel route (§32.2.1, eqs. 32.1–32.26), diffractive depth of focus $\pm2(f/\#)^2\lambda$ (§32.2.2), geometric depth of focus (§32.2.3), the two Rayleigh rules (§32.2.5) and Strehl in ZEMAX (§32.3).
- **Optional:** [Kenyon §7.2.1, eq. 7.23, p. 168] — Strehl ≈ 1 − (2πσ/λ)², λ/14 and the "diffraction-limited" convention.
- **Optional:** [Geary §30.6, pp. 346–350] — image compactness (RMS spot) as the geometric counterpart to wavefront variance.

---

## 1. Strehl ratio

**Definition** [Geary eq. 31.2, p. 356]: the ratio of the peak irradiance of the aberrated PSF to the peak of the aberration-free PSF with the same pupil, wavelength and power. Two variants matter in practice:

- *Strehl at the reference point* (the centre of the reference sphere, usually chief-ray or centroid). This is the quantity the formulas below describe.
- *Peak Strehl*: the PSF maximum wherever it occurs. For symmetric aberrations near focus the two are the same; for coma or tilt the peak moves.

From the Fourier picture of L01 the on-axis amplitude is just the pupil average of the phasor, so

$$
S = \left|\big\langle e^{\,i k W}\big\rangle_\text{pupil}\right|^2, \qquad k = 2\pi/\lambda .
$$

Expanding the exponential for small $W$ (and noting the mean of $W$ — piston — drops out of the modulus) gives

$$
S \approx 1 - (k\sigma)^2 \quad\text{(Maréchal)},\qquad S\approx e^{-(k\sigma)^2}\quad\text{(exponential / "extended Maréchal")},
$$

where $\sigma^2 = \langle W^2\rangle - \langle W\rangle^2$ is the **wavefront variance** over the pupil, weighted by area [Geary eqs. 31.3–31.9]. Compare with exact values (FFT, Task 1) for balanced spherical, coma and astigmatism:

| RMS σ (waves) | Exact S (SA / coma / astig, balanced) | $e^{-(k\sigma)^2}$ | $1-(k\sigma)^2$ |
|---|---|---|---|
| 0.050 | 0.906 / 0.906 / 0.906 | 0.906 | 0.901 |
| 0.0714 (λ/14) | 0.816 / 0.817 / 0.818 | 0.818 | 0.799 |
| 0.100 | 0.668 / 0.670 / 0.673 | 0.674 | 0.605 |
| 0.150 | 0.392 / 0.398 / 0.406 | 0.411 | 0.112 |
| 0.200 | 0.183 / 0.183 / 0.198 | 0.206 | −0.58 |

So: the exponential form is excellent down to S ≈ 0.2 (σ ≲ 0.2 λ) *regardless of aberration type*, which is what makes RMS wavefront such a powerful single number near the diffraction limit. The pure Maréchal form should not be trusted beyond σ ≈ 0.07 λ (Geary reaches the same conclusion at "0.05 λ" from his table, p. 357).

**Where both fail.** Geary's numerical example [§31.2.4, p. 360] — a 400 mm, F/4 spherical mirror with $W_{040} = 3.05$ µm, i.e. σ = 0.413 waves at 0.55 µm at the minimum-variance focus — plugs into the exponential and gets S = 0.0012. A direct FFT calculation of the same wavefront gives S ≈ 0.13. Neither number describes a usable image (it is far from diffraction-limited), but the lesson is: **for σ ≳ 0.2 λ, compute Strehl from the PSF, not from σ** — and probably use spot or MTF instead of Strehl at all [Geary §32.3: "unless a design ... approaches diffraction-limited performance, there is not much point in looking at Strehl values"].

### 1.1 The Maréchal criterion and "diffraction-limited"
Conventionally, a system is **diffraction-limited** when $S \ge 0.8$, i.e. $\sigma \le \lambda/14 = 0.0714\lambda$ (using $1-(k\sigma)^2 = 0.8$) [Kenyon p. 168]. The exponential form gives S = 0.82 at λ/14 — the same within the precision anyone cares about. Rayleigh's older **quarter-wave rule** (PV ≤ λ/4) [Geary §32.2.5, p. 375] corresponds to S ≈ 0.80–0.81 for defocus or balanced spherical (L01). The two criteria agree for smooth, low-order wavefronts where PV/RMS ≈ 3.5; for wavefronts with high-order "ripple" (polishing marks, aspheric mid-spatial-frequency errors) PV/RMS is often 5–10 and **RMS is the meaningful one** — a single sharp spike can have large PV and negligible effect on the image.

## 2. RMS of the classical aberrations

Using normalized pupil radius $\rho$ and azimuth $\theta$ (Course 02 L01 conventions), the RMS for unit coefficient:

| Aberration | Form | σ unbalanced | Balanced with | σ balanced | Max coefficient for λ/14 |
|---|---|---|---|---|---|
| Defocus | $W_{020}\rho^2$ | $1/\sqrt{12} = 0.2887$ | (piston only) | 0.2887 | 0.247 λ |
| Spherical | $W_{040}\rho^4$ | $\sqrt{4/45} = 0.2981$ | defocus $W_{020} = -W_{040}$ | $1/\sqrt{180} = 0.0745$ | 0.958 λ (0.240 λ unbalanced) |
| Coma | $W_{131}\rho^3\cos\theta$ | $1/\sqrt8 = 0.3536$ | tilt $-\tfrac23 W_{131}\rho\cos\theta$ | $1/\sqrt{72} = 0.1179$ | 0.606 λ |
| Astigmatism | $W_{222}\rho^2\cos^2\theta$ | $1/4 = 0.25$ | defocus $-\tfrac12W_{222}\rho^2$ | $1/\sqrt{24} = 0.2041$ | 0.350 λ |

Geary's Table 31.3 gives the unbalanced variances $W_{131}^2/8$ and $W_{222}^2/16$ [p. 364]; the balanced values follow by removing the best-fit tilt or defocus — exactly what the Zernike polynomials do automatically (Course 02 L01): Zernike Standard coefficients are *orthonormal*, so **the RMS wavefront is the root-sum-square of the Standard Zernike coefficients (excluding piston)**, and removing tilt/defocus terms is just dropping coefficients.

Practical reading:
- "1 wave of spherical aberration" sounds terrible but is diffraction-limited if you refocus.
- Coma and astigmatism cannot be refocused away; their tolerance is 2–3× tighter than balanced spherical.
- Tilt does not degrade the PSF shape, it only moves it (distortion/centroid shift) — which is why the "centroid" reference in the merit function (L04) is gentler than the "chief ray" reference.

## 3. Best focus depends on the criterion

For spherical aberration $W_{040}$ plus defocus $W_{020}$ (Geary Table 31.2, p. 360; Course 02 L02):

| Criterion | Optimum $W_{020}$ | Image-plane shift from paraxial focus ($\delta = 8N^2 W_{020}$, magnitude) |
|---|---|---|
| Maximum Strehl (min wavefront variance) | $-W_{040}$ | $8N^2W_{040}$ |
| Minimum RMS spot ("image compactness") | $-\tfrac43W_{040}$ | $\tfrac{32}{3}N^2W_{040}$ |
| Minimum blur circle (least confusion) | $-\tfrac32W_{040}$ | $12N^2W_{040}$ |

Geary's mirror (F/4, $W_{040} = 3.05$ µm): best Strehl 0.390 mm, best RMS spot 0.521 mm, minimum blur 0.586 mm from paraxial focus, all on the same side [Geary §31.2.5, §31.3, pp. 360–362]. He finds both the Strehl plane and the min-blur plane in ZEMAX by putting a dummy surface before the image, making its thickness variable and optimizing with the *wavefront* and *spot (PTV)* default merit functions respectively — you will repeat this in Task 3. Moral: **the optimizer's notion of "best" is whatever your merit function says.** Optimizing RMS spot for a near-diffraction-limited lens puts the image plane in the wrong place for Strehl/MTF.

The sign of $\delta$: with light travelling left to right, a positive (undercorrected) spherical lens has its best focus to the *left* of paraxial focus (towards the lens): negative $\delta$. For a concave mirror the light travels right to left after reflection, so the shift is numerically positive in OpticStudio's coordinate convention [Geary pp. 361–362].

## 4. Axial intensity and depth of focus

### 4.1 Diffraction (Rayleigh) depth of focus
Moving the observation plane by $\delta$ from the focus of a perfect lens introduces pure defocus $W_{020} = \delta/(8N^2)$ (Geary eq. 32.26 written the other way round; $N$ = working F/#). The on-axis amplitude is the pupil average of $e^{ikW_{020}\rho^2}$, and with $x = \rho^2$ this integral is elementary [Geary eqs. 32.9–32.22]:

$$
\frac{I(0,\delta)}{I_0} = \mathrm{sinc}^2\!\left(\frac{\pi W_{020}}{\lambda}\right) = \left[\frac{\sin(\pi W_{020}/\lambda)}{\pi W_{020}/\lambda}\right]^2 .
$$

- First zeros at $W_{020} = \pm\lambda$, i.e. $\delta = \pm 8\lambda N^2$ [Geary p. 369: zero-to-zero $400\lambda$ for F/5 = 253 µm at 0.6328 µm].
- At $W_{020} = \pm\lambda/4$ (Rayleigh's quarter wave) the axial intensity is $[\sin45°/(\pi/4)]^2 = 0.81$. This defines the **diffraction depth of focus**

$$
\delta_\text{DOF} = \pm 2\lambda N^2 = \pm\frac{\lambda}{2\,\text{NA}^2}
$$

[Geary eq. 32.27, p. 370]. It grows with the *square* of the F-number.

| λ (µm) | N | DOF (±µm) | first zeros (±µm) |
|---|---|---|---|
| 0.85 | 2.0 | 6.8 | 27.2 |
| 0.85 | 2.8 | 13.3 | 53.3 |
| 0.85 | 4.0 | 27.2 | 108.8 |
| 0.5876 | 4.0 | 18.8 | 75.2 |
| 0.6328 | 5.0 | 31.6 | 126.6 |

### 4.2 Geometric depth of focus
When aberrations or pixels are much larger than the Airy disk, use geometry instead [Geary §32.2.3]: a cone of half-angle $u' \approx 1/(2N)$ produces a blur of half-width $w$ at a distance $w/u' = 2Nw$ from focus. With an acceptable blur *diameter* $c$ (circle of confusion, e.g. 1–2 pixels):

$$
\delta_\text{geo} = \pm N c \qquad (\text{Geary: GDOF} = 4N w \text{ total}).
$$

Example: N = 2.8, c = 2 × 3.45 µm → ±19.3 µm. The diffraction and geometric DOF are comparable when $c \approx 2\lambda N$ — i.e. when the acceptable blur is close to the Airy diameter. In machine vision, a practical DOF is often defined as the focus range where MTF at Nyquist/2 stays above a threshold — the through-focus MTF of L02 — which automatically blends both regimes.

### 4.3 Depth of focus vs. depth of field
Depth of *focus* is in image space; depth of *field* is the corresponding object-space range. Near a given conjugate they are linked by the longitudinal magnification $\bar m \approx m^2$ (for $n = n'$): $\Delta z_\text{object} \approx \Delta z_\text{image}/m^2$. Course 04 L02 develops depth of field, hyperfocal distance and the F/#–diffraction trade-off properly; the key point now is that the *image-side* tolerance ($\pm2\lambda N^2$) is what the mechanical and thermal design must hold.

### 4.4 Aberrations and the through-focus curve
With spherical aberration the axial intensity curve becomes asymmetric and its peak drops and moves (Task 2). Astigmatism splits it into two foci. A practical diagnostic: OpticStudio's **RMS vs Focus** analysis with "Strehl Ratio" as data [Geary §32.3, Fig. 32.12] — a symmetric bell centred at zero focus shift means a well-focused, nearly aberration-free lens.

## 5. Wavefront error budgets

For a diffraction-limited system the RMS wavefront is the natural currency of a performance budget. Independent, random contributions add in quadrature (RSS):

$$
\sigma_\text{total} = \sqrt{\sigma_\text{design}^2 + \sigma_\text{fabrication}^2 + \sigma_\text{alignment}^2 + \sigma_\text{thermal}^2 + \sigma_\text{focus}^2 + \dots}
$$

and the result maps to Strehl via $e^{-(k\sigma)^2}$. Example budget for a Maréchal-level system:

| Contribution | Allocation (RMS) |
|---|---|
| Design residual (nominal) | λ/30 |
| Surface figure & index errors (fabrication) | λ/25 |
| Decenter/tilt/spacing after alignment | λ/30 |
| Thermal (over 0–45 °C, after refocus if any) | λ/40 |
| **RSS total** | **λ/15.0 (σ = 0.0667 λ) → S ≈ 0.84** |

Notes from practice:
- The design residual is usually allotted the *smallest* share: once the nominal design is a third of the total budget, more design effort buys little — tolerancing (Course 06) dominates.
- A focus error is just defocus: σ = |W_{020}|/√12 = |δ|/(8N²√12). A focus allocation of λ/30 RMS at F/2.8, 850 nm is $\delta = 8\cdot2.8^2\cdot\sqrt{12}\cdot(0.85/30) = 6.2$ µm — tiny, which is why fast lenses need active focus or thermal compensation (L09).
- Systems that are *not* diffraction-limited (most camera lenses at full field) are budgeted with MTF or encircled energy instead; the RSS idea still applies, but to blur variances (e.g. spot radii in quadrature), and then less rigorously.

## 6. In OpticStudio

- **Huygens PSF / FFT PSF** — Text tab reports a Strehl ratio for the selected field/wavelength(s). Huygens is the reference for tilted/wide-angle systems (L01).
- **Zernike Standard Coefficients** (Analyze → Wavefront → Zernike Standard Coefficients): reports RMS and PV wavefront (to chief ray and to centroid), each coefficient, and an *estimated* Strehl from the RMS (exponential formula) — fine for S ≳ 0.2 only [Geary §32.3 mentions the same block in the old ZEMAX].
- **Wavefront Map** and **OPD Fan**: visual check of PV and shape.
- **RMS vs Field**, **RMS vs Focus**, **RMS vs Wavelength** (Analyze → Image Quality → RMS, location varies by version): choose Data = Spot Radius, Wavefront or **Strehl Ratio**; method Gaussian quadrature or rectangular array. RMS vs Focus with Strehl is the fastest through-focus/DOF diagnostic.
- **Default merit function, Wavefront type**: inserts `OPDX` operands (OPD relative to the centroid-referenced sphere) with Gaussian-quadrature weights — the MF value is then the RMS wavefront error in waves [Geary Listing 31.1, §31.2.6]. With the image thickness variable, it automatically finds the maximum-Strehl focus.
- `ZERN` operand: target an individual Zernike coefficient (e.g. hold spherical or astigmatism to a value, or monitor them with weight 0).
- Polychromatic: OpticStudio's polychromatic RMS wavefront and Strehl are weighted over the System Explorer wavelengths. A lens can be diffraction-limited at each wavelength separately and still fail polychromatically because the foci differ (axial colour is just wavelength-dependent defocus).

**Pitfalls**
1. Reading the Zernike-estimated Strehl of a badly aberrated lens as meaningful (cf. Geary's 0.0012).
2. Comparing "RMS to chief" with "RMS to centroid" — the difference is tilt (and for the MTF/PSF shape, centroid is the relevant one).
3. Forgetting that the DOF formula uses the **working** F/#.
4. Specifying PV wavefront for surfaces with mid-spatial-frequency structure; use RMS (and maybe slope) instead.

---

## Worked example — Can a fast NIR camera lens be fixed-focus?

**System:** 850 nm, working F/2.8, 3.45 µm pixels; nominal design residual on axis σ = 0.04 λ.

1. **Nominal Strehl:** $e^{-(2\pi\cdot0.04)^2} = e^{-0.0632} = 0.94$.
2. **Diffraction DOF:** $\pm2\lambda N^2 = \pm2\times0.85\times7.84 = \pm13.3$ µm (S of an otherwise perfect lens stays ≥ 0.81).
3. **Budget for focus:** if we require total σ ≤ λ/14 = 0.0714 λ, the focus allocation is $\sqrt{0.0714^2 - 0.04^2} = 0.0592\lambda$ (assuming nothing else; in reality fabrication and alignment also take a share). Defocus with σ = 0.0592 λ is $W_{020} = 0.0592\sqrt{12} = 0.205\lambda$, i.e. $\delta = 8N^2W_{020} = 8\times7.84\times0.205\times0.85 = 10.9$ µm.
4. **Thermal check:** an aluminium barrel (CTE 23.6 ppm/K) holding a 25 mm flange-to-sensor distance grows by $25\times23.6\times10^{-6}\times25 = 14.8$ µm for a 25 K rise — larger than the whole focus allocation. Either the lens must be athermalized (glass dn/dT and mount CTE compensating, L09) or the camera must refocus/calibrate across temperature.
5. **Geometric view:** allowing a 2-pixel blur diameter gives ±Nc = ±19.3 µm — more forgiving, but at the cost of the contrast at Nyquist (L02 Task 1 showed MTF at Nyquist dropping from 0.57 to ≈0.29 at ±0.4 wave ≈ ±21 µm).

Conclusion: at F/2.8 in the NIR, focus stability of ~±10 µm is the right order of magnitude for a "sharp at Nyquist" design; mechanical and thermal design must be part of the optical design from the start.

---

## Key takeaways
- Strehl = peak/peak; $S \approx e^{-(2\pi\sigma/\lambda)^2}$ is accurate to S ≈ 0.2 for any aberration mix; below that compute the PSF.
- Diffraction-limited ⇔ S ≥ 0.8 ⇔ σ ≤ λ/14 ⇔ (for smooth wavefronts) PV ≤ λ/4.
- Balanced aberrations: spherical can be 1 wave and still diffraction-limited; coma 0.6 λ; astigmatism 0.35 λ; defocus 0.25 λ.
- Best focus is criterion-dependent (Strehl: $W_{020} = -W_{040}$; RMS spot: $-\tfrac43W_{040}$; min blur: $-\tfrac32W_{040}$).
- Diffraction DOF $\pm2\lambda N^2$ (S ≥ 0.81); geometric DOF $\pm Nc$. Both scale with the working F/#.
- Budgets add in quadrature; design residual should be a minority share of the total.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Strehl ratio | Peak irradiance of aberrated PSF / perfect PSF |
| Wavefront variance σ² | Area-weighted variance of W over the pupil; σ is the RMS wavefront error |
| Maréchal criterion | σ ≤ λ/14 ⇔ S ≥ 0.8 |
| Rayleigh quarter-wave rule | PV wavefront ≤ λ/4 |
| Balanced aberration | Aberration combined with the lower-order term (defocus, tilt) that minimizes its RMS |
| Diffraction depth of focus | ±2λN²: focus range with axial intensity ≥ 0.81 |
| Geometric depth of focus | ±Nc for an acceptable blur diameter c |
| Wavefront error budget | RSS allocation of σ among design, fabrication, alignment, environment |

## References
1. [Geary] J. M. Geary, *Introduction to Lens Design*, 2002: Ch. 31, pp. 355–364; Ch. 32, pp. 365–376; §30.6, pp. 346–350.
2. [Kenyon] I. R. Kenyon, *The Light Fantastic*, 2008: §7.2.1, p. 168 (eq. 7.23).
3. Ansys Optics KB KA-01494, "Huygens PSF and FFT PSF": <https://optics.ansys.com/hc/en-us/articles/42661795535251> — which PSF to use when reading a Strehl ratio.
4. ZOSPy API documentation, Huygens PSF and Strehl ratio wrapper (Strehl parsed from the analysis text output): <https://zospy.readthedocs.io/en/v2.1.1/api/zospy.analyses.psf.huygens_psf.HuygensPSFAndStrehlRatio.html>
