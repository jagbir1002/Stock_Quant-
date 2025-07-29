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



Enhancing the Analysis of Historical PE Ratios for the Magnificent 7 (2022–2025)


Problem statement:

Automating the Pe ratio extraction
Fix the percentile calculation from static to rolling basis and run a small backtesting using thresholds on PE ratio. 


Process:

1. Automating the Pe ratio extraction was done by using the code given by Devanshu, filename=’scrape_data.py. I have also made some changes in the code. Changes are as follows:
    a. I added a section named tickers, initially the previous code was extracting details from the website for just one company, now the code will extract the pe ratio according to the ticker name.
    b. I also added a for loop in order to iterate through the tickers dictionary and extract data for each stock.
    c. I also added an exception (try-except error)so that the code doesn't stop running even if data of any one ticker fails to be extracted. 
    d. I also imported os, in order to add all the extracted data into one single csv file, or create a csv file if it doesn't exist.
Done this to ease the usage of scrape_data.py in the file main_code.ipnb

3. Connected the excel file to the main_code.

4. Created a window to calculate the rolling percentile.

5. Ran a backtest (details of the backtest are mentioned in the notebook markdown)

6. Plotted the strategy vs market graph.




Backtesting the Strategies using PE and PB ratio with Multi Rolling Window Analysis for Magnificent 7 
[ AAPL, MSFT, NVDA, TSLA, META, GOOGL, AMZN ]

Problem statement:

1. Test for multiple rolling windows and backtesting the strategy of using $100K dollars as starting capital with key performance metrics ( MDD, ROI, SHARPE RATIO, ROI TO MDD )
2. Once the analysis is complete for PE, include PB ratio and test combined PE + PB strategies using similar logic

Process:

1. Creation of the processing_code.ipynb notebook. This contains the same code as the previous task for the automatic PE Ratio extraction from the Marcotrends website. 
( Extraction of PB ratio along with PE Ratio is the only one addition in this code )

2. Analysis_code_PE.ipynb is the notebook where different rolling windows are tested. I started with 20 as my rolling window then later tested for others as well. 
Also created an experiment tracking file at the end of this code, which can be used to save the results or keep the track for different rolling windows. 

3. I started the backtest strategy by Signal generation. 
    a. Buy signal : 1 ( if PE < 10 percentile, stock is undervalued )
    b. Sell signal : -1 ( if PE > 90 percentile, stock is overvalued )
    c. Hold : 0 
   Now I start calculating the performance metrics:
    a. ROI
    b. MDD
    c. Sharpe Ratio 
    d. ROI to MDD
    
4. S$P 500 index is downloaded using the yfinance module. These all the values are then plotted on the multiple y-axis plots

5. Now same process is repeated using PB ratio as well 

6. Backtest strategy for PE + PB 
    Enter on buy signal and stay invested until the sell signal
    2 Types of returns are calculated, strategy and market. Strategy returns are based on the buy and sell signals which are generated using PE and PB as thresholds.
    Position gets active when the signal is triggered. 
    On the other hand Market returns are calculated using simple buy and hold, no signals are used.
    These returns are then used to calculate performance metrics such as ROI, Sharpe Ratio, MDD, ROI to MDD.
    Following is the description of the signals:
        1. Buy : 1 ( When PE , PB < P10 )
        2. Sell : -1 ( When PE , PB > P90 )
        3. Hold : 0

7. The graph is then plotted after downloading the S&P 500 file. 
    ( A small part in the code is added before plotting, In order to ensure all values are numeric, errors="coerce" converts non numeric values to Nan. We are doing this to avoid errors during cumulative returns calculation. )
