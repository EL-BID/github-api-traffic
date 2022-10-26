from app import db, Repos, Traffic
from utils.scripts import GetTraffic, GetAccessToken, GetInstallations, GetRepos
import json
from app import app

with app.app_context():
    def UpdateRepos():
        repos = GetRepos()
        for repo in repos:
            try:
                db.session.add(Repos(repo["id"], repo["name"]))
                db.session.commit()
            except:
                pass