import schedule
import time
from main import run_pipeline

schedule.every().day.at("09:20").do(run_pipeline)

while True:
    schedule.run_pending()
    time.sleep(60)
