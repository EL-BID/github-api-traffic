from app import db, Repos, CloneSummary, CloneHistory, RepoViewsSummary, RepoViewsHistory
from utils.scripts import GetRepos, GetTraffic, GetAccessToken, GetViews
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


    def UpdateClonesSummary():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        for repo in repos:
            traffic = GetTraffic(token, repo.name)
            for t in traffic:
                try:
                    row = CloneSummary.query.filter_by(repo_name=repo.name).first()
                    old_clone = row.clone_count
                    old_clone_unique = row.clone_count_unique
                    actual_clone = t["count"]
                    actual_clone_unique = t["uniques"]
                    count = actual_clone - old_clone
                    count_unique = actual_clone_unique - old_clone_unique
                    row.clone_count = count + actual_clone
                    row.clone_count_unique = count_unique + actual_clone_unique
                    db.session.commit()
                except:
                    db.session.add(
                        CloneSummary(repo.name, t["count"], t["uniques"]))
                    db.session.commit()


    def UpdateClonesHistory():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        for repo in repos:
            traffic = GetTraffic(token, repo.name)
            for t in traffic:
                for clone in t["clones"]:
                    try:
                        db.session.add(CloneHistory(repo.name, clone["timestamp"], clone["count"],
                                                    clone["uniques"]))
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        pass


    def UpdateViewsSummary():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        for repo in repos:
            traffic = GetViews(token, repo.name)
            for t in traffic:
                try:
                    row = RepoViewsSummary.query.filter_by(repo_name=repo.name).first()
                    old_view = row.view_count
                    old_view_unique = row.view_count_unique
                    actual_view = t["count"]
                    actual_view_unique = t["uniques"]
                    count = actual_view - old_view
                    count_unique = actual_view_unique - old_view_unique
                    row.view_count = count + actual_view
                    row.view_count_unique = count_unique + actual_view_unique
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.add(
                        RepoViewsSummary(repo.name, t["count"], t["uniques"]))
                    db.session.commit()


    def UpdateViewsHistory():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        for repo in repos:
            traffic = GetViews(token, repo.name)
            for t in traffic:
                for view in t["views"]:
                    try:
                        db.session.add(RepoViewsHistory(repo.name, view["timestamp"], view["count"],
                                                    view["uniques"]))
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        pass
