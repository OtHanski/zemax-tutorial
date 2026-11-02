# L05 — Opto-mechanics and CAD integration

> **Course 06 · Tolerancing and manufacturing** · Estimated time: lecture ~2.5 h, tasks ~5 h
> **Prerequisites:** [L02 — TDE and compensators](../L02-tolerance-data-editor-and-compensators/), [L04 — desensitization](../L04-desensitization-and-as-built-performance/), [03/L09 — thermal analysis](../../03-image-quality-optimization/L09-thermal-and-environmental-analysis/) · **Next:** [L06 — Drawings, ISO 10110 and vendor hand-off](../L06-drawings-iso10110-and-vendor-handoff/)

## Learning objectives
- Describe the common ways of mounting lenses (drop-in barrel with spacers and retainer, stacked M12-style barrel, cells, adhesive bonding, burnished/rolled cells) and which tolerances each creates.
- Distinguish element decenter/tilt (TEDX/TETX — the part in the barrel) from surface decenter/tilt (TSDX/TSTX — the part's own wedge), and set realistic values from a mechanical tolerance stack.
- Set the pivot of element tilts correctly (front vertex by default; the MPVT operand for mechanical pivots, Premium/Enterprise).
- Compute radial and axial thermal effects of an aluminium barrel on glass lenses (clearance closing, air-space change) and connect them to OpticStudio's thermal modelling.
- Export a design to CAD (STEP/IGES/SAT/STL, OpticsBuilder) and explain what the mechanical engineer needs from you.
- Explain what STAR does (FEA deformation and temperature data → optical performance), when you need it, and how it is licensed.

## Reading
- **Core (online):** Ansys Optics KB, "Mechanical Pivot Points (MPVT) in tolerance analysis": <https://optics.ansys.com/hc/en-us/articles/42661839385875>
- **Core (online):** Ansys Optics KB, "Exporting an OpticStudio lens system to CAD" (File → CAD Files; STEP/IGES/SAT/STL): <https://optics.ansys.com/hc/en-us/articles/42661776495251>
- **Core (online):** Ansys Optics KB, "STAR structural-thermal-optical (STOP) analysis of a smartphone lens module": <https://optics.ansys.com/hc/en-us/articles/42661767481747>
- **Online:** Ansys Optics KB, "Exporting to CAD with OpticsBuilder" (Prepare for OpticsBuilder, ZBD files): <https://optics.ansys.com/hc/en-us/articles/42661832095763>
- **Online:** Ansys Optics KB, "Importing FEA thermal and structural data with the STAR module": <https://optics.ansys.com/hc/en-us/articles/42661780285203>
- **Optional:** Ansys webinar "Introduction to the Ansys OpticStudio STAR module": <https://ansys.com/resource-center/webinar/introduction-ansys-opticstudio-star-module>
- **Online:** Ansys Optics KB, "Dynamic CAD link in Non-Sequential mode" (CAD Part: Creo Parametric / Autodesk Inventor, Premium): <https://optics.ansys.com/hc/en-us/articles/42661854410259>
- **Online:** Ansys Optics KB, Part Designer example (CAD Part: Zemax Part Designer, `.ZPO` files): <https://optics.ansys.com/hc/en-us/articles/42661822586003>
- **Online:** PADT, "Importing CAD into Ansys Zemax OpticStudio using Non-Sequential mode" (step-by-step with the CAD Part: STEP/IGES/SAT object): <https://www.padtinc.com/2022/08/18/zemax-opticstudio-cad-non-sequential/>
- **Corpus (short):** [Kidger §1.6, p. 6] — the aperture stop "may simply be part of the lens mount" (a spacer or barrel lip is often the stop — so its tolerances are optical tolerances); [Kidger §12.4.3, p. 249] — the detector must not "see" the lens mount (a stray-light/thermal-IR reason to model the barrel in NSC). The three books do not treat opto-mechanics in depth; the online sources and Yoder are the primary material here.
- **Optional (book, not in the course corpus):** P. R. Yoder Jr., *Mounting Optics in Optical Instruments* (SPIE Press) — the standard reference for lens mounting, preload and thermal effects.
- **Background:** [03/L09](../../03-image-quality-optimization/L09-thermal-and-environmental-analysis/) for TEMP/PRES configurations and thermal pickups.

---

## 1. How lenses are held

The optical designer's tolerance model is only as good as their picture of the mechanics. The main mounting styles:

```
 Drop-in barrel (spacers + threaded retainer)          Stacked M12-style barrel
  ┌───────────────────────────────────┐                 ┌───────────────────────┐
  │shoulder│ L1 │spacer│ L2 │spacer│ L3 │retainer         │ L1│sp│L2│sp│L3│sp│L4│ ring
  └───────────────────────────────────┘                 └───────────────────────┘
  each lens rides in the bore; axial position            everything referenced to the
  by spacers; decenter = bore/OD clearance               front shoulder through the stack
```

| Style | How position is defined | Dominant tolerances | Typical use |
|---|---|---|---|
| **Drop-in barrel** with spacers and a threaded retainer ring | radial: lens OD in barrel bore; axial: spacer lengths; tilt: spacer face parallelism and seat geometry | element decenter = radial clearance + bore runout; element tilt = spacer wedge; air spaces = spacer length tolerances (stack-up) | industrial and machine-vision lenses |
| **Stacked barrel** (M12 and many camera modules) | as above, but every lens and spacer stacked against one shoulder | CT errors propagate down the stack (TTHI with Int1 = Int2, L02) | compact cameras |
| **Individual cells** (each lens in its own precision cell, cells stacked or adjusted) | cell bore/OD, cell faces | cell-to-cell decenter, adjustable (centering/shimming) | high-end, alignment-turned lenses |
| **Burnished / rolled cell** | cell lip rolled over the lens edge | low cost, little adjustment, stress risk | small fixed optics |
| **Adhesive bonding** (RTV ring, UV epoxy) | glue line; lens positioned by fixture or active alignment | glue shrinkage, thermal mismatch, creep | camera modules (lens holder to sensor PCB), filters |
| **Molded plastic lens stacks** | interlocking flanges molded on each lens | very low decenter if molds are good; thermal | mobile/compact cameras |

**Contact geometry.** A spacer touches a curved lens surface on a circle ("sharp-corner", tangential or toroidal contact). The lens is located by that circle on the *optical* surface, not by its edge — so element tilt and decenter in such mounts are set by the seat circle, the spacer face, and how well the lens self-centres between two curved contacts. For weakly curved surfaces self-centering is poor and the edge (OD) decides.

**Preload.** The retainer must hold the lens against shock and vibration without stressing it. A common rule of thumb for a threaded retainer relates the tightening torque $Q$ to the axial preload $P$ via $P \approx Q/(0.2\,D_T)$, with $D_T$ the thread pitch diameter (Yoder). Over-preload causes stress birefringence and surface deformation; temperature changes the preload (aluminium expands more than glass, §3).

## 2. Element vs surface tolerances — the mechanical meaning

| Error | Origin | OpticStudio |
|---|---|---|
| Lens optical axis not coincident with its own edge (wedge) | **lens fabrication** (centering, L01) | surface tilt/decenter: TSTX/TSTY, TIRX/TIRY, TSDX/TSDY on one surface of the element |
| Lens edge not on the barrel axis | **barrel + lens OD** (radial clearance, bore runout) | element decenter TEDX/TEDY over the element's surfaces |
| Lens seated tilted | spacer/seat wedge, dirt, uneven retainer | element tilt TETX/TETY |
| Cemented pair: one element shifted relative to the other | cementing fixture | TEDX/TETX on a single element *inside* the pair, plus TEDX/TETX on the pair |
| Group or barrel tilted relative to the sensor | holder, PCB, glue | TETX/TETY on the image surface or on all lens surfaces |

**Pivot points.** Element tilts rotate by default about the **front vertex** of the first surface of the element/group. Real elements tilt about a mechanical feature: the contact circle on the seat, the rear edge held by a retainer, the barrel's centre. OpticStudio's **MPVT** control operand (Premium and Enterprise) sets the pivot ("Pivot At") for the element operands that follow it — the KB article names TEDX/TEDY/TEDR/TETX/TETY/TETZ: Front Vertex (0, default), Rear Vertex (1), Front Mechanical Edge (2), Rear Mechanical Edge (3) or Geometrical Center (4) (KB article in Reading). The pivot matters: a tilt about a point far from the vertex is a tilt *plus* a decenter. To first order, tilting by $\theta$ about a pivot a distance $L$ behind the front vertex moves the vertex sideways by

$$
\delta \approx L\,\theta \qquad (\theta \text{ in radians}).
$$

Example: a 5 mm thick element tilted 0.05° about its rear vertex decenters its front vertex by $5\times0.05\times\pi/180$ = 0.0044 mm — comparable to a typical element-decenter tolerance, so the pivot choice is not cosmetic. For a whole 15 mm barrel tilted 0.1° about its rear flange the front element moves 0.026 mm. Without MPVT (e.g. in Professional) you build the pivot with coordinate breaks and dummy surfaces and tolerance those coordinate breaks with the user-defined operands (TUDX/TUDY, TUTX/TUTY).

**Correlations.** Mechanical errors are often correlated: if the whole barrel is tilted, all elements tilt together (one TETX over all surfaces), and the individual element tilts are *additional*. Model the hierarchy: barrel-level tolerances first (one row each), then element-level.

## 3. Mechanical stack-ups and thermal effects

### 3.1 Tolerance stack-ups
- **Radial decenter** of a drop-in lens: half the diametral clearance (bore max − OD min) plus the bore's runout (coaxiality) relative to the barrel datum. Worst case adds linearly; statistical models add in quadrature or by simulation.
- **Air spaces** from $k$ spacers in series: worst case $k\,\Delta t$, RSS $\sqrt k\,\Delta t$ for independent spacers.
- **Tilt** from spacer parallelism $p$ over contact diameter $d_c$: $\theta \approx p/d_c$.

### 3.2 Temperature
Aluminium ($\alpha \approx 23.6\times10^{-6}$/K for 6061) expands about three times more than N-BK7 ($7.1\times10^{-6}$/K).
- **Radial:** the diametral clearance between bore and lens changes by $\Delta c = D(\alpha_\text{Al}-\alpha_\text{g})\Delta T$. On cooling the gap closes; once it is zero the barrel squeezes the lens (radial stress, birefringence, possible surface deformation and, in extreme cases, fracture). On heating the gap opens and decenter can grow — a camera calibrated at 25 °C sees its principal point move.
- **Axial:** spacers grow with $\alpha_\text{Al}$, lenses with $\alpha_\text{g}$; air spaces change and preload changes.
- These rigid-body effects at uniform temperature are modelled in OpticStudio's thermal analysis (TEMP in the Multi-Configuration Editor, thermal pickups for spacer materials; 03/L09). Gradients and stress-induced deformation need FEA → STAR (§5).

## 4. CAD integration

What the mechanical engineer needs from you:
1. **Surface geometry** with clear apertures *and* mechanical diameters (lens OD, chip zones/bevels, flats for seats).
2. **Element thicknesses** and edge thicknesses; datum surfaces.
3. **Ray envelope** (the beam footprint through the system — so baffles, spacers and the barrel do not clip light) and a **stray-light keep-out** suggestion.
4. **Tolerances** that the mechanics must hold: radial clearance, spacer lengths, parallelism, sensor tilt/position, plus the compensator mechanism and its range.
5. The **thermal** design intent (barrel material, which athermalization relies on which spacer material).

OpticStudio routes:
- **File tab → Export group → CAD Files** (the *Export CAD Files* tool): STEP, IGES, SAT or STL of a surface range (First/Last Surface), optionally with rays (Ray Pattern, Number Of Rays, Wavelength/Field = All). Rays can go to STEP/IGES/SAT but **not STL** (STL has no line entity). Set mechanical semi-diameters and edge flats in the LDE first so the solids have real edges. Two caveats from the KB article: (1) the CAD origin is the **Global Coordinate Reference** surface (System Explorer / Surface Properties) — set it to a mechanical datum (e.g. the barrel's front flange or the sensor plane) so the mechanical engineer does not have to re-place the parts; (2) exported aspheres/freeforms are **approximated** by CAD spline surfaces — fine for packaging, not for ray tracing them back.
- **STEP vs IGES vs SAT vs STL.** STEP (AP203/214) is the default for solids exchange with modern CAD; IGES is older and often arrives as loose surfaces that must be stitched; SAT is the ACIS kernel format; STL is a triangle mesh — fine for 3D printing a mock-up, poor for mechanical design.
- **OpticsBuilder** (for Creo and other CAD tools, check current availability): **File → Prepare for OpticsBuilder** creates a `.ZBD` file; the mechanical engineer builds the housing around the optics inside CAD, ray-traces there (clipped rays shown in red) and can send the assembly back to OpticStudio's non-sequential mode.
- **Import of mechanics into Non-Sequential mode** for stray-light, vignetting and ghost analysis of the real barrel (Course 05 L07): in the NSC Editor choose object type **CAD Part: STEP/IGES/SAT** (files go in `…\Zemax\Objects\CAD Files`) or **CAD Part: STL**; in Premium, **dynamic links** (CAD Part: Creo Parametric, CAD Part: Autodesk Inventor; SolidWorks link availability varies by version) open native part files and expose their dimensions as editable/optimizable NSC parameters. Match CAD units to Lens Units (OpticStudio warns on mismatch). Assign coatings, materials and scatter models per face after import — CAD files carry geometry, not optical properties.
- **Part Designer** (Part Designer tab): builds parametric solids (sketch mode or script mode) saved as `.ZPO` and inserted as **CAD Part: Zemax Part Designer**; exposed dimensions become NSC parameters. Handy for quick barrels, spacers and baffles when no CAD model exists yet.
- **Sequential → NSC conversion** (File tab → Convert to NSC Group; location varies by version) turns the lens into NSC objects; together with the imported barrel this is the usual path to a "real-housing" stray-light model.

## 5. STAR — Structural, Thermal, Analysis and Results

When temperature is not uniform or parts deform under load, uniform-temperature thermal modelling is not enough. Examples relevant to Zivid-type products:
- an image sensor or VCSEL/LED driver dissipating watts a few millimetres from the lens: axial and radial temperature gradients;
- lenses bonded or clamped in a plastic or aluminium holder: mount-induced deformation;
- a projector lens heated by absorbed LED/laser light (thermal lensing).

**STAR** imports FEA results into OpticStudio:
1. FEA (Ansys Mechanical or any FEA tool) computes temperature fields and structural deformations of the optical elements; results are exported per surface as text datasets (Ansys Mechanical has an ACT extension, "OpticStudio STAR Module: Ansys Data Export Extension"; other FEA packages write the documented text format — Help: The STAR Tab > FEA Data Group > Load FEA Data).
2. In OpticStudio's STAR tools, datasets are assigned to surfaces; deformations are **fit** to the surfaces (rigid-body motions are removed by default before the fit — they are better handled as tilts/decenters/thickness changes; the **Fit Assessment** tool reports RMS/PV fit errors); temperatures become a spatially varying index (modelled as a gradient index inside the element) through the material's thermal index data.
3. Standard analyses (spot, MTF, through-focus MTF, wavefront) then show the performance of the deformed, heated system; multi-time-point data (e.g. a warm-up) can be loaded as separate systems.

In the UI the STAR tools live on a **STAR tab** (Load FEA Data with *Load FEA* / *Load Multi FEA*, a Coordinate System control for the FEA export frame, **Fit Assessment**, **System Viewer**); a "STAR User Analysis" (Programming tab → User Analyses) plots criteria such as MTFA across FEA time points. The end-to-end process is often called STOP (structural–thermal–optical performance) analysis.

**Licensing:** the smartphone-module KB article lists the requirements as Ansys Zemax OpticStudio **Enterprise**, *or* legacy OpticStudio Professional/Premium **plus a STAR module licence**. Your Premium licence may or may not include it — check the license manager or Help → About for "STAR". If you do not have it, you can still do the poor-man's version: export rigid-body motions and average temperatures from FEA by hand into thermal configurations, and Zernike-fit surface deformations yourself into Zernike sag surfaces.

## 6. In OpticStudio — opto-mechanical tolerancing checklist
1. Draw the mechanical concept (sketch is fine) before setting element tolerances.
2. Barrel-level rows: TETX/TETY over all lens surfaces (lens-holder tilt), TEDX/TEDY (lens-holder decenter relative to sensor), sensor tilt.
3. Element-level rows: TEDX/TEDY = radial clearance + runout; TETX/TETY = seat/spacer wedge; MPVT where the pivot is not the front vertex.
4. Fabrication rows: wedge as TSTX/TIRX on one surface per element (spheres), both TSDX and TSTX for aspheres.
5. TTHI adjust surfaces matching the stack (drop-in vs stacked).
6. Thermal configurations with the barrel material (03/L09), and check clearances at the cold extreme.
7. Export to CAD with mechanical diameters and the ray envelope, Global Coordinate Reference on a mechanical datum; hold a design review with the mechanical engineer around the tolerance table.
8. Bring the mechanical model back: import the barrel (CAD Part: STEP/IGES/SAT) into an NSC version of the lens and check vignetting and stray light from spacer edges and barrel walls (Course 05 L07).

## Worked example — an aluminium drop-in barrel for a Ø10 mm lens

**Radial decenter.** Bore Ø10.000 +0.010/0, lens OD Ø10.000 0/−0.010, bore runout (coaxiality to the barrel datum) Ø0.010 (i.e. 0.005 mm radial).
- Worst case: radial clearance (0.020)/2 = 0.010 mm + 0.005 mm = **0.015 mm**.
- Statistical (bore and OD uniform in tolerance, lens position uniform in the clearance disc, runout uniform in its disc, random directions — $10^6$-sample simulation): mean 0.0047 mm, 95th percentile **0.0089 mm**, maximum just under the 0.015 mm worst case.
- In OpticStudio: TEDX = TEDY = ±0.0089/… — careful: per-axis normal ±2σ with σ = 0.0036 mm reproduces a 95th-percentile radial value of 0.0089 mm (Rayleigh: $\sigma\sqrt{-2\ln 0.05}$ = 2.448σ) → **TEDX = TEDY = ±0.0073 mm** (normal, ±2σ). Uniform per-axis ±0.0089 would be another defensible choice. State which you used.

**Tilt.** Spacer faces parallel to 0.005 mm across a contact diameter of 9 mm → θ = 0.005/9 rad = **0.032°** (TETX/TETY ±0.032°).

**Air-space stack.** Four spacers in series, each ±0.010 mm: worst case ±0.040 mm, RSS ±0.020 mm for the position of the last lens relative to the first. With the focus compensator, the common shift is absorbed; the individual air spaces each keep ±0.010 mm.

**Thermal clearance.** Operation 0–45 °C, assembly at 25 °C: cooling by 25 K closes the diametral clearance by $10\,\text{mm}\times(23.6-7.1)\times10^{-6}\times25$ = **4.1 µm**. A lens at its maximum-material condition with zero clearance at 25 °C would be squeezed at 0 °C — specify a minimum diametral clearance ≥ 5 µm (or a radially compliant mount) for this temperature range; for a Ø16 mm element the closure is 6.6 µm, and for a −40 °C storage spec on Ø10 mm ($\Delta T$ = 65 K) it is 10.7 µm — storage, not operation, often sets the minimum clearance. The axial counterpart: a 2 mm aluminium spacer grows by 0.94 µm for +20 K — negligible for most camera lenses, but for an air space that is a strong compensator it may not be (check with thermal configurations).

All numbers computed with `python3` (Task 1).

## Key takeaways
- Know the mount before you set element tolerances: drop-in, stacked, cells, bonded or rolled each produce different error structures.
- Surface tolerances = how the lens is made (wedge); element tolerances = how it sits in the barrel (clearance, seat wedge); barrel tolerances = how the lens sits on the sensor.
- Tilts pivot about the front vertex by default; use MPVT (Premium/Enterprise) or coordinate breaks for mechanical pivots.
- Stack-ups: worst case adds linearly, statistics add in quadrature; per-axis normal tolerances imply a Rayleigh radial distribution.
- Aluminium barrels close the radial clearance on cooling by $D(\alpha_\text{Al}-\alpha_\text{g})\Delta T$ — ~4 µm per 10 mm per 25 K.
- Export STEP/IGES with mechanical diameters and ray envelopes; review tolerances jointly with the mechanical engineer.
- STAR brings FEA deformations and temperature fields into OpticStudio; it is a licensed module (included in Enterprise).

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| Drop-in barrel | Lenses inserted into a bore, separated by spacers, clamped by a retainer |
| Retainer | Threaded or snap ring providing axial preload |
| Preload | Axial clamping force on a lens |
| Runout / coaxiality | Deviation of a bore's axis from the barrel datum axis |
| Pivot point | Centre of rotation of a tilted element (MPVT operand) |
| Stack-up | Accumulation of individual part tolerances along a chain |
| STAR | OpticStudio module for importing FEA (structural/thermal) results into optical analysis |
| Fit Assessment | STAR tool reporting how well FEA data are fitted on optical surfaces |
| OpticsBuilder / ZBD | CAD-side tool and exchange file for optics placed in a mechanical CAD model |

## References
1. Ansys Optics KB, "Mechanical Pivot Points (MPVT)": <https://optics.ansys.com/hc/en-us/articles/42661839385875>
2. Ansys Optics KB, "Exporting a lens system to CAD": <https://optics.ansys.com/hc/en-us/articles/42661776495251>
3. Ansys Optics KB, "Exporting to CAD with OpticsBuilder": <https://optics.ansys.com/hc/en-us/articles/42661832095763>
4. Ansys Optics KB, "STAR STOP analysis of a smartphone lens module": <https://optics.ansys.com/hc/en-us/articles/42661767481747>
5. Ansys Optics KB, "Importing FEA data with the STAR module": <https://optics.ansys.com/hc/en-us/articles/42661780285203>
6. Ansys Optics KB, dynamic CAD link (Creo/Inventor) in Non-Sequential mode: <https://optics.ansys.com/hc/en-us/articles/42661854410259>
7. Ansys Optics KB, Part Designer example (CAD Part: Zemax Part Designer): <https://optics.ansys.com/hc/en-us/articles/42661822586003>
8. PADT, "Importing CAD into Ansys Zemax OpticStudio using Non-Sequential mode": <https://www.padtinc.com/2022/08/18/zemax-opticstudio-cad-non-sequential/>
9. engineering.com, "Zemax announces Structural, Thermal, Analysis and Results (STAR) module" (name and scope of STAR): <https://www.engineering.com/zemax-announces-structural-thermal-analysis-and-results-star-module/>
10. [Kidger §1.6, p. 6; §12.4.3, p. 249] — stop as part of the mount; detector must not see the mount.
11. Ansys webinar, "Introduction to the Ansys OpticStudio STAR module": <https://ansys.com/resource-center/webinar/introduction-ansys-opticstudio-star-module>
12. Zemax Community, "Using STAR with other thermal and position settings in OpticStudio": <https://community.zemax.com/star-module-user-group-85/using-star-with-other-thermal-and-position-settings-in-opticstudio-4986>
13. P. R. Yoder Jr., *Mounting Optics in Optical Instruments*, SPIE Press (standard reference; not in the course corpus).
