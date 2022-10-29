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


class Traffic(db.Model):
    __tablename__ = "traffic"
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


# Code
@app.route('/')
def API():
    data = []
    for repo in Repos.query.all():
        traffic = Traffic.query.filter_by(repo_name=repo.name).first()
        data.append(
            {"Repository": repo.name,
             "Traffic":
                 {"Clones": {"Consolidated": {"Count": traffic.clone_count,
                                              "Unique": traffic.clone_count_unique
                                              },
                             "Daily": {"timestamp": "2020-01-01",
                                       "Count": traffic.clone_count,
                                       "Unique": traffic.clone_count_unique
                                       }
                             }
                  }
             }
        )
    return jsonify(data)


if __name__ == '__main__':
    app.run()
