from approach_2 import approach_2
from constant import EXPECTED_YIELD_LEVEL_LIST, COVER_LEVEL_LIST
from itertools import product
import pandas as pd

# clear res_html first!!!

def main():
    # for (expected_yield_level, cover_level) in product(EXPECTED_YIELD_LEVEL_LIST, COVER_LEVEL_LIST):
    #     approach_2(expected_yield_level, cover_level)

    res_dict = dict()
    for expected_yield_level in EXPECTED_YIELD_LEVEL_LIST:
        res_dict[expected_yield_level] = dict()
        for cover_level in COVER_LEVEL_LIST:
            c = pd.read_csv(f'res_html/farmer_approach_2_{expected_yield_level}_{cover_level}_2018-01-01_2018-12-31_wealth.csv', index_col=0)
            r = c.iloc[[0,-1]].pct_change().values[-1][0]
            res_dict[expected_yield_level][cover_level] = r * 100   # %
    wealth_return_df = pd.DataFrame.from_dict(res_dict)
    wealth_return_df.index.name = 'Cover Level'
    a=1


if __name__ == '__main__':
    main()