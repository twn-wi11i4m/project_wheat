from farmer import Farmer, Farm
from util import *
from constant import *
from agriculture_products import WheatYears, Canola
# from constant import *
from insurance import AgriInsurance
from financial_product import FinancialProduct
from plot_wealth import *

def universal_approach_3_years(initial_cash_allocation=INITIAL_CASH_ALLOCATION):
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
    
    date_list = get_datelist('2018-01-01', '2020-12-31')

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
    

    for adate in date_list:
        year = adate.split('-')[0]
        farmer.set_adate(adate)
        invest_capital = initial_cash_allocation[year]['financial activity'] * farmer.cash
        wheat_years.set_year(year)

        if adate == important_dates_dict[year]['purchase_financial_product_date']:
            invest_capital = invest_capital
            farmer.add_FinancialProduct(
                FinancialProduct(
                    invest_capital=invest_capital, 
                    initial_date=important_dates_dict[year]['purchase_financial_product_date'],
                    final_payoff_date=important_dates_dict[year]['end_financial_product_date']
                )
            )
            farmer.cash_paid('invested capital', invest_capital)

        if adate == important_dates_dict[year]['payoff_financial_product_date'] and farmer.financial_products[year] is not None:
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
    save_wealth_csv(farmer, date_list, res_path='res_html', title=f'approach_2', sub_title='approach_2')

    fig = plot_portfolio(farmer, date_list, res_path='res_html', title=f'approach_2', sub_title=f"approach_2")
    return fig

if __name__ == "__main__":
    universal_approach_3_years()
    a=1