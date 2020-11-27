import unittest
from src.helpers.convertDB import unicodeString, convertStrProvince, convertStrDistrict, convertStrTown

class TestHelper(unittest.TestCase):
  def test_unicode_string(self):
    str_input = "Việt Nam"
    self.assertEqual(unicodeString(str_input), "Viet Nam")

  def test_convert_str_province(self):
    input_str = ["Thành phố Hà Nội", "Hà Nội", "tp. Hà Nội", "tp Hà Nội", "tỉnh Hà Nội", "t Hà Nội", "t. Hà Nội"]
    output_str = list(map(lambda str: convertStrProvince(unicodeString(str.lower())), input_str))
    self.assertTrue(all(str == output_str[0] for str in output_str))
    
  def test_convert_str_district(self):
    input_str = ["Quận Ba Đình", "q Ba Đình", "q. Ba Đình", "thị xã Ba Đình", "tx Ba Đình", "tx. Ba đình", "huyện Ba đình", "h Ba Đình", "h. Ba Đình", "thành phố ba đình", "tp Ba đình", "tp. Ba đình"]
    output_str = list(map(lambda s: convertStrDistrict(unicodeString(s.lower())), input_str))
    self.assertTrue(all(str == output_str[0] for str in output_str))

  def test_convert_str_town(self):
    input_str = ["Phường Đốc Ngữ", "Xã Đốc Ngữ", "Thị trấn Đốc Ngữ", "p Đốc Ngữ", "x Đốc Ngữ", "tt Đốc Ngữ", "p. Đốc Ngữ", "x. Đốc Ngữ", "tt. Đốc Ngữ"]
    output_str = list(map(lambda s: convertStrTown(unicodeString(s.lower())), input_str))
    self.assertEqual(len(set(output_str)), 1)