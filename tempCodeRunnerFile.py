import urllib.request
import json

# define the stock symbol whose summary profile data you want to fetch
stock_symbol = "AAPL"

# send a request to the Yahoo Finance API to fetch the summary profile data for the stock symbol
url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{stock_symbol}?modules=summaryProfile"
response = urllib.request.urlopen(url)

# read the response and decode the JSON data
data = response.read().decode("utf-8")
parsed_data = json.loads(data)

# print the JSON data
print(json.dumps(parsed_data, indent=4))