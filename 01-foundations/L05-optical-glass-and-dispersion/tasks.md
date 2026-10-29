# L05 — Tasks: Optical Glass and Dispersion

> Work in `work/` inside this lesson folder (e.g. save `work/L05_T3_singlet_NSF6.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Your own glass calculator and glass map (Python)
**Goal:** Compute dispersion quantities from Sellmeier coefficients and draw a mini glass map.
**Given / specs:** SCHOTT Sellmeier coefficients ($n^2 - 1 = \sum B_i\lambda^2/(\lambda^2 - C_i)$, λ in µm):

| Glass | $B_1$ | $B_2$ | $B_3$ | $C_1$ | $C_2$ | $C_3$ |
|---|---|---|---|---|---|---|
| N-BK7 | 1.03961212 | 0.231792344 | 1.01046945 | 0.00600069867 | 0.0200179144 | 103.560653 |
| N-SK16 | 1.34317774 | 0.241144399 | 0.994317969 | 0.00704687339 | 0.0229005 | 92.7508526 |
| N-LAK9 | 1.46231905 | 0.344399589 | 1.15508372 | 0.00724270156 | 0.0243353131 | 85.4686868 |
| F2 | 1.34533359 | 0.209073176 | 0.937357162 | 0.00997743871 | 0.0470450767 | 111.886764 |
| N-SF5 | 1.52481889 | 0.187085527 | 1.42729015 | 0.011254756 | 0.0588995392 | 129.141675 |
| N-SF6 | 1.77931763 | 0.338149866 | 2.08734474 | 0.0133714182 | 0.0617533621 | 174.01759 |

**Steps:**
1. Write `n(glass, lam)`. Compute $n_F, n_d, n_C, n_g$, $V_d$, $P_{g,F}$, and Kidger's $p = (n_F - n_d)/(n_F - n_C)$ for each glass.
2. Plot $n_d$ vs. $V_d$ (with the $V_d$ axis reversed, as on catalogue maps) and $P_{g,F}$ vs. $V_d$. Fit a straight line through the $P_{g,F}$ points — your "normal line".
3. Compute an "NIR Abbe number" $V_{850} = (n_{850} - 1)/(n_{800} - n_{900})$ for each glass and compare to $V_d$.
4. Optional: open a catalogue file from your OpticStudio installation (`SCHOTT.AGF` in the Glasscat folder — it is plain text). Parse the `NM` lines (name, formula number, $n_d$, $V_d$, …) and `CD` lines (coefficients) to make a full SCHOTT glass map.
**Deliverable:** `work/glass.py`, two plots, a table in notes.
**Check yourself:** $(n_d, V_d)$: N-BK7 (1.51680, 64.17), N-SK16 (1.62041, 60.32), N-LAK9 (1.69100, 54.71), F2 (1.62004, 36.37), N-SF5 (1.67271, 32.25), N-SF6 (1.80518, 25.36). $P_{g,F}$ from 0.5349 (N-BK7) to 0.6158 (N-SF6). $V_{850}$: ≈ 287 for N-BK7, ≈ 181 for N-SF5, ≈ 152 for N-SF6.

<details><summary>Hints</summary>

In the AGF format, the `NM` line holds: name, dispersion formula code, MIL number, $n_d$, $V_d$, … and the following `CD` line holds the dispersion coefficients. Formula code 2 is Sellmeier 1 (the form above). Check a few glasses against the Materials Catalog in OpticStudio.

</details>

## Task 2 — Axial colour and achromat powers (pen & paper)
**Goal:** Use the Abbe number for quick chromatic estimates.
**Steps:**
1. Estimate the F–C focal spread of a 100 mm thin singlet in N-BK7, N-SK16 and N-SF6.
2. For the N-BK7 singlet at F/5, estimate the geometric blur diameter (from colour only) at the plane midway between the F and C foci.
3. Compute the focal lengths of the two elements of a thin achromatic doublet with $f = 100$ mm using N-BK7 ($V = 64.17$) and F2 ($V = 36.37$). Which element is positive?
4. Repeat 3 with N-BK7 + N-SF5 ($V = 32.25$). Which pair needs weaker element powers, and why does that matter?
**Check yourself:** 1.56, 1.66, 3.94 mm; ≈ 0.15 mm; F2 pair: $f_1 = 43.3$ mm, $f_2 = -76.4$ mm; N-SF5 pair: $f_1 = 49.7$ mm, $f_2 = -99.0$ mm.

<details><summary>Solution</summary>

1. $f/V$: 100/64.17 = 1.56; 100/60.32 = 1.66; 100/25.36 = 3.94 mm.
2. Marginal-ray slope 1/(2N) = 0.1; at Δf/2 = 0.78 mm from each focus the ray height is 0.078 mm → blur diameter ≈ 0.156 mm.
3. $f_1 = f(V_1 - V_2)/V_1 = 100 \times 27.80/64.17 = 43.3$ mm (positive crown); $f_2 = -f(V_1 - V_2)/V_2 = -76.4$ mm (negative flint).
4. $f_1 = 100 \times 31.92/64.17 = 49.7$ mm, $f_2 = -99.0$ mm. The larger $V$-difference gives weaker elements → shallower curves → less higher-order aberration. Rule: pick crown/flint pairs with a large ΔV.

</details>

## Task 3 — Chromatic analysis of the singlet in OpticStudio
**Goal:** Learn OpticStudio's chromatic plots and see glass choice trade-offs.
**Given / specs:** `../L01-light-rays-and-opticstudio-tour/work/L01_singlet_f100.zmx` with an M-solve on the back thickness (paraxial focus at d).
**Steps:**
1. Analyze → Prescription Data: find the index table; confirm $n$ at F, d, C.
2. Open **Chromatic Focal Shift** and **Longitudinal Aberration** (Analyze tab, Aberrations group — or search the ribbon). Read the F-to-C focal shift.
3. Save a copy as `work/L05_T3_singlet_NSF6.zmx`, change both surfaces' glass to N-SF6 and the radii to ±160.14 mm (keeps EFL = 100.0 mm with t = 4). Repeat step 2. Also try N-SK16 with radii ±123.31 mm.
4. For each glass compare: on-axis monochromatic (d only) and polychromatic RMS spot after Quick Focus.
**Deliverable:** table in notes.
**Check yourself:** F–C back-focus spread: N-BK7 ≈ 1.54 mm, N-SK16 ≈ 1.63 mm, N-SF6 ≈ 3.85 mm. From a Python ray trace (on-axis, best focus, ~10 % tolerance): RMS radius mono / poly ≈ 27/54 µm (N-BK7), 23/54 µm (N-SK16), 19/118 µm (N-SF6). High index reduces spherical aberration (flatter curves) but high dispersion doubles the polychromatic blur.

## Task 4 — Shopping for glass (OpticStudio)
**Goal:** Use the material tools like a professional.
**Steps:**
1. Libraries → Materials Catalog. For N-BK7, N-SK16, N-LAK9, F2, N-SF5, N-SF6, record: status, relative cost, climatic resistance (CR), stain resistance (FR), dn/dT data availability, valid wavelength range, internal transmission at 400 nm for 10 mm thickness.
2. Libraries → Materials Analyses → **Glass Map** with SCHOTT loaded. Locate your six glasses. Add the OHARA catalogue and find the OHARA glass closest to N-BK7 (hint: S-BSL7).
3. Use **Glass Compare** (or the catalogue) to compare N-BK7 and S-BSL7 at F, d, C. How large are the index differences?
4. Plot internal transmission vs. wavelength for N-BK7 and N-SF6 (10 mm) from 350–1000 nm. Which is the better choice for a 405 nm laser projector?
**Deliverable:** a "glass short list" table in notes with your recommendation for (a) a visible machine-vision lens, (b) an 850 nm NIR lens.
**Check yourself:** relative cost of N-BK7 is the reference (≈ 1); lanthanum and dense flint glasses cost several times more. N-SF6 absorbs noticeably in the near UV/violet; N-BK7 transmits well there. Equivalent glasses from different vendors usually agree in $n_d$ to ~1e-4 but not exactly — always design with the vendor's glass you will buy.

## Task 5 — NIR singlet (OpticStudio)
**Goal:** See how a structured-light NIR band changes chromatic behaviour.
**Steps:**
1. Copy the L01 singlet to `work/L05_T5_singlet_nir.zmx`. Set wavelengths 0.825, 0.850, 0.875 µm (weights 1, 2, 1), primary 0.850.
2. Read EFL and BFL (M-solve) and the Chromatic Focal Shift plot.
3. Compare the axial colour with the visible (F–C) case.
4. If the same lens were focused for d-light and then used at 850 nm, how far out of focus would the sensor be? Express the defocus blur diameter at F/5.
**Check yourself:** EFL at 850 nm ≈ 101.38 mm; axial colour across 825–875 nm ≈ 0.18 mm (vs 1.54 mm F–C); the 850 nm focus is ≈ 1.35 mm behind the d focus → defocus blur diameter ≈ 1.35/5 ≈ 0.27 mm. Lesson: a visible-designed lens refocused for NIR is fine, but not used unchanged.

## Stretch task — model glass
In a copy of the singlet, replace N-BK7 by a **model glass** (Material solve type "Model") with $n_d = 1.5168$, $V_d = 64.17$, $\Delta P_{g,F} = 0$. Check that EFL and the chromatic focal shift are nearly identical to N-BK7. Then make $V_d$ a variable (L07 preview) and note that an optimizer would push it to the maximum allowed — why must model glasses always be bounded and later substituted by real glass?

## Reflection questions
1. Why do high-index glasses tend to be more dispersive?
2. Why is the Abbe number defined with $n_d - 1$ in the numerator?
3. Why can't two normal glasses correct secondary spectrum?
4. When would you request melt data from the glass supplier?
5. Why might a projector designer prefer N-BK7 over a lanthanum glass even if the lanthanum glass gives better aberrations?

<details><summary>Answers</summary>

1. High index comes from strong polarizability, typically from UV absorption bands lying closer to the visible (lead, titanium, niobium oxides); being nearer the resonance also makes the index vary faster with wavelength.
2. Lens power is proportional to $n - 1$; the fractional change of power between F and C is $(n_F - n_C)/(n_d - 1) = 1/V$, so $V$ directly gives axial colour ($\delta f \approx f/V$).
3. Secondary spectrum ∝ $(P_1 - P_2)/(V_1 - V_2)$; for glasses on the normal line $P$ is a linear function of $V$, so this ratio is a constant (≈ −0.0005) and cannot be made zero.
4. When the design is sensitive to index (fast lenses, tight wavefront budgets, large optics) — before final fabrication, to re-optimize spacings/radii to the real melt.
5. Cost, availability, weight, better UV/blue transmission, chemical resistance and thermal behaviour; and in high-power illumination absorption heating matters.

</details>
