from flask import jsonify
from src.models.Town import Town as TownModel

class Town:
  """
    Town repository
  """
  
  def __init__(self):
    self.townModel = TownModel

  def getTownByName(self, name):
    town = self.townModel.query.filter_by(name=name).first()
    return town

  def getTownBySlug(self, slug, districtId):
    town = self.townModel.query.filter((self.townModel.district_id == districtId) & self.townModel.slug.like("%{}%".format(slug))).first()
    return town

  def getTownBySlugIsNum(self, slug, districtId):
    town = self.townModel.query.filter((self.townModel.slug == slug) & (self.townModel.district_id == districtId)).first()
    return town  
  