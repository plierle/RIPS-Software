# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:05:53 2019
@author: Patrick Lierle

purpose: to establish a serial connection with the imaging filter wheel and
         provide functions to communicate with the GUI panel
"""
import serial
import serial.tools.list_ports

class FilterWheel:
        
    # assumes standard baud rate of 9600 bps
    BAUD_RATE = 9600
    
    # allows FilterWheel objects to be created by specifying a serial number
    def __init__(self, serialnum):
        self.serialnum = serialnum
        self.port = self.getPort()
    
    # performs a sensor calibrations and stores the results in flash
    def calibrate(self):
        self.openSerial()
        cmd = 'R6'
        try:
            self.ser.write(cmd.encode('utf-8'))
        except:
            return False
        self.ser.close()
        return True
    
    # finds the COM port associated with the serial number of the FilterWheel
    # object on which it is called. returns None for any error
    def getPort(self):
        for n in serial.tools.list_ports.comports():
            print(n.device)
            try:
                self.ser = serial.Serial(n.device, self.BAUD_RATE, timeout=0.05)
                cmd = 'I3'
                self.ser.write(cmd.encode('utf-8'))
                response = self.ser.read(7)[4:]
                self.closeSerial()
                retrieved_serial_num = response.decode('utf-8')
                if retrieved_serial_num == self.serialnum:
                    print(retrieved_serial_num,self.serialnum,n.device)
                    return n.device
            except:
                return None
            
    # establishes a serial connection, asks for positions, and closes serial
    def getPosition(self):
        self.openSerial()
        cmd = 'I2'
        self.ser.write(cmd.encode('utf-8'))
        response = self.ser.read(2)
        self.closeSerial()
        return int(response.decode('utf-8')[1:])
        
    # sets the filter wheel position to a user entered value
    def setPosition(self, pos):
        # ensures value is within range
        if pos < 1 or pos > 5:
            return False
        self.openSerial()
        cmd = 'G' + str(pos)
        try:
            self.ser.write(cmd.encode('utf-8'))
        except:
            return False
        self.ser.close()
        return True
            
    # returns the serial number of the filter wheel
    def getSerialNum(self):
        return self.serialnum
    
    # attempts to open a serial connection, returns boolean for success
    def openSerial(self):
        try:
            self.ser = serial.Serial(self.port, self.BAUD_RATE)
            return True
        except:
            return False
        
    # tries to close the serial connection and returns boolean
    def closeSerial(self):
        try:
            self.ser.close()
            return True
        except:
            return False
        