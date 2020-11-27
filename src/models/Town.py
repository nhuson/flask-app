from src import db
from . import District

class Town(db.Model):
  __tablename__ = "towns"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  code = db.Column(db.String(255), nullable=False)
  slug = db.Column(db.String(255), nullable=False)
  district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
  district = db.relationship('District', backref='Town', lazy=True)
  