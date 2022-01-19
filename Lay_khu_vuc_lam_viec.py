
import cv2
import numpy as np

camera_number = int(open('utils/Resolution.txt').read().split('\n')[7])
width = int(open('utils/Resolution.txt').read().split('\n')[0])
height = int(open('utils/Resolution.txt').read().split('\n')[1])
cam_mtx=np.load('utils/cam_mtx.npy')
dist=np.load('utils/dist.npy')
newcam_mtx=np.load('utils/newcam_mtx.npy')
roi=np.load('utils/roi.npy')

so = 4
cam = cv2.VideoCapture(camera_number)

img = cv2.imread('utils/nen.jpg', 1)
img2 = img.copy()
points = []
def make_720p(cap):
    cap.set(3, width)
    cap.set(4, height)
make_720p(cam)
pick_point = True
def click_event(event, x, y, flags, params):
    # checking for left mouse clicks
    global so
    if event == cv2.EVENT_LBUTTONDOWN:
        if so !=0:
            cv2.circle(img2, (x,y), 10, (255,0,0), -1)
            cv2.imshow('image', img2)
            so = so - 1
            points.append([x,y])
while True:
    _,frame = cam.read()
    if pick_point is True:
        cv2.namedWindow('image')
        # cv2.namedWindow('image', cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty('image',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.setMouseCallback('image', click_event)
        cv2.imshow('image', img2)
    

    
    k = cv2.waitKey(1) 
    if k == 114:
        # Nut R
        img2 = img.copy()
        so = 4
        points = []
    if k == 32:
        # Nut space
        pts1 = np.float32(points)
        pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
        crop_nen = cv2.warpPerspective(img, matrix, (width, height))
        cv2.namedWindow('text', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('text',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow('text', crop_nen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        np.save('utils/abc',matrix)
        pick_point = False
    if k == 27:
        # Nut ESC
        break
    
    if pick_point is not True:
        _,frame = cam.read()

        frame = cv2.undistort(frame, cam_mtx, dist, None, newcam_mtx)
        x, y, w, h = roi
        frame = frame[y:y+h, x:x+w]
        frame = cv2.warpPerspective(frame, matrix, (width, height))
        cv2.imshow('text1', frame)
        
cv2.destroyAllWindows()
cam.release()

