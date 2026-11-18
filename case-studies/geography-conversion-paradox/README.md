# Case Study 03 — How Metric Choice Changes Location Rankings

## Why purchase rate and purchase count can rank locations differently

This case study shifts the analysis from individual behavior to **geographic performance**.

The business question is simple:

> **Which locations are actually performing best — and does the answer change depending on how we define “performance”?**

Using the same 500-customer e-commerce dataset, I compare two different measures:

- **Purchase rate** — the percentage of customers who purchased at least once.
- **Average purchases per customer** — the average number of purchases across everyone in the location.

The two measures do not always tell the same story.

## Key findings

| Location | Customers | Purchase rate | Avg. purchases |
|---|---:|---:|---:|
| Delhi | 70 | 87% | 2.73 |
| Kolkata | 71 | 85% | 2.68 |
| Chennai | 56 | 82% | 2.55 |
| Mumbai | 59 | 81% | 2.46 |
| Pune | 59 | 81% | 2.14 |
| Ahmedabad | 62 | 77% | 2.45 |
| Bangalore | 61 | 74% | 2.41 |
| Hyderabad | 62 | 73% | 2.23 |

## The paradox

**Pune** is a useful example of why a single KPI can be misleading.

Its purchase rate is relatively strong at **81%**, yet its average purchase count is only **2.14**, the lowest of all eight locations.

Meanwhile, **Ahmedabad** has a lower purchase rate at **77%**, but a higher average purchase count of **2.45**.

This suggests that simply asking “How many customers purchased?” is not enough. A location can have a healthy base of purchasing customers while generating fewer purchases per customer.

## Business interpretation

The sample suggests questions for a follow-up investigation:

1. **Investigate the sample patterns** in Delhi and Kolkata before proposing changes to investment.
2. **Investigate repeat-purchase behavior** in locations with strong purchase rates but lower purchase depth.
3. **Avoid ranking locations on purchase rate alone.**
4. **Collect richer data** before attributing geographic differences to customer preferences, marketing effectiveness, or product availability.

## Why this matters

A dashboard can make one location look “better” simply because of the metric selected.

This case study demonstrates an important analytics principle:

> **Metric selection changes the business story.**

Instead of producing another geographic bar chart, the analysis deliberately compares competing definitions of performance.

## Limitations

The dataset does not include revenue, order value, product category, marketing spend, customer acquisition source, repeat-purchase timing, or geographic population/market size.

Therefore, these results describe the observed customer sample and should not be interpreted as evidence that location causes purchasing behavior.

## Portfolio angle

This case study complements the first two projects:

- **Signal Map:** challenges the assumption that browsing explains purchases.
- **Cart-to-Purchase Gap:** challenges the assumption that cart activity predicts purchasing.
- **Geography Conversion Paradox:** challenges the assumption that one KPI can define market performance.

Together, they demonstrate a consistent analytical approach: **question the obvious metric, investigate the exceptions, and state what the data cannot prove.**

## Source and verification status

On 18 November 2026, a [source comparison](../../data/Customer_Source_Check.md) reproduced the historical buyer counts, cart cross-tab, location purchase rankings and correlations on a public copy. Some published browsing, page and cart averages did not match it. The historical file, original collection details, real/simulated status and reuse terms remain unverified. These sample results do not measure employer or client outcomes.
