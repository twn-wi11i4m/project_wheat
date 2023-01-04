import pandas as pd

def get_datelist(start_date:str, end_date:str) -> list:
    """
    a datelist from start_date to end_date

    :return date_list: a sorted date list contain date str.
    """
    date_list = pd.date_range(start_date, end_date, freq='D').strftime("%Y-%m-%d").tolist()
    return date_list

def is_end_of_month(adate:str) -> bool:
    """
    month_end_list
    """
    month_end_list = pd.date_range('2000-01-31','2023-12-31',freq='M').strftime("%Y-%m-%d").tolist()
    return adate in month_end_list

def metric_tonne_to_bushel(metric_tonne, crop_type='wheat') -> float:
    """
    return the amount in bushel
    """
    if crop_type == 'wheat':
        bushel = metric_tonne * 36.74371
    elif crop_type == 'barley':
        bushel = metric_tonne * 45.9296
    return bushel

def bushel_to_metric_tonne(bushel, crop_type='wheat') -> float:
    """
    return the amount in metric tonne
    """
    if crop_type == 'wheat':
        metric_tonne = bushel * 0.0272
    elif crop_type == 'barley':
        metric_tonne = bushel * 0.0218
    return metric_tonne

def change_koi_name(s) -> str:
    """
    display the koi model in public way
    """
    mapper = {
        'Chagoi': 'KOI_product_v1'
    }
    return mapper.get(s,s) 




