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

## Methodology

The data in the time series
that we have used is represented by candlesticks in the form of Open, High, Low, Close values as well
as the properties of the candlesticks. Candlesticks are useful for representing the discrete data in an
understandable form. There exist some candlesticks for identifying particular patterns of the market
which helps to predict the future trends in the market (such as trend reversals).
We then created fuzzy rules on the basis of cluster of days , each set of 5 consecutive days being one
cluster. This helps us to create more number of clusters and expanding our document base. After that
we normalised the discrete value by defining some functions which quantify the properties of candle-
sticks and trends. On the basis of this data, we derived membership functions through which we created
fuzzified data. With the help of this fuzzy data, we then created fuzzy rules through which we were
able to realise the different candlestick patterns which exist in the stock market. Along with momentum
of the market, we used all of these characteristics to create documents for each cluster. Through fuzzy
information retrieval systems, we were able to rank each term according to its relevance in the pool of
documents representing the future trend. The query with the highest relevance is matched and we finally
get the future trend of the market along with the fuzzy documents representing the strength of our pre-
diction.
