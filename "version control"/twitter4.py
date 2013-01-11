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

hurricane = ['hurricane', '#sandy']

term1list = []
term2list = []

capslist = list(string.ascii_uppercase)

pFile = open('pList.txt','r').read()
nFile = open('nList.txt','r').read()

pList = pFile.split('\n')
nList = nFile.split('\n')

window1 = pyglet.window.Window(1200,600)
##window2 = pyglet.window.Window(800,600)

##window1.setvisible(visible=False)
##window2.setvisible(visible=False)

avg1 = 0
avg2 = 0


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

def publicEnemy1(name, text):
    global avg1
    randomMood = mood(text)
##    if randomMood != 0.0:
    q1.append(randomMood)
    avg1 = sum(q1)/len(q1)
    print 'Bar 1 %.3f' % avg1
    #h1.appendleft(avg)

    lineGraphA.newPoint(avg1*6)



def publicEnemy2(name, text):
    global avg2
    randomMood = mood(text)
##    if randomMood != 0.0:
    q2.append(randomMood)
    avg2 = sum(q2)/len(q2)
    print 'Bar 2 %.3f' % avg2
    #h2.appendleft(avg)

    lineGraphB.newPoint(avg2*6)


class PStreamListener1(UStreamListener):
    def on_status(self, status):
        try:
            publicEnemy1(status.author.screen_name, status.text)

        except Exception, e:
            print >> sys.stderr, 'Encountered exception:', e
            pass
        
class PStreamListener2(PStreamListener):
    def on_status(self, status):
        try:
            publicEnemy2(status.author.screen_name, status.text)

        except Exception, e:
            print >> sys.stderr, 'Encountered exception:', e
            pass

    def on_error(self, status):
        print "Problem with the public stream listener."
        errorHandler(status)

def pStream1():
    us = UStream(uAuth, PStreamListener1())
    us.filter(track = term1list)

def pStream2():
    ps = PStream(pAuth, PStreamListener2())
    ps.filter(track = term2list)

def errorHandler(status):
    if status == 406:
        pass
    elif status == 420:
        print "\nUh-oh. Looks like we got a 420 error from Twitter. :<\n"

    else:
        print "\nWell, this is new. We've got a",status,"error... I don't know what that means, so let's fire up Google...\n"

def start1():
    t1 = Thread(target = pStream1)
    t1.start()

def start2():
    t2 = Thread(target = pStream2)
    t2.start()

def run():
    global term1list
    global term2list

    term1 = raw_input("Please enter the first term: ")
    term2 = raw_input("Please enter the second term: ")

    term1list.append(term1)
    term2list.append(term2)

##    window1.setvisible(visible=True)
##    window2.setvisible(visible=True)

    start1()
    start2()

    pyglet.clock.schedule_interval(update,1/60.0)
    pyglet.app.run()

def bar1():
    height = avg1*6+100
    bar = pyglet.graphics.vertex_list(4, ('v2f', [1000,100, 1050,100, 1050,height, 1000,height]), ('c3f', [.25,0,0, .25,0,0, 1,0,0, 1,0,0]))

    label = pyglet.text.Label(term1list[0],
                          font_name='Helvetica',
                          font_size=16, bold=True, color=(0, 0, 0, 255),
                          x=1050, y=height+25, anchor_x='right')

    bar.draw(GL_POLYGON)
    label.draw()

def bar2():
    height = avg2*6+100
    bar = pyglet.graphics.vertex_list(4, ('v2f', [1075,100, 1125,100, 1125,height, 1075,height]), ('c3f', [0,0,.25, 0,0,.25, 0,0,1, 0,0,1]))

    label = pyglet.text.Label(term2list[0],
                          font_name='Helvetica',
                          font_size=16, bold=True, color=(0, 0, 0, 255),
                          x=1075, y=height+25, anchor_x='left')

    bar.draw(GL_POLYGON)
    label.draw()

def blackLine(x1,y1,x2,y2,w):
    line = pyglet.graphics.vertex_list(4, ('v2f', [x1-w,y1-w, x2+w,y1-w, x2+w,y2+w, x1-w,y2+w]), ('c3f', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    line.draw(GL_POLYGON)

class LineGraphA:
    def __init__(self):
        self.currentPoint = (0,0)
        self.previousPoint = (0,0)
        self.lineList = []
        self.startTime = int(time.time())
        self.location = 1000
        self.elapsed = 0
        self.y = 100
        self.previousY = 100
        self.rate = 1

    def newPoint(self, y):
        self.previousY = self.y
        self.y = int(y)+100
        self.previousPoint = (self.location-self.elapsed,self.previousY)
        self.currentPoint = (self.location, self.y)
        
        if self.previousPoint != (0,0):
            self.segment(self.previousPoint, self.currentPoint, 4)

        self.elapsed = 0
        
    def segment(self, start, end, w):
        self.x1 = start[0]
        self.x2 = end[0]
        self.y1 = start[1]
        self.y2 = end[1]

        self.width = self.x2-self.x1
        self.height = self.y2-self.y1
        self.length = math.sqrt(self.width*self.width+self.height*self.height)+1
        self.xs = (w*self.height/self.length)/2
        self.ys = (w*self.width/self.length)/2

        self.line = pyglet.graphics.vertex_list(4, ('v2f', [self.x1-self.xs,self.y1+self.ys, self.x1+self.xs,self.y1-self.ys, self.x2+self.xs,self.y2-self.ys, self.x2-self.xs,self.y2+self.ys,]), ('c3f', [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0]))
        self.lineList.append(self.line)

    def bufferLine(self, y, w):
        self.bLine = pyglet.graphics.vertex_list(4, ('v2f', [(self.location-self.elapsed)-w,y-w, self.location+w,y-w, self.location+w,y+w, (self.location-self.elapsed)-w,y+w]), ('c3f', [1, .75, .75, 1, .75, .75, 1, .75, .75, 1, .75, .75]))

    def update(self):
        for line in self.lineList:
            i = 0
            for point in line.vertices:
                if i % 2 == 0:
                    self.value = line.vertices[i]
                    line.vertices[i] = self.value-self.rate
                i = i+1
        self.elapsed = self.elapsed + self.rate

    def draw(self):
        self.bufferLine(self.y, 2)
        self.bLine.draw(GL_POLYGON)
        for line in self.lineList:
            line.draw(GL_POLYGON)
        self.update()
                

class LineGraphB:
    def __init__(self):
        self.currentPoint = (0,0)
        self.previousPoint = (0,0)
        self.lineList = []
        self.startTime = int(time.time())
        self.location = 1000
        self.elapsed = 0
        self.y = 100
        self.previousY = 100
        self.rate = 1

    def newPoint(self, y):
        self.previousY = self.y
        self.y = int(y)+100
        self.previousPoint = (self.location-self.elapsed,self.previousY)
        self.currentPoint = (self.location, self.y)
        
        if self.previousPoint != (0,0):
            self.segment(self.previousPoint, self.currentPoint, 4)

        self.elapsed = 0
        
    def segment(self, start, end, w):
        self.x1 = start[0]
        self.x2 = end[0]
        self.y1 = start[1]
        self.y2 = end[1]

        self.width = self.x2-self.x1
        self.height = self.y2-self.y1
        self.length = math.sqrt(self.width*self.width+self.height*self.height)+1
        self.xs = (w*self.height/self.length)/2
        self.ys = (w*self.width/self.length)/2

        self.line = pyglet.graphics.vertex_list(4, ('v2f', [self.x1-self.xs,self.y1+self.ys, self.x1+self.xs,self.y1-self.ys, self.x2+self.xs,self.y2-self.ys, self.x2-self.xs,self.y2+self.ys,]), ('c3f', [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1]))
        self.lineList.append(self.line)

    def bufferLine(self, y, w):
        self.bLine = pyglet.graphics.vertex_list(4, ('v2f', [(self.location-self.elapsed)-w,y-w, self.location+w,y-w, self.location+w,y+w, (self.location-self.elapsed)-w,y+w]), ('c3f', [.75, .75, 1, .75, .75, 1, .75, .75, 1, .75, .75, 1]))

    def update(self):
        for line in self.lineList:
            i = 0
            for point in line.vertices:
                if i % 2 == 0:
                    self.value = line.vertices[i]
                    line.vertices[i] = self.value-self.rate
                i = i+1
        self.elapsed = self.elapsed + self.rate

    def draw(self):
        self.bufferLine(self.y, 2)
        self.bLine.draw(GL_POLYGON)
        for line in self.lineList:
            line.draw(GL_POLYGON)
        self.update()


lineGraphA = LineGraphA()
lineGraphB = LineGraphB()

@window1.event
def on_draw():
    bg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 1200,0, 1200,800, 0,800]), ('c3f', [1,1,1, 1,1,1, .5,.5,.5, .5,.5,.5]))
    bg.draw(GL_POLYGON)

    blackLine(50,100,1150,100,2)

    lineGraphA.draw()
    lineGraphB.draw()

    bar1()
    bar2()

##@window2.event
##def on_draw():
##    bg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 800,0, 800,600, 0,600]), ('c3f', [1,1,1, 1,1,1, .75,.75,.75, .75,.75,.75]))
##    bg.draw(GL_POLYGON)
##
##
##    lineGraphA.draw()
##    lineGraphB.draw()


def update(ThisFunctionAlwaysWantsAnArgument):
    pass

run()
