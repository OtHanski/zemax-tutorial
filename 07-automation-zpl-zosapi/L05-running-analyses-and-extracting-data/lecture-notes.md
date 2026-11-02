# L05 — Running analyses and extracting data

> **Course 07 · Automation with ZPL and the ZOS-API** · Estimated time: lecture ~2.5 h, tasks ~5 h
> **Prerequisites:** [L04 — Building and editing systems from Python](../L04-building-and-editing-systems-from-python/); [Course 03 L01–L03 (PSF, MTF, Strehl)](../../03-image-quality-optimization/) · **Next:** [L06 — Batch ray tracing and custom metrics](../L06-batch-ray-tracing-and-custom-metrics/)

## Learning objectives
- Run any OpticStudio analysis from Python with the generic pattern `New_Analysis` → `GetSettings` → `ApplyAndWaitForCompletion` → `GetResults` → `Close`, and know the four result containers (data series, data grids, analysis-specific data such as `SpotData`, text file).
- Use ZOSPy's analysis wrappers (FFT MTF, through-focus MTF, Huygens MTF, wavefront map, Zernike coefficients, ray fan, single ray trace, cardinal points…) and get results as pandas DataFrames.
- Convert .NET arrays to numpy efficiently and attach the metadata (field, wavelength, configuration, sampling, units) that makes data reusable.
- Choose between analysis windows and merit-function operands (`MTFT/MTFS`, `RSCE`, `RWCE`, `DIST`, `RAID`…) for extracting numbers, and know when their results differ.
- Produce publication-quality plots (MTF vs frequency/field, spot RMS vs field, wavefront maps) with matplotlib from a script, including a perfect-lens reference curve.
- Diagnose the classic data-extraction errors: wrong field/wavelength indexing (0 = all vs 1-based), stale settings, transposed grids, sampling too coarse.

## Reading
- **Core:** ZOS-API Python examples 04 *Retrieve Data from FFT MTF* and 22 *Sequential Analysis*: <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex04_py.xhtml>, <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex22_py.xhtml> (examples index: <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_exov.xhtml>).
- **Core:** ZOSPy, "Performing analyses": <https://zospy.readthedocs.io/en/latest/user_guide/usage/analyses.html>; API list of wrappers: <https://zospy.readthedocs.io/en/latest/api.html>; FFT MTF wrapper: <https://zospy.readthedocs.io/en/latest/api/zospy.analyses.mtf.fft_mtf.FFTMTF.html>
- **Refresh:** [Course 03 L02 — MTF theory](../../03-image-quality-optimization/L02-mtf-theory-and-practice/lecture-notes.md) and [L03 — Strehl & wavefront](../../03-image-quality-optimization/L03-strehl-wavefront-error-depth-of-focus/lecture-notes.md); [Course 03 L04](../../03-image-quality-optimization/L04-merit-function-mastery/lecture-notes.md) on RSCE vs spot diagram.
- **Background:** [Kenyon §7.2, pp. 167–169] (PSF, OTF = MTF·e^{iPTF}) — for the perfect-lens reference curve in the worked example.
- **Reference:** ZOS-API Syntax Help → `ZOSAPI.Analysis` namespace (`I_Analyses`, `IA_`, `IAR_` results, `AnalysisIDM`), online e.g. <https://developer.ansys.com/docs/zos-api-interface-2025-r2/namespace_z_o_s_a_p_i_1_1_analysis.xhtml>.

---

## 1. The generic analysis pattern

Every analysis window in the GUI has an API twin:

```python
A = oss.Analyses                                       # I_Analyses
win = A.New_Analysis(C.Analysis.AnalysisIDM.StandardSpot)   # [ex. 22]; or typed creators like A.New_FftMtf() [ex. 04]
try:
    s = win.GetSettings()                              # analysis-specific settings interface
    s.Field.SetFieldNumber(0)                          # 0 = all fields   [ex. 22]
    s.Wavelength.SetWavelengthNumber(0)                # 0 = all wavelengths [ex. 22]
    s.ReferTo = C.Analysis.Settings.RMS.ReferTo.Centroid   # [ex. 22]
    win.ApplyAndWaitForCompletion()                    # compute (blocking)
    r = win.GetResults()                               # IAR_ results
    rms_um = r.SpotData.GetRMSSpotSizeFor(1, 1)        # field 1, wave 1  [ex. 22]
finally:
    win.Close()
```

Rules that cause most bugs:
- **Indexing:** settings use **0 = "all"** for field/wavelength selectors; result accessors use **1-based** field/wavelength numbers [ex. 22]. Configuration is whatever `MCE.SetCurrentConfiguration` set.
- **Settings interfaces are analysis-specific.** `GetSettings()` returns an interface with that analysis's properties (`MaximumFrequency`, `SampleSize` for FFT MTF [ex. 04]; `ReferTo`, `RayDensity` for spots [ex. 11, 22]). If a property seems missing, it may need the specific interface (pythonnet casting, L03 §3.3) or may be reachable only through a settings file (§1.2).
- **Close what you open.** Each `New_Analysis` is an analysis window inside the (possibly hidden) instance; hundreds of unclosed windows slow everything down.

### 1.1 Result containers
| Container | Typical analyses | Access |
|---|---|---|
| **Data series** (curves) | FFT/Huygens MTF vs frequency, through-focus MTF, ray fans, field curvature/distortion | `r.NumberOfDataSeries`, `r.GetDataSeries(i)`, `.XData.Data`, `.YData.Data` (2D: x × series) [ex. 04] |
| **Data grids** (2D maps) | wavefront map, PSF, footprint, image simulation | `r.NumberOfDataGrids`, `r.GetDataGrid(i)` → values + min/spacing (names: verify) |
| **Analysis-specific data** | spot diagram (`SpotData`), some reports | `r.SpotData.GetRMSSpotSizeFor(f, w)`, `GetGeoSpotSizeFor(f, w)` [ex. 22] |
| **Text output** | anything (always available) | `r.GetTextFile(path)` then parse — the API equivalent of ZPL `GETTEXTFILE` (method name: verify) |

When a structured container is missing or incomplete for an analysis, fall back to the text file. It's ugly but complete, and it's what you'd see in the GUI's Text tab.

### 1.2 Settings that are not exposed: `ModifySettings`
Some analyses expose only part of their settings as properties. The fallback is the analysis settings file (`.CFG`) plus keyword edits — the same keywords as ZPL's `MODIFYSETTINGS` [ex. 11, 15]:

```python
s = win.GetSettings()
cfg = r"C:\temp\uni.cfg"
s.SaveTo(cfg)                                   # [ex. 15]
s.ModifySettings(cfg, "UN1_OPERAND", "RSRE")    # keyword from the ZPL MODIFYSETTINGS list [ex. 11]
s.LoadFrom(cfg)                                 # [ex. 11, 15]
win.ApplyAndWaitForCompletion()
```

The keyword list (e.g. `SHA_ROTX`, `UN1_OPERAND`) is in the ZPL `MODIFYSETTINGS` help page.

### 1.3 .NET arrays to numpy
`YData.Data` is a `System.Double[,]`. The official example converts with nested Python loops (`reshape`/`transpose` helpers) [ex. 04] — fine for 100 points, slow for 10⁶. Faster:

```python
import numpy as np
def net2d_to_numpy(a) -> np.ndarray:
    rows, cols = a.GetLength(0), a.GetLength(1)
    flat = np.fromiter(a, dtype=float, count=rows * cols)   # iterates in row-major order — verify on a small known array!
    return flat.reshape(rows, cols)
```

For very large arrays, copying the raw memory via `System.Runtime.InteropServices.Marshal.Copy` into a pinned numpy buffer is faster still (ZOSPy does similar conversions internally). **Always test** any conversion on a small array whose values you know — transposition errors are silent.

### 1.4 Data grids: coordinates are part of the data
A data grid (wavefront map, PSF, footprint…) is a 2D array plus a coordinate description. The members used in practice are `Values` (the `Double[,]`), `Nx`, `Ny`, `Dx`, `Dy`, `MinX`, `MinY` [7]. Build the axes yourself:

```python
g = r.GetDataGrid(0)                       # index base: verify (0 in recent versions)
Z = net2d_to_numpy(g.Values)               # shape (Ny, Nx)? or (Nx, Ny)? -> check against the GUI once!
x = g.MinX + g.Dx * np.arange(g.Nx)        # MinX = pixel EDGE or pixel CENTRE?  see below
y = g.MinY + g.Dy * np.arange(g.Ny)
```

Two traps, both discussed on the Ansys/Zemax community forum [7]: (1) whether `MinX/MinY` denote the **edge** or the **centre** of the first cell differs between analyses, and for at least one analysis (Geometric Image Analysis) `MinY` was reported with the wrong sign; (2) the row order (does row 0 correspond to $y_\text{min}$ or $y_\text{max}$?) decides whether your plot is flipped. ZOSPy's `get_data_grid(cell_origin="bottom_left" | "center")` makes the first choice explicit [8]. The robust habit: for each new grid analysis, compare one asymmetric feature (e.g. the wavefront at an off-axis field, which has coma pointing one way) against the GUI's false-colour plot, and write the answer into the adapter's docstring.

### 1.5 Recipes for the core analyses (raw API)
The table gives the `AnalysisIDM` member, the result container, and what to watch. Names in *italics* are from memory of the Syntax Help and **must be verified against your installed version's ZOS-API Syntax Help** (Programming tab → ZOS-API Help, or the online interface docs [6]).

| Analysis | `AnalysisIDM` | Result | Notes |
|---|---|---|---|
| Standard spot diagram | `StandardSpot` [ex. 22] | `SpotData.GetRMSSpotSizeFor(f, w)`, `GetGeoSpotSizeFor(f, w)` [ex. 22] | values in µm; `ReferTo` (centroid/chief) and `RayDensity` matter; no ZOSPy 2.x wrapper at time of writing → use raw API or `zp.analyses.new_analysis` |
| FFT MTF | `FftMtf` (or `A.New_FftMtf()` [ex. 04]) | data series: one per field, `YData` with T and S columns [ex. 04] | `SampleSize`, `MaximumFrequency`; x in cycles/mm |
| Huygens MTF | *`HuygensMtf`* | data series | slower; set pupil *and* image sampling; ZOSPy has `HuygensMTF` [4] |
| Wavefront map | *`WavefrontMap`* | one data grid (waves) | ZOSPy `WavefrontMap(field=1, wavelength=1, sampling="64x64", remove_tilt=False, …)` [9]; note it takes **one** field/wavelength, not "All" |
| Field curvature / distortion | *`FieldCurvatureAndDistortion`* | data series (T/S focus shift vs field; distortion vs field — inspect `NumberOfDataSeries` and each series' `Description`/labels) | no ZOSPy wrapper at time of writing; `DIST`/`DIMX` operands are often easier for single numbers; real-image height vs paraxial reference as in Course 02 L05 |

Generic exploration snippet for an analysis you have never parsed before — run it once, print everything, then write the adapter:

```python
def dump_results(r):
    print("series:", r.NumberOfDataSeries, "grids:", r.NumberOfDataGrids)
    for i in range(r.NumberOfDataSeries):
        ds = r.GetDataSeries(i)
        y = ds.YData.Data
        print(i, ds.Description, "x:", ds.XData.Data.Length, "y:", y.GetLength(0), "x", y.GetLength(1))
    for i in range(r.NumberOfDataGrids):
        g = r.GetDataGrid(i)
        print(i, g.Description, g.Nx, g.Ny, g.Dx, g.Dy, g.MinX, g.MinY)
# member names: verify against your installed version's ZOS-API Syntax Help
```

### 1.6 Settings objects vs settings files — when to use which
| | Settings object (`GetSettings()` properties) | Settings file (`.CFG` + `ModifySettings`) |
|---|---|---|
| Discoverability | IDE/introspection, typed enums | keyword list in the ZPL `MODIFYSETTINGS` help |
| Coverage | most common settings; some analyses partial | everything the GUI dialog stores |
| Reproducibility | in your code | the `.CFG` file itself can be versioned in git and reused by GUI (*Save/Load* in the analysis settings dialog) and by ZPL |
| Typical use | sampling, field/wave, max frequency | obscure options, sharing exactly the GUI's setup with a colleague |

A pragmatic pattern: set up the analysis once in the GUI until the plot looks like the one in your report, **save its settings to a `.CFG` under `config/analyses/`**, and have the script `LoadFrom` that file and only override field/wavelength/configuration. ZOSPy's `run(oss, config_file=..., text_output_file=..., oncomplete="Close")` accepts the same idea: if `config_file` is `None`, a temporary file is created and removed [8].

## 2. ZOSPy analysis wrappers

ZOSPy wraps common analyses as classes whose constructor arguments are the settings; `.run(oss)` executes and parses [2]:

```python
import zospy as zp

mtf = zp.analyses.mtf.FFTMTF(sampling="128x128", field="All", wavelength="All",
                             maximum_frequency=150.0).run(oss)       # keyword names from the API page [3]
df = mtf.data                                                         # pandas DataFrame (inspect columns!)

tf = zp.analyses.mtf.FFTThroughFocusMTF(sampling="64x64", delta_focus=0.1).run(oss, oncomplete="Close")  # [2]
cp = zp.analyses.reports.CardinalPoints.with_settings(
        zp.analyses.reports.CardinalPointsSettings(surface_1=3, surface_2=4)).run(oss)               # [2]
```

`run()` returns a ZOSPy `AnalysisResult`; the parsed data is in `.data` (a DataFrame for curve/grid analyses, a structured object for reports — inspect it with `print(type(result.data))`). The `oncomplete` argument controls the window afterwards: `"Close"` (default), `"Release"` (keep it open, inactive) or `"Sustain"` (keep it open and active) [8] — `"Close"` is what you want in loops.

Available wrappers in recent ZOSPy include FFT MTF, FFT Through-Focus MTF, Huygens MTF; FFT/Huygens PSF and Huygens PSF & Strehl; ray fan and single ray trace; wavefront map, Zernike standard coefficients and Zernike vs field; cardinal points, surface data, system data; polarization pupil map/transmission; POP; geometric image analysis; system viewers [4]. Anything not wrapped: `zp.analyses.new_analysis(oss, zp.constants.Analysis.AnalysisIDM.<Name>, settings_first=True)`, adjust `.Settings`, then `ApplyAndWaitForCompletion()` [2].

**Version note:** ZOSPy 2.x reorganised the analyses (old-style functions remain under `zospy.analyses.old` [4]). Column names of returned DataFrames are part of the wrapper's contract but have changed between releases — write a small adapter function per analysis in your `analyses.py` that renames to *your* stable schema (e.g. `field, wavelength, freq_lpmm, mtf_t, mtf_s`). Then only that adapter changes when ZOSPy does.

## 3. Operands as a data source

Many numbers are easier and faster to get from **operands** than from windows:

| Quantity | Operand (MFE) | Notes |
|---|---|---|
| EFL, F/#, track, exit pupil | `EFFL`, `WFNO`, `TOTR`, `EXPP` | first-order; trivial |
| RMS spot (centroid) | `RSCE` | Gaussian-quadrature sampling ≠ spot diagram's grid (Course 03 L04) |
| RMS wavefront (centroid) | `RWCE` | waves |
| MTF at one frequency | `MTFT`, `MTFS` (FFT), `MTFA` (average) | per field/wave/sampling given in the row |
| Distortion | `DIST`, `DIMX` | % |
| Chief-ray angle | `RAID` | degrees, angle to the surface normal |
| Relative illumination | `RELI` | |

Two ways to evaluate operands from code: (a) rows already in the MFE (read `.Value` after `CalculateMeritFunction()`, L04); (b) temporary rows: insert at the end, evaluate, delete — or a scratch MFE file. In ZPL you'd use `OPEV()`; the API has no single "evaluate this operand" call that is as convenient (check the Syntax Help of your version for a direct evaluation method — some versions offer one on the MFE).

**Operand vs window can disagree** for legitimate reasons: sampling (GQ vs grid), reference (centroid vs chief), polychromatic weighting, field/wavelength selection, or the MTF operand's own sampling parameter. Before reporting, cross-check one representative number in both — once per design, not every run.

## 4. Making data reusable: tidy tables with metadata

Store results as **long ("tidy") tables**: one row per observation, explicit columns for every coordinate:

```text
config, object_mm, field_idx, field_value, field_type, wave_um, quantity, value, unit, sampling, zospy, opticstudio, lens_sha
2, 800, 3, 2.85, RealImageHeight, all, mtf_t@36.2, 0.663, 1, 128x128, 2.x, 25.2, a3f9...
```

Reasons: pandas `groupby`/`pivot` handle any slicing; plots become one-liners; comparisons across design versions become joins; nothing depends on remembering that "column 3 was config 1". Save as CSV (human-diffable) or Parquet (fast). Put the *settings* (sampling, max frequency, reference) in the table or in a sidecar JSON — numbers without settings are worthless in six months.

## 5. Plotting for engineers

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6, 4), constrained_layout=True)
for (field, orient), g in df.groupby(["field_value", "orient"]):
    ax.plot(g.freq_lpmm, g.mtf, ls="-" if orient == "T" else "--", label=f"{field:.2f} mm {orient}")
ax.plot(nu, mtf_perfect(nu, wl_um=0.85, fno=2.4), "k:", label="diffraction limit")
ax.axvline(36.2, color="0.6", lw=0.8); ax.axhline(0.45, color="0.6", lw=0.8)   # spec lines
ax.set(xlabel="Spatial frequency [lp/mm]", ylabel="MTF", ylim=(0, 1), title="Config 2 (0.8 m)")
ax.legend(fontsize=7, ncol=2); fig.savefig("mtf_cfg2.png", dpi=200)
```

Engineering-plot habits: draw the **spec lines** on the plot; always include the **diffraction limit**; T solid / S dashed (the OpticStudio convention, so colleagues read it instantly); same axis limits across configurations so plots can be compared side by side; file names that encode configuration and design version; never rely on colour alone.

## 6. Performance tips
- **Reuse windows** in loops: create the analysis once, change settings, `ApplyAndWaitForCompletion()` again; close at the end.
- **Sampling**: start at 64×64 (FFT MTF) and check convergence once (128, 256) for your lens; then fix it in a config file (the FFT MTF example sets `SampleSize = S_256x256` [ex. 04]).
- **Standalone mode** and lens update mode: GUI refresh costs time; ZOSPy exposes `oss.LensUpdateMode` (`None`, `EditorsOnly`, `AllWindows`) [5].
- **Prefer operands** (one number) over windows (a whole curve) inside loops; use windows for the final report.
- **Don't parse text** unless needed; when you must, parse once into your tidy schema and cache.

## 7. In OpticStudio — what to cross-check
- After writing an extraction function, run the same analysis in the GUI with the same settings and compare 2–3 numbers. Do it for each new analysis type you automate.
- Watch for "all fields" in polychromatic analyses: the GUI shows separate curves per field; the API result has one series per field (and two y-columns: T and S) [ex. 04 loops over series, y is 2D].
- Remember `SetCurrentConfiguration` before every analysis in multi-configuration lenses, and restore it.
- Huygens vs FFT: use Huygens PSF/MTF for steep beams, large field angles, or tilted image planes (Course 03 L01–L02); it's slower — sample accordingly.

## Worked example — perfect-lens MTF reference and Strehl sanity check

For the Course 04 capstone receiver (λ = 0.85 µm, F/2.4) the diffraction cutoff frequency is

$$
\nu_c = \frac{1}{\lambda N} = \frac{1}{0.85\times10^{-3}\ \text{mm} \times 2.4} = 490.2\ \text{lp/mm},
$$

and the MTF of an aberration-free circular pupil (incoherent) is

$$
\text{MTF}(\nu) = \frac{2}{\pi}\left[\arccos s - s\sqrt{1 - s^2}\right], \qquad s = \nu/\nu_c .
$$

| $\nu$ [lp/mm] | $s$ | MTF |
|---|---|---|
| 36.2 (8-px fringes) | 0.0738 | 0.906 |
| 72.5 | 0.148 | 0.812 |
| 145 (Nyquist of 3.45 µm pixels) | 0.296 | 0.629 |

These are the ceilings your extracted MTF must stay below; if your script reports 0.95 at 36.2 lp/mm at F/2.4, 850 nm, it's reading the wrong column, wavelength or F/#. (The capstone notes quote the same 0.91 at 36.2 lp/mm.)

Strehl sanity check with the Maréchal approximation $S \approx e^{-(2\pi \sigma)^2}$ ($\sigma$ = RMS wavefront error in waves): σ = 0.05 → S = 0.906; 0.07 → 0.824 (the "diffraction-limited" 0.8 boundary); 0.10 → 0.674. Cross-check your `RWCE` extraction against the Huygens PSF Strehl with these numbers: they agree well only for small σ.

Use `mtf_perfect(nu, wl_um, fno)` (Task 1) as a unit-tested function in your library — it's the simplest guard against extraction errors.

## Key takeaways
- One pattern for all analyses: `New_Analysis` → `GetSettings` → `ApplyAndWaitForCompletion` → `GetResults` → `Close`.
- Settings use 0 = all for fields/wavelengths; results are 1-based; configuration is global state you must set and restore.
- Results come as data series, data grids, analysis-specific objects (e.g. `SpotData`) or text; settings not exposed as properties go through `.CFG` + `ModifySettings`.
- ZOSPy wrappers return DataFrames — wrap them in adapters with your own stable column schema.
- Use operands for single numbers in loops, windows for curves/maps in reports; cross-check once.
- Store tidy tables with full metadata; plot with spec lines and the diffraction limit.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| `AnalysisIDM` | Enum identifying an analysis type (e.g. `StandardSpot`, `PathAnalysis`) |
| `IA_` / `IAR_` | API interfaces of an analysis window / its results |
| Data series / data grid | Result containers for curves / 2D maps |
| `ModifySettings` | Edit an analysis settings file by keyword (same keywords as ZPL `MODIFYSETTINGS`) |
| Tidy table | Long-format table with one observation per row and explicit coordinate columns |
| Cutoff frequency $\nu_c$ | $1/(\lambda N)$: highest frequency transmitted by an incoherent circular pupil |

## References
1. ZOS-API Python example 04 (FFT MTF data) <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex04_py.xhtml> and example 22 (spot analysis, batch ray trace) <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex22_py.xhtml>; examples 11 and 15 for `ModifySettings`: <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex11_py.xhtml>, <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex15_py.xhtml>
2. ZOSPy, performing analyses: <https://zospy.readthedocs.io/en/latest/user_guide/usage/analyses.html>
3. ZOSPy API, `FFTMTF`: <https://zospy.readthedocs.io/en/latest/api/zospy.analyses.mtf.fft_mtf.FFTMTF.html>
4. ZOSPy API overview (list of analysis wrappers, legacy `zospy.analyses.old`): <https://zospy.readthedocs.io/en/latest/api.html>
5. ZOSPy API, `OpticStudioSystem` (`LensUpdateMode`): <https://zospy.readthedocs.io/en/latest/api/zospy.zpcore.OpticStudioSystem.html>
6. ZOS-API Syntax Help, Analysis namespace: <https://developer.ansys.com/docs/zos-api-interface-2025-r2/namespace_z_o_s_a_p_i_1_1_analysis.xhtml>
7. Ansys Zemax community thread "Incorrect datagrid MinY for Geometric Image Analysis" (`IAR_DataGrid` members, edge-vs-centre convention): <https://community.zemax.com/zos-api-12/incorrect-datagrid-miny-for-geometric-image-analysis-5426>
8. ZOSPy API, `BaseAnalysisWrapper` (`run(oss, config_file, text_output_file, oncomplete)`, `get_data_grid(cell_origin=…)`, `get_data_series`, `get_text_output`): <https://zospy.readthedocs.io/en/latest/api/zospy.analyses.base.BaseAnalysisWrapper.html>
9. ZOSPy API, `WavefrontMap`: <https://zospy.readthedocs.io/en/latest/api/zospy.analyses.wavefront.wavefront_map.WavefrontMap.html>
10. [Kenyon §7.2, pp. 167–169] — PSF, OTF, MTF and PTF; Course 03 L02–L03 for MTF and Strehl background.
