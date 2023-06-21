from apscheduler.schedulers.blocking import BlockingScheduler
from updates import UpdateRepos, UpdateClonesSummary, UpdateClonesHistory, UpdateViewsSummary, UpdateViewsHistory, \
    UpdateRefSources, UpdatePaths, UpdateForks
from app import app
from flask import Flask

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', hours=24)
def job1():
    with app.app_context():
        out = UpdateRepos()
        print(out)



@scheduler.scheduled_job('interval', hours=24)
def job2():
    with app.app_context():
        out = UpdateClonesSummary()
        print(out)


@scheduler.scheduled_job('interval', hours=24)
def job3():
    with app.app_context():
        out = UpdateClonesHistory()
        print(out)


@scheduler.scheduled_job('interval', hours=24)
def job4():
    with app.app_context():
        out = UpdateViewsSummary()
        print(out)


@scheduler.scheduled_job('interval', hours=24)
def job5():
    with app.app_context():
        out = UpdateViewsHistory()
        print(out)


@scheduler.scheduled_job('interval', hours=24)
def job6():
    with app.app_context():
        out = UpdateRefSources()
        print(out)


@scheduler.scheduled_job('interval', hours=24)
def job7():
    with app.app_context():
        out = UpdatePaths()
        print(out)

@scheduler.scheduled_job('interval', hours=24)
def job8():
    with app.app_context():
        out = UpdateForks()
        print(out)

scheduler.start()
