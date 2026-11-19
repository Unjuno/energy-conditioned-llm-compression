# Next steps / 初期課題

1. **Measure actual energy.** Identify Linux RAPL access for CPU, supported total energy counters for GPU, or an external power meter; document device boundary, clock, prompt length, dtype, batch, and repetitions. Fail closed when unavailable.
2. **Design trainable structural adaptation.** Permit changes across attention, FFN and embedding while updating the remaining weights. No fixed pruning target.
3. **Preregister a matched-control test.** C = quality only; E = quality plus measured inference energy; P = quality plus physical parameter count. All three receive matched architecture search / training compute budgets.
4. **Keep a held-out evaluation set.** Define non-inferiority margin and thresholds before results.
5. **Publish evidence with explicit provenance.** Separate measured Joules, dimensionless work proxies, latencies, synthetic examples and hypotheses.

## Release guardrails

Public repository: do not commit `8M(2).zip`, checkpoint weights, proprietary training text, secrets, unlicensed artifacts, or full user/machine logs. No software license is granted until one is chosen.

## Minimal acceptance

- [ ] Unit tests pass.
- [ ] An accessible energy sensor measures J and its zone/scope is recorded.
- [ ] Experiments record seed, training budget, hardware, clocks, dtype, batch, input/output lengths.
- [ ] Structural compression is physical (not merely masked).
- [ ] Main held-out evaluation is separate from architecture-selection data.
