# Product Optimization and Revenue Contribution Analysis

## Afficionado Coffee Roasters

This repository contains the data, code, and manuscript document for a product portfolio analysis of Afficionado Coffee Roasters. The project examines revenue concentration, product performance, and store-level variation using transaction-level point-of-sale data.

## Overview

The analysis is based on a 2025 transactional dataset covering:

- 149,116 transactions
- 80 products
- 9 product categories
- 3 retail locations
- $698,812.33 in total revenue

The project was designed to support:

- product-level performance assessment
- Pareto revenue concentration analysis
- category and store comparison
- manuscript review alongside verified project outputs

## Repository Contents

### Core Files

- `streamlit_app.py`
  Interactive dashboard for product, category, store, and Pareto analysis.
- `requirements.txt`
  Python dependencies for the project.

### Documentation

- `README.md`
  Repository overview and usage instructions.
- `TRANSFORMATION_LOGIC.md`
  Data transformation and feature-engineering documentation.
- `CODE_ANALYSIS.md`
  Technical description of the dashboard structure and logic.

### Data

- `data/Afficionado Coffee Roasters.xlsx`
  Raw transaction-level workbook.
- `data/CONSOLIDATED_ANALYSIS.csv`
  Product-level analytical dataset.
- `data/CATEGORY_SUMMARY.csv`
  Category-level revenue and volume summary.
- `data/STORE_SUMMARY.csv`
  Store-level revenue and transaction summary.
- `data/SUMMARY_STATISTICS.csv`
  High-level portfolio statistics.


## Analytical Scope

The repository applies a structured product analytics workflow that includes:

- revenue calculation from transaction quantity and unit price
- product-level aggregation of revenue, volume, and transaction frequency
- category-level and store-level summaries
- Pareto classification based on cumulative revenue contribution
- a weighted efficiency score using normalized revenue and normalized volume
- popularity-versus-revenue quadrant analysis

## Key Results

Selected verified findings include:

- 42 products account for 79.25% of total revenue
- the remaining 38 products account for 20.75% of total revenue
- Coffee is the leading category at 38.63% of revenue
- Tea contributes 28.11% of revenue
- Hell's Kitchen has the highest total store revenue
- Lower Manhattan has the highest average revenue per transaction

## Installation

```bash
git clone https://github.com/ganapathi-ai/Product_Optimization_-_Revenue_Contribution_Analysis.git
cd Afficionado_Coffee_Roasters
pip install -r requirements.txt
```

## Usage

### Launch the Dashboard

```bash
streamlit run streamlit_app.py
```

## Reproducibility Notes

- The raw source workbook is included in `data/`.
- The derived CSV outputs correspond to the analytical summaries used by the dashboard and manuscript.
- Supporting methodological details are documented in `TRANSFORMATION_LOGIC.md`.

## Recommended Reading Order

For researchers reviewing the repository, the suggested order is:

1. `README.md`
2. `TRANSFORMATION_LOGIC.md`
3. `data/SUMMARY_STATISTICS.csv`
4. `data/CONSOLIDATED_ANALYSIS.csv`
5. `streamlit_app.py`


## License and Use

This repository is intended for research, academic review, and reproducibility of the accompanying analysis.
