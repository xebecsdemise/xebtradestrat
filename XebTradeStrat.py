# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from typing import Dict, List
from functools import reduce
from pandas import DataFrame
import numpy as np
# --------------------------------

import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


def bollinger_bands(stock_price, window_size, num_of_std):
    rolling_mean = stock_price.rolling(window=window_size).mean()
    rolling_std = stock_price.rolling(window=window_size).std()
    lower_band = rolling_mean - (rolling_std * num_of_std)

    return rolling_mean, lower_band


class XebTradeStrat(IStrategy):
    minimal_roi = {
    #    "0": 0.0125
      "0": 0.99
    }

    stoploss = -0.05
    timeframe = '1m'
    trailing_stop = True
    trailing_only_offset_is_reached = True
    trailing_stop_positive_offset = 0.00375  # Trigger positive stoploss once crosses above this percentage
    trailing_stop_positive = 0.00175 # Sell asset if it dips down this much


    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # mid, lower = bollinger_bands(dataframe['close'], window_size=40, num_of_std=2)
        # dataframe['mid'] = np.nan_to_num(mid)
        # dataframe['lower'] = np.nan_to_num(lower)
        # dataframe['bbdelta'] = (dataframe['mid'] - dataframe['lower']).abs()
        # dataframe['pricedelta'] = (dataframe['open'] - dataframe['close']).abs()
        # dataframe['closedelta'] = (dataframe['close'] - dataframe['close'].shift()).abs()
        # dataframe['tail'] = (dataframe['close'] - dataframe['low']).abs()
        dataframe['ema5'] = ta.EMA(dataframe, timeperiod=5)
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema30'] = ta.EMA(dataframe, timeperiod=30)
        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # dataframe['lower'].shift().gt(0) &
                # dataframe['bbdelta'].gt(dataframe['close'] * 0.008) &
                # dataframe['closedelta'].gt(dataframe['close'] * 0.0175) &
                # dataframe['tail'].lt(dataframe['bbdelta'] * 0.25) &
                # dataframe['close'].lt(dataframe['lower'].shift()) &
                # dataframe['close'].le(dataframe['close'].shift())
            ),
            'buy'] = 1
        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        no sell signal
        """
        dataframe.loc[:, 'sell'] = 0
        return dataframe