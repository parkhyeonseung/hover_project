#!/usr/bin/env python3
# encoding: utf-8
from ardu_serial import Ardu
import rospy
from std_msgs.msg import String

class Lidar:
    def __init__(self):
        self.cyg = Ardu(port='/dev/ttyUNO')
        self.pub_lidar = rospy.Publisher('lidar_data',String,queue_size=1)
        self.string = String()
        
    def read(self):
        self.data = self.cyg.read().decode()
        self.string.data = self.data
        self.pub_lidar.publish(self.string)
        # print(self.data)
            
if __name__ =="__main__":
    rospy.init_node("lidar_read")
    lidar = Lidar()
    while not rospy.is_shutdown():
        try:
            lidar.read()
        except KeyboardInterrupt:
            lidar.cyg.close()
            break
            
            
        