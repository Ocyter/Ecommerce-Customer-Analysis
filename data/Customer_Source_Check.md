# Checking the source of the 500-customer study

**Checked 18 November 2026.** A public comparison file reproduces the buyer counts, purchase rankings and correlations. It does not reproduce all the published browsing, page and cart averages. It is a cross-check, not a recovered original. No customer-level records have been added to this repository.

## Where the comparison came from

- [Aman Kharwal's dated walkthrough](https://amanxai.com/2023/11/06/customer-behaviour-analysis-using-python/) describes a file with this name and nine columns. Its published counts and numeric means match the comparison file. This is evidence for the comparison, not proof that Osita downloaded his original file here.
- The walkthrough links to [Statso's case study](https://statso.io/customer-behaviour-case-study/). That route displayed a 404 page when checked. The tutorial publication date (6 November 2023) is **not** a data collection date.
- The [comparison CSV at the inspected Git revision](https://github.com/Mfundo-debug/CustomerBehaviourAnalysis/blob/e5f238bad2fe0d8382c50527cda720d90af95f9c/ecommerce_customer_data.csv) is a third-party copy. Its SHA-256 is `f4bf7d931759c85e09186e642b201083c3ed2a97b9c5bf4a48ef41c7ff7f7fab`. No original checksum was available to compare with it.
- Source organisation, collection method and dates, real versus simulated status, and permission to redistribute the historical data remain unverified. The portfolio notebook references a local CSV and does not include stored data or executed cell outputs.

## What was checked

The historical portfolio scripts for customer, cart and location analysis were run against the comparison file. A separate [audit script](check_customer_copy.py) calculates [aggregate results](customer_comparison_aggregates.json) directly from the named columns. The copy contains 500 rows, nine columns, 500 distinct customer identifiers, no missing cells and no exact duplicate rows. Age and activity counts are nonnegative integers. None of those quality checks establishes where the data came from.

| Measure | Historical report | Pinned comparison copy | Interpretation |
| --- | ---: | ---: | --- |
| Customers with any purchase | 401 of 500 | 401 of 500 | Same count; 80.2% of rows |
| Non-buyers with cart activity | 95 of 99 | 95 of 99 | Same count; not a timed abandonment event |
| Buyers with no cart activity | 37 | 37 | Same count |
| Delhi: purchase rate / purchases per customer | 87% / 2.73 | 61 of 70 (87.1%) / 2.73 | Same after rounding |
| Pune: purchase rate / purchases per customer | 81% / 2.14 | 48 of 59 (81.4%) / 2.14 | Same after rounding |
| Mean browsing time | 30.77 | 30.74 | Values differ |
| Mean pages viewed | 27.00 | 27.182 | Values differ |
| Average mobile cart additions | 5.21 | 5.6573 | Values differ |

The four reported correlations with purchases also match to three decimal places. Group-level page and cart averages show additional discrepancies. The analysis report now labels and uses recomputed comparison-file averages in its tables; it does not retroactively identify the historical file. The live customer dashboard shows a corroborated customer count in place of the disputed page-view KPI. The historical version can be inspected in [the previous report](https://github.com/Ocyter/Ecommerce-Customer-Analysis/blob/0064247e2ca971c457dcf36f312e90a8ba308c1c/analysis_report.md).

## Reproduce and resolve

1. Obtain the pinned comparison file from the revision above. Keep it outside the public repository. This is a comparison route, not an assertion about data rights.
2. From the repository root, with pandas installed, run `python data/check_customer_copy.py /path/to/ecommerce_customer_data.csv`. Compare the printed SHA-256 and aggregates with the checked JSON.
3. If Osita recovers his own CSV, keep it separate. Compare its checksum and aggregate report. Different byte hashes can result from file encoding or line endings, so compare parsed values as well. Do not publish original rows without verified permission.
4. To attribute the original, retain the actual source citation, reuse terms, collection period and data status. If those cannot be established, keep the archival label and use the separately sourced public-data projects as the main evidence.
