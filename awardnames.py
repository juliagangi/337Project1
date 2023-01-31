import json
import numpy as np
import spacy

nlp = spacy.load("en_core_web_sm")

with open('gg2013.json', 'r') as f:
    data = json.load(f)

def build_frame(ceremony):
    return_dict = {}
    award_dict = {}
    return_dict["hosts"] = get_hosts(ceremony)
    return_dict["award data"] = award_dict
    award_names = award_names(ceremony)
    for award in award_names:
        curr_dict = {}
        curr_dict["nominees"] = get_nominees(award,the_movies)
        curr_dict["winner"] = get_nominees(award,the_movies)[0]
        award_dict[award] = curr_dict
    award_dict["best dressed"] = best_dressed()
    award_dict["worst dressed"] = worst_dressed()
    return return_dict

def get_hosts():
    return

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
                    if nlp(lastword[len(lastword)-1])[0].pos_ == "PUNCT":
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
                if nlp(word1)[0].pos_ == 'NOUN':
                    nouns.append(word1)
                elif nlp(word1)[0].pos_ == 'ADJ':
                    adjs.append(word1) 
                elif nlp(word1)[0].pos_ == 'VERB':
                    verbs.append(word1)                   
                if nlp(word2[len(word2)-1])[0].pos_ == 'PUNCT':
                    word = word2[0:len(word2)-1]
                elif nlp(word2)[0].pos_ == 'NOUN':
                    nouns.append(word2)
                elif nlp(word2)[0].pos_ == 'ADJ':
                    adjs.append(word2)
                elif nlp(word2)[0].pos_ == 'VERB':
                    verbs.append(word2)
                continue              
            if nlp(word[len(word)-1])[0].pos_ == 'PUNCT': # cut off punc at end of word
                word = word[0:len(word)-1]
            if nlp(word)[0].pos_ == 'NOUN':
                nouns.append(word)
            elif nlp(word)[0].pos_ == 'ADJ':
                adjs.append(word)
            elif nlp(word)[0].pos_ == 'VERB':
                verbs.append(word)
        updated_seen[award] = [updated_seen[award],[nouns],[adjs],[verbs],[]]
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
                    elif len(award1) < len(award2): # check if an award is start of another 
                        if award2.__contains__(award1): # ONLY UPDATE FREQ or ADD AS ALT NAME?
                            if award2.index(award1) == 0:
                                if updated_seen[award1][0] > updated_seen[award2][0]:
                                    updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                                    updated_seen[award2] = 0
                                else:
                                    updated_seen[award2] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                                    updated_seen[award1] = 0
                    elif len(award2) < len(award1): # check if an award is start of another
                        if award1.__contains__(award2): # ONLY UPDATE FREQ or ADD AS ALT NAME?
                            if award1.index(award2) == 0:
                                if updated_seen[award1][0] > updated_seen[award2][0]:
                                    updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                                    updated_seen[award2] = 0
                                else:
                                    updated_seen[award2] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                                    updated_seen[award1] = 0
                    # check if nominees are same
                    elif sorted(get_nominees(award1,the_movies)) == sorted(get_nominees(award2,the_movies)):
                            if updated_seen[award1][0] > updated_seen[award2][0]:
                                updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                                updated_seen[award2] = 0
                            else:
                                updated_seen[award2] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                                updated_seen[award1] = 0
                    else: # check if nouns list is fully contained by other
                        sortednouns1 = sorted(' '.join(nouns1))
                        sortednouns2 = sorted(' '.join(nouns2))
                        if len(nouns1) < len(nouns2):
                            if sortednouns2.__contains__(sortednouns1):
                                if updated_seen[award1][0] > updated_seen[award2][0]:
                                    updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                                    updated_seen[award2] = 0
                                else:
                                    updated_seen[award2] = [updated_seen[award2][0]+updated_seen[award1][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                                    updated_seen[award1] = 0
                        elif len(nouns1) > len(nouns2):
                            if sortednouns1.__contains__(sortednouns2):
                                if updated_seen[award1][0] > updated_seen[award2][0]:
                                    updated_seen[award1] = [updated_seen[award1][0]+updated_seen[award2][0],updated_seen[award1][1],updated_seen[award1][2],updated_seen[award1][3],updated_seen[award1][4]+[award2]]
                                    updated_seen[award2] = 0
                                else:
                                    updated_seen[award2] = [updated_seen[award2][0]+updated_seen[award1][0],updated_seen[award2][1],updated_seen[award2][2],updated_seen[award2][3],updated_seen[award2][4]+[award1]]
                                    updated_seen[award1] = 0
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

actordict = {}
with open('actors.csv') as csv_file:
    actordict = {}
    counter=0
    for row in csv_file:
        index = 0
        if counter==0:
            counter+=1
        else:
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
            actordict[name] = last

def get_people():
    relevant_tweets = []
    relevant_actors = {}
    for element in data:
        tweet = element['text'].lower()
        if tweet.__contains__('nominated') or tweet.__contains__('nominee') or tweet.__contains__('actress') or tweet.__contains__('actor') or tweet.__contains__('presenter') or tweet.__contains__('presenting') or tweet.__contains__('win') or tweet.__contains__('tonight'):# or tweet.__contains__('beat') or tweet.__contains__('nominated') or tweet.__contains__('host') or tweet.__contains__('presented') or tweet.__contains__('presenting') or tweet.__contains__('presents') or tweet.__contains__('nominee'):
            relevant_tweets.append(tweet)
    for tweet in relevant_tweets:
        for actor in actordict:
            last = actordict[actor].lower()
            lastvec = [actor, last]
            actor = actor.lower()
            if tweet.__contains__(actor) and actor not in relevant_actors:
                if actor.__contains__("-"):
                    name = ""
                    counter=0
                    while counter<len(actor):
                        if actor[counter]=="-":
                            name+=" "
                        else:
                            name+=actor[counter]
                        counter+=1
                    lastvec.append(name)
                relevant_actors[actor] = lastvec
    print(relevant_actors)
    return relevant_actors

the_awards = ['Best Drama', 'Best Screenplay', 'Best Director', 'tv Actress', 'Best Foreign Language Film', 'foreign', 'Supporting Actor', 'Supporting Actress', 'Comedy or Musical', 'comedy', 'Best Comedy', "Best Actress in a Comedy or Musical", "Actress in a Motion Picture", 'miniseries', 'original score', 'best actress in a tv drama', 'actress in a motion picture - drama', 'cecil b. demille award', 'actor in a musical/comedy', 'supporting actor in a series', 'supporting actor in a miniseries']
persondict = ['kerry washington', 'rachel weisz', 'helen mirren', 'taylor swift', 'anjelica huston', 'leonardo dicaprio', 'leon', 'julianne moore', 'jessica chastain', 'damian lewis', 'sarah hyland', 'ariel winter', 'cher', 'kevin costner', 'jennifer lopez', 'anne hathaway', 'bradley cooper', 'hugh jackman', 'denzel washington', 'kate hudson', 'eric stonestreet', 'jennifer lawrence', 'louis c.k.', 'zooey deschanel', 'ewan mcgregor', 'ben affleck', 'robert pattinson', 'sofia vergara', 'tina fey', 'amy poehler', 'claire danes', 'bill murray', 'priscilla presley', 'lucy liu', 'jessica alba', 'julianne hough', 'eva longoria', 'sally field', 'andrew lincoln', 'jay leno', 'kathryn bigelow', 'halle berry', 'jessica lange', 'lucille ball', 'helen hunt', 'stephen amell', 'linda gray', 'laura linney', 'dustin hoffman', 'emily deschanel', 'francesca eastwood', 'vanity', 'nicole kidman', 'jim parsons', 'megan fox', 'mel gibson', 'stacy keibler', 'naomi watts', 'robert downey jr.', 'julianna margulies', 'michelle dockery', 'george clooney', 'ricky gervais', 'olivia munn', 'lena dunham', 'david faustino', 'james cameron', 'kristen bell', 'dax shepard', 'amy adams', 'richard gere', 'emily blunt', 'meryl streep', 'ang lee', 'larry david', 'mandy patinkin', 'daniel day-lewis', 'mayim bialik', 'quentin tarantino', 'lea michele', 'alan arkin', 'tommy lee jones', 'christoph waltz', 'daniel craig', 'will arnett', 'benedict cumberbatch', 'connie britton', 'hayden panettiere', 'philip seymour hoffman', 'dennis quaid', 'maggie smith', 'sarah paulson', 'christina hendricks', 'mariska hargitay', 'christopher meloni', 'jared leto', 'gary oldman', 'jamie foxx', 'amanda seyfried', 'ed harris', 'kim kardashian', 'don cheadle', 'dmx', 'clint eastwood', 'woody harrelson', 'tom ford', 'danny strong', 'sia', 'allison williams', 'sigourney weaver', 'frances fisher', 'toby jones', 'sienna miller', 'jack black', 'elizabeth taylor', 'anna nicole smith', 'marion cotillard', 'drake', 'julia roberts', 'catherine zeta-jones', 'divine', 'jodie foster', 'bette davis', 'alec baldwin', 'matt leblanc', 'russell crowe', 'justin timberlake', 'rosario dawson', 'michael j. fox', 'christopher lloyd', 'judi dench', 'paul rudd', 'salma hayek', 'bryan cranston', 'steve buscemi', 'jennifer garner', 'jeff daniels', 'jon hamm', 'isla fisher', 'dev patel', 'hugh laurie', 'joaquin phoenix', 'harrison ford', 'michael c. hall', 'jeremy renner', 'david duchovny', 'lindsay lohan', 'jamie kennedy', 'common', 'vanessa hudgens', 'selena gomez', 'aaron sorkin', 'kate winslet', 'tim burton', 'harvey weinstein', 'diego klattenhoff', 'eddie redmayne', 'pauly shore', 'john goodman', 'sacha baron cohen', 'jason statham', 'john williams', 'joseph gordon-levitt', 'b.j. novak', 'nolan gould', 'rico rodriguez', 'christopher walken', 'madonna', 'paul f. tompkins', 'morena baccarin', 'iman', 'justin bieber', 'harry styles', 'roger moore', 'david hyde pierce', 'johnny depp', 'jeremy irons', 'whitney houston', 'audrey hepburn', 'chris rock', 'kiefer sutherland', 'steven spielberg', 'will ferrell', 'kristen wiig', 'heidi klum', 'eva mendes', 'archie panjabi', 'michael caine', 'haley joel osment', 'fred armisen', 'chris tucker', 'lenny kravitz', 'retta', 'beyonce', 'katharine mcphee', 'max greenfield', 'piper laurie', 'jimmy fallon', 'john krasinski', 'oprah winfrey', 'mr. t', 'melanie griffith', 'faye dunaway', 'demi moore', 'jonah hill', 'liza minnelli', 'helena bonham carter', 'morgan freeman', 'klaus kinski', 'jessica biel', 'spike lee', 'samuel l. jackson', 'danny huston', 'djimon hounsou', 'peter dinklage', 'ryan gosling', 'rza', 'debra messing', 'arnold schwarzenegger', 'gwyneth paltrow', 'monica potter', 'sylvester stallone', 'michael haneke', 'nathan fillion', 'hulk hogan', 'glenn close', 'jack huston', 'kevin bacon', 'nina dobrev', 'sandra oh', 'adam sandler', 'william h. macy', 'winona ryder', 'liev schreiber', 'jason bateman', 'julia louis-dreyfus', 'zosia mamet', 'adam driver', 'marina sirtis', 'matt ryan', 'jamie farr', 'aziz ansari', 'emily mortimer', 'elton john', 'david spade', 'michael dorn', 'brent spiner', 'katy perry', 'hugh dancy', 'johnny galecki', 'paul thomas anderson', 'orson welles', 'josh brolin', 'matt damon', 'rebel wilson', 'chad lowe', 'victor garber', 'emily vancamp', 'christian bale', 'john waters', 'aaron tveit', 'samantha barks', 'gerard butler', 'jim carrey', 'bea arthur', 'tim allen', 'lena olin', 'bryce dallas howard', 'alfred hitchcock', 'betty white', 'logan lerman', 'bruce lee', 'guillermo del toro', 'tina louise', 'john hawkes', 'margo', 'kristen stewart', 'woody allen', 'vin diesel', 'garrett hedlund', 'rihanna', 'tyler perry', 'mark harmon', 'frank sinatra', 'dean martin', 'seth macfarlane', 'ralph fiennes', 'rob lowe', 'deborra-lee furness', 'jason isaacs', 'sabu', 'danny mcbride', 'olivier martinez']
persondict.remove("leon")
persondict.remove("sia")
persondict.remove("vanity")
the_movies = ['argo', 'legally blonde', 'les miserables', 'salmon fishing in the yemen', 'best exotic marigold hotel', 'moonrise kingdom', 'salmon fishing in the yemen', 'silver linings playbook', 'ghostbusters', 'django unchained', 'divergent', 'life of pi', 'moana', 'james bond', 'avatar', 'lincoln', 'zero dark thirty', 'zero dark 30' 'salmon fishing', 'the intouchables', 'rust and bone', 'amour', 'a royal affair', "the girl", "hatfields and mccoys", "the hour", "political animals", "game change", "argo", "anna karenina", "cloud atlas", "lincoln", "life of pi"]

def find_name_or_movie(input):
    input = input.lower()
    for element in data:
            tweet = (element['text'])
            tweet = tweet.lower()
            if tweet.__contains__(input):
                print(tweet)

def get_nominees(award, movielist):
    award = award.lower()
    vote_dict = {}
    for element in data:
        tweet = (element['text'])
        tweet = tweet.lower()
        if tweet.__contains__(award):
            for person in persondict:
                if tweet.__contains__(person):
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
    num_movies = 0
    num_people = 0
    the_vec = []
    if award.__contains__("actor") or award.__contains__("actress") or award.__contains__("director") or award.__contains__("cecil"):
        the_vec = persondict
    else:
        the_vec = the_movies
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
    return nominees


def pos():
    string1 = "affair"
    print(nlp(string1)[0].pos_)
    string2 = "supporting"
    print(nlp(string2)[0].pos_)    

#pos()


def test():
    award1 = 'best supporting actor, motion picture'
    award2 = 'best supporting actor, drama'
    nom1 = sorted(get_nominees(award1,the_movies))
    nom2 = get_nominees(award2,the_movies)
    '''
    print(nom1)
    print(nom2)
    award1 = 'best actor, comedy/musical'
    award2 = 'best actor in a motion picture comedy/musical'
    print(get_nominees(award1,the_movies))
    print(get_nominees(award2,the_movies))
    '''



#test()

get_awards()