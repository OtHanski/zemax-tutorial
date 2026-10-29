# L07 — Secondary Spectrum, Apochromats and Glass Substitution

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~5 h
> **Prerequisites:** [L06 — Chromatic aberration and achromats](../L06-chromatic-aberration-and-achromats/); Course 01 [L05 optical glass](../../01-foundations/L05-optical-glass-and-dispersion/) · **Next:** [L08 — Seidel surface contributions](../L08-seidel-surface-contributions/)

## Learning objectives
- Define relative partial dispersion ($P_{g,F}$, $P_{F,d}$, $P_{d,C}$), the Abbe diagram and the **normal line**, and compute $\Delta P_{g,F}$ for a catalog glass.
- Derive the secondary-spectrum formula $\delta f = -f\,\Delta P/\Delta V$ for a thin achromat and use it to rank glass pairs; estimate the resulting blur against the Airy disk.
- Explain why "anomalous" glasses (N-FK51A, N-PK52A; N-KZFS short flints) reduce secondary spectrum, and what they cost (stronger elements, Petzval, thermal and manufacturing properties, price).
- Solve the three-glass thin-lens **apochromat** power equations and pick glasses with the "big triangle" rule.
- Design achromats with an air space (split doublet, dialyte) and explain the extra freedom.
- Use OpticStudio's glass tools (Glass Map, Glass Compare, Model glass, Substitute solve, Hammer optimisation) to search for better glass pairs, and multi-wavelength colour operands to correct three colours.

## Reading
- **Core:** [Geary Ch. 18, pp. 195–206] — partial dispersion, the normal glass line, secondary spectrum of an achromat (Eq. 18.24), when it matters (§18.5), flat-field achromat condition (§18.6).
- **Core:** [Geary Ch. 19, pp. 207–220] — separated (dialyte) achromat and the apochromatic constraint (§19.2–19.3).
- **Core:** [Geary Ch. 21, pp. 229–237] — three-glass apochromat: power solution by determinants, a worked 400 mm example, the "triangle" rule for glass choice, and three-colour correction in ZEMAX with PARR/DIFF.
- **Core:** [Kidger §5.1.3, pp. 94–97] — secondary spectrum, relative partial dispersion and the $-0.0005$ "normal glass" slope.
- **Core:** [Kidger §8.3–8.4, pp. 177–183] — split (air-spaced) Fraunhofer and Gauss doublets, induced aberrations, general limits of doublets.
- **Optional online:** SCHOTT glass pages (each lists $n_d$, $\nu_d$, $P_{g,F}$, $\Delta P_{g,F}$), e.g. N-FK51A: <https://www.schott.com/shop/advanced-optics/en/Optical-Glass/N-FK51A/c/glass-N-FK51A> and N-KZFS11: <https://www.schott.com/shop/advanced-optics/en/Optical-Glass/N-KZFS11/c/glass-N-KZFS11>; J. Greivenkamp, OPTI 502 "Materials" lecture notes (Univ. of Arizona) for a compact overview of glass maps: <https://wp.optics.arizona.edu/jgreivenkamp/wp-content/uploads/sites/11/2019/08/502-17-Materials.pdf>

---

## 1. Partial dispersion and the normal line

The Abbe number measures the *average slope* of $n(\lambda)$ between F and C. But $n(\lambda)$ is curved — steeper in the blue — so two glasses with the same $V$ can distribute their dispersion differently across the band. The **relative partial dispersion** for wavelengths $x$, $y$ is

$$
P_{x,y} = \frac{n_x - n_y}{n_F - n_C}.
$$

Common choices: $P_{g,F}$ (g = 435.8 nm, the blue end; Schott's headline number), $P_{F,d}$ and $P_{d,C}$ (with $P_{F,d} + P_{d,C} = 1$) [Geary §18.2; Kidger Eq. 5.11]. Geary tabulates BK7 at $P_{F,d} = 0.6928$, SF2 at 0.7078 [Geary p. 197].

Plot $P_{g,F}$ against $\nu_d$ for all catalog glasses and most of them fall on a straight line — the **normal line** [Geary Fig. 18.3; Kidger Fig. 5.5]. Schott defines it through the reference glasses K7 and F2 as

$$
P_{g,F}^{\text{normal}} = 0.6438 - 0.001682\,\nu_d ,\qquad \Delta P_{g,F} = P_{g,F} - P_{g,F}^{\text{normal}} .
$$

$\Delta P_{g,F}$ is printed on every SCHOTT data sheet. Values used in this lesson (from the SCHOTT online data sheets; recomputing $\Delta P$ from the formula reproduces the published values to ±0.0001):

| Glass | $n_d$ | $\nu_d$ | $P_{g,F}$ | $\Delta P_{g,F}$ | Type |
|---|---|---|---|---|---|
| N-BK7 | 1.51680 | 64.17 | 0.5349 | −0.0010 | normal crown |
| F2 | 1.62004 | 36.37 | 0.5828 | +0.0002 | normal flint (defines the line) |
| N-SF5 | 1.67271 | 32.25 | 0.5984 | +0.0088 | dense flint |
| **N-FK51A** | 1.48656 | 84.47 | 0.5359 | **+0.0342** | fluor crown, anomalous |
| **N-PK52A** | 1.49700 | 81.61 | 0.5377 | **+0.0311** | phosphate crown, anomalous |
| N-KZFS4 | 1.61336 | 44.49 | 0.5590 | −0.0100 | short flint |
| N-KZFS5 | 1.65412 | 39.70 | 0.5710 | −0.0060 | short flint |
| N-KZFS8 | 1.72047 | 34.70 | 0.5833 | −0.0021 | short flint |
| **N-KZFS11** | 1.63775 | 42.41 | 0.5605 | **−0.0120** | short flint |

"Short flints" (KZFS = Kurzflint) have unusually *short* blue dispersion for their $\nu$; fluor/phosphate crowns have unusually *long* blue dispersion for their very high $\nu$. Both are off the normal line in the directions that help (below). Crystalline CaF₂ and Ohara's FPL-type glasses (e.g. FPL53, $\nu_d \approx 95$, used in Geary's apochromat example) are further toward the anomalous high-$\nu$ corner.

## 2. Secondary spectrum of an achromat

Take the thin achromat of L06 ($K_1 = KV_1/\Delta V$, $K_2 = -KV_2/\Delta V$ with $\Delta V = V_1 - V_2$, F and C at a common focus). The power change between F and another wavelength $x$ is $\delta K = K_1P_1/V_1 + K_2P_2/V_2$ with $P = P_{x,F}$-type partial dispersions, which simplifies to [Kidger Eq. 5.15; Geary Eq. 18.24]

$$
\boxed{\;\delta K_x = K\,\frac{P_1 - P_2}{V_1 - V_2},\qquad \delta f_x = -f\,\frac{P_1-P_2}{V_1-V_2}\;}
$$

The ratio $\Delta P/\Delta V$ is the **slope of the line joining the two glasses** on the partial-dispersion diagram. Every pair of *normal* glasses lies on the normal line, so it has the same slope ($-0.001682$ for $P_{g,F}$; about $-0.0005$ for $P_{F,d}$ [Kidger §5.1.3]) and therefore **the same secondary spectrum, whatever normal glasses you pick**: roughly $f/2000$ for the d focus relative to F/C, and $f/600$ for g. Kidger's example: a 5 m telescope doublet has 2.5 mm of secondary spectrum — a reason why large telescopes are reflectors [Kidger p. 97].

To reduce it you need a pair whose connecting line is **flatter** than the normal line: a high-$\nu$ crown *above* the line (N-FK51A, N-PK52A, CaF₂, FPL glasses) and/or a flint *below* it (N-KZFS short flints). $\Delta P/\Delta V = 0$ would give a two-glass **apochromat** — rare in practice with reasonable powers.

### 2.1 When does it matter?
At the F/C focus, the marginal ray of wavelength $x$ is defocused by $\delta f_x$, so its blur radius is about $\delta f_x\,u' = \delta f_x/(2N)$ [Geary §18.5]. Compare with the Airy radius $1.22\lambda N$:

$$
\frac{\text{blur radius}}{\text{Airy radius}} \approx \frac{\delta f_x}{2.44\,\lambda N^2}.
$$

Geary's 400 mm F/10 BK7/SF2 achromat has ≈ 0.20 mm of d-to-F/C secondary spectrum and a d blur diameter of ≈ 20 µm versus a 14.3 µm Airy diameter — "resolution will be limited not by diffraction but by secondary colour" [Geary §18.5, pp. 202–205]. Rules of thumb:
- Long focal length + low $N$ (fast) → secondary spectrum dominates: telescopes, long lenses, microscope objectives, wide-band machine-vision lenses at F/2–F/4 with small pixels.
- Narrow-band systems (laser, VCSEL, a single-colour LED) → irrelevant; even a singlet may do.
- A colour camera with a Bayer sensor sees the blue/red residual as coloured halos and as lower MTF in the blue channel.

## 3. Glass pairs compared (thin lens, $f = 100$ mm, F/5)

Using the table of §1 and $\delta f_g = -f\,\Delta P_{g,F}/\Delta\nu$ (g focus relative to the common F/C focus):

| Pair | $K_1/K$ | $K_2/K$ | slope $\Delta P/\Delta\nu$ | $\delta f_g$ (mm) | g blur radius (µm) | $Pf$ |
|---|---|---|---|---|---|---|
| N-BK7 / F2 | 2.31 | −1.31 | −1.72×10⁻³ | +0.172 | 17 | 0.71 |
| N-BK7 / N-SF5 | 2.01 | −1.01 | −1.99×10⁻³ | +0.199 | 20 | 0.72 |
| N-FK51A / F2 | 1.76 | −0.76 | −0.98×10⁻³ | +0.098 | 10 | 0.72 |
| N-FK51A / N-KZFS8 | 1.70 | −0.70 | −0.95×10⁻³ | +0.095 | 10 | 0.74 |
| N-FK51A / N-KZFS5 | 1.89 | −0.89 | −0.78×10⁻³ | +0.078 | 8 | 0.73 |
| **N-FK51A / N-KZFS11** | 2.01 | −1.01 | −0.59×10⁻³ | **+0.058** | 6 | 0.74 |
| N-FK51A / N-KZFS4 | 2.11 | −1.11 | −0.58×10⁻³ | +0.058 | 6 | 0.73 |
| N-PK52A / N-KZFS11 | 2.08 | −1.08 | −0.58×10⁻³ | +0.058 | 6 | 0.73 |

(Airy radius at F/5: 2.7 µm at 436 nm, 3.6 µm at 588 nm.) Check against L06: the thick N-BK7/N-SF5 doublet had the g focus 0.195 mm beyond the F/C focus — the thin-lens formula gives 0.199 mm.

Observations a professional would make:
- **N-FK51A + a KZFS short flint cuts the blue secondary spectrum ~3×** at the *same* element powers as N-BK7/N-SF5. That's the classic "ED / semi-apo doublet". Going to N-FK51A with a normal flint (F2) gives only ~1.8×, but with weaker elements (thanks to the larger $\Delta\nu$).
- **Nothing is free.** Petzval gets slightly worse (the crown index is low, 1.487). Fluor/phosphate crowns are soft, stain- and scratch-sensitive, have high thermal expansion and strongly negative $dn/dT$ (check the SCHOTT data sheet — important for athermal design, Course 03 L09), and cost several times more than N-BK7. Short flints and fluor crowns can also be more susceptible to climate/acid; specify coatings and handling accordingly.
- Geary's cautionary note applies: why not always use them? Because of higher-order aberrations, environmental susceptibility, manufacturability and cost [Geary §18.3, p. 202].

## 4. Three-glass apochromats

With three thin lenses in contact, impose power, primary colour and secondary colour [Geary §21.2, Eq. 21.2]:

$$
\sum_i K_i = K,\qquad \sum_i \frac{K_i}{V_i} = 0,\qquad \sum_i \frac{P_iK_i}{V_i} = 0 .
$$

This is a 3×3 linear system; Geary solves it with determinants, giving $K_1 = K\,V_1\Delta P_{32}/(V_1\Delta P_{32} + V_2\Delta P_{13} + V_3\Delta P_{21})$ and cyclic permutations [Geary Eqs. 21.13–21.15], but `numpy.linalg.solve` is quicker. With $P = P_{g,F}$ the g, F and C foci coincide (three colours); the remaining **tertiary spectrum** is typically a few µm per 100 mm [Geary §21.5: 4 µm for a 400 mm apochromat versus 203 µm for the achromat].

**Glass choice — the triangle rule** [Geary §21.5, p. 236]: two glasses may be near the normal line, the third should be well off it; maximise the area of the triangle the three glasses form on the $P$–$\nu$ diagram. Small triangles mean nearly singular equations and huge, opposing element powers.

**Worked mini-example** (thin lens, $f = 100$ mm, $P_{g,F}$ and $\nu_d$ from §1): searching all triples of the nine glasses for the smallest $\sum|K_i|$ gives **N-FK51A / N-KZFS11 / N-SF5** with

$$
K_{\text{N-FK51A}} = 2.382K,\quad K_{\text{N-KZFS11}} = -1.972K,\quad K_{\text{N-SF5}} = +0.590K
$$

i.e. $f_i$ = 41.99, −50.71, +169.4 mm; $\sum K_i/V_i = 0$ and $\sum P_iK_i/V_i = 0$ check to machine precision; $Pf = 0.75$. Note the surprising positive dense flint: what matters is the geometry of the triangle on the $P$–$\nu$ diagram, not the crown/flint labels. A triple of normal glasses (e.g. N-BK7/F2/N-SF5) is nearly singular and would demand absurd powers.

Geary's own example uses SSKN5 / FPL53 / BAK1 for a 400 mm apochromat ($f_i$ = 172.9, 120.9, −86.5 mm) [Geary §21.4, p. 232].

## 5. Air-spaced achromats

**Split (air-spaced) doublet** [Kidger §8.3]: un-cementing gives a fourth curvature, so $S_I = S_{II} = C_L = 0$ and $f' = 100$ can all be met with almost any reasonable glass pair (glass choice becomes less critical). Two families exist: the split **Fraunhofer** (shallow curves) and the **Gauss** doublet (flint convex to the front, steep curves, more higher-order aberration). A small air gap also reduces high-order spherical: the negative element works in the already-aberrated beam of the positive one (an *induced* aberration) [Kidger §8.3.1, p. 178]. Costs: one more surface pair to coat and align, more sensitive to decentre (Course 06).

**Dialyte** (widely separated achromat) [Geary §19.2]: when the lenses are separated, the colour condition must weight each lens by the square of its marginal-ray height:

$$
\frac{y_1^2K_1}{V_1} + \frac{y_2^2K_2}{V_2} = 0,\qquad K = K_1 + K_2 - tK_1K_2 .
$$

This is just $C_L = \sum y_i^2K_i/V_i = 0$ from the Seidel formula. It lets a small flint element correct a large crown element (historically for big refractors) and is the general principle behind colour correction in any multi-element lens: **elements where the marginal ray is high dominate axial colour; elements where the chief ray is high (far from the stop) dominate lateral colour** ($C_T \propto \bar y\,y\,K/V$ for a thin lens).

## 6. Colour in non-visible and mixed bands

Partial dispersion is defined for *any* wavelength set. For a camera that must see a blue projected pattern (≈ 460 nm) and work at 850 nm, define $V$ and $P$ for your own band edges and centre (L06 §4) and redraw the glass map — glasses that are "anomalous" in the visible may be ordinary in the NIR and vice versa. OpticStudio's Glass Map lets you choose the wavelengths used for the axes (check the settings of the Glass Map analysis).

## 7. In OpticStudio

**Glass tools** (Libraries tab; names may vary slightly by version):
- **Materials Catalog** — browse SCHOTT, OHARA, CDGM, HOYA…; each glass shows formula coefficients, $n_d$, $V_d$, $P_{g,F}$/$\Delta P$, thermal data, transmission, relative cost and climate/stain codes. Always look at the cost and environmental codes before falling in love with an anomalous glass.
- **Glass Map** — $n$ vs $V$ or $P$ vs $V$ plots of the active catalogs, with the glasses used in your lens highlighted.
- **Glass Compare** — overlay index and partial-dispersion curves of selected glasses.
- **System Explorer → Material Catalogs** — restrict which catalogs the optimiser may use (e.g. only SCHOTT + OHARA, or only your vendor's preferred list).

**Glass as a variable.**
- **Model glass** (Material solve → Model): $n_d$, $V_d$ and $\Delta P_{g,F}$ become continuous variables. Optimise, then pick the nearest real glass (the "fictitious glass" approach Kidger describes in §8.2.1). Constrain the model glass to physically realistic regions of the glass map, otherwise the optimiser invents glass that doesn't exist (OpticStudio provides an operand for this — look up "RGLA" in the Help; also keep $n_d$/$V_d$ bounded with operand limits).
- **Substitute solve** (Material solve → Substitute, optionally restricted to a catalog): marks a material as replaceable by catalog glasses. Ordinary (damped least squares) optimisation does not change it; **Hammer** optimisation (and Global search) does, trying discrete glass swaps and re-optimising. Hammer and Global search are available in Professional/Premium editions — fine with your Premium licence.
- Practical recipe: (1) optimise with Model glasses and continuous variables; (2) convert to the nearest real glasses (OpticStudio can do this conversion from the solve dialog or via the substitution tools; or by hand from the Glass Map); (3) mark the glasses Substitute with a restricted catalog list; (4) run Hammer for a while; (5) inspect cost, availability and thermal data of what it picked.

**Three-colour correction.** AXCL brings two wavelengths to a common paraxial focus; for an apochromat use two AXCL operands (e.g. F–C and g–C, via the operand's wavelength arguments — check them in the MFE) or, as Geary does, PARR (paraxial ray height at the image for each wavelength) + DIFF [Geary §21.5, Listing 21.2]. In the end, a polychromatic default merit function with sensible wavelength weights is what you actually optimise; the paraxial colour operands are scaffolding.

**Analyses:** Chromatic Focal Shift (achromat: parabola; apochromat: cubic through three points), Longitudinal Aberration (spherochromatism), Lateral Color, and the polychromatic FFT MTF.

## Worked example — how much does N-FK51A/N-KZFS11 buy over N-BK7/F2?

$f = 100$ mm, F/5, thin lenses, F/C at a common focus.
1. **N-BK7/F2:** $\Delta P_{g,F}/\Delta\nu = (0.5349 - 0.5828)/(64.17 - 36.37) = -1.72\times10^{-3}$ → $\delta f_g = +0.172$ mm; g blur radius $0.172/(2\cdot5) = 17$ µm vs Airy radius at g $1.22(0.4358)(5) = 2.7$ µm — blue light badly out of focus.
2. **N-FK51A/N-KZFS11:** $(0.5359 - 0.5605)/(84.47 - 42.41) = -5.85\times10^{-4}$ → $\delta f_g = +0.058$ mm (3× smaller), blur radius 6 µm. Element focal lengths $f_1 = 100\cdot(84.47-42.41)/84.47 = 49.8$ mm, $f_2 = -100\cdot42.06/42.41 = -99.2$ mm — essentially the same powers as N-BK7/N-SF5 in L06.
3. **Three-glass apochromat** N-FK51A/N-KZFS11/N-SF5: g, F, C coincide; $f_i$ = 42.0, −50.7, +169.4 mm. More, stronger elements → more higher-order aberration to manage, and three-element mounting tolerances.

Whether step 2 or 3 is worth it is decided by the blur budget: for 3.45 µm pixels (a typical 5 MP machine-vision sensor) a 17 µm blue blur is unacceptable, 6 µm is borderline, and the apochromat (few µm of tertiary spectrum per 100 mm) is clean.

## Key takeaways
- Partial dispersion $P_{x,y}$ describes how dispersion is distributed across the band; most glasses lie on the normal line $P_{g,F} = 0.6438 - 0.001682\nu_d$.
- Secondary spectrum $\delta f = -f\,\Delta P/\Delta V$: any two normal glasses give ≈ $f/2000$ (d) and ≈ $f/600$ (g); only anomalous glasses (FK/PK/CaF₂ crowns, KZFS short flints) flatten the slope.
- N-FK51A/N-KZFS11 reduces blue secondary spectrum ~3× at the same element powers; costs: Petzval, thermal behaviour, fragility, price.
- Three-glass apochromat: solve the 3×3 system; choose glasses forming a large triangle on the $P$–$\nu$ diagram.
- Air-spaced doublets add a free curvature (aplanat with almost any glasses); colour of separated elements is weighted by $y^2$ (axial) and $y\bar y$ (lateral).
- In OpticStudio: Model glass → real glass → Substitute + Hammer, with catalog restrictions; check cost and environmental codes.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Relative partial dispersion $P_{x,y}$ | $(n_x - n_y)/(n_F - n_C)$ |
| Normal line | Straight line in the $P$–$\nu$ diagram on which most glasses lie |
| $\Delta P_{g,F}$ | Deviation of a glass's $P_{g,F}$ from the normal line ("anomalous partial dispersion") |
| Secondary spectrum | Residual focus spread of an achromat (other wavelengths vs the common F/C focus) |
| Tertiary spectrum | Residual focus spread of an apochromat |
| Apochromat | Three wavelengths brought to a common focus (usually three glasses) |
| Short flint (KZFS) | Flint with below-normal blue partial dispersion |
| Fluor / phosphate crown | High-$\nu$ crowns with above-normal partial dispersion (N-FK51A, N-PK52A) |
| Dialyte | Widely separated two-element achromat |
| Model glass / Substitute solve | OpticStudio mechanisms to vary glass continuously / by catalog swaps (Hammer) |

## References
1. [Geary] Ch. 18 "Secondary Color" pp. 195–206; Ch. 19 "Large Air-Spaced Achromat and French Landscape Lens" pp. 207–220 (§19.2–19.3); Ch. 21 "Apochromat" pp. 229–237.
2. [Kidger] §5.1.3 pp. 94–97; §8.2.1 pp. 171–172; §8.3–8.4 pp. 177–183.
3. SCHOTT AG online glass data sheets (values used here): N-FK51A <https://www.schott.com/shop/advanced-optics/en/Optical-Glass/N-FK51A/c/glass-N-FK51A>, N-KZFS11 <https://www.schott.com/shop/advanced-optics/en/Optical-Glass/N-KZFS11/c/glass-N-KZFS11>; the N-PK52A, N-KZFS4/5/8, F2 and N-SF5 pages are in the same shop (search the glass name).
4. J. Greivenkamp, OPTI 502 "Materials", Univ. of Arizona — <https://wp.optics.arizona.edu/jgreivenkamp/wp-content/uploads/sites/11/2019/08/502-17-Materials.pdf>
5. SCHOTT, "Optical Glass – Data Sheets" collection (PDF, older edition with full Sellmeier/thermal data) — <https://uio.no/studier/emner/matnat/fys/FYS2150/v17/kursmateriell/datablader-og-brukermanualer/schott-optical-glass-collection-datasheets-english-17012017.pdf>
