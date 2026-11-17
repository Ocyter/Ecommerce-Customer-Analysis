# Power BI build kit: work still to complete

This directory contains starter DAX and instructions, not a completed PBIX,
verified DAX execution or Power BI screenshot. The SQL page is HTML, not Power BI.

## Import the supplied synthetic outputs

| CSV in ../outputs/ | Table name | Purpose |
| --- | --- | --- |
| customers_clean.csv | Customers | Unique complete dimension |
| reporting_fact.csv | Orders | Quality-passed orders, all statuses |
| quarantine.csv | Quarantine | Rejected source rows and primary reasons |
| reconciliation.csv | Reconciliation | Full-extract totals |

1. In Power BI Desktop, use **Get data > Text/CSV** and **Transform data**.
   Assign text to keys/status/region and whole number to row counts and NGN amounts.
   Keep the missing amount in Quarantine as null. Inspect row counts and column quality.
2. Relate Customers[customer_id] (one) to Orders[customer_id] (many), single
   direction from Customers to Orders. Leave Quarantine and Reconciliation disconnected.
3. Create each measure in measures.dax separately. Test in Desktop; the starter
   expressions have not been executed in Power BI here.
4. Build a Reported orders page: completed-order count, amount by region and a
   region slicer. Label the scope as quality-passed completed synthetic orders.
5. Build a Quality and reconciliation page with all four route totals, the
   difference and the rejection reasons. Label it full-extract, independent of region.
   Show the missing-amount issue separately. Zero reconciliation difference does
   not mean the missing amount has been recovered.

## Desktop checks

| Check | Expected |
| --- | ---: |
| Customers / Orders / Quarantine rows | 4 / 5 / 7 |
| Unfiltered Completed Orders | 3 |
| Unfiltered Reported Amount NGN | 52000 |
| North completed orders / amount | 2 / 28000 |
| West completed orders / amount | 1 / 24000 |
| Input / Quarantined / Outside Scope / Reported rows | 12 / 7 / 2 / 3 |
| Reconciliation Difference | 0 |

Clear filters before checking unfiltered totals. South has no completed orders
after validation; use a consistent blank/zero display convention.

## Required evidence before publishing a completed Power BI claim

- PBIX or PBIP that opens and refreshes, with Desktop version and refresh date.
- Actual screenshots of each report page and Model view.
- The Power Query steps and DAX actually used, including changes to the starter.
- The validation outcomes and an explanation of your decisions in your own words.

An interactive public embed is optional. Retain the synthetic-data label and
do not present this as employer experience.

## Official references

- [Download Desktop](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop)
- [Get data](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-sources)
- [CALCULATE](https://learn.microsoft.com/en-us/dax/calculate-function-dax)
- [Desktop projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
