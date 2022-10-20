from db import db, Repo
from utils.scripts import GetTraffic, GetAccessToken, GetInstallations, GetRepos
import json


def UpdateRepos():
    repos = GetRepos()
    for repo in repos:
        if not Repo.query.filter_by(name=repo["name"]).first():
            db.session.add(Repo(repo["name"]))
            db.session.commit()