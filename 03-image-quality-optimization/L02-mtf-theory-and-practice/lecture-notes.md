# L02 — MTF theory and practice

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~3 h, tasks ~5 h
> **Prerequisites:** [L01 — Diffraction and the PSF](../L01-diffraction-and-the-psf/) · **Next:** [L03 — Strehl, wavefront error and depth of focus](../L03-strehl-wavefront-error-depth-of-focus/)

## Learning objectives
- Define contrast (modulation), OTF, MTF and PTF, and explain why sinusoids are the natural test objects for an incoherent, shift-invariant imaging system.
- Derive the diffraction cutoff $\nu_c = 1/(\lambda N_w) = 2\,\text{NA}/\lambda$ from the pupil-autocorrelation picture and evaluate the diffraction-limited MTF of a circular pupil at any frequency.
- Predict qualitatively and compute numerically how defocus and spherical aberration change the MTF, including contrast reversal.
- Explain when the geometric MTF is valid and why it is pessimistic for nearly diffraction-limited lenses.
- Use OpticStudio's FFT/Huygens/Geometric MTF, Through-Focus MTF and MTF-vs-Field analyses, interpret tangential vs. sagittal curves, and choose frequencies tied to a sensor (Nyquist, Nyquist/2).
- Cascade lens and pixel MTF and judge whether a lens is matched to a sensor.

## Reading
- **Core:** [Kidger §4.5, pp. 86–90] — compact definitions; OTF as the sheared-pupil integral (eq. 4.28); the geometrical approximation (eqs. 4.29–4.31); why multiplying geometric MTF by the perfect-lens MTF is a useful correction; cutoff $2\text{NA}/\lambda$.
- **Core:** [Kenyon §7.2.1, pp. 166–169] — convolution theorem; image = object ⊗ PSF (eq. 7.24); OTF = MTF·exp(i PTF) (eq. 7.26); the "lens A vs lens B" lesson (Fig. 7.4).
- **Core:** [Geary Ch. 34, pp. 389–398] — a gentle derivation of image modulation = OTF × object modulation (eqs. 34.1–34.25), PTF as lateral shift (Fig. 34.8), tangential vs sagittal MTF for an off-axis PSF (§34.5–34.6).
- **Optional:** [Kenyon §7.4, pp. 181–182] — image formation in the spatial-frequency domain.
- **Optional (online):** Ansys KB KA-01362, "How to calculate and optimize MTF" (M. Nicholson): <https://optics.ansys.com/hc/en-us/articles/42661772706835> — FFT vs geometric vs Huygens MTF, their validity, and the MTF*/GMT*/MTH* operand families.
- **Optional (online):** Zemax Community, "Which MTF result shall I trust if FFT, geometric and Huygens MTF differ?": <https://community.zemax.com/got-a-question-7/which-mtf-result-shall-i-trust-if-fft-mtf-geometric-mtf-and-huygens-mtf-have-different-results-2134>
- **Optional (online):** Zemax Community, "Optimize for MTF directly": <https://community.zemax.com/got-a-question-7/optimize-for-mtf-directly-185>

---

## 1. Why a transfer function?

The PSF (L01) tells you how one point is imaged. Real scenes are extended: edges, fringes, textures. If the illumination is **incoherent** (light from different object points does not interfere — true for LEDs, daylight, and, effectively, for laser speckle averaged over time), image *irradiances* add, and the image is a convolution [Kenyon eq. 7.24, p. 169]:

$$
I(x,y) = \iint O(x',y')\,\mathrm{PSF}(x - m x',\, y - m y')\,dx'\,dy' ,
$$

with $m$ the magnification. Two assumptions hide here: **linearity in irradiance** (incoherence) and **shift invariance** — the PSF is the same over the region considered (an *isoplanatic patch*). Real lenses have a PSF that changes with field, so we evaluate the transfer function separately at several field points; within a small patch the convolution model holds.

Convolution becomes multiplication after Fourier transforming (convolution theorem, [Kenyon eq. 7.22]): the spectrum of the image equals the spectrum of the object times the transform of the PSF. A sinusoid is an eigenfunction of convolution: a sinusoidal object of frequency $\nu$ comes out as a sinusoid of the same frequency, with reduced amplitude and possibly shifted. That is the whole reason optical engineers talk about sine targets.

## 2. Definitions

**Modulation (contrast)** of a pattern with maximum $I_\max$ and minimum $I_\min$ [Kidger eq. 4.27, p. 86; Geary eq. 34.4]:

$$
M = \frac{I_\max - I_\min}{I_\max + I_\min}.
$$

**Optical transfer function** (normalized to 1 at zero frequency):

$$
\mathrm{OTF}(\nu_x,\nu_y) = \frac{\iint \mathrm{PSF}(x,y)\,e^{-2\pi i(\nu_x x + \nu_y y)}\,dx\,dy}{\iint \mathrm{PSF}(x,y)\,dx\,dy} = \mathrm{MTF}\;e^{\,i\,\mathrm{PTF}}.
$$

- **MTF** = $|\mathrm{OTF}|$ = image modulation / object modulation at that frequency [Kidger eq. 4.26; Geary eqs. 34.24–34.25].
- **PTF** = phase: a lateral shift of the sinusoid, $\Delta x = \mathrm{PTF}/(2\pi\nu)$. A symmetric PSF has PTF of 0 or π only; π means **contrast reversal** (bright where dark should be) — Kidger notes many lenses show this at high frequency, and you will see it in defocused systems [Kidger p. 87; Geary p. 395]. Asymmetric PSFs (coma, lateral colour) give PTF that varies with frequency — the pattern is shifted, which matters for metrology and triangulation even when MTF looks fine.
- **Line spread function (LSF)** — the image of a line, i.e. the PSF integrated along one direction. Its 1-D transform is the MTF along the perpendicular direction. **Edge spread function (ESF)** — the integral of the LSF; the slanted-edge MTF measurement (ISO 12233) differentiates a measured edge to get the LSF, then transforms it.
- **Spatial frequency** is usually given in cycles/mm (= line pairs/mm, lp/mm) **in image space**. Object-space frequency = image-space frequency × |m|. For afocal systems OpticStudio uses cycles per milliradian.

**Tangential vs. sagittal.** Off axis the PSF is not rotationally symmetric, so the MTF depends on the orientation of the sinusoid [Geary §34.5–34.6]. In this course "tangential MTF" means the modulation of a pattern whose irradiance varies along the **tangential (meridional, y) direction**; "sagittal MTF" varies along **x**. The bar orientation is perpendicular to the direction of variation. Bar-orientation conventions differ between texts and test-equipment vendors; Task 4 has you verify OpticStudio's convention on a lens with pure astigmatism, where it is unambiguous which focus is which.

**Sine vs. bar targets.** A square-wave (bar) target contains odd harmonics; its contrast response (CTF) follows Coltman's series $\mathrm{CTF}(\nu) = \tfrac{4}{\pi}[\mathrm{MTF}(\nu) - \tfrac13\mathrm{MTF}(3\nu) + \tfrac15\mathrm{MTF}(5\nu) - \dots]$. For a perfect lens at $\nu = \nu_c/4$, MTF = 0.685 while CTF = 0.811 — bar charts flatter a lens. OpticStudio's MTF analyses offer a square-wave option; specify which you mean in every requirement.

## 3. The diffraction-limited MTF and the cutoff

### 3.1 OTF as the pupil autocorrelation
Because PSF $= |\mathcal F\{p\}|^2$, and the transform of $|U|^2$ is the autocorrelation of $p$, the OTF is the **overlap integral of the pupil function with a sheared copy of itself** [Kidger eq. 4.28, Fig. 4.24]:

$$
\mathrm{OTF}(s) = \frac{1}{A}\iint_{S(s)} \exp\!\left\{\frac{2\pi i}{\lambda}\Big[W\big(x+\tfrac{s}{2},y\big) - W\big(x-\tfrac{s}{2},y\big)\Big]\right\}dx\,dy ,
$$

where $A$ is the pupil area, $s$ is the shear and $S(s)$ the overlap region of the two sheared pupils. A shear of one full pupil diameter corresponds to the frequency at which the two copies stop overlapping: the **cutoff**

$$
\nu_c = \frac{1}{\lambda N_w} = \frac{2\,\text{NA}}{\lambda}
$$

[Kidger eq. 4.32, p. 89]. Kidger's example: F/2, λ = 0.5 µm → 1000 cycles/mm. Nothing above $\nu_c$ is transmitted, whatever the lens quality; that is a hard physical limit.

Two important consequences of the autocorrelation form:
1. With $W=0$ the OTF is simply the overlap *area* of two circles — real, positive, monotonically falling.
2. Phase errors make the integrand's phasors point in different directions, so they can only reduce $|$OTF$|$ (for a uniform clear pupil): **aberrations never increase the MTF above the diffraction limit**. The diffraction-limited curve is the ceiling on every MTF plot (OpticStudio draws it when "Show Diffraction Limit" is ticked).

### 3.2 The circular pupil formula
With normalized frequency $\hat\nu = \nu/\nu_c$:

$$
\mathrm{MTF}_\text{dl}(\hat\nu) = \frac{2}{\pi}\left[\arccos\hat\nu - \hat\nu\sqrt{1-\hat\nu^2}\right],\qquad 0\le\hat\nu\le1 .
$$

| $\hat\nu$ | 0.1 | 0.2 | 0.25 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 |
|---|---|---|---|---|---|---|---|---|---|---|
| MTF | 0.873 | 0.747 | 0.685 | 0.624 | 0.505 | 0.391 | 0.285 | 0.188 | 0.104 | 0.037 |

At half cutoff the MTF is 0.39 — Kidger's "about 40%" for his F/2 example at 500 cycles/mm [Kidger p. 90]. Note the nearly linear fall at low frequency: even a perfect lens loses ~13% contrast at one tenth of cutoff.

Useful fact: the volume under the 2-D OTF equals the PSF peak (central value of the inverse transform). Therefore the **Strehl ratio = (volume under aberrated OTF)/(volume under diffraction-limited OTF)** — a high Strehl lens has an MTF close to the ceiling everywhere (L03).

## 4. Aberrations and the MTF

Numerical results for a circular pupil (computed by FFT autocorrelation, as you will in Task 2), at normalized frequencies:

| Wavefront (waves) | $\hat\nu = 0.125$ | 0.25 | 0.345 | 0.5 | 0.75 |
|---|---|---|---|---|---|
| Perfect | 0.841 | 0.685 | 0.570 | 0.391 | 0.144 |
| Defocus $W_{020}=0.25$ (λ/4 PV) | 0.794 | 0.576 | 0.444 | 0.288 | 0.122 |
| Defocus $W_{020}=0.5$ | 0.661 | 0.318 | 0.174 | 0.085 | 0.070 |
| Defocus $W_{020}=1.0$ | 0.269 | −0.068 | −0.056 | −0.021 | −0.010 |
| Spherical $W_{040}=0.25$ at paraxial focus | 0.779 | 0.579 | 0.460 | 0.296 | 0.109 |
| Same, balanced with $W_{020}=-0.25$ | 0.834 | 0.674 | 0.561 | 0.386 | 0.142 |

(Negative values = OTF real part with contrast reversal; the MTF is the absolute value.)

Lessons:
- **Mid frequencies are the most sensitive.** A quarter wave of defocus costs 22% of the contrast at $\hat\nu=0.345$ but only 6% at $\hat\nu = 0.125$.
- **One wave of defocus** produces contrast reversal from about $\hat\nu\approx0.2$ upward — the classic "spurious resolution" seen when a camera is badly out of focus: the bars are there, but with black and white swapped.
- **Balancing pays.** Spherical aberration balanced with defocus is almost invisible in the MTF.
- **Low vs high frequency trade-offs are real.** Kenyon's Fig. 7.4 shows two lenses whose MTF curves cross: one better for coarse contrast, the other for fine detail [Kenyon p. 169]. A single number (Strehl, resolution limit) cannot capture this — which is why specifications list MTF at several frequencies.

### 4.1 Geometric MTF
For large aberrations the PSF approaches the spot diagram (L01 §3.2). The OTF can then be computed directly from ray intercepts [Kidger eqs. 4.29–4.31]:

$$
\mathrm{OTF}_\text{geo}(\nu) \approx \frac{1}{N_\text{rays}}\sum_\text{rays} w_j\,e^{-2\pi i\,\nu\,\delta y_j},
$$

the Fourier transform of the ray-density distribution ($\delta y_j$ = transverse aberration of ray $j$, $w_j$ its weight). For a uniform defocus blur disk of radius $r$ this gives $2J_1(2\pi\nu r)/(2\pi\nu r)$. Kidger recommends multiplying by the diffraction-limited MTF so that the result is right in both limits (large aberration and zero aberration); in between it is **pessimistic** [Kidger §4.5.3, p. 89]. Example (defocus, geometric × diffraction vs. true diffraction MTF):

| Defocus $W_{020}$ | $\hat\nu = 0.125$ geo×dl / true | $\hat\nu = 0.25$ geo×dl / true |
|---|---|---|
| 0.5 λ | 0.607 / 0.661 | 0.124 / 0.318 |
| 1.0 λ | 0.152 / 0.269 | −0.046 / −0.068 |

Rule (consistent with the Ansys guidance): use geometric MTF when the wavefront error is many waves (early design, global search, rough tolerancing); use FFT or Huygens MTF once the system is within a few waves. Geary suggests switching to MTF-based criteria once the PV wavefront error is around one wave [Geary §34.5, p. 396].

## 5. MTF across focus and field

**Through-focus MTF**: MTF at one or a few fixed frequencies plotted against image-plane shift. It shows
- where best focus is for each field and orientation (T and S peaks are separated by astigmatism; peaks move with field curvature),
- the **depth of focus** at a contrast threshold (L03 gives the diffraction theory: ±2λN² for λ/4 defocus),
- asymmetry from spherical aberration (MTF falls faster on one side).

**MTF vs field**: MTF at fixed frequencies (e.g. Nyquist/4, /2, Nyquist) plotted against field height, T and S separately. This is the standard way camera lenses are specified and compared. A good camera lens has T and S curves close together (low astigmatism) and a gentle roll-off to the corner.

**Choosing the image plane** is a compromise: the plane that maximizes centre MTF is rarely the one that maximizes a field-weighted average. OpticStudio's merit function (L04) handles this automatically if field weights express what matters.

## 6. System MTF: lens × sensor × everything else

Independent blur processes convolve, so their MTFs multiply:

$$
\mathrm{MTF}_\text{system} = \mathrm{MTF}_\text{lens}\times \mathrm{MTF}_\text{pixel}\times \mathrm{MTF}_\text{motion}\times\cdots
$$

For a square pixel of width $p$ with 100% fill factor, $\mathrm{MTF}_\text{pixel}(\nu) = |\mathrm{sinc}(\pi\nu p)|$ — equal to $2/\pi = 0.637$ at the **Nyquist frequency** $\nu_N = 1/(2p)$. Real pixels with microlenses and crosstalk are somewhat worse (Course 04 L01). Above Nyquist the sensor **aliases**: detail is not lost but folded into false low-frequency patterns (moiré). A lens whose MTF is still high above Nyquist will alias; one whose MTF is very low at Nyquist wastes pixels.

Rules of thumb for machine-vision lenses (orientation, not law):
- Specify lens MTF at $\nu_N/2$ and $\nu_N$ (and sometimes $\nu_N/4$), polychromatic over the actual source spectrum, at centre, 0.7 field and corner.
- A "well-matched" lens has MTF of roughly 0.5–0.7 at $\nu_N/2$ and 0.2–0.4 at $\nu_N$ on axis, at the working F/#.
- If the diffraction-limited MTF at $\nu_N$ is already low (small pixels, high F/#, NIR), no amount of lens design helps: change F/# or pixel size.

### 6.1 Why it matters for structured light
In phase-shifting fringe projection the depth noise is roughly proportional to (intensity noise)/(fringe modulation). Fringe modulation in the camera image is (projector MTF at the projected fringe frequency) × (camera lens MTF at the imaged fringe frequency) × (pixel MTF) × (defocus MTF if the surface is away from best focus). Every 2× loss of MTF at the fringe frequency costs about 2× in depth noise. The same holds for dot or speckle patterns: contrast at the pattern frequency drives correlation accuracy. Through-focus MTF at the pattern frequency is thus a direct predictor of how depth precision falls off across the working range.

## 7. In OpticStudio

- **Analyze → MTF** (group name varies slightly by release): **FFT MTF**, **FFT Through Focus MTF**, **FFT MTF vs Field**, **FFT MTF Map**, **FFT Surface MTF**; **Huygens MTF** and **Huygens Through Focus MTF**; **Geometric MTF**, **Geometric MTF vs Field**, **Geometric Through Focus MTF**. Ribbon search "MTF" lists them all.
- Key settings: Sampling (pupil grid; same aliasing logic as the FFT PSF, L01), Maximum Frequency (set it to ~1.2× the highest frequency you care about, not to $\nu_c$, so the plot is readable), Wavelength (polychromatic uses the System Explorer weights — set them to source × sensor response), Field, Show Diffraction Limit, Type (Modulation / Real / Imaginary / Phase / Square Wave), Use Polarization. Geometric MTF has an option to multiply by the diffraction limit (Kidger's correction; the exact label varies — "Scale by Diffraction Limit" in many versions).
- **Validity** is the same as for the PSFs: FFT MTF assumes the FFT-PSF conditions (far field, small pupil aberrations, near-normal chief ray); Huygens MTF works for tilted/curved image surfaces and when the chief ray cannot be traced, but is slower; geometric MTF is for many-wave aberrations [Ansys KA-01362]. If FFT and Huygens disagree, check Huygens sampling (Image Delta × Image Sampling must cover the PSF) before believing either.
- **Operands** (Merit Function Editor): `MTFT`, `MTFS`, `MTFA` (diffraction FFT MTF, tangential/sagittal/average), `GMTT`, `GMTS`, `GMTA` (geometric), `MTHT`, `MTHS`, `MTHA` (Huygens). Each takes sampling, wavelength, field and frequency arguments; check the operand help for the exact argument order in your version. Use them with *inequality* constructs (e.g. via `OPGT`, L04) or as targets of 1.0 with low weight. They are slow and noisy far from the diffraction limit, so the standard workflow is: optimize RMS spot → RMS wavefront → and only at the end add MTF targets or use the Optimization Wizard's **Contrast** criterion (Moore–Elliott contrast optimization), which Ansys recommends over raw MTF operands [Community "Optimize for MTF directly"].
- **Pitfalls:** forgetting that the frequency axis is image-space; comparing polychromatic and monochromatic curves; evaluating at the infinity F/# instead of the real working distance; ignoring PTF for metrology; trusting a single-field MTF.

---

## Worked example — matching a lens to a sensor

**System:** 850 nm, working F/2.8, sensor pixel 3.45 µm (100% fill assumed).

1. **Cutoff:** $\nu_c = 1/(0.85\times10^{-3}\,\text{mm}\times 2.8) = 420$ cycles/mm.
2. **Nyquist:** $\nu_N = 1/(2\times 3.45\times10^{-3}) = 145$ cycles/mm → $\hat\nu = 145/420 = 0.345$.
3. **Diffraction-limited lens MTF at Nyquist:** 0.570. **Pixel MTF:** $2/\pi = 0.637$. **Best possible system MTF at Nyquist:** $0.570\times0.637 = 0.363$.
4. **At Nyquist/2** (72.5 cycles/mm, $\hat\nu = 0.172$): lens 0.782; pixel $|\sin(\pi\nu p)/(\pi\nu p)|$ with $\pi\nu p = \pi/4$ gives 0.900; system 0.704.
5. **Defocus budget:** a quarter wave of defocus ($\Delta z = 8N^2\cdot\lambda/4 = 2\lambda N^2 = 2\times0.85\times2.8^2 = 13.3$ µm) lowers the lens MTF at Nyquist from 0.570 to 0.444 (table in §4). With a 13.3 µm focus error the system MTF at Nyquist is $0.444\times0.637 = 0.28$. This is why active alignment of the sensor (Course 06 L07) is common for fast lenses with small pixels.
6. **Interpretation:** a real lens at F/2.8 might reach 0.4–0.5 lens MTF at Nyquist on axis, i.e. 70–90% of the diffraction ceiling. Going to F/4 would lower the ceiling at Nyquist to 0.40 ($\hat\nu = 0.493$) — sharper corners perhaps, but a hard loss on axis.

---

## Key takeaways
- MTF = contrast transfer of sinusoids; OTF = MTF·e^{iPTF} = normalized Fourier transform of the PSF. It assumes incoherent light and an isoplanatic patch.
- The OTF is the autocorrelation of the pupil function; cutoff $\nu_c = 1/(\lambda N_w) = 2\text{NA}/\lambda$. The diffraction-limited curve is a ceiling (0.39 at half cutoff).
- Aberrations hit mid frequencies first; one wave of defocus causes contrast reversal; balanced aberrations are nearly harmless.
- Geometric MTF is correct for big aberrations, pessimistic near the diffraction limit; switch to FFT/Huygens MTF when within a few waves.
- Always look at T and S, across field, and through focus; specify frequencies tied to the sensor (Nyquist/2, Nyquist) and the actual spectrum and conjugates.
- System MTF is a product; the pixel alone gives 0.64 at Nyquist. For structured light, MTF at the pattern frequency through the depth range drives depth noise.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Modulation / contrast | $(I_\max - I_\min)/(I_\max + I_\min)$ |
| OTF | Normalized Fourier transform of the PSF; complex |
| MTF | Modulus of the OTF; contrast ratio image/object vs. frequency |
| PTF | Phase of the OTF; lateral shift of sinusoids; π = contrast reversal |
| LSF / ESF | Line / edge spread functions; 1-D routes to the MTF |
| Cutoff frequency | $\nu_c = 1/(\lambda N_w)$; no transfer above it |
| Isoplanatic patch | Region over which the PSF is (nearly) constant |
| Tangential / sagittal MTF | Modulation for patterns varying along y (meridional) / along x |
| Geometric MTF | OTF from ray-intercept distribution; valid for large aberrations |
| Through-focus MTF | MTF at fixed frequency vs. focus shift |
| Nyquist frequency | $1/(2p)$ for pixel pitch $p$; highest frequency sampled without aliasing |
| CTF / square-wave response | Contrast for bar targets; related to MTF by Coltman's series |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE PM92, 2002: §4.5, pp. 86–90.
2. [Kenyon] I. R. Kenyon, *The Light Fantastic*, 2008: §7.2.1, pp. 166–169; §7.4, pp. 181–182.
3. [Geary] J. M. Geary, *Introduction to Lens Design*, 2002: Ch. 34, pp. 389–398.
4. Ansys Optics KB KA-01362, M. Nicholson, "How to calculate and optimize MTF": <https://optics.ansys.com/hc/en-us/articles/42661772706835>
5. Zemax Community, "Which MTF result shall I trust…": <https://community.zemax.com/got-a-question-7/which-mtf-result-shall-i-trust-if-fft-mtf-geometric-mtf-and-huygens-mtf-have-different-results-2134>
6. Zemax Community, "Optimize for MTF directly": <https://community.zemax.com/got-a-question-7/optimize-for-mtf-directly-185>
7. ZOSPy API docs, FFT Through Focus MTF wrapper (useful later in Course 07): <https://zospy.readthedocs.io/en/latest/api/zospy.analyses.mtf.fft_through_focus_mtf.html>
