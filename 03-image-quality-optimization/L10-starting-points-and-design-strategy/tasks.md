# L10 — Tasks: Starting points, scaling and design strategy

> Work in `work/` inside this lesson folder (e.g. save `work/L10_T3_patent.zmx`). Commit your designs, `work/spec.md` and a short `work/notes.md` with answers.
> Estimated time: ~7 h (this is the course's integration lesson)

## Task 1 — Write and stress-test a specification (pen & paper / Python)
**Goal:** Practise turning a requirement into a feasible optical spec.
**Given / specs:** the lecture's 3D-camera receiver requirement: 800 mm field width at 1.0 m, 2448 × 2048 pixels of 3.45 µm, 850 nm (assume a ±15 nm LED/VCSEL band), sharp from 0.7 to 1.3 m, fixed focus, 0–45 °C operation, low cost, M12-size mechanics preferred.
**Steps:**
1. Copy the spec template from the lecture into `work/spec.md` and fill every line you can; mark unknowns as questions to the "customer".
2. Compute (Python) the first-order numbers: m, f, image distance, semi-field (horizontal, vertical, diagonal), EPD for F/2.8, F/4, F/5.6.
3. Feasibility: for each F/# compute diffraction-limited MTF at Nyquist and Nyquist/2, Airy diameter, the geometric blur at 0.7 and 1.3 m with focus set for symmetric blur, and the diffraction DOF. Add a thermal-defocus line using L09 (aluminium barrel, glass optics).
4. Write a one-paragraph recommendation with the trade-off and your preferred F/#.
**Deliverable:** `work/spec.md`, `work/first_order.py`, recommendation.
**Check yourself:** m = 0.01056; f = 10.45 mm; image distance 10.56 mm; diagonal semi-field 27.5° (horizontal ≈ 21.8°, vertical ≈ 18.5°); Newton focus positions 0.158 mm (0.7 m) and 0.085 mm (1.3 m) beyond f → ±36.8 µm; blur ≈ 13.1 / 9.2 / 6.6 µm at F/2.8 / F/4 / F/5.6; MTF_dl at 145 cycles/mm = 0.57 / 0.40 / 0.20; diffraction DOF (±2λN²) = ±13.3 / ±27.2 / ±53.3 µm; thermal defocus ≈ 0.22 µm/K for f ≈ 10.5 mm (Al barrel, glass lens) → ≈ 5.6 µm over +25 K.

<details><summary>Hints / solution sketch</summary>
Horizontal semi-field: atan(4.223/10.56) = 21.8°; vertical: atan(3.533/10.56) = 18.5°. Thermal: (23.6 − 2.15)×10⁻⁶ × 10.45 mm ≈ 0.224 µm/K. A defensible recommendation is F/4 with the pattern frequency (not Nyquist) as the sharpness criterion near the range ends, plus a request to the system team to confirm the depth range — but any well-argued choice is fine.
</details>

## Task 2 — A prescription toolkit (Python)
**Goal:** Automate the error-prone parts of reading and scaling prescriptions.
**Given / specs:** glass list (SCHOTT, $n_d$/$\nu_d$): N-BK7 1.51680/64.17, N-SK14 1.60311/60.60, N-SK16 1.62041/60.32, F2 1.62004/36.37, N-BAF10 1.67003/47.11, N-LAK7 1.65160/58.52, N-LAK22 1.65113/55.89, N-LAK9 1.69100/54.71, N-SF5 1.67271/32.25, N-SF6 1.80518/25.36.
**Steps:**
1. `glass_code(nd, vd)` → six-digit code; `nearest_glass(nd, vd)` → best match by a weighted distance (e.g. $|\Delta n_d|/0.01 + |\Delta\nu_d|/1$).
2. `conic_from_patent(K, convention)` for the two common sag conventions ($1-(1+K)c^2h^2$ → $k=K$; $1-Kc^2h^2$ → $k=K-1$).
3. `scale(prescription, s)` scaling radii, thicknesses, semi-diameters and even-asphere coefficients ($A_{2i} \to A_{2i}s^{1-2i}$).
4. Test: Kidger's telephoto (L06 Task 3 table, f = 100) scaled to f = 50; verify the result in OpticStudio (EFL = 50.000 after scaling).
5. Test the glass matcher on the codes 517642, 620603, 805254, 652585 and on a "patent" glass $n_d$ = 1.6935, $\nu_d$ = 53.2 (what is the nearest in the list, and how far off is it?).
**Deliverable:** `work/prescription_tools.py` + test output.
**Check yourself:** codes 517642 → N-BK7, 620603 → N-SK16, 805254 → N-SF6, 652585 → N-LAK7. 1.6935/53.2 → nearest N-LAK9 (1.6910/54.71; Δn = −0.0025, Δν = +1.5) — close enough for a model-glass start, not for a final design (use the real catalog with partial dispersion, or a model glass and later substitution). Scaled telephoto: all radii and thicknesses halved; telephoto ratio unchanged (0.909).

<details><summary>Hints / solution sketch</summary>
Glass code: `f"{round((nd-1)*1000):03d}{round(vd*10):03d}"`. For the asphere scaling remember that sag scales as $s$ and the radial coordinate as $s$: $A'_{2i}(sh)^{2i} = sA_{2i}h^{2i}$ ⇒ $A'_{2i} = A_{2i}s^{1-2i}$.
</details>

## Task 3 — Enter a real patent (OpticStudio)
**Goal:** Read a modern patent prescription end-to-end.
**Given / specs:** choose a patent on <https://patents.google.com> for a fixed-focal-length imaging lens with 4–6 elements, at least one aspheric surface, F/1.8–F/2.8, half field 20–40° (search e.g. `"imaging lens" "numerical example" aspheric "half angle of view"`; machine-vision, automotive or surveillance lenses are good choices). Record the patent number and example number in `notes.md`.
**Steps:**
1. Identify units/normalization, the stop, filter/cover glass, the sag equation and conic convention, and the aspheric terms used.
2. Enter it in OpticStudio (Even Asphere surfaces as needed; model glasses from $n_d/\nu_d$ first). Set aperture, field and wavelengths as the patent states.
3. Verify f, F/#, half field, image height and total length against the patent (≤ 0.5% differences expected with model glasses). Compare your field-curvature/distortion and longitudinal spherical plots with the patent's figures.
4. Replace model glasses by nearest catalog glasses (OHARA/SCHOTT/HOYA as appropriate) and re-optimize lightly to restore performance; note which glass swaps hurt.
**Deliverable:** `work/L10_T3_patent.zmx`, a verification table, a list of the conventions you had to interpret.
**Check yourself:** if EFL is right but aberration plots are clearly different, suspect the conic convention or a sign error in an aspheric coefficient; if EFL is off by a constant factor, the table is normalized.

## Task 4 — Scaling experiment (OpticStudio)
**Goal:** Verify the scaling laws.
**Given / specs:** your triplet `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx` (f = 50 mm, F/4, ±20°, F-d-C).
**Steps:**
1. Before touching OpticStudio, predict for scale factors s = 0.25 (f = 12.5 mm) and s = 4 (f = 200 mm): RMS spot radius, RMS wavefront (waves), Airy radius, and whether each version is closer to or further from the diffraction limit.
2. Scale the lens (Scale Lens / Make Focal tool) and measure: RMS spot at 0/14/20°, RMS wavefront, Airy radius, polychromatic MTF at 50 cycles/mm.
3. Re-optimize the f = 200 mm version (same merit function). How much of the loss can be recovered without changing the form?
**Deliverable:** prediction vs measurement table, 3–5 sentences.
**Check yourself:** RMS spot and RMS wavefront (in waves) scale by exactly s (0.25× and 4×) before re-optimization; the Airy radius stays 2.87 µm (1.22 × 0.5876 × 4). The 12.5 mm version is close to diffraction-limited where the 50 mm one was not; the 200 mm version is strongly aberration-limited and re-optimization recovers only part of the loss — a longer lens of the same F/# and field needs a more complex form.

## Task 5 — Candidate starting points for the receiver lens (OpticStudio)
**Goal:** Practise the "several starting points, one merit function" method; this prepares Course 04.
**Given / specs:** your Task 1 first order (f = 10.45 mm, your chosen F/#, 850 ± 15 nm, image height 5.5 mm, object at 1.0 m, cover glass 0.7 mm N-BK7), CRA ≤ 25°, TOTR ≤ 25 mm, |distortion| ≤ 2%.
**Steps:**
1. Prepare three candidates normalized to that first order: (a) your scaled Cooke triplet, (b) a sample-file objective (e.g. the double Gauss sample) scaled and stopped down, (c) your Task 3 patent lens scaled.
2. Build one merit function (L04 style) and save it as an `.MF` file; load it into each candidate.
3. Optimize each with DLS, then 10 minutes of Hammer.
4. Compare in a table: MTF at 72.5 and 145 cycles/mm (0/0.7/1.0 field), distortion, CRA, TOTR, element count, aspheres, and a quick sensitivity check (e.g. the RMS wavefront change for a 0.02 mm decenter of the most sensitive element — preview of Course 06).
5. Choose one with written reasons.
**Deliverable:** three files, comparison table, decision paragraph (also save it in `work/notes.md` — you will re-use it in Course 04 L10).
**Check yourself:** expect the patent-derived or 4-element candidate to win on performance, the triplet to win on simplicity and cost; the "best" choice depends on your stated priorities from `spec.md` — that is the point.

## Reflection questions
1. Why do most design projects fail at the specification or tolerancing stage rather than at optimization?
2. Why does scaling a lens down make it "better" relative to diffraction, and what does that imply for miniature cameras?
3. What are the three most common errors when entering a patent prescription?
4. When is it legitimate to start from a patent, and what must you check before shipping a product based on it?
5. Which three of Geary's sixteen design principles have you used most in this course, and where?

<details><summary>Answers</summary>

1. Infeasible or ambiguous specs make any optimization pointless; and nominal designs that ignore sensitivity fail as-built. Optimizers are good at the middle part; humans must get the ends right.
2. Geometric aberrations scale with size, diffraction (Airy radius ∝ λN) does not; a small lens at the same F/# and field has proportionally smaller aberrations in µm and in waves. Miniature cameras can therefore be fast and relatively simple, but they become diffraction- and pixel-limited and very sensitive to µm-level tolerances.
3. Wrong normalization/units; wrong conic convention (K vs K−1) or aspheric coefficient indexing/sign; mis-identified glass (or missing cover glass/filter, or wrong stop position).
4. As a learning tool and starting point it is always legitimate; patents are published to teach. Before commercial use, have a freedom-to-operate review (is the patent active in your markets, do your claims-relevant features match?), and in any case re-optimize to your own spec — the end design should be yours.
5. (Personal.) Typical answers: lens bending and stop position (Courses 01–02), splitting and balancing (L05), degrees of freedom/constraints (L04), Petzval control (Course 02 L04, L09).
</details>
