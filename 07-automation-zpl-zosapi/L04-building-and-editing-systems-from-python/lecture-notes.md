# L04 — Building and editing systems from Python

> **Course 07 · Automation with ZPL and the ZOS-API** · Estimated time: lecture ~2.5 h, tasks ~5 h
> **Prerequisites:** [L03 — ZOS-API architecture and Python setup](../L03-zos-api-architecture-and-python-setup/) (your `zlens` repo and `connect.py`) · **Next:** [L05 — Running analyses and extracting data](../L05-running-analyses-and-extracting-data/)

## Learning objectives
- Create a sequential system from scratch in Python: system aperture, fields, wavelengths, catalogues, surfaces, materials, stop, comments.
- Read and modify LDE cells, change surface types (e.g. Even Asphere, Coordinate Break) and access type-specific parameter columns.
- Apply solves (F-number, marginal-ray height, pickups, position) and set/unset variables from code.
- Build merit-function rows (operands, parameters, targets, weights), run the Optimization Wizard from code, evaluate the merit function and read individual operand values.
- Manipulate the Multi-Configuration Editor: add configurations and operands, set per-configuration values, switch configurations.
- Run local (DLS/OD) optimization, Hammer and Global from Python with time limits, and capture the merit-function history.
- Write helper functions that find surfaces and operand rows **by comment**, so scripts survive edits to the design.

## Reading
- **Core:** ZOS-API Python examples (2025 R1 documentation): 01 *New File and QuickFocus*, 03 *Open File and Optimize*, 11 *Basic Sequential*, 15 *Sequential Optimization*, 18 *Multiple Configurations*, 19 *Surface Properties* — index at <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_exov.xhtml>. Read 15 and 18 completely; they contain nearly every call in this lesson.
- **Core:** ZOSPy user guide, "Creating an optical system" (LDE, solvers): <https://zospy.readthedocs.io/en/latest/user_guide/usage/lens_data_editor.html>
- **Refresh:** [Course 01 L07 — solves, variables, first optimization](../../01-foundations/L07-solves-variables-first-optimization/lecture-notes.md); [Course 03 L04 — merit function mastery](../../03-image-quality-optimization/L04-merit-function-mastery/lecture-notes.md); [Course 03 L06 — multi-configuration](../../03-image-quality-optimization/L06-multi-configuration-and-zoom/lecture-notes.md).
- **Reference:** ZOS-API Syntax Help — `ILensDataEditor`, `ILDERow`, `IEditorCell`, `ISolveData`, `IMeritFunctionEditor`, `IMFERow`, `IMultiConfigEditor`, `ILocalOptimization`.

---

## 1. The editing model: rows, cells, solves

Every editor in the API follows the same pattern:

```
Editor (LDE / MFE / MCE / TDE / NCE)
 └─ Row  (ILDERow = surface, IMFERow = operand, IMCERow = MC operand, …)
     ├─ convenience properties (Radius, Thickness, Material, Comment, Target, Weight, …)
     └─ Cells (IEditorCell): RadiusCell, ThicknessCell, MaterialCell, GetSurfaceCell(column), GetOperandCell(column) …
          ├─ value  (DoubleValue / IntegerValue / Value(string))
          └─ solve  (CreateSolveType(type) → ISolveData → SetSolveData; MakeSolveVariable; MakeSolveFixed)
```

- **Convenience properties** set values directly: `surf.Radius = 100`, `surf.Thickness = 5`, `surf.Material = "N-BK7"` [ex. 11].
- **Cells** are where solves and variables live: `surf.ThicknessCell.MakeSolveVariable()` [ex. 3]; `surf.RadiusCell.CreateSolveType(ZOSAPI.Editors.SolveType.FNumber)` [ex. 15].
- Indices: LDE surfaces 0 … `NumberOfSurfaces − 1` (object = 0, image = last); MFE/MCE rows start at 1.

Everything below uses raw ZOS-API names reachable through ZOSPy's `oss` (which exposes `LDE`, `MFE`, `MCE`, `SystemData`, `Tools`) and enums through `zp.constants` (which mirror `ZOSAPI.*`). Where a call is quoted from an official example, it's tagged [ex. N]. Everything is version-sensitive in details: **verify against your installed version's ZOS-API Syntax Help**.

## 2. System Explorer from code

```python
import zospy as zp
C = zp.constants

def setup_system(oss, epd: float, fields_deg: list[float], waves_um: list[float], primary: int = 2):
    sd = oss.SystemData
    sd.Aperture.ApertureType = C.SystemData.ZemaxApertureType.EntrancePupilDiameter   # [ex. 15]
    sd.Aperture.ApertureValue = epd                                                   # [ex. 15]
    sd.MaterialCatalogs.AddCatalog("SCHOTT")                                           # [ex. 11]

    # fields: field 1 exists; set it, add the others
    sd.Fields.GetField(1).Y = fields_deg[0]          # property name: verify (X/Y on IField)
    for y in fields_deg[1:]:
        sd.Fields.AddField(0.0, y, 1.0)              # (x, y, weight)  [ex. 15]

    # wavelengths: a preset is easiest  [ex. 15]; or edit/add explicitly
    wl = sd.Wavelengths
    wl.GetWavelength(1).Wavelength = waves_um[0]     # [ZOSPy README]
    for w in waves_um[1:]:
        wl.AddWavelength(w, 1.0)                     # (µm, weight) — verify signature
    wl.GetWavelength(primary).MakePrimary()          # verify method name
```

Field *type* (angle, object height, paraxial/real image height) is set on the Fields object (`SetFieldType(ZOSAPI.SystemData.FieldType.ParaxialImageHeight)` [ex. 15]). Ray aiming, apodization, environment (temperature/pressure) and units are all under `SystemData` too (`Aperture.ApodizationType`, `Units.LensUnits` [ex. 11]; `Environment.AdjustIndexToEnvironment` [ex. 18]).

> **Habit:** after building, **print what you built** (`EPD`, field list, wavelengths, primary) and compare with System Explorer once. Two-line sanity checks save hours.

## 3. Lens Data Editor

### 3.1 Inserting and editing surfaces

```python
def build_singlet(oss, R1=102.7, R2=-102.7, t=4.0, glass="N-BK7"):
    lde = oss.LDE
    s1 = lde.InsertNewSurfaceAt(1)        # new system: 0 obj, 1 stop, 2 img → insert pushes stop down
    s2 = lde.InsertNewSurfaceAt(2)
    lde.GetSurfaceAt(0).Thickness = float("inf")      # object at infinity [ZOSPy README]
    s1.Radius, s1.Thickness, s1.Material, s1.Comment = R1, t, glass, "L1 front"
    s2.Radius, s2.Comment = R2, "L1 rear"
    s1.IsStop = True                      # [ex. 11]
    return s1, s2
```

After inserts, **re-fetch rows by index** if you are unsure which row is where — inserting shifts everything below. Better: give every surface a comment and look it up (§3.4).

### 3.2 Surface types and parameter columns
Changing a surface type is a two-step "settings object" pattern [ex. 19]:

```python
lde = oss.LDE
s = lde.GetSurfaceAt(3)
st = s.GetSurfaceTypeSettings(C.Editors.LDE.SurfaceType.EvenAspheric)   # [ex. 19 uses CoordinateBreak]
s.ChangeType(st)
s.Conic = -0.8                                                          # verify property name
# parameter columns: Par1, Par2, ... (meaning depends on the type; for Even Asphere: 2nd-, 4th-, 6th-order terms …)
s.GetSurfaceCell(C.Editors.LDE.SurfaceColumn.Par2).DoubleValue = 1.2e-5  # 4th-order term — check column mapping
```

Which `ParN` holds which coefficient differs per surface type — check the LDE column headers in the GUI after changing the type, or the Syntax Help for that type. Coordinate breaks: `ChangeType` to `CoordinateBreak`, then decenter/tilt in `Par1…Par5` (or use `TiltDecenterData` on an ordinary surface [ex. 19]).

### 3.3 Solves and variables

```python
SolveType = C.Editors.SolveType

# Variables [ex. 3]
lde.GetSurfaceAt(1).RadiusCell.MakeSolveVariable()
lde.GetSurfaceAt(2).RadiusCell.MakeSolveVariable()

# F-number solve on the last radius [ex. 15]
last = lde.GetSurfaceAt(lde.NumberOfSurfaces - 2)
sol = last.RadiusCell.CreateSolveType(SolveType.FNumber)
sol._S_FNumber.FNumber = 5.0
last.RadiusCell.SetSolveData(sol)

# Pickup: thickness of surface 10 follows another surface [ex. 15]
p = lde.GetSurfaceAt(10).ThicknessCell.CreateSolveType(SolveType.SurfacePickup)
# p._S_SurfacePickup.Surface = 2 ; .ScaleFactor = -1 ; .Column = SurfaceColumn.Thickness (names: verify)
lde.GetSurfaceAt(10).ThicknessCell.SetSolveData(p)

# Housekeeping tools [ex. 15]
oss.Tools.RemoveAllVariables()
oss.Tools.SetAllRadiiVariable()
```

The `_S_<Name>` accessor (e.g. `_S_FNumber`, `_S_ThermalPickup` [ex. 18], `_S_ElementPower` [ZOSPy docs]) is how pythonnet reaches the type-specific solve settings — this is the interface-casting issue from L03 §3.3 in practice. ZOSPy offers helper functions for some solves, e.g. `zp.solvers.position(cell, from_surface=..., length=...)` and `zp.solvers.material_model(cell, refractive_index=1.5)` [ZOSPy docs].

To freeze a variable again, set a fixed solve (`MakeSolveFixed()` — verify) or call `RemoveAllVariables()` and re-declare.

### 3.4 Find by comment — the most important helper

```python
def surface_by_comment(oss, comment: str) -> int:
    """Return the LDE index of the unique surface whose Comment equals `comment` (case-insensitive)."""
    lde = oss.LDE
    hits = [i for i in range(lde.NumberOfSurfaces)
            if (lde.GetSurfaceAt(i).Comment or "").strip().upper() == comment.upper()]
    if len(hits) != 1:
        raise LookupError(f"{len(hits)} surfaces with comment {comment!r}")
    return hits[0]

focus = surface_by_comment(oss, "FOCUS COMP")   # Course 04 capstone convention
```

Raise on 0 *or* >1 hits: silent "first match" is how scripts quietly edit the wrong surface after a colleague duplicates a lens element.

## 4. Merit Function Editor

### 4.1 Rows, operands, parameters

```python
MFE = oss.MFE
MOT = C.Editors.MFE.MeritOperandType
op = MFE.InsertNewOperandAt(1)          # or MFE.AddOperand()        [ex. 3]
op.ChangeType(MOT.EFFL)                 # [ex. 3 uses ASTI]
op.GetCellAt(3).IntegerValue = 2        # parameter columns by position: verify which index is "Wave" for EFFL
op.Target = 8.0                         # [ex. 3]
op.Weight = 1.0                         # [ex. 3]
```

Parameter columns: `op.GetCellAt(k)` by position [ex. 3], or `op.GetOperandCell(C.Editors.MFE.MeritColumn.Param1)` by name (verify). The column meaning (Surf, Wave, Hx, Hy, Px, Py, …) is operand-specific — exactly as in the GUI. **Tip:** build the row in the GUI once, then read it back from Python (`ChangeType`, cell values) to learn which index is which.

### 4.2 Default merit function via the Wizard
The Optimization Wizard is scriptable [ex. 15]:

```python
wiz = MFE.SEQOptimizationWizard
wiz.Data = 1               # enum-like integers: criterion/type (meaning: see Syntax Help; ex. 15 uses 1)
wiz.OverallWeight = 1
wiz.Ring = 2               # number of rings index
wiz.IsGlassUsed, wiz.GlassMin, wiz.GlassMax, wiz.GlassEdge = True, 3.0, 15.0, 3.0
wiz.IsAirUsed,   wiz.AirMin,   wiz.AirMax,   wiz.AirEdge   = True, 0.5, 1000.0, 0.5
wiz.Apply()
```

Integer codes such as `Data = 1` or `Ring = 2` are *indices into the GUI drop-downs* — read the Syntax Help for `ISEQOptimizationWizard` and confirm by applying and looking at the generated rows. Save/load merit functions as files: `MFE.SaveMeritFunction(path)`, `MFE.LoadMeritFunction(path)` [ex. 15] — a clean way to version the MF separately from the lens.

### 4.3 Evaluating
```python
mf = MFE.CalculateMeritFunction()       # recompute all rows, returns the MF value (verify)
efl = MFE.GetOperandAt(1).Value         # value column of row 1 (verify property name)
```

**Dashboard rows by comment.** The Course 04 capstone put zero-weight "dashboard" operands at the top of the MFE with comments. Read them by comment rather than by row number (helper in Task 3) — the MF can grow without breaking your report. For `BLNK` rows the comment is the text of the row; for other operands use the comment column (verify the column name/property in your version).

## 5. Multi-Configuration Editor

From example 18 [ex. 18]:

```python
MCE = oss.MCE
MCOT = C.Editors.MCE.MultiConfigOperandType
MCE.AddConfiguration(False)              # now 2 configs
MCE.AddConfiguration(False)              # 3 configs
op = MCE.GetOperandAt(1)
op.ChangeType(MCOT.THIC)
op.Param1 = 0                            # surface 0 → object distance
for cfg, dist in enumerate([600.0, 800.0, 1200.0], start=1):
    op.GetOperandCell(cfg).DoubleValue = dist
MCE.SetCurrentConfiguration(2)           # make config 2 active for analyses/ray traces
```

Configuration-dependent analysis = `SetCurrentConfiguration(k)` then run the analysis. Remember to restore the original configuration (L01 lesson, same rule). Thermal configurations use `TEMP`/`PRES` operands and thermal pickup solves [ex. 18].

## 6. Optimization from code

### 6.1 Local
```python
Opt = C.Tools.Optimization
lo = oss.Tools.OpenLocalOptimization()                   # [ex. 3, 15]
try:
    lo.Algorithm = Opt.OptimizationAlgorithm.DampedLeastSquares
    lo.Cycles = Opt.OptimizationCycles.Automatic
    lo.NumberOfCores = 8
    mf0 = lo.InitialMeritFunction
    lo.RunAndWaitForCompletion()
    mf1 = lo.CurrentMeritFunction
finally:
    lo.Close()
```

### 6.2 Hammer and Global, with time limits
```python
ho = oss.Tools.OpenHammerOptimization()                   # [ex. 3, 15]
try:
    ho.NumberOfCores = 8
    ho.RunAndWaitWithTimeout(600)      # seconds
    ho.Cancel(); ho.WaitForCompletion()
    best = ho.CurrentMeritFunction
finally:
    ho.Close()
```
Global optimization saves the best N solutions (`NumberToSave = OptimizationSaveCount.Save_10`; `CurrentMeritFunction(j)` per solution) [ex. 15].

### 6.3 Log the trajectory
For reproducibility, record per run: start MF, end MF, wall time, algorithm, cycles, cores, variable list (surface/column), and the git commit. Write this as one JSON line per run (`runs.jsonl`). In L07 you'll analyse dozens of such runs.

### 6.4 Quick Focus and other tools
`oss.Tools.OpenQuickFocus()` with `Criterion = QuickAdjustCriterion.SpotSizeRadial`, `UseCentroid = True` [ex. 15]; `OpenScale()` for scaling a lens [ex. 11]. Same open/run/close pattern.

## 7. Files

- `oss.load(path)` / `oss.save()` / `oss.save_as(path)` (ZOSPy; raw: `LoadFile`, `Save`, `SaveAs` [ex. 3]). Absolute paths.
- Save **`.zmx`** for anything you will diff (L03 §5.1). Save intermediate states (`_after_wizard.zmx`, `_after_dls.zmx`) when debugging a pipeline — they are cheap and make failures inspectable in the GUI.
- `oss.copy_system()` for what-if edits that must not touch the loaded design.

## 8. In OpticStudio — pitfalls
- **Indices shift** after `InsertNewSurfaceAt`/`RemoveSurfaceAt`; never cache an index across edits — cache comments.
- **Stop surface:** `IsStop` moves the stop; inserting before the stop moves its index.
- **Infinite thickness:** `float("inf")` works for the object distance [ZOSPy README]; printing it shows `Infinity`.
- **Glass not found:** a material name not in the loaded catalogues gives an error status rather than an exception in some versions — check `oss.get_current_status()` / `update_status()` (ZOSPy) after building.
- **Solve order:** solves evaluate in surface order; a solve that depends on a later surface may be one update behind (same rule as in L02).
- **Wizard integers** are drop-down indices; a different version may order the drop-down differently. Verify by reading the generated rows.
- **Units:** lens units (mm), µm for wavelengths, degrees for angles.

## Worked example — a singlet built entirely from Python, checked by hand

Build: object at ∞, EPD 20 mm, fields 0/3.5/5°, F-d-C with d primary, N-BK7 equiconvex singlet $R_1 = 102.7$, $R_2 = -102.7$, $t = 4$ mm (the Course 01 L01 lens).

**Hand check (thick lens, $n_d = 1.5168$):** surface powers $\phi_1 = (n-1)/R_1 = 0.5168/102.7 = 5.0321\times10^{-3}$ mm⁻¹, $\phi_2 = (1-n)/R_2 = 5.0321\times10^{-3}$ mm⁻¹;

$$
\phi = \phi_1 + \phi_2 - \frac{t}{n}\phi_1\phi_2 = 1.00643\times10^{-2} - \frac{4}{1.5168}(5.0321\times10^{-3})^2 = 9.9975\times10^{-3}\ \text{mm}^{-1},
$$

so $f' = 100.03$ mm and the back focal distance $\text{BFD} = f'\left(1 - \frac{t}{n}\phi_1\right) = 100.03 \times (1 - 0.013270) = 98.70$ mm.

**From code:** add rows `EFFL` (wave 2) and read `.Value` after `CalculateMeritFunction()`; put a marginal-ray-height solve (height 0) on the last thickness and read `lde.GetSurfaceAt(2).Thickness`. Expect EFFL ≈ 100.03 mm and the solved thickness ≈ 98.70 mm (paraxial focus). Then add an `FNumber` solve 5.0 on $R_2$ and make $R_1$ variable with an `EFFL` target of 100: after DLS, $F/\# = f'/D = 100/20 = 5$ is held by the solve and the bending moves toward the minimum-spherical form (Course 02 L02): for $n \approx 1.52$ at infinite conjugate that is a shape factor of roughly +0.7, i.e. a stronger front surface ($R_1$ shrinks to roughly 60 mm) and a much weaker rear surface ($|R_2|$ grows to several hundred mm) — as you found by hand in Course 01 L07.

## Key takeaways
- The API mirrors the editors: rows with convenience properties, cells with values and solves; solves via `CreateSolveType` → `_S_<Type>` settings → `SetSolveData`.
- Surface types change through `GetSurfaceTypeSettings` + `ChangeType`; type-specific data lives in `ParN` columns.
- MFE rows: `InsertNewOperandAt`/`AddOperand`, `ChangeType`, cells, `Target`, `Weight`; the Wizard is scriptable but its integers are drop-down indices.
- MCE: `AddConfiguration`, operand `ChangeType`, `Param1`, per-config `GetOperandCell(k)`; `SetCurrentConfiguration` before analyses.
- Optimizers are tools: open → configure → run (with timeout for Hammer/Global) → close in `finally`; log every run.
- Find surfaces and dashboard rows by comment; never trust cached indices.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| `ILDERow` / `IMFERow` / `IMCERow` | API row objects of the LDE, MFE, MCE |
| `IEditorCell` | One editor cell; holds a value and solve data |
| `CreateSolveType` / `SetSolveData` | Create solve settings of a given type for a cell / apply them |
| `_S_<Type>` | pythonnet accessor for type-specific solve or aperture settings |
| `GetSurfaceTypeSettings` / `ChangeType` | Two-step surface-type change |
| `SEQOptimizationWizard` | API handle of the sequential Optimization Wizard |
| `RunAndWaitWithTimeout` | Run a tool for at most N seconds |
| Dashboard row | Zero-weight MF operand used only to report a key number |

## References
1. ZOS-API examples index (2025 R1), with Python examples 01, 03, 11, 15, 18, 19: <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_exov.xhtml>; e.g. ex. 3 <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex03_py.xhtml>, ex. 15 <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex15_py.xhtml>, ex. 18 <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex18_py.xhtml>, ex. 19 <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex19_py.xhtml>, ex. 11 <https://developer.synopsys.com/docs/zos-api-interface-2025-r1/page_ex11_py.xhtml>
2. ZOSPy user guide, creating an optical system (LDE, solvers): <https://zospy.readthedocs.io/en/latest/user_guide/usage/lens_data_editor.html>
3. ZOSPy README example (aperture type, wavelength, infinite object): <https://github.com/MREYE-LUMC/ZOSPy>
4. ZOSPy API: `OpticStudioSystem` (load/save/save_as/copy_system/update_status): <https://zospy.readthedocs.io/en/latest/api/zospy.zpcore.OpticStudioSystem.html>
5. ZOS-API Syntax Help for your installed version (authoritative for every property name used above).
6. Course cross-references: Course 01 L07, Course 02 L02, Course 03 L04/L06, Course 04 L10 hand-off conventions.
