# [2026-06] Nemotron Evaluation Records

This small companion repository is a content-minimized index of the local
Nemotron competition research reports. It keeps the shape of the work visible
without rehosting the competition corpus: file provenance, SHA-256 digests,
row counts, field names, and aggregate numeric statistics are included; report
bodies and string values are not.

The local source tree is intentionally not mirrored here. It remains at the
research workspace used to produce the records. Readers who are authorized to
access the NVIDIA Nemotron Model Reasoning Challenge should obtain the source
competition material from the official Kaggle competition page and place it in
their own workspace. This repository does not provide prompt, answer,
completion, trace, test-row, or third-party dataset copies.

## Contents

- `reports/report-index.csv` — 174 local report paths, byte sizes, and hashes.
- `reports/schemas/` — one sidecar per report with format, schema, row count,
  and non-sensitive numeric summaries.
- `reports/summary.json` — aggregate file counts and sizes.
- `tools/build_report_index.py` — reproducible index builder; pass the local
  reports directory with `--root`.

The index is useful for checking whether a local report changed and for
rebuilding a permitted, local-only analysis. It is not a substitute for the
official competition data or for a permission to redistribute it.

## Source and citation

Competition: [NVIDIA Nemotron Model Reasoning Challenge](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge)

Please cite the official competition and the OpenKaggle source repository when
using these records. See `DATA_SOURCES.md` for the boundary and provenance
notes.
