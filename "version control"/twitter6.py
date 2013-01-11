import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener, Stream
from tweepy.pstreaming import PStreamListener, PStream
from tweepy.ustreaming import UStreamListener, UStream
import sys
import string
import urllib
import math
from math import sqrt
import Queue
import time
import random

import threading
from threading import Thread

import multiprocessing
from multiprocessing import Process

from pyglet.gl import *

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

avgTime = 50
historyTime = 50

q1 = deque(maxlen=avgTime)
q2 = deque(maxlen=avgTime)

h1 = deque(maxlen=historyTime)
h2 = deque(maxlen=historyTime)

h1.append(0)
h2.append(0)

xList = []
yList = []

timeA = []
timeB = []

startTime = time.time()

queue = Queue.Queue()

userNames = []
userHandles = []
userIDs = []

publicKeyWords = ['the','be','to','of','and','are','is','were','was']

capslist = list(string.ascii_uppercase)

pFile = open('pList.txt','r').read()
nFile = open('nList.txt','r').read()

pList = pFile.split('\n')
nList = nFile.split('\n')

handle = " "
tweet = " "

window = pyglet.window.Window(1200,600)

start = False

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
        if lowerCaseWord == 'fucking' or 'fuckin' or 'very' or 'super':
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
    ### Andjust and cap it from -100 to 100 ###
    if finalMood > 0.0:
        finalMood = sqrt(20*finalMood)
        if finalMood > 100:
            finalMood = 100
    if finalMood < 0.0:
        finalMood = sqrt(20*abs(finalMood))
        if finalMood > 100:
            finalMood = 100
        finalMood = -finalMood
    return finalMood

class UStreamListener(UStreamListener):
    def on_status(self, status):
        try:
            if status.author.screen_name not in userNames:
                if status.author.screen_name != 'DMS_423':
                    mention = str(status.text).split(None, 1)
                    if mention[0] == '@DMS_423':
                        userNames.append(str(status.author.screen_name))
                        userIDs.append(str(uApi.get_user(str(status.author.screen_name)).id))
                        print status.author.screen_name, "has joined the game."
                        urllib.urlretrieve(str(uApi.get_user(str(status.author.screen_name)).profile_image_url), 'icons/'+str(status.author.screen_name)+'.jpg')
                        uStream()
                        try:
                            uApi.update_status("@"+str(status.author.screen_name)+" Thank you for joining Kevin's super awesome Twitter mood analyzer (it's the bees-knees).")
                        except Exception, e:
                            try:
                                uApi.update_status("@"+str(status.author.screen_name)+" Thank you for joining Kevin's super awesome Twitter mood analyzer (it's the cat's pajamas).")
                            except Exception, e:
                                try:
                                    uApi.update_status("@"+str(status.author.screen_name)+" Thank you for joining Kevin's super awesome Twitter mood analyzer (it's cool beans).")
                                except Exception, e:
                                    uApi.update_status("@"+str(status.author.screen_name)+" Thank you for joining Kevin's super awesome Twitter mood analyzer (it's super swell).")

            else:
                player(status.author.screen_name, status.text, status.id)

        except Exception, e:
            print >> sys.stderr, 'Encountered exception:', e
            pass

    def on_error(self, status):
        errorHandler(status)
        
class PStreamListener(PStreamListener):
    def on_status(self, status):
        global tweet
        global handle
        try:
            print status.text
            handle = status.author.screen_name
            tweet = status.text

        except Exception, e:
            print >> sys.stderr, 'Encountered exception:', e
            pass

    def on_error(self, status):
        print "Problem with the public stream listener."
        errorHandler(status)

def uStream():
    us = UStream(uAuth, UStreamListener())
    us.filter(follow = userIDs, track = ['@DMS_423'])

def pStream():
    ps = PStream(pAuth, PStreamListener())
    ps.filter(track = publicKeyWords)

def errorHandler(status):
    if status == 406:
        pass
    elif status == 420:
        print "\nUh-oh. Looks like we got a 420 error from Twitter. :<\n"

    else:
        print "\nWell, this is new. We've got a",status,"error... I don't know what that means, so let's fire up Google...\n"

def start1():
    t1 = Thread(target = uStream)
    t1.start()

def start2():
    t2 = Thread(target = pStream)
    t2.start()

def run():
    #start1()
    start2()

    pyglet.clock.schedule_interval(update,1/10.0)
    pyglet.app.run()
    
class PublicTweets:
    def __init__(self):
        self.tweetLabel = None
        self.userNameLabel = None
        
    def newTweet(self, name, text, mood):
        self.y = 300+(mood*2.8)
        self.x = random.randint(0, 1200)
        self.tweet = pyglet.text.Label(text,
                              font_name='Helvetica',
                              font_size=16, color=(255, 255, 255, 255),
                              x=self.x, y=self.y, anchor_x='center')

        self.userName = pyglet.text.Label("@"+name,
                              font_name='Helvetica',
                              font_size=10, color=(150, 150, 150, 255),
                              x=self.x, y=self.y-15, anchor_x='center')
        
        self.tweetLabel = self.tweet
        self.userNameLabel = self.userName
        
    def draw(self):
        if self.tweetLabel != None:
            self.tweetLabel.draw()
            self.userNameLabel.draw()

publicTweets = PublicTweets()

bg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 1200,0, 1200,800, 0,800]), ('c4f', [0.25,0.25,.4,0.1, 0.25,0.25,0.4,0.1, 0.1,0.1,0.25,0.1, 0.1,0.1,0.25,0.1]))

def background():
    startbg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 1200,0, 1200,800, 0,800]), ('c3f', [0.25,0.25,.4, 0.25,0.25,0.4, 0.1,0.1,0.25, 0.1,0.1,0.25]))
    startbg.draw(GL_POLYGON)

@window.event
def on_draw():
    global start
    if start == False:
        background()
        start = True
    else:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        bg.draw(GL_POLYGON)
        glDisable(GL_BLEND)

    publicTweets.draw()

def update(ThisFunctionAlwaysWantsAnArgument):
    text = tweet
    userHandle = handle
    tweetMood = mood(text)
    text.encode('ascii', 'ignore')
    publicTweets.newTweet(userHandle, text, tweetMood)


run()
