import cv2
import numpy as np
import dk_ardruino
import serial
cam_mtx=np.load('utils/cam_mtx.npy')
dist=np.load('utils/dist.npy')
newcam_mtx=np.load('utils/newcam_mtx.npy')
roi=np.load('utils/roi.npy')
matrix = np.load('utils/abc.npy')
area1 = int(open('utils/Resolution.txt').read().split('\n')[2])
width = int(open('utils/Resolution.txt').read().split('\n')[0])
height = int(open('utils/Resolution.txt').read().split('\n')[1])
diff_low_t= int(open('utils/Resolution.txt').read().split('\n')[5])
diff_high_t= int(open('utils/Resolution.txt').read().split('\n')[6])
realwidth = int(open('utils/Resolution.txt').read().split('\n')[3])
realheight = int(open('utils/Resolution.txt').read().split('\n')[4])
camera_number = int(open('utils/Resolution.txt').read().split('\n')[7])
Serial_port = open('utils/Resolution.txt').read().split('\n')[8]
bg_capture=False
bg_counter=0
count = 0

cam = cv2.VideoCapture(camera_number)
def make_720p(cap):
    cap.set(3, width)
    cap.set(4, height)
make_720p(cam)

ser = serial.Serial(Serial_port, 9600, timeout=1)
arm = True
arm_c=dk_ardruino.arm_controller(ser)
arm_c.wait_forready()

def pickanddrop(XYZ, arm=True):
    #set drop position
    arm_x_dest=30
    arm_y_dest=6
    arm_x_dest1=30
    arm_y_dest1=-6
    for i in range(0,len(XYZ)):

        cam_x=76.5-XYZ[i][0] #camera X
        cam_x = round(cam_x,3)        
        cam_y=6-XYZ[i][1] #camera Y
        cam_y = round(cam_y,3)
        print(arm_x_dest,arm_y_dest,cam_x,cam_y)        
        if (arm==True): arm_c.move_and_pickup(cam_x,cam_y)        
        if (arm==True): 
            arm_c.transport_and_drop(arm_x_dest1,arm_y_dest1)
            print(arm_x_dest1,arm_y_dest1,cam_x,cam_y)
    if (arm==True): arm_c.move_home()


while True:
    ret, frame = cam.read()
    frame = cv2.undistort(frame, cam_mtx, dist, None, newcam_mtx)
    a, b, c, d = roi
    frame = frame[b:b+d, a:a+c]
    frame1 = frame.copy()
    
    if bg_capture == False:
        bg_counter+=1
        print(bg_counter)
        if bg_counter==10:
            crop_nen = cv2.warpPerspective(frame, matrix, (width, height))
            # crop_nen= frame
            bg_capture=True    
    if bg_capture == True:
        crop_phat_hien = cv2.warpPerspective(frame, matrix, (width, height))
        # crop_phat_hien = frame
        target_gray = cv2.cvtColor(crop_phat_hien, cv2.COLOR_BGR2GRAY)
        bg_gray = cv2.cvtColor(crop_nen, cv2.COLOR_BGR2GRAY)
        diff_gray = cv2.absdiff(target_gray,bg_gray)
        diff_gray_blur = cv2.GaussianBlur(diff_gray,(9,9),0)
        ret,diff_tresh = cv2.threshold(diff_gray_blur,diff_low_t,diff_high_t,cv2.THRESH_BINARY)
        diff = cv2.GaussianBlur(diff_tresh,(9,9),0)
        diff = cv2.dilate(diff, None, iterations=2)
        contours, hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        
        XYZ=[]
        for cnt in contours:
            (x,y,w,h) = cv2.boundingRect(cnt)
            cv2.rectangle(crop_phat_hien, (x, y), (x + w, y + h), (0, 0, 255), 2)
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
                if area > area1:
                    realx = (realwidth/width)*(x + (w/2))
                    realy = (realheight/height)*(y + (h/2))    
                    cv2.rectangle(crop_phat_hien, (x, y), (x + w, y + h), (0, 0, 255), 2)

                    adjust=0.1
                    y=int(y-((h*adjust)/2))
                    if y<0:
                        y=0
                    x=int(x-((w*adjust)/2))
                    if x<0:
                        x=0
                    w=int(w*(1+adjust))
                    h=int(h*(1+adjust))
                    if y<0: y=0
                    if x<0: x=0
                    if (x+w)>width: w=width-x
                    if (y+h)>height: h=height-y
                    if w>h:
                        #ensure contour is centered
                        y=int(y-((w-h)/2))
                        if y<0: y=0
                        #make a square
                        h=w
                        if (y+h)>height: y=height-h
                    if h>w:
                        x=int(x-((h-w)/2))
                        if x<0: x=0
                        w=h
                        if (x+w)>width: x=width-w
                    crop_img = crop_phat_hien[y:y+h, x:x+w]
                    # cv2.rectangle(crop_phat_hien, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # cv2.putText(crop_phat_hien, str(count), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)    

                    XYZ.append([realx,realy])
                    # XYZ.append([x,y,w,h])
        cv2.imshow('camera', diff)
        cv2.imshow('camera1', crop_phat_hien)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    if k%256 == 32:
        # for items in XYZ:
        #     x,y,w,h = items
        #     crop_img = frame1[y:y+h, x:x+w]
        #     cv2.imwrite("dataset/frame%d.png" % count, crop_img)
        #     count += 1
        pickanddrop(XYZ,arm)
        
if (arm==True): arm_c.move_home() 
cam.release()
cv2.destroyAllWindows()
ser.close()