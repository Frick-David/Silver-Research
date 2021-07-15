# ----- Library Imports -----
import requests
import pandas as pd
import csv
import requests

# ----- User Imports -----
from api_key import key
from helpers import test_status_code


base_url = 'https://cloud.iexapis.com/stable'
url = base_url + '/stock/{symbol}/advanced-stats'
# Batch Stock URL Request: /stock/{symbol}/batch
# Example API Call: https://cloud.iexapis.com/stable/stock/silv/advanced-stats
# We will be using IEXCloud: https://iexcloud.io/docs/api/#advanced-stats
# Mostly need Earnings, Income Statement, Balance Sheet, Cash Flow

# Stocks that we want the data for
stocks = ['SILV', 'AYA', 'MAG', 'FR', 'SVM', 'EDR', 'PAAS', 'HL', 'FRES', 'FVI', 'CDE', 'WPM', 'MMX', 'SSL']
base_url = 'https://cloud.iexapis.com/stable/stock'


df = pd.from_csv('silver-data.csv')
if df.empty:
    print('DataFrame is empty')

# We want to dump any none empty dataframe to the csv and load it on next run.

def get_data_for_stocks(stocks):
    # Iterate over stocks -- throw error if unable to get data
    for stock in stocks:
        request_url = make_url(stock)
        r = requests.get(request_url)


def make_url(stock, endpoint):
    # Include API token
    return f'{base_url}/{stock}/{endpoint}'


def get_advanced_stats(stock):
    # See Advanced Stats here: https://www.iexcloud.io/docs/api/#advanced-stats
    # From advanced stats: EBITDA, debtToEquity, profitMargin, enterpriseValue, enterpriseValueToRevenue
    #                      pegRatio, marketcap
    request_url = make_url(stock, f'/stock/{stock}/advanced-stats')
    r = requests.get(request_url)
    test_status_code(r)
    json = r.json()


def get_financials(stock):
    # See Financials here: https://www.iexcloud.io/docs/api/#financials
    # From financials: EBITDA, cashFlow, costOfRevenue, filingType, assetsCurrentCash (Cash and cash equivalents)
    #                  capex (capital expenditures), netIncome
    # API route: GET /stock/{symbol}/financials/
    request_url = make_url(stock, f'/stock/{symbol}/financials/')
    r = requests.get(request_url)
    test_status_code(r)
    json = r.json()

# ---- Monthly data ----
# Median Trailing 12-month free cash flow / enterprise value. -- this is the middle of the previous 12 months free cash flow to the most recent enterprise value.
# Free Cash Flow = Cash from Operations - Capital Expenditures
# Interest Expense -- on the api -- interestExpense
# Change in Working Capital = Change in Current Assets - Change in Current Liabilities
# Do not see working capital on the api - however there is totalCurrentsAssets and totalCurrentLiabilities -- Subtract the change over two periods on a monthly basis.


def calculate_metrics(df):
    # Enterprise Value / EBITDA -- Not the best metric
    # See: https://corporatefinanceinstitute.com/resources/knowledge/valuation/ev-ebitda/
    df['ev_to_ebitda'] = df['enterpriseValue'] / df['EBITDA']
    # See for ratios: https://corporatefinanceinstitute.com/resources/knowledge/finance/financial-ratios/
    # Current Ratio: See: https://www.investopedia.com/terms/c/currentratio.asp Current Assets / Current Liabilities
    # Current Assets / Current Liabilities
    df['current_ratio'] = df['currentAssets'] / df['totalCurrentLiabilities']
    # Debt Ratio: See https://www.investopedia.com/terms/d/debtratio.asp
    # Total Debt / Total Assets
    df['debt_ratio'] = df['totalDebt'] / df['totalAssets']
    # Debt to Equity Ratio: Debt to Equity Ratio = Total Liabilities / Shareholder Equity
    df['debt_to_equity_ratio'] = df['totalLiabilities'] / df['shareholderEquity']
    # Interest Coverage Ratio: Operating Income / Interest Expenses -- This might be pretty great
    df['interest_coverage_ratio'] = df['operatingIncome'] / df['InterestExpense']
    # Return on Assets Ratio = Net Income / Total Assets
    df['return_assets_ratio'] = df['netIncome'] / df['totalAssets']
    # Return on Equity Ratio = Net Income / Shareholder's Equity
    df['return_on_equity'] = df['netIncome'] / df['equityShareholder']
    # See if there was shareholder diluation. Ritchie said this was important.


def _get_time_series_data():
    # API route: GET /time-series/{id}/{key?}/{subkey?}
    # id = other route say cash flow
    # key is the stock
    # subkey is the 10-Q or the 10-
    # We want Median Trailing 12-month free cash flow - thuse we want the operatingCashFlow (cashFlowOperating) and CapEx (capex)
    # Example api route: /time-series/{CASH_FLOW}/SILV?token=YOUR_TOKEN_HERE?limit=12&subattribute
    request_url = make_url(stock, f'/stock/{symbol}/financials/')
    r = requests.get(request_url)
    test_status_code(r)
    json = r.json()

    # df['median_twelve_month_FCF']


def output_raw_data(df):
    print(' ------------------ ')
    for index, row in df.iterrows():
        print(row)
    print(' ------------------ ')


def dump_to_excel(df):
    import os
    # Dump the data to an excel file
    df.to_excel(os.path.dirname(sys.argv[0]).join('raw_data.xlsx', index=False))   # pip install openpyxl if error


# ----- Followup -----
# ----- By hand -----
# Mill Data - Getting the product to market -- if they have biggest mine but no mine they will not succeed.
# Black-Scholes Model  = calculate the discounted net present value of all mines + option value of the minues as shown by the formula
# Enterprise Value per Resource -- Get Resource amounts off of the websites
# See https://corporatefinanceinstitute.com/resources/knowledge/modeling/monthly-cash-flow-forecast-model/ for ideas for cash flow forecasting

if __name__ == '__main__':
    df = pd.DataFrame()

    dump = input("Do you want to save the data? Y or N")
    if dump == 'Y':
        dump_to_excel(df)
