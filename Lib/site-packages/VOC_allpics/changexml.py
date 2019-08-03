#https://blog.csdn.net/u013996948/article/details/79157795

from xml.etree.ElementTree import ElementTree,Element
import xml.etree.ElementTree as ET
import os 
#import cv2 as cv 


filelist = []
filedir = 'Annotations'
for root , dirs, files in os.walk(filedir):
    for file in files:
        filelist.append(file)

print(filelist)
for flie in filelist:
   tree = ET.parse(filedir + '/' + file)
#tree = ET.parse('D:\python\venv1\output.xml')
   root = tree.getroot()
   for elem in root.iter('width'):
      elem.text = '270'

   for elem in root.iter('height'):
      elem.text = '270'
   for elem in root.iter('xmin'):
      new_elem=(int(elem.text)//2)
      elem.text = str(new_elem)
   for elem in root.iter('ymin'):
      new_elem=(int(elem.text)//2)
      elem.text = str(new_elem)
   for elem in root.iter('xmax'):
      new_elem=(int(elem.text)//2)
      elem.text = str(new_elem)
   for elem in root.iter('ymax'):
      new_elem=(int(elem.text)//2)
      elem.text = str(new_elem)
   tree.write('Anno'+ '/' + file)
   print(file)
