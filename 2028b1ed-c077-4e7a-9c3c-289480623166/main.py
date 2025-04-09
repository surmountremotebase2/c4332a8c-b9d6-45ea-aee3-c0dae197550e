#Type code here
from surmount.base_class import Strategy, TargetAllocation, backtest
from surmount.technical_indicators import RSI, EMA, SMA, MACD, MFI, BB

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["SWVL"]

    @property
    def interval(self):
        return "1hour"

    def run(self, data_functions):
        data = data_functions["ohlcv"]

        spy_20_ma = SMA("SWVL", data, 20)
        spy_10_ma = SMA("SWVL", data, 10)
        spy_10_rsi = RSI("SWVL", data, 10)

        if None in [spy_20_ma, spy_10_ma, spy_10_rsi]:
            return None

        spy_stake = 0
        if spy_10_rsi[-1]<60 and spy_10_ma[-1]>spy_20_ma[-1]:
            spy_stake = 1

        return TargetAllocation({"SWVL": spy_stake})