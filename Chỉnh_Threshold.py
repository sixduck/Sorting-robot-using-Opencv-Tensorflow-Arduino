# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 00:18:13 2021

@author: Administrator
"""

import cv2  
import numpy as np


width = int(open('utils/Resolution.txt').read().split('\n')[0])
height = int(open('utils/Resolution.txt').read().split('\n')[1])
matrix = np.load('utils/abc.npy')


anh_phat_hien_crop = cv2.imread('utils/goc.jpg')
anh_nen_crop = cv2.imread('utils/nen.jpg')

anh_phat_hien_crop = cv2.warpPerspective(anh_phat_hien_crop, matrix, (width, height))
anh_nen_crop = cv2.warpPerspective(anh_nen_crop, matrix, (width, height))

def nothing(x):
    pass
def initializeTrackbars(intialTracbarVals=0):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Threshold1", "Trackbars", 0,255, nothing)
    cv2.createTrackbar("Threshold2", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("Threshold3", "Trackbars", 0, 20000, nothing)
def valTrackbars():
    Threshold1 = cv2.getTrackbarPos("Threshold1", "Trackbars")
    Threshold2 = cv2.getTrackbarPos("Threshold2", "Trackbars")
    Threshold3 = cv2.getTrackbarPos("Threshold3", "Trackbars")
    src = Threshold1,Threshold2,Threshold3
    return src
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range (0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

initializeTrackbars()

while True:
 
    thres = valTrackbars()
    
    target_gray = cv2.cvtColor(anh_phat_hien_crop, cv2.COLOR_BGR2GRAY)

    bg_gray = cv2.cvtColor(anh_nen_crop, cv2.COLOR_BGR2GRAY)

    diff_gray = cv2.absdiff(target_gray,bg_gray)
 
    diff_gray_blur = cv2.GaussianBlur(diff_gray,(5,5),0)

    ret,diff_tresh = cv2.threshold(diff_gray_blur,thres[0],thres[1],cv2.THRESH_BINARY)

    diff = cv2.GaussianBlur(diff_tresh,(5,5),0)

    contours, hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            
            area = w*h
            edge_noise=False
            if x==0:
                edge_noise=True
            if y==0:
                edge_noise=True
            if (x+w)== width:
                edge_noise=True
            if (y+h)== height:
                edge_noise=True
    
            if edge_noise==False:
                if area > thres[2]:
                    cv2.rectangle(diff, (x,y), (x+w,y+h), (255,225,0),2)
    
    # imageArray = ([anh_phat_hien_crop,diff])
    
    # stackedImage = stackImages(imageArray,0.75)
    
    cv2.namedWindow('img', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('img',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow('img',diff)

    # waitfor the user to press escape and break the while loop 
    k = cv2.waitKey(1)
    if k == 32:
        file1 = open("utils/Resolution.txt","r")
        arr = file1.read().split('\n')
        try:
            arr[5] = str(thres[0])
            arr[6] = str(thres[1])
            arr[2] = str(thres[2])
        except:
            print('error')
        with open('utils/Resolution.txt', "w") as myfile:
            for i in range(len(arr)):
                myfile.write(arr[i] + '\n')

    if k == 27:
        break
#destroys all window
cv2.destroyAllWindows()