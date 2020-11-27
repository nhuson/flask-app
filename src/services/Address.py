from src.repositories.Country import Country
from src.repositories.Province import Province
from src.repositories.District import District
from src.repositories.Town import Town
from src import redis_client
from src.helpers.convertDB import to_list, unicodeString, convertStrProvince, convertStrDistrict, convertStrTown, acronymWords
from src.helpers.enum import CLUSTER_BY
import json, functools

class AddressService:
  """
    Address Service
  """

  def __init__(self):
    self.countryRepo = Country()
    self.provinceRepo = Province()
    self.districtRepo = District()
    self.townRepo = Town()

  def getCountries(self):
    """
      Get list countries
    """
    countries = self.countryRepo.getCountries()
    return to_list(countries)

  def getProvinceByCountryId(self, countryId):
    '''
      Get all province by country code.
    '''
    provinces = self.countryRepo.getProvinceByCountryId(countryId)
    result = to_list(provinces)

    return result

  def getDistrictByProvinceId(self, provinceId):
    '''
      Get all district by province id.
    '''
    districts = self.provinceRepo.getDistrictsById(provinceId.split(','))
    result = to_list(districts)

    return result

  def getTownByDistrictId(self, districtId):
    '''
      Get all town by district id.
    '''
    towns = self.districtRepo.getTownsById(districtId.split(','))
    result = to_list(towns)

    return result

  def getDistrict(self, province, strAddress):
    '''
      Get District object
    '''
    result, district = [] ,None
    districts = province.districts[::-1]
    regexs = ['quan_', 'huyen_', 'thi_xa_', 'q_', 'q._', 'q', 'h', 'tp', 'tx', 'h._', 'tp._', 'tx._', 'q.', 'h_', 'h.', 'tp_', 'tp.', 'tx_', 'tx.', 'district_', '_district', 'dist_', '_dist', 'dist.', 'd.', 'city_', '_city', 'city.', 'city._','']
    for dist in districts:
      # Check districts has only character is number like "quan 1"...
      if dist.slug.isnumeric():
        for reg in ['quan_', 'q_', 'q._', 'q.', 'q', 'district_', '_district', 'dist_', '_dist', 'dist.', 'd.', 'city_', '_city', 'city.', 'city._']:
          if f"{reg}{convertStrDistrict(unicodeString(dist.slug).lower())}" in strAddress or f"{reg}0{convertStrDistrict(unicodeString(dist.slug).lower())}" in strAddress or f"{convertStrDistrict(unicodeString(dist.slug).lower())}{reg}" in strAddress or f"0{convertStrDistrict(unicodeString(dist.slug).lower())}{reg}" in strAddress:
            result.append({"num": int(dist.slug), "district": dist})
            break
      # Check others districts is string
      else:
        for reg in regexs:
          if f"{reg}{convertStrDistrict(unicodeString(dist.name).lower())}" in strAddress or f"{convertStrDistrict(unicodeString(dist.name).lower())}{reg}" in strAddress:
            num = f"{reg}{convertStrDistrict(unicodeString(dist.name).lower())}" if f"{reg}{convertStrDistrict(unicodeString(dist.name).lower())}" in strAddress else f"{convertStrDistrict(unicodeString(dist.name).lower())}{reg}"
            position = strAddress.index(f"{reg}{convertStrDistrict(unicodeString(dist.name).lower())}") if f"{reg}{convertStrDistrict(unicodeString(dist.name).lower())}" in strAddress else strAddress.index(f"{convertStrDistrict(unicodeString(dist.name).lower())}{reg}")
            result.append({"position": position, "district": dist, "num": len(num)})
            break  

    # Priority to district with the most right in string address, position appears neareast in string.
    if len(result) > 1:
      districtPosition = list(filter(lambda x: x.get('position'), result))
      if len(districtPosition):
        distTemp = functools.reduce(lambda a,b: a if a['position'] < b['position'] else a if a['position'] > b['position'] and a['num'] > b['num'] else b, districtPosition)
        district = distTemp.get('district')
      else:
        distTemp = functools.reduce(lambda a,b: a if a['num'] > b['num'] else b, result)
        district = distTemp.get('district')
    elif len(result) == 1:
      district = result[0].get('district')
    return district

  def getTown(self, district, strAddress):
    '''
      Get Town object
    '''
    result, town = [], None
    towns = district.towns[::-1]
    townRegexs = ['phuong_', 'xa_', 'thi_tran_', 'p._', 'p', 'x', 'tt', 'x._', 'tt._', 'p_', 'p.', 'x_', 'x.', 'tt_', 'tt.', 'town_', '_town', 'ward_', 'ward.', '_ward', 'w.', 'commune_', '_commune', '']
    for t in towns:
      # Check towns has slug is number like "phuong 01" 
      if t.slug.isnumeric():
        for reg in townRegexs[:-1]:
          if f"{reg}{convertStrTown(unicodeString(t.slug.lower()))}" in strAddress or f"{reg}0{convertStrTown(unicodeString(t.slug.lower()))}" in strAddress or f"{convertStrTown(unicodeString(t.slug.lower()))}{reg}" in strAddress or f"0{convertStrTown(unicodeString(t.slug.lower()))}{reg}" in strAddress:
            result.append({"num": int(t.slug), "town": t})
            break
      else:
        for reg in townRegexs:
          if f"{reg}{convertStrTown(unicodeString(t.name.lower()))}" in strAddress or f"{convertStrTown(unicodeString(t.name.lower()))}{reg}" in strAddress:
            num = f"{reg}{convertStrTown(unicodeString(t.name.lower()))}" if f"{reg}{convertStrTown(unicodeString(t.name.lower()))}" in strAddress else f"{convertStrTown(unicodeString(t.name.lower()))}{reg}"
            position = strAddress.index(f"{reg}{convertStrTown(unicodeString(t.name.lower()))}") if f"{reg}{convertStrTown(unicodeString(t.name.lower()))}" in strAddress else strAddress.index(f"{convertStrTown(unicodeString(t.name.lower()))}{reg}")
            result.append({"position": position, "town": t, "num": len(num)})
            break
    # Priority to town with the most right in string address, position appears neareast in string.
    if len(result) > 1:
      townPosition = list(filter(lambda x: x.get('position'), result))
      if len(townPosition):
        townTemp = functools.reduce(lambda a,b: a if a['position'] < b['position'] else a if a['position'] > b['position'] and a['num'] > b['num'] else b, result)
        town = townTemp.get('town')
      else:  
        townTemp = functools.reduce(lambda a,b: a if a['num'] > b['num'] else b, result)
        town = townTemp.get('town')
    elif len(result) == 1:
      town = result[0].get('town')
    return town

  def getAddressObject(self, params):
    """
      Auto correct province, district, town, street address from GG API or original Address
    """
    data, province, district, town = {}, None, None, None
    # Parse address from GG API
    if params.get('province'):
      provinceText = " ".join(params.get('province').split()).split(' ')
      provinceText = "_".join(list(map(lambda o: unicodeString(o).strip().lower(), provinceText))).replace(" ", "_")
      provinces = self.provinceRepo.getAllProvince()
      province = next((prov for prov in provinces if unicodeString(prov.name).lower().replace(' ', '_') in provinceText or (acronymWords(prov.name.lower()) == 'hcm' and acronymWords(prov.name.lower()) in provinceText)), None)
      data['province'] = {"name": province.name, "id": province.id} if province else {"id": None, "name": params.get('province')}

    if province and params.get('district'):
      districtText = " ".join(params.get('district').split()).split(' ')
      districtText = "_".join(list(map(lambda o: unicodeString(o).strip().lower(), districtText))).replace(" ", "_")
      district = self.getDistrict(province, districtText)
      data['district'] = {"id": district.id, "name": district.name} if district else {"id": None, "name": params.get('district')}

    if province and district and params.get('town'):
      townText = " ".join(params.get('town').split()).split(' ')
      townText = "_".join(list(map(lambda o: unicodeString(o).strip().lower(), townText))).replace(" ", "_")
      town = self.getTown(district, townText)
      data['town'] = {"id": town.id, "name": town.name} if town else {"name": params.get('town'), "id": None}

    # Parse address from origin address
    if params.get('address'):
      originAddress = params.get('address', None)
      if originAddress:
        tempOriginAddress = " ".join(originAddress.split()).split(',')
        tempAddress = list(map(lambda o: unicodeString(o).strip().lower(), tempOriginAddress))
        tempAddress = tempAddress[::-1]
        tempOriginAddress = tempOriginAddress[::-1]
        originAddress = "_".join(list(map(lambda o: unicodeString(o).strip().lower(), originAddress.split()))).replace(" ", "_")
        if tempAddress[0] == 'vn' or tempAddress[0] == 'vietnam' or tempAddress[0] == 'viet nam':
          tempOriginAddress = tempOriginAddress[1:]
      if originAddress and province is None:
        provinces = self.provinceRepo.getAllProvince()
        province = next((prov for prov in provinces if " ".join(unicodeString(prov.name).lower().split()).replace(' ', '_') in originAddress or (acronymWords(prov.name.lower()) == 'hcm' and acronymWords(prov.name.lower()) in originAddress)), None)
        data['province'] = {"id": province.id, "name": province.name} if province else ({"name": tempOriginAddress[0], "id": None} if len(tempOriginAddress) > 0 else {"name": "", "id": None})
      if originAddress and province and district is None:
        district = self.getDistrict(province, originAddress)
        data['district'] = {"id": district.id, "name": district.name} if district else ({"name": tempOriginAddress[1], "id": None} if len(tempOriginAddress) > 1 else {"name": "", "id": None})
      if originAddress and province and district and town is None:
        town = self.getTown(district, originAddress)
        data['town'] = {"id": town.id, "name": town.name} if town else ({"id": None, "name": tempOriginAddress[2]} if len(tempOriginAddress) > 2 else {"name": "", "id": None})

      if len(tempOriginAddress) and data.get('province') is None:
        data['province'] = {"name": tempOriginAddress[0], "id": None}
      if len(tempOriginAddress) > 1 and data.get('district') is None:
        data['district'] = {"name": tempOriginAddress[1], "id": None}
      if len(tempOriginAddress) > 2 and data.get('town') is None:
        data['town'] = {"name": tempOriginAddress[2], "id": None}
      if len(tempOriginAddress) > 3:
        streetAddress = tempOriginAddress[3:]
        data['street_address'] = ",".join(streetAddress[::-1])
    data['country'] = {"id": 1, "name": 'Việt Nam'}

    return province, district, town, data

  def getCustomerGroupByAddress(self, params):
    """
      Return customer group from address input
    """
    province, district, town, data = self.getAddressObject(params)
    if params.get('cluster_by'):
      if province and params.get('cluster_by') == CLUSTER_BY['province']:
        data['customerGroup'] = [province.id]
      elif (province and district and params.get('cluster_by') == CLUSTER_BY['district']) or (province and district and town is None and params.get('cluster_by') == CLUSTER_BY['town']):
        data['customerGroup'] = [f"{province.id}-{district.id}"]
      elif province and district and town and params.get('cluster_by') == CLUSTER_BY['town']:
        data['customerGroup'] = [f"{province.id}-{district.id}-{town.id}"]
      else:
        data['customerGroup'] = "Could not find the solution, please check the input data."
    return data
  
  def validAddress(self, params):
    """
      Validate address with province, district, town
    """  
    if params.get('province') is None or params.get('province') == '':
      return

    provinceText = convertStrProvince(unicodeString(params.get('province').strip().lower()))
    province = self.provinceRepo.getProvinceBySlug(provinceText)
    if province is None:
      raise Exception("Incorect name with province {}".format(params.get('province')))
    
    if params.get('district') and params.get('district') != '':
      districtSlugs = list(map(lambda d: d.slug, province.districts))
      districtText = convertStrDistrict(unicodeString(params.get('district').strip().lower()))
      districtText = str(int(districtText)) if districtText.isnumeric() else districtText
      if districtText not in districtSlugs:
        raise Exception("Cannot found district {} in province {}".format(params.get('district'), params.get('province')))
      
    if params.get('town') and params.get('town') != '':
      district = self.districtRepo.getDistrictBySlug(districtText, province.id)
      townSlugs = list(map(lambda t: t.slug, district.towns))
      townText = convertStrTown(unicodeString(params.get('town').strip().lower()))
      townText = str(int(townText)) if townText.isnumeric() else townText
      if townText not in townSlugs:
        raise Exception("Cannot found town {} in district {}".format(params.get('town'), params.get('district')))
  
  def generateCustomerGroup(self, params):
    """
      Generate customer group id from province, district, town address.
      The address come from import customer group like "Hà Nội#Ba Đình |Hà Nội#Hoàng Mai|Hà Nội# Tây Hồ".
      Return array customer group ids.
    """
    result, prov, dist, town = [], None, None, None
    address = params.get('address').split('|')
    for add in address:
      addPrams = add.split('#')
      if len(addPrams) == 1:
        [ prov ] = addPrams
        provinceText = convertStrProvince(unicodeString(prov).strip().lower())
        if redis_client.hget("province", provinceText):
          result.append(f"{redis_client.hget('province', provinceText).decode('utf-8')}")
        else:
          province = self.provinceRepo.getProvinceBySlug(provinceText)
          redis_client.hmset("province", { f"{provinceText}": province.id, f"districts_{provinceText}": json.dumps(to_list(province.districts)).encode('utf-8') })
          redis_client.expire("province", 3600)
          result.append(f"{province.id}")
      elif len(addPrams) == 2:
        [ prov, dist ] = addPrams
        provinceText = convertStrProvince(unicodeString(prov).strip().lower())
        districtText = convertStrDistrict(unicodeString(dist).strip().lower())
        if redis_client.hget("province", provinceText) and redis_client.hget("province", f"districts_{provinceText}"):
          districts = json.loads(redis_client.hget("province", f"districts_{provinceText}").decode('utf-8'))
          districtId = next((d['id'] for d in districts if str(d['slug']) == districtText), "")
          result.append(f"{redis_client.hget('province', provinceText).decode('utf-8')}-{districtId}")
        else:
          province = self.provinceRepo.getProvinceBySlug(provinceText)
          redis_client.hmset("province", { f"{provinceText}": province.id, f"districts_{provinceText}": json.dumps(to_list(province.districts)).encode('utf-8') })
          redis_client.expire("province", 3600)
          districtId = next((d.id for d in province.districts if str(d.slug) == districtText), "")
          result.append(f"{province.id}-{districtId}")
      else:
        [ prov, dist, town ] = addPrams
        provinceText = convertStrProvince(unicodeString(prov).strip().lower())
        districtText = convertStrDistrict(unicodeString(dist).strip().lower())
        districtText = str(int(districtText)) if districtText.isnumeric() else districtText
        townText = convertStrTown(unicodeString(town).strip().lower())
        townText = str(int(townText)) if townText.isnumeric() else townText

        if redis_client.hget("province", provinceText) and redis_client.hget("province", f"districts_{provinceText}") and redis_client.hget("district", f"towns_{districtText}"):
          districts = json.loads(redis_client.hget("province", f"districts_{provinceText}").decode('utf-8'))
          towns = json.loads(redis_client.hget("district", f"towns_{districtText}").decode('utf-8'))
          distId = next((d['id'] for d in districts if d['slug'] == districtText))
          townId = next((t['id'] for t in towns if t['slug'] == townText))
          result.append(f"{redis_client.hget('province', provinceText).decode('utf-8')}-{distId}-{townId}")
        else:
          province = self.provinceRepo.getProvinceBySlug(provinceText)
          district = self.districtRepo.getDistrictBySlug(districtText, province.id)
          redis_client.hmset("province", { f"{provinceText}": province.id, f"districts_{provinceText}": json.dumps(to_list(province.districts)).encode('utf-8') })
          redis_client.expire("province", 3600)
          redis_client.hmset("district", { f"towns_{districtText}": json.dumps(to_list(district.towns)).encode('utf-8') })
          redis_client.expire("district", 3600)
          distId = next((d.id for d in province.districts if d.slug == districtText))
          townId = next((t.id for t in district.towns if t.slug == townText))
          result.append(f"{province.id}-{distId}-{townId}")
        
    return result

  def customerGroupToAddress(self, customerGroups):
    """
      Generate address from customer group ids
    """
    result = {}
    for customerGroup in customerGroups.strip().split("|"):
      if result.get(customerGroup) is None: 
        [province, district, town] = [None, None, None]
        splitParams = customerGroup.strip().split('-')
        if len(splitParams) == 1:
          [ province ] = splitParams
        elif len(splitParams) == 2:
          [province, district] = splitParams
        else:
          [province, district, town] = splitParams
        
        if len(splitParams) == 1:
          if redis_client.hget("province", province):
            result[customerGroup] = { 'province': redis_client.hget("province", province).decode('utf-8') }
          else: 
            province = self.provinceRepo.getProvinceById(province)
            redis_client.hmset("province", { f"{province.id}": province.name, f"districts_{province.id}": json.dumps(to_list(province.districts)).encode('utf-8') })
            redis_client.expire("province", 3600) # caching one hour.
            result[customerGroup] = { 'province': province.name }
        elif len(splitParams) == 2:
          if redis_client.hget("province", province) and redis_client.hget("province", f"districts_{province}"):
            districts = json.loads(redis_client.hget("province", f"districts_{province}").decode('utf-8'))
            result[customerGroup] = { 'province': redis_client.hget("province", province).decode('utf-8'), 'district': next((d['name'] for d in districts if str(d['id']) == district), "") }
          else:
            province = self.provinceRepo.getProvinceById(province)
            redis_client.hmset("province", { f"{province.id}": province.name, f"districts_{province.id}": json.dumps(to_list(province.districts)).encode('utf-8') })
            redis_client.expire("province", 3600)
            result[customerGroup] = { 'province': province.name, 'district': next((d.name for d in province.districts if str(d.id) == district), "") }
        else:
          if redis_client.hget("province", province) and redis_client.hget("province", f"districts_{province}") and redis_client.hget("district", f"towns_{district}"):
            districts = json.loads(redis_client.hget("province", f"districts_{province}").decode('utf-8'))
            towns = json.loads(redis_client.hget("district", f"towns_{district}").decode('utf-8'))
            result[customerGroup] = { 'province': redis_client.hget("province", province).decode('utf-8'), 'district': next((d['name'] for d in districts if str(d['id']) == district), ""), 'town': next((t['name'] for t in towns if str(t['id']) == town), "") }
          else:
            province = self.provinceRepo.getProvinceById(province)
            district = self.districtRepo.getDistristById(district)
            redis_client.hmset("province", { f"{province.id}": province.name, f"districts_{province.id}": json.dumps(to_list(province.districts)).encode('utf-8') })
            redis_client.expire("province", 3600)
            redis_client.hmset("district", { f"towns_{district.id}": json.dumps(to_list(district.towns)).encode('utf-8') })
            redis_client.expire("district", 3600)
            result[customerGroup] = { 'province': province.name, 'district': district.name, 'town': next((t.name for t in district.towns if str(t.id) == town), "") }
    return result

  def getAddressByName(self, params):
    '''
      Return provinces, districts, towns by address name.
    '''
    data, province, district = { }, None, None
    if params.get('province'):
      provinceText = convertStrProvince(unicodeString(params.get('province')).lower())
      provinces = self.provinceRepo.getAllProvince()
      province = next((prov for prov in provinces if unicodeString(prov.name).lower().replace(' ', '_') in provinceText), None)
      if province:
        data['districts'] = to_list(province.districts)
      else:
        data['districts'] = []
    else:
      data['districts'] = []
    if province and params.get('district'):
      districtText = convertStrDistrict(unicodeString(params.get('district')).lower())
      try:
        districtText = int(districtText)
        district = self.districtRepo.getDistrictBySlugIsNum(str(districtText), province.id)
      except:
        district = self.districtRepo.getDistrictBySlug(districtText, province.id)
      if district:
        data['towns'] = to_list(district.towns)
      else:
        data['towns'] = []  
    else:
      data['towns'] = []

    return data

  def getAddressDetail(self, params):
    """
      Return province, district, town.
    """
    _, _, _, data = self.getAddressObject(params)
    return data