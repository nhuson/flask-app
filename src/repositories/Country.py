from flask import jsonify
from src.models.Country import Country as CountryModel

class Country:
  """
    Country repository
  """
  
  def __init__(self):
    self.countryModel = CountryModel

  def getCountries(self):
    countries =  self.countryModel.query.all()

    return countries

  def getProvinceByCountryId(self, id):
    country = self.countryModel.query.filter_by(id=id).first()

    return country.provinces
