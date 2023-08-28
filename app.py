from flask import Flask, Response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgresql://pgotxbkrrfgqrq:2ae7eb5adca4c1c1b9700b2d15b8ba3a6adc9acf2f218318b8748bc1b7da9e32@ec2-35-172-26-41.compute-1.amazonaws.com:5432/d24k43j83qm0uv"
db = SQLAlchemy(app)
app.config['JSON_SORT_KEYS'] = False
migrate = Migrate(app, db)


class Repos(db.Model):
    __tablename__ = 'repos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Repo %r>' % self.name


class CloneSummary(db.Model):
    __tablename__ = "clone_summary"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.String(200), db.ForeignKey('repos.name'), nullable=False, unique=True)
    clone_count = db.Column(db.Integer)
    clone_count_unique = db.Column(db.Integer)

    def __init__(self, repo_name, clone_count, clone_count_unique):
        self.repo_name = repo_name
        self.clone_count = clone_count
        self.clone_count_unique = clone_count_unique

    def __repr__(self):
        return '<Repo %r>' % self.repo_name


class CloneHistory(db.Model):
    __tablename__ = "clone_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.String(200), db.ForeignKey('repos.name'))
    timestamp = db.Column(db.DateTime, nullable=False)
    clone_count = db.Column(db.Integer)
    clone_count_unique = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('timestamp', 'repo_name', name='_repo_timestamp_uc'),)

    def __init__(self, repo_name, timestamp, clone_count, clone_count_unique):
        self.repo_name = repo_name
        self.timestamp = timestamp
        self.clone_count = clone_count
        self.clone_count_unique = clone_count_unique

    def __repr__(self):
        return '<Repo %r>' % self.repo_name


class RepoViewsSummary(db.Model):
    __tablename__ = "repo_views"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.String(200), db.ForeignKey('repos.name'))
    view_count = db.Column(db.Integer)
    view_count_unique = db.Column(db.Integer)

    def __init__(self, repo_name, view_count, view_count_unique):
        self.repo_name = repo_name
        self.view_count = view_count
        self.view_count_unique = view_count_unique

    def __repr__(self):
        return '<Repo %r>' % self.repo_name


class RepoViewsHistory(db.Model):
    __tablename__ = "repo_views_history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.String(200), db.ForeignKey('repos.name'))
    timestamp = db.Column(db.DateTime, nullable=False)
    view_count = db.Column(db.Integer)
    view_count_unique = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('timestamp', 'repo_name', name='_repo_view_timestamp_uc'),)

    def __init__(self, repo_name, timestamp, view_count, view_count_unique):
        self.repo_name = repo_name
        self.timestamp = timestamp
        self.view_count = view_count
        self.view_count_unique = view_count_unique

    def __repr__(self):
        return '<Repo %r>' % self.repo_name


class RefSources(db.Model):
    __tablename__ = "ref_sources"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.String(200), db.ForeignKey('repos.name'))
    source = db.Column(db.String(200))
    count = db.Column(db.Integer)
    unique = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('repo_name', 'source', name='_repo_source_uc'),)

    def __init__(self, repo_name, source, count, unique):
        self.repo_name = repo_name
        self.source = source
        self.count = count
        self.unique = unique

    def __repr__(self):
        return '<Repo %r>' % self.repo_name


class RefPaths(db.Model):
    __tablename__ = "ref_paths"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.String(200), db.ForeignKey('repos.name'))
    path = db.Column(db.String(200))
    title = db.Column(db.String(200))
    count = db.Column(db.Integer)
    unique = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('repo_name', 'path', name='_repo_path_uc'),)

    def __init__(self, repo_name, path, title, count, unique):
        self.repo_name = repo_name
        self.path = path
        self.title = title
        self.count = count
        self.unique = unique

    def __repr__(self):
        return '<Repo %r>' % self.repo_name

class Forks(db.Model):
    __tablename__ = "forks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(200),  unique=True)
    repo_name = db.Column(db.String(200), db.ForeignKey("repos.name"))

    def __init__(self, url, repo_name):
        self.url = url
        self.repo_name = repo_name

    def __repr__(self):
        return f'<Fork {self.url}>'


# Code
@app.route('/')
def API():
    data = []
    for repo in Repos.query.all():
        clones = CloneSummary.query.filter_by(repo_name=repo.name).first()
        views = RepoViewsSummary.query.filter_by(repo_name=repo.name).first()
        history_views = RepoViewsHistory.query.filter_by(repo_name=repo.name).all()
        history_clones = CloneHistory.query.filter_by(repo_name=repo.name).all()
        forks_count = Forks.query.filter_by(repo_name=repo.name).count()
        data.append(
            {"repository": repo.name,
             "traffic":
                 {"clones": {"consolidated": {"count": clones.clone_count,
                                              "unique": clones.clone_count_unique
                                              },
                             "history": [{"timestamp": str(clone.timestamp),
                                          "count": clone.clone_count,
                                          "unique": clone.clone_count_unique,
                                          } for clone in history_clones]

                             },
                    "views": {"consolidated": {"count": views.view_count,
                                             "unique": views.view_count_unique
                                             },
                            "history": [{"timestamp": str(view.timestamp),
                                         "count": view.view_count,
                                         "unique": view.view_count_unique,
                                         } for view in history_views]

                            },
                "referrers": [{"source": ref.source,
                                 "count": ref.count,
                                 "unique": ref.unique,
                                 } for ref in RefSources.query.filter_by(repo_name=repo.name).all()],
                "paths": [{"path": ref.path,
                             "title": ref.title,
                             "count": ref.count,
                             "unique": ref.unique,
                             } for ref in RefPaths.query.filter_by(repo_name=repo.name).all()],
                "forks": [
                        {
                            "url": fork.url
                        } for fork in Forks.query.filter_by(repo_name=repo.name).all()
                    ],
                "forks_count_total": forks_count  # Add forks count to the response
                  }
             }
        )

    ##return json with spaces pretty format
    return Response(json.dumps(data, indent=4, sort_keys=True), mimetype='application/json')


if __name__ == '__main__':
    app.run()
