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
    #print(tweetarr)
    return tweetarr

def winner_given_noms_and_award(noms, award):
    nom_dict = {}
    for eachnom in noms:
        nom_dict[eachnom] = 0
    tweetarr = []
    keywords = ['wins', 'won']
    for element in data:
        tweet = element['text']
        if tweet.__contains__(award):
            tweetarr.append(tweet)
    for twit in tweetarr:
        for nom in noms:
            if twit.__contains__(nom):
                nom_dict[nom]+=1
    #print(nom_dict)
    currmax = 0
    maxnom = noms[0]
    for nom in nom_dict:
        if nom_dict[nom] > currmax:
            currmax = nom_dict[nom]
            maxnom = nom
    print(maxnom)
    return maxnom

print("winner should be Les Mis")
winner_given_noms_and_award(['Salmon Fishing in the Yemen', 'Silver Linings Playbook', 'Moonrise Kingdom', 'Best Exotic Marigold Hotel', 'Les Miserables'], "Best Picture")
print("winner should be Argo")
winner_given_noms_and_award(['Life of Pi', 'Argo', 'Lincoln', 'Django Unchained', 'Zero Dark Thirty'], "Best Picture")
print("winner should be Jessica Chastain")
winner_given_noms_and_award(['Rachel Weisz', 'Naomi Watts', 'Jessica Chastain', 'Marion Cotillard', 'Helen Mirren'], "Best Actress")
print("winner should be Daniel Day-Lewis")
winner_given_noms_and_award(['Richard Gere', 'Daniel Day-Lewis', 'Joaquin Phoenix', 'Denzel Washington', 'John Hawkes'], "Best Actor")