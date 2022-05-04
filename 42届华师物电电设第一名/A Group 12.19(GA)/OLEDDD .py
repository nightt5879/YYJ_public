from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from time import sleep
from PIL import ImageFont
"""
OLED luma 驱动库测试程序
功能：显示 汉字古诗持续10秒
"""
__version__ = 1.0
# 初始化端口
serial = i2c(port=1, address=0x3C)
# 初始化设备，这里改ssd1306, ssd1325, ssd1331, sh1106
device = ssd1306(serial)
print("当前版本：", __version__)
font = ImageFont.truetype('/home/pi/Desktop/A Group 12.12/msyhl.ttc', 12)
# 调用显示函数
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

    draw.ellipse((3, 30, 7, 33), outline="white", fill="white")#5 z
    draw.ellipse((29, 2, 33, 7), outline="white", fill="white")#5 s
    draw.ellipse((55, 29, 60, 33), outline="white", fill="white")#5 you
    draw.ellipse((29, 55, 33, 60), outline="white", fill="white")#5 xia
    draw.ellipse((10, 10, 15, 15), outline="white", fill="white")#5 zs
    draw.ellipse((47, 10, 52, 15), outline="white", fill="white")#5 ys
    draw.ellipse((10, 47, 15, 52), outline="white", fill="white")#5 zx
    draw.ellipse((47, 47, 52, 52), outline="white", fill="white")#5 yx

    draw.ellipse((7, 30, 12, 33), outline="white", fill="white")#6 z
    draw.ellipse((29, 7, 33, 12), outline="white", fill="white")#6 s
    draw.ellipse((50, 29, 55, 33), outline="white", fill="white")#6 you
    draw.ellipse((29, 50, 33, 55), outline="white", fill="white")#6 xia
    draw.ellipse((14, 14, 18, 18), outline="white", fill="white")#6 zs
    draw.ellipse((43, 14, 48, 18), outline="white", fill="white")#6 youshang
    draw.ellipse((14, 43, 18, 48), outline="white", fill="white")#6 zuoxia
    draw.ellipse((43, 43, 48, 48), outline="white", fill="white")#6 youxia
    draw.ellipse((29, 7, 33, 12), outline="white", fill="white")#6 s

    draw.ellipse((12, 30, 17, 33), outline="white", fill="white")#7 z
    draw.ellipse((29, 12, 33, 17), outline="white", fill="white")#7 s
    draw.ellipse((45, 29, 50, 33), outline="white", fill="white")#7 you
    draw.ellipse((29, 45, 33, 50), outline="white", fill="white")#7 xia
    draw.ellipse((17, 17, 21, 21), outline="white", fill="white")#7 zs
    draw.ellipse((40, 17, 45, 21), outline="white", fill="white")#7 youshang
    draw.ellipse((17, 40, 21, 45), outline="white", fill="white")#7 zuoxia
    draw.ellipse((40, 40, 45, 45), outline="white", fill="white")#7 youxai

    draw.ellipse((17, 30, 22, 33), outline="white", fill="white")#8 z
    draw.ellipse((29, 17, 33, 22), outline="white", fill="white")#8 s
    draw.ellipse((40, 29, 45, 33), outline="white", fill="white")#8 you
    draw.ellipse((29, 40, 33, 45), outline="white", fill="white")#8 xia
    draw.ellipse((21, 21, 26, 26), outline="white", fill="white")#8 zs
    draw.ellipse((37, 21, 42, 26), outline="white", fill="white")#8 youshang
    draw.ellipse((21, 37, 26, 42), outline="white", fill="white")#8 zuoxia
    draw.ellipse((36, 36, 41, 41), outline="white", fill="white")#8 youxia

    draw.ellipse((22, 30, 27, 33), outline="white", fill="white")#9 z
    draw.ellipse((29, 22, 33, 27), outline="white", fill="white")#9 s
    draw.ellipse((35, 29, 40, 33), outline="white", fill="white")#9 you
    draw.ellipse((29, 35, 33, 40), outline="white", fill="white")#9 xia
    draw.ellipse((25, 25, 29, 29), outline="white", fill="white")#9 zs
    draw.ellipse((34, 25, 39, 29), outline="white", fill="white")#9 youshang
    draw.ellipse((25, 34, 30, 39), outline="white", fill="white")#9 zuoxia
    draw.ellipse((32, 32, 37, 37), outline="white", fill="white")#9 youxia

    draw.ellipse((29, 29, 33, 33), outline="white", fill="white")#10