from django.shortcuts import render, HttpResponse
import tweepy
from datetime import datetime, timezone

def tweepyAuth():
    auth = tweepy.OAuthHandler("sGVoIBh4jNQXOKyeQfoIhFf8x", "VF4DPLQ4ltkUnisGEYTGZSyTcnmYOqSRWnbDcqEKigKUWFGMV3")
    auth.set_access_token("299945902-W7SGzGPNK4H1Qy0ggnAdvVYULzd5m4UrHMoIIV7U", "3q3AghIcAsshpoTvL5xSvIfmMIozoZfyDrHm1yoZafwqr")
    api = tweepy.API(auth)
    return api

def parseTweet(lst):
    new_list = []
    for item in lst:
        temp = {}
        temp["text"] = item['text']
        temp["id"] = item['id']
        # Mengubah format penanggal Twitter Misal "Thu Dec 26 16:33:13 +0000 2019" menjadi penanggalan Indonesia dengan local timezone
        temp["created_at"] = datetime.strptime(item["created_at"], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%d-%m-%Y %H:%M:%S')
        temp["username"] = item['user']["screen_name"]
        temp["picture_url"] = item['user']["profile_image_url"]
        new_list.append(temp)  
    return new_list

def results(request):
    tweet = int(request.POST["tweet"])
    keyword = request.POST["keyword"]

    api = tweepyAuth() #Authentifikasi terlebih dahulu
    result = [status._json for status in tweepy.Cursor(api.search, q=keyword + '-filter:retweets', lang="id").items(tweet)] #Bentuk hasilnya list of dictionary
    hasil = parseTweet(result) #gunakan element yang diperlukan saja

    return render(request, 'hasil.html', {'tweet' : tweet, 'keyword' : keyword, 'hasil': hasil})