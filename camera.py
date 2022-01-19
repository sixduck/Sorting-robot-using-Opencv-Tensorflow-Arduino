from time import time
import dk_ardruino
import xu_ly_anh
import cv2
import numpy as np
import serial
from keras.models import load_model

cam_mtx=np.load('utils/cam_mtx.npy')
dist=np.load('utils/dist.npy')
newcam_mtx=np.load('utils/newcam_mtx.npy')
roi=np.load('utils/roi.npy')
width = int(open('utils/Resolution.txt').read().split('\n')[0])
height = int(open('utils/Resolution.txt').read().split('\n')[1])
camera_number = int(open('utils/Resolution.txt').read().split('\n')[7])
Serial_port = open('utils/Resolution.txt').read().split('\n')[8]

# Khởi động cổng COM
ser = serial.Serial(Serial_port, 9600, timeout=1)
arm = True
arm_c=dk_ardruino.arm_controller(ser)
arm_c.wait_forready()

# Khởi động camera
cam = cv2.VideoCapture(camera_number)
def make_720p(cap):
    cap.set(3, width)
    cap.set(4, height)
make_720p(cam)


# các biến sử dụng
obj_detected=0
obj_detected_prev=0
id_counter = 0

bg_counter=0
bg_capture=False
img_counter = 0

detectXYZ = True

# Load chạy vật thể
chay = xu_ly_anh.image_recognition()
chay.get_label()
np.set_printoptions(suppress=True)
model = load_model('utils/keras_model.h5')

# Hàm để gửi tín hiệu đến ardruino
def pickanddrop(XYZ, arm=True):
    #set drop position
    arm_x_dest=30
    arm_y_dest=6
    arm_x_dest1=30
    arm_y_dest1=-6
    for i in range(0,len(XYZ)):

        cam_x=76.2-XYZ[i][0] #camera X
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
    
    # Đọc frame từ cam
    ret, frame = cam.read()
    frame = cv2.undistort(frame, cam_mtx, dist, None, newcam_mtx)
    x, y, w, h = roi
    frame = frame[y:y+h, x:x+w]
    if not ret:
        break 
    

    if bg_capture == False:
        bg_counter+=1
        print(bg_counter)
        if bg_counter==52:
            cap_bg = frame
            bg_capture=True
        else:
            cv2.putText(frame, 'Khoi_dong', (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 5, (36,255,12), 2)
    if bg_capture == True:

        obj_detected_prev=obj_detected
        XYZ, anh = chay.chay_phat_hien(cap_bg, frame, model)
        obj_detected=len(XYZ)
        if obj_detected>0 and obj_detected==obj_detected_prev:
            id_counter+=1
            cv2.putText(anh,"Object Detected",(300,300),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2)
        cv2.namedWindow('camera', cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty('camera',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)        
        cv2.imshow('camera', anh)
    
    # if id_counter>20:
    #     cv2.putText(anh,"Picking",(300,300),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
    #     print("Trigger Arm")
    #     pickanddrop(XYZ,arm)
    #     id_counter=0   

    
    
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        cv2.putText(anh,"Picking",(300,300),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
        print("Trigger Arm")
        pickanddrop(XYZ,arm)
        id_counter=0   
        # SPACE pressed
        # cv2.imwrite('goc.jpg', frame)
        # print("Da Luu...")
        # cap_target = frame
        # start = time()
        # XYZ,anh = chay.chay_phat_hien(cap_bg, cap_target, model)
        # print('----% s---' % (time()-start))
        # # cv2.namedWindow('ket_qua', cv2.WND_PROP_FULLSCREEN)
        # # cv2.setWindowProperty('ket_qua',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        # cv2.imshow("camera",anh)
        # cv2.waitKey(10000)
        # # pickanddrop(XYZ,arm)
        # cv2.destroyAllWindows()
        
        
if (arm==True): arm_c.move_home()        
cam.release()
cv2.destroyAllWindows()
ser.close()


