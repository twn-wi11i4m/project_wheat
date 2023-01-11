import pandas as pd
import os
from constant import DATA_SOURCE_FOLDER_PATH

# https://economicdashboard.alberta.ca/GrainPrices
# all unit : $/metric tonne

class MarketData:
    def __init__(self) -> None:
        raw_df = pd.read_csv(
            os.path.join(DATA_SOURCE_FOLDER_PATH,'wheat_spot_price.csv'),
            index_col='When'
            )
        raw_df = raw_df[raw_df.Cal == 'Wheat excluding durum']
        raw_df.drop('Id',axis=1, inplace=True)
        raw_df.index = pd.to_datetime(raw_df.index)
        self.price_df = raw_df

    def get_price(self, adate, location='Alberta') -> float:
        last_price = self.price_df.loc[self.price_df.index <= adate].tail(1)[location].values[0]
        return last_price
    
    def get_price_df(self, adate, location='Alberta') -> pd.Series:
        price_series = self.price_df.loc[self.price_df.index <= adate][location]
        return price_series



class BaseRateData:
    def __init__(self) -> None:
        fi = pd.read_csv(
            os.path.join(DATA_SOURCE_FOLDER_PATH, 'baserate.csv')
        )
        self.fi = fi

    def get_risk_area(self, township:int, range:int, meridian:int):
        # farm_info = self.fi.values.tolist()
        # for i in farm_info: 
        #     if i[0] == township and i[1] == range and i[2] == meridian:
        #         self.risk_area = i[4] 
        #         break
        #based on passed in township, range, and meridian, and data from baserate.csv 
        df = self.fi
        res = df.loc[(df.township == township) & (df.range == range) & (df.meridian == meridian)]
        if len(res) != 0:
            self.risk_area = res.riskarea.values[0]
            return self.risk_area
        else:
            print('risk area not found!')
            return None

    def get_base_rate(self, township:int, range:int, meridian:int):
        # farm_info = self.fi.values.tolist()
        # for i in farm_info: 
        #     if i[0] == self.farm.township and i[1] == self.farm.range and i[2] == self.farm.meridian:
        #         base_rate = i[3]
        #         break
        df =  self.fi
        res = df.loc[(df.township == township) & (df.range == range) & (df.meridian == meridian)]
        if len(res) != 0:
            self.risk_area = res.baserate.values[0]
            return self.risk_area
        else:
            print('base rate not found!')
            return None


class YieldData:
    def __init__(self) -> None:
        cy = pd.read_csv(
            os.path.join(DATA_SOURCE_FOLDER_PATH, 'yield.csv')
        )
        self.cy = cy

    def get_yield_estimate(self, risk_area, crop, field):
        """
        field = ['fallow', 'stubble', 'irrigated']
        """
        df = self.cy
        res = df.loc[(df.riskarea == risk_area) & (df.crop == crop)]
        if len(res) == 0:
            print(f"Yield Data not found ({risk_area}, {crop})")
            return None
        # find yield if fallow, if stubble, if irrigated
        if field == 'fallow':
            return res.fallow.values[0]
        elif field == 'stubble':
            return res.stubble.values[0]
        elif field == 'irrigated':
            return res.irr.values[0]
        else:
            print(f"Field ({field}) not included in Yield Data")



class PremiumData:
    def __init__(self) -> None:
        p = pd.read_csv("DataSource/premium.csv")
        self.p = p
    
    #method retrieves the risk area crop premium as a percentage
    def get_crop_premium_percentage(self, risk_area, crop, field, coverage:int):
        """
        field = ['fallow', 'stubble', 'irrigated']
        """
        df = self.p

        res = df.loc[(df.riskarea == risk_area) & (df.crop == crop)]
        # find yield if fallow, if stubble, if irrigated
        if field == 'fallow':
            res = res.loc[res.field == 'F']
        elif field == 'stubble':
            res = res.loc[res.field == 'S']
        elif field == 'irrigated':
            res = res.loc[res.field == 'I']
        else:
            res = res
        # find coverage
        res = res.loc[res.coverage == coverage]
        percent_premium = round(res.premium.values[0] * 100, 2)
        return percent_premium



class YieldHistoricalData:
    def __init__(self) -> None:
        p = pd.read_csv(os.path.join(DATA_SOURCE_FOLDER_PATH, 'Yield Data - wheat yields.csv'), index_col='Year')
        p.index = pd.to_datetime(p.index.map(lambda x:f"{x}-12-31"))    # assume end of year
        p = p[['Yield']]
        self.p = p
    
    def get_yearly_yield_df(self, adate) -> pd.Series:
        p_s = self.p.loc[self.p.index <= adate]
        return p_s

