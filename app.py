import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="E-Commerce Signal Map", page_icon="🎯", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
.signal-card {padding: 1rem 1.1rem; border: 1px solid rgba(128,128,128,.22); border-radius: 14px; background: rgba(128,128,128,.06);}
.signal-label {font-size: .82rem; opacity: .72;}
.signal-value {font-size: 1.65rem; font-weight: 700; margin-top: .2rem;}
.insight {padding: 1rem 1.2rem; border-left: 4px solid #7c3aed; border-radius: 8px; background: rgba(124,58,237,.08);}
</style>
""", unsafe_allow_html=True)

st.title("🎯 E-Commerce Customer Signal Map")
st.caption("A 500-customer investigation into what the dataset actually says — and what it cannot tell us.")

uploaded = st.sidebar.file_uploader("Upload ecommerce_customer_data.csv", type="csv")
default_path = Path("ecommerce_customer_data.csv")
if uploaded is not None:
    df = pd.read_csv(uploaded)
elif default_path.exists():
    df = pd.read_csv(default_path)
else:
    st.info("Upload the dataset in the sidebar to explore the dashboard.")
    st.stop()

required = {"User_ID", "Gender", "Age", "Location", "Device_Type", "Product_Browsing_Time", "Total_Pages_Viewed", "Items_Added_to_Cart", "Total_Purchases"}
missing = required - set(df.columns)
if missing:
    st.error(f"Missing required columns: {', '.join(sorted(missing))}")
    st.stop()

purchased = df["Total_Purchases"] > 0
purchase_rate = purchased.mean() * 100
zero_purchase = int((~purchased).sum())
zero_cart = int((df["Items_Added_to_Cart"] == 0).sum())
avg_purchases = df["Total_Purchases"].mean()

c1, c2, c3, c4 = st.columns(4)
for col, label, value, note in [
    (c1, "Customers", f"{len(df):,}", "rows in dataset"),
    (c2, "Purchase rate", f"{purchase_rate:.1f}%", f"{len(df[purchased]):,} purchased"),
    (c3, "Avg. purchases", f"{avg_purchases:.2f}", "per customer"),
    (c4, "Zero-purchase", f"{zero_purchase:,}", f"{zero_cart:,} also had zero cart adds"),
]:
    col.markdown(f'<div class="signal-card"><div class="signal-label">{label}</div><div class="signal-value">{value}</div><div class="signal-label">{note}</div></div>', unsafe_allow_html=True)

st.sidebar.divider()
locations = st.sidebar.multiselect("Location", sorted(df["Location"].unique()), default=sorted(df["Location"].unique()))
devices = st.sidebar.multiselect("Device", sorted(df["Device_Type"].unique()), default=sorted(df["Device_Type"].unique()))
genders = st.sidebar.multiselect("Gender", sorted(df["Gender"].unique()), default=sorted(df["Gender"].unique()))

filtered = df[df["Location"].isin(locations) & df["Device_Type"].isin(devices) & df["Gender"].isin(genders)].copy()

st.subheader("The signal, not the template")
st.markdown('<div class="insight"><b>Headline finding:</b> browsing intensity is almost uncorrelated with purchases in this sample. More time, pages, or cart additions do not automatically translate into more purchases. Treat this as a descriptive finding — not a causal conclusion.</div>', unsafe_allow_html=True)

left, right = st.columns(2)
with left:
    loc = (filtered.groupby("Location").agg(Customers=("User_ID", "count"), Purchase_Rate=("Total_Purchases", lambda x: (x > 0).mean() * 100), Avg_Purchases=("Total_Purchases", "mean")).reset_index().sort_values("Purchase_Rate", ascending=False))
    fig = px.bar(loc, x="Purchase_Rate", y="Location", orientation="h", text=loc["Purchase_Rate"].map(lambda x: f"{x:.0f}%"), title="Purchase rate by location")
    fig.update_layout(height=390, xaxis_title="Purchase rate (%)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)
with right:
    dev = filtered.groupby("Device_Type").agg(Customers=("User_ID", "count"), Avg_Purchases=("Total_Purchases", "mean"), Purchase_Rate=("Total_Purchases", lambda x: (x > 0).mean() * 100)).reset_index().sort_values("Purchase_Rate", ascending=False)
    fig = px.bar(dev, x="Device_Type", y="Purchase_Rate", text=dev["Purchase_Rate"].map(lambda x: f"{x:.0f}%"), title="Purchase rate by device")
    fig.update_layout(height=390, yaxis_title="Purchase rate (%)", xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    fig = px.scatter(filtered, x="Product_Browsing_Time", y="Total_Purchases", size="Items_Added_to_Cart", color="Device_Type", hover_data=["Location", "Age"], title="Browsing time vs purchases")
    fig.update_layout(height=410, xaxis_title="Browsing time", yaxis_title="Total purchases")
    st.plotly_chart(fig, use_container_width=True)
with right:
    corr_cols = ["Age", "Product_Browsing_Time", "Total_Pages_Viewed", "Items_Added_to_Cart"]
    corr = filtered[corr_cols + ["Total_Purchases"]].corr(numeric_only=True)["Total_Purchases"].drop("Total_Purchases").reset_index()
    corr.columns = ["Metric", "Correlation"]
    corr["Metric"] = corr["Metric"].str.replace("_", " ")
    fig = px.bar(corr, x="Correlation", y="Metric", orientation="h", text=corr["Correlation"].map(lambda x: f"{x:.3f}"), title="Signal strength: correlation with purchases")
    fig.update_layout(height=410, xaxis_title="Pearson correlation", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer behavior profile")
profile = filtered.groupby("Gender").agg(Customers=("User_ID", "count"), Avg_Browsing=("Product_Browsing_Time", "mean"), Avg_Pages=("Total_Pages_Viewed", "mean"), Avg_Cart=("Items_Added_to_Cart", "mean"), Avg_Purchases=("Total_Purchases", "mean")).reset_index()
st.dataframe(profile.round(2), use_container_width=True, hide_index=True)

st.subheader("Questions worth investigating next")
st.markdown("- Why do some customers with cart activity still record no purchase?\n- Are returning customers, traffic sources, or campaigns stronger predictors than on-site activity?\n- Do particular location/device combinations behave differently?\n- Would repeat-purchase or cohort data reveal a stronger signal than this single customer snapshot?")

st.caption("Built as a portfolio analysis. Correlation is descriptive; it does not establish causation.")
