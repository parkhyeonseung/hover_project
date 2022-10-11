#!/usr/bin/env python3
# encoding: utf-8
from ardu_serial import Ardu
import rospy
from std_msgs.msg import String
from lidar_sub_updating import Lidar_sub
class Command ():
    def __init__(self):
        self.mega = Ardu(port='/dev/ttyMEGA')
        self.lidar = Lidar_sub()
        self.x_data = '00'
        self.y_data = '00'
        self.prev_x_data = 's0'
        self.prev_y_data = 's0'
        rospy.Subscriber('hover_command',String,self.yolo_sub,queue_size=1)
            
    def yolo_sub(self,c_data):
        yolo_data = c_data.data
        detect = yolo_data[0]
        prev_detect = yolo_data[1]
        in_middle = yolo_data[2]
        prev_in_middle = yolo_data[3]
        
        if detect == 't':
            if in_middle == 't':
                self.x_data = self.lidar.lidar_data #####lidar distance
                self.prev_x_data = self.x_data * 0.6
                self.y_data = 's0'
            else:
                if prev_in_middle == 't':
                    self.x_data = self.prev_x_data
                else:
                    self.x_data = 's0'
                    
                self.y_data = yolo_data[4:]
                self.prev_y_data = self.y_data * 0.6
                
        else:
            if prev_detect == 't':
                if prev_in_middle == 't':
                    self.x_data = self.prev_x_data
                    self.y_data = 's0'
                else:
                    self.x_data = 's0'
                    self.y_data = self.prev_y_data
            else:
                self.x_data = 's0'
                self.y_data = 's0'
                
        self.mega.input(self.x_data)
        self.mega.input(self.y_data)
            
if __name__ =="__main__":
    rospy.init_node('input_hover')
    command = Command()
    rospy.spin()
            
        