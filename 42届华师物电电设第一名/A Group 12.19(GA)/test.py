#舵机测试
import RPi.GPIO as GPIO
import time

pin = 12 # GPIO端口号，根据实际修改
sin =16
frequence = 50  # Hz (软件PWM方式，频率不能设置过高)
a = 10
b = 2

def setDirection(A,direction):
    duty = a / 180 * direction + b
    D1.ChangeDutyCycle(duty)
    time.sleep(1)
    
def move():
    setDirection(0)
    setDirection(180)
    setDirection(0)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
D1 = GPIO.PWM(pin,frequence)
D1.start(50)
for i in range (2):
    setDirection(D1,0)
    setDirection(D1,180)
    setDirection(D1,0)
    if i == 1:
        break
GPIO.cleanup()


GPIO.setmode(GPIO.BOARD)
GPIO.setup(sin, GPIO.OUT)
D1 = GPIO.PWM(sin,frequence)
D1.start(50)
GPIO.cleanup()





'''
#for color_detect
import cv2
#这两个是颜色检测的阈值
Color_Min = [1,142,104]
Color_Max = [10,255,255]

cam = cv2.VideoCapture(0)
ret,img = cam.read()
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, Color_Min, Color_Max)
kernel = np.ones((5, 5), np.uint8)
mask = cv2.erode(mask, kernel)
cv2.imshow('mask0', mask)
cv2.waitKey(40)
'''