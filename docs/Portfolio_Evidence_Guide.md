# Portfolio evidence guide | Osita Nwaigwe

Updated 18 November 2026. Use this as an interview and verification guide. It separates work a reviewer can inspect now from evidence only the candidate or an employer can provide.

## Start with the two strongest projects

1. **Commercial reporting:** [retail case study](https://ocyter.github.io/Ecommerce-Customer-Analysis/case-studies/public-data/retail/). Explain why the positive line total (£10.67m) differs from the signed total (£9.75m). Trace a month's positive, credit and adjustment values through the [monthly bridge](../case-studies/public-data/retail/monthly-bridge.csv). Explain why the biggest credit warrants inspection without calling it a lost sale. Show the sensitivity check before discussing whether repeat rows should be removed.
2. **Operations reporting:** [bikeshare case study](https://ocyter.github.io/Ecommerce-Customer-Analysis/case-studies/public-data/bikeshare/). Use the [hourly profile](../case-studies/public-data/bikeshare/hourly-profile.csv) to explain why the busiest working-day hour (17:00) differs from weekends and holidays (13:00). For example, 262,120 rentals divided by 499 observed working-day 17:00 rows gives 525.3. Explain why any decision about a *specific station* needs additional data.
3. **Verify the calculations yourself:** download the [Excel workbook](https://ocyter.github.io/Ecommerce-Customer-Analysis/downloads/Public_Data_Decision_Workbook.xlsx), inspect its formulas, and rebuild the source outputs using the [documented commands](../case-studies/public-data/README.md). Both datasets are attributed, licensed and pinned by checksum. Be ready to discuss which parts you ran, changed and checked yourself; do not present assisted preparation as sole unaided delivery.

## What would improve each decision

| To test | Minimum additional data | Check before making a recommendation | Success measure |
| --- | --- | --- | --- |
| Retail credit exceptions | Finance-approved linkage between credit and original invoice; reason, posted amount/date, disposition and settlement date | Confirm many-to-one and partial credits; reconcile linked plus unlinked value to the control total | Percentage of credit value matched; value and age of unexplained exceptions. Do not infer a return rate from the posting bridge. |
| Bike availability | Recent station ID, service hours, capacity, departures/arrivals, timestamped available bikes/docks and rebalancing cost | Check missing intervals, station closures and season; compare similar stations and equivalent time windows | Empty/full minutes per service hour and cost per hour of improvement. A pilot result would be new evidence, not a result of the current historical study. |

## Complete the Power BI check on Windows

The [portable project](https://ocyter.github.io/Ecommerce-Customer-Analysis/case-studies/sql-data-quality/power-bi/OrderReview-PowerBI.zip) already contains the semantic model and report: two pages, six visuals, five embedded imports and ten DAX measures. You do not need to design it from scratch or upload employer data.

1. Extract the ZIP on Windows and open OrderReview.pbip in a current Power BI Desktop that supports the project format. Select Refresh.
2. On the completed-orders page verify **3 / NGN52,000** overall; **2 / NGN28,000** for North and **1 / NGN24,000** for West. Clear the slicer.
3. On the quality page verify **12 raw**, **7 quarantined**, **2 outside scope**, **3 reported**, **1 missing amount**, and **zero row and known-amount differences**. These figures are controls for the full extract.
4. Inspect the Customers-to-Orders relationship in Model view. Save a screenshot of each page and Model view, the Desktop version, date, and a small table of expected versus actual results. If anything differs, keep the error or screenshot and fix it before saying it passed. [Full build and validation notes](../case-studies/sql-data-quality/power-bi/README.md).

The inputs, independent totals, file structure and visual bindings have been checked outside Desktop. This does not certify a Desktop refresh or prove the report displayed correctly on Windows.

## Original customer study

The [source comparison](../data/Customer_Source_Check.md) documents the public comparison CSV, hash, audit and discrepancies. It confirms 401 of 500 buyers on that file but does not establish it was the historical original. The comparison mean for pages is **27.182** rather than the historical **27.00**. The three analyses are grouped as earlier work on the homepage. To resolve provenance, provide the original file, original source/download record and rights information. Without them leave the archive labelled; the new studies stand on their own.

## What only you can supply

- **One workplace example, if permitted:** identify the team, question, your contribution, artifact, audience and documented use. An authorised redacted scorecard, query excerpt or reporting protocol is sufficient. Do not publish employer data or imply an employer sponsored these public studies. If there is no defensible before/after measure, describe how the artifact was used.
- **Personal contribution:** rerun one study, change one defensible assumption on a separate copy, and write a few sentences in your own words about the difference. Keep the original baseline intact. A short, demonstrable judgement is stronger than a longer tool list.
- **Exact grading rubric:** supply the Career Coach SKILL.md and any separate rubric if an actual assessment under those criteria is required. Source quality, scope, outputs and reproducibility are inspectable; a specific grade or hiring outcome is not guaranteed.
