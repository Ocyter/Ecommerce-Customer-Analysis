import pandas as pd

# Load customer dataset
# Keep ecommerce_customer_data.csv local; it is intentionally not published
# in the public repository.
df = pd.read_csv("ecommerce_customer_data.csv")

print("Shape:", df.shape)
print("\nColumns:")
print(df.dtypes)

print("\nDescriptive statistics:")
print(df.describe())

metrics = [
    "Product_Browsing_Time",
    "Total_Pages_Viewed",
    "Items_Added_to_Cart",
    "Total_Purchases",
]

print("\nGender averages:")
print(df.groupby("Gender")[metrics].mean().round(2))

print("\nDevice averages:")
print(df.groupby("Device_Type")[metrics].mean().round(2))

location = df.groupby("Location").agg(
    Customers=("User_ID", "count"),
    Avg_Purchases=("Total_Purchases", "mean"),
    Purchase_Rate=("Total_Purchases", lambda x: (x > 0).mean()),
).sort_values("Avg_Purchases", ascending=False)

print("\nLocation performance:")
print(location.round(2))

print("\nPurchase rate:", round((df["Total_Purchases"] > 0).mean(), 4))
print("Customers with zero cart items:", int((df["Items_Added_to_Cart"] == 0).sum()))
print("Customers with zero purchases:", int((df["Total_Purchases"] == 0).sum()))

corr = df[[
    "Age",
    "Product_Browsing_Time",
    "Total_Pages_Viewed",
    "Items_Added_to_Cart",
    "Total_Purchases",
]].corr()["Total_Purchases"]

print("\nCorrelations with Total_Purchases:")
print(corr.round(3))
