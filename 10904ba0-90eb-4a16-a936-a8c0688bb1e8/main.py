from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "AAPL"  # Setting the asset to trade

    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        # The data required for the RSI calculation
        return []

    @property
    def interval(self):
        return "1day"  # Using daily data for RSI calculation

    def run(self, data):
        # Initialize the target allocation with no investment
        allocation_dict = {self.ticker: 0.0}
        
        # Calculate RSI for the specified asset
        rsi_values = RSI(self.ticker, data["ohlcv"], 14)  # 14 period RSI
        
        if rsi_values is not None and len(rsi_values) > 0:
            current_rsi = rsi_values[-1]
            
            # If the RSI is below 40, it's considered oversold, signal to buy (allocate 100%)
            if current_rsi < 40:
                allocation_dict[self.ticker] = 1.0  # Buy
                log(f"RSI below 40, buying {self.ticker}")
                
            # If the RSI is above 60, it's considered overbought, signal to sell (allocate 0%)
            elif current_rsi > 60:
                allocation_dict[self.ticker] = 0.0  # Sell
                log(f"RSI above 60, selling {self.ticker}")
                
            # Otherwise, do not change the allocation
            else:
                log(f"RSI is {current_rsi}, holding {self.ticker}")
        
        return TargetAllocation(allocation_dict)