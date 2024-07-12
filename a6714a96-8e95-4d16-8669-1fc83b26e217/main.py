#Type code here
from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB
import os
import logging

logger = logging.getLogger("main.py")


class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["SPY"]

    @property
    def interval(self):
        return "1hour"

    def run(self, data_functions):
        current_working_directory = os.getcwd()
        raise Exception(current_working_directory)
        logger.info("current_working_directory" + current_working_directory)
        keys_file = open("keys.json", "r")
        logger.info(keys_file.read())
        data = data_functions["ohlcv"]

        spy_20_ma = SMA("SPY", data, 20)
        spy_10_ma = SMA("SPY", data, 10)
        spy_10_rsi = RSI("SPY", data, 10)

        if None in [spy_20_ma, spy_10_ma, spy_10_rsi]:
            return None

        spy_stake = 0
        if spy_10_rsi[-1]<60 and spy_10_ma[-1]>spy_20_ma[-1]:
            spy_stake = 1

        return TargetAllocation({"SPY": spy_stake})