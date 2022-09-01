#!/usr/bin/env python3
# encoding: utf-8
import rospy
from sensor_msgs.msg import Joy
# from geometry_msgs.msg import Twist
from hover_joy.msg import arraymsg
from ardu_serial import Ardu
# v 8_31
class joystick:
    def __init__(self):
        self.hover = Ardu()
        self.sp = '00'
        self.st = '00'
        self.x = None
        self.y = None
        self.joy = False
        self.yolo = False
        self.sp_speed_prev = 0
        self.st_speed_prev = 0
        self.turn_left = 0.4
        self.turn_right = 0.6
        self.speed_low = 0.4
        self.speed_high = 0.7
        self.sp = 'g0'
        self.st = 't0'
        self.hover.input('00')
        rospy.Subscriber('joy',Joy,self.buttoncallback,queue_size=1)
        rospy.Subscriber('yolo',arraymsg,self.yolocallback,queue_size=1)
        print('done')
        
    def buttoncallback(self, joy_data):
        if not isinstance(joy_data,Joy): return
        '''
        :jetson joy_data:
            axes 8: [0.0, -0.0, -0.0, -0.0, 0.0, 0.0, 0.0, 0.0]
            ## left joy
            axes[0] : + left/- right
            axes[1] : + front/- back
            ## right joy
            axes[2] : + left/- right
            axes[3] : + front/- back
         buttons 15:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                       A, B, '',X, Y, '','',R1,'',R2
            '''
        if joy_data.buttons[1] == 1:   ## B stop
            self.hover.input('00')
            self.hover.input('00')
            print('stop')
            self.joy = False
            self.yolo = False
        elif joy_data.buttons[0] == 1:   ## A mode joy
            self.hover.input('00')
            self.hover.input('00')
            print('joy')
            self.joy = True
            self.yolo = False
        elif joy_data.buttons[3] == 1:   # X mode yolo
            self.hover.input('00')
            self.hover.input('00')
            print('yolo')
            self.joy = False
            self.yolo = True
            
        if self.joy == True:
            x_data =  ( (round(joy_data.axes[1],1))*10 ) 
            y_data =  ( (round(joy_data.axes[0],1))*10 ) *-1
            x_data = 'g'+str(int(x_data*30))
            y_data = 't'+str(int(y_data*30))
            if (joy_data.axes[1] ==0) and (joy_data.axes[0] ==0) :
                x_data = 's0'
                y_data = 's0'
            self.hover.input(x_data)
            self.hover.input(y_data)  
        
    def yolocallback(self,xywh):
        xywh = xywh.data
        if self.yolo == True:
            
            if xywh[0] == 10.:
                self.hover.input('s0')
                self.hover.input('s0')
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
                
                self.hover.input(self.st)
                    
                if self.speed_low <= area_per <= self.speed_high:
                    ''' speed 0'''
                    self.sp = 'g' + '0'
                elif area_per > self.speed_high :
                    ''' back'''
                    self.sp = 'b' + '-90'
                elif  area_per < self.speed_low :
                    ''' go up'''
                    self.sp = 'g' +str(sp_speed+50)
                    
                self.hover.input(self.sp)
        else :
            return

if __name__ == "__main__":
    rospy.init_node('joy_ctrl')
    joy = joystick()
    try : rospy.spin()
    except KeyboardInterrupt:
        joy.hover.input('00')
        joy.hover.close()
    except :
        joy.hover.input('00')
        joy.hover.close()
        
        
            
            
        
        
        
