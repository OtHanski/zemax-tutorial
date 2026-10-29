# Zemax OpticStudio: from 101 to professional

A self-study programme in optical design with **Ansys Zemax OpticStudio** (Premium). It starts from scratch and goes up to intermediate/professional level, with an application focus on machine-vision cameras, structured-light projection, tolerancing and automation.

- **Structure:** 7 courses, 66 lessons. Each lesson folder has
  - `lecture-notes.md`: theory, OpticStudio how-to, a worked example, and references.
  - `tasks.md`: hands-on assignments (pen & paper, Python, OpticStudio), with hints and solutions in collapsible blocks.
- **References:** three books (Geary, Kidger, Kenyon) are the core corpus, plus linked public sources. See [`references/README.md`](references/README.md).
- **Map:** see [`CURRICULUM.md`](CURRICULUM.md) for every lesson with its readings.
- **Progress:** tick lessons off in [`PROGRESS.md`](PROGRESS.md).

## Courses

| # | Course | Lessons | Level |
|---|---|---|---|
| 01 | [Foundations: geometrical optics & OpticStudio basics](01-foundations/) | 8 | 101 |
| 02 | [Aberrations & classical lens design](02-aberrations-classical-design/) | 13 | 101 → 201 |
| 03 | [Image quality, optimization & physical optics](03-image-quality-optimization/) | 10 | 201 |
| 04 | [Machine-vision & camera lens design](04-machine-vision-camera-lenses/) | 10 | 301 (specialisation) |
| 05 | [Illumination, projection & non-sequential design](05-illumination-projection-nsc/) | 9 | 301 (specialisation) |
| 06 | [Tolerancing & manufacturing](06-tolerancing-manufacturing/) | 8 | 301 (specialisation) |
| 07 | [Automation with ZPL & the ZOS-API](07-automation-zpl-zosapi/) | 8 | 301 (specialisation) |

Take courses 01 → 02 → 03 in order. After that, courses 04–07 can be taken in any order. The capstones in 06 and 07 reuse the Course 04 capstone design.

## Suggested pace (≈ 1 year)

| Months | Work |
|---|---|
| 1–2 | Course 01 |
| 2–5 | Course 02 |
| 5–7 | Course 03 |
| 7–9 | Course 04 |
| 9–10 | Course 05 |
| 10–11 | Course 06 |
| 11–12 | Course 07 (or interleave it from Course 03 onwards; it is a good weekend companion) |

## How to work

1. Read the *Reading* section of the lesson, then the lecture notes.
2. Do the tasks. Save designs and notes in a `work/` folder inside the lesson folder, e.g. `01-foundations/L01-.../work/L01_T3_singlet.zmx`.
3. Commit your work. `.zmx` files are text, so diffs show prescription changes. Session files (`.ZDA`) and other OpticStudio clutter are git-ignored.
4. Lessons flag uncertain OpticStudio menu paths with "location varies by version". When you find the real path, fix the note in place and commit it; the course gets better as you go.

## Conventions

- Light travels left → right. Radii are positive when the centre of curvature lies to the right of the vertex. Thicknesses are positive left → right. See Course 01 L02.
- Standard visible wavelengths are F, d, C = 0.4861, 0.5876, 0.6563 µm. NIR lessons use 850 nm and 940 nm.
- Glass names follow the current SCHOTT catalog (N-BK7, N-SF5, …) unless stated otherwise.
