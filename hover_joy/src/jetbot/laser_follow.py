#!/usr/bin/env python3
# coding:utf-8
from cmath import inf
import math
import numpy as np
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from common import ROSCtrl
import rospy
RAD2DEG = 180 / math.pi
command = ''
class laserfollow:
    def __init__(self):
        rospy.on_shutdown(self.cancel)
        self.vel = Twist()
        self.pub_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=3)
        self.ros_ctrl = ROSCtrl()
        self.vel.linear.x = 0
        self.vel.angular.z = 0
        self.pub_vel.publish(Twist())
        self.sub_laser = rospy.Subscriber('/scan',LaserScan, self.follow,queue_size=1)
        
    def cancel(self):
        self.vel.linear.x = 0
        self.vel.angular.z = 0
        self.pub_vel.publish(Twist())
        self.pub_vel.unregister()
        
    def follow(self,scan_data):
        if not isinstance(scan_data,LaserScan):return
        ranges = np.array(scan_data.ranges)
        # print(scan_data.angle_min*RAD2DEG,scan_data.angle_max*RAD2DEG)
        frontDistList = []
        frontDistIDList = []
        minDistList = []
        minDistIDList = []
        for i in range(len(ranges)):
            angle = (scan_data.angle_min + scan_data.angle_increment * i) * RAD2DEG
            if abs(angle) >=160:
                if ranges[i] < 1.5:
                    frontDistList.append(ranges[i])
                    frontDistIDList.append(angle)
                else:
                    self.vel.angular.z = 0
                    self.vel.linear.x = 0
            elif 140 <= angle < 160 :
                minDistList.append(ranges[i])
                minDistIDList.append(angle)
            elif -140 >= angle > -160:
                minDistList.append(ranges[i])
                minDistIDList.append(angle)
                
        if len(frontDistIDList) !=0:
            minDist = min(frontDistList)
            if minDist >0.5:
                self.vel.linear.x = minDist-0.5
            elif 0.4 <minDist:
                self.vel.linear.x = 0
            else :
                self.vel.linear.x = -minDist
        if len(minDistIDList) !=0:
            tminDist = min(minDistList)
            tminDistID = minDistIDList[minDistList.index(tminDist)]
            if (180-abs(tminDistID)) >4:
                if tminDistID <0:
                    self.vel.angular.z = -0.3
                else :
                    self.vel.angular.z = 0.3
            else:
                self.vel.angular.z = 0
        
        if self.ros_ctrl.Joy_active == True:
            self.pub_vel.publish(self.vel)
        else: 
            self.vel.linear.x = 0
            self.vel.angular.z = 0
            self.pub_vel.publish(Twist())
        # self.pub_vel.publish(self.vel)
        
        
if __name__ == '__main__':
    rospy.init_node('laser_follow')
    try :
        laser = laserfollow()
    except KeyboardInterrupt:
        laser = laserfollow()
        laser.cancel()
    rospy.spin()