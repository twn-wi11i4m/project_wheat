from approach_3 import approach_3
# from constant import EXPECTED_YIELD_LEVEL_LIST, COVER_LEVEL_LIST, INVESTMENT_AMOUNT_LIST
from constant import INVEST_CAPITAL_LIST
from itertools import product
import pandas as pd

# clear res_html first!!!

def main():
    expected_yield_level = 'Fallow'
    cover_level = 50
    farmer_initial_cash = 100_000
    for invest_capital in INVEST_CAPITAL_LIST:
        approach_3(invest_capital=invest_capital)

    res_dict = dict()
    for invest_capital in INVEST_CAPITAL_LIST:
        c = pd.read_csv(f'res_html/farmer_approach_3_{expected_yield_level}_{cover_level}_{invest_capital}_2018-01-01_2018-12-31_wealth.csv', index_col=0)
        ratio_invest_capital = invest_capital / farmer_initial_cash
        res_dict[ratio_invest_capital] = round(c.iloc[[0,-1]].pct_change().values[-1][0] * 100, 5)  #%
    
    wealth_return_df =pd.DataFrame.from_dict(res_dict, orient='index', columns=['return'])
    wealth_return_df.index.name = 'invest ratio of initial wealth'
    a=1


if __name__ == '__main__':
    main()