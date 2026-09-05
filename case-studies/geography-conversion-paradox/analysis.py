import pandas as pd

DATA_PATH = "ecommerce_customer_data.csv"

df = pd.read_csv(DATA_PATH)

df["Purchased"] = df["Total_Purchases"] > 0

summary = (
    df.groupby("Location")
      .agg(
          Customers=("User_ID", "count"),
          Purchase_Rate=("Purchased", "mean"),
          Avg_Purchases=("Total_Purchases", "mean"),
          Median_Purchases=("Total_Purchases", "median"),
      )
      .sort_values("Avg_Purchases", ascending=False)
)

summary["Purchase_Rate"] = summary["Purchase_Rate"] * 100

print("Location performance")
print(summary.round(2))

print("\nRank by purchase rate")
print(summary.sort_values("Purchase_Rate", ascending=False)[["Purchase_Rate", "Avg_Purchases"]].round(2))

print("\nRank by average purchases")
print(summary.sort_values("Avg_Purchases", ascending=False)[["Purchase_Rate", "Avg_Purchases"]].round(2))

print("\nMetric gaps worth investigating")
for location, row in summary.iterrows():
    print(
        f"{location}: purchase rate={row['Purchase_Rate']:.1f}%, "
        f"avg purchases={row['Avg_Purchases']:.2f}"
    )
