# L06 — Telecentric metrology lenses

> **Course 04 · Machine-vision & camera lens design** · Estimated time: lecture ~2 h, tasks ~4.5 h
> **Prerequisites:** [01/L04 — stops & pupils](../../01-foundations/L04-stops-pupils-fields/), [02/L13 — afocal systems](../../02-aberrations-classical-design/L13-eyepieces-afocal-relays-windows/), [L02](../L02-camera-first-order-design/), [L03](../L03-relative-illumination-and-telecentricity/) · **Next:** [L07 — Plastic optics and molded aspheres](../L07-plastic-optics-and-molded-aspheres/)

## Learning objectives
- Explain perspective (entocentric) magnification error and compute it for a given object displacement.
- Construct object-space and bi-telecentric (double-telecentric) systems from thin lenses: place the stop, compute magnification, length, stop and front-element diameters.
- Compute depth of field and resolution of a telecentric lens from object-side NA, magnification and pixel size, and recognise the NA trade-off.
- Write and interpret a telecentricity specification (slope in degrees, magnification change per mm) together with distortion, and estimate the resulting measurement error.
- Set up an object-space telecentric system in OpticStudio correctly (Object Space Is Telecentric, aperture type, fields) and measure telecentricity error with operands and multi-configuration.
- Know where telecentric optics appear around a 3D-camera business: calibration and inspection rigs, gauging of projector masks/DOEs, and why they are *not* used for the 3D cameras themselves.

## Reading
- **Core:** [Kidger §1.6, pp. 6–8] — aperture stop, chief and marginal rays, entrance and exit pupils, field stops: everything telecentricity is built from.
- **Core:** [Kenyon §4.5.3, p. 88] — telecentric lenses: stop in the second focal plane, "projected rather than perspective view", typical numbers (5 cm objective, 10–20 cm working distance, < 1 % scale change for ±10 mm).
- **Online:** Opto Engineering, "Telecentric lenses tutorial" — perspective error, telecentric slope (≈ 0.1°), bi-telecentric advantages: <https://www.opto-e.com/resources/telecentric-lenses-tutorial>
- **Online:** Edmund Optics, "Advantages of Telecentricity" and "Distortion and the Telecentricity Specification": <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/advantages-of-telecentricity/>, <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/distortion-and-the-telecentricity-specification/>
- **Online:** Edmund Optics, "Telecentric Design Topics": <https://www.edmundoptics.com/resources/application-notes/imaging/telecentric-design-topics/>
- **Online:** Ansys Optics KB KA-01552 (object-space telecentric setting; image-space telecentricity by solve or EXPP/RECI): <https://optics.ansys.com/hc/en-us/articles/42661811743251>

---

## 1. The problem: perspective

An ordinary ("entocentric") lens sees the world through a point — its entrance pupil. Objects further away appear smaller: for an object of height $H$ at distance $s$ from the entrance pupil, a small axial displacement $\delta s$ changes the image size by

$$
\frac{\delta H'}{H'} \approx -\frac{\delta s}{s}.
$$

Example (Opto Engineering's): $s = 200$ mm, $H = 20$ mm, $\delta s = 1$ mm → $\delta H = 0.1$ mm on the object scale — a 0.5 % error, far larger than the 1–10 µm accuracies wanted in gauging. Perspective also means that the sides of 3D parts (bores, pins, the walls of a box) are visible and that parallel edges converge. For **dimensional measurement** of parts whose position along the axis is not perfectly controlled, this is fatal.

## 2. Object-space telecentric lenses

### 2.1 Principle
Put the aperture stop at the **rear (second) focal point** of the front optics [Kenyon §4.5.3, Fig. 4.16]. Then the entrance pupil — the image of the stop through everything in front of it — is at **infinity**, and every chief ray in object space is **parallel to the axis**. Moving the object along the axis defocuses the image but does not move the centroid of each blurred point: the measured size is unchanged.

Consequences that follow directly from the geometry:
- The **front element must be at least as large as the object field** (plus the beam footprint): you can only measure what fits inside the front lens [Kenyon §4.5.3]. A 50 mm field needs a ~55–60 mm front lens. This is why telecentric lenses are big, heavy and expensive, and why they are not used for wide-field scene capture such as 3D bin picking.
- The **working distance** is roughly the front focal length (object near the front focal plane of the front group, so the image is formed behind the stop by the rear group).
- The illumination should match: a **telecentric (collimated) backlight** gives sharp silhouettes of 3D parts because only rays parallel to the axis are collected.

### 2.2 Image-space side
If only the object side is telecentric, the rays reaching the sensor still arrive at field-dependent angles. Sensor defocus (focus drift, sensor tilt) then changes the image scale (L03: $\delta h = \delta z\tan\text{CRA}$), and the sensor's angular response varies across the field.

## 3. Bi-telecentric (double-telecentric) lenses

Make the system **afocal**: two positive groups with focal lengths $f_1$ and $f_2$ separated by $f_1 + f_2$, with the stop at their common focal point (a Keplerian telescope, Course 02 L13). Then the stop is at the back focal point of group 1 (object-space telecentric) *and* at the front focal point of group 2 (image-space telecentric). The magnification is

$$
m = -\frac{f_2}{f_1},
$$

**independent of both object and sensor position** — the defining property of a gauging lens. With the object at the front focal plane of group 1, the image lies at the back focal plane of group 2, and the thin-lens length object → image is

$$
L = f_1 + (f_1+f_2) + f_2 = 2(f_1+f_2).
$$

For $m = -0.25$ with $f_1 = 200$ mm, $f_2 = 50$ mm: $L = 500$ mm. Real designs fold or compress this (telephoto front group, retrofocus rear group), but bi-telecentric lenses remain long; Kenyon quotes ~30 cm for a typical instrument [Kenyon §4.5.3].

**Aperture.** In a telecentric system the natural aperture specification is the **object-side NA**: the stop of radius $r_s$ at the focal point of group 1 gives $\text{NA} \approx r_s/f_1$. Image-side NA is $\text{NA}' = \text{NA}/|m|$, and the image-side working F/# is $N_w = 1/(2\text{NA}') = |m|/(2\text{NA})$.

## 4. Depth of field and resolution

With object-side NA, a point displaced by $\delta z$ from best focus is blurred on the object scale into a disc of diameter ≈ $2\,\text{NA}\,\delta z$. If the acceptable blur on the sensor is $c$, i.e. $c/|m|$ on the object,

$$
\text{DOF}_\text{geom} = \pm\frac{c}{2|m|\,\text{NA}} = \pm\frac{N_w c}{m^2}\quad\Longrightarrow\quad \text{total DOF} = \frac{2N_wc}{m^2}.
$$

The diffraction depth of field (quarter-wave criterion, Course 03 L03 / [Geary §32.2.2]) is $\pm\lambda/(2\,\text{NA}^2)$ in object space. Resolution goes the other way: the Airy radius on the object is $0.61\lambda/\text{NA}$. **NA is the master trade-off**: double the NA → half the Airy radius, a quarter of the diffraction DOF and half the geometric DOF.

Typical gauging lenses run at object-side NA 0.01–0.05 and working F/# 6–16. Bi-telecentric designs keep the defocused spot symmetric across the field (the image-side cone is identical everywhere), which in practice makes edge positions more robust through focus; Opto Engineering report the usable field depth appearing ~20–30 % larger than for object-only telecentric optics ([Opto Engineering tutorial](https://www.opto-e.com/resources/telecentric-lenses-tutorial)).

## 5. Specifying telecentricity

No real lens is perfectly telecentric: pupil aberrations make the chief-ray angle in object space vary over the field and with wavelength. Vendors specify the **telecentric slope** $\theta_t$ (degrees, maximum over the field), sometimes per colour ([Edmund Optics, "Distortion and the Telecentricity Specification"](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/distortion-and-the-telecentricity-specification/)). An object displaced by $\delta s$ shifts its image (on the object scale) by

$$
\delta H = \delta s\,\tan\theta_t .
$$

A good lens has $\theta_t \approx 0.1°$: $\delta H = 1.7$ µm per mm of displacement — about 60× better than the entocentric example of §1 ([Opto Engineering](https://www.opto-e.com/resources/telecentric-lenses-tutorial)). The same idea applies on the image side (sensor focus shift × image-side slope).

A complete metrology error budget for a measured length $\ell$ combines:
1. **Telecentric slope** × axial position uncertainty (per field point, sign matters: slopes pointing outward vs inward change the size in opposite ways).
2. **Distortion** — telecentric lenses typically have ~0.1 % or less ([Opto Engineering](https://www.opto-e.com/resources/telecentric-lenses-tutorial)), often wavy (Edmund advises reading the curve, not the single number). Calibrated away if stable.
3. **Magnification stability** with temperature and wavelength (lateral colour).
4. **Edge-detection uncertainty**: blur, contrast and noise (MTF at the relevant frequency).

## 6. In OpticStudio

- **Object-space telecentric:** System Explorer → Aperture → *Object Space Is Telecentric*. The entrance pupil is placed at infinity: chief rays leave the object parallel to the axis. Angle fields and ray aiming are not allowed with this setting, and placing the stop at surface 1 is recommended ([KA-01552](https://optics.ansys.com/hc/en-us/articles/42661811743251)). Use *Object Height* fields and an aperture type that makes sense with an infinite entrance pupil — *Object Space NA* is the natural choice (check in your version which types are permitted with the flag).
- **Real stop location:** the flag defines how rays are launched; the *physical* stop must still sit at the focal point of the front group for the real lens to be telecentric. A good habit: design with the flag on, then verify by turning it off, putting the aperture on the physical stop surface (Float By Stop Size) and checking that the object-space chief-ray angles stay small.
- **Measuring telecentricity:** with the flag off, the real chief-ray angle in object space is the angle of the chief ray leaving surface 0 — use **RAED** or **RANG** on the object/first surface (RANG in radians) for several field points; on the image side, **RAID** at the image surface. Alternatively use a Multi-Configuration with the object thickness ±1 mm (no refocus) and compare chief-ray image heights (**REAY**) — that is literally the vendor's spec.
- **Image-space telecentric:** curvature solve on the last powered surface, or **EXPP** (weight 0) with **RECI** targeted to 0, or **RANG** on the last powered surface ([KA-01552](https://optics.ansys.com/hc/en-us/articles/42661811743251)).
- **Magnification:** **PMAG** gives paraxial magnification; for the real one, divide REAY at full field by the object height. Constrain with PMAG or with REAY targets.
- **Distortion:** DIMX / Field Curvature & Distortion; for a bi-telecentric lens look at the Grid Distortion too.

## Worked example — a 0.25× bi-telecentric gauging lens for a 2/3" sensor

**Given:** $m = -0.25$, sensor 8.45 × 7.07 mm (diag 11.01 mm), $p = 3.45$ µm, λ = 0.55 µm, object-side NA = 0.02, $c = 2p$.

1. **Object field:** 33.8 × 28.3 mm (diag 44.0 mm).
2. **Thin-lens layout:** $f_1 = 200$ mm, $f_2 = 50$ mm, $L = 500$ mm. Stop diameter $2f_1\text{NA} = 8.0$ mm. Front lens clear diameter ≥ 44.0 + 8.0 = 52 mm (each object point sends a cone of radius $f_1\text{NA} = 4$ mm to the front lens).
3. **Working F/#:** $N_w = 0.25/(2\cdot0.02) = 6.25$.
4. **Depth of field:** geometric total $2N_wc/m^2 = 2\cdot6.25\cdot0.0069/0.0625 = 1.38$ mm; diffraction ±$0.55\,\mu\text{m}/(2\cdot0.02^2)$ = ±0.69 mm.
5. **Resolution:** object-space pixel 13.8 µm; Airy radius on the object 16.8 µm. Diffraction MTF at the sensor Nyquist (145 lp/mm) at $N_w = 6.25$: 0.39. To reach 0.5 at Nyquist you would need $N_w \le 5.1$ (NA ≥ 0.025) — at the cost of DOF.
6. **Telecentric error:** with $\theta_t = 0.1°$ and parts varying ±1 mm in height: ±1.7 µm (≈ 0.13 object pixels). With a 16 mm entocentric lens at 200 mm, the same ±1 mm would change a 20 mm feature by ±100 µm.

## Key takeaways
- Entocentric lenses have perspective: $\delta H/H \approx -\delta s/s$.
- Object-space telecentric: stop at the rear focal point of the front group; entrance pupil at infinity; front lens ≥ object field.
- Bi-telecentric: afocal, stop at the common focus, $m = -f_2/f_1$ independent of object and sensor position, length ≈ $2(f_1+f_2)$ thin-lens.
- Object-side NA sets resolution ($0.61\lambda/\text{NA}$) and DOF ($2N_wc/m^2$, $\pm\lambda/2\text{NA}^2$) in opposite directions.
- Specify telecentric slope (deg) and read distortion curves; error $= \delta s\tan\theta_t$.
- In OpticStudio use *Object Space Is Telecentric* with Object Height fields and Object Space NA, then verify the physical stop with the flag off; measure slopes with RAED/RANG/REAY multi-config.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Entocentric | Ordinary lens with entrance pupil at a finite position (perspective) |
| Object-space telecentric | Entrance pupil at infinity; chief rays parallel to the axis in object space |
| Bi-/double-telecentric | Telecentric in object and image space; afocal construction |
| Telecentric slope $\theta_t$ | Residual chief-ray angle (deg); image shift per unit axial displacement |
| Hypercentric (pericentric) | Entrance pupil beyond the object; sees sides of objects ("around" them) |
| Telecentric backlight | Collimated illumination matching a telecentric lens |
| Object-side NA | $\sin$ of the marginal-ray half-angle at the object; natural aperture spec for telecentric lenses |

## References
1. [Kidger §1.6, pp. 6–8] — stops, pupils, chief and marginal rays, field stops.
2. [Kenyon §4.5.3, p. 88] — telecentric lenses in machine vision.
3. [Geary §32.2.2, pp. 370–371] — diffractive depth of focus (quarter-wave criterion).
4. Opto Engineering, "Telecentric lenses tutorial": <https://www.opto-e.com/resources/telecentric-lenses-tutorial>
5. Edmund Optics, "Advantages of Telecentricity": <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/advantages-of-telecentricity/>
6. Edmund Optics, "Distortion and the Telecentricity Specification": <https://www.edmundoptics.com/knowledge-center/application-notes/imaging/distortion-and-the-telecentricity-specification/>
7. Edmund Optics, "Telecentric Design Topics": <https://www.edmundoptics.com/resources/application-notes/imaging/telecentric-design-topics/>
8. Ansys Optics KB KA-01552, image-space telecentric lenses and the object-space telecentric flag: <https://optics.ansys.com/hc/en-us/articles/42661811743251>
