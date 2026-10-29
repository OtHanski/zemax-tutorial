# L05 — Optical Glass and Dispersion

> **Course 01 · Foundations** · Estimated time: lecture ~2.5 h, tasks ~4 h
> **Prerequisites:** [L03](../L03-paraxial-optics-and-ray-tracing/), [L04](../L04-stops-pupils-fields/) · **Next:** [L06 — Real rays and analysis tools](../L06-real-rays-and-analysis-tools/)

## Learning objectives
- Explain the physical origin of dispersion (absorption resonances in the UV and IR) and why index falls with wavelength across the visible ("normal dispersion").
- Evaluate refractive index from the Sellmeier formula and compute $n_d$, Abbe number $V_d$, and relative partial dispersions $P_{g,F}$ and $p = (n_F - n_d)/(n_F - n_C)$ for catalog glasses.
- Read the $n_d$–$V_d$ glass map (crowns vs. flints, glass families) and the partial-dispersion diagram, and explain why normal glasses limit secondary-spectrum correction.
- Estimate axial colour of a singlet ($\Delta f \approx f/V$) and the powers of a thin achromatic doublet ($\phi_1 = \phi V_1/(V_1 - V_2)$).
- Use OpticStudio's material tools (Materials Catalog, Glass Map, Dispersion Diagram, Glass Compare, Prescription index table) and choose glasses with practical criteria (availability, cost, chemical resistance, transmission, thermal behaviour, NIR dispersion).

## Reading
- **Core:** [Geary §6.2, pp. 51–58] — refractive index, dispersion, standard spectral lines (Table 6.1), Abbe number with the K7 vs. TiF1 comparison (Table 6.2), the glass chart, melt data, partial dispersion.
- **Core:** [Kidger §5.1, pp. 91–97] — the Schott dispersion polynomial, history of the achromat, thin-lens axial colour, Abbe V-value with the table of spectral lines, glass diagram, secondary spectrum and relative partial dispersion (Eqs. 5.6–5.15), lateral colour introduction.
- **Core:** [Kenyon §1.6, pp. 19–22] — absorption and dispersion overview, index curves for glass, fused silica, MgF₂, the Sellmeier formula, Beer's law.
- **Optional:** [Kenyon §11.5, pp. 304–308] — the classical oscillator model: why every absorption band is accompanied by a dispersion feature.
- **Optional online:** SCHOTT optical glass data sheets / catalog (manufacturer source of the coefficients OpticStudio uses); Ansys KB article on table glass (how to add your own material).

---

## 1. Why the index depends on wavelength

Light slows down in glass because its electric field drives the bound electrons (and, at long wavelengths, the ions) of the material into forced oscillation; the re-radiated waves add to the incident wave with a phase lag. Kenyon models each electron as a damped harmonic oscillator with resonance frequency $\omega_0$ [Kenyon §11.5.1, pp. 305–307]. Below resonance the material responds in phase and $n > 1$; as the driving frequency approaches resonance the response, and therefore $n$, grows; at resonance there is strong **absorption**.

Optical glasses have electronic resonances in the **ultraviolet** and lattice (vibrational) resonances in the **infrared**. In between — the transparent window — the index *rises towards the blue* because we are approaching the UV resonances. That is **normal dispersion** [Kenyon §1.6, p. 20; §11.5, pp. 304–305]. Close to an absorption band the index varies steeply, which is why high-index flint glasses (with UV absorption edges closer to the visible) are both more dispersive and less transmissive in the blue.

Transmission windows (approximate, from Kenyon §1.6, p. 21): crown glass 350–2000 nm, flint glass 420–2300 nm, fused silica 260–2500 nm, MgF₂ 120–8000 nm. All the common glasses transmit well at 850 and 940 nm — the NIR wavelengths typical for structured-light 3D cameras.

---

## 2. Describing dispersion: formulas

### 2.1 Sellmeier
The physically motivated fit (each term ≈ one resonance at wavelength $\sqrt{C_i}$):

$$
n^2(\lambda) - 1 = \sum_{i=1}^{3}\frac{B_i\,\lambda^2}{\lambda^2 - C_i}, \qquad \lambda \text{ in µm}, \; C_i \text{ in µm}^2 .
$$

(Kenyon prints a shortened version, $n^2 = 1 + \sum B_i/(\lambda^2 - C_i)$ [Kenyon Eq. 1.27, p. 21]; the manufacturers' form, used by SCHOTT and OpticStudio, is the one above.) For N-BK7, $C_1 = 0.0060$, $C_2 = 0.0200$ µm² correspond to UV resonances at ~77 nm and ~141 nm; $C_3 = 103.56$ µm² to an IR resonance near 10 µm.

### 2.2 Other formulas
The older **Schott formula** $n^2 = A_0 + A_1\lambda^2 + A_2\lambda^{-2} + A_3\lambda^{-4} + A_4\lambda^{-6} + A_5\lambda^{-8}$ [Kidger Eq. 5.1, p. 91] is a pure polynomial fit; it is accurate inside its fitting range and poor outside. Geary notes that SCHOTT replaced BK7 with lead/arsenic-free N-BK7 and moved to Sellmeier coefficients [Geary §6.2.4 footnote, p. 55]. OpticStudio supports many formulas (Schott, Sellmeier 1–5, Conrady, Herzberger, Extended, …) plus **table glass** files with measured index–wavelength pairs and spline interpolation (`.ZTG`). **Never extrapolate** a dispersion fit outside the wavelength range for which the manufacturer specifies it — OpticStudio warns when a wavelength is outside a glass's valid range.

---

## 3. Summarizing dispersion: index, Abbe number, partial dispersion

### 3.1 Reference wavelengths
The traditional spectral lines (Fraunhofer and lamp lines) [Geary Table 6.1, p. 52; Kidger §5.1.2, p. 93]:

| Line | λ (nm) | Source |
|---|---|---|
| i | 365.01 | Hg (UV) |
| h | 404.66 | Hg violet |
| g | 435.83 | Hg blue |
| F′ | 479.99 | Cd blue |
| F | 486.13 | H blue |
| e | 546.07 | Hg green |
| d | 587.56 | He yellow |
| D | 589.3 | Na yellow |
| C′ | 643.85 | Cd red |
| C | 656.27 | H red |
| r | 706.52 | He red |

Most design work uses **F, d, C** (with d as primary); European practice sometimes uses **F′, e, C′** (e is closer to the eye's peak sensitivity) [Kidger §5.1.2, p. 93].

### 3.2 Abbe number
$$
V_d = \frac{n_d - 1}{n_F - n_C}.
$$

It is the reciprocal of a "relative dispersion" — high $V$ = *low* dispersion [Geary Eq. 6.4, p. 54; Kidger Eq. 5.5, p. 93]. Why that particular combination? For a thin lens $\phi = (n-1)(c_1 - c_2)$, so the change of power between F and C is

$$
\delta\phi = (n_F - n_C)(c_1 - c_2) = \frac{\phi}{V} \quad\Rightarrow\quad \delta f \approx -\frac{f}{V}
$$

[Kidger Eq. 5.3, p. 92]. The Abbe number *directly* gives the axial colour of a thin lens: a 100 mm N-BK7 singlet ($V_d = 64.17$) has F-to-C focal spread ≈ 1.56 mm.

Geary's illustrative pair (Table 6.2, p. 55): K7 and TiF1 have almost the same $n_d$ (≈1.511), but $n_F - n_C$ of 0.00846 vs. 0.01002 gives $V_d$ = 60.4 vs. 51.0.

**Crowns and flints:** traditionally glasses with $V_d > 50$ (for $n_d < 1.60$; the boundary bends to $V_d > 55$ at higher indices) are **crowns**, the rest **flints** [Geary §6.2.4, pp. 54–55]. The letter codes in SCHOTT names tell the family: K = crown (Kron), BK = borosilicate crown, SK = dense crown, LAK = lanthanum crown, F = flint, SF = dense flint, LF = light flint, etc. The "N-" prefix means the lead- and arsenic-free (environmentally compliant) version.

### 3.3 Partial dispersion and secondary spectrum
The index curve is not a straight line, so knowing $n_F - n_C$ does not tell you how the dispersion is distributed within the band. The **relative partial dispersion** captures that. Two common forms:

$$
P_{g,F} = \frac{n_g - n_F}{n_F - n_C} \quad(\text{SCHOTT catalogue}),\qquad
p = \frac{n_F - n_d}{n_F - n_C}\quad(\text{Kidger Eq. 5.11}).
$$

Plotted against $V_d$, most glasses fall on (or near) a straight **"normal line"** [Geary §6.2.6, p. 55; Kidger Fig. 5.5, p. 96]. Kidger shows that a thin achromatic doublet corrected for F and C has a residual d-to-F focus error [Kidger Eq. 5.15, p. 96]

$$
\frac{\delta\phi_{d-F}}{\phi} = \frac{p_1 - p_2}{V_1 - V_2},
$$

and for normal glasses this ratio is about −0.0005 for this set of wavelengths: a 5 m focal-length doublet keeps ~2.5 mm of residual colour — the **secondary spectrum** [Kidger pp. 96–97]. Fixing it requires glasses off the normal line ("abnormal partial dispersion": fluor-crowns like N-FK51A, short flints like N-KZFS…) — Course 02 L07.

### 3.4 Glass maps
The **$n_d$–$V_d$ diagram** (SCHOTT's glass map; note $V_d$ increases to the *left* by tradition) is the designer's menu [Kidger Fig. 5.3, p. 94; Geary §6.2.4]. Patterns to remember:
- High index comes with high dispersion (top right): the "glass line" runs from low-index crowns (bottom left, $n \approx 1.5$, $V \approx 65$) to dense flints (top right, $n \approx 1.9$, $V \approx 20$).
- Lanthanum glasses (LAK, LAF, LASF) occupy the top-left: high index *and* relatively low dispersion — valuable for reducing Petzval curvature and surface curvatures, but expensive and dense.
- Fluor crowns (FK) at the far left: very low dispersion, abnormal partial dispersion.

---

## 4. Glass is more than $n$ and $V$

Professionals choose glass from a short list. Criteria beyond $n_d$, $V_d$:

| Property | Why it matters |
|---|---|
| **Availability / status** | Catalogues mark glasses as *preferred*, standard, inquiry, obsolete. Prefer preferred glasses; obsolete glass = redesign later. |
| **Relative cost** | Ranges from 1 (N-BK7) to > 30× for some lanthanum or fluor glasses. |
| **Internal transmission** | Dense flints absorb in the blue/UV; check at your wavelengths and thicknesses (Beer's law, $I = I_0 e^{-\alpha s}$ [Kenyon Eq. 1.28, p. 22]). |
| **Chemical & climatic resistance** (CR, FR, SR, AR, PR classes) | Staining and weathering during polishing and in the field. |
| **Thermal properties** (dn/dT, CTE) | Focus shift with temperature — critical for industrial cameras (Course 03 L09). |
| **Density, hardness, bubble class** | Weight, manufacturability. |
| **Melt data** | The real melt differs from catalogue values in the third or fourth decimal; for sensitive designs, re-optimize with measured melt indices before fabrication [Geary §6.2.5, p. 55]. |

**Plastics** (PMMA, polycarbonate, cyclo-olefin polymers such as Zeonex E48R) offer molding of aspheres at low cost but have high dn/dT, high CTE, low index and a narrow selection ($n \approx 1.49$–$1.59$, $V \approx 30$–$57$) — Course 04 L07. In OpticStudio they live in the MISC catalogue and in manufacturer catalogues (e.g. ZEON; names can differ from the trade names — search the Materials Catalog).

### 4.1 NIR design: dispersion almost disappears
Dispersion is strongest near the UV resonances; in the near-IR the index curve is much flatter. Defining an "NIR Abbe number" for an 800–900 nm band, $V_{\text{NIR}} = (n_{850} - 1)/(n_{800} - n_{900})$, gives ≈ 287 for N-BK7 and ≈ 152 for N-SF6 (vs. 64 and 25 in the visible). A structured-light camera working with a narrow 850 nm LED band (±25 nm) therefore has far less chromatic aberration than a visible camera — but the **focus shift between visible and NIR** is large (≈ 1.35 mm for our singlet from 587.6 to 850 nm), which matters if the same lens must work for both colour texture and NIR depth. Kidger's advice: for a non-visible band, make your own glass diagram at the relevant wavelengths [Kidger §5.1.2, p. 93].

---

## 5. In OpticStudio

- **Material catalogs:** System Explorer → Material Catalogs selects which catalogues (`.AGF` files: SCHOTT, OHARA, HOYA, CDGM, SUMITA, MISC, INFRARED, …) are searched. A material name in the LDE must exist in a loaded catalogue.
- **Materials Catalog tool** (Libraries tab): browse a glass's formula and coefficients, valid wavelength range, $n_d$, $V_d$, partial dispersion, thermal data (dn/dT constants, CTE), transmission data, relative cost, climate/stain/acid/alkali resistance codes and status. You can also add or edit glasses and catalogues here.
- **Materials analyses** (Libraries → Materials Analyses): **Glass Map** (any two of index, Abbe, partial dispersion, for the selected catalogues; useful to visualize candidates), **Dispersion Diagram** (n vs λ), **Glass Compare** (side-by-side properties), internal transmission vs. wavelength. Exact menu names vary slightly by version.
- **Index at your wavelengths:** the Prescription Data report lists the index of every material at every system wavelength [Geary §2.7, p. 19] — the quickest way to sanity-check.
- **Model glass:** instead of a catalogue glass you can use a "model" material described by $n_d$, $V_d$ and $\Delta P_{g,F}$ (set via the solve box on the Material cell). During early optimization $n_d$ and $V_d$ can be variables; afterwards you *substitute* the nearest real glass. Glass substitution in Hammer/Global optimization is covered in Course 03 L05.
- **Wavelength settings:** System Explorer → Wavelengths. Presets (F, d, C; F′, e, C′; single lines), weights (spectral weighting of your source/sensor), primary wavelength. For an NIR camera, enter e.g. 0.825, 0.850, 0.875 µm with weights following the LED spectrum.
- **Operands** you'll use later: `AXCL` (axial colour), `LACL` (lateral colour).
- **Pitfalls:**
  - Wavelengths outside the glass's valid range (warning in the LDE / Prescription).
  - Forgetting to load a catalogue → the material name turns red / errors.
  - Comparing $V_d$ numbers when your system is not at d: compute dispersion at *your* band.
  - Environment: System Explorer → Environment sets temperature and pressure; indices are relative to air at that condition. Thermal analysis is Course 03 L09.

---

## Worked example — dispersion data and the singlet's colour

**(a) N-BK7 from the Sellmeier coefficients** (SCHOTT: $B$ = 1.03961212, 0.231792344, 1.01046945; $C$ = 0.00600069867, 0.0200179144, 103.560653 µm²):

| λ (µm) | 0.4861 (F) | 0.5876 (d) | 0.6563 (C) | 0.4358 (g) | 0.850 | 0.940 |
|---|---|---|---|---|---|---|
| $n$ | 1.52238 | 1.51680 | 1.51432 | 1.52668 | 1.50984 | 1.50837 |

$V_d = 0.51680/(1.52238 - 1.51432) = 64.17$; $P_{g,F} = (1.52668 - 1.52238)/0.00805 = 0.5349$ (catalogue: 64.17 and 0.5349 ✓).

**(b) A small palette** (computed from SCHOTT Sellmeier data):

| Glass | $n_d$ | $V_d$ | $P_{g,F}$ | $n$ @ 850 nm | type |
|---|---|---|---|---|---|
| N-BK7 | 1.51680 | 64.17 | 0.5349 | 1.50984 | borosilicate crown |
| N-SK16 | 1.62041 | 60.32 | 0.5412 | 1.61172 | dense crown |
| N-LAK9 | 1.69100 | 54.71 | 0.5447 | 1.68038 | lanthanum crown |
| F2 | 1.62004 | 36.37 | 0.5828 | 1.60677 | flint (lead) |
| N-SF5 | 1.67271 | 32.25 | 0.5984 | 1.65669 | dense flint |
| N-SF6 | 1.80518 | 25.36 | 0.6158 | 1.78155 | dense flint |

Note how $P_{g,F}$ rises as $V_d$ falls — the normal line.

**(c) Axial colour of the Course 01 singlet.** Thin-lens estimate $f/V_d = 100/64.17 = 1.56$ mm. Paraxial trace of the real thick lens: EFL(F) = 98.962 mm, EFL(C) = 100.505 mm → 1.54 mm; BFL(F) = 97.639, BFL(C) = 99.175 mm. At F/5 the marginal ray slope is ±1/10, so midway between the F and C foci the geometric blur *diameter* from colour alone is about $1.54/10 \approx 0.15$ mm — larger than the monochromatic spherical-aberration blur. This is why the polychromatic spots in L01 were bigger than the d-light spots.

**(d) Preview: a thin achromat** with N-BK7 ($V_1 = 64.17$) and N-SF5 ($V_2 = 32.25$), $f = 100$ mm [Kidger Eq. 5.8, p. 95]:
$$
\phi_1 = \frac{\phi V_1}{V_1 - V_2} = \frac{0.01 \times 64.17}{31.92} = 0.020103\ \Rightarrow f_1 = 49.74\ \text{mm},\qquad \phi_2 = \frac{-\phi V_2}{V_1 - V_2} \Rightarrow f_2 = -98.96\ \text{mm}.
$$
Checking with the Sellmeier indices: F and C now focus together at 100.052 mm while d focuses at 100.000 mm — a residual secondary spectrum of 0.052 mm ≈ $f/1900$, matching Kidger's "−0.0005" rule ($p_1 = 0.6924$, $p_2 = 0.7090$, $(p_1 - p_2)/(V_1 - V_2) = -0.00052$). Compared to the singlet's 1.54 mm, the doublet reduces axial colour ~30×. You'll design it properly in Course 02 L06.

**(e) NIR.** The same singlet at 825/850/875 nm: EFL = 101.295/101.385/101.470 mm. A 50 nm wide NIR band gives only 0.18 mm of axial colour — 9× less than F–C — but the 850 nm focus lies 1.35 mm behind the d-light focus.

---

## Key takeaways
- Dispersion comes from UV (electronic) and IR (lattice) resonances; in the transparent window index falls with wavelength.
- Use Sellmeier (or the manufacturer's formula) within its valid range; never extrapolate.
- $V_d = (n_d-1)/(n_F-n_C)$ measures relative dispersion; thin-lens axial colour $\approx f/V$.
- Partial dispersion ($P_{g,F}$, $p$) lies near a "normal line"; the residual secondary spectrum of a normal-glass achromat is ≈ $f/2000$.
- Choose glass from the map *and* by availability, cost, transmission, chemical/climatic resistance, thermal behaviour and melt data.
- In the NIR, dispersion is small; design with a glass diagram at your actual wavelengths.
- OpticStudio: Material Catalogs in System Explorer, Libraries → Materials Catalog / Materials Analyses (Glass Map, Dispersion Diagram, Glass Compare), index table in Prescription Data.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Dispersion | Variation of refractive index with wavelength |
| Normal dispersion | Index decreasing with increasing wavelength |
| Sellmeier formula | $n^2 - 1 = \sum B_i\lambda^2/(\lambda^2 - C_i)$ |
| $n_d$ | Index at the helium d-line (587.56 nm) |
| Abbe number $V_d$ | $(n_d - 1)/(n_F - n_C)$ |
| Crown / flint | Low-dispersion ($V_d \gtrsim 50$) / high-dispersion glasses |
| Relative partial dispersion | $P_{g,F} = (n_g - n_F)/(n_F - n_C)$ (or Kidger's $p$) |
| Normal line | Approximately linear relation of $P$ vs. $V$ for most glasses |
| Secondary spectrum | Residual colour of an F–C corrected achromat |
| Axial (longitudinal) colour | Wavelength dependence of focus position |
| Lateral colour | Wavelength dependence of image height |
| Melt data | Measured indices of the actual glass melt |
| Glass map | $n_d$ vs. $V_d$ diagram |
| Model glass | Fictitious material defined by $n_d$, $V_d$ (and $\Delta P$) |
| AGF | OpticStudio glass catalogue file format |

## References
1. [Geary §6.2, pp. 51–58] Geary, *Introduction to Lens Design*: refractive index, dispersion, spectral lines (Table 6.1), Abbe number (Table 6.2), glass chart, melt data, partial dispersion.
2. [Kidger §5.1, pp. 91–97] Kidger, *Fundamental Optical Design*: dispersion formula, thin-lens axial colour, Abbe V-value, glass diagram, secondary spectrum, partial dispersion, lateral colour.
3. [Kenyon §1.6, pp. 19–22] Kenyon, *The Light Fantastic*: absorption and dispersion, Sellmeier formula, Beer's law.
4. [Kenyon §11.5, pp. 304–308] dispersion and absorption, the atomic oscillator model.
5. Ansys Optics knowledge base, "Using table glass in OpticStudio" — `.ZTG` format, spline interpolation, and the Dispersion Diagram path (Libraries → Materials Analyses → Dispersion Diagram): https://optics.ansys.com/hc/en-us/articles/42661868597395
6. opticalglass (Python package, readthedocs) — open-source reader for glass catalogues (SCHOTT, OHARA, HOYA, CDGM…) useful for scripting glass maps outside OpticStudio: https://opticalglass.readthedocs.io/en/latest/OG_Overview.html
