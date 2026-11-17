# Osita Nwaigwe: portfolio evidence guide

Prepared 17 November 2026. This is a practical completion plan, not a Career Coach
score or an employer assessment. The separate Career Coach rubric has not been
provided. No 100% score, ATS result, interview outcome or workplace impact is certified.

## 1. What has been strengthened

The homepage introduces Osita before the projects. Repeated copy is shortened,
date ranges use "to", and case studies remain together in one section. The
existing customer studies now show methods, direct source-code links and explicit
source-data limitations. The geographic recommendation is framed as investigation
rather than an unsupported investment instruction.

The separate SQL exercise adds transparent synthetic inputs, executable SQL,
row-level routing, independent expected-result checks and downloadable outputs.
It was prepared with AI assistance. It is not client work or proof of production scale.

The CV web page has a direct PDF link. The original uploaded master CV is unchanged.
The published PDF is built from the web CV rather than from a different vacancy's CV.

## 2. Recover the original e-commerce evidence

The public repository does not contain the 500-row CSV. Do not replace it with an
unrelated 500-row file and retain the same findings.

### What to locate

- The exact original file named ecommerce_customer_data.csv.
- Its original download/source URL, provider and dataset title.
- Whether the provider describes it as real, anonymised or synthetic.
- The licence or permission to use the file and share derived material.
- Collection/observation period, if given. A download date is not an observation period.
- Field definitions and units, including what a purchase and cart count mean.

The expected columns are User_ID, Gender, Age, Location, Device_Type,
Product_Browsing_Time, Total_Pages_Viewed, Items_Added_to_Cart and Total_Purchases.

Record missing facts as unknown. The current repository does not establish that
the data is real or that publication is prohibited. Its absence is not proof of
a confidentiality requirement.

### Recheck before strengthening a claim

1. Confirm row count, unique IDs, field types and valid categories.
2. Count missing values per column, duplicate IDs and repeated rows.
3. Inspect impossible or negative counts, and record decisions instead of silently deleting.
4. Rerun the existing pandas scripts. Compare results with 401 purchasers,
   99 non-purchasers, 95 cart-active non-purchasers and 37 zero-cart purchasers.
   These are existing published expectations, not independently reverified here.
5. Investigate differences before editing the public results. Record source version,
   file checksum, exclusions, denominator, formula and rounding.
6. If sharing is permitted, publish an appropriately documented sample or access route.
   Otherwise publish aggregate checks and explain the actual restriction.
7. If the source cannot be recovered, retire or clearly retain the study as an
   unverified archived exercise. Build a new study from a documented source.

## 3. Build a genuine Power BI deliverable without waiting for that file

The supplied SQL exercise already provides fully synthetic inputs. You can use
its outputs for a new practice report immediately; no employer data is required.

### Get the files

Download this repository. Open case-studies/sql-data-quality/outputs/.
Optionally rerun the verifier from the repository root:

```sh
python case-studies/sql-data-quality/run_demo.py
```

Python's standard library is sufficient. The fixture has 12 raw order rows and
7 customer rows, deliberately including quality problems.

### Import and model

| Import file | Power BI table | Role |
| --- | --- | --- |
| customers_clean.csv | Customers | Unique complete customer dimension |
| reporting_fact.csv | Orders | 5 quality-passed order rows |
| quarantine.csv | Quarantine | 7 rejected order rows |
| reconciliation.csv | Reconciliation | Full-extract totals |

Use Power BI Desktop's Text/CSV connector. In Transform data, make identifiers,
status and region text; row counts and NGN amounts whole numbers. Keep the missing
amount null. Inspect column quality and type conversions.

Create a one-to-many, single-direction relationship from
Customers[customer_id] to Orders[customer_id]. Leave Quarantine and Reconciliation
disconnected because they describe the complete input rather than the filtered
reporting subset.

Create the measures in case-studies/sql-data-quality/power-bi/measures.dax one
at a time. They are starter expressions, not validated Desktop execution.

### Build and test two pages

On Reported orders, show the completed-order count, reported NGN amount, an
amount-by-region chart and a region slicer. State that the dataset is synthetic.

On Quality and reconciliation, show input, quarantined, out-of-scope and reported
row counts; rejection reasons; and the reconciliation difference. Label these as
full-extract figures. Show one missing amount separately.

| Validation | Expected result |
| --- | ---: |
| Customers / Orders / Quarantine rows | 4 / 5 / 7 |
| Completed orders, no filters | 3 |
| Reported amount, no filters | NGN52,000 |
| North completed orders and amount | 2 and NGN28,000 |
| West completed orders and amount | 1 and NGN24,000 |
| Input / Quarantined / Outside scope / Reported rows | 12 / 7 / 2 / 3 |
| Row reconciliation difference | 0 |

Clear slicers before checking unfiltered totals. Confirm relationships do not
multiply rows. A zero reconciliation difference does not fill the missing amount.
Use the same blank/zero convention throughout.

### Send back the real deliverable

Provide the PBIX or PBIP project, an actual screenshot of each report page and
Model view, the Power Query steps, final DAX, Desktop version and refresh date.
Include the checks above and explain your own decisions. A public embed is optional.

Only after opening, refreshing and inspecting the actual report should the
portfolio call it a completed Power BI project. HTML tables and starter DAX do
not establish that a Power BI report was built.

## 4. Show how you reason, not just an output

Run the SQL exercise and explain these decisions in your own words:

- Why quarantine every duplicate-key row rather than keep the first?
- Why summarise customer keys before joining to orders?
- Why are pending and cancelled orders different from invalid records?
- Why can known amounts reconcile while one amount is still missing?
- What would change if two valid orders belonged to the same customer?

As a follow-up exercise, add a valid completed order to a copy of the fixture.
Predict which counts and totals should change before running the query.
Record the expected versus actual result. Do not change the original fixture's
published expectations or call copied work an independent project.

The present tests cover the small fixture's seeded cases. They do not establish
a universal validator, performance tuning or production readiness.

## 5. Gather evidence from real work, where available

For Genesys, AtlasCapture, National Assembly or mentorship examples, use only
material you are permitted to share. A new synthetic recreation can illustrate
a method but must be labelled as a recreation.

Useful evidence could include a permitted redacted dashboard, a query excerpt,
a validation checklist, an audit-trail structure, documentation or a scorecard.
For each item, record the problem, your own contribution, tools actually used,
the output, intended audience and documented use.

Do not invent a numerical improvement. If a before/after measurement exists,
keep its date range, baseline, denominator and evidence. Otherwise describe the
concrete work and purpose without a percentage.

For AI-assisted workflows, name a platform only if you actually used it and can
confirm the name. Document the input, workflow, review checks, outputs and your
role. Do not turn a future design into a past incident.

## 6. Evidence checklist and remaining work

| Criterion | Current position | What closes the gap |
| --- | --- | --- |
| Clear identity and target roles | Presented on homepage | Keep current |
| Factual roles and overlapping dates | Preserved in CV | Verify future edits against source CV |
| Methods and source-code access | Added to existing studies | Explain decisions independently |
| Reproducible SQL example | Supplied with synthetic fixtures and checks | Run it and extend a separate copy |
| Original e-commerce provenance | Not established | Exact source file and source/usage details |
| Original e-commerce recomputation | Not completed in this update | Recover file, audit it, rerun scripts |
| Power BI evidence | Build kit only | Checked PBIX/PBIP, screenshots, model and measures |
| Real workplace outcomes | No new metrics claimed | Share only measured, supportable outcomes |
| Direct CV PDF | Built by site deployment workflow | Review the available download after publishing |
| Mobile and desktop rendering this run | Browser access unavailable | Fresh visual and interaction checks |
| Career Coach score | Not assessable | Upload the exact SKILL.md and any scoring rubric |

Completion of a checklist is not proof of a perfect score or a hiring outcome.

## 7. What to send next, in priority order

1. Original e-commerce CSV and its source/permission details, if recoverable.
2. A working Power BI project plus the actual screenshots and validation notes above.
3. The Career Coach SKILL.md and any referenced scoring rubric.
4. Any permitted work examples and measured outcomes you want to add.

A photograph remains optional and can be added later.

## Official Power BI references

Checked 17 November 2026:

- [Download Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop)
- [Connect to data](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-data-sources)
- [CALCULATE and filter context](https://learn.microsoft.com/en-us/dax/calculate-function-dax)
- [Power BI Desktop projects](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)

The specific SQL fixture, starter model plan and expected values above are
project-specific instructions, not claims made by Microsoft.
