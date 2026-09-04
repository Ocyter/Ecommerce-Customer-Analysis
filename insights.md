# The 500-Customer Signal Map

> **The interesting result is not that customers browse more. It is that this dataset gives almost no linear signal that browsing activity predicts purchase volume.**

## 01 — The baseline

**500 customers · 8 locations · 3 devices · 80.2% purchased**

The customer base is relatively young (18–35) and behavior is tightly centered around:

- ~31 minutes of browsing
- ~27 pages viewed
- ~5 items added to cart
- ~2.5 purchases

That makes broad averages useful for context, but not especially useful for targeting.

## 02 — The strongest geographic contrast

**Delhi:** 2.73 average purchases / 87% purchase rate

**Pune:** 2.14 average purchases / 81% purchase rate

**Hyderabad:** 2.23 average purchases / 73% purchase rate

The location gap is more interesting than the age or gender gap. It suggests a useful next question: *is the difference caused by acquisition mix, merchandising, pricing, or customer experience?*

## 03 — Mobile wins, but only slightly

Mobile is the largest device group at **178 customers** and records **2.53 average purchases**. Desktop records 2.40 and tablet 2.45.

The difference is not large enough to claim that mobile causes higher purchasing. It is enough to justify mobile-first UX monitoring because it is the largest audience segment.

## 04 — The surprising non-signal

Pearson correlation with `Total_Purchases`:

| Signal | r |
|---|---:|
| Browsing time | -0.023 |
| Pages viewed | 0.014 |
| Items added to cart | 0.008 |
| Age | -0.042 |

These are effectively near-zero linear relationships.

That should change the next analytical move. Instead of simply asking **“what increases with purchases?”**, the next project should test:

- nonlinear relationships
- interaction effects
- customer clusters
- purchase/no-purchase classification
- location × device combinations
- cart-to-purchase behavior

## 05 — The 99-customer opportunity pool

**99 customers recorded zero purchases.**

There are also **41 customers with zero cart additions**.

These groups should not automatically be treated as one audience. A visitor who never added anything has a different problem from someone who added products but failed to purchase. The next analysis should separate discovery friction from checkout friction.

## 06 — What I would build next

If this were connected to a live e-commerce platform, the highest-value additions would be:

1. **Session-level events** — identify where users actually drop out.
2. **Order value** — distinguish purchase frequency from revenue impact.
3. **Product/category data** — find merchandise-level conversion patterns.
4. **Traffic source** — compare organic, paid, social, referral, and direct users.
5. **Timestamps** — build cohorts and identify repeat-purchase behavior.
6. **Checkout events** — isolate payment and delivery friction.

## Bottom line

This dataset is better at **describing who the customers are** than explaining **why they buy**.

That is not a weakness of the project—it is the central insight. A strong next iteration should move from descriptive segmentation toward event-level behavioral analysis and predictive modeling.
