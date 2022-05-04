import cv2
from pynput import keyboard
from YYJ import shijue1
import threading
import RPi.GPIO as GPIO
import time

#初始化激光发射
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)

GPIO.output(7, GPIO.HIGH)
time.sleep(2)
GPIO.output(7, GPIO.LOW)
GPIO.cleanup() 