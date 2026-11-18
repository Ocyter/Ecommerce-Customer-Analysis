# SQL data quality and reconciliation

A new portfolio practice demonstration using deliberately constructed data. It
is not an employer or client assignment and its figures are not measured
workplace improvements. Prepared with AI assistance; outputs are reproducible.

## Data provenance

The two CSVs in `data/` were created for this exercise on 17 November 2026.
All IDs, regions, statuses and whole-NGN amounts are invented. There are no real
people, orders or company results. The date is preparation, not an observation period.

## Run

From the repository root, with Python 3.8+ and SQLite 3.25+:

```sh
python case-studies/sql-data-quality/run_demo.py
```

No packages, accounts, private CSV or network access are required. The runner
loads a temporary in-memory database and writes outputs without altering inputs.

## Decisions

- Retain and quarantine every row in a duplicate order-key group.
- Summarise customer keys before joining; reject ambiguous customer references.
- Reject missing IDs, unknown customers, missing regions, missing/negative amounts
  and invalid statuses. Log one primary issue per order, in SQL CASE precedence.
- Pending/cancelled orders may pass quality while remaining outside the report.
- Do not impute the missing amount. Known-amount reconciliation reports it separately.

## Expected fixture results

| Route | Order rows |
| --- | ---: |
| Quarantined | 7 |
| Outside reporting scope | 2 |
| Reported completed orders | 3 |
| Total input order rows | 12 |

Three reported orders total NGN52,000: North NGN28,000 and West NGN24,000.
Seven rejected rows exercise six primary defect types. Missing-ID and invalid-status
guards exist but are not seeded in this fixture.

## Evidence

- `data/`: published synthetic CSV inputs.
- `queries.sql`: joins, CTE, window count, classification and aggregation.
- `run_demo.py`: independent expected fixture checks, input hashes and exports.
- `outputs/orders_checked.csv`: row-level decisions.
- `outputs/reconciliation.csv`: accounting of all rows and known amounts.
- `outputs/verification.json`: checked results and limitations.
- `power-bi/`: portable two-page PBIP, model, DAX and validation instructions. A Windows Desktop refresh and visual test are still outstanding.

The checks cover expected rejected rows, no join row multiplication, valid
reporting rows and regional aggregates. They do not establish production
readiness, performance gains or business impact.
