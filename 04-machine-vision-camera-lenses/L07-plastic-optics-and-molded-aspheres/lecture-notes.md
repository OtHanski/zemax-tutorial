# L07 — Plastic optics and molded aspheres

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2.5 h, tasks ~5 h
> **Prerequisites:** [01/L02 — conics and even aspheres](../../01-foundations/L02-surfaces-sign-conventions-aspheres/), [01/L05 — glass](../../01-foundations/L05-optical-glass-and-dispersion/), [03/L09 — thermal analysis](../../03-image-quality-optimization/L09-thermal-and-environmental-analysis/), [L04 — project](../L04-compact-fixed-focus-lens-project/) · **Next:** [L08 — Filters, cover glass, NIR and ghosts](../L08-filters-cover-glass-nir-and-ghosts/)

## Learning objectives
- Compare the main optical polymers (PMMA, PC, PS, COC/COP, optical polyesters) with glass in index, dispersion, $dn/dT$, expansion, water absorption, birefringence and temperature limits, and choose a polymer pair for a colour-corrected design.
- Compute the thermal focal-length coefficient $\gamma = \alpha - (dn/dT)/(n-1)$ and the thermal focus shift of plastic, glass and hybrid lenses; explain why plastics force an athermal strategy.
- Explain how stress birefringence arises in molded parts and when it matters (polarization optics, lasers, structured light with polarisers).
- Use even-asphere and Q-type (Qbfs, Qcon) surfaces in OpticStudio, and explain why Q-type coefficients are better conditioned and easier to relate to manufacturability.
- Apply moldability rules (thickness ratio, centre thickness, edge flange, slopes, gate) as constraints in the merit function.
- Decide between all-plastic, glass-plastic hybrid and all-glass for a machine-vision lens.

## Reading
- **Core:** [Kidger §7.5, pp. 159–162] — aspheric surfaces as "aspheric plates": $S_1 = 8a_4r^4(n'-n)$, stop-shift contributions to $S_2, S_3, S_5$ through $\bar h/h$; no effect on Petzval or first-order colour.
- **Core:** [Kenyon §10.6, p. 282] — photoelasticity: stressed plastic between crossed polarisers shows birefringence fringes.
- **Online:** N. Sultanova, S. Kasarova, I. Nikolov, "Application of optical polymers in plastic or hybrid glass-plastic optics", J. Optoelectron. Adv. Mater. 15 (2013) 58–61 — measured $n_d$, $V_d$, $dn/dT$ of PMMA, PS, PC, Zeonex E48R: <https://joam.inoe.ro/articles/application-of-optical-polymers-in-plastic-or-hybrid-glass-plastic-optics/fulltext>
- **Online:** G&H, "Materials for polymer optics" — qualitative comparison of PMMA, PC, PS, COP, OKP; plastics' $dn/dT$ ≈ 20× glass, CTE ≈ 10× glass: <https://gandh.com/news-and-resources/materials-for-polymer-optics>
- **Online:** ZEON, "Cyclo Olefin Polymer (COP) ZEONEX" brochure — grades, low birefringence and moisture absorption: <https://www.zeon.co.jp/cn/business/enterprise/pdf/200323392.pdf>
- **Online:** Edmund Optics FAQ, "Why plastic aspheric lenses?": <https://www.edmundoptics.co.uk/knowledge-center/frequently-asked-questions/optics/optical-lenses/why-plastic-aspheric-lenses>
- **Online:** Ansys Optics KB on asphere types in OpticStudio (Qbfs/Qcon vs even/extended asphere, "Find Best Asphere"): <https://optics.ansys.com/hc/en-us/articles/42661802686355>
- **Optional:** G. W. Forbes, "Shape specification for axially symmetric optical surfaces", Opt. Express 15, 5218 (2007) — the Q-type paper; and the Laser Focus World summary: <https://www.laserfocusworld.com/optics/article/16552818/optical-design-new-shape-specification-eases-design-and-fabrication-of-aspheres>

---

## 1. Why plastic?

Injection-molded plastic lenses dominate high-volume cameras (phones, automotive, consumer depth sensors). The reasons are economic and geometric:

- **Aspheres for free.** Once the mold insert is diamond-turned, every part has the same aspheric surfaces at no extra cost. Strong aspheres let 4–7 elements do what 8–12 spherical glass elements would.
- **Integrated mechanics.** Flanges, spacers, alignment features and stops can be molded into the lens.
- **Low mass, low unit cost** at volumes from ~10⁴ upward (the mold costs ~10⁴–10⁵ €).

And the reasons not to use them — which are exactly the properties a robust industrial 3D camera cares about:

- **Thermal behaviour**: $dn/dT$ ~ −1 × 10⁻⁴ /K, about 50–100× glass in magnitude and of opposite sign; CTE ~ 60–70 ppm/K, about 10× glass ([G&H](https://gandh.com/news-and-resources/materials-for-polymer-optics)).
- **Few materials**: essentially two "glass types" — a crown-like family ($n \approx 1.49$–1.54, $V \approx 56$–59) and a flint-like family ($n \approx 1.58$–1.64, $V \approx 20$–31). Colour correction is limited.
- **Moisture**: PMMA absorbs ~0.3 % water, changing index and shape; COP < 0.01 %.
- **Birefringence** from molding stress, **lower surface accuracy** than polished glass (form errors ~0.5–2 µm typical), **soft surfaces** (scratches, coatings harder), **temperature limits** (service temperatures ~80–130 °C).

## 2. The materials

Typical values (check the supplier's datasheet and your OpticStudio catalogue entry before designing; values vary by grade and measurement):

| Material | $n_d$ | $V_d$ | $dn/dT$ (10⁻⁶/K) | CTE (10⁻⁶/K) | Water absorption | Notes |
|---|---|---|---|---|---|---|
| PMMA (acrylic) | 1.491 | ~57–59 | ≈ −110 … −130 | ~65–70 | ~0.3 % | cheap, excellent transmission, low $T_g$ (~105 °C) |
| PC (polycarbonate) | 1.585 | ~30 | ≈ −110 … −140 | ~65–70 | ~0.2 % | tough, flint-like, high birefringence |
| PS (polystyrene) | 1.59 | ~30–31 | ≈ −120 … −130 | ~60–80 | low | flint-like, brittle |
| COP (e.g. Zeonex E48R) | 1.531 | ~56 | ≈ −100 … −130 | ~60 | < 0.01 % | low birefringence, the workhorse for camera lenses |
| COC (e.g. Topas grades) | ~1.53 | ~56–58 | ≈ −100 | ~60 | < 0.01 % | similar to COP |
| Optical polyesters (OKP) | ~1.61–1.64 | ~20–27 | — | — | — | high-index flint partner, very low birefringence |
| *N-BK7 (reference)* | *1.517* | *64* | *≈ +1.6* | *7.1* | — | |

Measured values from Sultanova et al. (2013): PMMA $n_d = 1.4914$, $V_d = 59.2$, $dn/dT = -130\times10^{-6}$/K; Zeonex E48R 1.5309, 56.5, $-126\times10^{-6}$/K; PS 1.5917, 30.5, $-131\times10^{-6}$/K. ZEON's brochure lists COP grades with glass-transition temperatures from roughly 120 to 160 °C depending on grade.

**Design consequence:** a plastic camera lens is typically built from a COP (crown) and a PC or OKP (flint) — e.g. "E48R + OKP4" or "E48R + PC" — exactly the two-glass achromat logic of Course 02 L06, with a small $\Delta V$ (≈ 25–35) and therefore strong powers.

**NIR note:** polymers transmit well at 850 and 940 nm in thin sections, but C–H vibrational overtone absorption bands exist in the near infrared; check the transmission curve of your grade at your wavelength and thickness.

## 3. Thermal behaviour: the dominant issue

For a thin lens in air, $1/f = (n-1)(c_1 - c_2)$. With temperature, curvatures scale with expansion ($c \propto 1/(1+\alpha\Delta T)$) and the index changes, giving the **thermo-optic (opto-thermal) coefficient**

$$
\gamma \equiv \frac{1}{f}\frac{df}{dT} = \alpha - \frac{1}{n-1}\frac{dn}{dT}
$$

(using $dn/dT$ relative to air). Numbers:

| Material | $\alpha$ (ppm/K) | $dn/dT$ (ppm/K) | $\gamma$ (ppm/K) | focus shift of an $f = 6$ mm lens over 40 K |
|---|---|---|---|---|
| PMMA | 67 | −120 | **+311** | +75 µm |
| PC | 67 | −115 | +264 | +63 µm |
| COP | 60 | −110 | +267 | +64 µm |
| N-BK7 | 7.1 | +1.6 | +4.0 | +1 µm |

An aluminium barrel ($\alpha$ = 23.6 ppm/K) of length ≈ 6 mm moves the sensor by only +5.7 µm over the same 40 K. With a depth of focus of ±10 µm at F/2.8 (L02), **an all-plastic lens with a plain metal barrel goes out of focus within ~10 K.** Phone cameras live with this because they autofocus; a fixed-focus industrial 3D camera cannot.

**Athermalization levers** (full treatment in Course 03 L09):
1. **Hybrid glass–plastic**: for elements in contact, $\gamma_\text{sys}\phi = \sum\gamma_i\phi_i$. To match a barrel, $\gamma_\text{sys} = \alpha_\text{barrel}$. Because $|\gamma_\text{plastic}| \gg |\gamma_\text{glass}|$, a *weak* plastic element is a powerful thermal lever (Worked example).
2. **Plastic power balance**: positive and negative plastic elements with similar $\gamma$ cancel each other's thermal drift (and partially their colour) — the standard trick in plastic camera lenses.
3. **Mechanical compensation**: spacer/barrel materials with high CTE (or plastic barrels) chosen so that the image moves with the lens.
4. **Glass for the strong elements**, plastic only for aspheric "correctors" with little power.

Even when focus is athermal, **image scale (EFL)** still changes with temperature — for a calibrated 3D camera that is a depth-scale error (L05 §4.3). Check both.

## 4. Birefringence

Molded parts freeze in stress: flow orientation near the **gate** and differential cooling leave residual stress, and stress makes the polymer birefringent (photoelasticity [Kenyon §10.6, p. 282]). Polycarbonate is notorious; COP and optical polyesters are low-birefringence grades ([ZEON brochure](https://www.zeon.co.jp/cn/business/enterprise/pdf/200323392.pdf); [G&H](https://gandh.com/news-and-resources/materials-for-polymer-optics)). Effects:
- Retardance of a few to tens of nm across a lens turns linear polarization elliptical: a problem for systems with polarisers (polarisation-filtered structured light to suppress specular reflections, polarisation cameras), laser projectors (speckle and DOE efficiency are polarisation-dependent) and interferometric metrology.
- For unpolarised intensity imaging, typical birefringence has only a small effect on MTF.
- Mitigation: low-birefringence resin, gate far from the clear aperture, uniform wall thickness, slow cooling/annealing, design-side placement of plastic elements away from polarisation-critical paths.

OpticStudio models birefringence with dedicated birefringent surface/material models and polarization ray tracing; stress-induced birefringence from mechanical/molding simulation comes in through STAR / structural coupling (Premium; Course 06 L05). In most camera work you **specify** a maximum retardance (e.g. < 20 nm/cm) rather than model it.

## 5. Aspheres: even asphere and Q-type

### 5.1 Even asphere
OpticStudio's *Even Asphere* surface:

$$
z(r) = \frac{c\,r^2}{1+\sqrt{1-(1+k)c^2r^2}} + \alpha_1r^2 + \alpha_2r^4 + \alpha_3r^6 + \alpha_4r^8+\dots
$$

(Course 01 L02). Kidger shows how the fourth-order term acts as an "aspheric plate": $S_1 = 8a_4r^4(n'-n)$ referred to the marginal-ray height, plus stop-shift contributions $S_2 = (\bar h/h)S_1$, $S_3 = (\bar h/h)^2S_1$, $S_5 = (\bar h/h)^3S_1$; aspheres do **not** change the Petzval sum or first-order colour [Kidger §7.5, Eqs. 7.42–7.44]. Hence the design rule: **aspheres near the stop correct spherical aberration; aspheres far from the stop (large $\bar h/h$) correct astigmatism and distortion** — which is why phone lenses put strong aspheres on the last elements near the sensor.

Practical problems with power-series coefficients:
- They are **not orthogonal**: $\alpha_3r^6$ and $\alpha_4r^8$ look alike over the aperture, so the optimizer produces huge coefficients of alternating sign that cancel — poorly conditioned, sensitive to rounding (always give 6+ significant digits on drawings), and hard to interpret.
- Their values depend on the lens units and the aperture radius.
- The $\alpha_1r^2$ term duplicates the base curvature — leave it at zero.

### 5.2 Q-type (Forbes) polynomials
Forbes (2007) introduced orthogonal bases for rotationally symmetric aspheres. OpticStudio's *Q-Type Asphere* surface offers two forms ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/42661802686355)):

- **Qbfs** ("best-fit sphere"): departure measured from a best-fit sphere, normal to it, with a basis designed so that the **RMS slope of the departure** is the sum of squares of the coefficients. For mild aspheres this ties coefficients directly to interferometric testability.
- **Qcon** ("conic"): departure from a base conic, with an orthogonal basis for the sag departure — for strong aspheres, such as molded camera lenses.

With normalised radial coordinate $u = r/r_\max$:

$$
z_\text{Qcon}(r) = \frac{c\,r^2}{1+\sqrt{1-(1+k)c^2r^2}} + u^4\sum_{m=0}^{M} a_m\,Q^\text{con}_m(u^2).
$$

Advantages: coefficients have physical meaning (µm of departure or slope), they are well conditioned (optimizer converges more smoothly, fewer cancelling terms), and adding a term does not change the meaning of the earlier ones. The KB comparison found Q-type and extended aspheres performing similarly in a double-Gauss test, and notes that OpticStudio's *Find Best Asphere* tool often ends up suggesting even aspheres ([Ansys KB](https://optics.ansys.com/hc/en-us/articles/42661802686355)) — the benefit is mainly conditioning and communication with the manufacturer, not magic performance. Check with your molder which representation their diamond-turning and metrology software accept; many still want even-asphere coefficients, which you can convert (refit) at the end.

**Normalization radius.** Both the even-asphere (in OpticStudio's *Extended Asphere*) and Q-type surfaces use a normalization radius; set it to the clear semi-aperture (slightly larger) and *do not change it after optimizing*, or the coefficients lose meaning.

## 6. Moldability rules (rules of thumb)

Discuss with the molder early; typical guidance for small camera lenses:

| Rule | Typical value | Why |
|---|---|---|
| Thickness ratio max/min (centre vs edge, including flange) | ≤ 3:1 (≤ 2:1 better) | uneven cooling → sink, stress, birefringence |
| Centre thickness | ~0.5–4 mm for small lenses; thick parts mean long cycles and voids | |
| Edge flange | 0.5–1.5 mm wide, outside the clear aperture | gate, ejector, mounting datum |
| Surface slope | keep below ~45–55° at the clear aperture edge | mold insert machining, metrology, coating uniformity |
| Inflection points | possible but costly to measure; avoid unless needed | |
| Clear aperture vs mechanical | ≥ 0.3–0.5 mm margin to the flange | gate-region distortion and birefringence |
| Form accuracy | ~0.5–2 µm PV typical; compensated by iterative mold correction | tolerance budget (Course 06) |
| Air gaps | spacers or interlocking flanges; ≥ 0.05–0.1 mm | stacking tolerances |

In the merit function: `MNCT`/`MXCT` (centre thickness), `MNET`/`ETGT` (edge thickness), ratios through `DIVI` of thickness operands bounded with `OPLT`, and slope checks in the Surface Sag analysis (and its slope output, if available in your version). Glass molding (precision glass-molded aspheres, e.g. low-$T_g$ glasses) is the robust alternative: aspheric freedom with glass thermal behaviour, at higher cost — very relevant for industrial cameras.

## 7. In OpticStudio

- **Materials:** plastics are in catalogues such as MISC (e.g. PMMA, POLYCARB) and vendor catalogues such as ZEON (E48R …); names and availability vary by version — use the Materials Catalog search. Check that each entry has thermal data (TCE and $dn/dT$ coefficients) before running thermal analyses; add or correct from datasheets if missing.
- **Surfaces:** *Even Asphere*, *Extended Asphere* (with normalization radius) and *Q-Type Asphere* (Qbfs / Qcon). Convert gradually: optimize spheres → add conic → add 4th/6th order → higher orders. Increase the number of rays (pupil sampling) once aspheres are strong, or optimization will "fit between the rays".
- **Thermal:** Multi-Configuration with TEMP and PRES operands (Course 03 L09) or the thermal analysis tools; evaluate focus and EFL at −10, 20, 50 °C.
- **Tools:** *Find Best Asphere* (suggests which surface to make aspheric, and which type), *Surface Sag* analysis (slopes, departure from best-fit sphere).

## Worked example — athermal hybrid singlet pair

**Given:** a 6 mm focal-length lens (thin, in contact), aluminium barrel ($\alpha_h$ = 23.6 ppm/K) whose length between lens and sensor ≈ $f$. Glass element N-BK7 ($\gamma_1 = 7.1 - 1.6/0.5168 = 4.0$ ppm/K) and plastic element PMMA ($\gamma_2 = 67 + 120/0.491 = 311$ ppm/K).

1. **All-PMMA lens:** focus shift over 40 K = $6\cdot311\times10^{-6}\cdot40$ = 75 µm; barrel moves 5.7 µm; mismatch ≈ 69 µm ≫ ±10 µm depth of focus.
2. **All-glass:** lens grows 1.0 µm, barrel 5.7 µm → mismatch 4.7 µm (OK, but note glass is "under-compensated" by an Al barrel).
3. **Athermal hybrid:** require $\phi_1\gamma_1 + \phi_2\gamma_2 = \alpha_h(\phi_1+\phi_2)$ with $\phi_1 + \phi_2 = 1/6$ mm⁻¹:

$$
\phi_2 = \phi\,\frac{\alpha_h - \gamma_1}{\gamma_2 - \gamma_1} = \frac16\cdot\frac{23.6-4.0}{311.4-4.0} \Rightarrow f_2 = 94.1\text{ mm},\quad f_1 = 6.41\text{ mm}.
$$

A weak *positive* PMMA element (f ≈ 94 mm) carrying ~6 % of the power makes the pair track the aluminium barrel. (Colour correction and the ±10 % uncertainty in polymer $dn/dT$ are ignored here — in a real design you solve thermal, achromatic and power conditions together and verify with multi-configuration thermal analysis; the $dn/dT$ uncertainty alone is why many industrial designs avoid giving plastics much power.)

## Key takeaways
- Plastics give cheap aspheres and integrated mechanics, at the cost of huge $dn/dT$ (~−10⁻⁴/K), large CTE, moisture, birefringence and limited materials.
- $\gamma = \alpha - (dn/dT)/(n-1)$: ~+300 ppm/K for polymers vs ~+4 ppm/K for N-BK7; a 6 mm all-plastic lens moves focus ~75 µm over 40 K.
- Athermalize by hybrid glass–plastic power splits, opposing plastic powers, or mechanics; also check EFL (scale) drift for calibrated 3D cameras.
- COP/COC are the low-birefringence, low-moisture workhorses; PC and OKP are the flints.
- Aspheres near the stop fix spherical; far from the stop they fix astigmatism and distortion; they do not change Petzval or first-order colour.
- Q-type (Qcon/Qbfs) coefficients are orthogonal and meaningful; even-asphere coefficients are ill-conditioned but still the lingua franca of many molders.
- Encode moldability (thickness ratio, flange, slope) in the merit function early.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| COP / COC | Cyclo-olefin polymer / copolymer (e.g. Zeonex, Topas) |
| Thermo-optic coefficient $\gamma$ | $(1/f)\,df/dT = \alpha - (dn/dT)/(n-1)$ |
| Athermalization | Making focus (and ideally EFL) insensitive to temperature |
| Stress birefringence | Birefringence from residual molding stress (photoelastic effect) |
| Gate | Point where the molten polymer enters the mold cavity |
| Even asphere | Conic + power series in $r^2$ |
| Q-type (Qbfs, Qcon) | Forbes orthogonal-polynomial asphere representations |
| Normalization radius | Radius used to normalize $r$ in extended/Q-type aspheres |
| Precision glass molding (PGM) | Molding aspheres from low-$T_g$ optical glass |

## References
1. [Kidger §7.5, pp. 159–162] — aspheric surfaces and their Seidel contributions.
2. [Kenyon §10.6, p. 282] — photoelasticity.
3. N. Sultanova, S. Kasarova, I. Nikolov, J. Optoelectron. Adv. Mater. 15, 58–61 (2013): <https://joam.inoe.ro/articles/application-of-optical-polymers-in-plastic-or-hybrid-glass-plastic-optics/fulltext>
4. G&H, "Materials for polymer optics": <https://gandh.com/news-and-resources/materials-for-polymer-optics>
5. ZEON, "Cyclo Olefin Polymer (COP) ZEONEX" brochure: <https://www.zeon.co.jp/cn/business/enterprise/pdf/200323392.pdf>
6. Edmund Optics, "Why plastic aspheric lenses?": <https://www.edmundoptics.co.uk/knowledge-center/frequently-asked-questions/optics/optical-lenses/why-plastic-aspheric-lenses>
7. Ansys Optics KB, asphere types (Qbfs, Qcon, extended asphere, Find Best Asphere): <https://optics.ansys.com/hc/en-us/articles/42661802686355>
8. G. W. Forbes, "Shape specification for axially symmetric optical surfaces", Opt. Express 15(8), 5218–5226 (2007); summary in Laser Focus World: <https://www.laserfocusworld.com/optics/article/16552818/optical-design-new-shape-specification-eases-design-and-fabrication-of-aspheres>
