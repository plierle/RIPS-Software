# -*- coding: utf-8 -*-
"""
Created on Tue May 28 11:52:42 2019
@author: Patrick Lierle

purpose: to create a savefile from the control panel with all settings that
can be read to revert the control panel to the saved settings
"""
import os
import datetime as dt
import shutil

class Savefile:

    def __init__(self):
        try:
            autosaveSettings = Savefile.readFile('saves\\autosave.txt')
            self.prefilter = autosaveSettings[0]
            self.spectralFilterSetting = autosaveSettings[1]
            self.imagingFilterSetting = autosaveSettings[2]
            self.slitSteps = int(autosaveSettings[3])
            self.slitAngle = float(autosaveSettings[4])
            self.rotiserizerSteps = int(autosaveSettings[5])
            self.rotiserizerAngle = float(autosaveSettings[6])
            self.rotiserizerVolts = float(autosaveSettings[7])
            self.spectralFocusSteps = int(autosaveSettings[8])
            self.spectralFocusVolts = float(autosaveSettings[9])
            self.imagingFocusSteps = int(autosaveSettings[10])
            self.imagingFocusVolts = float(autosaveSettings[11])
            self.wavelength = int(autosaveSettings[12])
            self.gratingAngleVolts = float(autosaveSettings[13])
            self.lastMove = int(autosaveSettings[14])
            self.platescale = float(autosaveSettings[15])
            self.grating = autosaveSettings[15]
        except:
            self.prefilter = "NONE"
            self.spectralFilterSetting = "OPEN"
            self.imagingFilterSetting = "OPEN"
            self.slitSteps = 0
            self.slitAngle = 0
            self.rotiserizerSteps = 0
            self.rotiserizerAngle = 0
            self.rotiserizerVolts = 0
            self.spectralFocusSteps = 0
            self.spectralFocusVolts = 0
            self.imagingFocusSteps = 0
            self.imagingFocusVolts = 0
            self.wavelength = 0
            self.gratingAngleVolts = 0
            self.lastMove = 0
            self.platescale = 0
            self.grating = None
    
    def updatePrefilter(self, name):
        old_setting = self.prefilter
        self.prefilter = name
        self.autosave()
        if not old_setting == name:
            self.log()
    
    
    def updateSpectralFilter(self, str):
        old_setting = self.spectralFilterSetting
        self.spectralFilterSetting=str
        self.autosave()
        if not old_setting == str:
            self.log()
    
    
    def updateImagingFilter(self, str):
        old_setting = self.imagingFilterSetting
        self.imagingFilterSetting=str
        self.autosave()
        if not old_setting == str:
            self.log()
    
        
    def updateSlitSteps(self, num):
        old_setting = self.slitSteps
        self.slitSteps = num
        self.autosave()
        if not old_setting == num:
            self.log()
    
        
    def updateSlitAngle(self, num):
        old_setting = self.slitAngle
        self.slitAngle = num
        self.autosave()
        if not old_setting == num:
            self.log()
    
    
    def updateMotorSteps(self, i, val):
        if i == 0:
            self.updateSpectralFocusSteps(val)
        elif i == 1:
            self.updateRotiserizerSteps(val)
        elif i == 2:
            self.updateImagingFocusSteps(val)
        elif i == 3:
            if val < 0:
                val = 0
            self.updateSlitSteps(val)

            
    def updateRotiserizerSteps(self, num):
        old_setting = self.rotiserizerSteps
        self.rotiserizerSteps = num
        self.autosave()
        if not old_setting == num:
            self.log()

            
    def updateRotiserizerAngle(self, num):
        old_setting = self.rotiserizerAngle
        self.rotiserizerAngle = num
        self.autosave()
        if not old_setting == num:
            self.log()

            
    def updateRotiserizerVolts(self, num):
        old_setting = self.rotiserizerVolts
        self.rotiserizerVolts = num
        self.autosave()
        if not old_setting == num:
            self.log()  
            
            
    def updateSpectralFocusSteps(self, num):
        old_setting = self.spectralFocusSteps
        self.spectralFocusSteps = num
        self.autosave()
        if not old_setting == num:
            self.log()
            
            
    def updateSpectralFocusVolts(self, num):
        old_setting = self.spectralFocusVolts
        self.spectralFocusVolts = num
        self.autosave()
        if not old_setting == num:
            self.log()
            
            
    def updateImagingFocusSteps(self, num):
        old_setting = self.imagingFocusSteps
        self.imagingFocusSteps = num
        self.autosave()
        if not old_setting == num:
            self.log()
            
            
    def updateImagingFocusVolts(self, num):
        old_setting = self.imagingFocusVolts
        self.imagingFocusVolts = num
        self.autosave()
        if not old_setting == num:
            self.log()
    
            
    def updateWavelength(self, num):
        old_setting = self.wavelength
        self.wavelength = num
        self.autosave()
        if not old_setting == num:
            self.log()
    
    
    def updateGratingVoltage(self, num):
        old_setting = self.gratingAngleVolts
        self.gratingAngleVolts = num
        self.autosave()
        if not old_setting == num:
            self.log()
    
        
    def updateLastMove(self, num):
        old_setting = self.lastMove
        self.lastMove = num
        self.autosave()
        if not old_setting == num:
            self.log()
        
        
    def updatePlatescale(self, num):
        old_setting = self.platescale
        self.platescale = num
        self.autosave()
        if not old_setting == num:
            self.log()
            
            
    def updateGrating(self, name):
        old_setting = self.grating
        self.grating = name
        self.autosave()
        if not old_setting == name:
            self.log()
    
        
    def clearLogs():
        if os.path.exists('logs'):
            shutil.rmtree('logs')
        
        
    def clearSaves():
        if os.path.exists('saves'):
            shutil.rmtree('saves')
        
        
    def autosave(self):
        # create or enter the saves folder for file creation
        if not os.path.exists('saves'):
            os.mkdir('saves')
        os.chdir('saves')
        # create or overwrite autosave file
        file = open('autosave.txt', 'w')
        # write settings into file
        file.write("Saved as of: \n%s\n\n"
                   "Aperture Prefilter:\n%s\n"
                   "Spectral Filter:\n%s\n"
                   "Imaging Filter:\n%s\n"
                   "Slit Width Steps:\n%d\n"
                   "Slit Viewer Angle:\n%d\n"
                   "Rotiserizer Steps:\n%d\n"
                   "Rotiserizer Phase Angle:\n%d\n"
                   "Rotiserizer Voltage:\n%d\n"
                   "Spectral Focus Steps:\n%d\n"
                   "Spectral Focus Voltage:\n%d\n"
                   "Imaging Focus Steps:\n%d\n"
                   "Imaging Focus Voltage:\n%d\n"
                   "Wavelength:\n%d\n"
                   "Grating Voltage:\n%d\n"
                   "Grating Last Move:\n%d\n"
                   "Platescale:\n%d\n"
                   "Grating:\n%s\n"
                   % (dt.datetime.now(),self.prefilter,self.spectralFilterSetting,
                      self.imagingFilterSetting,self.slitSteps,self.slitAngle,
                      self.rotiserizerSteps,self.rotiserizerAngle,self.rotiserizerVolts,
                      self.spectralFocusSteps,self.spectralFocusVolts,self.imagingFocusSteps,
                      self.imagingFocusVolts,self.wavelength,self.gratingAngleVolts,
                      self.lastMove,self.platescale,self.grating))
        # close file and exit saves directory
        file.close()
        os.chdir('..')
        
        
    def log(self):
        # create or enter the logs folder for file creation
        if not os.path.exists('logs'):
            os.mkdir('logs')
        os.chdir('logs')
        # create or overwrite autosave file
        file = open('%s.txt' % str(dt.datetime.now()).replace(':','_')[:-5], 
                                                                        'w')
        # write settings into file
        file.write("Saved as of: \n%s\n\n"
                   "Aperture Prefilter:\n%s\n"
                   "Spectral Filter:\n%s\n"
                   "Imaging Filter:\n%s\n"
                   "Slit Width Steps:\n%d\n"
                   "Slit Viewer Angle:\n%d\n"
                   "Rotiserizer Steps:\n%d\n"
                   "Rotiserizer Phase Angle:\n%d\n"
                   "Rotiserizer Voltage:\n%d\n"
                   "Spectral Focus Steps:\n%d\n"
                   "Spectral Focus Voltage:\n%d\n"
                   "Imaging Focus Steps:\n%d\n"
                   "Imaging Focus Voltage:\n%d\n"
                   "Wavelength:\n%d\n"
                   "Grating Voltage:\n%d\n"
                   "Grating Last Move:\n%d\n"
                   "Platescale:\n%d\n"
                   "Grating:\n%s\n"
                   % (dt.datetime.now(),self.prefilter,self.spectralFilterSetting,
                      self.imagingFilterSetting,self.slitSteps,self.slitAngle,
                      self.rotiserizerSteps,self.rotiserizerAngle,self.rotiserizerVolts,
                      self.spectralFocusSteps,self.spectralFocusVolts,self.imagingFocusSteps,
                      self.imagingFocusVolts,self.wavelength,self.gratingAngleVolts,
                      self.lastMove,self.platescale,self.grating))
        # close file and exit logs directory
        file.close()
        os.chdir('..')
        
        
    def save(self):
        # create or enter the saves folder for file creation
        if not os.path.exists('saves'):
            os.mkdir('saves')
        os.chdir('saves')
        # create save file
        file = open('%s.txt' % str(dt.datetime.now()).replace(':','_')[:-5], 
                                                                        'w')
        # write settings into file
        file.write("Saved as of: \n%s\n\n"
                   "Aperture Prefilter:\n%s\n"
                   "Spectral Filter:\n%s\n"
                   "Imaging Filter:\n%s\n"
                   "Slit Width Steps:\n%d\n"
                   "Slit Viewer Angle:\n%d\n"
                   "Rotiserizer Steps:\n%d\n"
                   "Rotiserizer Phase Angle:\n%d\n"
                   "Rotiserizer Voltage:\n%d\n"
                   "Spectral Focus Steps:\n%d\n"
                   "Spectral Focus Voltage:\n%d\n"
                   "Imaging Focus Steps:\n%d\n"
                   "Imaging Focus Voltage:\n%d\n"
                   "Wavelength:\n%d\n"
                   "Grating Voltage:\n%d\n"
                   "Grating Last Move:\n%d\n"
                   "Platescale:\n%d\n"
                   "Grating:\n%s\n"
                   % (dt.datetime.now(),self.prefilter,self.spectralFilterSetting,
                      self.imagingFilterSetting,self.slitSteps,self.slitAngle,
                      self.rotiserizerSteps,self.rotiserizerAngle,self.rotiserizerVolts,
                      self.spectralFocusSteps,self.spectralFocusVolts,self.imagingFocusSteps,
                      self.imagingFocusVolts,self.wavelength,self.gratingAngleVolts,
                      self.lastMove,self.platescale,self.grating))
        # close file and exit saves directory
        file.close()
        os.chdir('..')
        
        
    def readFile(str):
        # initialize array to be filled with values
        settings = []
        base_path = os.path.abspath(os.path.dirname(__file__))
        file = open(os.path.join(base_path, str))
        # parse the lines into an array
        lines = file.readlines()
        # extract filter wheel and angle data
        for i in range(17):
            if i < 3 or i > 15:
                settings.append(lines[4+2*i][:-1])
            else:
                settings.append(float(lines[4+2*i][:-1]))
        return settings