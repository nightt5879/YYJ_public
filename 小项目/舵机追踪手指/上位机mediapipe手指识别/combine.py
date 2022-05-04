# encoding=utf-8
import serial
import time
from control import shijue1

a=shijue1.Img()
a.camera(0)
a.name_windows('img')
a.finger_init()
fps = 0
start = time.time()
delay_time = 0
'''
下面是关键的算法
'''
def location(x,y):
    '''
    下面四个分别是边界值，方便调参
    '''
    line_x1 = 100
    line_x2 = 220
    line_y1 = 20
    line_y2 = 100
    if line_x1 <= x <= line_x2 and line_y1 <= y <= line_y2:
        # print('中心')
        x = 0xE5

    elif 0 < x < line_x1 and 0 < y < line_y1:
        # print('左上')
        x = 0xE1
    elif line_x2 < x < 320 and 0 < y < line_y1:
        # print('右上')
        x = 0xE3
    elif 0 < x < line_x1 and line_y2 < y < 240:
        # print('左下')
        x = 0xE7
    elif line_x2 < x < 320 and line_y2 < y < 240:
        # print('右下')
        x = 0xE9

    elif 0 <= x < line_x1 and line_y1 <= y <= line_y2:
        # print('正左')
        x = 0xE4
    elif line_x2 < x <= 320 and line_y1 <= y <= line_y2:
        # print('正右')
        x = 0xE6
    elif line_x1 <= x <= line_x2 and 0 <= y < line_y1:
        # print('正上')
        x = 0xE2
    else:
        # print('正下')
        x = 0xE5
    return x

if __name__ == '__main__':
    com = serial.Serial('COM4', 4800)  #串口数据
    while True:
        '''
        if fps == 1:
            start = time.time()
        '''
        a.get_img()
        a.img_flip('y')   #翻转下看得舒服
        a.finger_detect()
        if a.fingertip:
            x, y = a.fingertip['fore_finger']  #图像是320✖240的
            #print(x, y)
            data = location(x,y)
        else:
            data = 1   #没读到数据就不动
        a.show_image('img')
        a.delay(1)
        data = bytes([data])
        if delay_time == 3:
            com.write(data)
            delay_time = 0
        delay_time += 1
        '''
        count = com.inWaiting() # 获取串口缓冲区数据
        if count !=0 :
            recv = com.read(com.in_waiting) # 读出串口数据，数据采用gbk编码
            print(recv)  # 打印一下子
        #print('is send')
        '''
        '''
        if fps == 9:
            end = time.time()
            print(str(10/(end - start)) + 'fps')
            fps = 0
        fps += 1
        '''
    #print (com)
