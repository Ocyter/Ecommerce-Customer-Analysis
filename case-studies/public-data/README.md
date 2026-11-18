# Two decisions from public data

| Study | Audience / decision | Source and grain |
| --- | --- | --- |
| [Retail invoice bridge](https://ocyter.github.io/Ecommerce-Customer-Analysis/case-studies/public-data/retail/) | Finance or commercial analyst: reconcile positive postings, credit postings and other adjustments before interpreting sales | Daqing Chen (2015), [Online Retail](https://doi.org/10.24432/C5BW33), UCI. One workbook row per invoice line, Dec 2010 to 9 Dec 2011. |
| [Bike-share demand](https://ocyter.github.io/Ecommerce-Customer-Analysis/case-studies/public-data/bikeshare/) | Operations planner: shortlist clock hours to review station availability | Hadi Fanaee-T (2013), [Bike Sharing](https://doi.org/10.24432/C5W894), UCI. Hourly and daily system counts, 2011 and 2012. |

Both datasets are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The portfolio transforms the originals into aggregates, comparisons and charts. These AI-assisted demonstrations describe historical records. They do not claim commercial impact, a client relationship or improvements to either business.

## Reproduce

With Python 3.10+ and openpyxl 3.1 installed, from the repository root:

~~~sh
python case-studies/public-data/analyse.py --cache /tmp/osita-uci-cache
python case-studies/public-data/check_outputs.py
python case-studies/public-data/render.py
git diff --exit-code -- case-studies/public-data/bikeshare case-studies/public-data/retail
~~~

The first command downloads both official UCI ZIP files on first use, refuses changed hashes, and writes aggregate CSVs and audit JSON. Use a cache outside the site; raw rows are not deployed. Run without Python's -O flag so validation assertions execute. The independent [SQLite controls](review.sql) recalculate the monthly bridge in integer thousandths of a pound and rank hours from the exported counts. The renderer creates the published charts, tables and narratives from those checked outputs. No trained model or inferred outcome is used.

## Fields and decisions

**Retail.** InvoiceNo identifies an invoice, not a line. StockCode describes the item; Description is item text. Quantity is signed and UnitPrice is sterling per unit. InvoiceDate groups postings by month. CustomerID and Country describe the customer, not the original sale to which a credit relates. A negative-value line on a C-coded invoice is a credit; a non-C line with positive quantity and price enters positive value; everything else remains in the bridge. Credit percentages use positive value as the denominator and the absolute value of credits as numerator. Exact duplicate sensitivity uses all eight original fields and the first occurrence as baseline. No deduplication or rounding is silently applied. The catalog's general missingness label does not replace actual field checks.

**Bike sharing.** Date, clock hour and workingday define groups. Holiday/weekend records are pooled, not treated as identical days in every respect. Casual and registered rental counts must sum to cnt; rows count rentals, not unique customers. The grouped CSV carries rentals, rider counts and observed hour counts so averages can be recalculated. Filter to All **or** a calendar year: All is the pooled result, not another year to add. UCI's catalog headline lists 17,389 instances; the pinned hour.csv contains 17,379 distinct date/hour rows. The analysis uses the file, and reconciles each day to day.csv. Counts cannot measure unmet demand without station capacity and availability.

## Interview prompts

- Why can a small number of large credits distort a value-weighted KPI? Recalculate the share with and without the biggest credit; say which denominator is held fixed.
- Would deleting rows with no customer ID improve invoice reconciliation? Would that answer change for customer retention?
- Why use observed hours rather than raw rental totals to compare day types? Show where the two denominators differ in the CSV.
- What evidence would justify operational action? Explain the difference between measuring *recorded use* and measuring *unmet need*.

The [portfolio evidence guide](../../docs/Portfolio_Evidence_Guide.md) covers ownership, the earlier customer study, workplace examples and final Power BI Desktop verification.
