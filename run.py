# ----- Library Imports -----
import requests
import pandas as pd
import csv
import requests

# ----- User Imports -----
from api_key import key


base_url = 'https://cloud.iexapis.com/stable'
url = base_url + '/stock/{symbol}/advanced-stats'
# Batch Stock URL Request: /stock/{symbol}/batch
# Example API Call: https://cloud.iexapis.com/stable/stock/silv/advanced-stats
# We will be using IEXCloud: https://iexcloud.io/docs/api/#advanced-stats
# Mostly need Earnings, Income Statement, Balance Sheet, Cash Flow
# Might need price of stock

# Stocks that we want the data for
stocks = ['SILV', 'AYA', 'MAG', 'FR', 'SVM', 'EDR', 'PAAS', 'HL', 'FRES', 'FVI', 'CDE', 'WPM', 'MMX', 'SSL']

def get_data_for_stocks(stocks):
    # Iterate over stocks -- throw error if unable to get data
    for stock in stocks:
        request_url = make_url(stock)
        r = requests.get(request_url)


def make_url(stock, endpoint):
    # Include API token
    return f'https://cloud.iexapis.com/stable/stock/{stock}/{endpoint}'


def get_advanced_stats(stock):
    # See Advanced Stats here: https://www.iexcloud.io/docs/api/#advanced-stats
    # From advanced stats: EBITDA, debtToEquity, profitMargin, enterpriseValue, enterpriseValueToRevenue
    #                      pegRatio
    request_url = make_url(stock, f'/stock/{stock}/advanced-stats')
    r = requests.get(request_url)


def get_financials(stock):
    # See Financials here: https://www.iexcloud.io/docs/api/#financials
    # From financials: EBITDA, cashFlow, costOfRevenue, filingType, assetsCurrentCash (Cash and cash equivalents)
    #                  capex (capital expenditures), netIncome
    pass

# ---- Monthly data ----
# Median Trailing 12-month free cash flow to enterprise value. -- this is the middle of the previous 12 months free cash flow to the most recent enterprise value.
# Free Cash Flow = Cash from Operations - Capital Expenditures
# ----- Net Income == Net Profit ----- is on API under financials as netIncome
# Interest Expense -- on the api -- interestExpense
# Change in Working Capital = Change in Current Assets - Change in Current Liabilities
# Do not see working capital on the api - however there is totalCurrentsAssets and totalCurrentLiabilities -- Subtract the change over two periods on a monthly basis.

# ----- Metrics that we want -----
# Debt Ratio: Total Liabilities / Total Assets
# Debt to Equity Ratio: Debt to Equity Ratio = Total Liabilities / Shareholder Equity
# Interest Coverage Ratio: Operating Income / Interest Expenses -- This might be pretty great
# Debt Service Coverage Ratio: Operating Income / Total Debt Service
#
# Do not care about market value ratios
# pegRatio: See: https://duckduckgo.com/?t=ffab&q=pegRatio&ia=web

def calculate_metrics(df):
    # Enterprise Value / EBITDA -- Not the best metric
    # See: https://corporatefinanceinstitute.com/resources/knowledge/valuation/ev-ebitda/
    df['ev_to_ebitda'] = df['enterpriseValue'] / df['EBITDA']

    # Current Ratio: See: https://www.investopedia.com/terms/c/currentratio.asp Current Assets / Current Liabilities
    # Current Assets / Current Liabilities
    df['current_ratio'] = df['currentAssets'] / df['totalCurrentLiabilities']

    # Debt Ratio: See https://www.investopedia.com/terms/d/debtratio.asp
    # Total Debt / Total Assets
    df['debt_ratio'] = df['totalDebt'] / df['totalAssets']


def output_raw_data(df):
    print(' ------------------ ')
    for index, row in df.iterrows():
        print(row)
    print(' ------------------ ')


def dump_to_excel(df):
    import os
    # Dump the data to an excel file
    df.to_excel(os.path.dirname(sys.argv[0]).join('raw_data.xlsx', index=False)   # pip install openpyxl if error


# ----- Followup -----
# TO add by hand: Black-Scholes Model  = calculate the discounted net present value of all mines + option value of the minues as shown by the formula
# Enterprise Value / (per) Resource -- Get Resource amounts off of the websites
# Total Acquisition Cost - TAC
# Mill Data - Getting the product to market
