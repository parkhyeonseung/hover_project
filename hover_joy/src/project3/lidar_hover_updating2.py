#!/usr/bin/env python3
# encoding: utf-8
from ardu_serial import Ardu
import rospy
from std_msgs.msg import String
from cyg_sub_updating2 import Lidar
from joy_sub_updating2 import Joystick
class Command ():
    def __init__(self):
        self.mega = Ardu(port='/dev/ttyMEGA')
        self.lidar = Lidar()
        self.joystick = Joystick()
        self.x_data = '00'
        self.y_data = '00'
        self.prev_x_data = 's0'
        self.prev_y_data = 's0'
        rospy.Subscriber('hover_command',String,self.yolo_sub,queue_size=1)
            
    def yolo_sub(self,c_data):
        if (self.joystick.joy == True) or ( (self.joystick.joy==False) and (self.joystick.yolo == False) ):
            joy_data = c_data.data
            t_idx = joy_data.find('t')
            if t_idx:
                self.x_data = joy_data[0:t_idx]
                self.y_data = joy_data[t_idx:]
            else:
                self.x_data = joy_data[0:2]
                self.y_data = joy_data[2:]
        else: 
            yolo_data = c_data.data
            detect = yolo_data[0]
            prev_detect = yolo_data[1]
            in_middle = yolo_data[2]
            prev_in_middle = yolo_data[3]
            
            if detect == 't':
                if in_middle == 't':
                    if 0.6<self.lidar.minDist <1:          ###### stop
                        self.x_data = 0
                    elif self.lidar.minDist>=1:            ###### front
                        self.x_data = int(self.lidar.minDist*40)
                    elif self.lidar.minDist <=0.6:         ###### back
                        self.x_data = -90
                        
                    self.prev_x_data = int(self.x_data * 0.6)
                    self.y_data = 0
                else:
                    print("detect_else")
                    if prev_in_middle == 't':
                        self.x_data = self.prev_x_data
                    else:
                        self.x_data = 0
                        
                    self.y_data = int(yolo_data[4:])
                    self.prev_y_data = int(self.y_data * 0.4)
                    
            else:
                if prev_detect == 't':
                    if prev_in_middle == 't':
                        self.x_data = self.prev_x_data
                        self.y_data = 0
                    else:
                        self.x_data = 0
                        self.y_data = self.prev_y_data
                else:
                    self.x_data = 0
                    self.y_data = 0
                    
            if self.x_data ==0:
                self.x_data = 'g0'
            elif self.x_data >0:
                self.x_data = 'g'+str(self.x_data)
            else :
                self.x_data = 'b-90'
                
            if self.y_data ==0:
                self.y_data = 't0'
            else:
                self.y_data = 't'+str(self.y_data)
                
        print(self.x_data,',',self.y_data)
        self.mega.input(self.x_data)
        self.mega.input(self.y_data)
            
if __name__ =="__main__":
    rospy.init_node('input_hover')
    try:
        command = Command()
        rospy.spin()
    except KeyboardInterrupt:
        command = Command()
        command.mega.close_all()
            
        