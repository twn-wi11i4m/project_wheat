
import pandas as pd
import numpy as np
import os
from data_source import MarketData
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def initial_wealth_df(farmer, date_list:list) -> pd.DataFrame:
    wealth_df = pd.DataFrame(index=date_list)
    wealth_df['farmer_cash'] = farmer.initial_cash
    return wealth_df

def add_transaction_in_wealth_df(wealth_df:pd.DataFrame, cash_transaction_list) -> pd.DataFrame:
    # a=1
    for cash_transaction in cash_transaction_list:
        cash_transaction_date = cash_transaction['Date']
        transaction_cash_flow = cash_transaction['cash flow']
        # transaction_type = cash_transaction['transaction type']
        transaction_amount = cash_transaction['amount']
        wealth_chg = (-1 if transaction_cash_flow == 'paid' else 1) * transaction_amount
        # a=1
        wealth_df.loc[wealth_df.index >= cash_transaction_date] += wealth_chg
        
    return wealth_df

def add_financial_account_balance_in_wealth_df(wealth_df:pd.DataFrame, financial_products:dict) -> pd.DataFrame:
    for (k,v) in financial_products.items():
        if v is None:
            # no financial product
            continue
        wealth_df = wealth_df.join(v.account_tradelog.as_of_date_balance)
        wealth_df.rename(columns={'as_of_date_balance':f"{k}_balance"}, inplace=True)
    wealth_df.fillna(0, inplace=True)
    try:
        wealth_df['total_balance'] =  wealth_df.loc[:, [f"{k}_balance" for k in financial_products.keys() if f"{k}_balance" in wealth_df.columns]].sum(axis=1)
    except:
        wealth_df['total_balance'] = 0
    wealth_df['total_asset'] = wealth_df.loc[:, ['farmer_cash', 'total_balance']].sum(axis=1)
    return wealth_df

def save_wealth_csv(farmer, date_list:list, res_path:str, title:str, sub_title:str, is_include_detail=False):
    cash_transaction_list = farmer.cash_transaction_list
    wealth_df = initial_wealth_df(farmer, date_list)
    wealth_df = add_transaction_in_wealth_df(wealth_df, cash_transaction_list)
    if is_include_detail:
        wealth_df['detail'] = ""
        for adate in date_list:
            d_str = str(list(filter(lambda x:x['Date'] == adate, cash_transaction_list)))
            wealth_df.loc[adate, 'detail'] = d_str
    wealth_df.to_csv(os.path.join(res_path, f'farmer_{title}_{date_list[0]}_{date_list[-1]}_wealth.csv'))

def plot_wealth(farmer, date_list:list, res_path:str, title:str, sub_title:str):
    cash_transaction_list = farmer.cash_transaction_list
    wealth_df = initial_wealth_df(farmer, date_list)
    wealth_df = add_transaction_in_wealth_df(wealth_df, cash_transaction_list)
    # month_list = wealth_df.index.to_list()
    # wealth = np.round(wealth_df['farmer'].to_numpy(), 3)

    fig = make_subplots(
        specs=[
            [
                {
                    'secondary_y': True
                }
            ]
        ]
    )

    fig.add_trace(
        go.Scatter(
            x=wealth_df.index,
            y=wealth_df.farmer_cash,
            mode='lines',
            name='Farmer Cash ($)',
            marker={
                'color':'blue'
            }
        )
    )


    plot_title = 'Farmer Risk Management & Wealth Portfolio'
    layout = {
        'title':f"{plot_title}<br><sup>{sub_title}</sup>",
        'xaxis':{
            'title':'date',
            'ticklen':5,
            'zeroline': False
        },
        'yaxis': {
            'title': "Farmer Cash ($)",
        },
    }

    fig.update_layout(layout)

    # fig.show()
    fig.write_html(os.path.join(res_path, f'farmer_{title}_{date_list[0]}_{date_list[-1]}_wealth.html'))
    return fig

def plot_portfolio(farmer, date_list:list, res_path:str, title:str, sub_title:str, benchmark_farmer=None) -> None:
    if benchmark_farmer is not None:
        benchmark_cash_transaction_list = benchmark_farmer.cash_transaction_list
        benchmark_wealth_df = initial_wealth_df(benchmark_farmer, date_list)
        benchmark_wealth_df = add_transaction_in_wealth_df(benchmark_wealth_df, benchmark_cash_transaction_list)
        benchmark_wealth_df = add_financial_account_balance_in_wealth_df(benchmark_wealth_df, benchmark_farmer.financial_products)
    cash_transaction_list = farmer.cash_transaction_list
    wealth_df = initial_wealth_df(farmer, date_list)
    wealth_df = add_transaction_in_wealth_df(wealth_df, cash_transaction_list)
    wealth_df = add_financial_account_balance_in_wealth_df(wealth_df, farmer.financial_products)
    
    start_date, end_date = date_list[0], date_list[-1]
    whole_price_df = MarketData().price_df
    price_df = whole_price_df.loc[(whole_price_df.index >= start_date) & (whole_price_df.index <= end_date)]
    price_df.index.name = None

    if benchmark_farmer is not None:
        benchmark_portfolio_df = benchmark_wealth_df.copy()
        # benchmark_portfolio_df['Alberta spot price'] = price_df['Alberta']
        benchmark_portfolio_df.ffill(inplace=True)
    portfolio_df = wealth_df.copy()
    portfolio_df['Alberta spot price'] = price_df['Alberta']
    portfolio_df.ffill(inplace=True)

    # portfolio_df['Alberta spot price return'] =  (portfolio_df['Alberta spot price'].pct_change() +1).cumprod()
    # portfolio_df['Alberta spot price return'][0] = 1

    fig = make_subplots(
        specs=[
            [
                {
                    'secondary_y': True
                }
            ]
        ]
    )

    fig.add_trace(
        go.Scatter(
            x=portfolio_df.index,
            y=portfolio_df.farmer_cash,
            mode='lines',
            name='Farmer Cash ($)',
            marker={
                'color':'black'
            }
        )
    )
    fig.add_trace(
        go.Scatter(
            x=portfolio_df.index,
            y=portfolio_df.total_asset,
            mode='lines',
            name='Farmer Asset ($)',
            marker={
                'color':'blue'
            }
        )
    )
    if benchmark_farmer is not None:
        fig.add_trace(
            go.Scatter(
                x=benchmark_portfolio_df.index,
                y=benchmark_portfolio_df.total_asset,
                mode='lines',
                name='Farmer Asset with ONLY farming ($)',
                marker={
                    'color':'cyan'
                }
            )
        )

    fig.add_trace(
        go.Scatter(
            x=portfolio_df.index,
            y=portfolio_df['Alberta spot price'],
            yaxis='y2',
            mode='lines',
            name='Wheat Spot price ($)',
            marker={
                'color':'gray'
            }
        )
    )

    
    plot_title = 'Farmer Risk Management & Wealth Portfolio Dash Board'
    layout = {
        'title':f"{plot_title}<br><sup>{sub_title}</sup>",
        'xaxis':{
            'title':'date',
            'ticklen':5,
            'zeroline': False,
            # 'rangeselector':{
            #     'buttons':[
            #         {'count':1, 'label':'2020', 'step':'year', 'stepmode':'backward'},
            #         {'count':1, 'label':'2019', 'step':'year', 'stepmode':'backward'},
            #         {'count':1, 'label':'2018', 'step':'year', 'stepmode':'backward'},
            #         {'step':'All'}
            #     ]
            # },
            'rangeslider': {
                'visible':True
            },
            'type':'date'
        },
        'yaxis': {
            'title': "Farmer ($)",
            # 'layout_yaxis_range': [0,400000],
            # 'range': [0, 120_000]
            'range': [0, wealth_df.total_asset.max() * 1.1]
        },
        'yaxis2': {
            'title': 'Wheat Spot Price ($)'
        },
        'height':600,
        'legend': {
            'orientation': "h",
            # 'yanchor': "top",
            # 'y': 0,
            'xanchor': "right",
            'x': 1,
        }
        # 'sliders':sliders
    }

    fig.update_layout(layout)
    # fig.update_yaxes(range = [0,120_000])

    # fig.show()
    fig.write_html(os.path.join(res_path, f'farmer_{title}_{date_list[0]}_{date_list[-1]}_portfolio.html'))
    return fig