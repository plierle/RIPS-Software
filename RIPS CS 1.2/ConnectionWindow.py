# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 19:52:47 2019
@author: Patrick Lierle

Purpose: provide a startup window and splash that informs user of connected and
disconnected devices as well as their ports, and insures all critical devices 
are connected before proceeding
"""

import tkinter as tk
from tkinter import messagebox
import FilterWheel as fw
import VoltageTrackedMotor as voltageTrackedMotor
import Motor as motor
import Sensor as sensor

class ConnectionWindow:
    
    global IMG_FW_SERIAL_NUM, SPEC_FW_SERIAL_NUM, wasQuit
    IMG_FW_SERIAL_NUM = '295'
    SPEC_FW_SERIAL_NUM = '293'
    wasQuit = True
    
    
    def connectImagingFilterWheel():
        global imagingFW
        imagingFW = fw.FilterWheel(IMG_FW_SERIAL_NUM)
        if not imagingFW.getPort() == None:
            return True
        else: 
            imagingFW = None
            return False
        
        
    def connectSpectralFilterWheel():
        global spectralFW
        spectralFW = fw.FilterWheel(SPEC_FW_SERIAL_NUM)
        if not spectralFW.getPort() == None:
            return True
        else: 
            spectralFW = None
            return False
        
    
    def isFullyConnected():
        if imagingFW == None or spectralFW == None:
            return False
        for i in range(5):
            if not i==1 and not motors[i].isConnected():
                return False
        return True
    
        
    def connectMotor(i):
        if i == 0:
            motors.append(voltageTrackedMotor.VoltageTrackedMotor(2,428122,8200,
                          voltsensor=(527235,2), min=2.3, max=4.95))
            motors[0].name = "Spectral Focus Adjustment Motor"
        elif i == 1:
            ## CHANGE VOLTSENSOR TO PORT 3 ONCE INSTALLED, PORT 2 PLACEHOLDER
            motors.append(voltageTrackedMotor.VoltageTrackedMotor(0,522523,8200,
                          voltsensor=(527235,3), min=0.05, max=4.95))
            motors[1].name = "Rotiserizer Motor"
        elif i == 2:
            motors.append(voltageTrackedMotor.VoltageTrackedMotor(3,428122,8200,
                          voltsensor=(527235,1), min=1, max=4))
            motors[2].name = "Imaging Focus Adjustment Motor"
        elif i == 3:
            motors.append(motor.Motor(0, 428122, 0, min=0, max=28000))
            motors[3].name = "Slit Width Adjustment Motor"
        elif i == 4:
            motors.append(voltageTrackedMotor.VoltageTrackedMotor(1,428122,42776,
                          voltsensor=(527235,0), min=0.0392, max=4.1026))
            motors[4].name = "Grating Angle Adjustment Motor"
        return motors[i].isConnected()           
       
        
    def quitWindow(window):
        window.destroy()
        window.quit()
        
        
    def closeWindow(window):
        if ConnectionWindow.isFullyConnected():
            window.destroy()
            window.quit()
            global wasQuit
            wasQuit = False
        else:
            messagebox.showerror(title="Connection Failed", message=
                                 "All devices excluding the Rotiserizer must be"
                                 "connected to continue")
            
        
    def rescan(window):
        window.destroy()
        window.quit()
        ConnectionWindow.build()
    
    
    def build():
        # initialize motors list
        global motors
        motors = []
        
        # initialize window
        window = tk.Tk()
        window.geometry('350x350+700+250')
        window.title("External Device Connections")
        window.wm_iconbitmap("images/ripsbufull.ico")
        
        # create splash
        splash = tk.Toplevel()
        splash.geometry('400x420+675+250')
        splash.title("Detecting Devices...")
        splash.wm_iconbitmap("images/ripsbufull.ico")
        title = tk.Label(splash, text="Rapid Imaging Planetary "
                         "\nSpectrograph (RIPS) Controller", font = 'arial 15 bold')
        title.pack()
        img = tk.PhotoImage(file='images/rips.gif')
        imgLabel = tk.Label(splash, image=img)
        imgLabel.pack()
        copyrightLabel = tk.Label(splash, text="\u00A9 2019 "
                                  "Boston University Center for Space Physics")
        copyrightLabel.pack()
        splash.lift()
        splash.focus_force()
        splash.update()
        
        
        # create header
        header = tk.Label(window, text="External Devices:",         
                          font=("arial 10 bold"), relief="raised", padx=5, pady=5, bg='gray90')
        
        # initialize textbox with connection details
        text = tk.Text(window, height=31, width=41, bg='gray83')
        
        # add connection details in textbox
        text.insert(tk.END, "Imaging Filter Wheel . . . . \n"    
                                "    Serial: %s\n    Port: \n\n"
                                % IMG_FW_SERIAL_NUM)
        text.insert(tk.END, "Spectral Filter Wheel. . . . \n"    
                                "    Serial: %s\n    Port: \n\n"
                                % SPEC_FW_SERIAL_NUM)
        text.insert(tk.END, "Slit Width Motor . . . . . . \n"    
                                "    CC Serial: \n    Channel: \n\n")
        text.insert(tk.END, "Rotiserizer Motor. . . . . . \n"    
                                "    CC Serial: \n    Channel: \n\n")
        text.insert(tk.END, "Spectral Focus Motor . . . . \n"    
                                "    CC Serial: \n    Channel: \n\n")
        text.insert(tk.END, "Imaging Focus Motor. . . . . \n"    
                                "    CC Serial: \n    Channel: \n\n")
        text.insert(tk.END, "Grating Angle Motor. . . . . \n"    
                                "    CC Serial: \n    Channel: \n\n")
        text.insert(tk.END, "Grating. . . . . . . . . . . \n"    
                                "    Flavor: \n")
        
        # define a tag to make text green and one to make it bold
        text.tag_configure("green", foreground="green")
        text.tag_configure("red", foreground="red")
        text.tag_configure("bold", font="courier 10 bold")
        
        # apply bold tag to device names
        text.tag_add("bold", '1.0', '1.20')
        text.tag_add("bold", '5.0', '5.20')
        text.tag_add("bold", '9.0', '9.20')
        text.tag_add("bold", '13.0', '13.20')
        text.tag_add("bold", '17.0', '17.20')
        text.tag_add("bold", '21.0', '21.20')
        text.tag_add("bold", '25.0', '25.20')
        text.tag_add("bold", '29.0', '29.20')
        
        # check if imagingFW is connected and display connection info
        if ConnectionWindow.connectImagingFilterWheel():
            text.insert('1.29', ". Connected")
            text.tag_add("green", '1.31', '1.40')
            text.insert('3.11', imagingFW.getPort())
        else:
            text.insert('1.29','Disconnected')
            text.tag_add("red", '1.29', '1.41')
            text.insert('3.11', "None")
            
        # check if spectralFW is connected and display connection info
        if ConnectionWindow.connectSpectralFilterWheel():
            text.insert('5.29', ". Connected")
            text.tag_add("green", '5.31', '5.40')
            text.insert('7.11', spectralFW.getPort())
        else:
            text.insert('5.29','Disconnected')
            text.tag_add("red", '5.29', '5.41')
            text.insert('7.11', "None")
        
        # check if motors is connected and display connection info
        for i in range(5):
            lineNum = str(9+4*i)
            lineBelow = str(10+4*i)
            lineTwoBelow = str(11+4*i)
            if ConnectionWindow.connectMotor(i):
                text.insert(lineNum+'.29', ". Connected")
                text.tag_add("green", lineNum+'.31', lineNum+'.40')
                text.insert(lineBelow+'.16', motors[i].getCCSerialNum())
                text.insert(lineTwoBelow+'.13', motors[i].getChannel())
            else:
                text.insert(lineNum+'.29','Disconnected')
                text.tag_add("red", lineNum+'.29', lineNum+'.41')
                text.insert(lineBelow+'.16', "None")
                text.insert(lineTwoBelow+'.13', "None")
                
        # check if grating is installed and display info
        global grating
        if not motors[4].getVoltagePosition() == 0.0:
            text.insert('29.29', ". Connected")
            text.tag_add("green", '29.31', '29.40')
            identifier = sensor.Sensor(527235,0)
            if identifier.getState():
                text.insert('30.16','Echelle')
                grating = 'Echelle'
            else:
                text.insert('30.16','First Order')
                grating = 'First Order'
        else:
            text.insert('29.29','Disconnected')
            text.tag_add("red", '29.29', '29.41')
            text.insert('30.16','None')
                
        # revent the user from editing the text
        text.config(state='disabled')
        
        # create frame for buttons on bottom of textbox
        buttons = tk.Frame(window)
        buttons.grid(row=3, column=1)
        
        # create three bottom buttons for quit, continue, and rescan
        quitButton = tk.Button(buttons, text="quit", 
                        command=lambda: ConnectionWindow.quitWindow(window))
        continueButton = tk.Button(buttons, text="continue", 
                        command=lambda: ConnectionWindow.closeWindow(window))
        rescanButton = tk.Button(buttons, text="rescan", 
                        command=lambda: ConnectionWindow.rescan(window))
        
        # affix widgets to window
        header.grid(row=1, column=1, padx=10, pady=10)
        text.grid(row=2, column = 1, padx=10, pady=10)
        
        quitButton.grid(row=1, column=1, padx=20)
        continueButton.grid(row=1, column=2, padx=20)
        rescanButton.grid(row=1, column=3, padx=20)
        
        # color buttons gray
        quitButton.configure(bg='gray83')
        continueButton.configure(bg='gray83')
        rescanButton.configure(bg='gray83')
        
        # close splash and open connection panel
        splash.destroy()
        window.geometry('350x610+675+250')
        window.lift()
        window.focus_force()
        window.mainloop()
    
    
    def run():
        ConnectionWindow.build()
        return (imagingFW, spectralFW, motors, grating, wasQuit)
        
        
run = ConnectionWindow.run