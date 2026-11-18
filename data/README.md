# Data

The raw `ecommerce_customer_data.csv` file is intentionally not committed to the public repository.

## Expected columns

`User_ID`, `Gender`, `Age`, `Location`, `Device_Type`, `Product_Browsing_Time`, `Total_Pages_Viewed`, `Items_Added_to_Cart`, `Total_Purchases`

## Run locally

Place the CSV in the project root as `ecommerce_customer_data.csv`, or launch the Streamlit app and upload the CSV through the sidebar.

The dashboard is designed to work from the uploaded dataset without exposing customer-level data in the public repo.

## Source and verification status

On 18 November 2026, a [source comparison](Customer_Source_Check.md) reproduced the historical buyer counts, cart cross-tab, location purchase rankings and correlations on a public copy. Some published browsing, page and cart averages did not match it. The historical file, original collection details, real/simulated status and reuse terms remain unverified. These sample results do not measure employer or client outcomes.
