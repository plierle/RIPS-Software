# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:43:18 2019
@author: Patrick Lierle

purpose: to create a blueprint for sensor objects which can be used to find
        motor position
"""
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.DigitalInput import *

class Sensor:
    
    global change
    change = 0
    
    def __init__(self, ser, chan):
        self.sensor = DigitalInput()
        self.sensor.setDeviceSerialNumber(ser)
        self.sensor.setChannel(chan)
        self.sensor.setOnAttachHandler(Sensor.onAttachHandler)
        self.sensor.setOnStateChangeHandler(Sensor.onStateChangeHandler)

    # what should happen at the moment the sensor is attached
    def onAttachHandler(self):
        None

    # what should happen when the sensor is triggered
    def onStateChangeHandler(self, state):
        global change
        change += 1
        print(change)
        if change >= 2:
            return True
    
    # try to attach the sensor with the provided addressing
    def attach(self):
        try:
            self.sensor.openWaitForAttachment(1000)
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
    
    # get the current state (T/F) of the switch
    def getState(self):
        self.attach()
        try:
            state = self.sensor.getState()
            self.detach()
            return state
        except:
            self.detach()
    
    # check and see if the sensor is actually able to attach
    def isConnected(self):
        if self.attach() == False:
            return False
        else:
            self.detach()
            return True
    
    # when sensor is triggered after intial trigger, return true
    def trackChanges(self):
        global change
        change = 0
        self.attach()
        while change < 2:
            None
        if self.getState() == False:
            self.detach()
            return True
        else: self.detach