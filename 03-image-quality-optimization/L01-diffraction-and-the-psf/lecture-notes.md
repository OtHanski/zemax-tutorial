# L01 — Diffraction and the point spread function

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~3 h, tasks ~5 h
> **Prerequisites:** [Course 01 L04 (stops, pupils, F/#)](../../01-foundations/L04-stops-pupils-fields/), [Course 01 L06 (real rays, spot diagrams)](../../01-foundations/L06-real-rays-and-analysis-tools/), [Course 02 L01 (wavefront aberration, Zernikes)](../../02-aberrations-classical-design/L01-wavefront-and-transverse-aberrations/) · **Next:** [L02 — MTF theory and practice](../L02-mtf-theory-and-practice/)

## Learning objectives
- Explain, using the Huygens–Fresnel picture, why an aberration-free lens images a point as an Airy pattern, and why the pattern in the image plane is a *Fraunhofer* pattern even though the screen is at a finite distance.
- Write the PSF as the squared modulus of the Fourier transform of the pupil function, and identify every scaling constant (wavelength, working F/#, exit-pupil distance).
- Compute the Airy radius ($1.22\,\lambda N$), FWHM, encircled energy in the core, and peak irradiance for a given lens, wavelength and power, and compare them with a sensor pixel.
- State and use the Rayleigh, Sparrow and Maréchal-type "diffraction-limited" criteria, and explain why a geometric spot diagram stops being meaningful when the spot is comparable to the Airy disk.
- Choose between OpticStudio's FFT PSF and Huygens PSF for a given system (tilted image planes, large chief-ray angles, pupil aberrations, fast beams, strong defocus) and set their sampling parameters so the result is not aliased.
- Compute an FFT PSF of an aberrated circular pupil in Python and reproduce OpticStudio's numbers.

## Reading
- **Core:** [Kenyon §6.1–6.3, pp. 129–133] — Kirchhoff's inclination and range factors (§6.2), the phasor treatment of the slit (§6.3). Focus on the idea that path difference *linear* across the aperture is what makes Fraunhofer diffraction simple.
- **Core:** [Kenyon §6.7, pp. 138–139] — the circular aperture, Bessel-function derivation, 84% of the light in the Airy disk, Rayleigh's criterion.
- **Core:** [Kenyon §6.10, pp. 146–147] — Fresnel vs. Fraunhofer, the Rayleigh distance, and the elegant argument that the diffraction pattern observed *in the image plane of the source* is a Fraunhofer pattern.
- **Core:** [Geary §7.4.4, p. 82] — pupil function, coherent and incoherent PSF in one paragraph; [Geary §31.1–31.2.1, pp. 355–357] — the Airy core diameter $2.44\lambda(f/\#)$ and the transition from "spot compactness" to diffraction metrics.
- **Optional:** [Kenyon §6.4–6.6, pp. 133–138] (rectangular apertures, multiple slits, Babinet) — useful later for gratings and DOEs (Course 05 L08).
- **Optional (online):** Ansys knowledge base, "How to model the PSF in OpticStudio" (Ken Moore): <https://optics.ansys.com/hc/en-us/articles/42661723066515> — spot diagram vs FFT PSF vs Huygens PSF and their sampling settings.
- **Optional (online):** Ansys knowledge base KA-01494, "Huygens PSF and FFT PSF" (Betsy Goodwin): <https://optics.ansys.com/hc/en-us/articles/42661795535251> — validity conditions of the FFT PSF and the direction-cosine spot-diagram test.
- **Optional (online):** Zemax Community, "Why does the FFT PSF differ from the Huygens PSF? Which one should I trust?": <https://community.zemax.com/product-updates/why-does-the-fft-psf-differ-from-the-huygens-psf-which-one-should-i-trust-4466>

---

## 1. Why a perfect lens does not make a point

Everything in Courses 01–02 treated light as rays. A perfect lens in ray optics sends every ray from an object point to one image point: the spot diagram collapses to a dot. Real light is a wave, and the lens only lets through the part of the wavefront that fits inside the aperture stop. Cutting a wavefront off sharply at the pupil edge is exactly what produces diffraction: the image of a point becomes a small, structured patch whose size is set by the wavelength and the cone angle of the converging beam, not by the lens's aberrations [Geary §31.2.1, p. 355].

A useful way to picture it is the **reference sphere** from Course 02 L01. A perfect lens produces, in its exit pupil, a spherical wavefront centred on the paraxial image point. Each point of that wavefront acts as a source of secondary Huygens wavelets. At the centre of the sphere all wavelets arrive in phase: bright. Move a small distance $r$ sideways in the image plane and wavelets from opposite edges of the pupil acquire a path difference of roughly $r \cdot D/R$ (D = pupil diameter, R = radius of the reference sphere). When that path difference reaches about a wavelength, contributions from the two halves of the pupil cancel and the intensity drops to zero. So the size of the bright core is of order $\lambda R/D = \lambda N$, where $N$ is the (working) F-number. All the rest of this lesson is making that estimate exact and learning how OpticStudio computes it for real, aberrated lenses.

### 1.1 The Huygens–Fresnel–Kirchhoff picture
Kenyon gives Kirchhoff's form of the secondary-wavelet amplitude [Kenyon §6.2, eq. 6.1, p. 130]: each element $dS$ of the aperture contributes

$$
dE \propto \frac{e^{ik(r_\text{in}+r_\text{out})}}{r_\text{in}\,r_\text{out}}\;\frac{\cos\theta_\text{in}+\cos\theta_\text{out}}{2}\,dS ,
$$

where $k = 2\pi/\lambda$, $r_\text{in}, r_\text{out}$ are the distances from the source to the aperture element and from the element to the observation point, and the **inclination factor** $(\cos\theta_\text{in}+\cos\theta_\text{out})/2$ removes the unphysical backward wave. For lens design the important point is Kenyon's remark that when the inclination and range ($1/r$) factors vary little over the aperture they only scale the result and can be dropped. That is true for beams up to roughly F/1.5; for very fast beams (high NA) the factors matter and one moves to *vector* diffraction theory — which is why OpticStudio's documentation restricts the FFT PSF to slower than about F/1.5 (see §5).

### 1.2 Fraunhofer vs. Fresnel — and why the image plane is "Fraunhofer"
If a point $P$ is at distance $r$ from an aperture point $S$ located a transverse distance $\rho$ from the foot of the perpendicular, the path is $s = \sqrt{r^2+\rho^2} \approx r + \rho^2/2r$ [Kenyon eq. 6.42, p. 146]. The quadratic term is the signature of **Fresnel** diffraction. When the phase depends only *linearly* on position across the aperture, the diffraction is **Fraunhofer** and the pattern is a Fourier transform of the aperture. For a plane wave on an aperture of radius $a$ the far-field (Rayleigh) distance is $\pi a^2/\lambda$ [Kenyon eq. 6.45, p. 147].

Kenyon's key argument [§6.10, p. 147]: when you observe in the **image plane of the source**, imagine a negative lens just before the aperture that collimates the light and a positive lens just after that refocuses it. The two lenses cancel, so nothing changes — but now the aperture sees plane waves in and out, which is the Fraunhofer setup. Hence: *the diffraction pattern at the focus of an aberration-free lens is the Fraunhofer pattern of its exit pupil*, scaled by the focal distance. The converging spherical wave has "used up" the quadratic phase. Aberrations are the residual phase $W(x,y)$ that the lens did *not* cancel; they enter the Fraunhofer integral as a phase factor.

**When this breaks down.** The argument assumes the reference sphere is large compared with the wavelength-scaled pupil, i.e. a large **Fresnel number** of the converging beam, $N_F = a^2/(\lambda R)$ ($a$ = exit-pupil semi-diameter, $R$ = distance to focus). For a 25 mm F/2.8 camera lens at 850 nm, with the exit pupil about 25 mm from focus, $a = 4.46$ mm and $N_F \approx 4.46^2/(0.85\times10^{-3}\cdot 25) \approx 940$ — Fraunhofer is excellent. For a micro-lens of 30 µm diameter focusing 100 µm away, $N_F \approx 2.6$: the intensity maximum moves noticeably towards the lens ("focal shift") and you need Fresnel/angular-spectrum propagation (OpticStudio's Physical Optics Propagation, L07). The same caution applies far from focus (strong defocus): then the image plane is not where the wave converges, and the FFT method's assumptions fail.

## 2. Pupil function and PSF

Put Cartesian coordinates $(x_p, y_p)$ on the exit pupil and $(x, y)$ in the image plane, measured from the reference point (normally the chief-ray intersection). The **pupil function** is [Geary §7.4.4, eq. 7.4, p. 82]

$$
p(x_p,y_p) = A(x_p,y_p)\,\exp\!\left[\,i\,\frac{2\pi}{\lambda}\,W(x_p,y_p)\right],
$$

with $A$ the amplitude transmission (1 inside the pupil, 0 outside for a clear circular stop; non-uniform if there is apodization, e.g. a Gaussian laser beam or coating roll-off) and $W$ the wavefront aberration (OPD, in length units) relative to the reference sphere. Then the **coherent (amplitude) PSF** is the Fourier transform

$$
U(x,y) \propto \iint p(x_p,y_p)\,\exp\!\left[-\,\frac{2\pi i}{\lambda R}\,(x\,x_p + y\,y_p)\right] dx_p\,dy_p ,
$$

and the **incoherent PSF**, which is what a sensor measures, is $\mathrm{PSF}(x,y) = |U(x,y)|^2$ [Geary eqs. 7.5–7.6]. Here $R$ is the radius of the reference sphere (exit pupil to image distance). Writing it with normalized pupil coordinates $\rho_x = x_p/a$, $\rho_y = y_p/a$ shows that the natural image-plane unit is

$$
\frac{\lambda R}{2a} = \lambda N_w, \qquad N_w = \frac{1}{2\,n'\sin u'} ,
$$

the **working F-number** (image-space, at the actual conjugates, $u'$ = marginal ray angle in image space, $n'$ = image-space index). Two practical consequences:

1. **Use the working F/#, not the "infinity" F/#.** At magnification $m$ (negative for a real inverted image), $N_w \approx (1-m)N_\infty$ for a lens whose pupil magnification is ~1. A machine-vision lens at F/2.8 working at $m=-0.1$ has $N_w \approx 3.1$; at $m=-1$ (macro) $N_w \approx 5.6$. OpticStudio reports both (System Data: "Working F/#" and "Image Space F/#"); its Airy radius uses the working value.
2. **The PSF is a Fourier transform of the pupil.** Everything you know about FFTs — sampling, padding, aliasing, scaling theorems — applies directly (§4).

### 2.1 The Airy pattern
For a clear circular pupil and $W = 0$, the transform is a Bessel function [Kenyon §6.7, eqs. 6.17–6.18, pp. 138–139]:

$$
\mathrm{PSF}(r) = I_0\left[\frac{2J_1(v)}{v}\right]^2, \qquad v = \frac{\pi\,r}{\lambda N_w}.
$$

Useful numbers (all computed numerically, in units of $\lambda N_w$):

| Feature | Position $r/(\lambda N_w)$ | Value |
|---|---|---|
| First zero (Airy radius) | **1.220** | — |
| Second zero | 2.233 | — |
| Third zero | 3.238 | — |
| FWHM (full width) | 1.029 | — |
| First bright ring peak | 1.635 | 1.75% of $I_0$ |
| Encircled energy inside 1st zero | — | **83.8%** |
| … inside 2nd zero | — | 91.0% |
| … inside 3rd zero | — | 93.8% |

The famous "84%" [Kenyon p. 139] is the first entry. The Airy *disk diameter* $2.44\lambda N_w$ is what Geary uses [eq. 31.1, p. 355] and what OpticStudio draws as a circle on spot diagrams (Spot Diagram settings → Show Airy Disk). In NA terms, $r_\text{Airy} = 0.61\,\lambda/\text{NA}$ with $\text{NA} = n'\sin u'$.

**Peak irradiance.** If power $P$ passes the pupil of area $\pi a^2$, energy conservation and the Fourier-transform normalization give $I_0 = P\,\pi a^2/(\lambda^2 R^2) = \pi P/(4\lambda^2 N_w^2)$. For 1 mW at 850 nm and F/2.8 this is 139 W/mm² (139 µW/µm²). Laser-safety, sensor-saturation and damage questions start here.

### 2.2 Resolution criteria
- **Rayleigh:** two equal incoherent points are "resolved" when the peak of one falls on the first zero of the other: separation $1.22\lambda N_w$ (angular $1.22\lambda/D$ in object space) [Kenyon eq. 6.19, p. 139]. The intensity at the midpoint is then 73.5% of the peaks — a visible dip.
- **Sparrow:** the separation at which the dip just disappears (second derivative zero at the midpoint): $0.947\lambda N_w$. Closer to what a noise-free detector could separate.
- Both are about *two-point* resolution. For extended scenes we will use the MTF (L02), which contains strictly more information.

## 3. Aberrated PSFs and the meaning of "diffraction-limited"

### 3.1 Small aberrations: energy moves from core to rings
With a small aberration, the central peak drops and the lost energy goes mainly into the first ring [Geary Fig. 31.2, p. 356]. The ratio of the aberrated to unaberrated peak is the **Strehl ratio** $S$ (L03). For small RMS wavefront error $\sigma$ (in waves), $S \approx \exp[-(2\pi\sigma)^2]$ [Geary eq. 31.3, p. 356]. Three cases you can verify in the tasks:

| Wavefront | RMS $\sigma$ | Exact $S$ | $\exp[-(2\pi\sigma)^2]$ |
|---|---|---|---|
| Defocus, $W_{020} = 0.25\lambda$ (PV $\lambda/4$) | 0.0722 λ | 0.811 | 0.814 |
| Spherical $W_{040}=0.25\lambda$, paraxial focus | 0.0745 λ | 0.802 | 0.803 |
| Same spherical, balanced with $W_{020} = -0.25\lambda$ | 0.0186 λ | 0.987 | 0.986 |

This is why the classical **Rayleigh quarter-wave rule** (PV wavefront error ≤ λ/4) and the **Maréchal criterion** (RMS ≤ λ/14 ≈ 0.071 λ, i.e. $S \ge 0.8$) are considered equivalent for low-order aberrations. A lens meeting them over the field is called **diffraction-limited**. Note the table's last row: the *same* spherical aberration looks four times smaller in RMS when you refocus — the optimizer does this automatically if you let the back focus vary.

### 3.2 Large aberrations: the PSF becomes the spot diagram
When the wavefront error is many waves, the Fourier integral is dominated by points of stationary phase: each small patch of the pupil sends its light in the direction of its local wavefront normal, i.e. along its *ray*. The PSF then approaches the geometric ray density (the spot diagram, smoothed by a diffraction kernel of about the Airy size). This gives a practical rule:

| RMS spot radius vs. Airy radius | Regime | Trust |
|---|---|---|
| $\gg 1$ (say > 2–3×) | geometric | spot diagram, geometric MTF/EE are fine and fast |
| ~0.5–2× | transition | use diffraction analyses (FFT/Huygens PSF and MTF) |
| $\ll 1$ (spot inside Airy circle) | diffraction-limited | judge by wavefront RMS / Strehl; spot size is meaningless |

Geary's "spot completely enclosed by the Airy disk" requirement in his transmission-sphere homework [Geary §9.5, p. 101] is the geometric face of the same idea; it is a sufficient but crude test. Courses 01–02 optimized RMS *spot*; from L03 on we will often optimize RMS *wavefront* instead.

### 3.3 Shapes worth recognizing
- **Defocus:** symmetric; at 1 wave PV defocus ($W_{020} = \lambda$) the centre goes exactly dark (axial intensity $\propto \mathrm{sinc}^2(\pi W_{020}/\lambda)$).
- **Spherical:** symmetric but different on the two sides of focus — the standard star-test signature.
- **Coma:** a comet with the brighter head offset along the field direction; the centroid is displaced from the chief ray (lateral shift ↔ the "centroid vs chief ray" choice in the merit function).
- **Astigmatism:** a cross at best focus, lines at the sagittal and tangential foci [Geary Fig. 31.7, p. 363].

## 4. Computing a PSF numerically: the FFT and its sampling

The FFT method samples the pupil function on an $N\times N$ grid across the pupil diameter, embeds it in a larger $M\times M$ array of zeros (**padding factor** $Q = M/N$), and takes a 2-D FFT. The scaling follows from the discrete Fourier transform:

$$
\Delta x_\text{image} = \frac{\lambda N_w}{Q}, \qquad L_\text{image} = M\,\Delta x = N\,\lambda N_w .
$$

Read these carefully, because they are the source of every PSF artefact:

- **Padding sets image resolution.** $Q = 2$ gives a spacing of $\lambda N_w/2$, which is exactly the Nyquist interval for the *intensity* PSF (its spectrum — the OTF — extends to $1/(\lambda N_w)$, L02). Less than $Q=2$ undersamples the PSF itself.
- **Pupil sampling sets the image field size.** The PSF array is periodic with period $L = N\lambda N_w$. Anything that lands outside $\pm L/2$ wraps around (aliasing).
- **Wavefront slope limits N.** Adjacent pupil samples are $2/N$ apart in normalized coordinates. If the wavefront changes by more than half a wave between neighbours, the phase is under-sampled. That happens when the transverse ray aberration exceeds roughly $L/2 = N\lambda N_w/2$ — equivalently, when the geometric spot does not fit inside the computed window. A spot diagram tells you immediately how big the window must be.

Rule of thumb: choose $N$ so that $N\lambda N_w/2$ is at least 2–3× the geometric spot radius (100% of rays, not RMS), then keep $Q\ge 2$. Cost is $O(M^2\log M)$ per field and wavelength.

**Polychromatic PSFs.** The image spacing scales with $\lambda$, so PSFs at different wavelengths land on different grids and must be interpolated (or computed with wavelength-dependent pupil sampling) before summing with the spectral weights. This is one reason polychromatic FFT PSFs show small numerical differences from Huygens results.

## 5. FFT PSF vs. Huygens PSF in OpticStudio

### 5.1 FFT PSF
OpticStudio traces a grid of rays (the **Sampling** setting, 32×32 up to very large grids), finds the OPD and amplitude at the exit pupil, pads the grid to twice its size and FFTs it; the output grid therefore has twice as many points per side as the sampling grid [Ansys KB "How to model the PSF"]. The relation between the sampling setting and the image-plane spacing is given in the Help file (FFT PSF section); it is *not* a fixed $\lambda N/2$ for every sampling, so read the actual spacing from the Text tab rather than assuming. **Display** size can be smaller than the computed grid (it only crops). The result is computed in a plane **perpendicular to the chief ray**, centred on the chief ray (or centroid, if chosen).

Validity conditions documented by Ansys (KA-01494 and the Community note above):
- working F/# slower than about F/1.5 (scalar theory, no vector/obliquity effects);
- the image surface is near focus for all rays (far field; no huge defocus);
- the chief ray is nearly normal to the image surface (the Community note quotes trouble beyond ~20°) — so **not** for strongly tilted sensors (Scheimpflug, Course 04 L09) or large chief-ray-angle designs measured on the image surface;
- small **pupil aberrations**: the rays must be roughly uniformly distributed in direction-cosine space at the exit pupil. **Test:** Standard Spot Diagram → Settings → check **Direction Cosines**. A regular grid means FFT is fine; a distorted grid means use Huygens [KA-01494].

If sampling is insufficient for the aberration (the phase-slope condition of §4), OpticStudio prints a warning in the analysis such as "sampling too low, data inaccurate" — increase sampling (128 → 256 → 512) until the warning and the result stabilize, or switch to Huygens.

### 5.2 Huygens PSF
The Huygens PSF traces the pupil grid, treats each ray as a small wavelet (plane or spherical, carrying its amplitude and phase), and sums the wavelets **coherently at every point of an image grid lying on the image surface itself**. You choose three things independently: **Pupil Sampling**, **Image Sampling** (number of image points per side) and **Image Delta** (image point spacing in µm). The window size is Image Delta × Image Sampling [Ansys KB "How to model the PSF"]. Because the image grid is defined directly, there is no wrap-around aliasing, polychromatic sums need no interpolation, tilted and curved image surfaces are handled, and pupil distortion does not matter. The cost is roughly (pupil points) × (image points), so it is much slower: a 128² pupil × 128² image is ~2.7×10⁸ wavelet sums per wavelength and field.

Choosing Huygens settings sensibly:
- Image Delta ≤ $\lambda N_w/2$ (Nyquist for the intensity) — e.g. ≤ 1.2 µm at 850 nm, F/2.8. Smaller deltas only interpolate.
- Image Sampling × Image Delta ≥ 2–3× the geometric spot diameter.
- Pupil Sampling high enough that the wavefront changes by < λ/2 between pupil samples (same criterion as FFT). If the PSF looks speckled or has spurious fringes, increase pupil sampling.

### 5.3 Decision table

| Situation | Use |
|---|---|
| Well-corrected, centred system, flat image normal to chief ray, F/2–F/16 | FFT (fast) — confirm once with Huygens |
| Tilted or strongly curved image surface; Scheimpflug sensors | Huygens |
| Large CRA at the image (> ~20°) or strong pupil aberration (wide-angle, fisheye) | Huygens |
| Very fast (≤ F/1.5) | Huygens (vector/polarization option), and be aware even scalar Huygens has limits |
| Large defocus / through-focus far from focus | Huygens or POP |
| Non-sequential / mixed mode systems | Huygens (FFT not available in NSC) |
| Gaussian/laser beams, near-field, propagation through apertures | POP (L07) |

If FFT and Huygens disagree in a well-sampled case, trust Huygens and find out which FFT assumption you violated.

## 6. In OpticStudio — where things are

- **Analyze → Image Quality → PSF → FFT PSF / FFT PSF Cross Section / Huygens PSF / Huygens PSF Cross Section** (exact grouping varies slightly by release; ribbon search "PSF" finds them).
- Key settings: Sampling (FFT) or Pupil/Image Sampling + Image Delta (Huygens); Wavelength (one or polychromatic); Field; Type (Linear, Log, Phase, Real, Imaginary for FFT); Normalize (peak = 1 vs. Strehl-normalized); Use Polarization; Image/centroid reference (Huygens).
- Text tab: gives the grid spacing, the window width, the reference coordinates and a **Strehl ratio** estimate. Get into the habit of reading the Text tab, not just the picture.
- **Spot Diagram** with Airy circle: the fastest sanity check of which regime you are in.
- **Encircled Energy** (diffraction FFT or Huygens variants, and geometric) — fraction of energy within radius $r$; converges to the 83.8% value at $r = 1.22\lambda N_w$ for a perfect lens. Encircled/ensquared energy is a good spec for pixelated sensors ("≥ 80% of energy inside a 2×2-pixel box").
- **Wavefront Map** and **Zernike** coefficients: the pupil function's phase — the input to the PSF.
- Merit function: diffraction-based operands exist (MTF operands in L02; search the operand list in the MFE for "Strehl" to see whether your version offers a Strehl operand and which PSF method it uses), but in practice designers optimize RMS wavefront (default merit function, L04), which is faster and smoother, and *check* Strehl/PSF afterwards.

**Common pitfalls**
1. Reading spot size in a diffraction-limited system. Look at the Airy circle first.
2. Comparing FFT PSFs at different sampling and seeing "different" peak values — the normalization and grid changed. Compare Strehl or encircled energy, not peak pixel values.
3. Using FFT PSF on a tilted sensor or very wide-angle lens.
4. Polychromatic PSF with poorly chosen wavelength weights: weights should represent source spectrum × sensor QE × filter (e.g. a narrow 850 nm LED/VCSEL band for a structured-light receiver).
5. Ignoring the working F/#: a lens at close focus has a bigger Airy disk than its nameplate F/# suggests.

## 7. Why this matters for 3D cameras

A structured-light camera images projected patterns (fringes, dots) onto a sensor with a few-µm pitch. At 850 nm and F/2.8 the Airy diameter is 5.8 µm — larger than a 3.45 µm pixel. Even a perfect lens therefore blurs a projected edge over ~2 pixels; the projector side has the same limit. Sharpness, contrast and depth precision are thus partly set by physics, and the design question becomes "how close to the diffraction limit must we get, across which field and depth range?" — the theme of L02–L03. Moving to 940 nm (better sunlight rejection) enlarges the Airy disk by 10%; opening to F/2 shrinks it but reduces depth of field (L03).

---

## Worked example

**Lens:** 25 mm focal length machine-vision lens, F/2.8 at infinity, wavelength 850 nm, 1 mW from a dot of a dot-projector collected through the pupil. Sensor pixel 3.45 µm.

1. **Airy radius:** $1.22\,\lambda N = 1.2197 \times 0.85 \times 2.8 = 2.90$ µm; diameter 5.81 µm ≈ 1.7 pixels.
2. **FWHM:** $1.029 \times 0.85 \times 2.8 = 2.45$ µm.
3. **Peak irradiance:** $I_0 = \pi P/(4\lambda^2N^2) = \pi\times10^{-3}/(4\times(0.85\times10^{-6})^2\times2.8^2) = 1.39\times10^{8}$ W/m² = 139 W/mm². A useful way to read this: the PSF's "effective area" $P/I_0 = 4\lambda^2N^2/\pi = 7.2$ µm² is *smaller* than one 3.45 µm pixel (11.9 µm²). Integrating the Airy pattern over a pixel centred on the dot gives an **ensquared energy of 75%** (0.75 mW of the 1 mW) — the remaining 25% spills into neighbours. If the dot falls on a pixel corner, the energy is shared by four pixels. (You will compute this in Task 1.)
4. **Working F/# at 0.5 m object distance:** $m \approx -f/(s-f) = -25/475 = -0.053$, so $N_w \approx 2.8\times1.053 = 2.95$ and the Airy radius grows to 3.06 µm.
5. **FFT window planning:** suppose the geometric spot at the field edge has a 100%-ray radius of 20 µm. We need $N\lambda N_w/2 \ge 2\times 20$ µm → $N \ge 80/(0.85\times 2.8) = 33.6$. Choose $N = 64$: window $64\times0.85\times2.8 = 152$ µm, and with padding $Q=2$ the spacing is 1.19 µm (≈ 0.35 pixel). In OpticStudio, start with Sampling 64×64 or 128×128 and confirm by doubling.
6. **Huygens equivalent:** Image Delta 1.0 µm, Image Sampling 128 (128 µm window), Pupil Sampling 64–128.

---

## Key takeaways
- The image of a point is the Fraunhofer pattern of the exit pupil: $\mathrm{PSF} = |\mathcal F\{A e^{ikW}\}|^2$, in natural units of $\lambda N_w$.
- Airy radius $1.22\lambda N_w$, FWHM $1.03\lambda N_w$, 83.8% of the energy in the core; always use the **working** F/#.
- Rayleigh λ/4 PV and Maréchal λ/14 RMS (Strehl ≥ 0.8) define "diffraction-limited"; balancing an aberration with defocus can cut its RMS dramatically.
- If the geometric spot is several Airy radii, trust the spot diagram; if it is comparable or smaller, only diffraction analyses (and wavefront RMS) are meaningful.
- FFT sampling: padding sets image spacing ($\lambda N_w/Q$), pupil sampling sets window size ($N\lambda N_w$); aliasing appears when the spot does not fit the window.
- FFT PSF: fast, but assumes far field, near-normal chief ray, small pupil aberration, F/# ≳ 1.5. Huygens PSF: slower but robust on tilted/curved image surfaces, large CRA and pupil distortion. When they disagree, trust a well-sampled Huygens.
- Check the Direction Cosines spot diagram before trusting an FFT result in a wide-angle lens.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Fraunhofer diffraction | Diffraction where the phase across the aperture varies linearly with position; the pattern is the Fourier transform of the aperture. Holds at the focus of a lens. |
| Fresnel diffraction | Near-field diffraction with quadratic phase across the aperture. |
| Fresnel number | $N_F = a^2/(\lambda R)$; large values mean the focal-plane pattern is Fraunhofer-like. |
| Pupil function | Complex amplitude $A\,e^{ikW}$ over the exit pupil. |
| PSF (incoherent) | Irradiance image of a point source, $|\mathcal F\{p\}|^2$. |
| Airy pattern / Airy disk | PSF of a clear circular pupil; the disk is the core inside the first zero (radius $1.22\lambda N_w$). |
| Working F/# | $1/(2n'\sin u')$ at the actual conjugates; sets the diffraction scale. |
| Strehl ratio | Peak of the aberrated PSF / peak of the perfect PSF (L03). |
| Rayleigh / Sparrow criteria | Two-point resolution limits at $1.22\lambda N_w$ and $0.947\lambda N_w$. |
| Diffraction-limited | Wavefront error small enough (≈ λ/4 PV, λ/14 RMS) that diffraction dominates image size. |
| Padding factor | Ratio of FFT array size to pupil sample count; sets PSF sampling. |
| Image Delta | Huygens PSF image-point spacing (µm). |
| Pupil aberration | Non-uniform mapping between entrance and exit pupil coordinates; breaks the FFT PSF's uniform-sampling assumption. |

## References
1. [Kenyon] I. R. Kenyon, *The Light Fantastic*, OUP 2008: §6.1–6.3, pp. 129–133; §6.7, pp. 138–139; §6.10, pp. 146–147.
2. [Geary] J. M. Geary, *Introduction to Lens Design*, 2002: §7.4.4, p. 82; §9.5, p. 101; Ch. 31, pp. 355–364.
3. Ansys Optics knowledge base, K. Moore, "How to model the PSF in OpticStudio": <https://optics.ansys.com/hc/en-us/articles/42661723066515> — FFT grid doubling, Huygens Image Delta × Image Sampling.
4. Ansys Optics knowledge base KA-01494, B. Goodwin, "Huygens PSF and FFT PSF": <https://optics.ansys.com/hc/en-us/articles/42661795535251> — FFT validity conditions and the direction-cosine test.
5. Zemax Community, "Why does the FFT PSF differ from the Huygens PSF? Which one should I trust?": <https://community.zemax.com/product-updates/why-does-the-fft-psf-differ-from-the-huygens-psf-which-one-should-i-trust-4466>
6. Zemax Community, "FFT PSF sampling too low, data inaccurate": <https://community.zemax.com/got-a-question-7/fft-psf-sampling-too-low-data-inaccurate-2099> — practical advice on the sampling warning.
7. Zemax Community, "How does OpticStudio determine the grid over which the FFT PSF is calculated?": <https://community.zemax.com/got-a-question-7/how-does-opticstudio-determine-the-grid-over-which-the-fft-psf-is-calculated-5690> — shows that image spacing does not simply halve when sampling doubles; read the Help.
