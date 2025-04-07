# your_dashboard/pages/conclusions.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

dash.register_page(__name__, path='/conclusions', name="Conclusions")

# Placeholder data for recommendations. Replace with your actual data.
recommendations_data = [
    {
        'strategy': "Enhance Security Measures",
        'description': "Increase security personnel and improve protective equipment for aid workers in high-risk areas.",
        'evidence': "Data shows a correlation between high-risk regions and attacks on aid workers.",
        'resources': "Allocate additional funding for security training and equipment."
    },
    {
        'strategy': "Strengthen Community Relations",
        'description': "Engage with local communities to build trust and gather intelligence on potential threats.",
        'evidence': "Attacks often occur in areas with strained community relations.",
        'resources': "Organize community meetings and establish communication channels."
    },
    {
        'strategy': "Improve Data Sharing",
        'description': "Establish a secure platform for aid agencies to share incident data and threat assessments.",
        'evidence': "Real-time information sharing can improve response times and prevent future attacks.",
        'resources': "Develop a secure online platform and provide training on data sharing protocols."
    },
    {
        'strategy': "Advocate for Policy Changes",
        'description': "Lobby governments to enact policies that protect aid workers and promote peaceful conflict resolution.",
        'evidence': "Policy changes can create a safer operating environment for aid organizations.",
        'resources': "Engage with policymakers and organize advocacy campaigns."
    },
]

layout = html.Div([
    html.H1("Conclusions and Recommendations", className="text-center my-4"),
    html.Div([
        html.H3("Key Findings", className="text-center"),
        html.P(
            """
            Based on the analysis of the data, we have identified several key trends and patterns in security incidents affecting humanitarian efforts.
            These include the geographical distribution of attacks, the types of attacks, the human impact, the key actors involved, and the motives behind the attacks.
            The case studies highlight the devastating impact of these incidents on individuals and communities.
            """
        ),
    ], className="border p-3 mb-4"),
    html.H3("Recommendations for Aid Agencies", className="text-center"),
    dbc.Accordion(
        id="recommendations-accordion",
        children=[
            dbc.AccordionItem(
                title=rec['strategy'],
                children=[
                    html.P(rec['description']),
                    html.P(f"Evidence: {rec['evidence']}"),
                    html.P(f"Resources: {rec['resources']}"),
                ],
                item_id=str(index)
            )
            for index, rec in enumerate(recommendations_data)
        ],
        className="mb-4"
    ),
    html.H3("What You Can Do", className="text-center"),
    html.P(
        """
        Policymakers, aid workers, and the public can all contribute to improving the safety of humanitarian efforts.
        Here are some potential actions:
        """
    ),
    html.Ul([
        html.Li("Policymakers: Advocate for policies that protect aid workers and promote peaceful conflict resolution."),
        html.Li("Aid Workers: Follow security protocols, report incidents, and share information."),
        html.Li("Public: Support aid organizations and raise awareness about the challenges they face."),
    ]),
], className="p-4")