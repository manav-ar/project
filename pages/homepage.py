# your_dashboard/pages/homepage.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/', name="Homepage")

df = pd.read_csv('security_incidents.csv')
df['Total casualties'] = df['Total killed'] + df['Total wounded']

layout = html.Div([
    html.H1("Global Security Incidents Overview", className="text-center my-4"),
    dbc.Row([
        dbc.Col(dcc.Graph(id='global-heatmap'), md=8),
        dbc.Col([
            html.Div([
                html.H3("Total Incidents", className="text-center"),
                html.P(id='total-incidents', className="text-center display-4")
            ], className="border p-3 mb-3"),
            html.Div([
                html.H3("Total Casualties", className="text-center"),
                html.P(id='total-casualties', className="text-center display-4")
            ], className="border p-3 mb-3"),
            html.Div([
                html.H3("Total Kidnappings", className="text-center"),
                html.P(id='total-kidnappings', className="text-center display-4")
            ], className="border p-3")
        ], md=4),
    ]),
    dcc.Graph(id='timeline-animation'),
    dbc.Row([
        dbc.Col(dbc.Button("Explore Global Trends", href='/global_trends', color="primary", className="me-1"), md=3),
        dbc.Col(dbc.Button("Attack Types", href='/attack_types', color="secondary", className="me-1"), md=3),
        dbc.Col(dbc.Button("Human Impact", href='/human_impact', color="success", className="me-1"), md=3),
    ], className="mt-4 justify-content-center"),
], className="p-4")

@dash.callback(Output('global-heatmap', 'figure'), Input('global-heatmap', 'relayoutData'))
def update_heatmap(relayoutData):
    fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', color='Total casualties', hover_name='City', hover_data=['Country', 'Year', 'Details'], projection='orthographic')
    return fig

@dash.callback(Output('total-incidents', 'children'), Output('total-casualties', 'children'), Output('total-kidnappings', 'children'), Input('global-heatmap', 'relayoutData'))
def update_statistics(relayoutData):
    total_incidents = df['Incident ID'].nunique()
    total_casualties = df['Total casualties'].sum()
    total_kidnappings = df['Total kidnapped'].sum()
    return total_incidents, total_casualties, total_kidnappings

@dash.callback(Output('timeline-animation', 'figure'), Input('global-heatmap', 'relayoutData'))
def update_timeline(relayoutData):
    fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', color='Total casualties', hover_name='City', hover_data=['Country', 'Year', 'Details'], animation_frame='Year', projection='orthographic')
    return fig