from login import login
import time
from livePrice import livePrice
from datetime import datetime
# from schedule import every, repeat, run_pending
import schedule

import time
from pytz import timezone
from logger import logger

# @repeat(every(1).minutes)
# @repeat(every(2).seconds, HOLD_STATE)

class Trade:
    def __init__(self):
        self.logger = logger("NRDS.log")
        self.rs = login()
        self.TICKER = "NRDS"
        self.ORDER_PRICE = None
        self.share = 33
        self.rate = 0.92
        self.HOLD_STATE = "Ready To BUY"  # "Ready To SELL"
        self.peak = 0
        self.equity = 0.0

    def printLog(self, actualPrice, ORDER_PRICE):
        timenow = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
        
        def printStr( operater ):
            return timenow + " " + str(self.HOLD_STATE) + " peak(" +  str(self.peak) + ") $" + str(actualPrice) + " " + operater + " $" + str(self.ORDER_PRICE) +  "  equity: " + str(self.equity)

        if actualPrice > ORDER_PRICE: return printStr(">")
        else: return printStr("<")

    def job(self):
        actualPrice = livePrice(self.TICKER)
        self.peak = max(self.peak, actualPrice)
        self.ORDER_PRICE = int(self.peak * self.rate)

        print( self.printLog(actualPrice, self.ORDER_PRICE) )
        self.logger.critical( self.printLog(actualPrice, self.ORDER_PRICE) )

        # buy
        if self.HOLD_STATE == "Ready To BUY" and actualPrice > self.ORDER_PRICE : 
            self.HOLD_STATE = "Ready To SELL"
            res= self.rs.order_buy_market(self.TICKER, self.share)
            print(res)
            self.equity -= float( res['price'] )
            self.logger.critical( self.printLog(actualPrice, self.ORDER_PRICE) )

        # sell
        if self.HOLD_STATE == "Ready To SELL" and actualPrice < self.ORDER_PRICE: 
            self.HOLD_STATE = "Ready To BUY"
            res= self.rs.order_sell_market(self.TICKER, self.share)
            print(res)
            self.equity += float( res['entered_price'] )
            self.logger.critical( self.printLog(actualPrice, self.ORDER_PRICE) )


if __name__ == '__main__':
    Trade = Trade()
    # schedule.every(59).minutes.do(Trade.job)
    schedule.every(30).seconds.do(Trade.job)

    while True:
        schedule.run_pending()
        time.sleep(1)

