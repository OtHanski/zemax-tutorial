# L09 — Thermal and environmental analysis, athermalization

> **Course 03 · Image quality, optimization and physical optics** · Estimated time: lecture ~2.5 h, tasks ~6 h
> **Prerequisites:** [L03 — Depth of focus and budgets](../L03-strehl-wavefront-error-depth-of-focus/), [L06 — Multi-configuration](../L06-multi-configuration-and-zoom/), [Course 01 L05 (glass)](../../01-foundations/L05-optical-glass-and-dispersion/) · **Next:** [L10 — Starting points and design strategy](../L10-starting-points-and-design-strategy/)

## Learning objectives
- Compute the temperature dependence of a glass index from the SCHOTT $D_0, D_1, D_2, E_0, E_1, \lambda_{TK}$ model, and distinguish absolute from relative (to air) $dn/dT$.
- Derive the thermo-optic coefficient of a thin lens, $\beta = \dfrac{dn_\text{rel}/dT}{n-1} - \alpha$, and use it with the mount CTE to predict thermal defocus of a camera.
- Set up a thermal analysis in OpticStudio (Environment settings, TCE data, Make Thermal, `TEMP`/`PRES` MC operands, thermal pickups) and evaluate image quality over an industrial range such as 0–45 °C.
- Choose athermalization strategies: glass choice (athermal glasses, achromatic–athermal pairs), mount design (material choice, re-entrant spacers), plastic/glass hybrids, active compensation.
- Account for pressure/altitude and source-wavelength drift with temperature.

## Reading
- **Core:** [Kidger §12.5.2, p. 250] — short but to the point: large thermo-optic coefficients alter focus; athermalization is passive (mount materials) or active (sensors and motors). (Kidger's context is IR materials such as germanium, where the effect is ~100× larger than in optical glass — the logic is identical.)
- **Core (online):** SCHOTT Technical Information TIE-19, *Temperature Coefficient of the Refractive Index* (Aug. 2023): <https://media.schott.com/api/public/content/0dcd87a2d36942a3946d033f0a9065e6> — the dn/dT formula, absolute vs relative coefficients, the athermal constant $G$, and the "truly athermal" glasses (N-PK51, N-FK58, N-PK52A, N-FK51A).
- **Core (online):** Ansys KB (N.-H. Kim), thermal modeling in OpticStudio — Adjust Index Data To Environment, thermal pickups, spacer expansion model, Make Thermal, Hammer-based athermalization: <https://optics.ansys.com/hc/en-us/articles/43071134350995>
- **Optional:** ZOS-API example 18 (builds a thermal MCE manually with `TEMP`, `PRES`, `CRVT`, `THIC`, `GLSS`, `SDIA` and thermal pickups): <https://developer.ansys.com/docs/zemax-opticstudio-zos-api-2026-r1/apiexamples/example_18_cs.md>
- **Optional:** Zemax Community, "Using STAR with other thermal and position settings" (when uniform-temperature models are not enough): <https://community.zemax.com/star-module-user-group-85/using-star-with-other-thermal-and-position-settings-in-opticstudio-4986>
- **Refresh:** Course 03 L03 §5 (budgets) and L06 (MCE).

---

## 1. Why temperature matters for an industrial camera

An industrial 3D camera is specified for something like 0–45 °C operation (and wider for storage). Over that range:
- glass indices change by ~10⁻⁵ (more for dense flints, much more for plastics);
- glass and mount dimensions change by ~10⁻⁵–10⁻³;
- the source wavelength drifts (VCSELs typically ≈ 0.06–0.07 nm/K, edge-emitting diodes ≈ 0.25–0.3 nm/K — check the datasheet);
- the air index changes slightly with temperature and pressure.

For a fast NIR lens with a diffraction depth of focus of ±7–15 µm (L03), a few µm of thermal focus shift consumes a large part of the budget, and the calibration of a 3D camera (intrinsics, distortion, baseline) also drifts with temperature. Kidger's two options — make the effects cancel (passive) or compensate them (active) — remain the only options [Kidger §12.5.2].

## 2. Thermal behaviour of glass

### 2.1 Index: the SCHOTT model
SCHOTT describes the change of the **absolute** index (relative to vacuum) with temperature by [TIE-19, Eqs. 2–4]:

$$
\Delta n_\text{abs}(\lambda,T) = \frac{n^2(\lambda,T_0) - 1}{2\,n(\lambda,T_0)}\left[D_0\Delta T + D_1\Delta T^2 + D_2\Delta T^3 + \frac{E_0\Delta T + E_1\Delta T^2}{\lambda^2 - \lambda_{TK}^2}\right],
$$

$$
\frac{dn_\text{abs}}{dT} = \frac{n^2-1}{2n}\left[D_0 + 2D_1\Delta T + 3D_2\Delta T^2 + \frac{E_0 + 2E_1\Delta T}{\lambda^2-\lambda_{TK}^2}\right],
$$

with $T_0 = 20$ °C, $\Delta T = T - T_0$, λ in µm, and glass-specific constants from the data sheet (valid roughly −100…+140 °C and 0.365–1.014 µm). The $\lambda_{TK}$ term makes dn/dT larger at short wavelengths, especially in high-dispersion glasses.

Lens designers need the **relative** index (relative to air at the same temperature and pressure), because rays travel in air. Since $n_\text{rel} = n_\text{abs}/n_\text{air}$ [TIE-19 Eq. 5–7] and $dn_\text{air}/dT \approx -0.93\times10^{-6}$ /K near 20 °C and 1 atm,

$$
\frac{dn_\text{rel}}{dT} \approx \frac{dn_\text{abs}}{dT} - n\,\frac{dn_\text{air}}{dT} \approx \frac{dn_\text{abs}}{dT} + 0.93\times10^{-6}\,n .
$$

**N-BK7 check** (data-sheet constants $D_0 = 1.86\times10^{-6}$, $D_1 = 1.31\times10^{-8}$, $D_2 = -1.37\times10^{-11}$, $E_0 = 4.34\times10^{-7}$, $E_1 = 6.27\times10^{-10}$, $\lambda_{TK} = 0.17$ µm): average absolute dn/dT over 20–40 °C at the e-line (546 nm) = 1.62×10⁻⁶/K → relative ≈ 3.0×10⁻⁶/K, matching TIE-19's table value (3.00×10⁻⁶/K); at 940 nm: absolute 1.12×10⁻⁶/K, relative ≈ 2.5×10⁻⁶/K. Over 0–45 °C the absolute index of N-BK7 at 940 nm changes by −1.76×10⁻⁵ (at 0 °C) to +2.86×10⁻⁵ (at 45 °C) relative to 20 °C.

Typical magnitudes (relative dn/dT, visible): crown glasses +1…+4×10⁻⁶/K; dense flints and lanthanum glasses up to +10…+15×10⁻⁶/K; fluor-/phosphate crowns (N-PK51, N-FK51A …) *negative*, e.g. N-PK51 ≈ −6.7×10⁻⁶/K [TIE-19]; optical plastics ≈ −1×10⁻⁴/K (PMMA, polycarbonate, cyclo-olefins — check supplier data), i.e. 30–100× larger and of opposite sign.

### 2.2 Expansion
The coefficient of thermal expansion (CTE, TCE in OpticStudio) of glass is typically 5–10×10⁻⁶/K (N-BK7: 7.1×10⁻⁶/K for −30/+70 °C [TIE-19]); plastics 6–7×10⁻⁵/K; aluminium ≈ 23–24×10⁻⁶/K; stainless steels ≈ 10–17×10⁻⁶/K (alloy-dependent); titanium ≈ 8.6×10⁻⁶/K; Invar ≈ 1×10⁻⁶/K; engineering plastics for spacers ≈ 5–12×10⁻⁵/K (unfilled) — always use the supplier's value for your alloy/grade.

### 2.3 The thermo-optic coefficient of a lens
A thin lens has power $\varphi = (n-1)(c_1 - c_2)$. With temperature, curvatures scale as $1/(1+\alpha\Delta T)$ (uniform expansion) and $n$ changes:

$$
\frac{1}{\varphi}\frac{d\varphi}{dT} = \frac{dn_\text{rel}/dT}{n-1} - \alpha \equiv \beta,\qquad \frac{1}{f}\frac{df}{dT} = -\beta .
$$

$\beta$ (often called the thermo-optic or opto-thermal coefficient; some texts use the opposite sign convention for "$\delta$") is a *material property for a given wavelength*. TIE-19's "athermal constant" $G = \alpha(n-1) + dn_\text{rel}/dT$ is the analogous quantity for optical path through a plate: $d(\text{OPL})/dT = G\,d$ per unit thickness (N-BK7: $G$ = 6.68×10⁻⁶/K).

| Material (at ~940 nm) | $dn_\text{rel}/dT$ (/K) | α (/K) | $\beta$ (/K) | f change for f = 8 mm, +25 K |
|---|---|---|---|---|
| N-BK7 | ≈ +2.5×10⁻⁶ | 7.1×10⁻⁶ | ≈ −2.1×10⁻⁶ | +0.43 µm |
| PMMA (typical values) | ≈ −1.05×10⁻⁴ | ≈ 6.5×10⁻⁵ | ≈ −2.8×10⁻⁴ | +56 µm |

The glass lens barely changes; the plastic lens changes by ~56 µm — far beyond any depth of focus. That is why molded-plastic camera lenses (Course 04 L07) are designed with care for thermal compensation (combining plastic elements of opposite power, or a glass element carrying most of the power).

## 3. Thermal defocus of a camera

For a lens focused at infinity, the image lies ≈ $f$ behind the lens; the mount holding the sensor at that distance expands with its own CTE $\alpha_h$. To first order the image–sensor mismatch per kelvin is

$$
\frac{d\delta}{dT} \approx (\alpha_h + \beta)\,f \quad(\text{sensor moves } \alpha_h f,\ \text{image moves } -\beta f).
$$

**Passive athermalization condition:** $\beta_\text{system} = -\alpha_h$.

For a single N-BK7 lens at 940 nm in an aluminium barrel: $(23.6 - 2.1)\times10^{-6}\times f$ → 0.17 µm/K for f = 8 mm (4.3 µm over +25 K) and 0.54 µm/K for f = 25 mm (13.4 µm over +25 K). Compare with the diffraction DOF at F/2.8 and 940 nm, ±14.7 µm: a 25 mm lens would use up essentially the whole focus budget with temperature alone. Real multi-element lenses have system $\beta$ values that differ from any single glass; the MCE thermal model computes them exactly.

### 3.1 Athermalization strategies
1. **Mount design.** Choose a barrel/spacer material whose CTE matches $-\beta$, or build a **re-entrant (compound) spacer** from two materials whose expansions subtract: with outer length $L_A$ (CTE $\alpha_A$) and inner, reversed length $L_B$ (CTE $\alpha_B$), net length $L = L_A - L_B$ and effective expansion $\alpha_\text{eff}L = \alpha_AL_A - \alpha_BL_B$. Example: need $\alpha_\text{eff} = 2.15\times10^{-6}$/K over 25 mm with an aluminium tube (23.6) and a plastic insert (≈110×10⁻⁶/K, assumed): $L_A = 31.2$ mm, $L_B = 6.2$ mm.
2. **Glass choice.** Use the glass map in the (dispersion, β) plane: an **achromatic–athermal** doublet must satisfy $\varphi_1+\varphi_2 = \varphi$, $\varphi_1/V_1 + \varphi_2/V_2 = 0$ and $\varphi_1\beta_1 + \varphi_2\beta_2 = -\alpha_h\varphi$ — three conditions, two powers, so the glass pair must be chosen to satisfy the third. Negative-dn/dT glasses (N-PK51, N-FK51A, N-FK58, N-PK52A) are the classic tools [TIE-19]. In OpticStudio, the Ansys KB example does this by Hammer glass substitution with a two-temperature merit function.
3. **Glass–plastic hybrids.** A weak plastic element with large negative $\beta$ can compensate the barrel — but it also brings index uniformity, birefringence and humidity issues.
4. **Active compensation.** Motorized or piezo focus driven by a temperature sensor, or simply **thermal calibration**: many 3D cameras measure temperature and use temperature-dependent calibration parameters. Optics still must stay sharp enough; calibration fixes geometry, not blur.

### 3.2 Things the uniform model misses
OpticStudio's standard thermal model assumes each surface/element at a uniform temperature (different elements may have different temperatures via separate `TEMP` operands). **Gradients** (a hot sensor or VCSEL next to the lens, sun load), stress in bonded or clamped lenses, and housing deformation need finite-element results brought back into the optical model — that is **STAR** (structural-thermal-optical analysis, Premium; Course 06 L05). Humidity changes plastic lenses; pressure changes the air index and can deform sealed windows.

## 4. Pressure and the air index
OpticStudio computes the air index from the system temperature and pressure (System Explorer → Environment). At sea level and 20 °C, $n_\text{air} - 1 \approx 2.7\times10^{-4}$; roughly proportional to pressure. Lowering pressure (altitude, vacuum) raises all *relative* glass indices by ≈ $n\,(n_\text{air}-1)$×(fractional pressure change): for a lens designed at 1 atm and used in vacuum the relative index of N-BK7 rises by ≈ 4×10⁻⁴ — a noticeable focus shift for long-focal-length systems (space optics are designed "in vacuum"). For industrial cameras, pressure is usually second-order but cheap to check with a `PRES` configuration.

## 5. In OpticStudio — thermal analysis step by step

1. **Data check.** Every glass needs thermal data (D₀…λ_TK and TCE) in the catalog; the Materials Catalog shows it. Plastics in vendor catalogs usually have dn/dT entered differently; verify.
2. **Environment.** System Explorer → Environment: set temperature (20 °C) and pressure (1 atm); tick **Adjust Index Data To Environment** — otherwise glass indices do *not* change with temperature even if the catalog has the coefficients [Ansys KB Kim].
3. **Mount TCE.** For air spaces, the LDE's TCE column (per surface) sets the expansion of the spacer/barrel represented by that thickness; OpticStudio treats spacers as thin cylindrical shells expanding axially and radially [Ansys KB Kim]. Enter the barrel material's CTE (e.g. 23.6 for aluminium, in 10⁻⁶/K).
4. **Remove curvature-changing solves** such as marginal-ray-angle (F/#) solves before thermal analysis — they would "re-solve" curvatures in the hot configuration and hide the effect [Ansys KB Kim]. A focus solve on the image distance has the same problem: in a fixed-focus camera the sensor distance must follow the mount, not the image.
5. **Make Thermal** (tool in the Multi-Configuration Editor / ribbon; search "Make Thermal"): choose the temperatures (e.g. 0, 20, 45 °C) and pressure; it creates configurations with `TEMP` and `PRES` MC operands and **Thermal Pickup** solves on radii, thicknesses, semi-diameters and parameters, plus glass pickups. Configuration 1 is usually the nominal one.
6. **Evaluate** each configuration: EFL, back focus, RMS wavefront/spot, MTF at Nyquist/2, through-focus MTF (the best-focus shift per configuration is the thermal defocus), distortion (calibration drift!).
7. **Optimize for athermal behaviour**: default MF with Configuration = All, plus custom `CONF` blocks (e.g. `DIFF` of a focus-related quantity between hot and cold), glass substitution with Hammer (L05), or a variable mount TCE (if your version allows the TCE cell to be a variable; otherwise scan it by hand or via the MCE) to find the ideal barrel CTE.
8. Combine with source wavelength drift: add `WAVE` rows to the thermal configurations (e.g. 940.0 nm at 20 °C, 938.7 at 0 °C, 941.6 at 45 °C for 0.065 nm/K) if the lens has noticeable axial colour.

---

## Worked example — a 25 mm F/2.8 NIR lens over 0–45 °C

**Given:** f = 25 mm, F/2.8, 940 nm, lens effectively N-BK7-like ($\beta \approx -2.1\times10^{-6}$/K), aluminium barrel ($\alpha_h = 23.6\times10^{-6}$/K), nominal focus at 20 °C.

1. **Defocus rate:** $(\alpha_h + \beta)f = (23.6 - 2.15)\times10^{-6}\times25$ mm = 0.536 µm/K.
2. **Over the range:** at 45 °C (+25 K): +13.4 µm; at 0 °C (−20 K): −10.7 µm.
3. **Budget:** diffraction DOF at F/2.8, 940 nm: $\pm2\lambda N^2 = \pm14.7$ µm. Temperature alone uses ~90% of the budget at 45 °C; with the L03 allocation of ≈ ±9 µm for *all* focus errors, the design fails.
4. **Fixes:** (a) a barrel with $\alpha_h \approx 2\times10^{-6}$/K (Invar-like, heavy/expensive) or (b) the re-entrant Al + plastic spacer computed above (31.2 mm Al tube, 6.2 mm plastic insert) — beware plastic creep and humidity; (c) a glass pair with more negative $\beta$ (fluorophosphate positive element); (d) operate at higher F/# where DOF is larger (F/4: ±30 µm) at the cost of light; (e) temperature-dependent calibration plus a little focus margin.
5. **Verify in OpticStudio** with Make Thermal (0/20/45 °C), Al TCE on the air spaces, and through-focus MTF per configuration (Task 3).

---

## Key takeaways
- Glass dn/dT follows the SCHOTT model; use **relative** dn/dT (≈ absolute + 0.93×10⁻⁶·n /K) in lens design; N-BK7 ≈ +3×10⁻⁶/K (e-line, relative).
- Thermo-optic coefficient $\beta = (dn_\text{rel}/dT)/(n-1) - \alpha$; focal length changes by $-\beta f$ per K; plastics have |β| ~100× glass.
- Thermal defocus ≈ $(\alpha_h + \beta)f\Delta T$; athermal when $\beta_\text{system} = -\alpha_h$. Aluminium barrels need negative-β optics or compound spacers.
- OpticStudio: Adjust Index Data To Environment, TCE per air space, remove curvature solves, Make Thermal → `TEMP`/`PRES` + thermal pickups; evaluate every configuration; optimize with Configuration = All and Hammer glass substitution.
- Include source wavelength drift, pressure, and (via STAR) gradients when they matter.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| dn/dT (absolute / relative) | Temperature coefficient of index relative to vacuum / to air |
| CTE / TCE | Coefficient of thermal expansion (OpticStudio: TCE, in 10⁻⁶/K) |
| Thermo-optic coefficient β | $(dn_\text{rel}/dT)/(n-1) - \alpha$; fractional power change per K |
| Athermal constant G | $\alpha(n-1) + dn_\text{rel}/dT$ (SCHOTT TIE-19) |
| Athermalization | Making focus/performance insensitive to temperature (passive or active) |
| Re-entrant spacer | Two-material spacer whose expansions partly cancel |
| Thermal pickup | MCE solve that scales a parameter with temperature from a reference configuration |
| Make Thermal | OpticStudio tool that builds a thermal multi-configuration model |
| STAR | Structural-Thermal-Optical analysis with FEA data (Premium) |

## References
1. [Kidger] M. J. Kidger, *Fundamental Optical Design*, 2002: §12.5.2, p. 250.
2. SCHOTT, Technical Information TIE-19, *Temperature Coefficient of the Refractive Index* (2023): <https://media.schott.com/api/public/content/0dcd87a2d36942a3946d033f0a9065e6>
3. Ansys Optics KB (N.-H. Kim), thermal modeling in OpticStudio: <https://optics.ansys.com/hc/en-us/articles/43071134350995>
4. ZOS-API example 18 (thermal MCE by code): <https://developer.ansys.com/docs/zemax-opticstudio-zos-api-2026-r1/apiexamples/example_18_cs.md>
5. Zemax Community, "Using STAR with other thermal and position settings in OpticStudio": <https://community.zemax.com/star-module-user-group-85/using-star-with-other-thermal-and-position-settings-in-opticstudio-4986>
