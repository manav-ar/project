# your_dashboard/pages/human_impact.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

dash.register_page(__name__, path='/human_impact', name="Human Impact")

df = pd.read_csv('security_incidents.csv')
df['Total casualties'] = df['Total killed'] + df['Total wounded']

layout = html.Div([
    dbc.Row([
        dbc.Col(dcc.Graph(id='casualty-trend-line'),md=6),
        dbc.Col(dcc.Graph(id='casualty-gender-line'),md=6),
    ]),
    dbc.Row([
         dbc.Col(dcc.Graph(id='casualty-bubble-map'),md=12),
 ]),
    dbc.Checklist(
        options=[
            {'label': 'Casualties', 'value': 'casualties'},
        ],
        value=['casualties'],
        id='impact-type-checklist',
        inline=True,
        className="mt-3"
    )
])

@dash.callback(Output('casualty-trend-line', 'figure'), Input('impact-type-checklist', 'value'))
def update_casualty_trend_line(selected_impacts):
    if 'casualties' in selected_impacts:
        casualty_trend = df.groupby('Year')[['Nationals killed', 'Nationals wounded', 'Internationals killed', 'Internationals wounded']].sum().reset_index()
        fig = px.line(
            casualty_trend,
            x='Year',
            y=['Nationals killed', 'Nationals wounded', 'Internationals killed', 'Internationals wounded'],
            title='Nationality Trends Over Time',
            labels={'value': 'Count', 'variable': 'Category'}
        )
        
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        
        return fig
    else:
        return {}

@dash.callback(Output('casualty-gender-line', 'figure'), Input('impact-type-checklist', 'value'))
def update_casualty_trend_line(selected_impacts):
    if 'casualties' in selected_impacts:
        casualty_trend = df.groupby('Year')[['Gender Male', 'Gender Female']].sum().reset_index()
        fig = px.line(
            casualty_trend,
            x='Year',
            y=['Gender Male', 'Gender Female'],
            title='Gender Trends Over Time',
            labels={'value': 'Count', 'variable': 'Category'}
        )
        
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
                
        return fig
    else:
        return {}

@dash.callback(Output('casualty-bubble-map', 'figure'), Input('impact-type-checklist', 'value'))
def update_casualty_bubble_map(selected_impacts):
    if 'casualties' in selected_impacts:
        fig = px.scatter_geo(
            df,
            lat='Latitude',
            lon='Longitude',
            size='Total casualties',
            color='Total casualties',
            hover_name='City',
            hover_data=['Country', 'Year', 'Total casualties'],
            projection='natural earth',
            title='Casualties by Location'
        )
        return fig
    else:
        return {}

