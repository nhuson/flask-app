from flask import jsonify
from src.models.Province import Province as ProvinceModel

class Province:
  """
    Province repository
  """
  
  def __init__(self):
    self.provinceModel = ProvinceModel

  def getDistrictsById(self, id):
    provinces = self.provinceModel.query.filter(self.provinceModel.id.in_(id)).all()
    districts = []
    for province in provinces:
      districts = districts + province.districts
    return districts

  def getProvinceById(self, id):
    province = self.provinceModel.query.filter_by(id=id).first()
    return province

  def getProvinceBySlug(self, slug):
    province = self.provinceModel.query.filter(self.provinceModel.slug.like("%{}%".format(slug))).first()
    return province

  def getAllProvince(self):
    return self.provinceModel.query.all()  
  