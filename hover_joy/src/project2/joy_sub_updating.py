#!/usr/bin/env python3
# encoding: utf-8
import rospy
from sensor_msgs.msg import Joy
from hover_joy.msg import arraymsg
from std_msgs.msg import String
class Joystick:
    def __init__(self):
        self.joy = False
        self.yolo = False
        self.pub_data = '0000'
        self.pub = rospy.Publisher('hover_command',String,queue_size=1)
        print('done')
        rospy.Subscriber('joy',Joy,self.buttoncallback)
        
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
            print('stop')
            self.pub_data = '0000'
            self.joy = False
            self.yolo = False
        elif joy_data.buttons[0] == 1:   ## A mode joy
            print('joy')
            self.pub_data = '0000'
            self.joy = True
            self.yolo = False
        elif joy_data.buttons[3] == 1:   # X mode yolo
            print('yolo')
            self.pub_data = '0000'
            self.joy = False
            self.yolo = True
            
        if self.joy == True:
            x_data =  ( (round(joy_data.axes[1],1))*10 ) 
            y_data =  ( (round(joy_data.axes[0],1))*10 ) *-1
            x_data = 'g'+str(int(x_data*15))
            y_data = 't'+str(int(y_data*30))
            if (joy_data.axes[1] ==0) and (joy_data.axes[0] ==0) :
                x_data = 's00'
                y_data = 's00'
            self.pub_data = x_data+y_data
        self.pub.publish(self.pub_data)
        
if __name__ == "__main__":
    rospy.init_node('joystick')
    joystick = Joystick()
    rospy.spin()