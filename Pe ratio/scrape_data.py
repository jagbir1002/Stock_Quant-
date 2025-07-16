# # pip install beautifulsoup4
import bs4
import pandas as pd
import requests
from io import StringIO

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# # check some sample data
req_url = "https://www.macrotrends.net/stocks/charts/NVDA/nvidia/pe-ratio"
resp = requests.get(req_url, headers=headers)
# find table with PE ratio data in response
parser = bs4.BeautifulSoup(resp.text, "html.parser")
# take first table
pe_ratio_table = parser.find_all("table")[0]
df = pd.read_html(StringIO(str(pe_ratio_table)), skiprows=0)[0]
df.columns = df.columns.droplevel(0)  # Remove the top level
print(df.shape)
print(df.head())
print("----------------")
print()
print(df.iloc[0])