# Data sources and release boundary

The source material was produced during local research on the NVIDIA Nemotron
Model Reasoning Challenge. The official competition page is the authority for
rules, data access, and permitted uses:

<https://www.kaggle.com/competitions/nvidia-nemotron-model-reasoning-challenge>

This repository publishes derived metadata only. It does not distribute:

- official competition rows, labels, test/holdout material, or event streams;
- prompt, answer, completion, or trace text;
- copied third-party notebooks, datasets, weights, or adapters; or
- machine-local absolute paths or credentials.

`reports/report-index.csv` is an inventory of the local report files. Each
schema sidecar records the original relative report name and its digest, but
does not reproduce the report body. Numeric aggregates are retained only when
their field name is not a content-bearing or identifier-like field.

The source-only research code and the previously released sanitized evidence
are maintained in
[`OpenKaggle/nemotron-reasoning-research`](https://github.com/OpenKaggle/nemotron-reasoning-research).
The large first-party model artifact and compact override publications are
linked from that repository and have separate Kaggle dataset cards.
