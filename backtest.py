from farmer import Farmer_v2, Farm
from util import *
from constant import *
from agriculture_products import WheatYears, Canola
# from constant import *
from MPT_weighter_v2 import MPT_Weighter_v2
from insurance import AgriInsurance
from financial_product import FinancialProduct
from plot_wealth_v2 import *


# from main_test import WEIGHT_TABLE_DEFAULT_WEIGHT

DEFAULT_MPT_CONFIG = {
    'method': "min_volatility",
    'weight_bdd': {
        'financial_product_return': {'max':0.1, 'min':0.0},   # 0
        'spot_price_return': {'max':1, 'min':0.9},            # 1
        'insurance_return': {'max':0.1, 'min':0.0},           # 2
    },
}



# def backtest(
#     start_year=2018,
#     end_year=2020,
#     initial_cash_allocation={
#         '2018':{
#             'w_1': 0.33,
#             'w_2': 0.33,
#             'w_3': 0.33
#         },
#         '2019':{
#             'w_1': 0.33,
#             'w_2': 0.33,
#             'w_3': 0.33
#         },
#         '2020':{
#             'w_1': 0.33,
#             'w_2': 0.33,
#             'w_3': 0.33
#         },
#     },
#     return_farmer_only=False, 
#     benchmark_farmer=None,
#     financial_product_selection='naive',
#     is_MPT_weight=False,
#     mpt_config=DEFAULT_MPT_CONFIG,
#     ):

def backtest(
    start_year:int,
    end_year:int,
    initial_cash_allocation:dict,
    is_MPT_weight:bool,
    financial_product_selection:str,
    farm_and_farmer_dict:dict,
    insurance_dict:dict,
    cost_dict:dict,
    mpt_config=DEFAULT_MPT_CONFIG,
    return_farmer_only=False, 
    benchmark_farmer=None,
):
    # farm = Farm(township=7, range=21, meridian=4, farm_area=1)
    farm = Farm(
        township=farm_and_farmer_dict['Farm_Farmer_Township'], 
        range=farm_and_farmer_dict['Farm_Farmer_Range'],
        meridian=farm_and_farmer_dict['Farm_Farmer_Meridian'],
        farm_area=farm_and_farmer_dict['Farm_Farmer_Area']
    )
    # farmer = Farmer(initial_cash=100_000, farm=farm)
    farmer = Farmer_v2(
        initial_cash=farm_and_farmer_dict['Farm_Farmer_Initial_Cash'], 
        farm=farm
    )

    # farmer.cost = {
    #             'Operational Cost': {
    #                 'Seed Treatment':34,
    #                 'Fertilizer':180.26,
    #                 'Pesticide':55.33,
    #                 'Fuel':46.75,
    #                 'Machinery_Operation_Lease':25,
    #                 'Labour Hired':5.2,
    #                 'Drying Other Costs':17.75,
    #                 'Insurance Premium': None,
    #                 'Land Taxes':17.5,
    #                 'Storage Costs':18.19,
    #                 'Interest On Operation':16.42,
    #             },
    #             'Fixed Cost': {
    #                 'Land Costs': 97.17,
    #                 'Machinery Costs': 86.37
    #             }
    #         }
    farmer.cost_detail = cost_dict



    date_list = get_datelist(f'{start_year}-01-01', f'{end_year}-12-31')


    # Assume apply_agrinsurance_date and purchase_financial_product_date are the same day
    important_dates_dict = {
        '2018': {
            'apply_agrinsurance_date': '2018-04-01',
            'purchase_financial_product_date': '2018-04-01',
            'plant_crop_date' : '2018-04-10',
            'harvest_date': '2018-10-13',
            'end_financial_product_date': '2018-10-30',
            'payoff_financial_product_date': '2018-10-31',
            'sell_crop_date': '2018-11-03',
            'agriinsurance_indemnity_payment_date':'2018-11-05',
        },
        '2019':{
            'apply_agrinsurance_date': '2019-04-01',
            'purchase_financial_product_date': '2019-04-01',
            'plant_crop_date' : '2019-04-10',
            'harvest_date': '2019-10-13',
            'end_financial_product_date': '2019-10-30',
            'payoff_financial_product_date': '2019-10-31',
            'sell_crop_date': '2019-11-03',
            'agriinsurance_indemnity_payment_date':'2019-11-05',
        },
        '2020': {
            'apply_agrinsurance_date': '2020-04-01',
            'purchase_financial_product_date': '2020-04-01',
            'plant_crop_date' : '2020-04-10',
            'harvest_date': '2020-10-13',
            'end_financial_product_date': '2020-10-30',
            'payoff_financial_product_date': '2020-10-31',
            'sell_crop_date': '2020-11-03',
            'agriinsurance_indemnity_payment_date':'2020-11-05',
        }
    }


    wheat_years = WheatYears(years=['2018', '2019', '2020'], risk_area=farm.risk_area)

    if is_MPT_weight:
        # Assume we have a backtest period for the financial product
        previous_financial_product = FinancialProduct(
            # invest_capital=100_000,
            invest_capital=farm_and_farmer_dict['Farm_Farmer_Initial_Cash'],
            initial_date=f'{start_year-1}-04-01',
            final_payoff_date=f'{start_year-1}-10-30',
            selected_product=financial_product_selection
        )
        # Assume we have a backtest period for the insurance product
        # previosu_insurance_product = AgriInsurance(farm=farm, insured_acres=farm.farm_area, crop='HRS', field='stubble', coverage=50, include_hail_endorsement=True)
        previosu_insurance_product = AgriInsurance(
            farm=farm, 
            insured_acres=farm.farm_area, 
            crop=insurance_dict['Insurance_Product_Crop'], 
            field=insurance_dict['Insurance_Product_Field'], 
            coverage=insurance_dict['Insurance_Product_Coverage'], 
            include_hail_endorsement=insurance_dict['Insurance_Product_Include_Hail_Endorsement']
        )

        # we calculate the initial mpt weight
        mpt_weighter = MPT_Weighter_v2(
            lookback_days=360, 
            previous_market_data=MarketData(), 
            previous_financial_product=previous_financial_product,
            previous_insurance_product=previosu_insurance_product
            )

    wheat_years = WheatYears(years=['2017', '2018', '2019', '2020'], risk_area=farm.risk_area)
    if is_MPT_weight:
        wheat_years.set_year('2017')
        farmer.plant_crop(wheat_years)
        previous_yield = farmer.harvest()
        # mpt_weight = mpt_weighter.get_weight(last_lb_date='2018-01-02', previous_yield=previous_yield)

    # save the weight dict with year start, i.e. start before 2018
    mpt_weight_dict = {
        # '2018'
    }

    for adate in date_list:
        year = adate.split('-')[0]
        farmer.set_adate(adate)
        wheat_years.set_year(year)

        if adate == important_dates_dict[year]['purchase_financial_product_date']:
            # invest_capital = invest_capital
            if is_MPT_weight:
                mpt_weight = mpt_weighter.get_weight(
                    last_lb_date=adate, 
                    previous_yield=previous_yield, 
                    method=mpt_config['method'],
                    weight_bdd=mpt_config['weight_bdd']
                )
                mpt_weight_dict[year] = dict(mpt_weight)
                print('[MPT]==============')
                print(adate)
                print(mpt_weight)
                invest_capital = mpt_weight['financial_product_return'] * farmer.cash
            else:
                predefine_weight = initial_cash_allocation[year]
                print('[pre-define weight]==============')
                print(adate)
                print(predefine_weight)
                invest_capital = predefine_weight['w_1'] * farmer.cash
            
            if invest_capital <= 0:
                print(f"invest capital: {invest_capital} is not enough! No Financial product is added.")
                farmer.add_FinancialProduct(None)
            else:
                farmer.add_FinancialProduct(
                    FinancialProduct(
                        invest_capital=invest_capital, 
                        initial_date=important_dates_dict[year]['purchase_financial_product_date'],
                        final_payoff_date=important_dates_dict[year]['end_financial_product_date'],
                        selected_product=financial_product_selection
                    )
                )
                farmer.cash_paid('invested capital', invest_capital)

        if adate == important_dates_dict[year]['payoff_financial_product_date'] and farmer.financial_products[year] is not None:
            if is_MPT_weight:
                # update weighter
                previous_financial_product = farmer.financial_products[year]
                mpt_weighter = MPT_Weighter_v2(
                    lookback_days=360, 
                    previous_market_data=MarketData(), 
                    previous_financial_product=previous_financial_product,
                    previous_insurance_product=previosu_insurance_product
                    )
            
            payoff = farmer.financial_products[year].final_return_dollar()
            if payoff != 0:
                farmer.cash_received('revenue financial product', payoff)

        if adate == important_dates_dict[year]['apply_agrinsurance_date']:
            # farmer.insurance = AgriInsuranc(expected_yield_level=expected_yield_level, cover_level=cover_level, risk_area=farmer.risk_area)
            # mpt_weight = mpt_weighter.get_weight(last_lb_date=adate, previous_yield=previous_yield, method=mpt_config['method'])      # since apply_agrinsurance_date == purchase_financial_product_date
            if is_MPT_weight:
                insurance_capital = mpt_weight['insurance_return'] * farmer.cash
            else:
                insurance_capital = predefine_weight['w_3'] * farmer.cash
            
            # selected_insurance = AgriInsurance(farm=farm, insured_acres=farm.farm_area, crop='HRS', field='stubble', coverage=50, include_hail_endorsement=True)
            selected_insurance = AgriInsurance(
                farm=farm, 
                insured_acres=farm.farm_area, 
                crop=insurance_dict['Insurance_Product_Crop'], 
                field=insurance_dict['Insurance_Product_Field'], 
                coverage=insurance_dict['Insurance_Product_Coverage'], 
                include_hail_endorsement=insurance_dict['Insurance_Product_Include_Hail_Endorsement']
            )
            selected_insurance_total_premium = selected_insurance.get_total_premium()
            if selected_insurance_total_premium <= insurance_capital:
                print(f"Total insurance premium: {selected_insurance_total_premium} & insurance capital ({insurance_capital}) is sufficient to pay for.")
                farmer.insurance = selected_insurance
            else:
                print(f"Total insurance premium: {selected_insurance_total_premium} & insurance capital ({insurance_capital}) is not enough! No insurance is purchase.")
                farmer.insurance = None

        if farmer.insurance is not None and adate <= important_dates_dict[year]['agriinsurance_indemnity_payment_date']:
            if farmer.insurance.is_premium_pay_date(adate):
                monthly_premium = farmer.insurance.get_total_premium()
                farmer.cash_paid('insurance premium', monthly_premium)
        
        if adate == important_dates_dict[year]['plant_crop_date']:
            farmer.plant_crop(wheat_years)

        if adate == important_dates_dict[year]['harvest_date']:
            total_yield = farmer.harvest()
            total_variable_cost = farmer.total_variable_cost
            total_fixed_cost = farmer.total_fixed_cost
            farmer.cash_paid('total variable cost', total_variable_cost)
            farmer.cash_paid('total fixed cost', total_fixed_cost)

        if farmer.insurance is not None and adate == important_dates_dict[year]['agriinsurance_indemnity_payment_date']:
            revenue_insurance = farmer.insurance.calc_indemnity(total_yield)
            if revenue_insurance != 0:
                farmer.cash_received('Revenue Insurance', revenue_insurance)

        if adate == important_dates_dict[year]['sell_crop_date']:
            farmer.sell_crop(100)
            last_sell_crop_revenue = farmer.last_sell_crop_revenue
            farmer.cash_received('Revenue Crop', last_sell_crop_revenue)

    res_status = 'mpt' if is_MPT_weight else 'pre-define'
    save_wealth_csv(farmer, date_list, res_path='res_html', title=f'res', sub_title=f'{res_status}_{start_year}_{end_year}', is_include_detail=True)

    # if '2018-01-02' in date_list:
    #     d1 = round(mpt_weight_dict['2018']['financial_product_return'], 3)
    # else:
    #     d1=0
    # if '2019-01-02' in date_list:
    #     d2 = round(mpt_weight_dict['2019']['financial_product_return'], 3)
    # else:
    #     d2=0
    # if '2020-01-02' in date_list:
    #     d3 = round(mpt_weight_dict['2020']['financial_product_return'], 3)
    # else:
    #     d3=0

    # Clear MPT weight dict
    if is_MPT_weight:
        if '2018' in mpt_weight_dict:
            mpt_weight_dict['2018'] = dict(zip(mpt_weight_dict['2018'].keys(), list(map(lambda x:round(x, 2), mpt_weight_dict['2018'].values()))))
        if '2019' in mpt_weight_dict:
            mpt_weight_dict['2019'] = dict(zip(mpt_weight_dict['2019'].keys(), list(map(lambda x:round(x, 2), mpt_weight_dict['2019'].values()))))
        if '2020' in mpt_weight_dict:
            mpt_weight_dict['2020'] = dict(zip(mpt_weight_dict['2020'].keys(), list(map(lambda x:round(x, 2), mpt_weight_dict['2020'].values()))))


    if return_farmer_only:
        return farmer
    else:
        # sub_title_text = f"2018: {tuple(initial_cash_allocation['2018'].values())}, 2019: {tuple(initial_cash_allocation['2019'].values())}, 2020: {tuple(initial_cash_allocation['2020'].values())} <br> mpt method: {mpt_config['method']} | Financial Product: {change_koi_name(financial_product_selection)}"
        if is_MPT_weight:
            sub_title_text = f"2018: {tuple(mpt_weight_dict.get('2018', {}).values())}, 2019: {tuple(mpt_weight_dict.get('2019', {}).values())}, 2020: {tuple(mpt_weight_dict.get('2020', {}).values())} <br> mpt method: {mpt_config['method']} | Financial Product: {change_koi_name(financial_product_selection)}"
        else:
            sub_title_text = f"2018: {tuple(initial_cash_allocation.get('2018', {}).values())}, 2019: {tuple(initial_cash_allocation.get('2019', {}).values())}, 2020: {tuple(initial_cash_allocation.get('2020', {}).values())} <br> mpt method: N/A | Financial Product: {change_koi_name(financial_product_selection)}"
        fig = plot_portfolio(
            farmer, 
            date_list, 
            res_path='res_html', 
            title=f'approach_{res_status} weight', 
            # sub_title=f"approach 2018 ratio: {d1}, 2019 ratio: {d2}, 2020 ratio:{d3} with mpt method: {mpt_config['method']} | Financial Product: {change_koi_name(financial_product_selection)}", 
            sub_title=sub_title_text,
            benchmark_farmer=benchmark_farmer)
    return fig






if __name__ == "__main__":
    backtest_year_start = 2018
    backtest_year_end = 2020
    weights = {
        '2018':{
            'w_1': 0.12,
            'w_2': 0.34,
            'w_3': 0.54,
        },
        '2019':{
            'w_1': 0.45,
            'w_2': 0.15,
            'w_3': 0.40,
        },
        '2020':{
            'w_1': 0.21,
            'w_2': 0.31,
            'w_3': 0.48,
        },
    }
    # weights = {
    #     '2018':{
    #         'w_1': 1,
    #         'w_2': 0,
    #         'w_3': 0,
    #     },
    #     '2019':{
    #         'w_1': 1,
    #         'w_2': 0,
    #         'w_3': 0,
    #     },
    #     '2020':{
    #         'w_1': 1,
    #         'w_2': 0,
    #         'w_3': 0,
    #     },
    # }
    
    # financial_product_selection = 'naive'
    financial_product_selection = 'Chagoi'

    farm_and_farmer_dict = {
        'Farm_Farmer_Initial_Cash': 100000,
        'Farm_Farmer_Township': 7,
        'Farm_Farmer_Range': 21,
        'Farm_Farmer_Meridian': 4,
        'Farm_Farmer_Area': 1,
    }
    insurance_dict = {
        'Insurance_Product_Crop': 'HRS',
        'Insurance_Product_Field': 'stubble',
        'Insurance_Product_Coverage': 50,
        'Insurance_Product_Include_Hail_Endorsement': False,
    }
    cost_dict = {
        'Variable_Cost': {
            'Variable_Cost_Seed': 26.92,
            'Variable_Cost_Seed_Treatment': 0.74,
            'Variable_Cost_Fertilizer': 158.05,
            'Variable_Cost_Pesticide': 101.19,
            'Variable_Cost_Fuel': 15.31,
            'Variable_Cost_Machinery_Operation': 9.98,
            'Variable_Cost_Labour_Hired': 22.05,
            'Variable_Cost_Utilities_and_Misc': 4.23,
            'Variable_Cost_Insurance_Premium': 1.73,
            'Variable_Cost_Interest_On_Operation': 7.13,
        },
        'Fixed_Cost': {
            'Fixed_Cost_Building_Repair': 0.69,
            'Fixed_Cost_Property_Taxes': 5.55,
            'Fixed_Cost_Business_Overhead': 3.19,
            'Fixed_Cost_Machinery_Depreciation': 41.06,
            'Fixed_Cost_Building_Depreciation': 1.45,
            'Fixed_Cost_Machinery_Investment': 15.83,
            'Fixed_Cost_Building_Investment': 0.48,
            'Fixed_Cost_Land_Investment': 39.28,
        }
    }



    backtest(
        start_year=backtest_year_start,
        end_year=backtest_year_end,
        initial_cash_allocation=weights,
        is_MPT_weight=False,
        financial_product_selection=financial_product_selection,
        farm_and_farmer_dict=farm_and_farmer_dict,
        insurance_dict=insurance_dict,
        cost_dict=cost_dict
    )

    # backtest(
    #     start_year=backtest_year_start,
    #     end_year=backtest_year_end,
    #     initial_cash_allocation=weights,
    #     is_MPT_weight=True,
    #     financial_product_selection=financial_product_selection,
    #     farm_and_farmer_dict=farm_and_farmer_dict,
    #     insurance_dict=insurance_dict,
    #     cost_dict=cost_dict
    # )
    a=1