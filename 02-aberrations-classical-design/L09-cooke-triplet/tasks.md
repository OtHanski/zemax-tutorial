# L09 — Tasks: The Cooke triplet

> Work in `work/` inside this lesson folder (e.g. save `work/L09_T2_triplet.zmx`). Commit your designs and a short `work/notes.md` with answers.
> Estimated time: ~6 h

Common specification for Tasks 2–4: **f = 50 mm, F/4 (EPD 12.5 mm), semi-field 20° (fields 0°, 14°, 20°), wavelengths F, d, C (d primary), object at infinity, SCHOTT N-SK16 / F2 / N-SK16.**

## Task 1 — Thin-lens predesign solver (Python)
**Goal:** Solve the four shape-independent conditions and see the family of solutions.
**Given / specs:** N-SK16 $n_d=1.62041$, $V_d=60.32$; F2 $n_d=1.62004$, $V_d=36.37$; $f=50$ mm; stop at lens 2.
**Steps:**
1. Write `trace_thin(K1,K2,K3,d1,d2)` returning $h_1,h_2,h_3$, final $u'$ and the chief-ray heights $\bar h_1=-d_1\bar u$, $\bar h_3=d_2\bar u$ (stop at lens 2).
2. Use `scipy.optimize.fsolve` with unknowns $(K_1,K_2,K_3,d_2)$ for given $d_1$ and Petzval target $Pf$, enforcing: $K=1/50$, $\sum K_i/n_i = Pf\cdot K$, $\sum h_i^2K_i/V_i=0$, $\sum h_i\bar h_iK_i/V_i=0$.
3. Tabulate solutions for $Pf\in\{0.30,0.35,0.40\}$ and $d_1\in\{4,6,8,10\}$ mm. Then add $d_1=d_2$ as a fifth equation and solve for the symmetric-spacing case.
4. Plot $f_1$, $f_2$, $f_3$ vs. $d_1$ for $Pf=0.35$. What happens to the power balance when $d_1$ is small or large?
**Deliverable:** `work/triplet_predesign.py`, table + plot.
**Check yourself:** symmetric spacing, $Pf=0.40$: $f_1=29.57$, $f_2=-16.95$, $f_3=26.20$ mm, $d=5.70$ mm; $Pf=0.35$: $f_1=28.29$, $f_2=-15.61$, $f_3=24.95$, $d=5.91$. Non-symmetric example $Pf=0.35$, $d_1=4$: $d_2=11.80$, $f_1=18.58$, $f_2=-15.08$, $f_3=41.88$.

<details><summary>Hints / solution sketch</summary>

```python
import numpy as np
from scipy.optimize import fsolve
nA,VA,nB,VB = 1.62041,60.32,1.62004,36.37
K=1/50
def rays(K1,K2,K3,d1,d2):
    h1=1; u1=-K1; h2=h1+d1*u1; u2=u1-h2*K2; h3=h2+d2*u2; u3=u2-h3*K3
    hb1,hb3 = -d1*1.0, d2*1.0          # chief slope 1 in gap 1; lens 2 at stop
    return (h1,h2,h3),u3,(hb1,0,hb3)
def eqs(x,d1,Pt):
    K1,K2,K3,d2=x; (h,u3,hb)=rays(K1,K2,K3,d1,d2)
    Ks=(K1,K2,K3); ns=(nA,nB,nA); Vs=(VA,VB,VA)
    return [(-u3-K)/K, (sum(k/n for k,n in zip(Ks,ns))-Pt*K)/K,
            sum(hi*hi*k/V for hi,k,V in zip(h,Ks,Vs))/K,
            sum(hi*b*k/V for hi,b,k,V in zip(h,hb,Ks,Vs))/K]
x=fsolve(eqs,[2.5*K,-5*K,2.5*K,6],args=(6,0.35)); print(1/x[:3],x[3])
```
Small $d_1$ forces a weak rear lens and a long $d_2$ (front two lenses merge into a "Petzval-like" pair, cf. Kidger Fig. 10.6); large $d_1$ does the opposite. The near-symmetric middle is where coma, distortion and lateral colour will be easiest to correct.
</details>

## Task 2 — Build and optimize the triplet (OpticStudio)
**Goal:** Turn the predesign into an optimized lens and understand each optimization stage.
**Given / specs:** the common specification; starting prescription from the lecture worked example (R = 18.34/∞, −21.01/21.01, ∞/−16.25; thicknesses 3.0, 3.6, 1.2, 1.0, (stop), 2.6, 3.0; paraxial image distance via Marginal Ray Height solve = 0).
**Steps:**
1. Enter the lens; check EFL ≈ 50.8 mm and the Seidel Diagram (expect +/−/+ pattern per element for $S_I$ and $S_{IV}$).
2. Variables: six radii, air spaces 2, 4, 5 (before/after stop separately); last thickness: leave the solve, or make it variable for best focus.
3. Optimization Wizard: RMS spot radius, centroid reference, Gaussian quadrature 3 rings × 6 arms; glass boundary min centre 1.0, min edge 1.0 mm; air min centre 0.5, min edge 0.5 mm. Add `EFFL` target 50 (weight 1) above the DMFS line.
4. Run local optimization (DLS). Record merit function, RMS spot at 0/14/20°.
5. Switch to RMS wavefront (centroid) and re-optimize. Compare focus position and spot sizes (connect to lecture §5).
6. Compare your radii with Kidger's SK16/F6 design (18.609/460.967, −29.934/18.605, 67.594/−22.162).
**Deliverable:** `work/L09_T2_triplet.zmx`; table of RMS spot/RMS wavefront per field after each stage; Layout, Ray Fan, Field Curvature/Distortion, FFT MTF (to 80 cy/mm) screenshots described in `notes.md`.
**Check yourself:** RMS spot radii of roughly 5–15 µm on axis and 10–30 µm at 20°, distortion below ~1–2%, polychromatic MTF at 30 cy/mm around 0.5–0.7 on axis dropping at the field edge. The optimized form should look like Kidger Fig. 10.2: meniscus-ish front positive, near equi-concave negative, rear positive with stronger rear curvature.

<details><summary>Hints / solution sketch</summary>

- If the merit function stalls with a large astigmatic field at 20°, check the field weights (raise the 14° field) — triplets are typically balanced so the tangential and sagittal fields cross around 0.7–0.85 of full field [Kidger §6.9.4].
- If the negative lens gets very thin or touches the stop, your boundary constraints are not active (they must be *above* the DMFS line in Optimization Wizard output or use `MNCA`/`MNCG`/`MNEG`).
- Expect the final Seidel sums to be small but not zero: $S_{III}$ negative, $S_{IV}$ positive, $|S_I|$ and $|S_{II}|$ small — exactly the pattern of Kidger's table on p. 203.
</details>

## Task 3 — Glass experiment: the central flint (OpticStudio + analysis)
**Goal:** Reproduce Kidger's §10.3 conclusions with your own lens.
**Given / specs:** your optimized lens from Task 2.
**Steps:**
1. Save copies; replace F2 by (a) a lower-index flint, e.g. SCHOTT N-LF5 or LF5 ($n_d\approx1.58$), and (b) a higher-index flint, e.g. N-SF5 ($n_d=1.673$) or SF2. (Use whatever exists in your SCHOTT catalog version; note the exact names.)
2. Re-optimize each with the same merit function.
3. Compare merit function, RMS spot, axial colour (Chromatic Focal Shift), and the element powers/shapes.
4. Optionally make the flint a *Substitute* glass, restrict the catalog, and run **Hammer** for 5–10 minutes. Which glass does it pick?
**Deliverable:** comparison table and 3–5 sentences of interpretation in `notes.md`.
**Check yourself:** low-index flint → asymmetric layout, front two elements moving together, more higher-order spherical/coma; high-index flint → weaker negative lens, insufficient negative $S_I$, worse performance [Kidger Figs. 10.6–10.9]. Flints with $n_d$ close to the crown's usually win.

<details><summary>Hints / solution sketch</summary>

Read the Seidel Diagram before and after: in case (b) the negative lens's $S_I$ bar shrinks while the positives' bars do not, so the sum stays positive. Explain this in terms of $S_I\propto$ curvature³: a higher-index negative of the *same power* needs weaker curvatures, hence less (negative) spherical.
</details>

## Task 4 — Deliberate vignetting and relative illumination (OpticStudio)
**Goal:** Learn the vignetting workflow and its trade-offs.
**Given / specs:** Task 2 lens.
**Steps:**
1. Look at the **Footprint Diagram** on surfaces 1 and 7 at 20° with automatic semi-diameters. Note the largest semi-diameters.
2. Fix all clear semi-diameters to 1.05× the *axial* beam footprint (round up to 0.1 mm). Re-run the spot diagram: rays are now clipped (look for the vignetting % in the spot diagram text).
3. In the Field Data Editor press **Set Vignetting**. Read VDY and VCY for 14° and 20°; convert VCY to "oblique beam height as % of axial" ($1-VCY$).
4. Re-optimize (keep apertures fixed), Set Vignetting again, repeat until stable.
5. Plot **Relative Illumination**. Compare with $\cos^4 20^\circ$ and with Kidger's "~60% beam width, ~40% corner illumination".
6. Compare RMS spot and MTF at 20° with the unvignetted Task 2 design.
**Deliverable:** `work/L09_T4_vignetted.zmx`; table of VDY, VCY, relative illumination and RMS spot per field.
**Check yourself:** $\cos^4 20^\circ = 0.780$; with a 60% tangential beam width the corner illumination falls to roughly 0.6 × 0.78 ≈ 0.47 (OpticStudio's value includes pupil distortion, so expect 0.4–0.6). Off-axis RMS spot and tangential MTF usually *improve* when vignetted.

<details><summary>Hints / solution sketch</summary>

- $P_y' = VDY + P_y(1-VCY)$: a VCY of 0.4 means the tangential beam is 60% of full height; VDY shifts the surviving beam centre (typically negative or positive depending on which rim is clipped more).
- Always re-run Set Vignetting after re-optimizing; stale factors let the optimizer use rays that your fixed apertures would block.
</details>

## Task 5 — Image compactness by hand (pen & paper)
**Goal:** Connect the RMS spot to wavefront coefficients.
**Given / specs:** an F/4 lens with $W_{040} = 1$ wave at 0.5876 µm, nothing else.
**Steps:**
1. Derive $\langle\varepsilon^2\rangle$ for $W=W_{020}\rho^2+W_{040}\rho^4$ (lecture §5) and minimize over $W_{020}$.
2. Compute the minimum RMS spot radius and the focus shift from the paraxial focus.
3. Compute the focus shift for minimum *wavefront* RMS ($W_{020}=-W_{040}$) and compare.
**Deliverable:** derivation in `notes.md`.
**Check yourself:** $\sigma_{\min}=\tfrac43\cdot4\cdot0.5876 = 3.13$ µm; spot-optimal focus shift $\tfrac{32}{3}\cdot16\cdot0.5876 = 100.3$ µm; wavefront-optimal focus shift $8\cdot16\cdot0.5876 = 75.2$ µm (both towards the lens for undercorrected spherical).

<details><summary>Hints / solution sketch</summary>

$\langle\varepsilon^2\rangle = 4F^2\cdot 2\int_0^1(2W_{20}\rho+4W_{40}\rho^3)^2\rho\,d\rho = 4F^2[2W_{20}^2+\tfrac{16}{3}W_{20}W_{40}+4W_{40}^2]$. Setting the derivative to zero: $W_{20}=-\tfrac43W_{40}$, giving $\langle\varepsilon^2\rangle = 4F^2\cdot\tfrac49W_{40}^2$. A Monte-Carlo check in numpy reproduces 3.13 µm. Defocus $\delta z = -8F^2W_{020}$.
</details>

## Stretch task(s)
- **Tessar conversion:** split the rear N-SK16 element of your triplet into a cemented N-SK16/F2-type doublet (start with a flat cemented surface), re-optimize and quantify the gain [Geary §30.5].
- **Geary's route:** do [Geary Homework 30.9 #2] (10-inch F/5 triplet via a Celor rear half, SK16/F4), using the modern equivalent of *Tools > Make Focal* (the scale/"Make Focal Length" tool in the Lens Data Editor tools; location varies by version).
- **Patent check:** look up H. D. Taylor's US 568,053 on Google Patents and compare its proportions with your design.

## Reflection questions
1. Why does bending the central (stop) element change only spherical aberration and coma, to third order?
2. Why is a flat Petzval surface ($P=0$) not the goal of triplet design?
3. Your triplet's tangential MTF at 20° improved after you added vignetting. Is that "free"? What did you pay?
4. If your camera must operate at 850 nm only, which of the four predesign equations disappear, and what would you do with the freed degrees of freedom?

<details><summary>Answers</summary>

1. At the stop $\bar h=0$, so $\bar A = n\bar u$ at both surfaces of a thin lens there, independent of the curvatures. Thin-lens theory then gives, for a lens at the stop, $S_{III}=H^2K$ and $S_V=0$ — functions of power only — while $S_I$ and $S_{II}$ still depend on the bending (Kidger §7.2). So bending the stop element changes only $S_I$ and $S_{II}$.
2. Zero Petzval needs much stronger powers; surface contributions and higher-order aberrations grow. A residual Petzval balanced by negative astigmatism gives better overall field performance.
3. You paid in illumination (corner signal and SNR fall) and in effective aperture at the field edge (lower diffraction cut-off in the tangential direction). For a 3D camera the SNR cost often dominates.
4. Both colour equations vanish (monochromatic); the two freed variables can be used for higher-order correction, a shorter length, lower sensitivity, or cheaper glass (e.g. one glass type for all three elements — but then Petzval control relies on spacing alone).
</details>
