import pandas as pd

# https://economicdashboard.alberta.ca/GrainPrices
# all unit : $/metric tonne

class MarketData:
    def __init__(self) -> None:
        raw_df = pd.read_csv('wheat_spot_price.csv', index_col='When')
        raw_df = raw_df[raw_df.Cal == 'Wheat excluding durum']
        raw_df.drop('Id',axis=1, inplace=True)
        raw_df.index = pd.to_datetime(raw_df.index)
        self.price_df = raw_df

    def get_price(self, adate, location='Alberta') -> float:
        last_price = self.price_df.loc[self.price_df.index <= adate].tail(1)[location].values[0]
        return last_price



