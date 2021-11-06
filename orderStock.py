from login import login
import time
from livePrice import livePrice
from datetime import datetime
import schedule
import time
from pytz import timezone

rs = login()

TICKER = "UPRO"
ORDER_PRICE = 134
tradeValue = 100

print(TICKER, "limit: ", str(ORDER_PRICE), " price: " + str(tradeValue))
# condition
HOLD_STATE = False # False means sold out, True means hold 

def job():
    # price
    actualPrice = livePrice(TICKER)
    timenow = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')

    if actualPrice > ORDER_PRICE:
        print( timenow + ": $" + str(actualPrice) + " > " + "$" + str(ORDER_PRICE))
    else:
        print( timenow + ": $" + str(actualPrice) + " < " + "$" + str(ORDER_PRICE))

    # buy
    if HOLD_STATE == False and actualPrice > ORDER_PRICE : 
        HOLD_STATE = True
        res= rs.order_buy_crypto_by_price(TICKER, tradeValue)
        print(res)

    # sell
    if HOLD_STATE == True and actualPrice < ORDER_PRICE: 
        HOLD_STATE = False
        res= rs.order_sell_crypto_by_price(TICKER, tradeValue)
        print(res)


# schedule.every(2).seconds.do(job)
schedule.every(1).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)


