import json
import numpy as np
import spacy

nlp = spacy.load("en_core_web_sm")

with open('gg2013.json', 'r') as f:
    data = json.load(f)

def extract_tweets():
    tweetarr = []
    # check it has best/award AND another kw?
    keywords = ['wins', 'won', 'win', 'named', 'nominated', 'nominee', 'award', 'best', 'goes to', 'up for']
    for element in data:
        tweet = element['text']
        #if tweet.split()[0] == 'RT':
            #continue
        for keyword in keywords:
            if tweet.lower().__contains__(keyword):
                tweetarr.append(tweet.lower())
                break
    return tweetarr


def find_awards(tweets):
    award_names = []
    prohibited_punctuation = ['.','?','!']
    prohibited_elements = ['#','http']
    allowed_POS = ["NOUN","ADJ"]
    prohibited_POS = ["ADP","AUX","CONJ","DET","PRON","SCONJ"]
    before_keywords = ['award for', 'wins for','wins','won','named','win','nominated for','up for']
    after_keywords = ['goes to','went to']
    for origtweet in tweets:
        curr_list = {}
        ind = 0 
        tweet = origtweet.split()
        '''
        if tweet.__contains__('best'):
            index = tweet.index('best')
            for i in range(len(tweet)-index-1):
                breaking = 0
                if i == 0:
                    continue
                portion =  tweet[index:index+1+i]
                lastword = portion[len(portion)-1]
                #if lastword == prep | lastword == article:
                    #continue
                for symbol in punctuation:
                    if lastword[len(lastword)-1] == symbol:
                        portion = ' '.join(portion)
                        portion = portion[0:len(portion)-1]
                        breaking = 1
                if not breaking:
                    portion = ' '.join(portion)
                if portion.__contains__('http'):
                    break
                #curr_list = curr_list+[portion]
                curr_list[portion] = 1
                if breaking:
                    break
            award_names = award_names + [curr_list] # need to stay in same index
            #tweetnum = tweetnum + 1
        '''
        for keyword in before_keywords:
            breaking = 0
            if keyword.__contains__(' '):
                if origtweet.__contains__(keyword):
                    space_index = keyword.index(' ')
                    word1 = keyword[0:space_index]
                    word2 = keyword[space_index+1:len(keyword)]
                    keyword = word2
                else:
                    continue
            if tweet.__contains__(keyword):
                ind = 1
                index = tweet.index(keyword)
                for i in range(len(tweet)-index-1):
                    if i == 0:
                        continue    
                    portion = tweet[index+1:index+2+i]
                    firstword = portion[0]
                    lastword = portion[len(portion)-1]
                    if firstword != 'best':
                        continue
                    continuing = 1
                    for symbol in allowed_POS:
                        if nlp(lastword).pos_ == symbol:
                            continuing = 0
                    if continuing:
                        continue
                    portion = ' '.join(portion)
                    if not portion.__contains__('best'):
                        continue        
                    for symbol in prohibited_punctuation:
                        if lastword[len(lastword)-1] == symbol:
                            portion = portion[0:len(portion)-1]
                            # cut off last symbol  
                    for symbol in prohibited_elements:
                        if portion.__contains__(symbol):
                            breaking = 1        
                    #if lastword == prep | lastword == article:
                        #continue
                    if breaking:
                        break

                    '''
                    for symbol in punctuation:
                        if 
                        if lastword[len(lastword)-1] == symbol:
                            portion = ' '.join(portion)
                            portion = portion[0:len(portion)-1]
                            breaking = 1
                    if not breaking:
                        portion = ' '.join(portion)
                    if portion.__contains__('http'):
                        break
                    '''
                    curr_list[portion] = 1
                award_names = award_names + [curr_list]
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
                    if i == 0:
                        continue 
                    breaking = 0
                    portion = tweet[i:index]
                    firstword = portion[0]
                    lastword = portion[len(portion)-1]
                    continuing = 1
                    for symbol in allowed_POS:
                        if nlp(firstword).pos_ == symbol:
                            continuing = 0
                    if continuing:
                        continue
                    portion = ' '.join(portion)
                    if not portion.__contains__('best'):
                        continue 
                    for symbol in prohibited_punctuation:
                        if firstword[len(firstword)-1] == symbol:
                            breaking = 1
                        if lastword[len(lastword)-1] == symbol:
                            portion = portion[0:len(portion)-1]
                            # cut off last symbol  
                    for symbol in prohibited_elements:
                        if portion.__contains__(symbol):
                            breaking = 1
                    if breaking:
                        break
                    '''        
                    lastword = portion[len(portion)-1]
                    #if lastword == prep | lastword == article:
                        #continue
                    portion = ' '.join(portion)
                    for symbol in punctuation:
                        if lastword[len(lastword)-1] == symbol:
                            portion = portion[0:len(portion)-1]
                    if portion.__contains__('http'):
                        break
                    '''
                    curr_list[portion] = 1
                award_names = award_names + [curr_list]
                break
    return(award_names)

def rank_awards(awards):
    seen = {}
    for list in awards:
        for award in list:
            if award in seen:
                seen[award] = seen[award] + 1
            else:
                seen[award] = 1            
    for item in seen: # update freq of each str in awards
        for list1 in awards:
            if item in list1:
                list1[item] = seen[item]
    #return awards
    updated_seen = {} # populate w most freq from each tweet (no duplicates)
    for list2 in awards:
        if len(list2)==0:
            continue
        most_freq_pair = get_max_freq(list2)
        if most_freq_pair[0] not in updated_seen:
            updated_seen[most_freq_pair[0]] = most_freq_pair[1]
    most_frequent = {}
    i = 0
    for award in updated_seen:
        if i < 25:
            most_frequent[award] = updated_seen[award]
            i = i + 1
            continue
        curr_freq = updated_seen[award]
        min_pair = get_min_freq(most_frequent)
        min_freq = min_pair[1]
        if curr_freq > min_freq:
            min_freq_award = min_pair[0]
            most_frequent.pop(min_freq_award)
            most_frequent[award] = curr_freq
    return most_frequent

def get_min_freq(dict):
    for key in dict:
        curr_min = dict[key]
        curr_min_award = key
        break
    for key in dict:
        val = dict[key]
        if val < curr_min:
            curr_min = val
            curr_min_award = key
    return (curr_min_award, curr_min)

def get_max_freq(dict):
    for key in dict:
        curr_max = dict[key]
        curr_max_award = key
        break
    for key in dict:
        val = dict[key]
        if val > curr_max:
            curr_max = val
            curr_max_award = key
    return (curr_max_award, curr_max)

def test():
    str = ("dog")
    new = nlp(str)
    if new.pos_ == "NOUN":
        return 1

test()

'''d
tweetarr = extract_tweets()
awards = find_awards(tweetarr)
print(awards)
#print(rank_awards(awards))
'''