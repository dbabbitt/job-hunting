#!/usr/bin/env python
# coding: utf-8



# Soli Deo gloria



# From Anaconda Prompt (anaconda3), type:
# conda activate "C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\jh_env"; cd C:\Users\daveb\OneDrive\Documents\GitHub\job-hunting\py; cls; python data_visualization_dash_app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=2000,  # Update every 2 seconds
        n_intervals=0
    ),
    html.Div([
        html.Div(id='temperature-card', style={'margin': '20px', 'flex': '1'}),
        html.Div(id='pressure-card', style={'margin': '20px', 'flex': '1'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
    html.Div(id='injecting-time-card', style={'margin': '20px'}),
])

@app.callback(
    [Output('temperature-card', 'children'),
     Output('pressure-card', 'children'),
     Output('injecting-time-card', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_data(n):
    response = requests.get('http://127.0.0.1:5000/data')
    data = response.json()

    # Temperature Card
    temperature_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data['temperature'][0],
        title={'text': "Temperature (°C)"},
        # gauge={'axis': {'range': [0, 90]}},
        gauge = {'shape': "bullet"},
    ))

    # Pressure Card
    pressure_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data['pressure'][0],
        title={'text': "Pressure (psi)"},
        gauge={'axis': {'range': [100, 200]}}
    ))

    # Injecting Time Card
    injecting_time_text = f"Injecting Time: {data['injecting_time'][0]} seconds"

    return dcc.Graph(figure=temperature_fig), dcc.Graph(figure=pressure_fig), injecting_time_text

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)