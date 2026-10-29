# L04 — Tasks: Field Curvature, the Petzval Sum and Field Flatteners

> Work in `work/` inside this lesson folder (e.g. save `work/L04_T2_flattener.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4 h

## Task 1 — Petzval bookkeeping (pen & paper + Python)
**Goal:** Get fluent with $P = \sum K_i/n_i$ and the depth-of-focus budget.

**Steps / questions:**
1. Compute $P$ and $R_P$ for: (a) a thin N-BK7 lens, $f = 50$ mm; (b) the same power split into two thin N-BK7 lenses in contact; (c) a thin N-LASF44 lens ($n_d = 1.8042$), $f = 50$ mm; (d) Kidger's index-contrast pair $K_1 = 4$, $n_1 = 1.8$; $K_2 = -3$, $n_2 = 1.5$ (arbitrary units).
2. Two thin N-BK7 lenses $+K_1$ and $-K_1$ separated by $d = 20$ mm must give $f = 100$ mm. Find $f_1$. What is $P$? Which lens should come first if you want the shortest total track?
3. A 2/3" sensor (half-diagonal 5.5 mm) at 940 nm with a 12 mm, F/2.4 lens. Compute the diffraction depth of focus $\pm2\lambda N^2$ and the maximum $|P|$ (pure Petzval field, no astigmatism) for the image to stay within it at the corner. Express it as $|P|f$.

**Deliverable:** answers in `notes.md` (Python optional).

<details><summary>Solution</summary>

1. (a) $P = 0.02/1.5168 = 0.013186$ mm⁻¹, $R_P = -75.84$ mm. (b) unchanged — Petzval depends only on total power/indices of lenses in contact. (c) $P = 0.02/1.8042 = 0.011085$, $R_P = -90.21$ mm (16% flatter). (d) $P = 4/1.8 - 3/1.5 = 0.222$ vs $1/1.8 = 0.556$ for a single $n=1.8$ lens of power 1.
2. $K = dK_1^2 = 0.01$ → $K_1 = \sqrt{0.01/20} = 0.02236$ mm⁻¹, $f_1 = 44.72$ mm; $P = 0$. Negative lens first gives a retrofocus (long back focus, longer track); positive first gives a telephoto-like compact layout with total track shorter than $f$ — compute both BFLs as a check: positive first: BFL = $(1 - dK_1)/K$ = (1 − 0.4472)/0.01 = 55.3 mm, track 75.3 mm; negative first: BFL = $(1 + dK_1)/K$ = 144.7 mm, track 164.7 mm.
3. $\Delta z = \pm2(0.94)(2.4^2) = \pm10.8$ µm; $|P| < 2\Delta z/h'^2 = 0.0217/30.25 = 7.2\times10^{-4}$ mm⁻¹; $|P|f < 0.0086$ (vs 0.66 for a singlet).
</details>

## Task 2 — Field curves of a singlet, then flatten them (OpticStudio)
**Goal:** Compare Seidel, Coddington and OpticStudio's Field Curvature plot; build a field flattener.

**Given / specs:** your best-form singlet from L02 (`../L02-spherical-aberration-and-bending/work/L02_T2_bending.zmx`, R1 = 59.41, R2 = −397.1 mm, 4 mm N-BK7, stop on surface 1). Change to EPD 10 mm (F/10), fields 0°, 5°, 7°, 10°, λ = 0.5876 µm, image at paraxial focus.

**Steps:**
1. Open **Field Curvature/Distortion**. Read the T and S positions at 10°. Record the **Petzval radius** from the Seidel Coefficients header and the FCUR sum.
2. Predict the S, T, P positions from the Seidel sums ($\delta z = -(\ldots)/(2u'^2)$) and compare.
3. Insert an N-BK7 plano-concave **field flattener**, 2 mm thick, its first surface 5 mm in front of the original paraxial focus. Start with $f_{ff} \approx -100$ mm (R ≈ −51.7 mm on the side facing the lens, plane on the image side). Re-solve the image distance (marginal-ray height solve) and keep the system EFL free.
4. Optimise the flattener radius with PETC (target 0) or, better, with the default merit function (RMS spot, 4 fields) plus the singlet's R1 and the stop position (add a dummy stop surface in front, as in L03) as variables.
5. Compare before/after: Field Curvature plot, RMS spot at 10°, **Distortion** at 10°, and (adding F and C wavelengths) the **Lateral Color** plot.
6. Finally, delete the flattener, and instead make the image surface radius a variable (curved detector). What radius does the optimiser choose, and how does it compare with $R_P$ and the medial-surface radius?

**Deliverable:** `work/L04_T2_flattener.zmx`, `work/L04_T2_curvedimage.zmx`, table of before/after values.

**Check yourself:** At 10° from the paraxial plane, OpticStudio's Field Curvature plot should show S ≈ −2.5 mm and T ≈ −5.3 mm (my Coddington computation for this lens: −2.47 and −5.34 mm; Seidel: about −2.5 and −5.6 mm). Petzval radius ≈ −152 mm. After flattening, the Petzval sum is near zero and the remaining field is astigmatic (T and S symmetric about the image only if you also shifted the stop); distortion and lateral colour grow. The curved-image optimum lies between the S and T surfaces (≈ medial).

<details><summary>Hints</summary>

- The Field Curvature plot is relative to the **paraxial** image plane (Geary §29.9). If you move the image surface away from paraxial focus the plot does not follow.
- If your Field Curvature numbers differ from mine by a few %, check the EFL (thick-lens EFL here is ≈ 100.3 mm, so $u' = -0.0499$).
</details>

## Task 3 — Coddington trace in Python (Python)
**Goal:** Reproduce OpticStudio's Field Curvature curve from first principles.

**Steps:**
1. Write a meridional real-ray tracer (you have one from Course 01 L06, or adapt the snippet below) for the chief ray of the Task 2 singlet (stop at surface 1, ray through the vertex of surface 1 at angle $U$).
2. At each surface compute $\cos I$, $\cos I'$ and apply the Coddington equations (lecture §3), transferring $s$ and $t$ along the chief ray between surfaces ($s \leftarrow s - L$, with $L$ the path length between the two hit points).
3. Convert the final $s'$, $t'$ (along the ray) to axial positions relative to the paraxial focus and plot vs field angle 0–10°. Overlay the OpticStudio Field Curvature data (copy from the analysis *Text* tab).

**Check yourself:** S/T at 5°: −0.62/−1.36 mm; at 7°: −1.22/−2.65 mm; at 10°: −2.47/−5.34 mm (relative to paraxial focus, negative = toward the lens).

<details><summary>Snippet</summary>

```python
# at each surface: unit normal N at the hit point (sphere: N = (-c*y, 1-c*z)), direction d
cosI = d @ N; mu = n0/n1
cosIp = np.sqrt(1 - mu**2*(1 - cosI**2))
d_new = mu*d + (cosIp - mu*cosI)*N
obl = (n1*cosIp - n0*cosI)*c          # oblique power
s = n1/(obl + n0/s)                    # sagittal (s = inf for object at infinity)
t = n1*cosIp**2/(obl + n0*cosI**2/t)   # tangential
```
</details>

## Task 4 — Choosing the astigmatism balance (analysis)
**Given:** a lens with $S_{IV} = 0.004$ mm, $u' = -0.1$, image in air. You can tune $S_{III}$ (e.g. by stop position).
1. Compute $\delta z_P$, and $\delta z_S$, $\delta z_T$ for $S_{III} = 0$, $-S_{IV}/3$, $-S_{IV}/2$, $-S_{IV}$.
2. A structured-light projector images vertical stripes across a wide horizontal field. For a field point at the far left/right edge of the field, which image surface (S or T) determines the sharpness of the stripe edges?

<details><summary>Solution</summary>

$2u'^2 = 0.02$. $\delta z_P = -0.2$ mm. $S_{III}=0$: S = T = −0.2 mm. $S_{III} = -0.001333$: S = −0.133, T = 0 mm. $S_{III} = -0.002$: S = −0.1, T = +0.1 mm. $S_{III} = -0.004$: S = 0, T = +0.4 mm.
2. For a field point on the horizontal axis the meridional (tangential) plane is horizontal. A vertical stripe's intensity profile varies horizontally, so its edge sharpness is set by the tangential focus (the T line focus is perpendicular to the meridional plane, i.e. parallel to the stripes). So the **T surface** matters there. Points at the top/bottom of the field would be governed by the S surface for the same stripes — in a 2D field you usually choose the medial balance and check sagittal and tangential MTF separately.
</details>

## Stretch task
Take the Cooke triplet from L01 (`../L01-wavefront-and-transverse-aberrations/work/L01_T2_kidger_triplet.zmx`). From its Seidel report, compute $P$ by surface and identify which element cancels the Petzval sum of the other two. Then open its Field Curvature plot: do S and T cross? At what fraction of the field? Relate this to Kidger §6.9.4's comment on fifth-order balancing.

## Reflection questions
1. Why can't an aspheric surface change the Petzval sum?
2. A thick meniscus with equal radii has zero Petzval contribution but positive power. Where does the power come from?
3. Why does OpticStudio's Field Curvature plot sometimes look excellent for a lens that has poor off-axis spots?
4. Why do mobile-phone and machine-vision lenses so often end with a strongly curved, "gull-wing" aspheric element near the sensor?

<details><summary>Answers</summary>

1. Petzval curvature depends only on the paraxial (vertex) curvature and the indices; an asphere's higher-order terms don't change the vertex curvature. (An asphere can change *astigmatism* if it's away from the stop, which changes the T/S surfaces, but not $P$.)
2. From the separation: the two surfaces have equal and opposite surface powers, but the marginal ray height differs at the two surfaces, so the net power $(n-1)^2dc^2/n$ arises from the thickness — the same mechanism as two separated thin lenses of opposite power.
3. It traces only infinitesimally narrow beams around the chief ray: aperture-dependent off-axis aberrations (coma, oblique spherical) don't show up.
4. It sits where the marginal ray is low and the chief ray high: it acts as a field flattener (Petzval correction), and its aspheric profile corrects distortion and controls the chief-ray angle on the sensor (Course 04 L03).
</details>
