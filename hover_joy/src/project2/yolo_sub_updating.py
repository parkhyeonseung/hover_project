#!/usr/bin/env python3
# encoding: utf-8
import rospy
from hover_joy.msg import arraymsg
from std_msgs.msg import String
from joy_sub_updating import Joystick

class Yolo:
    def __init__(self):
        self.joystick = Joystick()
        self.st = '00'
        self.turn_left = 0.4
        self.turn_right = 0.6
        self.detect = 'f'
        self.in_middle = 'f'
        self.pub_data = '0000'
        self.pub = rospy.Publisher('hover_command',String,queue_size=1)
        rospy.Subscriber('yolo',arraymsg,self.yolocallback,queue_size=1)
        
    def yolocallback(self,xywh):
        if not isinstance(xywh,arraymsg): return
        if self.joystick.yolo == True:
            xywh = xywh.data
            if xywh[0] == 10.:
                self.detect = 'f'
                self.in_middle = 'f'
                self.prev_detect = 'f'
                self.st = '00'
            else:
                if xywh[1] != 0:
                    self.detect = 'f'
                else:
                    self.detect = 't'
                self.prev_detect = 't'
                
                st_speed = int(abs(0.5 -xywh[0]) * 200)
                st_speed = (st_speed // 10 ) *10
                
                    ##speed limit###
                if st_speed <10:
                    st_speed = 10
                elif st_speed >90:
                    st_speed = 90
                    ####################
                    
                if xywh[0] < self.turn_left:
                    '''turn left'''
                    self.in_middle = 'f'
                    self.st = 't'+'-'+ str(st_speed+170)
                    
                elif xywh[0] > self.turn_right:
                    '''turn_right'''
                    self.in_middle = 'f'
                    self.st = 't'+ str(st_speed+170)
                    
                elif self.turn_left <= xywh[0] <= self.turn_right :
                    ''' steer 0'''
                    self.in_middle = 't'
                    self.st = 't0' 
                    
                self.pub_data = self.detect+ self.prev_detect + self.in_middle+ self.prev_in_middle + self.st
                
            self.pub.publish(self.pub_data)
            self.prev_in_middle = self.in_middle
        else :
            return
        
        
if __name__ == "__main__":
    rospy.init_node('yolo_data')
    yolo = Yolo()
    rospy.spin()