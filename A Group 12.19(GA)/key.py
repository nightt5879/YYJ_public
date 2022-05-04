from control import gpio
import RPi.GPIO as GPIO
import time
import serial
from pynput import keyboard
import string
import threading




s = gpio.Mecanum_wheel()
s.uart_init()


def mu():
    m = machine.mpu6050()
    m.get_angle()

def on_press(key):
    try:

        if key.char == 'w':
            s.car_contr(-40,0,0)
        if key.char == 'a':
            s.car_contr(-0,0,1000)
        if key.char == 's':
            s.car_contr(40,0,0)
        if key.char == 'd':
            s.car_contr(-0,0,-1000)
        if key.char == 'q':
            s.car_contr(-0,50,0)
        if key.char == 'e':
            s.car_contr(-0,-50,-0)
    except AttributeError:
        print('special key {0} pressed'.format(key))


def on_release(key):
    s.car_contr(0,0,0)
    if key == keyboard.Key.esc:
        return False


def anjian():
    with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
        listener.join()


def get_test_move():
    car_speed = 40
    if input()=='1':
        ini_z_angle = m.z_angle
        for i in range(20):
            s.car_contr(0, -car_speed, 0)
            time.sleep(2)
            s.car_contr(0, 0, 0)
            time.sleep(0.2)
            s.car_contr(0, car_speed, 0)
            time.sleep(2)
            s.car_contr(0, 0, 0)


def xuanz():
    t = input()
    print(t)
    if t=='1':
        car_speed = 500
        s.car_contr(0, 0, car_speed)
# 键盘监听
    
# thread1 = threading.Thread(target=mu)
thread2 = threading.Thread(target=anjian)
# thread1.start()
thread2.start()

