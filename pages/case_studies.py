# your_dashboard/pages/case_studies.py
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

dash.register_page(__name__, path='/case_studies', name="Case Studies")

df = pd.read_csv('security_incidents.csv')
dfx = pd.read_csv('aid_worker_survivor_stories.csv')
df['Stories'] = dfx['story']

# Preprocess data to create case study summaries
case_studies = []
for index, row in df.iterrows():
    case_studies.append({
        'id': row['Incident ID'],
        'title': f"{row['Means of attack']} in {row['City']}, {row['Country']} ({row['Year']})",
        'summary': row['Details'],
        'location': f"{row['City']}, {row['Country']}",
        'year': row['Year'],
        'attack_type': row['Means of attack'],
        'latitude': row['Latitude'],
        'longitude': row['Longitude'],
        'story': row['Stories']
    })

layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Dropdown(
                    id='case-study-dropdown',
                    options=[{'label': study['title'], 'value': study['id']} for study in case_studies],
                    placeholder="Select a Case Study"
                ),
                html.Div(id='case-study-details', className="mt-3"),
            ], className="border p-3"),
            md=6
        ),
        dbc.Col(
            dcc.Graph(id='case-study-map'),
            md=6
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(id='case-study-stories', className="mt-3 scroll-container"),
            md=12
        )
    ]),
], className="p-4")

@dash.callback(
    Output('case-study-details', 'children'),
    Input('case-study-dropdown', 'value')
)
def update_case_study_details(selected_id):
    if selected_id:
        study = next(study for study in case_studies if study['id'] == selected_id)
        return html.Div([
            html.H3(study['title']),
            html.P(f"Location: {study['location']}"),
            html.P(f"Year: {study['year']}"),
            html.P(f"Attack Type: {study['attack_type']}"),
            html.P(study['summary']),
        ])
    else:
        return html.P("Select a case study to view details.")

@dash.callback(
    Output('case-study-map', 'figure'),
    Input('case-study-dropdown', 'value')
)
def update_case_study_map(selected_id):
    if selected_id:
        study = next(study for study in case_studies if study['id'] == selected_id)
        fig = px.scatter_geo(
            lat=[study['latitude']],
            lon=[study['longitude']],
            hover_name=[study['title']],
            hover_data={'Location': [study['location']], 'Year': [study['year']], 'Attack Type':[study['attack_type']], 'Summary': [study['summary']]},
            projection='natural earth',
            title=f"Location of {study['title']}"
        )
        return fig
    else:
        return px.scatter_geo(projection='natural earth', title="Select a case study to see its location.")

@dash.callback(
    Output('case-study-stories', 'children'),
    Input('case-study-dropdown', 'value')
)
def update_case_study_stories(selected_id):
    if selected_id:
        study = next(study for study in case_studies if study['id'] == selected_id)
        return html.Div([
            html.H3("Survivor Story"),
            html.P(f"{study['story']}"),
        ])
        # Replace with your actual survivor stories data or logic.
        # This is a placeholder for demonstration purposes.
        # story = f"Survivor story for incident {selected_id} is not yet available."
        # return html.Div([
        #     html.H3("Survivor Story"),
        #     html.P(story),
        #])
    else:
        return html.P("Select a case study to view survivor stories.")