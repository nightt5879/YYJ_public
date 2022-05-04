import sys
import os
def speak(a):
    path = "record/"+a+".m4a"
    os.system('mplayer %s' % path)
speak('10_again')