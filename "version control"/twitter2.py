import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener, Stream
from tweepy.pstreaming import PStreamListener, PStream
from tweepy.ustreaming import UStreamListener, UStream
import sys
import string
import urllib

import threading
from threading import Thread

from collections import deque

uConsumer_key="jmdtPOSRvAItfRnxsVU69w"
uConsumer_secret="7UzM3gbFU6br8sMNOoAC9AWHDjeykO6PQs37zR2F6Y"

uAccess_token="916121143-HxJ69tssZRG8sFi54rm7yioAV9P71XBktV2pRqpb"
uAccess_token_secret="1uEN6EPwmS71XmJFUVj99lnTQnDKlynQJpcUBlItA"

uAuth = OAuthHandler(uConsumer_key, uConsumer_secret)
uAuth.set_access_token(uAccess_token, uAccess_token_secret)

uApi = tweepy.API(uAuth)

pConsumer_key="c8zgKBZ00DlIEAQnIZPkNw"
pConsumer_secret="v8Amc7rXUuwKFyrC4IkKGV3r6BVBJb7Uxr2HbfbVj4"

pAccess_token="916121143-dQPrqbRZ3HMMflRzX0zWZKw7XdRbvazyds6qYjhV"
pAccess_token_secret="XLgHFQ5pTqxubICM5bQ0cCFzV0wreQ8PnL49Mjd6Wrk"

pAuth = OAuthHandler(pConsumer_key, pConsumer_secret)
pAuth.set_access_token(pAccess_token, pAccess_token_secret)

pApi = tweepy.API(pAuth)

aConsumer_key="Q9CNjqIZ6wKTxuXoDnHQ"
aConsumer_secret="7clj7nmf31m8KYoO80sKAXeIE3HWAL73Z7rwaf5sGE"

aAccess_token="916121143-kgfMmK6vhJJgzbNNy3WsvY9f3AYkdjAkfZZUzZNu"
aAccess_token_secret="zTcXkBDiKPC6jE2PGEkSHkzVWIIyv3EsDhgjx1B9JU"

aAuth = OAuthHandler(aConsumer_key, aConsumer_secret)
aAuth.set_access_token(aAccess_token, aAccess_token_secret)

aApi = tweepy.API(aAuth)

avgtime = 50
q = deque(maxlen=avgtime)

userNames = []
userHandles = []
userIDs = []

accountID = [aApi.get_user('@DMS_423').id]

publicKeyWords = ['the','be','to','of','and','are','is','were','was']

hurricane = ['hurricane', '#sandy']

capslist = list(string.ascii_uppercase)

pFile = open('pList.txt','r').read()
nFile = open('nList.txt','r').read()

pList = pFile.split('\n')
nList = nFile.split('\n')

def mood(text):
    overallMood = 0
    length = 0
    caps = 2
    exclamations = text.count('!')
    strippedText = text.strip('.?~#-!,')
    words = strippedText.split()
    for word in words:
        wordcaps = 0
        lowerCaseWord = word.lower()
        if lowerCaseWord in pList:
            overallMood = overallMood+1
        if lowerCaseWord in nList:
            overallMood = overallMood-1
        if lowerCaseWord == 'fucking' or 'fuckin':
            exclamations = exclamations+1
        for letter in list(word):
            if letter in capslist:
                wordcaps = wordcaps+1
        if wordcaps > 3:
            caps = caps + wordcaps
    if exclamations == 0:
        exclamations = 1
    elif exclamations == 1:
        exclamations = 2
    elif exclamations == 2:
        exclamations = 2.5
    elif exclamations == 3:
        exclamations = 3
    elif exclamations == 4:
        exclamations = 3.25
    else:
        exclamations = 3.5
    if overallMood != 0:
        length = (1+(((len(text)*1.25)/10)/12))
    finalMood = ((((overallMood * 3) * (length)) * (exclamations)) * (1+(abs(overallMood/2))) * (caps/2))
    return finalMood

def publicEnemy(name, text):
    randomMood = mood(text)
##    if randomMood != 0.0:
    q.append(randomMood)
    avg = sum(q)/len(q)
    print avg

def player(name, text):
    playerMood = mood(text)
    print name
    print text
    print playerMood

class UStreamListener(UStreamListener):
    def on_status(self, status):
        print "Got a user tweet."
        try:
            player(status.author.screen_name, status.text)
            print userNames
            print userIDs

        except Exception, e:
            print >> sys.stderr, 'Encountered exception:', e
            pass

    def on_error(self, status):
        errorHandler(status)

class AStreamListener(StreamListener):
    def on_status(self, status):
        print "Got an add request."
        try:
            if status.author.screen_name not in userNames:
                userNames.append(str(status.author.screen_name))
                userIDs.append(str(aApi.get_user(str(status.author.screen_name)).id))
                #userHandles.append('@'+str(aApi.get_user(str(status.author.screen_name)).id))
                print status.author.screen_name, "has joined the game."
                urllib.urlretrieve(str(aApi.get_user(str(status.author.screen_name)).profile_image_url), 'icons/'+str(status.author.screen_name)+'.jpg')
                startU()

        except Exception, e:
            print >> sys.stderr, 'Encountered exception:', e
            pass

    def on_error(self, status):
        print "Problem with the add stream listener."
        errorHandler(status)

class PStreamListener(PStreamListener):
    def on_status(self, status):
        try:
            publicEnemy(status.author.screen_name, status.text)

        except Exception, e:
            print >> sys.stderr, 'Encountered exception:', e
            pass

    def on_error(self, status):
        print "Problem with the public stream listener."
        errorHandler(status)

def uStream():
    s = UStream(uAuth, UStreamListener())
    s.filter(follow = userIDs)

def pStream():
    ps = PStream(pAuth, PStreamListener())
    ps.filter(track = publicKeyWords)

def aStream():
    adds = Stream(aAuth, AStreamListener())
    adds.filter(follow = accountID, track = ['@DMS_423'])

def errorHandler(status):
    if status == 406:
        pass
    elif status == 420:
        print "Uh-oh. Looks like we got a 420 error from Twitter. :<"

    else:
        print "Well, this is new. We've got a",status,"error... I don't know what that means, so let's fire up Google..."

def startP():
    t3 = Thread(target = pStream)
    t3.start()

def startA():
    t1 = Thread(target = aStream)
    t1.start()

def startU():
    t2 = Thread(target = uStream)
    t2.start()

def run():
    startP()
    startA()
    startU()

run()
