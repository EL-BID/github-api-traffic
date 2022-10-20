from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_migrate import Migrate


app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://lxjuedczmoskik:077885ca387faed49dd60a9f9f618b63d0396a4d8169dbf8aa54934748482a5c@ec2-54-80-123-146.compute-1.amazonaws.com:5432/duf72gsntfcng'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db = SQLAlchemy()


class Repo(db.Model):
    __tablename__ = 'repos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.relationship('Traffic', backref='repo', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Repo %r>' % self.name


# class Clone(db.Model):
#     __tablename__ = 'clones'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     timestamp = db.Column(db.DateTime)
#     count = db.Column(db.Integer)
#     uniques = db.Column(db.Integer)
#
#     def __init__(self, timestamp, count, uniques):
#         self.timestamp = timestamp
#         self.count = count
#         self.uniques = uniques
#
#     def __repr__(self):
#         return '<Clones %r>' % self.id


class Traffic(db.Model):
    __tablename__ = "traffic"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_id = db.Column(db.Integer, db.ForeignKey('repos.id'), nullable=False)
    clone_count = db.Column(db.Integer)
    clone_count_unique = db.Column(db.Integer)

    def __init__(self, repo, datetime, clone_count, clone_count_unique):
        self.repo = repo
        self.datetime = datetime
        self.clone_count = clone_count
        self.clone_count_unique = clone_count_unique

    def __repr__(self):
        return '<Repo %r>' % self.repo
