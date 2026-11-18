# Order Review: Power BI project

This AI-assisted practice report uses an invented order extract. A team deciding what revenue to report would first need to separate rejected rows from valid orders outside the reporting scope. This project shows that distinction and reconciles the result to the raw extract. Values are illustrative whole Nigerian naira, never client revenue.

## Open it

1. Download [OrderReview-PowerBI.zip](https://ocyter.github.io/Ecommerce-Customer-Analysis/case-studies/sql-data-quality/power-bi/OrderReview-PowerBI.zip) and **extract all files** to a writable folder on Windows.
2. In a current Power BI Desktop version with project and enhanced report-format support, open **OrderReview.pbip**. Keep the adjacent Report and SemanticModel folders together. If necessary, enable the Power BI Project/PBIR options available in your Desktop version and restart.
3. Select **Home > Refresh**. No data cache is bundled. All five import queries read snapshots embedded in the model, so no local path changes, credentials, external database or online connection are needed for the data itself.
4. Open **Completed orders | synthetic**. Select North and West on the region slicer; then clear it. Open **Data quality | full extract** to see the routes and the independently calculated differences.
5. In Model view verify the one-to-many, single-direction Customers → Orders relationship. RawOrders, Reconciliation and Quarantine intentionally have no relationship to the region dimension.

## What to check in Desktop

| View / test | Expected result |
| --- | --- |
| Completed orders; all regions | 3 completed orders; NGN52,000 |
| North | 2 completed orders; NGN28,000 |
| West | 1 completed order; NGN24,000 |
| South | 0 completed orders; NGN0 |
| Raw input | 12 rows, one missing amount |
| Row routing | 7 quarantined, 2 outside scope, 3 reported |
| Routed known amounts | NGN59,500 / NGN11,000 / NGN52,000 respectively |
| Differences against original raw orders | 0 rows, NGN0 known amount difference |

A known-amount difference of zero does not recover the missing amount. The regional slicer should change completed-order results only. On the quality page, clear any selection before reading full-extract totals.

## What was implemented and verified

The project includes two report pages with six bound visuals, ten DAX measures, five typed Power Query imports and a customer-to-orders relationship. The model embeds exact bytes of four verified SQL exports plus the separate original orders CSV. Input count and input known amount are taken from that independent raw table. Category totals are calculated from the SQL disposition output. This makes the control stronger than subtracting parts from their own sum. The empty amount remains null.

The fixture counts, regional totals and reconciliation were recalculated outside Desktop, visual field references were checked against the semantic model, and the PBIP, PBIR, PBISM and report JSON files were validated against Microsoft's published JSON schemas. These checks do not execute the Power Query or DAX engine. The report still needs a Windows Desktop open, refresh, slicer check, and screenshots of each page and Model view before claiming a Desktop-tested result. Record Desktop version, test date, and actual versus expected values above.

## Source and rebuilding

The readable source in this repository is under `power-bi/project/`. DAX is in the measures of `OrderReview.SemanticModel/model.bim`; the Power Query definitions are in its import partitions. The separate `measures.dax` is a readable copy of the project measures. To update with the fixture and regenerate the portable project and its ZIP from the repository root:

~~~sh
python case-studies/sql-data-quality/run_demo.py
python case-studies/sql-data-quality/power-bi/build_project.py
~~~

The refresh uses embedded snapshots, not a live link to the CSVs. Rebuild after changing the inputs. No service publishing, client data or deployment credentials are required for this demonstration.

**Microsoft references:** [Power BI Desktop projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview), [report format](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report), [semantic model format](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset).
