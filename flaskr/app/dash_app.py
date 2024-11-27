import dash
from dash import dcc, html
from dash.dependencies import Output, Input
from .consumer import messages

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Message Monitor"),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0),
    html.Div(id='live-update-text')
])

@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    return [html.Div(children=msg) for msg in messages]

def run_dash():
    app.run_server(debug=False, port=8050)