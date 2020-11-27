from src import db
from . import Country, District

class Province(db.Model):
  __tablename__ = "provinces"

  id = db.Column(db.Integer, primary_key=True, auto_increment=True)
  name = db.Column(db.String(255), nullable=False)
  code = db.Column(db.String(255), nullable=False)
  slug = db.Column(db.String(255), nullable=False)
  country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
  country = db.relationship('Country', backref='Province', lazy=True)
  districts = db.relationship('District', backref='Province', lazy=True)
  