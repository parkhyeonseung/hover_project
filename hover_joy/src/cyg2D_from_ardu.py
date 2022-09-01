#!/usr/bin/env python3
# encoding: utf-8
from ardu_serial import Ardu

cyg = Ardu(port='/dev/ttyUSB0')
hover = Ardu(port="/dev/ttyACM0")
while 1:
    try :
        data = cyg.read().decode()
        if data == 's':
            hover.input('00')
        elif data =='g':
            hover.input('g100')
        elif data =='r':
            hover.input('g0')
            hover.input('t150')
        
    except KeyboardInterrupt :
        cyg.close()
        break