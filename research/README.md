# Research (Stage 1) — SciSpace package

Literature, market, and regulatory research generated via SciSpace + web research (May 2026).
Source of record for the project's background and the manufacturing/commercial guide.

## Key deliverables
- [`scispace/urine_analyzer_report.md`](scispace/urine_analyzer_report.md) (+ `.pdf`) — comprehensive report
- [`scispace/Urine_Dipstick_Analyzer_Manufacturing_Report.md`](scispace/Urine_Dipstick_Analyzer_Manufacturing_Report.md) (+ `.html`) — **manufacturing & commercial guide (2P + 10P), Indian market.** Marked confidential by author; benchmarks Siemens Clinitek / Mission.

## Curated notes
- `scispace/india_ivd_market.md`, `scispace/ivd_india_regulatory_framework.md`, `scispace/india_mdr_chapter2.md`
- `scispace/insights_technology.md`, `scispace/wiki_urine_test_strip.md`, `scispace/robust_dipstick_paper.md`

## Raw data (regenerable web scrapes & literature exports)
- `scispace/scholar_*.csv`, `scispace/pubmed_*.csv`, `scispace/scispace_*.csv` — literature search results
- `scispace/web_*.csv`, `scispace/web_search_*.json` — raw web-scrape data (large)
- `scispace/cdsco_ivd_*.md` — partial/failed scrapes; superseded by `regulatory/01_cdsco_classification.md`

> Note: the manufacturing report describes both a **2-parameter (2P)** and **10-parameter (10P)**
> variant. The built firmware/hardware in this repo is the **10P** reader.
