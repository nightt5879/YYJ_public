# encoding=utf-8
import serial
import time

if __name__ == '__main__':
    com = serial.Serial('COM4', 4800)
    bytes = bytes([0xE1])
    while True:
        com.write(bytes)
        count = com.inWaiting() # 获取串口缓冲区数据
        if count !=0 :
            recv = com.read(com.in_waiting) # 读出串口数据，
            print(recv)  # 打印一下子
        #print('is send')
        time.sleep(0.1)
    #print (com)
