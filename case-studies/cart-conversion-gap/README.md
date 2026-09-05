# Case Study 02 — The Cart-to-Purchase Gap

## A closer look at why cart activity alone is a weak conversion signal

The first project asked whether browsing behavior explains purchases. This second case study takes a different angle: **does adding items to a cart actually tell us who will buy?**

Using the same 500-customer dataset, the analysis investigates the relationship between cart additions and completed purchases, with a deliberate focus on the customers who break the expected funnel story.

## The business question

> If two customers add items to their carts, should we expect them to have similar purchase outcomes?

The data suggests the answer is **no**.

## Key findings

- 401 of 500 customers made at least one purchase (80.2%).
- 99 customers made zero purchases.
- 95 of those 99 non-purchasers had added at least one item to their cart.
- Only 4 non-purchasers had zero cart additions.
- 37 customers purchased despite having zero recorded cart additions.
- Average cart additions were remarkably similar for purchasers (5.17) and non-purchasers (5.06).
- Cart additions therefore behave more like an **engagement signal** than a reliable purchase predictor in this dataset.

## The interesting part

A generic funnel report might stop at "customers add to cart before purchasing."

This case study asks the harder question: **what happens when customers do not follow that expected path?**

The result is a useful portfolio lesson: aggregate engagement metrics can hide very different customer journeys.

## Method

The analysis uses pandas to examine:

1. Purchase vs. non-purchase groups.
2. Cart activity among non-purchasers.
3. Purchases among zero-cart customers.
4. Average and median cart additions by purchase outcome.
5. Purchase-count distribution by cart activity.

## Important limitation

This dataset is customer-level and does not contain event timestamps, session IDs, product details, prices, checkout steps, traffic source, or abandonment reasons. Therefore, this case study identifies **conversion patterns**, not causal explanations for abandonment.

## Files

- `analysis.py` — reproducible analysis.
- `insights.md` — narrative interpretation and recommended next data to collect.

## Portfolio angle

This case study complements the main Signal Map project by demonstrating a different analytical skill: **challenging the obvious funnel story instead of simply visualizing it.**
