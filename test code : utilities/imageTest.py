import PIL
import urllib
import atexit
import sys

urllib.urlretrieve('http://i.qkme.me/3rl2cj.jpg', 'test.jpg')

@atexit.register
def onExit():
    print 'Exit'
    os.remove('test.jpg')

sys.exit()
