#!/usr/bin/env python3
# encoding: utf-8
import rospy
from hover_joy.msg import arraymsg
from std_msgs.msg import String

class Yolo:
    def __init__(self):
        self.st = '00'
        self.turn_left = 0.4
        self.turn_right = 0.6
        self.detect = 'f'
        self.prev_detect = 'f'
        self.in_middle = 'f'
        self.prev_in_middle='f'
        self.pub_data = 'ffff0'
        self.pub = rospy.Publisher('hover_command',String,queue_size=1)
        rospy.Subscriber('yolo',arraymsg,self.yolocallback,queue_size=1)
        
    def yolocallback(self,xywh):
        if not isinstance(xywh,arraymsg): return
        xywh = xywh.data
        if xywh[1] == 10:
            self.detect = 'f'
            self.in_middle = 'f'
            self.prev_detect = 'f'
            self.st = '00'
        else:
            if xywh[0] == 10:
                self.detect = 'f'
            else:
                self.detect = 't'
            self.prev_detect = 't'
            
            st_speed = xywh[0] - 0.5
            
            if xywh[0] < self.turn_left:
                '''turn left'''
                self.in_middle = 'f'
                self.st = str(st_speed)
                
            elif xywh[0] > self.turn_right:
                '''turn_right'''
                self.in_middle = 'f'
                self.st = str(st_speed)
                
            elif self.turn_left <= xywh[0] <= self.turn_right :
                ''' steer 0'''
                self.in_middle = 't'
                self.st = '0' 
                
        self.pub_data = self.detect+ self.prev_detect + self.in_middle+ self.prev_in_middle + self.st
            
        self.pub.publish(self.pub_data)
        self.prev_in_middle = self.in_middle
        
        
if __name__ == "__main__":
    rospy.init_node('yolo_data')
    yolo = Yolo()
    rospy.spin()