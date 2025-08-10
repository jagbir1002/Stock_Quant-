PE Ratio Based Trading Strategy

Project Overview:

This project is an extension of my earlier Manual PE Ratio Extraction analysis, where I manually downloaded and analyzed historical PE ratio data for the Magnificent 7 stocks. After receiving reviewer feedback, I improved the methodology by introducing rolling percentiles to make the analysis dynamic over time.

The result is a prototype quantitative trading strategy that generates buy and sell signals based on the PE ratio’s relative valuation within a rolling historical window. The strategy is then backtested and compared against a simple buy-and-hold benchmark.


Workflow & Code Logic:

    1. Data Extraction
        a. Scrapes historical PE ratio data and related stock prices from Macrotrends.net for a predefined set of tickers.
        b. Extracted data includes Date, Stock Price, Trailing Twelve Months (TTM) Earnings Per Share (EPS), and PE ratio.
        c. Data is cleaned, formatted, and saved locally as data/pe_ratio_data.csv.
        d. A polite delay (time.sleep(1.5)) is added between requests to avoid overloading the website.

    2. Data Preparation & Signal Generation
        a. Loads the saved PE ratio data and sorts it by ticker and date.
        b. Calculates rolling 10th percentile (Rolling_P10) and 90th percentile (Rolling_P90) of the PE ratio over a 250-day window (~1 trading year) per ticker.
        c. Generates trading signals based on PE ratio relative to these percentiles:
            1. Buy signal (1) when PE falls below the 10th percentile (potential undervaluation).
            2. Sell signal (-1) when PE rises above the 90th percentile (potential overvaluation).
            3. Hold/No action (0) otherwise.

    3. Strategy Backtesting
        For each stock ticker:
            1. Computes daily returns based on stock prices.
            2. Applies the buy/sell signals to simulate a trading strategy where the position is held when the signal is 1 and exited when the signal is -1.
            3. Calculates the cumulative returns for both the strategy and the buy-and-hold market returns.

    4. Visualization
        Plots the cumulative returns of the strategy against the market for each stock to visually assess performance and strategy effectiveness.



How to Run:

    1. Run the data extraction script to scrape and save PE ratio data.
    2. Run the signal generation and backtesting code to calculate trading signals and simulate strategy returns.
    3. Review the generated plots comparing the strategy to market returns.


Notes & Improvements from Previous Project:

    1. Built upon Manual PE Ratio Extraction project, which used fixed percentiles for the entire dataset.
    2. Introduced rolling percentiles for dynamic, time-sensitive thresholds.
    3. More realistic simulation by updating valuation ranges as new data becomes available.
    4. Uses automated scraping instead of manual Excel downloads.
    5. Can be extended to:
        a. A larger stock universe.
        b. Different rolling windows & quantile thresholds.
        c. Transaction cost modeling.