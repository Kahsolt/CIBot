#encoding: utf-8
from apscheduler.schedulers.background import BackgroundScheduler
from app.models import *

#
# 定时任务 Scheds
#


scheduler = BackgroundScheduler()
try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()


@scheduler.scheduled_job("cron", minute="*/1")
def doWhat():
    pass
