from apscheduler.schedulers.blocking import BlockingScheduler
from updates import UpdateRepos, UpdateClonesSummary, UpdateClonesHistory, UpdateViewsSummary, UpdateViewsHistory, \
    UpdateRefSources, UpdatePaths
from app import app
from flask import Flask

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def job1():
    with app.app_context():
        out = UpdateRepos()
        print(out)



@scheduler.scheduled_job('interval', minutes=2)
def job2():
    with app.app_context():
        out = UpdateClonesSummary()
        print(out)


@scheduler.scheduled_job('interval', minutes=3)
def job3():
    with app.app_context():
        out = UpdateClonesHistory()
        print(out)


@scheduler.scheduled_job('interval', minutes=4)
def job4():
    with app.app_context():
        out = UpdateViewsSummary()
        print(out)


@scheduler.scheduled_job('interval', minutes=5)
def job5():
    with app.app_context():
        out = UpdateViewsHistory()
        print(out)


@scheduler.scheduled_job('interval', minutes=6)
def job6():
    with app.app_context():
        out = UpdateRefSources()
        print(out)


@scheduler.scheduled_job('interval', minutes=7)
def job7():
    with app.app_context():
        out = UpdatePaths()
        print(out)


scheduler.start()
