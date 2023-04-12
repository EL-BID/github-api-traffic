from app import db, Repos, CloneSummary, CloneHistory, RepoViewsSummary, RepoViewsHistory, RefSources, RefPaths
from utils.scripts import GetRepos, GetTraffic, GetAccessToken, GetViews, GetRefSources, GetRefPaths
import json
from app import app

with app.app_context():
    def UpdateRepos():
        repos = GetRepos()
        for repo in repos:
            try:
                db.session.add(Repos(repo["id"], repo["name"]))
                db.session.commit()
            except Exception as e:
                print(e)
                db.session.rollback()
                return "Failed"


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


    def UpdateRefSources():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        for repo in repos:
            traffic = GetRefSources(token, repo.name)
            for t in traffic:
                for ref in t:
                    try:
                        print(repo.name, ref["referrer"], ref["count"], ref["uniques"])
                        row = RefSources.query.filter_by(repo_name=repo.name, source=ref["referrer"]).first()
                        old_ref = row.count
                        old_ref_unique = row.unique
                        actual_ref = ref["count"]
                        actual_ref_unique = ref["uniques"]
                        count = actual_ref - old_ref
                        count_unique = actual_ref_unique - old_ref_unique
                        row.count = count + actual_ref
                        row.unique = count_unique + actual_ref_unique
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.add(
                            RefSources(repo.name, ref["referrer"], ref["count"], ref["uniques"]))
                        db.session.commit()


    def UpdatePaths():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        for repo in repos:
            paths = GetRefPaths(token, repo.name)
            for t in paths:
                for path in t:
                    try:
                        row = RefPaths.query.filter_by(repo_name=repo.name, source=path["title"]).first()
                        old_path = row.count
                        old_path_unique = row.unique
                        actual_path = path["count"]
                        actual_path_unique = path["uniques"]
                        count = actual_path - old_path
                        count_unique = actual_path_unique - old_path_unique
                        row.count = count + actual_path
                        row.unique = count_unique + actual_path_unique
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.add(
                            RefPaths(repo.name, path["path"], path["title"], path["count"], path["uniques"]))
                        db.session.commit()