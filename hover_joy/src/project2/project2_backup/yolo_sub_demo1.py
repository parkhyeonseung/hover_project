#!/usr/bin/env python3
# encoding: utf-8
import rospy
from hover_joy.msg import arraymsg
from std_msgs.msg import String
from joy_sub_updating import Joystick

class Yolo:
    def __init__(self):
        self.joystick = Joystick()
        self.sp = '00'
        self.st = '00'
        self.x = None
        self.y = None
        self.sp_speed_prev = 0
        self.st_speed_prev = 0
        self.turn_left = 0.4
        self.turn_right = 0.6
        self.speed_low = 0.3
        self.speed_high = 0.6
        self.sp = 'g0'
        self.st = 't0'
        self.pub_data = '0000'
        self.pub = rospy.Publisher('hover_command',String,queue_size=1)
        rospy.Subscriber('yolo',arraymsg,self.yolocallback,queue_size=1)
        
    def yolocallback(self,xywh):
        if not isinstance(xywh,arraymsg): return
        if self.joystick.yolo == True:
            xywh = xywh.data
            if xywh[0] == 10.:
                self.pub_data = 's0s0'
                self.sp_speed_prev =0
            else:
                area_per = xywh[2] * xywh[3] * 10  ## 0~
                
                sp_speed = int((1 - area_per) * 100)
                sp_speed = (sp_speed // 10) * 10
                
                st_speed = int(abs(0.5 -xywh[0]) * 200)
                st_speed = (st_speed // 10 ) *10
                
                self.sp_speed_prev = sp_speed
                self.st_speed_prev = st_speed
                
                    ##speed limit###
                if st_speed <10:
                    st_speed = 10
                elif st_speed >90:
                    st_speed = 90
                    ####################
                    
                if xywh[0] < self.turn_left:
                    '''turn left'''
                    if self.sp[1] == '0':
                        self.st = 't'+'-'+ str(st_speed+170)
                    else:
                        self.st = 't'+'-'+ str(st_speed+60)
                elif xywh[0] > self.turn_right:
                    '''turn_right'''
                    if self.sp[1] == '0':
                        self.st = 't'+ str(st_speed+170)
                    else:
                        self.st = 't'+ str(st_speed+60)
                elif self.turn_left <= xywh[0] <= self.turn_right :
                    ''' steer 0'''
                    self.st = 't0' 
                
                if self.speed_low <= area_per <= self.speed_high:
                    ''' speed 0'''
                    self.sp = 'g' + '0'
                elif area_per > self.speed_high :
                    ''' back'''
                    self.sp = 'b' + '-90'
                elif  area_per < self.speed_low :
                    ''' go up'''
                    self.sp = 'g' +str(sp_speed+10)
                    
                self.pub_data = self.sp+self.st
                
            self.pub.publish(self.pub_data)
        else :
            return
        
        
if __name__ == "__main__":
    rospy.init_node('yolo_data')
    yolo = Yolo()
    rospy.spin()