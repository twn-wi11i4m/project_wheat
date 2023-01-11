import dash
from dash import Dash, dcc, html, Input, Output, ctx, dash_table
import pandas as pd
# import dash_bootstrap_components as dbc
# from universal_approach import universal_approach_3_years
# from universal_approach_mpt import universal_approach_3_years_mpt
# from universal_approach_mpt_short import universal_approach_3_years_mpt_short
from backtest import backtest
from insurance import AgriInsurance
from farmer import Farm

from datetime import datetime
from constant import INITIAL_CASH_ALLOCATION, FARMING_ONLY_CASH_ALLOCATION, HTML_COST_SESSION_BUTTON_STYLE, HTML_FARM_FARMER_SESSION_BUTTON_STYLE

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Farmer Wealth Portfolio Dash Board"


# default value (variable and fixed) for cost session
VARIABLE_COST_SEED = None
VARIABLE_COST_SEED_TREATMENT = None
VARIABLE_COST_FERTILIZER = None
VARIABLE_COST_PESTICIDE = None
VARIABLE_COST_FUEL = None
VARIABLE_COST_MACHINERY_OPERATION = None
VARIABLE_COST_LABOUR_HIRED = None
VARIABLE_COST_UTILITIES_AND_MISC = None
# VARIABLE_COST_INSURANCE_PREMIUM = None
VARIABLE_COST_INTEREST_ON_OPERATION = None

FIXED_COST_BUILDING_REPAIR = None
FIXED_COST_PROPERTY_TAXES = None
FIXED_COST_BUSINESS_OVERHEAD = None
FIXED_COST_MACHINERY_DEPRECIATION = None
FIXED_COST_BUILDING_DEPRECIATION = None 
FIXED_COST_MACHINERY_INVESTMENT = None
FIXED_COST_BUILDING_INVESTMENT = None
FIXED_COST_LAND_INVESTMENT = None

DEFAULT_COST = (
    VARIABLE_COST_SEED,
    VARIABLE_COST_SEED_TREATMENT,
    VARIABLE_COST_FERTILIZER,
    VARIABLE_COST_PESTICIDE,
    VARIABLE_COST_FUEL,
    VARIABLE_COST_MACHINERY_OPERATION,
    VARIABLE_COST_LABOUR_HIRED,
    VARIABLE_COST_UTILITIES_AND_MISC,
    # VARIABLE_COST_INSURANCE_PREMIUM,
    VARIABLE_COST_INTEREST_ON_OPERATION,
    FIXED_COST_BUILDING_REPAIR,
    FIXED_COST_PROPERTY_TAXES,
    FIXED_COST_BUSINESS_OVERHEAD,
    FIXED_COST_MACHINERY_DEPRECIATION,
    FIXED_COST_BUILDING_DEPRECIATION,
    FIXED_COST_MACHINERY_INVESTMENT,
    FIXED_COST_BUILDING_INVESTMENT,
    FIXED_COST_LAND_INVESTMENT
)

# wheat variable cost
WHEAT_VARIABLE_COST_SEED = 26.92
WHEAT_VARIABLE_COST_SEED_TREATMENT = 0.74
WHEAT_VARIABLE_COST_FERTILIZER = 158.05
WHEAT_VARIABLE_COST_PESTICIDE = 101.19
WHEAT_VARIABLE_COST_FUEL = 15.31
WHEAT_VARIABLE_COST_MACHINERY_OPERATION = 9.98
WHEAT_VARIABLE_COST_LABOUR_HIRED = 22.05
WHEAT_VARIABLE_COST_UTILITIES_AND_MISC = 4.23
# WHEAT_VARIABLE_COST_INSURANCE_PREMIUM = None
WHEAT_VARIABLE_COST_INTEREST_ON_OPERATION = 7.13

WHEAT_FIXED_COST_BUILDING_REPAIR = 0.69
WHEAT_FIXED_COST_PROPERTY_TAXES = 5.55
WHEAT_FIXED_COST_BUSINESS_OVERHEAD = 3.19
WHEAT_FIXED_COST_MACHINERY_DEPRECIATION = 41.06
WHEAT_FIXED_COST_BUILDING_DEPRECIATION = 1.45
WHEAT_FIXED_COST_MACHINERY_INVESTMENT = 15.83
WHEAT_FIXED_COST_BUILDING_INVESTMENT = 0.48
WHEAT_FIXED_COST_LAND_INVESTMENT = 39.28

WHEAT_DEFAULT_COST = (
    WHEAT_VARIABLE_COST_SEED, 
    WHEAT_VARIABLE_COST_SEED_TREATMENT, 
    WHEAT_VARIABLE_COST_FERTILIZER, 
    WHEAT_VARIABLE_COST_PESTICIDE, 
    WHEAT_VARIABLE_COST_FUEL, 
    WHEAT_VARIABLE_COST_MACHINERY_OPERATION, 
    WHEAT_VARIABLE_COST_LABOUR_HIRED, 
    WHEAT_VARIABLE_COST_UTILITIES_AND_MISC, 
    # WHEAT_VARIABLE_COST_INSURANCE_PREMIUM, 
    WHEAT_VARIABLE_COST_INTEREST_ON_OPERATION,
    WHEAT_FIXED_COST_BUILDING_REPAIR,
    WHEAT_FIXED_COST_PROPERTY_TAXES,
    WHEAT_FIXED_COST_BUSINESS_OVERHEAD,
    WHEAT_FIXED_COST_MACHINERY_DEPRECIATION,
    WHEAT_FIXED_COST_BUILDING_DEPRECIATION,
    WHEAT_FIXED_COST_MACHINERY_INVESTMENT,
    WHEAT_FIXED_COST_BUILDING_INVESTMENT,
    WHEAT_FIXED_COST_LAND_INVESTMENT
)


# canola variable cost
CANOLA_VARIABLE_COST_SEED = 75.73
CANOLA_VARIABLE_COST_SEED_TREATMENT = 9
CANOLA_VARIABLE_COST_FERTILIZER = 187.62
CANOLA_VARIABLE_COST_PESTICIDE = 74.88
CANOLA_VARIABLE_COST_FUEL = 16.21
CANOLA_VARIABLE_COST_MACHINERY_OPERATION = 9.98
CANOLA_VARIABLE_COST_LABOUR_HIRED = 21.05
CANOLA_VARIABLE_COST_UTILITIES_AND_MISC = 4.23
# CANOLA_VARIABLE_COST_INSURANCE_PREMIUM = None
CANOLA_VARIABLE_COST_INTEREST_ON_OPERATION = 8.46

CANOLA_FIXED_COST_BUILDING_REPAIR = 0.69
CANOLA_FIXED_COST_PROPERTY_TAXES = 5.55
CANOLA_FIXED_COST_BUSINESS_OVERHEAD = 3.19
CANOLA_FIXED_COST_MACHINERY_DEPRECIATION = 41.06
CANOLA_FIXED_COST_BUILDING_DEPRECIATION = 1.45 
CANOLA_FIXED_COST_MACHINERY_INVESTMENT = 15.83
CANOLA_FIXED_COST_BUILDING_INVESTMENT = 0.48
CANOLA_FIXED_COST_LAND_INVESTMENT = 39.28

CANOLA_DEFAULT_COST = (
    CANOLA_VARIABLE_COST_SEED,
    CANOLA_VARIABLE_COST_SEED_TREATMENT,
    CANOLA_VARIABLE_COST_FERTILIZER,
    CANOLA_VARIABLE_COST_PESTICIDE,
    CANOLA_VARIABLE_COST_FUEL,
    CANOLA_VARIABLE_COST_MACHINERY_OPERATION,
    CANOLA_VARIABLE_COST_LABOUR_HIRED,
    CANOLA_VARIABLE_COST_UTILITIES_AND_MISC,
    # CANOLA_VARIABLE_COST_INSURANCE_PREMIUM,
    CANOLA_VARIABLE_COST_INTEREST_ON_OPERATION,
    CANOLA_FIXED_COST_BUILDING_REPAIR,
    CANOLA_FIXED_COST_PROPERTY_TAXES,
    CANOLA_FIXED_COST_BUSINESS_OVERHEAD,
    CANOLA_FIXED_COST_MACHINERY_DEPRECIATION,
    CANOLA_FIXED_COST_BUILDING_DEPRECIATION,
    CANOLA_FIXED_COST_MACHINERY_INVESTMENT,
    CANOLA_FIXED_COST_BUILDING_INVESTMENT,
    CANOLA_FIXED_COST_LAND_INVESTMENT
)

WEIGHT_TABLE_DEFAULT_WEIGHT = [
    {'year':2018, 'weight_1':0.33, 'weight_2':0.33, 'weight_3':0.33},
    {'year':2019, 'weight_1':0.33, 'weight_2':0.33, 'weight_3':0.33},
    {'year':2020, 'weight_1':0.33, 'weight_2':0.33, 'weight_3':0.33},
]

RESULT_PERFORMANCE_TABLE_DEFAULT_DATA = [
    {'year':2018, 'wealth_change_dollar':0, 'wealth_change_pct': 0},
    {'year':2019, 'wealth_change_dollar':0, 'wealth_change_pct': 0},
    {'year':2020, 'wealth_change_dollar':0, 'wealth_change_pct': 0},
]


FARM_FARMER_DEFAULT_INITIAL_CASH = 100_000
FARM_FARMER_DEFAULT_TOWNSHIP = 7
FARM_FARMER_DEFAULT_RANGE = 21
FARM_FARMER_DEFAULT_MERIDIAN = 4
FARM_FARMER_DEFAULT_AREA = 1

FARM_FARMER_DEFAULT_SETTING = (
    FARM_FARMER_DEFAULT_INITIAL_CASH,
    FARM_FARMER_DEFAULT_TOWNSHIP,
    FARM_FARMER_DEFAULT_RANGE,
    FARM_FARMER_DEFAULT_MERIDIAN,
    FARM_FARMER_DEFAULT_AREA
)


app.layout = html.Div([
    html.Div(
        [dcc.Graph(id='result-graph')],
        style={'width':"100%", 'height':"600px", 'display':'inline-block'}
    ),
    html.Hr(
        style={"color": "#FEC700"}
        ),
    html.Div(
        className='row',
        children=[
            html.Div(
                className='six columns',
                children=[
                    html.H4(id='Backtest_Year_Range', style={"font-weight": "bold", 'display':'inline-block'}),
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
                            id='Backtest_Year_Range_Slider'
                        )
                    ),
                    html.H4('Weight', style={"font-weight": "bold", 'display':'inline-block'}),
                    html.Div([
                        dash_table.DataTable(
                            id='weight_table',
                            columns=(
                                [
                                    {'id': 'year', 'name': 'Year', 'editable': False}, 
                                    {'id': 'weight_1', 'name': 'Financial', 'editable': True},
                                    {'id': 'weight_2', 'name': 'Physical', 'editable': True},
                                    {'id': 'weight_3', 'name': 'Insurance', 'editable': True}
                                ]
                            ),
                            fixed_columns={'headers': True,'data': 1},
                            data=WEIGHT_TABLE_DEFAULT_WEIGHT,
                        ),
                    ]),
                    html.Div([
                        html.Button('MPT Weight', id='MPT_Weight', n_clicks=0),
                        html.Button('Clear Weight', id='Default_Weight', n_clicks=0),
                    ]),
                    html.H4('Financial Product', style={"font-weight": "bold", 'display':'inline-block'}),
                    html.Div([
                        html.Div('Selection:', style={'width':"15%", 'display':'inline-block'}),
                        html.Div(
                            dcc.Dropdown(
                                ['naive', 'KOI_product_v1'], 
                                value='naive', 
                                id='financial_product_selection'
                            ),
                            style={'width':"20%", 'display':'inline-block'}),
                    ]),
                    # html.Div([
                    #     html.Button('Backtest!', id='start_backtest', n_clicks=0, style={'color':'red'}),
                    # ])



                ]
            ),
            html.Div(
                className='six columns',
                children=[
                    html.H4('Result Performance', style={"font-weight": "bold", 'display':'inline-block'}),
                    dash_table.DataTable(
                            id='result_performance_table',
                            columns=(
                                [
                                    {'id': 'year', 'name': 'Year'}, 
                                    {'id': 'wealth_change_dollar', 'name': 'wealth chg ($)'},
                                    {'id': 'wealth_change_pct', 'name': 'wealth chg (%)'},
                                ]
                            ),
                            fixed_columns={'headers': True,'data': 1},
                            data=RESULT_PERFORMANCE_TABLE_DEFAULT_DATA,
                        ),
                ]
            )
        ]
    ),
    html.Hr(
        style={"color": "#FEC700"}
        ),
    
    html.Div([
        html.H4('Farm & Farmer Section', style={"font-weight": "bold", 'display':'inline-block'}),
        html.Button('Default farm & farmer Setting', id='Default_farm_farmer_Setting', n_clicks=0, style=HTML_FARM_FARMER_SESSION_BUTTON_STYLE),
    ]),
    html.Div([
        html.Div([
            'Initial Cash ($): ',
            dcc.Input(id="Farm_Farmer_Initial_Cash", value=100_000, type="number", placeholder="$", style={'marginRight':'10px'}),
            'Farm Township: ',
            dcc.Input(id="Farm_Farmer_Township", value=1, type="number", placeholder="", style={'marginRight':'10px', 'width': '80px'}),
            'Farm Range: ',
            dcc.Input(id="Farm_Farmer_Range", value=1, type="number", placeholder="", style={'marginRight':'10px', 'width': '80px'}),
            'Farm Meridian: ',
            dcc.Input(id="Farm_Farmer_Meridian", value=5, type="number", placeholder="", style={'marginRight':'10px', 'width': '80px'}),
            'Farm Area (Acre): ',
            dcc.Input(id="Farm_Farmer_Area", value=1, type="number", placeholder="Acre", style={'marginRight':'10px', 'width': '80px'}),
        ]),
    ]),

    html.Hr(
        style={"color": "#FEC700"}
        ),
    html.H4('Insurance Product Section', style={"font-weight": "bold", 'display':'inline-block'}),
    html.Div([
        html.Div('Crop:', style={'width':"6%", 'display':'inline-block'}),
        html.Div(
            dcc.Dropdown(
                ['canolapolish', 'canolaargentine', 'CPS', 'HRS'], 
                value='HRS', 
                id='Insurance_Product_Crop'
            ),
            style={'width':"15%",'display':'inline-block'}),
        html.Div('Field:', style={'width':"6%", 'display':'inline-block'}),
        html.Div(
            dcc.Dropdown(
                ['stubble', 'fallow', 'irrigated'], 
                value='stubble', 
                id='Insurance_Product_Field'
            ),
            style={'width':"15%", 'display':'inline-block'}),
        html.Div('Coverage:', style={'width':"6%", 'display':'inline-block'}),
        html.Div(
            dcc.Dropdown(
                [50, 60, 70, 80], 
                value=50, 
                id='Insurance_Product_Coverage'
            ),
            style={'width':"10%", 'display':'inline-block'}),
        html.Div('Hail endorsement:', style={'width':"14%", 'display':'inline-block'}),
        html.Div(
            dcc.Checklist(
                [''], 
                value=[], 
                id='Insurance_Product_Include_Hail_Endorsement'
            ),
            style={'width':"5%", 'display':'inline-block'}),
    ]),
    html.Div(id='insurance_detail'),
    html.Hr(
        style={"color": "#FEC700"}
    ),
    html.Div([
            html.H4('Cost Section', style={"font-weight": "bold", 'display':'inline-block'}),
            html.Button('Default Wheat Cost', id='Default_Wheat_Cost', n_clicks=0, style=HTML_COST_SESSION_BUTTON_STYLE),
            html.Button('Default Canola Cost', id='Default_Canola_Cost', n_clicks=0, style=HTML_COST_SESSION_BUTTON_STYLE),
            html.Button('Self Define Cost', id='Self_Define_Cost', n_clicks=0, style=HTML_COST_SESSION_BUTTON_STYLE),
        ]),
    html.Div(
        className='row',
        children=[
            html.Div(
                className='six columns',
                children=[
                    html.Div(
                        'Variable Cost:', style={"font-weight": "bold"}
                    ),
                    html.Div([
                        'Seed ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Seed", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Seed Treatment ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Seed_Treatment", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Fertilizer ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Fertilizer", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Pesticide ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Pesticide", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Fuel ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Fuel", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Machinery Operation ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Machinery_Operation", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Labour Hired ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Labour_Hired", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Utilities and Misc ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Utilities_and_Misc", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Insurance Premium ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Insurance_Premium", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Interest On Operation ($ per acre): ',
                        dcc.Input(id="Variable_Cost_Interest_On_Operation", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                ]
            ),
            html.Div(
                className='six columns',
                children=[
                    html.Div([
                        html.Div('Fixed Cost:', style={"font-weight": "bold"})
                    ]),
                    html.Div([
                        'Building Repair ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Building_Repair", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Property Taxes ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Property_Taxes", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Business Overhead ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Business_Overhead", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Machinery Depreciation ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Machinery_Depreciation", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Building Depreciation ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Building_Depreciation", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Machinery Investment ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Machinery_Investment", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Building Investment ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Building_Investment", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                    html.Div([
                        'Land Investment ($ per acre): ', 
                        dcc.Input(id="Fixed_Cost_Land_Investment", value=None, type="number", placeholder="$ per acre", style={'marginRight':'10px'}),
                    ]),
                ]
            )
        ]
    ),
    html.Hr(
        style={"color": "#FEC700"}
    ),
    html.Div([
        html.Button('Backtest!', id='start_backtest', n_clicks=0, style={'color':'red'}),
    ])


])


@app.callback(
    Output('Variable_Cost_Seed', 'value'),
    Output('Variable_Cost_Seed_Treatment', 'value'),
    Output('Variable_Cost_Fertilizer', 'value'),
    Output('Variable_Cost_Pesticide', 'value'),
    Output('Variable_Cost_Fuel', 'value'),
    Output('Variable_Cost_Machinery_Operation', 'value'),
    Output('Variable_Cost_Labour_Hired', 'value'),
    Output('Variable_Cost_Utilities_and_Misc', 'value'),
    # Output('Variable_Cost_Insurance_Premium', 'value'),
    Output('Variable_Cost_Interest_On_Operation', 'value'),
    Output('Fixed_Cost_Building_Repair', 'value'),
    Output('Fixed_Cost_Property_Taxes', 'value'),
    Output('Fixed_Cost_Business_Overhead', 'value'),
    Output('Fixed_Cost_Machinery_Depreciation', 'value'),
    Output('Fixed_Cost_Building_Depreciation', 'value'),
    Output('Fixed_Cost_Machinery_Investment', 'value'),
    Output('Fixed_Cost_Building_Investment', 'value'),
    Output('Fixed_Cost_Land_Investment', 'value'),
    Input('Default_Wheat_Cost', 'n_clicks'),
    Input('Default_Canola_Cost', 'n_clicks'),
    Input('Self_Define_Cost', 'n_clicks')
    )
def displayClick(btn1, btn2, btn3):
    if "Default_Wheat_Cost" == ctx.triggered_id:
        return WHEAT_DEFAULT_COST
    elif "Default_Canola_Cost" == ctx.triggered_id:
        return CANOLA_DEFAULT_COST
    elif "Self_Define_Cost" == ctx.triggered_id:
        return DEFAULT_COST
    else:
        return DEFAULT_COST

@app.callback(
    Output('Farm_Farmer_Initial_Cash', 'value'),
    Output('Farm_Farmer_Township', 'value'),
    Output('Farm_Farmer_Range', 'value'),
    Output('Farm_Farmer_Meridian', 'value'),
    Output('Farm_Farmer_Area', 'value'),
    Input('Default_farm_farmer_Setting', 'n_clicks')
)
def displayClick(btn1):
    if "Default_farm_farmer_Setting" == ctx.triggered_id:
        return FARM_FARMER_DEFAULT_SETTING
    else:
        return FARM_FARMER_DEFAULT_SETTING

# @app.callback(
#     Output('Variable_Cost_Insurance_Premium', 'value'),
#     Input()
# )


@app.callback(
    Output('weight_table', 'data'),
    Input('Default_Weight', 'n_clicks'),
    Input('MPT_Weight', 'n_clicks')
)
def displayClick(btn1, btn2):
    if 'Default_Weight' == ctx.triggered_id:
        return WEIGHT_TABLE_DEFAULT_WEIGHT
    elif "MPT_Weight" == ctx.triggered_id:
        return []
    else:
        return WEIGHT_TABLE_DEFAULT_WEIGHT

@app.callback(
    Output('insurance_detail', 'children'),
    Output('Variable_Cost_Insurance_Premium', 'value'),
    Input('Farm_Farmer_Township', 'value'),
    Input('Farm_Farmer_Range', 'value'),
    Input('Farm_Farmer_Meridian', 'value'),
    Input('Farm_Farmer_Area', 'value'),
    Input('Insurance_Product_Crop', 'value'),
    Input('Insurance_Product_Field', 'value'),
    Input('Insurance_Product_Coverage', 'value'),
    Input('Insurance_Product_Include_Hail_Endorsement', 'value')
)
def update_output(township, range, meridian, farm_area, crop, field, coverage, is_hail_endorsement):
    farm = Farm(township, range, meridian, farm_area)
    is_include_hail_endorsement = ('' in is_hail_endorsement)
    insurance = AgriInsurance(
        farm=farm,
        insured_acres=farm.farm_area,
        crop=crop,
        field=field,
        coverage=int(coverage),
        include_hail_endorsement=is_include_hail_endorsement
    )
    total_premium = insurance.get_total_premium()
    VARIABLE_COST_INSURANCE_PREMIUM = WHEAT_VARIABLE_COST_INSURANCE_PREMIUM = CANOLA_VARIABLE_COST_INSURANCE_PREMIUM = total_premium
    detail_summary = insurance.get_insurance_information_str(for_html=True)
    res_datail = []
    for e in detail_summary:
        res_datail.append(e)
        res_datail.append(html.Br())
    res_datail.pop()
    return res_datail, VARIABLE_COST_INSURANCE_PREMIUM


@app.callback(
    Output('Backtest_Year_Range', 'children'),
    Input('Backtest_Year_Range_Slider', 'value')
)
def display_value(value):
    return f"Backtest Year Range from {value[0]} to {value[1]}"















@app.callback(
    Output('result-graph', 'figure'),
    Output('result_performance_table', 'data'),
    Input('start_backtest', 'n_clicks'),
    Input('Backtest_Year_Range_Slider', 'value'),
    Input('weight_table', 'data'),
    Input('financial_product_selection', 'value'),
    Input('Farm_Farmer_Initial_Cash', 'value'),
    Input('Farm_Farmer_Township', 'value'),
    Input('Farm_Farmer_Range', 'value'),
    Input('Farm_Farmer_Meridian', 'value'),
    Input('Farm_Farmer_Area', 'value'),
    Input('Insurance_Product_Crop', 'value'),
    Input('Insurance_Product_Field', 'value'),
    Input('Insurance_Product_Coverage', 'value'),
    Input('Insurance_Product_Include_Hail_Endorsement', 'value'),
    Input('Variable_Cost_Seed', 'value'),
    Input('Variable_Cost_Seed_Treatment', 'value'),
    Input('Variable_Cost_Fertilizer', 'value'),
    Input('Variable_Cost_Pesticide', 'value'),
    Input('Variable_Cost_Fuel', 'value'),
    Input('Variable_Cost_Machinery_Operation', 'value'),
    Input('Variable_Cost_Labour_Hired', 'value'),
    Input('Variable_Cost_Utilities_and_Misc', 'value'),
    Input('Variable_Cost_Insurance_Premium', 'value'),
    Input('Variable_Cost_Interest_On_Operation', 'value'),
    Input('Fixed_Cost_Building_Repair', 'value'),
    Input('Fixed_Cost_Property_Taxes', 'value'),
    Input('Fixed_Cost_Business_Overhead', 'value'),
    Input('Fixed_Cost_Machinery_Depreciation', 'value'),
    Input('Fixed_Cost_Building_Depreciation', 'value'),
    Input('Fixed_Cost_Machinery_Investment', 'value'),
    Input('Fixed_Cost_Building_Investment', 'value'),
    Input('Fixed_Cost_Land_Investment', 'value'),
)
def update_output(
    btn1,
    backtest_year_range,
    weight_data, 
    financial_product_selection,
    Farm_Farmer_Initial_Cash,
    Farm_Farmer_Township,
    Farm_Farmer_Range,
    Farm_Farmer_Meridian,
    Farm_Farmer_Area,
    Insurance_Product_Crop,
    Insurance_Product_Field,
    Insurance_Product_Coverage,
    Insurance_Product_Include_Hail_Endorsement,
    Variable_Cost_Seed,
    Variable_Cost_Seed_Treatment,
    Variable_Cost_Fertilizer,
    Variable_Cost_Pesticide,
    Variable_Cost_Fuel,
    Variable_Cost_Machinery_Operation,
    Variable_Cost_Labour_Hired,
    Variable_Cost_Utilities_and_Misc,
    Variable_Cost_Insurance_Premium,
    Variable_Cost_Interest_On_Operation,
    Fixed_Cost_Building_Repair,
    Fixed_Cost_Property_Taxes,
    Fixed_Cost_Business_Overhead,
    Fixed_Cost_Machinery_Depreciation,
    Fixed_Cost_Building_Depreciation,
    Fixed_Cost_Machinery_Investment,
    Fixed_Cost_Building_Investment,
    Fixed_Cost_Land_Investment,
    ):
    if "start_backtest" == ctx.triggered_id:
        backtest_year_start, backtest_year_end = backtest_year_range
        if len(weight_data) == 0:
            print('weight_data is not found, use default MPT weight instead.')
            is_MPT_weight = True
            weights = FARMING_ONLY_CASH_ALLOCATION
        else:
            is_MPT_weight = False
            weights = {
                '2018':{
                    'w_1': round(float(weight_data[0]['weight_1']), 2),
                    'w_2': round(float(weight_data[0]['weight_2']), 2),
                    'w_3': round(float(weight_data[0]['weight_3']), 2),
                },
                '2019':{
                    'w_1': round(float(weight_data[1]['weight_1']), 2),
                    'w_2': round(float(weight_data[1]['weight_2']), 2),
                    'w_3': round(float(weight_data[1]['weight_3']), 2),
                },
                '2020':{
                    'w_1': round(float(weight_data[2]['weight_1']), 2),
                    'w_2': round(float(weight_data[2]['weight_2']), 2),
                    'w_3': round(float(weight_data[2]['weight_3']), 2),
                },
            }
        if financial_product_selection == 'KOI_product_v1':
            financial_product_selection = 'Chagoi'
        farm_and_farmer_dict = {
            'Farm_Farmer_Initial_Cash': Farm_Farmer_Initial_Cash,
            'Farm_Farmer_Township': Farm_Farmer_Township,
            'Farm_Farmer_Range': Farm_Farmer_Range,
            'Farm_Farmer_Meridian': Farm_Farmer_Meridian,
            'Farm_Farmer_Area': Farm_Farmer_Area,
        }
        insurance_dict = {
            'Insurance_Product_Crop': Insurance_Product_Crop,
            'Insurance_Product_Field': Insurance_Product_Field,
            'Insurance_Product_Coverage': int(Insurance_Product_Coverage),
            'Insurance_Product_Include_Hail_Endorsement': ('' in Insurance_Product_Include_Hail_Endorsement),
        }
        cost_dict = {
            'Variable_Cost': {
                'Variable_Cost_Seed': Variable_Cost_Seed,
                'Variable_Cost_Seed_Treatment': Variable_Cost_Seed_Treatment,
                'Variable_Cost_Fertilizer': Variable_Cost_Fertilizer,
                'Variable_Cost_Pesticide': Variable_Cost_Pesticide,
                'Variable_Cost_Fuel': Variable_Cost_Fuel,
                'Variable_Cost_Machinery_Operation': Variable_Cost_Machinery_Operation,
                'Variable_Cost_Labour_Hired': Variable_Cost_Labour_Hired,
                'Variable_Cost_Utilities_and_Misc': Variable_Cost_Utilities_and_Misc,
                'Variable_Cost_Insurance_Premium': Variable_Cost_Insurance_Premium,
                'Variable_Cost_Interest_On_Operation': Variable_Cost_Interest_On_Operation,
            },
            'Fixed_Cost': {
                'Fixed_Cost_Building_Repair': Fixed_Cost_Building_Repair,
                'Fixed_Cost_Property_Taxes': Fixed_Cost_Property_Taxes,
                'Fixed_Cost_Business_Overhead': Fixed_Cost_Business_Overhead,
                'Fixed_Cost_Machinery_Depreciation': Fixed_Cost_Machinery_Depreciation,
                'Fixed_Cost_Building_Depreciation': Fixed_Cost_Building_Depreciation,
                'Fixed_Cost_Machinery_Investment': Fixed_Cost_Machinery_Investment,
                'Fixed_Cost_Building_Investment': Fixed_Cost_Building_Investment,
                'Fixed_Cost_Land_Investment': Fixed_Cost_Land_Investment,
            }
        }
        
        benchmark_farmer = backtest(
            start_year=backtest_year_start,
            end_year=backtest_year_end,
            initial_cash_allocation=FARMING_ONLY_CASH_ALLOCATION,
            is_MPT_weight=False,
            financial_product_selection=financial_product_selection,
            farm_and_farmer_dict=farm_and_farmer_dict,
            insurance_dict=insurance_dict,
            cost_dict=cost_dict,
            return_farmer_only=True
        )
        #################################
        #################################
        #################################

        DEFAULT_MPT_CONFIG = {
            'method': "min_volatility",
            'weight_bdd': {
                'financial_product_return': {'max':0.35, 'min':0.05},   # 0
                'spot_price_return': {'max':1, 'min':0.6},            # 1
                'insurance_return': {'max':0.1, 'min':0.0},           # 2
            },
        }

        #################################
        #################################
        #################################

        fig = backtest(
            start_year=backtest_year_start,
            end_year=backtest_year_end,
            initial_cash_allocation=weights,
            is_MPT_weight=is_MPT_weight,
            financial_product_selection=financial_product_selection,
            farm_and_farmer_dict=farm_and_farmer_dict,
            insurance_dict=insurance_dict,
            cost_dict=cost_dict,
            benchmark_farmer=benchmark_farmer,
            mpt_config=DEFAULT_MPT_CONFIG
        )

        # update result performance
        farmer_asset_df = pd.DataFrame(index=fig.data[1].x, data=fig.data[1].y)
        result_performance = RESULT_PERFORMANCE_TABLE_DEFAULT_DATA
        if '2018-01-01' in farmer_asset_df.index:
            r_2018_dollar = round(farmer_asset_df.loc[['2018-01-01', '2018-12-31']].diff().iloc[-1][0], 2)
            r_2018_pct = round(farmer_asset_df.loc[['2018-01-01', '2018-12-31']].pct_change().iloc[-1][0] * 100, 2)
            result_performance[0] = {'year': 2018, 'wealth_change_dollar':r_2018_dollar, 'wealth_change_pct': r_2018_pct}
        # a=1
        if '2019-01-01' in farmer_asset_df.index:
            r_2019_dollar = round(farmer_asset_df.loc[['2019-01-01', '2019-12-31']].diff().iloc[-1][0], 2)
            r_2019_pct = round(farmer_asset_df.loc[['2019-01-01', '2019-12-31']].pct_change().iloc[-1][0] * 100, 2)
            result_performance[1] = {'year': 2019, 'wealth_change_dollar':r_2019_dollar, 'wealth_change_pct': r_2019_pct}
        # a=1
        if '2020-01-01' in farmer_asset_df.index:
            r_2020_dollar = round(farmer_asset_df.loc[['2020-01-01', '2020-12-31']].diff().iloc[-1][0], 2)
            r_2020_pct = round(farmer_asset_df.loc[['2020-01-01', '2020-12-31']].pct_change().iloc[-1][0] * 100, 2)
            result_performance[2] = {'year': 2020, 'wealth_change_dollar':r_2020_dollar, 'wealth_change_pct': r_2020_pct}
        # a=1

        print(f"Finish result at {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")

        return fig, result_performance
    else:
        return fig, RESULT_PERFORMANCE_TABLE_DEFAULT_DATA




if __name__ == '__main__':
    app.run_server(debug=True, port=8058, host='0.0.0.0')