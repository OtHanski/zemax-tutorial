# L03 — Tasks: ZOS-API architecture and Python setup

> This lesson creates the **automation repository** you will use for the rest of the course: `work/zlens/` inside this lesson folder (or a separate repo you link from `work/notes.md` — recommended, since L04–L08 build on it). Commit early and often.
> Estimated time: ~4.5 h

---

## Task 1 — Run the official sample unchanged (OpticStudio + Python)
**Goal:** Separate "environment broken" from "code broken" before writing anything.
**Steps:**
1. Note your OpticStudio version (Help → About) and licence edition in `notes.md`.
2. Install a Python 3.11 or 3.12 (64-bit) interpreter (python.org or `winget`); create a throw-away venv and `pip install pythonnet numpy matplotlib`.
3. Generate the Python *Standalone Application* boilerplate from the Programming tab (location varies by version) or take sample 1 from the ZOS-API sample folder. Run it unchanged.
4. Open the file it saved in OpticStudio GUI and confirm it is the lens the script built.
5. Read the boilerplate class and annotate in `notes.md`: where the registry is read, where the DLLs are loaded, where the licence is checked, what `__del__` does.
**Deliverable:** `notes.md` section "Environment", the generated lens file.
**Check yourself:** the script ends without an exception and the hidden instance disappears from Task Manager afterwards. If it fails on `clr`: pythonnet is missing or 32/64-bit mismatch. If it fails on the licence check: your licence does not allow API use from this machine — talk to your administrator before going further.

## Task 2 — Project skeleton with ZOSPy (Python + git)
**Goal:** The reproducible environment from lecture §5.
**Steps:**
1. Create the layout of lecture §5 (`pyproject.toml`, `src/zlens/`, `scripts/`, `tests/`, `designs/`, `results/`). Use `uv`, `pipenv`, `poetry` or plain venv — but produce a lock file or a fully pinned `requirements.txt`.
2. Dependencies: `zospy`, `numpy`, `pandas`, `matplotlib`, `pytest`. Pin exact versions.
3. `git init`; write `.gitignore` (`.venv/`, `results/`, `__pycache__/`, `*.ZDA`, `bin/`, `obj/`) and `.gitattributes` (`*.zos binary`, `*.zar binary`, and the `.zmx` rule decided in Task 3).
4. Copy (don't move) these designs into `designs/`: the Cooke triplet `../../02-aberrations-classical-design/L09-cooke-triplet/work/L09_T2_triplet.zmx` and, if finished, `../../04-machine-vision-camera-lenses/L10-capstone-machine-vision-lens/work/capstone.zmx`.
**Deliverable:** first commit with the skeleton.
**Check yourself:** a fresh clone + `pip install -r requirements.txt` (or `uv sync`) on another folder reproduces the environment without manual steps.

## Task 3 — .zmx encoding and diffs (git)
**Goal:** Make design changes reviewable.
**Steps:**
1. Find out how your OpticStudio writes `.zmx` files: open one in VS Code (status bar shows encoding), and/or after Task 4 run `zos.get_txtfile_encoding()`.
2. Change one thickness of the triplet in the GUI, save, and run `git diff designs/L09_T2_triplet.zmx`.
3. If git says "Binary files differ", fix it (preference to ANSI, or `.gitattributes` with `working-tree-encoding`/`textconv`) and repeat until the diff shows the single changed `DISZ` line (the thickness keyword in .zmx files).
4. Revert the change (`git checkout -- designs/...`).
**Deliverable:** working `.gitattributes`, a short note on which approach you chose and why.
**Check yourself:** a one-cell change produces a diff of a few lines. Expect also a changed header/date line or similar metadata in some versions — that's normal noise; don't try to suppress it.

## Task 4 — `connect.py`: one door in and out (Python)
**Goal:** A robust connection module with logging, used by every later script.
**Steps:**
1. Write `src/zlens/connect.py` with a context manager:
   ```python
   from contextlib import contextmanager
   from pathlib import Path
   import hashlib, logging, platform, subprocess
   import zospy as zp

   log = logging.getLogger("zlens")

   @contextmanager
   def opticstudio(mode: str = "standalone", lens: Path | None = None):
       zos = zp.ZOS()
       oss = zos.connect(mode)
       try:
           log.info("OpticStudio %s, ZOSPy %s, Python %s", zos.version, zp.__version__, platform.python_version())
           if lens is not None:
               lens = Path(lens).resolve()
               log.info("lens %s sha256 %s", lens, hashlib.sha256(lens.read_bytes()).hexdigest()[:12])
               oss.load(str(lens))
           yield zos, oss
       finally:
           zos.disconnect()
   ```
   (Check `zp.__version__` exists in your ZOSPy version; otherwise use `importlib.metadata.version("zospy")`.)
2. Add a helper `git_describe() -> str` (`git describe --always --dirty`) and log it too.
3. Add a `tool(oss, opener)` context manager that opens a tool and **always** closes it, e.g. `with tool(oss, oss.Tools.OpenLocalOptimization) as opt: ...`.
4. `scripts/smoke.py`: open the triplet, print number of surfaces, EPD/aperture value, number of fields and wavelengths, primary wavelength, and the radius/thickness/material/comment of each surface (properties `Radius`, `Thickness`, `Material`, `Comment` of an LDE row — verify against the Syntax Help), then exit.
5. Run it in standalone mode; then enable Interactive Extension in OpticStudio and run it with `mode="extension"`. Time both (`time.perf_counter`).
**Deliverable:** `connect.py`, `smoke.py`, log output of both runs, timings.
**Check yourself:** the surface table matches the LDE. Standalone start-up typically takes a few to ~20 s (licence check + instance launch); extension connect is faster to start but slower per operation when the GUI updates. After the standalone run no `OpticStudio.exe` remains.

<details><summary>Hints</summary>

- `NumberOfSurfaces` includes object and image surfaces; surface indices run 0…N−1.
- In extension mode, `zos.disconnect()` leaves the GUI open; in standalone mode it closes the hidden instance.
- If the second run in the same Python session fails, you created a second `ZOS()` or connected twice — see the ZOSPy FAQ.
</details>

## Task 5 — Failure drills (Python)
**Goal:** Know what failures look like before they happen at 2 a.m. in a sweep.
**Steps:** provoke and record the error message and recovery for each:
1. Load a non-existent file path; load with a relative path.
2. Open the local optimizer, raise an exception before closing it, catch it, and try to open the optimizer again — with and without your `tool()` context manager.
3. Start two standalone scripts at the same time (two terminals). What does the second one get? (Note: this uses a second instance — only if your licence allows; otherwise just document what the licence manager says.)
4. Kill a running standalone script with Ctrl+C mid-optimization; check Task Manager.
**Deliverable:** table in `notes.md`: failure → symptom → fix.
**Check yourself:** (2) without the context manager the second `Open…` returns `None` or raises because a tool is still open; with it, it works. (4) a zombie `OpticStudio.exe` may remain — kill it, and add a note to your README.

## Stretch task
Write a pure-pythonnet version of `smoke.py` (no ZOSPy) using the condensed boilerplate of lecture §4.1. Compare lines of code and identify two things ZOSPy does for you that you had to do by hand.

## Reflection questions
1. Why is "connect once per process, reuse the instance" faster than "one instance per job", and when would you still restart the instance?
2. Which parts of your future automation code can be unit-tested without OpticStudio? Give three examples.
3. Why should scripts never write into `designs/`?
4. A colleague sends a 2023 forum snippet using `zos.connect_as_standalone()`. What do you check first?

<details><summary>Answers</summary>

1. Start-up (instance launch, licence check, catalogue loading) is paid once instead of per job. Restart deliberately after many jobs if memory grows, after a crash, or when you need a clean state (e.g. different catalogue/preferences).
2. Spec-checking logic (PASS/FAIL with margins), distortion fitting (Brown–Conrady), statistics on Monte Carlo results, report generation from saved CSVs, unit conversions, filter-shift formulas — anything that takes numbers in and returns numbers/text.
3. Inputs must stay immutable for reproducibility: a report must be regenerable from a git commit; writing into `designs/` makes runs order-dependent and can silently destroy the reference design.
4. The ZOSPy version it was written for (API changed at 2.0), the OpticStudio version, and the current docs' equivalent (`zp.ZOS().connect("standalone")`).
</details>
