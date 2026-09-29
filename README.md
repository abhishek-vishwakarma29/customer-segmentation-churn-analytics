# Customer Segmentation & Churn Pattern Analytics in European Banking

## 📌 Project Overview

This project analyzes customer churn patterns in a European banking dataset using Python and interactive data visualization.

The analysis focuses on identifying customer segments with different churn levels and examining how churn varies across geography, age, tenure, credit score, balance, gender, customer engagement, and product usage.

An interactive Streamlit dashboard was developed to present the analysis and allow users to explore customer segments using filters.

---

## 🎯 Objectives

The main objectives of this project are to:

- Calculate the overall customer churn rate.
- Analyze churn across different customer segments.
- Compare churn patterns across France, Germany, and Spain.
- Examine churn by age, tenure, credit score, and balance.
- Analyze high-value customers based on balance.
- Study customer engagement and product usage patterns.
- Identify segments with relatively higher observed churn.
- Develop an interactive Streamlit dashboard for business analysis.

---

## 📊 Dataset

The project uses a European banking customer dataset containing **10,000 customer records**.

The dataset includes information such as:

- Customer ID
- Credit Score
- Geography
- Gender
- Age
- Tenure
- Balance
- Number of Products
- Credit Card Ownership
- Active Membership
- Estimated Salary
- Churn Status (`Exited`)

The geographical segments covered are:

- France
- Germany
- Spain

---

## 🔍 Data Preparation

The dataset was checked for:

- Missing values
- Duplicate records
- Duplicate customer IDs
- Valid categorical values
- Binary variables
- Churn labels
- Numerical ranges

The `Year` column was removed because it contained a constant value, while `Surname` was removed because it was not required for analytical segmentation.

Additional customer segments were created for:

- Age
- Credit Score
- Tenure
- Balance

---

## 📈 Analysis Performed

The project includes analysis of:

### Geography
Comparison of customer churn across France, Germany, and Spain.

### Age
Customer segmentation into:

- `<30`
- `30–45`
- `46–60`
- `60+`

### Credit Score

Customers were grouped into:

- Low
- Medium
- High

### Tenure

Customers were classified as:

- New
- Mid-term
- Long-term

### Balance

Customers were classified into:

- Zero-balance
- Low-balance
- High-balance

Additional analysis covers:

- Gender
- Geography × Age
- Customer activity
- Number of products
- Credit card ownership
- Salary and balance
- Geography × Activity

---

## 📊 Key Findings

Some important observed patterns from the analysis are:

| Metric | Result |
|---|---:|
| Overall Churn Rate | 20.37% |
| France Churn Rate | 16.15% |
| Germany Churn Rate | 32.44% |
| Spain Churn Rate | 16.67% |
| Age 46–60 Churn Rate | 51.12% |
| High-Balance Churn Rate | 24.98% |
| Engagement Drop Indicator | 12.58 percentage points |
| New Customer Churn Rate | 21.14% |
| Low Credit Score Churn Rate | 21.75% |

These results represent observed patterns and associations within the dataset and should not be interpreted as proof of causal relationships.

---

## 📌 Key Performance Indicators

The project calculates several analytical KPIs:

- **Overall Churn Rate**
- **Segment Churn Rate**
- **High-Value Churn Ratio**
- **Geographic Risk Index**
- **Engagement Drop Indicator**

These KPIs are also incorporated into the Streamlit dashboard.

---

## 🖥️ Streamlit Dashboard

The interactive dashboard contains five major sections:

1. **Overview**
2. **Segment Analysis**
3. **High-Value Customers**
4. **Engagement**
5. **Financial Analysis**

The dashboard also provides:

- Geography filters
- Age segment filters
- Credit score filters
- Balance segment filters
- Dynamic KPI updates
- Customer data preview
- Filtered-data download

---


## 🖥️ Dashboard Preview

The project includes an interactive Streamlit dashboard for exploring customer churn patterns, customer segments, engagement, and financial characteristics.

### Dashboard Overview

![Dashboard Overview](Figures/17_dashboard_overview.png)

### Segment Analysis

![Segment Analysis](Figures/18_dashboard_segments.png)


## 🛠️ Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
- Jupyter Notebook
- VS Code

---

## 📁 Project Structure

```text
customer-segmentation-churn-analytics/
│
├── app.py
├── European_Bank.csv
├── analysis notebook
│
└── Figures/
    ├── 01_overall_churn.png
    ├── 02_geography_churn.png
    ├── 03_age_churn.png
    ├── 04_tenure_churn.png
    ├── 05_credit_score_churn.png
    ├── 06_balance_churn.png
    ├── 07_geography_age_heatmap.png
    ├── 08_gender_churn.png
    └── ...

## How to run the dashboard
1. Clone the repository
git clone https://github.com/abhishek-vishwakarma29/customer-segmentation-churn-analytics.git

2. Open the project folder
cd customer-segmentation-churn-analytics

3. Install the required libraries
pip install pandas matplotlib seaborn streamlit

4. Run the Streamlit application
python -m streamlit run app.py

The dashboard will open in your browser

## 📚 Project Deliverables

The project includes:

Data analysis notebook
Streamlit dashboard
Analytical visualizations
Customer segmentation analysis
Churn analysis
High-value customer analysis
Research paper

