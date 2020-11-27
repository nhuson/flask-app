from src import db
from . import Province, Town

class District(db.Model):
  __tablename__ = "districts"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255), nullable=False)
  code = db.Column(db.String(255), nullable=False)
  slug = db.Column(db.String(255), nullable=False)
  province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'))
  province = db.relationship('Province', backref='District', lazy=True)
  towns = db.relationship('Town', backref='District', lazy=True)
  