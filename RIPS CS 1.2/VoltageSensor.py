# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 18:43:00 2019

@author: jeffreyb
"""

from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.VoltageInput import *
from time import sleep

class VoltageSensor:
    
    def __init__(self, ser, chan):
        self.sensor = VoltageInput()
        self.sensor.setDeviceSerialNumber(ser)
        self.sensor.setChannel(chan)
        self.sensor.setOnAttachHandler(VoltageSensor.onAttachHandler)
        self.sensor.setOnVoltageChangeHandler(VoltageSensor.onVoltageChangeHandler)
        self.currentVoltage = self.readVoltage()

    # what should happen at the moment the sensor is attached
    def onAttachHandler(self):
        None
        
    # what should happen when the sensor is triggered
    def onVoltageChangeHandler(self, volts):
        None
    
    # try to attach the sensor with the provided addressing
    def attach(self):
        try:
            self.sensor.openWaitForAttachment(1000)
            self.sensor.setDataInterval(1)
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
    def getVoltage(self):
        return self.currentVoltage
    
    def readVoltage(self):
        self.attach()
        try:
            info = self.sensor.getVoltage()
            self.detach()
            return info
        except:
            self.detach()
            
    def trackVoltage(self):
        self.attach()
        sleep(30)
        self.detach()
        return True