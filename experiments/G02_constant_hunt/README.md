# G02 — the constant hunt (H2)  [blocked by: G01 peak]

Locate γ* per target (refined scan around G01's peak) and test γ*/Δ invariance
for the three Δ definitions in `hamiltonians.py` (mixer strength, median edge
|ΔE|, spectral width). Targets: `IsingTarget.e01_chain`, `.sk` (frustrated —
ENAQT logic predicts the strongest effect here), `.rfim_chain`; sizes 6–10;
T ∈ {0.1, 0.3, 1.0}. Pre-registered tolerance: γ*/Δ drift ≤ 10× across cells
where H1 holds, else H2 is dead. Deliverable: G02_RESULTS.md + one figure
(γ*/Δ vs target/size/T for each Δ definition).
