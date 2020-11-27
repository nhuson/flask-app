'''
  Helper convert data.
'''
import re

def unicodeString(s):
  s = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
  s = re.sub(r'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
  s = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', s)
  s = re.sub(r'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
  s = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
  s = re.sub(r'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
  s = re.sub(r'[ìíịỉĩ]', 'i', s)
  s = re.sub(r'[ÌÍỊỈĨ]', 'I', s)
  s = re.sub(r'[ùúụủũưừứựửữ]', 'u', s)
  s = re.sub(r'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
  s = re.sub(r'[ỳýỵỷỹ]', 'y', s)
  s = re.sub(r'[ỲÝỴỶỸ]', 'Y', s)
  s = re.sub(r'[Đ]', 'D', s)
  s = re.sub(r'[đ]', 'd', s)
  s = re.sub(r"'", '', s)
  s = re.sub(r"-", '', s)

  return s

def to_dict(row):
  d = {}
  for column in row.__table__.columns:
    d[column.name] = getattr(row, column.name)

  return d

def to_list(rows):
  data = []
  for row in rows:
    d = {}
    for column in row.__table__.columns:
      d[column.name] = getattr(row, column.name)
    data.append(d)

  return data  

def convertStrProvince(province):
  result = province.replace(" ", "_").replace('thanh_pho_', "")
  regexs = ["tinh_", "t_", "tp._", "t._", "t.", "tp.", "tp_"]
  for reg in regexs:
    if result.find(reg) == 0:
      result = result.replace(reg, "", 1)

  return result

def convertStrDistrict(district):
  result = ''
  districtStr = district
  engRegs = ['district', 'dist', 'city']
  for engReg in engRegs:
    if districtStr.find(engReg) == 0:
      districtStr = districtStr.replace(engReg, "quan", 1)
    elif districtStr.find(engReg) > 0:
      distTemp = districtStr.split(" ")
      distTemp = distTemp[:-1]
      districtStr = " ".join(distTemp)
  result = districtStr.replace(" ", "_").replace('thanh_pho_', '')
  regexs = ['quan_', 'huyen_', 'thi_xa_', 'q_', 'q._', 'h._', 'tp._', 'tx._', 'q.', 'h_', 'h.', 'tp_', 'tp.', 'tx_', 'tx.']
  for reg in regexs:
    if result.find(reg) == 0:
      result = result.replace(reg, "", 1)
  return result  

def convertStrTown(town):
  result = ''
  townStr = town
  engRegs = ['town', 'ward', 'commune']
  for engReg in engRegs:
    if townStr.find(engReg) == 0:
      townStr = townStr.replace(engReg, "phuong", 1)
    elif townStr.find(engReg) > 0:
      townTemp = townStr.split(" ")
      townTemp = townTemp[:-1]
      townStr = " ".join(townTemp)
  result = townStr.replace(' ', '_')
  regexs = ['phuong_', 'xa_', 'thi_tran_', 'p._', 'x._', 'tt._', 'p_', 'p.', 'x_', 'x.', 'tt_', 'tt.']
  for reg in regexs:
    if result.find(reg) == 0:
      result = result.replace(reg, "", 1)
  
  return result        

def acronymWords(word):
  return "".join(w[0] for w in word.split())
