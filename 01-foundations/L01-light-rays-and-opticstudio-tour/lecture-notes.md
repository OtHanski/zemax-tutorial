# L01 — Light, Rays and a First Tour of OpticStudio

> **Course 01 · Foundations** · Estimated time: lecture ~3 h, tasks ~4 h
> **Prerequisites:** none (high-school trigonometry, basic physics) · **Next:** [L02 — Surfaces, sign conventions and aspheres](../L02-surfaces-sign-conventions-aspheres/)

## Learning objectives
After this lesson you should be able to:
- Explain what a lens designer is trying to achieve and list the main specifications (focal length, F-number, field, wavelength band, image quality, package, environment, cost) that drive a design.
- State the relationship between light waves, wavefronts and rays, and say when the ray (geometrical-optics) picture is good enough and when it is not.
- Apply Snell's law and the law of reflection, compute a critical angle, and derive Snell's law from Fermat's principle of stationary optical path.
- Explain why the *nonlinearity* of Snell's law ($\sin I \ne I$) is the root cause of monochromatic aberrations.
- Set up a lens from scratch in OpticStudio: system aperture, fields, wavelengths, a singlet in the Lens Data Editor (LDE), a Cross-Section layout, Quick Focus and a Standard Spot Diagram.
- Save, re-open and organize OpticStudio work (lens file `.zmx`/`.zos`, session file `.zda`, archive `.zar`).

## Reading
- **Core:** [Geary Ch. 1, pp. 1–8] — why lens design, specifications, the "aperture vs. field" map of design types (Fig. 1.6). Read for the big picture; skip the homework figure (the scan is poor).
- **Core:** [Geary Ch. 2, pp. 11–20] — the original ZEMAX "first session" with a biconvex BK7 lens. The menu names are from 2002 (the "Gen/Fie/Wav" buttons); this lesson translates them to the modern ribbon. Pay attention to §2.8.1 (three different F-numbers) and §2.8.2 (why 0.707 of the maximum field is a standard field point).
- **Core:** [Kidger §1.1–1.5, pp. 1–6] — coordinate system, rectilinear propagation, Snell's law (in the compact form $\sin I' = q \sin I$), reflection as $n' = -n$, Fermat's principle, wavefronts and the theorem of Malus and Dupin.
- **Core:** [Kenyon §1.2, pp. 6–8] — light as an electromagnetic wave; $v = f\lambda$. [Kenyon §2.1, pp. 31–36] — rays vs. wavefronts, Huygens' construction, Snell's law from wave matching and from Fermat's principle.
- **Optional:** Ansys Optics knowledge-base series "How to design a singlet lens" (Part 1 setup, Part 2 analysis, Part 3 optimization) — the official equivalent of our first session, using an F/4 HeNe singlet (links in References).

---

## 1. What lens design is (and why it is hard)

A lens system takes light from every point of an object and tries to bring it back to a corresponding point in an image. Geary opens with two lenses of identical focal length (so identical image *size*): one is a single element, the other a multi-element photographic objective [Geary §1.2.1, p. 3]. The extra elements are not there to change magnification; they exist to fix **image quality** — colour, spherical aberration, off-axis aberrations and field curvature — so that a sharp, evenly bright image lands on a *flat* detector.

Two ideas from that chapter frame this whole course:

1. **Imaging is a convolution.** A perfect system maps every object point to an image point (a scaled copy of the object). A real system maps each point to a small blob — the *point spread function* (PSF). The image of an extended object is the ideal image blurred by that blob [Geary §1.2.2, pp. 3–4]. Every analysis window you will open in OpticStudio (spot diagrams, ray fans, MTF, PSF) is ultimately a way of describing that blob.
2. **Difficulty grows with aperture and field.** Rays far from the axis, or arriving at large field angles, hit surfaces at large angles of incidence, where Snell's law is strongly nonlinear [Geary §1.2.3, pp. 4–5]. Geary's Fig. 1.6 (after W. Smith) plots design forms against F-number and half-field: a parabola for F/10 and a few degrees; a Cooke triplet for moderate apertures and ~20°; a double Gauss for F/2 and ±20°; retrofocus and fisheye designs for very wide fields. You will build several of these in Courses 01–02.

### 1.1 Specifications first
Before touching the software, a professional pins down the specification [Geary §1.2.4, pp. 5–8]:

| Spec | Typical question | Machine-vision example (Zivid-type 3D camera) |
|---|---|---|
| Format / sensor size | How big is the image? | e.g. a 2/3" sensor, ~11 mm diagonal |
| Field of view (FOV) | How much of the scene? | sets the effective focal length (EFL) |
| F-number | How much light, how much depth of field? | F/2.8–F/8 trade-off: brightness vs. depth of field vs. diffraction |
| Wavelength band | Visible? NIR? Laser line? | projector LED colour, or 850/940 nm NIR |
| Image quality | MTF at a given lp/mm, spot size, distortion | must resolve the pixel pitch, low distortion for calibration |
| Package & environment | Length, diameter, mass, temperature, shock | industrial temperature range, robot-mounted |
| Cost & manufacturability | Number of elements, aspheres, tolerances | spherical glass is cheapest; aspheres and tight tolerances cost money |

Geary warns about two failure modes: a customer who does not know what they need (specs change mid-design), and over-specification (tolerances beyond what anyone can make or measure). Part of the designer's job is to negotiate a realistic spec.

---

## 2. What is light? Waves, wavefronts and rays

### 2.1 Light is an electromagnetic wave
Light is a transverse electromagnetic wave: oscillating electric and magnetic fields, perpendicular to each other and to the propagation direction [Kenyon §1.2, pp. 6–8]. Wavelength $\lambda$, frequency $f$ and speed $v$ are related by

$$
v = f\lambda .
$$

In a material with refractive index $n$ the wave slows down to

$$
v = \frac{c}{n},
$$

where $c \approx 2.998\times10^8$ m/s is the speed of light in vacuum [Kidger Eq. (1.2), p. 3]. The **frequency does not change** when light enters glass, so the wavelength inside the material shrinks to $\lambda/n$ [Kenyon §2.1.2, p. 34]. For N-BK7 at the helium d-line ($\lambda = 587.6$ nm, $n_d = 1.5168$): $v = 1.976\times10^8$ m/s and $\lambda_{\text{glass}} = 387.4$ nm.

Optical design software always quotes the **vacuum (or air) wavelength**. In OpticStudio, wavelengths are entered in **micrometres** (µm) regardless of lens units, e.g. 0.5876 for the d-line.

### 2.2 Wavefronts and rays
A **wavefront** is a surface of constant phase. Geometrical optics gives an equivalent definition: a surface of constant *optical path length* (OPL) measured from a point in the object [Kidger §1.5, p. 5]. A **ray** is the normal to the wavefront — the direction energy flows. In a homogeneous, isotropic medium the rays are perpendicular to the wavefronts (theorem of Malus and Dupin) [Kidger §1.5, p. 6]; birefringent crystals are the exception.

```
  point source        spherical wavefronts          after a perfect lens
      *   )   )   )   )            ---->     (   (   (   *  image point
     rays = radial lines (normals)               converging sphere
```

A perfect lens turns the diverging spherical wavefront from an object point into a converging spherical wavefront centred on the image point. **Aberrations** are the deviations of the real wavefront from that ideal sphere. We will measure them in waves (OPD fans, wavefront maps) or as ray errors in the image plane (ray fans, spot diagrams). This duality — wavefront error vs. ray error — runs through the whole curriculum.

### 2.3 When is the ray picture enough?
Rays are the limit $\lambda \to 0$ of wave optics [Kidger Ch. 1 intro, p. 1]. Light passing an aperture of width $a$ spreads by an angle of order $\lambda/a$; for green light and a 1 cm aperture this is about $5\times10^{-5}$ rad [Kenyon §2.1, p. 32] — negligible for tracing rays *through* a lens, but not negligible at the image, where it sets the smallest possible spot. For a circular aperture the diffraction-limited spot (the Airy disk) has diameter

$$
D_{\text{Airy}} = 2.44\,\lambda\,N,
$$

with $N$ the working F-number. For $\lambda = 0.5876$ µm and $N = 5$: $D_{\text{Airy}} = 7.17$ µm.

Rule of thumb you will use constantly:
- **Geometric spot ≫ Airy disk** → the lens is *aberration-limited*; ray-based analyses (spot diagrams, ray fans) tell the truth.
- **Geometric spot ≲ Airy disk** → the lens is near *diffraction-limited*; you must switch to wave-based metrics (OPD, Strehl, FFT/Huygens MTF and PSF — Course 03).

OpticStudio helps by drawing the Airy circle on the Standard Spot Diagram (an option in the settings), so you can see at a glance which regime you are in.

---

## 3. Reflection and refraction

### 3.1 Snell's law
At the boundary between media of index $n$ and $n'$, a ray with angle of incidence $I$ (measured from the surface normal) refracts to angle $I'$ with

$$
n \sin I = n' \sin I' .
$$

The incident ray, refracted ray and normal all lie in one plane, the **plane of incidence** [Kidger §1.3, pp. 2–3]. Kidger writes it compactly as $\sin I' = q \sin I$ with $q = n/n'$.

Kenyon derives it twice [Kenyon §2.1.2–2.1.3, pp. 33–35]: (a) from Huygens' secondary wavelets — the wave crests must match along the interface, so $\lambda_1/\sin\theta_1 = \lambda_2/\sin\theta_2$; and (b) from Fermat's principle (Section 4 below). Both give the same law; the wave-matching argument is the one that generalizes to diffraction gratings in Course 05.

### 3.2 Reflection as a special case
The law of reflection is $I' = -I$ (equal angles, opposite signs in the ray-tracing sign convention). Kidger notes the classic designer's trick: treat a mirror as a refraction with $n' = -n$ ($q = -1$); then all refraction formulas work for mirrors unchanged, with the index flipping sign after every reflection [Kidger §1.3, pp. 3–4]. OpticStudio does the bookkeeping for you: you type `MIRROR` in the Material column and the software handles the direction reversal (thicknesses after a mirror become negative — more in L02 and Course 02 L12).

### 3.3 Total internal reflection
Going from glass to air ($n > n'$), $\sin I' = (n/n')\sin I$ exceeds 1 once $I$ is larger than the **critical angle**

$$
I_c = \arcsin\frac{n'}{n}.
$$

For N-BK7 to air, $I_c = \arcsin(1/1.5168) = 41.2°$. Beyond this, all light is reflected (TIR). TIR is useful (prisms, light guides, TIR collimators in Course 05) and harmful (rays in a lens that TIR are lost; OpticStudio reports them as ray-trace errors).

### 3.4 Why Snell's law causes aberrations
Expand the sine:

$$
\sin I = I - \frac{I^3}{6} + \frac{I^5}{120} - \dots
$$

If $\sin I$ were exactly $I$, every spherical surface would image perfectly (this is the **paraxial** approximation of L03). The cubic term is the source of the classical third-order (Seidel) aberrations; the fifth-order term gives fifth-order aberrations, and so on.

| $I$ | $I$ (rad) | $\sin I$ | relative error of $\sin I \approx I$ |
|---|---|---|---|
| 5° | 0.08727 | 0.08716 | 0.13 % |
| 10° | 0.17453 | 0.17365 | 0.51 % |
| 20° | 0.34907 | 0.34202 | 2.1 % |
| 30° | 0.52360 | 0.50000 | 4.7 % |

The error grows roughly as $I^2$. Large apertures (rays far from the axis) and large fields (oblique rays) both raise the angles of incidence [Geary Fig. 1.5, p. 5]. **A good designer's instinct is to keep angles of incidence small and to share the bending of rays among many surfaces** — "lens splitting", which you will try in L08.

---

## 4. Fermat's principle and optical path length

The **optical path length** of a ray crossing media of index $n_i$ over geometric lengths $d_i$ is

$$
\text{OPL} = \sum_i n_i d_i
$$

[Kidger Eq. (1.7), p. 5; Kenyon Eq. (2.13), p. 34]. Since $n_i d_i / c$ is the travel time, OPL is "time-of-flight times $c$".

**Fermat's principle:** the OPL along a physically possible ray is *stationary* (usually a minimum) with respect to small variations of the path [Kidger §1.4, p. 5]. Kenyon's proof [§2.1.3, pp. 34–35]: put point A at height $h_1$ above a flat interface and point C at depth $h_2$ below it; let the ray cross at horizontal coordinate $x$. Then

$$
L(x) = n_1\sqrt{x^2 + h_1^2} + n_2\sqrt{(X - x)^2 + h_2^2},
$$

and $dL/dx = 0$ gives $n_1\sin\theta_1 = n_2\sin\theta_2$.

Why a lens designer cares:
- **Perfect imaging = equal OPL.** A perfect image point is one for which *all* rays from the object point have the same OPL. Deviations of OPL across the pupil are the wavefront aberration — exactly what OpticStudio's **OPD Fan** and **Wavefront Map** plot (L06).
- **Optimization intuition.** Since the real OPL is stationary, small errors in ray *position* produce only second-order changes in OPL — one reason wavefront-based merit functions behave smoothly.

---

## 5. Coordinate system and conventions (preview)

We follow Kidger and OpticStudio [Kidger §1.1, p. 1]:
- The optical axis is **z**; light travels from left to right (+z).
- **y** is up in the plane of the drawing (the *meridional* or tangential plane); **x** completes a right-handed system.
- Quantities after refraction/reflection are primed: $n'$, $I'$, $u'$.
- Distances are positive left-to-right; a radius is positive when its centre of curvature is to the right of the surface vertex; ray angles $u$ are positive counter-clockwise (as in Kidger and Geary).

L02 develops the full sign convention. For now remember: a **biconvex** lens in OpticStudio has $R_1 > 0$ and $R_2 < 0$.

---

## 6. Your first OpticStudio session

Geary's Chapter 2 walks through entering a 100 mm-radius biconvex BK7 lens in ZEMAX SE (2002). The concepts are unchanged; the user interface has moved to a **ribbon**. Below is the same exercise in modern OpticStudio for the lens you will use throughout Course 01:

> **The Course 01 reference singlet:** EFL ≈ 100 mm, F/5 (entrance pupil diameter 20 mm), object at infinity, half-field 5°, visible light (F, d, C), equiconvex N-BK7, 4 mm thick.

### 6.1 The window
- **Ribbon tabs** across the top: *File, Setup, Analyze, Optimize, Tolerance, Libraries, Part Designer, Programming, Help*. Setup holds editors and system settings; Analyze holds all analysis windows; Optimize holds the Merit Function Editor, Quick Focus, Quick Adjust and optimizers.
- **System Explorer** (left-hand panel; Setup → System Explorer if hidden): global system data — Aperture, Fields, Wavelengths, Environment, Polarization, Advanced, Ray Aiming, Material Catalogs, Title/Notes, Files, Units, Cost estimator.
- **Lens Data Editor (LDE)**: the spreadsheet of surfaces. It opens by default; otherwise Setup → Lens Data.
- **Analysis windows** open as tabs or floating windows; each has a *Settings* panel (the gear/"Settings" button at the top-left of the window) and updates automatically when the lens changes (unless you switch automatic updating off).

### 6.2 Step by step
1. **New file.** File → New. You get a default system with three surfaces: `OBJ` (object), `STO` (stop) and `IMA` (image).
2. **Units.** System Explorer → Units → Lens Units = Millimeters (the default).
3. **Aperture.** System Explorer → Aperture → *Aperture Type* = **Entrance Pupil Diameter**, *Aperture Value* = **20**. Other aperture types (Image Space F/#, Object Space NA, Float By Stop Size, Paraxial Working F/#, Object Cone Angle) are covered in L04. The aperture defines the size of the beam traced; it is *not* the same as the physical semi-diameters in the LDE [Geary §2.2.1, p. 12].
4. **Fields.** System Explorer → Fields → Open Field Data Editor. Field Type = **Angle** (degrees). Enter three fields: **0, 3.5, 5** (Y-field), weights 1. Why 3.5? It is 0.7 × 5°: the radius 0.707 splits a unit circle into two equal areas, so a field at ~0.7 of the maximum samples the "average" region of a circular field [Geary §2.8.2, p. 20].
5. **Wavelengths.** System Explorer → Wavelengths → open the wavelength settings and use the preset **F, d, C (Visible)**: 0.4861, 0.5876, 0.6563 µm, with **d (0.5876) as primary**. The primary wavelength is used for all first-order (paraxial) quantities like EFL [Geary §2.2.2, p. 13].
6. **Material catalogue.** System Explorer → Material Catalogs: make sure **SCHOTT** is loaded (it is by default).
7. **Insert surfaces.** In the LDE, click on the `IMA` row and press **Insert** once: you now have OBJ, STO, 2, IMA. The stop will be the front face of the lens; surface 2 is the back face.
8. **Enter the lens:**

| Surf | Comment | Radius | Thickness | Material | Semi-Diameter |
|---|---|---|---|---|---|
| OBJ | | Infinity | Infinity | | |
| STO | front | 102.7 | 4.0 | N-BK7 | (auto) |
| 2 | back | −102.7 | 95.0 | | (auto) |
| IMA | | Infinity | — | | |

   Typing `N-BK7` in the Material column pulls the dispersion formula from the SCHOTT catalogue. The 95 mm is a deliberately rough guess at the back focal distance.
9. **Look at it.** Open **Cross-Section** (Setup → System Viewers → Cross-Section; also available on the Analyze tab). You see three ray bundles (0°, 3.5°, 5°) entering from the left, refracting at the lens and approaching the image plane. With 95 mm the bundles cross *behind* the image surface — the image is out of focus.
10. **Paraxial focus with a solve.** Click the small cell to the right of the *Thickness* of surface 2 → Solve Type = **Marginal Ray Height**, Height = 0. A letter `M` appears. OpticStudio now sets that thickness to the distance at which the paraxial marginal ray crosses the axis: the paraxial back focal length (≈ 98.7 mm). This is Geary's "M-solve" [Geary §2.2.1, p. 12]; solves are the topic of L07.
11. **System data.** Analyze → Reports → **System Data** (Geary's "Sys" button). Read off: Effective Focal Length ≈ 100.0 mm, Back Focal Length ≈ 98.7 mm, Image Space F/# ≈ 5.0, Paraxial Image Height ≈ 8.75 mm, Total Track ≈ 102.7 mm.
12. **Spot diagram.** Analyze → Rays & Spots → **Standard Spot Diagram**. One spot per field, colours = wavelengths. Note the RMS and GEO radii printed under each spot, and the Airy circle (turn on "Show Airy Disk" in Settings). Spots of order 100 µm vs. an Airy radius of ~3.6 µm: this lens is heavily aberration-limited.
13. **Quick Focus.** Remove the `M` solve first (set the solve type back to Fixed — otherwise the solve keeps overriding the thickness). Then Optimize → Manual Adjustment → **Quick Focus** (shortcut Ctrl+Shift+Q), criterion **RMS Spot Radius**, **Use Centroid** checked. Quick Focus adjusts *the thickness of the surface before the image* to minimize the chosen criterion averaged over fields and wavelengths. The thickness drops from 98.7 to ~97 mm: the best focus lies *in front of* the paraxial focus because marginal rays of a positive singlet focus short (undercorrected spherical aberration — Course 02 L02). The spots shrink markedly.
14. **Save.** File → Save As → `L01_singlet_f100.zmx`.

### 6.3 Files you will meet
| File | What it is |
|---|---|
| `.zmx` | Lens file in text (ASCII) form: prescription, apertures, fields, wavelengths, merit function, etc. Human-readable, diff-able in git. |
| `.zos` | The same content in a binary lens file (introduced in OpticStudio 21.3). You can choose which format to save. |
| `.zda` | **Session file**: which analysis windows and editors were open, where, and with which settings. If it sits in the same folder as the lens file, re-opening the lens restores your workspace. Session files are controlled by a "Use Session Files" preference (Setup → Project Preferences; location varies by version). |
| `.cfg` | Configuration/settings files: global ones (e.g. the default settings for each analysis), and lens-specific ones next to the lens file. |
| `.zar` | Archive: a compressed bundle of the lens plus the catalogues, coatings and other files it needs — use this to send a design to a colleague (File → Create Archive / Open Archive). `.zprj` is a newer project format that can include more (e.g. CAD part files). |

**Professional habit (version control):** Geary insists on documenting each optimization step with a systematic file-naming scheme (e.g. `TRIP204b` = second triplet, step 4, before optimization) [Geary §2.6, pp. 17–18]. With git you can do better: save `.zmx` (text) files, commit after every meaningful step with a message describing variables and merit function. Commit the `.zda` too if you want to restore your windows. Course 07 automates this.

---

## 7. In OpticStudio — what the first-session numbers mean

- **Three F-numbers.** System Data lists *Image Space F/#* (= EFL/EPD for an object at infinity), *Paraxial Working F/#* (= $1/(2\tan U')$ from the paraxial marginal ray angle) and *Working F/#* (= $1/(2\sin U')$ from the real marginal ray angle) [Geary §2.8.1, p. 19]. For an infinite object and a slow lens they agree; they differ for finite conjugates (L04) and for fast lenses.
- **Semi-diameters.** In "automatic" mode OpticStudio sizes every surface to pass all rays from all fields. If you type a value, the cell gets a `U` (user-defined) flag and the surface becomes a hard aperture *only if* you also add an aperture to it. In Geary's example the semi-diameter (25 mm) is larger than the beam (20 mm EPD radius), which is normal: lenses need a mechanical rim.
- **Paraxial vs. real.** EFL, BFL and image height in System Data are *paraxial* (first-order) quantities computed at the primary wavelength. The Spot Diagram is computed with *real* (exact) rays. Their disagreement is aberration.
- **Pitfalls:**
  - A solve silently overrides your typed value. Watch the little letter flags (`M`, `F`, `V`, `P`) next to the cells.
  - Wavelengths are always in µm, lens dimensions in lens units (mm).
  - If the Cross-Section shows rays missing a surface or bending wildly, look for a sign error in a radius (L02).
  - Analysis windows have their own settings (e.g. which wavelength, how many rays). When comparing numbers with a colleague, compare settings too.

---

## Worked example — designing the reference singlet on paper

**Problem.** Find radii for an equiconvex N-BK7 singlet with EFL = 100 mm at the d-line, then check the F/5 Airy disk and the image height at 5°.

1. **Index.** From the SCHOTT Sellmeier formula, $n_d(\text{N-BK7}) = 1.51680$.
2. **Thin-lens estimate.** The lensmaker's equation for a thin lens in air: $1/f = (n-1)(1/R_1 - 1/R_2)$. Equiconvex means $R_2 = -R_1 = -R$:
$$
\frac{1}{f} = \frac{2(n-1)}{R} \;\Rightarrow\; R = 2(n-1)f = 2(0.5168)(100) = 103.36\ \text{mm}.
$$
3. **Thick-lens correction.** A real lens has thickness $t$. The thick-lens power (derived in L03) is $\phi = \phi_1 + \phi_2 - (t/n)\phi_1\phi_2$, with surface powers $\phi_1 = (n-1)/R_1$, $\phi_2 = (1-n)/R_2$. With $t = 4$ mm the negative third term slightly lowers the power, so the radii must get slightly shorter. Solving $\phi = 1/100$ gives $R = 102.67$ mm; we round to **102.7 mm**, which gives EFL = 100.03 mm.
4. **Back focal length.** For this lens the paraxial BFL is 98.70 mm (L03 shows how to compute it). Total track = 4 + 98.70 = 102.70 mm.
5. **Airy disk.** $D_{\text{Airy}} = 2.44 \times 0.5876\ \mu\text{m} \times 5 = 7.17\ \mu$m.
6. **Image height.** For a distant object, the chief ray at field angle $\theta$ lands at $h' = f\tan\theta = 100 \tan 5° = 8.75$ mm.
7. **Colour preview.** At F (486.1 nm) and C (656.3 nm) the EFL is 98.96 mm and 100.50 mm: a 1.54 mm spread of focus, roughly $f/V_d$ with Abbe number $V_d = 64.17$ ($100/64.17 = 1.56$). This axial colour (L05, Course 02 L06) is why the polychromatic spot is bigger than the monochromatic one.

**Check with a ray tracer.** A simple Python real-ray trace of this lens (square pupil grid, centroid reference) gives, at the paraxial focus, an on-axis RMS spot radius of ≈ 81 µm in d-light and ≈ 105 µm polychromatic; after a Quick-Focus-like refocus (minimum field-averaged polychromatic RMS) the image plane moves ≈ 1.7 mm towards the lens and the on-axis polychromatic RMS drops to ≈ 60 µm. OpticStudio uses a different pupil sampling (hexapolar rings for the spot diagram), so expect agreement to within ~10 %, not to the micrometre.

**Snell's-law mini-example.** A ray in air hits a flat N-BK7 surface at 30°: $\sin I' = \sin 30° / 1.5168 = 0.3296$, so $I' = 19.25°$. Inside the glass, a ray hitting the glass–air surface at more than 41.2° is totally internally reflected.

---

## Key takeaways
- Lens design is about **image quality** at a given focal length, aperture and field, inside constraints of package, environment and cost — start from a clear specification.
- Rays are normals to wavefronts; geometrical optics is the $\lambda \to 0$ limit. Compare the geometric spot to the Airy disk ($2.44\lambda N$) to know whether ray or wave metrics matter.
- Snell's law $n\sin I = n'\sin I'$ is exact; its nonlinearity ($\sin I \neq I$) is the origin of monochromatic aberrations. Keep angles of incidence small.
- Fermat: real rays have stationary optical path; perfect imaging means equal OPL for all rays to the image point. Wavefront error = OPL error.
- In OpticStudio, global data (aperture, fields, wavelengths, catalogues) lives in the **System Explorer**; surface data lives in the **Lens Data Editor**; results come from **Analyze** windows.
- Solves (e.g. Marginal Ray Height) automate dependent quantities; Quick Focus finds best focus by adjusting the last thickness.
- Save lens files as `.zmx` (text, git-friendly); `.zda` restores your windows; `.zar` packages a design for someone else.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Ray | Line normal to the wavefront showing the direction of energy flow |
| Wavefront | Surface of constant phase / constant optical path length from an object point |
| Optical path length (OPL) | $\sum n_i d_i$; time of flight × $c$ |
| Refractive index $n$ | $c/v$; ratio of vacuum to material speed of light (wavelength dependent) |
| Snell's law | $n\sin I = n'\sin I'$ |
| Critical angle | $\arcsin(n'/n)$; above it, total internal reflection |
| Aberration | Departure of the real wavefront (or ray) from the ideal |
| PSF | Point spread function — the image of a point |
| Airy disk | Diffraction-limited PSF of a circular pupil; diameter $2.44\lambda N$ |
| EFL | Effective focal length |
| BFL | Back focal length: last surface to paraxial focus |
| EPD | Entrance pupil diameter (system aperture) |
| F-number $N$ | EFL/EPD for an infinite object |
| Paraxial | Small-angle approximation $\sin I \approx I$ |
| Lens Data Editor (LDE) | OpticStudio spreadsheet of surfaces |
| System Explorer | OpticStudio panel for aperture, fields, wavelengths, catalogues, units |
| Solve | A rule that sets a lens parameter automatically (e.g. Marginal Ray Height) |
| Quick Focus | Tool that adjusts the last thickness to minimize spot or wavefront error |
| Session file (.zda) | Stores open windows and their settings for a lens file |

## References
1. [Geary Ch. 1, pp. 1–8] J. M. Geary, *Introduction to Lens Design*, §1.1–1.2: motivation, imaging as convolution, aperture/field map, specifications.
2. [Geary Ch. 2, pp. 11–20] §2.2 data entry, §2.3 layout, §2.4 first-order properties, §2.6 keeping track of designs, §2.7 glass catalogue, §2.8 F-numbers and 0.707 zones.
3. [Kidger §1.1–1.5, pp. 1–6] M. J. Kidger, *Fundamental Optical Design*: coordinate system, rectilinear propagation, Snell's law, Fermat's principle, wavefronts and Malus–Dupin.
4. [Kenyon §1.2, pp. 6–8] I. R. Kenyon, *The Light Fantastic*: electromagnetic waves.
5. [Kenyon §2.1, pp. 31–36] Rays and Huygens' principle; reflection and Snell's law from Huygens and from Fermat; simple imaging.
6. Ansys Optics, "How to design a singlet lens – Part 1: Setup" — the official first-session walkthrough (F/4, 100 mm, N-BK7, HeNe; F-number solve): https://optics.ansys.com/hc/jp/articles/42661252179987
7. Ansys Optics, "How to design a singlet lens – Part 2: Analysis" — Cross-Section, Spot Diagram, Ray/OPD Fan, Quick Focus menu paths: https://optics.ansys.com/hc/en-us/articles/42661948544787
8. Ansys Optics, "How to design a singlet lens – Part 3: Optimization" — variables, Optimization Wizard, boundary values (used again in L07): https://optics.ansys.com/hc/en-us/articles/42661700528275
9. Ansys Optics knowledge base, OpticStudio file types (ZMX/ZOS, ZDA session files, CFG, ZAR/ZPRJ): https://optics.ansys.com/hc/en-us/articles/42661745091603
10. Ansys Innovation Space, "Creating a Singlet: Performance Analysis & Optimization – Getting Started with Ansys Zemax OpticStudio Part 2" (free video course): https://innovationspace.ansys.com/courses/?p=85680
