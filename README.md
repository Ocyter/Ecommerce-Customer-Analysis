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

## Source and verification status

The original 500-row CSV is not published. The repository does not document its
original provider, licence, observation period or whether it is real or simulated.
The existing figures are retained as published portfolio results; this update
does not independently rerun them. Missing-value and duplicate-check outcomes
are not supplied. Full verification needs the original file and its provenance.
These are sample descriptions, not employer outcomes or evidence of an uplift.

## Separate SQL practice exercise

[SQL data quality and reconciliation](case-studies/sql-data-quality/README.md) uses
new, explicitly synthetic fixtures. Inputs, SQL, a runnable verifier and checked
outputs are supplied. It is separate from the customer dataset above and is not
a client project or completed Power BI deliverable.

[Download the portfolio CV](downloads/Osita_Nwaigwe_Portfolio_CV.pdf).

## Portfolio completion guide

[Practical data and Power BI evidence guide](docs/Portfolio_Evidence_Guide.md).
