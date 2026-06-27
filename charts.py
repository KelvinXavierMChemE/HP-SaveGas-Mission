"""
==========================================================
LPG SAFETY CHARTS
Author : Kelvin Xavier M

Contains all plotting functions used by Streamlit.
==========================================================
"""

import matplotlib.pyplot as plt
import pandas as pd


# ==========================================================
# PIE CHART
# ==========================================================

def risk_distribution_chart(df):

    risk_counts = df["Risk Category"].value_counts()

    fig, ax = plt.subplots(figsize=(5,5))

    ax.pie(
        risk_counts,
        labels=risk_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Risk Distribution")

    return fig


# ==========================================================
# HISTOGRAM
# ==========================================================

def risk_histogram(df):

    fig, ax = plt.subplots(figsize=(8,4))

    ax.hist(
        df["Risk Score"],
        bins=10
    )

    ax.set_title("Risk Score Distribution")

    ax.set_xlabel("Risk Score")

    ax.set_ylabel("Number of Customers")

    return fig


# ==========================================================
# DISTRICT RISK
# ==========================================================

def district_average_risk(df):

    if "District" not in df.columns:
        return None

    district = (
        df.groupby("District")["Risk Score"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8,5))

    district.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Average Risk by District")

    ax.set_ylabel("Average Risk Score")

    ax.set_xlabel("District")

    plt.xticks(rotation=45)

    plt.tight_layout()

    return fig


# ==========================================================
# RISK CATEGORY BAR CHART
# ==========================================================

def category_bar_chart(df):

    counts = (
        df["Risk Category"]
        .value_counts()
        .reindex(
            ["Low","Medium","High","Critical"],
            fill_value=0
        )
    )

    fig, ax = plt.subplots(figsize=(6,4))

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Customers by Risk Category")

    ax.set_xlabel("Risk Category")

    ax.set_ylabel("Customers")

    plt.tight_layout()

    return fig


# ==========================================================
# STOVE AGE DISTRIBUTION
# ==========================================================

def stove_age_chart(df):

    counts = df["Stove Age"].value_counts()

    fig, ax = plt.subplots(figsize=(6,4))

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Stove Age Distribution")

    ax.set_ylabel("Customers")

    plt.xticks(rotation=30)

    plt.tight_layout()

    return fig


# ==========================================================
# GAS SMELL RESPONSES
# ==========================================================

def gas_smell_chart(df):

    counts = df["Gas Smell"].value_counts()

    fig, ax = plt.subplots(figsize=(6,4))

    counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Gas Smell Responses")

    ax.set_ylabel("Customers")

    plt.tight_layout()

    return fig


# ==========================================================
# INSPECTION REQUESTS
# ==========================================================

def inspection_request_chart(df):

    if "Free Inspection" not in df.columns:
        return None

    counts = df["Free Inspection"].value_counts()

    fig, ax = plt.subplots(figsize=(5,5))

    ax.pie(
        counts,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title("Customers Requesting Inspection")

    return fig


# ==========================================================
# TOP HIGH-RISK CUSTOMERS
# ==========================================================

def top_high_risk(df, n=10):

    columns = [
        "Customer ID",
        "Customer Name",
        "District",
        "Risk Score",
        "Risk Category"
    ]

    available = [c for c in columns if c in df.columns]

    return (
        df.sort_values(
            by="Risk Score",
            ascending=False
        )[available]
        .head(n)
    )


# ==========================================================
# SUMMARY STATISTICS
# ==========================================================

def summary_statistics(df):

    summary = {

        "Total Customers":
            len(df),

        "Average Risk":
            round(df["Risk Score"].mean(),2),

        "Maximum Risk":
            df["Risk Score"].max(),

        "Minimum Risk":
            df["Risk Score"].min(),

        "Critical Customers":
            len(df[df["Risk Category"]=="Critical"]),

        "High Risk Customers":
            len(df[df["Risk Category"]=="High"]),

        "Medium Risk Customers":
            len(df[df["Risk Category"]=="Medium"]),

        "Low Risk Customers":
            len(df[df["Risk Category"]=="Low"])
    }

    return summary