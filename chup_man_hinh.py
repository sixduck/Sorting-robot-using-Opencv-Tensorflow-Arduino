# -*- coding: utf-8 -*-
"""
Created on Fri Oct 15 16:46:01 2021

@author: Administrator
"""

import cv2
import numpy as np
width = int(open('utils/Resolution.txt').read().split('\n')[0])
height = int(open('utils/Resolution.txt').read().split('\n')[1])
camera_number = int(open('utils/Resolution.txt').read().split('\n')[7])
cam_mtx=np.load('utils/cam_mtx.npy')
dist=np.load('utils/dist.npy')
newcam_mtx=np.load('utils/newcam_mtx.npy')
roi=np.load('utils/roi.npy')


cam = cv2.VideoCapture(camera_number)
def make_720p(cap):
    cap.set(3, width)
    cap.set(4, height)
make_720p(cam)

cv2.namedWindow("test")




while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    
    frame = cv2.undistort(frame, cam_mtx, dist, None, newcam_mtx)
    x, y, w, h = roi
    frame = frame[y:y+h, x:x+w]
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        height,width,_ = frame.shape
        
        file1 = open("utils/Resolution.txt","r")
        arr = file1.read().split('\n')
        try:
            arr[0] = str(width)
            arr[1] = str(height)
        except:
            print('error')
        with open('utils/Resolution.txt', "w") as myfile:
            for i in range(len(arr)):
                myfile.write(arr[i] + '\n')
        break
    elif k%256 == 110:
        # n pressed
        img_name = "utils/nen.jpg"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))

    elif k%256 == 103:
        # g pressed
        img_name = "utils/goc.jpg"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))


cam.release()
cv2.destroyAllWindows()