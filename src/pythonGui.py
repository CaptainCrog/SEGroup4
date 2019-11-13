from tkinter import *
import tkinter.messagebox
import tkinter

def getNewsCallBack(List, Location):
   print (List)
   print (Location)

def returnHeadlinesCallBack():
   tkinter.messagebox.showinfo("Headlines", "<Healines here>")

def politicsFilterCallBack(List):
   if "politics" in List:
      List.remove("politics")
   else:
      List.append("politics")

def businessFilterCallBack(List):
   if "business" in List:
      List.remove("business")
   else:
      List.append("business")

def techFilterCallBack(List):
   if "tech" in List:
      List.remove("tech")
   else:
      List.append("tech")

def scienceFilterCallBack(List):
   if "science" in List:
      List.remove("science")
   else:
      List.append("science")

def healthFilterCallBack(List):
   if "health" in List:
      List.remove("health")
   else:
      List.append("health")
   
def entertainmentFilterCallBack(List):
   if "entertainment" in List:
      List.remove("entertainment")
   else:
      List.append("entertainment")

def globalFilterCallBack(Location):
   if "uk" in Location:
      Location.remove("uk")
      Location.append("global") 
   
def ukFilterCallBack(Location):
   if "global" in Location:
      Location.remove("global")
      Location.append("uk")    

class GUI():
   def __init__(self):
      window = tkinter.Tk()
      window.geometry('640x480')
      window.configure(bg = "#191414")
      window.title("News based Spotify Suggestions")

      canvas = Canvas(window, width = 50, height = 50, bg = "#191414", highlightthickness=0, relief='ridge')      
      canvas.place(x=10,y=10)
      img = PhotoImage(file = "Spotify_Logo.png")
      canvas.create_image(0,0, anchor=NW, image=img)
      
      filtersList = [ ]
      Location = ["global"]

      filterHeader = tkinter.Label(window, text = "News Filters", bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 18))
      filterHeader.place(x = 75, y = 75, width = 490)
      politicsFilter = tkinter.Checkbutton(window, text = "Politics", command = lambda: politicsFilterCallBack(filtersList), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      politicsFilter.place(x = 180, y = 115)
      businessFilter = tkinter.Checkbutton(window, text = "Business", command = lambda: businessFilterCallBack(filtersList), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      businessFilter.place(x = 180, y = 145)
      techFilter = tkinter.Checkbutton(window, text = "Technology", command = lambda: techFilterCallBack(filtersList), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      techFilter.place(x = 180, y = 175)
      scienceFilter = tkinter.Checkbutton(window, text = "Science", command = lambda: scienceFilterCallBack(filtersList), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      scienceFilter.place(x = 370, y = 115)
      allFilters = tkinter.Checkbutton(window, text = "Health", command = lambda: healthFilterCallBack(filtersList), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      allFilters.place(x = 370, y = 145)
      entertainmentFilter = tkinter.Checkbutton(window, text = "Entertainment", command = lambda: entertainmentFilterCallBack(filtersList), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      entertainmentFilter.place(x = 370, y = 175)

      filterHeader = tkinter.Label(window, text = "News Location", bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 18))
      filterHeader.place(x = 75, y = 240, width = 490)
      globalFilter = tkinter.Checkbutton(window, text = "Global", command = lambda: globalFilterCallBack(Location), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      globalFilter.place(x = 180, y = 280)
      ukFilter = tkinter.Checkbutton(window, text = "UK", command = lambda: ukFilterCallBack(Location), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      ukFilter.place(x = 370, y = 280)
      
      getNews = tkinter.Button(window, text ="Get Playlist", command = lambda: getNewsCallBack(filtersList, Location), bg = "#1DB954", fg= "#191414", font=("Proxima Nova", 24))
      getNews.place(bordermode=OUTSIDE, height = 75, width = 200,  x = 220, y = 355)

      returnHeadlines = tkinter.Button(window, text = "Display Results", command = lambda: returnHeadlinesCallBack(), bg = "#1DB954", fg= "#191414", font=("Proxima Nova", 12))
      returnHeadlines.place(bordermode=OUTSIDE, height = 25, width = 150,  x = 245, y = 440)

      window.mainloop()
GUI()
