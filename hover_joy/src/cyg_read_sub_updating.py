#!/usr/bin/env python3
# encoding: utf-8
from ardu_serial import Ardu
import rospy
from std_msgs.msg import String
import threading
cyg_data='w'
x_data = '00'
y_data = '00'
class Lidar ():
    def __init__(self):
        global cyg_data,x_data,y_data
        self.cyg = Ardu(port='/dev/ttyUNO')
        self.mega = Ardu(port='/dev/ttyMEGA')
        cyg_data = 'w'
        x_data = '00'
        y_data = '00'
        rospy.Subscriber('hover_command',String,self.yolo_sub,queue_size=1)
        
    def read(self):
        global cyg_data,x_data,y_data
        while not rospy.is_shutdown():
            cyg_data = self.cyg.read().decode()
            if cyg_data == 'w':
                self.mega.input('00')
            elif cyg_data == 's':
                if '-' in x_data:
                    self.mega.input(x_data)
                    self.mega.input(y_data)
                    print('back')
                else:
                    self.mega.input('g0')
                    self.mega.input(y_data)
                    print('stop')
            else :print('go')           
                     
    def yolo_sub(self,c_data):
        global cyg_data,x_data,y_data
        yolo_data = c_data.data
        t_idx = yolo_data.find('t')
        if t_idx:
            x_data = yolo_data[0:t_idx]
            y_data = yolo_data[t_idx:]
        else:
            x_data = yolo_data[0:2]
            y_data = yolo_data[2:]
        if cyg_data == 'g':
            self.mega.input(x_data)
            self.mega.input(y_data)
            
if __name__ =="__main__":
    rospy.init_node('input_hover')
    lidar = Lidar()
    th1 = threading.Thread(target = lidar.read())
    try:
        th1.start()
        th1.join()
        rospy.spin()
    except KeyboardInterrupt:
        lidar.cyg.close()
        lidar.mega.close()
            
            
        