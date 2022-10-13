#!/usr/bin/env python3
# encoding: utf-8
import time
import serial
import os,sys

class Ardu():
    def __init__(self,port = "/dev/ttyMEGA",baudrate = 115200):
        self.port = port
        self.stop = '00'
        self.data = '00'
        try : self.ser = serial.Serial(port =self.port, baudrate = baudrate)
        except : 
            print('port error ')
        
    def read(self):
        return self.ser.read()
        
    def input(self,data):
        if self.ser.readable():
            self.data = data
            try :
                self.ser.write(self.data.encode('utf-8'))
                time.sleep(0.2)
                return True
                
                
            except KeyboardInterrupt :
                self.ser.write(self.stop.encode())
                self.ser.close()
                return False
            
            except  :
                self.ser.write(self.stop.encode())
                self.ser.close()
                return False
        else:
            print('check your port')
            return False
        
    def close(self):
        self.ser.close()
        time.sleep(0.2)



if __name__ == "__main__":
    hover = Ardu()
