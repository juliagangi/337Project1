import json
import numpy as np
import spacy

nlp = spacy.load("en_core_web_sm")

with open('gg2013.json', 'r') as f:
    data = json.load(f)

def best_dressed(data):
    seen = {}
    forbidden_punct = [',','"','.','!','!','@','#','=',':']
    for element in data:
        tweet = element['text']
        if tweet.split()[0] == 'RT':
            continue
        tweet = tweet.lower()
        if tweet.__contains__('best dressed'):
            start = tweet.index('best dressed')
            appended_best = "best"
            if start != 0:
                prev_char = tweet[start-1]
                index = start-1
                chars_to_add = 5
                while prev_char != ' ' and prev_char != '\n' and index>-1:
                    appended_best = tweet[index:index+chars_to_add]
                    index = index - 1
                    prev_char = tweet[index]
                    chars_to_add = chars_to_add + 1
            tweet = tweet.split()
            index = tweet.index(appended_best) + 2
            for i in range(len(tweet)-1):
                selection = tweet[i:i+2]
                if selection.__contains__('is'):
                    continue
                selection = ' '.join(selection)
                j = 1
                new_selection = selection
                while nlp(selection[len(selection)-j])[0].pos_ == 'PUNCT':
                    new_selection = selection[0:len(selection)-j]
                    j = j + 1
                skip = 0
                for punct in forbidden_punct:
                    if new_selection.__contains__(punct):
                        skip = 1
                        break
                if skip:
                    continue
                ent = nlp(new_selection)[0] 
                if ent.ent_type_ == 'PERSON':
                    if new_selection in seen:
                        seen[new_selection] = seen[new_selection]+1
                    else:
                        seen[new_selection]=1
    for item in seen:
        curr_best = seen[item]
        curr_best_dressed = item
        break
    for item in seen:
        curr = seen[item]
        if curr > curr_best:
            curr_best = curr
            curr_best_dressed = item
    return curr_best_dressed

def worst_dressed(data):
    seen = {}
    forbidden_punct = [',','"','.','!','!','@','#','=',':']
    for element in data:
        tweet = element['text']
        if tweet.split()[0] == 'RT':
            continue
        tweet = tweet.lower()
        if tweet.__contains__('worst dressed'):
            start = tweet.index('worst dressed')
            appended_worst = "worst"
            if start != 0:
                prev_char = tweet[start-1]
                index = start-1
                chars_to_add = 6
                while prev_char != ' ' and prev_char != '\n' and index>-1:
                    appended_worst = tweet[index:index+chars_to_add]
                    index = index - 1
                    prev_char = tweet[index]
                    chars_to_add = chars_to_add + 1
            tweet = tweet.split()
            index = tweet.index(appended_worst) + 2
            for i in range(len(tweet)-1):
                selection = tweet[i:i+2]
                if selection.__contains__('is'):
                    continue
                selection = ' '.join(selection)
                j = 1
                new_selection = selection
                while nlp(selection[len(selection)-j])[0].pos_ == 'PUNCT':
                    new_selection = selection[0:len(selection)-j]
                    j = j + 1
                skip = 0
                for punct in forbidden_punct:
                    if new_selection.__contains__(punct):
                        skip = 1
                        break
                if skip:
                    continue
                ent = nlp(new_selection)[0] 
                if ent.ent_type_ == 'PERSON':
                    if new_selection in seen:
                        seen[new_selection] = seen[new_selection]+1
                    else:
                        seen[new_selection]=1
    for item in seen:
        curr_worst = seen[item]
        curr_worst_dressed = item
        break
    for item in seen:
        curr = seen[item]
        if curr > curr_worst:
            curr_worst = curr
            curr_worst_dressed = item
    return curr_worst_dressed

def extract_tweets(data):
    tweetarr = []
    keywords = ['wins', 'won', 'win', 'named', 'nominated', 'nominee', 'award', 'goes to', 'up for']
    for element in data:
        tweet = element['text']
        if tweet.split()[0] == 'RT':
            continue
        for keyword in keywords:
            tweet = tweet.lower()
            if tweet.__contains__(keyword):
                if tweet.__contains__('best'):
                    tweetarr.append(tweet)
                break
    return tweetarr

'''
def extract_tweets(data):
    tweetarr = []
    keywords = ['wins', 'won', 'win', 'named', 'nominated', 'nominee', 'award', 'goes to', 'up for']
    for element in data:
        tweet = element['text']
        if tweet.split()[0] == 'RT':
            continue
        for keyword in keywords:
            tweet = tweet.lower()
            if tweet.__contains__(keyword):
                if tweet.__contains__('best'):
                    tweetarr.append(tweet)
                break
    return tweetarr
'''

def find_awards(data):
    award_names = []
    prohibited_punctuation = ['.','?','!']
    prohibited_elements = ['#','http']
    allowed_POS = ["NOUN","ADJ"]
    prohibited_POS = ["ADP","AUX","CONJ","DET","PRON","SCONJ"]
    before_keywords = ['award for', 'wins for','wins','won','named','win','nominated for','up for']
    after_keywords = ['goes to','went to']
    for element in data:
        origtweet = element['text']
        #if origtweet.split()[0] == 'RT':
        #    continue
        origtweet = origtweet.lower()
        curr_list = {}
        ind = 0 
        tweet = origtweet.split()
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
                    firstword_pos = nlp(firstword)[0].pos_
                    if (firstword_pos != "ADJ") | (firstword_pos != "NOUN"):
                        continue
                    if nlp(lastword)[0].pos_ != "NOUN":
                        continue
                    if not portion.__contains__('best'):
                        continue
                    if portion.__contains__('dressed') or portion.__contains__('speech'):
                        continue 
                    portion = ' '.join(portion)      
                    for symbol in prohibited_punctuation:
                        if lastword[len(lastword)-1] == symbol:
                            portion = portion[0:len(portion)-1]
                            curr_list[portion] = 1
                            breaking = 1
                            # cut off punctuation
                    for symbol in prohibited_elements:
                        if portion.__contains__(symbol):
                            breaking = 1  
                    if breaking:
                        break
                    if nlp(lastword[len(lastword)-1])[0].pos_ == "PUNCT":
                        portion = portion[0:len(portion)-1]
                        #cut off punctuation
                        #don't want to standardize incorrect phrases
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
                    if nlp(firstword)[0].pos_ != "ADJ":
                        continue
                    if not portion.__contains__('best'):
                        continue 
                    if portion.__contains__('dressed') or portion.__contains__('speech'):
                        continue 
                    portion = ' '.join(portion)
                    #check leftmost word isn't in prev sentence
                    for symbol in prohibited_punctuation:
                        if firstword[len(firstword)-1] == symbol:
                            breaking = 1
                    if nlp(lastword[len(lastword)-1])[0].pos_ == "PUNCT":
                        portion = portion[0:len(portion)-1]
                        #cut off punctuation
                        #don't need to cut off end punct?
                    for symbol in prohibited_elements:
                        if portion.__contains__(symbol):
                            breaking = 1
                    if breaking:
                        break
                    curr_list[portion] = 1
                award_names = award_names + [curr_list]
                break
    return award_names

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
    updated_seen = {} # populate w most freq from each tweet (no duplicates)
    for list2 in awards:
        if len(list2)==0:
            continue
        most_freq_pair = get_max_freq(list2)
        if most_freq_pair[0] in updated_seen:
            updated_seen[most_freq_pair[0]] = updated_seen[most_freq_pair[0]] + most_freq_pair[1]
        if most_freq_pair[0] not in updated_seen:
            updated_seen[most_freq_pair[0]] = most_freq_pair[1]

    '''
    # combine different namings of same award
    for award1 in updated_seen:
        for award2 in updated_seen:
            if award2 != award1:
                if updated_seen[award1] != 0 and updated_seen[award2] != 0:
                    if get_nominees(award1).sort() == get_nominees(award2).sort():
                        if isinstance(updated_seen[award1],int):
                            updated_seen[award1] = [[award2],updated_seen[award1] + updated_seen[award2]]
                        else:
                            updated_seen[award1][0].append(award2)
                            updated_seen[award1][1] = updated_seen[award1][1] + updated_seen[award2]
                        updated_seen[award2] = 0
    # remove redundant awards    
    final_seen = {}
    for key in updated_seen:
        if updated_seen[key] != 0:
            final_seen[key] = updated_seen[key]
    i = 0
    most_frequent = []
    for award in final_seen:
        if final_seen[award][1] > 1:
            most_frequent.append(award[0].append(award))
    return most_frequent
    '''
    # compare parts of speech:
    for award in updated_seen:
        nouns = []
        adjs = []
        for word in award.split():
            if nlp(word)[0].pos_ == 'PUNCT':
                continue
            if nlp(word[len(word)-1])[0].pos_ == 'PUNCT':
                word = word[0:len(word)-1]
            if nlp(word)[0].pos_ == 'NOUN':
                nouns.append(word)
            elif nlp(word)[0].pos_ == 'ADJ':
                adjs.append(word)
        updated_seen[award] = [updated_seen[award],[nouns],[adjs],[]]
    for award1 in updated_seen:
        for award2 in updated_seen:
            if award1 != award2:
                if updated_seen[award1] != 0 and updated_seen[award2] != 0:
                    nouns1 = updated_seen[award1][1]
                    nouns2 = updated_seen[award2][1]
                    adjs1 = updated_seen[award1][2]
                    adjs2 = updated_seen[award2][2]
                    if sorted(nouns1) == sorted(nouns2):
                        if sorted(adjs1) == sorted(adjs2):
                            updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3]+[award2]]
                            updated_seen[award2] = 0
                    elif len(award1) < len(award2):
                        if award2.__contains__(award1):
                            if award2.index(award1) == 0:
                                updated_seen[award1] = 0
                    elif len(award2) < len(award1):
                        if award1.__contains__(award2):
                            if award1.index(award2) == 0:
                                updated_seen[award2] = 0
    final_seen = {}
    for award in updated_seen:
        if updated_seen[award] != 0:
            final_seen[award] = [updated_seen[award][0],updated_seen[award][3]]

    most_frequent = {}
    i = 0
    for award in final_seen:
        # if updated_seen[award][1] > thres: most_frequent.append(award[0].append(award))
        if i < 25:
            most_frequent[award] = final_seen[award]
            i = i + 1
            continue
        curr_freq = final_seen[award][0]
        min_pair = get_min_freq(most_frequent)
        min_freq = min_pair[1]
        if curr_freq > min_freq:
            min_freq_award = min_pair[0]
            most_frequent.pop(min_freq_award)
            most_frequent[award] = final_seen[award]
    return most_frequent

def get_min_in_list(list): # list of 2-item lists
    curr_min_award = list[0][0]
    curr_min = list[0][1]
    for i in range(len(list)):
        val = list[i][1]
        if val < curr_min:
            curr_min = val
            curr_min_award = list[i][0]
    return (curr_min_award, curr_min)

def get_min_freq(dict):
    for key in dict:
        curr_min = dict[key][0]
        curr_min_award = key
        break
    for key in dict:
        val = dict[key][0]
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

def get_nominees(award):
    return ["here","heree"]

def get_awards():
    awards = find_awards(data)
    print(rank_awards(awards))

get_awards()


