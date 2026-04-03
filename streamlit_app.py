import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from pathlib import Path

st.set_page_config(page_title="Product Optimization Dashboard", layout="wide", page_icon="☕")

# Load consolidated data (cloud-compatible path handling)
@st.cache_data
def load_data():
    # Use pathlib for OS-independent path handling
    script_dir = Path(__file__).parent if '__file__' in dir() else Path.cwd()
    data_path = script_dir / 'data' / 'CONSOLIDATED_ANALYSIS.csv'
    
    # Try alternate path if running from different working directory
    if not data_path.exists():
        data_path = Path('data') / 'CONSOLIDATED_ANALYSIS.csv'
    
    consolidated = pd.read_csv(data_path)
    return consolidated

df = load_data()

# Header
st.title("☕ Afficionado Coffee Roasters")
st.header("Product Optimization & Revenue Contribution Analysis")
st.markdown("**Interactive Dashboard for Data-Driven Menu Decisions** | Powered by Comprehensive Product Analytics")
st.markdown("---")

# ============================================================================
# SIDEBAR FILTERS (PRD REQUIREMENT: Comprehensive Filtering)
# ============================================================================
st.sidebar.header("🔍 Filters")

# Filter 1: Product Category Filter (Multi-select)
selected_categories = st.sidebar.multiselect(
    "📦 Product Category",
    options=sorted(df['product_category'].unique()),
    default=sorted(df['product_category'].unique()),
    key="category_filter",
    help="Filter by product category"
)

selected_types = st.sidebar.multiselect(
    "🏷️ Product Type",
    options=sorted(df['product_category'].unique()),
    default=sorted(df['product_category'].unique())
)

# Filter 2: Product Type Filter (Multi-select)
selected_types = st.sidebar.multiselect(
    "Product Type",
    options=sorted(df['product_type'].unique()),
    default=sorted(df['product_type'].unique())
)

# Filter 3: Store Location Selector (Multi-select)
selected_stores = st.sidebar.multiselect(
    "Store Location",
    options=['All Stores', 'Astoria', 'Hell\'s Kitchen', 'Lower Manhattan'],
    default='All Stores'
)

# Filter 4: Performance Tier Filter
selected_tiers = st.sidebar.multiselect(
    "⭐ Performance Tier",
    options=['Hero', 'High', 'Medium', 'Low'],
    default=['Hero', 'High', 'Medium', 'Low']
)

# Filter 5: Top-N Slider
top_n = st.sidebar.slider("🔝 Top N Products", min_value=5, max_value=50, value=10, step=5)

# Filter 6: Revenue Range Slider
revenue_range = st.sidebar.slider(
    "💰 Revenue Range ($)",
    min_value=float(df['total_revenue'].min()),
    max_value=float(df['total_revenue'].max()),
    value=(float(df['total_revenue'].min()), float(df['total_revenue'].max())),
    step=1000.0
)

# Filter 7: Volume Range Slider
volume_range = st.sidebar.slider(
    "📊 Unit Volume Range",
    min_value=int(df['total_units_sold'].min()),
    max_value=int(df['total_units_sold'].max()),
    value=(int(df['total_units_sold'].min()), int(df['total_units_sold'].max())),
    step=100
)

# Filter 8: Efficiency Score Range
efficiency_range = st.sidebar.slider(
    "📈 Efficiency Score Range",
    min_value=0.0,
    max_value=1.0,
    value=(0.0, 1.0),
    step=0.05
)

# ============================================================================
# APPLY FILTERS
# ============================================================================
# Store name to column mapping
store_name_to_col = {
    'Astoria': 'revenue_Astoria',
    "Hell's Kitchen": "revenue_Hell's_Kitchen",
    'Lower Manhattan': 'revenue_Lower_Manhattan'
}

filtered_df = df[
    (df['product_category'].isin(selected_categories)) &
    (df['product_type'].isin(selected_types)) &
    (df['performance_tier'].isin(selected_tiers)) &
    (df['total_revenue'] >= revenue_range[0]) &
    (df['total_revenue'] <= revenue_range[1]) &
    (df['total_units_sold'] >= volume_range[0]) &
    (df['total_units_sold'] <= volume_range[1]) &
    (df['efficiency_score'] >= efficiency_range[0]) &
    (df['efficiency_score'] <= efficiency_range[1])
].copy()

# Handle store-specific filtering
if 'All Stores' not in selected_stores:
    store_cols = [store_name_to_col[store] for store in selected_stores]
    # Filter for products with measurable revenue in selected stores
    filtered_df = filtered_df[filtered_df[store_cols].sum(axis=1) > 0]

# ============================================================================
# KEY METRICS (KPI Display)
# ============================================================================
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("💰 Total Revenue", f"${filtered_df['total_revenue'].sum():,.0f}")
with col2:
    st.metric("📦 Products", f"{len(filtered_df)}")
with col3:
    st.metric("⭐ Hero Products", f"{len(filtered_df[filtered_df['performance_tier']=='Hero'])}")
with col4:
    st.metric("📊 Avg Efficiency", f"{filtered_df['efficiency_score'].mean():.3f}")
with col5:
    st.metric("📈 Avg Volume", f"{filtered_df['total_units_sold'].mean():,.0f}"))

st.markdown("---")

# ============================================================================
# TAB LAYOUT (PRD REQUIREMENT: 6 Modules + Data View)
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Product Rankings",
    "🎯 Revenue Contribution",
    "📈 Popularity vs Revenue",
    "📊 Pareto Analysis",
    "🏪 Store Performance",
    "🔍 Product Details",
    "📥 Data Export"
])
    "📋 Consolidated Data"
])

# ============================================================================
# TAB 1: PRODUCT RANKING DASHBOARD (PRD Module 1)
# ============================================================================
with tab1:
    st.subheader("Product Performance Rankings")
    st.markdown("**Ranking Dimensions:** Volume | Revenue | Efficiency Score | Transaction Frequency")
    
    col1, col2 = st.columns(2)
    
    # TOP-N BY VOLUME
    with col1:
        st.markdown("#### 🔝 Top Products by Sales Volume")
        volume_data = filtered_df.nlargest(top_n, 'total_units_sold')[
            ['product_detail', 'product_category', 'total_units_sold', 'efficiency_score', 'performance_tier']
        ].copy()
        volume_data['efficiency_score'] = volume_data['efficiency_score'].round(3)
        
        fig = px.bar(volume_data, x='total_units_sold', y='product_detail',
                     color='performance_tier', orientation='h',
                     labels={'total_units_sold': 'Units Sold', 'product_detail': 'Product'},
                     color_discrete_map={'Hero': '#FFD700', 'High': '#90EE90', 'Medium': '#87CEEB', 'Low': '#FFB6C6'})
        fig.update_layout(height=500, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # TOP-N BY REVENUE
    with col2:
        st.markdown("#### 💰 Top Products by Revenue")
        revenue_data = filtered_df.nlargest(top_n, 'total_revenue')[
            ['product_detail', 'product_category', 'total_revenue', 'revenue_share_pct', 'performance_tier']
        ].copy()
        
        fig = px.bar(revenue_data, x='total_revenue', y='product_detail',
                     color='performance_tier', orientation='h',
                     labels={'total_revenue': 'Revenue ($)', 'product_detail': 'Product'},
                     color_discrete_map={'Hero': '#FFD700', 'High': '#90EE90', 'Medium': '#87CEEB', 'Low': '#FFB6C6'})
        fig.update_layout(height=500, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # TOP-N BY EFFICIENCY
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### ⭐ Top Products by Efficiency Score")
        efficiency_data = filtered_df.nlargest(top_n, 'efficiency_score')[
            ['product_detail', 'product_category', 'efficiency_score', 'performance_tier']
        ].copy()
        
        fig = px.bar(efficiency_data, x='efficiency_score', y='product_detail',
                     color='performance_tier', orientation='h',
                     labels={'efficiency_score': 'Efficiency Score', 'product_detail': 'Product'},
                     color_discrete_map={'Hero': '#FFD700', 'High': '#90EE90', 'Medium': '#87CEEB', 'Low': '#FFB6C6'})
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # TOP-N BY TRANSACTION FREQUENCY
    with col4:
        st.markdown("#### 🔄 Top Products by Transaction Frequency")
        trans_data = filtered_df.nlargest(top_n, 'transaction_count')[
            ['product_detail', 'product_category', 'transaction_count', 'performance_tier']
        ].copy()
        
        fig = px.bar(trans_data, x='transaction_count', y='product_detail',
                     color='performance_tier', orientation='h',
                     labels={'transaction_count': 'Transaction Count', 'product_detail': 'Product'},
                     color_discrete_map={'Hero': '#FFD700', 'High': '#90EE90', 'Medium': '#87CEEB', 'Low': '#FFB6C6'})
        fig.update_layout(height=500, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # COMPLETE RANKINGS TABLE
    st.markdown("#### 📋 Complete Rankings Table")
    rankings_table = filtered_df[[
        'product_detail', 'product_category', 'performance_tier',
        'total_revenue', 'revenue_rank', 'total_units_sold', 'volume_rank',
        'efficiency_score', 'transaction_count'
    ]].copy()
    rankings_table.columns = ['Product', 'Category', 'Tier', 'Revenue', 'Rev Rank', 'Units', 'Vol Rank', 'Efficiency', 'Transactions']
    rankings_table = rankings_table.sort_values('Revenue', ascending=False)
    st.dataframe(rankings_table, hide_index=True, use_container_width=True, height=400)

# ============================================================================
# TAB 2: REVENUE CONTRIBUTION (PRD Module 2)
# ============================================================================
with tab2:
    st.subheader("Revenue Contribution Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    # TREEMAP: Revenue Distribution by Category and Product
    with col1:
        st.markdown("#### 🎯 Revenue Share by Category & Product")
        treemap_data = filtered_df.nlargest(20, 'total_revenue')
        
        fig = px.treemap(treemap_data,
                         path=['product_category', 'product_detail'],
                         values='total_revenue',
                         color='efficiency_score',
                         color_continuous_scale='RdYlGn',
                         labels={'efficiency_score': 'Efficiency'},
                         hover_data={'total_revenue': ':.2f', 'revenue_share_pct': ':.2f'})
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    # TOP CONTRIBUTORS TABLE
    with col2:
        st.markdown("#### 💰 Top 10 Revenue Contributors")
        top_10 = filtered_df.nlargest(10, 'total_revenue')[
            ['product_detail', 'total_revenue', 'revenue_share_pct', 'efficiency_score']
        ].copy()
        top_10['total_revenue'] = top_10['total_revenue'].apply(lambda x: f"${x:,.0f}")
        top_10['revenue_share_pct'] = top_10['revenue_share_pct'].apply(lambda x: f"{x:.2f}%")
        top_10['efficiency_score'] = top_10['efficiency_score'].apply(lambda x: f"{x:.3f}")
        top_10.columns = ['Product', 'Revenue', 'Share %', 'Efficiency']
        st.dataframe(top_10, hide_index=True, height=450)
    
    # CATEGORY BREAKDOWN
    st.markdown("---")
    st.markdown("#### 📊 Category Revenue Distribution")
    category_data = filtered_df.groupby('product_category').agg({
        'total_revenue': 'sum',
        'product_id': 'count',
        'efficiency_score': 'mean'
    }).reset_index().sort_values('total_revenue', ascending=False)
    category_data['revenue_pct'] = (category_data['total_revenue'] / category_data['total_revenue'].sum() * 100).round(1)
    
    fig = px.pie(category_data, values='total_revenue', names='product_category',
                 color_discrete_sequence=px.colors.sequential.Oranges_r)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 3: POPULARITY VS REVENUE ANALYSIS (PRD Module 3 - NEW)
# ============================================================================
with tab3:
    st.subheader("Popularity vs. Revenue Analysis - Scatter Plot")
    st.markdown("**Identify products by volume-revenue alignment**: Size=Efficiency | Color=Performance Tier")
    
    # SCATTER PLOT: Volume vs Revenue
    scatter_data = filtered_df.copy()
    
    fig = px.scatter(scatter_data,
                     x='total_units_sold',
                     y='total_revenue',
                     size='efficiency_score',
                     color='performance_tier',
                     hover_name='product_detail',
                     hover_data={'total_units_sold': ':.0f', 'total_revenue': ':.2f', 'efficiency_score': ':.3f'},
                     color_discrete_map={'Hero': '#FFD700', 'High': '#90EE90', 'Medium': '#87CEEB', 'Low': '#FFB6C6'},
                     labels={'total_units_sold': 'Units Sold', 'total_revenue': 'Revenue ($)'},
                     size_max=40)
    
    fig.update_layout(height=600, title="Volume vs. Revenue: Product Performance Distribution")
    st.plotly_chart(fig, use_container_width=True)
    
    # QUADRANT ANALYSIS
    st.markdown("---")
    st.markdown("#### 📍 Quadrant Analysis")
    
    median_volume = scatter_data['total_units_sold'].median()
    median_revenue = scatter_data['total_revenue'].median()
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Quadrant 1: High Volume, High Revenue (Hero zone)
    q1 = scatter_data[(scatter_data['total_units_sold'] >= median_volume) &
                      (scatter_data['total_revenue'] >= median_revenue)]
    with col1:
        st.metric("⭐ Hero Zone\n(High Vol, High Rev)", f"{len(q1)} products",
                  f"${q1['total_revenue'].sum():,.0f}")
    
    # Quadrant 2: Low Volume, High Revenue (Premium)
    q2 = scatter_data[(scatter_data['total_units_sold'] < median_volume) &
                      (scatter_data['total_revenue'] >= median_revenue)]
    with col2:
        st.metric("💎 Premium\n(Low Vol, High Rev)", f"{len(q2)} products",
                  f"${q2['total_revenue'].sum():,.0f}")
    
    # Quadrant 3: Low Volume, Low Revenue (Rationalization)
    q3 = scatter_data[(scatter_data['total_units_sold'] < median_volume) &
                      (scatter_data['total_revenue'] < median_revenue)]
    with col3:
        st.metric("❌ Rationalization\n(Low Vol, Low Rev)", f"{len(q3)} products",
                  f"${q3['total_revenue'].sum():,.0f}")
    
    # Quadrant 4: High Volume, Low Revenue (Volume drivers)
    q4 = scatter_data[(scatter_data['total_units_sold'] >= median_volume) &
                      (scatter_data['total_revenue'] < median_revenue)]
    with col4:
        st.metric("📦 Volume Drivers\n(High Vol, Low Rev)", f"{len(q4)} products",
                  f"${q4['total_revenue'].sum():,.0f}")

# ============================================================================
# TAB 4: PARETO ANALYSIS (PRD Module 4)
# ============================================================================
with tab4:
    st.subheader("Revenue Concentration & Pareto Analysis (80/20 Rule)")
    
    pareto_data = df.sort_values('revenue_rank').copy()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pareto_80 = len(pareto_data[pareto_data['pareto_class'] == 'Top_80%'])
        st.metric("📊 Products for 80% Revenue", f"{pareto_80}\n({pareto_80/len(df)*100:.1f}%)")
    with col2:
        top_10_share = pareto_data.head(10)['revenue_share_pct'].sum()
        st.metric("🔝 Top 10 Revenue Share", f"{top_10_share:.2f}%")
    with col3:
        long_tail = len(pareto_data[pareto_data['pareto_class'] == 'Long_Tail'])
        st.metric("📉 Long-Tail Products", f"{long_tail}\n({long_tail/len(df)*100:.1f}%)")
    
    st.markdown("---")
    st.markdown("#### 📈 Cumulative Revenue Curve (Pareto Chart)")
    
    # Pareto curve with dual axes
    fig = go.Figure()
    
    # Bar chart for individual product revenue
    fig.add_trace(go.Bar(
        x=pareto_data['revenue_rank'].head(40),
        y=pareto_data['total_revenue'].head(40),
        name='Product Revenue',
        marker_color='#D2691E',
        yaxis='y1'
    ))
    
    # Line chart for cumulative percentage
    fig.add_trace(go.Scatter(
        x=pareto_data['revenue_rank'].head(40),
        y=pareto_data['cumulative_revenue_pct'].head(40),
        name='Cumulative %',
        yaxis='y2',
        line=dict(color='#8B4513', width=3),
        mode='lines+markers'
    ))
    
    # Add 80% threshold line
    fig.add_hline(y=80, line_dash="dash", line_color="red",
                  annotation_text="80% Threshold", yref='y2')
    
    fig.update_layout(
        yaxis=dict(title='Revenue per Product ($)'),
        yaxis2=dict(title='Cumulative Revenue %', overlaying='y', side='right', range=[0, 105]),
        xaxis=dict(title='Product Rank'),
        height=500,
        hovermode='x unified',
        title="Pareto Analysis: Revenue Distribution Concentration"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Pareto Statistics
    st.markdown("---")
    st.markdown("#### 📊 Pareto Classification Statistics")
    pareto_stats = pd.DataFrame({
        'Classification': ['Top 80%', 'Long-Tail'],
        'Product Count': [
            len(pareto_data[pareto_data['pareto_class'] == 'Top_80%']),
            len(pareto_data[pareto_data['pareto_class'] == 'Long_Tail'])
        ],
        'Total Revenue': [
            pareto_data[pareto_data['pareto_class'] == 'Top_80%']['total_revenue'].sum(),
            pareto_data[pareto_data['pareto_class'] == 'Long_Tail']['total_revenue'].sum()
        ],
        'Revenue %': [
            pareto_data[pareto_data['pareto_class'] == 'Top_80%']['revenue_share_pct'].sum(),
            pareto_data[pareto_data['pareto_class'] == 'Long_Tail']['revenue_share_pct'].sum()
        ]
    })
    pareto_stats['Total Revenue'] = pareto_stats['Total Revenue'].apply(lambda x: f"${x:,.0f}")
    pareto_stats['Revenue %'] = pareto_stats['Revenue %'].apply(lambda x: f"{x:.2f}%")
    st.dataframe(pareto_stats, hide_index=True, use_container_width=True)

# ============================================================================
# TAB 5: STORE PERFORMANCE (PRD Module 5 - NEW)
# ============================================================================
with tab5:
    st.subheader("Store Performance Comparison Analysis")
    
    # Store selection and column mapping
    store_name_to_col = {
        'Astoria': 'revenue_Astoria',
        "Hell's Kitchen": "revenue_Hell's_Kitchen",
        'Lower Manhattan': 'revenue_Lower_Manhattan'
    }
    
    analysis_stores = st.multiselect(
        "🏪 Select Stores to Compare",
        options=list(store_name_to_col.keys()),
        default=list(store_name_to_col.keys())
    )
    
    # Store metrics
    col1, col2, col3 = st.columns(3)
    
    store_revenues = {}
    for store in analysis_stores:
        store_col = store_name_to_col[store]
        store_rev = df[store_col].sum()
        store_revenues[store] = store_rev
    
    for idx, store in enumerate(['Astoria', "Hell's Kitchen", 'Lower Manhattan']):
        if store in analysis_stores:
            cols_list = [col1, col2, col3]
            with cols_list[idx]:
                st.metric(store, f"${store_revenues.get(store, 0):,.0f}")
    
    st.markdown("---")
    st.markdown("#### 📊 Revenue Distribution by Store")
    
    # Store comparison chart
    store_data_list = []
    for store in analysis_stores:
        store_col = store_name_to_col[store]
        store_data_list.append({
            'Store': store,
            'Revenue': df[store_col].sum()
        })
    
    store_df = pd.DataFrame(store_data_list)
    
    fig = px.bar(store_df, x='Store', y='Revenue',
                 color='Store',
                 color_discrete_sequence=px.colors.qualitative.Set2,
                 labels={'Revenue': 'Total Revenue ($)'})
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Store-specific product rankings
    st.markdown("---")
    st.markdown("#### 🏆 Top Products by Store")
    
    store_cols = {store: store_name_to_col[store] for store in analysis_stores}
    
    for col_idx, store in enumerate(analysis_stores):
        if col_idx % 3 == 0:
            cols = st.columns(3)
        
        store_col = store_cols[store]
        top_store_products = df[[
            'product_detail', 'product_category', store_col
        ]].copy().nlargest(5, store_col)
        top_store_products[store_col] = top_store_products[store_col].apply(lambda x: f"${x:,.0f}")
        top_store_products.columns = ['Product', 'Category', f'{store} Revenue']
        
        with cols[col_idx % 3]:
            st.markdown(f"**{store}**")
            st.dataframe(top_store_products, hide_index=True, height=250, use_container_width=True)

# ============================================================================
# TAB 6: PRODUCT DRILL-DOWN (PRD Module 6 - NEW)
# ============================================================================
with tab6:
    st.subheader("Product Drill-Down Detail View")
    
    # Product selector
    product_select = st.selectbox(
        "🔍 Select Product for Detailed Analysis",
        options=df['product_detail'].sort_values(),
        help="Choose a product to view comprehensive metrics"
    )
    
    product_info = df[df['product_detail'] == product_select].iloc[0]
    
    # Comprehensive Product Card
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📋 Product Identification")
        st.write(f"**Product Name:** {product_info['product_detail']}")
        st.write(f"**Category:** {product_info['product_category']}")
        st.write(f"**Type:** {product_info['product_type']}")
        st.write(f"**Performance Tier:** {product_info['performance_tier']}")
    
    with col2:
        st.markdown("#### 💰 Revenue Metrics")
        st.metric("Total Revenue", f"${product_info['total_revenue']:,.2f}")
        st.metric("Revenue Share %", f"{product_info['revenue_share_pct']:.2f}%")
        st.metric("Revenue Rank", f"#{int(product_info['revenue_rank'])}")
    
    with col3:
        st.markdown("#### 📊 Volume Metrics")
        st.metric("Units Sold", f"{int(product_info['total_units_sold']):,}")
        st.metric("Volume Rank", f"#{int(product_info['volume_rank'])}")
        st.metric("Transactions", f"{int(product_info['transaction_count']):,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⭐ Performance Metrics")
        st.metric("Efficiency Score", f"{product_info['efficiency_score']:.3f}")
        st.metric("Pareto Classification", product_info['pareto_class'])
        st.metric("Average Unit Price", f"${product_info['avg_unit_price']:.2f}")
    
    with col2:
        st.markdown("#### 📍 Category Positioning")
        category_avg_eff = df[df['product_category'] == product_info['product_category']]['efficiency_score'].mean()
        st.metric("Category Efficiency Avg", f"{category_avg_eff:.3f}")
        
        percentile = (df['efficiency_score'] <= product_info['efficiency_score']).sum() / len(df) * 100
        st.metric("Efficiency Percentile", f"{percentile:.0f}th")
        
        st.metric("Category", product_info['product_category'])
    
    st.markdown("---")
    
    # Store-level breakdown
    st.markdown("#### 🏪 Store-Level Performance")
    store_col_mapping = {
        'Astoria': 'revenue_Astoria',
        "Hell's Kitchen": "revenue_Hell's_Kitchen",
        'Lower Manhattan': 'revenue_Lower_Manhattan'
    }
    
    store_breakdown = pd.DataFrame({
        'Store': list(store_col_mapping.keys()),
        'Revenue': [product_info.get(store_col_mapping[s], 0) for s in store_col_mapping.keys()]
    })
    store_breakdown['Revenue'] = store_breakdown['Revenue'].apply(lambda x: f"${x:,.2f}")
    
    fig = px.bar(store_breakdown, x='Store', y='Revenue',
                 color='Store',
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 7: CONSOLIDATED DATA (PRD Requirement: Data Export)
# ============================================================================
with tab7:
    st.subheader("Consolidated Product Analysis Data")
    st.markdown("Complete dataset with all analytical metrics. **Sortable, filterable, and downloadable as CSV.**")
    
    # Display full consolidated data with all relevant columns
    display_df = filtered_df[[
        'product_detail', 'product_category', 'product_type', 'performance_tier',
        'total_revenue', 'revenue_share_pct', 'revenue_rank',
        'total_units_sold', 'volume_rank', 'efficiency_score',
        'pareto_class', 'transaction_count', 'avg_unit_price'
    ]].copy().sort_values('total_revenue', ascending=False)
    
    display_df.columns = [
        'Product', 'Category', 'Type', 'Tier',
        'Revenue', 'Share %', 'Rev Rank',
        'Units Sold', 'Vol Rank', 'Efficiency',
        'Pareto', 'Transactions', 'Avg Price'
    ]
    
    st.dataframe(display_df, hide_index=True, height=600, use_container_width=True)
    
    st.markdown("---")
    
    # Download buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name="afficionado_product_analysis_filtered.csv",
            mime="text/csv",
            help="Download filtered products as CSV"
        )
    
    with col2:
        csv_all = df.to_csv(index=False)
        st.download_button(
            label="📥 Download All Data (CSV)",
            data=csv_all,
            file_name="afficionado_product_analysis_complete.csv",
            mime="text/csv",
            help="Download all 80 products as CSV"
        )
    
    with col3:
        try:
            # Cloud-compatible file path handling
            script_dir = Path(__file__).parent if '__file__' in dir() else Path.cwd()
            docx_path = script_dir / 'RESEARCH_PAPER_MANUSCRIPT_20PAGE.docx'
            
            # Try alternate path if running from different directory
            if not docx_path.exists():
                docx_path = Path('RESEARCH_PAPER_MANUSCRIPT_20PAGE.docx')
            
            if docx_path.exists():
                with open(docx_path, "rb") as file:
                    st.download_button(
                        label="📄 Download Research Paper (MS Word)",
                        data=file,
                        file_name="Afficionado_Product_Analysis_Research_Paper.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        help="20-page MIT-level research manuscript"
                    )
            else:
                st.markdown("**Research Manuscript:** Not available in current environment")
        except Exception as e:
            st.markdown(f"**Note:** Could not load research paper ({str(e)})")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 0.85em;'>"
    "Afficionado Coffee Roasters | Product Portfolio Analysis Dashboard<br/>"
    "Comprehensive performance metrics and data-driven recommendations"
    "</div>",
    unsafe_allow_html=True
)
