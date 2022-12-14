import dash
from dash import Dash, dcc, html, Input, Output, ctx
from universal_approach import universal_approach_3_years
from universal_approach_mpt import universal_approach_3_years_mpt
from universal_approach_mpt_short import universal_approach_3_years_mpt_short
from datetime import datetime
from constant import INITIAL_CASH_ALLOCATION

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# run benchmark dict only (farmer does not invest in koi)
y_rn_raw_num_list = [
(2018, 2018), 
(2019, 2019), 
(2020, 2020), 
(2018, 2019), 
(2019, 2020), 
(2018, 2020), 
]
benchmark_farmer_list = list(map(lambda x: universal_approach_3_years(start_year=x[0], end_year=x[1], initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True), y_rn_raw_num_list))
y_rn_num_list = list(map(lambda x:f"{x[0]} {x[1]}", y_rn_raw_num_list))
benchmark_farmer_dict = dict(zip(y_rn_num_list, benchmark_farmer_list))
# benchmark_farmer_dict = {
#     '2018 2018': universal_approach_3_years(start_year=2018, end_year=2018, initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True),
#     '2019 2019': universal_approach_3_years(start_year=2019, end_year=2019, initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True),
#     '2020 2020': universal_approach_3_years(start_year=2020, end_year=2020, initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True),
#     '2018 2019': universal_approach_3_years(start_year=2018, end_year=2019, initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True),
#     '2019 2020': universal_approach_3_years(start_year=2019, end_year=2020, initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True),
#     '2018 2020': universal_approach_3_years(start_year=2018, end_year=2020, initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True),
# }
# benchmark_farmer = universal_approach_3_years(initial_cash_allocation=INITIAL_CASH_ALLOCATION, return_farmer_only=True)

# run mpt output
# mpt_fig_result = universal_approach_3_years_mpt(benchmark_farmer=benchmark_farmer)
print()


app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    html.Div(
        [
            dcc.Graph(id='graph-with-slider')
        ],
        # style={'width':"100%", 'height':"700px", 'display':'inline-block'}
        style={'width':"100%", 'height':"600px", 'display':'inline-block'}
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
    html.Div(
        [
            html.Button('MPT weight', id='mpt_weight', n_clicks=0),
            html.Button('MPT weight (with short)', id='mpt_weight_short', n_clicks=0),
            html.Div(
                [
                    'MPT optimization method: ',
                ],
                style={'width':"200px", 'display':'inline-block'}
            ),
            html.Div(
                [
                    # dcc.Dropdown(
                    #     ['max_sharpe', 'min_volatility', 'max_quadratic_utility'], 
                    #     'min_volatility', 
                    #     id='mpt_method')
                    'min_volatility'
                ],
                style={'width':"25%", 'display':'inline-block'}
            ),
        ]
    ),
    html.Div(id='year_range'),
    html.Div(
        dcc.RangeSlider(
            min=2018, 
            max=2020, 
            step=1, 
            value=[2018, 2020], marks={
                2018: '2018',
                2019: '2019',
                2020: '2020',
                },
            id='my-year-range-slider')
    )
])



# @app.callback(
#     Output('updatemode-output-container_2018', 'value'),
#     Output('updatemode-output-container_2019', 'value'),
#     Output('updatemode-output-container_2020', 'value'),
#     Input('mpt_weight', 'n_clicks')
# )
# def displayClick(n_clicks):
#     # if "mpt_weight" == ctx.triggered_id:
#     #     print('mpt button is clicked')
#     #     fig = mpt_fig_result
#     #     return fig
#     if n_clicks is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         print('yesy')
#         return update_output(0.1, 0.2, 0.3)

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
    Output('year_range', 'children'),
    Input('my-year-range-slider', 'value')
)
def display_value(value):
    return f"backtest range selection: [{value[0]}, {value[1]}]"

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('2018-ratio', 'value'),
    Input('2019-ratio', 'value'),
    Input('2020-ratio', 'value'),
    Input('mpt_weight', 'n_clicks'),
    Input('mpt_weight_short', 'n_clicks'),
    Input('my-year-range-slider', 'value'),
    # Input('mpt_method', 'value'),
)
def update_output(value1, value2, value3, n_clicks_1, n_clicks_2, rn, mpt_method='min_volatility'):
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
    y_rn_start, y_rn_end = rn
    benchmark_farmer = benchmark_farmer_dict[f"{y_rn_start} {y_rn_end}"]
    if "mpt_weight" == ctx.triggered_id:
        mpt_config = {
            'method':mpt_method
        }
        # fig = universal_approach_3_years(initial_cash_allocation=initial_cash_allocation)
        print('======run mpt result======')
        print(f"mpt method: {mpt_method}")
        # fig = mpt_fig_result
        fig =  universal_approach_3_years_mpt(
            start_year=y_rn_start,
            end_year=y_rn_end,
            benchmark_farmer=benchmark_farmer,
            mpt_config=mpt_config)
        print('done')
        print(f"Finish mpt result at {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
        print()
        print()
        print()
        return fig
    elif "mpt_weight_short" == ctx.triggered_id:
        mpt_config = {
            'method':mpt_method
        }
        # fig = universal_approach_3_years(initial_cash_allocation=initial_cash_allocation)
        print('======run mpt (with short) result======')
        print(f"mpt method: {mpt_method}")
        # fig = mpt_fig_result
        fig =  universal_approach_3_years_mpt_short(
            start_year=y_rn_start,
            end_year=y_rn_end,
            benchmark_farmer=benchmark_farmer,
            mpt_config=mpt_config)
        print('done')
        print(f"Finish mpt (with short) result at {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
        print()
        print()
        print()
        return fig
    else:
        # fig = mpt_fig_result
        fig = universal_approach_3_years(
            start_year=y_rn_start,
            end_year=y_rn_end,
            initial_cash_allocation=initial_cash_allocation,
            benchmark_farmer=benchmark_farmer)
        # raise dash.exceptions.PreventUpdate
        
    # fig.layout.title = f"{value1}_{value2}"
    print(f"Finish result ({value1}, {value2}, {value3}) at {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
    print(f"year range : {y_rn_start} {y_rn_end}")
    print()
    print()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8051, host='0.0.0.0')