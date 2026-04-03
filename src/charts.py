"""
Chart builder module for the Eco-Formulation Copilot.

This file creates the interactive Plotly charts that appear in the
dashboard section of the Streamlit app. Each function takes the
formulations DataFrame and returns a Plotly figure object.

WHY PLOTLY (not Matplotlib):
Plotly charts are interactive — the recruiter can hover over data points,
zoom in, and filter. This mimics Power BI functionality, which is exactly
what the P&G job description asks for. Matplotlib produces static images.

FLOW:
    DataFrame (from data_loader.py)
        ↓
    build_scatter_chart() → Interactive scatter plot figure
    build_bar_chart()     → Interactive bar chart figure
    build_surfactant_pie_chart() → Distribution pie chart figure
        ↓
    Returned to app.py → Rendered inside Streamlit
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def build_scatter_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates an interactive scatter plot: Cost vs Biodegradability.

    Each dot is one formulation. The X axis shows how much it costs.
    The Y axis shows how biodegradable it is. The colour shows
    the cleaning efficacy score.

    WHY THIS CHART:
    P&G scientists constantly balance cost against sustainability.
    This chart instantly shows which formulas are cheap AND eco-friendly
    (bottom-right corner = ideal zone).

    Parameters:
        df: The formulations DataFrame from data_loader.py

    Returns:
        A Plotly Figure object ready to be displayed in Streamlit.
    """
    fig = px.scatter(
        df,
        x="Cost_Per_Litre_GBP",
        y="Biodegradability_Score",
        color="Cleaning_Efficacy_Score",
        hover_data=["Formula_ID", "Surfactant_Type", "Toxicity_Level"],
        title="Cost vs Biodegradability (colour = Cleaning Efficacy)",
        labels={
            "Cost_Per_Litre_GBP": "Cost per Litre (£)",
            "Biodegradability_Score": "Biodegradability Score (0-100)",
            "Cleaning_Efficacy_Score": "Cleaning Efficacy (0-100)",
        },
        color_continuous_scale="Viridis",
    )

    fig.update_layout(
        template="plotly_white",
        height=450,
        margin=dict(l=40, r=40, t=50, b=40),
    )

    return fig


def build_bar_chart(df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Creates a horizontal bar chart of the Top N most effective formulas.

    Sorted by Cleaning_Efficacy_Score in descending order.
    The colour of each bar shows the Biodegradability_Score.

    WHY THIS CHART:
    Scientists want to quickly see which formulas clean best.
    Showing biodegradability as the colour answers the follow-up
    question: "But are the best cleaners also eco-friendly?"

    Parameters:
        df: The formulations DataFrame from data_loader.py
        top_n: Number of top formulas to show. Defaults to 10.

    Returns:
        A Plotly Figure object ready to be displayed in Streamlit.
    """
    top_df = df.nlargest(top_n, "Cleaning_Efficacy_Score")

    fig = px.bar(
        top_df,
        x="Cleaning_Efficacy_Score",
        y="Formula_ID",
        orientation="h",
        color="Biodegradability_Score",
        hover_data=["Surfactant_Type", "Cost_Per_Litre_GBP", "Toxicity_Level"],
        title=f"Top {top_n} Formulas by Cleaning Efficacy (colour = Biodegradability)",
        labels={
            "Cleaning_Efficacy_Score": "Cleaning Efficacy Score (0-100)",
            "Formula_ID": "Formula",
            "Biodegradability_Score": "Biodegradability (0-100)",
        },
        color_continuous_scale="Greens",
    )

    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
        yaxis=dict(categoryorder="total ascending"),
    )

    return fig


def build_surfactant_pie_chart(df: pd.DataFrame) -> go.Figure:
    """
    Creates a pie chart showing the distribution of surfactant types.

    WHY THIS CHART:
    It gives an instant overview of how many formulas use each
    surfactant. If one type dominates the dataset, the scientist
    knows the testing is skewed and may want to balance it.

    Parameters:
        df: The formulations DataFrame from data_loader.py

    Returns:
        A Plotly Figure object ready to be displayed in Streamlit.
    """
    surfactant_counts = df["Surfactant_Type"].value_counts().reset_index()
    surfactant_counts.columns = ["Surfactant_Type", "Count"]

    fig = px.pie(
        surfactant_counts,
        names="Surfactant_Type",
        values="Count",
        title="Surfactant Type Distribution",
        hole=0.3,
    )

    fig.update_layout(
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
    )

    return fig
