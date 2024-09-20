from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    
    @property
    def assets(self):
        # Strategy only involves trading AAPL
        return ["AAPL"]

    @property
    def interval(self):
        # Trading on an hourly interval
        return "1hour"

    def run(self, data):
        # Initialize AAPL stake based on the strategy condition
        aapl_stake = None

        # Extracting close prices for AAPL to calculate EMA and SMA
        close_prices = [i["AAPL"]["close"] for i in data["ohlcv"] if "AAPL" in i]

        # EMA and SMA calculations
        ema_7 = EMA("AAPL", data["ohlcv"], length=7)
        sma_14 = SMA("AAPL", data["ohlcv"], length=14)

        # Ensure we have enough data points to calculate both EMA and SMA
        if len(ema_7) > 0 and len(sma_14) > 0:
            ema_current = ema_7[-1]
            sma_current = sma_14[-1]
            ema_previous = ema_7[-2]
            sma_previous = sma_14[-2]

            # Buy condition: EMA crosses above SMA
            if ema_previous < sma_previous and ema_current > sma_current:
                log("Condition met for buying.")
                aapl_stake = 1  # Buy (or hold maximum position in) AAPL
            
            # Sell condition: EMA crosses below SMA
            elif ema_previous > sma_previous and ema_current < sma_current:
                log("Condition met for selling.")
                aapl_stake = 0  # Sell all AAPL positions

        # In case there's no explicit buy or sell signal, do not change the current allocation.
        if aapl_stake is None:
            log("No trading signal. Holding position.")
            return TargetAllocation({})  # Returns an empty target allocation to indicate holding the position.

        # Returning AAPL stake based on the conditions met above
        return TargetAllocation({"AAPL": aapl_stake})