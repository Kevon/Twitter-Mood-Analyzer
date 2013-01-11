import time, math, random
from pyglet.gl import *

import threading
from threading import Thread

window = pyglet.window.Window(1200,600)
bg = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 1200,0, 1200,800, 0,800]), ('c4f', [1,1,1,0.1, 1,1,1,0.1, .5,.5,.5,0.1, .5,.5,.5,0.1]))

start = False

def blackLine(x1,y1,x2,y2,w):
    line = pyglet.graphics.vertex_list(4, ('v2f', [x1-w,y1-w, x2+w,y1-w, x2+w,y2+w, x1-w,y2+w]), ('c3f', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))
    line.draw(GL_POLYGON)


def black():
    black = pyglet.graphics.vertex_list(4, ('v2f', [0,0, 1200,0, 1200,800, 0,800]), ('c3f', [0,0,0, 0,0,0, 0,0,0, 0,0,0]))
    black.draw(GL_POLYGON)

@window.event
def on_draw():
    global start
    if start == False:
        black()
        start = True
    else:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        bg.draw(GL_POLYGON)
        glDisable(GL_BLEND)


def swag():
    if random.randint(0,50) == 25:
        blackLine(random.randint(0,1200),random.randint(0,600),random.randint(0,1200),random.randint(0,600),2)

def thread():
    t1 = Thread(target = swag)
    t1.start()
    
pyglet.app.run()
thread()


