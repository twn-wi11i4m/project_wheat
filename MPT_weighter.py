from KOICommonTools.Common.ConstantsGeneral import KOI_DATE_FORMAT_YMD
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from data_source import MarketData
from financial_product import FinancialProduct
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from util import get_datelist



class MPT_Weighter:
    def __init__(self, lookback_days, previous_market_data:object, previous_financial_product:object, is_short=False) -> None:
        # self.spot_price_data = market_data
        # self.financial_product_data = financial_product.account_tradelog
        self.previous_market_data = previous_market_data
        self.previous_financial_product = previous_financial_product
        self.lookback_days = lookback_days
        self.is_short = is_short
        # self.method = method
        pass

    def _get_raw_data(self, last_lb_date) -> pd.DataFrame:
        end_date = last_lb_date
        start_date = datetime.strftime(datetime.strptime(last_lb_date, KOI_DATE_FORMAT_YMD) - relativedelta(days=self.lookback_days), KOI_DATE_FORMAT_YMD)
        # date_list = get_datelist(start_date, end_date)
        raw_market_df = self.previous_market_data.get_price_df(end_date)
        raw_market_df = raw_market_df.loc[(raw_market_df.index >= start_date) & (raw_market_df.index <= end_date)]
        raw_financial_df = self.previous_financial_product.account_tradelog['as_of_date_balance']
        raw_financial_df = raw_financial_df.loc[(raw_financial_df.index >= start_date) & (raw_financial_df.index <= end_date)]
        raw_market_df.index = pd.to_datetime(raw_market_df.index)
        raw_financial_df.index = pd.to_datetime(raw_financial_df.index)
        self.raw_df = pd.concat([raw_financial_df, raw_market_df], axis=1)
        self.raw_df.ffill(inplace=True)
        self.raw_df.bfill(inplace=True)
        self.raw_df.rename(columns = {'as_of_date_balance':'financial_product_return', 'Alberta':'spot_price_return'}, inplace=True)


    def _get_return_and_covariance(self, last_lb_date) :
        self._get_raw_data(last_lb_date)
        self.mu = expected_returns.mean_historical_return(self.raw_df)
        self.S = risk_models.sample_cov(self.raw_df)
        a=1

    def get_weight(self, last_lb_date, method='min_volatility'):
        self._get_return_and_covariance(last_lb_date)
        if self.is_short:
            self.ef = EfficientFrontier(self.mu, self.S, weight_bounds=(-1, 1))
        else:
            self.ef = EfficientFrontier(self.mu, self.S, weight_bounds=(0, 1))
        if method == 'max_sharpe':
            self.weight = self.ef.max_sharpe()
        elif method == 'min_volatility':
            self.weight = self.ef.min_volatility()
        elif method == 'max_quadratic_utility':
            self.weight = self.ef.max_quadratic_utility()

        return self.weight



if __name__ == '__main__':
    market_data = MarketData()
    financial_product = FinancialProduct(invest_capital=100_000, initial_date='2017-01-01',final_payoff_date='2017-11-23')
    mpt_weight = MPT_Weighter(lookback_days=183, previous_market_data=market_data, previous_financial_product=financial_product)
    a = mpt_weight.get_weight(last_lb_date='2018-01-02')
    b=1