# L09 — Tasks: Thermal and environmental analysis, athermalization

> Work in `work/` inside this lesson folder (e.g. save `work/L09_T3_nir_thermal.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~6 h

## Task 1 — dn/dT from the SCHOTT model (Python)
**Goal:** Compute thermal index changes yourself and connect absolute, relative and β.
**Given / specs:** N-BK7 Sellmeier ($B$ = 1.03961212, 0.231792344, 1.01046945; $C$ = 0.00600069867, 0.0200179144, 103.560653 µm²); thermal constants $D_0 = 1.86\times10^{-6}$, $D_1 = 1.31\times10^{-8}$, $D_2 = -1.37\times10^{-11}$, $E_0 = 4.34\times10^{-7}$, $E_1 = 6.27\times10^{-10}$, $\lambda_{TK} = 0.17$ µm; $\alpha$ = 7.1×10⁻⁶/K; $dn_\text{air}/dT \approx -0.93\times10^{-6}$/K.
**Steps:**
1. Implement $\Delta n_\text{abs}(\lambda, T)$ and $dn_\text{abs}/dT$ (lecture §2.1).
2. Compute the 20–40 °C average absolute and relative dn/dT at 546.07 nm, 850 nm, 940 nm and 1060 nm. Compare with TIE-19 (relative: 3.00 at e-line, 2.40 at 1060 nm, in 10⁻⁶/K).
3. Compute $\Delta n_\text{abs}$ at 940 nm for 0 °C and 45 °C.
4. Compute $\beta$ and $G$ at 546 nm and 940 nm.
5. In OpticStudio's Materials Catalog look up the thermal constants of N-SF6 and N-PK51 (or N-FK51A); repeat steps 2 and 4. Which glass has negative β?
**Deliverable:** `work/dndt.py`, table.
**Check yourself:** e-line: absolute 1.62×10⁻⁶/K, relative ≈ 3.04×10⁻⁶/K; 940 nm: absolute 1.12×10⁻⁶/K, relative ≈ 2.52×10⁻⁶/K; 1060 nm relative ≈ 2.47×10⁻⁶/K (TIE-19: 2.40 — the small difference comes from the simplified air term). $\Delta n_\text{abs}$(940 nm) = −1.76×10⁻⁵ at 0 °C, +2.86×10⁻⁵ at 45 °C. β ≈ −1.25×10⁻⁶/K (546 nm), −2.15×10⁻⁶/K (940 nm); $G$ = 6.68×10⁻⁶/K (e-line), as in TIE-19. N-SF6: large positive dn/dT; N-PK51: negative dn/dT (≈ −6.7×10⁻⁶/K relative at e-line per TIE-19) and strongly negative β.

<details><summary>Hints / solution sketch</summary>
Use the 20 °C catalog (relative) index for $n(\lambda, T_0)$ — TIE-19 says that is accurate enough. The average over 20–40 °C is $[\Delta n(40) - \Delta n(20)]/20$, with $\Delta n(20) = 0$.
</details>

## Task 2 — Thermal defocus and an athermal mount (pen & paper / Python)
**Goal:** First-order athermal design before modeling.
**Given / specs:** single-material lens (β from Task 1 at 940 nm) focused at infinity; mounts: aluminium 23.6, stainless steel 17.3, titanium 8.6, Invar 1.2 (×10⁻⁶/K; use your supplier's values in real work).
**Steps:**
1. For f = 8 mm and 25 mm, compute the defocus rate $(\alpha_h + \beta)f$ (µm/K) for each mount and the defocus at 0 °C and 45 °C relative to 20 °C.
2. Compare with the diffraction DOF at 940 nm for F/2 and F/2.8.
3. Design a re-entrant spacer for f = 25 mm that is athermal with N-BK7 at 940 nm using aluminium (outer) and a plastic insert with CTE 110×10⁻⁶/K (assumed). Then with stainless steel (outer) + aluminium (inner). Which is practical?
4. Repeat step 1 for a PMMA lens (n = 1.485, dn/dT = −1.05×10⁻⁴/K, α = 6.5×10⁻⁵/K; typical literature values).
**Deliverable:** table and a short design note.
**Check yourself:** f = 25 mm, Al: 0.536 µm/K → +13.4 µm at 45 °C, −10.7 µm at 0 °C; DOF ±14.7 µm (F/2.8) and ±7.5 µm (F/2). Re-entrant Al + plastic: $L_A$ = 31.2 mm, $L_B$ = 6.2 mm. Steel + Al: $L_A$ = 85.1 mm (steel), $L_B$ = 60.1 mm (Al) — impractically long. PMMA: β ≈ −2.8×10⁻⁴/K → focal length grows by ≈ 56 µm for f = 8 mm over +25 K.

<details><summary>Hints / solution sketch</summary>
Re-entrant: $L_A - L_B = L$, $\alpha_AL_A - \alpha_BL_B = \alpha_\text{eff}L$ with $\alpha_\text{eff} = -\beta$ → $L_A = L(\alpha_\text{eff} - \alpha_B)/(\alpha_A - \alpha_B)$. The materials must differ strongly in CTE for a compact solution.
</details>

## Task 3 — Thermal model of the NIR receiver lens (OpticStudio)
**Goal:** Run a complete thermal analysis over 0–45 °C.
**Given / specs:** `../L08-polarization-and-coatings/work/L08_T3_nir_coated.zmx` (or the L05 lens). Barrel: aluminium (TCE 23.6) for all air spaces including the back focal distance (lens to sensor); the cover glass is mounted on the sensor (its air gap to the sensor package: aluminium too, for simplicity).
**Steps:**
1. Save as `work/L09_T3_nir_thermal.zmx`. System Explorer → Environment: 20 °C, 1 atm, tick **Adjust Index Data To Environment**. Remove F/# and focus solves (replace by fixed values).
2. Enter TCE = 23.6 for the air-space surfaces. Check that every glass has thermal data (Materials Catalog).
3. **Make Thermal**: configurations at 0, 20, 45 °C (pressure 1 atm). Inspect the MCE: `TEMP`, `PRES`, thermal pickups.
4. In each configuration record: EFL, back focal distance vs. best focus (from FFT Through Focus MTF at 83 cycles/mm, on axis and at 0.7 field), RMS wavefront, distortion at full field.
5. Compare the thermal focus shift with your first-order estimate (Task 2, f = 8 mm). Explain any difference.
6. Add `WAVE` changes for a VCSEL drifting 0.065 nm/K (938.7 / 940 / 941.6 nm centre wavelengths). Does it matter?
**Deliverable:** MCE screenshot, table per configuration, 4–6 sentences.
**Check yourself:** for an 8 mm glass lens in aluminium the thermal focus shift should be a few µm over ±20–25 K (first order: ≈ 0.17 µm/K → ≈ +4.3 µm at 45 °C), small compared with the F/2 DOF only if the lens's system β is close to the single-glass estimate; high-index/high-dn/dT glasses chosen by Hammer in L05 can change this noticeably. Distortion changes by a tiny fraction of a percent — but for a calibrated 3D camera even 0.01% at the image corner (≈0.3 µm ≈ 0.1 pixel) can matter. Wavelength drift of ±1.6 nm is negligible for focus unless the lens has strong axial colour.

<details><summary>Hints / solution sketch</summary>
If EFL does not change at all between configurations, "Adjust Index Data To Environment" is off or the glasses lack thermal data. If the hot configuration still shows perfect focus, a focus solve is re-solving the image distance in each configuration — remove it.
</details>

## Task 4 — Athermalize (OpticStudio)
**Goal:** Use the thermal MCE as an optimization target.
**Given / specs:** Task 3 model.
**Steps:**
1. **Mount route:** find the barrel TCE (applied to the lens-to-sensor air space) that makes best focus identical at 0 and 45 °C — by scanning TCE by hand or by making it variable (if allowed) with a merit function containing `CONF 1`/`CONF 3` blocks and a `DIFF` of a focus-sensitive quantity (e.g. RMS wavefront on axis, or the on-axis MTF at 83 cycles/mm) with target 0.
2. **Glass route:** keep aluminium; set glasses to Substitute (SCHOTT preferred) and run Hammer (20–30 min) with a merit function that combines image quality in all three configurations (default MF, Configuration = All). Keep EFL fixed with `EFFL` in configuration 2.
3. Compare: thermal focus shift, nominal MTF, glass list (look for fluor-/phosphate crowns), cost/manufacturability concerns.
**Deliverable:** two files `work/L09_T4_mount.zmx`, `work/L09_T4_glass.zmx`, comparison table.
**Check yourself:** the mount route should find a TCE near $-\beta_\text{system}$ (a few ×10⁻⁶/K for a glass lens — Invar/titanium territory or a compound spacer); the glass route typically pulls in a negative-dn/dT glass for a positive element and reduces the shift substantially at a small cost in nominal performance (the Ansys KB example reaches near-equal RMS wavefront at two temperatures this way).

## Task 5 — A plastic element (OpticStudio)
**Goal:** Feel the scale of plastic thermal effects.
**Given / specs:** Task 3 model; replace the weakest positive element's glass by PMMA (from the plastics catalog in OpticStudio; note the catalog's thermal data) and re-optimize nominally at 20 °C.
**Steps:**
1. Re-run Make Thermal (0/20/45 °C) and record the focus shift.
2. Try to athermalize by adding a second plastic element of opposite power (e.g. polycarbonate or a cyclo-olefin polymer — catalog names vary, e.g. Zeonex E48R in the ZEON catalog) and re-optimizing over all three temperatures.
**Deliverable:** table and a paragraph on whether a hybrid design is worth it for this camera.
**Check yourself:** the single PMMA element should increase the thermal focus shift several-fold compared with the all-glass lens (the element's β is ~100× larger than glass); a balanced positive/negative plastic pair can cancel most of it — the standard trick in mobile-phone lenses.

## Reflection questions
1. Why do lens designers use relative rather than absolute dn/dT?
2. A glass with positive dn/dT can still have negative β. Explain.
3. Why can't a focus solve stay in the model during thermal analysis of a fixed-focus camera?
4. What does a uniform-temperature MCE thermal model miss, and when do you need STAR?
5. Your 3D camera is calibrated at 25 °C. List the optical quantities that drift with temperature and would bias depth measurements, not just blur them.

<details><summary>Answers</summary>

1. Rays propagate in air whose index also changes with T and P; OpticStudio works with indices relative to the surrounding air, so the relevant change is that of $n_\text{glass}/n_\text{air}$.
2. $\beta = (dn/dT)/(n-1) - \alpha$: if expansion (which weakens curvatures) outweighs the index increase, power falls with temperature. N-BK7 at 940 nm: $2.5\times10^{-6}/0.508 = 4.9\times10^{-6} < 7.1\times10^{-6}$ → β < 0.
3. The solve would move the image surface to perfect focus in every configuration, hiding exactly the defocus you want to measure; in the real camera the sensor position is set by the mount's thermal expansion.
4. Gradients (axial/radial temperature differences), mount-induced stress and birefringence, deformation of mounts and lenses under load, and time-dependent effects. STAR (FEA-based) when heat sources sit near the optics (sensor, VCSEL, electronics), when the lens is bonded/clamped, or for precision optics where µm-level deformations matter.
5. Focal length (scale/intrinsics), principal point (decenter shifts with asymmetric mounts), distortion coefficients, baseline between camera and projector (mechanical CTE), projector pattern scale and position, and the effective wavelength (bandpass shift). Each changes the triangulation geometry → depth bias; hence temperature-aware calibration.
</details>
