from farmer import Farmer
from util import *
from agriculture_products import Wheat, Canola
# from constant import *
from insurance import AgriInsuranc
from financial_product import FinancialProduct
from plot_wealth import *

def approach_3(expected_yield_level='Fallow', cover_level=50, invest_capital=50_000):
    farmer = Farmer(initial_cash=100_000, farm_area=1, risk_area=4)
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

    date_list = get_datelist('2018-01-01', '2018-12-31')

    apply_agrinsurance_date = '2018-04-01'
    agriinsuranc_indemnity_payment_date = '2018-11-05'

    purchase_financial_product_date = '2018-04-01'
    payoff_financial_product_date = '2018-10-31'

    plant_crop_date = '2018-04-10'
    harvest_date = '2018-10-13'
    sell_crop_date = '2018-11-03'

    wheat = Wheat(year='2018', risk_area=4)

    for adate in date_list:
        farmer.set_adate(adate)

        if adate == purchase_financial_product_date:
            invest_capital = invest_capital
            farmer.financial_product = FinancialProduct(invest_capital=invest_capital, initial_date=purchase_financial_product_date,final_payoff_date=payoff_financial_product_date)
            farmer.cash_paid('invested capital', invest_capital)

        if adate == payoff_financial_product_date and farmer.financial_product is not None:
            payoff = farmer.financial_product.final_return_dollar()
            if payoff != 0:
                farmer.cash_received('revenue financial product', payoff)


        if adate == apply_agrinsurance_date:
            farmer.insurance = AgriInsuranc(expected_yield_level=expected_yield_level, cover_level=cover_level, risk_area=farmer.risk_area)
        
        if farmer.insurance is not None and adate <= agriinsuranc_indemnity_payment_date:
            if farmer.insurance.premium_pay_date(adate):
                monthly_premium = farmer.insurance.monthly_premium
                farmer.cash_paid('insurance premium', monthly_premium)


        if adate == plant_crop_date:
            farmer.plant_crop(wheat)

        if adate == harvest_date:
            total_yield = farmer.harvest()
            total_operational_cost = farmer.total_operational_cost
            total_fixed_cost = farmer.total_fixed_cost
            farmer.cash_paid('total operational cost', total_operational_cost)
            farmer.cash_paid('total fixed cost', total_fixed_cost)

        if adate == agriinsuranc_indemnity_payment_date:
            revenue_insurance = farmer.insurance.indemnity_payment(total_yield)
            if revenue_insurance != 0:
                farmer.cash_received('Revenue Insurance', revenue_insurance)

        if adate == sell_crop_date:
            farmer.sell_crop(100)
            last_sell_crop_revenue = farmer.last_sell_crop_revenue
            farmer.cash_received('Revenue Crop', last_sell_crop_revenue)



    plot_wealth(farmer, date_list, res_path='res_html', title=f'approach_3_{invest_capital}', sub_title='approach_3')
    
    save_wealth_csv(farmer, date_list, res_path='res_html', title=f'approach_3_{expected_yield_level}_{cover_level}_{invest_capital}', sub_title='approach_3')
    # plot_portfolio(farmer, date_list, res_path='res_html', title='approach_3', sub_title='approach_3')


    a=1
if __name__ == '__main__':
    approach_3()