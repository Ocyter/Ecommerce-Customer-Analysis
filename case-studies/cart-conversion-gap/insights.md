# Insights — The Cart-to-Purchase Gap

## 1. The expected funnel breaks in both directions

There are 95 customers who added at least one item to their cart but recorded zero purchases. At the same time, 37 customers recorded purchases despite having zero cart additions.

That means the customer journey represented in this dataset is not a clean linear path of browse → cart → purchase.

## 2. Cart volume barely separates buyers from non-buyers

Purchasers averaged 5.17 cart additions, while non-purchasers averaged 5.06. The medians are both 5.

The practical implication is important: **cart volume alone is not a strong discriminator of purchase outcome here.**

## 3. The missing variable may be intent, not activity

The dataset captures how much activity occurred, but not what happened around that activity. We cannot see:

- whether the same products were added repeatedly;
- whether prices or discounts changed;
- whether checkout was attempted;
- whether payment failed;
- how long the cart remained open;
- whether the customer returned later;
- where the customer came from.

Those variables could explain why similar cart activity leads to different outcomes.

## 4. Recommended next analysis

If this were a production analytics project, the next dataset request would be event-level data containing:

`customer_id → session_id → timestamp → product → cart_event → checkout_event → payment_event → purchase_event`

With that structure, the analysis could move from descriptive segmentation to a true conversion-funnel diagnosis.

## 5. Portfolio takeaway

The strongest insight is not that carts "cause" purchases. It is that **a familiar business funnel should be tested, not assumed**.

A good analyst should be willing to report when the data does not behave like the textbook journey.
