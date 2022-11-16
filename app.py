from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://lxjuedczmoskik:077885ca387faed49dd60a9f9f618b63d0396a4d8169dbf8aa54934748482a5c@ec2-54-80-123-146.compute-1.amazonaws.com:5432/duf72gsntfcng'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Repos(db.Model):
    __tablename__ = 'repos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return '<Repo %r>' % self.name


class CloneSummary(db.Model):
    __tablename__ = "clone_summary"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.String(80), db.ForeignKey('repos.name'), nullable=False, unique=True)
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
    repo_name = db.Column(db.String(80), db.ForeignKey('repos.name'))
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


# Code
@app.route('/')
def API():
    data = []
    for repo in Repos.query.all():
        clones = CloneSummary.query.filter_by(repo_name=repo.name).first()
        history_clones = CloneHistory.query.filter_by(repo_name=repo.name).all()
        data.append(
            {"Repository": repo.name,
             "Traffic":
                 {"Clones": {"Consolidated": {"Count": clones.clone_count,
                                              "Unique": clones.clone_count_unique
                                              },
                             "History": [{"Count": clone.clone_count,
                                          "Timestamp": clone.timestamp,
                                          "Unique": clone.clone_count_unique,
                                          } for clone in history_clones]

                             }
                  }
             }
        )
    return jsonify(data)


if __name__ == '__main__':
    app.run()
