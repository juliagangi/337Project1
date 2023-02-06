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
    award_names = get_awards(data)
    bestdressed = best_dressed(data)
    worstdressed = worst_dressed(data)
    hosts = get_hosts()
    return_dict["hosts"] = hosts
    hosts = ', '.join(hosts)
    print('Host: '+hosts+'\n')
    movies = get_movies()[0]
    shows = get_movies()[1]
    people = get_people()
    for award in award_names:
        curr_dict = {}
        nominees = get_nominees(award,movies,shows,people)
        presenters = get_presenters(award)
        winner = nominees[0]
        curr_dict["nominees:"] = nominees
        curr_dict["presenters:"] = presenters
        curr_dict["winner:"] = winner
        award_dict[award[0]] = curr_dict
        this_award = award[0]
        nominees = ', '.join(nominees)
        print('Award: '+this_award+'')
        print('Nominees: '+nominees+'')
        print('Presenters: '+presenters+'')
        print('Winner: '+winner+'\n')
    return_dict["award data:"] = award_dict
    print('Best Dressed: '+bestdressed+'')
    print('Worst Dressed: '+worstdressed+'')
    print(return_dict)
    return return_dict

def get_awards(data):
    awards1 = find_awards(data)
    awards = rank_awards(awards1)
    keywords = the_keywords(awards)
    new_awards = get_keywords(awards,keywords)
    final_awards = plus(new_awards)
    return final_awards

def the_keywords(awards):
    keywords = []
    for award in awards:
        award = award[0]
        award = award.split()
        for word in award:
            if len(word)>3 and word not in keywords and word!="best":
                keywords.append(word)
    for word in keywords:
        if word.__contains__("-") or word.__contains__("/") or word.__contains__(",") or word.__contains__(":"):
            keywords.remove(word)
    return keywords


def get_keywords(the_awards,keywords):
    new_awards = []
    for awards in the_awards:
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
            elif word in keywords and not new_award_name.__contains__(word):
                new_award_name+=word
                new_award_name += " "
            counter+=1
        new_award_name = new_award_name[:-1]
        awards.append(new_award_name)
        new_awards.append(awards)
    return new_awards

def plus(awards):
    first = ""
    second = ""
    third = ""
    for element in awards:
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
    return awards

def checkplus(some_award, a_tweet):
    for part in some_award:
        if not a_tweet.__contains__(part):
            return False
    return True

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
    final_seen = {}
    for award in updated_seen: # remove awards that are now alternative names for other
        if updated_seen[award] != 0:
            final_seen[award] = [updated_seen[award][0],updated_seen[award][4]]
    most_frequent = {}
    i = 0
    for award in final_seen:
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

def get_min_in_list(list):
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
    relevant_actors = {}
    for element in data:
        tweet = element['text'].lower()
        #if tweet[0]=="r" and tweet[1] == "t":
        #    counter+=1
        if tweet.__contains__('nominated') or tweet.__contains__('nominee') or tweet.__contains__('actress') or tweet.__contains__('actor')  or tweet.__contains__('presenting') or tweet.__contains__('win') or tweet.__contains__('tonight') or tweet.__contains__('presenter'):
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
    relevant_movies = {}
    relevant_shows = {}
    for element in data:
        tweet = element['text'].lower()
        #if tweet[0]=="r" and tweet[1] == "t":
            #counter+=1
        if tweet.__contains__('nominated') or tweet.__contains__('nominee') or tweet.__contains__('movie') or tweet.__contains__('win') or tweet.__contains__('award') or tweet.__contains__('series') or tweet.__contains__('show'):
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

def duplicate_lastnames(persondict):
    duplicates = []
    lastnamedict = {}
    for person in persondict:
        splitname = person.split()
        lastname = splitname[-1]
        if lastname in lastnamedict:
            duplicates.append(lastname)
    return duplicates

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

winnerMap = {}
def get_nominees(awards, movielist, tvshows, persondict):
    dupes = duplicate_lastnames(persondict)
    vote_dict = {}
    for element in data:
        tweet = element['text']
        tweet = tweet.lower()
        counter=0
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
        the_vec = persondict
    elif award[0].__contains__("series"):
        the_vec = tvshows
    else:
        the_vec = movielist
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
    if 'a' in nominees:
        nominees.remove('a')
    if 'b' in nominees:
        nominees.remove('b')
    if 'c' in nominees:
        nominees.remove('c')
    if 'd' in nominees:
        nominees.remove('d')
    if 'e' in nominees:
        nominees.remove('e')
    winnerMap[awards[0]] = nomone
    return nominees

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

def get_presenters(award):
    tweetarr = []
    presenterMap = defaultdict(int)
    for element in data:
        tweet = element['text'].lower()
        if checkplus_end(award,tweet):
            if tweet.__contains__("present"):
                tweetarr.append(tweet)   
    for t in tweetarr:
        twt = re.findall("^(.*?)present", t)
        if twt:
            pid = nlp(t)
            for e in pid.ents:
                if e.label_ == 'PERSON':
                    
                    presenterMap[e.text] += 1
    tweetarr = []
    presTup = (" ",0)
    for (k,v) in presenterMap.items():
        if v > presTup[1]:
            presTup = (k,v)
    return presTup[0]

build_json(data)
