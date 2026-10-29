# L12 — Mirrors and catadioptric systems

> **Course 02 · Aberrations and classical lens design** · Estimated time: lecture ~3 h, tasks ~5–6 h
> **Prerequisites:** [Course 01 L02 (conics and aspheres)](../../01-foundations/L02-surfaces-sign-conventions-aspheres/), [L04 (Petzval)](../L04-field-curvature-petzval-flatteners/), [L08 (Seidel surface contributions, stop shift)](../L08-seidel-surface-contributions/) · **Next:** [L13 — Eyepieces, afocal systems, relays and windows](../L13-eyepieces-afocal-relays-windows/)

## Learning objectives
- Apply the Seidel formulas to mirrors with the $n' = -n$ convention, including the conic (aspheric) contribution $\Delta S_I = K c^3 h^4 (n'-n)$ and its stop-shifted coma, astigmatism and distortion.
- Derive the conic constant that removes spherical aberration from a mirror (parabola for infinity) and from a Cassegrain secondary; compute Ritchey–Chrétien conics from first-order data.
- Do the first-order layout of a two-mirror telescope (separation, secondary radius, back focus, EFL, obscuration) and enter it correctly in OpticStudio (MIRROR, negative thicknesses, conics, holes and obscurations).
- Explain the Schmidt principle (stop at the mirror's centre of curvature + aspheric plate), compute the plate profile, and describe spherochromatism and the curved image.
- Recognize classical catadioptric forms (Maksutov, Mangin, field correctors) and know which aberration each element is there to fix.
- Explain why mirrors are attractive for broadband/NIR systems and what they cost (obscuration, stray light, alignment sensitivity).

## Reading
- **Core:** [Geary Ch. 24, pp. 261–270] — conic constant of the parabolic mirror via the Seidel sum (§24.2), lens vs. sphere vs. parabola Seidel comparison (§24.3), aspheric lens correction (§24.4), the Schmidt corrector plate (§24.5), spectral effects (§24.6), Schmidt camera (§24.7).
- **Core:** [Geary Ch. 26, pp. 287–299] — Newtonian, Cassegrain family (classic, Ritchey–Chrétien, Dall–Kirkham), Gregorian, Schmidt; a complete Cassegrain first-order design and conic calculation (§26.3), entering it in ZEMAX with hole and obscuration (§26.4), central obscuration and stray light (§26.5).
- **Core:** [Kidger §6.8, pp. 129–130] and [Kidger Ch. 13, pp. 253–281] — mirror Seidel conventions; catadioptric systems: Cassegrain with Wynne correctors, parabola coma correctors, Ritchey–Chrétien (Kitt Peak), Schmidt camera and its achromatized and field-flattened variants, Maksutov–Bouwers Cassegrain, Mangin systems, mirror telephoto.
- **Optional:** [Kenyon §8.2–8.3, pp. 198–204] — telescope design and the Schmidt camera from a physics viewpoint (HST, Keck, VLT).

---

## 1. Mirrors in Seidel theory

### Conventions
OpticStudio models a mirror by putting **MIRROR** in the Material column; after the mirror the light travels in −z, so the *next thickness is negative*, and internally the index changes sign. Seidel theory uses the same trick: after reflection $n' = -n$ [Kidger §6.8]. With that, every formula of L08 applies unchanged.

For a mirror in air ($n = 1$, $n' = -1$), object at infinity ($u = 0$):

- Power: $K = c(n'-n) = -2c$. A **concave** mirror facing the light has its centre to the left ($c<0$) ⇒ $K>0$.
- Refraction invariant: $A = hc$; after reflection $n'u' = -hc(n'-n) = 2hc$, so $\delta(u/n) = u'/n' - 0 = 2hc$ [Kidger eq. 13.2].
- **Spherical aberration** of a sphere: $S_I = -A^2h\,\delta(u/n) = -2h^4c^3$ [Kidger eq. 13.3]; for a concave mirror ($c<0$) this is positive. As a wavefront: $W_{040} = S_I/8 = h^4/(4|R|^3)$.
- **Petzval:** $S_{IV} = -H^2c\,\delta(1/n) = 2H^2c = -H^2K$ [Kidger eq. 13.4]. A positive mirror has *negative* Petzval — the opposite of a positive lens. Mirrors and lenses can therefore flatten each other's fields (Schmidt–Cassegrain, Mangin, Maksutov designs).
- **Colour:** zero. Mirrors have no dispersion — the main reason for using them in broadband (UV–IR) systems.

### Aspheric (conic) contribution
A conic surface $z = \dfrac{cr^2}{1+\sqrt{1-(1+K)c^2r^2}}$ expands as $z = \tfrac12cr^2 + \tfrac18(1+K)c^3r^4 + \dots$, so relative to the base sphere it adds a fourth-order sag $\tfrac18Kc^3r^4$. That adds, at that surface only,

$$
\Delta S_I = K\,c^3\,h^4\,(n'-n),\qquad
\Delta S_{II} = \frac{\bar h}{h}\Delta S_I,\quad
\Delta S_{III} = \Big(\frac{\bar h}{h}\Big)^2\Delta S_I,\quad
\Delta S_V = \Big(\frac{\bar h}{h}\Big)^3\Delta S_I,\quad \Delta S_{IV}=0 .
$$

(The off-axis terms are just the stop-shift equations applied to a "pure spherical-aberration" surface; an even-asphere term $a_4r^4$ is equivalent to $K c^3/8$, i.e. $\Delta S_I = 8a_4h^4(n'-n)$.) Geary writes the same contribution inside his Buchdahl-style sum [Geary eq. 24.2]. Two lessons follow immediately:
- **An asphere at the stop ($\bar h = 0$) changes only spherical aberration.** That is the Schmidt principle.
- **An asphere away from the stop also changes coma, astigmatism and distortion** — that is how the Cassegrain secondary and the Ritchey–Chrétien pair correct coma.

### Parabola from one line of algebra
For a concave mirror at infinity, $S_I + \Delta S_I = -2h^4c^3 + Kc^3h^4(-2) = 0 \Rightarrow K = -1$ — a paraboloid [Geary §24.2]. (Geary's 100 mm F/10 example: $-0.000156 - 0.000156K = 0$.) At its centre of curvature, a *sphere* is perfect and the parabola is not — the conic that is perfect depends on the conjugates.

**Lens vs. mirror** [Geary Table 24.1, 400 mm F/10, 5°]: a BK7 thin lens has $W_{040} \approx 1.72\lambda$ and much more coma than a sphere or parabola ($W_{040} = 0.14\lambda$ and $0$), all three have the same astigmatism ($W_{222} = 6.52\lambda$: astigmatism of a thin element at the stop is $H^2K$, independent of form), and the mirrors have *more* field curvature (Petzval radius 400 mm vs. −607 mm, opposite sign).

## 2. Two-mirror telescopes

| Form | Primary | Secondary | Corrected | Notes |
|---|---|---|---|---|
| Newtonian | paraboloid | flat fold | $S_I$ | coma-limited field |
| Classical Cassegrain | paraboloid | convex hyperboloid | $S_I$ | coma remains |
| Ritchey–Chrétien | hyperboloid | hyperboloid | $S_I$, $S_{II}$ (aplanatic) | astigmatism + field curvature limit; HST, Keck, VLT |
| Dall–Kirkham | ellipsoid | sphere | $S_I$ | easy secondary; more coma |
| Gregorian | paraboloid | concave ellipsoid | $S_I$ | internal focus, longer |

[Geary §26.2, Table 26.1; Kidger §13.2.]

### First-order layout
Unfold the system (treat the mirrors as thin lenses of power $\phi_1 = -2c_1$, $\phi_2 = -2c_2$) and use the ordinary $y$–$u$ trace [Geary §26.3.1]:

1. Primary focal length $f_1 = |R_1|/2$; marginal height $h_1 = D/2$.
2. Choose the secondary height $h_2$ (it sets the obscuration $h_2/h_1$); separation $d = f_1(1 - h_2/h_1)$.
3. Choose the secondary power so the final focus lands a convenient distance behind the primary.
4. $\text{EFL} = h_1/|u'_\text{final}|$; the **secondary magnification** $m = \text{EFL}/f_1$; back focal distance from the primary vertex $= \beta f_1$.

**Conic constants.** Classical Cassegrain (parabolic primary): the secondary must image the primary's focus perfectly to the final focus:

$$
K_2^{\text{classic}} = -\Big(\frac{m+1}{m-1}\Big)^2 .
$$

Ritchey–Chrétien (zero $S_I$ and $S_{II}$), in the standard two-mirror notation (Schroeder's *Astronomical Optics*; derivable from the formulas of §1):

$$
K_1 = -1 - \frac{2(1+\beta)}{m^2(m-\beta)},\qquad
K_2 = -\Big(\frac{m+1}{m-1}\Big)^2 - \frac{2m(m+1)}{(m-\beta)(m-1)^3}.
$$

I verified both against a numerical Seidel sum with the conic contributions above (see worked example): they zero $S_I$ (classic) and $S_I$, $S_{II}$ (RC) exactly.

**Petzval sum of two mirrors:** $P = 2(c_1 - c_2)$ (in air). It vanishes only if the radii are equal — normally impossible with a compact Cassegrain, so the field is curved and **astigmatism + field curvature** limit the RC; large telescopes add refracting field correctors near the focus (Wynne designs, Kidger Figs. 13.3, 13.11).

### Practicalities
- **Central obscuration** reduces throughput by the area ratio $\varepsilon^2$ (30% linear obscuration ⇒ 9% area) and moves energy from the Airy core into the rings, lowering mid-frequency MTF [Geary §26.5.1; Kidger §13.1]. Geary's example: 17%; HST ~13%.
- **Stray light:** rays can skip both mirrors and reach the detector through the primary's hole — baffles (primary and secondary baffle tubes) are mandatory [Geary §26.5.2]. In OpticStudio Premium you would check this in non-sequential mode (Course 05 L07).
- **Narrow field:** the image must fit through the hole; two-mirror systems are always narrow-field (~1° for telescopes; a 500–1000 mm F/8 mirror telephoto covers 35 mm film with a ~0.3 obstruction ratio [Kidger p. 253]).

## 3. The Schmidt camera

Put the **stop at the centre of curvature** of a spherical mirror: every chief ray then passes through the centre and hits the mirror normally ($\bar A = 0$ for the mirror), so the mirror contributes **no coma, astigmatism or distortion** (L08 zero conditions) — only spherical aberration and Petzval. Every field point sees the same mirror; the image lies on a sphere of radius $R/2$ concentric with the mirror [Geary §24.7; Kidger p. 267].

Now remove the spherical aberration with a thin aspheric plate **at the stop** (where an asphere changes only $S_I$). The plate must add an optical path $(n-1)\Delta t(y) = -W(y)$ that cancels the mirror's $W = y^4/(4R^3)$ [Geary §24.5.2]:

$$
\Delta t(y) = -\frac{y^4}{4R^3(n-1)} \quad\Longleftrightarrow\quad a_4 = \frac{c^3}{4(n'-n)} \ \text{on the aspheric face}.
$$

Geary's 30 cm F/2 example ($R = 120.6$ cm, $n = 1.5151$): edge thickness variation 140 µm, $W_{040} = 72$ µm. Kidger's UK Schmidt plate ($R = 6121$ mm, $n = 1.528$, asphere on the rear face) has $A_4 = 2.03\times10^{-12}$ mm⁻³, essentially the formula's $2.06\times10^{-12}$ (the small difference comes from the weak base curvature and the $A_6$ term).

**Spherochromatism.** The mirror's aberration is wavelength-independent, the plate's is not, so spherical aberration varies with colour. The classical cure is to add a little base power (a $y^2$ term) so the plate profile has a *neutral zone* — the profile $\propto y^4 - \tfrac32\rho^2y^2$ has zero slope at $y = 0.866\rho$ and minimizes the chromatic spread; Geary shows the same effect by letting the plate radius vary [§24.6]. Kidger's achromatized Schmidt uses a two-glass plate [Figs. 13.16–13.17].

**Curved image.** Fine for curved photographic plates; for a flat sensor add a field-flattening lens near the image (Linfoot, Wynne's thick self-achromatic flattener, Kidger Fig. 13.18).

**Oblique spherical aberration** remains: off-axis beams see the plate foreshortened; a slightly non-concentric focal surface reduces it [Kidger p. 267].

## 4. Other catadioptric forms (recognition level)

- **Maksutov–Bouwers:** a thick meniscus *concentric* with the stop corrects the mirror's spherical aberration with spherical surfaces only; nearly self-achromatic. In the Maksutov–Cassegrain variant the secondary is a spot on the meniscus [Kidger Fig. 13.20].
- **Mangin mirror:** a negative meniscus with a mirrored rear surface; light passes the glass twice. The glass overcorrects the mirror's spherical aberration; extra lenses fix colour and field [Kidger Figs. 13.23–13.25: Wiedemann F/1.25 with a component-by-component Seidel table worth studying]. In OpticStudio the Mangin is entered as three surfaces (refract, reflect, refract) with **pickups** keeping the repeated surface identical.
- **Mirror telephoto** (500 mm F/6 for SLR) — very short, light, but with an annular pupil ("donut bokeh") [Kidger Fig. 13.29].
- **Field correctors:** parabola coma correctors (one lens; Kidger Fig. 13.5), three-lens afocal correctors (Wynne) — "afocal" so as not to add secondary spectrum.

**Engineering angle.** Industrial uses include broadband (UV–LWIR) and NIR imaging, laser beam expanders (Dall–Kirkham used in reverse [Geary §26.2.2]), off-axis (unobscured) mirror collimators for projectors and test equipment, and freeform reflective relays. For a Zivid-style structured-light projector, a reflective condenser or fold can save length and avoid colour issues with broadband LEDs — but alignment tolerances of mirrors are ~2× those of a lens surface for tilt (reflection doubles angular errors), which you will quantify in Course 06.

## 5. In OpticStudio

- **Entering mirrors:** Material = `MIRROR`; thickness after a mirror is negative (and after a second mirror positive again); radii keep the global sign convention (Geary's Cassegrain: both radii negative) [Geary §26.4].
- **Conics:** the *Conic* column of a Standard surface; higher terms via *Even Asphere* (2nd, 4th, 6th… order coefficients). Make the 4th-order term variable with `SPHA` = 0 to "design" a Schmidt plate, as Geary does.
- **Holes and obscurations:** Surface Properties → Aperture → *Circular Aperture* with a minimum radius (hole in the primary), and a dummy surface with a *Circular Obscuration* at the secondary's position (Geary §26.4). The analyses then show the annular pupil (FFT PSF/MTF reflect the obscuration).
- **Ray aiming:** for strongly obscured or fast systems turn on ray aiming (System Explorer → Ray Aiming) if the stop is not the first surface.
- **Seidel analysis** treats conics and even aspheres correctly; the per-surface table separates nothing, so compare with your own script to see "sphere" vs "asphere" parts (Kidger prints them separately).
- **Operands:** `SPHA`, `COMA`, `ASTI` (waves) to drive conics; `EFFL`; `TTHI`/`TOTR` for length; for non-sequential stray-light checks use Premium's NSC tools later.
- **Pitfall:** placing an obscuration on the *secondary mirror surface* itself also blocks the light reflected from it in some set-ups — use a dummy surface in the incoming beam at the same z.

## Worked example

**Geary's Cassegrain (units cm).** Primary $R_1 = -120.598$ ($f_1 = 60.30$), $D = 30$, secondary $R_2 = -25$, separation $-50$ (OpticStudio sign).

*First order* (my paraxial trace): secondary marginal height $h_2 = 2.562$ (obscuration $2.562/15 = 17\%$), back focus 58.49 cm behind the secondary (8.49 cm behind the primary), EFL = 342.45 cm, F/11.4 — Geary: 58.493, 342.466, F/11.4. Secondary magnification $m = 342.45/60.30 = 5.679$; $\beta = 8.49/60.30 = 0.1408$.

*Conics:* classical $K_2 = -(6.679/4.679)^2 = -2.0375$ (Geary −2.037: hyperbola). Ritchey–Chrétien: $K_1 = -1.01277$, $K_2 = -2.17123$.

*Seidel check* (EPD 30, semi-field 0.5°, my script with conic terms; lens units cm):

| | $S_I$ | $S_{II}$ | $S_{III}$ | $S_{IV}$ | $S_V$ |
|---|---|---|---|---|---|
| Spheres | 0.04649 | −0.00204 | −0.00008 | 0.00109 | −0.00018 |
| Classical (−1, −2.0375) | 0 | −0.000126 | 0.00025 | 0.00109 | −0.00013 |
| RC (−1.0128, −2.1712) | 0 | 0 | 0.00027 | 0.00109 | −0.00012 |

The spherical-mirror version has $W_{040} = S_I/8 = 105.7\lambda$ at 0.55 µm — Geary reports "105λ" from ZEMAX. The RC removes the classical Cassegrain's coma at the price of slightly more astigmatism; the Petzval term is unchanged by conics: $P = 2(c_1-c_2) = 0.0634$ cm⁻¹, Petzval radius −15.8 cm — strongly curved compared with the 342 cm focal length, which is why RC telescopes need field correctors for wide fields.

**Schmidt plate for Geary's F/2 mirror.** $R = 120.6$ cm, $y_{\max} = 15$ cm, $n = 1.5151$: $\Delta t(15) = 15^4/(4\times120.6^3\times0.5151) = 0.0140$ cm = 140 µm ✓; in mm units the 4th-order coefficient magnitude is $1/(4R^3(n-1)) = 2.77\times10^{-10}$ mm⁻³.

## Key takeaways
- Use $n' = -n$ at mirrors and all Seidel formulas carry over; mirrors have no colour and *negative* Petzval for positive power.
- A conic adds $\Delta S_I = Kc^3h^4(n'-n)$; away from the stop it also adds coma/astigmatism/distortion via $\bar h/h$ — the lever used by Cassegrain secondaries and RC pairs.
- Parabola: perfect at infinity; classical Cassegrain $K_2 = -((m+1)/(m-1))^2$; Ritchey–Chrétien hyperboloids cancel $S_I$ and $S_{II}$.
- Schmidt: stop at the centre of curvature kills off-axis mirror aberrations; an aspheric plate at the stop kills spherical; spherochromatism and a curved image remain.
- Two-mirror systems are compact and achromatic but narrow-field, obscured, stray-light-prone and alignment-sensitive.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Conic constant $K$ | $K=0$ sphere, $-1<K<0$ prolate ellipse, $K=-1$ paraboloid, $K<-1$ hyperboloid, $K>0$ oblate ellipse |
| Cassegrain / Gregorian | Concave primary + convex / concave secondary |
| Ritchey–Chrétien | Aplanatic Cassegrain with two hyperboloids |
| Secondary magnification $m$ | System EFL / primary focal length |
| Obscuration ratio | Secondary (or hole) diameter / primary diameter |
| Schmidt corrector | Aspheric plate at the centre of curvature of a spherical mirror |
| Spherochromatism | Variation of spherical aberration with wavelength |
| Neutral zone | Radius where a Schmidt plate has zero slope (≈0.866 of the aperture) |
| Mangin mirror | Meniscus lens with a reflective rear surface |
| Maksutov corrector | Thick concentric meniscus correcting a spherical mirror |
| Field corrector | Lens group near focus that removes off-axis aberrations of a mirror system |

## References
1. [Geary] J. M. Geary, *Introduction to Lens Design*, Willmann-Bell 2002 — Ch. 24, pp. 261–270; Ch. 26, pp. 287–299; Table 24.1.
2. [Kidger] M. J. Kidger, *Fundamental Optical Design*, SPIE Press 2002 — §6.8, pp. 129–130; Ch. 13, pp. 253–281.
3. [Kenyon] I. R. Kenyon, *The Light Fantastic*, OUP 2008 — §8.2–8.3, pp. 198–204.
4. D. J. Schroeder, *Astronomical Optics*, 2nd ed., Academic Press 2000 — standard source for the two-mirror conic formulas (not in corpus).
