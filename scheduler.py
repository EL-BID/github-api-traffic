from apscheduler.schedulers.blocking import BlockingScheduler
from updates import UpdateRepos, UpdateClonesSummary, UpdateClonesHistory, UpdateViewsSummary, UpdateViewsHistory, \
    UpdateRefSources, UpdatePaths, UpdateForks
from app import app
from flask import Flask

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', hours=19)
def job1():
    with app.app_context():
        out = UpdateRepos()
        print(out)


@scheduler.scheduled_job('interval', hours=12)
def job2():
    with app.app_context():
        out = UpdateClonesSummary()
        print(out)


@scheduler.scheduled_job('interval', hours=13)
def job3():
    with app.app_context():
        out = UpdateClonesHistory()
        print(out)


@scheduler.scheduled_job('interval', hours=14)
def job4():
    with app.app_context():
        out = UpdateViewsSummary()
        print(out)


@scheduler.scheduled_job('interval', hours=15)
def job5():
    with app.app_context():
        out = UpdateViewsHistory()
        print(out)


@scheduler.scheduled_job('interval', hours=16)
def job6():
    with app.app_context():
        out = UpdateRefSources()
        print(out)


@scheduler.scheduled_job('interval', hours=17)
def job7():
    with app.app_context():
        out = UpdatePaths()
        print(out)


@scheduler.scheduled_job('interval', hours=18)
def job8():
    with app.app_context():
        out = UpdateForks()
        print(out)


scheduler.start()
