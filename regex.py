import re

reg_ex = []

def matching(reg_ex):
    for expr in reg_ex:
        pattern = re.compile(expr, re.IGNORECASE)
        for tweet in tweets:
            matches = pattern.match(tweet)
            pattern.findall() #takes string w commas separating items
                # returns parts of items that match pattern


'''
index tweet database w "host" & other variations
find index of where name would be (2 words before)
-- make sure "don't" isn't before
apply voting system (for a given tweet, take prev 2 and 3 words (movie title) & put in a set)
each tweet has 1 set, award maps to array of sets, find intersections in sets to figure out correct movie/winner name
how to figure out that best television comedy = best tv comedy
- take increasing # of words starting from "best"

notes -- 
- look for punctuation to stop search?
- start with 'best'?
- how to avoid 'best' being the most frequent?
- stop at # or http?
- filter for length ? (must be > 1)

don't need type/relationship constraints or regular expressions

return as :
{"hosts": [...,...], "award data": {"award_name": {"nominated": [...,...], "winner": [...]}, "award_name": {...}}}
winners:
/.* (<artist_name>) (wins | won) (<award_name>)
/.* (<artist_name>) [^should've] won (<award_name>)
/.* (<artist_name>) [^didn't] win (<award_name>)
/.* (<award_name>) goes to (<artist_name>)

/1 = artist_name
/2 = award_name

nominees:
/.* (<artist_name>) .+ [^(wasn't | should've been)] (nominated | up) for (<award_name>)
    add (was | has been) or (was | has) [^not] (been)?
/1 = artist_name
/2 = award_name

award names:
/Best genre (Film | Movie)
/Best (Female | Male) role
/Best (<x>).* role
    - so TV = Television
/.* Best ([A-Z]([a-z])*)+ .*
    - Best followed by at least 1 capitalized word
/.* Best ([A-Z]([a-z]*))+ for a ([A-Z]([a-z]*))
    - if genre is at end 

for variables (artist/award name):
[a-zA-Z] or other way to put constraints on artist_name
using type constraints after applying regex?
how to store in variable

type constraints:
artist_name:
- must contain only letters
- must be an artist (or match a nickname)
- must be in list of nominees for that award

award_name:
- must contain only letters
- must start with Best or Most (use type expr)
'''

