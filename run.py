# ----- Library Imports -----
import requests
import pandas as pd

# ----- User Imports -----
from api_key import key


import csv
import requests

base_url = 'https://cloud.iexapis.com/stable'
url = base_url + '/stock/{symbol}/advanced-stats'
# Example API Call: https://cloud.iexapis.com/stable/stock/silv/advanced-stats

# We will be using IEXCloud: https://iexcloud.io/docs/api/#advanced-stats
# Mostly need Earnings, Income Statement, Balance Sheet, Cash Flow
# Might need price of stock


stocks = ['SILV', 'PAAS', 'MAG', 'FR']

# Monthly data
# Median Trailing 12-month free cash flow to enterprise value.
# I think this is the middle of the previous 12 months free cash flow to the most recent enterprise value.

# I need the 12 month trailing free cash flow
# Free Cash Flow = Net Profit + Interest Expense - Net Capital Expenditure (CAPEX) - Net Changes in Working Capital
#                  - Tax Shield on Interest Expense
# ----- Net Income == Net Profit ----- Is on API -- netIncome
# Interest Expense -- on the api -- interestExpense
# Capital Expenditures == CapEx -- on the api as capitalExpenditures
# Change in Working Capital = Change in Current Assets - Change in Current Liabilities
# Do not see working capital on the api - however there is totalCurrentsAssets and totalCurrentLiabilities -- Subtract the change over two periods on a monthly basis.


# Ebitda --> In Advanced Statistics besides enterprise value as well.
# Enterprise Value --> Enterprise value is in advanced statistics
# Enterprise Value / EBITDA --> Why I do not think this was the best value.

# I need other ratios definined the excel file
# Cash and Cash Equivalents --> Cashflow  --> API has it as currentCash or totalCash in financials -- pretty sure it is currentCash
# CapEx = Capital Expenditures  --> Cashflow --> API has it in Return of Capital under capex

# Get Financial Ratios

# Put it into Excel format
# df.to_excel(r'Path where the exported excel file will be stored\File Name.xlsx', index = False)               # pip install openpyxl if error


# TO add by hand: Black-Scholes Model  = calculate the discounted net present value of all mines + option value of the minues as shown by the formula
# Enterprise Value / (per) Resource -- Get Resource amounts off of the websites
# Total Acquisition Cost - TAC
# Mills - Getting the product to market
