# L08 — Diffractive Optics and Pattern Projection

> **Course 05 · Illumination, projection and non-sequential design** · Estimated time: lecture ~3.5 h, tasks ~6–7 h
> **Prerequisites:** [L02](../L02-non-sequential-fundamentals/lecture-notes.md) (ray splitting, detectors), [L03](../L03-source-modeling-leds-and-lasers/lecture-notes.md) (laser diodes, VCSEL arrays, speckle), [Course 02 L06](../../02-aberrations-classical-design/L06-chromatic-aberration-and-achromats/lecture-notes.md) (achromat equations), [Course 03 L01](../../03-image-quality-optimization/L01-diffraction-and-the-psf/lecture-notes.md) and [L02](../../03-image-quality-optimization/L02-mtf-theory-and-practice/lecture-notes.md) (Fraunhofer diffraction, Fourier optics) · **Next:** [L09 — Capstone: structured-light projector](../L09-capstone-structured-light-projector/lecture-notes.md)

## Learning objectives
- Apply the **grating equation** $n_2\sin\theta_m - n_1\sin\theta_i = m\lambda/d$ in transmission and reflection, compute order angles and the number of propagating orders, and explain why dot grids on a flat screen show **pincushion** distortion.
- Compute scalar **diffraction efficiencies** of blazed (kinoform), multilevel, binary-phase, binary-amplitude and sinusoidal gratings, and estimate how etch-depth and wavelength errors feed the **zero order**.
- Describe a **diffractive lens** by its phase function, convert the OpticStudio **Binary 2** coefficient $A_1$ into focal length, and explain the **Sweatt model** and the diffractive Abbe number $\nu_\text{diff} = -3.45$.
- Design (on paper) a **hybrid refractive–diffractive achromat**: power split, zone count, minimum zone width, and its secondary-spectrum penalty.
- Set up the sequential **Diffraction Grating** and **Binary 2** surfaces, and a non-sequential **Diffraction Grating** object that splits rays into several orders. Know which of these numbers OpticStudio does **not** compute: order efficiencies.
- Explain how **fan-out DOEs** (Dammann gratings, spot-array generators, VCSEL-array replication) build dot-pattern projectors, and reason about the **zero-order** and **eye-safety** problems.
- Explain the Fourier-optics view of a DOE (far field = Fourier transform of one period), relate it to holography, and say when you need scalar FFT, IFTA, or rigorous (RCWA/FDTD, e.g. Ansys Lumerical) tools.

## Reading
- **Core:** [Kenyon §6.5, pp. 134–136] — Fraunhofer diffraction by $N$ identical slits: principal maxima $N^2$ times the single-slit peak, narrowing as $1/N$, and the product "single-slit envelope × array factor". This is the whole physics of a grating in one page.
- **Core:** [Kenyon §6.8, pp. 139–140] — diffraction gratings: resolving power $\lambda/\Delta\lambda = Np$ (eq. 6.23), free spectral range, and the reflection-grating equation $a(\sin\theta-\sin\alpha)=p\lambda$ (eq. 6.26).
- **Core:** [Kenyon §6.9.1, pp. 142–143] — ruled vs. holographic gratings, **blazing** and the blaze wavelength $\lambda_\text{blaze} = a\sin\phi$ (eq. 6.33); Fig. 6.16 shows the single-slit envelope steered onto the first order.
- **Core:** [Kenyon §6.12–6.12.1, pp. 151–154] — Fresnel zones $\rho_m^2 = mR\lambda$ (eq. 6.55) and the **zone plate** as a lens with focal length $\rho_m^2/m\lambda$. This is the ancestor of every diffractive lens.
- **Core:** [Kenyon §7.2.1, pp. 166–167] — the diffracted amplitude is the **Fourier transform** of the aperture transmission; a grating is a convolution of one cell with a comb.
- **Core:** [Kenyon §7.7–7.7.2, pp. 188–190] — holography as recorded interference; the reconstruction gives orders −1, 0, +1; phase vs. amplitude holograms (≈ 33 % vs. 6 % into one first order); speckle on rough surfaces.
- **Optional:** [Kenyon §7.7.4, p. 191] — thick (volume/Bragg) holograms: angle and wavelength selectivity. [Kidger §12.5.3, p. 250] — diamond-turned diffractive surfaces in thermal-IR lenses, and why the visible is harder.
- **Core (online):** Ansys Optics KB on how OpticStudio treats diffractive surfaces (grating equation with refraction, sign of orders, 100 % efficiency assumption): <https://optics.ansys.com/hc/jp/articles/42661739263251>
- **Core (online):** Ansys Optics KB, *How to design DOE lens or metalens in OpticStudio* (Binary 2 phase design, efficiency cannot be computed by ray tracing, RCWA coupling): <https://optics.ansys.com/hc/en-us/articles/42661666194323>
- **Core (online):** Ansys Optics KB, Binary 2 hybrid singlet example (Binary 2 phase, zone positions via `Phases.zpl`): <https://optics.ansys.com/hc/en-us/articles/42661706685075>
- **Optional (online):** G. J. Swanson, *Binary Optics Technology: The Theory and Design of Multi-level Diffractive Optical Elements*, MIT Lincoln Lab TR-854 (1989), the classic free report on multilevel efficiency and hybrid achromats: <https://apps.dtic.mil/sti/pdfs/ADA213404.pdf>; and its sequel on where scalar theory fails, TR-914 (1991): <https://apps.dtic.mil/sti/pdfs/ADA235404.pdf>

---

## 1. Why a structured-light engineer needs diffraction

The Zivid-style projector you built in L05 images a DMD: every pixel of the pattern is an object point, and the lens is the whole story. There is a second family of 3D projectors, common in phones, robots and some industrial sensors: a **laser or VCSEL array** followed by a **diffractive optical element (DOE)**. The DOE turns one beam into a fan of beams, which can be a line, a grid of dots, or a pseudo-random dot cloud. It has no moving parts and fits in a few mm³. It also brings efficiency and spot uniformity that depend on nanometre-level etch depths, a **zero order** that can break eye safety, and **speckle**.

Diffractive surfaces also show up in imaging optics. A **hybrid refractive–diffractive** lens corrects colour with a single element, because a diffractive surface disperses light about 20× more strongly than glass, and with the opposite sign.

Pure ray tracing gets only half of this right, and the course has to be clear about which half:

| Quantity | Set by | OpticStudio ray trace? |
|---|---|---|
| **Direction** of each order | Period $d$ (local phase gradient) | Yes, exactly (grating equation) |
| **Power** in each order | Shape of one period: depth, profile, duty cycle, polarisation | No. You supply it (table/DLL) or compute it elsewhere |
| Spot shape, speckle, interference between orders | Coherent field | Only with POP or physical-optics tools |

## 2. The grating equation

### 2.1 From $N$ slits to orders
Kenyon builds the grating from $N$ identical slits of width $w$ at spacing $a$ [Kenyon §6.5, pp. 134–136]. The far-field amplitude is the product of a **single-slit envelope** and an **array factor** $\sin(N\beta)/\sin\beta$, with $\beta = \pi a\sin\theta/\lambda$. The array factor has **principal maxima** wherever adjacent slits are in phase. Their peak intensity is $N^2$ times the single-slit value and their angular width shrinks as $1/N$. For a grating with thousands of illuminated lines, the principal maxima, the **diffraction orders**, are the only thing left [Kenyon §6.8, p. 139].

Use $d$ for the period, $m$ for the order, and $n_1, n_2$ for the indices before and after the grating. The general form for a transmission grating is

$$
n_2\sin\theta_m - n_1\sin\theta_i = \frac{m\lambda}{d},
$$

where $\lambda$ is the **vacuum** wavelength and the angles are measured from the grating normal in the plane perpendicular to the grooves. With $m = 0$ this is just Snell's law, which is why OpticStudio writes it this way: it bends rays with "Snell plus a grating term" (Ansys KB on diffractive surfaces). For a reflection grating in air, Kenyon's eq. 6.26 reads $a(\sin\theta - \sin\alpha) = p\lambda$. The symbols differ from ours ($a=d$, $p=m$), and Kenyon's reflected angle $\theta$ is measured on the incident side.

**Sign convention.** The sign of $m$ is a convention, and different tools, books and vendors disagree. OpticStudio says positive orders bend rays toward positive angles relative to the axis (KB). In practice, trace order $+1$ once and look at the layout before you trust any sign.

**Consequences worth remembering:**
- **Propagating orders** need $|\sin\theta_m|\le 1$. At normal incidence in air, the largest order is $m_\text{max} = \lfloor d/\lambda\rfloor$. A grating with $d < \lambda$ (sub-wavelength) transmits only the zero order. That is the regime of anti-reflection "moth-eye" structures and metasurfaces, and there scalar thinking breaks down completely.
- **Angular dispersion**: $d\theta_m/d\lambda = m/(d\cos\theta_m)$. A DOE fan-out is a spectrometer whether you want it or not. A laser that drifts from 850 to 860 nm moves a spot at 15° by 1.2 % in $\sin\theta$. For triangulation that is a calibration term with temperature (§7).
- **Resolving power** $\lambda/\Delta\lambda = Nm$ [Kenyon eq. 6.23] and the **order width** $\Delta\theta \approx \lambda/(Nd\cos\theta) = \lambda/(D\cos\theta)$, with $D = Nd$ the illuminated width. For a projector this says: **the spot divergence is set by the beam, not by the DOE**. Each order is a copy of the incident beam's angular spectrum, shifted to $\sin\theta_m$.

### 2.2 2D gratings and the pincushion of dot grids
A crossed 2D grating with periods $d_x, d_y$ at normal incidence sends order $(m_x, m_y)$ to the direction cosines

$$
\alpha = \frac{m_x\lambda}{d_x},\qquad \beta = \frac{m_y\lambda}{d_y},\qquad \gamma = \sqrt{1-\alpha^2-\beta^2}.
$$

Orders sit on a **regular grid in direction-cosine space**, not in angle space and not on a flat wall. On a screen at distance $L$, $x = L\alpha/\gamma$ and $y = L\beta/\gamma$. Corner spots have the smallest $\gamma$, so they are pushed outward. The result is a **pincushion**-shaped dot grid (see the Worked example). Two practical consequences:
1. If you want a rectilinear grid on a plane, the DOE design must pre-distort it, so the cell is no longer a simple crossed grating.
2. Your 3D-camera calibration will absorb this anyway. What matters is that the pattern is **stable** with temperature and wavelength.

### 2.3 Fourier view (Kenyon Ch. 7)
Kenyon shows that the Fraunhofer amplitude is the Fourier transform of the screen transmission $t(x)$, with conjugate variable $k_x = k\sin\theta$ [Kenyon §7.2.1, p. 166]. A periodic transmission is the convolution of one cell $h(x)$ with a comb of period $d$. Its transform is therefore the cell's transform **sampled** on a comb at $\sin\theta = m\lambda/d$. In one sentence:

> **The period decides where the orders go; the content of one period decides how much light each order gets.**

That is why the order efficiencies of a periodic DOE are simply the squared Fourier-series coefficients of one period:

$$
\eta_m = |c_m|^2,\qquad c_m = \frac{1}{d}\int_0^d t(x)\,e^{-2\pi i m x/d}\,dx,
$$

valid in the **thin-element (scalar) approximation**. You will compute $c_m$ with an FFT in Task 1. For a pure-phase element, $|t| = 1$, Parseval gives $\sum_m\eta_m = 1$ (energy conserved). For an amplitude element the absorbed light is lost.

## 3. Diffraction efficiency

### 3.1 The textbook gratings
All values below are scalar, normal-incidence, at the design wavelength:

| Grating (one period) | $\eta_0$ | $\eta_{\pm1}$ (each) | Notes |
|---|---|---|---|
| Binary amplitude, 50 % duty | 25 % | $1/\pi^2$ = 10.1 % | even orders 0; half the light absorbed |
| Sinusoidal amplitude, full modulation | 25 % | 1/16 = 6.25 % | Kenyon's "6 %" [§7.7.2, p. 190] |
| Sinusoidal phase, amplitude $a$ | $J_0^2(a)$ | $J_1^2(a)$, max 33.9 % at $a$ = 1.84 rad | Kenyon's "33 %"; $\eta_m = J_m^2(a)$ |
| Binary phase 0/π, 50 % duty | 0 | $4/\pi^2$ = 40.5 % | odd orders $4/(\pi m)^2$; even orders 0; symmetric ±1 |
| $N$-level staircase blaze | ≈ 0 | $\eta_{+1} = \mathrm{sinc}^2(1/N)$ | 2 → 40.5 %, 4 → 81.1 %, 8 → 95.0 %, 16 → 98.7 % |
| Continuous blaze (kinoform), depth $\lambda_0/(n-1)$ | 0 | $\eta_{+1}$ = 100 % | at $\lambda_0$ only |

Here $\mathrm{sinc}(x) = \sin(\pi x)/(\pi x)$. The multilevel row is Swanson's classic result (TR-854). It is why commercial DOEs are 2-, 4- or 8-level lithographic stacks: each extra mask doubles the levels.

### 3.2 Blazing
Kenyon introduces blazing for ruled reflection gratings [§6.9.1, pp. 142–143]. Tilting each facet by the blaze angle $\phi$ steers the single-slit envelope onto the first order, so most of the light lands there. The blaze wavelength is $\lambda_\text{blaze} = a\sin\phi$ (eq. 6.33). The transmission analogue is the **kinoform**: a sawtooth phase ramp of $2\pi$ per period, which is a prism "folded" modulo $2\pi$. A diffractive lens is a kinoform whose period shrinks with radius.

Off the design wavelength the sawtooth is no longer exactly $2\pi$ deep. With a phase depth of $2\pi\alpha$, where

$$
\alpha(\lambda) = \frac{\lambda_0}{\lambda}\,\frac{n(\lambda)-1}{n(\lambda_0)-1}\;\approx\;\frac{\lambda_0}{\lambda},
$$

the scalar efficiency into order $m$ is

$$
\eta_m(\lambda) = \mathrm{sinc}^2(m-\alpha).
$$

Numbers (verified, ignoring material dispersion unless stated):
- Visible hybrid lens blazed at 550 nm: at 450 nm, $\alpha$ = 1.222 and $\eta_1$ = 84.8 % (82.7 % including N-BK7 dispersion). At 650 nm, $\eta_1$ = 92.5 %. The missing light goes mostly into orders 0 and 2. These are **out-of-focus ghosts** that lower contrast (veiling glare, as in L07). This is why diffractive surfaces are rare in high-contrast visible camera lenses and common in narrow-band NIR systems.
- NIR element blazed at 850 nm, used at 940 nm: $\eta_1$ = 97.0 %, $\eta_0$ = 1.1 %.

### 3.3 Fabrication errors and the zero order
For a two-level phase grating with levels 0 and $\varphi$, write $t = A + B\,s(x)$ with $s = \pm1$, $A = (1+e^{i\varphi})/2$ and $B = (1-e^{i\varphi})/2$. Then all non-zero orders scale by $|B|^2 = \sin^2(\varphi/2)$, and the zero order becomes $|A + B\,c_0^{(s)}|^2$. For the 50 % duty π-grating ($c_0^{(s)} = 0$), a depth error $\varphi = \pi(1+\varepsilon)$ gives

$$
\eta_0 = \cos^2(\varphi/2) = \sin^2(\pi\varepsilon/2):\quad
\varepsilon = 2\,\% \to 0.10\,\%,\quad 5\,\% \to 0.62\,\%,\quad 10\,\% \to 2.4\,\%.
$$

The same equation covers **wavelength mismatch**: $\varphi \propto (n-1)/\lambda$. A π-grating made for 850 nm and used at 940 nm has $\varphi = 0.904\pi$, so $\eta_0$ = 2.2 %. For fused silica ($n$ ≈ 1.4525 at 850 nm), the π-depth is $h = \lambda/(2(n-1))$ = 0.939 µm. A 5 % error is 47 nm, which is a realistic etch tolerance. Vendors quote zero orders of order 1–2 % for good fan-out DOEs, and list the causes as depth error, wavelength, divergence, polarisation and features approaching λ (Holo/Or, *Methods to reduce zero order*: <https://www.holoor.co.il/methods-to-reduce-zero-order-2>).

The zero order matters more than its percentage suggests. When the DOE is designed so that order 0 is one of the dots (all Dammann gratings with odd $N$), an error makes the **central dot brighter**. In a 2D separable design, the effect is roughly doubled. In the Worked example, a 5×5 Dammann made for 850 nm and run at 940 nm puts 4.6 % into the central spot against 2.3 % per normal spot. A DOE with **even** symmetric fan-out (zero order nominally dark) leaks the error into a spot that should not exist.

## 4. Diffractive lenses

### 4.1 From zone plate to kinoform lens
A Fresnel zone plate with zone radii $\rho_m^2 = mR\lambda$ focuses like a thin lens with focal length $f = \rho_m^2/(m\lambda)$ [Kenyon §6.12.1, pp. 153–154]. Holography makes the same structure: recording the interference of a point source and a plane wave gives exactly these zones [Kenyon §7.7.1, eq. 7.69, p. 188]. An amplitude zone plate wastes most of the light (its first order is only ~10 %). A **phase** zone plate blazed into a sawtooth kinoform sends ideally 100 % into $m = +1$.

The modern description uses a **phase function** $\Phi(r)$ added to the wavefront (in radians). For a thin lens of focal length $f$, the required phase is

$$
\Phi(r) = -\frac{\pi r^2}{\lambda_0 f}\quad(\text{paraxial}),
$$

and the physical surface is $\Phi$ wrapped modulo $2\pi$, with $2\pi$ zone boundaries at $r_j = \sqrt{2j\lambda_0 f}$. The **zone count** within a semi-aperture $r$ is $N_z = r^2/(2\lambda_0 f)$. The **minimum zone width** at the edge is $\Lambda_\text{min} \approx \lambda_0 f/r$, which is just the local grating period that deviates a ray by $r/f$. The minimum zone width sets manufacturability: diamond turning likes tens of µm, lithography goes to a few µm. It also sets accuracy, because scalar efficiency is trustworthy only when $\Lambda \gg \lambda$ (rule of thumb ≳ 5–10 λ; see Swanson TR-914 and §6).

### 4.2 The Binary 2 surface
OpticStudio's sequential **Binary 2** surface is a standard (even-asphere-capable) surface plus a radially symmetric phase:

$$
\Phi(\rho) = M\sum_{i=1}^{N} A_i\,\rho^{2i},\qquad \rho = r/R_\text{norm},
$$

where $M$ is the diffraction order, $A_i$ are coefficients in radians, $N$ is the number of terms and $R_\text{norm}$ is the normalisation radius. All of these are surface parameters in the Lens Data Editor (older versions used the Extra Data Editor). The phase is wavelength-independent, but the optical path it adds is $\text{OPL} = \Phi\lambda/2\pi$ at the **actual** wavelength $\lambda$ (Ansys KB, Binary 2 article). Matching the $r^2$ term with a thin lens, $\text{OPL} = -r^2/(2f)$, gives

$$
\frac{1}{f_\text{DOE}(\lambda)} = -\frac{M A_1\lambda}{\pi R_\text{norm}^2}
\quad\Longrightarrow\quad A_1 = -\frac{\pi R_\text{norm}^2}{M\lambda_0 f}.
$$

So **positive power needs $A_1 < 0$** for $M = +1$. Check the sign of EFFL after you enter it, because the stated convention is easy to flip. Higher terms $A_2, A_3, \dots$ act exactly like aspheric terms. They correct spherical aberration and, because they disperse, **spherochromatism**. Relatives include **Binary 1** (x–y polynomial phase, for non-rotationally-symmetric DOEs), Radial Grating, Elliptical Grating and Zernike Standard Phase. Like Binary 2, all of them assume 100 % efficiency into order $M$.

### 4.3 Dispersion: $\nu_\text{diff} = -3.45$
Because $1/f \propto \lambda$, a diffractive lens has an "Abbe number"

$$
\nu_\text{diff} = \frac{\lambda_d}{\lambda_F - \lambda_C} = \frac{0.5876}{0.4861 - 0.6563} = -3.453,
$$

and a partial dispersion $P_{g,F} = (\lambda_g - \lambda_F)/(\lambda_F - \lambda_C) = 0.296$. Compare N-BK7: $\nu_d$ = 64.17, $P_{g,F}$ = 0.535. The diffractive lens is negative-dispersive (blue focuses **farther** away, the opposite of glass) and about 19× stronger in magnitude than N-BK7. In the NIR you define the analogue for your band, e.g. $\nu = \lambda_0/(\lambda_\text{short}-\lambda_\text{long})$.

**The Sweatt model.** Sweatt showed that a diffractive lens behaves exactly like a thin refractive lens of **infinite index** and vanishing curvature: $(n-1)(c_1-c_2) = 1/f$ is held constant while $n\to\infty$, with $n(\lambda) - 1 \propto \lambda$ (W. C. Sweatt, *J. Opt. Soc. Am.* 67, 803 (1977); 69, 486 (1979)). Three useful consequences:
1. Every Seidel/thin-lens formula you learned in Course 02 applies, with $n \to \infty$ and the "Sweatt dispersion".
2. The **Petzval contribution** $\phi/n \to 0$. A diffractive surface adds power **without field curvature**, a real asset in flat-field designs.
3. Before Binary surfaces existed, designers literally modelled DOEs in lens-design codes as glass with $n \approx 10^4$. You can still do that as a cross-check.

### 4.4 The hybrid achromat
Apply the thin-lens achromat equations (Course 02 L06) to a refractive lens of power $\phi_r$ and Abbe number $\nu_r$ combined with a DOE of power $\phi_d$:

$$
\phi_r + \phi_d = \phi,\qquad \frac{\phi_r}{\nu_r} + \frac{\phi_d}{\nu_\text{diff}} = 0
\;\Rightarrow\;
\phi_d = \phi\,\frac{-\nu_\text{diff}}{\nu_r - \nu_\text{diff}}.
$$

For N-BK7, $\phi_d/\phi = 3.453/67.62 = 0.0511$. The DOE carries only **5 %** of the power, and both powers are **positive**. A glass doublet (N-BK7/F2) needs $\phi_1 = 2.31\phi$ and $\phi_2 = -1.31\phi$, with strongly curved surfaces. That is the attraction: a hybrid singlet is weak, light, has small aberrations from the refractive part, and contains a single element (Stone & George, *Appl. Opt.* 27, 2960 (1988)).

The catch is **secondary spectrum**. The residual focal spread between F/C and g is $\Delta f \approx f\,(P_r - P_d)/(\nu_r - \nu_d)$ in magnitude. For $f$ = 50 mm: hybrid N-BK7 + DOE gives 0.18 mm, the N-BK7/F2 doublet 0.086 mm. The hybrid is about **2× worse**, because the diffractive $P_{g,F}$ = 0.296 is far off the normal glass line. Add the efficiency loss away from the blaze wavelength (§3.2) and the picture is clear. Hybrids are excellent in the **IR** (Kidger §12.5.3) and in **narrow-band** systems such as laser projectors, NIR receivers with a bandpass filter, and DVD/CD pickups. They are a compromise for broadband visible imaging.

## 5. Fan-out DOEs and dot-pattern projectors

### 5.1 The architecture
A typical laser dot projector, as found in many depth sensors:

```
VCSEL array ──► collimating lens (f ~ few mm) ──► DOE (fan-out, k×k orders) ──► scene
(N_e emitters,      images the emitter layout          tiles k² copies of the
 pseudo-random)     to infinity: N_e beamlets          emitter pattern across the FOV
```

Each emitter becomes a collimated beamlet in a slightly different direction. The DOE replicates the whole emitter pattern into $k\times k$ angular tiles. The scene sees about $N_e k^2$ dots, for example 300 emitters × 3×3 tiles ≈ 2700 dots. The design job splits into a **refractive part** (the collimator, designed sequentially like the L05 projection lens but reversed, with VCSEL emitters as the field) and a **diffractive part** (the DOE: tile angles from the grating equation, tile powers from the cell design). Variants include a single laser with a DOE generating a pseudo-random dot cloud directly (needs a large, IFTA-designed cell), line generators (1D fan-out or Powell lens), and DOE + diffuser flood illuminators. Patent literature describes these architectures, for example a DOE that deliberately expands the undiffracted beam for eye safety (US 9,959,465: <https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9959465>) and hybrid refractive–diffractive dot projectors (<https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12188763>).

**DMD projector vs. DOE dot projector** for a 3D camera:

| | DMD + projection lens (L05) | Laser/VCSEL + DOE |
|---|---|---|
| Pattern | Programmable (phase shifting, Gray code) | Fixed (one or a few patterns) |
| Depth method | Multi-shot fringe/phase | Single-shot dot matching (active stereo) |
| Efficiency, size | Étendue-limited, larger | High radiance, tiny |
| Problems | Lens cost, thermal, DMD window ghosts | Zero order, eye safety, speckle, wavelength drift |

### 5.2 Dammann gratings
H. Dammann's idea (early 1970s) was a **binary 0/π phase** grating whose transition points within one period are chosen so that the $N$ central orders are equal and as strong as possible. For a symmetric cell with transitions at $x_1, \dots, x_K$ in the half period $[0, 1/2]$, the Fourier coefficients are analytic:

$$
c_0 = 2\sum_{k=0}^{K} (-1)^k (x_{k+1}-x_k),\qquad
c_m = \frac{1}{\pi m}\sum_{k=0}^{K} (-1)^k\big[\sin(2\pi m x_{k+1}) - \sin(2\pi m x_k)\big],
$$

with $x_0 = 0$, $x_{K+1} = 1/2$ and $\eta_m = c_m^2$. Demanding $\eta_0 = \eta_1 = \dots = \eta_M$ gives $M$ equations, so $K = M$ transitions are the minimum. Our own optimisation (Task 1, verified by FFT) gives:

| Fan-out | Transitions (in half period) | Total efficiency | Per spot |
|---|---|---|---|
| 1×3 | 0.1324 (or 0.3676) | 66.4 % | 22.1 % |
| 1×5 | 0.1324, 0.4807 | 77.4 % | 15.5 % |
| 1×7 | 0.1229, 0.3448, 0.3954 | 65.5 % | 9.4 % |

(For 1×7, multi-start searches with 4–6 transitions did not beat 65.5 % for us. Published tables list values for many $N$; treat ours as "what a simple optimiser finds" and compare with Jahns et al. or Zhou & Liu if you need the record.) The remaining 23–35 % goes into **higher orders**. Those are useless outside the FOV and are a stray-light and safety concern. A crossed 2D Dammann ($t(x,y) = t(x)t(y)$, still binary because $\pm1\times\pm1 = \pm1$) has $\eta_{2D} = \eta_{1D}^2$, e.g. 5×5 → 59.9 %. Binary is cheap: one mask, one etch, and the ± orders are symmetric by construction.

To do better you need **multilevel or continuous phase**. A continuous-phase 1×3 "triplicator" reaches 92.6 %, and 1×5/1×7 cells exceed 92 % (Task 1, Stretch). Such profiles are found with an **iterative Fourier transform algorithm (IFTA**, Gerchberg–Saxton type), alternating between "phase-only in the DOE plane" and "desired amplitudes in the order plane", or with gradient optimisation as you will do. Whatever the cell, if it is periodic, the FFT of one period gives its scalar order efficiencies.

### 5.3 Zero order and eye safety
A DOE dot projector is a **laser product** and must be classified under IEC 60825-1, typically aiming for Class 1. The standard and a laser-safety specialist give the actual limits; this is not a lesson in AEL arithmetic. The optical designer must understand three mechanisms:
1. **Each dot is a collimated beamlet.** A collimated beam can be focused by the eye to a tiny retinal spot (the "small source" case), so per-dot power is what counts, and the brightest dot dominates. That is usually the **zero order**, which grows with depth error, wavelength drift and temperature (§3.3).
2. **Fault conditions**: if the DOE cracks, delaminates, or condensation fills its relief, the full beam can exit undiffracted. Products therefore add DOE integrity detection or design the system so that the undiffracted beam is itself safe, e.g. by keeping it divergent (US 9,959,465 above).
3. **Many emitters help**: with a VCSEL array and a collimator, each dot comes from one emitter with an apparent source size larger than a single-mode laser, and the power is spread over many dots.

The tasks therefore treat "max dot power / mean dot power" and "zero-order fraction under worst-case depth and wavelength" as first-class specifications, alongside efficiency and uniformity.

### 5.4 Speckle and dot patterns
L03 introduced speckle [Kenyon §14.4.5, p. 397; §7.7.2, p. 190]. In the camera image, a laser-lit rough surface shows a granular intensity pattern with grain size ≈ $2.44\,\lambda N_w(1+|m|)$ at the sensor, set by the **receiving** lens working F-number $N_w$ and magnification $m$. For fully developed polarised speckle the contrast is $C = \sigma_I/\langle I\rangle = 1$. Averaging $N$ independent speckle patterns (different wavelengths, angles, polarisations, moving diffusers, many incoherent emitters overlapping) reduces it as $C = 1/\sqrt{N}$.

For triangulation, Dorsch, Häusler and Herrmann showed that speckle sets a **fundamental** limit on locating a spot. The centroid uncertainty corresponds to a depth uncertainty $\delta z \approx C\lambda/(2\pi\sin u_\text{obs}\sin\theta)$, where $\sin u_\text{obs}$ is the observation aperture and $\theta$ the triangulation angle (*Appl. Opt.* 33, 1306 (1994)). Example: $\lambda$ = 850 nm, $\sin u_\text{obs}$ = 0.02, $\theta$ = 15°, $C$ = 1 gives $\delta z$ ≈ 26 µm, **independent of SNR and pixel count**. This is one reason high-accuracy industrial 3D cameras favour incoherent (LED) illumination, and why laser dot projectors are paired with speckle-reduction tricks.

## 6. When ray tracing is not enough

The thin-element (scalar) model assumes the DOE simply multiplies the field by $e^{i\Phi(x)}$. It breaks down when:
- **feature size** approaches λ (rule of thumb: periods below about 5–10 λ, or large deflection angles beyond ~20–30°). Then shadowing by finite-depth walls, polarisation dependence and resonance effects appear. Swanson's TR-914 explains why scalar theory is optimistic, and Holo/Or quotes the ~5λ limit.
- the element is **thick** (volume holograms, Bragg selectivity [Kenyon §7.7.4, p. 191]).
- **sub-wavelength** structures are used (metasurfaces, moth-eye AR).

The tool hierarchy:

| Need | Tool |
|---|---|
| Order directions, system layout, imaging with one order | OpticStudio sequential (Diffraction Grating, Binary 1/2) |
| Several orders at once, stray orders, energy bookkeeping with **given** efficiencies | OpticStudio NSC with ray splitting by order |
| Order efficiencies of a large-period cell, cell design | Scalar FFT / IFTA (Python, Task 1) |
| Efficiencies of fine or deep structures, polarisation, angle dependence | Rigorous: **RCWA** (periodic) or **FDTD**, e.g. **Ansys Lumerical** |
| Coherent beam through DOE (spot shape, interference between orders) | POP (one order at a time) or a dedicated wave-optics propagator |

Ansys now couples these: Lumerical RCWA results can be passed to OpticStudio NSC objects via the **Lumerical Sub-Wavelength Model (LSWM)** DLL. That is a Premium/Enterprise feature requiring a Lumerical licence; see *Exporting Dynamic LSWM DOE Models to Static JSON*: <https://optics.ansys.com/hc/en-us/articles/42661871922067>. You do not need this for the course. You do need to know that the efficiency numbers in a ray trace are **inputs**, and to say where they came from.

## 7. In OpticStudio

### 7.1 Sequential: Diffraction Grating surface
- In the LDE, set the surface type to **Diffraction Grating**. Its parameters are the groove frequency in **lines/µm** (= $1/d$ with $d$ in µm) and the **Diffraction Order**. The grooves are straight and parallel to the local x axis, so diffraction happens in the local y–z plane (check the Help page for your version). Grating plus refraction obey $n_2\sin\theta_2 - n_1\sin\theta_1 = M\lambda/d$.
- One configuration traces **one** order at 100 % efficiency. To see several orders, use the **Multi-Configuration Editor** with the order parameter varied per configuration (a PARn row on the grating surface). Holo/Or's Zemax tutorial does exactly this for a 1×5 splitter: <https://www.holoor.co.il/wp-content/uploads/2018/03/Beam-splitter-tutorial-for-Zemax.pdf?x17494>. An alternative trick represents each order by a **field angle**.
- If an order is evanescent ($|\sin\theta| > 1$), the ray fails. A ray-error message on a grating usually means you asked for a non-existent order.
- For a lens after a fan-out DOE (e.g., the collimator), it is often cleaner to model the DOE as **field angles** at the collimator's object side and leave the grating out entirely.

### 7.2 Sequential: Binary 2 (and friends)
- Set the surface type to **Binary 2**. Enter Diffraction Order $M$ (usually 1), number of terms, **Normalization Radius** (set it to about the semi-diameter and **never change it after optimising**, or all $A_i$ change meaning), and the coefficients $A_1, A_2, \dots$ in radians.
- Make $A_1$ (power) and $A_2$ (spherochromatism) variables. Standard operands work: EFFL for focal length, AXCL for axial colour, LACL for lateral colour.
- To inspect the phase and zones, use the surface phase analyses under **Analyze** (location varies by version; search the ribbon for "Phase"), or the `Phases.zpl` macro used in the Ansys Binary 2 article to list zone radii for fabrication.
- Remember: the trace assumes **100 % efficiency into order M**. Out-of-band efficiency loss and ghost orders are **not** in the MTF or spot diagram. You add them by hand (scalar $\mathrm{sinc}^2$) or in NSC.

### 7.3 Non-sequential: multiple orders and ray splitting
- The NSC **Diffraction Grating** object is a Standard-Lens-like solid with a ruled grating face. Its parameters include the grating frequency (lines/µm) and a default diffraction order (Ansys getting-started article on NSC: <https://optics.ansys.com/hc/en-us/articles/42661670424851>). Phase objects such as **Binary 1/Binary 2** also exist in NSC (help section "Binary 1 (non-sequential geometry objects)").
- **Splitting into several orders at once** is configured in **Object Properties → Diffraction**. There you choose how energy is split among orders: by a table of relative energies you type in, or by a **diffractive DLL** ("Split by DLL function", e.g. the sample `diff_samp_1.dll`, as used in the Holo/Or tutorial). You also set a **Start Order** and **Stop Order**. A Zemax community answer states that at most **40 orders** are traced simultaneously (<https://community.zemax.com/got-a-question-7/how-to-model-diffractive-optical-element-doe-with-high-order-3145>). For a 2D fan-out, place **two crossed gratings** (the second rotated 90° about z), as in the Holo/Or tutorial. *Verify the exact option labels in your version's Help; they have been stable but are worded slightly differently between releases.*
- Turn on **Split NSC Rays** (Ray Trace Control and detector updates) or you will see only one order. Raise **Maximum Segments per Ray** (L02) if many orders × many surfaces hit the limit.
- The sample file *Diffraction grating multiple orders.zmx* in the Non-sequential/Diffractives samples folder shows each input ray split into five orders. Open it before Task 3.
- To see the pattern, place a **Detector Rectangle** at a distance (spatial dots, including pincushion) or view a detector in **angle space**/a **Detector Polar** (direction cosines → the regular grid). Use ZRD filter strings (L02/L07) to isolate rays that hit the grating object.
- The efficiencies you type into the split table come **from you**: Task 1's FFT, a vendor datasheet, or RCWA/LSWM.

### 7.4 Common mistakes
- Treating the sequential trace of order +1 as the whole story, so the 0 and 2 orders are forgotten. In a projector they are real ghosts. In a hybrid camera lens they are veiling glare.
- Changing the normalisation radius of a Binary 2 surface after optimisation.
- Forgetting that the grating equation uses the **vacuum** wavelength with media indices, so a grating embedded in glass gives different angles inside and the same angles once back in air.
- Reporting DOE efficiencies from a ray trace. The ray trace only returns what you put in.
- Ignoring wavelength drift. VCSELs shift about 0.06–0.07 nm/K, which moves dots by $\Delta\sin\theta/\sin\theta = \Delta\lambda/\lambda$ and changes the zero order.

## Worked example — a 1×7 line of dots and a 5×5 dot grid at 850 nm

**(a) Period for a 1×7 fan-out spanning ±15°.** The outermost order $m = 3$ must leave at 15° at normal incidence in air:

$$
d = \frac{3\lambda}{\sin 15^\circ} = \frac{3\times0.85}{0.2588} = 9.85\ \mu\text{m}\ (0.1015\ \text{lines/µm}).
$$

Orders 1, 2, 3 leave at 4.95°, 9.94°, 15.00°. On a wall at $L$ = 1000 mm they land at 86.6, 175.2 and 267.9 mm. A perfectly equal spacing would be 89.3 mm (one third of 267.9), so the outer gaps are wider: $\tan\theta$ grows faster than $\sin\theta$. The period is 11.6 λ, comfortably in the scalar regime.

**(b) Efficiency of the binary Dammann version.** From §5.2 with 3 transitions: 65.5 % total, 9.4 % per dot. A 4-level or continuous cell would reach more than 90 %.

**(c) A 5×5 crossed Dammann at 850 nm.** The 1D 1×5 cell (transitions 0.1324, 0.4807) has $\eta$ = 15.47 % per order and 77.4 % total. In 2D, each of 25 dots gets $0.1547^2$ = 2.39 % and the total is 59.9 %. From a 200 mW laser, each dot carries 4.8 mW and about 80 mW goes into higher orders.

**(d) Pincushion.** With $d_x = d_y$ = 9.85 µm and orders up to ±3 (if it were 7×7), the corner order (3,3) has $\alpha = \beta = 0.2588$ and $\gamma = 0.9306$. On the wall it lands at $x$ = 278.1 mm, versus 267.9 mm for the on-axis order (3,0). The corner is pushed out by **3.8 %**: classic pincushion.

**(e) Zero order under errors.** For the 5×5 grid (1D cell $c_0 = +0.393$), a +5 % etch-depth error raises the central (0,0) dot to 3.0 % against 2.38 % for a typical dot (+26 %). Running the 850 nm design at 940 nm gives 4.6 % against 2.34 % (**~2×**). The brightest dot, not the average, sets the laser-safety margin. These numbers come from $t = A + B\,s(x)s(y)$ (§3.3) and are reproduced in Task 1.

**(f) Hybrid achromat sanity numbers** (for Task 4): $f$ = 50 mm, N-BK7 + Binary 2, EPD 25 mm. Then $f_\text{DOE}$ = 979 mm, $f_\text{refr}$ = 52.7 mm, $A_1 = -\pi(12.5)^2/(0.5876\times10^{-3}\cdot979) = -853$ rad with $R_\text{norm}$ = 12.5 mm, about 136 zones, and a minimum zone width ≈ 46 µm, easily diamond-turned.

## Key takeaways
- **Period → angles, cell content → efficiencies.** The grating equation (Snell plus $m\lambda/d$) is exact in a ray trace. Efficiencies are the squared Fourier coefficients of one period in scalar theory, and need RCWA/FDTD when features approach λ.
- Order spots are copies of the incident beam: **beam quality sets dot size**, the DOE sets dot positions. Orders form a grid in **direction cosines**, which appears as pincushion on a flat wall.
- Binary phase gratings top out near 40.5 % per first order, $N$-level stairs reach $\mathrm{sinc}^2(1/N)$, and Dammann fan-outs reach 66–77 %. Continuous/IFTA cells exceed 90 %.
- The **zero order** is driven by etch depth and wavelength error, $\eta_0 \approx \sin^2(\pi\varepsilon/2)$ for a π-grating. In a dot projector it sets the brightest dot and therefore eye safety; design for worst-case tolerance and fault conditions.
- A diffractive lens behaves like a Sweatt infinite-index lens: $\nu_\text{diff} = -3.45$, $P_{g,F}$ = 0.296, zero Petzval. A hybrid achromat puts ~5 % of the power in the DOE but has ~2× the secondary spectrum of a glass doublet and loses efficiency away from the blaze wavelength. Hybrids are good for narrow-band NIR, weak for broadband visible.
- In OpticStudio: Diffraction Grating and Binary 2 trace **one order at 100 %**. Use multi-config for others, or NSC **Object Properties → Diffraction** splitting (≤ 40 orders) with efficiencies you supply.
- Laser patterns bring **speckle**, a fundamental triangulation noise floor $\delta z \approx C\lambda/(2\pi\sin u\sin\theta)$, reduced only by diversity ($1/\sqrt N$).

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Diffraction order $m$ | Integer labelling the directions where waves from all periods add in phase |
| Grating equation | $n_2\sin\theta_m - n_1\sin\theta_i = m\lambda/d$ |
| Diffraction efficiency $\eta_m$ | Fraction of incident power diffracted into order $m$ |
| Blaze / blaze wavelength | Facet tilt (or sawtooth phase) that concentrates light in one order; $\lambda_\text{blaze}=a\sin\phi$ |
| Kinoform | Continuous sawtooth phase profile wrapped modulo $2\pi$ |
| Multilevel (binary) optics | Staircase approximation of a kinoform made with $\log_2 N$ lithographic masks |
| DOE | Diffractive optical element: any surface relief or index structure designed to diffract |
| Fan-out / beam splitter DOE | Periodic DOE producing an array of equal-power orders |
| Dammann grating | Binary 0/π phase grating with optimised transition points giving equal orders |
| IFTA | Iterative Fourier transform algorithm (Gerchberg–Saxton type) for phase-only DOE design |
| Zero order | Undiffracted light ($m=0$); a hot spot when the DOE is imperfect |
| Binary 2 surface | OpticStudio surface adding radial phase $M\sum A_i\rho^{2i}$ |
| Normalization radius | $R_\text{norm}$ dividing $r$ in the Binary 2 polynomial |
| Sweatt model | Equivalence of a diffractive lens with a thin lens of infinite index |
| Diffractive Abbe number | $\nu = \lambda_d/(\lambda_F-\lambda_C) = -3.45$ |
| Hybrid achromat | Refractive lens plus diffractive surface correcting primary colour |
| Zone | Annulus over which a diffractive lens phase increases by $2\pi$ |
| RCWA | Rigorous coupled-wave analysis, an exact EM solver for periodic structures |
| LSWM | Lumerical Sub-Wavelength Model, a DLL bringing RCWA results into OpticStudio |
| Speckle contrast $C$ | $\sigma_I/\langle I\rangle$ of a speckle pattern; 1 for fully developed speckle |

## References
1. [Kenyon §6.5, pp. 134–136] Diffraction from multiple identical slits.
2. [Kenyon §6.8, pp. 139–140] Diffraction gratings; resolving power, free spectral range, reflection grating equation.
3. [Kenyon §6.9.1, pp. 142–143] Grating structure, ruled vs. holographic, blazing.
4. [Kenyon §6.12–6.12.1, pp. 151–154] Fresnel zones and zone plates.
5. [Kenyon §7.2.1, pp. 166–167] Diffraction as Fourier transform; convolution picture of gratings.
6. [Kenyon §7.7–7.7.4, pp. 188–191] Holography; phase vs. amplitude efficiency; speckle; thick holograms.
7. [Kenyon §14.4.5, p. 397] Laser speckle (see also L03).
8. [Kidger §12.5.3, p. 250] Diffractive surfaces in thermal-IR lenses.
9. W. C. Sweatt, "Describing holographic optical elements as lenses," *J. Opt. Soc. Am.* 67, 803 (1977); "Mathematical equivalence between a holographic optical element and an ultra-high index lens," *J. Opt. Soc. Am.* 69, 486 (1979).
10. T. Stone and N. George, "Hybrid diffractive-refractive lenses and achromats," *Appl. Opt.* 27, 2960 (1988).
11. R. G. Dorsch, G. Häusler, J. M. Herrmann, "Laser triangulation: fundamental uncertainty in distance measurement," *Appl. Opt.* 33, 1306 (1994).
12. H. Dammann and K. Görtler, "High-efficiency in-line multiple imaging by means of multiple phase holograms," *Opt. Commun.* 3, 312 (1971). J. Jahns, M. M. Downs, M. E. Prise, N. Streibl, S. J. Walker, "Dammann gratings for laser beam shaping," *Opt. Eng.* 28, 1267 (1989); C. Zhou and L. Liu, "Numerical study of Dammann array illuminators," *Appl. Opt.* 34, 5961 (1995).
13. IEC 60825-1, *Safety of laser products — Part 1: Equipment classification and requirements* (current edition).
14. G. J. Swanson, *Binary Optics Technology: The Theory and Design of Multi-level Diffractive Optical Elements*, MIT Lincoln Lab TR-854 (1989): <https://apps.dtic.mil/sti/pdfs/ADA213404.pdf>
15. G. J. Swanson, *Binary Optics Technology: Theoretical Limits on the Diffraction Efficiency of Multilevel DOEs*, MIT Lincoln Lab TR-914 (1991): <https://apps.dtic.mil/sti/pdfs/ADA235404.pdf>
16. Ansys Optics KB, diffractive surfaces in OpticStudio (grating equation, order sign, efficiency assumption): <https://optics.ansys.com/hc/jp/articles/42661739263251>
17. Ansys Optics KB, *How to design DOE lens or metalens in OpticStudio*: <https://optics.ansys.com/hc/en-us/articles/42661666194323>
18. Ansys Optics KB, Binary 2 hybrid singlet (phase, OPL = Φλ/2π, zone radii): <https://optics.ansys.com/hc/en-us/articles/42661706685075>
19. Ansys Optics KB, Exploring Non-Sequential Mode (Diffraction Grating object, splitting into orders, diffractive DLLs): <https://optics.ansys.com/hc/en-us/articles/42661670424851>
20. Ansys Optics KB, *Exporting Dynamic LSWM DOE Models to Static JSON for OpticStudio and Speos* (RCWA ↔ OpticStudio): <https://optics.ansys.com/hc/en-us/articles/42661871922067>
21. Zemax Community, DOE with many orders (40-order limit, Object Properties → Diffraction): <https://community.zemax.com/got-a-question-7/how-to-model-diffractive-optical-element-doe-with-high-order-3145>
22. Holo/Or, *Beam splitter tutorial for Zemax* (sequential multi-config, field-angle and NSC "Split by DLL function" methods): <https://www.holoor.co.il/wp-content/uploads/2018/03/Beam-splitter-tutorial-for-Zemax.pdf?x17494>
23. Holo/Or, *Methods to reduce zero order*: <https://www.holoor.co.il/methods-to-reduce-zero-order-2>
24. US Patent 9,959,465, "Diffractive optical element with undiffracted light expansion for eye safe operation": <https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9959465>
25. US Patent 12,188,763, "Dot projector including hybrid refractive-diffractive optical elements": <https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12188763>
