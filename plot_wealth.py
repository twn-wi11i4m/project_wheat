import pyecharts.options as opts
from pyecharts.charts import Line
# from pyecharts import Overlap
import pandas as pd
import numpy as np
import os
from market_price import MarketData

def initial_wealth_df(farmer, date_list:list) -> pd.DataFrame:
    wealth_df = pd.DataFrame(index=date_list)
    wealth_df['farmer'] = farmer.initial_cash
    return wealth_df

def add_transaction_in_wealth_df(wealth_df:pd.DataFrame, transaction_list) -> pd.DataFrame:
    # a=1
    for transaction in transaction_list:
        transaction_date = transaction['Date']
        transaction_cash_flow = transaction['cash flow']
        # transaction_type = transaction['transaction type']
        transaction_amount = transaction['amount']
        wealth_chg = (-1 if transaction_cash_flow == 'paid' else 1) * transaction_amount
        # a=1
        wealth_df.loc[wealth_df.index >= transaction_date] += wealth_chg
        
    return wealth_df

def save_wealth_csv(farmer, date_list:list, res_path:str, title:str, sub_title:str):
    transaction_list = farmer.transaction_list
    wealth_df = initial_wealth_df(farmer, date_list)
    wealth_df = add_transaction_in_wealth_df(wealth_df, transaction_list)
    wealth_df.to_csv(os.path.join(res_path, f'farmer_{title}_{date_list[0]}_{date_list[-1]}_wealth.csv'))

def plot_wealth(farmer, date_list:list, res_path:str, title:str, sub_title:str):
    transaction_list = farmer.transaction_list
    wealth_df = initial_wealth_df(farmer, date_list)
    wealth_df = add_transaction_in_wealth_df(wealth_df, transaction_list)
    # month_list = wealth_df.index.to_list()
    wealth = np.round(wealth_df['farmer'].to_numpy(), 3)

    line = Line(init_opts=opts.InitOpts(width="1200px", height="500px", page_title=title))
    line.add_xaxis(xaxis_data=date_list)
    line.add_yaxis(
            series_name="Farmer Wealth ($)",
            y_axis=wealth,
            color='blue',
        )
    # line.add_yaxis(
    #         series_name="Alberta Wheat spot price",
    #         y_axis=benchmark,
    #         color='grey',
    #     )

    # color setting
    # line.colors[0], line.colors[1] =line.colors[1], line.colors[0]

    line.set_series_opts(
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
    line.set_global_opts(
            title_opts=opts.TitleOpts(title="Farmer Risk Management & Wealth Portfolio", subtitle=sub_title),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=opts.SplitAreaOpts(is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)),
            ),
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=True,
                    type_= "slider",
                    range_start=0,
                    range_end=400,
                ),
            ]
        )

    # line.render(os.path.join(FOLDER_PATH, f"{year}_approach_1.html"))
    line.render(os.path.join(res_path, f'farmer_{title}_{date_list[0]}_{date_list[-1]}_wealth.html'))

def plot_portfolio(farmer, date_list:list, res_path:str, title:str, sub_title:str) -> None:
    transaction_list = farmer.transaction_list
    wealth_df = initial_wealth_df(farmer, date_list)
    wealth_df = add_transaction_in_wealth_df(wealth_df, transaction_list)
    start_date, end_date = date_list[0], date_list[-1]
    whole_price_df = MarketData().price_df
    price_df = whole_price_df.loc[(whole_price_df.index >= start_date) & (whole_price_df.index <= end_date)]
    price_df.index.name = None

    portfolio_df = wealth_df.copy()
    portfolio_df['Alberta spot price'] = price_df['Alberta']
    portfolio_df.ffill(inplace=True)

    # portfolio_df['Alberta spot price return'] =  (portfolio_df['Alberta spot price'].pct_change() +1).cumprod()
    # portfolio_df['Alberta spot price return'][0] = 1

    benchmark = np.round(portfolio_df['Alberta spot price'].to_numpy(),3)
    wealth = np.round(portfolio_df['farmer'].to_numpy(), 3)

    line = Line(init_opts=opts.InitOpts(width="1200px", height="500px", page_title=title))
    line.add_xaxis(xaxis_data=date_list)
    line.add_yaxis(
            series_name="Farmer Wealth ($)",
            y_axis=wealth,
            color='blue',
        )
    line.add_yaxis(
            series_name="Benchmark ($)",
            y_axis=benchmark,
            color='grey',
        )

    line.colors[0], line.colors[1] =line.colors[1], line.colors[0]

    line.set_series_opts(
            # areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=False),
        )
    line.set_global_opts(
            title_opts=opts.TitleOpts(title="Farmer Risk Management & Wealth Portfolio", subtitle=sub_title),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            toolbox_opts=opts.ToolboxOpts(is_show=True),
            xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
            yaxis_opts=opts.AxisOpts(
                is_scale=True,
                splitarea_opts=
                    opts.SplitAreaOpts(
                        is_show=True, 
                        areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    )
            ),
            # legend_opts=[opts.LegendOpts(pos_right='right', pos_top='20%', pos_bottom='50%')]
            datazoom_opts=[
                opts.DataZoomOpts(
                    is_show=True,
                    type_= "slider",
                    range_start=0,
                    range_end=400,
                ),
            ]
        )
    line.render(os.path.join(res_path, f'farmer_{title}_{date_list[0]}_{date_list[-1]}_portfolio.html'))