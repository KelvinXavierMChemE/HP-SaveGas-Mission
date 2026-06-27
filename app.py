"""
==========================================================
SafeFlame
LPG Safety Intelligence Platform

Author : Kelvin Xavier M

Main Streamlit Application
==========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd

from risk_engine import analyze_dataframe

from charts import (
    summary_statistics,
    top_high_risk,
    risk_distribution_chart,
    district_average_risk,
    risk_histogram,
    category_bar_chart,
    stove_age_chart,
    gas_smell_chart,
    inspection_request_chart
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="SafeFlame",
    page_icon="🔥",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================

st.title("🔥 SafeFlame")
st.subheader("LPG Safety Intelligence Platform")

st.markdown(
"""
Upload customer survey responses to automatically identify
high-risk LPG connections and generate actionable insights.
"""
)

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Navigation")

st.sidebar.success("Upload an Excel file to begin analysis.")

st.sidebar.markdown("---")

st.sidebar.info(
"""
Workflow

1. Upload Excel

2. Automatic Risk Assessment

3. Dashboard

4. Customer Analysis

5. Download Reports
"""
)

# ==========================================================
# FILE UPLOAD
# ==========================================================

uploaded_file = st.file_uploader(
    "Upload Microsoft Forms Responses (.xlsx)",
    type=["xlsx"]
)

# ==========================================================
# MAIN PROGRAM
# ==========================================================

if uploaded_file is not None:

    # ------------------------------------
    # Read Excel
    # ------------------------------------

    df = pd.read_excel(uploaded_file)

    # ------------------------------------
    # Analyze
    # ------------------------------------

    df = analyze_dataframe(df)

    # ------------------------------------
    # Statistics
    # ------------------------------------

    stats = summary_statistics(df)

    st.success("Analysis Completed Successfully.")

    st.divider()

    # ======================================================
    # KPI CARDS
    # ======================================================

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "Customers",
        stats["Total Customers"]
    )

    col2.metric(
        "Low Risk",
        stats["Low Risk Customers"]
    )

    col3.metric(
        "Medium Risk",
        stats["Medium Risk Customers"]
    )

    col4.metric(
        "High Risk",
        stats["High Risk Customers"]
    )

    col5.metric(
        "Critical",
        stats["Critical Customers"]
    )

    col6.metric(
        "Average Risk",
        stats["Average Risk"]
    )

    st.divider()
    
        # ======================================================
    # EXECUTIVE SUMMARY
    # ======================================================
    
    st.header("📋 Executive Summary")
    
    high_percent = (
        (stats["High Risk Customers"] + stats["Critical Customers"])
        / stats["Total Customers"]
    ) * 100
    
    avg_risk = stats["Average Risk"]
    
    inspection_requests = 0
    
    if "Free Inspection" in df.columns:
        inspection_requests = len(
            df[df["Free Inspection"] == "Yes"]
        )
    
    summary = f"""
    • Total customers surveyed : **{stats['Total Customers']}**
    
    • **{high_percent:.1f}%** of customers belong to the High/Critical risk category.
    
    • Average Risk Score : **{avg_risk:.1f}**
    
    • High Risk Customers : **{stats['High Risk Customers']}**
    
    • Critical Customers : **{stats['Critical Customers']}**
    
    • Customers requesting inspection : **{inspection_requests}**
    """
    
    st.info(summary)
    
    st.divider()
    
    # ======================================================
    # SIDEBAR FILTERS
    # ======================================================
    
    st.sidebar.header("Filters")
    
    filtered_df = df.copy()
    
    if "District" in df.columns:
    
        districts = sorted(df["District"].dropna().unique())
    
        selected_district = st.sidebar.selectbox(
            "District",
            ["All"] + list(districts)
        )
    
        if selected_district != "All":
    
            filtered_df = filtered_df[
                filtered_df["District"] == selected_district
            ]
    
    risk_filter = st.sidebar.selectbox(
        "Risk Category",
        ["All", "Low", "Medium", "High", "Critical"]
    )
    
    if risk_filter != "All":
    
        filtered_df = filtered_df[
            filtered_df["Risk Category"] == risk_filter
        ]
    
    st.sidebar.write(f"Customers : {len(filtered_df)}")
    
    # ======================================================
    # CUSTOMER SEARCH
    # ======================================================
    
    st.header("🔍 Customer Search")
    
    search_column = st.selectbox(
        "Search By",
        ["Customer ID", "Customer Name"]
    )
    
    search_value = st.text_input(
        "Enter Search Value"
    )
    
    customer_df = filtered_df
    
    if search_value.strip() != "":
    
        customer_df = filtered_df[
            filtered_df[search_column]
            .astype(str)
            .str.contains(
                search_value,
                case=False,
                na=False
            )
        ]
    
    st.dataframe(
        customer_df,
        use_container_width=True
    )
    
    st.divider()
    
    # ======================================================
    # CUSTOMER PROFILE
    # ======================================================
    
    st.header("👤 Customer Profile")
    
    if len(customer_df) == 0:
    
        st.warning("No customer found.")
    
    else:
    
        customer = customer_df.iloc[0]
    
        col1, col2 = st.columns(2)
    
        with col1:
    
            st.subheader("Basic Information")
    
            st.write("**Customer ID:**", customer["Customer ID"])
    
            st.write("**Customer Name:**", customer["Customer Name"])
    
            if "District" in customer.index:
                st.write("**District:**", customer["District"])
    
            st.write("**Risk Score:**", customer["Risk Score"])
    
            st.write("**Risk Category:**", customer["Risk Category"])
    
        with col2:
    
            st.subheader("Recommendation")
    
            st.success(
                customer["Recommendation"]
            )
    
        st.subheader("Reasons for Risk")
    
        if customer["Reasons"] == "":
    
            st.success("No significant safety concerns identified.")
    
        else:
    
            st.text(customer["Reasons"])
    
    st.divider()
    
    
        # ======================================================
    # DASHBOARD VISUALIZATIONS
    # ======================================================
    
    st.header("📊 Dashboard")
    
    # ------------------------------------------------------
    # FIRST ROW
    # ------------------------------------------------------
    
    col1, col2 = st.columns(2)
    
    with col1:
    
        st.subheader("Risk Distribution")
    
        fig = risk_distribution_chart(filtered_df)
    
        st.pyplot(fig)
    
    
    with col2:
    
        st.subheader("Customers by Risk Category")
    
        fig = category_bar_chart(filtered_df)
    
        st.pyplot(fig)
    
    
    st.divider()
    
    # ------------------------------------------------------
    # SECOND ROW
    # ------------------------------------------------------
    
    col3, col4 = st.columns(2)
    
    with col3:
    
        st.subheader("Risk Score Distribution")
    
        fig = risk_histogram(filtered_df)
    
        st.pyplot(fig)
    
    
    with col4:
    
        if "District" in filtered_df.columns:
    
            st.subheader("Average Risk by District")
    
            fig = district_average_risk(filtered_df)
    
            if fig is not None:
    
                st.pyplot(fig)
    
            else:
    
                st.info("District information unavailable.")
    
        else:
    
            st.info("District column not found.")
    
    
    st.divider()
    
    # ------------------------------------------------------
    # THIRD ROW
    # ------------------------------------------------------
    
    col5, col6 = st.columns(2)
    
    with col5:
    
        st.subheader("Stove Age Distribution")
    
        fig = stove_age_chart(filtered_df)
    
        st.pyplot(fig)
    
    
    with col6:
    
        st.subheader("Gas Smell Responses")
    
        fig = gas_smell_chart(filtered_df)
    
        st.pyplot(fig)
    
    st.divider()
    
    # ------------------------------------------------------
    # OPTIONAL INSPECTION CHART
    # ------------------------------------------------------
    
    if "Free Inspection" in filtered_df.columns:
    
        st.subheader("Inspection Requests")
    
        fig = inspection_request_chart(filtered_df)
    
        if fig is not None:
    
            st.pyplot(fig)
    
    st.divider()
    
    # ======================================================
    # TOP HIGH RISK CUSTOMERS
    # ======================================================
    
    st.header("🚨 Top High-Risk Customers")
    
    top_customers = top_high_risk(filtered_df)
    
    st.dataframe(
        top_customers,
        use_container_width=True
    )
    
    st.divider()
    
    # ======================================================
    # QUICK INSIGHTS
    # ======================================================
    
    st.header("📈 Quick Insights")
    
    highest = filtered_df["Risk Score"].max()
    
    lowest = filtered_df["Risk Score"].min()
    
    average = filtered_df["Risk Score"].mean()
    
    st.write(f"Highest Risk Score : **{highest}**")
    
    st.write(f"Lowest Risk Score : **{lowest}**")
    
    st.write(f"Average Risk Score : **{average:.2f}**")
    
    if "District" in filtered_df.columns:
    
        district_avg = (
            filtered_df
            .groupby("District")["Risk Score"]
            .mean()
            .sort_values(ascending=False)
        )
    
        highest_district = district_avg.index[0]
    
        st.success(
            f"District with highest average risk : **{highest_district}**"
        )
    
    st.divider()
    
    # ======================================================
    # SAFETY RECOMMENDATIONS
    # ======================================================
    
    st.header("🛡 Recommended Actions")
    
    critical = len(
        filtered_df[
            filtered_df["Risk Category"]=="Critical"
        ]
    )
    
    high = len(
        filtered_df[
            filtered_df["Risk Category"]=="High"
        ]
    )
    
    medium = len(
        filtered_df[
            filtered_df["Risk Category"]=="Medium"
        ]
    )
    
    if critical > 0:
    
        st.error(
            f"Immediate inspection required for {critical} customer(s)."
        )
    
    if high > 0:
    
        st.warning(
            f"Schedule inspection within one week for {high} customer(s)."
        )
    
    if medium > 0:
    
        st.info(
            f"Customer awareness campaign recommended for {medium} customer(s)."
        )
    
    if critical==0 and high==0:
    
        st.success(
            "No immediate inspections are currently required."
        )
    
    st.divider()
    
    
        # ======================================================
    # DOWNLOADABLE REPORTS
    # ======================================================
    
    from io import BytesIO
    
    st.header("📥 Download Reports")
    
    col1, col2, col3 = st.columns(3)
    
    # ----------------------------
    # Complete Report
    # ----------------------------
    
    with col1:
    
        output = BytesIO()
    
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            filtered_df.to_excel(
                writer,
                index=False,
                sheet_name="Risk Report"
            )
    
        st.download_button(
            "⬇ Download Complete Report",
            output.getvalue(),
            file_name="LPG_Risk_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # ----------------------------
    # High Risk Report
    # ----------------------------
    
    with col2:
    
        high_df = filtered_df[
            filtered_df["Risk Category"].isin(
                ["High","Critical"]
            )
        ]
    
        output2 = BytesIO()
    
        with pd.ExcelWriter(output2, engine="openpyxl") as writer:
            high_df.to_excel(
                writer,
                index=False,
                sheet_name="High Risk"
            )
    
        st.download_button(
            "🚨 Download High Risk List",
            output2.getvalue(),
            file_name="High_Risk_Customers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # ----------------------------
    # Inspection Requests
    # ----------------------------
    
    with col3:
    
        if "Free Inspection" in filtered_df.columns:
    
            inspect_df = filtered_df[
                filtered_df["Free Inspection"]=="Yes"
            ]
    
        else:
    
            inspect_df = pd.DataFrame()
    
        output3 = BytesIO()
    
        with pd.ExcelWriter(output3, engine="openpyxl") as writer:
            inspect_df.to_excel(
                writer,
                index=False,
                sheet_name="Inspection Requests"
            )
    
        st.download_button(
            "🛠 Inspection Requests",
            output3.getvalue(),
            file_name="Inspection_List.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    st.divider()
    
    # ======================================================
    # MANAGEMENT SUMMARY
    # ======================================================
    
    st.header("📋 Management Summary")
    
    critical = stats["Critical Customers"]
    high = stats["High Risk Customers"]
    medium = stats["Medium Risk Customers"]
    low = stats["Low Risk Customers"]
    
    summary = f"""
    ### Executive Findings
    
    • Total customers analyzed : **{stats['Total Customers']}**
    
    • Average Risk Score : **{stats['Average Risk']:.2f}**
    
    • **{critical}** Critical-risk customers require immediate inspection.
    
    • **{high}** High-risk customers should be inspected within one week.
    
    • **{medium}** Medium-risk customers should receive preventive maintenance awareness.
    
    • **{low}** customers currently present minimal safety concerns.
    
    ---
    
    ### Recommended Actions
    
    ✅ Prioritize inspections for Critical customers.
    
    ✅ Schedule preventive maintenance for High-risk customers.
    
    ✅ Conduct awareness campaigns for Medium-risk customers.
    
    ✅ Continue periodic monitoring for Low-risk customers.
    """
    
    st.markdown(summary)
    
    st.divider()
    
    # ======================================================
    # ABOUT THE PROJECT
    # ======================================================
    
    with st.expander("ℹ About SafeFlame"):
    
        st.markdown("""
    ### SafeFlame
    
    SafeFlame is a prototype LPG Safety Intelligence Platform.
    
    Workflow
    
    Customer Database
    
    ↓
    
    Personalized Email (Power Automate)
    
    ↓
    
    Microsoft Forms
    
    ↓
    
    Streamlit Risk Engine
    
    ↓
    
    Analytics Dashboard
    
    ↓
    
    Inspection Reports
    
    This prototype demonstrates how digital technologies can automate
    customer outreach, safety assessment and managerial decision making.
    """)
    
    st.divider()
    
    # ======================================================
    # FOOTER
    # ======================================================
    
    st.markdown("---")
    
    st.caption(
        "Developed by Kelvin Xavier M | Prototype for Automation Hackathon | Powered by Python & Streamlit"
    )

    # ======================================================
    # DATA PREVIEW
    # ======================================================

    with st.expander("📄 View Processed Dataset"):

        st.dataframe(
            df,
            use_container_width=True
        )

    # ======================================================
    # Remaining dashboard continues in Part 2...
    # ======================================================

else:

    st.info("Please upload an Excel file to begin.")