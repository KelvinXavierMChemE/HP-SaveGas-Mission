

"""
==========================================================
LPG SAFETY RISK ENGINE
Author : Kelvin Xavier M
Description:
Contains all business logic for LPG safety assessment.
==========================================================
"""

import pandas as pd


# --------------------------------------------------------
# Risk Calculation
# --------------------------------------------------------

def calculate_risk(row):
    """
    Calculates risk score for one customer.
    Returns:
        score
        reasons
        recommendation
    """

    score = 0
    reasons = []

    # -------------------------
    # Stove Age
    # -------------------------

    if row["Stove Age"] == "More than 15 years":
        score += 40
        reasons.append("Stove is older than 15 years.")

    elif row["Stove Age"] == "10–15 years":
        score += 20
        reasons.append("Stove is between 10 and 15 years old.")

    # -------------------------
    # Hose Age
    # -------------------------

    if row["Hose Age"] == "More than 5 years":
        score += 20
        reasons.append("Rubber hose is older than 5 years.")

    elif row["Hose Age"] == "Don't know":
        score += 10
        reasons.append("Customer does not know hose age.")

    # -------------------------
    # Burners
    # -------------------------

    if int(row["Burners"]) >= 3:
        score += 10
        reasons.append("Multiple burner stove.")

    # -------------------------
    # Gas Smell
    # -------------------------

    if row["Gas Smell"] == "Frequently":
        score += 50
        reasons.append("Customer frequently notices LPG smell.")

    elif row["Gas Smell"] == "Once":
        score += 25
        reasons.append("Gas smell noticed earlier.")

    # -------------------------
    # Last Service
    # -------------------------

    if row["Last Service"] == "Never":
        score += 25
        reasons.append("Stove has never been serviced.")

    elif row["Last Service"] == "More than 3 years":
        score += 15
        reasons.append("Service overdue.")

    # -------------------------
    # Regulator
    # -------------------------

    if row["Regulator Condition"] == "Damaged":
        score += 30
        reasons.append("Regulator reported damaged.")

    elif row["Regulator Condition"] == "Not Sure":
        score += 10
        reasons.append("Regulator condition unknown.")

    # -------------------------
    # Soap Test
    # -------------------------

    if row["Soap Test"] == "Never":
        score += 20
        reasons.append("Leak test never performed.")

    elif row["Soap Test"] == "Occasionally":
        score += 10
        reasons.append("Leak test not performed regularly.")

    # -------------------------
    # Regulator Closing Habit
    # -------------------------

    if row["Close Regulator"] == "Never":
        score += 20
        reasons.append("Regulator not closed after cooking.")

    elif row["Close Regulator"] == "Sometimes":
        score += 10
        reasons.append("Regulator not always closed.")

    # -------------------------
    # Kitchen Ventilation
    # -------------------------

    if row["Ventilation"] == "No":
        score += 20
        reasons.append("Kitchen lacks ventilation.")

    elif row["Ventilation"] == "Partially":
        score += 10
        reasons.append("Kitchen partially ventilated.")

    # -------------------------
    # Cylinder Location
    # -------------------------

    if row["Cylinder Location"] == "Closed cabinet":
        score += 20
        reasons.append("Cylinder kept inside closed cabinet.")

    # -------------------------
    # Hose Certification
    # -------------------------

    if row["ISI Hose"] == "No":
        score += 20
        reasons.append("Non-ISI hose being used.")

    elif row["ISI Hose"] == "Don't Know":
        score += 10
        reasons.append("Customer unaware of hose certification.")

    # ------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------

    if score >= 130:

        recommendation = (
            "Immediate inspection recommended within 24 hours."
        )

    elif score >= 80:

        recommendation = (
            "Inspection recommended within one week."
        )

    elif score >= 40:

        recommendation = (
            "Customer awareness and preventive maintenance advised."
        )

    else:

        recommendation = (
            "No immediate action required."
        )

    return score, reasons, recommendation


# --------------------------------------------------------
# Category
# --------------------------------------------------------

def classify_risk(score):

    if score >= 130:
        return "Critical"

    elif score >= 80:
        return "High"

    elif score >= 40:
        return "Medium"

    else:
        return "Low"


# --------------------------------------------------------
# Entire DataFrame
# --------------------------------------------------------

def analyze_dataframe(df):

    scores = []
    categories = []
    reasons_list = []
    recommendations = []

    for _, row in df.iterrows():

        score, reasons, recommendation = calculate_risk(row)

        scores.append(score)

        categories.append(
            classify_risk(score)
        )

        reasons_list.append(
            "\n".join(reasons)
        )

        recommendations.append(
            recommendation
        )

    df["Risk Score"] = scores
    df["Risk Category"] = categories
    df["Reasons"] = reasons_list
    df["Recommendation"] = recommendations

    return df