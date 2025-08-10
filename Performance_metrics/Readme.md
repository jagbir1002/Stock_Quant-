Performance Metrics – Stock Valuation & Strategy Analysis

Overview:

    This folder contains a progressive series of projects analyzing stock valuation metrics and their use in trading strategies.
    The work evolves from basic PE ratio analysis to automated data extraction and finally to multi-metric (PE + PB) backtesting with performance evaluation.

Project Evolution:

    1. PE Ratio – Manual Extraction
        Folder: Peratio_manual_extraction

        Description:
            a. The starting point of the project.
            b. Uses manually downloaded CSV files containing historical Price-to-Earnings (PE) ratio data.
            c. Performs basic data cleaning and visualization of the PE ratio over time for selected companies.
            d. No automation or trading logic — purely exploratory and visual analysis.

    2. PE Ratio – Rolling Percentile Strategy
        Folder: Peratio_rolling_percentile

        Description:
            a. An automated extension of the manual approach.
            b. Scrapes historical PE ratio data from Macrotrends.net (no manual download).
            c. Calculates rolling 10th and 90th percentiles over a defined window to identify undervalued and overvalued conditions.   d. Generates buy/sell trading signals and compares strategy returns vs. market returns.
            e. Adds visual plots of cumulative returns and signal points.

    3. Performance Metrics Analysis (PE + PB Ratios)
        Folder: Perfmance_metrics_analysis

        Description:
            a. The most advanced stage of the project, combining:
                1. Automated PE + PB ratio extraction from Macrotrends.net.
                2. Dual-metric signal generation:
                3. Buy when both PE and PB ratios are in their respective bottom 10% (undervalued).
                4. Sell when both are in the top 10% (overvalued).

            b. Backtesting framework with:
                1. ROI (Return on Investment)
                2. Max Drawdown (MDD)
                3. Sharpe Ratio
                4. ROI-to-MDD ratio

            c. Produces cumulative returns charts and other visualizations to evaluate performance.


Notes:

    1. All projects use historical financial data from Macrotrends.net.
    2. Delays are included in scraping scripts to avoid overwhelming the source server.
    3. This work is for educational purposes and should not be considered financial advice.
    4. The evolution showcases how a basic idea can be expanded into a more data-driven, automated, and performance-tested trading framework.