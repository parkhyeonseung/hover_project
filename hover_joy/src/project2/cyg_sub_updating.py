#!/usr/bin/env python3
# encoding: utf-8
from cmath import inf
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import numpy as np
import math

class Lidar:
    def __init__(self):
        self.pub_lidar = rospy.Publisher('lidar_data',String,queue_size=1)
        self.string = String()
        self.RAD2DEG = 180/math.pi
        rospy.Subscriber('scan_laser',LaserScan,self.laser_callback,queue_size=1)
        
    def laser_callback(self,scan_data):
        ## -60 ~ 60
        if not isinstance(scan_data,LaserScan):return
        frontDistList = []
        frontDistIDList = []
        ranges = np.array(scan_data.ranges)
        for i in range(len(ranges)):
            angle = (scan_data.angle_min + scan_data.angle_increment * i) * self.RAD2DEG
            if abs(angle) <=5:
                if ranges[i] != math.inf:      
                    frontDistList.append(ranges[i])
                    frontDistIDList.append(angle) 
                
        if len(frontDistIDList) !=0:
            self.minDist = min(frontDistList)
            
        else:
            self.minDist = 0
            
        # print(self.minDist)
            
if __name__ =="__main__":
    rospy.init_node("lidar_read")
    lidar = Lidar()
    rospy.spin()