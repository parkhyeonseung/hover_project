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
        rospy.Subscriber('hover_command',String,self.yolo_sub,queue_size=1)
            
    def yolo_sub(self,c_data):
        yolo_data = c_data.data
        t_idx = yolo_data.find('t')
        if t_idx:
            self.x_data = yolo_data[0:t_idx]
            self.y_data = yolo_data[t_idx:]
        else:
            self.x_data = yolo_data[0:2]
            self.y_data = yolo_data[2:]
            
        if self.lidar.lidar_data == 'w':
                self.mega.input('00')
        elif self.lidar.lidar_data == 's':
            if '-' in self.x_data:
                self.mega.input(self.x_data)
                self.mega.input(self.y_data)
                print('back')
            else:
                self.mega.input('g0')
                self.mega.input(self.y_data)
                print('stop')
        elif self.lidar.lidar_data == 'g':
            self.mega.input(self.x_data)
            self.mega.input(self.y_data)
            print('go')
        
            
if __name__ =="__main__":
    rospy.init_node('input_hover')
    command = Command()
    rospy.spin()
            
        