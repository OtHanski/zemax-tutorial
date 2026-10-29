# L02 — User-defined operands, solves and analyses

> **Course 07 · Automation with ZPL and the ZOS-API** · Estimated time: lecture ~2.5 h, tasks ~5 h
> **Prerequisites:** [L01 — ZPL macro fundamentals](../L01-zpl-macro-fundamentals/), [Course 03 L04 (merit function mastery)](../../03-image-quality-optimization/L04-merit-function-mastery/) · **Next:** [L03 — ZOS-API architecture and Python setup](../L03-zos-api-architecture-and-python-setup/)

## Learning objectives
- Put a custom ZPL computation into the merit function with `ZPLM`, pass inputs through Hx/Hy/Px/Py (`PVHX()`…), return one or many values with `OPTRETURN`, and use the Data column correctly.
- Write a ZPL macro *solve* (`SOLVERETURN`) and state the rules that keep solves from breaking the lens.
- Explain the ZOS-API extension points — User Operand (`UDOC`), User Analysis, User Extension — and what each can and cannot access.
- Read and adapt the C# User Operand and User Analysis boilerplate templates (build type, naming, folder).
- Estimate the run-time cost of a custom operand inside DLS/Hammer optimization, and choose between ZPLM, UDOC, built-in operands and a scripted outer loop.
- Recognize obsolete mechanisms (`UDOP`, DDE) in old files and know the migration path.

## Reading
- **Core (online):** Ansys KB, D. Hill, optimizing with a user-defined ZPL macro (ZPLM; working-F/# example) — <https://optics.ansys.com/hc/en-us/articles/42661785079315>
- **Core (online):** Ansys KB, A. Croce, ZPLM with a centre-of-mass constraint (PVHX/PVHY, OPTRETURN, multiple return values) — <https://optics.ansys.com/hc/en-us/articles/43071134436883>
- **Core (online):** Ansys KB, N.-H. Kim (upd. A. Croce), ZPL macro solves (`SOLVERETURN`, rules) — <https://optics.ansys.com/hc/en-us/articles/43071107400467>
- **Core (online):** Ansys KB, H. Hu, creating a User Operand with the ZOS-API (C#, UDOC##, build settings) — <https://optics.ansys.com/hc/en-us/articles/42661799284499>
- **Core (online):** Ansys KB, T. Pickering, creating a User Analysis with the ZOS-API — <https://optics.ansys.com/hc/en-us/articles/42661869482131>
- **Optional:** Ansys KB, T. Jacobs, overview of the ZOS-API sample files and connection modes — <https://optics.ansys.com/hc/en-us/articles/42661773562899>
- **Optional:** Zemax Community, "Are UDOPs supported in OpticStudio any more?" — <https://community.zemax.com/licensing-and-installation-8/are-udops-supported-in-opticstudio-any-more-4088>
- **In the software:** Help → Merit Function Editor operand list (`ZPLM`, `UDOC`); Help → ZOS-API → the sample code folder (`Documents\Zemax\ZOS-API Sample Code` or similar; location varies by version).

---

## 1. Why customize the merit function at all?

The operand library has hundreds of entries, but real specifications keep producing quantities nobody built an operand for:

- the maximum angle of incidence on a bandpass filter **over the whole pupil and all fields** (Course 04 L08, capstone spec S7);
- the residual of a Brown–Conrady distortion fit, in pixels (capstone S12);
- a 3D-camera depth-noise proxy combining MTF at the fringe frequency with the triangulation geometry (Course 04 L09);
- a centre-of-mass constraint for a handheld or gimballed optic [2];
- a "smoothness" metric on an aspheric departure, or a molding-friendly slope limit.

Three ways to get such a number into an optimization:

```
             fast to write ─────────────────────────────► fast to run
   ┌──────────────────┐   ┌────────────────────┐   ┌─────────────────────┐
   │ Built-in operands│   │ ZPLM + ZPL macro   │   │ UDOC (compiled C#/  │
   │ + math operands  │   │ (interpreted)      │   │ C++ via ZOS-API)    │
   └──────────────────┘   └────────────────────┘   └─────────────────────┘
           ▲ always try this first
   And outside the MF: a Python outer loop (L07) that calls OpticStudio's optimizer.
```

**Always try built-in operands first.** Math operands (`SUMM`, `DIFF`, `PROD`, `DIVI`, `SQRT`, `ABSO`, `MAXX`, `MINN`, `OPGT`, `OPLT`, …; Course 03 L04) can build surprisingly complex expressions from other rows: the maximum AOI over a handful of rays is a `MAXX` over `RAID` rows. Only when the expression needs loops, branching or data that operands can't produce do you write code.

## 2. ZPLM: a ZPL macro as an operand

### 2.1 Mechanics
- The macro file must be named `ZPLnn.ZPL`, $nn$ = 00…99, in the macro folder [1][2].
- In the MFE, the `ZPLM` row has the arguments **Mac#**, **Data**, **Hx, Hy, Px, Py** [2].
  - **Mac#** = $nn$ selects the file.
  - **Hx, Hy, Px, Py** are four free numeric inputs. The macro reads them with `PVHX()`, `PVHY()`, `PVPX()`, `PVPY()`. They need not be normalized field/pupil coordinates; use them as surface numbers, wavelengths, frequencies, whatever [2].
  - **Data** selects which of the macro's results this row reports.
- The macro returns values with `OPTRETURN n, value` into a global result array, $n$ = 0…50 [2] (one KB article spells it `OPRETURN`; the keyword list in your Help is authoritative — it's `OPTRETURN` in current documentation [2]).
- **The macro executes only for rows with Data = 0.** Rows with other Data values read results stored by the most recent Data-0 call [2]. So: one `ZPLM … Data 0` row first (it runs the macro and reports result 0), then further `ZPLM` rows with the same Mac# and Data = 1, 2, … to expose more results without re-running.

```
 MFE row   Type   Mac#  Data  Hx  Hy  Px  Py   Target  Weight   ← reads OPTRETURN slot
   12      ZPLM    17    0    1   0   0   0    24.0    0         (runs ZPL17, slot 0)
   13      ZPLM    17    1    1   0   0   0    0       0         (slot 1, no rerun)
   14      OPLT   12           ...                24.0    10      (constrain row 12 ≤ 24°)
```

### 2.2 The rules of the game
- **Runs on a copy.** Operand macros (and UDOCs) work on a temporary copy of the system; UI-related commands (`GETT()`, window handling) are ineffective [L01 ref 7], [6].
- **Don't modify the lens** you are evaluating, except temporarily and restored before returning; never call `OPTIMIZE` inside an operand.
- **Fail loudly but finitely.** If a ray fails, return a large but finite penalty (e.g. 1e3 in the operand's units) rather than nothing, so the optimizer moves away instead of silently using stale numbers. Document the convention in the macro header.
- **Units and weight.** The returned number has whatever units you chose; its MF contribution is weight × (value − target)². The centre-of-mass article uses a very small weight for this reason [2]. Better: return values already scaled to "fraction of tolerance" (Course 03 L04 tolerance weighting), so weight 1 means "as important as the IQ block".
- **Smoothness.** DLS computes derivatives by finite differences. An operand that jumps (e.g. a `MAX` over rays that switches which ray is maximal, or a ray that becomes vignetted) has kinks; the optimizer can stall. Prefer smooth surrogates where possible — e.g. an RMS-like soft maximum $\left(\sum_i x_i^p / N\right)^{1/p}$ with $p \approx 8$ instead of a hard max.

### 2.3 Cost inside the optimizer
Each DLS iteration evaluates the merit function roughly $(N_\text{var} + 1)$ times for the Jacobian plus a few times for the line search/damping. If your macro takes $t_m$ per call:

$$
t_\text{iter} \gtrsim (N_\text{var} + 1 + k_\text{damp})\, t_m ,
$$

with $k_\text{damp}$ a handful. Ansys's own benchmark found a ZPLM working-F/# operand costs only ~0.5 s extra over native `WFNO` for a whole triplet optimization [1] — cheap macros are fine. A macro that traces a 41 × 41 pupil grid at 5 fields (≈ 6600 rays, 0.1–1 s interpreted) in a 25-variable lens costs tens of seconds per iteration — and Hammer runs thousands of iterations. That is the point where you move to a compiled UDOC, or to a cheaper sample (Gaussian-quadrature rings instead of a dense grid).

## 3. ZPL macro solves

A *solve* sets one editor cell from a computation every time the lens updates (Course 01 L07). A **ZPL Macro** solve type lets a macro do that computation [3]:

- Choose solve type "ZPL Macro" on almost any editor cell and enter the macro name (no `.ZPL` needed) [3].
- The macro computes the value and hands it back with **`SOLVERETURN value`** [3].
- On radius cells the solve works in **curvature**: return $1/R$, not $R$ [3].
- On error (vignetting, TIR), exit **without** `SOLVERETURN`, so the cell is not overwritten [3].
- **Never** call `UPDATE` in a solve (infinite loop risk), never use `INPUT`, change only the solved cell, don't depend on data that comes after the cell, don't use ray data in solves before the stop, keep it short [3].

Typical uses: a thickness that keeps an *edge* clearance to a mechanical part; a semi-diameter that follows a footprint plus margin; an air gap that places a filter at a fixed distance from the sensor in every configuration; a radius that makes a surface aplanatic for the real (not paraxial) marginal ray.

## 4. The ZOS-API extension points

The ZOS-API (L03 in depth) offers five ways for code to talk to OpticStudio [5]:

| Mode | Who starts it | UI | Typical use | Notes |
|---|---|---|---|---|
| **Standalone application** | Your program; launches a hidden OpticStudio instance | none | batch jobs, pipelines, CI-like reports (L04–L08) | consumes a licence seat/instance |
| **Interactive extension** | Your program; connects to an OpticStudio you already have open | live | notebook-driven exploration while watching the GUI | must enable it in OpticStudio first |
| **User extension** | Launched from OpticStudio's Programming tab | optional updates | tools for colleagues ("click to run") | compiled exe in the Extensions folder |
| **User analysis** | An analysis window | OpticStudio graphics | custom plots/tables that live in the GUI and the session file | one data type per analysis |
| **User operand** (`UDOC`) | A merit-function row | none | compiled custom operand | works on a copy; no access to open analyses [5] |

### 4.1 User Operand (UDOC)
From the Ansys walkthrough [4] and sample-file overview [5]:

- Must be **compiled** — C# or C++ only (not Python or MATLAB) [5].
- Start from the boilerplate: Programming tab → C# → User Operand (location varies by version; the generated Visual Studio solution lands in the ZOS-API Projects folder) [4].
- The executable must be named **`UDOCnn.exe`** ($nn$ = 00…99) and placed in `{Zemax}\ZOS-API\Operands` [4][5]. In the MFE, `UDOC` with **Prog#** $= nn$.
- Inputs arrive as `TheApplication.OperandArgument1…4` (fixed names, filled from the UDOC row's argument columns) [4].
- Results go into the `operandResults[]` array; the UDOC row's **Data** column selects which element is reported (0 → element 0) [4].
- A **Timeout** argument limits how long OpticStudio waits for the result (ms) [4].
- Build as **Windows Application** (not Console, or a console window pops up on every evaluation) and in **Release** mode for distribution [4].

The core of a UDOC (adapted from the Ansys "sum of thicknesses" example [4]; the template supplies the surrounding plumbing — keep it as generated):

```csharp
// --- inside the template's "Add your custom code here..." block ---
// Inputs from the UDOC row (names fixed by the template)
int s1 = (int)TheApplication.OperandArgument1;
int s2 = (int)TheApplication.OperandArgument2;

IOpticalSystem sys = TheApplication.PrimarySystem;   // a COPY of the lens being optimized
int nSurf = sys.LDE.NumberOfSurfaces;

if (s1 < 1 || s2 >= nSurf || s1 > s2)
{
    operandResults[0] = 1e9;          // invalid input → big penalty (Ansys example convention)
}
else
{
    double sum = 0.0;
    for (int s = s1; s <= s2; s++)
        sum += Math.Abs(sys.LDE.GetSurfaceAt(s).Thickness);
    operandResults[0] = sum;          // Data = 0 returns this
}
// Template code after this block writes operandResults back to OpticStudio.
```

Verify property names (`LDE`, `NumberOfSurfaces`, `GetSurfaceAt`, `Thickness`) against your installed version's ZOS-API Syntax Help; they have been stable for many releases.

**Why UDOC beats ZPLM for heavy work:** compiled code, and inside a UDOC you can use the API's **batch ray trace** (L06), which traces thousands of rays per call with far less overhead than `RAYTRACE` one-by-one. The ZOS-API also ships a sample UDOC computing surface sag via `ILensDataEditor.GetSag` [5].

### 4.2 User Analysis
A User Analysis is a compiled program that fills an OpticStudio analysis window with your data — a custom plot that lives in the GUI, updates with the lens, and can be saved in the session [6]:

- Boilerplate: Programming → C# → User Analysis; build **Release**; move the executable to `{Zemax}\ZOS-API\User Analysis`; it then appears under Programming → User Analyses [6].
- One output type per analysis: **2D line plot, 2D grid plot, 2D RGB grid plot, or text** [6].
- Window title via `TheAnalysisData.WindowTitle`; a line plot is created with `TheAnalysisData.Make2DLinePlot(...)` and series added with `AddSeries(...)` [6].
- A **settings dialog** (key–value dictionary: integer, float, double, boolean, string, byte) lets users choose surface, range, frequency etc. instead of hard-coding [6].
- Sample: `SampleAnalysis1.cs` reproduces FFT MTF vs Field [5] — read it before writing your own.

Sketch of the data part (structure only; method signatures differ by version — **verify against your installed version's ZOS-API Syntax Help** and the shipped sample):

```csharp
TheAnalysisData.WindowTitle = "Filter AOI vs image height";
// compute x[] = image heights (mm), y[] = max AOI (deg) with batch ray trace ...
var plot = TheAnalysisData.Make2DLinePlot(/* title, number of points, x data, ... */);
plot.AddSeries(/* "max AOI", y data, colour ... */);
```

When is a User Analysis worth it? When colleagues who don't script need the plot inside OpticStudio, repeatedly, with the lens. For your *own* analysis work a Python script with matplotlib (L05) is faster to write and easier to version.

### 4.3 User Extension
A compiled program launched from the Programming tab that gets full access to the open system and (optionally) suspends UI updates while it works [5] — the right packaging for "button-press" tools for a team (e.g. "export the Zivid standard design report"). The Python equivalent for your own use is the interactive-extension connection (L03).

## 5. Legacy: DDE and UDOP

Before the ZOS-API, external programs talked to Zemax via Windows **DDE**, and user operands via the **`UDOP`** operand driven by DDE executables. DDE has been shut down in the Ansys Zemax OpticStudio releases, so `UDOP` and DDE tools (including old MATLAB/Python DDE toolboxes such as PyZDDE) no longer work; staff recommend porting to the ZOS-API, and a KB guide maps DDE data items to ZOS-API methods [7]. If an old design file contains a `UDOP` row, replace it with `ZPLM`, `UDOC` or built-in operands.

## 6. Choosing — a decision table

| Need | First choice | Why |
|---|---|---|
| Combination of existing operand values | Math operands in the MFE | zero code, fully transparent, fast |
| Loop/branch over a few dozen rays, prototype | `ZPLM` | minutes to write; fine speed |
| Same, but thousands of rays or used in Hammer/Global | `UDOC` (C#) with batch ray trace | compiled, vectorized tracing |
| Keep a cell consistent with a rule | ZPL macro solve (or built-in solve) | updates on every lens change |
| Custom plot for non-programming colleagues | User Analysis | lives in the GUI/session |
| Custom metric for *your* study, sweeps, reports | Python standalone (L04–L08) | numpy/pandas/matplotlib, git |
| Metric too expensive to put in the MF at all | Python outer loop around OpticStudio's optimizer (L07) | evaluate it every N iterations |

## 7. In OpticStudio — pitfalls
- **Stale results:** rows with Data ≠ 0 show the values from the last Data-0 call; if the Data-0 row is *below* them in the editor, they show the previous evaluation. Put the Data-0 row first.
- **Macro not found:** after adding a `ZPLnn.ZPL` or solve macro, refresh the macro list (Programming tab) [3]; check the folder in Project Preferences.
- **UDOC not found / timeout:** wrong name (`UDOC7.exe` vs `UDOC07.exe`), wrong folder, Debug build missing runtime libraries, or a console build stealing focus [4].
- **Multi-configuration:** an operand macro evaluates the *current* configuration of the copy. To evaluate configuration 3, put a `CONF 3` row above it in the MFE (that's how the MFE handles configuration-dependent rows), rather than switching configurations inside the macro.
- **Non-smooth operands** stall DLS: check the operand value vs a variable with a quick scan (the macro from L01 Task 5 adapted) before optimizing with it.
- **Licence/edition:** ZPL and ZPLM work in all editions; the ZOS-API extension points require an edition that includes the API (Premium/Professional — check your licence's feature list).

## Worked example — a ZPLM filter-AOI operand and its optimization cost

**Goal:** constrain the maximum AOI on the bandpass filter of the Course 04 capstone (S7: ≤ 24°) and understand what the limit means spectrally.

**(a) Physics.** A thin-film interference filter's centre wavelength shifts blue with AOI $\theta$:

$$
\lambda(\theta) = \lambda_0 \sqrt{1 - \left(\frac{\sin\theta}{n_\text{eff}}\right)^2},
$$

where $\lambda_0$ is the normal-incidence centre wavelength and $n_\text{eff}$ the filter's effective index (Course 04 L08). With $\lambda_0$ = 850 nm and $n_\text{eff}$ = 1.8:

| AOI | $\lambda(\theta)$ | shift |
|---|---|---|
| 12° | 844.3 nm | −5.7 nm |
| 20° | 834.5 nm | −15.5 nm |
| 24° | 828.0 nm | −22.0 nm |

So the spec's 24° corresponds to a ~22 nm shift that the filter's passband design must absorb — the reason the AOI is constrained, and why returning the *shift in nm* (slot 1) is more meaningful to a reviewer than the angle.

**(b) The macro** (`ZPL17.ZPL`; inputs: Hx = field fraction $H_y$, Hy = pupil grid size; uses L01 Task 4's filter-finding code):

```zpl
! ZPL17.ZPL — max AOI (deg) on surface commented "FILTER"; slot 0 = AOI, slot 1 = shift (nm)
hy = PVHX()
n  = PVHY()
IF (n < 3) THEN n = 7
lam0 = 0.850
neff = 1.8
target$ = "FILTER"
GOSUB FINDSURF                         # sets sf (filter front surface), as in L01
IF (sf == 0)
    OPTRETURN 0, 90                    # not found → large finite penalty
    OPTRETURN 1, 0
    END
ENDIF
amax = 0
FOR i, 0, n-1, 1
    FOR j, 0, n-1, 1
        px = -1 + 2*i/(n-1)
        py = -1 + 2*j/(n-1)
        IF (px*px + py*py <= 1)
            RAYTRACE 0, hy, px, py, PWAV()
            IF ((RAYE() == 0) & (RAYV() == 0))
                a = ACOS(ABSO(RAYN(sf-1))) * 180 / 3.14159265358979
                IF (a > amax) THEN amax = a
            ENDIF
        ENDIF
    NEXT
NEXT
s = SINE(amax*3.14159265358979/180) / neff
OPTRETURN 0, amax
OPTRETURN 1, 1000*lam0*(1 - SQRT(1 - s*s))
```

(Logical-and operator and `==`/`!=` spelling: check *About the ZPL → operators* for your version. `ACOS` returns radians.)

**(c) Cost.** With $n = 7$, 29 of the 49 grid points lie inside the unit circle → 29 rays per call. A typical interpreted `RAYTRACE` costs on the order of tens of µs, so the call is ~1–3 ms — negligible even with 3 rows (fields 0.5, 0.75, 1.0) and 25 variables: $26 \times 3 \times 3\ \text{ms} \approx 0.23$ s per DLS iteration. At $n = 41$ (1257 grid points with $p_x^2+p_y^2 \le 1$) the cost is ~43× higher and worth moving to a UDOC.

```text
n = 7  →   29 points inside the pupil
n = 15 →  149
n = 41 → 1257
```

## Key takeaways
- Try built-in and math operands first; write code only for loops, branches or genuinely new quantities.
- `ZPLM`: file `ZPLnn.ZPL`, inputs via `PVHX/PVHY/PVPX/PVPY`, outputs via `OPTRETURN slot, value`, macro runs only on Data = 0 rows.
- ZPL macro solves return with `SOLVERETURN`, must not `UPDATE` or touch other cells, and return curvature for radius cells.
- UDOC = compiled C#/C++ user operand (`UDOCnn.exe` in `ZOS-API\Operands`, Windows-app Release build); User Analysis = compiled custom analysis window; User Extension = compiled GUI tool.
- Custom operands run on a copy of the system and are called $(N_\text{var}+1)$+ times per DLS iteration: keep them cheap, smooth, finite and scaled.
- DDE/UDOP are dead; port to the ZOS-API.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| ZPLM | Merit-function operand that runs macro `ZPLnn.ZPL` and reports one of its `OPTRETURN` values |
| `OPTRETURN` | ZPL keyword storing a result in the operand's return slot (0–50) |
| `PVHX()`…`PVPY()` | ZPL functions returning the Hx, Hy, Px, Py arguments of the calling ZPLM row |
| ZPL macro solve | Solve type that sets an editor cell from a macro via `SOLVERETURN` |
| UDOC | Merit-function operand calling a compiled ZOS-API user operand `UDOCnn.exe` |
| User Analysis | Compiled ZOS-API program that fills a custom OpticStudio analysis window |
| User Extension | Compiled ZOS-API program launched from the Programming tab |
| UDOP / DDE | Obsolete user-operand / inter-process mechanisms, no longer supported |

## References
1. Ansys KB, D. Hill, "optimizing with a user-defined ZPL macro" (ZPLM, working F/#, timing): <https://optics.ansys.com/hc/en-us/articles/42661785079315>
2. Ansys KB, A. Croce, ZPLM centre-of-mass example (PVHX…, OPTRETURN, Data semantics): <https://optics.ansys.com/hc/en-us/articles/43071134436883>
3. Ansys KB, N.-H. Kim, upd. A. Croce, ZPL macro solves: <https://optics.ansys.com/hc/en-us/articles/43071107400467>
4. Ansys KB, H. Hu, creating a User Operand with the ZOS-API: <https://optics.ansys.com/hc/en-us/articles/42661799284499>
5. Ansys KB, T. Jacobs, ZOS-API sample files and connection modes: <https://optics.ansys.com/hc/en-us/articles/42661773562899>
6. Ansys KB, T. Pickering, creating a User Analysis with the ZOS-API: <https://optics.ansys.com/hc/en-us/articles/42661869482131>
7. Zemax Community, UDOP/DDE support: <https://community.zemax.com/licensing-and-installation-8/are-udops-supported-in-opticstudio-any-more-4088>
8. ZOS-API Syntax Help (installed with OpticStudio; online copies of recent versions are hosted on the Ansys/Synopsys developer portal, e.g. the Analysis namespace page <https://developer.ansys.com/docs/zos-api-interface-2025-r2/namespace_z_o_s_a_p_i_1_1_analysis.xhtml>).
