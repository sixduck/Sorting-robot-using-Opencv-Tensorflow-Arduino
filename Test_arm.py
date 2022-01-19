# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 19:55:38 2021

@author: Admin
"""
import serial
import dk_ardruino
ser = serial.Serial('COM3', 9600, timeout=1)
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


