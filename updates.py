from app import db, Repos, CloneSummary, CloneHistory, RepoViewsSummary, RepoViewsHistory, RefSources, RefPaths, Forks
from utils.scripts import GetRepos, GetTraffic, GetAccessToken, GetViews, GetRefSources, GetRefPaths, GetForks
import json
from app import app

with app.app_context():
    def UpdateRepos():
        page = 1
        per_page = 30
        while True:
            repos = GetRepos(page=page, per_page=per_page)
            if not repos:
                break
            for repo in repos:
                try:
                    db.session.add(Repos(repo["id"], repo["name"]))
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    continue
            page += 1


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

                    if actual_clone >= old_clone:
                        count = actual_clone - old_clone
                    else:
                        count = actual_clone

                    if actual_clone_unique >= old_clone_unique:
                        count_unique = actual_clone_unique - old_clone_unique
                    else:
                        count_unique = actual_clone_unique

                    row.clone_count = count + old_clone
                    row.clone_count_unique = count_unique + old_clone_unique
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.add(CloneSummary(repo.name, t["count"], t["uniques"]))
                    db.session.commit()
                    continue



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
                        continue


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

                    if actual_view >= old_view:
                        count = actual_view - old_view
                    else:
                        count = actual_view

                    if actual_view_unique >= old_view_unique:
                        count_unique = actual_view_unique - old_view_unique
                    else:
                        count_unique = actual_view_unique

                    row.view_count = count + old_view
                    row.view_count_unique = count_unique + old_view_unique
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.add(RepoViewsSummary(repo.name, t["count"], t["uniques"]))
                    db.session.commit()
                    continue



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
                        continue


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

                        if actual_ref >= old_ref:
                            count = actual_ref - old_ref
                        else:
                            count = actual_ref

                        if actual_ref_unique >= old_ref_unique:
                            count_unique = actual_ref_unique - old_ref_unique
                        else:
                            count_unique = actual_ref_unique

                        row.count = count + old_ref
                        row.unique = count_unique + old_ref_unique
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.add(
                            RefSources(repo.name, ref["referrer"], ref["count"], ref["uniques"]))
                        db.session.commit()
                        continue



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

                        if actual_path >= old_path:
                            count = actual_path - old_path
                        else:
                            count = actual_path

                        if actual_path_unique >= old_path_unique:
                            count_unique = actual_path_unique - old_path_unique
                        else:
                            count_unique = actual_path_unique

                        row.count = count + old_path
                        row.unique = count_unique + old_path_unique
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.add(
                            RefPaths(repo.name, path["path"], path["title"], path["count"], path["uniques"]))
                        db.session.commit()
                        continue

    def UpdateForks():
        token = GetAccessToken()
        token = json.loads(token)["token"]
        repos = Repos.query.all()
        print(token, repos)
        for repo in repos:
            forks = GetForks(token, repo)
            print("forks")
            print(forks)
            for fork in forks:
                try:
                    fork_obj = Forks(url=fork["html_url"], repo_name=repo)
                    db.session.add(fork_obj)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()
                    continue

