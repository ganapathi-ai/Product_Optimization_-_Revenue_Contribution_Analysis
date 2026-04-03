# Afficionado Coffee Roasters
## Product Optimization & Revenue Contribution Analysis

---

## 📋 Project Overview

Comprehensive product-centric analytics for **Afficionado Coffee Roasters** to optimize menu performance, identify revenue drivers, and support data-driven merchandising decisions.

**Dataset:** Provided by Unified Mentor as part of a Data Science project | 149,116 transactions | 80 products | 3 stores | $698,812 total revenue

**Project Status:** ✅ **COMPLETE** - All deliverables generated

---

## 📑 DOCUMENTATION

### 🎯 Product Requirements Document (PRD)
- **File:** [PRODUCT_REQUIREMENTS_DOCUMENT.md](PRODUCT_REQUIREMENTS_DOCUMENT.md)
- **Status:** ✅ Complete
- **Contents:**
  - Background and context
  - Problem statement and objectives
  - Dataset description
  - Complete analytical methodology (7 phases)
  - KPI definitions and metrics
  - Streamlit dashboard requirements
  - Success criteria
  - Implementation timeline

### 📚 Technical Documentation
- **File:** [TRANSFORMATION_LOGIC.md](TRANSFORMATION_LOGIC.md)
- **Status:** ✅ Complete
- **Contents:**
  - Data transformation procedures
  - Feature engineering formulas
  - Aggregation logic
  - Performance metric calculations
  - Column definitions

### 💻 Code Analysis & Implementation Guide
- **File:** [CODE_ANALYSIS.md](CODE_ANALYSIS.md)
- **Status:** ✅ Complete (706-line implementation)
- **Contents:**
  - Architecture overview
  - Data loading and caching strategy
  - 8-filter sidebar system
  - 7-module tab structure
    - Tab 1: Product Rankings (4 visualizations)
    - Tab 2: Revenue Contribution (3 visualizations)
    - Tab 3: Popularity vs Revenue (quadrant analysis)
    - Tab 4: Pareto Analysis (dual-axis)
    - Tab 5: Store Performance (store comparison)
    - Tab 6: Product Drill-Down (detail view)
    - Tab 7: Data Export (CSV & DOCX download)
  - 10 Plotly visualizations
  - 25+ KPI metrics
  - Error handling and cloud compliance
  - Performance optimization techniques
  - Code quality metrics
  - Deployment readiness verification

### 📊 Research Paper (20-Page Manuscript)
- **File:** `RESEARCH_PAPER_MANUSCRIPT_20PAGE.docx`
- **Status:** ✅ Complete
- **Format:** Microsoft Word DOCX (ready for download)
- **Academic Level:** MIT/Harvard-level research paper
- **Contents:**
  - Title page and abstract
  - Table of contents
  - Executive summary
  - Introduction & background
  - Literature review
  - Problem statement
  - Dataset description
  - Analytical methodology
  - Key performance indicators
  - Revenue analysis with data tables
  - Product performance stratification
  - Pareto analysis
  - Efficiency scoring analysis
  - Store performance comparison
  - Strategic insights
  - 4-phase recommendations
  - Implementation roadmap
  - Risk assessment
  - Conclusion
  - References
  - Appendices

---

## 🎯 Objectives

### Primary Objectives
✅ Identify top-selling and least-selling products  
✅ Quantify revenue contribution by product and category  
✅ Measure revenue concentration across the menu  

### Secondary Objectives
✅ Support menu simplification and optimization  
✅ Identify high-impact "hero" products  
✅ Highlight low-performing products for review  

---

## 🔍 Key Findings

### Revenue Concentration
- **42 products (52.5%)** generate **80% of revenue** (Pareto principle)
- **Top 10 products** contribute **25.38%** of total revenue
- **22 long-tail products** contribute only **6.04%** combined

### Category Performance
| Category | Revenue | Share % |
|----------|---------|--------|
| Coffee | $269,952 | 38.63% |
| Tea | $196,406 | 28.11% |
| Bakery | $82,316 | 11.78% |
| Drinking Chocolate | $72,416 | 10.36% |

### Product Efficiency
- **High Performers:** Large-size premium beverages (efficiency score > 0.9)
- **Low Performers:** Loose tea and packaged goods (efficiency score < 0.05)

### Store Performance
- **Consistent across locations:** Revenue variance < 3%
- **Hell's Kitchen:** $236,511 (highest)
- **Lower Manhattan:** $230,057 (highest avg per transaction)

---

## 📊 Analytical Methodology

### 1. Data Ingestion & Validation
- Load transaction-level data from Excel
- Validate product identifiers, prices, and quantities
- Ensure data quality and consistency

### 2. Revenue Computation
```python
revenue = transaction_qty × unit_price
```
- Aggregate by product, product type, and category
- Calculate revenue share percentages

### 3. Product Popularity Analysis
- Rank products by sales volume
- Identify top and bottom performers
- Compare volume rank vs revenue rank

### 4. Revenue Contribution Analysis
- Calculate revenue share per product
- Identify revenue anchors and long-tail products
- Analyze category dependencies

### 5. Pareto Analysis (80/20 Rule)
- Cumulative revenue distribution
- Revenue concentration metrics
- Menu balance assessment

### 6. Product Efficiency Scoring
```python
efficiency_score = (revenue_weight × 0.6) + (volume_weight × 0.4)
```

---

## 🚀 Usage

### Installation
```bash
pip install -r requirements.txt
```

### Run Analysis
```bash
# Core product optimization analysis
python product_optimization_analysis.py
```

### Launch Streamlit Dashboard
```bash
streamlit run streamlit_app.py
```

### Optional: Run ML Pipeline
```bash
# Feature engineering
python transform_data.py

# ML predictions & segmentation
python ml_pipeline.py

# Advanced analytics
python advanced_analytics.py

# Generate visualizations
python visualize_insights.py
```

---

## 📁 Project Structure

```
Afficionado_Coffee_Roasters/
│
├── data/
│   ├── Afficionado Coffee Roasters.xlsx    # Source data
│   ├── product_revenue_analysis.csv        # Product-level revenue
│   ├── category_performance.csv            # Category metrics
│   ├── product_efficiency.csv              # Efficiency scores
│   └── store_category_revenue.csv          # Store × category matrix
│
├── product_optimization_analysis.py        # Main analysis script
├── streamlit_app.py                        # Interactive dashboard
├── RESEARCH_PAPER.md                       # Comprehensive report
│
├── transform_data.py                       # Feature engineering
├── ml_pipeline.py                          # ML predictions
├── advanced_analytics.py                   # Anomaly detection
├── visualize_insights.py                   # Chart generation
│
├── requirements.txt                        # Dependencies
└── README.md                               # This file
```

---

## 📈 Streamlit Dashboard Features

### Core Modules
1. **Product Rankings** - Top/bottom performers by volume and revenue
2. **Revenue Contribution** - Treemap visualization and contribution tables
3. **Category Analysis** - Category distribution and performance metrics
4. **Pareto Analysis** - 80/20 rule visualization and concentration metrics
5. **Product Drill-Down** - Detailed performance tables with export

### Interactive Filters
- Store location selector (multi-select)
- Product category filter (multi-select)
- Top-N products slider (5-50)

### Key Visualizations
- Horizontal bar charts (rankings)
- Treemap (revenue contribution)
- Pie charts (category distribution)
- Pareto curve (cumulative revenue)
- Performance tables (drill-down)

---

## 🎯 Key Performance Indicators (KPIs)

| KPI | Value | Description |
|-----|-------|-------------|
| **Product Revenue Contribution** | 3.03% | Top product share |
| **Category Revenue Share** | 38.63% | Coffee category dominance |
| **Revenue Concentration Ratio** | 25.38% | Top 10 products |
| **Product Efficiency Score** | 0.476 avg | Revenue per SKU |
| **Pareto Threshold** | 42 products | For 80% revenue |

---

## 💡 Strategic Recommendations

### 1. Menu Optimization
- **Reduce SKUs:** From 80 to 60-65 products
- **Discontinue:** 22 long-tail products (< 0.5% revenue share)
- **Promote:** Top 42 "hero" products

### 2. Category Strategy
- **Coffee & Tea:** Maintain focus (66.74% combined revenue)
- **Drinking Chocolate:** Expand offerings (high efficiency)
- **Loose Tea:** Consolidate or discontinue (low performance)

### 3. Operational Efficiency
- **Standardize:** Replicate best practices across stores
- **Inventory:** Focus on high-efficiency products
- **Pricing:** Dynamic pricing for slow-movers

### 4. Revenue Growth
- **Upsell:** Large-size premium beverages
- **Bundle:** Coffee beans with brewing equipment
- **Loyalty:** Program focused on top 20 products

---

## � COMPLETE DELIVERABLES

### Deliverable 1: Product Requirements Document (PRD)
- **File:** [PRODUCT_REQUIREMENTS_DOCUMENT.md](PRODUCT_REQUIREMENTS_DOCUMENT.md)
- **Status:** ✅ Complete
- **Contents:** Background, problem statement, objectives, dataset schema, analytical methodology (7 phases), KPI definitions, dashboard requirements, success criteria, implementation timeline

### Deliverable 2: 20-Page Research Manuscript (MS Word DOCX Format)
- **File:** `RESEARCH_PAPER_MANUSCRIPT_20PAGE.docx` (49 KB)
- **Status:** ✅ Complete & Ready for Download
- **Academic Level:** MIT/Harvard-level research paper
- **Format:** Microsoft Word DOCX (not markdown)
- **Contents:**
  - Title page with author, institution, and date
  - Abstract and table of contents
  - Executive summary with key findings
  - Introduction and organizational context
  - Literature review (Pareto principle, revenue concentration, menu engineering)
  - Problem statement and research objectives
  - Dataset description with data quality assessment
  - Analytical methodology (7 detailed phases)
  - Key performance indicators and metrics
  - Revenue analysis with data tables
  - Product performance stratification (Hero, High, Medium, Low tiers)
  - Pareto analysis (80/20 rule application)
  - Efficiency scoring and innovation analysis
  - Comparative store performance analysis
  - Strategic insights and implications
  - 4-phase implementation recommendations
  - Implementation roadmap with timeline
  - Risk assessment and mitigation strategies
  - Conclusion and future research directions
  - Academic references (10 sources)
  - Appendices with top 30 products dataset

### Deliverable 3: Comprehensive Technical Documentation
- **File:** [TRANSFORMATION_LOGIC.md](TRANSFORMATION_LOGIC.md)
- **Status:** ✅ Complete
- **Contents:** Data transformation procedures, feature engineering formulas, aggregation logic, performance metric calculations, all 25 output columns documented

### Deliverable 4: Streamlit Interactive Dashboard
- **File:** [streamlit_app.py](streamlit_app.py)
- **Status:** ✅ Available & Functional
- **Features:** Product rankings, category revenue distribution, Pareto analysis, store performance comparison, drill-down details, interactive filters

### Deliverable 5: Consolidated Analysis Dataset (CSV)
- **File:** [data/CONSOLIDATED_ANALYSIS.csv](data/CONSOLIDATED_ANALYSIS.csv)
- **Status:** ✅ Available
- **Rows:** 80 products with complete analysis
- **Columns:** 25 comprehensive metrics and derived features

---

## 🚀 Getting Started

### Quick Start - Local Development

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Streamlit Dashboard**
   ```bash
   streamlit run streamlit_app.py
   ```
   The app will open at `http://localhost:8501`

3. **Generate Research Paper** (optional)
   ```bash
   python generate_comprehensive_manuscript.py
   ```

### Cloud Deployment

For complete Streamlit Cloud deployment instructions, see: [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)

**Quick Deploy:**
1. Push repository to GitHub
2. Go to https://share.streamlit.io/
3. Connect your GitHub repo
4. Select `streamlit_app.py` as main file
5. Deploy!

### Verification

Run cloud compliance checks:
```bash
python verify_cloud_compliance.py
```

---

## 📚 Documentation Map

| Document | Purpose | Audience |
|----------|---------|----------|
| [README.md](README.md) | Project overview and getting started | Everyone |
| [CODE_ANALYSIS.md](CODE_ANALYSIS.md) | Technical implementation details | Developers |
| [PRODUCT_REQUIREMENTS_DOCUMENT.md](PRODUCT_REQUIREMENTS_DOCUMENT.md) | Complete PRD with specifications | Product team |
| [PRD_VERIFICATION_CHECKLIST.md](PRD_VERIFICATION_CHECKLIST.md) | Requirement compliance matrix | Project managers |
| [TRANSFORMATION_LOGIC.md](TRANSFORMATION_LOGIC.md) | Data engineering documentation | Data scientists |
| [RESEARCH_PAPER.md](RESEARCH_PAPER.md) | Markdown version of research | Readers |
| `RESEARCH_PAPER_MANUSCRIPT_20PAGE.docx` | Official MS Word manuscript | Executives |
| [STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md) | Deployment guide | DevOps/Tech leads |

---

## ✅ Verification & Quality Assurance

### Cloud Compliance Checklist
- ✅ OS-independent file paths
- ✅ Relative path resolution
- ✅ Error handling for missing files
- ✅ Graceful degradation
- ✅ No hardcoded credentials
- ✅ All dependencies pinned in requirements.txt
- ✅ Streamlit configuration included
- ✅ Verified store column mappings

### Code Quality
- ✅ 706 lines of clean, documented code
- ✅ Single decorator for performance caching
- ✅ Comprehensive error handling
- ✅ 119 Streamlit UI components
- ✅ 10 interactive Plotly visualizations
- ✅ 8 dynamic filters
- ✅ 25+ KPI metrics

### Test Coverage
- ✅ Syntax validation (Python compile check)
- ✅ Data loading verification
- ✅ Store column accessibility
- ✅ Filter application logic
- ✅ File operation handling

---

## 📞 Support & Questions

For implementation questions or issues:

1. **Local Development:** Check `CODE_ANALYSIS.md` for architecture details
2. **Deployment Issues:** See `STREAMLIT_CLOUD_DEPLOYMENT.md`
3. **Data Questions:** Review `TRANSFORMATION_LOGIC.md`
4. **Requirements:** Consult `PRODUCT_REQUIREMENTS_DOCUMENT.md`

---

## 📄 License & Attribution

This project was created as part of a comprehensive Data Science analysis and includes:
- Original data provided by Unified Mentor
- Custom analytical framework and implementation
- Professional software engineering (Streamlit, Plotly, Pandas)
- Academic research manuscript
- Complete technical documentation

---

**Project Completion Date:** April 2026  
**Status:** ✅ Production Ready
- **Status:** ✅ Available
- **Rows:** 80 products with complete analysis
- **Columns:** 25 comprehensive metrics and derived features

### Deliverable 6: Executive Summary for Stakeholders
- **Location:** Section 1 (Executive Summary) in Research Manuscript
- **Status:** ✅ Complete
- **Contents:** Key findings, Pareto metrics, category analysis, strategic recommendations, implementation priorities

---

## 📊 Deliverables (Legacy)

✅ **Research Paper** - Comprehensive EDA, insights, and recommendations ([RESEARCH_PAPER.md](RESEARCH_PAPER.md))  
✅ **Streamlit Dashboard** - Interactive analytics with filters and drill-down  
✅ **CSV Outputs** - Product rankings, category performance, efficiency scores  
✅ **Executive Summary** - Key findings and strategic recommendations

---

## 🛠️ Technical Stack

- **Python 3.8+**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - ML algorithms
- **matplotlib/seaborn** - Static visualizations
- **plotly** - Interactive charts
- **streamlit** - Web dashboard
- **openpyxl** - Excel file handling

---

## 📝 Methodology Notes

### Revenue Calculation
```python
revenue = transaction_qty × unit_price
```

### Revenue Share Percentage
```python
revenue_share_pct = (product_revenue / total_revenue) × 100
```

### Efficiency Score
```python
efficiency_score = (revenue_rank × 0.6) + (volume_rank × 0.4)
```

### Pareto Analysis
- Sort products by revenue (descending)
- Calculate cumulative revenue percentage
- Identify threshold where cumulative % reaches 80%

---

## 🎓 Business Impact

### Problem Solved
- ❌ **Before:** Intuition-driven menu decisions
- ✅ **After:** Data-driven product optimization

### Value Created
- **Operational Efficiency:** Reduce menu complexity by 20-25%
- **Revenue Focus:** Concentrate marketing on 42 high-performers
- **Cost Reduction:** Eliminate low-impact inventory
- **Customer Experience:** Simplified menu, faster service

---

## 📞 Support

For questions or issues:
1. Review [RESEARCH_PAPER.md](RESEARCH_PAPER.md) for detailed analysis
2. Check data outputs in `data/` folder
3. Run Streamlit dashboard for interactive exploration

---

## 📄 License

This project is for educational and analytical purposes.

---

**Afficionado Coffee Roasters** | Product Optimization Analysis | Data-Driven Menu Intelligence
#   P r o d u c t _ O p t i m i z a t i o n _ - _ R e v e n u e _ C o n t r i b u t i o n _ A n a l y s i s  
 