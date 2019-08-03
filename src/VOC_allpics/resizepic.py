import os 
import cv2 as cv 


filelist = []
filedir = 'JPEGImages'
for root , dirs, files in os.walk(filedir):
    for file in files:
        filelist.append(file)

print(filelist)


for file in filelist:
    img = cv.imread(filedir +'/' +file)
    dst = cv.resize(img, (270,270), cv.INTER_LINEAR)
    cv.imwrite('JPE'+ '/'  + file, dst)
    
