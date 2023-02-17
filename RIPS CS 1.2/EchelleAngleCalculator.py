# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:43:18 2019
@author: Patrick Lierle

purpose: to provide functions that accept a wavelength and return the echelle
         grating angle at which that wavelength is visible for all orders, a
         given order, or the optimum (by throughput) order
"""

import numpy as np

class EchelleAngleCalculator:
    
    # ld is the lin density of the echelle, d is the dispersion and insext is 
    # the angle between the incident and diffracted beams
    global ld, d, insext, pi, blaze
    ld = 31.6
    d = 1/ld * 10**7
    insext = 1.6
    pi = np.pi
    blaze = 180/pi * np.arctan(2)
    
    
    # given a wavelength and desired order, return angle of incidence in degrees
    # that will position the wavelength in the center of the ccd
    def findEchelleAngleForOrder(wave, order):
        # use the wavelength-angle equation documented in the user manual
        A = -1*np.sqrt(4*(d**2)*(np.cos(pi/225)**2)-(wave**2)*(order**2))
        B = d+d*np.cos(2*pi/225)
        C = d*np.sin(2*pi/225)+wave*order
        theta = 360/pi * np.arctan((A+B)/C)
        return theta
        
    
    # given a wavelength and desired range of orders, return angles of incidence 
    # in degrees that will position the wavelength in the center of the ccd.
    # inclusive at both bounds
    def findEchelleAngleForOrderRange(wave, minorder, maxorder):
        # use the wavelength-angle equation documented in the user manual
        A = []
        B = d+d*np.cos(2*pi/225)
        C = []
        for i in range(minorder,maxorder+1):
            A.append(-1*np.sqrt(4*(d**2)*(np.cos(pi/225)**2)-(wave**2)*(i**2)))
            C.append(d*np.sin(2*pi/225)+wave*i)
        thetas = 360/pi * np.arctan((A+B)/C)
        return thetas
        
        
    def findBestEchelleAngle(wave):
        # obtain list of angles for full range of legitimate orders
        thetas = EchelleAngleCalculator.findEchelleAngleForOrderRange(wave, 0, 107)
        # make a list of the distance to the blaze angle from each incident angle
        blazeDifference = list(abs(blaze - thetas))
        # find at what order the above is minimized
        bestOrder = blazeDifference.index(min(blazeDifference))
        # retrieve the angle for that order
        bestTheta = thetas[bestOrder]
        return bestTheta, bestOrder
        
    
    
print(EchelleAngleCalculator.findBestEchelleAngle(6563))