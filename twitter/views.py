from django.shortcuts import render, HttpResponse
import tweepy
import re
import pytz
from datetime import datetime, timezone
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import pickle

def tweepyAuth():
    auth = tweepy.OAuthHandler("sGVoIBh4jNQXOKyeQfoIhFf8x", "VF4DPLQ4ltkUnisGEYTGZSyTcnmYOqSRWnbDcqEKigKUWFGMV3")
    auth.set_access_token("299945902-W7SGzGPNK4H1Qy0ggnAdvVYULzd5m4UrHMoIIV7U", "3q3AghIcAsshpoTvL5xSvIfmMIozoZfyDrHm1yoZafwqr")
    api = tweepy.API(auth)
    return api

def removeURL(text):
    no_url = re.sub(r'http\S+', '', text)
    return no_url

def noise_removal(text):
    no_noise = re.sub("(\\W|\\d)"," ",text)
    return no_noise

def remove_stopword(text):
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    stop = stopword.remove(text)
    return stop

def remove_whitespaces(text):
    no_whitespaces = re.sub(r'\s+', ' ', text)
    return no_whitespaces

def cleaningText(lst):
    new_list = []
    for item in lst:
        temp = {}
        temp["text"] = item['text']
        temp["text"] = remove_whitespaces(remove_stopword(noise_removal(removeURL(item['text'].lower()))))
        new_list.append(temp)  
    return new_list

def listToString(s):  
    # initialize an empty string 
    str1 = " " 
    # return string   
    return (str1.join(s)) 

def getSentiment(lst):
    vectorizer = pickle.load(open('vectorizer.sav', 'rb'))
    classifier_linear = pickle.load(open('classifier.sav', 'rb'))
    
    #Use Indonesia Timezone (GMT+7)
    indonesia = pytz.timezone('Asia/Jakarta')

    new_list = []
    for item in lst:
        temp = {}
        temp["text"] = item['text']
        temp["id"] = item['id']
        # Mengubah format penanggal Twitter Misal "Thu Dec 26 16:33:13 +0000 2019" menjadi penanggalan Indonesia dengan local timezone
        temp["created_at"] = datetime.strptime(item["created_at"], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=timezone.utc).astimezone(indonesia).strftime('%d-%m-%Y %H:%M:%S')
        temp["username"] = item['user']["screen_name"]
        temp["picture_url"] = item['user']["profile_image_url"]
        clean_tweet = remove_whitespaces(remove_stopword(noise_removal(removeURL(item['text'].lower())))) #Cleaned Text
        temp["clean_tweet"] = clean_tweet
        tweet_vector = vectorizer.transform([clean_tweet]) # Vectorizing
        sentiment = classifier_linear.predict(tweet_vector)
        if (sentiment >= 0.5):
            temp["sentimen"] = "positif"
        elif (sentiment <= 0.5 and sentiment >= -0.5):
            temp["sentimen"] = "netral"
        else:
            temp["sentimen"] = "negatif"
        new_list.append(temp)
    return new_list

def results(request):
    tweet = int(request.POST["tweet"])
    keyword = request.POST["keyword"]

    api = tweepyAuth() #Authentifikasi terlebih dahulu
    result = [status._json for status in tweepy.Cursor(api.search, q=keyword + '-filter:retweets', lang="id").items(tweet)] #Bentuk hasilnya list of dictionary
    hasil = getSentiment(result) #gunakan element yang diperlukan saja
    positif = 0
    netral = 0
    negatif = 0
    counter = 0
    for item in hasil:
        counter += 1
        if (item["sentimen"] == "positif"):
            positif += 1
        elif (item["sentimen"] == "netral"):
            netral += 1
        else:
            negatif += 1
    if counter > 0:
        PersenPositif = round(positif * 100 / counter, 2)
        PersenNetral = round(netral * 100 / counter, 2)
        PersenNegatif = round(negatif * 100 / counter, 2)
    else:
        PersenPositif = 0
        PersenNegatif = 0
        PersenNetral = 0

    return render(request, 'hasil.html', {'tweet' : tweet, 'keyword' : keyword, 'hasil': hasil, 'positif': positif, 
                                          'negatif': negatif, 'netral': netral, 'PersenPositif': PersenPositif, 'PersenNetral': PersenNetral,
                                          'PersenNegatif': PersenNegatif, 'counter': counter})