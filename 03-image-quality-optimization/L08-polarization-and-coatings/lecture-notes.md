# L08 — Polarization, Fresnel losses and thin-film coatings

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~3 h, tasks ~5 h
> **Prerequisites:** [Course 01 L01 (Snell, TIR)](../../01-foundations/L01-light-rays-and-opticstudio-tour/), [L07 — Gaussian beams](../L07-gaussian-beams-and-pop/) (wave picture) · **Next:** [L09 — Thermal and environmental analysis](../L09-thermal-and-environmental-analysis/)

## Learning objectives
- Write and use the Fresnel equations for s- and p-polarization; compute normal-incidence reflectance, Brewster's angle, the critical angle and the phase shifts on total internal reflection.
- Describe polarization states with Jones vectors and simple optical elements (polarizer, wave plate) with Jones matrices; define diattenuation and retardance.
- Compute the reflectance of single- and multi-layer thin films with the characteristic-matrix method; design a quarter-wave AR coating and a two-layer V-coat for a NIR wavelength, and predict their angle and wavelength dependence.
- Define materials and coatings in an OpticStudio coating file (`MATE`, `COAT`, ideal coatings), apply them to surfaces, and analyse transmission and polarization with the Coatings and Polarization analyses.
- Build a transmission budget for a multi-element lens and specify an AR coating sensibly (band, AOI range, average and maximum R).

## Reading
- **Core:** [Kenyon §9.5–9.6, pp. 241–248] — boundary conditions, Fresnel's equations (eqs. 9.71–9.74), reflectance and transmittance (9.76–9.77), Brewster's angle (9.78), normal incidence (9.79–9.80), TIR phase shifts (9.81–9.86), sign conventions (Fig. 9.13).
- **Core:** [Kenyon §9.7–9.7.1, pp. 249–254] — interference filters; the characteristic matrix of a layer (9.93–9.95), multilayers (9.96–9.98), single-layer AR condition $n_1 = \sqrt{n_\text{in}n_\text{out}}$ and MgF₂ (1.4%), two-layer AR (9.100–9.101), high reflectors and their bandwidth (9.102–9.104), Fabry–Perot bandpass filters.
- **Core:** [Kenyon §10.2, §10.5–10.5.1, pp. 265–268, 276–278] — states of polarization, wave plates, Jones vectors and matrices; [§10.3, pp. 268–269] dichroism and Malus' law; [§10.5.3, p. 280] polarizing beam splitters.
- **Online:** Ansys KB KA-01539, "Adding metal/material data to the coating file" — `MATE` and `COAT` syntax, relative vs absolute thickness, applying coatings in sequential and NSC: <https://optics.ansys.com/hc/en-us/articles/42661779524627>
- **Online:** Ansys KB (H. Chen), coatings in OpticStudio — Coating catalog, Coatings analyses, don't edit COATING.DAT directly: <https://optics.ansys.com/hc/en-us/articles/43071115297043>
- **Optional:** Zemax Community, "Multi-layer coating for band pass": <https://community.zemax.com/got-a-question-7/multi-layer-coating-for-band-pass-456>; "How to set up the coating": <https://community.zemax.com/got-a-question-7/how-to-set-up-the-coating-1134>

---

## 1. Why a lens designer cares

Up to now every surface has transmitted 100% and polarization has been ignored. Real surfaces reflect (4–5% per uncoated glass–air surface), coatings change that by an order of magnitude, glass absorbs a little, and every one of these effects depends on angle of incidence (AOI), wavelength and polarization. Consequences:

- **Throughput.** Twenty uncoated surfaces (a 10-element lens) transmit only $(1-0.041)^{20} = 43\%$ at 940 nm in N-BK7; with a 0.25% V-coat on each, 95%.
- **Ghosts and stray light.** Every reflection can form a ghost image of a bright source — critical for active 3D cameras that see their own projector light and specular glints (Course 04 L08, Course 05 L07).
- **Polarization-dependent performance.** Fast lenses have large AOIs at the pupil edge; s and p transmit differently (diattenuation) and acquire different phases (retardance), which slightly apodizes and aberrates the pupil. Polarization-based optics (polarizers to suppress specular reflections, polarizing beam splitters, LCoS projectors) need it modelled explicitly.
- **Coatings shift with angle.** A bandpass filter or AR coating designed at normal incidence moves to shorter wavelengths at oblique incidence — a key constraint for NIR filters behind wide-angle or high-CRA lenses (Course 04 L08).

## 2. Fresnel equations

At a plane interface from index $n_1$ to $n_2$, angle of incidence $\theta_i$ and refraction angle $\theta_t$ (Snell), the amplitude coefficients are [Kenyon eqs. 9.71–9.74]:

$$
r_s = \frac{n_1\cos\theta_i - n_2\cos\theta_t}{n_1\cos\theta_i + n_2\cos\theta_t},\qquad
t_s = \frac{2n_1\cos\theta_i}{n_1\cos\theta_i + n_2\cos\theta_t},
$$

$$
r_p = \frac{n_2\cos\theta_i - n_1\cos\theta_t}{n_1\cos\theta_t + n_2\cos\theta_i},\qquad
t_p = \frac{2n_1\cos\theta_i}{n_1\cos\theta_t + n_2\cos\theta_i}.
$$

**s** (TE, German *senkrecht*): E perpendicular to the plane of incidence; **p** (TM): E in the plane of incidence. Reflectance $R = |r|^2$; transmittance $T = |t|^2\,\dfrac{n_2\cos\theta_t}{n_1\cos\theta_i}$ (the factor accounts for the change of beam cross-section and impedance; Kenyon eq. 9.77) so that $R + T = 1$ without absorption. Sign conventions for $r_p$ differ between books (Kenyon Fig. 9.13 discusses why); reflectances do not depend on them.

Key numbers for N-BK7 ($n_d = 1.5168$), from air:
- **Normal incidence:** $R_0 = \left(\frac{n_2-n_1}{n_2+n_1}\right)^2 = 4.22\%$ [eq. 9.79]; at 940 nm ($n = 1.5084$) 4.11%. A plate (two surfaces) loses ≈ 8%.
- **45°:** $R_s = 9.6\%$, $R_p = 0.92\%$ — strongly polarizing.
- **Brewster's angle:** $\tan\theta_B = n_2/n_1$ [eq. 9.78] → 56.6°; $R_p = 0$ there. Brewster windows in lasers and pile-of-plates polarizers use this.
- **Cemented interface** N-BK7/N-SF5 ($n$ = 1.5168/1.6727): $R = 0.24\%$ — why cemented surfaces are rarely AR-coated.

**Total internal reflection.** Going from glass into air beyond the critical angle $\theta_c = \arcsin(n_2/n_1)$ (41.2° for N-BK7), $\cos\theta_t$ becomes imaginary, $|r_s| = |r_p| = 1$ and both acquire *different* phase shifts [eqs. 9.81–9.86]. TIR prisms therefore change the polarization state (Fresnel rhomb = a TIR-based quarter-wave retarder); NSC models of TIR light guides need polarization for correct phase but not for energy.

## 3. Describing polarization: Jones calculus

A fully polarized, monochromatic plane wave is described by the **Jones vector** of its transverse field components [Kenyon §10.5.1]:

$$
\mathbf E = \begin{pmatrix}E_x\\E_y\end{pmatrix}:\quad
\text{x-linear }\begin{pmatrix}1\\0\end{pmatrix},\quad
45°\text{ linear }\tfrac{1}{\sqrt2}\begin{pmatrix}1\\1\end{pmatrix},\quad
\text{circular }\tfrac{1}{\sqrt2}\begin{pmatrix}1\\\pm i\end{pmatrix}.
$$

Optical elements are 2×2 **Jones matrices**: an ideal x-polarizer $\begin{pmatrix}1&0\\0&0\end{pmatrix}$; a wave plate with fast axis along x and retardance $\delta$: $\begin{pmatrix}1&0\\0&e^{i\delta}\end{pmatrix}$ ($\delta = \pi/2$ quarter-wave, $\pi$ half-wave); rotate with $R(-\alpha)\,J\,R(\alpha)$. **Malus' law** — intensity through a polarizer at angle $\alpha$ to linear input: $I = I_0\cos^2\alpha$ [Kenyon §10.3].

At an interface the Fresnel coefficients form a diagonal Jones matrix in the local s/p basis: $\mathrm{diag}(t_s, t_p)$. Two derived quantities describe any such element:
- **Diattenuation** $D = \dfrac{T_\max - T_\min}{T_\max + T_\min}$ — partial polarizer behaviour ($|T_s - T_p|$ effects).
- **Retardance** — phase difference between the eigen-polarizations ($\arg t_p - \arg t_s$).

**Unpolarized light** is handled by averaging the results for two orthogonal input states (e.g. x and y). OpticStudio does this when the system is set to "Unpolarized".

Practical uses in 3D vision: **cross-polarization** (polarized illumination + analyser at 90° in front of the camera) suppresses specular glints from metal parts at the cost of >50% light; **polarizing beam splitters** route light in coaxial designs and LCoS projectors [Kenyon §10.5.3]; and stress birefringence in molded plastic lenses (Course 04 L07) adds unintended retardance.

## 4. Thin-film coatings

### 4.1 The characteristic matrix
For a homogeneous layer of index $n$, physical thickness $d$, at angle $\theta$ inside the layer, the tangential fields at its two faces are related by [Kenyon eqs. 9.93–9.94; Macleod's standard form]:

$$
M = \begin{pmatrix}\cos\varphi & \dfrac{i\sin\varphi}{\eta}\\[4pt] i\eta\sin\varphi & \cos\varphi\end{pmatrix},\qquad \varphi = \frac{2\pi n d\cos\theta}{\lambda},\qquad \eta = \begin{cases}n\cos\theta & (s)\\ n/\cos\theta & (p)\end{cases}
$$

(Kenyon's matrix has the opposite sign of $i$ because his time convention is $e^{i\omega t}$; results for $R$ are identical.) A stack is the product $M = M_1M_2\cdots M_m$ (layer 1 next to the incident medium). With $\begin{pmatrix}B\\C\end{pmatrix} = M\begin{pmatrix}1\\\eta_s\end{pmatrix}$ for substrate admittance $\eta_s$ and incident-medium admittance $\eta_0$:

$$
r = \frac{\eta_0 B - C}{\eta_0 B + C},\qquad R = |r|^2 .
$$

You will implement this in ~20 lines of Python (Task 1); it is exactly what OpticStudio's coating engine does for every ray at every coated surface.

### 4.2 Single-layer AR
At normal incidence a quarter-wave optical thickness ($nd = \lambda_0/4$, $\varphi = \pi/2$) gives $M = \begin{pmatrix}0 & i/n\\ in & 0\end{pmatrix}$ and

$$
R = \left(\frac{n_0n_s - n^2}{n_0n_s + n^2}\right)^2 ,
$$

zero when $n = \sqrt{n_0n_s}$ [Kenyon eq. 9.99]. For glass of index 1.5 that is 1.22 — no durable material that low exists; MgF₂ (1.38) is the classic compromise: $R = 1.4\%$ on $n = 1.5$ [Kenyon p. 252], 1.28% on N-BK7 at 550 nm.

Wavelength and angle dependence of that MgF₂ layer (quarter-wave at 550 nm, on N-BK7):

| λ (nm) | 450 | 550 | 650 | 850 |
|---|---|---|---|---|
| R (%) | 1.64 | 1.28 | 1.46 | 2.11 |

| AOI (°) at 550 nm | 0 | 20 | 30 | 45 |
|---|---|---|---|---|
| $R_s$ (%) | 1.28 | 1.59 | 2.10 | 4.05 |
| $R_p$ (%) | 1.28 | 1.03 | 0.72 | 0.14 |

A visible MgF₂ coating is a poor NIR AR coating (2.1% at 850 nm): the camera lens must be coated **for its own band**.

### 4.3 Two-layer and multilayer AR
Two quarter-wave layers (air-side index $n_1$, glass-side $n_2$) give zero reflectance when $n_2/n_1 = \sqrt{n_s/n_0}$ [Kenyon eq. 9.101 and text] — with MgF₂ outside, the inner layer needs $n_2 \approx 1.38\sqrt{1.508} = 1.69$ on N-BK7 at 940 nm. More flexible is the **V-coat**: a thin high-index layer plus a thicker low-index layer with *non*-quarter-wave thicknesses, solved for zero reflectance at one wavelength. Example at 940 nm on N-BK7 (assumed indices: Ta₂O₅ 2.07, SiO₂ 1.45): glass | 41.5 nm Ta₂O₅ | 207.6 nm SiO₂ | air gives $R = 0$ at 940 nm, 0.03% at 920/960 nm, 0.12–0.16% at 900/980 nm. Narrowband NIR systems (structured light at 850/940 nm) are ideal for V-coats: < 0.25% per surface over the source band is routine.

**Broadband AR (BBAR)** coatings use 4–8 layers of alternating high/low index to reach an average $R$ below ~0.5% across 400–700 nm (or 400–1000 nm with more layers). **High reflectors** stack $(HL)^m$ quarter-waves; reflectance approaches 1 with a stop band of half-width $\Delta\lambda/\lambda_0 = (2/\pi)\arcsin[(n_H - n_L)/(n_H + n_L)]$ (the standard quarter-wave-stack result; for MgF₂/TiO₂ it gives 0.167, matching the ≈0.165 Kenyon quotes on p. 253). A **Fabry–Perot bandpass** inserts a half-wave spacer between two reflectors, $(HL)^mHH(LH)^m$ [Kenyon p. 253] — the structure behind the narrow NIR bandpass filters on 3D cameras, and the VCSEL's own DBR mirrors (Kenyon §14.8.1).

### 4.4 Angle shift of interference coatings
For an interference coating with effective index $n_\text{eff}$, the spectral features shift with AOI approximately as $\lambda(\theta) \approx \lambda_0\sqrt{1 - (\sin\theta/n_\text{eff})^2}$ — always toward shorter wavelengths. A 940 nm bandpass with $n_\text{eff} \approx 1.8$ shifts by about −10 nm at 15° and −26 nm at 25° (Course 04 L08 treats filter placement and CRA). The lens design must therefore know the **AOI distribution** on each coated surface — exactly what a footprint diagram plus `RAID` monitoring gives you.

## 5. Glass absorption
Bulk glass transmits imperfectly, especially in the blue/UV and for high-index, high-dispersion flints. Catalogs give **internal transmittance** $\tau_i$ for a reference thickness (e.g. 10 mm or 25 mm); for thickness $d$: $\tau(d) = \tau_i^{d/d_\text{ref}}$. In the NIR (850–940 nm) almost all optical glasses have $\tau_i > 0.99$ per 10 mm, so coatings dominate the budget; in the visible blue, dense flints and some lanthanum glasses can lose several percent. OpticStudio uses the catalog transmission data when polarization/transmission is computed.

## 6. In OpticStudio

### 6.1 Coating files
- **Libraries → Coating Tools → Edit Coating File** (location varies by version). Save a *copy* under a new name in the Coatings folder of your Zemax data folder — `COATING.DAT` is overwritten by updates [Ansys KB KA-01539; H. Chen]. Select your file in **System Explorer → Files** and Reload.
- `MATE <name>` followed by lines of wavelength (µm, ascending), $n$, $k$. In OpticStudio's convention a **negative** extinction coefficient indicates absorption [KA-01539].
- `COAT <name>` followed by lines `material thickness is_absolute loop_index taper`: thickness is an **optical thickness in waves at the primary wavelength** when `is_absolute = 0` (0.25 = quarter wave), or physical µm otherwise. All `MATE`/`TAPR` definitions come before the `COAT` definitions.
- **Ideal coatings** (`IDEAL`, `IDEAL2`) specify transmission/reflection directly without layers — perfect for system budgets before a coating vendor is chosen; `TABLE` coatings use tabulated R/T vs angle and wavelength (e.g. from vendor data).
- Apply in the **Lens Data Editor**: Surface Properties → Coating (or the Coating column). In NSC: Object Properties → Coat/Scatter, and turn on *Use Polarization* (and *Split NSC Rays* to see reflections) in ray traces.

### 6.2 Polarization settings and analyses
- **System Explorer → Polarization**: input polarization state (Jones vector $J_x$, $J_y$ with phases) or *Unpolarized*; options such as converting thin-film phase to ray-equivalent phase. Many image-quality analyses have a *Use Polarization* checkbox: when on, the pupil apodization and phase from coatings enter the PSF/MTF.
- **Analyze → Coatings** analyses: reflection, transmission, absorption, diattenuation, phase and retardance **vs angle** or **vs wavelength**, for a chosen surface (names vary slightly by release). Use them to verify a coating before trusting system results.
- **Analyze → Polarization**: *Polarization Ray Trace* (field vectors and losses surface by surface for one ray), *Polarization Pupil Map* (polarization ellipse across the exit pupil), *Transmission* (system transmission per field and wavelength, including coatings and bulk absorption), *Phase Aberration* (polarization-induced phase).
- **Ghost Focus Generator** (Course 04 L08) uses surface reflectances (from coatings) to rank ghost paths.

### 6.3 Pitfalls
1. Coatings defined but polarization off: many analyses ignore them. Check with the Transmission analysis.
2. Relative coating thickness tied to the *primary* wavelength: change the primary wavelength and your "quarter wave" changes. Use absolute thicknesses for real vendor designs.
3. Editing `COATING.DAT` in place (lost on update).
4. Forgetting that the AOI on a coating varies over the pupil and field: evaluate at the actual AOI range (footprint, `RAID`).
5. Expecting an ideal AR to fix ghosts: even 0.2% reflections matter when the source is 10⁴× brighter than the scene (a projector seen by its own camera, the sun).

---

## Worked example — transmission budget of a NIR receiver lens

A 5-element 940 nm receiver lens (10 air–glass surfaces) plus a sensor cover glass (2 surfaces) and a bandpass filter (2 surfaces, its own coatings, assume $T = 0.92$ in band):

| Option | Per-surface R | 12 lens + cover surfaces | × filter | Total |
|---|---|---|---|---|
| Uncoated N-BK7-like (4.1%) | 0.041 | $0.959^{12} = 0.605$ | 0.92 | 0.56 |
| Visible MgF₂ (2.1% at 850–940 nm) | 0.021 | $0.979^{12} = 0.775$ | 0.92 | 0.71 |
| NIR V-coat (0.25%) | 0.0025 | $0.9975^{12} = 0.970$ | 0.92 | 0.89 |

Bulk absorption in 15 mm of glass at 940 nm adds < 1% loss. Moving from a visible coating to a proper NIR V-coat buys 25% more signal — equivalent to opening the aperture by about 1/3 stop, at almost no cost. Equally important, the 0.25% surfaces make every two-reflection ghost ~(0.0025/0.021)² ≈ 1/70 as bright as with the visible coating.

**AR specification wording** (for the coating vendor): "Ravg ≤ 0.25% per surface over 920–960 nm, Rmax ≤ 0.5%, AOI 0–30°, unpolarized; substrate N-BK7 / N-SF5 (state all glasses); durability per ISO 9211-3 (or MIL-C-48497)". Durability/test standards: confirm the exact standard with the vendor.

---

## Key takeaways
- Fresnel: $R_0 = ((n_2-n_1)/(n_2+n_1))^2$ ≈ 4% for glass; s reflects more than p at oblique incidence; $R_p = 0$ at Brewster ($\tan\theta_B = n_2/n_1$); TIR adds polarization-dependent phase.
- Jones vectors/matrices describe polarized light and elements; diattenuation and retardance characterize interfaces and coatings.
- Characteristic matrices make any multilayer a few lines of code; QW AR needs $n=\sqrt{n_0n_s}$; MgF₂ gives ~1.3–1.4% on crown glass; V-coats give ~0% at one wavelength; filters shift blue with angle.
- OpticStudio: coatings via `MATE`/`COAT`/ideal definitions in a *copy* of the coating file; apply per surface; turn polarization on; verify with Coatings and Transmission analyses.
- Coat for the actual band and AOI range; budget transmission and ghost reflectance together.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| s / p polarization | E perpendicular / parallel to the plane of incidence (TE / TM) |
| Brewster's angle | AOI where $R_p = 0$; $\tan\theta_B = n_2/n_1$ |
| Jones vector / matrix | 2-component complex field description / 2×2 element description |
| Diattenuation | Polarization-dependent transmission, $(T_\max-T_\min)/(T_\max+T_\min)$ |
| Retardance | Phase difference between eigenpolarizations |
| Quarter-wave optical thickness (QWOT) | $nd = \lambda_0/4$ |
| V-coat | Two-layer AR with zero reflectance at one wavelength |
| BBAR | Broadband multilayer anti-reflection coating |
| Characteristic matrix | 2×2 matrix relating tangential E and H across a layer |
| Internal transmittance | Bulk glass transmission excluding surface reflections |
| Ideal coating | OpticStudio coating defined by R/T values rather than layers |

## References
1. [Kenyon] I. R. Kenyon, *The Light Fantastic*, 2008: §9.5–9.7.1, pp. 241–254; §10.2–10.3, pp. 265–269; §10.5–10.5.3, pp. 276–280; §14.8.1, pp. 418–419.
2. Ansys Optics KB KA-01539, coating file `MATE`/`COAT` syntax and application: <https://optics.ansys.com/hc/en-us/articles/42661779524627>
3. Ansys Optics KB (H. Chen), coatings in OpticStudio: <https://optics.ansys.com/hc/en-us/articles/43071115297043>
4. Zemax Community, "Multi-layer coating for band pass": <https://community.zemax.com/got-a-question-7/multi-layer-coating-for-band-pass-456>
5. Zemax Community, "How to set up the coating": <https://community.zemax.com/got-a-question-7/how-to-set-up-the-coating-1134>
6. H. A. Macleod, *Thin-Film Optical Filters* (CRC Press) — the standard reference for the characteristic-matrix formalism used in §4.1 (no link; library/book).
