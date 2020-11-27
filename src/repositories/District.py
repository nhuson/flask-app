from flask import jsonify
from src.models.District import District as DistrictModel

class District:
  """
    District repository
  """
  
  def __init__(self):
    self.districtModel = DistrictModel

  def getTownsById(self, id):
    districts = self.districtModel.query.filter(self.districtModel.id.in_(id)).all()
    towns = []
    for district in districts:
      towns = towns + district.towns
    return towns

  def getDistristById(self, id):
    district = self.districtModel.query.filter_by(id=id).first()
    return district

  def getDistrictBySlug(self, slug, provinceId):
    district = self.districtModel.query.filter((self.districtModel.province_id == provinceId) & self.districtModel.slug.like("%{}%".format(slug))).first()
    return district 

  def getDistrictBySlugIsNum(self, slug, provinceId):
    town = self.districtModel.query.filter((self.districtModel.slug == slug) & (self.districtModel.province_id == provinceId)).first()
    return town  