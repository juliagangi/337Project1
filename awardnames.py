import json
import numpy as np
import csv
import spacy
from spacy import displacy
import os
import sys
import re
from collections import defaultdict
nlp = spacy.load("en_core_web_sm")

with open('gg2013.json', 'r') as f:
    data = json.load(f)

def build_json(data):
    return_dict = {}
    award_dict = {}
    return_dict["hosts"] = get_hosts()
    award_names = get_awards(data)
    for award in award_names:
        curr_dict = {}
        nominees = get_nominees(award,the_movies,the_shows)
        curr_dict["nominees:"] = nominees
        curr_dict["presenters:"] = get_presenters(award)
        curr_dict["winner:"] = nominees[0]
        award_dict[award[0]] = curr_dict
    return_dict["award data"] = award_dict
    return return_dict


def build_human_readable(data):
    hosts = ', '.join(get_hosts())
    print('Host: '+hosts+'\n')
    award_names = get_awards(data)
    for award in award_names:
        nominees = (get_nominees(award,the_movies,the_shows))
        nominees = ', '.join(nominees)
        presenters = ', '.join(get_presenters(award))
        winner = nominees[0]
        this_award = award[0]
        print('Award: '+this_award+'')
        print('Nominees: '+nominees+'')
        print('Presenters: '+presenters+'')
        print('Winner: '+winner+'\n')
    bestdressed = best_dressed(data)
    worstdressed = worst_dressed(data)
    print('Best Dressed: '+bestdressed+'')
    print('Worst Dressed: '+worstdressed+'')


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
    forbidden_punct = [',','"','.','!','@','#','=',':']
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


def find_awards(data):
    award_names = []
    prohibited_punctuation = ['.','?','!']
    prohibited_elements = ['#','http']
    allowed_POS = ["NOUN","ADJ"]
    prohibited_POS = ["ADP","AUX","CONJ","DET","PRON","SCONJ"]
    prohibited_words = ["dressed","speech","moment"]
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
                    portion = ' '.join(portion)      
                    for symbol in prohibited_punctuation:
                        if lastword[len(lastword)-1] == symbol:
                            portion = portion[0:len(portion)-1]
                            curr_list[portion] = 1
                            breaking = 1
                            # cut off punctuation
                    for word in prohibited_words:
                        if portion.__contains__(word):
                            breaking = 1
                    for element in prohibited_elements:
                        if portion.__contains__(element):
                            breaking = 1  
                    if breaking:
                        break
                    lastchar = lastword[len(lastword)-1]
                    if nlp(lastchar)[0].pos_ == "PUNCT" and lastchar != ')':
                        portion = portion[0:len(portion)-1]
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
                    for word in prohibited_words:
                        if portion.__contains__(word):
                            breaking = 1
                    for element in prohibited_elements:
                        if portion.__contains__(element):
                            breaking = 1
                    if breaking:
                        break
                    curr_list[portion] = 1
                award_names = award_names + [curr_list]
                break
    return award_names

def rank_awards(data):
    awards = find_awards(data)
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
    updated_seen = {} 
    for list2 in awards: # populate w most freq from each tweet (no duplicates)
        if len(list2)==0:
            continue
        most_freq_pair = get_max_freq(list2)
        if most_freq_pair[0] in updated_seen:
            updated_seen[most_freq_pair[0]] = updated_seen[most_freq_pair[0]] + most_freq_pair[1]
        if most_freq_pair[0] not in updated_seen:
            updated_seen[most_freq_pair[0]] = most_freq_pair[1]
    # create parts of speech lists for each award
    for award in updated_seen:
        nouns = []
        adjs = []
        verbs = []
        for word in award.split():
            if nlp(word)[0].pos_ == 'PUNCT':
                continue
            if word.__contains__('/'): # split terms that in form word1/word2
                index = word.index('/') 
                word1 = word[0:index]
                word2 = word[index+1:len(word)]
                if nlp(word1[0])[0].pos_ == 'PUNCT':
                    word1 = word1[1:len(word1)]
                if nlp(word1)[0].pos_ == 'NOUN':
                    nouns.append(word1)
                elif nlp(word1)[0].pos_ == 'ADJ':
                    adjs.append(word1) 
                elif nlp(word1)[0].pos_ == 'VERB':
                    verbs.append(word1)                   
                if nlp(word2[len(word2)-1])[0].pos_ == 'PUNCT':
                    word2 = word2[0:len(word2)-1]
                elif nlp(word2)[0].pos_ == 'NOUN':
                    nouns.append(word2)
                elif nlp(word2)[0].pos_ == 'ADJ':
                    adjs.append(word2)
                elif nlp(word2)[0].pos_ == 'VERB':
                    verbs.append(word2)
                continue              
            if nlp(word[len(word)-1])[0].pos_ == 'PUNCT': # cut off punc at end of word
                word = word[0:len(word)-1]
            if nlp(word[0])[0].pos_ == 'PUNCT':
                word = word[1:len(word)]
            if nlp(word)[0].pos_ == 'NOUN':
                nouns.append(word)
            elif nlp(word)[0].pos_ == 'ADJ':
                adjs.append(word)
            elif nlp(word)[0].pos_ == 'VERB':
                verbs.append(word)
        updated_seen[award] = [updated_seen[award],nouns,adjs,verbs,[]]
    for award1 in updated_seen: # combine different namings of same award
        for award2 in updated_seen:
            if award1 != award2:
                if updated_seen[award1] != 0 and updated_seen[award2] != 0:
                    nouns1 = updated_seen[award1][1]
                    nouns2 = updated_seen[award2][1]
                    adjs1 = updated_seen[award1][2]
                    adjs2 = updated_seen[award2][2]
                    verbs1 = updated_seen[award1][3]
                    verbs2 = updated_seen[award2][3]
                    if sorted(nouns1) == sorted(nouns2): # check if all parts of speech lists match
                        if sorted(adjs1) == sorted(adjs2):
                            if sorted(verbs1) == sorted(verbs2):
                                if updated_seen[award1][0] > updated_seen[award2][0]:
                                    updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                                    updated_seen[award2] = 0
                                else:
                                    updated_seen[award2] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                                    updated_seen[award1] = 0 
                    else:
                        if len(award1) < len(award2) and award2.__contains__(award1): # check if an award is start of another 
                            if award2.index(award1) == 0:
                                updated_seen[award2][0] = updated_seen[award1][0]+updated_seen[award2][0]
                                updated_seen[award1] = 0
                        elif len(award2) < len(award1) and award1.__contains__(award2): # check if an award is start of another
                            if award1.index(award2) == 0:
                                updated_seen[award1][0] = updated_seen[award1][0]+updated_seen[award2][0]
                                updated_seen[award2] = 0
                        '''
                        else: # check if nouns list is fully contained by other
                            sortednouns1 = ' '.join(sorted(nouns1))
                            sortednouns2 = ' '.join(sorted(nouns2))
                            #if award1 == 'best actor in a motion picture comedy/musical' and award2 == 'best actor, comedy/musical':
                            #    print("in else")
                            #    print(sortednouns1)
                            #    print(sortednouns2)
                            #if award1 == 'best actress, tv drama' and award2 == 'best actress in a tv series, drama':
                            #    print("in else2")
                            #    print(sortednouns1)
                            #    print(sortednouns2)
                            if len(nouns1) < len(nouns2):
                                if sortednouns2.__contains__(sortednouns1):
                                    updated_seen[award2] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                                    updated_seen[award1] = 0
                            elif len(nouns1) > len(nouns2):
                                if sortednouns1.__contains__(sortednouns2):
                                    updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                                    updated_seen[award2] = 0
                        # check if nominees are same
                        
                    elif sorted(get_nominees(award1,the_movies,the_shows)) == sorted(get_nominees(award2,the_movies,the_shows)):
                        if updated_seen[award1][0] > updated_seen[award2][0]:
                            updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                            updated_seen[award2] = 0
                        else:
                            updated_seen[award2] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                            updated_seen[award1] = 0  
                    else:
                        continue
                    '''    
    '''                         
    most_frequent = []
    for award in final_seen:
        if final_seen[award][1] > 1:
            most_frequent.append(award[0].append(award))
    return most_frequent
    '''
    final_seen = {}
    for award in updated_seen: # remove awards that are now alternative names for other
        if updated_seen[award] != 0:
            final_seen[award] = [updated_seen[award][0],updated_seen[award][4]]
    most_frequent = {}
    i = 0
    '''
    return_array = []
    for award in final_seen:
        if final_seen[award][0] > 25:
            return_array.append([award]+final_seen[award][1])
    return return_array
    '''
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
    the_awards = []
    for award in most_frequent:
        the_awards.append([award]+most_frequent[award][1])
    return the_awards

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

def get_awards(data):
    awards = find_awards(data)
    return rank_awards(awards)



actordict = {}
moviedict = {}
with open('newfile.csv') as csv_file:   
    counter=1
    for row in csv_file:
        index = 0
        if counter==19132:
            break
        elif counter%2!=0:
            name = ""
            last = ""
            lastflag = False
            while row[index] != ',':
                name+=row[index]
                if lastflag == True:
                    last+= row[index]
                if row[index] == " ":
                    lastflag = True
                index+=1
            if lastflag==True:
                actordict[name] = last
        counter+=1

titles = []
with open('Top5000.csv') as csv_file:
    counter=0
    for row in csv_file:
        index = 0
        if counter==0:
            counter+=1
        else:
            row = row.split(',')
            titles.append(row[5])

shows = []
with open('1000shows.csv') as csv_file:
    counter=0
    for row in csv_file:
        index = 0
        if counter==0:
            counter+=1
        else:
            row = row.split(',')
            shows.append(row[5])

def get_people():
    relevant_tweets = []
    relevant_actors = {}
    counter=0
    for element in data:
        tweet = element['text'].lower()
        #if tweet[0]=="r" and tweet[1] == "t":
        #    counter+=1
        if tweet.__contains__('nominated') or tweet.__contains__('nominee') or tweet.__contains__('actress') or tweet.__contains__('actor')  or tweet.__contains__('presenting') or tweet.__contains__('win') or tweet.__contains__('tonight') or tweet.__contains__('presenter'):
            relevant_tweets.append(tweet)
    for tweet in relevant_tweets:
        for actor in actordict:
            last = actordict[actor].lower()
            actor = actor.lower()
            lastvec = [actor, last]
            if tweet.__contains__(actor) and actor not in relevant_actors:
                if lastvec[-1] == "" or len(lastvec[-1])<=2:
                    lastvec.pop(-1)
                    lastvec.append("trewqyuioplkhgd")
                    lastvec[0] = "a;lskdjfa;lsdkjf"
                relevant_actors[actor] = lastvec
    return relevant_actors

def get_movies():
    relevant_tweets = []
    relevant_movies = {}
    relevant_shows = {}
    counter=0
    for element in data:
        tweet = element['text'].lower()
        #if tweet[0]=="r" and tweet[1] == "t":
            #counter+=1
        if tweet.__contains__('nominated') or tweet.__contains__('nominee') or tweet.__contains__('movie') or tweet.__contains__('win') or tweet.__contains__('award') or tweet.__contains__('series') or tweet.__contains__('show'):
            relevant_tweets.append(tweet)
    for tweet in relevant_tweets:
        for movie in titles:
            movie = movie.lower()
            if tweet.__contains__(movie) and movie not in relevant_movies:
                if movie[0]=="t" and movie[1] == "h" and movie[2] == "e":
                    without_the = movie[4:]
                    relevant_movies[movie] = [movie, without_the]
                if len(movie)>=4:
                    relevant_movies[movie] = [movie]
        for show in shows:
            show = show.lower()
            if tweet.__contains__(show) and len(show)>4:
                relevant_shows[show] = show
    return [relevant_movies, relevant_shows]

the_shows = {'julia': 'julia', 'modern family': 'modern family', 'medium': 'medium', 'homeland': 'homeland', 'girls': 'girls', 'shameless': 'shameless', 'scandal': 'scandal', 'episodes': 'episodes', 'revenge': 'revenge', 'the girl': 'the girl', 'taggart': 'taggart', 'ellen': 'ellen', 'angel': 'angel', 'the newsroom': 'the newsroom', 'smash': 'smash', 'the goodies': 'the goodies', 'africa': 'africa', 'breaking bad': 'breaking bad', 'matlock': 'matlock', 'the walking dead': 'the walking dead', 'downton abbey': 'downton abbey', 'boardwalk empire': 'boardwalk empire', 'empire': 'empire', 'the big bang theory': 'the big bang theory', 'cheers': 'cheers', 'the flash': 'the flash', 'nashville': 'nashville', 'the andy williams show': 'the andy williams show', 'american horror story': 'american horror story', 'game change': 'game change', 'bones': 'bones', 'bottom': 'bottom', 'californication': 'californication', 'chuck': 'chuck', 'dallas': 'dallas', 'friends': 'friends', 'the hour': 'the hour', 'community': 'community', 'political animals': 'political animals', 'the league': 'the league', 'suits': 'suits', 'hatfields and mccoys': 'hatfields and mccoys', 'seinfeld': 'seinfeld', 'gilmore girls': 'gilmore girls', 'buffy the vampire slayer': 'buffy the vampire slayer', 'dexter': 'dexter', 'dear john': 'dear john', 'teachers': 'teachers', 'alias': 'alias', 'saturday night live': 'saturday night live', 'vicious': 'vicious', 'bodies': 'bodies', 'soul train': 'soul train', 'i spy': 'i spy', 'grimm': 'grimm', 'casanova': 'casanova', 'the thorn birds': 'the thorn birds', 'parenthood': 'parenthood', 'game of thrones': 'game of thrones', 'the only way is essex': 'the only way is essex', 'sherlock': 'sherlock', 'mad men': 'mad men', 'band of brothers': 'band of brothers', 'cracker': 'cracker', 'a grande família': 'a grande família', 'gossip girl': 'gossip girl', 'treme': 'treme', 'stella': 'stella', 'sons of anarchy': 'sons of anarchy', 'firefly': 'firefly', 'once upon a time': 'once upon a time', 'my so-called life': 'my so-called life', 'bread': 'bread', 'true blood': 'true blood', 'merlin': 'merlin', 'minder': 'minder', 'the street': 'the street', 'the wire': 'the wire', 'fargo': 'fargo', 'the flintstones': 'the flintstones', 'castle': 'castle', 'fringe': 'fringe', 'roots': 'roots', 'the x factor': 'the x factor', 'our girl': 'our girl', 'my family': 'my family', 'the west wing': 'the west wing', 'charmed': 'charmed', 'derek': 'derek', "grey's anatomy": "grey's anatomy", 'the unit': 'the unit', 'heroes': 'heroes', 'the bill': 'the bill', 'the office': 'the office', 'the stand': 'the stand', 'new girl': 'new girl', 'veronica mars': 'veronica mars', 'twin peaks': 'twin peaks', '30 rock': '30 rock', 'roswell': 'roswell', 'batman': 'batman', 'the golden girls': 'the golden girls', 'cannon': 'cannon', 'family guy': 'family guy', 'louie': 'louie', 'elementary': 'elementary', 'derrick': 'derrick', 'good times': 'good times', 'the carol burnett show': 'the carol burnett show', 'the following': 'the following', 'the trip': 'the trip', 'happy endings': 'happy endings', 'arrow': 'arrow', 'pretty little liars': 'pretty little liars', 'dynasty': 'dynasty', 'duck dynasty': 'duck dynasty', 'archer': 'archer', 'ray donovan': 'ray donovan', 'star trek': 'star trek', 'dancing with the stars': 'dancing with the stars', 'the americans': 'the americans', 'the avengers': 'the avengers', 'hustle': 'hustle', 'this life': 'this life', 'accused': 'accused', 'entourage': 'entourage', 'maverick': 'maverick', 'parks and recreation': 'parks and recreation', 'absolutely fabulous': 'absolutely fabulous', 'chips': 'chips', 'familie': 'familie', "parade's end": "parade's end", 'the voice': 'the voice', 'skins': 'skins', 'the untouchables': 'the untouchables', 'getting on': 'getting on', 'extras': 'extras', 'prisoner': 'prisoner', 'scrubs': 'scrubs', 'navarro': 'navarro'}
the_movies = {'salmon fishing in the yemen': ['salmon fishing in the yemen'], 'deep blue sea': ['deep blue sea'], 'hitch': ['hitch'], '2012': ['2012'], 'hitchcock': ['hitchcock'], 'cars': ['cars'], 'always': ['always'], 'paul': ['paul'], 'django unchained': ['django unchained'], 'lincoln': ['lincoln'], 'hair': ['hair'], 'bronson': ['bronson'], 'last night': ['last night'], 'zero dark thirty': ['zero dark thirty'], 'enough': ['enough'], 'rope': ['rope'], 'control': ['control'], 'amour': ['amour'], 'argo': ['argo'], 'the conversation': ['the conversation'], 'drive': ['drive'], 'following': ['following'], 'stay': ['stay'], 'rush': ['rush'], 'the crow': ['the crow'], 'wild': ['wild'], 'hunger': ['hunger'], 'skyfall': ['skyfall'], 'anna': ['anna'], 'once': ['once'], 'silver linings playbook': ['silver linings playbook'], 'blow': ['blow'], 'my girl': ['my girl'], 'shame': ['shame'], 'next': ['next'], 'nine': ['nine'], 'hick': ['hick'], 'gamer': ['gamer'], 'safe': ['safe'], 'chocolat': ['chocolat'], 'chef': ['chef'], 'lucy': ['lucy'], 'the golden compass': ['the golden compass'], 'knowing': ['knowing'], 'rent': ['rent'], 'selena': ['selena'], 'network': ['network'], 'brave': ['brave'], 'flight': ['flight'], 'tron': ['tron'], 'gone with the wind': ['gone with the wind'], 'gone': ['gone'], 'super': ['super'], 'the interview': ['the interview'], 'mommy': ['mommy'], 'heat': ['heat'], 'ghost': ['ghost'], 'ghostbusters': ['ghostbusters'], 'laura': ['laura'], 'antz': ['antz'], 'persona': ['persona'], 'jobs': ['jobs'], 'weekend': ['weekend'], 'doubt': ['doubt'], 'iron man': ['iron man'], 'frankenstein': ['frankenstein'], 'frank': ['frank'], 'true grit': ['true grit'], 'the tourist': ['the tourist'], 'the way': ['the way'], 'the host': ['the host'], 'dave': ['dave'], 'election': ['election'], 'cocktail': ['cocktail'], 'salt': ['salt'], 'speed': ['speed'], 'the lorax': ['the lorax'], 'devil': ['devil'], 'the double': ['the double'], 'agora': ['agora'], 'gandhi': ['gandhi'], '1408': ['1408'], 'signs': ['signs'], 'the hunger games': ['the hunger games'], 'life of pi': ['life of pi'], 'alexander': ['alexander'], 'wanted': ['wanted'], 'radio': ['radio'], 'the pill': ['the pill'], 'funny people': ['funny people'], 'powder': ['powder'], 'taken': ['taken'], 'the first time': ['the first time'], 'the master': ['the master'], 'bound': ['bound'], 'clue': ['clue'], 'chicago': ['chicago'], 'the flash': ['the flash'], 'the thing': ['the thing'], 'freaks': ['freaks'], 'shaft': ['shaft'], 'rebecca': ['rebecca'], 'trash': ['trash'], 'titanic': ['titanic'], 'inglourious basterds': ['inglourious basterds'], 'legend': ['legend'], 'alive': ['alive'], "sophie's choice": ["sophie's choice"], 'the road': ['the road'], 'on the road': ['on the road'], 'carrie': ['carrie'], 'jaws': ['jaws'], 'gravity': ['gravity'], 'troy': ['troy'], 'the watch': ['the watch'], 'blitz': ['blitz'], 'game change': ['game change'], 'one day': ['one day'], 'scream': ['scream'], 'les misérables': ['les misérables'], 'bobby': ['bobby'], 'brick': ['brick'], 'some like it hot': ['some like it hot'], 'patton': ['patton'], 'annie': ['annie'], 'submarine': ['submarine'], 'wreck-it ralph': ['wreck-it ralph'], 'easy a': ['easy a'], 'timeline': ['timeline'], 'babe': ['babe'], 'robots': ['robots'], 'thirteen': ['thirteen'], 'the game': ['the game'], 'beautiful creatures': ['beautiful creatures'], 'the departed': ['the departed'], 'primer': ['primer'], 'prime': ['prime'], 'tusk': ['tusk'], 'setup': ['setup'], 'temple grandin': ['temple grandin'], 'somewhere': ['somewhere'], 'mama': ['mama'], 'back to the future': ['back to the future'], 'australia': ['australia'], 'not cool': ['not cool'], 'trance': ['trance'], 'buffy the vampire slayer': ['buffy the vampire slayer'], 'lawless': ['lawless'], 'a haunted house': ['a haunted house'], 'dear john': ['dear john'], 'crash': ['crash'], 'traffic': ['traffic'], 'accepted': ['accepted'], 'the kid': ['the kid'], 'the box': ['the box'], 'goon': ['goon'], 'a single man': ['a single man'], 'halloween': ['halloween'], 'holes': ['holes'], 'epic': ['epic'], 'the dark knight': ['the dark knight'], 'the dark knight rises': ['the dark knight rises'], 'casanova': ['casanova'], 'thor': ['thor'], 'flipped': ['flipped'], 'the best exotic marigold hotel': ['the best exotic marigold hotel'], 'hope springs': ['hope springs'], 'eat pray love': ['eat pray love'], 'catwoman': ['catwoman'], 'selma': ['selma'], 'star wars': ['star wars'], 'brothers': ['brothers'], 'closer': ['closer'], 'clueless': ['clueless'], 'pride': ['pride'], 'conspiracy': ['conspiracy'], 'rudderless': ['rudderless'], 'that awkward moment': ['that awkward moment'], 'the others': ['the others'], 'home alone': ['home alone'], 'scoop': ['scoop'], 'now and then': ['now and then'], 'monster': ['monster'], 'monsters': ['monsters'], 'spartacus': ['spartacus'], 'hotel transylvania': ['hotel transylvania'], 'awake': ['awake'], 'deception': ['deception'], 'the american': ['the american'], 'the core': ['the core'], 'the producers': ['the producers'], 'abduction': ['abduction'], 'anna karenina': ['anna karenina'], 'x-men': ['x-men'], 'moon': ['moon'], 'moonrise kingdom': ['moonrise kingdom'], 'parker': ['parker'], 'fargo': ['fargo'], 'gigli': ['gigli'], 'the ward': ['the ward'], 'the score': ['the score'], 'superman': ['superman'], 'the flintstones': ['the flintstones'], 'cloud atlas': ['cloud atlas'], 'premature': ['premature'], 'evolution': ['evolution'], 'act of valor': ['act of valor'], 'music and lyrics': ['music and lyrics'], 'epic movie': ['epic movie'], 'the queen': ['the queen'], 'noah': ['noah'], 'wall street': ['wall street'], 'amistad': ['amistad'], 'precious': ['precious'], 'despicable me': ['despicable me'], 'twilight': ['twilight'], 'witness': ['witness'], 'legion': ['legion'], 'philadelphia': ['philadelphia'], 'the beaver': ['the beaver'], 'beasts of the southern wild': ['beasts of the southern wild'], 'felon': ['felon'], 'neighbors': ['neighbors'], 'chronicle': ['chronicle'], 'die hard': ['die hard'], 'looper': ['looper'], 'the words': ['the words'], 'filth': ['filth'], "breakfast at tiffany's": ["breakfast at tiffany's"], 'pocahontas': ['pocahontas'], 'machete': ['machete'], 'machete kills': ['machete kills'], 'domino': ['domino'], "valentine's day": ["valentine's day"], 'spy kids': ['spy kids'], 'sherlock holmes': ['sherlock holmes'], 'alien': ['alien'], 'upside down': ['upside down'], '"honey': ['"honey'], 'bedazzled': ['bedazzled'], 'dances with wolves': ['dances with wolves'], "she's all that": ["she's all that"], 'kinsey': ['kinsey'], 'hulk': ['hulk'], 'waterworld': ['waterworld'], 'goodfellas': ['goodfellas'], 'the bodyguard': ['the bodyguard'], 'deja vu': ['deja vu'], 'field of dreams': ['field of dreams'], 'snatch': ['snatch'], 'roman holiday': ['roman holiday'], '"dude': ['"dude'], 'exam': ['exam'], 'locke': ['locke'], 'casper': ['casper'], 'hot tub time machine': ['hot tub time machine'], 'brazil': ['brazil'], 'the hangover': ['the hangover'], 'the eagle': ['the eagle'], "winter's bone": ["winter's bone"], 'ted 2': ['ted 2'], 'glitter': ['glitter'], 'hook': ['hook'], 'the artist': ['the artist'], 'sabrina': ['sabrina'], 'bait': ['bait'], 'veronica mars': ['veronica mars'], 'the guardian': ['the guardian'], 'the guard': ['the guard'], 'rise of the guardians': ['rise of the guardians'], 'house at the end of the street': ['house at the end of the street'], 'the princess diaries': ['the princess diaries'], 'be cool': ['be cool'], 'trouble with the curve': ['trouble with the curve'], 'the paperboy': ['the paperboy'], 'magic mike': ['magic mike'], 'peter pan': ['peter pan'], 'into the wild': ['into the wild'], 'battleship': ['battleship'], 'batman': ['batman'], 'the spirit': ['the spirit'], 'the fly': ['the fly'], 'unstoppable': ['unstoppable'], 'milk': ['milk'], 'the butler': ['the butler'], 'tootsie': ['tootsie'], 'mean girls': ['mean girls'], 'gangster squad': ['gangster squad'], 'pulp fiction': ['pulp fiction'], 'the family': ['the family'], 'about time': ['about time'], 'unknown': ['unknown'], 'a river runs through it': ['a river runs through it'], 'hotel rwanda': ['hotel rwanda'], 'rush hour': ['rush hour'], 'superhero movie': ['superhero movie'], 'the campaign': ['the campaign'], "it's complicated": ["it's complicated"], 'd2: the mighty ducks': ['d2: the mighty ducks'], 'bullet to the head': ['bullet to the head'], 'rocky': ['rocky'], 'the terminator': ['the terminator'], 'intouchables': ['intouchables'], 'rambo': ['rambo'], 'chaos': ['chaos'], 'rust and bone': ['rust and bone'], 'romeo and juliet': ['romeo and juliet'], 'outbreak': ['outbreak'], 'the other guys': ['the other guys'], 'frankenweenie': ['frankenweenie'], 'doom': ['doom'], 'paranorman': ['paranorman'], 'the witches': ['the witches'], 'eraser': ['eraser'], 'far and away': ['far and away'], 'monsters university': ['monsters university'], 'get the gringo': ['get the gringo'], 'pitch perfect': ['pitch perfect'], 'perfect sense': ['perfect sense'], 'requiem for a dream': ['requiem for a dream'], 'sunshine': ['sunshine'], 'buried': ['buried'], 'role models': ['role models'], 'star trek': ['star trek'], 'hobo with a shotgun': ['hobo with a shotgun'], 'body double': ['body double'], 'kon-tiki': ['kon-tiki'], 'true story': ['true story'], 'the avengers': ['the avengers'], 'flightplan': ['flightplan'], 'friday': ['friday'], 'frida': ['frida'], 'freaky friday': ['freaky friday'], 'contact': ['contact'], 'panic room': ['panic room'], 'the holiday': ['the holiday'], 'sex tape': ['sex tape'], 'little fockers': ['little fockers'], 'inside man': ['inside man'], 'chloe': ['chloe'], 'barefoot': ['barefoot'], 'out of time': ['out of time'], 'blade': ['blade'], 'the hours': ['the hours'], 'mallrats': ['mallrats'], 'how high': ['how high'], 'twister': ['twister'], 'sideways': ['sideways'], 'daredevil': ['daredevil'], 'bang bang': ['bang bang'], 'armageddon': ['armageddon'], 'shrek': ['shrek'], 'entourage': ['entourage'], 'notorious': ['notorious'], 'this is 40': ['this is 40'], 'the call': ['the call'], 'maverick': ['maverick'], '"i love you': ['"i love you'], 'kick-ass': ['kick-ass'], 'old school': ['old school'], 'bring it on': ['bring it on'], 'disconnect': ['disconnect'], 'giant': ['giant'], 'marnie': ['marnie'], 'the vow': ['the vow'], 'bernie': ['bernie'], 'school of rock': ['school of rock'], 'van helsing': ['van helsing'], 'elektra': ['elektra'], 'passion': ['passion'], 'the losers': ['the losers'], '13 going on 30': ['13 going on 30'], 'the expendables': ['the expendables'], 'the expendables 2': ['the expendables 2'], 'the wolverine': ['the wolverine'], 'hugo': ['hugo'], 'tangled': ['tangled'], 'aliens': ['aliens'], 'prometheus': ['prometheus'], 'the hurt locker': ['the hurt locker'], 'avatar': ['avatar'], 'the dictator': ['the dictator'], 'takers': ['takers'], 'love story': ['love story'], 'killers': ['killers'], 'christine': ['christine'], 'samba': ['samba'], 'glory': ['glory'], 'the sessions': ['the sessions'], 'gangs of new york': ['gangs of new york'], 'orphan': ['orphan'], 'do the right thing': ['do the right thing'], 'in the name of the father': ['in the name of the father'], 'the untouchables': ['the untouchables'], 'taken 2': ['taken 2'], 'mirror mirror': ['mirror mirror'], 'big trouble in little china': ['big trouble in little china'], 'pretty woman': ['pretty woman'], 'the town': ['the town'], 'the grey': ['the grey'], 'abraham lincoln: vampire hunter': ['abraham lincoln: vampire hunter'], 'true lies': ['true lies'], 'hackers': ['hackers'], 'click': ['click'], '"good night': ['"good night'], 'miracle': ['miracle'], 'iron man 2': ['iron man 2'], 'the scorpion king': ['the scorpion king'], 'brokeback mountain': ['brokeback mountain'], 'the crazies': ['the crazies'], 'non-stop': ['non-stop'], 'the ring': ['the ring'], 'goldfinger': ['goldfinger'], 'saving private ryan': ['saving private ryan'], 'the hunt for red october': ['the hunt for red october'], 'the reader': ['the reader'], 'cube': ['cube'], 'dreamgirls': ['dreamgirls'], 'akira': ['akira'], 'vertigo': ['vertigo'], 'jack reacher': ['jack reacher'], 'inception': ['inception'], 'taxi driver': ['taxi driver'], 'heathers': ['heathers'], 'as good as it gets': ['as good as it gets']}

persondict = {'kerry washington': ['kerry washington', 'washington'], 'helen mirren': ['helen mirren', 'mirren'], 'anjelica huston': ['anjelica huston', 'huston'], 'leonardo dicaprio': ['leonardo dicaprio', 'dicaprio'], 'jessica chastain': ['jessica chastain', 'chastain'], 'sarah hyland': ['sarah hyland', 'hyland'], 'ariel winter': ['ariel winter', 'winter'], 'jennifer lopez': ['jennifer lopez', 'lopez'], 'anne hathaway': ['anne hathaway', 'hathaway'], 'bradley cooper': ['bradley cooper', 'cooper'], 'hugh jackman': ['hugh jackman', 'jackman'], 'jennifer lawrence': ['jennifer lawrence', 'lawrence'], 'louis c.k.': ['louis c.k.', 'c.k.'], 'ben affleck': ['ben affleck', 'affleck'], 'bill murray': ['bill murray', 'murray'], 'priscilla presley': ['priscilla presley', 'presley'], 'lucy liu': ['lucy liu', 'liu'], 'julianne hough': ['julianne hough', 'hough'], 'taylor swift': ['taylor swift', 'swift'], 'sofia vergara': ['sofia vergara', 'vergara'], 'eva longoria': ['eva longoria', 'longoria'], 'sally field': ['sally field', 'field'], 'andrew lincoln': ['andrew lincoln', 'lincoln'], 'jay leno': ['jay leno', 'leno'], 'jessica lange': ['jessica lange', 'lange'], 'tina fey': ['tina fey', 'fey'], 'amy poehler': ['amy poehler', 'poehler'], 'lucille ball': ['lucille ball', 'ball'], 'helen hunt': ['helen hunt', 'hunt'], 'linda gray': ['linda gray', 'gray'], 'dustin hoffman': ['dustin hoffman', 'hoffman'], 'emily deschanel': ['emily deschanel', 'deschanel'], 'laura linney': ['laura linney', 'linney'], 'francesca eastwood': ['francesca eastwood', 'eastwood'], 'nicole kidman': ['nicole kidman', 'kidman'], 'jim parsons': ['jim parsons', 'parsons'], 'mel gibson': ['mel gibson', 'gibson'], 'stacy keibler': ['stacy keibler', 'keibler'], 'julianne moore': ['julianne moore', 'moore'], 'robert downey jr.': ['robert downey jr.', 'downey jr.'], 'julianna margulies': ['julianna margulies', 'margulies'], 'michelle dockery': ['michelle dockery', 'dockery'], 'george clooney': ['george clooney', 'clooney'], 'ricky gervais': ['ricky gervais', 'gervais'], 'zooey deschanel': ['zooey deschanel', 'deschanel'], 'olivia munn': ['olivia munn', 'munn'], 'lena dunham': ['lena dunham', 'dunham'], 'david faustino': ['david faustino', 'faustino'], 'kristen bell': ['kristen bell', 'bell'], 'dax shepard': ['dax shepard', 'shepard'], 'jessica alba': ['jessica alba', 'alba'], 'james cameron': ['james cameron', 'cameron'], 'amy adams': ['amy adams', 'adams'], 'richard gere': ['richard gere', 'gere'], 'kathryn bigelow': ['kathryn bigelow', 'bigelow'], 'emily blunt': ['emily blunt', 'blunt'], 'meryl streep': ['meryl streep', 'streep'], 'ang lee': ['ang lee', 'lee'], 'daniel day-lewis': ['daniel day-lewis', 'day-lewis'], 'kate hudson': ['kate hudson', 'hudson'], 'lea michele': ['lea michele', 'michele'], 'alan arkin': ['alan arkin', 'arkin'], 'tommy lee jones': ['tommy lee jones', 'lee jones'], 'christoph waltz': ['christoph waltz', 'waltz'], 'daniel craig': ['daniel craig', 'craig'], 'denzel washington': ['denzel washington', 'washington'], 'benedict cumberbatch': ['benedict cumberbatch', 'cumberbatch'], 'mandy patinkin': ['mandy patinkin', 'patinkin'], 'dennis quaid': ['dennis quaid', 'quaid'], 'maggie smith': ['maggie smith', 'smith'], 'connie britton': ['connie britton', 'britton'], 'hayden panettiere': ['hayden panettiere', 'panettiere'], 'sarah paulson': ['sarah paulson', 'paulson'], 'christina hendricks': ['christina hendricks', 'hendricks'], 'philip seymour hoffman': ['philip seymour hoffman', 'seymour hoffman'], 'mariska hargitay': ['mariska hargitay', 'hargitay'], 'christopher meloni': ['christopher meloni', 'meloni'], 'quentin tarantino': ['quentin tarantino', 'tarantino'], 'jared leto': ['jared leto', 'leto'], 'gary oldman': ['gary oldman', 'oldman'], 'jamie foxx': ['jamie foxx', 'foxx'], 'halle berry': ['halle berry', 'berry'], 'ed harris': ['ed harris', 'harris'], 'kim kardashian': ['kim kardashian', 'kardashian'], 'don cheadle': ['don cheadle', 'cheadle'], 'clint eastwood': ['clint eastwood', 'eastwood'], 'tom ford': ['tom ford', 'ford'], 'amanda seyfried': ['amanda seyfried', 'seyfried'], 'danny strong': ['danny strong', 'strong'], 'allison williams': ['allison williams', 'williams'], 'sigourney weaver': ['sigourney weaver', 'weaver'], 'frances fisher': ['frances fisher', 'fisher'], 'toby jones': ['toby jones', 'jones'], 'sienna miller': ['sienna miller', 'miller'], 'jack black': ['jack black', 'black'], 'anna nicole smith': ['anna nicole smith', 'nicole smith'], 'claire danes': ['claire danes', 'danes'], 'marion cotillard': ['marion cotillard', 'cotillard'], 'julia roberts': ['julia roberts', 'roberts'], 'catherine zeta-jones': ['catherine zeta-jones', 'zeta-jones'], 'alec baldwin': ['alec baldwin', 'baldwin'], 'matt leblanc': ['matt leblanc', 'leblanc'], 'russell crowe': ['russell crowe', 'crowe'], 'justin timberlake': ['justin timberlake', 'timberlake'], 'rosario dawson': ['rosario dawson', 'dawson'], 'judi dench': ['judi dench', 'dench'], 'paul rudd': ['paul rudd', 'rudd'], 'salma hayek': ['salma hayek', 'hayek'], 'bryan cranston': ['bryan cranston', 'cranston'], 'steve buscemi': ['steve buscemi', 'buscemi'], 'jennifer garner': ['jennifer garner', 'garner'], 'jeff daniels': ['jeff daniels', 'daniels'], 'jon hamm': ['jon hamm', 'hamm'], 'damian lewis': ['damian lewis', 'lewis'], 'dev patel': ['dev patel', 'patel'], 'hugh laurie': ['hugh laurie', 'laurie'], 'harrison ford': ['harrison ford', 'ford'], 'michael c. hall': ['michael c. hall', 'c. hall'], 'jeremy renner': ['jeremy renner', 'renner'], 'lindsay lohan': ['lindsay lohan', 'lohan'], 'kate winslet': ['kate winslet', 'winslet'], 'harvey weinstein': ['harvey weinstein', 'weinstein'], 'diego klattenhoff': ['diego klattenhoff', 'klattenhoff'], 'eddie redmayne': ['eddie redmayne', 'redmayne'], 'isla fisher': ['isla fisher', 'fisher'], 'john goodman': ['john goodman', 'goodman'], 'naomi watts': ['naomi watts', 'watts'], 'jason statham': ['jason statham', 'statham'], 'john williams': ['john williams', 'williams'], 'joseph gordon-levitt': ['joseph gordon-levitt', 'gordon-levitt'], 'michael j. fox': ['michael j. fox', 'j. fox'], 'nolan gould': ['nolan gould', 'gould'], 'rico rodriguez': ['rico rodriguez', 'rodriguez'], 'christopher walken': ['christopher walken', 'walken'], 'megan fox': ['megan fox', 'fox'], 'paul f. tompkins': ['paul f. tompkins', 'f. tompkins'], 'jodie foster': ['jodie foster', 'foster'], 'eric stonestreet': ['eric stonestreet', 'stonestreet'], 'justin bieber': ['justin bieber', 'bieber'], 'harry styles': ['harry styles', 'styles'], 'kevin costner': ['kevin costner', 'costner'], 'woody harrelson': ['woody harrelson', 'harrelson'], 'david hyde pierce': ['david hyde pierce', 'hyde pierce'], 'johnny depp': ['johnny depp', 'depp'], 'chris rock': ['chris rock', 'rock'], 'kiefer sutherland': ['kiefer sutherland', 'sutherland'], 'steven spielberg': ['steven spielberg', 'spielberg'], 'will ferrell': ['will ferrell', 'ferrell'], 'kristen wiig': ['kristen wiig', 'wiig'], 'heidi klum': ['heidi klum', 'klum'], 'archie panjabi': ['archie panjabi', 'panjabi'], 'michael caine': ['michael caine', 'caine'], 'haley joel osment': ['haley joel osment', 'joel osment'], 'fred armisen': ['fred armisen', 'armisen'], 'chris tucker': ['chris tucker', 'tucker'], 'whitney houston': ['whitney houston', 'houston'], 'max greenfield': ['max greenfield', 'greenfield'], 'john krasinski': ['john krasinski', 'krasinski'], 'oprah winfrey': ['oprah winfrey', 'winfrey'], 'melanie griffith': ['melanie griffith', 'griffith'], 'demi moore': ['demi moore', 'moore'], 'jonah hill': ['jonah hill', 'hill'], 'liza minnelli': ['liza minnelli', 'minnelli'], 'helena bonham carter': ['helena bonham carter', 'bonham carter'], 'ewan mcgregor': ['ewan mcgregor', 'mcgregor'], 'morgan freeman': ['morgan freeman', 'freeman'], 'klaus kinski': ['klaus kinski', 'kinski'], 'robert pattinson': ['robert pattinson', 'pattinson'], 'spike lee': ['spike lee', 'lee'], 'samuel l. jackson': ['samuel l. jackson', 'l. jackson'], 'peter dinklage': ['peter dinklage', 'dinklage'], 'jeremy irons': ['jeremy irons', 'irons'], 'debra messing': ['debra messing', 'messing'], 'arnold schwarzenegger': ['arnold schwarzenegger', 'schwarzenegger'], 'monica potter': ['monica potter', 'potter'], 'sylvester stallone': ['sylvester stallone', 'stallone'], 'michael haneke': ['michael haneke', 'haneke'], 'nathan fillion': ['nathan fillion', 'fillion'], 'glenn close': ['glenn close', 'close'], 'jack huston': ['jack huston', 'huston'], 'nina dobrev': ['nina dobrev', 'dobrev'], 'sacha baron cohen': ['sacha baron cohen', 'baron cohen'], 'tim burton': ['tim burton', 'burton'], 'adam sandler': ['adam sandler', 'sandler'], 'william h. macy': ['william h. macy', 'h. macy'], 'winona ryder': ['winona ryder', 'ryder'], 'liev schreiber': ['liev schreiber', 'schreiber'], 'will arnett': ['will arnett', 'arnett'], 'julia louis-dreyfus': ['julia louis-dreyfus', 'louis-dreyfus'], 'adam driver': ['adam driver', 'driver'], 'marina sirtis': ['marina sirtis', 'sirtis'], 'jamie farr': ['jamie farr', 'farr'], 'jason bateman': ['jason bateman', 'bateman'], 'aziz ansari': ['aziz ansari', 'ansari'], 'emily mortimer': ['emily mortimer', 'mortimer'], 'katharine mcphee': ['katharine mcphee', 'mcphee'], 'hulk hogan': ['hulk hogan', 'hogan'], 'katy perry': ['katy perry', 'perry'], 'joaquin phoenix': ['joaquin phoenix', 'phoenix'], 'paul thomas anderson': ['paul thomas anderson', 'thomas anderson'], 'josh brolin': ['josh brolin', 'brolin'], 'matt damon': ['matt damon', 'damon'], 'jimmy fallon': ['jimmy fallon', 'fallon'], 'chad lowe': ['chad lowe', 'lowe'], 'emily vancamp': ['emily vancamp', 'vancamp'], 'christian bale': ['christian bale', 'bale'], 'zosia mamet': ['zosia mamet', 'mamet'], 'kevin bacon': ['kevin bacon', 'bacon'], 'john waters': ['john waters', 'waters'], 'ryan gosling': ['ryan gosling', 'gosling'], 'aaron tveit': ['aaron tveit', 'tveit'], 'samantha barks': ['samantha barks', 'barks'], 'gerard butler': ['gerard butler', 'butler'], 'jim carrey': ['jim carrey', 'carrey'], 'bea arthur': ['bea arthur', 'arthur'], 'rachel weisz': ['rachel weisz', 'weisz'], 'bryce dallas howard': ['bryce dallas howard', 'dallas howard'], 'betty white': ['betty white', 'white'], 'guillermo del toro': ['guillermo del toro', 'del toro'], 'john hawkes': ['john hawkes', 'hawkes'], 'victor garber': ['victor garber', 'garber'], 'vin diesel': ['vin diesel', 'diesel'], 'garrett hedlund': ['garrett hedlund', 'hedlund'], 'mark harmon': ['mark harmon', 'harmon'], 'frank sinatra': ['frank sinatra', 'sinatra'], 'dean martin': ['dean martin', 'martin'], 'seth macfarlane': ['seth macfarlane', 'macfarlane'], 'ralph fiennes': ['ralph fiennes', 'fiennes'], 'rob lowe': ['rob lowe', 'lowe'], 'jason isaacs': ['jason isaacs', 'isaacs'], 'hugh dancy': ['hugh dancy', 'dancy'], 'danny mcbride': ['danny mcbride', 'mcbride'], 'olivier martinez': ['olivier martinez', 'martinez']}
'''
the_awards = ['Best Drama', 'Best Screenplay', 'Best Director', 'tv Actress', 'Best Foreign Language Film', 'foreign', 'Supporting Actor', 'Supporting Actress', 'Comedy or Musical', 'comedy', 'Best Comedy', "Best Actress in a Comedy or Musical", "Actress in a Motion Picture", 'miniseries', 'original score', 'best actress in a tv drama', 'actress in a motion picture - drama', 'cecil b. demille award', 'actor in a musical/comedy', 'supporting actor in a series', 'supporting actor in a miniseries']
'''
duplicates = []
def duplicate_lastnames():
    duplicates = []
    lastnamedict = {}
    for person in persondict:
        splitname = person.split()
        lastname = splitname[-1]
        if lastname in lastnamedict:
            duplicates.append(lastname)

def find_name_or_movie(input):
    input = input.lower()
    for element in data:
            tweet = (element['text'])
            tweet = tweet.lower()
            if tweet.__contains__(input):
                print(tweet)


def compare_winners(votedict, vec):
    winner = ""
    curmax = 0
    for element in votedict:
        if votedict[element]>curmax:
            curmax = votedict[element]
            winner = element
    for element in data:
        tweet = element['text']
        if tweet.split()[0] == 'RT':
            continue
        tweet = tweet.lower()
        if tweet.__contains__(winner):
            if tweet.__contains__("won") or tweet.__contains__("stole") or tweet.__contains__("beat") or tweet.__contains__("lost") or tweet.__contains__("wins") or tweet.__contains__("loses") or tweet.__contains__("should"):
                for item in vec:
                    if tweet.__contains__(item):
                        if item in votedict:
                            votedict[item]+=1
                        else:
                            votedict[item] = 1
    return votedict

keywords = ['supporting', 'actor', 'drama', 'motion', 'picture', 'actress', 'tv', 'series', 'miniseries', 'movie', 'original', 'song', 'comedy', 'musical', 'show', 'screenplay', 'animated', 'feature', 'film', 'director']

def checkplus(some_award, a_tweet):
    for part in some_award:
        if not a_tweet.__contains__(part):
            return False
    return True

winnerMap = {}
def get_nominees(awards, movielist, tvshows):
    #award = award.lower()
    dupes = duplicate_lastnames()
    vote_dict = {}
    for element in data:
        tweet = (element['text'])
        tweet = tweet.lower()
        counter=0
        #if tweet[0]=="r" and tweet[1]=="t":
            #counter+=1
        for award in awards:
            counter+=1
            if counter == len(awards):
                if checkplus(award, tweet) == True:
                    for person in persondict:
                        namelist = persondict[person]
                        if tweet.__contains__(namelist[0]):# or tweet.__contains__(namelist[1]):
                            if person in vote_dict:
                                vote_dict[person]+=1
                            else:
                                vote_dict[person]=1
                        elif tweet.__contains__(namelist[1]) and namelist[1] not in dupes:# or tweet.__contains__(namelist[1]):
                            if person in vote_dict:
                                vote_dict[person]+=1
                            else:
                                vote_dict[person]=1
                    for movie in movielist:
                        movie = movie.lower()
                        if tweet.__contains__(movie):
                            if movie in vote_dict:
                                vote_dict[movie]+=1
                            else:
                                vote_dict[movie]=1
                    for show in tvshows:
                        if tweet.__contains__(show):
                            if show in vote_dict:
                                vote_dict[show]+=1
                            else:
                                vote_dict[show]=1
                else:
                    pass
                #award = award.lower()
                #print(award)
            elif tweet.__contains__(award):
                for person in persondict:
                    namelist = persondict[person]
                    if tweet.__contains__(namelist[0]):# or tweet.__contains__(namelist[1]):
                        if person in vote_dict:
                            vote_dict[person]+=1
                        else:
                            vote_dict[person]=1
                    elif tweet.__contains__(namelist[1]) and namelist[1] not in dupes:# or tweet.__contains__(namelist[1]):
                        if person in vote_dict:
                            vote_dict[person]+=1
                        else:
                            vote_dict[person]=1
                for movie in movielist:
                    movie = movie.lower()
                    if tweet.__contains__(movie):
                        if movie in vote_dict:
                            vote_dict[movie]+=1
                        else:
                            vote_dict[movie]=1
                for show in tvshows:
                    if tweet.__contains__(show):
                        if show in vote_dict:
                            vote_dict[show]+=1
                        else:
                            vote_dict[show]=1
                break
    the_vec = []
    if award[0].__contains__("actor") or award[0].__contains__("actress") or award[0].__contains__("director") or award[0].__contains__("cecil"):
        #print(award[0])
        #print("HEREEE1")
        the_vec = persondict
    elif award[0].__contains__("series"):
        #print(award[0])
        #print("HEREEE2")
        the_vec = the_shows
    else:
        #print(award[0])
        #print("HEREEE3")
        the_vec = the_movies
    vote_dict = compare_winners(vote_dict, the_vec)
    first = 0
    second = 0
    third = 0
    fourth = 0
    fifth = 0

    nomone = 'a'
    nomtwo = 'b'
    nomthree = 'c'
    nomfour = 'd'
    nomfive = 'e'
    for index in vote_dict:
        if vote_dict[index]>first and index in the_vec:
            fifth = fourth
            fourth = third
            third = second
            second = first
            first = vote_dict[index]
            nomfive = nomfour
            nomfour = nomthree
            nomthree = nomtwo
            nomtwo = nomone
            nomone = index
        elif vote_dict[index]>second and index in the_vec:
            fifth = fourth
            fourth = third
            third = second
            second = vote_dict[index]
            nomfive = nomfour
            nomfour = nomthree
            nomthree = nomtwo
            nomtwo = index
        elif vote_dict[index]>third and index in the_vec:
            fifth = fourth
            fourth = third
            third = vote_dict[index]
            nomfive = nomfour
            nomfour = nomthree
            nomthree = index
        elif vote_dict[index]>fourth and index in the_vec:
            fifth = fourth
            fourth = vote_dict[index]
            nomfive = nomfour
            nomfour = index
        elif vote_dict[index]>fifth and index in the_vec:
            fifth = vote_dict[index]
            nomfive = index
    nominees = [nomone, nomtwo, nomthree, nomfour, nomfive]
    if nomfive == 'e':
        nominees.remove(nomfive)
    if nomfour == 'd':
        nominees.remove(nomfour)
    if nomthree == 'c':
        nominees.remove(nomthree)
    if nomtwo == 'b':
        nominees.remove(nomtwo)
    if nomone == 'a':
        nominees.remove(nomone)
    winnerMap[awards[0]] = nomone
    #print(awards[0])
    #print(nominees)
    #print(vote_dict)
    return nominees

def duplicate_lastnames():
    duplicates = []
    lastnamedict = {}
    for person in persondict:
        splitname = person.split()
        lastname = splitname[-1]
        if lastname in lastnamedict:
            duplicates.append(lastname)
    return duplicates

def host_array():
    tweetarr = []
    keywords = ['hosted']
    for element in data:
        tweet = element['text']
        for keyword in keywords:
            if tweet.__contains__(keyword):
                if not tweet.__contains__("should"):
                    tweetarr.append(tweet)
                    break
    return tweetarr

def get_hosts():
    host_arr = host_array()
    hdict = defaultdict(int)
    for t in host_arr:
        doc = nlp(t)
        for e in doc.ents:
            if e.label_ == 'PERSON':
                hdict[e.text] += 1
    host = []
    for k,v in hdict.items():
        if v > 50 and len(k.split()) > 1:
            host.append(k)
    return host

def checkplus_end(some_award, a_tweet):
    for part in some_award[len(some_award) - 1]:
        if not a_tweet.__contains__(part):
            return False
    return True

def get_keywords(data):
    new_awards = []
    #awards_list = rank_awards(data)
    for awards in array_awards:
        element = awards[0]
        if element.__contains__("/") or element.__contains__(",") or element.__contains__("-") or element.__contains__(":"):
            counter=0
            string = ""
            while counter<len(element):
                if element[counter] != "/" and element[counter] != "," and element[counter] != "-" and element[counter] != ":":
                    string+=element[counter]
                elif element[counter] == "," or element[counter]=="-" or element[counter]==":":
                    pass
                else:
                    string+=" "
                counter+=1
            element = string
        element = element.split()
        vector = []
        new_award_name = ""
        counter = 0
        for word in element:
            if word == "director":
                new_award_name = "director "
                break
            elif word=="screenplay":
                new_award_name = "screenplay "
                break
            elif word == "animated":
                new_award_name = "feature film "
                break
            elif word in keywords and not new_award_name.__contains__(word):
                new_award_name+=word
                new_award_name += " "
            counter+=1
        new_award_name = new_award_name[:-1]
        awards.append(new_award_name)
        new_awards.append(awards)
    return new_awards

def plus(data):
    my_awards = get_keywords(data)
    first = ""
    second = ""
    third = ""
    for element in my_awards:
        parsed = element[-1]
        parsed = parsed.split()
        counter=0
        for word in parsed:
            if counter<len(parsed)-1:
                if word=="actor" or word=="actress" or word=="screenplay" or word=="picture":
                    counter+=1
                    parsed.insert(counter, "plus")
                else:
                    counter+=1
        first = False
        second = False
        third = ""
        one = ""
        two = ""
        for word in parsed:
            if word=="plus":
                if first == True:
                    second = True
                first = True
            elif first==False:
                one+=word
                one+=" "
            elif first == True and second == False and word != "plus":
                two+=word
                two+=" "
            elif first==True and second==True:
                third+=word
                third+=" "
        parts = []
        if len(third)>1:
            one = one[:-1]
            two = two[:-1]
            third = third[:-1]
            parts = [one, two, third]
        elif len(two)>1:
            one = one[:-1]
            two = two[:-1]
            parts = [one, two]
        else:
            one = one[:-1]
            parts = [one]
        element[-1] = parts
    return my_awards

def get_presenters(awards):
    tweetarr = []
    presenterMap = defaultdict(int)
    for element in data:
        tweet = element['text'].lower()
        for aName in awards:
            if tweet.__contains__(aName):
                if tweet.__contains__("present"):
                    tweetarr.append(tweet)   
    print("presenter of ", award[0] ,":")
        #print(len(tweetarr))
    for t in tweetarr:
        twt = re.findall("^(.*?)present", t)
        if twt:
            pid = nlp(t)
            for e in pid.ents:
                if e.label_ == 'PERSON':
                    
                    presenterMap[e.text] += 1
    tweetarr = []
        #print(presenterMap)
    presTup = (" ",0)
    for (k,v) in presenterMap.items():
        if v > presTup[1]:
            presTup = (k,v)
    return presTup[0]


array_awards = [['best supporting actor in a drama','best supporting actor, drama'], ['best supporting actor, motion picture','best supporting actor in a motion picture'], ['best supporting actress tv series, miniseries, or tv movie'], ['best actress in a mini-series/tv movie','best actress in a mini-series, tv movie'], ['best actor for tv drama','best tv drama actor', 'best actor in tv drama'], ['best original song award'], ['best actor in a miniseries/tv movie','best tv movie or miniseries actor'], ['best actress in a motion picture comedy or musical','best actress motion picture comedy or musical'], ['best supporting actor in a tv show, miniseries or tv movie award'], ['best supporting actress in a motion picture','best supporting actress motion picture', 'best supporting actress for motion picture'], ['best screenplay in a motion picture','golden globe awards for best female', 'best motion picture screenplay', 'best screenplay, motion picture', 'best screenplay - motion picture', 'best screenplay for a motion picture', 'best motion picture, comedy/musical'], ['best actor tv series - comedy or musical'], ['best actress, tv drama','best tv drama actress', 'best actress in a tv drama', 'best drama tv actress'], ['best actress in a tv series, drama','best actress in a tv series - drama'], ['best animated feature film'], ['best actress in a tv comedy or musical','best actress in a tv comedy/musical'], ['best actress in a comedy or musical series','best actress in a motion picture for drama'], ['best director for motion picture','best director for a motion picture', 'best director of a motion picture', 'best director - motion picture'], ['best tv comedy/musical','best tan by an actress', 'best look of the night'], ['best actor in a motion picture comedy/musical','best original song category, the golden globe', 'best actor in a motion picture, comedy/musical'], ['best actor, comedy/musical','best actor in comedy/musical', 'best actor, musical or comedy', 'best actor in comedy or musical'], ['best actress in a motion picture drama','best actress for motion picture- drama', 'best actress, motion picture/drama', 'best actress for a motion picture drama'], ['best actor in a motion picture drama','best actor, motion picture drama', 'best actor in motion picture drama'], ['best motion picture drama','best motion picture - drama', 'best motion picture in drama'], ['best actor, drama: golden globe for film']]
#awards = plus()
'''
def combine_nominees(awards):
    returndict = {}
    for award in awards:
        get_nominees(award,the_movies,the_shows)
        nomarray = get_presenters(award)
        returndict[award[0]] = nomarray
    return returndict
'''

#print(build_json(data))
<<<<<<< HEAD
print(plus(data))
=======
print(plus(data))
>>>>>>> 510a8a024a526eab60a766464d645c104e88f0ab
