
import cv2 as cv
import numpy as np
import pandas as pd
from torch import sort

#loading image 
img = cv.imread('test01.jpg')
cv.imshow('original', img)
imginverted = cv.bitwise_not(img)

#since there are 4 sperate rectangle i want to divide the image into four parts 
#first vertically 

height = imginverted.shape[0]
width = imginverted.shape[1]

# Cut the image in half
width_cutoff = width // 2
left1 = imginverted[:, :width_cutoff]
right1 = imginverted[:, width_cutoff:]

#rotate image LEFT1 to 90 CLOCKWISE
leftimg = cv.rotate(left1, cv.ROTATE_90_CLOCKWISE)

# start vertical devide image
height = leftimg.shape[0]
width = leftimg.shape[1]

# Cut the image in half
width_cutoff = width // 2
l1 = leftimg[:, :width_cutoff]
l2 = leftimg[:, width_cutoff:]

#rotate image to 90 COUNTERCLOCKWISE
l1 = cv.rotate(l1, cv.ROTATE_90_COUNTERCLOCKWISE)

#rotate image to 90 COUNTERCLOCKWISE
l2 = cv.rotate(l2, cv.ROTATE_90_COUNTERCLOCKWISE)

#rotate image LEFT1 to 90 CLOCKWISE
rightimg = cv.rotate(right1, cv.ROTATE_90_CLOCKWISE)

# start vertical devide image
height = rightimg.shape[0]
width = rightimg.shape[1]

# Cut the image in half
width_cutoff = width // 2
r1 = rightimg[:, :width_cutoff]
r2 = rightimg[:, width_cutoff:]


#rotate image to 90 COUNTERCLOCKWISE
r1 = cv.rotate(r1, cv.ROTATE_90_COUNTERCLOCKWISE)

#rotate image to 90 COUNTERCLOCKWISE
r2 = cv.rotate(r2, cv.ROTATE_90_COUNTERCLOCKWISE)


def rotate(img, angle, rotPoint=None):
    (height,width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2,height//2)
    
    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width,height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated1 = rotate(l1, -30)
rotated2= rotate(l2, 15)
rotated3 = rotate(r1, 30)
rotated4 = rotate(r2, -15)

h_img1 = cv.hconcat([rotated2, rotated4])
h_img2 = cv.hconcat([rotated1, rotated3])
v_img = cv.vconcat([h_img1,h_img2])

# Edge detection
dst = cv.Canny(cv.bitwise_not(v_img), 50, 200, None, 3)

linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 10, None, 10, 5)

#to get point
# print(linesP)

# if linesP is not None:
#     for i in range(0, len(linesP)):
#         l = linesP[i][0]
#         cv.line(v_img, (l[0], l[1]), (l[2], l[3]), (0,255,0), 1)


#x1,y1 and x2,y2
l1=[104,77,190,77]
l2=[489,63,620,63]
l3=[89,378,265,378]
l4=[464,458,547,458]

line1 = l1[2]-l1[0]
line2 = l2[2]-l2[0]
line3 = l3[2]-l3[0]
line4 = l4[2]-l4[0]

lengths = [line1,line2,line3,line4]

# print(lengths)

textpositionx = [150,550,150,550] 
textpositiony = [180,180,300,300] 
i=0

d2=[1,2,3,4]
s1 = pd.DataFrame(lengths)
s2 = pd.DataFrame(lengths)
s2 = s2.sort_values(by=0)
s2[1] = d2
f1 = pd.merge(s1, s2, left_index=True, right_index=True)
finallist = [f1[1][0],f1[1][1],f1[1][2],f1[1][3]]

for length in lengths :
    cv.putText(v_img, f"{finallist[i] }" , (textpositionx[i],textpositiony[i]), cv.QT_FONT_NORMAL, 1.0, (255,255,255), 1)    
    i=i+1
cv.imshow('lines', cv.bitwise_not(v_img))

cv.waitKey(0)