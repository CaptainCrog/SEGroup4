from newsapi import NewsApiClient
import json

newsapi = NewsApiClient(api_key='e53a6a804d6b43fd9a407428e2de12da')

top_headlines = newsapi.get_top_headlines()

for i in range(5):
  print(top_headlines['articles'][i]['title'])