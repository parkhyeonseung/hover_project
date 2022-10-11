#!/usr/bin/env python
# coding:utf-8
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
class ROSCtrl:
    def __init__(self):
        self.Joy_active = False
        self.sub_JoyState = rospy.Subscriber('joy', Joy, self.JoyStateCallback)

    def JoyStateCallback(self, msg):
        if not isinstance(msg, Joy): return
        if msg.buttons[1] == 1:  #B
            self.Joy_active = False
        elif msg.buttons[0] == 1: #A
            self.Joy_active = True

class SinglePID:
    def __init__(self, P=0.1, I=0.0, D=0.1):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        print("init_pid: ", P, I, D)
        self.pid_reset()

    def Set_pid(self, P, I, D):
        self.Kp = P
        self.Ki = I
        self.Kd = D
        print("set_pid: ", P, I, D)
        self.pid_reset()

    def pid_compute(self, target, current):
        self.error = target - current
        self.intergral += self.error
        self.derivative = self.error - self.prevError
        result = self.Kp * self.error + self.Ki * self.intergral + self.Kd * self.derivative
        self.prevError = self.error
        return result

    def pid_reset(self):
        self.error = 0
        self.intergral = 0
        self.derivative = 0
        self.prevError = 0