# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:43:00 2019

@author: jeffreyb
"""

from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageRatioInput import *
from time import sleep
import LimitedMotor
import os

class VoltageRatioSensor:
    
    def __init__(self, ser, chan):
        self.sensor = VoltageRatioInput()
        self.sensor.setDeviceSerialNumber(ser)
        self.sensor.setChannel(chan)
        self.sensor.setOnAttachHandler(VoltageRatioSensor.onAttachHandler)
        self.sensor.setOnVoltageRatioChangeHandler(VoltageRatioSensor.onVoltageRatioChangeHandler)

    # what should happen at the moment the sensor is attached
    def onAttachHandler(self):
        None
        
    # what should happen when the sensor is triggered
    def onVoltageRatioChangeHandler(self, volts):
        #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print(volts)
        None
    
    # try to attach the sensor with the provided addressing
    def attach(self):
        try:
            self.sensor.openWaitForAttachment(1000)
            self.sensor.setDataInterval(256)
            return True
        except:
            return False
        
    # detach the sensor if it is attached
    def detach(self):
        try:
            self.sensor.close()
            return True
        except:
            return False
    
    # retrieve the serial number of the controller card being used
    def getCCSerialNum(self):
        self.attach()
        try:
            info = self.sensor.getDeviceSerialNumber()
            self.detach()
            return info
        except:
            self.detach()
            return None
    
    # get the channel number to which the sensor is attached
    def getChannel(self):
        self.attach()
        try:
            info = self.sensor.getChannel()
            self.detach()
            return info
        except:
            self.detach()
            return None
        
    #
    def readVoltageRatio(self):
        self.attach()
        try:
            info = self.sensor.getVoltageRatio()
            self.detach()
            return info
        except:
            self.detach()
            
    #
    def trackVoltageRatio(self):
        self.attach()
        sleep(10)
        self.detach()
        return True