import pandas as pd
from constant import *
from data_source import MarketData, BaseRateData
from util import *

#Class for Farm
class Farm: 
    #initiate class with instance variables: 
    def __init__(self, township=1, range=1, meridian=5, farm_area=1) -> None:
        self.township = township #farm township 
        self.range = range #farm range 
        self.meridian = meridian #farm meridian 
        #based on passed in township, range, and meridian, and data from baserate.csv 
        self.risk_area = BaseRateData().get_risk_area(township=township, range=range, meridian=meridian) #farm risk area
        self.farm_area = farm_area

    #Method prints out all of the farm information
    def get_farm_information(self) -> None: 
        print("Farm Information: ")
        print(f"Farm Meridian, Township, Range: {self.meridian},{self.township},{self.range}")
        print(f"Farm Risk Area: {self.risk_area}")
        print(f"Farm Area: {self.farm_area}")
        print('')

# class Farmer:
#     def __init__(self, initial_cash=100_000, farm=Farm()) -> None:
#         self.initial_cash = initial_cash
#         # self.cash = self.initial_cash
#         self.farm_area = farm.farm_area
#         self.risk_area = farm.risk_area
#         self.crop = None
#         self.insurance = None
#         self.financial_products = dict()
#         self.financial_account = pd.DataFrame()
#         self.crop_inventory = 0
#         self.cash_transaction_list = []
#         # self.asset_transaction_list = []

#         self.last_sell_crop_revenue = 0
#         # self.cost unit: $/Acre
#         self.cost_detail = {
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
#         # self.operational_cost = None
#         # self.fixed_cost = None
    
#     def set_adate(self, date:str) -> None:
#         self.adate = date
#         self.year = self.adate.split('-')[0]
#         if self.year not in self.financial_products:
#             self.financial_products[self.year] = None
    
#     def apply_AgriInsurance(self, insurance:object) -> None:
#         self.insurance = insurance

#     def add_FinancialProduct(self, financial_product:object) -> None:
#         self.financial_products[self.year] = financial_product

#     def plant_crop(self, crop:object) -> None:
#         self.crop = crop

#     def sell_crop(self, pct_inventory:int) -> None:
#         """
#         Sell the crop in pct of inventory at spot price.
#         We only consider latest available spot price.
#         """
#         adate = self.adate
#         assert pct_inventory <= 100, f"only able to sell less than or equal to 100% of inventory!"
#         # price_df = MarketData().price_df
#         # last_available_price = price_df.loc[price_df.index <= adate].tail(1)['Alberta'].values[0]   # unit: $/metric tonne
#         last_available_price = MarketData().get_price(adate)
#         sell_amount_bushel = self.crop_inventory * (pct_inventory/100)
#         self.crop_inventory -= sell_amount_bushel
#         sell_amount_metric_tonne = bushel_to_metric_tonne(sell_amount_bushel)
#         revenue = last_available_price * sell_amount_metric_tonne
#         # self.cash += revenue
#         self.last_sell_crop_revenue = revenue
#         # return revenue


#     def harvest(self) -> None:
#         """
#         return the average yield (Bu/Acre)
#         """
#         y = self.crop.harvest()
#         total_yield = y * self.farm_area
#         self.crop_inventory += total_yield
#         return total_yield

#     def cash_paid(self, transaction_type, amount) -> None:
#         self.cash_transaction_list.append(
#             {
#                 'Date':self.adate,
#                 'cash flow': 'paid',
#                 'transaction type': transaction_type,
#                 'amount': amount
#             }
#         )

#     def cash_received(self, transaction_type, amount) -> None:
#         self.cash_transaction_list.append(
#             {
#                 'Date':self.adate,
#                 'cash flow': 'received',
#                 'transaction type': transaction_type,
#                 'amount': amount
#             }
#         )

#     # def asset_gain(self, transaction_type, amount) -> None:
#     #     self.asset_transaction_list.append(
#     #         {
#     #             'Date':self.adate,
#     #             'cash flow': 'gain',
#     #             'transaction type': transaction_type,
#     #             'amount': amount
#     #         }
#     #     )
       
#     # def asset_lose(self, transaction_type, amount) -> None:
#     #      self.asset_transaction_list.append(
#     #         {
#     #             'Date':self.adate,
#     #             'cash flow': 'lose',
#     #             'transaction type': transaction_type,
#     #             'amount': amount
#     #         }
#     #     )




#     @property
#     def cash(self) -> float:
#         transactions_list = list(map(lambda x: (-1 if x['cash flow'] == 'paid' else 1) * (x['amount']), self.cash_transaction_list))
#         cash_list = [self.initial_cash] + transactions_list
#         return sum(cash_list)

#     @property
#     def operational_cost(self) -> float:
#         return sum(list(map(lambda x: 0 if x is None else x, self.cost_detail['Operational Cost'].values())))

#     @property
#     def fixed_cost(self) -> float:
#         return sum(list(map(lambda x: 0 if x is None else x, self.cost_detail['Fixed Cost'].values())))

#     @property
#     def total_operational_cost(self) -> float:
#         return self.farm_area * self.operational_cost
    
#     @property
#     def total_fixed_cost(self) -> float:
#         return self.farm_area * self.fixed_cost

#     @property
#     def total_cost(self) -> float:
#         return self.total_fixed_cost + self.total_operational_cost










class Farmer_v2:
    def __init__(self, initial_cash=100_000, farm=Farm()) -> None:
        self.initial_cash = initial_cash
        # self.cash = self.initial_cash
        self.farm_area = farm.farm_area
        self.risk_area = farm.risk_area
        self.crop = None
        self.insurance = None
        self.financial_products = dict()
        self.financial_account = pd.DataFrame()
        self.crop_inventory = 0
        self.cash_transaction_list = []
        # self.asset_transaction_list = []

        self.last_sell_crop_revenue = 0
        # self.cost unit: $/Acre
        # self.cost_detail = {
        #     'Operational Cost': {
        #         'Seed Treatment':34,
        #         'Fertilizer':180.26,
        #         'Pesticide':55.33,
        #         'Fuel':46.75,
        #         'Machinery_Operation_Lease':25,
        #         'Labour Hired':5.2,
        #         'Drying Other Costs':17.75,
        #         'Insurance Premium': None,
        #         'Land Taxes':17.5,
        #         'Storage Costs':18.19,
        #         'Interest On Operation':16.42,
        #     },
        #     'Fixed Cost': {
        #         'Land Costs': 97.17,
        #         'Machinery Costs': 86.37
        #     }
        # }
        self.cost_detail = {
            'Variable_Cost': None,
            'Fixed_Cost': None
        }
        # self.operational_cost = None
        # self.fixed_cost = None
    
    def set_adate(self, date:str) -> None:
        self.adate = date
        self.year = self.adate.split('-')[0]
        if self.year not in self.financial_products:
            self.financial_products[self.year] = None
    
    def apply_AgriInsurance(self, insurance:object) -> None:
        self.insurance = insurance

    def add_FinancialProduct(self, financial_product:object) -> None:
        self.financial_products[self.year] = financial_product

    def plant_crop(self, crop:object) -> None:
        self.crop = crop

    def sell_crop(self, pct_inventory:int) -> None:
        """
        Sell the crop in pct of inventory at spot price.
        We only consider latest available spot price.
        """
        adate = self.adate
        assert pct_inventory <= 100, f"only able to sell less than or equal to 100% of inventory!"
        # price_df = MarketData().price_df
        # last_available_price = price_df.loc[price_df.index <= adate].tail(1)['Alberta'].values[0]   # unit: $/metric tonne
        last_available_price = MarketData().get_price(adate)
        sell_amount_bushel = self.crop_inventory * (pct_inventory/100)
        self.crop_inventory -= sell_amount_bushel
        sell_amount_metric_tonne = bushel_to_metric_tonne(sell_amount_bushel)
        revenue = last_available_price * sell_amount_metric_tonne
        # self.cash += revenue
        self.last_sell_crop_revenue = revenue
        # return revenue


    def harvest(self) -> None:
        """
        return the average yield (Bu/Acre)
        """
        y = self.crop.harvest()
        total_yield = y * self.farm_area
        self.crop_inventory += total_yield
        return total_yield

    def cash_paid(self, transaction_type, amount) -> None:
        self.cash_transaction_list.append(
            {
                'Date':self.adate,
                'cash flow': 'paid',
                'transaction type': transaction_type,
                'amount': amount
            }
        )

    def cash_received(self, transaction_type, amount) -> None:
        self.cash_transaction_list.append(
            {
                'Date':self.adate,
                'cash flow': 'received',
                'transaction type': transaction_type,
                'amount': amount
            }
        )

    # def asset_gain(self, transaction_type, amount) -> None:
    #     self.asset_transaction_list.append(
    #         {
    #             'Date':self.adate,
    #             'cash flow': 'gain',
    #             'transaction type': transaction_type,
    #             'amount': amount
    #         }
    #     )
       
    # def asset_lose(self, transaction_type, amount) -> None:
    #      self.asset_transaction_list.append(
    #         {
    #             'Date':self.adate,
    #             'cash flow': 'lose',
    #             'transaction type': transaction_type,
    #             'amount': amount
    #         }
    #     )

    @property
    def cash(self) -> float:
        transactions_list = list(map(lambda x: (-1 if x['cash flow'] == 'paid' else 1) * (x['amount']), self.cash_transaction_list))
        cash_list = [self.initial_cash] + transactions_list
        return sum(cash_list)

    @property
    def variable_cost(self) -> float:
        return sum(list(map(lambda x: 0 if x is None else x, self.cost_detail['Variable_Cost'].values())))

    @property
    def fixed_cost(self) -> float:
        return sum(list(map(lambda x: 0 if x is None else x, self.cost_detail['Fixed_Cost'].values())))

    @property
    def total_variable_cost(self) -> float:
        return self.farm_area * self.variable_cost
    
    @property
    def total_fixed_cost(self) -> float:
        return self.farm_area * self.fixed_cost

    @property
    def total_cost(self) -> float:
        return self.total_fixed_cost + self.total_operational_cost

