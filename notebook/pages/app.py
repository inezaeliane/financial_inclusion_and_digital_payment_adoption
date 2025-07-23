import dash
from dash import Dash
import dash_bootstrap_components as dbc
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt


app = Dash(__name__,
           use_pages=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Financial Inclusion Dashboard",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink(" Home", href="/")),
            dbc.NavItem(dbc.NavLink(" Trends", href="/trends")),
            dbc.NavItem(dbc.NavLink(" Demographics", href="/demographics")),
            dbc.NavItem(dbc.NavLink("Digital Payments", href="/digital")),
            dbc.NavItem(dbc.NavLink("Barriers", href="/barriers")),
            dbc.NavItem(dbc.NavLink("Grouping", href="/clusters")),
        ]
    ),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
