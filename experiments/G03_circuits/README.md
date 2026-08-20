# G03 — circuit unravellings  [blocked by: H1 alive after G01/G02]

Implement the two unravellings of arXiv:2111.02897 as Qiskit circuits:
(1) stochastic-Hamiltonian (random Z-phase kicks per Trotter step — classical
randomness realizes dephasing in expectation over shots; NB each shot is a
trajectory, the SHOT AVERAGE is the channel — proposal sampling wants one
trajectory per proposal, which is exactly one shot: convenient);
(2) collision scheme (ancilla + reset per step).
Validate against `lindblad.proposal_matrix` at n=6 (TV < 1e-3 at realistic
shots). Then Aer with device-calibrated noise: measure effective γ̂ (fit the
proposal-matrix dephasing that best explains shots — reuse E03's T_eff fitting
idea, but for γ) and ask how far native γ̂ sits from γ*. Deliverable:
G03_RESULTS.md + honest ESS/sec at circuit level (shots, latency, resets —
the E02c kill-shot applied to ourselves).
