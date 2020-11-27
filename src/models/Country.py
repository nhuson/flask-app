from src import db
from . import Province

class Country(db.Model):
  __tablename__ = "countries"

  id = db.Column(db.Integer, primary_key=True, auto_increment=True)
  name = db.Column(db.String(50), unique=True)
  code = db.Column(db.String(50), unique=True)
  provinces = db.relationship('Province', backref='Country', lazy=True)
  