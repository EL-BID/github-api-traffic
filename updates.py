from app import db, Repos, Traffic
from utils.scripts import GetRepos, GetTraffic, GetAccessToken
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


    def UpdateTraffic():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        for repo in repos:
            traffic = GetTraffic(token, repo.name)
            for t in traffic:
                #get actual traffic count and unique values and compare with the ones in the database
                # do total=actual-old and unique=actual-old
                # save total as count and unique as count_unique
                try:
                    old_clon = Traffic.query.filter_by(repo_name=repo.name).first().clone_count
                    old_clon_unique = Traffic.query.filter_by(repo_name=repo.name).first().clone_count_unique
                    actual_clon = t["count"]
                    actual_clon_unique = t["uniques"]
                    count = actual_clon - old_clon
                    count_unique = actual_clon_unique - old_clon_unique
                    db.session.update(Traffic(repo.id, repo.name, count+actual_clon, count_unique+actual_clon_unique))
                    db.session.commit()
                except:
                    pass
