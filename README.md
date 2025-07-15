# Stock_Quant-

Analysis of Historical PE Ratios for the Magnificent 7 (2022–2025)

Problem Statement:

Extract and visualize the historical PE Ratio for all the 7 magnificent stocks.
[ AAPL, MSFT, NVDA, TSLA, META, GOOGL, AMZN ]

Process:
1. Extract the data from the source. ( yahoo finance, Marcotrends )
    The approach used by me was to manually enter the data from Marcotrends, this site provided me with the historical pe ratio data. I also used module yfinance at first to check whether I can get my data from there.
    This were the conclusions I found
    a. yfinance do not have the historical data from past years. It only contains the latest pe ratio and the daily prices of the stock.
    b. I could get the pe ratios from paid API’s which could give me the historical data. 
    c. So I found a website named Marcotrends which provided me the historical data that extracted manually onto the excel file, which  I later used to plot the graph

2. Check the extracted data is correct or not

3. Calculate the 10th and 90th percentile for each of the stock’s PE ratio. 

4. Visualize by plotting graph
    a. I plotted different graph for each of the stocks 
    b. Then I plotted a combined graph to make my analysis and side by side comparison with other stocks

5. Analyze pattern
    Analysis made by me looking at the graphs
    a. Stocks like NVDA and TSLA, shows the highest fluctuations with sharp drops and peaks 
    b. Stock AMZN shows a temporary peak which was in early 2023, which indicates that the PE ratio increased significantly, but later on it stabilized.
    c.Stocks such as AAPL, MSFT, GOOGL and META show relatively stable PE ratios over the same period of time, with the least fluctuations.
