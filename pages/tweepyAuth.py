import tweepy
def tweepyAuth():
    auth = tweepy.OAuthHandler("sGVoIBh4jNQXOKyeQfoIhFf8x", "VF4DPLQ4ltkUnisGEYTGZSyTcnmYOqSRWnbDcqEKigKUWFGMV3")
    auth.set_access_token("299945902-W7SGzGPNK4H1Qy0ggnAdvVYULzd5m4UrHMoIIV7U", "3q3AghIcAsshpoTvL5xSvIfmMIozoZfyDrHm1yoZafwqr")
    api = tweepy.API(auth)
    return api