# L01 — Tasks: Radiometry, Photometry and Étendue

> Work in `work/` inside this lesson folder (e.g. save `work/L01_T3_lambertian.zmx`). Commit your scripts, designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — A radiometry calculator (Python)
**Goal:** Build a small, reusable `work/radiometry.py` that you will keep extending through this course (the capstone L09 uses it for its light budget).
**Given / specs:** Use the worked example of the lecture (100 lm white LED; 1 W, 850 nm, 1 × 1 mm Lambertian die; 0.3-inch 1280 × 720 DMD, 5.4 µm pitch, ±17° tilt).
**Steps:**
1. Write functions `lambert_I0(P)`, `lambert_L(P, A)`, `irradiance_on_plane(I0, d, theta)` ($E = I_0\cos^4\theta/d^2$), `cone_fraction(theta)` ($\sin^2\theta$), `etendue(A, theta, n=1)` ($\pi n^2A\sin^2\theta$), `photons_per_s(P, lam)`.
2. Reproduce every number in Parts A–C of the worked example.
3. Add a function `electrons_per_pixel(E_scene, rho, tau, N, pixel, t, eta, lam)` implementing §5.6 and evaluate: a projector puts **0.3 W at 850 nm** uniformly onto a **1.0 m × 0.6 m** scene area; the scene is a Lambertian grey card with $\rho = 0.5$; the camera lens has $\tau = 0.9$ and F/2.8; pixel pitch 3.45 µm (fill factor 100 %), exposure 10 ms, QE 0.30 at 850 nm.
**Deliverable:** script + printed table in `notes.md`.
**Check yourself:** scene irradiance 0.50 W/m²; camera image irradiance ≈ 7.2 × 10⁻³ W/m²; ≈ 1.1 × 10³ electrons per pixel per 10 ms.

<details><summary>Solution sketch</summary>

$E_{\text{scene}} = 0.3/0.6 = 0.5$ W/m². $L = \rho E/\pi$; $E' = \pi L\tau/(4N^2) = 0.5\cdot0.5\cdot0.9/(4\cdot 2.8^2) = 7.17\times10^{-3}$ W/m². Pixel area $1.19\times10^{-11}$ m², so 8.54 × 10⁻¹⁶ J in 10 ms; photon energy at 850 nm is 2.34 × 10⁻¹⁹ J → 3650 photons → 1096 e⁻ at QE 0.3. Shot-noise-limited SNR ≈ √1096 ≈ 33. Keep this number: in the capstone you will ask how much of it survives the real illumination efficiency, and how it compares to ambient light.

</details>

## Task 2 — Cosine-power sources (pen & paper, then Python)
**Goal:** Understand the "Cosine Exponent" parameter that many OpticStudio NSC sources have.
**Given / specs:** A source has intensity $I(\theta) = I_0\cos^n\theta$ (forward hemisphere only).
**Steps:**
1. Show that the total flux is $\Phi = 2\pi I_0/(n+1)$, so $I_0 = (n+1)\Phi/(2\pi)$.
2. Show that the fraction of flux inside a cone of half-angle $\theta$ is $1-\cos^{n+1}\theta$. Check that $n = 1$ reproduces the Lambertian $\sin^2\theta$.
3. Find the half-angle at half-maximum intensity, $\theta_{1/2} = \arccos(0.5^{1/n})$.
4. Tabulate $\theta_{1/2}$ and the fraction inside 30° for $n$ = 1, 2, 5, 10, 30.
5. An LED datasheet says "viewing angle 2θ½ = 60°". Which $n$ models it (to first order)?
**Deliverable:** derivation + table in `notes.md`.
**Check yourself:**

| $n$ | $\theta_{1/2}$ | fraction in 30° | $I_0/\Phi$ (sr⁻¹) |
|---|---|---|---|
| 1 | 60.0° | 25.0 % | 0.318 |
| 2 | 45.0° | 35.1 % | 0.477 |
| 5 | 29.5° | 57.8 % | 0.955 |
| 10 | 21.1° | 79.5 % | 1.751 |
| 30 | 12.3° | 98.8 % | 4.934 |

Viewing angle 60° → $\theta_{1/2} = 30°$ → $n = \ln 0.5/\ln\cos 30° = 4.8$ (≈ 5).

<details><summary>Hints</summary>

$\Phi = \int_0^{2\pi}\!\int_0^{\pi/2} I_0\cos^n\theta\sin\theta\,d\theta\,d\phi = 2\pi I_0\left[-\tfrac{\cos^{n+1}\theta}{n+1}\right]_0^{\pi/2}$. Real LED patterns are rarely exactly $\cos^n$ (the "bat-wing" shapes of some packages are not even monotonic); that is why L03 uses measured source files.

</details>

## Task 3 — Check a Lambertian source numerically (OpticStudio)
**Goal:** First contact with the Non-Sequential Component Editor, used purely as a radiometry calculator. (L02 explains everything properly; here just follow the recipe.)
**Given / specs:** Units mm, source units Watts, wavelength 0.85 µm.
**Steps:**
1. *File → New*, then switch to non-sequential mode (Setup tab → the *Sequential/Non-Sequential* mode switch; OpticStudio asks whether to convert — answer yes for a blank file). Save as `work/L01_T3_lambertian.zmx`.
2. In System Explorer set *Units → Source Units* = Watts, *Analysis Units* = W/m² if offered (otherwise note that the default is W/cm²; 1 W/cm² = 10⁴ W/m²). Wavelength 0.85 µm.
3. Object 1: **Source Rectangle**, X/Y Half Width 0.5 mm, Power 1 W, *Cosine Exponent* 1, # Layout Rays 50, # Analysis Rays 1 000 000.
4. Object 2: **Detector Rectangle** at Z = 500 mm, X/Y Half Width 200 mm, 101 × 101 pixels.
5. Run a ray trace (Analyze → *Ray Trace* control, clear detectors, trace) and open the *Detector Viewer* (Analyze → Detector Viewer). Read the peak irradiance, the total power on the detector and the irradiance at the edge-centre and the corner pixels.
6. Repeat with Cosine Exponent 5.
**Deliverable:** screenshot-free table in `notes.md`: expected vs. simulated values.
**Check yourself (Lambertian, n = 1):** on-axis 1.27 W/m² (1.27 × 10⁻⁴ W/cm²); edge-centre (21.8°) 0.95 W/m²; corner (29.5°) 0.73 W/m²; total power on detector 0.168 W (16.8 %). Simulated values should agree within the Monte-Carlo noise: with 10⁶ rays on 101² pixels only ~17 rays land in an average pixel, so expect ±20–25 % pixel-to-pixel noise — that is why you should compare the *total* power (very precise) and smooth or re-bin for the pixel values.

<details><summary>Hints / solution sketch</summary>

The fraction of a Lambertian emitter landing on a centred rectangle of half-widths $X, Y$ at distance $d$ has a closed form (with $a = X/d$, $b = Y/d$): $F = \frac{2}{\pi}\left[\frac{a}{\sqrt{1+a^2}}\arctan\frac{b}{\sqrt{1+a^2}} + \frac{b}{\sqrt{1+b^2}}\arctan\frac{a}{\sqrt{1+b^2}}\right]$, which gives 0.1682 for $a = b = 0.4$ — it matches a brute-force numerical integration of $E = I_0 d^2/r^4$ over the detector. If the irradiance is off by exactly 10⁴, check the analysis units (cm² vs m²). If it is ≈ 2× too high, check that the source emits into one hemisphere only.

</details>

## Task 4 — Étendue matching for a small DMD (pen & paper)
**Goal:** Decide what LED die size a small DMD can use.
**Given / specs:** A 0.2-inch-class DMD with 854 × 480 mirrors at 5.4 µm pitch, ±17° tilt (TI DLP2010-class; confirm against the datasheet of the device you actually use). Illumination native F/# $= 1/(2\sin 17°)$.
**Steps:**
1. Active area, diagonal (inches) and DMD étendue.
2. Largest bare Lambertian (flat, emitting into air) die area the DMD can accept; side of a square die.
3. Best-case étendue efficiency for square dies of 0.5, 1.0 and 1.5 mm side.
4. The 1 mm die is now encapsulated under a hemispherical silicone dome ($n = 1.5$) that extracts more light from the chip. What is the étendue of the light leaving the dome, assuming all of it is extracted into the hemisphere? Explain using $G = \pi n^2 A$ and the fact that a dome magnifies the die by $n$.
5. If the condenser only collects ±40° from the bare 1 mm die, what étendue actually reaches the DMD and what fraction of the LED flux is that?
**Deliverable:** numbers + two sentences on whether "a bigger LED" helps.
**Check yourself:** 4.612 × 2.592 mm = 11.95 mm², 0.21″ diagonal; $G_{\text{DMD}} = 3.21$ mm² sr; max die area 1.02 mm² (≈ 1.01 mm square); efficiencies 100 %, 100 %, 45 %; dome: 7.07 mm² sr (2.2× the DMD); ±40° cone: 1.30 mm² sr, 41 % of the flux.

<details><summary>Solution sketch</summary>

$G = \pi\cdot 11.95\cdot\sin^2 17° = 3.21$ mm² sr. $A_{\max} = G/\pi = 1.02$ mm². For a 1.5 mm die, $G_{\text{LED}} = 7.07$, efficiency $3.21/7.07 = 0.454$. The dome: inside silicone the die étendue is $\pi n^2 A = 7.07$ mm² sr (the dome lets light escape that would otherwise be trapped by TIR at a flat chip/air interface); in air you see a die magnified by $n$, area $n^2A$, emitting into $\pi$ — same 7.07. So the domed 1 mm LED is étendue-equivalent to a 1.5 mm bare die: more total flux, but the DMD can only take 45 % of it. ±40°: $\pi\cdot1\cdot\sin^2 40° = 1.30$ mm² sr; flux fraction $\sin^2 40° = 41.3$ %.

</details>

## Task 5 — Photometry sanity checks (pen & paper)
**Goal:** Fluency with lm/cd/lx/nit and with the NIR "zero lumen" trap.
**Steps:**
1. A green LED emits 0.5 W at 555 nm. Luminous flux? If it is Lambertian with a 1 mm² die, what is its luminance in cd/m²?
2. The same 0.5 W at 650 nm, where $V = 0.107$ (CIE 1924 photopic value). Luminous flux?
3. A machine-vision datasheet says an illuminator produces "500 lx at 1 m" from 850 nm LEDs. What is wrong with this specification, and what would you ask the supplier for instead?
4. Kenyon quotes high-pressure sodium lamps at ~120 lm/W wall-plug. What is the upper bound on lm/W for *any* source, and why can a real white source never reach it?
**Check yourself:** 341.5 lm; 1.09 × 10⁸ cd/m²; 36.5 lm; (3) lux is meaningless at 850 nm — ask for W/m² (or W/sr and the angular pattern) at the stated wavelength; (4) 683 lm/W, only for monochromatic 555 nm light; any spread of wavelengths has $V < 1$ somewhere.

<details><summary>Solution</summary>

1. $683 \times 0.5 = 341.5$ lm; $I_0 = 341.5/\pi = 108.7$ cd; $L = 108.7/10^{-6} = 1.09\times10^8$ cd/m².
2. $683 \times 0.107 \times 0.5 = 36.5$ lm.
3. Either the "lux" is a mislabelled radiometric number or it refers to a visible pilot LED; insist on radiometric units.
4. 683 lm/W at 555 nm (definition of the lumen). Broadband white sources are typically limited to roughly 250–350 lm/W of *optical* power depending on colour rendering — an upper bound, not a typical LED efficacy.

</details>

## Stretch task — Measure étendue in OpticStudio
Put the 1 × 1 mm Lambertian source of Task 3 in front of a circular aperture (Annulus or a Detector Rectangle with a hole is awkward — use an *Annulus* object at Z = 10 mm with inner radius chosen so that the aperture subtends ±20° from the source centre) and a large Detector Rectangle behind it. Compare the transmitted power with $\sin^2 20° = 11.7$ % of the source power. Then shift the aperture laterally by 2 mm and explain why the fraction changes (the "uniform cone at every point" assumption behind $G = \pi A\sin^2\theta$ fails for finite geometry).

## Reflection questions
1. Why does an LED die look equally bright whether you look at it from 0° or 60°, although its intensity at 60° is half?
2. A colleague proposes putting a 3 × 3 mm LED behind your 0.3″ DMD "to get 9× more light". Give the étendue argument in two sentences, and say what *would* give more light on the scene.
3. Why is étendue sometimes called the optical analogue of entropy?
4. Where in an imaging lens does the Lagrange invariant appear, and why is $G = \pi^2H^2$ a natural link between the camera lenses of Course 04 and the projectors of this course?

<details><summary>Answers</summary>

1. Radiance is constant: the projected area you see shrinks as $\cos\theta$ in the same proportion as the intensity, so the ratio (brightness) is unchanged.
2. The DMD accepts only 7.2 mm² sr; the 3 × 3 die has 28 mm² sr, so at best 26 % of its flux can be used — ≈ 2.3× the 1 mm² LED's flux only if the radiance is equal, and in practice larger dies often have *lower* radiance (current density, heating). More light needs higher radiance (better LED bin, higher current density, laser source) or a larger DMD.
3. Like entropy it can stay constant (ideal lossless, aberration-free optics) or grow (scatter, diffusers, aberrations, mismatched shapes), but never decrease without throwing light away.
4. $H$ is invariant through any paraxial system and equals $nu h$ at the image; étendue is the 2-D, finite-angle generalisation, so the same number limits both how much light a camera collects from a scene and how much a projector can deliver from its DMD.

</details>
