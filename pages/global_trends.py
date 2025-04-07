# your_dashboard/pages/global_trends.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/global_trends', name="Global Trends")

df = pd.read_csv('security_incidents.csv')
df['Total casualties'] = df['Total killed'] + df['Total wounded']

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.RangeSlider(id='year-slider', min=df['Year'].min(), max=df['Year'].max(), value=[df['Year'].min()+5, df['Year'].max()], marks={str(year): str(year) for year in df['Year'].unique()}), md=6),
        dbc.Col(dcc.Dropdown(id='attack-type-dropdown', options=[{'label': attack, 'value': attack} for attack in df['Means of attack'].unique()], value=['Body-borne IED', 'Roadside IED', 'Vehicle-born IED'], multi=True, placeholder="Select Attack Types"), md=6)
    ], className="mt-3"),
    dbc.Row([
        dbc.Col([dcc.Graph(id='global-trends-map')]),
        dbc.Col([dcc.Graph(id='country-attack-trends')])]),
    
], className="p-4")

@dash.callback(Output('global-trends-map', 'figure'), Input('year-slider', 'value'), Input('attack-type-dropdown', 'value'))
def update_trends_map(year_range, selected_attacks):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_attacks:
        filtered_df = filtered_df[filtered_df['Means of attack'].isin(selected_attacks)]
    fig = px.choropleth(filtered_df.groupby('Country')['Total casualties'].sum().reset_index(), locations='Country', locationmode='country names', color='Total casualties', hover_name='Country')
    return fig

@dash.callback(Output('country-attack-trends', 'figure'), Input('global-trends-map', 'clickData'), Input('year-slider', 'value'), Input('attack-type-dropdown', 'value'))
def update_country_trends(clickData, year_range, selected_attacks):
    if clickData:
        country = clickData['points'][0]['location']
        filtered_df = df[(df['Country'] == country) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        if selected_attacks:
            filtered_df = filtered_df[filtered_df['Means of attack'].isin(selected_attacks)]
        country_trend = filtered_df.groupby('Year')['Total casualties'].sum().reset_index()
        fig = px.line(country_trend, x='Year', y='Total casualties', title=f"Casualties in {country} by selected Means over Time")
        return fig
    else:
        country = 'Afghanistan'
        filtered_df = df[(df['Country'] == country) & (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
        if selected_attacks:
            filtered_df = filtered_df[filtered_df['Means of attack'].isin(selected_attacks)]
        country_trend = filtered_df.groupby('Year')['Total casualties'].sum().reset_index()
        fig = px.line(country_trend, x='Year', y='Total casualties', title=f"Casualties in {country} by selected Means over Time")
        return fig