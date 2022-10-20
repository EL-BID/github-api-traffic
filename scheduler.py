from apscheduler.schedulers.blocking import BlockingScheduler
from updates import UpdateRepos


class Config:
    SCHEDULER_API_ENABLED = True


scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=3)
def job1():
    out = UpdateRepos()
    print(out)


scheduler.start()
