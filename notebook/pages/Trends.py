import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/")

# ✅ Load and clean data
df = pd.read_csv("C:/Users/user/OneDrive/Desktop/All Files/All work project/data-financial-inclusion-and-digital-payment-adoption/data/processed/world data.csv")
df["Indicator value"] = df["Indicator value"].astype(str).str.replace('%', '', regex=False).astype(float)

# ✅ Define indicators and filter for key years
key_indicators = [
    "Account (% age 15+)",
    "Financial institution account (% age 15+)",
    "Mobile money account (% age 15+)",
    "Made or received digital payments (% age 15+)"
]
df_filtered = df[
    (df["Indicator"].isin(key_indicators)) &
    (df["Year"].isin([2011, 2014, 2017, 2021]))
].copy()

# ✅ Layout
layout = html.Div([
    html.H2("📊 Q1: Financial Inclusion Trends — Compare Global/Regions with Rwanda",
            style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Financial Indicator:"),
        dcc.Dropdown(
            id="indicator-dropdown",
            options=[{"label": ind, "value": ind} for ind in key_indicators],
            value="Account (% age 15+)",
            clearable=False
        ),
    ], style={"width": "50%", "margin": "auto"}),

    html.Div([
        html.Label("Select View:"),
        dcc.RadioItems(
            id="view-toggle",
            options=[
                {"label": "Global", "value": "Global"},
                {"label": "Regional", "value": "Regional"},
                {"label": "Rwanda", "value": "Rwanda"}
            ],
            value="Global",
            labelStyle={"display": "inline-block", "margin-right": "10px"}
        ),
    ], style={"width": "50%", "margin": "auto", "padding": "20px", "textAlign": "center"}),

    dcc.Graph(id="combined-trend")
])

# ✅ Callback to update the figure
@dash.callback(
    Output("combined-trend", "figure"),
    Input("indicator-dropdown", "value"),
    Input("view-toggle", "value")
)
def update_combined_trend(indicator, view):
    trend_data = []

    if view == "Global":
        global_df = df_filtered[df_filtered["Indicator"] == indicator].groupby("Year")["Indicator value"].mean().reset_index()
        global_df["Source"] = "Global Average"
        trend_data.append(global_df)

        # Also add Rwanda for comparison
        rwanda_df = df_filtered[
            (df_filtered["Indicator"] == indicator) &
            (df_filtered["Country name"] == "Rwanda")
        ][["Year", "Indicator value"]].copy()
        rwanda_df["Source"] = "Rwanda"
        trend_data.append(rwanda_df)

    elif view == "Regional":
        region_df = df_filtered[df_filtered["Indicator"] == indicator].groupby(["Region", "Year"])["Indicator value"].mean().reset_index()
        region_df.rename(columns={"Region": "Source"}, inplace=True)
        trend_data.append(region_df)

        # Also add Rwanda for comparison
        rwanda_df = df_filtered[
            (df_filtered["Indicator"] == indicator) &
            (df_filtered["Country name"] == "Rwanda")
        ][["Year", "Indicator value"]].copy()
        rwanda_df["Source"] = "Rwanda"
        trend_data.append(rwanda_df)

    elif view == "Rwanda":
        rwanda_df = df_filtered[
            (df_filtered["Indicator"] == indicator) &
            (df_filtered["Country name"] == "Rwanda")
        ][["Year", "Indicator value"]].copy()
        rwanda_df["Source"] = "Rwanda"
        trend_data.append(rwanda_df)

    if not trend_data:
        return px.line(title="No data available for selected view.")

    combined_df = pd.concat(trend_data, ignore_index=True)

    fig = px.line(
        combined_df,
        x="Year",
        y="Indicator value",
        color="Source",
        markers=True,
        title=f"{indicator} — Trends: {view} Comparison",
        labels={"Indicator value": "%", "Source": "Scope"},
        height=600
    )

    # Show value labels for Global and Rwanda only
    for trace in fig.data:
        if trace.name in ["Global Average", "Rwanda"]:
            trace.mode = "lines+markers+text"
            trace.text = [f"{y:.1f}%" for y in trace.y]
            trace.textposition = "top center"
        else:
            trace.mode = "lines+markers"

    fig.update_layout(hovermode="x unified")

    return fig
