"""
Author: Enrique Rodriguez
Date: 11/19/2018
Purpose: To create a music player, from a selected file, with prev, next, play, and stop functionality

Notes:
    os is for accessing the file directory
    pygame is for music playing
    tkinter is to make the basic GUI of the app
    mutagen handles audio metadata
"""
import os
import pygame
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import ttk     #Binding to newer themed widgets
from mutagen.id3 import ID3

#Establish main window
root = Tk()
root.title("UGFC's Network Project")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#List of songs and reference index
listofsongs = []    #Song file names
realnames = []      #Song names
index = 0           #Index

currentSong = StringVar()
songLabel = Label(root, textvariable = currentSong, width = 50)

#Create a file directory search
def directorychooser():

    directory = askdirectory()
    os.chdir(directory)

    #Scan all .mp3 files in chose directory
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio = ID3(realdir)
            realnames.append(audio["TIT2"].text[0])

            listofsongs.append(files)

    pygame.mixer.init()                         #Initialize a mixer
    pygame.mixer.music.load(listofsongs[index]) #Load a song into the mixer

directorychooser()

#Play the previous song in the list
def previousSong(event):
    global index
    if(index > 0):
        index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updateLabel()
#Play the next song in the list
def nextSong(event):
    global index
    if(index < len(listofsongs) - 1):
        index += 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updateLabel()
#Stop the song on the list
def stopSong(event):
    pygame.mixer.music.stop()
    currentSong.set("")
#Play the song on the list
def playSong(event):
    pygame.mixer.music.play()
    updateLabel()

#Update Now Playing Label
def updateLabel():
    global index
    currentSong.set(realnames[index])

#Create a GUI
title = ttk.Label(mainframe, text = 'Now Playing:')
title.grid(column = 2, row = 0, sticky = '')

nowPlaying = ttk.Label(mainframe, textvariable = currentSong)
nowPlaying.grid(column = 2, row = 1, sticky = '')

listbox = Listbox(mainframe, width = 40, )
listbox.grid(column = 2, row = 2, sticky = '')

realnames.reverse()
for items in realnames:
    listbox.insert(0,items)
realnames.reverse()

#Buttons
playButton = ttk.Button(mainframe, text = "Play")
playButton.grid(column = 2, row = 3, sticky = '')
playButton.bind("<Button-1>", playSong)

stopButton = ttk.Button(mainframe, text = "Stop")
stopButton.grid(column = 2, row = 4, sticky = '')
stopButton.bind("<Button-1>", stopSong)

previousButton = ttk.Button(mainframe,text = "Prev.")
previousButton.grid(column = 2, row = 3, sticky = (W))
previousButton.bind("<Button-1>", previousSong)

nextButton = ttk.Button(mainframe,text = "Next")
nextButton.grid(column = 2, row = 3, sticky = (E))
nextButton.bind("<Button-1>", nextSong)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()
