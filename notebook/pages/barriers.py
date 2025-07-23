import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Register page
dash.register_page(__name__, path="/barriers", name="Barriers to Inclusion")

# Load dataset
df = pd.read_csv("C:/Users/user/OneDrive/Desktop/All Files/All work project/data-financial-inclusion-and-digital-payment-adoption/data/processed/world data.csv")

# Convert Indicator value from percentage strings to float
df["Indicator value"] = df["Indicator value"].str.replace('%', '').astype(float)

# Define barrier-related keywords
barrier_keywords = (
    "barrier|reason for not having an account|no account|"
    "lack of money|too expensive|too far|family member has|"
    "lack of documentation|lack of trust|religious|no need|not useful|"
    "do not trust financial institutions"
)

# Filter for barrier indicators
df_barriers = df[df["Indicator"].str.contains(barrier_keywords, case=False, regex=True)]

# Layout
layout = html.Div([
    html.H2("📊 Barriers to Financial Inclusion in Low- and Middle-Income Countries"),

    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            options=[{"label": r, "value": r} for r in sorted(df_barriers["Region"].dropna().unique())],
            id="region-dropdown",
            placeholder="Select Region"
        )
    ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),

    html.Div([
        html.Label("Select Income Group:"),
        dcc.Dropdown(
            options=[{"label": i, "value": i} for i in sorted(df_barriers["Income group"].dropna().unique())],
            id="income-dropdown",
            placeholder="Select Income Group"
        )
    ], style={'width': '30%', 'display': 'inline-block', 'marginRight': '2%'}),

    html.Div([
        html.Label("Select Country:"),
        dcc.Dropdown(
            options=[{"label": c, "value": c} for c in sorted(df_barriers["Country name"].dropna().unique())],
            id="country-dropdown",
            placeholder="Select Country"
        )
    ], style={'width': '30%', 'display': 'inline-block'}),

    html.Br(), html.Br(),

    dcc.Graph(id="barrier-graph")
])

# Callback
@dash.callback(
    Output("barrier-graph", "figure"),
    [Input("region-dropdown", "value"),
     Input("income-dropdown", "value"),
     Input("country-dropdown", "value")]
)
def update_barrier_graph(region, income_group, country):
    filtered = df_barriers.copy()

    if region:
        filtered = filtered[filtered["Region"] == region]
    if income_group:
        filtered = filtered[filtered["Income group"] == income_group]
    if country:
        filtered = filtered[filtered["Country name"] == country]

    if filtered.empty:
        return px.bar(title="No data available for selected filters.")

    summary = filtered.groupby("Indicator")["Indicator value"].mean().reset_index()
    summary = summary.sort_values(by="Indicator value", ascending=False)

    fig = px.bar(
        summary,
        x="Indicator value", y="Indicator",
        orientation="h",
        title="Most Prevalent Barriers to Financial Inclusion",
        labels={"Indicator value": "Average Prevalence (%)", "Indicator": "Barrier Type"},
        height=600
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    return fig
