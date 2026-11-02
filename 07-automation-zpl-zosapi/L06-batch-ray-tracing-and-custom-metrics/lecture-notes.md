# L06 — Batch ray tracing and custom metrics

> **Course 07 · Automation with ZPL and the ZOS-API** · Estimated time: lecture ~3 h, tasks ~6 h
> **Prerequisites:** [L05 — Running analyses and extracting data](../L05-running-analyses-and-extracting-data/); [L01 — ZPL fundamentals (`RAYTRACE`, `RAYE`/`RAYV`)](../L01-zpl-macro-fundamentals/); [Course 04 L03 — relative illumination & telecentricity](../../04-machine-vision-camera-lenses/L03-relative-illumination-and-telecentricity/); [Course 04 L05 — distortion mappings & Brown–Conrady](../../04-machine-vision-camera-lenses/L05-wide-angle-and-distortion-mappings/) · **Next:** [L07 — Automated optimization and tolerancing](../L07-automated-optimization-and-tolerancing/)

> **API caveat (read first).** The batch-ray-trace calls used in the official example 22 (`OpenBatchRayTrace`, `CreateNormUnpol`, `AddRay`, `RunAndWaitForCompletion`, `StartReadingResults`, `ReadNextResult`, `ClearData`, `Close`) are quoted from that example [1]. Everything else marked *verify* — enum members, helper-DLL signatures, `SetFieldType`, `Marshal.Copy` overloads from pythonnet — is written from documentation and forum threads, not run against your installation. **Verify against your installed version's ZOS-API Syntax Help** (Programming tab → ZOS-API Help) before you rely on it, and record what you find in `notes.md`.

## Learning objectives
- Trace arbitrary sets of real rays with `IBatchRayTrace` / `IRayTraceNormUnpolData`. That means using normalized field and pupil coordinates correctly, reading the 15-value result tuple, filtering on error and vignetting codes, and choosing an OPD mode.
- Explain where the time goes when Python traces rays one `AddRay`/`ReadNextResult` call at a time, and choose between a per-ray loop, the Ansys `RayTrace.dll` helper, your own compiled C# helper, a ZPL loop and a UDOC.
- Build four camera metrics from your own rays: a full-field 2D distortion map with a Brown–Conrady fit, CRA vs image height, RMS spot radius from a pupil grid, and depth-dependent (multi-configuration) image-point shift.
- Post-process ray data with vectorized numpy (masks, weighted centroids, per-group statistics) and no Python loops over rays.
- Validate every custom metric against an OpticStudio operand or analysis (`REAY`, `RAID`, `DIST`, `RSCE`, `OPDC`, Grid Distortion, Standard Spot), and explain the differences that remain.
- Spot the classic traps: a Real Image Height field type that hides distortion, sparse fit points that hide model residuals, square-grid sampling bias, and stale configurations.

## Reading
- **Core (API):** ZOS-API Python example 22, *Single/batch ray trace + spot diagram*. This is the reference pattern for `CreateNormUnpol`/`AddRay`/`ReadNextResult` in Python: <https://developer.synopsys.com/docs/zos-api-interface-2025-r2/page_ex22_py.xhtml> (same example on the Ansys developer portal: <https://developer.ansys.com/docs/zos-api-interface-2025-r2/_python_standalone_22_seq_spot_diagram_8py-example.xhtml>).
- **Core (performance):** M. Humphreys, Ansys Optics KB, "Batch Processing of Ray Trace Data using ZOS-API in MATLAB or Python" (`RayTrace.dll`): <https://optics.ansys.com/hc/en-us/articles/42661765866899-Batch-Processing-of-Ray-Trace-Data-using-ZOS-API-in-MATLAB-or-Python>.
- **Core (optics):** [Kidger §4.4.2.4, pp. 79–82], distortion definitions for finite and infinite conjugates. Read §4.4.2.4.4 (p. 81) on how pupil aberration and defocus change the computed distortion. It is the theory behind §5.4 of this lesson.
- **Refresh:** [Geary Ch. 7, §7.1–7.3, pp. 65–76] and [Kidger §4.2–4.3, pp. 65–70], ray patterns in the pupil and spot diagrams. [Geary Ch. 15, pp. 167–173], distortion.
- **Forum threads worth reading** (practical details the help file glosses over): Python + `RayTrace.dll` <https://community.zemax.com/got-a-question-7/getting-raytrace-dll-working-in-python-for-seq-raytracing-2769>; OPD modes <https://community.zemax.com/got-a-question-7/understanding-opdmode-in-zosapi-tools-raytrace-3012>; minimal Python batch example <https://community.zemax.com/zos-api-12/zos-api-python-sequential-batch-ray-trace-example-4564>; "large amount of single ray trace" <https://community.zemax.com/zos-api-12/large-amount-of-single-ray-trace-5733>.
- **ZOSPy constants** (`None` → `None_`): <https://zospy.readthedocs.io/en/latest/usage/04_constants.html>.

---

## 1. Why trace rays yourself?

Analyses (L05) answer the questions Ansys anticipated. Operands answer them one number at a time. Many questions a 3D-camera engineer asks fall between the two:

- *Where does every pixel of the sensor look in object space, and how well does the calibration model (Brown–Conrady) describe it?* The Field Curvature/Distortion plot gives one radial curve; Grid Distortion gives a coarse grid in a text dump. Neither gives you the fit residual in pixels.
- *What is the chief-ray angle at the sensor at 200 image heights and 8 azimuths, and how far is it from the sensor's microlens CRA curve?*
- *How far does the image of a fixed object direction move when the object goes from 0.6 m to 1.2 m?* This is depth-dependent distortion, which turns directly into 3D error after triangulation (Course 04 L09).
- *What is the RMS spot radius, computed exactly the way my detection algorithm sees the blur (centroid, my weighting, my sampling)?*

All four are ray-level questions. The ray is the atom of geometric optics [Kidger Ch. 3, §3.1–3.5, pp. 45–57]: every spot diagram, every distortion number and every geometric MTF is built from traced rays. If you can trace 10⁵ rays per second into numpy, you can build any geometric metric you like, and then validate it against the built-in one.

`IBatchRayTrace` is the ZOS-API tool for this. It does in compiled code what `RAYTRACE` does one ray at a time in ZPL (L01), and it is what UDOCs use internally for heavy operands (L02).

## 2. The batch ray trace tool

### 2.1 The family of ray-data objects

`oss.Tools.OpenBatchRayTrace()` returns an `IBatchRayTrace`. Like the optimizer and the tolerancer, it is a *tool*: only one can be open per system, and it must be closed (L03 §2). From it you create a ray container of one of four sequential types [2]:

| Creator → interface | Rays defined by | Polarization | Old DDE analogue |
|---|---|---|---|
| `CreateNormUnpol` → `IRayTraceNormUnpolData` | normalized field $(H_x,H_y)$ + normalized pupil $(P_x,P_y)$ | no | mode 0 |
| `CreateNormPol` → `IRayTraceNormPolData` | normalized coords | yes (Jones vector in, intensity/phase out) | mode 2 |
| `CreateDirectUnpol` → `IRayTraceDirectUnpolData` | explicit start point $(X,Y,Z)$ + direction cosines $(L,M,N)$ on a start surface | no | mode 1 |
| `CreateDirectPol` → `IRayTraceDirectPolData` | explicit | yes | mode 3 |

There is also a non-sequential ray trace and a ZRD reader (Course 05), which this lesson does not cover. **Normalized unpolarized** covers 90 % of lens-design metrics and is the subject here. Use *direct* rays when you need rays that do not come from a field point, for example a footprint study from a specific point on the object, or rays launched from an intermediate surface.

### 2.2 Normalized coordinates — what (Hx, Hy, Px, Py) really mean

These are the same coordinates as in the merit function (`REAY`, `RAID`…) and in ZPL `RAYTRACE` (L01 §5.1):

- **Field** $(H_x, H_y)$ is scaled so that the *maximum field* has $|H| = 1$. The scaling depends on the **field normalization** setting (System Explorer → Fields: *Radial* or *Rectangular*; location varies by version). With *Radial* normalization, $H_x^2 + H_y^2 \le 1$ spans a circle of radius "max field". With *Rectangular*, $H_x$ and $H_y$ are scaled independently by the max $|x|$ and max $|y|$ field. The field points in the Field Data Editor are only a convenience. The batch trace never asks for a field *number*, so you can trace any field point.
- **What "field" means depends on the field type.** With *Angle*, $H$ scales object-space angles. With *Object Height*, it scales object coordinates. With *Paraxial/Real Image Height*, OpticStudio solves for the object point whose chief ray lands at $H \cdot h_{max}$ on the image. This last point is the biggest trap in the lesson: **with Real Image Height fields, a grid of $(H_x,H_y)$ lands on a perfect grid on the sensor by construction.** A "distortion map" built from those rays shows zero distortion. The Course 04 capstone uses Real Image Height fields. §5.1 shows how to deal with this.
- **Pupil** $(P_x, P_y)$: $P_x^2 + P_y^2 = 1$ is the edge of the entrance pupil. With **ray aiming** on (the capstone has it on), $(P_x, P_y)$ are mapped onto the real stop, so $P = 0$ is the real chief ray through the stop centre. With ray aiming off it is the ray aimed at the paraxial entrance-pupil centre. For wide-angle lenses with strong pupil aberration the two differ visibly (Kidger §4.4.2.4.4 explains why distortion then depends on the choice).
- **Vignetting factors** (VDX, VDY, VCX, VCY, VAN in the Field Data Editor) rescale the pupil per field, so $|P| = 1$ then means the edge of the *vignetted* pupil. Most analyses honour this, and the batch trace does too. Keep vignetting factors at zero for metric studies, or record that they are set.
- **Wavelength** is a 1-based wavelength *number* passed per ray, so one batch can mix wavelengths.

### 2.3 The canonical pattern

The structure follows example 22 [1]. The wrapping (ZOSPy `oss`, numpy, `try/finally`) is ours.

```python
# src/zlens/raytrace.py — minimal, slow-but-correct reference implementation
import numpy as np
import zospy as zp
from System import Int32, Double            # pythonnet; placeholders for out-parameters [1]

FIELDS = ("X", "Y", "Z", "L", "M", "N", "l2", "m2", "n2", "opd", "intensity")

def trace_norm_unpol(oss, hx, hy, px, py, wave, to_surface=None, opd_mode="None_"):
    """Trace real, normalized, unpolarized rays. Returns dict of numpy arrays (length n).
    Rays are returned in input order (ray numbers are 1-based in the API)."""
    hx, hy, px, py, wave = np.broadcast_arrays(*(np.asarray(a) for a in (hx, hy, px, py, wave)))
    hx, hy, px, py, wave = (a.ravel() for a in (hx, hy, px, py, wave))
    n = hx.size
    if to_surface is None:
        to_surface = oss.LDE.NumberOfSurfaces - 1                    # image surface
    RT = zp.constants.Tools.RayTrace                                  # verify path in your ZOSPy
    tool = oss.Tools.OpenBatchRayTrace()
    if tool is None:
        raise RuntimeError("Could not open batch ray trace: is another tool open?")
    try:
        data = tool.CreateNormUnpol(n, RT.RaysType.Real, to_surface)  # [1]
        mode = getattr(RT.OPDMode, opd_mode)                          # 'None_' in ZOSPy constants [9]
        for i in range(n):                                            # <-- the slow part (§3)
            data.AddRay(int(wave[i]), float(hx[i]), float(hy[i]),
                        float(px[i]), float(py[i]), mode)
        tool.RunAndWaitForCompletion()
        data.StartReadingResults()
        out = {k: np.full(n, np.nan) for k in FIELDS}
        err = np.zeros(n, np.int32); vig = np.zeros(n, np.int32)
        ph = [Int32(0)] * 3 + [Double(0.0)] * 11                      # 3 int + 11 double out-params [1]
        while True:
            r = data.ReadNextResult(*ph)          # (ok, rayNumber, err, vig, X..intensity)
            if not r[0]:
                break
            k = r[1] - 1
            err[k], vig[k] = r[2], r[3]
            for j, name in enumerate(FIELDS):
                out[name][k] = r[4 + j]
    finally:
        tool.Close()
    out.update(err=err, vig=vig, hx=hx, hy=hy, px=px, py=py, wave=wave)
    return out
```

Notes on the details:

- **The result tuple.** pythonnet returns the method's `bool` first, then every out-parameter: ray number, error code, vignette code, $X, Y, Z$, direction cosines $L, M, N$, surface-normal cosines $l_2, m_2, n_2$, OPD and intensity. That makes 15 values. Example 22 reads exactly this layout: `output[1]` ray number, `[2]` error, `[3]` vignette, `[4]` X, `[5]` Y [1]. Coordinates are in lens units, in the **local coordinate frame of the target surface** (the same as `REAX/REAY`). This is different from global coordinates after coordinate breaks.
- **Error and vignette codes** follow the ZPL `RAYE()`/`RAYV()` conventions you already know (L01 §5.2). Error 0 means OK. A positive error is the surface number where the ray missed. A negative error flags total internal reflection at surface |code|. A non-zero vignette code is the surface where the ray was clipped by an aperture. **Always build a mask** `ok = (err == 0) & (vig == 0)`. A vignetted ray can still carry plausible-looking coordinates. Example 22 keeps only rays where both codes are zero [1].
- **Enums named `None`.** `None` is a Python keyword. Example 22 uses `Enum.Parse(ZOSAPI.Tools.RayTrace.OPDMode, "None")` [1]. ZOSPy exposes the same member as `OPDMode.None_` [9].
- **Capacity.** The first argument of `CreateNormUnpol` is the maximum number of rays you will add. To reuse the container with a new batch, call `data.ClearData()` [1]. For very large traces, work in chunks of 10⁵–10⁶ rays so the memory per container stays bounded.
- **Configuration.** The tool traces the *current* configuration. Set it (`oss.MCE.SetCurrentConfiguration(k)`; L05) **before** opening the tool, and restore it in `finally`. Do not edit the lens while a tool is open.
- **`RaysType.Paraxial`** (verify) traces paraxial rays with the same interface. That is handy for computing paraxial reference heights with exactly the same field/pupil definitions.

### 2.4 OPD modes

`AddRay` takes an `OPDMode`. The forum thread with Ansys staff describes three members [5]. `None` returns no OPD reference; the thread reports that the returned value then behaves like an absolute optical path length, probably in lens units. `Current` returns the path difference relative to the *previous* ray. `CurrentAndChief` returns the OPD relative to the chief ray of the current field. The practical recipe from that thread is: trace the chief ray first, or use `CurrentAndChief`, and expect OPD in **waves**. The order of rays in the batch can therefore matter.

The thread also documents an unexplained factor of ~10 between a user's OPD and the Wavefront Map. Treat OPD from the batch trace as *untrusted until validated*. Compare a handful of pupil points with the `OPDC` operand (OPD w.r.t. chief ray, in waves) at the same $(H_x,H_y,P_x,P_y)$ before you build wavefront metrics on it.

## 3. Performance: why per-ray calls are slow, and what to do

The trace itself is fast: OpticStudio traces millions of real rays per second through a 10-surface lens. What costs time in §2.3 is the **two Python→.NET calls per ray** (`AddRay`, `ReadNextResult`). Each call converts arguments, allocates tuples and, in interactive-extension mode, crosses a process boundary (L03 §2). Example 22's own comment says that pythonnet requires placeholder objects for every by-reference argument [1]. That is 14 boxed values per ray, plus a 15-tuple coming back.

Ansys's KB article quantifies the problem in MATLAB: **961 rays in more than 4 s** with native loops (≈ 4 ms/ray), against **10,000 rays in about 1 s** with the compiled helper. It claims speed-ups of up to 40× depending on the machine [2]. Python via pythonnet in standalone mode is usually much better than that MATLAB figure, but per-ray costs of tens of µs (standalone) to ~1 ms (extension mode) are typical. Task 1 makes you **measure** your own numbers. The budget arithmetic:

$$
t \approx N_{\text{rays}} \cdot c_{\text{call}} + t_{\text{trace}}, \qquad N_{\text{rays}} = 3228 \text{ pupil points} \times 6 \text{ fields} \times 3 \text{ configs} = 58\,104 .
$$

At $c_{\text{call}} = 50$ µs that is 2.9 s, which is fine for a report. At 1 ms it is 58 s, which is not fine inside an optimization loop.

Your options, from simplest to fastest:

| Approach | How | Per-ray Python cost | When |
|---|---|---|---|
| **A. Per-ray loop** (§2.3) | `AddRay`/`ReadNextResult` from Python | full call overhead ×2 | reference implementation, unit tests, ≤ 10⁴ rays |
| **B. Ansys `RayTrace.dll`** [2][3] | Compiled C# helper loaded with `clr.AddReference`; wraps the four batch interfaces, adds rays from arrays and reads results in blocks. The forum example uses `BatchRayTrace.ReadNormUnpolData(tool, normUnpol)`, `InitializeOutput(...)`, `AddRay(wave, [hx…], [hy…], [px…], [py…], mode)` with *lists*, then loops `ReadNextBlock(rays)` until it returns 0 and reads `rays.X`, `rays.Y` [3] | one call per block | fast results with zero C# work. **Caveats:** posted 2021, not updated since, confirmed by its author in 2025 [6]; the ZRD part predates the new ZRD format; you must unblock the downloaded zip; a 2025 user could not import it [3]. Verify it still loads against your OpticStudio's .NET runtime |
| **C. Your own C# helper** (§3.1) | 40 lines of C#, same idea as B, built against *your* installed `ZOSAPI.dll` | one call per batch | best long-term option for you: you control the code, the target framework and the output layout (a flat `double[]` you can bulk-copy into numpy) |
| **D. ZPL loop** (§4) | `RAYTRACE` inside OpticStudio, write a text file, read it with numpy | none (interpreted, in-process) | quick studies, no Python; tens of µs per ray (L02 §3) |
| **E. UDOC / user extension** (L02) | C# operand calling the batch trace | none | metric used *inside* the merit function |
| **F. Built-in analyses/operands** | Grid Distortion, Standard Spot, `RSCE`, `REAY` | n/a | whenever they compute what you need. Always the validation reference |

Before you optimize, check whether ZOSPy has gained a batch wrapper. At the time of writing its API reference lists `SingleRayTrace` and `RayFan` analysis wrappers under `zospy.analyses.raysandspots`, and no batch ray trace [10]. A `SingleRayTrace` analysis per ray is the *slowest* possible option, because each call is a whole analysis window. Newer ZOS-API releases may add bulk (array) members to the ray-data interfaces. Search the Syntax Help for `IRayTraceNormUnpolData` and look for anything that takes arrays before writing a helper.

### 3.1 Sketch of your own helper (C#)

```csharp
// FastTrace.cs — class library referencing ZOSAPI.dll and ZOSAPI_Interfaces.dll from the
// OpticStudio install folder (Copy Local = False, as the KB article advises for RayTrace.dll [2]).
// Target the same .NET runtime as your OpticStudio — verify. Signatures: verify in Syntax Help.
using ZOSAPI.Tools.RayTrace;
public static class FastTrace {
    // out11 has length 11*n: X,Y,Z,L,M,N,l2,m2,n2,opd,intensity per ray (row-major)
    public static int NormUnpol(IBatchRayTrace tool, int toSurface, OPDMode mode,
        int[] wave, double[] hx, double[] hy, double[] px, double[] py,
        int[] err, int[] vig, double[] out11)
    {
        int n = hx.Length;
        IRayTraceNormUnpolData d = tool.CreateNormUnpol(n, RaysType.Real, toSurface);
        for (int i = 0; i < n; i++) d.AddRay(wave[i], hx[i], hy[i], px[i], py[i], mode);
        tool.RunAndWaitForCompletion();
        d.StartReadingResults();
        int rn, e, v, count = 0;
        double X, Y, Z, L, M, N, l2, m2, n2, opd, I;
        while (d.ReadNextResult(out rn, out e, out v, out X, out Y, out Z,
                                out L, out M, out N, out l2, out m2, out n2, out opd, out I)) {
            int k = rn - 1, b = 11 * k;
            err[k] = e; vig[k] = v;
            out11[b] = X; out11[b+1] = Y; out11[b+2] = Z; out11[b+3] = L; out11[b+4] = M;
            out11[b+5] = N; out11[b+6] = l2; out11[b+7] = m2; out11[b+8] = n2;
            out11[b+9] = opd; out11[b+10] = I;
            count++;
        }
        return count;
    }
}
```

On the Python side, you want the .NET↔numpy copies to be bulk memory copies, not element loops (L05 Stretch 1):

```python
import clr, ctypes, numpy as np
from System import Array, Double, Int32, IntPtr
from System.Runtime.InteropServices import Marshal

def np_to_net_double(a):
    a = np.ascontiguousarray(a, dtype=np.float64)
    net = Array.CreateInstance(Double, a.size)
    Marshal.Copy(IntPtr(a.ctypes.data), net, 0, a.size)       # IntPtr -> double[] overload; verify
    return net

def net_double_to_np(net, n):
    a = np.empty(n, dtype=np.float64)
    Marshal.Copy(net, 0, IntPtr(a.ctypes.data), n)            # double[] -> IntPtr overload; verify
    return a
```

Keep the pure-Python implementation A as the **oracle**. A unit test traces the same 200 random rays with A and with C and asserts equality to 1e-12. Whenever you upgrade OpticStudio, that test tells you whether the helper still works.

## 4. ZPL `RAYTRACE` vs the batch tool

The same ray, both ways:

```
! ZPL (L01): chief ray at Hy = 0.7, wavelength 1, to the image
RAYTRACE 0, 0.7, 0, 0, 1
IF (RAYE() != 0) | (RAYV() != 0) THEN PRINT "bad ray"
y = RAYY(NSUR())
```

```python
r = trace_norm_unpol(oss, hx=0, hy=0.7, px=0, py=0, wave=1)
y = r["Y"][0] if (r["err"][0] == 0 and r["vig"][0] == 0) else np.nan
```

| | ZPL `RAYTRACE` | ZOS-API batch (A) | ZOS-API batch (B/C) |
|---|---|---|---|
| Runs | inside OpticStudio, interpreted | your process ↔ OpticStudio | your process ↔ OpticStudio, compiled loop |
| Per-ray overhead | interpreter step (tens of µs) | 2 interop calls | ~0 (one call per batch) |
| Results | `RAYX()…RAYN()`, `RAYE()`, `RAYV()`, *all surfaces* of the last ray | one target surface per batch | one target surface per batch |
| Data out | `PRINT`/`OUTPUT` to text, then parse | numpy directly | numpy directly |
| Versioning, tests, plots | weak | strong | strong |

One difference matters in practice. A ZPL `RAYTRACE` leaves the ray's data at **every** surface accessible (`RAYY(s)` for any `s`). The batch trace returns **one** target surface. For footprints on several surfaces you run several batches (cheap) or use ZPL. Both honour ray aiming and vignetting factors, and both use the same normalized coordinates. Your Task 2 checks that they agree to machine precision.

## 5. Custom metrics for a 3D-camera receiver

The running example is the Course 04 capstone `designs/capstone.zmx`: f = 8 mm, F/2.4, 850 nm, 3.45 µm pixels, Real Image Height fields up to 5.7 mm, configurations 1–3 = object at 0.6 / 0.8 / 1.2 m, specs S10 (CRA), S12 (Brown–Conrady residual ≤ 0.1 px), S13 (distortion stability ≤ 0.5 px for ±15 µm sensor shift).

### 5.1 Full-field distortion map and Brown–Conrady fit

**Goal:** a table of (object direction → sensor position in pixels) over the *whole rectangular sensor*, a fitted camera model, and the residual map.

**Step 1 — define the field in object space.** Because of the Real Image Height trap (§2.2), work on a scratch copy of the lens (`save_as` into `results/`, never into `designs/`, per L03) and switch the field type to *Object Height* for finite conjugates (*Angle* for infinite ones). The API call is something like `oss.SystemData.Fields.SetFieldType(zp.constants.SystemData.FieldType.ObjectHeight)` (enum member name: *verify*). Then set the maximum field $Y_{max}$ so that the sensor corner (5.5 mm) is covered with margin. Find it by tracing: start from $Y_{max} \approx 1.1 \times 5.7\ \text{mm} \times (d - f)/f$ and check that the chief ray at $H = 1$ lands beyond 5.5 mm. Now the object point of a ray at $(H_x,H_y)$ is $(H_x Y_{max}, H_y Y_{max})$ **by construction**. With radial normalization, a grid $H_x\in[-a,a]$, $H_y\in[-b,b]$ covers a rectangle.

**Step 2 — the pinhole reference.** A calibrated camera model projects through a single centre. Optically, that centre is the entrance pupil. With $T_0$ the object thickness (object → surface 1) and $z_E$ the paraxial entrance-pupil position measured from surface 1 (`ENPP` operand), the distance from object plane to pupil is $d_E = T_0 + z_E$. The ideal normalized coordinates are

$$
x = \frac{X_{obj}}{d_E},\qquad y = \frac{Y_{obj}}{d_E},\qquad r^2 = x^2 + y^2,
$$

and for an infinite conjugate $x = \tan\theta_x$, $y = \tan\theta_y$ (Course 04 L05).

**Step 3 — trace chief rays** $(P_x,P_y) = (0,0)$ for a dense field grid (41×41 is cheap) to the image surface. Convert to pixels: $u = X_{img}/p$, $v = Y_{img}/p$. The image is inverted, so the fitted focal length comes out negative; either accept that or flip the sign of $u, v$ as a real camera readout effectively does.

**Step 4 — fit.** Brown–Conrady with a common focal length $F$ (in px), radial $k_1,k_2$, tangential $p_1,p_2$ and principal point $(c_u,c_v)$:

$$
u = F\left[x(1+k_1r^2+k_2r^4) + 2p_1xy + p_2(r^2+2x^2)\right] + c_u ,
$$
$$
v = F\left[y(1+k_1r^2+k_2r^4) + p_1(r^2+2y^2) + 2p_2xy\right] + c_v .
$$

The model is **linear** in the unknowns $(F, Fk_1, Fk_2, Fp_1, Fp_2, c_u, c_v)$, so stack the $u$ and $v$ equations and solve one `np.linalg.lstsq`. No iterative optimizer is needed. For the nominal, rotationally symmetric design, $p_1=p_2=c_u=c_v=0$ to numerical precision, and their fitted values are a sanity check. They become non-zero in tolerancing Monte Carlo files (Course 06), which is exactly why you want the 2D map rather than one radial curve.

**Step 5 — residuals** $\Delta u, \Delta v$ in px, as a quiver plot and as max/RMS numbers. **Evaluate residuals on a dense grid that is independent of the fit points.** The worked example below shows a 6-point fit that "passes" at its own nodes and fails between them.

**Two definitions of "distortion".** OpticStudio's distortion percentage (`DIST`, the Field Curvature/Distortion plot) compares the real chief-ray height with the *paraxial* height. Your fit compares it with a *fitted* $F$. The fitted $F$ absorbs part of the distortion into the scale, so its "percent distortion" differs from `DIST`. Both are correct. Report which one you use [Kidger §4.4.2.4, pp. 79–82].

### 5.2 Chief-ray angle vs image height

For the chief ray at the image surface with direction cosines $(L, M, N)$ and landing point $(X, Y)$, $\rho = \sqrt{X^2+Y^2}$:

$$
\text{CRA}_{\text{unsigned}} = \arccos |N|,\qquad
\text{CRA}_{\text{signed}} = \operatorname{atan2}\!\left(\frac{XL + YM}{\rho},\ N\right).
$$

The signed form uses the radial component of the direction. It is positive when the ray travels *away* from the axis, which is the usual sensor-datasheet convention (rays hitting outer pixels from the inside). For a tilted or curved image surface, use the returned surface normal $(l_2, m_2, n_2)$ instead of the z-axis: $\cos(\text{AOI}) = |L l_2 + M m_2 + N n_2|$.

Plot CRA against $\rho$ (not against $H$) for several azimuths, and overlay the sensor's CRA curve and acceptance band (capstone: sensor 0° ± 10°, design goal ≤ 8°, limit ≤ 12°). Watch for **non-monotonic** CRA curves. Lenses with a strong rear field element often peak at 70–80 % field and fall towards the corner, and a single "CRA at full field" number hides that peak. Cross-check: `RAID` at the image surface for the chief ray gives the unsigned angle of incidence in degrees and should match $\arccos|N|$ to display precision.

Expected magnitudes come from the paraxial picture (Course 04 L03). For an exit pupil a distance $d_{XP}$ in front of the image, $\tan \text{CRA} \approx \rho/d_{XP}$. With $\rho$ = 5.5 mm, $d_{XP}$ = 39.1 mm gives 8.0° and 25.9 mm gives 12.0°, which are the capstone's goal and limit.

### 5.3 RMS spot radius from your own pupil grid

The definition is simple. For rays $i$ with weights $w_i$ (wavelength weight; also pupil apodization if used), landing at $(x_i, y_i)$:

$$
\bar x = \frac{\sum w_i x_i}{\sum w_i},\quad \bar y = \frac{\sum w_i y_i}{\sum w_i},\qquad
r_{\text{RMS}} = \sqrt{\frac{\sum w_i\left[(x_i-\bar x)^2 + (y_i-\bar y)^2\right]}{\sum w_i}} .
$$

Use $(x_{chief}, y_{chief})$ instead of the centroid for the "chief ray" reference.

The details are where scripts and the GUI disagree:

- **Pupil pattern.** The Standard Spot diagram traces a hexapolar pattern by default, with a "ray density" setting [Geary §7.2.1, pp. 65–66; Kidger §4.2, pp. 65–67]. The `RSCE` operand uses Gaussian quadrature (rings × arms), which converges very fast for smooth aberrations. Your grid is a third sampling of the same integral. All three converge to the same number. At finite sampling they differ by ~0.1–3 %.
- **Square grids are biased at the edge.** A grid whose outermost points sit exactly on $|P|=1$ (`linspace(-1,1,n)`) under-represents the rim, and the rim is where aberrations are largest. A **cell-centred** grid ($P_k = (k+\tfrac12)\cdot 2/n - 1$) converges about twice as fast. The worked example quantifies this.
- **Polychromatic.** The centroid is the weighted centroid over *all* wavelengths. It is not the mean of per-wavelength centroids, unless the weights are equal *and* the ray counts per wavelength are equal.
- **Vignetted rays** are excluded by the mask, as in the GUI. With vignetting factors set, the "full pupil" is already the reduced one (§2.2).
- **Intensity.** For the unpolarized trace, the returned intensity is not a full transmission calculation. Use the polarized trace if you need coating/absorption weighting (Course 03 L08), and verify what the field contains in your version.

The point of computing it yourself is that you can then compute the metric your pipeline cares about: the centroid *position* (for distortion-at-best-focus), the **encircled-energy radius**, or the RMS **in the sensor's pixel grid**.

### 5.4 Depth-dependent image-point shift (multi-configuration)

For structured-light triangulation, the question is: *if the calibration was done at 0.8 m, how far does the image of a point move, relative to the calibrated model, when the point is at 0.6 m or 1.2 m along the same line of sight?*

Paraxially the answer is **zero**. A chief ray through the entrance-pupil centre at object angle $u$ leaves the exit-pupil centre at a fixed angle $u'$, so it lands on the fixed sensor at the same height regardless of object distance. Defocus blurs the spot, but the centre of a pure-defocus blur stays on the chief ray. The non-zero shifts come from real effects:

1. **Pupil aberration.** The real chief ray (through the stop centre, ray aiming on) crosses the axis at a field-dependent point, not at the paraxial entrance pupil. The "projection centre" is therefore smeared along the axis. Points on one line of sight through the *paraxial* pupil are seen along slightly different real chief rays at different depths [Kidger §4.4.2.4.4, p. 81].
2. **Conjugate-dependent aberrations.** Distortion (and coma, which moves the centroid) changes with object distance. Photogrammetrists have modelled this since D. C. Brown's work on close-range calibration (1971), and it is why some calibrations make $k_i$ depth-dependent.
3. **Focus shifts on the image side** (thermal, sensor tilt, S13). Moving the sensor by $\Delta z$ moves every landing point radially by $\Delta z \tan(\text{CRA})$. This is where CRA (§5.2) and distortion stability meet.

**Recipe:** for each configuration $k$ (set config, then trace), place object points at $X = d_{E,k}\,x$, $Y = d_{E,k}\,y$ for a fixed set of normalized directions $(x,y)$. That again needs the Object Height field type, so the field value must change per configuration: put the maximum field in the Multi-Configuration Editor or compute $H$ per configuration. Trace the chief ray and (for coma-sensitive results) a pupil grid to get the centroid. Report $\Delta$ = position(config k) − position(config 2) in px, as a vector map and as max $|\Delta|$ vs field. To *separate* the effects, repeat with the paraxial ray type (§2.3): any shift that remains paraxially means your object placement is wrong.

## 6. Vectorized post-processing

Rule: **trace in one batch, post-process with zero Python loops.** Lay rays out as a regular array (fields × waves × pupil), flatten for tracing, and reshape for analysis:

```python
# pupil grid: cell-centred n x n, keep points inside the unit circle
n = 64
g = (np.arange(n) + 0.5) * 2 / n - 1
PX, PY = np.meshgrid(g, g); inside = PX**2 + PY**2 <= 1
px, py = PX[inside], PY[inside]                                   # (P,)  P = 3228 for n = 64

H = np.array([0, 0.3, 0.5, 0.7, 0.9, 1.0]); W = np.array([1])     # field (Hy), wave numbers
F_, W_, P_ = np.meshgrid(np.arange(H.size), np.arange(W.size), np.arange(px.size), indexing="ij")
r = trace_norm_unpol(oss, hx=0.0, hy=H[F_].ravel(), px=px[P_].ravel(), py=py[P_].ravel(),
                     wave=W[W_].ravel())
shape = (H.size, W.size, px.size)
X, Y = r["X"].reshape(shape), r["Y"].reshape(shape)
ok = ((r["err"] == 0) & (r["vig"] == 0)).reshape(shape)

w = ok * wave_weights[None, :, None]                               # zero weight for bad rays
sw = w.sum(axis=(1, 2))                                            # per field (polychromatic)
cx = (w * np.nan_to_num(X)).sum(axis=(1, 2)) / sw
cy = (w * np.nan_to_num(Y)).sum(axis=(1, 2)) / sw
r2 = (np.nan_to_num(X) - cx[:, None, None])**2 + (np.nan_to_num(Y) - cy[:, None, None])**2
rms = np.sqrt((w * r2).sum(axis=(1, 2)) / sw)                      # per field, lens units
```

Patterns to reuse:
- **Masks as weights** (`w = ok * weights`) instead of boolean indexing, so shapes stay regular. Use `nan_to_num` so NaNs in masked rays cannot poison sums.
- **Irregular groups** (e.g. rays tagged by pixel): `np.bincount(group, weights=...)` or `np.add.at`.
- **Fits**: build design matrices with broadcasting (`np.c_[x, x*r2, x*r2**2]`) and call `lstsq` once.
- **Tidy output** (L05 §4): flatten into a DataFrame with `config, hx, hy, wave, metric, value, unit` plus the sidecar JSON (lens SHA-256, versions, sampling).

## 7. Validation — every custom metric gets a reference

| Your metric | Reference in OpticStudio | Expected agreement |
|---|---|---|
| Chief-ray landing $(X,Y)$ | `REAX`/`REAY` at image surface, same $(H_x,H_y,0,0)$ | identical to ~1e-12 mm (same tracer) |
| Paraxial landing | `RaysType.Paraxial` vs paraxial image height (`PIMH`) at $H=1$ | identical |
| Radial distortion vs paraxial | `DIST` / Field Curvature/Distortion; `DIMX` for the maximum | to displayed digits if you use the paraxial reference |
| 2D distortion map | Grid Distortion analysis (text output) | same points to displayed digits; grid and reference definitions differ — read its text header |
| CRA | `RAID` at the image surface (chief ray) | display precision |
| RMS spot (centroid) | `RSCE` (Gaussian quadrature); Standard Spot RMS | < 0.5 % vs `RSCE` at converged sampling; ~1–3 % vs hexapolar spot |
| Centroid position | `CENX`/`CENY` (check the operand help for sampling arguments) | ~sampling level |
| OPD | `OPDC` at the same pupil point | display precision, after you fix mode/units (§2.4) |
| Depth-dependent shift | `REAY` rows in each configuration (MCE, or `CONF` operand before them) | identical for chief rays |

When a number disagrees, check in this order: field type and normalization → configuration → ray aiming → vignetting factors → wavelength index → reference (centroid/chief/paraxial) → sampling. In practice that order finds the bug almost every time.

## 8. In OpticStudio — practical notes
- Prototype one ray in the GUI first with **Analyze → Rays & Spots → Single Ray Trace** (location varies by version). Same $(H_x,H_y,P_x,P_y)$, and you can read every surface. Your batch result for that ray must match it.
- Keep a scratch merit function with weight-0 `REAY`, `RAID`, `RSCE` rows for 2–3 field points. It is the fastest cross-check while you develop (L04/L05).
- Changing the field type rewrites the meaning of every field point. Do it only on scratch copies. After `SetFieldType`, re-enter the field values and re-check ray aiming.
- The batch tool is a modal tool. If your script dies with it open, the system stays locked for other tools until you close it (or the session). The `try/finally` in §2.3 is not optional.
- Premium vs other editions: the ZOS-API, including batch ray tracing, is available in Professional and Premium. Standalone applications need a licence that allows API use. Your Premium licence covers everything in this lesson.

## Worked example

**(a) Brown–Conrady fit: sparse vs dense validation.** Consider an f = 8 mm lens whose true mapping in normalized coordinates $x=\tan\theta$ is $r = f\,x\,(1 - 0.09x^2 + 0.02x^4 - 0.02x^6)$ (a smooth barrel lens with some 7th-order content; pixel $p$ = 3.45 µm). Six chief rays give:

| θ [°] | $x$ | $r$ [mm] | distortion vs $f\tan\theta$ |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 7 | 0.12278 | 0.98095 | −0.135 % |
| 14 | 0.24933 | 1.98361 | −0.552 % |
| 21 | 0.38386 | 3.03132 | −1.289 % |
| 28 | 0.53171 | 4.15032 | −2.430 % |
| 35 | 0.70021 | 5.36821 | −4.168 % |

Fit $r = F x + (Fk_1)x^3 + (Fk_2)x^5$ by linear least squares on these six points: $F$ = 7.9985 mm (2318.4 px), $k_1$ = −0.0864, $k_2$ = 0.0036. The residuals at the six nodes are at most **0.049 px**, comfortably inside S12 (≤ 0.1 px). Now evaluate the *same* fit on 351 angles from 0 to 35°: the maximum residual is **0.121 px**, which fails S12. Refitting on all 351 points cannot rescue it either: the best $k_1,k_2$ fit then has a maximum residual of 0.149 px, because least squares minimizes RMS, not the maximum. The $k_1$-only fit on six points shows 0.101 px at the nodes. The lesson: a residual reported at the fitting points is optimistic. Validate on an independent dense set, and that is cheap only with batch tracing. (Numbers computed with numpy; reproduce them in Task 3.)

**(b) CRA and distortion stability (S13).** A sensor shift of $\Delta z$ = 15 µm moves the landing point radially by $\Delta z\tan(\text{CRA})$:

| CRA at corner | shift [µm] | shift [px, 3.45 µm] |
|---|---|---|
| 4° | 1.05 | 0.30 |
| 6° | 1.58 | 0.46 |
| 8° | 2.11 | 0.61 |
| 12° | 3.19 | 0.92 |

S13 (≤ 0.5 px) therefore requires CRA ≤ $\arctan(0.5 \times 3.45/15)$ = **6.6°** wherever S13 is evaluated. That is tighter than S10's 8° *goal*. If your capstone met S10 with an 8° corner CRA, it does **not** meet S13 at the corner. This is exactly the kind of cross-spec inconsistency a custom metric exposes. Task 4 makes you check your own design and decide whether to tighten S10 or relax S13.

**(c) Sanity test for your RMS-spot code.** For a perfect lens defocused by $\Delta z$ at image-space F/$N$, the transverse error is linear in pupil radius: $\epsilon = a\rho$ with $a = \Delta z/(2N)$ (small-angle). Over a uniformly filled circular pupil, $\langle\rho^2\rangle = 1/2$, so $r_{RMS} = a/\sqrt2$. For F/2.4 and $\Delta z$ = 27 µm, which is roughly the image-side focus difference between 0.6 m and 0.8 m objects for f = 8 mm since $f^2/592 - f^2/792 = 0.1081 - 0.0808$ mm: $a$ = 5.625 µm and $r_{RMS}$ = **3.98 µm**. Sampling the pupil with a grid gives $r_{RMS}/a$:

| grid $n$ | rays in pupil (cell-centred) | $r_{RMS}/a$ cell-centred | rays (edge-inclusive) | $r_{RMS}/a$ edge-inclusive |
|---|---|---|---|---|
| 8 | 52 | 0.7156 | 32 | 0.6389 |
| 16 | 208 | 0.7185 | 172 | 0.6977 |
| 32 | 812 | 0.7104 | 740 | 0.7002 |
| 64 | 3228 | 0.7083 | 3096 | 0.7047 |
| 128 | 12 892 | 0.7078 | 12 644 | 0.7065 |

The exact value is $1/\sqrt2$ = 0.70711. At $n$ = 64 the cell-centred grid is +0.17 % off, the edge-inclusive one −0.34 %. Use the analytic case as a **unit test with no OpticStudio**: generate $\epsilon = a(P_x,P_y)$, run your RMS function, and assert agreement to within the tabulated sampling error.

## Key takeaways
- The batch pattern is `OpenBatchRayTrace` → `CreateNormUnpol(n, Real, toSurf)` → `AddRay(wave, Hx, Hy, Px, Py, OPDMode)` ×n → `RunAndWaitForCompletion` → `StartReadingResults` → `ReadNextResult` until it returns false → `Close` in `finally`.
- Always mask on error *and* vignette codes. Results come back in the target surface's local frame, with 1-based ray numbers.
- Normalized field coordinates mean what the field type says. With Real Image Height fields, a field grid lands on a perfect grid and hides distortion, so use object-space fields on a scratch copy for mapping studies.
- Per-ray interop calls are the bottleneck, not the trace. Measure, then move the loops into compiled code (Ansys `RayTrace.dll` or your own C# helper) and bulk-copy arrays to numpy.
- Fit calibration models by linear least squares and validate residuals on a dense independent set. Sparse points flatter the model.
- CRA, distortion stability and depth-dependent shift are coupled ($\Delta z\tan$CRA). Custom metrics reveal spec conflicts that single operands hide.
- Every custom metric needs a built-in reference (`REAY`, `RAID`, `DIST`, `RSCE`, `OPDC`, Grid Distortion), checked once per metric and kept as a test.

## Glossary (new terms in this lesson)
| Term | Meaning |
|---|---|
| `IBatchRayTrace` | ZOS-API tool for tracing many rays per call; opened from `system.Tools` |
| `IRayTraceNormUnpolData` | Ray container for normalized, unpolarized rays (`AddRay`, `StartReadingResults`, `ReadNextResult`, `ClearData`) |
| Normalized field $(H_x,H_y)$ | Field coordinates scaled to max field = 1; meaning set by field type and radial/rectangular normalization |
| Normalized pupil $(P_x,P_y)$ | Entrance-pupil coordinates scaled to the pupil edge = 1 (aimed at the stop with ray aiming) |
| Error / vignette code | Per-ray status: 0 = OK; error > 0 missed surface, < 0 TIR; vignette = clipping surface |
| `OPDMode` | Per-ray choice of OPD reference (`None`, `Current`, `CurrentAndChief`) |
| `RayTrace.dll` | Ansys KB C# helper that moves the add/read loops into compiled code |
| Projection centre | The single point a pinhole camera model projects through; optically ≈ entrance pupil |
| Depth-dependent distortion | Change of the image of a fixed line of sight with object distance, caused by pupil aberration and conjugate-dependent aberrations |
| Cell-centred grid | Sampling grid with points at cell centres, not edges; less rim bias |

## References
Books (cited as [Kidger …], [Geary …] in the text):
- [Kidger §4.4.2.4, pp. 79–82] distortion for finite/infinite conjugates; §4.4.2.4.4, p. 81, pupil aberration and defocus. [Kidger Ch. 3, §3.1–3.5, pp. 45–57] real ray tracing. [Kidger §4.2–4.3, pp. 65–70] ray aberration plots and spot diagrams.
- [Geary Ch. 7, §7.1–7.3, pp. 65–76] ray patterns, spot diagrams. [Geary Ch. 15, pp. 167–173] distortion.
- D. C. Brown, "Close-range camera calibration", *Photogrammetric Engineering* 37(8), 1971. The classic source on distance-dependent distortion (bibliographic pointer; no link verified).

Online (numbers in brackets in the text refer to this list):

- [1] ZOS-API Python example 22 (batch ray trace + spot diagram): <https://developer.synopsys.com/docs/zos-api-interface-2025-r2/page_ex22_py.xhtml>; Ansys portal copy: <https://developer.ansys.com/docs/zos-api-interface-2025-r2/_python_standalone_22_seq_spot_diagram_8py-example.xhtml>
- [2] M. Humphreys, "Batch Processing of Ray Trace Data using ZOS-API in MATLAB or Python" (`RayTrace.dll`, interfaces, timing): <https://optics.ansys.com/hc/en-us/articles/42661765866899-Batch-Processing-of-Ray-Trace-Data-using-ZOS-API-in-MATLAB-or-Python>
- [3] Zemax Community, "Getting Raytrace.dll working in Python for SEQ raytracing?" (Python usage of `ReadNormUnpolData`, `ReadNextBlock`): <https://community.zemax.com/got-a-question-7/getting-raytrace-dll-working-in-python-for-seq-raytracing-2769>
- [4] Zemax Community, "ZOS-API: (Python) sequential batch ray trace example": <https://community.zemax.com/zos-api-12/zos-api-python-sequential-batch-ray-trace-example-4564>
- [5] Zemax Community, "Understanding OPDMode in ZOSAPI.Tools.RayTrace": <https://community.zemax.com/got-a-question-7/understanding-opdmode-in-zosapi-tools-raytrace-3012>
- [6] Zemax Community, "Large amount of single ray trace" (batch vs single, DLL status 2025): <https://community.zemax.com/zos-api-12/large-amount-of-single-ray-trace-5733>
- [7] Zemax Community, "RemotingException when running the BatchRayTrace with Python in Interactive Extension" (extension-mode pitfalls): <https://community.zemax.com/zos-api-12/remotingexception-when-running-the-batchraytrace-with-python-in-interactive-extension-1105>
- [8] Batch ray trace template gist (minimal C#-style Python usage, `Enum.Parse` for `OPDMode`): <https://gist.github.com/Omnistic/eed68902207eed664f807a266c5750a0>
- [9] ZOSPy, "Using ZOS-API constants" (`None_`): <https://zospy.readthedocs.io/en/latest/usage/04_constants.html>
- [10] ZOSPy API reference (`raysandspots` wrappers; no batch wrapper listed at time of writing): <https://zospy.readthedocs.io/en/latest/api.html>
- Course cross-references: [Course 04 L03](../../04-machine-vision-camera-lenses/L03-relative-illumination-and-telecentricity/lecture-notes.md) (CRA, exit pupil), [Course 04 L05](../../04-machine-vision-camera-lenses/L05-wide-angle-and-distortion-mappings/lecture-notes.md) (Brown–Conrady), [Course 04 L09](../../04-machine-vision-camera-lenses/L09-3d-vision-optics-scheimpflug-stereo/lecture-notes.md) (triangulation), [Course 04 L10](../../04-machine-vision-camera-lenses/L10-capstone-machine-vision-lens/lecture-notes.md) (specs S10/S12/S13).
