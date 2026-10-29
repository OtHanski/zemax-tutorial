# L09 — The Cooke triplet

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~6 h
> **Prerequisites:** [L04 (Petzval)](../L04-field-curvature-petzval-flatteners/), [L06 (achromats)](../L06-chromatic-aberration-and-achromats/), [L08 (Seidel surface contributions)](../L08-seidel-surface-contributions/), [Course 01 L07 (optimization)](../../01-foundations/L07-solves-variables-first-optimization/) · **Next:** [L10 — Symmetric lenses, double Gauss and vignetting](../L10-symmetric-lenses-double-gauss-vignetting/)

## Learning objectives
- Explain why three separated elements (+ − +) are the minimum that can correct all seven Seidel aberrations over a useful field, and count the degrees of freedom.
- Set up and solve the thin-lens predesign equations (power, Petzval sum, axial and lateral colour) in Python, and convert the solution to a thick-lens starting prescription.
- Build, constrain and optimize a 50 mm F/4, ±20° triplet in OpticStudio, and read its Seidel Diagram to explain the final aberration balance.
- Choose glasses for a triplet with physical reasoning (index for Petzval and spherical, dispersion for colour), and predict what happens if the central flint index is changed.
- Use and interpret vignetting factors (VDX/VDY/VCX/VCY) and relative illumination for a deliberately vignetted triplet.
- Relate RMS spot radius ("image compactness") to wavefront coefficients and compute the optimum defocus for spherical aberration.

## Reading
- **Core:** [Kidger Ch. 10, pp. 199–208] — thin-lens Seidel theory of the triplet (§10.1), an optimized 50 mm F/4 SK16/F6/SK16 example with full Seidel table (§10.2), glass choice (§10.3), vignetting (§10.4).
- **Core:** [Geary Ch. 30, pp. 343–353] — design philosophy (§30.2), Geary's "rear half first" procedure (§30.3), image compactness and its link to RMS spot (§30.6–30.7), lateral colour revisited (§30.8). Homework 30.9 #2 is an excellent extra.
- **Core (refresh):** [Geary Ch. 28, pp. 315–327] — the Celor procedure that Geary reuses for the triplet (you will meet it properly in L10).
- **Optional:** [Kidger §7.7, pp. 164–166] — general design strategies (symmetry, power distribution).
- **Optional:** Ansys Optics knowledge-base article on vignetting factors (S. Gangadhara): <https://optics.ansys.com/hc/en-us/articles/42661826659347>, and the community answer "How do vignetting factors affect my ray trace?": <https://community.zemax.com/got-a-question-7/how-do-vignetting-factors-affect-my-ray-trace-87>

---

## 1. Why the triplet is the milestone design

Up to now each design form has corrected only a subset of the aberrations:

| Form | Corrects | Cannot correct |
|---|---|---|
| Singlet (bent, stop shifted) | coma (or astigmatism) | spherical, Petzval, colour |
| Cemented achromat at the stop | spherical, coma, axial colour | astigmatism, Petzval |
| Landscape / periscopic | coma, astigmatism (some) | spherical, Petzval, colour |

The missing piece is **Petzval sum**. For thin lenses $P = \sum_i K_i/n_i$ (L04), while the power of separated thin lenses is $K = \sum_i (h_i/h_1) K_i$ [Kidger eq. 2.66]. A negative lens placed where the marginal ray is *lower* contributes fully to $P$ but less to $K$. That is the whole trick: positive and negative powers of similar magnitude with a separation give a net positive power but a small Petzval sum [Geary §30.2, pp. 343–344; Kidger Ch. 10 intro].

A two-element + − system does this but is very asymmetric, so coma, distortion and lateral colour are large. H. Dennis Taylor's 1893 solution (US patents 540,132 and 568,053) splits the positive lens into two, one on each side of the negative lens with the stop near the middle. Approximate front–back symmetry then suppresses the odd aberrations (coma, distortion, lateral colour), exactly as you saw with the periscopic lens in L03.

### Degrees of freedom
With glasses chosen and thicknesses fixed (thicknesses are poor variables: they should be 5–10% of the diameter for manufacturability [Kidger p. 200]), the thin-lens triplet has **eight** variables: three powers $K_1, K_2, K_3$, three shape factors (bendings), and two air spaces $d_1, d_2$. The targets are **eight**: focal length plus the seven Seidel aberrations $S_I$–$S_V$, $C_I$, $C_{II}$. Hence the classic statement: the Cooke triplet is the simplest lens that can correct *all* third-order aberrations [Kidger p. 199; Geary p. 343].

Kidger's recommended sequence splits the problem in two:

1. **Shape-independent aberrations** — power, Petzval, axial colour, lateral colour — depend only on $K_i$ and the ray heights (i.e. on $K_i$, $d_1$, $d_2$). Four equations, five unknowns ⇒ a one-parameter family of solutions.
2. **Shape-dependent aberrations** — $S_I$, $S_{II}$, $S_{III}$, $S_V$ — are then controlled by the three bendings. Bending the outer lenses (away from the stop) changes all four; bending the central lens (at the stop) changes only $S_I$ and $S_{II}$ (stop-shift logic of L08: $\bar h \approx 0$ there). So: use outer bendings for $S_{III}$ and $S_V$, the inner bending for $S_{II}$, and the spare parameter from step 1 to bring $S_I$ to zero. Sometimes two complete solutions exist for a glass pair [Kidger §10.1, pp. 200–201].

In modern practice you would do step 1 by hand (it gives you a physically sensible start in ten minutes) and let the optimizer do step 2.

## 2. Thin-lens predesign equations

Normalise the marginal ray to $h_1 = 1$ and put the stop at lens 2, so $\bar h_2 = 0$. For thin lenses with Abbe numbers $V_i$ [Kidger eq. 10.1]:

$$
\begin{aligned}
K &= K_1 + \frac{h_2}{h_1}K_2 + \frac{h_3}{h_1}K_3 &&\text{(power)}\\
P &= \frac{K_1}{n_1} + \frac{K_2}{n_2} + \frac{K_3}{n_3} &&\text{(Petzval sum)}\\
0 &= \frac{h_1^2K_1}{V_1} + \frac{h_2^2K_2}{V_2} + \frac{h_3^2K_3}{V_3} &&\text{(axial colour)}\\
0 &= \frac{h_1\bar h_1K_1}{V_1} + \frac{h_2\bar h_2K_2}{V_2} + \frac{h_3\bar h_3K_3}{V_3} &&\text{(lateral colour; middle term vanishes)}
\end{aligned}
$$

(Kidger's printed eq. 10.1 has $V_1$ in the last denominator — a typo; it is $V_3$.) The heights follow from the thin-lens trace: $u'_1 = -h_1K_1$, $h_2 = h_1 + d_1u'_1$, $u'_2 = u'_1 - h_2K_2$, $h_3 = h_2 + d_2u'_2$; for the chief ray through the centre of lens 2 with slope $\bar u$ in the first gap, $\bar h_1 = -d_1\bar u$ and $\bar h_3 = d_2\bar u$ (lens 2 at the stop does not deviate the chief ray).

**Do not target $P = 0$.** Zero Petzval forces strong powers, large surface contributions and big higher-order aberrations; the best balance leaves a residual Petzval that is cancelled by a little negative astigmatism (L04: flatten the *tangential* or *mean* field, not the Petzval surface). Kidger quotes $P \approx 0.35K$ as typical [p. 200]; his optimized 50 mm example ends at $P\approx0.44K$ (computed from his prescription). A range $Pf = 0.3$–$0.45$ is a good starting window. For comparison, a single N-SK16 lens has $Pf = 1/n = 0.62$.

### Choosing the glasses
[Kidger §10.3, pp. 204–206] gives the reasoning:
- **Positive lenses:** high index (reduces surface curvatures ⇒ less $S_I$ and lower Petzval $K/n$) and low dispersion (high $V$) ⇒ a *dense crown*: SK16 / N-SK16 is the textbook choice; N-LAK9, N-SSK… for more performance.
- **Negative lens:** you want *low* index (bigger negative Petzval contribution $K_2/n_2$) but *high* dispersion (to correct colour with little power). These conflict, so a compromise flint with an index close to the crowns is used — F2, F4, F6, LF5.
- Swapping the central F6 for low-index LF7 improves colour but the design goes asymmetric and gains higher-order spherical and coma; swapping it for high-index SF18 needs less negative power for colour, so there isn't enough negative $S_I$ and the design collapses [Kidger Figs. 10.6–10.9].
- Rule of thumb: crowns and flint with nearly *equal* $n_d$ and a $V$ difference of ~20–25 are a good triplet pair. N-SK16 ($n_d=1.6204$, $V_d=60.3$) with F2 ($n_d=1.6200$, $V_d=36.4$) is almost the ideal of that rule.

## 3. From thin lenses to a thick starting prescription

1. Pick bendings: front lens roughly convex-plano (curved side to the object, like the singlet of L08), central lens roughly equi-concave, rear lens roughly plano-convex with the convex side to the image. These are Seidel-sensible and close to Kidger's optimized shapes (front 18.6/461, middle −29.9/18.6, rear 67.6/−22.2 mm).
2. Radii from the lensmaker's equation: plano-convex $R = (n-1)f$; equi-concave $R = 2(n-1)f$.
3. Thicknesses: positives ≈ 3 mm (edge thickness ≥ ~1 mm at the clear aperture), negative ≈ 1.2 mm (centre thickness ≥ ~1 mm and ≥ ~D/10 is a common shop rule for small negatives).
4. Vertex air spaces ≈ thin-lens separations minus half the adjacent thicknesses. Put the stop in the second air space, ~1 mm behind the negative lens (a real iris or shutter needs clearance [Kidger p. 200]).
5. Let a marginal-ray-angle (F/#) solve or an `EFFL` target fix the focal length.

Geary's alternative [§30.3, pp. 344–345] builds the triplet as two "Celor rear halves" — a plano-concave negative with the stop on its flat side plus an equi-convex positive — optimizes the half, mirrors it to make a symmetric system with the stop buried in the negative element, optimizes with the rear half slaved to the front (pickup solves), then breaks symmetry and finally moves the stop into air. It is slower but teaches the role of symmetry very clearly; L10 uses it.

## 4. What the optimized triplet looks like

Kidger's optimized SK16/F6/SK16 triplet, 50 mm F/4, ±22° [§10.2, pp. 202–203] shows the classic aberration *balance* rather than zero:

- Spherical aberration well corrected; coma small thanks to near symmetry.
- Third-order astigmatism deliberately left negative ($\Sigma S_{III} = -0.016$) to balance the residual Petzval ($\Sigma S_{IV}=+0.056$) and fifth-order astigmatism, so the tangential field bends back at the edge.
- The Seidel table shows large positive contributions from the outer lenses and large negative from the central lens for all *even* aberrations ($S_I$, $S_{III}$, $S_{IV}$, $C_I$); the odd ones ($S_V$, $C_{II}$) cancel between lenses 1 and 3 [Kidger Table 10.1].
- Performance: sagittal quality falls off above ~10°; MTF at 30 cy/mm "only just acceptable" at F/4, much better at F/5.6–F/8. A triplet is a ~F/3.5–F/5.6, ±20–25° lens; beyond that you need more elements (Tessar, double Gauss, L10).

**Tessar.** Splitting the rear positive into a cemented doublet adds a curvature (one more degree of freedom) and a "buried" surface for colour and higher-order spherical; at equal specs a Tessar beats a triplet [Geary §30.5, p. 346]. Many cheap machine-vision and M12 board lenses are triplet or Tessar derivatives with plastic aspheres (Course 04).

## 5. Image compactness — the RMS spot in wavefront language

Geary defines *image compactness* as the pupil-averaged squared transverse ray error and shows it is what the default RMS-spot (`TRAC`-based) merit function minimizes [Geary §30.6, pp. 346–350]. With normalized pupil radius $\rho$, the transverse error is $\varepsilon = 2(F/\#)\,\partial W/\partial\rho$ (in air). For defocus plus spherical, $W = W_{020}\rho^2 + W_{040}\rho^4$, and averaging $\varepsilon^2$ over the unit disk:

$$
\langle\varepsilon^2\rangle = 4(F/\#)^2\Big[2W_{020}^2 + \tfrac{16}{3}W_{020}W_{040} + 4W_{040}^2\Big].
$$

Minimizing over $W_{020}$ gives $W_{020} = -\tfrac43 W_{040}$ and

$$
\sigma_{\text{RMS}} = \tfrac43\,(F/\#)\,W_{040},\qquad \delta z = -8(F/\#)^2 W_{020} = \tfrac{32}{3}(F/\#)^2 W_{040}.
$$

Compare with L02: the *wavefront*-RMS-optimal defocus is $W_{020} = -W_{040}$, the *spot*-RMS-optimal defocus is $-\tfrac43 W_{040}$. The two default merit functions (RMS wavefront vs RMS spot) therefore converge to slightly different focus positions — worth knowing when you compare MTF-optimized and spot-optimized designs.

## 6. Vignetting in a triplet

A triplet covering ±20° with clear apertures sized for the full axial beam at all fields would be big and expensive. Practical triplets clip the oblique beam: the full-field beam is typically about **60%** of the axial beam width, and with $\cos^4$ fall-off the corner illumination is only ~40% of the centre [Kidger §10.4, pp. 206–208]. Vignetting also *improves* image quality, because it removes the most aberrated rim rays of the oblique beam (mostly the tangential upper/lower rim — exactly where triplet aberrations are worst). An unvignetted triplet has more uniform illumination but a more strongly curved sagittal field and worse off-axis MTF [Kidger Figs. 10.10–10.13].

### How OpticStudio handles it
OpticStudio launches rays to fill the paraxial entrance pupil; surface **apertures** (clear semi-diameters set as fixed) then block rays physically. **Vignetting factors** in the Field Data Editor instead *redefine* the pupil seen by each field so that the optimizer and analyses only use rays that actually get through:

$$
P_x' = VDX + P_x(1-VCX),\qquad P_y' = VDY + P_y(1-VCY),
$$

where $(P_x, P_y)$ are normalized pupil coordinates, VDX/VDY *decentre* and VCX/VCY *compress* the pupil, and TAN rotates the pattern. Use them like this:

1. Design first with no vignetting (semi-diameters in automatic mode) and see how large the elements become.
2. Decide the maximum clear apertures (e.g. 1.1× the axial-beam footprint) and fix them (semi-diameter solve "Fixed" or use `MXSD`-type constraints).
3. Press **Set Vignetting** (Field Data Editor toolbar; location varies by version) so OpticStudio computes factors such that each field's marginal rays just pass the apertures; re-optimize; repeat Set Vignetting a few times as the design moves. **Clear Vignetting** resets them.
4. Check **Relative Illumination** (Analyze → Image Quality / Illumination group; location varies by version) and the **Footprint Diagram** for each surface.

Caveats: vignetting factors are an approximation of the true vignetted pupil (fine for circular/rectangular apertures, poor for strange shapes); they are ignored by Seidel analyses; and if you forget to update them after big changes, the optimizer may "cheat" by using rays that the hardware will block. The Ansys article above shows that with good vignetting factors you can keep the fast Gaussian-quadrature pupil sampling in the default merit function instead of a rectangular grid.

**Zivid angle.** For a 3D camera, vignetting is a radiometric budget item: the corner signal-to-noise of the structured-light pattern is what limits depth noise at the image edges. A camera lens is therefore typically specified with relative illumination ≥ 50–60% at full field; a classic camera triplet at 40% would be marginal. Course 04 L03 returns to this.

## 7. In OpticStudio

- **Starting point.** Enter the thick prescription (Section 3); System Explorer: Aperture type *Entrance Pupil Diameter* (12.5 mm for F/4 at 50 mm) or *Image Space F/#*; Fields *Angle* 0, 14, 20° (0, 0.7, 1.0 normalized); Wavelengths F, d, C (d primary).
- **Variables:** all six radii and the air spaces (not the stop position initially; then let the space before and after the stop vary separately). Keep glass thicknesses fixed or bounded.
- **Constraints (operands you can trust):** `EFFL` = 50; `MNCT`/`MXCT` (min/max centre thickness; `MNCG`/`MNCA` for glass/air only) and `MNEG`/`MNEA` (min edge thickness of glass/air) — or use the boundary-constraint section of the **Optimization Wizard** for glass and air; `TOTR` if you want a length cap. Use the Optimization Wizard's RMS spot radius (centroid reference) to start; switch to RMS wavefront later.
- **Glass as variable (optional):** set the glass solve to *Substitute* and use **Hammer** with a catalog restricted to a few glasses, or *Model* glass (nd, Vd variable) and then convert to the nearest real glass (Course 03 L05).
- **Diagnostics:** **Seidel Diagram** (expect the alternating +/−/+ pattern), **Field Curvature/Distortion**, **Ray Fan**, **Standard Spot Diagram**, **FFT MTF** to 60–80 cy/mm, **Relative Illumination**, **Footprint Diagram**.
- **Pitfall:** if the optimizer drives the middle element to touch a neighbour or makes it 0.2 mm thick, your boundary constraints are missing. If the stop jumps into glass, you forgot to make its adjacent air spaces separate variables with minimum values.

## Worked example — thin-lens predesign of a 50 mm F/4 N-SK16 / F2 / N-SK16 triplet

Glasses (SCHOTT): N-SK16 $n_d = 1.62041$, $V_d = 60.32$; F2 $n_d = 1.62004$, $V_d = 36.37$. Target $f = 50$ mm, $Pf = 0.40$ (Petzval radius $-125$ mm), $C_I = C_{II} = 0$. With the spare parameter used to force **equal spacings** $d_1 = d_2$ (near-symmetric), solving the four equations numerically (script in Task 1) gives:

| Quantity | Value |
|---|---|
| $f_1$ (N-SK16) | +29.57 mm |
| $f_2$ (F2) | −16.95 mm |
| $f_3$ (N-SK16) | +26.20 mm |
| $d_1 = d_2$ | 5.70 mm |
| $h_2/h_1$, $h_3/h_1$ | 0.807, 0.886 |
| thin-lens BFL | 44.3 mm |

Check the logic: the negative lens has the strongest power ($|K_2| \approx 2.95K$) but sits where the marginal ray is only 0.81 of its entrance height, so its power contribution is $-2.38K$ while its Petzval contribution is $-1.82K$ (vs. $+1.04K$ and $+1.18K$ from the positives, after dividing by $n$): $1.04 - 1.82 + 1.18 = 0.40$ ✓. Changing the target to $Pf = 0.35$ makes all powers stronger ($f_2 = -15.6$ mm) — the price of a flatter Petzval field.

Thick starting prescription (plano/equi bendings, 3/1.2/3 mm thick, stop 1 mm behind the negative lens):

| Surf | R (mm) | t (mm) | Glass |
|---|---|---|---|
| 1 | 18.34 | 3.0 | N-SK16 |
| 2 | ∞ | 3.6 | |
| 3 | −21.01 | 1.2 | F2 |
| 4 | 21.01 | 1.0 | |
| STO | ∞ | 2.6 | |
| 6 | ∞ | 3.0 | N-SK16 |
| 7 | −16.25 | ≈ 44.9 (paraxial) | |

Paraxial: $f = 50.8$ mm, BFL 44.9 mm. Seidel sums (EPD 12.5, 20°): $S_I = 0.023$, $S_{II} = 0.012$, $S_{III} = -0.053$, $S_{IV} = 0.041$, $S_V = 0.011$ mm, and $S_{IV}/H^2 \cdot f = 0.40$ — the Petzval target survives the thick-lens conversion. The optimizer's job is now mainly the shape-dependent terms.

**Compactness check** (Geary §30.6.4): a 400 mm F/4 spherical mirror has $W_{040} = h^4/(4R^3) = 50^4/(4\cdot800^3) = 3.05$ µm; the best-focus RMS spot is $\tfrac43 \cdot 4 \cdot 3.05 = 16.3$ µm, located $\tfrac{32}{3}\cdot 16 \cdot 3.05 = 520$ µm from paraxial focus — the numbers Geary confirms in ZEMAX with a `TRAC` merit function.

## Key takeaways
- The triplet corrects Petzval with separated + − + powers and the odd aberrations with near symmetry about a central stop; 8 variables vs 8 targets make it the simplest "fully correctable" anastigmat.
- Solve power, Petzval and colour first with thin-lens algebra (one free parameter remains), then let bendings handle $S_I$, $S_{II}$, $S_{III}$, $S_V$.
- Do not aim for zero Petzval; $Pf \approx 0.3$–$0.45$ with negative astigmatism is the professional balance.
- Glass rule: high-index, high-V crowns; flint with similar index and ~20–25 lower V.
- Vignetting (~60% oblique beam width) is normal and beneficial for image quality; model it with fixed apertures plus vignetting factors and check relative illumination.
- RMS spot is minimized at $W_{020} = -\tfrac43W_{040}$ (spot) vs $-W_{040}$ (wavefront): different merit functions, different best focus.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Cooke triplet | Three separated singlets (+ − +) with the stop near the negative element; H. D. Taylor 1893 |
| Tessar | Triplet with the rear positive replaced by a cemented doublet |
| Shape-independent aberrations | Power, Petzval, axial/lateral colour of thin lenses — depend only on powers and positions |
| Shape-dependent aberrations | $S_I$, $S_{II}$, $S_{III}$, $S_V$ — change with lens bending |
| Image compactness | Pupil-averaged squared transverse ray error (≈ RMS spot²) [Geary] |
| Vignetting factors | VDX/VDY (decentre) and VCX/VCY (compression) of the pupil per field, plus TAN |
| Set Vignetting | OpticStudio tool that computes vignetting factors from current apertures |
| Relative illumination | Image irradiance at a field point relative to the axis, including vignetting and $\cos^4$-type effects |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE Press 2002 — Ch. 10, pp. 199–208; eq. 2.66 p. 39; §7.7 pp. 164–166.
2. [Geary] J. M. Geary, *Introduction to Lens Design*, Willmann-Bell 2002 — Ch. 30, pp. 343–353; Ch. 28, pp. 315–327.
3. H. D. Taylor, US Patents 540,132 (1895) and 568,053 (1896) — cited in [Kidger p. 199]; searchable on Google Patents.
4. S. Gangadhara, "Using vignetting factors…" Ansys Optics knowledge base: <https://optics.ansys.com/hc/en-us/articles/42661826659347>
5. Zemax community, "How do vignetting factors affect my ray trace?": <https://community.zemax.com/got-a-question-7/how-do-vignetting-factors-affect-my-ray-trace-87>
