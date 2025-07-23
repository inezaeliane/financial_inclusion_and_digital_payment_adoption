import dash
from dash import Dash
import dash_bootstrap_components as dbc, html

app = Dash(__name__,
           use_pages=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Navbar(
        dbc.Container([
            dbc.NavbarBrand("Financial Inclusion Dashboard", href="/", className="ms-2"),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Trends", href="/")),
                    dbc.NavItem(dbc.NavLink("Demographics", href="/demographics")),
                    dbc.NavItem(dbc.NavLink("Digital Payments", href="/digital")),
                    dbc.NavItem(dbc.NavLink("Barriers", href="/barriers")),
                    dbc.NavItem(dbc.NavLink("Grouping", href="/clusters")),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ]),
        color="primary",
        dark=True,
        className="mb-4"
    ),
    dash.page_container
], fluid=True)

# Toggle collapse on small screens
@app.callback(
    dash.Output("navbar-collapse", "is_open"),
    [dash.Input("navbar-toggler", "n_clicks")],
    [dash.State("navbar-collapse", "is_open")],
)
def toggle_navbar(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run(debug=True)
