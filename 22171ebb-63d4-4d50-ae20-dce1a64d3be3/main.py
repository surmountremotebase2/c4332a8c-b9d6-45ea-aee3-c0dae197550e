#Type code here
from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

from surmount.technical_indicators import RSI
from surmount.data import Ratios

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ("AAPL")
        self.data_list = [Ratios(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        return "1hour"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {i: 1/len(self.tickers) for i in self.tickers}
        ohlcv = data.get("ohlcv")
        ratios = data.get(("ratios","AAPL"))
        log(str(ohlcv))
        log(str(ratios))
        # WRITE STRATEGY LOGIC HERE
        return TargetAllocation(allocation_dict)