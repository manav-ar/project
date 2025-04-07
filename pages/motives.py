# your_dashboard/pages/motives.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/motives', name="Motives")

df = pd.read_csv('security_incidents.csv')
df = df.dropna(subset=['Motive'])

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.RangeSlider(id='year-slider', min=df['Year'].min(), max=df['Year'].max(), value=[df['Year'].min(), df['Year'].max()], marks={str(year): str(year) for year in df['Year'].unique()}), md=8),
        dbc.Col(dcc.Dropdown(id='motive-dropdown', options=[{'label': motive, 'value': motive} for motive in df['Motive'].unique()], multi=True, placeholder="Select Motive"), md=4),
        ], className="mt-3"),
    
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='motive-bar'), md=3),
        dbc.Col(dcc.Graph(id='motive-timeline'), md=4),
        dbc.Col(dcc.Graph(id='attack-location-map'), md=5),
        ]),

    
])

@dash.callback(Output('motive-bar', 'figure'), Input('year-slider', 'value'),  Input('motive-dropdown', 'value'))
def update_motive_bar(year_range, selected_motive):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_motive:
        filtered_df = filtered_df[filtered_df['Motive'].isin(selected_motive)]
    motive_counts = filtered_df['Motive'].value_counts(normalize=True).mul(100).round(1).reset_index()
    fig = px.bar(motive_counts, y=motive_counts.proportion, x='Motive', color = motive_counts['Motive'], labels={'index': 'Percentage(%)', 'Motive': 'Motive'}).update_layout(showlegend=False)
    fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    
    return fig

@dash.callback(Output('attack-location-map', 'figure'), Input('year-slider', 'value'), Input('motive-dropdown', 'value'))
def update_attack_location_map(year_range, selected_motive):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_motive:
        filtered_df = filtered_df[filtered_df['Motive'].isin(selected_motive)]
    fig = px.scatter_geo(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        color='Motive',
        hover_name='City',
        hover_data=['Country', 'Year', 'Motive'],
        projection='natural earth'
    )
    
    fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    
    return fig

@dash.callback(Output('motive-timeline', 'figure'), Input('year-slider', 'value'), Input('motive-dropdown', 'value'))
def update_motive_timeline(year_range, selected_motive):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_motive:
        filtered_df = filtered_df[filtered_df['Motive'].isin(selected_motive)]
    motive_year = filtered_df.groupby(['Year', 'Motive']).size().reset_index(name='count')
    fig = px.line(motive_year, x='Year', y='count', color='Motive')
    
    fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
    
    return fig