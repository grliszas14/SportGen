import pandas as pd

tweets = pd.read_csv("../dataset/tweets.csv")
print(tweets.head())
tweets = tweets.drop(
    columns=["ID", "lang", "Date", "Source", "len", "Likes", "RTs", "Hashtags", "UserMentionNames", "UserMentionID",
             "Name", "Place", "Followers", "Friends"])
raw = tweets['Orig_Tweet']
processed = tweets['Tweet']

raw.to_csv("../dataset/tweets_raw.csv", sep=";", header=True, index=False)
processed.to_csv("../dataset/tweets_processed.csv", sep=";", header=True, index=False)

