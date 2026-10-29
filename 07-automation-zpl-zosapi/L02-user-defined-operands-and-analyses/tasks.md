# L02 — Tasks: User-defined operands, solves and analyses

> Work in `work/` inside this lesson folder. Macros in `work/macros/` (copy to your OpticStudio macro folder to run), C# projects in `work/csharp/` (commit source and `.csproj`/`.sln`, not `bin/` or `obj/`). Answers in `work/notes.md`.
> Estimated time: ~5 h (Tasks 1–3 core; Task 4 needs Visual Studio with the .NET desktop workload)

Test lenses:
- **Triplet:** `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx`.
- **NIR camera lens with filter:** your Course 04 L08 design (`../../04-machine-vision-camera-lenses/L08-filters-cover-glass-nir-and-ghosts/work/`), or the triplet with a 1 mm N-BK7 plate added 1 mm before the image, comment "FILTER" on its front surface.

---

## Task 1 — Working F/# via ZPLM (ZPL + OpticStudio)
**Goal:** Reproduce the Ansys ZPLM example end to end.
**Steps:**
1. Write `ZPL10.ZPL`: trace the real marginal ray (on axis, $P_y = 1$, primary wavelength), compute $F/\#_w = 1/(2 n' |M|)$ with $n' = 1$ (image space in air), `OPTRETURN 0, wfno`. Add a ray-failure branch returning a finite penalty.
2. In the triplet's MFE add `ZPLM` (Mac# 10, Data 0) and `WFNO` rows (weight 0). Update. Compare.
3. Change the EPD by 10 % and compare again.
**Deliverable:** macro, screenshot/text of the two MFE rows before and after.
**Check yourself:** the two values agree to ≥ 4 significant figures (Ansys reports exact agreement on its example, 4.9782 [ref 1 of the lecture]). If they differ in the 3rd digit, check: image-space medium, which wavelength `WFNO` uses, and whether the image surface is tilted/curved.

## Task 2 — Multi-value operand with Data slots (ZPL)
**Goal:** Understand the "runs only on Data = 0" rule.
**Steps:**
1. Implement `ZPL17.ZPL` from the lecture worked example (filter AOI, slot 0 = max AOI, slot 1 = spectral shift in nm). Use the filter-finding subroutine from L01 Task 4.
2. On the NIR lens add three groups of rows for $H_y$ = 0, 0.7, 1.0: `ZPLM 17 Data 0` followed by `ZPLM 17 Data 1`. Put a deliberate trap in: for $H_y$ = 1.0, place the Data-1 row *above* its Data-0 row. Update twice and explain what you see.
3. Add `MAXX` over the three AOI rows and an `OPLT` 24 constraint on it.
4. Pen & paper: verify the lecture's spectral-shift table (12°, 20°, 24° with $n_\text{eff}$ = 1.8, $\lambda_0$ = 850 nm), then compute the shift at 24° for $n_\text{eff}$ = 2.0.
**Deliverable:** macro, MFE excerpt, explanation of the trap, step 4 numbers.
**Check yourself:** on axis the max AOI equals the image-space marginal-ray angle: $\arcsin(1/(2F/\#_w))$ (12.0° at F/2.4). Step 4: $n_\text{eff}$ = 2.0 → $\lambda$ = 832.3 nm, shift −17.7 nm (a higher-index filter design shifts less). The misplaced Data-1 row shows the value left over from the previous Data-0 call (stale).

<details><summary>Solution sketch (step 4)</summary>

$\sin 24° = 0.40674$; $/2.0 = 0.20337$; squared 0.041359; $\sqrt{1 - 0.041359} = 0.97910$; $850 \times 0.97910 = 832.2$ nm (shift −17.8 nm, to rounding).
</details>

## Task 3 — Smooth vs hard maximum (Python + OpticStudio)
**Goal:** See why non-smooth operands hurt DLS.
**Steps:**
1. Python: for a toy "AOI" set $a_i(x) = 20 + 3\sin(x + i\pi/3)$, $i = 0…5$, plot over $x \in [0, 2\pi]$ the hard max and the soft max $\left(\frac1N\sum a_i^p\right)^{1/p}$ for $p$ = 4, 8, 16. Plot their numerical derivatives (central difference, $h$ = 10⁻³).
2. Add a variant of `ZPL17` returning the $p = 8$ soft max in slot 2.
3. On the NIR lens, set the AOI constraint to a target 2° below the current value (so it is active), and run DLS (automatic, same variables) twice: once constraining the hard max, once the soft max (with target adjusted so both demand the same reduction). Compare iterations to converge and final MF.
**Deliverable:** plots, comparison, 3-sentence conclusion.
**Check yourself:** the hard max has kinks (derivative jumps) where the maximal index switches; the soft max is smooth and lies slightly below the hard max (by less than ~1° for $p$ = 8 here). In the optimization, the soft version usually converges in fewer or equal cycles; the effect is larger with more rays/fields.

## Task 4 — Your first UDOC in C# (Visual Studio)
**Goal:** Build, deploy and call a compiled user operand.
**Steps:**
1. Generate the User Operand boilerplate (Programming tab → C# → User Operand; location varies by version). Open it in Visual Studio.
2. Implement the lecture's "sum of absolute thicknesses between surfaces s1 and s2" code. Set Output Type = Windows Application, configuration = Release. Name the assembly `UDOC05`.
3. Copy `UDOC05.exe` to `{Zemax}\ZOS-API\Operands` (Documents\Zemax\…). In the triplet MFE add `UDOC` Prog# 5 with arguments 1 and 6 (or the triplet's first and last lens surfaces); compare with a `TTHI` row over the same range (TTHI sums thicknesses — check its exact definition in the operand Help).
4. Extend it: return in slot 1 the *glass-only* thickness (skip surfaces whose material is blank/air — find the property name for the material in the Syntax Help, e.g. a `Material` string on the surface). Use Data = 1 to read it.
5. Measure: time 100 MF updates (Optimize → … or simply a DLS with 0 variables, or scripted later) with and without the UDOC row. Report ms per call.
**Deliverable:** source in `work/csharp/UDOC05/`, MFE excerpt, timing.
**Check yourself:** UDOC slot 0 = TTHI result for the same range (if both include the same surfaces). If OpticStudio reports a timeout or "cannot find", check the exe name (two digits), folder, and that you built Release. A console build pops up windows during updates — that's the classic mistake from the Ansys article.

<details><summary>Hints</summary>

- The template's comments show where `operandResults` is filled and written back; don't remove that code.
- If you don't want to install Visual Studio now, do Task 4 as reading only: open the sample `UDOC` source in the ZOS-API sample folder, annotate it line by line in `notes.md`, and return to it after L03 (which installs a .NET toolchain anyway).
</details>

## Task 5 — ZPL macro solve (OpticStudio + ZPL)
**Goal:** Keep a mechanical rule true automatically.
**Given:** the NIR lens with "FILTER" front surface. Requirement: the filter's rear face must be exactly 0.80 mm from the image plane, whatever the focus.
**Steps:**
1. Identify which thickness cell controls filter-to-image distance and which controls focus (the "FOCUS COMP" thickness *before* the filter).
2. Write `filter_gap.ZPL` as a solve on the thickness *after* the filter: it should return a value such that the gap is 0.80 mm. (Trivial, on purpose — first get the mechanics right: `SOLVERETURN`, no `UPDATE`.)
3. Make it non-trivial: return the gap that keeps the *edge* of the image-side filter footprint ≥ 0.5 mm away from a sensor-package wall at height 6.5 mm, using the real marginal ray at full field — think about whether this is allowed by the solve rules (ray data, position relative to the stop, which cells you depend on).
4. Vary FOCUS COMP and watch the solve react.
**Deliverable:** macro(s), short explanation of which rules from lecture §3 constrained your design.
**Check yourself:** step 2 behaves like a fixed thickness (sanity check). In step 3, the solve is after the stop, so ray data is allowed; it must not depend on cells after itself (the image surface is fine only if its position is not itself the result of a later solve).

## Stretch task
Write a minimal **User Analysis** that plots max filter AOI vs normalized field (21 points) as a 2D line plot, using the SampleAnalysis1 source as a guide. Deploy it to `ZOS-API\User Analysis`, open it on the NIR lens, and save a session file to confirm it restores.

## Reflection questions
1. Why does an operand macro run on a *copy* of the lens, and what does that rule out?
2. You have a 40-variable design and a custom metric that takes 0.5 s per evaluation. Is putting it in the MF reasonable for DLS? For Hammer? What would you do instead?
3. Why should a failing custom operand return a large finite number rather than zero or nothing?
4. When would you deliver a tool to colleagues as a User Analysis rather than a Python script?

<details><summary>Answers</summary>

1. The optimizer perturbs variables on its own copy to compute derivatives; your code must evaluate that perturbed state, not the GUI's lens. It rules out reading open windows (`GETT`), relying on UI state, and permanently changing the user's lens.
2. ≈ (40+1+a few) × 0.5 s ≈ 22+ s per DLS iteration — tolerable for a short final polish; impossible for Hammer (thousands of iterations). Instead: a cheaper surrogate in the MF (fewer rays, built-in operands), and evaluate the expensive metric in a Python outer loop every N optimization cycles (L07), or port it to a UDOC with batch ray tracing.
3. Zero (or a stale value) looks like a perfect result, so the optimizer *moves toward* the failure region; a large finite penalty pushes it away while keeping the MF numerically valid.
4. When non-programmers need it repeatedly inside OpticStudio, it should update with the lens and live in session files, and the output fits one of the four data types; a Python script is better for your own studies, batch work and anything under version control with tests.
</details>
