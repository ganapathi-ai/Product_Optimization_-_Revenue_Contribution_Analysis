import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
from scipy import stats

# ─────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Afficionado Coffee Roasters – Product Analytics",
    layout="wide",
    page_icon="☕",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────
# CUSTOM CSS – Coffee-Themed Branding
# ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp {
        background-color: #FDF6EC;
        color: #1A0A00 !important;
    }
    .stApp * {
        color: #1A0A00;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C1005 0%, #6F4E37 100%);
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] .stMarkdown {
        color: #F5E6D3 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #D4A96A !important;
        color: #1A0A00 !important;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 2px solid #D4A96A;
        border-radius: 12px;
        padding: 12px 16px;
        box-shadow: 0 3px 10px rgba(111,78,55,0.18);
    }
    [data-testid="stMetricLabel"] * {
        color: #5C3317 !important;
        font-weight: 700 !important;
        font-size: 0.88em !important;
    }
    [data-testid="stMetricValue"] * {
        color: #1A0A00 !important;
        font-weight: 800 !important;
        font-size: 1.15em !important;
    }
    [data-testid="stMetricDelta"] * {
        font-weight: 600 !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #EDD8B8;
        border-radius: 10px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #3B1A08 !important;
        font-weight: 700;
        padding: 6px 14px;
        background-color: transparent;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6F4E37 !important;
        color: #FDF6EC !important;
    }
    .stTabs [aria-selected="false"]:hover {
        background-color: #D4A96A !important;
        color: #1A0A00 !important;
    }

    h1 { color: #2C1005 !important; font-weight: 800 !important; }
    h2 { color: #3B1A08 !important; font-weight: 700 !important; }
    h3, h4 { color: #4A2512 !important; font-weight: 700 !important; }

    p, .stMarkdown p, .stMarkdown li, .stMarkdown span,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] * {
        color: #1A0A00 !important;
    }

    .stDataFrame {
        border: 2px solid #D4A96A;
        border-radius: 8px;
    }
    .stDataFrame td, .stDataFrame th,
    .stDataFrame [role="cell"], .stDataFrame [role="columnheader"],
    .stDataFrame span, .stDataFrame div {
        color: #1A0A00 !important;
        background-color: #FFFFFF !important;
    }
    .stDataFrame [role="columnheader"] {
        background-color: #F5E6D3 !important;
        color: #2C1005 !important;
        font-weight: 700 !important;
    }

    .dashboard-table-wrap {
        border: 2px solid #D4A96A;
        border-radius: 10px;
        background: #FFFFFF;
        overflow: auto;
        box-shadow: 0 3px 10px rgba(111,78,55,0.12);
    }
    .dashboard-table {
        width: 100%;
        border-collapse: collapse;
        color: #1A0A00 !important;
        background: #FFFFFF;
        font-size: 0.95rem;
    }
    .dashboard-table thead th {
        position: sticky;
        top: 0;
        z-index: 1;
        background: #F5E6D3;
        color: #2C1005 !important;
        border-bottom: 1px solid #D4A96A;
        padding: 0.7rem 0.8rem;
        text-align: left;
        font-weight: 700;
        white-space: nowrap;
    }
    .dashboard-table tbody td {
        color: #1A0A00 !important;
        background: #FFFFFF;
        border-bottom: 1px solid #F1E0C5;
        padding: 0.65rem 0.8rem;
        vertical-align: top;
    }
    .dashboard-table tbody tr:nth-child(even) td {
        background: #FFF8F0;
    }
    .dashboard-table tbody tr:hover td {
        background: #F9EFD9;
    }

    .stSelectbox label, .stMultiSelect label,
    .stSlider label, .stNumberInput label,
    label[data-testid="stWidgetLabel"] * {
        color: #1A0A00 !important;
        font-weight: 600 !important;
    }
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: #1A0A00 !important;
    }
    [data-baseweb="menu"] li {
        color: #1A0A00 !important;
    }
    .stSlider [data-testid="stTickBar"] * {
        color: #5C3317 !important;
    }

    hr { border-color: #D4A96A; border-width: 1.5px; }

    .stDownloadButton > button {
        background-color: #6F4E37;
        color: #FDF6EC !important;
        border-radius: 8px;
        border: none;
        font-weight: 700;
    }
    .stDownloadButton > button:hover {
        background-color: #2C1005;
        color: #FFFFFF !important;
    }

    .footer-text {
        text-align: center;
        color: #5C3317 !important;
        font-size: 0.82em;
        padding: 10px 0 4px 0;
    }

    .stat-box {
        background: #FFF8F0;
        border: 2px solid #D4A96A;
        border-radius: 8px;
        padding: 10px 16px;
        color: #1A0A00 !important;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: rgba(255, 248, 240, 0.14) !important;
        border: 1px solid #D4A96A !important;
        color: #FFF8F0 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-baseweb="select"] div,
    [data-testid="stSidebar"] [data-baseweb="select"] svg,
    [data-testid="stSidebar"] [data-baseweb="base-input"] input,
    [data-testid="stSidebar"] [data-baseweb="base-input"] span,
    [data-testid="stSidebar"] [data-baseweb="base-input"] div {
        color: #FFF8F0 !important;
        fill: #FFF8F0 !important;
        caret-color: #FFF8F0 !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] input::placeholder,
    [data-testid="stSidebar"] [data-baseweb="base-input"] input::placeholder {
        color: #F5E6D3 !important;
        opacity: 1 !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] * {
        color: #FFF3E0 !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] * {
        color: #F5E6D3 !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    script_dir = Path(__file__).parent if "__file__" in dir() else Path.cwd()
    data_path = script_dir / "data" / "CONSOLIDATED_ANALYSIS.csv"
    if not data_path.exists():
        data_path = Path("data") / "CONSOLIDATED_ANALYSIS.csv"
    return pd.read_csv(data_path)

df = load_data()

if df.empty:
    st.error("🚨 Data could not be loaded or the source file is empty. Please check the data source: `data/CONSOLIDATED_ANALYSIS.csv`")
    st.stop()

# ─────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────
st.title("☕ Afficionado Coffee Roasters")
st.header("Product Optimization & Revenue Contribution Analysis")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────────────────────────────
st.sidebar.markdown("## ☕ Dashboard Filters")

# 1. Product Category
selected_categories = st.sidebar.multiselect(
    "📦 Product Category",
    options=sorted(df["product_category"].unique()),
    default=sorted(df["product_category"].unique()),
    key="category_filter",
)

# 2. Product Type
selected_types = st.sidebar.multiselect(
    "🏷️ Product Type",
    options=sorted(df["product_type"].unique()),
    default=sorted(df["product_type"].unique()),
)

# 3. Store Location
selected_stores = st.sidebar.multiselect(
    "🏪 Store Location",
    options=["All Stores", "Astoria", "Hell's Kitchen", "Lower Manhattan"],
    default=["All Stores"],
)

# 4. Performance Tier
selected_tiers = st.sidebar.multiselect(
    "⭐ Performance Tier",
    options=["Hero", "High", "Medium", "Low"],
    default=["Hero", "High", "Medium", "Low"],
)

# 5. Top-N Slider
top_n = st.sidebar.slider("🔝 Top N Products", min_value=5, max_value=50, value=10, step=5)

# 6. Revenue Range
revenue_range = st.sidebar.slider(
    "💰 Revenue Range ($)",
    min_value=float(df["total_revenue"].min()),
    max_value=float(df["total_revenue"].max()),
    value=(float(df["total_revenue"].min()), float(df["total_revenue"].max())),
    step=500.0,
)

# 7. Volume Range
volume_range = st.sidebar.slider(
    "📊 Unit Volume Range",
    min_value=int(df["total_units_sold"].min()),
    max_value=int(df["total_units_sold"].max()),
    value=(int(df["total_units_sold"].min()), int(df["total_units_sold"].max())),
    step=100,
)

# 8. Efficiency Score Range
efficiency_range = st.sidebar.slider(
    "📈 Efficiency Score Range",
    min_value=0.0,
    max_value=1.0,
    value=(0.0, 1.0),
    step=0.05,
)

# ─────────────────────────────────────────────────────────────────
# STORE COLUMN MAP
# ─────────────────────────────────────────────────────────────────
store_name_to_col = {
    "Astoria": "revenue_Astoria",
    "Hell's Kitchen": "revenue_Hell's_Kitchen",
    "Lower Manhattan": "revenue_Lower_Manhattan",
}

# ─────────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────────
filtered_df = df[
    (df["product_category"].isin(selected_categories))
    & (df["product_type"].isin(selected_types))
    & (df["performance_tier"].isin(selected_tiers))
    & (df["total_revenue"] >= revenue_range[0])
    & (df["total_revenue"] <= revenue_range[1])
    & (df["total_units_sold"] >= volume_range[0])
    & (df["total_units_sold"] <= volume_range[1])
    & (df["efficiency_score"] >= efficiency_range[0])
    & (df["efficiency_score"] <= efficiency_range[1])
].copy()

if "All Stores" not in selected_stores and selected_stores:
    store_cols = [store_name_to_col[s] for s in selected_stores if s in store_name_to_col]
    filtered_df = filtered_df[filtered_df[store_cols].sum(axis=1) > 0]

# ─────────────────────────────────────────────────────────────────
# KPI STRIP
# ─────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.metric("💰 Total Revenue", f"${filtered_df['total_revenue'].sum():,.2f}")
with c2:
    st.metric("📦 Products", f"{len(filtered_df)}")
with c3:
    st.metric("⭐ Hero Products", f"{(filtered_df['performance_tier']=='Hero').sum()}")
with c4:
    st.metric("📈 Avg Efficiency", f"{filtered_df['efficiency_score'].mean():.3f}")
with c5:
    st.metric("📊 Avg Volume", f"{filtered_df['total_units_sold'].mean():,.0f}")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────
# COLOUR MAP — consistent across all charts
# ─────────────────────────────────────────────────────────────────
TIER_COLORS = {
    "Hero":   "#D97706",   # amber — visible on cream
    "High":   "#16A34A",   # deep green
    "Medium": "#2563EB",   # deep blue
    "Low":    "#DC2626",   # strong red
}

# Global Plotly chart layout — dark text on white/cream backgrounds
CHART_LAYOUT = dict(
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FAFAFA",
    font=dict(color="#1A0A00", family="Arial, sans-serif", size=13),
    title_font=dict(color="#2C1005", size=16, family="Arial Black, sans-serif"),
    legend=dict(
        font=dict(color="#1A0A00"),
        bgcolor="#FDF6EC",
        bordercolor="#D4A96A",
        borderwidth=1,
    ),
    margin=dict(t=60, b=50, l=50, r=30),
)

# Safe: always identical to CHART_LAYOUT (no xaxis/yaxis in base dict)
CHART_LAYOUT_BASE = CHART_LAYOUT

# Axis style kwargs — apply via update_xaxes()/update_yaxes() to avoid conflicts
_AXIS_STYLE = dict(
    color="#1A0A00",
    tickfont=dict(color="#1A0A00"),
    title_font=dict(color="#2C1005"),
    gridcolor="#EDD8B8",
    linecolor="#8B6246",
)

def apply_chart_style(fig):
    """Apply dark-text axis styling and global layout to any Plotly figure."""
    fig.update_layout(**CHART_LAYOUT)
    fig.update_xaxes(**_AXIS_STYLE)
    fig.update_yaxes(**_AXIS_STYLE)
    return fig


def render_visible_table(dataframe, *, height=400):
    """Render tables with guaranteed readable text on all themed backgrounds."""
    if dataframe.empty:
        st.info("No data available to display.")
        return

    html_table = dataframe.to_html(index=False, classes="dashboard-table", border=0, escape=False)
    st.markdown(
        (
            f"<div class='dashboard-table-wrap' style='max-height:{height}px;'>"
            f"{html_table}"
            "</div>"
        ),
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Product Rankings",
    "🎯 Revenue Contribution",
    "📈 Popularity vs Revenue",
    "📊 Pareto Analysis",
    "🏪 Store Performance",
    "🔍 Product Details",
    "📥 Data Export",
])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — PRODUCT RANKINGS
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Product Performance Rankings")
    st.markdown("Rank products across four dimensions: **Volume · Revenue · Efficiency · Transaction Frequency**")
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### 🔝 Top Products by Sales Volume")
            vol_data = (
                filtered_df.nlargest(top_n, "total_units_sold")[
                    ["product_detail", "product_category", "total_units_sold", "performance_tier"]
                ]
                .copy()
            )
            fig = px.bar(
                vol_data, x="total_units_sold", y="product_detail", orientation="h",
                color="performance_tier", color_discrete_map=TIER_COLORS,
                labels={"total_units_sold": "Units Sold", "product_detail": "Product", "performance_tier": "Tier"},
            )
            fig.update_traces(
                customdata=vol_data[["product_category", "performance_tier"]].to_numpy(),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Units Sold: %{x:,.0f}<br>"
                    "Category: %{customdata[0]}<br>"
                    "Performance Tier: %{customdata[1]}<extra></extra>"
                ),
            )
            fig.update_layout(
                height=500,
                showlegend=True,
                title="Top Products by Sales Volume",
                legend_title_text="Performance Tier",
                yaxis={"categoryorder": "total ascending"},
            )
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)

        with c2:
            st.markdown("#### 💰 Top Products by Revenue")
            rev_data = (
                filtered_df.nlargest(top_n, "total_revenue")[
                    ["product_detail", "product_category", "total_revenue", "revenue_share_pct", "performance_tier"]
                ]
                .copy()
            )
            fig = px.bar(
                rev_data, x="total_revenue", y="product_detail", orientation="h",
                color="performance_tier", color_discrete_map=TIER_COLORS,
                labels={"total_revenue": "Revenue ($)", "product_detail": "Product", "performance_tier": "Tier"},
            )
            fig.update_traces(
                customdata=rev_data[["product_category", "revenue_share_pct", "performance_tier"]].to_numpy(),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Revenue: $%{x:,.2f}<br>"
                    "Category: %{customdata[0]}<br>"
                    "Revenue Share: %{customdata[1]:.2f}%<br>"
                    "Performance Tier: %{customdata[2]}<extra></extra>"
                ),
            )
            fig.update_layout(
                height=500,
                showlegend=True,
                title="Top Products by Revenue",
                legend_title_text="Performance Tier",
                yaxis={"categoryorder": "total ascending"},
            )
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)

        c3, c4 = st.columns(2)

        with c3:
            st.markdown("#### ⭐ Top Products by Efficiency Score")
            eff_data = (
                filtered_df.nlargest(top_n, "efficiency_score")[
                    ["product_detail", "product_category", "efficiency_score", "performance_tier"]
                ]
                .copy()
            )
            fig = px.bar(
                eff_data, x="efficiency_score", y="product_detail", orientation="h",
                color="performance_tier", color_discrete_map=TIER_COLORS,
                labels={"efficiency_score": "Efficiency Score", "product_detail": "Product", "performance_tier": "Tier"},
            )
            fig.update_traces(
                customdata=eff_data[["product_category", "performance_tier"]].to_numpy(),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Efficiency Score: %{x:.3f}<br>"
                    "Category: %{customdata[0]}<br>"
                    "Performance Tier: %{customdata[1]}<extra></extra>"
                ),
            )
            fig.update_layout(
                height=500,
                showlegend=False,
                title="Top Products by Efficiency Score",
                yaxis={"categoryorder": "total ascending"},
            )
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)

        with c4:
            st.markdown("#### 🔄 Top Products by Transaction Frequency")
            txn_data = (
                filtered_df.nlargest(top_n, "transaction_count")[
                    ["product_detail", "product_category", "transaction_count", "performance_tier"]
                ]
                .copy()
            )
            fig = px.bar(
                txn_data, x="transaction_count", y="product_detail", orientation="h",
                color="performance_tier", color_discrete_map=TIER_COLORS,
                labels={"transaction_count": "Transactions", "product_detail": "Product", "performance_tier": "Tier"},
            )
            fig.update_traces(
                customdata=txn_data[["product_category", "performance_tier"]].to_numpy(),
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Transactions: %{x:,.0f}<br>"
                    "Category: %{customdata[0]}<br>"
                    "Performance Tier: %{customdata[1]}<extra></extra>"
                ),
            )
            fig.update_layout(
                height=500,
                showlegend=False,
                title="Top Products by Transaction Frequency",
                yaxis={"categoryorder": "total ascending"},
            )
            st.plotly_chart(apply_chart_style(fig), use_container_width=True)

        st.markdown("#### 📋 Complete Rankings Table")
        tbl = (
            filtered_df[
                [
                    "product_detail", "product_category", "performance_tier",
                    "total_revenue", "revenue_rank", "total_units_sold", "volume_rank",
                    "efficiency_score", "transaction_count",
                ]
            ]
            .copy()
            .sort_values("total_revenue", ascending=False)
        )
        tbl.columns = ["Product", "Category", "Tier", "Revenue ($)", "Rev Rank", "Units Sold", "Vol Rank", "Efficiency", "Transactions"]
        tbl["Revenue ($)"] = tbl["Revenue ($)"].map("${:,.2f}".format)
        render_visible_table(tbl, height=400)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — REVENUE CONTRIBUTION
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("Revenue Contribution Analysis")
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        c1, c2 = st.columns([2, 1])

        with c1:
            st.markdown("#### 🎯 Revenue Share by Category & Product (Treemap)")
            treemap_data = filtered_df.nlargest(20, "total_revenue")
            if not treemap_data.empty:
                fig = px.treemap(
                    treemap_data,
                    path=["product_category", "product_detail"],
                    values="total_revenue",
                    color="efficiency_score",
                    color_continuous_scale="RdYlGn",
                    hover_data={"total_revenue": ":,.2f", "revenue_share_pct": ":.2f"},
                    labels={"efficiency_score": "Efficiency", "total_revenue": "Revenue ($)"},
                )
                fig.update_traces(
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Category: %{parent}<br>"
                        "Revenue: $%{value:,.2f}<br>"
                        "Efficiency Score: %{color:.3f}<extra></extra>"
                    ),
                    root_color="#F5E6D3",
                )
                fig.update_layout(height=480, title="Revenue Contribution by Category and Product")
                st.plotly_chart(apply_chart_style(fig), use_container_width=True)
            else:
                st.info("No data to display for the treemap with the current filters.")

        with c2:
            st.markdown("#### 💰 Top 10 Revenue Contributors")
            top10 = (
                filtered_df.nlargest(10, "total_revenue")[
                    ["product_detail", "total_revenue", "revenue_share_pct", "efficiency_score"]
                ]
                .copy()
            )
            if not top10.empty:
                top10["total_revenue"] = top10["total_revenue"].apply(lambda x: f"${x:,.0f}")
                top10["revenue_share_pct"] = top10["revenue_share_pct"].apply(lambda x: f"{x:.2f}%")
                top10["efficiency_score"] = top10["efficiency_score"].apply(lambda x: f"{x:.3f}")
                top10.columns = ["Product", "Revenue", "Share %", "Efficiency"]
                render_visible_table(top10, height=460)
            else:
                st.info("No data to display for top 10 revenue contributors with the current filters.")

        st.markdown("---")
        st.markdown("#### 📊 Category Revenue Distribution")

        cat_data = (
            filtered_df.groupby("product_category")
            .agg(total_revenue=("total_revenue", "sum"), unique_products=("product_id", "count"),
                 avg_efficiency=("efficiency_score", "mean"))
            .reset_index()
            .sort_values("total_revenue", ascending=True)
        )
        
        if cat_data.empty:
            st.info("No category data to display for the current filters.")
        else:
            total_cat_revenue = cat_data["total_revenue"].sum()
            if total_cat_revenue > 0:
                cat_data["revenue_pct"] = (cat_data["total_revenue"] / total_cat_revenue * 100).round(2)
            else:
                cat_data["revenue_pct"] = 0

            col_pie, col_bar = st.columns(2)

            with col_pie:
                fig = px.pie(
                    cat_data, values="total_revenue", names="product_category",
                    color_discrete_sequence=px.colors.sequential.Oranges_r,
                    hole=0.35,
                )
                fig.update_traces(textposition="inside", textinfo="percent+label",
                                  textfont=dict(color="#1A0A00", size=12),
                                  hovertemplate=(
                                      "<b>%{label}</b><br>"
                                      "Revenue: $%{value:,.2f}<br>"
                                      "Share: %{percent}<extra></extra>"
                                  ))
                fig.update_layout(height=420, showlegend=False, title="Category Revenue Share")
                apply_chart_style(fig)
                st.plotly_chart(fig, use_container_width=True)

            with col_bar:
                fig = px.bar(
                    cat_data, x="total_revenue", y="product_category", orientation="h",
                    color="total_revenue", color_continuous_scale="Oranges",
                    text=cat_data["revenue_pct"].apply(lambda x: f"{x:.1f}%"),
                    labels={"total_revenue": "Revenue ($)", "product_category": "Category"},
                )
                fig.update_traces(
                    textposition="outside",
                    textfont=dict(color="#1A0A00"),
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Revenue: $%{x:,.2f}<br>"
                        "Share: %{text}<extra></extra>"
                    ),
                )
                fig.update_coloraxes(showscale=False)
                fig.update_layout(height=420, title="Category Revenue Ranking")
                fig.update_yaxes(categoryorder="total ascending")
                apply_chart_style(fig)
                st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — POPULARITY vs REVENUE (SCATTER)
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("Popularity vs. Revenue — Scatter Analysis")
    st.markdown("**Size** = Efficiency Score | **Color** = Performance Tier | "
                "**Axes** = Units Sold × Total Revenue")

    if filtered_df.empty:
        st.warning("No data available for the selected filters to display this analysis.")
    else:
        scat = filtered_df.copy()

        # Pearson correlation
        if len(scat) >= 3:
            r_val, p_val = stats.pearsonr(scat["total_units_sold"], scat["total_revenue"])
        else:
            r_val, p_val = float("nan"), float("nan")

        # Scale efficiency for bubble size (avoid 0-size bubbles)
        scat["bubble_size"] = (scat["efficiency_score"] * 38 + 4).clip(lower=4)

        fig = px.scatter(
            scat,
            x="total_units_sold",
            y="total_revenue",
            size="bubble_size",
            color="performance_tier",
            hover_name="product_detail",
            custom_data=["efficiency_score", "product_category", "performance_tier"],
            hover_data={
                "total_units_sold": ":,.0f",
                "total_revenue": ":,.2f",
                "efficiency_score": ":.3f",
                "product_category": True,
                "bubble_size": False,
            },
            color_discrete_map=TIER_COLORS,
            labels={"total_units_sold": "Units Sold", "total_revenue": "Revenue ($)", "performance_tier": "Tier"},
            size_max=42,
        )
        fig.update_traces(
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Units Sold: %{x:,.0f}<br>"
                "Revenue: $%{y:,.2f}<br>"
                "Efficiency Score: %{customdata[0]:.3f}<br>"
                "Category: %{customdata[1]}<br>"
                "Performance Tier: %{customdata[2]}<extra></extra>"
            )
        )

        # Median reference lines
        med_vol = scat["total_units_sold"].median()
        med_rev = scat["total_revenue"].median()
        med_vol_label = f"{med_vol:,.1f}" if not float(med_vol).is_integer() else f"{med_vol:,.0f}"
        fig.add_vline(x=med_vol, line_dash="dot", line_color="#8B6246",
                      annotation_text=f"Median Volume={med_vol_label}", annotation_position="top right")
        fig.add_hline(y=med_rev, line_dash="dot", line_color="#8B6246",
                      annotation_text=f"Median Revenue=${med_rev:,.0f}", annotation_position="top right")

        fig.update_layout(
            height=580,
            title="Volume vs. Revenue: Product Performance Distribution",
        )
        apply_chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)

        # Statistical annotation
        if not np.isnan(r_val):
            sig = "significant" if p_val < 0.05 else "not significant"
            stat_color = "#15803D" if p_val < 0.05 else "#B91C1C"
            st.markdown(
                f"<div style='background:#FFFFFF;border:2px solid #D4A96A;border-radius:8px;"
                f"padding:10px 16px;color:#1A0A00;'>"
                f"📐 <b style='color:#2C1005'>Pearson Correlation (Volume × Revenue):</b> "
                f"<span style='color:{stat_color};font-size:1.08em;font-weight:700'>r = {r_val:.4f}</span>"
                f"&nbsp;|&nbsp; "
                f"<span style='color:#1A0A00'>p-value = {p_val:.4e}</span>&nbsp;|&nbsp; "
                f"<i style='color:#4A2512'>Statistically {sig} (α = 0.05)</i>&nbsp;|&nbsp; "
                f"<span style='color:#1A0A00'>n = {len(scat)} products</span>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("#### 📍 Quadrant Analysis (Median-Based Boundaries)")

        q1 = scat[(scat["total_units_sold"] >= med_vol) & (scat["total_revenue"] >= med_rev)]
        q2 = scat[(scat["total_units_sold"] < med_vol) & (scat["total_revenue"] >= med_rev)]
        q3 = scat[(scat["total_units_sold"] < med_vol) & (scat["total_revenue"] < med_rev)]
        q4 = scat[(scat["total_units_sold"] >= med_vol) & (scat["total_revenue"] < med_rev)]

        qc1, qc2, qc3, qc4 = st.columns(4)
        with qc1:
            st.metric("⭐ Hero Zone (High Vol, High Rev)", f"{len(q1)} products", f"${q1['total_revenue'].sum():,.0f}")
        with qc2:
            st.metric("💎 Premium (Low Vol, High Rev)", f"{len(q2)} products", f"${q2['total_revenue'].sum():,.0f}")
        with qc3:
            st.metric("❌ Rationalize (Low Vol, Low Rev)", f"{len(q3)} products", f"${q3['total_revenue'].sum():,.0f}")
        with qc4:
            st.metric("📦 Volume Drivers (High Vol, Low Rev)", f"{len(q4)} products", f"${q4['total_revenue'].sum():,.0f}")

# ══════════════════════════════════════════════════════════════════
# TAB 4 — PARETO ANALYSIS
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("Revenue Concentration & Pareto Analysis (80/20 Rule)")

    if filtered_df.empty:
        st.warning("No data available for the selected filters to perform Pareto analysis.")
    else:
        # Recompute Pareto statistics from the filtered view so the chart and summary
        # reflect the data currently on screen rather than the global precomputed ranks.
        pareto_data = filtered_df.sort_values(
            ["total_revenue", "product_detail"], ascending=[False, True]
        ).copy()
        pareto_total_revenue = pareto_data["total_revenue"].sum()
        pareto_data["pareto_revenue_rank"] = (
            pareto_data["total_revenue"].rank(method="min", ascending=False).astype(int)
        )
        pareto_data["pareto_cumulative_revenue"] = pareto_data["total_revenue"].cumsum()
        pareto_data["pareto_cumulative_revenue_pct"] = (
            pareto_data["pareto_cumulative_revenue"] / pareto_total_revenue * 100
        )
        pareto_data["pareto_revenue_share_pct"] = (
            pareto_data["total_revenue"] / pareto_total_revenue * 100
        )
        pareto_data["pareto_filtered_class"] = np.where(
            pareto_data["pareto_cumulative_revenue_pct"] <= 80, "Top_80%", "Long_Tail"
        )

        if pareto_data.empty:
            st.warning("No products available after sorting for Pareto analysis.")
        else:
            pc1, pc2, pc3 = st.columns(3)
            with pc1:
                p80 = len(pareto_data[pareto_data["pareto_filtered_class"] == "Top_80%"])
                st.metric("📊 Products Driving 80% Revenue", f"{p80}  ({p80/len(pareto_data)*100:.1f}%)")
            with pc2:
                top10_share = pareto_data.head(10)["total_revenue"].sum() / pareto_total_revenue * 100
                st.metric("🔝 Top 10 Products Revenue Share", f"{top10_share:.2f}%")
            with pc3:
                lt = len(pareto_data[pareto_data["pareto_filtered_class"] == "Long_Tail"])
                st.metric("📉 Long-Tail Products", f"{lt}  ({lt/len(pareto_data)*100:.1f}%)")

            st.markdown("---")
            st.markdown("#### 📈 Cumulative Revenue Curve (Pareto Chart) — Top 40 Products")

            top40 = pareto_data.head(40)

            if top40.empty:
                st.info("Not enough products to display the Pareto chart.")
            else:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=top40["pareto_revenue_rank"],
                    y=top40["total_revenue"],
                    name="Product Revenue",
                    marker_color="#D2691E",
                    yaxis="y1",
                    hovertemplate="Rank %{x}<br>Revenue: $%{y:,.2f}<extra></extra>",
                ))
                fig.add_trace(go.Scatter(
                    x=top40["pareto_revenue_rank"],
                    y=top40["pareto_cumulative_revenue_pct"],
                    name="Cumulative Revenue Share",
                    yaxis="y2",
                    line=dict(color="#3B1A08", width=3),
                    mode="lines+markers",
                    marker=dict(size=6),
                    hovertemplate="Rank %{x}<br>Cumulative: %{y:.1f}%<extra></extra>",
                ))
                fig.add_hline(
                    y=80, line_dash="dash", line_color="red",
                    annotation_text="80% Revenue Threshold", yref="y2",
                    annotation_position="top right",
                )
                fig.update_layout(
                    yaxis=dict(title="Revenue per Product ($)", color="#1A0A00",
                               tickfont=dict(color="#1A0A00"), title_font=dict(color="#2C1005"),
                               gridcolor="#EDD8B8"),
                    yaxis2=dict(title="Cumulative Revenue %", overlaying="y", side="right",
                                range=[0, 105], color="#1A0A00",
                                tickfont=dict(color="#1A0A00"), title_font=dict(color="#2C1005")),
                    xaxis=dict(title="Product Rank (by Revenue)", color="#1A0A00",
                               tickfont=dict(color="#1A0A00"), title_font=dict(color="#2C1005"),
                               gridcolor="#EDD8B8"),
                    height=520,
                    hovermode="x unified",
                    title="Pareto Analysis: Revenue Distribution Concentration",
                    legend=dict(x=0.02, y=0.98, font=dict(color="#1A0A00"),
                                bgcolor="#FDF6EC", bordercolor="#D4A96A", borderwidth=1),
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#FAFAFA",
                    font=dict(color="#1A0A00", family="Arial, sans-serif", size=13),
                    margin=dict(t=60, b=50, l=50, r=30),
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            st.markdown("#### 📊 Pareto Classification Summary")
            pareto_stats = pd.DataFrame({
                "Classification": ["Top 80%", "Long-Tail"],
                "Product Count": [
                    len(pareto_data[pareto_data["pareto_filtered_class"] == "Top_80%"]),
                    len(pareto_data[pareto_data["pareto_filtered_class"] == "Long_Tail"]),
                ],
                "Total Revenue ($)": [
                    f"${pareto_data[pareto_data['pareto_filtered_class']=='Top_80%']['total_revenue'].sum():,.2f}",
                    f"${pareto_data[pareto_data['pareto_filtered_class']=='Long_Tail']['total_revenue'].sum():,.2f}",
                ],
                "Revenue Share (%)": [
                    f"{pareto_data[pareto_data['pareto_filtered_class']=='Top_80%']['pareto_revenue_share_pct'].sum():.2f}%",
                    f"{pareto_data[pareto_data['pareto_filtered_class']=='Long_Tail']['pareto_revenue_share_pct'].sum():.2f}%",
                ],
                "% of Products": [
                    f"{len(pareto_data[pareto_data['pareto_filtered_class']=='Top_80%'])/len(pareto_data)*100:.1f}%",
                    f"{len(pareto_data[pareto_data['pareto_filtered_class']=='Long_Tail'])/len(pareto_data)*100:.1f}%",
                ],
            })
            render_visible_table(pareto_stats, height=220)

# ══════════════════════════════════════════════════════════════════
# TAB 5 — STORE PERFORMANCE
# ══════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("Store Performance Comparison Analysis")

    analysis_stores = st.multiselect(
        "🏪 Select Stores to Compare",
        options=list(store_name_to_col.keys()),
        default=list(store_name_to_col.keys()),
    )
    
    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        store_revenues = {
            s: filtered_df[store_name_to_col[s]].sum()
            for s in analysis_stores
        }
        total_store_rev = sum(store_revenues.values())

        sc1, sc2, sc3 = st.columns(3)
        cols_list = [sc1, sc2, sc3]
        all_stores = ["Astoria", "Hell's Kitchen", "Lower Manhattan"]
        for idx, store in enumerate(all_stores):
            if store in analysis_stores:
                rev = store_revenues.get(store, 0)
                pct = rev / total_store_rev * 100 if total_store_rev > 0 else 0
                with cols_list[idx]:
                    st.metric(f"🏪 {store}", f"${rev:,.2f}", f"{pct:.2f}% share")

        st.markdown("---")
        st.markdown("#### 📊 Revenue Distribution by Store")

        store_df = pd.DataFrame([
            {"Store": s, "Revenue ($)": store_revenues[s],
             "Share (%)": store_revenues[s] / total_store_rev * 100 if total_store_rev else 0}
            for s in analysis_stores
        ])

        fig = px.bar(
            store_df, x="Store", y="Revenue ($)",
            color="Store",
            text=store_df["Share (%)"].apply(lambda x: f"{x:.2f}%"),
            color_discrete_sequence=["#6F4E37", "#D2691E", "#DEB887"],
            labels={"Revenue ($)": "Total Revenue ($)"},
        )
        fig.update_traces(
            textposition="outside",
            textfont=dict(color="#1A0A00"),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Revenue: $%{y:,.2f}<br>"
                "Share: %{text}<extra></extra>"
            ),
        )
        fig.update_layout(height=400, showlegend=False, title="Store Revenue Distribution")
        apply_chart_style(fig)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.markdown("#### 🏆 Top 5 Products by Store")

        store_cols_map = {s: store_name_to_col[s] for s in analysis_stores}
        disp_cols = st.columns(len(analysis_stores)) if analysis_stores else []

        for idx, store in enumerate(analysis_stores):
            with disp_cols[idx]:
                st.markdown(f"**{store}**")
                scol = store_cols_map[store]
                top5 = (
                    filtered_df[["product_detail", "product_category", scol]]
                    .nlargest(5, scol)
                    .copy()
                )
                if top5.empty or top5[scol].sum() == 0:
                    st.info("No revenue for this store in filtered data.")
                else:
                    top5[scol] = top5[scol].apply(lambda x: f"${x:,.2f}")
                    top5.columns = ["Product", "Category", f"{store} Revenue"]
                    render_visible_table(top5, height=260)

# ══════════════════════════════════════════════════════════════════
# TAB 6 — PRODUCT DRILL-DOWN
# ══════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("Product Drill-Down – Individual Performance View")
    
    if filtered_df.empty:
        st.warning("No products match the current filters.")
    else:
        product_select = st.selectbox(
            "🔍 Select Product for Detailed Analysis",
            options=sorted(filtered_df["product_detail"].unique()),
        )

        prod_df = filtered_df[filtered_df["product_detail"] == product_select]

        if prod_df.empty:
            st.warning(f"Could not find details for product: '{product_select}'.")
            st.stop()

        prod = prod_df.iloc[0]

        dc1, dc2, dc3 = st.columns(3)
        with dc1:
            st.markdown("#### 📋 Product Identity")
            st.write(f"**Name:** {prod['product_detail']}")
            st.write(f"**Category:** {prod['product_category']}")
            st.write(f"**Type:** {prod['product_type']}")
            st.write(f"**Tier:** {prod['performance_tier']}")
            st.write(f"**Pareto Class:** {prod['pareto_class']}")

        with dc2:
            st.markdown("#### 💰 Revenue Metrics")
            st.metric("Total Revenue", f"${prod['total_revenue']:,.2f}")
            st.metric("Revenue Share", f"{prod['revenue_share_pct']:.2f}%")
            st.metric("Revenue Rank", f"#{int(prod['revenue_rank'])}")
            st.metric("Avg Unit Price", f"${prod['avg_unit_price']:.2f}")

        with dc3:
            st.markdown("#### 📦 Volume Metrics")
            st.metric("Units Sold", f"{int(prod['total_units_sold']):,}")
            st.metric("Volume Rank", f"#{int(prod['volume_rank'])}")
            st.metric("Transactions", f"{int(prod['transaction_count']):,}")
            st.metric("Efficiency Score", f"{prod['efficiency_score']:.3f}")

        st.markdown("---")

        da1, da2 = st.columns(2)

        with da1:
            st.markdown("#### ⭐ Category Positioning")
            cat_group = filtered_df[filtered_df["product_category"] == prod["product_category"]]
            cat_avg_eff = cat_group["efficiency_score"].mean()
            percentile = (df["efficiency_score"] <= prod["efficiency_score"]).sum() / len(df) * 100
            
            cat_ranks = cat_group["total_revenue"].rank(method="min", ascending=False)
            cat_rank = int(cat_ranks.get(prod.name, -1))

            st.metric("Category Avg Efficiency", f"{cat_avg_eff:.3f}")
            st.metric("Global Efficiency Percentile", f"{percentile:.0f}th")
            st.metric("Rank Within Category", f"#{cat_rank} of {len(cat_group)}" if cat_rank != -1 else "N/A")

        with da2:
            st.markdown("#### 🏪 Store-Level Revenue Breakdown")
            store_vals = {
                store: float(prod.get(store_name_to_col[store], 0))
                for store in store_name_to_col
            }
            store_bk = pd.DataFrame({
                "Store": list(store_vals.keys()),
                "Revenue": list(store_vals.values()),
            })
            fig = px.bar(
                store_bk, x="Store", y="Revenue",
                color="Store",
                color_discrete_sequence=["#6F4E37", "#D2691E", "#DEB887"],
                text=store_bk["Revenue"].apply(lambda x: f"${x:,.2f}"),
                labels={"Revenue": "Revenue ($)"},
            )
            fig.update_traces(
                textposition="outside",
                textfont=dict(color="#1A0A00"),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Revenue: $%{y:,.2f}<extra></extra>"
                ),
            )
            fig.update_layout(height=300, showlegend=False, title="Store Revenue Breakdown")
            fig.update_yaxes(tickprefix="$")
            apply_chart_style(fig)
            st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# TAB 7 — DATA EXPORT
# ══════════════════════════════════════════════════════════════════
with tab7:
    st.subheader("Consolidated Product Analysis Data & Exports")
    st.markdown("Complete dataset with all analytical metrics — sortable, filterable, downloadable.")

    disp = (
        filtered_df[[
            "product_detail", "product_category", "product_type", "performance_tier",
            "total_revenue", "revenue_share_pct", "revenue_rank",
            "total_units_sold", "volume_rank", "efficiency_score",
            "pareto_class", "transaction_count", "avg_unit_price",
        ]]
        .copy()
        .sort_values("total_revenue", ascending=False)
    )
    disp.columns = [
        "Product", "Category", "Type", "Tier",
        "Revenue ($)", "Share %", "Rev Rank",
        "Units Sold", "Vol Rank", "Efficiency",
        "Pareto", "Transactions", "Avg Price ($)",
    ]
    render_visible_table(disp, height=560)

    st.markdown("---")
    st.markdown("#### 📥 Download Options")

    dl1 = st.columns(1)[0]

    with dl1:
        csv_filtered = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_filtered,
            file_name="afficionado_filtered_analysis.csv",
            mime="text/csv",
        )

# ─────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────
st.markdown("---")

