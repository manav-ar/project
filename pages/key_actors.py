# your_dashboard/pages/key_actors.py
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import plotly.express as px

dash.register_page(__name__, path='/key_actors', name="Key Actors")

df = pd.read_csv('security_incidents.csv')
df = df.dropna(subset=['Country'])
df = df[df['Actor name']!= 'Unknown']
df = df[df['Actor name']!= 'Not applicable']

layout = html.Div([
    
    dbc.Row([
        dbc.Col(dcc.RangeSlider(id='year-slider', min=df['Year'].min(), max=df['Year'].max(), value=[df['Year'].min(), df['Year'].max()], marks={str(year): str(year) for year in df['Year'].unique()}), md=12),
        dbc.Col(dcc.Dropdown(id='country-dropdown', options=[{'label': attack, 'value': attack} for attack in df['Country'].unique()], multi=True, placeholder="Select Country"), md=12)
        ], className="mt-3"),    

    dbc.Row([
        dbc.Col(dcc.Graph(id='actor-network-graph'),md=12)]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='actor-word-cloud'), md=6),
        dbc.Col(dcc.Graph(id='actor-attack-count-bar'), md=6),
    ]),
    
])

@dash.callback(Output('actor-network-graph', 'figure'),  Input('year-slider', 'value'), Input('country-dropdown', 'value'))
def update_actor_network_graph(year_range, selected_regions):
    # Create network graph

    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_regions)]
    
    G = nx.Graph()
    for index, row in filtered_df.iterrows():
        actor = row['Actor name']
        region = row['Country']
        method = row['Means of attack']

        if pd.notna(actor):
            G.add_node(actor, type="actor")
        if pd.notna(region):
            G.add_node(region, type="region")
        if pd.notna(method):
            G.add_node(method, type="method")

        if pd.notna(actor) and pd.notna(region):
            G.add_edge(actor, region)
        if pd.notna(actor) and pd.notna(method):
            G.add_edge(actor, method)

    pos = nx.spring_layout(G, seed=42) 
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='#1f78b4',
            size=10,
            line_width=2))

    # node_adjacencies = []
    # node_text = []
    # for node, adjacencies in enumerate(G.adjacency()):
    #     node_adjacencies.append(len(adjacencies[1]))
    #     node_text.append(adjacencies[0])
    node_colors = []
    node_adjacencies = []
    node_text = []  
    for node, adjacencies in G.adjacency():
        node_type = G.nodes[node].get("type")
        if node_type == "region":
            node_colors.append("#1f78b4")  # Blue
        elif node_type == "actor":
            node_colors.append("#33a02c")  # Green
        elif node_type == "method":
            node_colors.append("#e31a1c")  # Red
        else:
            node_colors.append("#aaaaaa")  # Default gray
        
        node_adjacencies.append(len(adjacencies))
        node_text.append(node)
    
    node_trace.marker.color = node_colors
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text="",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig

@dash.callback(Output('actor-word-cloud', 'figure'), Input('year-slider', 'value'), Input('country-dropdown', 'value'))
def update_actor_word_cloud(year_range, selected_regions):
    from wordcloud import WordCloud
    import io
    import base64
    from PIL import Image

    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_regions)]
    
    
    actor_names = ' '.join(filtered_df['Actor name'].dropna().astype(str).tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(actor_names)
    img_buffer = io.BytesIO()
    wordcloud.to_image().save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

    fig = go.Figure(go.Image(source=f'data:image/png;base64,{img_str}'))
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    return fig

@dash.callback(Output('actor-attack-count-bar', 'figure'), Input('year-slider', 'value'), Input('country-dropdown', 'value'))
def update_actor_attack_count_bar(year_range, selected_regions):
    filtered_df = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Country'].isin(selected_regions)]
    
    actor_attack_counts = filtered_df['Actor name'].value_counts().reset_index()
    fig = px.bar(actor_attack_counts, x=actor_attack_counts['count'], y='Actor name', labels={'index': 'Actor name', 'Means of attack': 'Count'})
    return fig