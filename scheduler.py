from apscheduler.schedulers.blocking import BlockingScheduler
from updates import UpdateRepos, UpdateClonesSummary, UpdateClonesHistory, UpdateViewsSummary, UpdateViewsHistory, \
    UpdateRefSources, UpdatePaths
from app import app

with app.app_context():

    class Config:
        SCHEDULER_API_ENABLED = True


    scheduler = BlockingScheduler()

    @scheduler.scheduled_job('cron', day_of_week='mon-sun', hour=0, minute=0)
    def job1():
        out = UpdateRepos()
        print(out)

    def job2():
        out = UpdateClonesSummary()
        print(out)

    def job3():
        out = UpdateClonesHistory()
        print(out)

    def job4():
        out = UpdateViewsSummary()
        print(out)

    def job5():
        out = UpdateViewsHistory()
        print(out)

    def job6():
        out = UpdateRefSources()
        print(out)

    def job7():
        out = UpdatePaths()
        print(out)


    scheduler.start()
