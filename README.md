# Stock-Market-Trend-Forecasting
A time series prediction tool using fuzzy logic and fuzzy information
retrieval system to predict the trends in stock markets using Python, using metrics
such as RSI, common candlestick patterns, NIFTY50/ BSI OHLC data.

Paper : https://drive.google.com/open?id=1O9l39u5vvq-1GljLf930MpLsjXWdMXw8

## ABSTRACT

The time series is an efficient way to study about the existing trends and then take future decisions
according to the results obtained during the analysis. Stock market is one such platform where time
series is of utmost use and importance in order to predict the future market trend. Even though stock
markets have a high level of entropy and randomness about them , still they are somewhat time driven
and by sentiments of market players. This leads to the task of modelling of the stock market which is a
difficult task as it includes the raw, random data and the hidden market sentiment. To solve this problem,
we convert the time series consisting of raw data of stock markets having Open, High, Low, Close values
into a fuzzy linguistic time series. Information Retrieval systems are used to find the most relevant docu-
ments based upon a query. Fuzzy Information Retrieval Systems use this logic and find the most relevant
document based upon the tf-idf scores of values in the documents. The novelty of the approach followed
here is that we include the different kinds of candlesticks that are used to quantify the trend reversals in
a market (for example - hanging man, kicking bullish candlestick) and the relative strength index (RSI)
values (which signify momentum of the market) to our list of parameters. These added factors to the
fuzzy representation of trends in our documents makes the future trend prediction more accurate.
