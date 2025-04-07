# your_dashboard/pages/attack_types.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/attack_types', name="Attack Types")

df = pd.read_csv('security_incidents.csv')
df = df.dropna(subset=['Country'])

layout = html.Div([
    
    
    dbc.Row([
        dbc.Col(dcc.RangeSlider(id='year-slider', min=df['Year'].min(), max=df['Year'].max(), value=[df['Year'].min(), df['Year'].max()], marks={str(year): str(year) for year in df['Year'].unique()}), md=12),
        dbc.Col(dcc.Dropdown(id='country-dropdown', options=[{'label': attack, 'value': attack} for attack in df['Country'].unique()], multi=True, placeholder="Select Country"), md=12)
        ], className="mt-3"),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='attack-type-bar'), md=6),
        dbc.Col( dcc.Graph(id='attack-type-treemap'), md=6),
    ]),
    
])

@dash.callback(Output('attack-type-bar', 'figure'), Input('year-slider', 'value'), Input('country-dropdown', 'value'))
def update_attack_type_bar(year_range, selected_regions):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_regions)]
        attack_counts = filtered_df[['Country','Means of attack']].value_counts().reset_index()
        fig = px.bar(attack_counts, x=attack_counts['count'], y='Means of attack', color = 'Country', labels={'index': 'Attack Type', 'Means of attack': 'Count'})
    else:
        attack_counts = filtered_df['Means of attack'].value_counts().reset_index()
        fig = px.bar(attack_counts, x=attack_counts['count'], y='Means of attack', labels={'index': 'Attack Type', 'Means of attack': 'Count'})
    return fig

@dash.callback(Output('attack-type-treemap', 'figure'), Input('year-slider', 'value'), Input('country-dropdown', 'value'))
def update_attack_type_treemap(year_range, selected_regions):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_regions)]
        attack_year = filtered_df.groupby(['Year', 'Means of attack', 'Country']).size().reset_index(name='count')
        fig = px.treemap(attack_year, path=['Year', 'Means of attack','Country'], values='count')
    
    else:   
        attack_year = filtered_df.groupby(['Year', 'Means of attack']).size().reset_index(name='count')
        fig = px.treemap(attack_year, path=['Year', 'Means of attack'], values='count')
    return fig