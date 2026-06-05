"""
transform.py
============
Afficionado Coffee Roasters – Data Transformation Pipeline
-----------------------------------------------------------
Reads the raw Excel file and produces four CSV outputs:
  - data/CONSOLIDATED_ANALYSIS.csv   (80 products × 25 columns)
  - data/CATEGORY_SUMMARY.csv        (9 categories)
  - data/STORE_SUMMARY.csv           (3 stores)
  - data/SUMMARY_STATISTICS.csv      (key headline metrics)

Author : Ganapathi Kakarla
Version: 1.0
"""

import re
import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
RAW_FILE  = BASE_DIR / "data" / "Afficionado Coffee Roasters.xlsx"
OUT_DIR   = BASE_DIR / "data"

# ---------------------------------------------------------------------------
# 1. LOAD RAW DATA
# ---------------------------------------------------------------------------
print("Loading raw data …")
df = pd.read_excel(RAW_FILE)
print(f"  Loaded {len(df):,} rows × {df.shape[1]} columns")

# Normalise column names to snake_case
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\s+", "_", regex=True)
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# ---------------------------------------------------------------------------
# 2. TRANSACTION-LEVEL FEATURES
# ---------------------------------------------------------------------------
print("Engineering transaction-level features …")

# 2.1 Revenue
df["revenue"] = df["transaction_qty"] * df["unit_price"]

# 2.2 Hour extraction
df["transaction_time"] = pd.to_datetime(
    df["transaction_time"].astype(str), format="%H:%M:%S", errors="coerce"
)
df["hour"] = df["transaction_time"].dt.hour

# 2.3 Day-part classification
def classify_day_part(h):
    if h < 6:
        return "Night"
    elif h < 12:
        return "Morning"
    elif h < 18:
        return "Afternoon"
    else:
        return "Evening"

df["day_part"] = df["hour"].apply(classify_day_part)

# 2.4 Product size extraction (Sm / Rg / Lg from product_detail)
def extract_size(name: str) -> str:
    match = re.search(r"\b(Sm|Rg|Lg)\b", str(name))
    return match.group(1) if match else "Regular"

df["product_size"] = df["product_detail"].apply(extract_size)

# 2.5 Price category
def classify_price(p: float) -> str:
    if p <= 2:
        return "Budget"
    elif p <= 4:
        return "Standard"
    elif p <= 10:
        return "Premium"
    else:
        return "Luxury"

df["price_category"] = df["unit_price"].apply(classify_price)

# ---------------------------------------------------------------------------
# 3. PRODUCT-LEVEL AGGREGATIONS
# ---------------------------------------------------------------------------
print("Computing product-level aggregations …")

prod_agg = (
    df.groupby(
        ["product_id", "product_detail", "product_category", "product_type"],
        as_index=False,
    )
    .agg(
        total_revenue=("revenue", "sum"),
        total_units_sold=("transaction_qty", "sum"),
        transaction_count=("transaction_id", "count"),
        avg_unit_price=("unit_price", "mean"),
    )
)

total_rev = prod_agg["total_revenue"].sum()

# 3.5 Revenue share %
prod_agg["revenue_share_pct"] = (prod_agg["total_revenue"] / total_rev) * 100

# 3.6 Revenue rank (1 = highest)
prod_agg["revenue_rank"] = prod_agg["total_revenue"].rank(
    ascending=False, method="min"
).astype(int)

# 3.7 Volume rank
prod_agg["volume_rank"] = prod_agg["total_units_sold"].rank(
    ascending=False, method="min"
).astype(int)

# 3.8 Cumulative revenue (sorted by revenue desc)
prod_agg = prod_agg.sort_values("total_revenue", ascending=False).reset_index(drop=True)
prod_agg["cumulative_revenue"] = prod_agg["total_revenue"].cumsum()

# 3.9 Cumulative revenue %
prod_agg["cumulative_revenue_pct"] = (prod_agg["cumulative_revenue"] / total_rev) * 100

# 3.10 Efficiency score  E = 0.6 × (R / max_R) + 0.4 × (V / max_V)
max_rev = prod_agg["total_revenue"].max()
max_vol = prod_agg["total_units_sold"].max()
prod_agg["efficiency_score"] = (
    0.6 * (prod_agg["total_revenue"] / max_rev)
    + 0.4 * (prod_agg["total_units_sold"] / max_vol)
).round(4)

# 3.11 Performance tier
def perf_tier(score: float) -> str:
    if score >= 0.8:
        return "Hero"
    elif score >= 0.5:
        return "High"
    elif score >= 0.2:
        return "Medium"
    else:
        return "Low"

prod_agg["performance_tier"] = prod_agg["efficiency_score"].apply(perf_tier)

# 3.12 Pareto classification
prod_agg["pareto_class"] = prod_agg["cumulative_revenue_pct"].apply(
    lambda x: "Top_80%" if x <= 80 else "Long_Tail"
)

# ---------------------------------------------------------------------------
# 4. CATEGORY-LEVEL AGGREGATIONS
# ---------------------------------------------------------------------------
print("Computing category-level aggregations …")

cat_agg = (
    df.groupby("product_category", as_index=False)
    .agg(
        category_revenue=("revenue", "sum"),
        unique_products=("product_id", "nunique"),
    )
)
cat_agg["category_revenue_share_pct"] = (cat_agg["category_revenue"] / total_rev) * 100
cat_agg["avg_revenue_per_product"] = cat_agg["category_revenue"] / cat_agg["unique_products"]

# Merge into product table
prod_agg = prod_agg.merge(
    cat_agg[["product_category", "category_revenue", "category_revenue_share_pct",
             "unique_products", "avg_revenue_per_product"]],
    on="product_category",
    how="left",
)

# ---------------------------------------------------------------------------
# 5. PRODUCT-TYPE AGGREGATIONS
# ---------------------------------------------------------------------------
print("Computing product-type aggregations …")

type_agg = (
    df.groupby("product_type", as_index=False)
    .agg(type_revenue=("revenue", "sum"))
)
type_agg["type_revenue_share_pct"] = (type_agg["type_revenue"] / total_rev) * 100

prod_agg = prod_agg.merge(
    type_agg[["product_type", "type_revenue", "type_revenue_share_pct"]],
    on="product_type",
    how="left",
)

# ---------------------------------------------------------------------------
# 6. STORE-LEVEL AGGREGATIONS
# ---------------------------------------------------------------------------
print("Computing store-level aggregations …")

store_agg = (
    df.groupby("store_location", as_index=False)
    .agg(
        store_total_revenue=("revenue", "sum"),
        store_avg_revenue=("revenue", "mean"),
        store_transaction_count=("transaction_id", "count"),
    )
)
store_agg["store_revenue_share_pct"] = (
    store_agg["store_total_revenue"] / total_rev
) * 100

# Per-product per-store revenue (pivoted columns)
store_prod = (
    df.groupby(["product_id", "store_location"])["revenue"]
    .sum()
    .unstack(fill_value=0)
    .reset_index()
)
# Rename columns to safe names
store_prod.columns = (
    ["product_id"]
    + [
        "revenue_" + c.replace(" ", "_").replace("'", "")
        for c in store_prod.columns[1:]
    ]
)

prod_agg = prod_agg.merge(store_prod, on="product_id", how="left")

# ---------------------------------------------------------------------------
# 7. FINAL COLUMN ORDERING
# ---------------------------------------------------------------------------
id_cols    = ["product_id", "product_detail", "product_category", "product_type"]
perf_cols  = [
    "total_revenue", "revenue_share_pct", "revenue_rank",
    "total_units_sold", "volume_rank", "transaction_count",
    "avg_unit_price", "efficiency_score", "performance_tier",
]
cumul_cols = ["cumulative_revenue", "cumulative_revenue_pct", "pareto_class"]
cat_cols   = [
    "category_revenue", "category_revenue_share_pct",
    "unique_products", "avg_revenue_per_product",
]
type_cols  = ["type_revenue", "type_revenue_share_pct"]
store_cols = [c for c in prod_agg.columns if c.startswith("revenue_")]

final_cols = id_cols + perf_cols + cumul_cols + cat_cols + type_cols + store_cols
# Keep only columns that actually exist (safety net)
final_cols = [c for c in final_cols if c in prod_agg.columns]

consolidated = prod_agg[final_cols].copy()

# ---------------------------------------------------------------------------
# 8. WRITE OUTPUTS
# ---------------------------------------------------------------------------
print("Writing output CSVs …")

consolidated.to_csv(OUT_DIR / "CONSOLIDATED_ANALYSIS.csv", index=False)
print(f"  ✓ CONSOLIDATED_ANALYSIS.csv  ({consolidated.shape[0]} rows × {consolidated.shape[1]} columns)")

cat_agg.to_csv(OUT_DIR / "CATEGORY_SUMMARY.csv", index=False)
print(f"  ✓ CATEGORY_SUMMARY.csv       ({cat_agg.shape[0]} rows × {cat_agg.shape[1]} columns)")

store_agg.to_csv(OUT_DIR / "STORE_SUMMARY.csv", index=False)
print(f"  ✓ STORE_SUMMARY.csv          ({store_agg.shape[0]} rows × {store_agg.shape[1]} columns)")

# Summary statistics
summary = {
    "metric": [
        "total_revenue", "avg_transaction_value", "total_transactions",
        "unique_products", "hero_products", "low_products",
        "pareto_threshold_products", "top_category",
        "top_store", "top_store_revenue",
        "most_efficient_category", "least_efficient_category",
    ],
    "value": [
        round(total_rev, 2),
        round(df["revenue"].mean(), 2),
        len(df),
        consolidated["product_id"].nunique(),
        int((consolidated["performance_tier"] == "Hero").sum()),
        int((consolidated["performance_tier"] == "Low").sum()),
        int((consolidated["pareto_class"] == "Top_80%").sum()),
        cat_agg.loc[cat_agg["category_revenue"].idxmax(), "product_category"],
        store_agg.loc[store_agg["store_total_revenue"].idxmax(), "store_location"],
        round(store_agg["store_total_revenue"].max(), 2),
        cat_agg.loc[cat_agg["avg_revenue_per_product"].idxmax(), "product_category"],
        cat_agg.loc[cat_agg["avg_revenue_per_product"].idxmin(), "product_category"],
    ],
}
summary_df = pd.DataFrame(summary)
summary_df.to_csv(OUT_DIR / "SUMMARY_STATISTICS.csv", index=False)
print(f"  ✓ SUMMARY_STATISTICS.csv     ({summary_df.shape[0]} rows × {summary_df.shape[1]} columns)")

print("\nTransformation complete ✓")
