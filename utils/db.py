from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lxjuedczmoskik:077885ca387faed49dd60a9f9f618b63d0396a4d8169dbf8aa54934748482a5c@ec2-54-80-123-146.compute-1.amazonaws.com:5432/duf72gsntfcng'
db = SQLAlchemy(app)


class Clone(db.Model):
    __tablename__ = 'clones'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    count = db.Column(db.Integer)
    uniques = db.Column(db.Integer)

    def __init__(self, timestamp, count, uniques):
        self.timestamp = timestamp
        self.count = count
        self.uniques = uniques

    def __repr__(self):
        return '<Clones %r>' % self.repo


class Traffic(db.Model):
    __tablename__ = "traffic"
    id = db.Column(db.Integer, primary_key=True)
    repo = db.Column(db.String(120))
    datetime = db.Column(db.DateTime)
    clone_count = db.Column(db.Integer)
    clone_count_unique = db.Column(db.Integer)
    clones = db.relationship('Clone', backref='traffic', lazy='dynamic')

    def __init__(self, repo, datetime, clone_count, clone_count_unique):
        self.repo = repo
        self.datetime = datetime
        self.clone_count = clone_count
        self.clone_count_unique = clone_count_unique

    def __repr__(self):
        return '<Repo %r>' % self.repo