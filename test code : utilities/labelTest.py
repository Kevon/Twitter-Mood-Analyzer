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


window = pyglet.window.Window(1200,600)

start = False

def pStream():
    while True:
        if random.randint(0,50) == 25:
            tweetMood = random.randint(-100,100)
            publicTweets.newTweet("@TestAccount", "status.text", tweetMood)

def start2():
    t2 = Thread(target = pStream)
    t2.start()

def run():

    start2()

    pyglet.clock.schedule_interval(update,1/60.0)
    pyglet.app.run()
    
class PublicTweets:
    def __init__(self):
        self.tweetLabel = None
        
    def newTweet(self, name, text, mood):
        self.y = 300+(mood*3)
        self.x = random.randint(0, 1200)
        self.tweet = pyglet.text.Label(text,
                              font_name='Helvetica',
                              font_size=12, color=(255, 255, 255, 255),
                              x=self.x, y=self.y, anchor_x='center')
        
        self.tweetLabel = self.tweet
        
    def draw(self):
        if self.tweetLabel != None:
            self.tweetLabel.draw()

publicTweets = PublicTweets()

bg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 1200,0, 1200,800, 0,800]), ('c4f', [0.25,0.25,.4,0.1, 0.25,0.25,0.4,0.1, 0.1,0.1,0.25,0.1, 0.1,0.1,0.25,0.1]))

def background():
    startbg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 1200,0, 1200,800, 0,800]), ('c3f', [0.25,0.25,0.4, 0.25,0.25,0.4, 0.1,0.1,0.25, 0.1,0.1,0.25]))
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
        tweetMood = random.randint(-100,100)
        publicTweets.newTweet("@TestAccount", "status.text", tweetMood)
        print "get"

run()
