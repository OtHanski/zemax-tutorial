# L07 — Gaussian beams and Physical Optics Propagation

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~3 h, tasks ~6 h
> **Prerequisites:** [L01 — Diffraction and the PSF](../L01-diffraction-and-the-psf/), [Course 01 L03 (ABCD matrices)](../../01-foundations/L03-paraxial-optics-and-ray-tracing/) · **Next:** [L08 — Polarization and coatings](../L08-polarization-and-coatings/)

## Learning objectives
- Write the TEM₀₀ Gaussian beam: $w(z)$, $R(z)$, Gouy phase, Rayleigh range, far-field divergence; convert between 1/e², FWHM and second-moment (D4σ) widths.
- Propagate a Gaussian beam through lenses with the complex beam parameter $q$ and the ABCD law; predict focused waist size and position (including the "waist is not at the focal point" effect).
- Use the embedded-Gaussian $M^2$ model for real laser diodes, VCSELs and multimode beams; compute beam parameter product and brightness consequences.
- Choose between ray tracing, OpticStudio's **Paraxial Gaussian Beam** analysis and **Physical Optics Propagation (POP)**, set up POP (beam definition, sampling, pilot beam, propagator choice), and check its results.
- Model a fibre- or laser-diode-fed collimator/focuser in POP, including aperture truncation, and connect it to laser-based structured-light sources.

## Reading
- **Core:** [Kenyon §6.15, pp. 156–161] — TEM₀₀ field (eq. 6.61), Rayleigh distance and divergence $\theta = \lambda/(\pi w_0)$ (6.63), $w(z)$ (6.64), complex curvature $1/q = 1/R - i\lambda/(\pi w^2)$ (6.67–6.69), $R(z)$ (6.72), waist from $w$ and $R$ (6.73–6.74), cavity stability (6.75), matrix method (§6.15.1) and the "focused waist is closer than the focal point" example.
- **Core:** [Kenyon §14.7–14.7.1, pp. 408–414] — semiconductor lasers: elliptical, astigmatic edge-emitter beams; the $M^2$ definition $\Theta = M\theta$, $W_0 = M w_0$ (eq. 14.43).
- **Core:** [Kenyon §14.8.1, pp. 418–419] — VCSELs: circular beams, $M^2$ "a little above unity", arrays directly from the wafer.
- **Optional:** [Kenyon §14.4.5, p. 397] — laser speckle (why coherent structured light is noisy).
- **Online:** Ansys KB, "Three tools to model Gaussian beam propagation in sequential mode" (ray, Paraxial Gaussian Beam, POP; `GBPS`, `POPD`): <https://optics.ansys.com/hc/en-us/articles/42661948624019>
- **Online:** Ansys KB, "Physical Optics Propagation overview" (pilot beam, Fresnel vs angular spectrum, separate X/Y, fibre coupling `FICP`, beam files): <https://optics.ansys.com/hc/en-us/articles/42661957754131>
- **Online:** Ansys KB KA-01601, E. Elliott, "Using POP, Part 1" (sampling, warnings in the Prop Report, fibre-launched beam): <https://optics.ansys.com/hc/en-us/articles/42661958168083>
- **Optional:** Zemax Community, "Question about the X and Y width in POP beam definition": <https://community.zemax.com/got-a-question-7/question-about-the-x-and-y-width-in-pop-beam-definition-1157>

---

## 1. Why rays are not enough for beams

Imaging (L01–L03) assumes that all significant diffraction happens between the exit pupil and the image ("single-step" diffraction). That fails for:
- **Laser beams** with a Gaussian amplitude profile, propagated over long distances where they are nearly collimated (rays say "parallel forever"; the beam actually spreads);
- **Intermediate foci** and focusing *far from* where rays converge (the waist of a weakly focused beam is not at the geometric focus);
- **Apertures in the beam path** — spatial filters, clipping by a lens mount — that create diffraction rings rays cannot predict;
- **Fibre coupling**, which depends on the overlap of complex fields.

The Ansys KB article on the "three tools" makes exactly this split: ray tracing is fast and fine away from those cases; the **Paraxial Gaussian Beam** analysis handles ideal Gaussian beams through paraxial systems; **POP** propagates the full complex field and handles everything else.

## 2. The TEM₀₀ Gaussian beam

The lowest-order mode of a laser cavity has a Gaussian transverse profile [Kenyon eq. 6.61]. With the waist at $z = 0$:

$$
E(r,z) \propto \frac{w_0}{w(z)}\exp\!\left(-\frac{r^2}{w^2(z)}\right)\exp\!\left(-ik\Big[z + \frac{r^2}{2R(z)}\Big] + i\psi(z)\right),
$$

$$
w^2(z) = w_0^2\left[1 + \left(\frac{z}{z_R}\right)^2\right],\quad R(z) = z\left[1 + \left(\frac{z_R}{z}\right)^2\right],\quad \psi(z) = \arctan\frac{z}{z_R},\quad z_R = \frac{\pi w_0^2}{\lambda}.
$$

[Kenyon eqs. 6.64, 6.71, 6.72.] Symbols: $w$ = 1/e² **intensity** radius (1/e of the field), $w_0$ waist radius, $R$ wavefront radius of curvature, $\psi$ the **Gouy phase** (an extra π phase shift through a focus), $z_R$ the **Rayleigh range**. Key consequences:
- **Far-field half-angle divergence** $\theta = \lambda/(\pi w_0)$ [eq. 6.63]: small waist ⇔ large divergence. The product $w_0\theta = \lambda/\pi$ is fixed — the Gaussian beam's étendue is the minimum allowed ($\sim\lambda^2$; Kenyon exercise 6.11).
- Over $|z| \le z_R$ the beam stays within $\sqrt2\,w_0$: $2z_R$ is the beam's **depth of focus** (confocal parameter).
- The wavefront is flat at the waist, most curved at $z = \pm z_R$ ($R = 2z_R$), and tends to $R \approx z$ (a spherical wave from the waist) far away.

**Irradiance and widths.** $I(r) = \dfrac{2P}{\pi w^2}\exp(-2r^2/w^2)$: peak $2P/(\pi w^2)$ (twice the "average over the 1/e² disk"). Power inside radius $a$: $1 - e^{-2a^2/w^2}$ — 86.5% at $a = w$, 98.9% at $a = 1.5w$, 99.97% at $a = 2w$. FWHM diameter $= 1.1774\,w$. For a Gaussian the second-moment (D4σ, ISO 11146) diameter equals $2w$; for non-Gaussian beams D4σ is the standard definition used with $M^2$.

## 3. The q parameter and the ABCD law

Kenyon combines $R$ and $w$ into one complex number [eq. 6.67]:

$$
\frac{1}{q} = \frac{1}{R} - i\frac{\lambda}{\pi w^2},\qquad q(z) = z + i z_R \text{ (waist at } z=0).
$$

Free propagation simply adds distance to $q$, exactly as it would to a ray's "radius of curvature" $R = y/u$. Any paraxial system with ray-transfer matrix $\begin{pmatrix}A&B\\C&D\end{pmatrix}$ acting on $(y, u)$ transforms

$$
q' = \frac{Aq + B}{Cq + D}
$$

(the ABCD law). Kenyon writes his matrices acting on (angle, height) and therefore states the law as $q' = (c + dq)/(a + bq)$ [eq. 6.81]; it is the same physics with the matrix elements reordered — keep to one convention (Course 01 L03 uses $(y, u)$ and $\begin{pmatrix}1&d\\0&1\end{pmatrix}$, $\begin{pmatrix}1&0\\-1/f&1\end{pmatrix}$).

**Focusing a collimated beam.** A lens of focal length $f$ at a waist of radius $w$ [Kenyon §6.15.1]: the new waist is

$$
w_0' = \frac{w}{\sqrt{1 + (\pi w^2/\lambda f)^2}} \approx \frac{\lambda f}{\pi w},\qquad z_0' = \frac{f}{1 + (\lambda f/\pi w^2)^2}\ (<f).
$$

The waist lies *slightly inside* the focal point — negligible for well-collimated beams, large for weakly focused ones (a classic surprise in laser-line generators and fibre couplers). Compare with the Airy radius $1.22\lambda N$: for a Gaussian beam filling a lens to $D = 2w$, $w_0' = \lambda f/(\pi w) = (2/\pi)\lambda N \approx 0.64\lambda N$ — a smaller *1/e²* radius than the Airy *first-zero* radius, but with no rings.

**General waist-to-waist imaging** (Self's form of the lens equation) follows from the same law; you will just compute it numerically with the ABCD law in Task 1, which is how OpticStudio's Paraxial Gaussian Beam analysis does it.

## 4. Real beams: $M^2$

Real sources are not perfect TEM₀₀ beams. The **embedded-Gaussian** model [Kenyon eq. 14.43]: a real beam behaves like a Gaussian whose waist and divergence are both $M$ times larger than the ideal one with the same Rayleigh range:

$$
W_0 = M w_0,\quad \Theta = M\theta\ \Rightarrow\ W_0\Theta = M^2\frac{\lambda}{\pi},\qquad W^2(z) = W_0^2 + z^2\Theta^2,\quad z_R = \frac{\pi W_0^2}{M^2\lambda}.
$$

$W_0\Theta$ is the **beam parameter product (BPP)**; it is conserved by aberration-free optics, so $M^2$ is a property of the source. Consequences: a beam with $M^2 = 4$ focuses to a spot 4× larger (for the same input size) or has 4× less depth of focus for the same spot. Paraxial Gaussian Beam in OpticStudio accepts an $M^2$ factor; POP can model it via multimode beams or file-defined fields.

Typical sources for 3D sensing:

| Source | Beam | $M^2$ | Notes |
|---|---|---|---|
| Single-mode fibre (e.g. 850 nm) | circular Gaussian, MFD ≈ 5–6 µm | ≈ 1 | clean; POP "Fiber"/Gaussian launch |
| Single-mode VCSEL | circular, half-angle 1/e² ≈ 5–10° | ≈ 1–1.5 | Kenyon §14.8.1: "a little above unity" |
| Multimode VCSEL / VCSEL array | each emitter several modes | ≈ 2–10 per emitter | arrays are what dot projectors use |
| Edge-emitting laser diode | elliptical, astigmatic; fast axis ≈ 20–35° FWHM, slow ≈ 5–12° FWHM | fast ≈ 1, slow ≫ 1 for broad-area | needs anamorphic/cylindrical optics (Kenyon §14.7.1) |

(Ranges are typical datasheet orders of magnitude; always use the actual device datasheet.) Datasheets usually quote **FWHM full angles**; convert to the 1/e² half-angle with $\theta_{1/e^2} = \Theta_\text{FWHM}/1.1774$ — e.g. 25° FWHM → 21.2° (1/e² half-angle).

Also remember **speckle** [Kenyon §14.4.5]: coherent light scattered from a rough surface forms a random interference pattern. For structured-light 3D, speckle adds phase/intensity noise to the imaged pattern; it is reduced by low coherence (multimode/multi-emitter sources, LEDs), angular or wavelength diversity, and larger imaging apertures (speckle size ≈ $\lambda N$ at the sensor).

## 5. OpticStudio's three tools

### 5.1 Ray tracing
Fast; correct for imaging; models beam "edges" if you trace the 1/e² cone as the aperture. Wrong near the waist of weakly focused beams and for long collimated propagation.

### 5.2 Paraxial Gaussian Beam (and Skew Gaussian Beam)
Analyze → (Laser and Fibers group; location varies by version) → **Paraxial Gaussian Beam**. Input: wavelength, waist size, waist position relative to the first surface, $M^2$. Output per surface: beam size, waist, waist position, Rayleigh range, divergence, phase radius. It propagates $q$ with the paraxial ABCD matrices of the system — no aberrations, no apertures. Operand `GBPS` returns the paraxial beam size at a surface (used in the Ansys example to optimize a beam expander). *Skew Gaussian Beam* handles non-rotationally-symmetric (decentred/tilted) systems paraxially.

### 5.3 Physical Optics Propagation (POP)
Analyze → **Physical Optics** (POP); Premium/Professional feature. POP stores the beam as a complex array on each surface and propagates it surface-to-surface with diffraction, applying each surface's phase (from real ray tracing) and aperture [Ansys KB POP overview]. Essentials:
- **Beam Definition**: type (Gaussian Waist, Gaussian Angle, Gaussian Size+Angle, Top Hat, Fiber-mode-like Gaussian, Multimode, Astigmatic Gaussian, File… — names vary slightly by version), waist X/Y, decenter, **X/Y sampling** (64…4096 points, powers of two), **X/Y width** of the array, "Auto" button to choose a width from the beam. The NA in the System Explorer does *not* define the POP beam; you must enter the beam in POP [KA-01601].
- **Pilot beam**: at each surface POP fits an ideal Gaussian ("pilot") to the propagating beam and uses it to choose the propagator: inside the pilot's Rayleigh range an **angular spectrum** (plane-wave) propagator, outside it a **Fresnel** (spherical-reference) propagator — whichever is numerically more accurate. The **Separate X, Y** option keeps separate pilot beams in x and y for astigmatic/anamorphic beams (laser diodes, cylinders).
- **Start / End surface**, "Use Polarization", "Use Disk Storage", save beam files at every surface (Beam File Viewer) — inspect them, not just the final plot.
- **Prop Report tab**: lists propagator choices and warnings such as "low sampling of pilot beam" — the final plot can look clean while an intermediate surface was undersampled [KA-01601]. Always read it.
- **Fiber coupling**: "Compute Fiber Coupling Integral" with a receiving-fibre mode gives coupling efficiency; operand `FICP` optimizes it. `POPD` returns POP data (e.g. beam radius, peak irradiance, coupling) at a surface for optimization, using settings saved from the POP window (Save button) [Ansys KB three tools].
- **Axicons and unusual surfaces** can confuse automatic propagator choice; set the propagator manually where needed [Ansys KB POP overview].

**Sampling guidance.** The array must (i) be wide enough to contain the beam plus its diffracted wings everywhere it propagates (≥ 3–4× the 1/e² diameter when apertures clip; ≥ 2–3× otherwise), and (ii) have enough points to sample the beam *and* the residual phase (after the pilot beam is removed). Start at 256×256 with Auto width, then double sampling and width until the quantities you care about (beam radius, peak irradiance, coupling) change by < 1%.

### 5.4 Which tool?

| Question | Tool |
|---|---|
| Waist size/location after a collimator or expander, ideal beam | Paraxial Gaussian Beam |
| Same, but lens aberrations matter (fast collimator, big field) | POP |
| Clipping by apertures, spatial filters, diffraction rings | POP |
| Fibre coupling efficiency | POP (+ `FICP`) |
| Image quality of an imaging lens | ray-based PSF/MTF (L01–L02) |
| Extended or incoherent sources, illumination uniformity | Non-sequential mode (Course 05) |

## 6. Application — laser sources in structured light

- **Laser-line and dot projectors** use a collimator after a VCSEL or edge emitter, followed by a DOE, Powell lens or microlens array (Course 05 L08). The collimator's job is set by Gaussian optics: output beam size $\approx f\theta$, residual divergence $\approx W_0/f$ (for a source at the front focal plane). A DOE's dot size in the far field is then set by this residual divergence and $M^2$.
- **Line thickness over depth**: a focused laser line of 1/e² half-width $w_0$ stays within √2 of it over $\pm z_R = \pm\pi w_0^2/(M^2\lambda)$. That is the projector-side analogue of the camera's depth of focus — and a fundamental trade-off (thin line ⇔ short range).
- **Eye safety**: peak irradiance $2P/(\pi w^2)$ and the source's apparent size drive laser-safety classification; POP gives realistic profiles including clipping.
- **Speckle** limits fringe/dot localization with coherent sources.

## 7. Pitfalls
1. Mixing 1/e² radius, FWHM and diameter. Write the definition next to every number.
2. Entering the waist position with the wrong sign (OpticStudio's waist position is measured relative to the start surface; check a known case first).
3. Expecting the focused waist at the paraxial focus for a weakly focused beam.
4. POP array too small (wrap-around) or too coarse (phase aliasing) — read the Prop Report, check convergence.
5. Using POP for an incoherent extended source (LED). It is a coherent, single-mode (or user-defined multimode) propagator.

---

## Worked example — fibre to collimated beam to focused spot

**Given:** single-mode fibre at 850 nm, mode-field diameter 5.6 µm ($w_0 = 2.8$ µm); collimator $f_1 = 10$ mm with the fibre tip at its front focal point; 100 mm of free space; focusing lens $f_2 = 50$ mm.

1. **Source:** $z_R = \pi w_0^2/\lambda = \pi(2.8)^2/0.85 = 29.0$ µm; divergence $\theta = \lambda/(\pi w_0) = 0.0966$ rad (5.54°, 1/e² half-angle; NA$_{1/e^2}$ ≈ 0.097).
2. **After the collimator:** $w = w_0\sqrt{1 + (f_1/z_R)^2} \approx f_1\theta = 0.966$ mm; residual divergence $\lambda/(\pi w) = 0.28$ mrad. The ABCD law puts the new waist at the *back* focal plane, 10 mm behind the collimator (source at front focal plane ⇒ waist at back focal plane).
3. **After 100 mm and the $f_2 = 50$ mm lens:** ABCD gives a waist of 14.0 µm located 50.008 mm behind the lens — practically at the focal point, because the incoming beam's Rayleigh range ($\pi w^2/\lambda$ ≈ 3.45 m) is huge compared with $f_2$. Check: $w_0'' \approx \lambda f_2/(\pi w) = 0.85\times10^{-3}\times 50/(\pi\times0.966) = 14.0$ µm, i.e. the fibre mode imaged with magnification $f_2/f_1 = 5$ (2.8 × 5 = 14).
4. **Depth of focus of the spot:** $z_R'' = \pi(14.0\ \mu\text{m})^2/0.85\ \mu\text{m} = 0.724$ mm → ±0.72 mm within √2 of the waist.
5. **Peak irradiance** at the focus for 1 mW: $2P/(\pi w^2) = 2\times10^{-3}/(\pi\times(0.014)^2) = 3.25$ W/mm².
6. **Clear apertures:** to pass 98.9% of the power, lens clear radius ≥ $1.5w$ = 1.45 mm; ≥ $2w$ = 1.93 mm makes truncation effects negligible (99.97%). With a clear radius equal to $w$ only 86.5% passes and POP will show ringing in the focal spot.

---

## Key takeaways
- Gaussian beam: $z_R = \pi w_0^2/\lambda$, $\theta = \lambda/(\pi w_0)$, $w(z)$ and $R(z)$ as above; $w$ is the 1/e² intensity radius.
- $1/q = 1/R - i\lambda/(\pi w^2)$ and $q' = (Aq+B)/(Cq+D)$ propagate beams through any paraxial system.
- Focused waist $\approx \lambda f/(\pi w)$, located slightly inside the focal point; depth of focus $\pm z_R$.
- $M^2$ scales divergence and spot size; BPP $= M^2\lambda/\pi$ is a source property.
- Paraxial Gaussian Beam for ideal paraxial beams; POP for aberrations, apertures, fibre coupling, near-field; rays for imaging.
- POP needs care: beam definition entered in POP, pilot beam and propagator choice, sampling convergence, Prop Report warnings.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| TEM₀₀ | Fundamental Gaussian laser mode |
| Waist $w_0$ | Minimum 1/e² intensity radius of a beam |
| Rayleigh range $z_R$ | Distance from waist where the area doubles, $\pi w_0^2/(M^2\lambda)$ |
| Gouy phase | Extra on-axis phase $\arctan(z/z_R)$ through a focus |
| q parameter | Complex beam parameter combining $R$ and $w$ |
| ABCD law | $q' = (Aq+B)/(Cq+D)$ |
| $M^2$ | Beam-quality factor; ratio of real to ideal BPP |
| BPP | Beam parameter product $W_0\Theta$ |
| D4σ width | Second-moment beam diameter (ISO 11146) |
| POP | Physical Optics Propagation: diffraction-based propagation of a sampled complex field |
| Pilot beam | Best-fit Gaussian used by POP to select propagators and remove phase |
| Angular spectrum / Fresnel propagator | Plane-wave vs spherical-reference diffraction propagators |
| Speckle | Random interference from coherent light on rough surfaces |

## References
1. [Kenyon] I. R. Kenyon, *The Light Fantastic*, 2008: §6.15–6.15.1, pp. 156–161; §14.4.5, p. 397; §14.7–14.7.1, pp. 408–414; §14.8.1, pp. 418–419.
2. Ansys Optics KB, "Three tools to model Gaussian beam propagation in sequential mode": <https://optics.ansys.com/hc/en-us/articles/42661948624019>
3. Ansys Optics KB, "Physical Optics Propagation (POP) overview": <https://optics.ansys.com/hc/en-us/articles/42661957754131>
4. Ansys Optics KB KA-01601, E. Elliott, "Using POP, Part 1": <https://optics.ansys.com/hc/en-us/articles/42661958168083>
5. Zemax Community, "Question about the X and Y width in POP beam definition": <https://community.zemax.com/got-a-question-7/question-about-the-x-and-y-width-in-pop-beam-definition-1157>
6. Zemax Community, "Ask an engineer: Gaussian beam propagation": <https://community.zemax.com/user-news-alerts-5/ask-an-engineer-gaussian-beam-propagation-1965>
