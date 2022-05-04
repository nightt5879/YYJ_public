import cv2
from pynput import keyboard
from YYJ import shijue1
import threading

#初始化
a=shijue1.Img()
a.camera(0)

#参数
k = 0    #这是用来保存键盘返回值的
#键盘监听部分
def on_press(key):
    num = 0
    try:
        k = key.char
        print(k)
        if k =='o':
            m, d = red_detect()
            print (m, d)
    except AttributeError:
        k =key
        print(k)
        #print('special {}'.format(key))   #可以调用看监听是不是正常wowwaso


def on_release(key):
    #print(threading.current_thread().name+'{0}release'.format(key)) #可以调用看是不是监听正常oo
    if key == keyboard.Key.esc:
        return False


def anjian():
    with keyboard.Listener(
        on_press=on_press, on_release=on_release) as listener:
        listener.join()


#视觉部分
def red_detect():
    num = 0    #防止一次读取不到值（刷掉一些残留帧）
    while num < 5:
        a.color_detect_init("red")
        a.get_img()
        a.color_detect()
        a.name_windows('img')
        a.show_image('img')
        a.delay(1)
        if num == 4:
            return a.midle, a.distance
        num += 1
    
#射击部分，结合键盘监听部分o
#def shoot():waadswa

# 子线程 1 键盘监听wsad
t = threading.Thread(target=anjian,name='1')
t.start()



