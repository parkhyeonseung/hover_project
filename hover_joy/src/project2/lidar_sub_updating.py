#!/usr/bin/env python3
# encoding: utf-8
import rospy
from std_msgs.msg import String
class Lidar_sub:
    def __init__(self):
        rospy.Subscriber('lidar_data',String,self.lidar_callback,queue_size=1)
        
    def lidar_callback(self,data):
        self.lidar_data = data.data