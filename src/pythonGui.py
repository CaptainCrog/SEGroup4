from tkinter import *
import tkinter.messagebox
import tkinter

top = tkinter.Tk()
top.geometry('480x350')
top.configure(bg = "#191414")
top.title("News based Spotify Suggestions")

def helloCallBack():
   tkinter.messagebox.showinfo("Hello", "Hello 2: Electric Boogaloo")

def checkBoxCallBack():
   print ("Checkbox checked")
   #adds checkbox option to query?


#canvas = Canvas(top, width = 300, height = 300)      
#canvas.pack() 
#img = PhotoImage(file = "Spotify_Logo.ppm")
#canvas.create_image(50, 50, image = img)
   
B2 = tkinter.Checkbutton(top, text = "Politics", command = checkBoxCallBack, bg = "#1DB954")
B2.place(x = 50, y = 50)

B = tkinter.Button(top, text ="Get News", command = helloCallBack, bg = "#1DB954")
B.place(bordermode=OUTSIDE, height = 50, width = 100,  x = 190, y = 250)
# Code to add widgets will go here...
top.mainloop()
