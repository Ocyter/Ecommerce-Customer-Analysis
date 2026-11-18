"""Compare a supplied 500-customer CSV against archived aggregate claims. No row-level output."""
from pathlib import Path
import argparse
import hashlib
import io
import json

import pandas as pd


def compare(data):
    d = pd.read_csv(io.BytesIO(data))
    schema = ["User_ID", "Gender", "Age", "Location", "Device_Type", "Product_Browsing_Time",
              "Total_Pages_Viewed", "Items_Added_to_Cart", "Total_Purchases"]
    if list(d.columns) != schema:
        raise ValueError("File does not match the expected nine-column schema.")
    if len(d) != 500 or d.isna().any().any() or not d.User_ID.is_unique:
        raise ValueError("Not the expected complete 500-customer comparison sample.")
    for col in ["Age", "Product_Browsing_Time", "Total_Pages_Viewed", "Items_Added_to_Cart", "Total_Purchases"]:
        if not pd.api.types.is_integer_dtype(d[col]) or d[col].min() < 0:
            raise ValueError("Unexpected counts in " + col)
    bought = d.Total_Purchases.gt(0)
    cart = d.Items_Added_to_Cart.gt(0)
    dims = {}
    for field in ["Gender", "Device_Type", "Location"]:
        grouped = d.assign(purchased=bought).groupby(field)
        agg = grouped.agg(customers=("User_ID", "count"), buyers=("purchased", "sum"),
                          mean_browsing=("Product_Browsing_Time", "mean"), mean_pages=("Total_Pages_Viewed", "mean"),
                          mean_cart=("Items_Added_to_Cart", "mean"), mean_purchases=("Total_Purchases", "mean"))
        dims[field] = json.loads(agg.round(6).to_json(orient="index"))
    corr = d[["Age", "Product_Browsing_Time", "Total_Pages_Viewed", "Items_Added_to_Cart", "Total_Purchases"]].corr()
    return {"sha256": hashlib.sha256(data).hexdigest(), "rows": len(d), "columns": len(schema),
            "missing_cells": int(d.isna().sum().sum()), "duplicate_rows": int(d.duplicated().sum()),
            "distinct_ids": int(d.User_ID.nunique()), "buyers": int(bought.sum()),
            "cart_and_buyer": int((cart & bought).sum()), "cart_and_nonbuyer": int((cart & ~bought).sum()),
            "no_cart_and_buyer": int((~cart & bought).sum()), "no_cart_and_nonbuyer": int((~cart & ~bought).sum()),
            "overall_means": d[schema[5:]].mean().round(6).to_dict(),
            "median_purchases": float(d.Total_Purchases.median()), "age_range": [int(d.Age.min()), int(d.Age.max())],
            "pearson_to_purchase_count": corr.Total_Purchases.iloc[:-1].round(6).to_dict(), "segments": dims}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("file", type=Path)
    args = p.parse_args()
    print(json.dumps(compare(args.file.read_bytes()), indent=2, sort_keys=True))
