Manual PE Ratio Analysis — Magnificent 7 Stocks

Project Overview: 

    This project performs a manual exploratory analysis of the historical Price-to-Earnings (PE) ratio data for the “Magnificent 7” stocks: NVDA, AAPL, MSFT, GOOGL, AMZN, META, and TSLA. The historical data was manually downloaded and saved in Excel files, which are then analyzed and visualized to identify trends and fluctuations in valuation over time.

Workflow & Code Logic: 

    1. Data Loading
        a. Loads historical PE ratio data from an Excel workbook where each stock has its own sheet.
        b. Data columns include: TickerName, Date, Stock Price, Net EPS, and PE ratio.
        c. Dates are parsed and sorted chronologically for accurate time series analysis.

    2. Percentile Calculation & Filtering
        a. Calculates the 10th and 90th percentiles of the PE ratio for each stock to identify extreme valuation points:
            1. Below 10th percentile: Potential undervaluation zones.
            2. Above 90th percentile: Potential overvaluation zones.

        b. Filters the data to mark dates where the PE ratio falls below or above these percentiles.

    3. Visualization
        a. Plots time series of the PE ratio for each stock.
        b. Highlights dates where the PE ratio is below the 10th percentile (green dots) and above the 90th percentile (red dots).
        c. Provides a combined graph showing PE ratio trends of all seven stocks for comparative analysis.



Observations from Analysis: 

    - High Volatility Stocks:
        NVDA and TSLA exhibit significant fluctuations in PE ratios, marked by sharp peaks and drops, indicating volatile market valuation.

    - Temporary Peaks:
        AMZN showed a notable PE spike in early 2023, followed by stabilization, suggesting temporary overvaluation during that period.

    - Stable Valuations:
        AAPL, MSFT, GOOGL, and META display relatively stable PE ratios over time, indicating consistent valuation with fewer extreme fluctuations.



How to Use:

    1. Ensure the Excel file containing historical PE data is available locally with sheets named after each ticker.
    2. Run the notebook/script to load data, calculate percentiles, and generate visualizations.
    3. Use the plots to visually assess valuation extremes and historical trends for each stock.



Notes:

    1. This analysis is based on manually collected data for a limited set of stocks and is intended for educational and exploratory purposes.
    2. The methodology can be extended to automate data extraction and expand the universe of stocks analyzed.
    3. Percentile thresholds (10th and 90th) can be adjusted depending on the analysis goals.