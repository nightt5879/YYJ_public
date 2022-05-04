from control import shijue1
import time
a = None


a=shijue1.Img()
a.camera(0)
a.name_windows('img')
a.finger_init()
fps = 0
start = time.time()
while True:
    if fps == 1:
        start = time.time()
    a.get_img()
    a.finger_detect()
    if a.fingertip:
        x,y = a.fingertip['fore_finger']
        print(x,y)
    a.show_image('img')
    a.delay(1)
    if fps == 9:
        end = time.time()
        #print(str(10/(end - start)) + 'fps')
        fps = 0
    fps += 1