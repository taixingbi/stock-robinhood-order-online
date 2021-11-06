import schedule
import time

def job():
    print("job")

# schedule.every(2).seconds.do(job)
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)