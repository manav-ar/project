# your_dashboard/app.py
import dash
import dash_bootstrap_components as dbc
from dash import page_registry, page_container, html

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    # dbc.NavbarSimple(
    #     children=[
    #         dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
    #         for page in page_registry.values()
    #         if page["module"] != "pages.not_found"
    #     ],
    #     brand="Global Security Incidents Dashboard",
    #     color="primary",
    #     dark=True,
    # ),
    page_container,
])

server = app.server

if __name__ == "__main__":
    app.run(debug=True)