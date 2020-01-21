import ccxt
import pandas as pd

"""
Exchange data uses ccxt to get price data from different exchanges.
The exchanges used are Binance, Bittrex, Bitfinex, Kraken and Kucoin
"""

class ExchangeData():
    def __init__(self):
        #try except
        #Initiate exchange data with objects for each exchange
        binance = ccxt.binance()
        bittrex = ccxt.bittrex()
        bitfinex = ccxt.bitfinex()
        kraken = ccxt.kraken()
        kucoin = ccxt.kucoin()
        #Dictionary with the ccxt objects
        self.exchanges = {'binance': binance, 'bittrex': bittrex, 'bitfinex': bitfinex, 'kraken': kraken, 'kucoin': kucoin}
        #Get a list of tickers from Binance exchange to use throughout
        self.ticker_list = []
        self.get_tickers_list()
        #CREATE A DATAFRAME FOR THE PRICE AND VOLUME DATA
        self.volume = pd.DataFrame(index=self.ticker_list, columns= list(self.exchanges.keys()))
        self.pricedf = pd.DataFrame(index=self.ticker_list, columns= list(self.exchanges.keys()))
        self.spread = pd.DataFrame(index=self.ticker_list, columns= list(self.exchanges.keys()))

    """Calculate Bid Offer Spread Percentage"""
    def spread_percentage(self, bid, ask):
        spread_perc = (ask-bid)/bid
        return spread_perc

    """Get a list of tickers from Binance to use throughout"""
    def get_tickers_list(self):
        for t in self.exchanges['binance'].fetch_tickers():
            self.ticker_list.append(t)

    """Get price and volume data and store it in dataframes"""
    def get_all_prices(self):
        #put fetch tickers in list for each exchange and extract the data
        for nm in self.exchanges:
            all_prices = self.exchanges[nm].fetch_tickers()
            #Iterate over each ticker and get information if it is available
            for tick in self.ticker_list:
                vol = 0
                try:
                    bid = all_prices[tick]['bid']
                    ask = all_prices[tick]['ask']
                    self.pricedf[nm][tick] = bid
                    vol = all_prices[tick]['baseVolume']
                    self.volume[nm][tick] = vol
                    self.spread[nm][tick] = self.spread_percentage(bid, ask)
                except:
                    self.pricedf[nm][tick] = None
                    self.volume[nm][tick] = 0
                    self.spread[nm][tick] = 0
                    continue


##Double buying price determine
    # def coin_btc_eth(pr, ex,coin):
    #     double_buy = None
    #     if pr[ex+'-'+coin+'/ETH'] != None and pr[ex+'-ETH/BTC'] != None:
    #         double_buy =  pr[ex+'-ETH/BTC'] / pr[ex+'-'+coin+'/ETH']
    #
    #     return double_buy
