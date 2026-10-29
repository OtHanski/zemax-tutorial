# L08 — Tasks: Seidel surface contributions, stop shift and aplanatic surfaces

> Work in `work/` inside this lesson folder (e.g. save `work/L08_T3_singlet.zmx`, `work/seidel.py`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~4–5 h

Conventions for all tasks: wavelength d = 0.5876 µm only (unless stated), lens units mm, object at infinity, $n_d$(N-BK7) = 1.5168, $n_d$(N-SF5) = 1.6727 (use the catalogue value OpticStudio shows if it differs in the 4th decimal — your Seidel numbers will then differ in the 4th digit).

## Task 1 — Seidel table by hand: the "wrong-way-round" singlet (pen & paper)
**Goal:** Do one complete Seidel calculation by hand so the formulas become routine.
**Given / specs:** N-BK7 plano-convex lens, **plane side towards the object**: $R_1=\infty$, $R_2=-51.68$ mm, thickness 4 mm, EPD 20 mm, stop on surface 1, semi-field 5°.
**Steps:**
1. Trace the marginal ray ($h_1=10$, $u=0$) and chief ray ($\bar h_1=0$, $\bar u=\tan 5^\circ$). Tabulate $h, u', \bar h, \bar u', A, \bar A, \delta(u/n), \delta(1/n)$ for both surfaces.
2. Compute $H$ and $S_I$–$S_V$ per surface and the sums. Use the $A$-free distortion formula where $A=0$.
3. Compare with the convex-first orientation in the lecture's worked example. Which surface does all the work now, and why does surface 1 contribute nothing to $S_I$, $S_{II}$, $S_{III}$?
4. Convert $S_I$ to $W_{040}$ in waves and to transverse spherical aberration.
**Deliverable:** hand table (photo or typed) in `work/notes.md`.
**Check yourself:** $\Sigma S_I = 0.0861$ mm (about 4× the convex-first value of 0.0218).

<details><summary>Hints / solution sketch</summary>

- Surface 1 ($c=0$): $A_1 = 0$, $u'_1=0$, $\delta(u/n)_1 = 0$ ⇒ $S_I=S_{II}=S_{III}=0$; $S_{IV}=0$ (plane). Distortion via $S_V=-\bar A^3h\,\delta(1/n^2)$ with $\bar A_1=0.087489$, $h=10$, $\delta(1/n^2)=1/1.5168^2-1=-0.56535$: $S_{V,1}=+0.003786$.
- Surface 2: $h_2=10$, $u=0$, $c=-1/51.68=-0.019350$, $n=1.5168\to1$: $A_2 = 1.5168(10)(-0.019350) = -0.293498$; $u'_2 = -h c(n'-n)/n' \Rightarrow u'_2 = -10(-0.019350)(1-1.5168) = -0.1$; $\delta(u/n) = -0.1-0 = -0.1$.
- Chief ray in glass: $\bar u' = 0.087489/1.5168 = 0.057680$, $\bar h_2 = 0.230720$, $\bar A_2 = 1.5168(0.230720\cdot(-0.019350)+0.057680) = 0.080717$. $H = 0.87489$.
- Surface 2: $S_I = -(0.293498)^2(10)(-0.1) = 0.086141$; $S_{II} = -(-0.293498)(0.080717)(10)(-0.1) = -0.023690$; $S_{III} = 0.006515$; $S_{IV} = -H^2 c\,(1-1/1.5168) = 0.005046$; $S_V = (\bar A/A)(S_{III}+S_{IV}) = -0.003180$.
- Sums: $S_I=0.086141$, $S_{II}=-0.023690$, $S_{III}=0.006515$, $S_{IV}=0.005046$, $S_V=0.000606$.
- $W_{040} = 0.086141/8 = 0.010768$ mm $= 18.3\lambda$; TSA $= S_I/(2u') = -0.431$ mm.
- Note $S_{IV}$ is identical in both orientations: Petzval does not care about bending.
</details>

## Task 2 — Write your own Seidel calculator and validate it against Kidger (Python)
**Goal:** A reusable `seidel.py` you will use again in L09–L12.
**Given / specs:** Kidger's Kingslake triplet [Kidger §6.2.7, p. 113]: radii 42.98790, −248.07740, −38.21035, 43.95894, 656.66349, −33.50754; thicknesses 4.0, 10.51018, 2.5, 9.86946, 4.5, (86.48643 to image); indices 1.620408, 1, 1.616589, 1, 1.620408, 1; EPD 22.222 mm (F/4.5, f=100); semi-field 20°.
**Steps:**
1. Implement `trace(c, d, n, h0, u0)` (paraxial $y$–$nu$ trace) and `seidel(...)` returning per-surface $A$, $\bar A$, $\delta(u/n)$ and $S_I$–$S_V$ (use the division-free $S_V$ formula) plus $C_I$, $C_{II}$ if you pass $\delta n$ values.
2. Find the chief ray by tracing two auxiliary rays and combining them so $\bar h=0$ at the stop (see lecture §4).
3. Run with the stop **exactly on surface 4**. Then insert a dummy plane surface 0.958 mm behind surface 4, make it the stop, and run again.
4. Verify the stop-shift equations: compute $k=\Delta(\bar h/h)$ from the two runs (it must be identical at every surface), predict the new $S_{II}$, $S_{III}$, $S_V$ from the old sums and compare.
**Deliverable:** `work/seidel.py`, printed tables for both stop positions.
**Check yourself:** stop on surface 4: $\Sigma = (0.011435,\ 0.010916,\ -0.027285,\ 0.062162,\ -0.060302)$. Stop 0.958 mm behind surface 4: $(0.011435,\ 0.010332,\ -0.028370,\ 0.062162,\ -0.059214)$ — Kidger's printed sums (0.011432, 0.010331, −0.028367, 0.062155, −0.059211) to rounding of his indices. $k=-0.051029$.

<details><summary>Hints / solution sketch</summary>

A compact reference implementation (indices `n[k]` = index *after* surface k, `d[k]` = distance after surface k):

```python
import numpy as np
def trace(c, d, n, h0, u0, n0=1.0):
    N=len(c); h=np.zeros(N); u=np.zeros(N+1); h[0]=h0; u[0]=u0
    for k in range(N):
        nb = n[k-1] if k else n0
        u[k+1] = (nb*u[k] - h[k]*c[k]*(n[k]-nb))/n[k]
        if k < N-1: h[k+1] = h[k] + u[k+1]*d[k]
    return h, u

def seidel(c, d, n, stop, h1, u0, ubar0, n0=1.0):
    c=np.asarray(c,float); n=np.asarray(n,float)
    h,u   = trace(c,d,n,h1,u0,n0)
    ha,ua = trace(c,d,n,0.0,ubar0,n0)     # aux ray a
    hb,ub = trace(c,d,n,1.0,0.0,n0)       # aux ray b
    k = -ha[stop]/hb[stop]
    hc, uc = ha+k*hb, ua+k*ub             # chief ray
    nb = np.r_[n0, n[:-1]]
    A  = nb*(h*c + u[:-1]);  Ab = nb*(hc*c + uc[:-1])
    H  = n0*(uc[0]*h[0] - u[0]*hc[0])
    du = u[1:]/n - u[:-1]/nb
    S1=-A**2*h*du; S2=-A*Ab*h*du; S3=-Ab**2*h*du
    S4=-H**2*c*(1/n-1/nb)
    S5=-Ab**3*h*(1/n**2-1/nb**2) + hc*Ab*(2*h*Ab-hc*A)*c*(1/n-1/nb)
    return dict(A=A,Ab=Ab,H=H,S1=S1,S2=S2,S3=S3,S4=S4,S5=S5,h=h,hbar=hc)
```

Use `c = 0` for plane/dummy surfaces (not `1/1e18` — both work, but 0 is cleaner). Kidger's tabulated chief-ray heights ($\bar h_4=-0.44278$, $\bar u=0.46220$ after surface 4) show that his chief ray crosses the axis $0.44278/0.46220 = 0.958$ mm behind surface 4, which is why you need the dummy stop to reproduce his table exactly.
</details>

## Task 3 — Compare with OpticStudio's Seidel Coefficients (OpticStudio + Python)
**Goal:** Match your numbers to OpticStudio and learn to read its output.
**Given / specs:**
- (a) the convex-first PCX singlet of the lecture worked example ($R_1=51.68$, $R_2=\infty$, 4 mm N-BK7, EPD 20, stop on surface 1, field 0/3.5/5°);
- (b) the cemented doublet $R_1=61.07$, $R_2=-44.17$, $R_3=-128.89$, thicknesses 6.0 mm N-BK7 and 2.5 mm N-SF5, EPD 20, stop on surface 1, field 0/3.5/5°. Put a Marginal Ray Height solve (= 0) on the last thickness.
**Steps:**
1. Enter both lenses (System Explorer: Aperture = Entrance Pupil Diameter 20; Fields = Angle; Wavelengths = F, d, C with d primary).
2. Open **Analyze → Aberrations → Seidel Coefficients**. Identify the paraxial ray data block and the `SPHA S1 … DIST S5 CLA CTR` columns. Compare each surface with your script (use the exact catalogue $n_d$ OpticStudio lists in the Prescription Data).
3. Open the **Seidel Diagram**. Which doublet surface carries the largest $|S_I|$? Which pairs cancel?
4. In the Merit Function Editor add `SPHA` (Surf 0), `COMA` (Surf 0), `ASTI` (Surf 0) and check how their values relate to the $S$ columns (factor 1/8 or 1/2 and division by λ).
5. Switch the field sign (enter −5° as max field). Which Seidel columns change sign?
**Deliverable:** a side-by-side table (script vs OpticStudio) in `work/notes.md`; `work/L08_T3_singlet.zmx`, `work/L08_T3_doublet.zmx`.
**Check yourself:**
- Singlet sums: $S_I=0.021779$, $S_{II}=0.002543$, $S_{III}=0.007540$, $S_{IV}=0.005046$, $S_V=0.000100$ mm; $W_{040}=4.63$ waves.
- Doublet ($f=99.44$ mm, BFL 95.36 mm with the indices above): $S_I=0.002677$, $S_{II}=-0.000451$, $S_{III}=0.007166$, $S_{IV}=0.005594$, $S_V=0.000502$; per surface $S_I = 0.009862,\ -0.031407,\ 0.024221$ — the cemented interface (surface 2) is the strong overcorrecting surface.
- Agreement to 3–4 significant figures (differences come only from index decimals). If $S_{II}$ and $S_V$ have opposite signs to yours, your chief ray goes to the opposite field point.

<details><summary>Hints / solution sketch</summary>

- `SPHA` ≈ $S_I/(8\lambda)$ and `COMA` ≈ $S_{II}/(2\lambda)$, `ASTI` ≈ $S_{III}/(2\lambda)$ in waves at the primary wavelength (singlet: 4.63, 2.16, 6.42 waves). If your version shows different factors, note it — the operand help page for your release is authoritative.
- Only $S_{II}$, $S_V$ (and $C_{II}$) flip with the field sign.
- In the doublet, almost all of the astigmatism (0.0072) survives: the cemented doublet at the stop cannot correct astigmatism — that is exactly the motivation for separated-element designs (L09).
</details>

## Task 4 — Find the coma-free stop position (Python → OpticStudio)
**Goal:** Use the stop-shift equations predictively, as Wollaston did.
**Given / specs:** both orientations of the singlet (Task 1 and Task 3a).
**Steps:**
1. For each orientation compute $k=-S_{II}/S_I$ and the predicted $S_{III}^*$ and $S_V^*$ after the shift.
2. Convert $k=\Delta(\bar h/h)$ into a physical stop position (front stop in air for the plane-first lens; rear stop in air behind the convex-first lens). Check with your script by inserting a dummy stop surface and solving for its distance.
3. In OpticStudio insert the dummy stop at that distance (make it the stop: Surface Properties → Type → "Make Surface Stop"), and confirm in the Seidel Coefficients that $\Sigma S_{II}\approx0$. Look at the Ray Fan at 5°: is the coma asymmetry gone?
4. Explain why, for the plane-first lens, the coma-free position also gives **zero astigmatism**.
**Deliverable:** stop distances, predicted vs. OpticStudio Seidel sums; `work/L08_T4_stopshift.zmx`.
**Check yourself:**
- Plane-first lens: $k=+0.2750$ → stop **31.43 mm in front** of the plane face; then $S_{II}=S_{III}=0$, $S_V=0.00379$.
- Convex-first lens: $k=-0.1168$ → stop **9.14 mm behind** the plane rear face; then $S_{III}=0.00724$, $S_V=-0.00306$.

<details><summary>Hints / solution sketch</summary>

- Plane-first: all of $S_I$–$S_{III}$ come from the single curved surface 2, and for one surface $S_{III}-S_{II}^2/S_I = 0$ identically ($\bar A^2 - (A\bar A)^2/A^2 = 0$). The coma-free stop is where the chief ray passes through the **centre of curvature** of surface 2 ($\bar A_2 = 0$): 51.68 − 4 = 47.68 mm of glass equivalent in front of surface 1, i.e. $47.68/1.5168 = 31.43$ mm of air in front of the plane face. You have rediscovered the concentric ("monocentric") stop.
- $S_{III}^* = S_{III} + 2kS_{II} + k^2S_I$; with $k=-S_{II}/S_I$ this is $S_{III}-S_{II}^2/S_I$.
- Convex-first: $S_{III}^* = 0.007540 - 0.002543^2/0.021779 = 0.007243$.
</details>

## Task 5 — Aplanatic conjugates and the immersion trick (pen & paper + Python)
**Goal:** Prove to yourself that an aplanatic surface is free of spherical aberration to all orders.
**Given / specs:** A single spherical surface from N-BK7 ($n=1.5168$) into air, $R=-10$ mm (centre of curvature to the left), object point inside the glass.
**Steps:**
1. Compute the aplanatic object distance $l$, image distance $l'$, and paraxial magnification $m = n l'/(n' l)$.
2. Write a 15-line exact (real-ray) meridional trace in Python: launch rays from the object point at angles $U = 0.05, 0.2, 0.4, 0.6$ rad, refract with vector Snell's law, and compute where each refracted ray (extended backwards) crosses the axis.
3. Compute $\sin U'/\sin U$ for each ray. What does that say about the NA reduction?
4. (OpticStudio, optional) Model it: Object surface material N-BK7, object thickness $|l|$, one surface $R=-10$, then a paraxial check. Look at the Ray Fan.
**Deliverable:** numbers + script in `work/notes.md`.
**Check yourself:** $l=-16.593$ mm, $l'=-25.168$ mm (virtual image), $m=2.30$; every ray crosses at $-25.168$ mm to 1e-12; $\sin U'/\sin U = 1/n = 0.6593$ for every ray, so NA (in glass, $n\sin U$) → $\sin U'$ is reduced by $n^2=2.30$.

<details><summary>Hints / solution sketch</summary>

$l = R(n+n')/n = -10(2.5168)/1.5168 = -16.593$; $l' = R(n+n')/n' = -25.168$; $m = 1.5168\times25.168/16.593 = 2.30 = n^2$. The ray-independent axis crossing proves zero spherical aberration to all orders; the constant $\sin U'/\sin U$ is the sine condition (zero coma). The surface is the second surface of the classical "hemisphere + meniscus" microscope front group [Kidger §6.5.1].
</details>

## Stretch task(s)
- **Seidel of a mirror.** Use your script with $n'=-1$ on a spherical mirror, $R=-200$ mm, EPD 25 mm, object at infinity, stop at the mirror. Confirm $S_{IV}=-H^2K$ and $S_I = -2h^4c^3 = 2h^4/|R|^3 = 0.006104$ mm (with $h=12.5$, $c=-0.005$), then compare with OpticStudio (Material = MIRROR). (Preview of L12.)
- **Pupil Seidels.** Extend the script to compute $\bar S_I$ (swap marginal and chief data) for the Kidger triplet. Relate a non-zero $\bar S_I$ to the change in distortion when the object comes in from infinity to 1 m (use OpticStudio with Object distance 1000 mm).
- Reproduce Geary's surface-by-surface coma and astigmatism of his convex-plano fused-silica singlet ($n=1.458$; $\Sigma S_{II}=0.001181$ cm, $\Sigma S_{III}=0.002470$ cm) [Geary §13.3, pp. 150–153] with your script — you will need his prescription from Ch. 10 (§10.3). Then try the homework in [Geary §13.6].

## Reflection questions
1. Why can the Seidel coefficients be computed from paraxial rays, which have no aberrations at all?
2. A colleague proposes moving the stop of an F/2 lens to remove its residual astigmatism. Under what condition on the other Seidel sums will that fail?
3. A surface sits exactly in an intermediate image. Which Seidel contributions vanish, which do not, and why might you still move it a little away from the image in practice?
4. In a Seidel Diagram, surface 3 shows $S_I=+0.30$ and surface 4 shows $S_I=-0.29$. What does this suggest about tolerancing and higher-order aberrations?

<details><summary>Answers</summary>

1. Real ray heights differ from paraxial heights by $O(h^3)$, so $y^4$ differs from $h^4$ only at sixth order — the order already neglected. The paraxial rays just provide the geometry ($h$, angles of incidence) at which the fourth-order wavefront is evaluated.
2. Astigmatism is stop-independent when $S_I = S_{II} = 0$. A well-corrected F/2 lens is nearly aplanatic, so moving the stop barely changes $S_{III}$ — the fix must come from the design (bending, spacing, glass).
3. $h=0$ ⇒ $S_I,S_{II},S_{III},C_I,C_{II}=0$; $S_{IV}$ (power) and in general $S_V$ remain. Dust and scratches on a surface at an image are in focus — real field lenses sit slightly away from the image.
4. A big cancelling pair means each surface "works hard": small decentres/tilts or radius errors of either surface unbalance the pair (high sensitivity), and large surface contributions also imply large fifth-order terms. A designer would try to spread the correction over more surfaces.
</details>
