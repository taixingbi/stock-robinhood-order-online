from datetime import datetime
import time

from yahoo_fin import stock_info as si
import cryptocompare

CRYPTO= ["BTC", "DOGE", "ETH"]

def livePrice(ticker):
    # print("livePrice")
    if ticker in CRYPTO: 
        response= cryptocompare.get_price(ticker, currency='USD') 
        live_price= response[ticker]['USD']
    else:
        live_price= si.get_live_price(ticker) 
        live_price= live_price.item() # numpy to float

    # timestamp_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # timestamp = time.time()
    return live_price

if __name__ == "__main__":
    price= livePrice("BTC") 
    print(price)