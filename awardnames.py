import json
import numpy as np

with open('gg2013.json', 'r') as f:
    data = json.load(f)

def text():
    str = "this is my test string"
    keyword = 'is my'
    print(keyword.index(' '))

def extract_tweets():
    tweetarr = []
    keywords = ['wins', 'won', 'win', 'named', 'nominated', 'nominee', 'award', 'best', 'goes to', 'up for']
    for element in data:
        tweet = element['text']
        if tweet.split()[0] == 'RT':
            continue
        for keyword in keywords:
            if tweet.lower().__contains__(keyword):
                tweetarr.append(tweet.lower())
                break
    return tweetarr


def find_awards(tweets):
    award_names = []
    punctuation = ['.','?']
    before_keywords = ['wins for','wins','won','named','win','nominated for','up for','award for']
    after_keywords = ['goes to','went to']
    for origtweet in tweets:
        curr_list = []
        ind = 0 
        tweet = origtweet.split()
        for keyword in before_keywords:
            if keyword.__contains__(' '):
                if origtweet.__contains__(keyword):
                    space_index = keyword.index(' ')
                    word1 = keyword[0:space_index]
                    word2 = keyword[space_index+1:len(keyword)]
                    keyword = word2
            if tweet.__contains__(keyword):
                index = tweet.index(keyword)
                for i in range(len(tweet)-index-1):
                    portion = tweet[index+1:index+2+i]
                    portion = ' '.join(portion)
                    if i == 0:
                        continue
                    if portion.__contains__('http'):
                        break
                    curr_list = curr_list+[portion]
                    for symbol in punctuation:
                        if portion[len(portion)-1] == symbol:
                            break
                award_names = award_names + [curr_list]
                ind = 1
                break
        if ind:
            continue
        for keyword in after_keywords:
            if keyword.__contains__(' '):
                if origtweet.__contains__(keyword):
                    space_index = keyword.index(' ')
                    word1 = keyword[0:space_index]
                    word2 = keyword[space_index+1:len(keyword)]
                    keyword = word1
            if tweet.__contains__(keyword):
                index = tweet.index(keyword)
                for i in range(index):
                    portion = tweet[i:index]
                    portion = ' '.join(portion)
                    if i == 0:
                        continue
                    if portion.__contains__('http'):
                        break
                    curr_list = curr_list+[portion]
                    for symbol in punctuation:
                        if portion[len(portion)-1] == symbol:
                            break
                award_names = award_names + [curr_list]
    return(award_names)

def rank_awards(awards):
    seen = {}
    for list in awards:
        for award in list:
            if award in seen:
                seen[award] = seen[award] + 1
            else:
                seen[award] = 1
    '''
    most_frequent = {}
    awards = list(seen.keys())
    freqs = list(seen.values())
    for i in range(len(awards)):
        while i < 30:
            most_frequent[awards[i]] = freqs[i] # populate with first 30 awards
        highest_freqs = list(most_frequent.values()) # 30 highest freqs
        curr_min = min(highest_freqs) # 30th highest freq
        curr_freq = freqs[i] # curr freq
        if curr_freq > curr_min:
            min_index = highest_freqs.index(curr_min) # index in most freq
            top_awards = list(most_frequent.keys()) # 30 most freq awards
            pop_award = top_awards[min_index] # award name
            add_award = awards[i] # curr award
            most_frequent.pop(pop_award)
            most_frequent[add_award] = curr_freq    
    '''
    #print(seen)
    most_frequent = {}
    i = 0
    for award in seen:
        if i < 30:
            most_frequent[award] = seen[award]
            i = i + 1
            continue
        curr_freq = seen[award]
        min_pair = get_min_freq(most_frequent)
        min_freq = min_pair[1]
        if curr_freq > min_freq:
            min_freq_award = min_pair[0]
            most_frequent.pop(min_freq_award)
            most_frequent[award] = curr_freq
    #print(most_frequent)
    return most_frequent

def get_min_freq(dict):
    for key in dict:
        curr_min = dict[key]
        curr_min_award = key
        exit
    for key in dict:
        val = dict[key]
        if val < curr_min:
            curr_min = val
            curr_min_award = key
    return (curr_min_award, curr_min)


def test():
    dict={'fake':0}
    dict={'fake':0}
    vals = list(dict.values())
    vals = list(dict.values())
    #print(vals)
    dict["a"]=1
    dict["b"]=2
    dict["c"]=3

    print(dict.keys())

#test()

#print(find_awards(["rt @seanoconnz: did argo get nominated for best original song for this \"dream on\" song? hope so, it sounds great. #goldenglobes",
#"best original song goes to \"skyfall\" by adele! #goldenglobes"]))
tweetarr = extract_tweets()
awards = find_awards(tweetarr)
#print(awards)
print(rank_awards(awards))

