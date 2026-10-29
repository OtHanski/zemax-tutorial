# L11 — Tasks: The Petzval lens and the telephoto

> Work in `work/` inside this lesson folder (e.g. save `work/L11_T3_petzval.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~5–6 h

## Task 1 — Derive the Petzval layout and its field limit (pen & paper)
**Goal:** Own the first-order and third-order logic of the form.
**Given / specs:** thin lenses A (front, at the stop) and B; object at infinity; system focal length $f$.
**Steps:**
1. Impose equal marginal-ray deviation at A and B and $y_B = y_A/2$. Derive $f_A$, $f_B$, $d$ and BFL in terms of $f$.
2. Compute the Petzval sum for $n_A = n_B = 1.6$ and compare with a single lens of focal length $f$.
3. For $f = 100$ mm, F/2, semi-field 10°: compute $H$, $\eta'$, and the sagittal transverse error when the tangential field is flattened ($S_{III} = -S_{IV}/3$), assuming $\Sigma S_{IV}=H^2K$ as in Kidger.
4. Repeat 3 for F/4 and for 5°. How does the blur scale with F/# and field?
**Deliverable:** derivation and numbers in `work/notes.md`.
**Check yourself:** $f_A = 2f$, $f_B = f$, $d = f$, BFL $= f/2$; $Pf = 0.9375$ vs 0.625 for a singlet; $H = 4.408$ mm, $\eta' = 17.63$ mm, $\delta\xi' = -0.259$ mm. At F/4: −0.130 mm; at 5° (F/2): $\eta' = 8.75$ mm, −0.064 mm. Blur ∝ $\eta'^2/F\#$.

<details><summary>Hints / solution sketch</summary>

$u'_A = -y_A/f_A$; $u'_B = u'_A - y_BK_B = 2u'_A$ ⇒ $y_BK_B = -u'_A = y_A/f_A$, with $y_B = y_A/2$ ⇒ $f_B = f_A/2$. Final slope $-y_A/f = 2u'_A = -2y_A/f_A$ ⇒ $f_A = 2f$. Transfer: $y_B = y_A + d\,u'_A = y_A(1 - d/2f) = y_A/2$ ⇒ $d = f$. BFL $= -y_B/u'_B = (y_A/2)/(y_A/f) = f/2$. Sagittal: $\delta\xi' = (S_{III}+S_{IV})/(2u') = \tfrac23H^2K/(2u') = u'\eta'^2K/3$ with $H=-u'\eta'$ magnitude 4.408.
</details>

## Task 2 — First-order explorer: field flattener and telephoto ratio (Python)
**Goal:** Build quick paraxial intuition before touching OpticStudio.
**Given / specs:** thin lenses, object at infinity.
**Steps:**
1. Write `system(Ks, ds)` returning EFL, BFL and marginal-ray heights (thin-lens $y$–$u$ trace).
2. Petzval lens of Task 1 (f = 100): add a flattener of power $K_f$ chosen to make the total Petzval sum zero (flattener $n_f = 1.6776$, other lenses $n = 1.6$). Place it at $g = 1, 3, 5, 10$ mm before the original image. Tabulate the new EFL, the new BFL and $h_f/h_A$.
3. Telephoto, $f = 200$ mm: for telephoto ratios $T = 0.65 \ldots 0.95$ with a fixed BFL $b = 0.4f$, compute $f_1$, $f_2$, $d$ and $Pf$ (both $n=1.5$). Plot $f_1/f$ and $Pf$ vs. $T$.
4. Which $T$ gives $P = 0$? What happens to $f_1$ (and hence the front group's F/#) as $T$ decreases?
**Deliverable:** `work/first_order.py`, tables/plots.
**Check yourself:** flattener $f_f = -63.6$ mm; at $g = 3$ mm: EFL 104.95 mm, new BFL 3.15 mm, $h_f/h_A = 0.03$. Telephoto with $d = 60$, $b = 80$: $f_1 = 100$, $f_2 = -80$, $T = 0.70$, $Pf = -0.33$; the equal-opposite case $f_1 = -f_2 = 100$ has $d = 50$, $b = 100$, $T = 0.75$, $P = 0$.

<details><summary>Hints / solution sketch</summary>

$f_1 = df/(f-b)$, $h_2 = 1 - d/f_1$, $K_2 = (1/f - 1/f_1)/h_2$, $L = d + b$. With $b$ fixed, $d = Tf - b$. Shorter telephotos need a stronger front lens (smaller $f_1/f$), i.e. the front group works at a lower F/# than the system — the aperture limitation of telephotos — and the Petzval sum goes increasingly negative.
</details>

## Task 3 — Petzval objective in OpticStudio: flat, curved, flattened (OpticStudio)
**Goal:** Reproduce Kidger's three Petzval solutions and compare them quantitatively.
**Given / specs:** Kidger's two-doublet Petzval lens [Kidger §9.3.1, p. 187]: f = 100 mm, F/2.3 (EPD 43.1 mm), semi-field 10° (fields 0, 7, 10°), wavelengths 0.546 (primary), 0.650, 0.475 µm. Radii 89.98583, −84.19189, 376.69338, (stop: plane), 71.13013, −37.24710, −209.61078; thicknesses 15, 4, 40, 40, 14, 3, (56.146 to image). Glasses: use **Model glass** solves with the indices/Abbe numbers in Kidger's table (1.567505/40.53, 1.677649/29.80, 1.626901/43.56, 1.694169/28.84) — note Kidger's indices are at 546 nm, so your EFL may differ by a few tenths of a percent.
**Steps:**
1. Enter the lens; check EFL, Seidel sums against Kidger ($\Sigma S_I=0.028$, $\Sigma S_{III}=-0.033$, $\Sigma S_{IV}=0.132$). Explain any small differences.
2. Replace the model glasses with real catalog glasses close on the glass map (Glass Compare or the "find nearest" option in the model-glass solve; location varies by version), then re-optimize (RMS spot, all radii and the 2nd–4th air spaces variable, `EFFL` = 100).
3. **Curved image:** make the image radius variable and re-optimize. Compare with $-1/P$.
4. **Field flattener:** restore a flat image; insert a plano-concave SF5-type element (2 mm thick) about 2 mm before the image; re-optimize with `EFFL` = 100 and `MNCA` ≥ 1.5 mm for the last air gap.
5. For all three variants record: RMS spot (0/7/10°), Field Curvature/Distortion, image-space chief-ray angle at 10° (`RAID` on the image surface, or read from the Ray Trace / Single Ray Trace table), BFL.
**Deliverable:** `work/L11_T3_petzval_flat.zmx`, `..._curved.zmx`, `..._flattener.zmx`; comparison table.
**Check yourself:** curved-image optimum radius roughly −90 to −110 mm (Kidger: −93.6 mm); the flattener variant has the flattest field and best edge RMS spot but a BFL of only a few mm and a larger chief-ray angle at the image; the flat-image variant shows a flat tangential but curved sagittal field.

<details><summary>Hints / solution sketch</summary>

- Model glass: in the Glass column, solve type *Model*, enter Nd and Vd (and dPgF = 0).
- If the chief-ray angle matters (it will, for sensors — Course 04 L03), note how the flattener tilts the edge chief ray away from telecentric.
</details>

## Task 4 — Design a telephoto (OpticStudio)
**Goal:** Practise first-order-driven design and see the telephoto's characteristic residuals.
**Given / specs:** f = 200 mm, F/5.6 (EPD 35.7 mm), semi-field 6° (0, 4, 6°), F/d/C, object at infinity. Telephoto ratio **T ≤ 0.75** (front vertex to image ≤ 150 mm). Front group: cemented N-BK7/N-SF5 doublet; rear group: cemented doublet (e.g. N-SF5 / N-BK7, negative overall). Stop: between the groups, ≥ 15 mm from the rear group.
**Steps:**
1. Use Task 2 for the thin-lens powers ($f_1 \approx 100$, $f_2 \approx -80$ to $-100$, $d \approx 50$–60). Achromatize each group roughly with the L06 thin-lens achromat formulas.
2. Enter thick lenses; constrain `EFFL` = 200, `TOTR` ≤ 150 (or `TTHI` over all surfaces), `AXCL` = 0, glass/air boundary constraints.
3. Optimize first with only the rear group variable (Kidger's advice), then everything.
4. Record distortion at 6° (sign!), lateral colour, RMS spot, and the front group's working F/# (`EFLY` over the front-group surfaces divided by its clear aperture).
**Deliverable:** `work/L11_T4_tele.zmx`; notes with T, distortion, residual Seidel sums.
**Check yourself:** a two-doublet telephoto at F/5.6, ±6° should reach RMS spots of a few tens of µm or better; distortion is typically positive (pincushion) at the 0.5–2% level and is the largest residual; front group works around F/2.8–F/3.5 ($f_1 \approx 100$–120 mm over a ~36 mm aperture).

<details><summary>Hints / solution sketch</summary>

If the optimizer shortens the lens by collapsing the stop gap, add `MNCA` on the gaps. If distortion is too large, the classic cure is a weak element far from the stop or slight power redistribution; accept some — it is the price of the asymmetric form.
</details>

## Stretch task(s)
- **Geary's Petzval homework procedure** [Geary §33.3]: hold the front achromat fixed, design the rear group with the Celor equations (L10 Task 1, rear group $f = f_{\text{front}}/2$), enforce $f/\text{BFL} = 2$ with `TTHI` + `DIVI`, then release that constraint and see colour and spot size improve.
- **Focus criteria:** in your Task 3 lens, compare best focus by RMS spot, RMS wavefront and peak of the Through-Focus (Huygens or FFT) Strehl on axis; relate to [Geary §33.5, Table 33.1].
- **Reverse it:** swap the telephoto groups (negative front) for a f = 20 mm wide-angle with BFL ≥ 30 mm — your first retrofocus (preview of Course 04 L05).

## Reflection questions
1. Why does making each Petzval group spherically corrected *and* giving them opposite coma lead to a lens whose stop position no longer matters (to third order)?
2. A Petzval lens with a field flattener looks perfect at 10°. Why is it unwise to push it to 20°?
3. Why must the front group of a telephoto be faster than the complete lens, and what does that imply for the maximum practical aperture?
4. Your machine-vision camera needs a 50 mm, F/2, narrow-field lens but only has 12 mm of back focus because of a filter stack. Which of today's forms would you start from, and why?

<details><summary>Answers</summary>

1. The stop-shift equations: if $\Sigma S_I = \Sigma S_{II} = 0$, then $\Delta S_{III} = 2k S_{II} + k^2S_I = 0$ and $\Delta S_{II} = kS_I = 0$; only distortion and lateral colour still depend on the stop.
2. The edge-of-field rays hit the steep flattener surfaces at large angles: higher-order aberrations and tight tolerances; also the image-space chief-ray angle becomes large (poor for sensors).
3. $f_1 = df/(f-b) < f$ for any telephoto; the front group's diameter is close to the system EPD, so its F/# $= f_1/\text{EPD} < f/\text{EPD}$. Fast telephotos demand very fast front groups with large higher-order aberrations.
4. A Petzval lens (long working focal length, narrow field, F/2-capable) with BFL = f/2 = 25 mm comfortably clears 12 mm; avoid a field flattener (it kills back focus); flatten the field with astigmatism balance or accept slight curvature within the depth of focus.
</details>
