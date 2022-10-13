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
        # print(len(ranges))    # 160
        # print(scan_data.angle_min) # -1.0471975803375244
        # print(scan_data.angle_increment)  #0.013089969754219055
        # print(self.RAD2DEG) # 57.29577951308232
        for i in range(len(ranges)):            
            angle = (scan_data.angle_min + scan_data.angle_increment * i) * self.RAD2DEG # ang -60~ 60
            if abs(angle) <=2:
                # print(angle, ranges[i])
                if ranges[i] != math.inf:      
                    frontDistList.append(ranges[i])
                    frontDistIDList.append(angle) 
        
        print("    ")        
        if len(frontDistIDList) !=0:
            self.minDist = min(frontDistList)
        else:
            self.minDist = 0
            
        # print(self.minDist)
        # -2.2500000626119543 3.5929999351501465
        # -2.2500000626119543 3.5929999351501465
        # -1.5000000417413029 inf
        # -1.5000000417413029 inf
        # -0.7500000208706514 inf
        # -0.7500000208706514 inf
        # 0.0 inf
        # 0.0 inf
        # 0.7500000208706514 inf
        # 0.7500000208706514 inf
        # 1.5000000417413029 inf
        # 1.5000000417413029 inf
        # 2.2500000626119543 inf
        # 2.2500000626119543 inf    
if __name__ =="__main__":
    rospy.init_node("lidar_read")
    lidar = Lidar()
    rospy.spin()