# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 16:09:57 2019

@author: Patrick Lierle
"""
from LimitedMotor import LimitedMotor
import VoltageRatioSensor as voltageRatioSensor
from time import sleep

class VoltageRatioTrackedMotor(LimitedMotor):
    
    # based on polarity of motor connection
    global OPEN_STATE, STEPS_SCALE_FACTOR
    OPEN_STATE = False
    STEPS_SCALE_FACTOR = 40960
    
    def __init__(self, chan, ser, pos, sensor=None, voltsensor=None, units=None):
            LimitedMotor.__init__(self, chan, ser, pos, sensor=sensor, units=units)
            self.voltSensorAddress = voltsensor

    # moves the motor until it hits a Sensor at which point it stops
    def setVoltagePosition(self, targetVoltage, threshold):
        self.attach()
        try:
            self.setVelocityLimit(383)
            if self.getVoltagePosition() > targetVoltage:
                self.motor.setTargetPosition(2000000)
                while self.getVoltagePosition() > targetVoltage:
                    None
                #self.motor.setVelocityLimit(50)
                #while self.getVoltagePosition() > targetVoltage:
                    #None
                self.detach()
                self.fineTuneVoltage(targetVoltage, threshold)
            elif self.getVoltagePosition() < targetVoltage:
                self.motor.setTargetPosition(-2000000)
                while self.getVoltagePosition() < targetVoltage:
                    None
                #self.motor.setVelocityLimit(50)
                #while self.getVoltagePosition() < targetVoltage:
                    #None
                self.detach()
                self.fineTuneVoltage(targetVoltage, threshold)
            return True
        except:
            self.detach()
            return False
        
    def fineTuneVoltage(self, targetVoltage, threshold):
        try:        
            self.setAcceleration(141)
            if abs(targetVoltage - self.getVoltagePosition()) < threshold:
                return True
            difference = targetVoltage - self.getVoltagePosition()
            self.setRelativePosition(-1 * difference * STEPS_SCALE_FACTOR)
            self.setVoltagePositionV2(targetVoltage)
            return True
        except:
            return False
        
    def getVoltagePosition(self):
        voltSensor = voltageRatioSensor.VoltageRatioSensor(self.voltSensorAddress[0],
                                                 self.voltSensorAddress[1])
        return voltSensor.readVoltageRatio()

boot = VoltageRatioTrackedMotor(0,428122, 0, sensor=(527235,0), voltsensor=(527235,0))
boot.setVelocityLimit(383)

print(boot.getVoltagePosition())

