# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 17:53:45 2019
@author: Patrick Lierle

purpose:
"""

import tkinter as tk

class FilterEditor:

    global imgNames, specNames
    
    # creates dialogue and returns updated name arrays
    def openDialogue(imgOps, specOps, imgPos, specPos):
        # initialize the window
        window = tk.Tk()
        window.geometry("400x312+675+250")
        window.title("Edit Filters")
        window.wm_iconbitmap("images/ripsbufull.ico")
        
        # prepare section headers to be displayed
        imgHeader = tk.Label(window, text="Imaging Filter Wheel",
                    font=("times 10 bold"), relief="raised", padx=5, pady=5)
        specHeader = tk.Label(window, text="Spectral Filter Wheel", 
                    font=("times 10 bold"), relief="raised", padx=5, pady=5)
        
        # create a list of filter number labels
        filterNumberLabels = []
        
        # populate the list
        for i in range(5):
            filterNumberLabels.append(tk.Label(window, 
                                               text="Filter %d:" % (i+1)))
        
        # create two lists of entryboxes
        imagingEntries = []
        spectralEntries = []
        
        # populate the lists, make the current position green
        for i in range(5):
            if i+1 == imgPos:
                imagingEntries.append(tk.Entry(window, bg='green2'))
            else:
                imagingEntries.append(tk.Entry(window))
            
        for i in range(5):
            if i+1 == specPos:
                spectralEntries.append(tk.Entry(window, bg='green2'))
            else:
                spectralEntries.append(tk.Entry(window))
            
        # fill entryboxes with current settings
        for i in range(5):
            imagingEntries[i].insert(0,imgOps[i])
            
        for i in range(5):
            spectralEntries[i].insert(0,specOps[i])
            
        # reset arrays to be empty
        imgNames = []
        specNames = []
        
        def retrieveNames():
            for i in imagingEntries:
                imgNames.append(i.get())
            for i in spectralEntries:
                specNames.append(i.get())
            window.destroy()
            window.quit()
        
        # create apply button to save filter settings
        applyButton = tk.Button(window, text="apply", 
                                command=retrieveNames)
        
         # affix the headers to the window
        imgHeader.grid(row=1, column=2, padx=10, pady=10)
        specHeader.grid(row=1, column=3, padx=10, pady=10)
        
        # affix the labels to the window
        for i in range(5):
            filterNumberLabels[i].grid(row=i+2, column=1, padx=10, pady=10)
        
        # affix the entryboxes to the window
        for i in range(5):
            imagingEntries[i].grid(row=i+2, column=2, padx=10, pady=10)
            
        for i in range(5):
            spectralEntries[i].grid(row=i+2, column=3, padx=10, pady=10)
            
        # affix apply button to the window and make it gray
        applyButton.grid(row=7, column=3, padx=10, pady=10)
        applyButton.configure(bg='gray83')
        
        # display everything onscreen
        window.focus_force()
        window.mainloop()
        
        return imgNames,specNames
        

openDialogue = FilterEditor.openDialogue