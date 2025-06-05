import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    # TASK 1: Dropdown for launch site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            *[
                {'label': site, 'value': site}
                for site in spacex_df['Launch Site'].unique()
            ]
        ],
        value='ALL',
        placeholder="Select a Launch Site",
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart for success counts
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Payload slider
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(i): str(int(i)) for i in range(int(min_payload), int(max_payload)+1, 2000)},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter plot for payload vs success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        filtered_df = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(filtered_df, names='Launch Site', title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        counts = filtered_df['class'].value_counts().rename({0: 'Failure', 1: 'Success'})
        fig = px.pie(values=counts.values, names=counts.index, title=f'Success vs Failure for site {selected_site}')
    return fig

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('payload-slider', 'value')]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(filtered_df,
                     x='Payload Mass (kg)',
                     y='class',
                     color='Booster Version',
                     title='Payload vs. Launch Success',
                     labels={'class': 'Launch Success (1=Success, 0=Failure)'})
    return fig

if __name__ == '__main__':
    app.run(debug=True)
