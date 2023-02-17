# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 18:56:42 2019
@author: Patrick Lierle

Purpose: to fit curves to plots of voltage vs wavelength and voltage vs focus 
that allow RIPS to be able to convert back and forth between any of the three 
quantities for motor movement and position determination
"""
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt

class Curvefit:

    # initialize global variables to be accessed throughout class
    global firstOrderWavelengths, firstOrderBlueVoltages, firstOrderRedVoltages
    global firstOrderBlueWavelengthCoeffs, firstOrderRedWavelengthCoeffs
    global echelleWavelengths, echelleBlueVoltages, echelleRedVoltages
    global echelleBlueWavelengthCoeffs, echelleRedWavelengthCoeffs
    global focusWavelengths, focusVoltages, focusCoeffs

    # generate lists of wavelengths with corresponding (from) red and blue voltages for First Order
    firstOrderWavelengths = [4340,4861,6563]
    firstOrderBlueVoltages = [2.293,2.3993,2.7000]
    firstOrderRedVoltages = [2.3053,2.4054,2.7140]
    # generate lists of wavelengths with corresponding (from) red and blue voltages for Echelle
    echelleWavelengths = [5881.90,5889.95,5895.92]
    echelleBlueVoltages = [2.0159,2.0366,2.0519]
    echelleRedVoltages = [2.0220,2.0391,2.0549]
    # generate lists of wavelengths and corresponding focus voltages
    focusWavelengths = [4101,4340,4861,5800,7060,8115,9120]
    focusVoltages = [4.1496,3.5995,2.9915,2.9249,3.3300,3.7863,4.4591]
    
    # fit a quadratic to the wavelength values for red and blue First Order
    firstOrderBlueWavelengthCoeffs = poly.polyfit(firstOrderWavelengths, firstOrderBlueVoltages, 2)
    firstOrderRedWavelengthCoeffs = poly.polyfit(firstOrderWavelengths, firstOrderRedVoltages, 2)
    # fit a quadratic to the wavelength values for red and blue Echelle
    echelleBlueWavelengthCoeffs = poly.polyfit(echelleWavelengths, echelleBlueVoltages, 2)
    echelleRedWavelengthCoeffs = poly.polyfit(echelleWavelengths, echelleRedVoltages, 2)
    # fit a cubic to the focus data because it is not symmetrical
    focusCoeffs = poly.polyfit(focusWavelengths, focusVoltages, 3)


    # given a wavelength, return an expected voltage value if traveling from blue
    def getVoltageFitFromBlue(x, grating):
        if grating == "Echelle":
            return poly.polyval(x,echelleBlueWavelengthCoeffs)
        elif grating == "First Order":
            return poly.polyval(x,firstOrderBlueWavelengthCoeffs)
        else:
            return False
    
    
    # given a wavelength, return an expected voltage value if traveling from red
    def getVoltageFitFromRed(x, grating):
        if grating == "Echelle":
            return poly.polyval(x,echelleRedWavelengthCoeffs)
        elif grating == "First Order":
            return poly.polyval(x,firstOrderRedWavelengthCoeffs)
        else:
            return False
    
    
    # given a voltage, return an expected wavelength value if traveling from blue
    def getWavelengthFitFromBlue(x, grating):
        # use the quadratic formula to fit a wavelength to a voltage
        if grating == "Echelle":
            a = echelleBlueWavelengthCoeffs[2]
            b = echelleBlueWavelengthCoeffs[1]
            c = echelleBlueWavelengthCoeffs[0] - x
        elif grating == "First Order":
            a = firstOrderBlueWavelengthCoeffs[2]
            b = firstOrderBlueWavelengthCoeffs[1]
            c = firstOrderBlueWavelengthCoeffs[0] - x
        else:
            return False
        discrim = b**2 - 4*a*c
        return (-1*b + np.sqrt(discrim)) / (2*a) 
    
    
    # given a voltage, return an expected wavelength value if traveling from red
    def getWavelengthFitFromRed(x, grating):
        # use the quadratic formula to fit a wavelength to a voltage
        if grating == "Echelle":
            a = echelleRedWavelengthCoeffs[2]
            b = echelleRedWavelengthCoeffs[1]
            c = echelleRedWavelengthCoeffs[0] - x
        elif grating == "First Order":
            a = firstOrderRedWavelengthCoeffs[2]
            b = firstOrderRedWavelengthCoeffs[1]
            c = firstOrderRedWavelengthCoeffs[0] - x
        else:
            return False
        discrim = b**2 - 4*a*c
        return (-1*b + np.sqrt(discrim)) / (2*a) 
 
    
    # given a wavelength, return an expected spectral focus voltage value
    def getFocusFit(x):
        return poly.polyval(x,focusCoeffs)
    
    
    # given a voltage measurement from red, return the expected value from blue
    def switchVoltageToFromBlue(volt, grating):
        wavelength = Curvefit.getWavelengthFitFromRed(volt, grating)
        return Curvefit.getVoltageFitFromBlue(wavelength, grating)
    
    
    # given a voltage measurement from blue, return the expected value from red
    def switchVoltageToFromRed(volt, grating):
        wavelength = Curvefit.getWavelengthFitFromBlue(volt, grating)
        return Curvefit.getVoltageFitFromRed(wavelength, grating)
    
    
    # generate a plot with position voltage and focus voltage vs wavelength
    def visualize():
        blueCurve = poly.polyval(echelleWavelengths,echelleBlueWavelengthCoeffs)
        redCurve = poly.polyval(echelleWavelengths,echelleRedWavelengthCoeffs)
        #focusCurve = poly.polyval(focusWavelengths,focusCoeffs)
        plt.scatter(echelleWavelengths,echelleBlueVoltages)
        plt.scatter(echelleWavelengths,echelleRedVoltages)
        #plt.scatter(focusWavelengths,focusVoltages)
        plt.plot(echelleWavelengths,blueCurve)
        plt.plot(echelleWavelengths,redCurve)
        #plt.plot(focusWavelengths,focusCurve)
        
Curvefit.visualize()
print(Curvefit.getVoltageFitFromBlue(3777,'Echelle'))