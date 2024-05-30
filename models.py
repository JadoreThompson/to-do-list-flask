from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=True)
    done = db.Column(db.Integer, default=0)
