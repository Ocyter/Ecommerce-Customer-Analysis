import pandas as pd

DATA_PATH = "ecommerce_customer_data.csv"

df = pd.read_csv(DATA_PATH)

# Create simple outcome flags.
df["Purchased"] = df["Total_Purchases"] > 0
df["Cart_Active"] = df["Items_Added_to_Cart"] > 0

print("=== CART-TO-PURCHASE GAP ===")
print(f"Customers: {len(df):,}")
print(f"Purchase rate: {df['Purchased'].mean():.1%}")
print(f"Zero-purchase customers: {(~df['Purchased']).sum():,}")
print(f"Non-purchasers with cart activity: {((~df['Purchased']) & df['Cart_Active']).sum():,}")
print(f"Purchasers with zero cart additions: {(df['Purchased'] & ~df['Cart_Active']).sum():,}")

print("\nAverage cart additions by purchase outcome:")
print(df.groupby("Purchased")["Items_Added_to_Cart"].agg(["count", "mean", "median"]).round(2))

print("\nAverage cart additions by purchase count:")
print(df.groupby("Total_Purchases")["Items_Added_to_Cart"].agg(["count", "mean", "median"]).round(2))

print("\nCross-tab: cart active vs purchase outcome")
print(pd.crosstab(df["Cart_Active"], df["Purchased"]))

print("\nInterpretation:")
print("Cart activity is common among both purchasers and non-purchasers.")
print("This dataset does not support treating cart additions as a strong standalone conversion predictor.")
