import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class MovingAverageCalculator:
    '''Code base for a moving average calculator. Computes moving averages on a time series
    stock price dataset
    Parameters:
    -------------
    prices: str-> The relevant filename containing the preprocessed time series data.'''

    def __init__(self, prices):
        self.prices = prices
        self.__sma = []

    @property
    def sma(self):
        return self.__sma

    def moving_averages(self, window: int, type: str) -> dict:
        '''
        Returns DataFrame of given dataset and the moving averages as specified.
        Parameters:
        -----------------
        window: int -> Moving average window
        type: str -> One of "high", "low", "open" or "close" prices
        :return: Dictionary:
        keys : values
        Data : DataFrame of formatted TS data and moving average values
        Buy_values : Bull values
        Buy_dates : Bull dates
        Sell_values: Bear values
        Sell_dates : Sell dates

        '''
        buy_dates = []
        buy_values = []
        sell_dates = []
        sell_values = []
        results = {}
        for i in range(len(self.prices) - window + 1):
            avg = np.mean(self.prices[type][i:i + window])
            self.__sma.append(avg)
        self.prices = self.prices.iloc[window - 1:]
        for i in range(1, len(self.prices)):
            if self.prices[type].iloc[i - 1] < self.__sma[i - 1] and self.prices[type].iloc[i] > self.__sma[i]:
                buy_dates.append(self.prices.index[i])
                buy_values.append(self.prices[type].iloc[i])
            elif self.prices[type].iloc[i - 1] > self.__sma[i - 1] and self.prices[type].iloc[i] < self.__sma[i]:
                sell_dates.append(self.prices.index[i])
                sell_values.append(self.prices[type].iloc[i])

        self.prices[f"{type} MA {window}"] = self.__sma
        results["Data"] = self.prices
        results["Buy_values"] = buy_values
        results["Buy_dates"] = pd.to_datetime(buy_dates)
        results["Sell_dates"] = pd.to_datetime(sell_dates)
        results["Sell_values"] = sell_values

        return results


def wrangle(key:str, train_size:float= 0.8, file=None, filename=None, *args, **kwargs) -> dict:
    '''Written strictly to deal with data extracted using AlphaVantage API's.
    Not for general use. Designed to deal with stock price data and present it in a usable(DataFrame)
    condition.
    Parameters:
    --------------------
            filename: str -> The file in question. Must be json.
            train_size: float(optional) -> The size of data kept for training
            key: str: The relevant key header in the file

    Returns-> dictionary of training data(closing stock prices) and test data

            '''
    if filename:
        with open(filename) as f:
            data = json.load(f)
    else:
        data = file

    # Identifying relevant keys and values for extraction
    # Conversion of data to a DataFrame and transposition to allow for easier manipulation
    # df_comp = pd.DataFrame(data["Time Series (Daily)"]).T
    df_comp = pd.DataFrame(data[key]).T
    # Conversion of 'Object' types to float
    for i in df_comp.columns:
        df_comp[i] = df_comp[i].astype(float)
    df_comp = df_comp[::-1]

    df_comp.rename(
        columns={"4. close": "close", "1. open": "open", "2. high": "high", "3. low": "low", "5. volume": "volume"},
        inplace=True)
    df = df_comp.copy()
    df["dates"] = df.index
    df_comp["dates"] = df_comp.index

    df.dates = pd.to_datetime(df.dates, yearfirst=True)
    df.set_index("dates", inplace=True)
    df = df.asfreq('b')
    df.fillna(method="ffill", inplace=True)

    df_comp.dates = pd.to_datetime(df_comp.dates, yearfirst=True)
    df_comp.set_index("dates", inplace=True)
    df_comp = df_comp.asfreq('b')
    df_comp.fillna(method="ffill", inplace=True)

    df_ = df_comp.copy()

    #del df["open"], df["high"], df["low"], df["volume"]

    size = int(train_size * len(df))
    df_train = df.iloc[:size]
    df_test = df.iloc[size:]

    frames = {"train": df_train, "test": df_test, "copy": df_}

    return frames

def stock_ticker(ticker):
    API_BASE_URL = f"https: // www.alphavantage.co / query?function = TIME_SERIES_DAILY & symbol = {ticker} & outputsize = compact & apikey"
    return API_BASE_URL

#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=compact&apikey=992C8IN2OQA4ZPF2