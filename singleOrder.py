from login import login
import time
from livePrice import livePrice

rs = login()

res= rs.order_buy_market("NRDS", str(1))
print(res)