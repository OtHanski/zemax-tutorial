# L02 — Tasks: MTF theory and practice

> Work in `work/` inside this lesson folder (e.g. save `work/L02_T3_paraxial_f25.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — MTF from the pupil (Python)
**Goal:** Compute the OTF two ways and build intuition for aberrated MTFs.
**Given / specs:** circular pupil; wavefront $W(\rho) = W_{020}\rho^2 + W_{040}\rho^4$ in waves.
**Steps:**
1. Implement the analytic $\mathrm{MTF}_\text{dl}(\hat\nu)$ and tabulate it at $\hat\nu = 0.1, 0.2, …, 0.9$.
2. Extend your L01 `fft_psf` code: OTF = FFT of the PSF, normalized at zero frequency. Show that a shift of one pupil diameter in the autocorrelation corresponds to $\hat\nu = 1$, and that the perfect-pupil OTF matches the analytic curve to < 0.005.
3. Compute MTF curves for $W_{020} = 0, 0.25, 0.5, 1.0$ and for $W_{040} = 0.25$ with $W_{020} = 0$ and $-0.25$. Plot the *real part* of the OTF so that contrast reversals appear as negative values.
4. **Through-focus:** at $\hat\nu = 0.345$, compute MTF for $W_{020}$ from −0.6 to +0.6 waves. Convert $W_{020}$ to image shift $\Delta z = 8N^2 W_{020}\lambda$ for λ = 0.85 µm, N = 2.8. Find the focus range over which MTF ≥ 50% of its peak.
5. **Geometric approximation:** for pure defocus, the geometric OTF is $2J_1(x)/x$ with $x = 2\pi\nu r$, blur radius $r = 4N W_{020}\lambda$. Compare geometric × diffraction-limited with the true diffraction result for $W_{020} = 0.5, 1, 2, 4$ waves at $\hat\nu = 0.125$ and 0.25. When does the approximation become good?
**Deliverable:** `work/mtf_pupil.py`, plots, short commentary in `notes.md`.
**Check yourself:** values in the lecture tables (§3.2 and §4). Through-focus at $\hat\nu = 0.345$: 0.571 at focus, 0.444 at $W_{020}=\pm0.25$, ≈0.285 (half) at $\pm0.4$ waves → ±21 µm at F/2.8, 850 nm. Geometric × dl at 0.5 λ, $\hat\nu = 0.25$: 0.12 vs. true 0.32 — badly pessimistic; the two converge (in magnitude, not in every ripple) for several waves of defocus.

<details><summary>Hints / solution sketch</summary>

```python
def otf_profile(W, N=128, Q=4):
    M = N*Q; x = (np.arange(M)-M//2)/(N/2); X, Y = np.meshgrid(x, x)
    R = np.hypot(X, Y); P = (R <= 1)*1.0
    I = abs(np.fft.fft2(P*np.exp(2j*np.pi*W(R))))**2
    O = np.fft.fftshift(np.fft.fft2(I)); O /= O[M//2, M//2]
    return np.real(O[M//2, M//2:M//2+N+1])   # index k  ->  nu_hat = k/N
```
The FFT of the PSF array is (circularly) the autocorrelation of the padded pupil, so the frequency index counts pupil-sample shifts: N samples = one pupil diameter = cutoff. Use Q ≥ 2 to avoid the autocorrelation wrapping onto itself.
</details>

## Task 2 — Lens × pixel (Python / pen & paper)
**Goal:** Know the ceiling for a lens–sensor pair before designing anything.
**Given / specs:** λ = 0.85 µm; pixel pitch 3.45 µm and 2.2 µm (100% fill); F/2.0, 2.8, 4.0.
**Steps:**
1. For each combination compute $\nu_c$, $\nu_N$, $\hat\nu_N$, diffraction-limited lens MTF at Nyquist, pixel MTF at Nyquist, and the product.
2. Repeat at $\nu_N/2$.
3. Which combinations are "diffraction-starved" (system MTF at Nyquist < 0.15 even with a perfect lens)?
**Deliverable:** table in `notes.md`.
**Check yourself:** 3.45 µm: F/2 → lens 0.690, system 0.439; F/2.8 → 0.570/0.363; F/4 → 0.399/0.254. 2.2 µm: F/2 → 0.521/0.331; F/2.8 → 0.347/0.221; F/4 → 0.126/0.080 (starved).

<details><summary>Hints / solution sketch</summary>
Pixel MTF at Nyquist is always $2/\pi = 0.637$ for a 100%-fill square pixel. Small pixels in the NIR need fast lenses — and fast lenses have small depth of focus (L03), which is the central tension of compact 3D-camera optics.
</details>

## Task 3 — Calibrate OpticStudio's MTF (OpticStudio)
**Goal:** Reproduce the analytic numbers so you trust the tool's conventions.
**Given / specs:** Paraxial surface (stop) f = 25 mm, EPD 8.9286 mm (F/2.8), object at infinity, field 0°, λ = 0.85 µm.
**Steps:**
1. Save as `work/L02_T3_paraxial_f25.zmx`. Open FFT MTF with max frequency 450 cycles/mm, Show Diffraction Limit on. Read values at 72.5, 145 and 210 cycles/mm from the Text tab.
2. Open Huygens MTF and Geometric MTF at the same settings. Explain the Geometric MTF result for a perfect lens (with and without the diffraction-limit scaling option).
3. FFT Through Focus MTF at 145 cycles/mm, ±0.03 mm, 21 steps. Find the ±50% points.
**Deliverable:** table of OpticStudio vs. Python values.
**Check yourself:** cutoff 420 cycles/mm; MTF 0.782 at 72.5, 0.570 at 145, 0.391 at 210; through-focus half-peak at about ±21 µm. The unscaled geometric MTF of a perfect lens is 1.0 at all frequencies (all rays hit one point) — a reminder that geometric MTF ignores diffraction unless you scale it.

<details><summary>Hints / solution sketch</summary>
If your values are off by a few %, check that the sampling is ≥ 64×64 and that the system has only one wavelength. If the cutoff is wrong, you probably set the aperture as Image Space F/# vs Entrance Pupil Diameter inconsistently.
</details>

## Task 4 — MTF of the Cooke triplet across field and focus (OpticStudio)
**Goal:** Read real MTF plots like a lens designer.
**Given / specs:** your optimized triplet `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx` (50 mm, F/4, ±20°, F-d-C). Assume a 3.45 µm pixel sensor → Nyquist 145 cycles/mm.
**Steps:**
1. Polychromatic FFT MTF to 160 cycles/mm at fields 0°, 14°, 20°. Record T and S at 36, 72.5 and 145 cycles/mm.
2. FFT MTF vs Field at 36 and 72.5 cycles/mm.
3. FFT Through Focus MTF at 72.5 cycles/mm for the 14° and 20° fields. Note the focus shift of the T and S peaks.
4. Open Field Curvature/Distortion. Compare the T–S separation at 20° with the separation of the T and S peaks in the through-focus plot. Use this to confirm which curve OpticStudio calls "T".
5. Compare FFT MTF and Geometric MTF at 20°. Which regime is the triplet in (compare RMS spot with the Airy radius 1.22 × 0.5876 × 4 = 2.87 µm)?
6. Decide whether moving the image plane by ±0.02 mm would improve the *field-averaged* MTF at 72.5 cycles/mm.
**Deliverable:** table + 5–8 sentence interpretation; screenshots or exported text in `work/`.
**Check yourself:** diffraction cutoff ≈ 425 cycles/mm (d-light, F/4). Expect on-axis MTF at 72.5 cycles/mm well below the diffraction ceiling (0.78 at $\hat\nu = 0.17$) — typical classic-triplet values are 0.3–0.6, worse at the field edge, with T and S diverging at 20°. The T and S through-focus peaks should be separated by roughly the T–S distance read from the field-curvature plot at that field.

<details><summary>Hints / solution sketch</summary>
If the triplet is clearly geometric-aberration-limited (RMS spot several times the Airy radius), FFT and Geometric MTF will roughly agree at low frequency; near the diffraction limit (on axis) the geometric curve without scaling will be too optimistic and with scaling slightly pessimistic.
</details>

## Task 5 — Fringe contrast through depth (analysis)
**Goal:** Connect MTF to structured-light performance.
**Given / specs:** camera lens = the paraxial F/2.8 lens of Task 3; sinusoidal fringe pattern imaged with a period of 12 pixels of 3.45 µm.
**Steps:**
1. Compute the fringe frequency on the sensor (cycles/mm) and $\hat\nu$.
2. Using your Task 1 code, compute fringe modulation vs. image-side defocus from −50 to +50 µm.
3. If depth noise ∝ 1/modulation, by what factor does noise rise at ±30 µm image defocus?
4. Using Newton's longitudinal magnification $\Delta z' \approx m^2\Delta z$ with $m = -0.05$ (object at ~0.5 m), convert ±30 µm to an object-space depth range.
**Deliverable:** plot and three numbers in `notes.md`.
**Check yourself:** period 41.4 µm → 24.2 cycles/mm, $\hat\nu = 0.0575$. The MTF at this low frequency is very tolerant: 0.861 at ±30 µm vs 0.927 in focus (93% retained), so depth noise rises by only ≈1.08×. $\Delta z = 30\,\mu\text{m}/0.0025 = 12$ mm in object space — so a fixed-focus design must accept much more defocus than that for a 0.3–1 m working range; this is where large-defocus (geometric) behaviour and depth of field (Course 04 L02) take over.

<details><summary>Hints / solution sketch</summary>
At ±30 µm, $W_{020} = 30/(8\cdot2.8^2\cdot0.85) = 0.563$ waves. Compute the OTF at $\hat\nu = 0.0575$ for that defocus with N = 256 to resolve the low frequency (index ≈ 15 at N = 256). Low-frequency patterns survive defocus much better than high-frequency ones — one reason projected patterns are coarse relative to the pixel pitch.
</details>

## Stretch task — Slanted edge in Python
Simulate an image of a slanted edge (5° tilt) through the defocused PSF of Task 1 ($W_{020}=0.25$), sample it with 3.45 µm pixels, then implement the slanted-edge method: project pixels onto the edge normal into 4× oversampled bins, differentiate the ESF to get the LSF, FFT to get the MTF. Compare with lens × pixel MTF from Task 2. (This is how the lens MTF is measured in production — Course 06 L07.)

## Reflection questions
1. Why can the MTF of an aberrated lens never exceed the diffraction-limited MTF (for a clear, uniformly illuminated pupil)?
2. A lens has MTF 0.6 at 30 cycles/mm and 0.1 at 120 cycles/mm; another has 0.5 and 0.25. Which do you choose for (a) a 5 µm pixel machine-vision camera, (b) a 2 µm pixel camera?
3. What does a negative real OTF mean physically? Where have you seen it?
4. Why does OpticStudio's geometric MTF show 1.0 at all frequencies for a perfect lens, and why is "geometric × diffraction-limited" pessimistic for nearly perfect lenses?
5. Why should the PTF be checked in a triangulation-based 3D camera even if the MTF is acceptable?

<details><summary>Answers</summary>

1. The OTF is the normalized overlap integral of the pupil with its sheared copy; aberrations only add phase factors of unit modulus inside that integral, and $|\int e^{i\phi}| \le \int 1$.
2. Nyquist is 100 cycles/mm for 5 µm and 250 cycles/mm for 2 µm. (a) The relevant band is ≤ 100 cycles/mm; the second lens is better at 100 (≈0.28 vs ≈0.2 by interpolation) but the first gives more contrast at 30 — for edge detection on coarse features the first may be preferable; at Nyquist/2 (50 cycles/mm) they are similar. (b) Clearly the second lens (higher MTF at high frequency). The point: compare at the frequencies your sensor and task use.
3. Contrast reversal: bright and dark bars swapped (PTF = π). Seen in strongly defocused images (spurious resolution) — the 1-wave defocus curve in Task 1.
4. Geometric MTF transforms the ray intercept distribution; with zero aberration all rays coincide, a delta function, whose transform is 1. Multiplying by the diffraction MTF fixes the zero-aberration limit, but for small aberrations diffraction and aberration do not blur independently (the wave effects partly "smooth" the aberration), so the product double-counts.
5. A frequency-dependent PTF shifts the imaged pattern laterally (and differently for different frequencies and fields), which biases the measured phase/position of fringes or dots → systematic depth errors, not just noise. Calibration absorbs some of it, but only if it is stable with temperature and focus.
</details>
