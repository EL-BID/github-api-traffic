from apscheduler.schedulers.blocking import BlockingScheduler
from updates import UpdateRepos, UpdateClonesSummary, UpdateClonesHistory, UpdateViewsSummary, UpdateViewsHistory, \
    UpdateRefSources, UpdatePaths
from app import app

with app.app_context():
    class Config:
        SCHEDULER_API_ENABLED = True


    scheduler = BlockingScheduler()


    @scheduler.scheduled_job('interval', hours=20)
    def job1():
        out = UpdateRepos()
        print(out)


    # schedule every minute for testing
    @scheduler.scheduled_job('interval', hours=21)
    def job2():
        out = UpdateClonesSummary()
        print(out)


    @scheduler.scheduled_job('interval', hours=22)
    def job3():
        out = UpdateClonesHistory()
        print(out)


    @scheduler.scheduled_job('interval', hours=23)
    def job4():
        out = UpdateViewsSummary()
        print(out)


    @scheduler.scheduled_job('interval', hours=24)
    def job5():
        out = UpdateViewsHistory()
        print(out)


    @scheduler.scheduled_job('interval', hours=25)
    def job6():
        out = UpdateRefSources()
        print(out)


    @scheduler.scheduled_job('interval', hours=26)
    def job7():
        out = UpdatePaths()
        print(out)


    scheduler.start()
