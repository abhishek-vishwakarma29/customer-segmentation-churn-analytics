import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="European Banking Churn Analytics",
    page_icon="🏦",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv("European_Bank.csv")

# =========================================================
# CREATE SEGMENTATION COLUMNS
# =========================================================

# Age Segment
df["AgeSegment"] = pd.cut(
    df["Age"],
    bins=[0, 29, 45, 60, float("inf")],
    labels=["<30", "30–45", "46–60", "60+"]
)

# Credit Score Band
df["CreditScoreBand"] = pd.cut(
    df["CreditScore"],
    bins=[0, 599, 699, float("inf")],
    labels=["Low", "Medium", "High"]
)

# Tenure Group
df["TenureGroup"] = pd.cut(
    df["Tenure"],
    bins=[-1, 3, 6, 10],
    labels=["New", "Mid-term", "Long-term"]
)

# Balance Segment
balance_median = df["Balance"].median()

df["BalanceSegment"] = "Low-balance"

df.loc[
    df["Balance"] == 0,
    "BalanceSegment"
] = "Zero-balance"

df.loc[
    df["Balance"] > balance_median,
    "BalanceSegment"
] = "High-balance"

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")

selected_geography = st.sidebar.multiselect(
    "Select Geography",
    options=sorted(df["Geography"].unique()),
    default=sorted(df["Geography"].unique())
)

selected_age = st.sidebar.multiselect(
    "Select Age Group",
    options=df["AgeSegment"].dropna().unique().tolist(),
    default=df["AgeSegment"].dropna().unique().tolist()
)

selected_credit = st.sidebar.multiselect(
    "Select Credit Score",
    options=df["CreditScoreBand"].dropna().unique().tolist(),
    default=df["CreditScoreBand"].dropna().unique().tolist()
)

selected_balance = st.sidebar.multiselect(
    "Select Balance Segment",
    options=df["BalanceSegment"].unique(),
    default=df["BalanceSegment"].unique()
)

# Apply filters
filtered_df = df[
    (df["Geography"].isin(selected_geography)) &
    (df["AgeSegment"].isin(selected_age)) &
    (df["CreditScoreBand"].isin(selected_credit)) &
    (df["BalanceSegment"].isin(selected_balance))
]

st.sidebar.write(
    f"**Customers Selected:** {len(filtered_df):,}"
)

# =========================================================
# TITLE
# =========================================================

st.title("🏦 Customer Segmentation & Churn Pattern Analytics")
st.subheader("European Banking")

st.write(
    "Interactive analysis of customer churn, segmentation, "
    "engagement and financial characteristics."
)

# =========================================================
# KPI CALCULATIONS
# =========================================================

overall_churn_rate = (
    filtered_df["Exited"].mean() * 100
    if len(filtered_df) > 0 else 0
)

high_value_customers = filtered_df[
    filtered_df["BalanceSegment"] == "High-balance"
]

high_value_churn_ratio = (
    high_value_customers["Exited"].mean() * 100
    if len(high_value_customers) > 0 else 0
)

geography_summary = (
    filtered_df.groupby("Geography")["Exited"].mean() * 100
)

geographic_risk_index = (
    geography_summary.max() / overall_churn_rate
    if overall_churn_rate > 0 and len(geography_summary) > 0
    else 0
)

activity_summary = (
    filtered_df.groupby("IsActiveMember")["Exited"].mean() * 100
)

active_churn_rate = (
    activity_summary.loc[1]
    if 1 in activity_summary.index else 0
)

inactive_churn_rate = (
    activity_summary.loc[0]
    if 0 in activity_summary.index else 0
)

engagement_drop_indicator = (
    inactive_churn_rate - active_churn_rate
)

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview",
    "🌍 Segments",
    "💎 High-Value Customers",
    "👤 Engagement",
    "💰 Financial Analysis"
])

# =========================================================
# TAB 1 — OVERVIEW
# =========================================================

with tab1:

    st.header("📊 Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Overall Churn Rate",
            f"{overall_churn_rate:.2f}%"
        )

    with col2:
        st.metric(
            "High-Value Churn Ratio",
            f"{high_value_churn_ratio:.2f}%"
        )

    with col3:
        st.metric(
            "Geographic Risk Index",
            f"{geographic_risk_index:.2f}"
        )

    with col4:
        st.metric(
            "Engagement Drop",
            f"{engagement_drop_indicator:.2f} pp"
        )

    st.divider()

# =========================================================
# KEY INSIGHTS
# =========================================================

st.subheader("💡 Key Insights")

st.info(
    """
    • Overall customer churn in the dataset is 20.37%.

    • Germany has a churn rate of 32.44%, compared with 16.15% in France
      and 16.67% in Spain.

    • Customers aged 46–60 show a churn rate of 51.12%.

    • High-balance customers have a churn rate of 24.98%.

    • The engagement drop indicator is 12.58 percentage points,
      based on the difference between inactive and active customer
      churn rates.
    """
)

col1, col2 = st.columns(2)

with col1:
        st.metric(
            "Customers Selected",
            f"{len(filtered_df):,}"
        )

with col2:
        st.metric(
            "Customers Churned",
            f"{filtered_df['Exited'].sum():,}"
        )
            # =========================================================
    # PROJECT INFORMATION
    # =========================================================

st.subheader("📋 Project Information")

project_info = pd.DataFrame({
        "Item": [
            "Dataset",
            "Records",
            "Geographies",
            "Target Variable",
            "Analysis Focus"
        ],
        "Details": [
            "European Banking Customer Dataset",
            "10,000",
            "France, Germany, Spain",
            "Exited",
            "Customer Segmentation & Churn Analysis"
        ]
    })
st.dataframe(
    project_info,
    hide_index=True,
    use_container_width=True
)

st.write("### Dataset Preview")

st.dataframe(
    filtered_df.head(10),
    use_container_width=True
)
    # =========================================================
    # METHODOLOGY NOTE
    # =========================================================

st.subheader("Methodology Note")

st.caption(
        "Customer segments are created using the project-defined age, "
        "credit score, tenure and balance categories. Churn rates represent "
        "observed proportions of customers with Exited = 1 within each segment. "
        "These patterns describe associations in the dataset and should not "
        "be interpreted as causal effects."
    )
# ============================================================
# RETENTION RECOMMENDATIONS
# ============================================================

st.subheader("🎯 Retention Recommendations")

recommendations = pd.DataFrame({
    "Area": [
        "Germany",
        "Age 46–60",
        "High-Balance Customers",
        "Customer Engagement",
        "New Customers"
    ],
    "Recommended Action": [
        "Review country-specific customer experience, service patterns and product usage.",
        "Develop targeted engagement and retention initiatives for this age segment.",
        "Prioritize monitoring and retention efforts for customers with higher balances.",
        "Monitor inactive customers and strengthen engagement activities.",
        "Review onboarding and early-stage engagement to reduce early churn."
    ]
})

st.dataframe(
    recommendations,
    hide_index=True,
    use_container_width=True
)
# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.subheader("📥 Download Filtered Data")

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Customer Data",
    data=csv_data,
    file_name="filtered_customer_data.csv",
    mime="text/csv"
)
# =========================================================
# TAB 2 — SEGMENTS
# =========================================================

with tab2:

    st.header("🌍 Customer Segmentation")

    # -----------------------------
    # Geography
    # -----------------------------

    st.subheader("🌍 Geography Analysis")

    geography_summary = filtered_df.groupby("Geography").agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    geography_summary["Churn_Rate"] = (
        geography_summary["Churn_Rate"] * 100
    ).round(2)

    st.dataframe(
        geography_summary,
        use_container_width=True
    )

    st.bar_chart(
        geography_summary["Churn_Rate"]
    )

    # -----------------------------
    # Age
    # -----------------------------

    st.subheader("👥 Age Analysis")

    age_summary = filtered_df.groupby(
        "AgeSegment",
        observed=True
    ).agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    age_summary["Churn_Rate"] = (
        age_summary["Churn_Rate"] * 100
    ).round(2)

    st.dataframe(
        age_summary,
        use_container_width=True
    )

    st.bar_chart(
        age_summary["Churn_Rate"]
    )

    # -----------------------------
    # Tenure
    # -----------------------------

    st.subheader("⏳ Tenure Analysis")

    tenure_summary = filtered_df.groupby(
        "TenureGroup",
        observed=True
    ).agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    tenure_summary["Churn_Rate"] = (
        tenure_summary["Churn_Rate"] * 100
    ).round(2)

    st.dataframe(
        tenure_summary,
        use_container_width=True
    )

    st.bar_chart(
        tenure_summary["Churn_Rate"]
    )

    # -----------------------------
    # Credit Score
    # -----------------------------

    st.subheader("💳 Credit Score Analysis")

    credit_summary = filtered_df.groupby(
        "CreditScoreBand",
        observed=True
    ).agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    credit_summary["Churn_Rate"] = (
        credit_summary["Churn_Rate"] * 100
    ).round(2)

    st.dataframe(
        credit_summary,
        use_container_width=True
    )

    st.bar_chart(
        credit_summary["Churn_Rate"]
    )

    # -----------------------------
    # Balance
    # -----------------------------

    st.subheader("💰 Balance Analysis")

    balance_summary = filtered_df.groupby(
        "BalanceSegment"
    ).agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    balance_summary["Churn_Rate"] = (
        balance_summary["Churn_Rate"] * 100
    ).round(2)

    st.dataframe(
        balance_summary,
        use_container_width=True
    )

    st.bar_chart(
        balance_summary["Churn_Rate"]
    )

    # -----------------------------
    # Geography × Age
    # -----------------------------

    st.subheader("🌍👥 Geography × Age")

    geo_age_summary = filtered_df.groupby(
        ["Geography", "AgeSegment"],
        observed=True
    ).agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    ).reset_index()

    geo_age_summary["Churn_Rate"] = (
        geo_age_summary["Churn_Rate"] * 100
    ).round(2)

    geo_age_pivot = geo_age_summary.pivot(
        index="Geography",
        columns="AgeSegment",
        values="Churn_Rate"
    )

    st.dataframe(
        geo_age_pivot,
        use_container_width=True
    )

# =========================================================
# TAB 3 — HIGH-VALUE CUSTOMERS
# =========================================================

with tab3:

    st.header("💎 High-Value Customer Analysis")

    high_value_total = len(high_value_customers)

    high_value_churned = (
        high_value_customers["Exited"].sum()
    )

    high_value_churn_rate = (
        high_value_customers["Exited"].mean() * 100
        if high_value_total > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "High-Value Customers",
            f"{high_value_total:,}"
        )

    with col2:
        st.metric(
            "High-Value Churners",
            f"{high_value_churned:,}"
        )

    with col3:
        st.metric(
            "High-Value Churn Rate",
            f"{high_value_churn_rate:.2f}%"
        )

    st.divider()

    st.subheader("💎 High-Value Churn by Geography")

    high_value_geo = high_value_customers.groupby(
        "Geography"
    ).agg(
        High_Value_Customers=("CustomerId", "count"),
        Churned_High_Value=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    high_value_geo["Churn_Rate"] = (
        high_value_geo["Churn_Rate"] * 100
    ).round(2)

    st.dataframe(
        high_value_geo,
        use_container_width=True
    )

    st.bar_chart(
        high_value_geo["Churn_Rate"]
    )

# =========================================================
# TAB 4 — ENGAGEMENT
# =========================================================

with tab4:

    st.header("👤 Engagement & Product Analysis")

    # -----------------------------
    # Activity
    # -----------------------------

    st.subheader("👤 Active vs Inactive Customers")

    activity_summary = filtered_df.groupby(
        "IsActiveMember"
    ).agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    activity_summary["Churn_Rate"] = (
        activity_summary["Churn_Rate"] * 100
    ).round(2)

    activity_summary.index = activity_summary.index.map({
        0: "Inactive",
        1: "Active"
    })

    st.dataframe(
        activity_summary,
        use_container_width=True
    )

    st.bar_chart(
        activity_summary["Churn_Rate"]
    )

    # -----------------------------
    # Products
    # -----------------------------

    st.subheader("📦 Number of Products")

    product_summary = filtered_df.groupby(
        "NumOfProducts"
    ).agg(
        Total_Customers=("CustomerId", "count"),
        Churned_Customers=("Exited", "sum"),
        Churn_Rate=("Exited", "mean")
    )

    product_summary["Churn_Rate"] = (
        product_summary["Churn_Rate"] * 100
    ).round(2)

    st.dataframe(
        product_summary,
        use_container_width=True
    )

    st.bar_chart(
        product_summary["Churn_Rate"]
    )

# =========================================================
# TAB 5 — FINANCIAL ANALYSIS
# =========================================================

with tab5:

    st.header("💰 Financial Analysis")

    # -----------------------------
    # Financial Profile
    # -----------------------------

    st.subheader("Financial Profile: Churned vs Retained")

    financial_summary = filtered_df.groupby(
        "Exited"
    ).agg(
        Average_Balance=("Balance", "mean"),
        Average_Salary=("EstimatedSalary", "mean"),
        Total_Customers=("CustomerId", "count")
    )

    financial_summary.index = financial_summary.index.map({
        0: "Retained",
        1: "Churned"
    })

    financial_summary["Average_Balance"] = (
        financial_summary["Average_Balance"].round(2)
    )

    financial_summary["Average_Salary"] = (
        financial_summary["Average_Salary"].round(2)
    )

    st.dataframe(
        financial_summary,
        use_container_width=True
    )

    # -----------------------------
    # Balance vs Salary
    # -----------------------------

    st.subheader("Balance vs Estimated Salary")

    st.scatter_chart(
        filtered_df,
        x="EstimatedSalary",
        y="Balance"
    )

    st.caption(
        "This chart shows the observed relationship between "
        "estimated salary and account balance."
    )

    # -----------------------------
    # High-value financial profile
    # -----------------------------

    st.subheader("High-Value Customer Financial Profile")

    if len(high_value_customers) > 0:

        high_value_financial = high_value_customers.groupby(
            "Exited"
        ).agg(
            Average_Balance=("Balance", "mean"),
            Average_Salary=("EstimatedSalary", "mean"),
            Customers=("CustomerId", "count")
        )

        high_value_financial.index = (
            high_value_financial.index.map({
                0: "Retained",
                1: "Churned"
            })
        )

        high_value_financial[
            "Average_Balance"
        ] = high_value_financial[
            "Average_Balance"
        ].round(2)

        high_value_financial[
            "Average_Salary"
        ] = high_value_financial[
            "Average_Salary"
        ].round(2)

        st.dataframe(
            high_value_financial,
            use_container_width=True
        )

    else:

        st.info(
            "No high-value customers match the selected filters."
        )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Customer Segmentation & Churn Pattern Analytics "
    "| European Banking"
)