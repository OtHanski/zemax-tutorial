# L07 — Tasks: Secondary Spectrum, Apochromats and Glass Substitution

> Work in `work/` inside this lesson folder (e.g. save `work/L07_T3_ed_doublet.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5 h

## Task 1 — The partial-dispersion diagram (Python)
**Goal:** Build your own $P_{g,F}$–$\nu_d$ diagram and rank glass pairs.

**Given:** the nine glasses in lecture §1 (values from SCHOTT data sheets). Optional: export more glasses from OpticStudio's Materials Catalog (SCHOTT) — $n_d$, $V_d$, $P_{g,F}$ are listed per glass.

**Steps:**
1. Compute $\Delta P_{g,F} = P_{g,F} - (0.6438 - 0.001682\,\nu_d)$ for each glass and compare with the SCHOTT values in the table.
2. Plot $P_{g,F}$ vs $\nu_d$ (reversed $\nu$ axis, as in catalogs) with the normal line.
3. For every crown/flint pair with $\nu_1 > \nu_2 + 15$, compute $K_1/K$, $K_2/K$, $\delta f_g$ for $f = 100$ mm and $Pf$. Sort by $|\delta f_g|$ and list the top five with their element powers.
4. Draw the line joining N-BK7–F2 and N-FK51A–N-KZFS11 on your plot; relate the slopes to $\delta f_g$.

**Deliverable:** `work/pdiagram.py`, `work/pdiagram.png`, ranked table.

**Check yourself:** N-BK7/F2: slope −1.72×10⁻³, $\delta f_g = 0.172$ mm; N-FK51A/N-KZFS11: −5.85×10⁻⁴, 0.058 mm (lecture §3 table). The normal-line slope is −0.001682, so any two normal glasses give ≈ 0.17 mm per 100 mm.

## Task 2 — Three-glass apochromat solver (Python)
**Goal:** Solve the apochromat equations and test the triangle rule.

**Steps:**
1. Write `apo(g1, g2, g3)` solving $\sum K_i = 1$, $\sum K_i/\nu_i = 0$, $\sum P_iK_i/\nu_i = 0$ (normalized $K=1$).
2. Loop over all triples from Task 1; for each compute $\sum|K_i|$ and the area of the triangle in the $(\nu_d, P_{g,F})$ plane. Scatter-plot $\sum|K_i|$ vs area.
3. Reproduce Geary's example (§21.4) with his data ($\nu$: SSKN5 50.88, FPL53 94.97, BAK1 57.55; $\Delta P_{d,C}$ values in his Table 21.2) and check his powers.

**Check yourself:** best triple among the nine: N-FK51A / N-KZFS11 / N-SF5 with $K$ = 2.382, −1.972, +0.590 (triangle area ≈ 0.67 in these units). A normal-glass triple N-BK7/F2/N-SF5 has area ≈ 0.12 and needs $K$ = 4.24, −9.77, +6.54 — unbuildable. Geary: $f_i$ ≈ 172.9, 120.9, −86.5 mm for $f = 400$ mm.

## Task 3 — From achromat to "ED" doublet (OpticStudio)
**Goal:** Quantify what an anomalous-dispersion pair buys in a real design.

**Given:** your L06 design `../L06-chromatic-aberration-and-achromats/work/L06_T3_dmf.zmx` (N-BK7/N-SF5, $f = 100$ mm, F/5, ±1°). Add the g line (0.4358 µm) to the wavelengths (weights: g 0.5, F 1, d 1, C 1).

**Steps:**
1. Record: Chromatic Focal Shift (maximum focal-shift range and the g-focus offset), polychromatic RMS spot at 0°, polychromatic FFT MTF at 100 lp/mm.
2. Save as `work/L07_T3_ed_doublet.zmx`. Change the glasses to N-FK51A / N-KZFS11. Start radii from the thin-lens powers ($f_1 = 49.8$, $f_2 = -99.2$ mm; choose an equiconvex crown, compute the flint's rear radius).
3. Re-optimise with the same merit function (EFFL = 100, AXCL F–C = 0 and the polychromatic default merit function).
4. Compare all numbers from step 1. Also compare the SPHA/COMA balance and the radii (any steeper curves?). Check the glass data (Materials Catalog): relative cost, CTE, $dn/dT$, climate/stain resistance codes for N-FK51A vs N-BK7.

**Check yourself:** the g-focus offset from the F/C focus drops from ≈ 0.2 mm to ≈ 0.06 mm (thin-lens estimates 0.199 → 0.058 mm); polychromatic spot/MTF on axis improve markedly; element powers stay similar. N-FK51A is several times more expensive than N-BK7 and has roughly twice its thermal expansion — note the exact values from the catalog.

## Task 4 — Let Hammer pick the glasses (OpticStudio, Premium feature)
**Goal:** Practise glass substitution with catalog restrictions.

**Steps:**
1. Start from the N-BK7/F2 cemented doublet from L06 Task 1 (any zero-spherical bending, $f = 100$ mm, F/5, ±1°, wavelengths g, F, d, C).
2. Material solve on both elements → **Substitute** (catalog: SCHOTT). In System Explorer, restrict Material Catalogs to SCHOTT only.
3. Merit function: default (RMS wavefront, centroid, polychromatic) + EFFL = 100 + edge-thickness and centre-thickness boundary operands for both elements (e.g. minimum edge 1.5 mm, centre ≤ 8 mm).
4. Run local optimisation first, then **Hammer** for ~10 minutes. Record which glass pair it found and the merit function value. Save `work/L07_T4_hammer.zmx`.
5. Repeat with both elements set to **Model** glass (vary $n_d$, $V_d$, $\Delta P_{g,F}$), with bounds that keep them inside the populated part of the glass map. Where does the optimum fall on your Task 1 diagram? Which real glasses are nearest?

**Check yourself:** Hammer typically drifts toward a high-$\nu$ anomalous crown paired with a short or dense flint (the exact pair depends on weights and constraints — that's fine). The Model-glass optimum should lie in the "flatter-than-normal slope" region of your diagram. Always check that the chosen glasses are not "inquiry/obsolete" status and that their cost/climate codes are acceptable.

## Stretch task — A three-glass apochromat
Build the N-FK51A / N-KZFS11 / N-SF5 apochromat ($f = 100$ mm, F/5) from Task 2 powers: order (N-SF5 +, N-FK51A +, N-KZFS11 −) or any order you prefer, cemented or with tiny air gaps; reasonable thicknesses. Correct colour at C, F and g with two AXCL operands (or PARR + DIFF as in Geary §21.5), then optimise with the polychromatic default merit function. Plot the Chromatic Focal Shift: you should see an S-shaped (cubic) curve passing through three common points, with a total range of only a few µm over F–C — compare with your Task 3 doublets.

## Reflection questions
1. Why do all pairs of normal glasses have the same secondary spectrum, no matter how different their $\nu$ values are?
2. A colleague proposes CaF₂ for the crown of a 3D-camera lens to kill secondary spectrum. List three non-optical concerns.
3. Why does the triangle rule work, mathematically?
4. For an 850 nm VCSEL-based structured-light projector, is secondary spectrum a concern? For a white-LED projector with an RGB camera?

<details><summary>Answers</summary>

1. $\delta f = -f\,\Delta P/\Delta\nu$ and for any two points on a straight line $\Delta P/\Delta\nu$ is the line's slope — a constant.
2. Thermal: very high CTE and large $dn/dT$ (focus shift and stress with temperature); mechanical: soft, cleaves, thermal-shock sensitive, hard to polish and coat; cost and availability; also it's hygroscopic-ish/requires care with cleaning — specify handling and coatings.
3. The 3×3 system's determinant is proportional to the area of the triangle formed by the three glasses in the $(1/\nu, P/\nu)$-type plane; a small area means a nearly singular matrix and therefore large, opposing powers.
4. VCSEL: narrow band (≲ 1–2 nm), so primary axial colour is tiny and secondary spectrum irrelevant (thermal wavelength drift may still matter). White LED + RGB camera: yes — both the projector lens and the camera lens must be achromatized across the visible, and secondary spectrum shows as blue-channel blur and colour fringes.
</details>
