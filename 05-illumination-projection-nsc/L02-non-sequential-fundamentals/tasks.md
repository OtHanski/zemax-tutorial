# L02 — Tasks: Non-Sequential Fundamentals

> Work in `work/` inside this lesson folder (e.g. save `work/L02_T2_singlet_nsc.zmx`). Commit your designs, scripts and a short `work/notes.md` with answers.
> Estimated time: ~4–5 h

## Task 1 — Ray budgets and splitting trees (pen & paper / Python)
**Goal:** Plan ray counts before you press "Trace".
**Steps:**
1. A uniformly illuminated Detector Rectangle with 10 × 10 pixels receives all the rays of a source. What relative pixel noise do you expect for 10⁴, 10⁵ and 10⁶ analysis rays? Repeat for 100 × 100 pixels.
2. You need 2 % pixel noise on a 64 × 40 uniformity map, and only 30 % of the source rays reach the detector. How many analysis rays?
3. A ray passes through 4 uncoated lenses (8 interfaces) with ray splitting on. If every interface splits, how many segments can one launched ray generate? Why is the real number much smaller?
4. With Minimum Relative Ray Intensity = 10⁻³ and $R = 4\ \%$ per interface, how many successive reflections can a ghost branch survive before it is terminated?
**Deliverable:** answers in `notes.md`.
**Check yourself:** (1) 10 %, 3.2 %, 1.0 % for 10 × 10; 32 %, 10 %, 3.2 % for 100 × 100. (2) $k = 2500$ hits/pixel × 2560 pixels / 0.3 ≈ 2.1 × 10⁷ rays. (3) $2^{9}-1 = 511$. (4) Two: $0.04^2 = 1.6\times10^{-3}$ survives, $0.04^3 = 6.4\times10^{-5}$ does not.

<details><summary>Hints</summary>

(3) The tree is pruned because many branches leave the system (miss everything), TIR does not split, and branches below the intensity threshold are killed. (4) That is why a 10⁻³ threshold is fine for throughput but useless for a stray-light study of 3rd-order ghosts.

</details>

## Task 2 — Your first NSC system: singlet, source, detector (OpticStudio)
**Goal:** Build the worked example of the lecture and verify the energy bookkeeping.
**Given / specs:** Units mm; source units W; analysis units W/mm² or W/cm² (note which); wavelength 0.85 µm. Objects exactly as in the lecture worked example: Source Ellipse Ø 20 mm collimated, 1 W at Z = 0; Standard Lens N-BK7, Z = 10, R₁ = 50.98 mm, R₂ = 0 (flat), thickness 5 mm, clear semi-diameters 12.5 mm; Detector Rectangle `ABSORB`, half widths 0.5 mm, 101 × 101 pixels, at Z = 111.69 mm.
**Steps:**
1. Build the system with 20 layout rays; check the NSC 3D Layout and Shaded Model. Name each object in the Comment column. Save as `work/L02_T2_singlet_nsc.zmx`.
2. Make the detector's Z position a **pickup** (or use *Ref Object* = 2) so that it stays 101.69 mm behind the lens front vertex if you move the lens.
3. Trace 10⁶ analysis rays three times: (a) polarization off, no splitting; (b) polarization on, no splitting; (c) polarization on, splitting on. Record Total Power, Peak Irradiance and Total Hits from the Detector Viewer.
4. For case (b), move the detector in 0.2 mm steps from Z = 110.7 to 111.9 mm and record peak irradiance. Where is the best focus (by peak irradiance)? Compare with the paraxial focus and with the marginal-ray focus (110.56 mm absolute).
5. Show the detector as a cross-section and estimate the spot diameter at the paraxial focus.
**Deliverable:** `.zmx`, a table of the three energy cases and the focus scan.
**Check yourself:** (a) ≈ 1.000 W, (b) ≈ 0.918–0.919 W, (c) ≈ 0.919 W plus a trace of ghost light. Spot at paraxial focus ≈ 0.2 mm diameter (bright core with a halo — spherical aberration); the peak-irradiance best focus lies between the marginal and paraxial foci, roughly 0.5–0.8 mm in front of the paraxial focus. Peak irradiance is noisy: two runs with different random seeds can differ by several per cent.

<details><summary>Hints / what good looks like</summary>

- If case (a) shows < 1 W, rays are missing the lens or the detector (check clear semi-diameters and detector size).
- If the Detector Viewer reports power ~10⁴ times off, you mixed cm² and m² in the irradiance units — the *Total Power* value in W does not depend on area units, which is why it is the first number to check.
- The pickup: in the detector's Z Position cell, use the solve type *Pickup* from object 2's Z position with offset 101.69, or set Ref Object = 2 and Z = 101.69.

</details>

## Task 3 — Where does the other 8 % go? Back-reflections, ZRD and filter strings (OpticStudio)
**Goal:** Use ray splitting, a transparent detector, a Ray Database and filter strings to account for every watt.
**Given / specs:** Start from `work/L02_T2_singlet_nsc.zmx`. Add object 4: Detector Rectangle, **material blank (transparent)**, Z = 5 mm, half widths 20 mm, 50 × 50 pixels. Save as `work/L02_T3_ghosts.zmx`.
**Steps:**
1. Trace 10⁶ rays with polarization and splitting on, *Save Rays* to `L02_T3.ZRD`.
2. Look at detector 4 without filter. Why does it show ≈ 1.08 W, more than the source power?
3. Replay the ZRD into the Detector Viewer for detector 4 with the filter `G2`, then `!G2`. Record total power for each.
4. Use `X_GHOST(0,2)` on detector 3. What does it show and how much power?
5. Set *Minimum Relative Ray Intensity* (System Explorer → Non-Sequential) to 0.05 and re-trace. What happens to detector 4, and what does the lost-energy report say?
6. Open the Ray Database Viewer and find one ray that reflected off the flat back face, returned through the front face and hit detector 4. Write down its segment list.
**Deliverable:** table of powers, explanation, one annotated ray history.
**Check yourself:** `!G2` on detector 4 ≈ 1.000 W (the forward beam crossing the transparent detector); `G2` ≈ 0.079 W ($R + (1-R)^2R/(1-R^2)$ = 0.0793 at normal incidence, slightly higher in practice because the curved face sees up to 11° incidence). The front-face reflection diverges (convex mirror, $f = -R_1/2 = -25.5$ mm) to ≈ Ø 24 mm at the detector, so the 40 mm detector catches it all. With a 5 % threshold, all reflected children (≈ 4 %) are killed: detector 4 shows only the forward 1 W and ≈ 0.08 W appears as threshold loss.

<details><summary>Hints</summary>

- A transparent detector counts every ray segment that crosses it, in both directions. That is useful (one detector sees forward and back light) and dangerous (double counting).
- `G2` selects rays ghost-reflected from object 2 (the lens); with splitting on, every reflected child from either lens face carries the flag.
- The double-bounce ghost on detector 3 carries ≈ $R^2 \approx 0.17$ % of the power, but at the 1 mm detector it is spread out (it focuses at a different distance), so `X_GHOST(0,2)` on detector 3 shows a tiny, smooth background — on the order of 10⁻⁵–10⁻⁴ W, depending on where its focus falls.

</details>

## Task 4 — Monte-Carlo noise, measured (OpticStudio + Python)
**Goal:** Verify $\sigma/\mu \approx 1/\sqrt{k}$ and learn to export detector data.
**Given / specs:** New NSC file `work/L02_T4_noise.zmx`: Source Rectangle 5 × 5 mm half widths, collimated, 1 W; Detector Rectangle `ABSORB` at Z = 10 mm, 5 × 5 mm half widths.
**Steps:**
1. For detector resolutions 10 × 10 and 100 × 100, trace 10⁴, 10⁵, 10⁶ (and 10⁷ for 100 × 100) rays.
2. Export each detector result as text (Detector Viewer → Text tab → save, or *Export*), and compute mean and standard deviation of the pixel values in Python (ignore edge pixels if partially lit).
3. Plot measured σ/μ against $1/\sqrt{k}$, with $k$ = rays per pixel.
4. Repeat one case with the source's *Sampling* set to Sobol (if your source offers it). What changes?
**Deliverable:** script `work/noise.py`, plot, conclusion.
**Check yourself:** points lie on the 1/√k line (10 %, 3.2 %, 1 % for 10 × 10). Sobol sampling on a uniform collimated source gives noticeably *lower* noise than 1/√k, because quasi-random points cover the area more evenly than random ones.

## Task 5 — Reading filter strings (pen & paper)
**Goal:** Fluency with the filter grammar. Objects: 1 source, 2 lens A, 3 lens B, 4 housing (absorbing), 5 detector.
For each string, describe in words what it selects on detector 5:
1. `H4`
2. `!H4 & !G2 & !G3`
3. `X_GHOST(0,2)`
4. `G3 & !G2`
5. `~001002003005`
6. `X_HIT(2,2)`
<details><summary>Answers</summary>

1. Rays that touched the housing at some point (stray light via the housing; with no scatter defined, that is housing reflections only if the housing is not ABSORB — otherwise nothing reaches 5).
2. "Clean" signal: never hit the housing and never ghost-reflected from either lens.
3. Second-generation ghosts from any object: the classic two-reflection ghost images.
4. Ghosts that reflected off lens B but were not ghost-reflected by lens A.
5. Rays that went source 1 → lens A → lens B → detector 5 directly and stopped there (the nominal path; a trailing `#` would also allow rays that continue beyond 5).
6. Rays that hit lens A exactly twice — e.g. a ghost bouncing between lens B and lens A, or simply the two faces? Careful: `X_HIT(n,b)` counts hits on the object; a nominal ray already hits lens A's front and back faces, so check in the Ray Database Viewer how your version counts faces before relying on this flag. This is exactly why you should test filters on a toy model.

</details>

## Stretch task — Make (and fix) a geometry error
Put a Source Ellipse so that it straddles the front face of the lens in Task 2 (half inside, half outside). Trace with *Ignore Errors* off; read the error message, use *Setup → Create Error Ray*, inspect the resulting Source Ray in the layout and in the Ray Database Viewer, then fix the model (move the source out, or use *Inside Of*).

## Reflection questions
1. Why can't the sequential Lens Data Editor model a light pipe with an unknown number of wall reflections?
2. You have 10⁷ rays to spend. When would you use a 500 × 500 detector anyway?
3. Why is "Total Power" on a detector much more trustworthy than "Peak Irradiance"?
4. When is it acceptable to run with polarization off?

<details><summary>Answers</summary>

1. Sequential tracing requires every ray to visit a fixed list of surfaces once each; each wall bounce would be a separate "surface", and different rays need different numbers and orders of bounces.
2. When you need to see fine structure (e.g. images of the LED die, fringe edges of a projected pattern) and accept noise per pixel — then judge uniformity on a re-binned or smoothed version; or when the light is concentrated into a few pixels anyway.
3. Total power averages over all hits (relative error ~1/√N_total); peak irradiance is a single noisy pixel and the maximum of many noisy values is biased high.
4. For geometry and layout checks, first-order throughput estimates with AR-coated optics (where Fresnel losses are small), and early illumination uniformity studies — never for ghost/stray-light work or absolute efficiency claims.

</details>
