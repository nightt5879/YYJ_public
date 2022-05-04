#!/usr/local/bin/python3
from __future__ import division
import time
import sys

system_platform = sys.platform
if 'win' in system_platform:
    pass
else:
    import serial
    import Adafruit_DHT
    import RPi.GPIO as GPIO
    import Adafruit_PCA9685

    # 设置编码格式为BCM，关闭警告
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


old_fb = 0
old_lr = 0
old_tn = 0


# 7月份钣金小车版本对应扩展板的 io_BCM字典
io2gpio = {0: 16, 1: 12, 2: 25,
           3: 24, 4: 22, 5: 23,
           6: 27, 7: 17, 8: 4}

pwm2gpio = {0: 0, 1: 1,
            2: 2, 3: 3}

uw_io = {1: [5, 6],
         2: [13, 19]}


# 初始类 IO
class io():
    def __init__(self, io_num):
        self.gpio = io2gpio[io_num]
        self.ioin = 404
        GPIO.setmode(GPIO.BCM)
    
    def __str__(self):
        pass
    
    def setmode(self, gpiomode):
        # 设置GPIO的模式,bcm或者board
        if gpiomode == 'BCM':
            GPIO.setmode(GPIO.BCM)
        elif gpiomode == 'BOARD':
            GPIO.setmode(GPIO.BOARD)
    
    def setinout(self, inorout):
        # 设置GPIO的输入或者输出
        if inorout == 'IN':
            GPIO.setup(self.gpio, GPIO.IN)
        elif inorout == 'OUT':
            GPIO.setup(self.gpio, GPIO.OUT)
    
    def setioout(self, dianping):
        # GPIO输出高or低电平
        if dianping == 'HIGH':
            GPIO.output(self.gpio, GPIO.HIGH)
        elif dianping == 'LOW':
            GPIO.output(self.gpio, GPIO.LOW)
    
    def getioin(self):
        # 获取GPIO口的输入电平
        if GPIO.input(self.gpio) == 0:
            # 低电平,返回false
            time.sleep(0.01)
            if GPIO.input(self.gpio) == 0:
                # 防抖设计
                self.ioin = 0
                # 输入为低电平
        else:
            self.ioin = 1
            time.sleep(0.01)
    
    def cleanio(self):
        # 清理io口
        GPIO.cleanup(self.gpio)


class io2pwm():
    def __init__(self, io_num, freq=50, duty=50):
        self.pwm_io = io2gpio[io_num]
        GPIO.setup(self.pwm_io, GPIO.OUT)
        self.freq = freq
        self.duty = duty
    
    '''
        # 通过IO口输出pwm波
        p = GPIO.PWM(channel, frequency)
        p.start(dc) # where dc is the duty cycle (0.0 <= dc <= 100)
        p.ChangeFrequency(freq)  # freq 是以Hz为单位的新频率
        p.ChangeDutyCycle(dc)  # where 0.0 <= dc <= 100.0
        p.stop()
    '''
    
    def start(self):
        # 开始产生pwm
        self.io_pwm = GPIO.PWM(self.pwm_io, self.freq)
        self.io_pwm.start(self.duty)
    
    def set_freq(self, pwm_freq):
        self.freq = pwm_freq
    
    def set_duty(self, pwm_duty):
        self.duty = pwm_duty
        self.io_pwm.ChangeDutyCycle(self.duty)
    
    def end(self):
        # 关闭pwm波
        self.io_pwm.stop()


class PWM():
    def __init__(self, pwm_io):
        # 初始化,必须提供是哪个pwm口，即打开pwm功能,pwm_io>40
        self.pw = Adafruit_PCA9685.PCA9685()
        self.io_pwm = pwm2gpio[pwm_io]
        self.duty = 50
        self.freq = 262
        # 1:262 2:294 3:330 4:349 5:392 6:440 7:494
    
    '''
    pwm = Adafruit_PCA9685()
    def set_servo_angle(channel, angle):
        date = 4096*((angle*11)+500)/20000
        pwm.set_pwm(channel, 0, date)

    pwm.set_pwm_freq(50)
    while True:
        channel = int(input())
        angle = int(input())
        set_servo_angle(channel, angle)

    '''
    '''
        duty : 占空比
        freq : 频率
        self.io_pwm: 通道
    '''
    
    def pwm_start(self):
        # pw产生的PWM波发生器
        self.pw.set_pwm(self.io_pwm, 0, int((100 - self.duty) * 40.95))
        # 对于低电平有效的RGB灯而言
    
    def change_duty(self, duty):
        self.duty = duty
        self.pw.set_pwm(self.io_pwm, 0, int((100 - self.duty) * 40.95))
    
    def change_freq(self, freq):
        self.freq = freq
        self.pw.set_pwm_freq(self.freq)
    
    def pwm_stop(self):
        self.pw.set_pwm(self.io_pwm, 0, int((100 - 0) * 40.95))


class csb():
    def __init__(self, uw_num):
        self.trig_p = uw_io[uw_num][0]
        self.echo_p = uw_io[uw_num][1]
        self.dis = 0
        GPIO.setup(self.trig_p, GPIO.OUT)
        GPIO.setup(self.echo_p, GPIO.IN)
    
    '''
        self.trig_p: trig 对应的引脚
        self.echo_p: echo 对应的引脚
        self.dis   : 返回的距离
    '''
    
    def sent_t_pulse(self):
        # 发送超声波
        GPIO.output(self.trig_p, 0)
        time.sleep(0.0002)
        GPIO.output(self.trig_p, 1)
        time.sleep(0.0001)
        GPIO.output(self.trig_p, 0)
    
    def wait_for_e(self, value, timeout):
        count = timeout
        while GPIO.input(self.echo_p) != value and count > 0:
            count = count - 1
    
    def get_distance(self):
        self.sent_t_pulse()
        self.wait_for_e(True, 10000)
        start = time.time()
        self.wait_for_e(False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        self.dis = distance_cm


# 普通io口的蜂鸣器,有源蜂鸣器
class beep():
    def __init__(self, beepio):
        self.gpio = io2gpio[beepio]
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio, GPIO.HIGH)
        self.data = 0
    
    def beep_s(self, seconds):
        GPIO.output(self.gpio, GPIO.LOW)
        time.sleep(seconds)
        GPIO.output(self.gpio, GPIO.HIGH)
    
    def open_b(self):
        GPIO.output(self.gpio, GPIO.LOW)
    
    def close_b(self):
        GPIO.output(self.gpio, GPIO.HIGH)


class led():
    def __init__(self, ledio):
        self.gpio = io2gpio[ledio]
        GPIO.setup(self.gpio, GPIO.OUT)
        GPIO.output(self.gpio, GPIO.HIGH)
    
    def openled(self):
        # 灯亮
        GPIO.output(self.gpio, GPIO.HIGH)
    
    def closeled(self):
        GPIO.output(self.gpio, GPIO.LOW)


class tmp_hum():
    def __init__(self, t_h_io):
        self.gpio = io2gpio[t_h_io]
        GPIO.setup(self.gpio, GPIO.IN)
        self.temp = 'none'
        self.humi = 'none'
    
    def getTemp_Humi(self):
        tmp = Adafruit_DHT.DHT11
        humi, temp = Adafruit_DHT.read_retry(tmp, self.gpio)
        if temp == None or humi == None:
            self.data = "获取温湿度失败"
        else:
            self.temp = str(temp) + '℃'
            self.humi = str(humi) + '%'


class hongwai():
    # 红外检测模块
    def __init__(self, hongwaiio):
        self.gpio = io2gpio[hongwaiio]
        GPIO.setup(self.gpio, GPIO.IN)
        # 红外IO设置为输入模式
        self.data = 0
        # 没有东西遮挡为False
    
    def get_return(self):
        # 获取GPIO口的输入电平
        if GPIO.input(self.gpio) == 0:
            # 低电平,返回false
            time.sleep(0.01)
            if GPIO.input(self.gpio) == 0:
                # 防抖设计
                self.data = 0
                # 输入为低电平
        else:
            self.data = 1
            time.sleep(0.01)


class servo(PWM):
    def __init__(self, servo_io):
        super().__init__(servo_io)
        self.io = servo_io
        self.duty = 0
        self.pw.set_pwm(self.io, 0, int(2.5 * 40.95))
    
    def setServoAngle(self, angle):  # 设置舵机角度
        # duty=4096*((angle*11)+500)/20000   #由角度算占空比
        # print('duty',duty)
        # self.duty=int(duty)
        self.duty = (angle / 18 + 3) - 0.5
        # print('duty',self.duty)
        self.pw.set_pwm(self.io, 0, int(self.duty * 40.95))


class Mecanum_wheel():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyAMA0', 115200)
        self.dec = 'none'
        self.contr_fb = 0
        self.contr_lr = 0
        self.contr_tn = 0
        self.car_speed = {'car_go': 0, 'car_back': 0,
                          'car_turn_l': 0, 'car_turn_r': 0,
                          'car_across_l': 0, 'car_across_r': 0}
        self.came = 0  # 识别到等待线之后才把cam置为1
        
        GPIO.setwarnings(False)  # 关闭警告说明
        GPIO.setup(0, GPIO.IN)  # 设置引脚1（BCM编号）为输入通道1GPIO.setup(0, GPIO.IN) #设置引脚1（BCM编号）为输入通道
        GPIO.setup(1, GPIO.IN)  # 设置引脚1（BCM编号）为输入通道
    
    def uart_init(self):
        if self.ser.isOpen == False:
            self.ser.open()  # 打开串口
    
    def uart_receive(self):
        try:
            # 打开串口
            if self.ser.is_open == False:
                self.ser.open()
            while True:
                count = self.ser.inWaiting()
                if count != 0:
                    # 读取内容并显示
                    recv = self.ser.read(count)
                    print(recv)
                
                # 清空接收缓冲区
                self.ser.flushInput()
                # 必要的软件延时
                time.sleep(0.1)
        except KeyboardInterrupt:
            if self.ser != None:
                self.ser.close()
    
    def stop(self):
        self.car_contr(0, 0, 0)
    
    def car_go(self):
        self.car_contr((self.car_speed['car_go']), 0, 0)

    def car_back(self):
        self.car_contr(-(self.car_speed['car_back']), 0, 0)

    def car_across_l(self):
        self.car_contr(0, -(self.car_speed['car_across_l']), 0)

    def car_across_r(self):
        self.car_contr(0, (self.car_speed['car_across_r']), 0)

    def car_turn_l(self):
        self.car_contr(0, 0, (self.car_speed['car_turn_l']))

    def car_turn_r(self):
        self.car_contr(0, 0, -(self.car_speed['car_turn_r']))
    
    # 小车控制函数
    def car_contr(self, contr_fb=0, contr_lr=0, contr_tn=0):
        '''
        目前所用协议为 V1.0 ChenZuHong 2021-10-9
        :param contr_fb: 控制小车前进，协议中正数前进，负数后退，单位为mm/s
        :param contr_lr: 控制小车平移，协议中正数右平移，负数左平移，单位为mm/s
        :param contr_tn: 控制小车旋转，协议中正数逆时针，负数顺时针，单位为°/s
        '''
        global old_fb, old_lr, old_tn
        if (contr_fb != old_fb) or (contr_lr != old_lr) or (contr_tn != old_tn):
            old_fb = contr_fb
            old_lr = contr_lr
            old_tn = contr_tn
            # 当速度为负的，做数据处理，得到电机反转的速度
            # fb 控制前后移动，lr控制左右平移，tn控制左右转向
            # fb = -10表示前进，lr = -10 表示向左平移，tn = -500表示左转
            if contr_fb < 0:
                contr_fb = 65536 + contr_fb
            if contr_lr < 0:
                contr_lr = 65536 + contr_lr
            if contr_tn < 0:
                contr_tn = 65536 + contr_tn
            byte_list = [0x55, 0x0E, 0x01, 0x01,
                         int(contr_fb / 256), int(contr_fb % 256),
                         int(contr_tn / 256), int(contr_tn % 256),
                         int(contr_lr / 256), int(contr_lr % 256),
                         0, 0, 1]
            k = 0
            for i in range(len(byte_list)):
                k += byte_list[i]
                k = k % 256
            byte_list.append(k)
            # 格式化要发送的数据帧
            contr_law = b"%c%c%c%c%c%c%c%c%c%c%c%c%c%c" % (byte_list[0], byte_list[1], byte_list[2], byte_list[3],
                                                           byte_list[4], byte_list[5], byte_list[6], byte_list[7],
                                                           byte_list[8], byte_list[9], byte_list[10], byte_list[11],
                                                           byte_list[12], byte_list[13])
            '''
            byte_list[0], byte_list[1], byte_list[2], byte_list[3]: 数据帧前四位， 协议中是 0x55, 0x0E, 0x01, 0x01
            byte_list[4], byte_list[5]: 协议中控制前进速度高八位、低八位
            byte_list[6], byte_list[7]: 协议中控制旋转速度高八位、低八位
            byte_list[8], byte_list[9]: 协议中控制平移速度高八位、低八位
            byte_list[10], byte_list[11]:保留位，默认为0，0
            byte_list[12], byte_list[13]:帧ID，默认为1， 校验位，由前面13个数据叠加而成
            '''
            # 发送数据帧
            self.ser.write(contr_law)

            # 防止连续快速发送数据导致出错
            time.sleep(0.005)
    
    def before_xunxian(self, io_l, io_r):
        self.hw_l = hongwai(io_l)
        self.hw_r = hongwai(io_r)
    
    def xunxian(self):
        self.hw_l.get_return()
        self.hw_r.get_return()
        self.came = 0
        
        if self.hw_l.data == 1 and self.hw_r.data == 1:
            self.car_contr(-10, 0, 0)  # 三个参数分别代表/前进后退/左右平移/左右旋转的速度
        
        if self.hw_l.data == 0 and self.hw_r.data == 1:
            self.car_contr(-5, 0, -500)
        
        if self.hw_l.data == 1 and self.hw_r.data == 0:
            self.car_contr(-5, 0, 500)
        
        if self.hw_l.data == 0 and self.hw_r.data == 0:
            self.car_contr(0, 0, 0)
            self.came = 1


def main_test_shijuexunxian():
    import cv2
    import numpy as np
    m = Mecanum_wheel()
    m.stop()
    cap = cv2.VideoCapture(0)  # 实例化摄像头
    center = 320  # 刚开始假设黑线中心在图像中心
    empty = []
    while True:
        ret, frame = cap.read()  # capture frame_by_frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 获取灰度图像
        ret, dst = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)  # 对灰度图像进行二值化
        dst = cv2.erode(dst, None, iterations=6)  # 腐蚀操作，黑线中间的白色区域变小。
        # cv2.imshow('BINARY',dst)        #树莓派桌面显示二值化图像，比较占资源默认
        # cv2.waitKey(40)
        color_1 = dst[380]  # 单看1/4高度的那一行像素
        color_2 = dst[430]
        # cv2.imshow('color',color)
        black_count_1 = np.sum(color_1 == 0)  # 统计黑色的像素点个数
        black_index_1 = np.where(color_1 == 0)
        
        black_count_2 = np.sum(color_2 == 0)  # 统计黑色的像素点个数
        black_index_2 = np.where(color_2 == 0)
        # print('black_index',black_index)
        
        if black_count_1 == 0:
            black_count_1 = 1
        if black_count_2 == 0:
            black_count_2 = 1
        if list(black_index_1[0]) == empty:
            center_1 = 0
            m.stop()
        else:
            center_1 = (black_index_1[0][0] + black_index_1[0][black_count_1 - 1]) / 2
        
        if list(black_index_2[0]) == empty:
            center_2 = 0
            m.stop()
        else:
            center_2 = (black_index_2[0][0] + black_index_2[0][black_count_2 - 1]) / 2
        center = (center_1 + center_2) / 2
        print('center', center)
        #     #找到黑色点的中心点位置
        # direction=center-320  #于标准中心的偏移量
        # print('direction',direction)
        if center == -320:  # 相差太多，说明冲出去了，则小车停止
            # time.sleep(0.007)
            m.stop()
        elif center > 370:  # 说明中心在右边320+150=430
            # time.sleep(0.007)
            print('turn_right')
            m.car_turn_l(45)
        elif center < 270:  # 说明中心在左边320-150=170
            # time.sleep(0.007)
            print('turn_left')
            m.car_turn_r(45)
        else:
            print('go')
            # time.sleep(0.007)
            m.car_go(25)
    cap.release()
    cv2.destroyAllWindows()


'''
m=car(1,2)
m.stop()
cap = cv2.VideoCapture(0)   #实例化摄像头
center=320  #刚开始假设黑线中心在图像中心
empty=[]
while True:
    ret,frame = cap.read()  #capture frame_by_frame
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #获取灰度图像
    ret,dst=cv2.threshold(gray,70,255,cv2.THRESH_BINARY)#对灰度图像进行二值化
    dst=cv2.erode(dst,None,iterations=6)  #腐蚀操作，黑线中间的白色区域变小。
    #cv2.imshow('BINARY',dst)        #树莓派桌面显示二值化图像，比较占资源默认
    #cv2.waitKey(40)
    color_1=dst[380]  #单看1/4高度的那一行像素
    color_2=dst[430]
    #cv2.imshow('color',color)
    black_count_1=np.sum(color_1==0)  #统计黑色的像素点个数
    black_index_1=np.where(color_1==0)

    black_count_2=np.sum(color_2==0)  #统计黑色的像素点个数
    black_index_2=np.where(color_2==0)
    #print('black_index',black_index)

    if black_count_1==0:
        black_count_1=1
    if black_count_2==0:
        black_count_2=1
    if list(black_index_1[0])==empty:
        center_1=0
        m.stop()
    else:
        center_1=(black_index_1[0][0]+black_index_1[0][black_count_1-1])/2

    if list(black_index_2[0])==empty:
        center_2=0
        m.stop()
    else:
        center_2=(black_index_2[0][0]+black_index_2[0][black_count_2-1])/2
    center=(center_1+center_2)/2
    print('center',center)
#     #找到黑色点的中心点位置
    #direction=center-320  #于标准中心的偏移量
    #print('direction',direction)
    if center==-320:  #相差太多，说明冲出去了，则小车停止
        #time.sleep(0.007)
        m.stop()
    elif center>370:  #说明中心在右边320+150=430
        #time.sleep(0.007)
        print('turn_right')
        m.turn_left(10,45)
    elif center<270:  #说明中心在左边320-150=170
        #time.sleep(0.007)
        print('turn_left')
        m.turn_right(45,10)
    else:
        print('go')
        #time.sleep(0.007)
        m.go(25,25)
cap.release()
cv2.destroyAllWindows()
'''