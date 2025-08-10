PE Ratio Analysis

Overview:

    This project implements a complete workflow for PE ratio-based stock analysis and backtesting.
    It follows a systematic approach:
        a. Data Extraction – Scraping PE ratio data from Macrotrends.
        b. Analysis – Computing rolling quantiles for PE ratios to generate buy/sell signals.
        c. Backtesting – Evaluating the performance of the strategy using historical stock data.
        d. Visualization – Plotting strategy vs. market performance.

    The analysis focuses on a set of large-cap US tech stocks:
        NVDA, AAPL, MSFT, GOOGL, AMZN, META, TSLA


Workflow: 

    1. Processing Code
        a. Scrapes PE ratio data from Macrotrends.
        b. Converts raw HTML tables into clean CSV format.
        c. Saves:
            pe_ratio_data.csv — Historical PE ratio data for all tickers.
        d. Implements polite scraping with:
            1. Custom headers
            2. Random sleep intervals between requests

    2. Analysis Code
        a. Reads pe_ratio_data.csv
        b. Computes rolling 10th percentile (Rolling_P10) and 90th percentile (Rolling_P90) for PE ratios over multiple windows:
            [20, 60, 120, 180, 250, 500] trading days
        c. Generates signals:   
            1. Buy (1) → PE < Rolling_P10  
            2. Sell (-1) → PE > Rolling_P90
            3. Hold (0) → Otherwise
        d. Saves results to pe_ratio_rolling_analysis.csv
        e. Initializes an empty experiment_tracking.csv for backtesting metrics.

    3. Backtesting Code
        a. Simulates a long-only strategy:
            1. Enter position on Buy signal
            2. Exit position on Sell signal
        b. Tracks:
            1. ROI – Return on investment
            2. Max Drawdown (MDD) – Largest peak-to-trough decline
            3. Sharpe Ratio – Risk-adjusted return
            4. ROI/MDD Ratio – Risk-return efficiency
        c.Saves results in experiment_tracking.csv.

    4. Plot Code
        a. Generates visual comparisons between:
            1. Market returns vs. strategy returns
            2. Buy/Sell points on the price chart

        b. Helps interpret how PE-based signals perform over time.



Example Strategy Logic:

    1. Buy Example:
        If NVDA’s current PE = 15 and the 10th percentile (Rolling_P10) over the last 180 days = 16 → Buy.

    2. Sell Example:
        If NVDA’s current PE = 50 and the 90th percentile (Rolling_P90) = 48 → Sell.


Output Files:

    1. pe_ratio_data.csv --> Raw PE ratio data for all tickers
    2. pe_ratio_rolling_analysis.csv --> Signals & rolling quantile calculations
    3. experiment_tracking.csv -->	Backtest performance metrics


Key Notes

    1. This version only uses PE ratio — PB ratio is handled in the extended PE+PB Ratio Analysis project.
    2. Random delays are added to prevent blocking by Macrotrends.
    3. The rolling windows are flexible — change in Analysis_code.ipynb to test different horizons.