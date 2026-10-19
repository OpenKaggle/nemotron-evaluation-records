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

### Report bodies release

`OpenKaggle/nemotron-evaluation-records` publishes report bodies only as a
release asset, never as repository content. Release `report-bodies-2026-10-18`
publishes 82 of the 174 reports (lane L3: first-party audit, summary and prose
artifacts) and leaves 92 unpublished: 58 with competition row-level content
(prompt, answer, completion, per-row trace text, row identifiers, `hard_tail_*`
row tables, `solver_eval.json`), 5 derived from a third party's `valid_labels`
file, and 29 third-party notebook/dataset mirrors that stay link-only at their
canonical upstream.

In the 27 bodies prepared for that release, row identifiers (`id`,
`example_ids`), worst-token text and worst-token context fragments were removed
outright, not replaced by digests; token ids, counts, quantiles and log-probability
statistics are retained. The 55 bodies reused from
`OpenKaggle/nemotron-reasoning-research` (`reports/sanitized-evidence-2026-09-28`)
keep that edition's convention, in which such values appear as
`{ "length": N, "sha256": ... }` objects; the archive's `PROVENANCE.yml`
records the split, and the parent project tracks a strict purge of those digests
as follow-up work.

`reports/report-index.csv` is an inventory of the local report files. Each
schema sidecar records the original relative report name and its digest, but
does not reproduce the report body. Numeric aggregates are retained only when
their field name is not a content-bearing or identifier-like field.

The source-only research code and the previously released sanitized evidence
are maintained in
[`OpenKaggle/nemotron-reasoning-research`](https://github.com/OpenKaggle/nemotron-reasoning-research).
The large first-party model artifact and compact override publications are
linked from that repository and have separate Kaggle dataset cards.
