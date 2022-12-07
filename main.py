from dash import Dash, dcc, html, Input, Output
from universal_approach import universal_approach_3_years

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div(
        [
            dcc.Graph(id='graph-with-slider')
        ],
        style={'width':"100%", 'height':"700px", 'display':'inline-block'}
    ),
    html.Div(
        [
            dcc.Slider(0, 1, marks={0:{'label':'0'}, 0.5:{'label':'0.5'}, 1:{'label':'1'}}, value=0.5, id='2018-ratio'),
            html.Div(
                id='updatemode-output-container_2018',
            ),
        ],
        style={'width':"30%", 'height':"50px", 'display':'inline-block'}
    ),
    html.Div(
        [
            dcc.Slider(0, 1, marks={0:{'label':'0'}, 0.5:{'label':'0.5'}, 1:{'label':'1'}}, value=0.5, id='2019-ratio'),
            html.Div(
                id='updatemode-output-container_2019',
            ),
        ],
        style={'width':"30%", 'height':"50px", 'display':'inline-block'}
    ),
    html.Div(
        [
            dcc.Slider(0, 1, marks={0:{'label':'0'}, 0.5:{'label':'0.5'}, 1:{'label':'1'}}, value=0.5, id='2020-ratio'),
            html.Div(
                id='updatemode-output-container_2020',
            ),
        ],
        style={'width':"30%", 'height':"50px", 'display':'inline-block'}
    ),
])

@app.callback(
    Output('updatemode-output-container_2018', 'children'),
    Input('2018-ratio', 'value')
)
def display_value(value):
    return f"financial activity ratio in 2018: {value}"

@app.callback(
    Output('updatemode-output-container_2019', 'children'),
    Input('2019-ratio', 'value')
)
def display_value(value):
    return f"financial activity ratio in 2019: {value}"

@app.callback(
    Output('updatemode-output-container_2020', 'children'),
    Input('2020-ratio', 'value')
)
def display_value(value):
    return f"financial activity ratio in 2020: {value}"

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('2018-ratio', 'value'),
    Input('2019-ratio', 'value'),
    Input('2020-ratio', 'value')
)
def update_output(value1, value2, value3):
    initial_cash_allocation={
        '2018': {
            'farming activity': 1-value1,
            'financial activity':value1
        },
        '2019': {
            'farming activity': 1-value2,
            'financial activity':value2
        },
        '2020': {
            'farming activity': 1-value3,
            'financial activity':value3
        },
    }

    fig = universal_approach_3_years(initial_cash_allocation=initial_cash_allocation)
    # fig.layout.title = f"{value1}_{value2}"
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)