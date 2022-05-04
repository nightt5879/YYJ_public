#color_detect
from YYJ import shijue1
import cv2

a=shijue1.Img()
a.camera(0)

def red_detect():
    a.color_detect_init("red")
    a.get_img()
    a.color_detect()
    a.name_windows('img')
    a.show_image('img')
    a.delay(1)
    return a.midle,a.distance

while True:
    red_detect()
    m, d = red_detect()
    #print(m[0], m[1])
    print(d)
    