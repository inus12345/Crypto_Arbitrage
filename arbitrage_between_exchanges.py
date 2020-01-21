import exchange_data
import price_data
import time
from datetime import datetime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

print("##############################################")
print("Current Time =", current_time)
print("##############################################")

#Manipulate price data
getPriceData = price_data.PriceData()
getPriceData.remove_none(2) #remove prices with not enough data
#getPriceData.print_prices()
getPriceData.determine_arbitrage()





#    time.sleep(1000)
