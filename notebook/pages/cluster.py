import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

dash.register_page(__name__, path="/clusters", name="Country Segments Map")

# ============================
# Load and clean data
# ============================
df = pd.read_csv(
    r"C:/Users/user/OneDrive/Desktop/All Files/All work project/data-financial-inclusion-and-digital-payment-adoption/data/processed/world data.csv"
)

# Remove % and convert to float
df["Indicator value"] = (
    df["Indicator value"].astype(str).str.replace("%", "", regex=False).astype(float)
)

# =============================
# Clustering logic
# =============================
def segment_countries(df, year, region=None):
    df_filtered = df[df['Year'] == year]
    if region:
        df_filtered = df_filtered[df_filtered['Region'] == region]

    df_pivot = df_filtered.pivot_table(
        index='Country name', columns='Indicator', values='Indicator value'
    )

    # Drop indicators missing in >50% of countries, then fill remaining NaNs
    df_pivot = df_pivot.dropna(thresh=int(0.5 * len(df_pivot)), axis=1)
    df_pivot = df_pivot.fillna(df_pivot.mean())

    # Standardize and reduce dimensions
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_pivot)

    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_data)

    # Assign both PCA components together to avoid fragmentation
    df_pivot = df_pivot.assign(PCA1=pca_result[:, 0], PCA2=pca_result[:, 1]).copy()
    df_pivot.reset_index(inplace=True)

    # Add income group for segmentation
    income_info = df_filtered[['Country name', 'Income group']].drop_duplicates()
    df_segmented = df_pivot.merge(income_info, on='Country name', how='left')
    df_segmented.rename(columns={'Income group': 'Segment'}, inplace=True)

    return df_segmented

# =============================
# Layout
# =============================
layout = html.Div([
    html.H2("🌍 Financial Inclusion Segmentation Map by Country"),

    html.Label("Select Year:"),
    dcc.Dropdown(
        id='year_dropdown',
        options=[{'label': y, 'value': y} for y in sorted(df['Year'].unique())],
        value=df['Year'].max()
    ),

    html.Label("Select Region (optional):"),
    dcc.Dropdown(
        id='region_dropdown',
        options=[{'label': r, 'value': r} for r in sorted(df['Region'].dropna().unique())],
        placeholder='All Regions',
        clearable=True
    ),

    dcc.Graph(id='map_graph')
])

# =============================
# Callback for Map Only
# =============================
@dash.callback(
    Output('map_graph', 'figure'),
    [Input('year_dropdown', 'value'),
     Input('region_dropdown', 'value')]
)
def update_map(year, region):
    df_segmented = segment_countries(df, year, region)

    fig = px.choropleth(
        df_segmented,
        locations='Country name',
        locationmode='country names',
        color='Segment',
        hover_name='Country name',
        title=f'Financial Inclusion Segments ({year})',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(geo=dict(showframe=False, showcoastlines=True))

    return fig
