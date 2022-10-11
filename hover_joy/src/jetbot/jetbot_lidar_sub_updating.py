#!/usr/bin/env python3
# encoding: utf-8
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
import math

class Lidar_sub:
    def __init__(self):
        self.RAD2DEG = 180 / math.pi
        rospy.Subscriber('/scan',LaserScan, self.lidar_callback,queue_size=1)
        
    def lidar_callback(self,scan_data):
        if not isinstance(scan_data,LaserScan):return
        frontDistList = []
        frontDistIDList = []
        ranges = np.array(scan_data.ranges)
        for i in range(len(ranges)):
            angle = (scan_data.angle_min + scan_data.angle_increment * i) * self.RAD2DEG
            if abs(angle) >=170:      
                if ranges[i] < 3:
                    frontDistList.append(ranges[i])
                    frontDistIDList.append(angle) 
                    
        if len(frontDistIDList) !=0:
            self.minDist = min(frontDistList)
        else:
            self.minDist = 4