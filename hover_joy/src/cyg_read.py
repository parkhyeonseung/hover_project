#!/usr/bin/env python3
# encoding: utf-8
from ardu_serial import Ardu
import rospy
from std_msgs.msg import String


class Lidar ():
    def __init__(self):
        self.cyg = Ardu(port='/dev/ttyUNO')
        self.cyg_pub = rospy.Publisher('cyg_data',String,queue_size=1)
        self.data = 'w'
        self.pre_data = 'w'
        
    def read(self):
        self.data = self.cyg.read().decode()
        print(self.data)
            
if __name__ =="__main__":
    rospy.init_node('cyg_read')
    lidar = Lidar()
    while not rospy.is_shutdown():
        try:
            lidar.read()
        except KeyboardInterrupt:
            lidar.cyg.close()
            break
            
            
        