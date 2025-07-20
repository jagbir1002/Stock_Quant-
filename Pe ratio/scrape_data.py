# Old code 
'''def get_pe_ratio(ticker, company_name):  
    # pip install beautifulsoup4
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

    return df'''


# Modified code
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

def get_pe_ratio(ticker, company_name):
    try:
        req_url = f"https://www.macrotrends.net/stocks/charts/{ticker}/{company_name}/pe-ratio"
        resp = requests.get(req_url, headers=headers, timeout=10)

        if resp.status_code != 200:
            print(f"[ERROR] Failed to fetch {ticker}: status code {resp.status_code}")
            return pd.DataFrame()

        parser = bs4.BeautifulSoup(resp.text, "html.parser")
        tables = parser.find_all("table")

        if not tables:
            print(f"[ERROR] No tables found for {ticker}")
            return pd.DataFrame()

        df = pd.read_html(StringIO(str(tables[0])), skiprows=0)[0]

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(0)

        df['Ticker'] = ticker

        print(df.shape)
        print(df.head())
        print("----------------")
        print(df.iloc[0])

        return df   # <--- This line is necessary

    except Exception as e:
        print(f"[ERROR] Exception while processing {ticker}: {e}")
        return pd.DataFrame()

