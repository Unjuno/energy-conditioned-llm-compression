# Energy-Conditioned LLM Compression

An exploratory research repository investigating whether **inference-energy selection pressure during training** can reduce structural redundancy and the **number of physically stored LLM parameters**, without materially degrading held-out predictive performance.

日本語：推論エネルギーに対する選択圧を学習過程に導入すると、未知データ性能を保ちながら内部計算と保存パラメータ数を減らせるかを検証します。

> **Status: HYPOTHESIS / NOT VERIFIED.** Existing pilots used an **uncalibrated energy proxy**, did **not measure joules**, and did **not retrain model weights under energy pressure**. Smaller structures were observed, but quality degraded. Do not cite pilot results as evidence of energy savings.

## Research hypotheses

- **H1 — Energy adaptation:** same held-out quality with lower **measured J/generated token**.
- **H2 — Structural compression:** under energy pressure the **physically stored** parameter count decreases; masked or skipped weights do not count as removed.
- **H3 — Representation efficiency:** at matched physical parameter count and training budget, the energy-conditioned model performs at least as well on unseen data.

H1 does **not** imply H2 or H3. Reduced energy from quantization, memory access, or conditional compute may leave stored parameter count unchanged.

## Repository structure

- [Hypotheses and terminology](docs/HYPOTHESIS.md)
- [Prospective experimental protocol](docs/PROTOCOL.md) — proposed, not performed
- [Pilot findings and limitations](docs/PILOT_FINDINGS.md)
- [References](docs/REFERENCES.md)
- `energy_meter/` — Linux CPU-package RAPL meter; errors if unavailable
- `scripts/` — metering probe and result summarizer
- `tests/` — meter unit tests
- `results/` — archived pilot summaries and provenance

## Quick start

Python 3.11+; Linux is needed for RAPL measurements. Packages for **legacy** pilots may require specific wheel builds.

1. `python -m pip install -r requirements.txt`
2. `python -m unittest discover -s tests -v`
3. `python scripts/probe_energy.py`

If the probe prints `no-accessible-meter`, do not label timings, operations or memory traffic as Joules.

## Study status

| Question | Result |
| --- | --- |
| Can a pilot prune physical parameters? | Yes, but held-out quality degraded |
| Did it lower measured inference energy? | **Not measured** |
| Did energy pressure reorganize weights during training? | **Not tested** |
| Does it beat direct parameter pruning at matched quality? | **Not established** |

## Data / safety / licensing

The user-provided source model `8M(2).zip`, raw third-party datasets, model weights and machine-specific logs are **excluded**. Confirm their licenses before redistribution. The repository's own license has not yet been selected.

Research inspiration: energy-constrained neural computation, structured model compression and computer architecture; they are not direct evidence for the central hypothesis.
