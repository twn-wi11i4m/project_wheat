from farmer import Farmer
from util import *
from agriculture_products import Wheat, Canola
# from constant import *
from plot_wealth import *

def appraoch_1():
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

    plant_crop_date = '2018-04-10'
    harvest_date = '2018-10-13'
    sell_crop_date = '2018-11-03'

    wheat = Wheat(year='2018', risk_area=4)

    for adate in date_list:
        farmer.set_adate(adate)

        if adate == plant_crop_date:
            farmer.plant_crop(wheat)

        if adate == harvest_date:
            farmer.harvest()
            total_operational_cost = farmer.total_operational_cost
            total_fixed_cost = farmer.total_fixed_cost
            farmer.cash_paid('total operational cost', total_operational_cost)
            farmer.cash_paid('total fixed cost', total_fixed_cost)

        if adate == sell_crop_date:
            farmer.sell_crop(100)
            last_sell_crop_revenue = farmer.last_sell_crop_revenue
            farmer.cash_received('Revenue Crop', last_sell_crop_revenue)

    # plot_wealth(farmer, date_list, res_path='res_html', title='approach_1', sub_title='approach_1')
    save_wealth_csv(farmer, date_list, res_path='res_html', title='approach_1', sub_title='approach_1')
    plot_portfolio(farmer, date_list, res_path='res_html', title='approach_1', sub_title='approach_1')


    a=1
if __name__ == "__main__":
    appraoch_1()