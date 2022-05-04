import os
import cv2
import sys
import imutils
from PIL import Image
import numpy as np
import pyzbar.pyzbar as pyzbar
from collections import deque

system_platform = sys.platform
main_path = '/home/pi/class/'  # 读取和保存文件所用主文件夹
if 'win' in system_platform:
    file_path = os.getcwd()
    # 获取当前文件的位置
    main_path = file_path + '/resources/assets/class/'
picture_path = main_path + 'picture/'  # 图片文件夹
model_path = main_path + 'model/'  # 识别模型文件夹
d_path = main_path + 'camera_pos/'
dat_path = main_path + 'data/face_recognize/'

items_num = {0: '9', 1: '1', 2: '2', 3: '3',
             4: '4', 5: '5', 6: '6', 7: '7', 8: '8'}  # 方向数字指示牌
items_dir = {9: '左转', 10: '右转'}
items_label = {11: '语音'}
items_laji = {0: '易拉罐', 1: '纸团', 2: '塑料瓶', 3: '电池', 4: '报纸', 5: '灯泡', 6: '花生壳', 7: '香蕉皮'}


class Assist_converse:
    def __init__(self):
        pass


def new_file(path):
    if os.path.isdir(path):
        pass
    else:
        print('未找到该文件夹。开始创建文件夹')
        os.makedirs(path)


def pic_read(filename, mode):
    '''
        其实严格来说，不是imread不支持中文路径，而是不支持non-ascii。
        所以不论路径如何转换编码格式，应该都不能解决问题。
        解决的思路就是先用其他支持中文的API，把图片数据导入到内存中，
        然后通过opencv从内存读入图片的方法，读入图片。
    :param filename:  图片的路径包括名称
    :param mode:  读取的模式，彩色还是灰度
    :return: 返回读取的图片
    '''
    raw_data = np.fromfile(filename, dtype=np.uint8)
    img = cv2.imdecode(raw_data, mode)
    return img


class Img():
    def __init__(self):

        '''
        默认属性都放在此处
        '''
        self.img = None
        self.cam = None

        self.ID = ''
        self.model_ID = self.ID

        self.data_path = None
        self.save_model_name = None
        self.face_model = model_path + 'face_0.xml'
        self.face_detector = cv2.CascadeClassifier(self.face_model)

        self.faces = None
        self.ids = None
        self.face_name = 'none'

        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

        self.img = None
        self.Type = None

        self.path = ''
        self.cascade = None
        self.color_data = 'no_people'

        self.pht = ''
        self.flag_cap = 0
        self.flag_mask = 0

        self.er_data = 'none'
        self.QR_code_data = None
        #魔改调用版本（啊J）
        self.midle = [0,0]
        self.side = 'none'
        self.distance = 0
        self.tan = 0

    '''
        这是视觉专用的库
    '''

    # 获取摄像头
    def camera(self, num=0):
        self.cam = cv2.VideoCapture(num)

    def close_camera(self):
        self.cam.release()

    # get_img 是用来获取单张图片的
    def get_img(self):
        self.ret, img = self.cam.read()
        if self.ret:
            self.img = img
        else:
            print("未检测到摄像头，请注意摄像头是否接触不良或者未设置允许摄像头")

    # img_flip 是用来翻转镜像图片的
    def img_flip(self, isflip=1):
        if isflip == 1:
            self.img = cv2.flip(self.img, 1)
        else:
            self.img = self.img

    # get_frame 是从某个路径中获取图片
    def get_frame(self, path, mode=cv2.IMREAD_COLOR):
        self.img = pic_read(path, mode)

    # name_windows 是用来命名图片展示窗口的
    def name_windows(self, name):
        cv2.namedWindow(name, 0)
        cv2.resizeWindow(name,500,500)

    # close_windows 是用来关闭所有窗口的
    def close_windows(self):
        cv2.destroyAllWindows()

    # show_image是用来将图片展示在定义的某个窗口中的
    def show_image(self, windows_name, img=[]):
        if len(img) == 0:
            img = self.img
        img = img[0:500,0:500]
        cv2.circle(img,(250,250),5,(0,0,255),-1)   #加入中心点坐标用于校准（YYJ）
        cv2.circle(img,(250,250),20,(0,255,0),0)
        # cv2.resizeWindow(windows_name, 640, 480)
        cv2.imshow(windows_name, img)

    # write_image 是用来保存图片的函数，注意：pic_name中不能存在中文，包括路径和文件命名
    def write_image(self, pic_name, jpg_png=False):
        mode = '.png'
        if jpg_png:
            mode = '.jpg'
        path = picture_path + pic_name + mode
        cv2.imwrite(path, self.img)
        print('图片已保存到：', path)

    # resize 是用来改变图像的大小的
    def resize(self, newsize=(1, 1)):
        self.img = cv2.resize(self.img, newsize)

    # delay 是用来进行展示延时的，有一个或者多个窗口进行展示时，此函数必须用上
    def delay(self, time=1):
        try:
            cv2.waitKey(time)
        except KeyboardInterrupt:
            pass

    # erosion 是用给图片进行腐蚀操作的
    def erosion(self):
        self.img = cv2.erode(self.img, None, iterations=2)

    # dilation 是用来给图片进行膨胀操作的
    def dilation(self):
        self.img = cv2.dilate(self.img, None, iterations=2)

    # BGR2GRAY是用来将彩色图转成灰度图的
    def BGR2GRAY(self):
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.Type = "灰度图"

    # GRAY2BIN 是用来将灰度图转成二值化图的
    def GRAY2BIN(self):
        _, self.img = cv2.threshold(self.img, 0, 255, cv2.THRESH_OTSU)
        self.Type = "二值化图"

    '''
        以下 change_ID、get_data、get_info、train、predict_init、predict函数都是用来进行人脸识别的
        change_ID: 用来获取想要进行人脸注册的人名
        get_data: 用来获取该人名对应的人脸图片
        get_info: 用来获取get_data得到的数据集中的人脸标签和信息
        train:  根据get_info的信息进行训练
        predict_init:初始化检测器
        predict: 进行预测
        示例1 获取数据集，训练，并进行预测：
        I = Img()
        I.camera(0)
        I.change_ID('JACK')
        I.get_data(50)
        I.train()
        I.predict_init()
        while True:
            I.get_img()
            I.predict()
            I.delay(1)
        示例2 直接读取某一个保存好的模型进行预测：
        I = Img()
        I.camera(0)
        I.predict_init('JACK')
        while True:
            I.get_img()
            I.predict()
            I.delay(1)
    '''

    def change_ID(self, ID):
        self.ID = ID
        self.data_path = dat_path + self.ID + '/'
        new_file(self.data_path)
        self.save_model_name = model_path + self.ID + '.yml'

    def get_data(self, pic_num=50, time=1):
        i = 0
        while True:
            if i >= pic_num:
                cv2.destroyAllWindows()
                break
            self.get_img()
            self.name_windows('img')
            self.show_image('img')
            pic_my_name = self.data_path + self.ID + '_' + str(i) + '.jpg'
            i += 1
            cv2.imwrite(pic_my_name, self.img)
            self.delay(time)

    def get_info(self):
        try:
            facesSamples = []
            ids = []
            self.data_ = dat_path
            self.names = []
            imgP = []
            file = os.listdir(self.data_)
            for i in range(len(file)):
                next_file_path = self.data_ + file[i] + '/'
                for f in os.listdir(next_file_path):
                    if f.split('.')[1] != 'jpg':
                        continue
                    self.names.append(file[i])
                    imgP.append(os.path.join(next_file_path, f))
            # print(self.names)
            # print(len(imgP), len(self.names))
            for im in range(len(imgP)):
                # 打开图片,黑白化
                PIL_img = Image.open(imgP[im]).convert('L')
                # 将图像转换为数组，以黑白深浅
                # PIL_img = cv2.resize(PIL_img, dsize=(400, 400))
                img_numpy = np.array(PIL_img, 'uint8')
                # 获取图片人脸特征
                faces = self.face_detector.detectMultiScale(img_numpy)
                # 获取每张图片的id和姓名

                # 预防无面容照片
                for x, y, w, h in faces:
                    ids.append(im)
                    facesSamples.append(img_numpy[y:y + h, x:x + w])
            self.faces = facesSamples
            self.ids = ids
            print('成功读取标签')
            return True
        except FileNotFoundError:
            print('请检查数据集是否在路径内')
            return False

    def train(self):
        self.get_info()
        self.recognizer.train(self.faces, np.array(self.ids))
        self.recognizer.write(self.save_model_name)
        print('训练完毕，模型已保存到：', self.save_model_name, '模型名称为：', self.ID)

    def predict_init(self, m_name=''):

        ret = self.get_info()
        if ret == False:
            return False

        model_name = self.save_model_name
        if len(m_name) != 0:
            model_name = model_path + m_name + '.yml'
        # print(model_name, type(model_name))
        if os.path.isfile(model_name):
            self.recognizer.read(model_name)
        # except:
        #     print('please get your model')

    def predict(self):
        try:
            img = self.img
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 转换为灰度
            face = self.face_detector.detectMultiScale(gray, 1.1, 5, cv2.CASCADE_SCALE_IMAGE, (100, 100), (300, 300))
            for x, y, w, h in face:
                cv2.rectangle(img, (x, y), (x + w, y + h), color=(0, 0, 255), thickness=2)
                cv2.circle(img, center=(x + w // 2, y + h // 2), radius=w // 2, color=(0, 255, 0), thickness=1)
                # 人脸识别
                ids, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                print('名字', str(self.names[ids - 1]), '置信值：', confidence)
                try:
                    if confidence > 80:
                        cv2.putText(img, 'unkonw', (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 1)
                    else:
                        cv2.putText(img, str(self.names[ids - 1]), (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                                    (0, 255, 0), 1)
                        self.face_name = str(self.names[ids - 1])
                except:
                    pass

            self.name_windows('face recognize result')
            self.show_image('face recognize result', img)
        except cv2.error:
            print('请到官网进行反馈')

    '''
        以下 face_detect_init、face_detect、face_cap、face_mask 是用来实现人脸检测以及给人脸戴帽子戴口罩的
        face_detect_init: 输入选择用来识别的人脸模型
        face_detect: 进行人脸检测
        face_cap: 调用face_detect，并对框出来的人脸进行贴图
        face_mask：同上
        示例1 人脸检测：
        I = Img()
        I.camera(0)
        I.face_detect_init('face')
        I.name_windows('output')
        while True:
            I.get_img()
            I.face_detect()
            I.show_image('output')
            I.delay(1)
        
        示例2 戴帽子（戴口罩同理）：
        I = Img()
        I.camera(0)
        I.face_detect_init('face')
        I.name_windows('output')
        while True:
            I.get_img()
            I.face_cap()
            I.show_image('output')
            I.delay(1)
        
    '''

    def face_detect_init(self, model_name):
        self.path = model_path + model_name + '.xml'
        self.cascade = cv2.CascadeClassifier(self.path)
        # self.color_data = 'no_people'

    def face_detect(self):
        self.color_data = '没有人'
        global move  # 用于调整帽子的位置

        def adjust(event, x, y, flags, param):  # 鼠标滑轮调整帽子和口罩的位置
            if event == cv2.EVENT_MOUSEWHEEL:
                global move
                try:
                    move += 10 if flags < 0 else -10
                except:
                    pass

        # img_new = cv2.flip(self.img, 1)
        img_new = np.copy(self.img)
        gray = cv2.cvtColor(img_new, cv2.COLOR_BGR2GRAY)  # 转换灰色
        faces = self.cascade.detectMultiScale(gray, 1.15, 5)  # 系数得调。
        if len(faces):  # 大于0则检测到人脸
            self.color_data = '有人'
            for (x, y, w, h) in faces:
                cv2.rectangle(img_new, (x, y), (x + w, y + h), (255, 0, 0), 2)
                if x > 0 and y > 0:
                    cv2.rectangle(img_new, (x, y), (x + w, y + h), (255, 0, 0), 1)
                    if self.flag_cap == 1 or self.flag_mask == 1:
                        try:
                            drc = cv2.imread(self.pht)
                            if self.flag_cap == 1:
                                hat1 = cv2.resize(drc, (w, y))  # 根据找到的人脸的大小修改帽子的大小
                                gray_hat = cv2.cvtColor(hat1, cv2.COLOR_BGR2GRAY)
                                ret, binary = cv2.threshold(gray_hat, 0, 1,
                                                            cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化的目的是把帽子旁边的白色外景去掉

                                hat1[binary == 1] = 0
                                img_new[y - hat1.shape[0] + move:y + move, x:x + hat1.shape[1]][hat1 != 0] = 0  # 把帽子抠出来
                                img_new[y - hat1.shape[0] + move:y + move, x:x + hat1.shape[1]] = img_new[
                                                                                                  y - hat1.shape[
                                                                                                      0] + move:y + move,
                                                                                                  x:x + hat1.shape[
                                                                                                      1]] + hat1  # 戴帽子

                            if self.flag_mask == 1:
                                mask1 = cv2.resize(drc, (w, int(2 * h // 3)))  # 根据找到的人脸的大小修改帽子的大小
                                gray_mask = cv2.cvtColor(mask1, cv2.COLOR_BGR2GRAY)
                                ret, binary = cv2.threshold(gray_mask, 245, 1,
                                                            cv2.THRESH_BINARY)  # 二值化的目的是把帽子旁边的白色外景去掉

                                mask1[binary == 1] = 0
                                img_new[y + h // 2 + move:y + h // 2 + mask1.shape[0] + move, x:x + mask1.shape[1]][
                                    mask1 != 0] = 0  # 把口罩抠出来
                                img_new[y + h // 2 + move:y + h // 2 + mask1.shape[0] + move,
                                x:x + mask1.shape[1]] = img_new[y + h // 2 + move:y + h // 2 + mask1.shape[0] + move,
                                                        x:x + mask1.shape[1]] + mask1  # 戴帽子

                        except:
                            move -= 10 if move > 0 else -10  # 防止帽子或口罩超出图片
        # self.img = img_new
        self.name_windows('face detect result')
        self.show_image('face detect result', img_new)

    def face_cap(self, path):
        self.pht = d_path + path + '.jpg'
        self.flag_cap = 1
        self.face_detect()

    def face_mask(self, path):
        self.pht = d_path + path + '.jpg'
        self.flag_mask = 1
        self.face_detect()

    '''
        以下 decodeDispaly、erweima_detect函数是用来实现扫描二维码功能的
        decodeDisplay: 解码
        erweima_detect:进行二维码检测
        示例：
        I = Img()
        I.camera(0)
        I.name_windows('img')
        while True:
            I.get_img()
            I.erweima_detect()
            I.show_image('img')
            print(I.QR_code_data)
            I.delay(1)
    '''

    def decodeDisplay(self, image):  # 解码部分
        barcodes = pyzbar.decode(image)
        img = self.img
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 5)
            cv2.circle(img, (int(x + w / 2), int(y + h / 2)), int(h / 2), (255, 0, 0), 5)
            barcodeData = barcode.data.decode("utf-8")
            self.er_data = barcodeData
            self.QR_code_data = self.er_data
        self.name_windows('Result of QRcode')
        self.show_image('Result of QRcode', img)

    def erweima_detect(self):
        img = self.img
        self.er_data = 'none'
        self.QR_code_data = self.er_data
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.decodeDisplay(gray)

    '''
        以下model_、onnx_detect_new、model_recognize函数是用来调用pt生成的模型的
        model_:默认初始化
        onnx_detect_new: 
        model_recognize: 
        示例：
        I = Img()
        I.camera(0)
        I.model_('lxy1007.proto')
        I.name_windows('img')
        while True:
            I.get_img()
            I.model_recognize()
            result = I.m_data
            I.show_image('img')
            I.delay(1)
    '''

    def model_(self, model_name='lxy1007.proto'):
        self.model = cv2.dnn.readNetFromONNX(model_path + model_name)  # 如'finally.proto'
        f = model_name.split(".")
        self.item = f[0]
        self.pro = 0
        self.m_data = 'none'

    def onnx_detect_new(self, img):
        # self.model_()
        img = np.asarray(img, dtype=np.float) / 255
        img = img.transpose(2, 0, 1)
        img = img[np.newaxis, :]
        self.model.setInput(img)
        pro = self.model.forward()
        e_x = np.exp(pro.squeeze() - np.max(pro.squeeze()))
        self.pro = e_x / e_x.sum()

    def model_recognize(self):
        frame = cv2.resize(self.img, (224, 224))
        self.onnx_detect_new(frame)
        if np.max(self.pro) > 0.9:
            classNum = np.argmax(self.pro)
            if classNum in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
                self.m_data = items_num[classNum]
            elif classNum in [9, 10]:
                self.m_data = items_dir[classNum]
            elif classNum == 11:
                self.m_data = items_label[classNum]
        else:
            self.m_data = 'none'

    '''
        beauty_face 函数是用来磨皮的
        
    '''

    def beauty_face(self):
        v1 = 3  # 磨皮程度
        v2 = 2  # 细节程度
        dx = v1 * 5  # 双边滤波参数之一
        fc = v1 * 12.5  # 双边滤波参数之一
        p = 0.1
        # 双边滤波
        copy = self.img
        temp1 = cv2.bilateralFilter(copy, dx, fc, fc)
        temp2 = cv2.subtract(temp1, copy)
        temp2 = cv2.add(temp2, (10, 10, 10, 128))
        # 高斯模糊
        temp3 = cv2.GaussianBlur(temp2, (2 * v2 - 1, 2 * v2 - 1), 0)
        temp4 = cv2.add(copy, temp3)
        dst = cv2.addWeighted(copy, p, temp4, 1 - p, 0.0)
        img = cv2.add(dst, (10, 10, 10, 255))
        self.name_windows('after_beauty')
        self.show_image('after_beauty', img)


    '''
       以下 color_detect_init、set_hsv、getpos、setcolorvalue、color_detect是用来进行颜色检测的

    '''

    def color_detect_init(self, color):
        self.color_data = 'none'  # 保存颜色的检测结果
        if color == 'red':
            self.color_list_lower = [0, 0, 10]  # 这是红色的数值  正常激光的  0, 0, 211
            self.color_list_upper = [10, 255, 255]
        elif color == 'green':
            self.color_list_lower = [35, 43, 46]
            self.color_list_upper = [77, 255, 255]
        elif color == 'yellow':
            self.color_list_lower = [26, 43, 46]
            self.color_list_upper = [34, 255, 255]
        elif color == 'blue':
            self.color_list_lower = [80, 43, 46]
            self.color_list_upper = [124, 255, 255]
        elif color == 'orange':
            self.color_list_lower = [11, 43, 46]
            self.color_list_upper = [25, 255, 255]
        elif color == 'black':
            self.color_list_lower = [0, 0, 0]
            self.color_list_upper = [180, 255, 46]
        elif color == 'white':
            self.color_list_lower = [0, 0, 221]
            self.color_list_upper = [180, 30, 255]
        elif color == 'gray':
            self.color_list_lower = [0, 0, 46]
            self.color_list_upper = [180, 43, 220]
        elif color == 'purple':
            self.color_list_lower = [125, 43, 46]
            self.color_list_upper = [155, 255, 255]
        elif color == 'qing':
            self.color_list_lower = [78, 43, 46]
            self.color_list_upper = [99, 255, 255]

        self.colorLower = np.array(self.color_list_lower)  # 这是红色的数值
        self.colorUpper = np.array(self.color_list_upper)
        self.color = color
        # 初始化追踪点的列表
        self.mybuffer = 16
        self.pts = deque(maxlen=self.mybuffer)
        self.counter = 0
        self.Hmax = self.Smax = self.Vmax = 0
        self.Hmin = self.Smin = self.Vmin = 255

    def set_hsv(self, color):
        image = self.img.copy()
        self.HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        cv2.imshow("imageHSV", self.HSV)
        cv2.imshow('image', image)
        cv2.setMouseCallback("imageHSV", self.getpos)
        cv2.waitKey(0)
        self.color_list_lower = [self.Hmax, self.Smax, self.Vmax]
        self.color_list_upper = [self.Hmin, self.Smin, self.Vmin]
        self.colorLower = np.array(self.color_list_lower)  # 这是红色的数值
        self.colorUpper = np.array(self.color_list_upper)
        self.color = color
        print(self.colorLower)
        print(self.colorUpper)

    def getpos(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:  # 定义一个鼠标左键按下去的事件
            print(self.HSV[y, x])
            if self.HSV[y, x][0] < self.Hmin:
                self.Hmin = self.HSV[y, x][0]
            if self.HSV[y, x][0] > self.Hmax:
                self.Hmax = self.HSV[y, x][0]
            if self.HSV[y, x][1] < self.Smin:
                self.Smin = self.HSV[y, x][1]
            if self.HSV[y, x][1] > self.Smax:
                self.Smax = self.HSV[y, x][1]
            if self.HSV[y, x][2] < self.Vmin:
                self.Vmin = self.HSV[y, x][2]
            if self.HSV[y, x][2] > self.Vmax:
                self.Vmax = self.HSV[y, x][2]

    def setcolorvalue(self, color, color_list_low, color_list_up):
        self.color_list_lower = color_list_low
        self.color_list_upper = color_list_up
        self.colorLower = np.array(self.color_list_lower)  # 这是红色的数值
        self.colorUpper = np.array(self.color_list_upper)
        self.color = color
        print('设置阈值成功，当前阈值为：', self.color_list_lower, self.color_list_upper)

    def color_detect(self):
        frame = self.img
        self.data = 'none'
        self.frame = frame
        self.img_new = frame
        # 转到HSV空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # cv2.imshow('hsv',hsv)
        # cv2.waitKey(40)
        # 根据阈值构建掩膜
        mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
        #         cv2.imshow('mask_original', mask)
        #         cv2.waitKey(40)
        # 腐蚀操作
        mask = cv2.erode(mask, None, iterations=2)
        # 膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        # 初始化识别物体圆形轮廓质心
        center = None
        # 如果存在轮廓
        if len(cnts) > 0:
            # 找到面积最大的轮廓
            c = max(cnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)  # 最大面积区域的外接矩形   x,y是左上角的坐标，w,h是矩形的宽和高
            # print('x,y,w,h',x,y,w,h)
            if w > 60 and h > 60:  # 宽和高大于一定数值的才要。
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
                cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 255), 2)
                #print('{0}',format(x))
                if x < 0 or y < 0:
                    # self.img_new=frame_bgr
                    self.img_new = frame
                else:
                    self.img_new = frame_bgr[y:y+h,x:x+w]
                    self.img_new = frame[y:y + h, x:x + w]
                    # self.img = self.img_new
                cv2.imshow('result', self.img_new)
                cv2.waitKey(3)

            # 确定面积最大的轮廓的外接圆
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            self.x = x
            self.y = y
            self.radius = radius
            # 计算轮廓的矩
            M = cv2.moments(c)
            # 计算质心
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # 只有当半径大于100mm时，才执行画图
            if radius > 5:
                # img_circle=cv2.circle(self.frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                # cv2.circle(self.frame, center, 5, (0, 0, 255), -1)

                # 把质心添加到pts中，并且是添加到列表左侧
                self.pts.appendleft(center)
                # cv2.imshow('color1', self.frame)
                # cv2.waitKey(1)
                self.color_data = self.color
                #魔改魔改魔改魔改魔改魔改魔改魔改魔改
                X = x+w/2 ;Y = y+h/2  #中心点坐标
                '''
                if X > 250：
                    self.side = 'right'
                elif X <250:
                    self.side = 'left'
                else:
                    self.side = 'mid'
                self.tan = (Y-250)/(X-250)
                '''
                self.distance = ((X-250)**2+(Y-250)**2)**0.5
                self.midle = [X,Y]   #检测后返回红点的中心值

        else:  # 如果图像中没有检测到识别物体，则清空pts，图像上不显示轨迹。
            self.pts.clear()
            # cv2.imshow('color2', self.frame)
            # cv2.waitKey(1)
            self.color_data = 'other_color'
            self.midle = [0,0]
            self.distance = 0
            #self.tan = 0
            #self.side = 'none'
    '''
        以下是彬锋师兄于2021年初写的视觉函数，用于重庆杯的比赛内容
    '''

    # 二值化图寻迹
    def offset_calculate1(self, y=-1, img=[]):
        if len(img) == 0:
            img = self.img
        if -1 == y:
            y = img.shape[0]
            y = y // 2
        line = img[y]
        white_count = np.sum(line == 0)
        white_index = np.where(line == 0)
        if white_count == 0:
            return 0
        center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
        # 求图像中心
        img_width = self.img.shape[1]
        img_center = img_width // 2
        direction = center - img_center
        direction = int(direction)
        return direction

    def line_angle1(self, img=[]):
        if len(img) == 0:
            img = self.img
        h = img.shape[0]
        up = []
        down = []
        for i in range(0, h // 2, 10):
            up.append(self.offset_calculate1(i))
        for i in range(h // 2, h, 10):
            down.append(self.offset_calculate1(i))
        a = sum(up) // len(up)
        b = sum(down) // len(down)
        angle = (a - b) // 180
        return angle

    def offset1(self, img=[]):
        if len(img) == 0:
            img = self.img
        y = img.shape[0]
        line = img[y // 2]
        white_count = np.sum(line == 0)
        white_index = np.where(line == 0)
        if white_count == 0:
            return False
        else:
            return True

    def dotted_line1(self, img=[]):
        if len(img) == 0:
            img = self.img
        cnts = self.bin_detect(img)
        x = []
        for c in cnts:
            area = self.cnt_area(c)
            M = cv2.moments(c)
            if area > 3000:
                cx = int(M["m10"] / M["m00"])
                x.append(cx)
        if len(x) < 2:
            return False
        a = np.std(np.array(x))
        if a > 150:
            return False
        else:
            return True

    # 彩色图寻迹

    def offset_calculate2(self):
        gray = cv2.cvtColor(self.img.copy(), cv2.COLOR_BGR2GRAY)
        retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        img = cv2.dilate(dst, None, iterations=2)
        h = img.shape[0]
        direction = self.offset_calculate1(h // 2, img)
        return direction

    def line_angle2(self):
        gray = cv2.cvtColor(self.img.copy(), cv2.COLOR_BGR2GRAY)
        retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        img = cv2.dilate(dst, None, iterations=2)
        angele = self.line_angle1(img)
        return angele

    def offset2(self):
        gray = cv2.cvtColor(self.img.copy(), cv2.COLOR_BGR2GRAY)
        retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        img = cv2.dilate(dst, None, iterations=2)
        result = self.offset1(img)
        return result

    def dotted_line2(self):
        gray = cv2.cvtColor(self.img.copy(), cv2.COLOR_BGR2GRAY)
        retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        img = cv2.dilate(dst, None, iterations=2)
        result = self.dotted_line1(img)
        return result

    def cnt_area(self, cnt):
        area = cv2.contourArea(cnt)
        return area

    def detect(self, c, Shape):
        # 定义形状名称和判断近似形状
        shape = "未知形状"
        peri = cv2.arcLength(c, True)  # 周长
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        r1 = peri / 6.2  # 半径
        area = cv2.contourArea(c)  # 面积
        r2 = (area / 3.14) ** 0.5
        if abs(r1 - r2) < 0.22 * r1 and len(approx) > 4:
            shape = "圆形"
        elif len(approx) == 3:
            shape = "三角形"
        # 判断四边形是正方形还是长方形
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "正方形" if ar >= 0.95 and ar <= 1.05 else "长方形"
        else:
            pass
        return (shape == Shape)

    def bin_detect(self, img=[]):
        if len(img) == 0:
            img = self.img
        # 在阈值图像中查找轮廓并初始化形状检测器
        cnts = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        max_cnts = []
        for c in cnts:
            area = self.cnt_area(c)
            if area > 2000:
                max_cnts.append(c)
        return max_cnts

    def cnt_draw(self, c, shape):
        M = cv2.moments(c)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        cv2.drawContours(self.img, [c], -1, (0, 255, 0), 2)
        cv2.putText(self.img, shape, (cx, cy), 0, 2, (0, 255, 0), 3)

    def cnt_center(self, c):
        M = cv2.moments(c)
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return [cx, cy]

if __name__ == '__main__':
    a = Img()
    a.camera(0)
    a.color_detect_init('blue')
    while True:
        a.get_img()
        a.BGR2GRAY()
        a.GRAY2BIN()
        a.name_windows('yyj')
        a.show_image('yyj')
        a.delay(1)

