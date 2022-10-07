#!/usr/bin/env python3
# encoding: utf-8
from ardu_serial import Ardu

class Lidar ():
    def __init__(self):
        self.cyg = Ardu(port='/dev/ttyUNO')
        self.data = 'w'
        self.pre_data = 'w'
        while 1:
            try:
                self.read()
            except KeyboardInterrupt:
                self.cyg.close()
                break
        
    def read(self):
        self.data = self.cyg.read().decode()
        # print(self.data)
            
if __name__ =="__main__":
    lidar = Lidar()
    while 1:
        try:
            lidar.read()
        except KeyboardInterrupt:
            lidar.cyg.close()
            break
            
            
        