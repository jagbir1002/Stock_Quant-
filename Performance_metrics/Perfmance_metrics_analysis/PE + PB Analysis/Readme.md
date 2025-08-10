PE + PB Ratio Analysis

Overview: 
       
       This project analyzes Price-to-Earnings (PE) and Price-to-Book (PB) ratios for selected stocks, applies rolling quantile-based thresholds to generate trading signals, and evaluates their performance using backtesting metrics such as ROI, Max Drawdown, Sharpe Ratio, and ROI-to-MDD ratio.

The workflow is organized into four Jupyter notebooks:

       1. Processing_code – Data extraction from Macrotrends
       2. Analysis_code – Rolling quantile-based PE & PB analysis
       3. Backtesting_code – Strategy simulation and performance evaluation
       4. Plot_code – Visualization of results

1. Processing_code
       Purpose: 
       Fetches historical PE and PB ratio data for selected tickers from Macrotrends.

       Key Steps:
              a. Uses requests + BeautifulSoup to scrape HTML tables.
              b. Extracts and cleans data for:
                     1. Date
                     2. Stock Price
                     3. TTM Net EPS (for PE)
                     4. Book Value per Share (for PB)
                     5. PE Ratio
                     6. PB Ratio

              c. Supports multiple tickers (e.g., NVDA, AAPL, MSFT, GOOGL, AMZN, META, TSLA).
              d. Saves consolidated PE and PB ratio data into data/pe_pb_ratio_data.csv.

2. Analysis_code
       Purpose: 
       Generate trading signals using rolling quantile analysis for both PE and PB ratios.

       Logic:
              a. For each ticker and rolling window size (20, 60, 120, 180, 250, 500 days):
                     1. Calculate 10th percentile (Rolling_P10) and 90th percentile (Rolling_P90) for PE.
                     2. Calculate 10th percentile (Rolling_PB10) and 90th percentile (Rolling_PB90) for PB.
                     3. Generate signals:
                            a. Buy Signal (1): PE < Rolling_P10 and PB < Rolling_PB10 (potentially undervalued on both metrics)
                            b. Sell Signal (-1): PE > Rolling_P90 and PB > Rolling_PB90 (potentially overvalued on both metrics)
                            c. Hold (0): Otherwise
              b. Saves results to data/pe_pb_ratio_rolling_analysis.csv.
              c. Initializes experiment_tracking.csv for later backtesting metrics.

3. Backtesting_code
       Purpose: 
       Simulate a long-only trading strategy using combined PE + PB signals and calculate performance metrics.

       Strategy Rules:
              a. Enter Long: Previous day’s signal = 1
              b. Exit Position: Previous day’s signal = -1

       Performance Metrics:
              a. ROI – Total return from the strategy
              b. Max Drawdown (MDD) – Largest portfolio decline from peak
              c. Sharpe Ratio – Risk-adjusted return
              d. ROI-to-MDD – Return relative to drawdown

       Saves backtest results into experiment_tracking.csv.

4. Plot_code
       Purpose: 
       Visualize results from the combined PE + PB analysis and backtesting.

       Typical Plots:
              a. Cumulative returns (Strategy vs. Market)
              b. Buy/Sell signal markers over price chart
              c. Rolling PE & PB thresholds and actual values



Notes:

       1. Uses both valuation metrics (PE & PB) to filter potential trades.  
       2. Data scraping includes 5–10 second delays between requests to avoid server overload.
       3. Rolling quantiles require at least 5 valid data points before producing a signal.
       4. The combined condition makes this stricter than single-metric strategies, potentially reducing false signals.

