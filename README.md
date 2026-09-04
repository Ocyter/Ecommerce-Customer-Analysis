# E-commerce Customer Analysis

A data-analysis project exploring customer browsing behavior, cart activity, purchases, device usage, gender, age, and location.

## Project contents

- **[Analysis Report](analysis_report.md)** — executive summary, findings, segment comparisons, correlation analysis, and recommendations.
- **[analysis.py](analysis.py)** — reproducible pandas analysis script.

## Dataset

The analysis uses a 500-row customer-level e-commerce dataset with 9 fields covering customer ID, gender, age, location, device type, browsing time, pages viewed, items added to cart, and purchases.

The raw customer CSV is intentionally not published in this public repository.

## Highlights

- 80.2% of customers made at least one purchase.
- Mobile is the largest device segment.
- Delhi has the highest average purchase count in this sample.
- Linear correlations between purchases and the recorded browsing/cart variables are very weak.

See the **Analysis Report** for details and limitations.

## Reproduce

```bash
pip install pandas
python analysis.py
```

## Note

The findings are descriptive and do not establish causal relationships. More granular event-level data would support stronger conversion-funnel, cohort, and predictive analyses.
