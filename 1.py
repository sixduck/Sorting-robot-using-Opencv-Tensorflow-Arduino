







# capture a frame from the camera and save it to the file as a png
import cv2
import numpy as np
import os

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
count = 0
while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    #with each space key is pressed, save the current frame to a file
    if cv2.waitKey(1) & 0xFF == ord(' '):
        cv2.imwrite('frame%d.png' % count, frame)
        count += 1
        print(count)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


