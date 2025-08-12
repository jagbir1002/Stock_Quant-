Project Description 

The system is designed with research-grade data integrity in mind, enabling downstream quantitative modeling, factor analysis, and systematic strategy development.

Core workflow:

    1. Universe Selection – Scrapes the latest top 2,000 companies (by market cap) from stockanalysis.com, retrieving ticker symbols, company names, and market caps, and storing them in an Excel file.

    2. Filing Acquisition – For each ticker, the pipeline interfaces with SEC EDGAR to download the most recent annual and quarterly filings in priority order:
        a. 10-K (Annual Reports)
        b. 20-F (Foreign Issuers Annual Reports)
        c. 10-Q (Quarterly Reports)

    3. Parsing & Extraction – Uses HTML parsing to extract targeted financial statement line items from the Balance Sheet, including:
        a. Assets (Current, Non-Current, Total)
        b. Liabilities (Current, Non-Current, Total)
        c. Equity (Shareholders’/Stockholders’ Equity)
        d. Other critical fields required for financial ratio computation.
    
    4. Data Cleaning & Validation – Implements:
        a. Pattern matching with target variants to ensure accuracy.
        b. Exclusion logic to prevent false matches (e.g., ratios, percentages instead of amounts).
        c. Currency and unit standardization for cross-company comparability.

    5. Output & Storage – Appends results to a master Excel database without overwriting prior entries, supporting incremental historical builds.

Use Case:

    This dataset serves as the foundation for backtesting equity strategies, factor research, and multi-factor ranking models, ensuring all financial inputs are sourced directly from primary filings for maximum reliability.

Key Features:

    1. Automated universe definition based on latest market cap rankings.
    2. SEC EDGAR integration with intelligent filing type prioritization.
    3. High-precision HTML parsing with robust matching logic.
    4. Incremental, append-only data storage for time-series analysis.



Project Workflow & Code Logic


1. Downloading_company_name.ipynb
    Purpose: 
        Scrapes the website [StockAnalysis](https://stockanalysis.com/list/biggest-companies/) to get top 2000 companies according to market cap

    Output:
        Saves the list of companies (Ticker, Company Name, Market Cap) to an Excel file named:
        Data/Stock List.xlsx

    Notes:
        a. The scraping step should be repeated regularly to keep the dataset aligned with current market caps.
        b. The output Excel is used as input for the SEC filings extraction step.


2. sec_filings_extraction.py

        Purpose:
            Uses the tickers from `Stock List.xlsx` to **download and parse SEC filings** (10-K, 10-Q, and 20-F) and extract targeted financial metrics.

        Data Sources:  
            SEC EDGAR API(primary source for US and foreign company filings)

        Data Extraction Process:
            1. Reads tickers from `Stock List.xlsx`
            2. For each ticker:
                Fetches the latest 10-K filing (priority for US companies)
                If unavailable, fetches 20-F (foreign annual reports)
                If both unavailable, falls back to **10-Q** (quarterly report)
            3. Parses filing tables to extract only relevant metrics defined in `TARGET_VARIANTS`, such as:
                a. Revenue
                b. Net Income
                c. EPS
                d. Total Assets
                e. Total Equity
                f. Current Assets
                g. Current Liabilities
                h. Long-term Debt
            4. Filters out irrelevant matches using `EXCLUDE_VARIANTS` (e.g., percentage rows, unrelated currency values)
            5. Standardizes currency to USD when available

        Output: 
            Appends all extracted data to:
            a. Filngs ( Here all the lastest filings are saved )
            b. Final_Data.xlsx ( All the parsed data from the html filings downloaded is saved here)