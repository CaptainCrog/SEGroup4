#!/usr/bin/python

import tkinter
import tkinter.messagebox

top = tkinter.Tk()
top.geometry('900x480')
top.title("Spotify New Application")
def helloCallBack():
   tkinter.messagebox.showinfo( "Hello Python", "Hello World")

B = tkinter.Button(top, text ="Get News", command = helloCallBack)
B.pack(padx = 50, pady = 50)
# Code to add widgets will go here...
top.mainloop()