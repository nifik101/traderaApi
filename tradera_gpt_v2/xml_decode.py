import xml.etree.ElementTree as ET

root = ET.parse("tradera_cat.xml")

res = root.getroot()

layer_one = root.find(".//")
print("layer_one", layer_one)
