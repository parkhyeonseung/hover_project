#!/usr/bin/env python3
# encoding: utf-8
import rospy
from std_msgs.msg import String
from jetbot_lidar_sub_updating import Lidar_sub
from geometry_msgs.msg import Twist
from common import ROSCtrl

class Command ():
    def __init__(self):
        self.lidar = Lidar_sub()
        self.ros_ctrl = ROSCtrl()
        self.vel = Twist()
        self.pub_vel = rospy.Publisher('/cmd_vel',Twist,queue_size=3)
        self.x_data = 0
        self.y_data = 0
        self.prev_x_data = 0
        self.prev_y_data = 0
        rospy.Subscriber('hover_command',String,self.yolo_sub,queue_size=1)
            
    def yolo_sub(self,c_data):
        yolo_data = c_data.data
        detect = yolo_data[0]
        prev_detect = yolo_data[1]
        in_middle = yolo_data[2]
        prev_in_middle = yolo_data[3]
        if self.lidar.minDist == 4:
            self.x_data = 0
        else:
            dis_to_vel = self.lidar.minDist*0.4
            if dis_to_vel >1:
                dis_to_vel = 1
            if 0.3<dis_to_vel <0.5:
                dis_to_vel = 0
            elif dis_to_vel <=0.3:
                dis_to_vel = dis_to_vel - 0.5
        
        if detect == 't':
            if in_middle == 't':
                self.x_data = dis_to_vel #####lidar distance
                self.prev_x_data = self.x_data * 0.6
                self.y_data = 0
            else:
                if prev_in_middle == 't':
                    self.x_data = self.prev_x_data
                else:
                    self.x_data = 0
                    
                self.y_data = float(yolo_data[4:])* 1.8
                if self.y_data >1:
                    self.y_data = 1
                self.prev_y_data = self.y_data * 0.6
                
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
                
        self.vel.linear.x = self.x_data
        self.vel.angular.z = self.y_data
        if self.ros_ctrl.Joy_active == True:
            self.pub_vel.publish(self.vel)
        else: 
            self.vel.linear.x = 0
            self.vel.angular.z = 0
            self.pub_vel.publish(self.vel)
            
    def close(self):
        self.vel.linear.x = 0
        self.vel.angular.z = 0
        self.pub_vel.publish(self.vel)
            
if __name__ =="__main__":
    rospy.init_node('input_hover')
    try :
        command = Command()
        rospy.spin()
    except KeyboardInterrupt:
        command.close()
            
        