from KOICommonTools.Common.ConstantsGeneral import KOI_DATE_FORMAT_YMD
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from data_source import MarketData
from financial_product import FinancialProduct
from insurance import AgriInsurance
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from util import get_datelist
from farmer import Farmer_v2, Farm
from data_source import YieldHistoricalData
import copy



class MPT_Weighter_v2:
    def __init__(self, lookback_days, previous_market_data:object, previous_financial_product:object, previous_insurance_product:object, is_short=False) -> None:
        # self.spot_price_data = market_data
        # self.financial_product_data = financial_product.account_tradelog
        self.previous_market_data = previous_market_data
        self.previous_financial_product = previous_financial_product
        self.previous_insurance_product = previous_insurance_product
        self.lookback_days = lookback_days
        self.is_short = is_short
        self.default_df_columns = ['financial_product_return', 'spot_price_return', 'insurance_return']
        # self.method = method
        
        # # Albert's idea
        # self.weight_bdd = {
        #     'financial_product_return': {'max':0.1, 'min':0.0},   # 0
        #     'spot_price_return': {'max':1, 'min':0.9},            # 1
        #     'insurance_return': {'max':0.1, 'min':0.0},           # 2
        # }

        # # My idea
        # self.weight_bdd = {
        #     'financial_product_return': {'max':0.6, 'min':0.0},     # 0
        #     'spot_price_return': {'max':1, 'min':0.2},              # 1
        #     'insurance_return': {'max':0.2, 'min':0.1},             # 2
        # }

        # default weight bound
        self.default_weight_bdd = {
            'financial_product_return': {'max':0.1, 'min':0.0},   # 0
            'spot_price_return': {'max':1, 'min':0.9},            # 1
            'insurance_return': {'max':0.1, 'min':0.0},           # 2
        }

        self.insurance_lookback_years = 6
        self.historical_yield_data = YieldHistoricalData()

        pass

    def _get_raw_data(self, last_lb_date, output_columns=['financial_product_return', 'spot_price_return']) -> pd.DataFrame:
        """
        The raw_df is price dataframe
        if output_columns = ['financial_product_return', 'spot_price_return'],  then the dataframe lookback length will be 'self.lookback_days' in daily interval.
        if output_columns = ['financial_product_return', 'spot_price_return', 'insurance_return'],which include 'insurance_return', then the dataframe lookback length will be 'insurance_lookback_years' in annually interval.
        """
        end_date = last_lb_date
        if output_columns == ['financial_product_return', 'spot_price_return']:
            start_date = datetime.strftime(datetime.strptime(last_lb_date, KOI_DATE_FORMAT_YMD) - relativedelta(days=self.lookback_days), KOI_DATE_FORMAT_YMD)
            date_list = get_datelist(start_date, end_date)
            raw_market_df = self.previous_market_data.get_price_df(end_date)
            raw_market_df = raw_market_df.loc[(raw_market_df.index >= start_date) & (raw_market_df.index <= end_date)]
            
            # hard code hear
            sy = str(int(last_lb_date.split('-')[0])-1)
            a_11 = self.previous_financial_product.final_payoff_date[4:]
            a_12 = self.previous_financial_product.initial_date[4:]
            self.previous_financial_product.final_payoff_date = f"{sy}{a_11}"
            self.previous_financial_product.initial_date = f"{sy}{a_12}"

            raw_financial_df = self.previous_financial_product.account_tradelog['as_of_date_balance']
            raw_financial_df = raw_financial_df.loc[(raw_financial_df.index >= start_date) & (raw_financial_df.index <= end_date)]
            raw_market_df.index = pd.to_datetime(raw_market_df.index)
            raw_financial_df.index = pd.to_datetime(raw_financial_df.index)
            self.raw_df = pd.concat([raw_financial_df, raw_market_df], axis=1)
            self.raw_df.ffill(inplace=True)
            self.raw_df.bfill(inplace=True)
            self.raw_df.rename(columns = {'as_of_date_balance':'financial_product_return', 'Alberta':'spot_price_return'}, inplace=True)
            a=1
        elif output_columns == ['financial_product_return', 'spot_price_return', 'insurance_return']:
            # lookback 6 years
            start_date = datetime.strftime(datetime.strptime(last_lb_date, KOI_DATE_FORMAT_YMD) - relativedelta(years=self.insurance_lookback_years), KOI_DATE_FORMAT_YMD)
            # date_list = get_datelist(start_date, end_date)

            #historical yield
            raw_historical_yield_df = self.historical_yield_data.get_yearly_yield_df(end_date)
            raw_historical_yield_df = raw_historical_yield_df.loc[(raw_historical_yield_df.index >= start_date) & (raw_historical_yield_df.index <= end_date)]

            # insurance return from historical yield
            raw_insurance_df = raw_historical_yield_df.applymap(lambda x:self.previous_insurance_product.calc_indemnity(x))
            raw_insurance_df += 1

            # market data
            raw_market_df_ii = self.previous_market_data.get_price_df(end_date)
            raw_market_df_ii = raw_market_df_ii.loc[(raw_market_df_ii.index >= start_date) & (raw_market_df_ii.index <= end_date)]
            raw_market_df_ii.index = pd.to_datetime(raw_market_df_ii.index)
            # annualized average
            raw_market_df_ii = raw_market_df_ii.groupby(raw_market_df_ii.index.year).mean()
            raw_market_df_ii.index = raw_market_df_ii.index.map(lambda x:f"{x}-12-31")
            raw_market_df_ii.index = pd.to_datetime(raw_market_df_ii.index)
            raw_market_df_ii = raw_market_df_ii.loc[raw_market_df_ii.index <= end_date]

            # financial data
            sdi, edi = self.previous_financial_product.initial_date, self.previous_financial_product.final_payoff_date
            raw_financial_df_past_1 = copy.deepcopy(self.previous_financial_product)
            raw_financial_df_past_2 = copy.deepcopy(self.previous_financial_product)
            raw_financial_df_past_3 = copy.deepcopy(self.previous_financial_product)
            raw_financial_df_past_4 = copy.deepcopy(self.previous_financial_product)
            raw_financial_df_past_5 = copy.deepcopy(self.previous_financial_product)

            raw_financial_df_past_1.initial_date = f"{int(sdi.split('-')[0])-1}-{sdi.split('-')[1]}-{sdi.split('-')[2]}"
            raw_financial_df_past_2.initial_date = f"{int(sdi.split('-')[0])-2}-{sdi.split('-')[1]}-{sdi.split('-')[2]}"
            raw_financial_df_past_3.initial_date = f"{int(sdi.split('-')[0])-3}-{sdi.split('-')[1]}-{sdi.split('-')[2]}"
            raw_financial_df_past_4.initial_date = f"{int(sdi.split('-')[0])-4}-{sdi.split('-')[1]}-{sdi.split('-')[2]}"
            raw_financial_df_past_5.initial_date = f"{int(sdi.split('-')[0])-5}-{sdi.split('-')[1]}-{sdi.split('-')[2]}"

            raw_financial_df_past_1.final_payoff_date = f"{int(edi.split('-')[0])-1}-{edi.split('-')[1]}-{edi.split('-')[2]}"
            raw_financial_df_past_2.final_payoff_date = f"{int(edi.split('-')[0])-2}-{edi.split('-')[1]}-{edi.split('-')[2]}"
            raw_financial_df_past_3.final_payoff_date = f"{int(edi.split('-')[0])-3}-{edi.split('-')[1]}-{edi.split('-')[2]}"
            raw_financial_df_past_4.final_payoff_date = f"{int(edi.split('-')[0])-4}-{edi.split('-')[1]}-{edi.split('-')[2]}"
            raw_financial_df_past_5.final_payoff_date = f"{int(edi.split('-')[0])-5}-{edi.split('-')[1]}-{edi.split('-')[2]}"

            raw_financial_df_ii = self.previous_financial_product.account_tradelog['as_of_date_balance']
            raw_financial_df_ii = raw_financial_df_ii.loc[(raw_financial_df_ii.index >= start_date) & (raw_financial_df_ii.index <= end_date)]
            # annualized

            raw_financial_df_ii_past_1 = raw_financial_df_past_1.account_tradelog['as_of_date_balance']
            raw_financial_df_ii_past_2 = raw_financial_df_past_2.account_tradelog['as_of_date_balance']
            raw_financial_df_ii_past_3 = raw_financial_df_past_3.account_tradelog['as_of_date_balance']
            raw_financial_df_ii_past_4 = raw_financial_df_past_4.account_tradelog['as_of_date_balance']
            raw_financial_df_ii_past_5 = raw_financial_df_past_5.account_tradelog['as_of_date_balance']
      
            raw_financial_df_ii.index = pd.to_datetime(raw_financial_df_ii.index)
            
            raw_financial_df_ii_past_1.index = pd.to_datetime(raw_financial_df_ii_past_1.index)
            raw_financial_df_ii_past_2.index = pd.to_datetime(raw_financial_df_ii_past_2.index)
            raw_financial_df_ii_past_3.index = pd.to_datetime(raw_financial_df_ii_past_3.index)
            raw_financial_df_ii_past_4.index = pd.to_datetime(raw_financial_df_ii_past_4.index)
            raw_financial_df_ii_past_5.index = pd.to_datetime(raw_financial_df_ii_past_5.index)

            # concat into one dataframe
            raw_financial_df = pd.concat(
                [raw_financial_df_ii_past_5, raw_financial_df_ii_past_4, raw_financial_df_ii_past_3, raw_financial_df_ii_past_2, raw_financial_df_ii_past_1, raw_financial_df_ii],
                axis=0
            )
            raw_financial_df = raw_financial_df.groupby(raw_financial_df.index.year).mean()
            raw_financial_df.index = raw_financial_df.index.map(lambda x:f"{x}-12-31")
            raw_financial_df.index = pd.to_datetime(raw_financial_df.index)

            self.raw_df_ii = pd.concat([raw_financial_df, raw_market_df_ii, raw_insurance_df], axis=1)
            self.raw_df_ii.ffill(inplace=True)
            self.raw_df_ii.bfill(inplace=True)
            self.raw_df_ii.rename(columns = {'as_of_date_balance':'financial_product_return', 'Alberta':'spot_price_return', 'Yield':'insurance_return'}, inplace=True)
            a=1
        else:
            print(f"Wrong config: output_columns={output_columns}")

    # def _get_insurance_return(self) -> float:
    #     indemnity = self.previous_insurance_product.calc_indemnity(self.previous_yield)
    #     total_paid_premium = self.previous_insurance_product.get_total_crop_premium()
    #     r = max(((indemnity - total_paid_premium)/total_paid_premium), 0)
    #     return r

    # def _get_insurance_var(self) -> float:
    #     # assume the insurance same as spot price variance
    #     v_df = risk_models.sample_cov(self.raw_df)
    #     v = v_df.loc['spot_price_return', 'spot_price_return']
    #     return v
    
    # def _add_insurnace_var_into_S(self, insurance_var) -> pd.DataFrame:
    #     i = 'insurance_return'
    #     self.S[i] = [0, 0]
    #     self.S.loc[i] = [0, 0, insurance_var]

    def _get_return_and_covariance(self, last_lb_date) :
        self._get_raw_data(last_lb_date,  output_columns=['financial_product_return', 'spot_price_return'])
        self.mu = expected_returns.mean_historical_return(self.raw_df)
        # insurance_r = self._get_insurance_return()
        # self.mu['insurance_return'] = insurance_r
        # insurance_var = self._get_insurance_var()
        self.S = risk_models.sample_cov(self.raw_df)
        
        self._get_raw_data(last_lb_date,  output_columns=['financial_product_return', 'spot_price_return', 'insurance_return'])
        self.mu_ii = expected_returns.mean_historical_return(self.raw_df_ii)
        self.S_ii = risk_models.sample_cov(self.raw_df_ii)

        # apply self.mu_ii into self.mu
        self.mu['insurance_return'] = self.mu_ii['insurance_return']

        # apply self.S_ii into self.S
        self.S['insurance_return'] = self.S_ii['insurance_return']
        self.S.loc['insurance_return'] = self.S_ii['insurance_return']
        

    def get_weight(self, last_lb_date, previous_yield, method='min_volatility', weight_bdd=None):
        self.previous_yield = previous_yield
        self._get_return_and_covariance(last_lb_date)
        if self.is_short:
            self.ef = EfficientFrontier(self.mu, self.S, weight_bounds=(-1, 1))
        else:
            self.ef = EfficientFrontier(self.mu, self.S, weight_bounds=(0, 1))

        if weight_bdd is None:
            print('weight bound is not specify. Use default weight bound')
            weight_bdd = self.default_weight_bdd
        # add weight_bdd if exist
        try:
            self.ef.add_constraint(lambda x : x[0] >= weight_bdd['financial_product_return']['min'])
            self.ef.add_constraint(lambda x : x[0] <= weight_bdd['financial_product_return']['max'])
            self.ef.add_constraint(lambda x : x[1] >= weight_bdd['spot_price_return']['min'])
            self.ef.add_constraint(lambda x : x[1] <= weight_bdd['spot_price_return']['max'])
            self.ef.add_constraint(lambda x : x[2] >= weight_bdd['insurance_return']['min'])
            self.ef.add_constraint(lambda x : x[2] <= weight_bdd['insurance_return']['max'])
            print(f"constraint added: {weight_bdd}")
        except:
            print(f"No constraints are added")
            pass
        a=1
        if method == 'max_sharpe':
            self.ef.max_sharpe()
        elif method == 'min_volatility':
            self.ef.min_volatility()
        elif method == 'max_quadratic_utility':
            self.ef.max_quadratic_utility()
        # cutoff=0.0001, rounding=5
        return self.ef.clean_weights()



if __name__ == '__main__':
    market_data = MarketData()
    farm = Farm(township=7, range=21, meridian=4, farm_area=1)
    farmer = Farmer_v2(initial_cash=100_000, farm=farm)
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
    financial_product = FinancialProduct(invest_capital=100_000, initial_date='2017-01-01',final_payoff_date='2017-11-23', selected_product='Chagoi')
    insurance_product = AgriInsurance(farm=farm, insured_acres=farm.farm_area, crop='HRS', field='stubble', coverage=50, include_hail_endorsement=True)
    mpt_weight = MPT_Weighter_v2(
        lookback_days=360, 
        previous_market_data=market_data, 
        previous_financial_product=financial_product,
        previous_insurance_product=insurance_product)
    # a = mpt_weight.get_weight(last_lb_date='2018-01-02', previous_yield=24)   # no insurance return 
    a = mpt_weight.get_weight(last_lb_date='2018-01-02', previous_yield=19.8)     # some insurance return 
    b=1