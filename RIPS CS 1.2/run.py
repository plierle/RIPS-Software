# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:00:23 2019
@author: Patrick Lierle

Purpose: to provide a single file that runs all aspects of the program by calling
upon other classes
"""
import MainWindow, ConnectionWindow

class run:
    # show startup screens and generate connections array
    # 0: imgFW, 1: specFW, 2: motor array, 3: grating, 4: wasQuit variable
    connections = ConnectionWindow.run()
    # if the connection window wasn't quit, open main window
    if not connections[4]:
        MainWindow.run(connections)