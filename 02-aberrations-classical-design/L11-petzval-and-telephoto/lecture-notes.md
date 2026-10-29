# L11 — The Petzval lens and the telephoto

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~2.5 h, tasks ~5–6 h
> **Prerequisites:** [L04 (Petzval sum, field flatteners)](../L04-field-curvature-petzval-flatteners/), [L06 (achromats)](../L06-chromatic-aberration-and-achromats/), [L08 (stop shift)](../L08-seidel-surface-contributions/), [L10 (Celor rear half)](../L10-symmetric-lenses-double-gauss-vignetting/) · **Next:** [L12 — Mirrors and catadioptrics](../L12-mirrors-and-catadioptrics/)

## Learning objectives
- Derive the thin-lens Petzval layout ($f_A = 2f$, $f_B = f$, $d = f$, BFL $= f/2$) from the "equal deviation" condition and explain why it minimizes the shape-dependent aberrations.
- Use the stop-shift equations to explain how two separated positive groups can cancel astigmatism, and estimate the residual sagittal blur from Seidel coefficients.
- Choose among three ways of dealing with the Petzval lens's large Petzval sum: flat-tangential compromise, curved image surface, and a field flattener — and quantify each.
- Design a two-thin-lens telephoto for a given focal length and telephoto ratio, and compute its Petzval sum.
- Build, constrain (`EFFL`, `AXCL`, `TTHI`, `DIVI`, `TOTR`) and optimize a Petzval objective and a telephoto in OpticStudio, including a curved image surface.
- Recognize where these forms appear in modern products (long-focal machine-vision lenses, projection lenses, compact long-focus camera modules).

## Reading
- **Core:** [Kidger Ch. 9, pp. 183–197] — Seidel analysis of the Petzval lens (§9.1, including the transverse-aberration estimate §9.1.1), optimization (§9.2), three worked designs: two cemented doublets, curved image, field flattener (§9.3), and the telephoto (§9.4).
- **Core:** [Geary Ch. 33, pp. 377–381] — thin-lens Petzval derivation (§33.2) and Geary's ZEMAX procedure with the `TTHI`/`DIVI` BFL constraint (§33.3).
- **Optional:** [Geary §33.5, pp. 382–386] — "Image Quality IV": which focus criterion (minimum blur, compactness, Strehl, first axial peak) to use for 0.5–3 waves of spherical aberration. Useful background for Course 03.
- **Optional:** [Geary §19.5] (Chevalier lens) for the historical context of Petzval's portrait lens.

---

## 1. Why another form? The doublet's astigmatism wall

A thin lens (or cemented doublet) **at the stop** has astigmatism

$$
S_{III} = H^2 K ,
$$

independent of bending and glass [Kidger eq. 7.8]. Nothing you do to the doublet itself removes it, which limits doublets to fields of a few degrees. To cancel astigmatism you need power *away from the stop*, where the stop-shift terms $2kS_{II} + k^2 S_I$ (L08) can generate astigmatism of the opposite sign.

The Petzval lens (Joseph Petzval, 1839–1840; F/3.6 — about twenty times faster than the Chevalier lenses of the day [Geary §33.1]) does this with **two separated positive groups** with the stop near the first. Historically the front was a cemented achromat and the rear an air-spaced (inverted Celor-like) pair [Kidger p. 183; Geary Fig. 33.1].

## 2. First-order layout: the equal-deviation rule

Ask that the two thin lenses deviate the marginal ray *equally* (spreading the work minimizes the shape-dependent aberrations, which grow steeply with deviation) and that the marginal ray height at the second lens is half that at the first [Geary §33.2]:

$$
y_B = \tfrac12 y_A,\qquad u'_A = -y_A/f_A,\qquad u'_B = 2u'_A .
$$

Working through the paraxial equations gives

$$
f_A = 2f,\qquad f_B = f,\qquad d = f,\qquad \text{BFL} = f/2 .
$$

Check with the two-lens power formula: $K = K_A + K_B - dK_AK_B = \tfrac{K}{2} + K - \tfrac1K\cdot\tfrac{K}{2}\cdot K = K$ ✓. Kidger states the same rule of thumb (powers $K/2$ and $K$, separation $1/K$) [§9.1, p. 184]. Total track is $1.5f$ — a Petzval lens is long.

**The catch: Petzval sum.** Both groups are positive, so with a mean index 1.6,

$$
P = \frac{K/2 + K}{1.6} \approx 0.94\,K ,
$$

about 50% *more* than a single lens of the same power ($K/1.6 \approx 0.63K$). The Petzval radius is about $-1.07f$ — the defining weakness of the form [Kidger §9.3.2].

## 3. Seidel analysis: astigmatism balance and its price

Following [Kidger §9.1]: let each group be an achromat corrected for spherical aberration ($S_{I,A}=S_{I,B}=0$), stop at A. Then the total coma is $S_{II,A}+S_{II,B}$ and the total astigmatism, from the stop-shift equations applied to B (with $k_B = H E_B$),

$$
\Sigma S_{III} = H^2K_A + H^2K_B + 2k_B S_{II,B}.
$$

So: give group B a deliberate coma $S_{II,B}$ of the right sign to cancel the astigmatism, and give group A an equal and opposite coma so the total coma vanishes. You need **two different doublets, each spherically corrected, with equal and opposite coma** — a classic exercise in doublet bending (L06/L08). Once $S_I = S_{II} = 0$ for the whole lens, the stop position no longer matters to third order; keeping it at the front group minimizes the front diameter, which is the element exposed to the environment [Kidger p. 185].

### What field can it cover?
With $\Sigma S_{IV} = H^2\sum K/n \approx H^2K$ (for $n\approx1.5$), the best one can do with astigmatism is to flatten the *tangential* field: $3S_{III} + S_{IV} = 0 \Rightarrow S_{III} = -S_{IV}/3$. The sagittal error at the edge of the pupil is then

$$
\delta\xi' = \frac{S_{III}+S_{IV}}{2n'u'} = \frac{\tfrac23 H^2K}{2u'} = \frac{u'\eta'^2K}{3}.
$$

For $f=100$ mm, F/2 ($u'=-0.25$), $\theta = 10^\circ$ ($\eta' = 17.63$ mm, $H = 4.41$ mm): $\delta\xi' = -0.25\times17.63^2\times0.01/3 = -0.26$ mm (Kidger rounds $\eta'$ to 17 and quotes −0.24 mm) [§9.1.1, pp. 185–186]. A blur of ~0.5 mm diameter at 10° — poor, but ten times the field of an equivalent doublet. This is why the classic Petzval is a **narrow-field (≤ ±10–12°), fast (F/1.5–F/3)** lens.

## 4. Three ways out of the Petzval-curvature trap

Kidger's §9.3 compares three optimized f = 100 mm designs:

1. **Flat image, two cemented doublets** (F/2.3, ±10°): tangential field nearly flat, sagittal curved; S-shaped ray fans (residual spherical) but little coma; vignetting by the rear group improves the tangential fans. $\Sigma S_{IV} = 0.132$ ($P = S_{IV}/H^2 = 0.0092$ mm⁻¹). The finite-ray sagittal error, 0.20 mm, is a bit less than the Seidel 0.24 mm thanks to higher-order sagittal oblique spherical aberration.
2. **Curved image surface.** If the detector (or film, or a fibre faceplate) can be curved, let the image radius be a variable: Kidger's optimum is $R_{\text{img}} = -93.6$ mm vs. the thin-lens Petzval radius estimate $-1/P \approx -100$ mm [§9.3.2]. Curved sensors remain niche, but this is how you find the "natural" field shape of a design.
3. **Field flattener.** A negative lens close to the image: since $h\approx0$ there, it adds almost nothing to $S_I$, $S_{II}$, $S_{III}$ and colour, but it contributes $S_{IV} = H^2K_f/n_f < 0$. In Kidger's design an SF5 plano-concave ($R=-38.17$ mm, $f\approx-56$ mm) contributes $S_{IV}=-0.144$, taking the total from ≈ +0.13 to −0.01 [§9.3.3]. Not in contact with the image (dust and scratches would be in focus): ~2 mm away. Limit: at larger fields the edge rays hit the steep flattener surfaces obliquely, so the field-flattened Petzval is still a ≤ ±10° lens at ~F/2. The flattener also shortens the BFL drastically — a mechanical issue for cameras with filters or cover glass.

**Zivid angle.** Long-focus, fast, narrow-field lenses for inspection cameras are Petzval derivatives; so are many projection lenses (L05 of Course 05), where a field-flattener-like element near the DMD/LCoS is common. For any camera with a cover glass and IR filter in front of the sensor, the field-flattener option competes for the same few millimetres of back focus — always budget it early.

## 5. The telephoto

### Principle
Two thin lenses $+K_1$ and $-K_1$ separated by $d$ have total power $K = dK_1^2 > 0$ regardless of order [Kidger eq. 9.7]. With the **positive lens in front** this is a *telephoto*: the rear principal plane lies in front of the lens, so the physical length $L$ (front vertex to image) is shorter than $f$. The figure of merit is the **telephoto ratio**

$$
T = L/f < 1 .
$$

With equal indices the Petzval sum $K_1/n - K_1/n = 0$; if each component is an aplanat, there are no stop-shift terms, so $S_{III} = H^2(K_1+K_2) = 0$ too: a telephoto can in principle have all monochromatic Seidel terms zero [Kidger §9.4, p. 194].

### Design equations
For a front positive lens $f_1$, rear negative $f_2$, separation $d$ and back focal distance $b$ (all thin, object at infinity):

$$
f_1 = \frac{d\,f}{f-b},\qquad h_2 = 1 - \frac{d}{f_1},\qquad K_2 = \frac{1/f - 1/f_1}{h_2},\qquad L = d + b .
$$

Two things to notice:
- **The front group is faster than the system**: it carries more power than the whole lens. Kidger's F/4 example has a front group working at about F/3 [p. 195] — this is what limits telephoto apertures.
- **No front–back symmetry** ⇒ odd aberrations are not automatically cancelled: telephotos characteristically show **pincushion distortion** (Kidger's example: $\Sigma S_V = -0.091$, the largest residual in his table) and lateral colour.

Kidger's multielement telephoto (f = 100 mm, F/4, ±10°) has a single + cemented doublet front group, a stop, and a cemented negative-ish rear doublet, with a total length of 90.9 mm (T ≈ 0.91) and nearly all Seidel sums ≤ 0.005 except distortion [pp. 195–197]. His design tip: first design an aplanatic front component, add the negative group and optimize it alone, then free everything; and do try removing the extra front singlet — "greatly inferior" without it.

### Reverse telephoto (retrofocus)
Swap the order (negative in front) and the back focal distance becomes *longer* than $f$: the classic wide-angle SLR lens and many machine-vision wide-angle lenses that must clear a filter stack or a mirror. Course 04 L05 picks this up.

## 6. Choosing a form: how a designer thinks

By now you have met the main classical families. A professional's first question for a new specification is not "which glass?" but "which *form* has the degrees of freedom this aperture–field combination needs?":

| Requirement | Natural starting form | Why |
|---|---|---|
| Narrow field (≤ ±3°), F/4–F/8 | cemented or air-spaced doublet (L06–L07) | only $S_I$, $S_{II}$, $C_I$ matter |
| Narrow field (≤ ±10°), fast (F/1.5–F/3) | Petzval (+ flattener if back focus allows) | two positive groups share the aperture work |
| Medium field (±20–25°), F/3.5–F/5.6 | Cooke triplet / Tessar (L09) | minimum form correcting all seven Seidel terms |
| Medium field, F/1.4–F/2 | double Gauss (L10) | symmetry + thick menisci for Petzval |
| Long focal length, short body | telephoto | $T = L/f < 1$ |
| Short focal length, long back focus | retrofocus (reverse telephoto) | clears filters, mirrors, prisms |
| Very long focal length, broadband | mirror or catadioptric (L12) | no colour, compact folded path |

Two rules of thumb sit behind this table. First, **aperture is "paid for" with elements that share the marginal-ray deviation** (Petzval, double Gauss), while **field is "paid for" with elements away from the stop and with symmetry** (triplet, Celor, double Gauss). Second, the **Petzval sum is decided by the power distribution and glass indices before any bending is chosen** — if the form cannot bring $Pf$ down to roughly 0.3–0.5 (or tolerate the resulting field curvature), no amount of optimization will rescue it. Check $Pf$ for any candidate form with the thin-lens formulas in five minutes before you open OpticStudio.

## 7. In OpticStudio

- **First-order constraints:** `EFFL` for focal length; `TTHI` (sum of thicknesses over a surface range) for the BFL or for the total length; `DIVI` (divide two operand values) to enforce ratios, e.g. Geary's $f/\text{BFL} = 2$ [Geary §33.3]; `TOTR` (total track) for telephoto length; `EFLY` on a surface range to hold a group focal length; `AXCL`, `LACL` for colour.
- **Stop midway between groups** (Geary): pick up the rear-stop air space from the front-stop air space.
- **Curved image surface:** make the image surface radius a variable (Standard surface type); a *Field Curvature* plot then shows S and T relative to that curved surface.
- **Field flattener:** add a plano-concave element 1–3 mm before the image; watch `MNEA`/`MNCA` and the image-space chief ray angle (it will grow — relevant to sensor CRA, Course 04 L03).
- **Walk the field out** in steps and regenerate the default merit function each time (Geary's advice) to avoid "ray cannot be traced" errors.
- **Diagnostics:** Seidel Diagram (look for the opposite-sign coma of the two groups), Field Curvature/Distortion, Longitudinal Aberration, Ray Fan (vignetting shows as shortened tangential fans), Relative Illumination.

## Worked example

**(a) Thin-lens Petzval, f = 100 mm, F/2.** $f_A = 200$, $f_B = 100$, $d = 100$, BFL = 50 mm (verified by paraxial trace: $h_B/h_A = 0.5$, EFL 100.0, BFL 50.0). With $n=1.6$: $P = (0.005+0.010)/1.6 = 0.009375$ mm⁻¹, Petzval radius $-106.7$ mm. At $\eta' = 17.63$ mm (10°) the Petzval surface is $\eta'^2P/2 = 1.46$ mm from the flat image plane — at F/2 that is a blur diameter of ~0.73 mm if uncorrected by astigmatism.

**(b) Adding a field flattener.** To cancel $P$ with an SF5-type flattener ($n = 1.6776$): $K_f = -0.009375\times1.6776$, $f_f = -63.6$ mm. Placed 3 mm before the original image ($h_f/h_A = 0.03$), it changes the EFL to 104.95 mm, and the image now lies only 3.15 mm behind the flattener (which itself sits 47 mm behind lens B). So: flat Petzval field, ~5% longer focal length (re-scale or re-optimize), and almost no back focus — exactly the trade-offs of Kidger's Fig. 9.8 design.

**(c) Telephoto, f = 200 mm, T = 0.70.** Choose $d = 60$, $b = 80$ ($L = 140$ mm). Then $f_1 = 60\times200/120 = 100$ mm, $h_2 = 0.4$, $K_2 = (0.005-0.010)/0.4 = -0.0125$, $f_2 = -80$ mm. Petzval with $n = 1.5$ for both: $P f = (0.01 - 0.0125)/1.5\times200 = -0.33$ — a slightly *over*-corrected (backward-curving) Petzval field, typical of strong telephotos. The equal-and-opposite case $f_1 = 100$, $f_2 = -100$ needs $d = K/K_1^2 = 50$ mm and gives $b = 100$, $T = 0.75$ with $P = 0$.

## Key takeaways
- A lens at the stop always has $S_{III}=H^2K$; separated groups and stop-shift terms are needed to cancel astigmatism.
- Petzval layout: $f_A = 2f$, $f_B = f$, $d = f$, BFL $= f/2$ (equal marginal-ray deviation); fast and sharp on axis, but Petzval sum ~1.5× that of a singlet.
- Manage the Petzval sum by flattening the tangential field (sagittal blur $\approx u'\eta'^2K/3$), curving the image, or a field flattener near the image (costs back focus and raises CRA).
- Telephoto: front positive faster than the system, rear negative; $T = L/f < 1$; Petzval can be zero; distortion (pincushion) and lateral colour are the typical residuals.
- Use `TTHI`, `DIVI`, `TOTR`, `EFLY` to impose first-order architecture during optimization, and walk the field out gradually.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Petzval (portrait) lens | Two separated positive groups, stop near the front group |
| Equal-deviation rule | Each group deviates the marginal ray by the same angle |
| Anastigmat | Lens with astigmatism corrected (S and T coincide), possibly on a curved surface |
| Field flattener | Negative element near an image; corrects Petzval with little other effect |
| Telephoto ratio | $T = L/f$, physical length over focal length |
| Reverse telephoto / retrofocus | Negative group first; BFL longer than f |
| SOBSA / TOBSA | Sagittal / tangential oblique spherical aberration (higher-order field-dependent spherical) |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE Press 2002 — Ch. 9, pp. 183–197; eq. 7.8 (§7.2).
2. [Geary] J. M. Geary, *Introduction to Lens Design*, Willmann-Bell 2002 — Ch. 33, pp. 377–386; §19.5 (Chevalier lens).
