import time
import random
import math

from pyglet.gl import *

import collections
from collections import deque


window = pyglet.window.Window(800,600)

class LineGraph:
    def __init__(self):
        self.currentPoint = (0,0)
        self.previousPoint = (0,0)
        self.lineList = deque(maxlen=25)
        self.startTime = int(time.time())
        self.location = 600
        self.elapsed = 0
        self.y = 0
        self.previousY = 0
        self.rate = .25

    def newPoint(self, y):
        self.previousY = self.y
        self.y = int(y)
        self.previousPoint = (self.location-self.elapsed,self.previousY)
        self.currentPoint = (self.location, (self.y))
        
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

        self.length = math.sqrt(self.width*self.width+self.height*self.height)

        self.xs = (w*self.height/self.length)/2

        self.ys = (w*self.width/self.length)/2

        self.line = pyglet.graphics.vertex_list(4, ('v2f', [self.x1-self.xs,self.y1+self.ys, self.x1+self.xs,self.y1-self.ys, self.x2+self.xs,self.y2-self.ys, self.x2-self.xs,self.y2+self.ys,]), ('c3f', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        self.lineList.append(self.line)

    def bufferLine(self, y, w):
        self.bLine = pyglet.graphics.vertex_list(4, ('v2f', [(self.location-self.elapsed)-w,y-w, self.location+w,y-w, self.location+w,y+w, (self.location-self.elapsed)-w,y+w]), ('c3f', [.5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5, .5]))

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


lineGraph = LineGraph()

value = 300

def line(x1, y1, x2, y2, w):
        line = pyglet.graphics.vertex_list(4, ('v2f', [x1-w,y1-w, x1+w,y1-w, x2+w,y2+w, x2-w,y2+w]), ('c3f', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
        line.draw(GL_TRIANGLE_FAN)

@window.event
def on_draw():
    global value
    
    bg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 800,0, 800,600, 0,600]), ('c3f', [1,1,1, 1,1,1, .75,.75,.75, .75,.75,.75]))
    bg.draw(GL_POLYGON)

    i = random.randint(0,50)

    line(600,0,600,800,2)
    
    if i == 1:
        value = value + random.randint(-50,50)

        lineGraph.newPoint(value)

    lineGraph.draw()
    lineGraph.update()

def update(blah):
    pass

pyglet.clock.schedule_interval(update,1/60.0)
pyglet.app.run()
