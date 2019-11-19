# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:39:17 2019

"""

from tkinter import *
import tkinter.messagebox
import tkinter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
from newsapi import NewsApiClient
import spotipy.util as util
import nltk
nltk.download('brown')
nltk.download('punkt')
from nltk.corpus import brown
import datetime

# This is a fast and simple noun phrase extractor (based on NLTK)
# Feel free to use it, just keep a link back to this post
# http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
# Create by Shlomi Babluki
# May, 2013


# This is our fast Part of Speech tagger
#############################################################################
brown_train = brown.tagged_sents(categories='news')
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*', 'NN')
     ])
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)
#############################################################################


# This is our semi-CFG; Extend it according to your own needs
#############################################################################
cfg = {}
cfg["NNP+NNP"] = "NNP"
cfg["NN+NN"] = "NNI"
cfg["NNI+NN"] = "NNI"
cfg["JJ+JJ"] = "JJ"
cfg["JJ+NN"] = "NNI"


#############################################################################


class NPExtractor(object):
    def __init__(self, sentence):
        self.sentence = sentence

    # Split the sentence into singlw words/tokens
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens

    # Normalize brown corpus' tags ("NN", "NN-PL", "NNS" > "NN")
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    # Extract the main topics from the sentence
    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))

        merge = True
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        matches = []
        for t in tags:
            #if t[1] == "NNP" or t[1] == "NNI" :
            if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches


news = NewsApiClient(api_key='fe1bbf9f375842fcbae8cf90741f7fa5')
#client_credentials_manager = SpotifyClientCredentials(client_id="da5a1895b29f46b8aab5d2007dba9b9c", client_secret="4c5154e4ae7c4223ab08fee6540a2600")

login = tkinter.Tk()
login.geometry('640x480')
login.configure(bg = "#191414")
tkinter.Label(login, text="Spotify Username", bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 18)).place(x = 75, y = 75, width = 490)
tkinter.Label(login, text="Login to spotify, goto account overview for Username", bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12)).place(x = 75, y = 175, width = 490)

usernameBox = tkinter.Entry(login)
usernameBox.place(x = 75, y = 150, width = 490)
tkinter.Button(login, 
          text='OK',
           bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 18),
          command=login.quit).place(x = 75, y = 300, width = 490)
login.mainloop()
username = usernameBox.get()
login.destroy()
token = util.prompt_for_user_token(username, scope="playlist-modify-public", client_id="da5a1895b29f46b8aab5d2007dba9b9c", client_secret="4c5154e4ae7c4223ab08fee6540a2600", redirect_uri="http://localhost:8888/callback")
spotify = spotipy.Spotify(auth=token)

def getNews(List, Location):
    headlines= []
    if len(List) == 0: 
        if "global" in Location:       
            headlines.append(news.get_top_headlines(language='en'))
        if "uk" in Location:       
            headlines.append(news.get_top_headlines(country='gb'))
    if len(List) > 0:       
        if "global" in Location:   
            for c in List:    
                headlines.append(news.get_top_headlines(language='en',category=c))
        if "uk" in Location:       
            for c in List:    
                headlines.append(news.get_top_headlines(country='gb', language='en', category=c))
    return headlines

def getNewsCallBack(List, Location):
    
    now = str(datetime.datetime.now())
    now = now[0:len(now)-7]
    
    headlines = getNews(List, Location)
    '''
    headlines= []
    if len(List) == 0: 
        if "global" in Location:       
            headlines.append(news.get_top_headlines(language='en'))
        if "uk" in Location:       
            headlines.append(news.get_top_headlines(country='gb'))
    if len(List) > 0:       
        if "global" in Location:   
            for c in List:    
                headlines.append(news.get_top_headlines(language='en',category=c))
        if "uk" in Location:       
            for c in List:    
                headlines.append(news.get_top_headlines(country='gb', language='en', category=c))
    '''
    for h in headlines:   
        results=[]
    for h in headlines:
        for i in range(5):
            sentence = h['articles'][i]['title']
            np_extractor = NPExtractor(sentence)
            result = np_extractor.extract()
            for r in result:
                results.append(r)
        track= results
        track_json = []
        for t in track:
            track_json.append(spotify.search(q='track:' + t, type='track'))
        
        track_id = []
        
        for i in range(len(track_json)):    
            if not(len(track_json[i]['tracks']['items']) == 0):
                track_id.append(track_json[i]['tracks']['items'][0]['id'])
        #tkinter.Label(window, text = headlines).pack()
    test = spotify.user_playlist_create(username, 'News' + ' ' + str(now), public=True)
    spotify.user_playlist_add_tracks(username, test['id'], track_id)
    webbrowser.open('https://open.spotify.com/playlist/'+test['id'])
  

def returnHeadlinesCallBack(List, Location):
   titles = ''
   for h in getNews(List, Location):
       for i in range(5):
           sentence = h['articles'][i]['title']
           titles += sentence + '\n'
           np_extractor = NPExtractor(sentence)
           result = np_extractor.extract()
           for j in result:
               titles += j + '; '
           titles += '\n\n'
   tkinter.messagebox.showinfo("Headlines", titles)

def sportsFilterCallBack(List):
   if "sports" in List:
      List.remove("sports")
   else:
      List.append("sports")

def businessFilterCallBack(List):
   if "business" in List:
      List.remove("business")
   else:
      List.append("business")

def techFilterCallBack(List):
   if "technology" in List:
      List.remove("technology")
   else:
      List.append("technology")

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
      sportsFilter = tkinter.Checkbutton(window, text = "Sports", command = lambda: sportsFilterCallBack(filtersList), bg = "#191414", fg = "#1DB954", font=("Proxima Nova", 12))
      sportsFilter.place(x = 180, y = 115)
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

      returnHeadlines = tkinter.Button(window, text = "Display Results", command = lambda: returnHeadlinesCallBack(filtersList, Location), bg = "#1DB954", fg= "#191414", font=("Proxima Nova", 12))
      returnHeadlines.place(bordermode=OUTSIDE, height = 25, width = 150,  x = 245, y = 440)

      window.mainloop()
GUI()