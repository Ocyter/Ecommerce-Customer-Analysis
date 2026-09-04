# E-commerce Customer Analysis

## Executive Summary

This project analyzes **500 customer records** to understand browsing behavior, cart activity, and purchases across gender, device type, age, and location.

### Key findings

- **80.2%** of customers made at least one purchase (401 of 500).
- Average purchases per customer: **2.46**; median: **2**.
- **Mobile** is the most common device (178 customers, 35.6%) and has the highest average purchases among devices (**2.53**).
- **Delhi** has the highest average purchases per customer (**2.73**) and the highest purchase rate (**87%**) among the locations in this sample.
- Purchase volume has **very weak linear relationships** with browsing time, pages viewed, and items added to cart. Pearson correlations with purchases are -0.023, 0.014, and 0.008 respectively.
- Age also has a very weak linear relationship with purchases (**r = -0.042**), so age alone is not a strong predictor here.

## Dataset Overview

| Metric | Value |
|---|---:|
| Customers | 500 |
| Columns | 9 |
| Gender categories | 2 |
| Locations | 8 |
| Devices | 3 |
| Age range | 18–35 |
| Average browsing time | 30.77 |
| Average pages viewed | 27.00 |
| Average items added to cart | 5.15 |
| Average purchases | 2.46 |
| Customers with at least one purchase | 401 (80.2%) |
| Customers with zero purchases | 99 (19.8%) |

## Customer Profile

### Gender

| Gender | Customers | Avg. browsing time | Avg. pages | Avg. cart items | Avg. purchases |
|---|---:|---:|---:|---:|---:|
| Female | 239 | 31.55 | 27.03 | 5.08 | 2.28 |
| Male | 261 | 30.00 | 26.97 | 5.21 | 2.64 |

Male customers average 2.64 purchases versus 2.28 for female customers. This is descriptive only and should not be interpreted as a causal gender effect.

### Device Type

| Device | Customers | Avg. browsing time | Avg. pages | Avg. cart items | Avg. purchases |
|---|---:|---:|---:|---:|---:|
| Desktop | 159 | 29.83 | 26.92 | 5.06 | 2.40 |
| Mobile | 178 | 30.67 | 27.13 | 5.21 | 2.53 |
| Tablet | 163 | 31.71 | 26.94 | 5.17 | 2.45 |

Mobile is the largest segment and has slightly higher average purchases than desktop and tablet users. The differences are modest.

## Location Performance

| Location | Customers | Avg. browsing time | Avg. pages | Avg. cart items | Avg. purchases | Purchase rate |
|---|---:|---:|---:|---:|---:|---:|
| Delhi | 70 | 29.37 | 26.91 | 5.27 | 2.73 | 87% |
| Kolkata | 71 | 33.44 | 27.21 | 5.10 | 2.68 | 85% |
| Chennai | 56 | 27.14 | 26.61 | 5.18 | 2.55 | 82% |
| Mumbai | 59 | 30.42 | 26.66 | 5.15 | 2.46 | 81% |
| Ahmedabad | 62 | 29.73 | 27.19 | 5.06 | 2.45 | 77% |
| Bangalore | 61 | 32.54 | 27.52 | 5.18 | 2.41 | 74% |
| Hyderabad | 62 | 33.32 | 27.40 | 5.08 | 2.23 | 73% |
| Pune | 59 | 29.34 | 26.27 | 5.15 | 2.14 | 81% |

Delhi leads the sample on both average purchases and purchase rate, while Hyderabad has the lowest purchase rate and Pune has the lowest average purchases. These differences are useful for segmentation, but the dataset does not establish why they occur.

## Funnel Observations

There are **41 customers with zero items added to cart** and **99 customers with zero purchases**. Because the dataset contains aggregate customer-level counts rather than timestamps or individual sessions, a precise step-by-step conversion funnel cannot be calculated.

Useful customer segments include:

1. Browsers with no cart activity.
2. Cart users with no purchases.
3. Customers with one or more purchases.
4. High-purchase customers.

## Correlation Analysis

| Variable | Correlation with purchases |
|---|---:|
| Product browsing time | -0.023 |
| Total pages viewed | 0.014 |
| Items added to cart | 0.008 |
| Age | -0.042 |

All values are close to zero, indicating little linear association in this sample. This does **not** prove that these variables have no predictive value; nonlinear effects, interactions, and the aggregated nature of the dataset may matter.

## Business Recommendations

1. **Prioritize mobile UX.** Mobile represents the largest customer segment, so checkout speed, product discovery, and cart usability should be monitored closely.
2. **Investigate cart abandonment.** Customers with no purchases are a natural segment for remarketing or checkout-friction analysis.
3. **Compare locations.** Delhi and Kolkata perform strongly on purchase metrics; Hyderabad and Pune warrant investigation for potential differences in acquisition, product mix, or conversion experience.
4. **Avoid over-targeting on age or gender alone.** Their relationships with purchase volume are weak in this dataset.
5. **Collect event-level data.** Session timestamps, product/category IDs, prices, traffic source, checkout steps, and individual order events would enable stronger funnel and cohort analysis.

## Methodology

- Loaded the CSV with pandas.
- Checked dimensions, data types, categorical distributions, and descriptive statistics.
- Compared purchase behavior by gender, device, and location.
- Calculated purchase rate as the percentage of customers with `Total_Purchases > 0`.
- Calculated Pearson correlations for numeric behavioral variables.
- Made descriptive observations only; no causal claims were made.

## Data Privacy

The repository does **not** include the raw customer CSV. Because this is a public repository and the dataset contains user-level records, excluding the raw data is a safer publishing practice.
