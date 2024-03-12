# process data from music parser here
import xml.etree.ElementTree as ET

file = open("parser_output.txt", "r")
f = file.read()
f.type()
print(f)

tree = ET.parse('parser_output.xml')