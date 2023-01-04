import os


EXPECT_YIELD= {
    'Fallow': 31.9,
    'Stubble': 25.2,
    'Irr': 82.2
}

PLANT_CROP_DATE = '2018-05-04'
HARVEST_DATE = '2018-10-06'


EXPECTED_YIELD_LEVEL_LIST = [
    "Fallow",
    "Stubble",
    "Irrigated"
]

COVER_LEVEL_LIST = [
    50,
    60,
    70,
    80
]

INVEST_CAPITAL_LIST = [
    10_000 + i * 10_000 for i in range(11)
]

DATA_SOURCE_FOLDER_PATH = "DataSource"
KOI_CHAGOI_FOLDER_PATH = os.path.join(DATA_SOURCE_FOLDER_PATH, "Chagoi_wheat_futures_scale_up_results")

INITIAL_CASH_ALLOCATION = {
    '2018':{
        'farming activity': 1,
        'financial activity':0
    },
    '2019':{
            'farming activity': 1,
            'financial activity':0
    },
    '2020':{
            'farming activity': 1,
            'financial activity':0
        }
}

FARMING_ONLY_CASH_ALLOCATION = {
    '2018':{
        'w_1': 0.00,
        'w_2': 1.00,
        'w_3': 0.00,
    },
    '2019':{
        'w_1': 0.00,
        'w_2': 1.00,
        'w_3': 0.00,
    },
    '2020':{
        'w_1': 0.00,
        'w_2': 1.00,
        'w_3': 0.00,
    },
}

HTML_FARM_FARMER_SESSION_BUTTON_STYLE = {
    'width': '240px', 
    'height': '28px', 
    'cursor': 'pointer', 
    'align': 'center',
    'border-radius': '4px', 
    'verticalAlign': 'center',
    'margin-left': '4px',
    'margin-right': '4px',
    'paddingLeft': '2px',
    'paddingRight': '2px',
    'paddingTop':'0px',
    'paddingBottom':'0px',
    'text-align':'center',
    'font-size': '9px'
    }

HTML_COST_SESSION_BUTTON_STYLE = {
    'width': '140px', 
    'height': '28px', 
    'cursor': 'pointer', 
    'align': 'center',
    'border-radius': '4px', 
    'verticalAlign': 'center',
    'margin-left': '4px',
    'margin-right': '4px',
    'paddingLeft': '2px',
    'paddingRight': '2px',
    'paddingTop':'0px',
    'paddingBottom':'0px',
    'text-align':'center',
    'font-size': '9px'
    }