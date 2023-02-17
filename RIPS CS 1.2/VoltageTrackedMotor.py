# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 16:09:57 2019
@author: Patrick Lierle

"""
from Motor import Motor
import VoltageSensor as voltageSensor
from Curvefit import Curvefit as fit

class VoltageTrackedMotor(Motor):
    
    
    def __init__(self, chan, ser, scalefactor, voltsensor=None, units=None, 
                 min=None, max=None):
        Motor.__init__(self, chan, ser, 0, units=units)
        self.voltSensorAddress = voltsensor
        self.scalefactor = scalefactor
        self.min = 0
        self.max = 0
        if not min==None:
            self.min = min
        if not max==None:
            self.max = max
        self.motor.setOnPositionChangeHandler(VoltageTrackedMotor.onPositionChangeHandler)
    
    
    def onPositionChangeHandler(self, position):
        None
        
        
    # get an accurate average voltage position of a motor by examining 20
    # individual voltage readings and disregarding noise in the measurements
    def getAverageVoltagePosition(self):
        # fill an array with 20 individual voltage readings for the motor
        voltages = []
        for i in range(20):
            volts = self.getVoltagePosition()
            voltages.append(volts)
        # fill another array with the 20 voltages truncated to 2 decimal places
        truncatedVoltages = [float(str(elem)[:4]) for elem in voltages]
        # determine the mode of this truncated array and call it shortMode
        shortMode = max(set(truncatedVoltages), key=truncatedVoltages.count)
        # fill a final array with those of the 20 voltages that have the same 
        # 2 decimal truncation as the shortMode, call this weededVoltages
        weededVoltages = []
        for i in voltages:
            if float(str(i)[:4]) == shortMode:
                weededVoltages.append(i)
        # finally, return the mode of this array, which is the selective mode
        # of the first 20 readings after removing noise
        return max(set(weededVoltages), key=weededVoltages.count)
        
    
    # move the motor to a specific voltage read by the slide potentiometer
    def goToVoltage(self, targVoltage, count, targetWavelength):
        targetVoltage = targVoltage
        # ensure the requested position does not exceed the bounds of the motor
        if targetVoltage < self.min or targetVoltage > self.max:
            raise ValueError("entered value is outside of voltage bounds " 
                             "[%.4f-%.4f]" % (self.min,self.max))
        print(count)
        # determine the current voltage position of the motor by averaging
        currentVoltage = self.getAverageVoltagePosition()
        # end routine if motor has arrived or has timed out
        if abs(targetVoltage - currentVoltage) < 0.0005 or count > 10:
            return True
        # calculates 73% of the estimated number of steps to get to target so 
        # as not to overshoot the target
        stepsize = (targetVoltage - currentVoltage)*self.scalefactor*0.73
        print("stepsize = %f" % stepsize)
        # moves the 73%
        self.setRelativePosition(stepsize)
        # repeats until at target or timed out
        self.goToVoltage(targVoltage, count+1, targetWavelength)
    
    
    # alternative first stage (count==1) of voltage targeting that also focuses
    def goToVoltageAndFocus(self, targVoltage, focusmotor, targetFocusVoltage, targetWavelength, grating):
        targetVoltage = targVoltage
        # ensure the requested position does not exceed the bounds of the motor
        if targetVoltage < self.min or targetVoltage > self.max:
            raise ValueError("entered value: %.4f is outside of voltage bounds " 
                             "[%.4f-%.4f]" % (targetVoltage,self.min,self.max))
        # determine the current voltage position of the motor by averaging
        currentVoltage = self.getAverageVoltagePosition()
        # accomodate the case where the two estimations of voltage for the target
        # wavelength overlap the estimations for the current wavelength
        # this happens when traveling small distances and changing direction
        if self.lastMove == 0:
            currentWavelength = ((fit.getWavelengthFitFromBlue(currentVoltage, grating)
                                +fit.getWavelengthFitFromRed(currentVoltage, grating))/2.0)
        elif self.lastMove > 0:
            currentWavelength = fit.getWavelengthFitFromBlue(currentVoltage, grating)
        elif self.lastMove < 0:
            currentWavelength = fit.getWavelengthFitFromRed(currentVoltage, grating)
        
        if targetWavelength > currentWavelength and targetVoltage < currentVoltage:
            print("CONVERTED")
            currentVoltage = (currentVoltage +
                              fit.switchVoltageToFromBlue(currentVoltage, grating))/2
            targetVoltage = (targetVoltage + 
                              fit.switchVoltageToFromRed(targetVoltage, grating))/2
            stepsize = (targetVoltage-currentVoltage)*self.scalefactor + 50
            
        elif targetWavelength < currentWavelength and targetVoltage > currentVoltage:
            print("CONVERTED")
            currentVoltage = (currentVoltage +
                              fit.switchVoltageToFromRed(currentVoltage, grating))/2
            targetVoltage = (targetVoltage + 
                              fit.switchVoltageToFromBlue(targetVoltage, grating))/2
            stepsize = (targetVoltage-currentVoltage)*self.scalefactor - 50
        else:
            # calculate 73% of the estimated number of steps to get to target so 
            # as not to overshoot the target
            stepsize = (targetVoltage - currentVoltage)*self.scalefactor*0.73
            print("stepsize = %f" % stepsize)
        # end routine if motor has arrived or has timed out
        print("UPDATED target %f and current %f" % (targetVoltage,currentVoltage))
        if abs(targetVoltage - currentVoltage) < 0.0005:
            return True
        # determine how many steps to move focus motor
        currentFocusVoltage = focusmotor.getAverageVoltagePosition()
        print("current focus voltage %f: " % currentFocusVoltage)
        focusSteps = (targetFocusVoltage - currentFocusVoltage)*focusmotor.scalefactor
        print("target focus voltage %f: " % targetFocusVoltage)
        print("focus steps %f: " % focusSteps)
        # attach focus motor and grating motor
        focusmotor.attach()
        self.attach()
        print("FM ATTACHED")
        # move focus motor and grating motor
        focusmotor.motor.setTargetPosition(focusSteps)
        print("FM MOVING")
        self.motor.setTargetPosition(stepsize)
        # do nothing until both motors are stopped
        while self.motor.getIsMoving() or focusmotor.motor.getIsMoving():
            None
        self.detach()
        focusmotor.detach()
        self.lastMove = stepsize
        print("FM DETACHED")
        # continue next stage of voltage targeting now that focus is complete
        if targVoltage == targetVoltage:
            self.goToVoltage(targetVoltage, 2, targetWavelength)
        
        
    def setPosition(self, pos):
        currentVoltage = self.getAverageVoltagePosition()
        print("CV %d" % currentVoltage)
        targetVoltage = pos
        print("TV %d" % targetVoltage)
        print("SF %d" % self.scalefactor)
        if self.lastMove < 0:
            stepsize = (targetVoltage-currentVoltage)*self.scalefactor + 50
            
        elif self.lastMove > 0:
            stepsize = (targetVoltage-currentVoltage)*self.scalefactor - 50
        else:
            stepsize = (targetVoltage-currentVoltage)*self.scalefactor
        print("STEPSIZE B: %d" % stepsize)
        self.setRelativePosition(stepsize)
    
        
    # set a target steps position relative to current position and move there
    def setRelativePosition(self, pos):
        # ensure the requested position does not exceed the bounds of the motor
        finalVolts = self.getVoltagePosition() + pos * self.scalefactor**(-1)
        print("FV: %f     pos: %f    sf: %f    cp: %f" % (finalVolts, pos, self.scalefactor, self.getVoltagePosition()))
        if finalVolts > self.max or finalVolts < self.min:
            raise ValueError("entered value would exceed voltage bounds "
                             "[%.4f-%.4f]" % (self.min,self.max))
        try:
            # account for backlash
            if pos > 0 and self.lastMove < 0:
                pos += 50
            elif pos < 0 and self.lastMove > 0:
                pos -= 50
            self.attach()
            print("start: %f" % self.motor.getPosition())
            # issue command to motor to move to new position
            self.motor.setTargetPosition(pos)
            # allow motor to finish moving before continuing
            while self.motor.getIsMoving():
                None
            print("end: %f" % self.motor.getPosition())
            # to ensure the update wavelength works right 
            if abs(pos) > 50:
                self.lastMove = pos
            print(pos)
            print(self.lastMove)
            self.detach()
            return True
        except:
            self.detach
            print("FAILED")
            return False
        
    
    # get a one-time voltage reading from the associated voltage input
    def getVoltagePosition(self):
        voltSensor = voltageSensor.VoltageSensor(self.voltSensorAddress[0],
                                                 self.voltSensorAddress[1])
        return voltSensor.readVoltage()

#mot = VoltageTrackedMotor(1,428122,42776,
#                          voltsensor=(527235,0), min=0.0392, max=4.1026)
#mot.setRelativePosition(-150)
#print(mot.getAverageVoltagePosition())