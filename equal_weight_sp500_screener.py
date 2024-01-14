import numpy as np
import pandas as pd
import xlsxwriter
import math
import requests

tocks = pd.read_csv("sp_500_stocks.csv")                         

from my_secrets import X_RapidAPI_Key

# use Yahoo finance API with RapidAPI to get real-time stock info for one ticker

from my_secrets import X_RapidAPI_Key
symbol = "AAPL"
api_url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{symbol}"
headers = {
	"X-RapidAPI-Key": X_RapidAPI_Key,
	"X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
}

response = requests.get(api_url, headers=headers).json()

# parsing for real-time stock price and market cap using list comprehension

data = response["body"]
price = [price["regularMarketPrice"] for price in data]
market_cap = [price["marketCap"] for price in data]
price, market_cap

# creating pandas dataframe

my_columns = {"Ticker": symbol, "Price": price,"Market Capitalization": market_cap, "Number Of Shares to Buy": "N/A"}
final_dataframe = pd.DataFrame(columns = my_columns)
final_dataframe

final_dataframe = final_dataframe._append(pd.Series([symbol, price, market_cap, "N/A"], index = my_columns), ignore_index = True)
final_dataframe

# looping through the tickers in our list of stocks from sp_500_stocks.csv

final_dataframe = pd.DataFrame(columns = my_columns)
for symbol in stocks["Ticker"][:1]:
    api_url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{symbol}"
    headers = {
        "X-RapidAPI-Key": X_RapidAPI_Key,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }
    response = requests.get(api_url, headers=headers).json()
    
    data = response["body"]
    price = [price["regularMarketPrice"] for price in data]
    market_cap = [price["marketCap"] for price in data]
    
    final_dataframe = final_dataframe._append(pd.Series([symbol, price, market_cap, "N/A"], 
                                                       index = my_columns), ignore_index = True)

# Using Batch API Calls to Improve Performance

tickers = stocks["Ticker"].tolist()
batch_size = 200  # Maximum tickers per batch as per the API limitation

# Initialize lists to store data
all_prices = []
all_market_caps = []
all_tickers = []

# Calculate the number of batches needed
num_batches = math.ceil(len(tickers) / batch_size)

# Iterate through batches
for i in range(num_batches):
    # Get tickers for the current batch
    start_index = i * batch_size
    end_index = min((i + 1) * batch_size, len(tickers))
    batch_tickers = tickers[start_index:end_index]

    # Prepare API URL for the current batch
    symbols_str = ','.join(batch_tickers)
    api_url = f"https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/{symbols_str}"
    headers = {
        "X-RapidAPI-Key": X_RapidAPI_Key,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    # Make API call for the current batch
    response = requests.get(api_url, headers=headers).json()

    # Ensure 'body' key is present in the response
    if "body" in response:
        data = response["body"]

        # Extract prices, market caps, and tickers
        for item in data:
            price = item.get("regularMarketPrice")
            market_cap = item.get("marketCap")
            ticker = item.get("symbol", "N/A")

            # Append data only if market_cap is not None
            if market_cap is not None:
                all_prices.append(price)
                all_market_caps.append(market_cap)
                all_tickers.append(ticker)

# Filter out None values from market caps and convert to integers
valid_market_caps = [int(round(cap)) for cap in all_market_caps if cap is not None]

# Create DataFrame using all retrieved data
final_data = {
    "Ticker": all_tickers[:len(valid_market_caps)],
    "Stock Price": all_prices[:len(valid_market_caps)],
    "Market Capitalization": valid_market_caps
}

final_dataframe = pd.DataFrame(final_data)

# Calculating the Number of Shares to Buy

portfolio_size = input("Enter the value of your portfolio:")

try:
    val = float(portfolio_size)
except ValueError:
    print("That's not a number! \n Try again:")
    portfolio_size = input("Enter the value of your portfolio:")

position_size = val / len(final_dataframe.index)
for i in range(0, len(final_dataframe.index)):
    final_dataframe.loc[i, 'Number Of Shares to Buy'] = math.floor(position_size / final_dataframe.loc[i, 'Stock Price'])
final_dataframe

#Initializing our XlsxWriter Object

with pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter') as writer:
    final_dataframe.to_excel(writer, sheet_name='Recommended Trades', index = False)

#Creating the Formats We'll Need For Our .xlsx File

background_color = '#0a0a23'
font_color = '#ffffff'

string_format = writer.book.add_format(
        {
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

dollar_format = writer.book.add_format(
        {
            'num_format':'$0.00',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

integer_format = writer.book.add_format(
        {
            'num_format':'0',
            'font_color': font_color,
            'bg_color': background_color,
            'border': 1
        }
    )

#Applying the Formats to the Columns of Our .xlsx File

column_formats = { 
                    'A': ['Ticker', string_format],
                    'B': ['Price', dollar_format],
                    'C': ['Market Capitalization', dollar_format],
                    'D': ['Number of Shares to Buy', integer_format]
                    }

for column in column_formats.keys():
    writer.sheets['Recommended Trades'].set_column(f'{column}:{column}', 20, column_formats[column][1])
    writer.sheets['Recommended Trades'].write(f'{column}1', column_formats[column][0], string_format)


# Closing Our Excel Output

writer.close()
