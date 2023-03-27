import urllib.request
import json

# define the stock symbol whose summary profile data you want to fetch
stock_symbol = "TWITTERX-USD"

# send a request to the Yahoo Finance API to fetch the summary profile data for the stock symbol
url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{stock_symbol}?modules=summaryProfile"
response = urllib.request.urlopen(url)

# read the response and decode the JSON data
data = response.read().decode("utf-8")
parsed_data = json.loads(data)
# print(json.dumps(parsed_data, indent=4))
# print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
comp = parsed_data["quoteSummary"]['result'][0]['summaryProfile']
website = comp['website']
summary = ".".join(comp['longBusinessSummary'].split(".")[:2]) + "."
location = comp['state'] + ', ' + comp['country']
employees = comp['fullTimeEmployees']
sector = comp['sector']
industry = comp['industry']
companyName = 'Apple'
logo_url = 'https://logo.clearbit.com/' + companyName.lower() + '.com'
print(logo_url)
# print the JSON data
