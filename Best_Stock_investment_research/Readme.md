Project Workflow & Code Logic

1. Downloading_top200_stocks.ipynb

    Purpose: Scrapes the website Stockanalysis to get the current top 200 companies ranked by market capitalization.
    Output: Saves the list of companies and their tickers in an Excel file named Top200_StockAnalysis.xlsx.
    Note: This scraping step should be repeated regularly to keep the dataset up to date with market changes.



2. Data_extraction.ipynb

    Purpose: Uses the tickers from the downloaded Excel file to collect historical financial data for each company.
    Data Sources:
        1. Macrotrends website (quarterly data): ROE, ROA, Debt to Equity, P/E ratio, P/B ratio
        2. yfinance API (annual data): Dividend Yield, Market Cap, Volume

    Data Processing:
        1. Converts Macrotrends’ quarterly data into annual data to align with yfinance’s annual data frequency.
        2. Saves each parameter’s annual data separately as CSV files under Data/Files, e.g., PE_Annual.csv, ROE_Annual.csv, DividendYield_Data.csv, etc.



3. Analysis_code.ipynb

    Purpose: Merges all annual CSV files into a single Excel file named final_merged_by_year.csv. (Data/Ranked Stocks)

    Data Analysis & Filtering:
        1. Calculates rolling percentiles (5-year window) for key financial metrics to normalize values across time and stocks. For example:
            a. Value metrics: PE and PB percentiles (lower values are better → inverted)
            b. Quality metrics: ROE and ROA percentiles (higher is better)
            c. Risk metric: DebtToEquity percentile (lower is better → inverted)

        2. Combines percentiles into composite scores:
            a. Value_Score = average(PE_percentile, PB_percentile)
            b. Quality_Score = average(ROE_percentile, ROA_percentile)
            c. Risk_Score = DebtToEquity_percentile
            d. Total_Score = 0.4 * Value_Score + 0.4 * Quality_Score + 0.2 * Risk_Score

        3. Stepwise Filtering per year to progressively narrow down the stocks by selecting the top companies based on a sequence of filters:

            a. Keep top 150 by highest ROE
            b. From these, keep top 100 by highest ROA
            c. Then top 80 by highest Dividend Yield
            d. Then top 60 by lowest DebtToEquity
            e. Then top 50 by lowest PE
            f. Then top 40 by lowest PB
            g. Then top 30 by highest Market Cap
            h. Finally, top 20 by highest Volume

        4. Ranks the filtered stocks per year by their Total_Score.

        5. Saves the ranked list with relevant columns to final_scored_ranked.csv. (Data/Ranked Stocks)


4. Backtesting_code.ipynb

    Purpose: Simulates an investment portfolio using the top-ranked stocks from the analysis phase to evaluate historical performance and key risk-return metrics.

    Key Steps:

        1. Loads the ranked stocks data (final_scored_ranked.csv) containing yearly rankings and selects the top N stocks (default 20) for each year.

        2. Iterates through each year in the backtest period:
            a. Downloads daily historical closing prices for the selected stocks from yfinance.
            b. Skips any year if no valid price data is available.

        3. Constructs an equal-weighted portfolio by allocating the initial capital evenly across the selected stocks for that year.

        4. Calculates daily portfolio value by summing the value of shares held for each stock.

        5. Computes individual stock performance metrics per year, including:
            a. Total Return
            b. CAGR (Compound Annual Growth Rate)
            c. Sharpe Ratio (annualized risk-adjusted return)
            d. Max Drawdown (largest peak-to-trough loss)

        6. Aggregates metrics over multiple years for stocks appearing repeatedly, averaging returns and Sharpe ratios while taking the worst max drawdown.

        7. Calculates overall portfolio-level metrics across the entire backtest period:
            a. Total Return
            b. CAGR
            c. Sharpe Ratio
            d. Max Drawdown

        8. Visualizes portfolio cumulative returns over the full period and in three sub-periods (2010–2015, 2016–2020, 2021–2025), including year-end capital points.

        9. Ranks stocks by a Combined Score (CAGR + Sharpe – Max Drawdown) and displays the top 20 performers.

        10. Produces a final stable stock ranking by combining normalized combined scores with normalized appearance counts (years the stock appeared in portfolio), weighted 70% and 30% respectively.

        11. Saves two Excel files:
            a. best_stocks_max_returns.xlsx containing ranked metrics based on maximum returns
            b. best_stocks_stable_combined.xlsx containing rankings factoring both performance and stability