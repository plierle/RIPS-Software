# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:43:18 2019
@author: Patrick Lierle

purpose: to establish a motor object that can open a channel to a stepper
         motor and perform a variety of functions involving its position,
         velocity, and acceleration
"""
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *


class Motor:
    
    def __init__(self, chan, ser, pos, min=None, max=None, units=None):
        self.motor = Stepper()
        self.motor.setChannel(chan)
        self.motor.setDeviceSerialNumber(ser)
        self.pos = int(pos)
        
        self.min = -1000000
        self.max = 1000000
        if not min == None:
            self.min = min
        if not max == None:
            self.max = max
            
        self.rescale = 1.0
        if not units == None:
            if units.lower()[:1] == "d":
                self.rescale = 360/4096
            elif units.lower()[:1] == "r":
                self.rescale = 1/4096
        self.velocityLimit = 200*self.rescale
        self.acceleration = 200*self.rescale
        self.lastMove = 0
        self.name = ""
    
    # what should happen at the moment the motor is attached
    def onAttachHandler(self):
        None
        
    # try to attach the motor then set its rescale factor and engage it
    def attach(self):
        try:
            self.motor.setOnAttachHandler(Motor.onAttachHandler)
            self.motor.openWaitForAttachment(1000)
            self.motor.setRescaleFactor(self.rescale)
            self.motor.setVelocityLimit(self.velocityLimit)
            self.motor.setAcceleration(self.acceleration)
            self.motor.setEngaged(True)
            return True
        except:
            return False
        
    # if there is a motor attached, close it's connection
    def detach(self):
        try:
            self.motor.close()
            return True
        except:
            return False
        
    # retrieve the serial number of the motor controller card
    def getCCSerialNum(self):
        self.attach()
        try:
            info = self.motor.getDeviceSerialNumber()
            self.detach()
            return info
        except:
            self.detach()
            return None
        
    # retrieve the channel of the controller card where the motor is attached
    def getChannel(self):
        self.attach()
        try:
            info = self.motor.getChannel()
            self.detach()
            return info
        except:
            self.detach()
            return None
        
    # retrieve the position the motor thinks it is in (0 at attachment)
    def getMotorPosition(self):
        self.attach()
        try:
            motpos = self.motor.getPosition()
            self.detach()
            return motpos
        except:
            self.detach
            return None

    # retrieve the position being tracked within the Motor object class
    def getPosition(self):
        return self.pos
    
    # retrieve the current rescale factor being applied to the motor
    def getRescaleFactor(self):
        return self.rescale
            
    # return to position zero according to the tracked Motor position 
    def goHome(self):
        return self.setPosition(0)
    
    # returns whether the specified motor is attached or not
    def isConnected(self):
        if self.attach() == False:
            return False
        else:
            self.detach()
            return True
       
    # returns whether the motor is moving or not
    def isMoving(self):
        self.attach()
        try:
            info = self.motor.getVelocity()
            self.detach()
            return not (info == 0)
        except:
            self.detach()
            print("failed")
       
    # set the acceleration of the motor
    def setAcceleration(self, val):
        self.acceleration = float(val)    
    
    # redefine current position as val according to Motor class tracker
    def setCurrentPositionAs(self, val):
        self.pos = int(val)

    # set a target position and moves there from current position
    def setPosition(self, target):
        self.attach()
        if target > self.max:  # if the requested position exceeds the upward bounds
            return False
        elif target < self.min: # if it is less than the minimum
            lm = target - self.pos
            newpos = self.min
        elif self.lastMove > 50 and target < self.pos: # if it requires backlash compensation
            newpos = target
            target -= 25
            lm = target - self.pos - 25
            print("lastmove %d and backlashcorrected pos %d" % (self.lastMove,target))
        else:   # if it is between the bounds
            lm = target - self.pos
            newpos = target
                
        try:
            self.motor.setTargetPosition(target-self.pos)
            while self.motor.getIsMoving():
                None
            self.detach()
            self.lastMove = lm
            self.pos = newpos
            print("END lastmove %d and backlashcorrected pos %d" % (self.lastMove,target))
            return True
        except:
            self.detach
            return False
    
    # set a target position relative to current position and moves there
    def setRelativePosition(self, pos):
        self.attach()
        try:
            self.motor.setTargetPosition(pos)
            self.pos = self.pos + pos
            while self.motor.getIsMoving():
                None
            self.detach()
            self.lastMove = pos
            return True
        except:
            self.detach
            return False
    
    # accept both a rescale factor and position and travel accordingly
    def setRescaledPosition(self, val, pos):
        self.attach()
        try:
            self.rescale = val
            self.motor.setTargetPosition(pos)
            while self.motor.getIsMoving():
                None
            self.detach()
            return True
        except:
            self.detach()
            return False
        
    # set the rescale factor of the motor
    def setRescaleFactor(self, val):
        self.attach()
        try:
            self.rescale = val
            self.detach()
            return True
        except:
            self.detach()
            return False
        
    # set the maximum speed of the motor
    def setVelocityLimit(self, val):
        self.velocityLimit = float(val)