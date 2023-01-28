import json
import csv
import spacy
from spacy import displacy

#NER = spacy.load("en_core_web_sm")
#raw_text="The movie Silver Linings Playbook wins the best comedy"
#text1 = NER(raw_text)

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


with open('/Users/gilliangracey/Downloads/gg2013.json', 'r') as f:
    data = json.load(f)

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
#get_people()

#persondict = get_people()
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

def get_award_names():
    return

def get_movie_names():
    return

def nominees_given_awards(awardslist, movielist):
    for award in awardslist:
        award = award.lower()
        vote_dict = {}
        for element in data:
            tweet = (element['text'])
            tweet = tweet.lower()
            if tweet.__contains__(award):
                for person in persondict:
                    #nicknamelist = persondict[person]
                    #person = person.lower()
                    #for nickname in nicknamelist:
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
        print('The nominees for '+award+' are:')
        print(nomone)
        print(nomtwo)
        print(nomthree)
        print(nomfour)
        print(nomfive)
        print("    ")
        print('The winner of '+award+' is:')
        print(nomone)
        print("    ")
        print(vote_dict)
        print("    ")
        vote_dict = {}
    return


#nominees_given_awards(the_awards, the_movies)
#find_name_or_movie('jay leno')
#find_name_or_movie('philip seymour hoffman')
#find_name_or_movie('jay leno')337
