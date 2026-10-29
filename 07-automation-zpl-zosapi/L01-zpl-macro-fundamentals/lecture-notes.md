# L01 — ZPL macro fundamentals

> **Course 07 · Automation with ZPL and the ZOS-API** · Estimated time: lecture ~2.5 h, tasks ~4.5 h
> **Prerequisites:** [Course 01 L06 (real rays)](../../01-foundations/L06-real-rays-and-analysis-tools/), [Course 01 L07 (solves, MF)](../../01-foundations/L07-solves-variables-first-optimization/), [Course 03 L04 (merit functions)](../../03-image-quality-optimization/L04-merit-function-mastery/) · **Next:** [L02 — User-defined operands and analyses](../L02-user-defined-operands-and-analyses/)

## Learning objectives
- Explain where ZPL fits next to the ZOS-API (what it is good for, what it cannot do) and decide which to use for a given task.
- Write, save and run a ZPL macro from the Programming tab, using variables, string variables, arrays, `FOR` loops, `IF` blocks, subroutines and formatted `PRINT`.
- Trace single real rays with `RAYTRACE`, read coordinates and direction cosines with `RAYX/RAYY/RAYZ/RAYL/RAYM/RAYN`, and *always* check the error/vignetting state with `RAYE()`/`RAYV()`.
- Read lens data with functions (`NSUR()`, `THIC()`, `CURV()`, `$GLASS()`, `$COMMENT()`…) and change it with `SURP`/`SETSURFACEPROPERTY` followed by `UPDATE`.
- Send output to the screen or a file with `OUTPUT`/`PRINT`/`FORMAT`, and pull analysis text into a macro with `GETTEXTFILE` (and know why `GETT()` is fragile).
- Write macros that are robust: no hard-coded surface/wavelength numbers, state restored at the end, debug switch.

## Reading
- **Core (online):** Ansys Optics KB, D. Hill (updated A. Croce), "Zemax Programming Language (ZPL)" overview — <https://optics.ansys.com/hc/en-us/articles/42661729425299>. Syntax of variables, arrays, `IF`, `FOR`, `RAYTRACE`, `CALLMACRO`, `GOSUB`.
- **Core (online):** Ansys Optics KB, M. Nicholson, tips for writing and debugging ZPL macros — <https://optics.ansys.com/hc/en-us/articles/43071052488851>. Debug switch, restore state, `UPDATE`, `RAYE()`, avoid hard-coded values.
- **Core (in the software):** Help → *The Programming Tab → About the ZPL* — the keyword list and the numeric/string function lists. This is the authoritative dictionary; every keyword in this lesson should be looked up there once.
- **Optional (forum, staff answers):** OUTPUT and GETTEXTFILE syntax — <https://community.zemax.com/zpl-13/can-i-create-a-new-text-file-for-output-inside-of-zpl-macro-164>; why `GETT()` does not work inside operand macros — <https://community.zemax.com/got-a-question-7/zplm-macro-gett-is-not-effective-to-extract-values-is-there-a-workaround-854>.
- **Books:** the three course books predate ZPL-as-we-know-it or don't cover it; Geary's appendix mentions macros only in passing. This course leans on the Ansys documentation.

---

## 1. Why learn ZPL if you are going to use Python?

OpticStudio has two programming interfaces:

| | **ZPL** (Zemax Programming Language) | **ZOS-API** (.NET API; Python via pythonnet / ZOSPy, C#, MATLAB) |
|---|---|---|
| Runs | Inside OpticStudio, interpreted | In your own process (standalone) or as a plug-in (extension, user operand, user analysis) |
| Language | BASIC-like, case-insensitive | Any .NET-capable language |
| Strengths | Zero setup; ships with every edition; quick one-off calculations; callable from the merit function (`ZPLM`) and from solves; shareable as a single text file | Full programming language, libraries (numpy, pandas, scipy, matplotlib), version control, tests, speed (batch ray trace), access to almost every editor and analysis |
| Weaknesses | Slow interpreter; limited data structures; no libraries; awkward string handling; text-window scraping for analysis data | Setup, version-sensitive API, licence/instance handling |

Ansys's own summary: ZPL is interpreted and therefore slower than compiled code for heavy computation, it cannot define user surfaces or objects (that's what DLLs are for), and for speed or integration with other tools the recommended route is the ZOS-API [1].

So why spend a lesson on it?

1. **You will read other people's ZPL.** Two decades of sample macros, KB articles, vendor files and colleagues' tools are in ZPL. Many KB solutions still end with "here is a macro".
2. **`ZPLM` operands and ZPL solves** are the lowest-friction way to put a custom computation *inside* the merit function (L02). The ZOS-API equivalent (a compiled User Operand) is more powerful but needs a build toolchain.
3. **Quick experiments.** "Trace this ray at 20 field points and print the angle at the filter" is five lines of ZPL and no environment to set up.
4. **The mental model transfers.** ZPL keywords map almost one-to-one onto ZOS-API calls (`RAYTRACE` ↔ single ray trace / batch ray trace, `OPTIMIZE` ↔ `LocalOptimization`, `GETTEXTFILE` ↔ `GetTextFile`, `SURP` ↔ `LDE.GetSurfaceAt(n).Thickness = …`). Learning ZPL first makes the API documentation easier to read.

**Rule of thumb used in this course:** if it is a one-off or must live in the merit function and is cheap → ZPL. If it touches more than a few hundred rays, needs plots/statistics, runs unattended, or must be reproducible under git → Python + ZOS-API (L03 onward).

## 2. Where macros live and how to run them

- **Macro folder.** By default `Documents\Zemax\Macros`. The data folder root (and hence the macro folder) is set in *Setup → Project Preferences → Folders* (location varies by version — search "Folders" in Project Preferences). `OUTPUT` with a bare file name writes into this macro folder [3].
- **File type.** Plain text, extension `.ZPL`. Any editor works; OpticStudio has a built-in editor (Programming tab → *Edit/Run* or similar; location varies by version — search the ribbon for "Macro"). VS Code with a generic BASIC/plain-text mode is fine; keep macros under git like any code.
- **Running.** Programming tab → the macro list (*Macro List* / *Edit/Run ZPL Macros*) shows every `.ZPL` in the macro folder. Output appears in a text window, which you can save. A macro that is running can be terminated from that window.
- **Numbered macros.** Files named `ZPL00.ZPL` … `ZPL99.ZPL` are special: they are the ones the `ZPLM` merit-function operand can call (L02) [5].
- **Case.** ZPL is case-insensitive. Convention (from Ansys's own tips): keywords and functions in UPPERCASE, variables in lowercase [2].
- **Comments.** A line starting with `!` is a comment; text after `#` on a line is ignored [1].

A first macro (save as `hello_lens.ZPL`):

```zpl
! hello_lens.ZPL — print a summary of the current lens
n = NSUR()                       # number of surfaces (image surface index)
PRINT "Lens: ", $LENSNAME()
PRINT "Surfaces: ", n, "   Wavelengths: ", NWAV(), "   Primary: ", PWAV()
FORMAT 10.4
FOR s, 1, n, 1
    PRINT s, "  R = ", RADI(s), "  t = ", THIC(s), "  ", $GLASS(s), "  ", $COMMENT(s)
NEXT
```

`$LENSNAME()`, `$GLASS()` and `$COMMENT()` are string functions (string functions and string variables carry a `$`). If any function name here doesn't exist in your version, the editor will flag it — look it up in *About the ZPL → String Functions* (verify against your installed version's Help; the surface functions `RADI`, `THIC`, `NSUR` are long-standing).

## 3. The language in one page

### 3.1 Variables and arithmetic
- Numeric variables need no declaration and are 64-bit doubles: `z = x + y` [1].
- String variables end in `$`: `name$ = "FOCUS COMP"`. Concatenate with `+`; convert numbers with `$STR(x)`.
- Names ≤ 28 characters, no spaces/operators, cannot equal a keyword or function name [1]. A frequent first error: naming a variable `thic` or `rayx`.
- Math functions use four-letter-ish names: `SQRT()`, `ABSO()`, `SINE()`, `COSI()`, `TANG()`, `ASIN()`, `ACOS()`, `ATAN()`, `EXPE()`, `LOGE()`, `LOGT()`, `INTE()` (check the numeric function list for the exact set; trig functions work in radians).

### 3.2 Arrays
- `VEC1`…`VEC4` are predefined global vectors; size them with `SETVECSIZE` [1].
- User arrays: `DECLARE spot, DOUBLE, 2, 20, 3` (name, type, number of dimensions, sizes); index with `spot(i, j)`; free with `RELEASE spot` [1]. Indices start at 1.
- Known quirk: some keywords don't accept an array element as an argument directly; assign it to a scalar first (a community example: `c = L1(1,1)` then `SURP 12, 2, c`) [6].

### 3.3 Control flow

```zpl
FOR i, 1, 10, 1          # also accepted: FOR i = 1, 10, 1
    IF (i > 5) THEN PRINT "i is greater than 5"
NEXT

IF (err != 0)
    PRINT "ray failed at surface ", RAYV()
ELSE
    PRINT "ok"
ENDIF
```

Single-line `IF (…) THEN …` and block `IF … ELSE … ENDIF` exist [1]. Use `GOSUB name` with `SUB name … RETURN` for subroutines inside one macro, `CALLMACRO` to run another macro file (data passed through buffers) [1]. `END` stops the macro. Older macros use `LABEL`/`GOTO` loops; avoid them in new code.

> **Edge cases are yours.** The Ansys article warns that ZPL will not handle equality/edge cases for you (`IF (A > 5)` vs `A = 5`) [1]. Floating-point comparisons of real-ray data should always use a tolerance: `IF (ABSO(a - b) < 1e-9)`.

### 3.4 Output
- `PRINT` with comma-separated items: `PRINT "The chief ray height is ", RAYY(NSUR())` [1].
- `FORMAT` sets the numeric format for subsequent prints (e.g. `FORMAT 12.6` → width 12, 6 decimals; there is also an exponential option — see Help).
- `OUTPUT filename` redirects subsequent `PRINT` output to a file (bare name → macro folder); `OUTPUT SCREEN` switches back [3]. Use full paths or `$DATAPATH()`-style string functions if you want output next to the lens (verify the exact function name in your Help).
- Write **machine-readable** output when Python will consume it: one header line, comma- or tab-separated columns, no decorative text. You will parse these files with `pandas.read_csv` in later lessons.

## 4. Reading and changing the lens

### 4.1 Reading: functions
Functions return values and can appear only on the right-hand side of an assignment; keywords *do* things [1].

| Function | Returns |
|---|---|
| `NSUR()` | number of surfaces = index of the image surface (object is surface 0) |
| `NWAV()`, `PWAV()`, `WAVL(n)` | number of wavelengths, primary wavelength number, wavelength n in µm |
| `NFLD()`, `FLDX(n)`, `FLDY(n)` | number of fields, field n coordinates (in the system's field units) |
| `CONF()`, `NCON()` | current configuration, number of configurations |
| `RADI(s)`, `CURV(s)`, `THIC(s)`, `CONI(s)`, `SDIA(s)` | radius, curvature, thickness, conic, semi-diameter of surface s |
| `$GLASS(s)`, `$COMMENT(s)` | material name, comment string |
| `SPRO(s, code)` | general surface property by numeric code |
| `OPEV(code, …)` | evaluates any merit-function operand on the fly; get the code with `OCOD("EFFL")` [1] |

`OPEV` is the bridge to the whole operand library: anything you can put in the Merit Function Editor you can evaluate from a macro. Its argument list mirrors the MFE columns (Int1, Int2, Data1…); check the exact signature in Help (verify against your installed version). Example intent: `efl = OPEV(OCOD("EFFL"), 0, PWAV(), 0, 0, 0, 0, 0, 0)`.

Finding surfaces **by comment** rather than by number is the single most valuable robustness habit, and the reason the Course 04 capstone insists on comments like "STOP" and "FOCUS COMP":

```zpl
SUB FINDSURF                       # in: target$ ; out: found (0 = not found)
    found = 0
    FOR s, 0, NSUR(), 1
        IF ($COMMENT(s) $== target$) THEN found = s   # string compare: check operator in Help
    NEXT
RETURN
```

String comparison syntax differs from numeric comparison in ZPL; look up "string comparison" in *About the ZPL* before relying on this (the Ansys forum also points to the numeric helpers `SURC()`/`SRCN()`/`SPRO()` for locating surfaces by comment) [7].

### 4.2 Changing: SURP / SETSURFACEPROPERTY and UPDATE
`SETSURFACEPROPERTY surf, code, value` (short form `SURP`) changes a surface property; `code` selects the column (curvature, thickness, glass, semi-diameter, conic, parameters, …) — the numeric code table is in Help under `SETSURFACEPROPERTY` and is version-dependent, so look it up instead of memorising it. Other keywords handle variables (`SETVAR`), solves (`SOLVETYPE`), system data, configurations (`SETCONFIG`), multi-configuration operands (`SETMCOPERAND`) and merit-function rows (`SETOPERAND`) — again, check exact syntax in Help.

**Changes are not applied until `UPDATE`.** OpticStudio recomputes paraxial data, solves and pickups only when the macro executes `UPDATE` (or `UPDATE ALL` to also refresh open windows) [2]. A classic bug: change a thickness, trace a ray, get the *old* answer. Pattern:

```zpl
SURP fsurf, 3, t_new      # 3 = thickness in many versions — VERIFY the code in Help
UPDATE
RAYTRACE 0, 1, 0, 0, PWAV()
```

### 4.3 Restore what you change
A macro that leaves the lens in a different configuration, with a different primary wavelength or with a modified thickness is a time-bomb. Save state on entry, restore on exit [2]:

```zpl
orig_config = CONF()
...           # work in other configurations
SETCONFIG orig_config
```

For geometry changes, either undo them explicitly or work on a copy (`SAVELENS`/`LOADLENS`).

## 5. Real ray tracing from a macro

### 5.1 RAYTRACE and its results
`RAYTRACE hx, hy, px, py, wave` traces one real ray with normalized field $(H_x,H_y)$ and normalized pupil $(P_x,P_y)$ coordinates at wavelength number `wave`, from the object to the image surface, in the current configuration [1]. Normalization is the same as in the merit function (Course 01 L04): $H_y = 1$ is the maximum field, $P_y = 1$ the edge of the entrance pupil; with ray aiming on, pupil coordinates refer to the (aimed) stop.

After the trace, results for every surface $s$ are available until the next trace:

| Function | Meaning | Units / frame |
|---|---|---|
| `RAYX(s)`, `RAYY(s)`, `RAYZ(s)` | intersection coordinates | lens units, **local** coordinates of surface $s$ |
| `RAYL(s)`, `RAYM(s)`, `RAYN(s)` | direction cosines after refraction at $s$ | dimensionless, local frame |
| `RAYE()` | error code of the last trace (0 = OK) | — |
| `RAYV()` | surface where the ray was vignetted (0 = not vignetted) | — |

Global coordinates differ from local ones after coordinate breaks/tilts; use the global-coordinate functions (e.g. `GLCX/GLCY/GLCZ` for surface vertex positions) or `RAYTRACEX`/global variants when the system is not rotationally symmetric. `RAYTRACEX` starts a ray from an arbitrary surface with explicit coordinates [1].

### 5.2 Always check RAYE() and RAYV()
If a ray misses a surface, undergoes TIR, or is clipped by an aperture, the RAY* functions return garbage or stale numbers without stopping the macro. Ansys's first debugging rule: after every `RAYTRACE`, check `RAYE()` [2]. In this course: check both.

```zpl
RAYTRACE hx, hy, px, py, w
IF (RAYE() != 0) THEN GOSUB RAYFAIL
IF (RAYV() != 0) THEN GOSUB RAYCLIPPED
```

(Inequality is `!=` in ZPL; verify in Help — older macros sometimes use `<>`.)

### 5.3 What you can compute from one ray
- **Image height / distortion:** real chief ray `RAYTRACE 0, hy, 0, 0, w` → `RAYY(NSUR())`. Compare with the paraxial height (from `PARAXIAL`-type functions or an operand via `OPEV`) to get distortion.
- **Angles:** the angle to the surface normal or the axis: with local direction cosines $(L, M, N)$, the angle to the local $z$-axis is $\theta = \arccos N$; in the meridional plane $\tan\theta_y = M/N$. Chief-ray angle at the sensor: $\theta = \arccos(\text{RAYN}(n_{img}))$ — but in the *medium after* that surface.
- **Working F/#:** from a real marginal ray's direction cosine in image space, $F/\#_w = 1/(2 n' \sin\theta')$, with $\sin\theta' = \sqrt{L^2 + M^2}$ for a ray in the $y$–$z$ plane $= |M|$.
- **Transverse aberration:** $\varepsilon_y = y(P_y) - y_{chief}$ on the image surface — a ray fan, one line at a time.
- **Footprints:** min/max of RAYY at a surface over a pupil grid → beam size at the filter, clear apertures.
- **Angle of incidence on a filter**: for a plane surface normal to $z$, AOI $= \arccos N$ of the ray *before* the surface, i.e. use `RAYN(s-1)` (direction after surface $s-1$ is the direction arriving at $s$). This is how you check spec S7 of the Course 04 capstone (filter AOI ≤ 24°).

### 5.4 Sampling the pupil
A macro that loops over a square grid of $(P_x,P_y)$, skips points with $P_x^2 + P_y^2 > 1$, traces each ray, accumulates sums of $x, y, x^2, y^2$ and counts valid rays gives you an RMS spot radius about the centroid:

$$
r_\text{RMS} = \sqrt{\overline{x^2} - \bar x^2 + \overline{y^2} - \bar y^2},
$$

where the bars are averages over the $N$ valid rays and $(x, y)$ are image-plane intersection coordinates. With a uniform grid this approximates the Spot Diagram's "RMS radius (centroid reference)"; the Merit Function's Gaussian quadrature uses weighted rings and arms instead, which is why numbers differ slightly (Course 03 L04).

## 6. Getting analysis data into a macro

Not everything is a single ray. Three routes, from best to worst:

1. **Operands via `OPEV()`**: MTF (`MTFT`, `MTFS`), RMS spot (`RSCE`), wavefront (`RWCE`), distortion (`DIST`) etc. Fast, no windows, works inside `ZPLM`.
2. **`GETTEXTFILE textfile$, type$, settingsfile$, flag`**: runs an analysis by its three-letter code (e.g. `Spt` spot diagram, `Ima` image analysis, `Tfm` FFT through-focus MTF) and writes its text output to a file, which you then read back with `OPEN`/`READ`-style keywords (or simply parse later in Python) [3][4]. Settings come from a `.CFG` settings file you save from the analysis window; `MODIFYSETTINGS` changes individual settings.
3. **`GETT(window, line, column)`**: extracts a number from an *open* text window. It depends on what is on screen and does **not** work inside operand macros, because those run on a temporary copy of the lens [7]. Avoid it in anything you intend to reuse.

The analysis three-letter codes and settings-file mechanics are exactly what the ZOS-API exposes more cleanly (`Analyses.New_Analysis(...)`, `GetSettings()`, `GetResults()`) — L05 replaces this whole section with Python.

## 7. Writing macros like software

Apply the habits you'd apply to C:

- **Debug switch:** `debug = 1` at the top; `IF (debug) THEN PRINT …` [2].
- **No magic numbers:** use `NSUR()`, `NWAV()`, `PWAV()`, `NFLD()`; find surfaces by comment [2].
- **Validate inputs:** if the macro uses `INPUT`, clamp: `IF (w > NWAV()) THEN w = NWAV()` [2].
- **Restore state** at the end (configuration, primary wavelength, any geometry you changed) [2].
- **Header block** with purpose, inputs, outputs, units, OpticStudio version tested, author, date.
- **Version control:** keep `Macros/` (or a project-specific macro folder) in git; ZPL is text and diffs cleanly.
- **Performance:** each `RAYTRACE` costs an interpreter round-trip; tens of thousands of rays are fine, millions are not — that's what batch ray tracing in the API is for (L06).

## 8. In OpticStudio — checklist and pitfalls

- **Primary wavelength and configuration** are whatever the lens is currently set to; state them explicitly in the macro.
- **Ray aiming:** if the lens uses ray aiming, `RAYTRACE` honours it (the pupil coordinates are aimed). If you see a mismatch between macro results and a Ray Fan, check ray-aiming and the field type first.
- **Field units:** `hx, hy` are normalized to the maximum *radial* field (and the field normalization option — radial vs rectangular — in System Explorer → Fields matters).
- **Image surface index:** `NSUR()` is the image surface; the last physical surface is `NSUR() - 1`.
- **Local vs global coordinates:** for tilted filters, Scheimpflug sensors (Course 04 L09) or fold mirrors, RAYX/Y/Z are local.
- **Units:** lens units (usually mm); wavelengths in µm.
- **Non-sequential:** NSC uses a different keyword set (`NSTR`, `NSDD`, object-property functions); this lesson is sequential only.

## Worked example — working F/# and distortion from a macro

Lens: the Course 01 singlet, $f' = 100$ mm, EPD = 20 mm (F/5), object at infinity, field 5°.

**(a) Working F/# by hand (paraxial limit).** The paraxial marginal ray leaves the lens with slope $u' = -h/f' = -10/100 = -0.1$. Its direction cosine in image space is $M = \sin\theta' = 0.1/\sqrt{1 + 0.1^2} = 0.09950$, so

$$
F/\#_w = \frac{1}{2 n' \sin\theta'} = \frac{1}{2 \cdot 1 \cdot 0.09950} = 5.025 .
$$

The macro does the same with the real ray:

```zpl
RAYTRACE 0, 0, 0, 1, PWAV()
IF (RAYE() != 0) THEN PRINT "marginal ray failed" 
m = RAYM(NSUR())
wfno = 1 / (2 * ABSO(m))          # image space is air, n' = 1
PRINT "Working F/# = ", wfno
```

On the real singlet expect a value close to 5.0 (spherical aberration changes the real marginal ray's angle slightly). Compare with the `WFNO` operand: Ansys's own `ZPLM` example does exactly this check and finds agreement [5].

**(b) Distortion.** Paraxial image height at 5°: $y_p = f'\tan 5° = 100 \times 0.087489 = 8.7489$ mm. Suppose the real chief ray (`RAYTRACE 0, 1, 0, 0, PWAV()`, then `RAYY(NSUR())` on the paraxial-focus image plane) lands at $y_r = 8.732$ mm. Then

$$
D = \frac{y_r - y_p}{y_p}\times 100\% = \frac{8.732 - 8.7489}{8.7489}\times100\% = -0.193\% \;\text{(barrel)}.
$$

**(c) RMS spot from four rays.** Valid rays land at $(x, y)$ = (4, 0), (−4, 0), (0, 3), (0, −3) µm. Centroid (0, 0); $\overline{x^2} = (16+16)/4 = 8$, $\overline{y^2} = (9+9)/4 = 4.5$ µm²; $r_\text{RMS} = \sqrt{12.5} = 3.54$ µm. Your macro in Task 3 must reproduce exactly this if you feed it these points.

## Key takeaways
- ZPL is a small, interpreted, BASIC-like language inside OpticStudio: ideal for quick calculations and merit-function hooks, not for heavy or reproducible pipelines (use the ZOS-API for those).
- Keywords *act* (`RAYTRACE`, `SURP`, `UPDATE`, `OPTIMIZE`, `OUTPUT`); functions *return* (`RAYY()`, `THIC()`, `NSUR()`, `OPEV()`).
- After every `RAYTRACE`, check `RAYE()` (and `RAYV()`); RAY* coordinates are in the local frame of each surface.
- Lens changes take effect only after `UPDATE`; restore anything you change.
- `OPEV()` gives a macro the entire operand library; `GETTEXTFILE` gives it any analysis's text output; `GETT()` is fragile.
- Find surfaces by comment and never hard-code surface or wavelength numbers — your later Python scripts will use the same convention.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| ZPL | Zemax Programming Language: OpticStudio's built-in interpreted macro language |
| Keyword | ZPL statement that performs an action (`RAYTRACE`, `UPDATE`, `PRINT`) |
| Function | ZPL expression returning a value (`RAYY()`, `THIC()`); right-hand side only |
| Direction cosines (L, M, N) | Components of the unit ray direction vector along local x, y, z |
| `RAYE()` / `RAYV()` | Error code / vignetting surface of the last traced ray |
| `UPDATE` | Keyword that recomputes the lens (solves, pickups, paraxial data) after changes |
| `OPEV()` | Function that evaluates an arbitrary merit-function operand |
| `GETTEXTFILE` | Keyword that runs an analysis and saves its text output to a file |
| Macro folder | Directory OpticStudio scans for `.ZPL` files (Documents\Zemax\Macros by default) |

## References
1. Ansys Optics KB, D. Hill, upd. A. Croce, "Zemax Programming Language (ZPL)": <https://optics.ansys.com/hc/en-us/articles/42661729425299>
2. Ansys Optics KB, M. Nicholson, tips for writing and debugging ZPL macros: <https://optics.ansys.com/hc/en-us/articles/43071052488851>
3. Zemax Community (staff answer), OUTPUT and GETTEXTFILE syntax: <https://community.zemax.com/zpl-13/can-i-create-a-new-text-file-for-output-inside-of-zpl-macro-164>
4. Zemax Community, through-focus MTF data with ZPL (GETTEXTFILE type codes): <https://community.zemax.com/zpl-13/through-focus-mtf-data-with-zpl-484>
5. Ansys Optics KB, D. Hill, optimizing with a user-defined ZPL macro (ZPLM, working F/# example): <https://optics.ansys.com/hc/en-us/articles/42661785079315>
6. Zemax Community, SETSURFACEPROPERTY with a variable/array: <https://community.zemax.com/zpl-13/how-to-setsurfaceproperty-using-a-variable-4769>
7. Zemax Community (staff answers), finding a surface by comment (SURC/SRCN/SPRO) <https://community.zemax.com/got-a-question-7/how-to-find-the-surface-with-specific-comment-in-zpl-macro-3300> and GETT in ZPLM macros <https://community.zemax.com/got-a-question-7/zplm-macro-gett-is-not-effective-to-extract-values-is-there-a-workaround-854>
8. OpticStudio Help → The Programming Tab → About the ZPL (keyword, numeric-function and string-function lists) — installed with the software; authoritative for your version.
