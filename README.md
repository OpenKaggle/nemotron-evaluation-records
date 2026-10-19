# [2026-06] Nemotron Evaluation Records

This small companion repository is a content-minimized index of the local
Nemotron competition research reports. It keeps the shape of the work visible
without rehosting the competition corpus: file provenance, SHA-256 digests,
row counts, field names, and aggregate numeric statistics are included. Report
bodies are not stored in this git tree: the publishable subset is distributed as
a versioned release asset (see `Releases -> report-bodies-2026-10-18`, described
below).

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

## Report bodies (release asset)

`Releases -> report-bodies-2026-10-18` carries **82 of the 174** report bodies
as sanitized first-party text (813,487 bytes), with `MANIFEST.tsv`,
`SHA256SUMS`, `NOTICE.md` and `PROVENANCE.yml` inside the archive. Every file
keeps its original relative path, so it can be matched line for line against
`reports/report-index.csv`. The manifest also records the digest of each
untouched local original.

The other **92** reports stay local, by lane: 58 hold competition row-level
content (prompts, answers, completions, per-row trace text, row identifiers,
`hard_tail_*` row tables, the 9,500-record `solver_eval.json`), 5 derive from a
third party's label file, and 29 are third-party notebook or dataset mirrors
that are linked at their canonical upstream rather than copied. See
`DATA_SOURCES.md` for the boundary.

The index is useful for checking whether a local report changed and for
rebuilding a permitted, local-only analysis. It is not a substitute for the
official competition data or for a permission to redistribute it.

## Source and citation

Competition: [NVIDIA Nemotron Model Reasoning Challenge](https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge)

Please cite the official competition and the OpenKaggle source repository when
using these records. See `DATA_SOURCES.md` for the boundary and provenance
notes.
