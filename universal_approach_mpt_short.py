from farmer import Farmer, Farm
from util import *
from constant import *
from agriculture_products import WheatYears, Canola
# from constant import *
from MPT_weighter import MPT_Weighter
from insurance import AgriInsurance
from financial_product import FinancialProduct
from plot_wealth import *

DEFAULT_MPT_CONFIG = {
    'method': "min_volatility",
}


def universal_approach_3_years_mpt_short(
    start_year=2018,
    end_year=2020, 
    return_farmer_only=False, 
    benchmark_farmer=None, 
    mpt_config=DEFAULT_MPT_CONFIG,
    financial_product_selection='naive'
    ):
    farm = Farm(township=7, range=21, meridian=4, farm_area=1)
    farmer = Farmer(initial_cash=100_000, farm=farm)
    farmer.cost = {
                'Operational Cost': {
                    'Seed Treatment':34,
                    'Fertilizer':180.26,
                    'Pesticide':55.33,
                    'Fuel':46.75,
                    'Machinery_Operation_Lease':25,
                    'Labour Hired':5.2,
                    'Drying Other Costs':17.75,
                    'Insurance Premium': None,
                    'Land Taxes':17.5,
                    'Storage Costs':18.19,
                    'Interest On Operation':16.42,
                },
                'Fixed Cost': {
                    'Land Costs': 97.17,
                    'Machinery Costs': 86.37
                }
            }

    # universal approach
    # initial_cash_allocation = {
    #     'farming activity': 1,
    #     'financial activity':0
    # }
    
    date_list = get_datelist(f'{start_year}-01-01', f'{end_year}-12-31')

    important_dates_dict = {
        '2018': {
            'apply_agrinsurance_date': '2018-04-01',
            'agriinsuranc_indemnity_payment_date':'2018-11-05',
            'plant_crop_date' : '2018-04-10',
            'harvest_date': '2018-10-13',
            'sell_crop_date': '2018-11-03',
            'purchase_financial_product_date': '2018-04-01',
            'end_financial_product_date': '2018-10-30',
            'payoff_financial_product_date': '2018-10-31',
        },
        '2019':{
            'apply_agrinsurance_date': '2019-04-01',
            'agriinsuranc_indemnity_payment_date':'2019-11-05',
            'plant_crop_date' : '2019-04-10',
            'harvest_date': '2019-10-13',
            'sell_crop_date': '2019-11-03',
            'purchase_financial_product_date': '2019-04-01',
            'end_financial_product_date': '2019-10-30',
            'payoff_financial_product_date': '2019-10-31',
        },
        '2020': {
            'apply_agrinsurance_date': '2020-04-01',
            'agriinsuranc_indemnity_payment_date':'2020-11-05',
            'plant_crop_date' : '2020-04-10',
            'harvest_date': '2020-10-13',
            'sell_crop_date': '2020-11-03',
            'purchase_financial_product_date': '2020-04-01',
            'end_financial_product_date': '2020-10-30',
            'payoff_financial_product_date': '2020-10-31',
        }
    }

    wheat_years = WheatYears(years=['2018', '2019', '2020'], risk_area=farm.risk_area)
    
    # Assume we have a backtest period for the financial product
    previous_financial_product = FinancialProduct(
        invest_capital=100_000,
        initial_date=f'{start_year-1}-04-01',
        final_payoff_date=f'{start_year-1}-10-30',
        selected_product=financial_product_selection
    )
    # we calculate the initial mpt weight
    mpt_weighter = MPT_Weighter(
        lookback_days=360,
        previous_market_data=MarketData(),
        previous_financial_product=previous_financial_product,
        is_short=True)
    # mpt_weight = mpt_weighter.get_weight(last_lb_date='2018-01-02')

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
            mpt_weight = mpt_weighter.get_weight(last_lb_date=adate, method=mpt_config['method'])
            mpt_weight_dict[year] = dict(mpt_weight)
            print('==============')
            print(adate)
            print(mpt_weight)
            invest_capital = mpt_weight['financial_product_return'] * farmer.cash
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
            # update weighter
            previous_financial_product = farmer.financial_products[year]
            mpt_weighter = MPT_Weighter(lookback_days=360, previous_market_data=MarketData(), previous_financial_product=previous_financial_product)
            payoff = farmer.financial_products[year].final_return_dollar()
            if payoff != 0:
                farmer.cash_received('revenue financial product', payoff)



        if adate == important_dates_dict[year]['apply_agrinsurance_date']:
            # farmer.insurance = AgriInsuranc(expected_yield_level=expected_yield_level, cover_level=cover_level, risk_area=farmer.risk_area)
            farmer.insurance = AgriInsurance(farm=farm, insured_acres=farm.farm_area, crop='HRS', field='stubble', coverage=50, include_hail_endorsement=True)

        if farmer.insurance is not None and adate <= important_dates_dict[year]['agriinsuranc_indemnity_payment_date']:
            if farmer.insurance.is_premium_pay_date(adate):
                monthly_premium = farmer.insurance.get_total_premium()
                farmer.cash_paid('insurance premium', monthly_premium)


        if adate == important_dates_dict[year]['plant_crop_date']:
            farmer.plant_crop(wheat_years)

        if adate == important_dates_dict[year]['harvest_date']:
            total_yield = farmer.harvest()
            total_operational_cost = farmer.total_operational_cost
            total_fixed_cost = farmer.total_fixed_cost
            farmer.cash_paid('total operational cost', total_operational_cost)
            farmer.cash_paid('total fixed cost', total_fixed_cost)

        if adate == important_dates_dict[year]['agriinsuranc_indemnity_payment_date']:
            revenue_insurance = farmer.insurance.calc_indemnity(total_yield)
            if revenue_insurance != 0:
                farmer.cash_received('Revenue Insurance', revenue_insurance)

        if adate == important_dates_dict[year]['sell_crop_date']:
            farmer.sell_crop(100)
            last_sell_crop_revenue = farmer.last_sell_crop_revenue
            farmer.cash_received('Revenue Crop', last_sell_crop_revenue)
        
    # plot_wealth(farmer, date_list, res_path='res_html', title='approach_2', sub_title='approach_2')
    save_wealth_csv(farmer, date_list, res_path='res_html', title=f'approach', sub_title='approach_2')
    # d1=initial_cash_allocation['2018']['financial activity']
    # d2=initial_cash_allocation['2019']['financial activity']
    # d3=initial_cash_allocation['2020']['financial activity']
    if '2018-01-02' in date_list:
        d1 = round(mpt_weight_dict['2018']['financial_product_return'], 3)
    else:
        d1=0
    if '2019-01-02' in date_list:
        d2 = round(mpt_weight_dict['2019']['financial_product_return'], 3)
    else:
        d2=0
    if '2020-01-02' in date_list:
        d3 = round(mpt_weight_dict['2020']['financial_product_return'], 3)
    else:
        d3=0
    if return_farmer_only:
        return farmer
    else:
        fig = plot_portfolio(farmer, date_list, res_path='res_html', title=f'approach_mpt_short', sub_title=f"approach 2018 ratio: {d1}, 2019 ratio: {d2}, 2020 ratio:{d3} with mpt (with short) method: {mpt_config['method']} | Financial Product: {change_koi_name(financial_product_selection)}", benchmark_farmer=benchmark_farmer)
    return fig

if __name__ == "__main__":
    universal_approach_3_years_mpt_short()
    a=1