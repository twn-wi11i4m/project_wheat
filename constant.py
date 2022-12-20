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