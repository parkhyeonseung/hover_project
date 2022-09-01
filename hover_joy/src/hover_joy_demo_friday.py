#!/usr/bin/env python3
# encoding: utf-8
import time
import rospy
from sensor_msgs.msg import Joy
# from geometry_msgs.msg import Twist
from hover_joy.msg import arraymsg
from ardu_serial import Ardu

class joystick:
    def __init__(self):
        self.hover = Hover()
        self.x = None
        self.x_prev = None
        self.y = None
        self.y_prev = None
        self.step = 30
        self.max_speed = 300
        self.joy = True
        self.data = ['','','0']
        self.joy_dir = "0"
        self.var = 0
        self.sp_speed_prev = None
        self.st_speed_prev = None
        self.yolo_command = True
        self.turn_left = 0.35;
        self.turn_right = 0.65
        self.speed_low = 0.4
        self.speed_high = 0.7
        # self.cancel_time = time.time()
        # self.rate = rospy.Rate(10)
        self.hover.input_hover('000')
        self.sub_joy = rospy.Subscriber('joy',Joy,self.buttoncallback)
        self.sub_yolo = rospy.Subscriber('yolo',arraymsg,self.yolocallback)
        # self.rate.sleep()
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
                       A,
            '''
        if joy_data.buttons[0] == 1:
            self.joy = not self.joy
            self.hover.input_hover('000')
            
        if self.joy == False:
            print('yolo')
        else :
            print('joy')
            
        self.x = round(joy_data.axes[1],1)
        self.y = round(joy_data.axes[0],1)
        if (self.x == self.x_prev) and (self.y == self.y_prev):            
            pass
        
        else:
            if abs(joy_data.axes[1]) > abs(joy_data.axes[0]):
                self.val = ( ( (round(joy_data.axes[1],1))*10 ) )
                self.joy_dir = "x"
            elif abs(joy_data.axes[0]) > abs(joy_data.axes[1]):
                self.val = ( ( (round(joy_data.axes[0],1))*10 )  )
                self.joy_dir = "z"
            elif (joy_data.axes[1] ==0) and (joy_data.axes[0] ==0) :
                self.val = 0
                self.joy_dir = "n"
            else:
                self.joy_dir = '0'
                self.val = 0 
                
            if self.val >9:
                self.val = 9;
                
            self.val = str(int(self.val))
            
            if self.joy == True:
                self.data[0] = 'j'
                self.data[1] = self.joy_dir 
                self.data[2] = self.val
                
                data = ''
                            
                for i in range(3):
                    data += self.data[i]
                    
                self.hover.input_hover(data)
                
            
            self.x_prev = self.x
            self.y_prev = self.y                
                
        # print(data)
        # self.hover.input_hover(data)
        
    def yolocallback(self,xywh):
        # if not isinstance(yolo_data,String): return
        xywh = xywh.data
        if self.joy ==False:
            
            if xywh[0] == 10.:
                self.hover.input_hover('000')
                self.sp_speed_prev =None
                self.sp_speed_prev = None
                self.yolo_command = True
            else:
                area_per = xywh[2] * xywh[3] * 10  ## 0~
                # print(area_per)
                                    
                sp_speed = int((1 - area_per) * 100)
                sp_speed = (sp_speed // 10) * 10
                
                st_speed = int(abs(0.5 -xywh[0]) * 200)
                st_speed = (st_speed // 10 ) *10
                
                if (sp_speed == self.sp_speed_prev) and (st_speed == self.sp_speed_prev):
                    self.yolo_command = False
                    self.sp_speed_prev = sp_speed
                    self.st_speed_prev = st_speed
                else :
                    self.yolo_command = True
                    
                if self.yolo_command :
                    if area_per > self.speed_high :
                        ''' speed down'''
                        sp = 'b' + '-80'
                            
                    elif xywh[0] < self.turn_left:
                        '''turn left'''
                        if st_speed <10:
                            st_speed = 10
                        elif st_speed >90:
                            st_speed = 90
                        sp = 't'+'-'+ str(st_speed+170)
                        
                    elif xywh[0] > self.turn_right:
                        '''turn_right'''
                        if st_speed <10:
                            st_speed = 10
                        elif st_speed >90:
                            st_speed = 90
                        sp = 't' + str(st_speed+170)
                            
                    elif self.turn_left <= xywh[0] <= self.turn_right :
                        ''' steer 0'''
                        if 0.2 <= area_per <= self.speed_low :
                            ''' go '''
                            sp = 'g' +'60'
                        
                        elif area_per < 0.2:
                            ''' speed up'''
                            if sp_speed >99:
                                sp_speed = 90
                            if sp_speed <10:
                                sp_speed = 10
                            sp = 'g'  + str(10 + sp_speed)
                            
                        elif self.speed_low <= area_per <= self.speed_high:
                            ''' speed 0'''
                            sp = '0' + '0'
                            
                    yolo_data = 'y'+sp    ##y
                    # print(yolo_data)
                    self.hover.input_hover(yolo_data)

                    self.sp_speed_prev = sp_speed
                    self.st_speed_prev = st_speed
                
        else :
            pass

if __name__ == "__main__":
    rospy.init_node('joy_ctrl')
    joy = joystick()
    try : rospy.spin()
    except KeyboardInterrupt:
        joy.hover.input_hover('000')
        joy.hover.close_hover()
    except rospy.ROSInterruptException:
        rospy.loginfo('exception')
        
        
            
            
        
        
        
