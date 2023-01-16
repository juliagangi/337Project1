import json

with open('/Users/gilliangracey/Downloads/gg2013.json', 'r') as f:
    data = json.load(f)

def tweet_array():
    tweetarr = []
    keywords = ['wins', 'won', 'nominated', 'nominee', 'award', 'Award', 'Best', 'best']
    for element in data:
        tweet = element['text']
        for keyword in keywords:
            if tweet.__contains__(keyword):
                tweetarr.append(tweet)
                break
    print(tweetarr)
    return tweetarr
tweet_array()

#wins, won, nominated, award, nominee, best, most