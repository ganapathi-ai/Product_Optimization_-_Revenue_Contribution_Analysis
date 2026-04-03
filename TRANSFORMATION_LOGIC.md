# DATA TRANSFORMATION LOGIC DOCUMENTATION
## Afficionado Coffee Roasters - Feature Engineering & Analysis

---

## OVERVIEW

This document explains every transformation, calculation, and feature engineering step applied to the raw transaction data.

**Source Data:** `Afficionado Coffee Roasters.xlsx`  
**Output:** `CONSOLIDATED_ANALYSIS.csv` (single comprehensive file)

---

## 1. TRANSACTION-LEVEL FEATURES

### 1.1 Revenue Calculation
**Formula:**
```python
revenue = transaction_qty × unit_price
```

**Logic:** Basic revenue computation at transaction level  
**Purpose:** Foundation for all revenue-based analysis  
**Example:** 2 units × $3.50 = $7.00

---

### 1.2 Hour Extraction
**Formula:**
```python
hour = extract_hour(transaction_time)
```

**Logic:** Parse time string (HH:MM:SS) and extract hour component  
**Purpose:** Time-based pattern analysis  
**Example:** "14:30:15" → 14

---

### 1.3 Day Part Classification
**Formula:**
```python
day_part = categorize_by_hour(hour)
  - Night: 0-6
  - Morning: 6-12
  - Afternoon: 12-18
  - Evening: 18-24
```

**Logic:** Bin hours into business-relevant time segments  
**Purpose:** Identify peak sales periods  
**Example:** hour=10 → "Morning"

---

### 1.4 Product Size Extraction
**Formula:**
```python
product_size = extract_suffix(product_detail, pattern='Sm|Rg|Lg')
```

**Logic:** Extract size indicator from product name using regex  
**Purpose:** Size-based pricing and preference analysis  
**Example:** "Latte Rg" → "Rg"

---

### 1.5 Price Category Classification
**Formula:**
```python
price_category = bin_price(unit_price)
  - Budget: $0-2
  - Standard: $2-4
  - Premium: $4-10
  - Luxury: $10-50
```

**Logic:** Segment products by price tier  
**Purpose:** Price sensitivity and positioning analysis  
**Example:** $3.50 → "Standard"

---

## 2. PRODUCT-LEVEL AGGREGATIONS

### 2.1 Total Revenue per Product
**Formula:**
```python
total_revenue = SUM(revenue) GROUP BY product_id
```

**Logic:** Aggregate all transaction revenues for each product  
**Purpose:** Identify revenue drivers  
**Example:** Product #39 (Latte Rg) → $19,112.25

---

### 2.2 Total Units Sold
**Formula:**
```python
total_units_sold = SUM(transaction_qty) GROUP BY product_id
```

**Logic:** Sum all quantities sold per product  
**Purpose:** Measure product popularity  
**Example:** Product #50 (Earl Grey Rg) → 4,708 units

---

### 2.3 Transaction Count
**Formula:**
```python
transaction_count = COUNT(transaction_id) GROUP BY product_id
```

**Logic:** Count distinct transactions per product  
**Purpose:** Measure purchase frequency  
**Example:** Product #39 → 2,896 transactions

---

### 2.4 Average Unit Price
**Formula:**
```python
avg_unit_price = MEAN(unit_price) GROUP BY product_id
```

**Logic:** Calculate mean price per product  
**Purpose:** Pricing consistency check  
**Example:** Product #39 → $4.25

---

### 2.5 Revenue Share Percentage
**Formula:**
```python
revenue_share_pct = (product_revenue / total_revenue) × 100
```

**Logic:** Calculate each product's contribution to total revenue  
**Purpose:** Identify revenue concentration  
**Example:** $19,112 / $698,812 × 100 = 2.73%

---

### 2.6 Revenue Rank
**Formula:**
```python
revenue_rank = RANK(total_revenue, descending=True)
```

**Logic:** Assign rank based on revenue (1=highest)  
**Purpose:** Quick identification of top performers  
**Example:** Latte Rg → Rank 3

---

### 2.7 Volume Rank
**Formula:**
```python
volume_rank = RANK(total_units_sold, descending=True)
```

**Logic:** Assign rank based on units sold  
**Purpose:** Identify popularity vs profitability gaps  
**Example:** Earl Grey Rg → Rank 1 (most popular)

---

### 2.8 Cumulative Revenue
**Formula:**
```python
cumulative_revenue = CUMSUM(total_revenue) ORDER BY total_revenue DESC
```

**Logic:** Running sum of revenue from highest to lowest  
**Purpose:** Pareto analysis foundation  
**Example:** Top 3 products → $61,270 cumulative

---

### 2.9 Cumulative Revenue Percentage
**Formula:**
```python
cumulative_revenue_pct = (cumulative_revenue / total_revenue) × 100
```

**Logic:** Express cumulative revenue as percentage  
**Purpose:** Identify 80/20 threshold  
**Example:** Top 10 products → 25.38%

---

### 2.10 Efficiency Score
**Formula:**
```python
efficiency_score = (revenue_weight × 0.6) + (volume_weight × 0.4)

where:
  revenue_weight = product_revenue / max_product_revenue
  volume_weight = product_units / max_product_units
```

**Logic:** Composite metric balancing profitability (60%) and popularity (40%)  
**Purpose:** Holistic product performance assessment  
**Range:** 0.0 to 1.0  
**Example:** Dark chocolate Lg → 0.992 (hero product)

**Interpretation:**
- 0.8-1.0: Hero products (high revenue + high volume)
- 0.5-0.8: High performers
- 0.2-0.5: Medium performers
- 0.0-0.2: Low performers

---

### 2.11 Performance Tier Classification
**Formula:**
```python
performance_tier = categorize_efficiency(efficiency_score)
  - Hero: 0.8-1.0
  - High: 0.5-0.8
  - Medium: 0.2-0.5
  - Low: 0.0-0.2
```

**Logic:** Bin efficiency scores into actionable tiers  
**Purpose:** Strategic product classification  
**Example:** Score 0.992 → "Hero"

---

### 2.12 Pareto Classification
**Formula:**
```python
pareto_class = IF(cumulative_revenue_pct <= 80, "Top_80%", "Long_Tail")
```

**Logic:** Classify products based on 80/20 rule  
**Purpose:** Menu optimization decisions  
**Example:** Top 42 products → "Top_80%"

---

## 3. CATEGORY-LEVEL AGGREGATIONS

### 3.1 Category Revenue
**Formula:**
```python
category_revenue = SUM(revenue) GROUP BY product_category
```

**Logic:** Total revenue per category  
**Purpose:** Category performance comparison  
**Example:** Coffee → $269,952.45

---

### 3.2 Category Revenue Share
**Formula:**
```python
category_revenue_share_pct = (category_revenue / total_revenue) × 100
```

**Logic:** Each category's contribution to total  
**Purpose:** Business dependency analysis  
**Example:** Coffee → 38.63%

---

### 3.3 Unique Products per Category
**Formula:**
```python
unique_products = COUNT(DISTINCT product_id) GROUP BY product_category
```

**Logic:** Number of SKUs per category  
**Purpose:** Menu complexity assessment  
**Example:** Coffee → 21 products

---

### 3.4 Average Revenue per Product (Category)
**Formula:**
```python
avg_revenue_per_product = category_revenue / unique_products
```

**Logic:** Mean revenue contribution per SKU in category  
**Purpose:** Category efficiency comparison  
**Example:** Drinking Chocolate → $18,104 per product

---

## 4. PRODUCT TYPE AGGREGATIONS

### 4.1 Type Revenue
**Formula:**
```python
type_revenue = SUM(revenue) GROUP BY product_type
```

**Logic:** Revenue by product variant  
**Purpose:** Variant-level performance  
**Example:** Barista Espresso → $91,406.20

---

### 4.2 Type Revenue Share
**Formula:**
```python
type_revenue_share_pct = (type_revenue / total_revenue) × 100
```

**Logic:** Variant contribution to total  
**Purpose:** Identify top product types  
**Example:** Barista Espresso → 13.08%

---

## 5. STORE-LEVEL AGGREGATIONS

### 5.1 Store Total Revenue
**Formula:**
```python
store_total_revenue = SUM(revenue) GROUP BY store_location
```

**Logic:** Total revenue per store  
**Purpose:** Store performance comparison  
**Example:** Hell's Kitchen → $236,511.17

---

### 5.2 Store Average Revenue
**Formula:**
```python
store_avg_revenue = MEAN(revenue) GROUP BY store_location
```

**Logic:** Mean transaction value per store  
**Purpose:** Transaction quality assessment  
**Example:** Lower Manhattan → $4.81

---

### 5.3 Store Revenue Share
**Formula:**
```python
store_revenue_share_pct = (store_revenue / total_revenue) × 100
```

**Logic:** Each store's contribution  
**Purpose:** Geographic performance  
**Example:** Hell's Kitchen → 33.8%

---

### 5.4 Store × Product Revenue
**Formula:**
```python
revenue_by_store = SUM(revenue) GROUP BY (store_location, product_id)
```

**Logic:** Revenue per product per store  
**Purpose:** Location-specific product performance  
**Example:** Latte Rg at Astoria → $6,500

---

## 6. CONSOLIDATED OUTPUT STRUCTURE

### Column Organization (25 columns total)

**Group 1: Product Identification (4 columns)**
- product_id
- product_detail
- product_category
- product_type

**Group 2: Performance Metrics (9 columns)**
- total_revenue
- revenue_share_pct
- revenue_rank
- total_units_sold
- volume_rank
- transaction_count
- avg_unit_price
- efficiency_score
- performance_tier

**Group 3: Cumulative Analysis (3 columns)**
- cumulative_revenue
- cumulative_revenue_pct
- pareto_class

**Group 4: Category Metrics (4 columns)**
- category_revenue
- category_revenue_share_pct
- unique_products
- avg_revenue_per_product

**Group 5: Product Type Metrics (2 columns)**
- type_revenue
- type_revenue_share_pct

**Group 6: Store Performance (3 columns)**
- revenue_Astoria
- revenue_Hell's_Kitchen
- revenue_Lower_Manhattan

---

## 7. KEY METRICS SUMMARY

### Revenue Metrics
- **Total Revenue:** $698,812.33
- **Average Transaction:** $4.69
- **Revenue Range:** $755.20 - $21,151.75

### Product Metrics
- **Total Products:** 80
- **Hero Products (>0.8 efficiency):** 15
- **Low Products (<0.2 efficiency):** 10
- **Pareto Threshold:** 42 products for 80% revenue

### Category Metrics
- **Top Category:** Coffee (38.63%)
- **Most Efficient:** Drinking Chocolate ($18,104/product)
- **Least Efficient:** Packaged Chocolate ($1,469/product)

### Store Metrics
- **Top Store:** Hell's Kitchen ($236,511)
- **Highest Avg Transaction:** Lower Manhattan ($4.81)
- **Most Consistent:** <3% variance across stores

---

## 8. DATA QUALITY CHECKS

### Validation Rules Applied
1. ✓ All revenues > 0
2. ✓ All quantities > 0
3. ✓ All prices > 0
4. ✓ Revenue = qty × price (verified)
5. ✓ Sum of revenue shares = 100%
6. ✓ No missing product identifiers
7. ✓ No duplicate product IDs

---

## 9. TRANSFORMATION PIPELINE

```
Raw Data (149,116 transactions)
    ↓
Transaction-Level Features (5 features)
    ↓
Product Aggregation (80 products)
    ↓
Category Aggregation (9 categories)
    ↓
Store Aggregation (3 stores)
    ↓
Product Type Aggregation (30 types)
    ↓
Merge All Dimensions
    ↓
CONSOLIDATED_ANALYSIS.csv (80 rows × 25 columns)
```

---

## 10. FILE OUTPUTS

### Primary Output
**CONSOLIDATED_ANALYSIS.csv**
- 80 products × 25 columns
- All metrics in one file
- Ready for analysis and visualization

### Supporting Outputs
**SUMMARY_STATISTICS.csv**
- 12 key metrics
- Executive summary format

**CATEGORY_SUMMARY.csv**
- 9 categories
- Category-level insights

**STORE_SUMMARY.csv**
- 3 stores
- Store performance metrics

---

## 11. USAGE EXAMPLES

### Find Hero Products
```python
df = pd.read_csv('CONSOLIDATED_ANALYSIS.csv')
heroes = df[df['performance_tier'] == 'Hero']
```

### Identify Long-Tail Products
```python
long_tail = df[df['pareto_class'] == 'Long_Tail']
```

### Top 10 Revenue Contributors
```python
top_10 = df.nsmallest(10, 'revenue_rank')
```

### Products Below 0.5% Revenue Share
```python
underperformers = df[df['revenue_share_pct'] < 0.5]
```

---

## 12. MATHEMATICAL NOTATION

### Revenue Share
$$\text{Revenue Share}_i = \frac{R_i}{\sum_{j=1}^{n} R_j} \times 100$$

### Efficiency Score
$$E_i = 0.6 \times \frac{R_i}{\max(R)} + 0.4 \times \frac{V_i}{\max(V)}$$

### Cumulative Revenue Percentage
$$C_i = \frac{\sum_{j=1}^{i} R_j}{\sum_{j=1}^{n} R_j} \times 100$$

Where:
- $R_i$ = Revenue of product $i$
- $V_i$ = Volume (units) of product $i$
- $n$ = Total number of products
- $C_i$ = Cumulative revenue percentage at product $i$

---

## 13. BUSINESS INTERPRETATION GUIDE

### Efficiency Score Interpretation
- **0.9-1.0:** Premium performers - protect and promote
- **0.7-0.9:** Strong performers - maintain focus
- **0.5-0.7:** Solid performers - monitor
- **0.3-0.5:** Moderate performers - evaluate
- **0.0-0.3:** Weak performers - review or discontinue

### Pareto Classification Actions
- **Top_80%:** Core menu items - prioritize
- **Long_Tail:** Review for strategic value or discontinue

### Performance Tier Actions
- **Hero:** Feature in marketing, ensure availability
- **High:** Maintain current strategy
- **Medium:** Optimize pricing or promotion
- **Low:** Discontinue or redesign

---

**Documentation Version:** 1.0  
**Last Updated:** 2025  
**Author:** Data Analytics Team
