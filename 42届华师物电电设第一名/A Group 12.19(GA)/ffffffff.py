#!/usr/bin/env python
# coding: utf-8


import os
import time
from mutagen.mp3 import MP3

music_path = 'StarSky.mp3'
mp3 = MP3(music_path)
os.system('mplayer %s' % music_path)
# 可以根据mp3时长进行休眠
time.sleep(mp3.info.length)