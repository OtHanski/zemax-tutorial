# L01 — Tasks: Diffraction and the point spread function

> Work in `work/` inside this lesson folder (e.g. save `work/L01_T3_paraxial_f100.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — Airy numbers and pixels (Python)
**Goal:** Derive the Airy-pattern constants yourself and connect them to a real sensor.
**Given / specs:** $\mathrm{PSF}(v) = [2J_1(v)/v]^2$, $v = \pi r/(\lambda N)$; encircled energy $EE(v) = 1 - J_0^2(v) - J_1^2(v)$. Sensor pixel 3.45 µm; λ = 0.85 µm; N = 2.8.
**Steps:**
1. With `scipy.special.jn_zeros(1, 3)` find the first three zeros of $J_1$ and convert them to units of $\lambda N$.
2. Evaluate the encircled energy at those zeros. Find the FWHM with `brentq`.
3. Two Airy patterns separated by $1.22\lambda N$: compute the midpoint intensity relative to the peaks (Rayleigh dip). Find the separation at which the dip vanishes (Sparrow).
4. Numerically integrate the Airy PSF over a 3.45 µm pixel (a) centred on the PSF, (b) with the PSF at a pixel corner. Express as fractions of the total power.
5. Repeat step 4 for N = 2.0 and N = 4.0 and for λ = 0.94 µm. Tabulate.
**Deliverable:** `work/airy.py`, a table in `notes.md`.
**Check yourself:** zeros at 1.220, 2.233, 3.238 λN; EE 83.8%, 91.0%, 93.8%; FWHM 1.029 λN; Rayleigh dip 73.5%; Sparrow 0.947 λN. At 0.85 µm, F/2.8: centred pixel 75.0%, corner placement 21.7% per pixel (four pixels share ~87%).

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
from scipy.special import j0, j1, jn_zeros
from scipy.optimize import brentq
z = jn_zeros(1, 3); print(z/np.pi)                    # radii in lambda*N
print(1 - j0(z)**2 - j1(z)**2)                        # encircled energy
v = brentq(lambda v: (2*j1(v)/v)**2 - 0.5, 0.1, 3); print(2*v/np.pi)  # FWHM
lamN, p = 0.85*2.8, 3.45
x = np.linspace(-p/2, p/2, 801); X, Y = np.meshgrid(x, x)
v = np.pi*np.hypot(X, Y)/lamN + 1e-12
I = (2*j1(v)/v)**2
print(I.mean()*p*p * np.pi/(4*lamN**2))              # normalized so total power = 1
```
The normalization $\int\!\!\int [2J_1(v)/v]^2\,dA = 4\lambda^2N^2/\pi$ follows from $I_0 = \pi P/(4\lambda^2N^2)$. A faster lens puts more energy into one pixel (diffraction shrinks), but only until aberrations take over — the subject of the rest of this course.
</details>

## Task 2 — Your own FFT PSF (Python)
**Goal:** Build the FFT-PSF engine OpticStudio uses, with explicit control of sampling, and see aliasing happen.
**Given / specs:** circular pupil, uniform amplitude; wavefront in waves $W(\rho) = W_{020}\rho^2 + W_{040}\rho^4$.
**Steps:**
1. Write `fft_psf(N, Q, W)` that samples the pupil with N points across its diameter, embeds it in an $M = QN$ array, applies $e^{2\pi i W}$, FFTs and returns $|U|^2$, the image spacing ($\lambda N/Q$ in units of $\lambda N$, i.e. $1/Q$) and the Strehl ratio (peak of aberrated / peak of perfect, computed with the same grid).
2. Verify on the perfect pupil (N = 64, Q = 8) that the first minimum is near 1.22 (it will land on the nearest grid point, ≈1.25).
3. Compute the Strehl ratio for: (a) $W_{020} = 0.25$; (b) $W_{040} = 0.25$ at paraxial focus; (c) $W_{040} = 0.25$, $W_{020} = -0.25$; (d) $W_{040} = 1.0$, $W_{020} = -1.0$; (e) $W_{020}=1.0$. Also compute the RMS wavefront of each analytically or numerically and the estimate $\exp[-(2\pi\sigma)^2]$.
4. Plot log-scale PSFs for (b) on both sides of focus ($W_{020} = \pm0.5$) — the star-test asymmetry.
5. **Aliasing experiment:** take $W_{020} = 8$ waves (strong defocus). Compute with N = 32, Q = 2 and with N = 256, Q = 2. Compare the window size with the geometric blur radius ($= 2N_w\cdot 2W_{020}\lambda$ … derive it from $\varepsilon = -2N\,\partial W/\partial\rho$ evaluated at $\rho = 1$) and explain what you see in the N = 32 result.
**Deliverable:** `work/fftpsf.py`, plots, a table of Strehl values.
**Check yourself:** (a) σ = 0.0722 λ, S ≈ 0.811 (exact 0.8106 = $[\sin(\pi/4)/(\pi/4)]^2$); (b) σ = 0.0745 λ, S ≈ 0.802; (c) σ = 0.0186 λ, S ≈ 0.987; (d) σ = 0.0745 λ, S ≈ 0.802 — same as (b): *balanced* 1-wave spherical is as good as *unbalanced* quarter-wave spherical; (e) central intensity exactly 0 (peak ≈ 0.05 off-centre). For 8 waves of defocus the geometric blur radius is $2N\cdot 2\cdot 8\lambda = 32\lambda N$, i.e. the full window of an N = 32 grid ($\pm16\lambda N$): the PSF wraps around and the result is garbage.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
def fft_psf(N=64, Q=4, W=lambda r: 0*r):
    M = N*Q
    x = (np.arange(M) - M//2) / (N/2)          # normalized pupil coordinate, pupil radius = 1
    X, Y = np.meshgrid(x, x); R = np.hypot(X, Y); P = (R <= 1).astype(float)
    E = P*np.exp(2j*np.pi*W(R))
    I  = abs(np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(E))))**2
    I0 = abs(np.fft.fft2(P))**2
    return I, 1/Q, I.max()/I0.max()
```
Image spacing: the DFT frequency step is $1/(M\,\delta)$ with pupil step $\delta = D/N$; multiply by $\lambda R$ to get $\lambda R N/(MD) = \lambda N_w/Q$. RMS of $\rho^4-\rho^2$: $\sqrt{1/180} = 0.0745$; of $\rho^4$ alone: $\sqrt{4/45}=0.298$, so 0.25 waves gives 0.0745 too. Transverse aberration: $\varepsilon_y = -\frac{R}{a}\,\partial W/\partial\rho = -2N_w\,\partial W/\partial\rho$ (W in length units).
</details>

## Task 3 — Perfect lens, defocus and the Airy disk (OpticStudio)
**Goal:** Calibrate your eye on OpticStudio's diffraction analyses with a system whose answer you know exactly.
**Given / specs:** Paraxial surface, focal length 100 mm, stop on the paraxial surface, EPD 20 mm (F/5), object at infinity, single field 0°, single wavelength 0.5876 µm. Image distance 100 mm.
**Steps:**
1. Build the system (Surface type *Paraxial* on the stop, focal length 100). Save as `work/L01_T3_paraxial_f100.zmx`.
2. Open the Standard Spot Diagram with the Airy disk shown; note the Airy radius reported. Open FFT PSF, FFT PSF Cross Section, Huygens PSF, Huygens PSF Cross Section and Diffraction Encircled Energy.
3. Read the Text tab of each PSF: grid spacing, window width, Strehl. Change FFT sampling 64→128→256 and record how spacing and width change.
4. Change the image distance by +0.0294 mm. Record the Strehl ratio from FFT and Huygens PSF; look at the cross-section.
5. Change it to +0.1175 mm (one wave of $W_{020}$). Look at the PSF centre.
**Deliverable:** table of Airy radius, Strehl (in focus, λ/4 and 1 λ defocus) from both methods; two sentences on how the sampling setting changed spacing/width.
**Check yourself:** Airy radius 3.58 µm (= 1.22 × 0.5876 × 5). Encircled energy ≈ 84% at r ≈ 3.6 µm. Defocus 0.0294 mm is $W_{020} = \Delta z/(8N^2) = 0.25\lambda$ → Strehl ≈ 0.81. At 0.1175 mm the centre is (nearly) dark and the PSF is a ring.

<details><summary>Hints / solution sketch</summary>

If the Strehl at best focus is not 1.000, check that there is only one wavelength and that the paraxial surface is the stop. The FFT spacing will not simply halve when you double sampling (see the Community thread in the lecture references) — that is why you read the Text tab. Huygens results should match FFT to within ~1% here; if not, increase Huygens pupil sampling.
</details>

## Task 4 — A real lens: the achromat (OpticStudio)
**Goal:** See the geometric-to-diffraction transition on a real design.
**Given / specs:** Your cemented N-BK7/N-SF5 achromat from Course 02 (`../../02-aberrations-classical-design/L06-chromatic-aberration-and-achromats/work/L06_T2_achromat.zmx`, f = 100 mm, F/5, fields 0°, 0.7°, 1°, F-d-C).
**Steps:**
1. Polychromatic spot diagram with Airy circle at all fields. Classify each field as geometric/transition/diffraction-limited (lecture §3.2 table).
2. Polychromatic FFT PSF and Huygens PSF at 0° and 1°. Record Strehl.
3. Monochromatic (d only) Strehl at 0°. Explain the difference to the polychromatic value (secondary spectrum, Course 02 L07).
4. Run the Direction Cosines spot-diagram test. Is FFT valid here?
**Deliverable:** table (field × {RMS spot, Airy radius, Strehl poly, Strehl mono}), 3–5 sentences of interpretation.
**Check yourself:** on axis the RMS spot should be comparable with or smaller than the 3.6 µm Airy radius; the d-only Strehl should be high (≳0.8) and the polychromatic Strehl lower because the F and C foci differ slightly from d (secondary spectrum ≈ f/2000–f/2500 for a classic achromat). The direction-cosine grid is regular → FFT is valid.

<details><summary>Hints / solution sketch</summary>
If your achromat was optimized for RMS spot, re-optimize a copy for RMS wavefront (Optimization Wizard → Wavefront) and compare Strehl — this is a preview of L03/L04.
</details>

## Task 5 — When FFT fails: a tilted sensor (OpticStudio)
**Goal:** Demonstrate the FFT PSF's chief-ray-normal assumption.
**Given / specs:** Paraxial lens f = 25 mm, EPD 8.93 mm (F/2.8), λ = 0.85 µm, on-axis field only. Insert a Coordinate Break before the image surface with Tilt About X = 30° (and the opposite break is not needed for the image surface).
**Steps:**
1. Without tilt: compute FFT and Huygens PSF (Huygens: Pupil Sampling 64, Image Sampling 128, Image Delta 0.5 µm). Note FWHM in x and y from the cross sections.
2. With 30° tilt: repeat. Compare the y-FWHM (in the tilt direction) between the two methods.
3. Run the Direction Cosines spot diagram for both cases.
**Deliverable:** `work/L01_T5_tilt30.zmx`, the four FWHM values, a short explanation.
**Check yourself:** untilted FWHM ≈ 1.029 × 0.85 × 2.8 = 2.45 µm in both methods. With the tilt, Huygens (computed on the tilted surface) shows the PSF stretched along y by about $1/\cos 30° = 1.15$ (≈ 2.8 µm), while FFT (computed normal to the chief ray) still reports ≈ 2.45 µm.

<details><summary>Hints / solution sketch</summary>
The FFT answer is not "wrong" — it answers a different question (the PSF in the plane perpendicular to the beam). The sensor, however, lies in the tilted plane, so Huygens is the relevant one. Scheimpflug camera designs (Course 04 L09) need this every time.
</details>

## Stretch task — Sampling convergence on an aberrated singlet
Open `../../01-foundations/L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx` (100 mm F/5 equiconvex N-BK7, many waves of spherical). Compute on-axis FFT PSF at sampling 32, 64, 128, 256, 512 and Huygens PSF at increasing pupil sampling. Plot Strehl and the 50% encircled-energy radius vs sampling. At which sampling does the "sampling too low" warning disappear, and does that coincide with the result converging? Compare with the geometric spot diagram (the PSF should resemble it).

## Reflection questions
1. Why is the pattern at the focus of a lens a Fraunhofer pattern, even though the image plane is only a few cm from the lens?
2. A lens has an RMS spot radius of 1 µm and an Airy radius of 3 µm. Your colleague says "the spot is 1 µm, so it resolves 1 µm features". What is wrong?
3. You change a camera lens from F/2.8 to F/4 at 850 nm. By what factor does the Airy radius change, and what happens to the peak irradiance for the same scene radiance?
4. Name three situations in which you would not trust the FFT PSF, and say what you would use instead.
5. Why does refocusing reduce the RMS wavefront error of spherical aberration by a factor of 4, but not that of coma?

<details><summary>Answers</summary>

1. The converging spherical wave cancels the quadratic (Fresnel) phase across the pupil; observation at the image of the source is equivalent to the far field (Kenyon §6.10). Only the residual aberration $W$ remains, as a phase in the Fourier integral.
2. In the diffraction-limited regime the image of a point is the Airy pattern (≈6 µm diameter core), not the geometric spot. Resolution is set by $\lambda N$ (Rayleigh ≈ 3 µm separation), and the MTF (L02) tells you the contrast at each frequency.
3. Airy radius scales with N: ×4/2.8 = 1.43. The image-plane irradiance from an extended scene falls as $1/N^2$ (×0.49); the peak of a point image's PSF, for the same collected power, falls as $1/N^2$ too — and the collected power also falls by $1/N^2$, so the PSF peak of a point source drops to ~0.24×.
4. Tilted/curved image surfaces (Scheimpflug), large chief-ray angles or strong pupil aberrations (wide-angle), very fast beams (≤ F/1.5), heavy defocus/near field, NSC systems. Use Huygens PSF, or POP for beams/near-field.
5. Defocus ($\rho^2$) has a similar radial shape to $\rho^4$ and can cancel much of it (σ from 0.298 to 0.0745 per unit $W_{040}$). Coma ($\rho^3\cos\theta$) has different angular dependence; only tilt ($\rho\cos\theta$, i.e. a lateral shift/centroid reference) helps it, reducing σ from $1/\sqrt8$ to $1/\sqrt{72}$ per unit $W_{131}$.
</details>
