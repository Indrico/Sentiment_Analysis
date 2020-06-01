from django.shortcuts import render
from .tweepyAuth import tweepyAuth

#Convert List To Dictionary
def listToDict(lst):
    dictOfWords = { lst[i] for i in range(0, len(lst) ) }
    return dictOfWords

def index(request):
    #initialize Tweepy API
    # api = tweepy.API(auth)
    api = tweepyAuth()

    #Indonesia WOEID
    indonesia_woeid = 1048536
    public_tweets = api.trends_place(indonesia_woeid)

    #Untuk mengambil trending topic
    trending = []
    for tweet in public_tweets:
        for index in range(len(tweet["trends"])):
            trending.append(tweet["trends"][index]["name"])
    
    # print(trending) - For Debugging

    #Convert array to object so django can use it
    trend_name = listToDict(trending)

    return render(request, 'index.html', {'Trend_Name' : trend_name})