from pynput import keyboard
from YYJ import shijue1
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import ImageFont
import cv2
import threading
import RPi.GPIO as GPIO
import time
import random
import sys
import os
import vlc


'''
'''
GPIO.cleanup()  #干 直接先给个clean up  for 测试ooo
#初始化
a=shijue1.Img()
a.camera(0)



#参数
k = 0    #这是用来保存键盘返回值的
x = 180    #水平方向自由度
z = 0    #竖直方向自由度
p = 0    #判断连中问题
result = '未获'
loc = '未获'
#舵机参数部分

frequence = 50  # Hz (软件PWM方式，频率不能设置过高)

#初始化舵机  1号
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
D1 = GPIO.PWM(40,frequence)
D1.start(50)   #这个是干什么的？？？？哦odadao

#2号
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
D2 = GPIO.PWM(16,frequence)
D2.start(50)

#初始化激光发射
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)

#初始化oled

__version__ = 1.0    # 初始化端口
serial = i2c(port=1, address=0x3C)  # 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
device = ssd1306(serial)
print("当前版本：", __version__)
font = ImageFont.truetype('/home/pi/Desktop/A Group 12.12/msyhl.ttc', 12) # 调用显示函数



x, z = 80, 80
#键盘监听部分
def on_press(key):
    global x, z, f, result, loc
    f = 0.5
    num = 0
    try:
        k = key.char
        print(k)
        if k == 'o':#
            #setDirection(D1,x)
            #setDirection(D2,z)
            D1.ChangeDutyCycle(0)
            D2.ChangeDutyCycle(0)
            GPIO.output(29, GPIO.HIGH)
            #time.sleep(0.5)
            m, d = red_detect()
            print(1)
            tan, side = ccl_num(m[0],m[1])
            loc = ccl_CN(tan,m[0],side)
            result = ccl_target(d)
            print('中心点坐标：{0}; 距离：{1}'.format(m,d))
            print('tan:{}; side:{}'.format(tan,side))
            print('环数：{}; 方位：{}'.format(result, loc))
            result_oled()
            #语音播报部分
            '''
            speak(result)
            speak(loc)
            '''
            #print(tan, side)orrqro
            time.sleep(2)
            GPIO.output(29, GPIO.LOW)
            print('done')
        #舵机控制部分o
        if k == 'q':  #reset 舵机位置(0)qraaaaaaaaa哦doooo
            x = 9.0
            z = 80
            setDirection(D1,x)
            setDirection(D2,z)
            #D1.ChangeDutyCycle(0)   #清空占空比，这句是防抖关键句，如果没有这句，舵机会狂抖不止
            #D2.ChangeDutyCycle(0)
        if k == 'r':  #reset 舵机位置radreqr
            x = 7.5
            z = 91.0
            setDirection(D1,x)
            setDirection(D2,z)
            #D1.ChangeDutyCycle(0)
            #D2.ChangeDutyCycle(0)
        if k == 'a':#Wra
            x += f
            if x >= 180:
                x = 180
            setDirection(D1,x)
            #D1.ChangeDutyCycle(0)
            print(x)
        if k == 'd':#qrswwwwwsssssswwswwwwwsswsssssssssssssswwwaaadddrwsrwrwwrraaddwsrws
            x -= f
            if x <= 0:
                x = 0
            setDirection(D1,x)
            #D1.ChangeDutyCycle(0)
            print(x)
        if k == 's':#W
            z += f
            if z >= 180:
                z = 180
            setDirection(D2,z)
            #D2.ChangeDutyCycle(0)
            print(z)
        if k == 'w':#oddro
            z -= f
            if z <= 0:
                z = 0
            setDirection(D2,z)
            #D2.ChangeDutyCycle(0)
            print(z)
        #D1.ChangeDutyCycle(0)
        #D2.ChangeDutyCycle(0)
        if k == 'z':
            print(x,z)
        '''
        自瞄部分
        '''
        if k == '0':  #所谓的回归中心
            as_10()
        if k == '9':
            as_9()
        if k == '8':
            as_8()
        if k == '7':
            as_7()
        if k == '6':
            as_6()
        if k == '5':
            as_5()
        if k == 'm':
            D1.ChangeDutyCycle(0)
            D2.ChangeDutyCycle(0)
            GPIO.output(29, GPIO.HIGH)
            time.sleep(3)
            GPIO.output(29, GPIO.LOW)
        if k == 't':
            D1.ChangeDutyCycle(0)
            D2.ChangeDutyCycle(0)

        if k == 'l':
            speak(result,loc)

        if k == 'n':
            #bground()
            result_oled()

        if k == 'm':
            start()



    except AttributeError:
        k =key
        print(k)
        #print('special {}'.format(key))   #可以调用看监听是不是正常oo

def on_release(key):
    #print(threading.current_thread().name+'{0}release'.format(key)) #可以调用看是不是监听正常
    if key == keyboard.Key.esc:
        return False


def anjian():
    with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
        listener.join()


#视觉部分"/home/pi/Desktop/A Group 12.12/record/10.m4a"
def red_detect():
    num = 0    #防止一次读取不到值（刷掉一些残留帧）wooo
    while num < 10:
        a.color_detect_init("red")
        a.get_img()
        a.color_detect()
        a.name_windows('img')
        a.show_image('img')
        a.delay(1)
        if num == 9:
            return a.midle, a.distance   #要用到的方位信息wadwoo
        num += 1

#舵机部分
'''
def go(a):  #直接是走了个赋值在输出命令再结束  能否直接赋值后调用？？？？
    global pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(a, GPIO.OUT)
    pwm = GPIO.PWM(a,frequence)
    pwm.start(50)
    move()
    GPIO.cleanup()
'''
#W
def setDirection(A,direction):
    duty =  10/ 180 * direction + 2   #a/ 180 * direction + b  a=10 b=2
    A.ChangeDutyCycle(duty)

def move():
    setDirection(0)
    setDirection(180)
    setDirection(0)


#数据处理部分

def ccl_target(d):  #计算d来返回靶数  里面的d是动态调节的o
    i = 'none'
    global p
    if d == 0:
        p += 1
        if p >= 2:
            i = 'out_again'
        else:
            i = 'out'
    elif d < 50:
        p += 1
        if p >= 2:
            i = '10_again'
        else:
            i = '10'
    elif d < 83:
        p = 0
        i = '9'
    elif d < 110:
        p = 0
        i = '8'
    elif d < 140:
        p = 0
        i = '7'
    elif d < 170:
        p = 0
        i = '6'
    elif d < 220:
        p = 0
        i = '5'
    else:
        p += 1
        if p >= 2:
            i = 'out_again'
        else:
            i = 'out'
    return i

def ccl_num(x,y):  #计算tan值和方位oo
    X = x-250
    Y = y-250
    tan = 0
    side = 'none'
    if X != -250:
        if X > 0:
            side = 'right'
        elif X < 0:
            side = 'left'   #这里需不需要考虑没有识别到的情况wao
        if X != 0:
            tan = Y/X
    return tan, side

def ccl_CN(t,y,z):   #计算具体的位置，返回的是汉语了！！！ t:tan  y:纵轴值  z：方位值  左边还是右边
    location = 'no location'
    if z != 'none': #应该基本没有刚好读取到250的情况吧。。。。
        if z == 'right':
            if t < -2.414:
                location = '正上'
            elif t < -0.414:
                location = '右上'
            elif t < 0.414:
                location = '正右'
            elif t < 2.414:
                location = '右下'
            else:
                location = '正下'
        elif z == 'left':      #写else也可以但是爷不想！
            if t < -2.414:
                location = '正下'
            elif t < -0.414:
                location = '左下'
            elif t < 0.414:
                location = '正左'
            elif t < 2.414:
                location = '左上'
            else:
                location = '正上'

    else:
        if y > 250:
                location = '正下'
        elif 0< y < 250:           #不会吧不会吧  不会真出现正正好好双250吧？！oo
                location = '正上'

    return location

#自瞄部分   很恶心u1s1想放到一个大包里面了。。。。
def as_10():
    setDirection(D1, 91.0)
    setDirection(D2, 86.5)

def as_9():
    global x, z
    i = random.randint(1, 2)
    if i == 1:
        x = 8.5
        z = 91.0
        setDirection(D1, x)
        setDirection(D2, z)
    if i == 2:
        x = 6.5
        z = 90.0
        setDirection(D1, x)
        setDirection(D2, z)

def as_8():
    global x, z
    i = random.randint(1, 2)
    if i == 1:
        x = 8.5
        z = 88.0
        setDirection(D1, x)
        setDirection(D2, z)
    if i == 2:
        x = 5.5
        z = 89.0
        setDirection(D1, x)
        setDirection(D2, z)

def as_7():
    global x, z
    i = random.randint(1, 2)
    if i == 1:
        x = 10.5
        z = 91.0
        setDirection(D1, x)
        setDirection(D2, z)
    if i == 2:
        x = 6.5
        z = 86.5
        setDirection(D1, x)
        setDirection(D2, z)

def as_6():
    global x, z
    i = random.randint(1, 2)
    if i == 1:
        x = 4.5
        z = 87.0
        setDirection(D1, x)
        setDirection(D2, z)
    if i == 2:
        x = 11.5
        z = 91.0
        setDirection(D1, x)
        setDirection(D2, z)

def as_5():
    global x, z
    i = random.randint(1, 2)
    if i == 1:
        x = 12.5
        z = 91.0
        setDirection(D1, x)
        setDirection(D2, z)
    if i == 2:
        x = 4.5
        z = 85.0
        setDirection(D1, x)
        setDirection(D2, z)

#语音部分
def speak(a,b):
    path1 = "/home/pi/Desktop/A Group 12.12/record/"+a+".m4a"
    w = vlc.MediaPlayer(path1)
    w.play()
    time.sleep(2)
    w.stop()
    path2 = "/home/pi/Desktop/A Group 12.12/record/"+b+".m4a"
    q = vlc.MediaPlayer(path2)
    q.play()
    time.sleep(2)
    q.stop()

#oled部分
#背景
def bground():
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((65, 10), "环数：", fill="white", font=font)
        draw.text((65, 24), "方位：", fill="white", font=font)
        draw.text((65, 38), "早八三明治", fill="white", font=font)
        draw.ellipse((2, 2, 60, 60), outline="white", fill="black")
        draw.ellipse((7, 7, 55, 55), outline="white", fill="black")
        draw.ellipse((12, 12, 50, 50), outline="white", fill="black")
        draw.ellipse((17, 17, 45, 45), outline="white", fill="black")
        draw.ellipse((22, 22, 40, 40), outline="white", fill="black")
        draw.ellipse((27, 27, 35, 35), outline="white", fill="black")



def start():
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")

#环数和方位
def result_oled():
    global loc, result
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((65, 10), "环数：", fill="white", font=font)
        draw.text((65, 24), "方位：", fill="white", font=font)
        draw.text((65, 38), "早八三明治", fill="white", font=font)
        draw.text((100, 10), result, fill="white", font=font)
        draw.text((100, 24), loc, fill="white", font=font)
        draw.ellipse((2, 2, 60, 60), outline="white", fill="black")
        draw.ellipse((7, 7, 55, 55), outline="white", fill="black")
        draw.ellipse((12, 12, 50, 50), outline="white", fill="black")
        draw.ellipse((17, 17, 45, 45), outline="white", fill="black")
        draw.ellipse((22, 22, 40, 40), outline="white", fill="black")
        draw.ellipse((27, 27, 35, 35), outline="white", fill="black")
        #位置
        if result == '10':
            draw.ellipse((29, 29, 33, 33), outline="white", fill="white")
        elif result == '9':
            if loc == '正左':
                draw.ellipse((22, 30, 27, 33), outline="white", fill="white")
            elif loc == '左上':
                draw.ellipse((25, 25, 29, 29), outline="white", fill="white")
            elif loc == '正上':
                draw.ellipse((29, 22, 33, 27), outline="white", fill="white")
            elif loc == '右上':
                draw.ellipse((34, 25, 39, 29), outline="white", fill="white")
            elif loc == '正右':
                draw.ellipse((35, 29, 40, 33), outline="white", fill="white")
            elif loc == '右下':
                draw.ellipse((32, 32, 37, 37), outline="white", fill="white")
            elif loc == '正下':
                draw.ellipse((29, 22, 33, 27), outline="white", fill="white")
            elif loc == '左下':
                draw.ellipse((25, 25, 29, 29), outline="white", fill="white")
        elif result == '8':
            if loc == '正左':
                draw.ellipse((17, 30, 22, 33), outline="white", fill="white")
            elif loc == '左上':
                draw.ellipse((21, 21, 26, 26), outline="white", fill="white")
            elif loc == '正上':
                draw.ellipse((29, 17, 33, 22), outline="white", fill="white")
            elif loc == '右上':
                draw.ellipse((37, 21, 42, 26), outline="white", fill="white")
            elif loc == '正右':
                draw.ellipse((40, 29, 45, 33), outline="white", fill="white")
            elif loc == '右下':
                draw.ellipse((36, 36, 41, 41), outline="white", fill="white")
            elif loc == '正下':
                draw.ellipse((29, 40, 33, 45), outline="white", fill="white")
            elif loc == '左下':
                draw.ellipse((21, 37, 26, 42), outline="white", fill="white")
        elif result == '7':
            if loc == '正左':
                draw.ellipse((12, 30, 17, 33), outline="white", fill="white")
            elif loc == '左上':
                draw.ellipse((17, 17, 21, 21), outline="white", fill="white")
            elif loc == '正上':
                draw.ellipse((29, 12, 33, 17), outline="white", fill="white")
            elif loc == '右上':
                draw.ellipse((40, 17, 45, 21), outline="white", fill="white")
            elif loc == '正右':
                draw.ellipse((45, 29, 50, 33), outline="white", fill="white")
            elif loc == '右下':
                draw.ellipse((40, 40, 45, 45), outline="white", fill="white")
            elif loc == '正下':
                draw.ellipse((29, 12, 33, 17), outline="white", fill="white")
            elif loc == '左下':
                draw.ellipse((17, 40, 21, 45), outline="white", fill="white")
        elif result == '6':
            if loc == '正左':
                draw.ellipse((7, 30, 12, 33), outline="white", fill="white")
            elif loc == '左上':
                draw.ellipse((14, 14, 18, 18), outline="white", fill="white")
            elif loc == '正上':
                draw.ellipse((29, 7, 33, 12), outline="white", fill="white")
            elif loc == '右上':
                draw.ellipse((43, 14, 48, 18), outline="white", fill="white")
            elif loc == '正右':
                draw.ellipse((50, 29, 55, 33), outline="white", fill="white")
            elif loc == '右下':
                draw.ellipse((43, 43, 48, 48), outline="white", fill="white")
            elif loc == '正下':
                draw.ellipse((29, 50, 33, 55), outline="white", fill="white")
            elif loc == '左下':
                draw.ellipse((14, 43, 18, 48), outline="white", fill="white")
        elif result == '5':
            if loc == '正左':
                draw.ellipse((3, 30, 7, 33), outline="white", fill="white")
            elif loc == '左上':
                draw.ellipse((10, 10, 15, 15), outline="white", fill="white")
            elif loc == '正上':
                draw.ellipse((29, 2, 33, 7), outline="white", fill="white")
            elif loc == '右上':
                draw.ellipse((47, 10, 52, 15), outline="white", fill="white")
            elif loc == '正右':
                draw.ellipse((55, 29, 60, 33), outline="white", fill="white")
            elif loc == '右下':
                draw.ellipse((47, 47, 52, 52), outline="white", fill="white")
            elif loc == '正下':
                draw.ellipse((29, 55, 33, 60), outline="white", fill="white")
            elif loc == '左下':
                draw.ellipse((10, 10, 15, 15), outline="white", fill="white")

# 子线程 1 键盘监听wsad
t = threading.Thread(target=anjian,name='1')
t.start()
start()