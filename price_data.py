import ccxt
import pandas as pd
import exchange_data
import numpy as np
import itertools

class PriceData(exchange_data.ExchangeData):
    def __init__(self):
        super().__init__()
        self.get_all_prices()


    def remove_none(self, degree_none=2):
        self.pricedf.insert(5, 'status', 1, True)

        for i in range(self.pricedf['binance'].count()):
            countNone = 0
            for k in self.pricedf.iloc[i]:
                if k == None:
                    countNone += 1
            if countNone > degree_none:
                self.pricedf['status'][i] = 0

        self.pricedf = self.pricedf[self.pricedf.status == 1]

#Take as input the cut off volume for an arbitrage strategy. Default is 100
    def price_difference_matrix(self, trading_pair, volCut = 100):
        exchangeNames = list(self.exchanges.keys())
        numEx = len(exchangeNames)
        arbitrage_matrix = np.empty((numEx,numEx))

        arbitrage_trigger = 0

        for (x,i) in zip(exchangeNames, range(numEx)):
            for (y,j) in zip(exchangeNames, range(numEx)):
                priceEx_x = self.pricedf[x][trading_pair]
                priceEx_y = self.pricedf[y][trading_pair]
                percentage = 0

                if priceEx_x == None or priceEx_y == None:
                    percentage = 0
                    arbitrage_matrix[i][j] = 0
                elif priceEx_x == 0 or priceEx_y == 0:
                    percentage = 0
                    arbitrage_matrix[i][j] = 0
                else:
                    try:
                        percentage = ((priceEx_x-priceEx_y)/priceEx_x)*100
                        if percentage != 0:
                            arbitrage_matrix[i][j]=round(percentage, 2)
                        else:
                            arbitrage_matrix[i][j] = 0
                    except:
                        print('Except')
                        print(priceEx_x)
                        print(priceEx_y)
                        arbitrage_matrix[i][j]=0

                if (percentage > 2 and percentage < 10) or (percentage < -2 and percentage > -10):
                    if self.volume[x][trading_pair] > volCut and self.volume[y][trading_pair] > volCut:
                        if self.spread[x][trading_pair] < 0.05 and self.spread[y][trading_pair] < 0.05:
                            arbitrage_trigger += 1
##If the arbitrage trigger is true then the arbitrage matrix is printed
        if arbitrage_trigger > 2:
            print('==========================')
            print(trading_pair)
            print('==========================')
            print('binance | bittrex | bitfinex | kraken | kucoin')
            print(arbitrage_matrix)


    def determine_arbitrage(self):
        for tick in list(self.pricedf.index.values):
            self.price_difference_matrix(tick)

    def print_prices(self):
        print(self.pricedf)
        print(self.volume)
