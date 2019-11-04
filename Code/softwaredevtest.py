# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tkinter
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
from newsapi import NewsApiClient

import nltk
from nltk.corpus import brown

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
            if t[1] == "NNP" or t[1] == "NNI":
                # if t[1] == "NNP" or t[1] == "NNI" or t[1] == "NN":
                matches.append(t[0])
        return matches


# Main method, just run "python np_extractor.py"
#def main():
#    sentence = "Earth is dangerous."
#    np_extractor = NPExtractor(sentence)
#    result = np_extractor.extract()
#    print("This sentence is about: %s" % ", ".join(result))


#if __name__ == '__main__':
#    main()

news = NewsApiClient(api_key='fe1bbf9f375842fcbae8cf90741f7fa5')
headlines = news.get_top_headlines(sources='bbc-news')
client_credentials_manager = SpotifyClientCredentials(client_id="da5a1895b29f46b8aab5d2007dba9b9c", client_secret="4c5154e4ae7c4223ab08fee6540a2600")

spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
def play() :
    sentence = headlines['articles'][1]['title']
    print(sentence)
    np_extractor = NPExtractor(sentence)
    result = np_extractor.extract()
    print("This sentence is about: %s" % ", ".join(result))
    track= result[0]
    track_id = spotify.search(q='track:' + track, type='track')    
    tkinter.Label(window, text = headlines).pack()
    webbrowser.open(track_id['tracks']['items'][0]['external_urls']['spotify'])
    #print(headlines['articles'][0]['title'])

window = tkinter.Tk()
# to rename the title of the window
window.title("GUI")
window.geometry("600x50")
top = tkinter.Frame(window).pack()
bottom = tkinter.Frame(window).pack(side = "bottom")
# pack is used to show the object in the window
label = tkinter.Label(window, text = "Play me the news").pack()
btn1 = tkinter.Button(top, text = "Play", fg = "red", command = play).pack()
window.mainloop()