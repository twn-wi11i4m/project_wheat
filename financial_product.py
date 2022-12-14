import pandas as pd
import numpy as np
from util import get_datelist
from KOICommonTools.GetDataClient import get_price

def KOI_trading(start_date, end_date, tickers='RSC2 COMDTY'):
    data = get_price(tickers, 'DAILY', '2017-01-01', use_df=True)[tickers]['NONE']
    enter_date = data[data.index >= start_date].index[0]
    exit_date = data[data.index >= end_date].index[0]
    enter_type = 'MKT'

    day_1_return = (data.loc[enter_date].PX_LAST - data.loc[enter_date].PX_OPEN)/data.loc[enter_date].PX_OPEN
    r_df = data.pct_change().loc[(data.index >= enter_date) & (data.index <= exit_date)].PX_LAST
    r_df.loc[enter_date] = day_1_return
    r_df.name = 'daily_return'
    return r_df

class FinancialProduct:
    """
    Assume we only trade RSC2 COMDTY
    """
    def __init__(self, invest_capital, initial_date, final_payoff_date) -> None:
        self.invest_capital = invest_capital
        self.initial_date = initial_date
        self.final_payoff_date = final_payoff_date

    def final_return_dollar(self) -> float:
        """
        assume there is some return, i.e., 5% of invest capital
        The dollar is including the management fee and other operational cost in KOI
        """
        # return max(self.invest_capital * (1 + 0.05), 0)
        return max(self.account_tradelog.as_of_date_balance.iloc[-1], 0)

    def _get_daily_return(self, date_list:list) -> pd.Series:
        np.random.seed(42)
        daily_return =  KOI_trading(self.initial_date, self.final_payoff_date)
        df = pd.DataFrame(index=date_list)
        df = df.join(daily_return)
        df.fillna(0, inplace=True)
        return df.daily_return
 

    @property
    def account_tradelog(self) -> pd.DataFrame:
        date_list = get_datelist(self.initial_date, self.final_payoff_date)
        tradelog = pd.DataFrame(
            index=date_list
        )
        tradelog['initial_capital'] = self.invest_capital
        tradelog['daily_return'] = self._get_daily_return(date_list)
        tradelog['total_return'] = tradelog['daily_return'].cumsum()
        tradelog['as_of_date_balance'] = tradelog['initial_capital'] * (1 + tradelog['total_return'])
        return tradelog



if __name__ == '__main__':
    KOI_trading('2018-03-04', '2018-04-05')
    financial_product = FinancialProduct(100, '2020-01-01', '2020-05-04')
    financial_product.account_tradelog

