import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Register this page with path /demographic
dash.register_page(__name__, path="/demographics")

# Load and clean the data once (update your path accordingly)
df = pd.read_csv(
    r"C:/Users/user/OneDrive/Desktop/All Files/All work project/data-financial-inclusion-and-digital-payment-adoption/data/processed/world data.csv"
)

# Clean 'Indicator value' column: remove '%' and convert to float
df["Indicator value"] = (
    df["Indicator value"].astype(str).str.replace("%", "", regex=False).astype(float)
)

# Keywords to identify DFS (Digital Financial Service) indicators
dfs_keywords = [
    "mobile money",
    "digital payment",
    "internet",
    "online",
    "send money",
    "receive money",
    "used a mobile phone",
    "used the internet",
    "e-wallet",
    "used a mobile",
]

def assign_type(indicator):
    if pd.isna(indicator):
        return "Account"  # default if missing
    indicator_lower = indicator.lower()
    if any(keyword in indicator_lower for keyword in dfs_keywords):
        return "DFS"
    else:
        return "Account"

df["Type"] = df["Indicator"].apply(assign_type)

# Split into Account and DFS dataframes
account_df = df[df["Type"] == "Account"]
dfs_df = df[df["Type"] == "DFS"]

# Filter data by demographic groups (using partial match)
account_data = {
    "Age": account_df[account_df["Indicator"].str.contains("Age", case=False, na=False)],
    "Gender": account_df[account_df["Indicator"].str.contains("female|male", case=False, na=False)],
    "Education": account_df[account_df["Indicator"].str.contains("Education", case=False, na=False)],
    "Income": account_df[account_df["Indicator"].str.contains("Income", case=False, na=False)],
}

dfs_data = {
    "Age": dfs_df[dfs_df["Indicator"].str.contains("Age", case=False, na=False)],
    "Gender": dfs_df[dfs_df["Indicator"].str.contains("female|male", case=False, na=False)],
    "Education": dfs_df[dfs_df["Indicator"].str.contains("Education", case=False, na=False)],
    "Income": dfs_df[dfs_df["Indicator"].str.contains("Income", case=False, na=False)],
}

# Dash page layout
layout = html.Div(
    [
        html.H2(
            "📊 Q2: Demographic Breakdown — Financial Inclusion",
            style={"textAlign": "center", "marginBottom": "20px"},
        ),
        html.Div(
            [
                html.Label("Select Data Type:"),
                dcc.Dropdown(
                    id="data-type",
                    options=[
                        {"label": "Account Ownership", "value": "Account"},
                        {"label": "Digital Financial Service Usage", "value": "DFS"},
                    ],
                    value="Account",
                    clearable=False,
                ),
            ],
            style={"width": "45%", "display": "inline-block", "padding": "0 20px"},
        ),
        html.Div(
            [
                html.Label("Select Demographic Factor:"),
                dcc.Dropdown(
                    id="demographic",
                    options=[
                        {"label": "Age", "value": "Age"},
                        {"label": "Gender", "value": "Gender"},
                        {"label": "Education", "value": "Education"},
                        {"label": "Income", "value": "Income"},
                    ],
                    value="Age",
                    clearable=False,
                ),
            ],
            style={"width": "45%", "display": "inline-block"},
        ),
        dcc.Graph(id="bar-graph", style={"marginTop": "40px"}),
    ],
    style={"maxWidth": "900px", "margin": "auto"},
)

# Callback for updating the bar graph based on dropdown selections
@dash.callback(
    Output("bar-graph", "figure"),
    [Input("data-type", "value"), Input("demographic", "value")],
)
def update_graph(data_type, demographic):
    if data_type == "Account":
        df_selected = account_data.get(demographic)
    else:
        df_selected = dfs_data.get(demographic)

    if df_selected is None or df_selected.empty:
        return px.bar(title="No data available for this selection.")

    # Group by 'Indicator' and average 'Indicator value'
    df_summary = (
        df_selected.groupby("Indicator")["Indicator value"]
        .mean()
        .reset_index()
        .sort_values(by="Indicator value", ascending=True)
        .head(20)
    )

    # Create horizontal bar chart
    fig = px.bar(
        df_summary,
        x="Indicator value",
        y="Indicator",
        orientation="h",
        title=f"{data_type} by {demographic}",
        labels={"Indicator value": "%"},
        text_auto=".2s",
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        margin={"t": 50, "b": 100},
        yaxis={"categoryorder": "total ascending"},
    )

    return fig
