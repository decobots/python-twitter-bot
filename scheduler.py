from apscheduler.schedulers.blocking import BlockingScheduler
from main import heroku_main

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=3)
def timed_job():
    heroku_main()


scheduler.start()
