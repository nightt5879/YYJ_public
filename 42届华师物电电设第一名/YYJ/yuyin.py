#!/usr/local/bin/python3

from aip.speech import AipSpeech
import os
import wave
import time
import pyaudio
import audioop
import pygame
# import base64
import requests
import urllib
import sys
import random
from importlib import reload
#/home/pi/Desktop/A Group 12.11/record/10.mp3
system_platform = sys.platform
main_path = '/home/pi/Desktop/'  # 读取和保存文件所用主文件夹
if 'win' in system_platform:
    # 获取当前文件的位置
    file_path = os.getcwd()
    main_path = file_path + '\\resources\\assets\\class\\'
    # main_path = 'F:\\1018software\\release\\win-unpacked\\resources\\assets\\class\\'
txt_path = main_path + 'txt\\'  # 文本文件夹
audio_path = main_path + 'A Group 12.11/record/'  # 音频文件夹
if os.path.exists(audio_path) == False:
    os.makedirs(audio_path)
try:
    # 开始时删除所有合成音频--Nonexxxxxxx.mp3/wav(固定格式)
    for i in os.listdir(audio_path):
        type = i.split('.')
        if type[0][4:].isdigit():  # 因为软件创建变量时默认定义为None，所以从第5个字符开始判断
            os.remove(audio_path + i)
except FileNotFoundError as e:
    print(e)
    print('无法进行数据删除')
    sys.exit()

# 百度API账号
app_id = '19925995'
app_key = '7GRa93EkYrOyFTfDkjHdl9WH'
app_secret_key = 'Q5qIyUFKP7U2ktBE4Y5oSUcom2x2v8sT'


def TxtWrite(idd, key, secret):
    global app_id
    global app_key
    global app_secret_key
    app_id = idd
    app_key = key
    app_secret_key = secret


class Yuyin():
    def __init__(self):

        self.app_id = app_id
        self.api_key = app_key
        self.secret_key = app_secret_key

        self.p = pyaudio.PyAudio()

        self.client = AipSpeech(self.app_id, self.api_key, self.secret_key)

        # 语速和音量和音高（频率）
        self.vol = 9  # 感觉并没有什么特别大的差别
        self.spd = 5  # 数值一般为0-10
        self.per = 4  # 默认女声（数值只能0-5，但是除了男女声之外差别不大）

    #
    def TxtWrite(self, idd='', key='', secret=''):
        self.app_id = idd
        self.api_key = key
        self.secret_key = secret

    def change_vol_spd_gender(self, vol, spd, per):
        self.vol = 2 * vol - 1
        self.spd = 2 * spd - 1
        if per == 'man':
            self.per = 3
        elif per == 'woman':
            self.per = 4

    def chat(self, my_text):
        iner_url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'
        url = iner_url.format(urllib.parse.quote(my_text))
        html = requests.get(url)
        self.chat_ret = html.json()["content"]

    # 读取文件并保存为字符串
    def TxtRead(self, filename):
        f = open(filename, "r")
        txt = f.read()
        f.close()
        return txt

    # 修改成语音文件格式到适合百度语音api
    def downsampleWav(self, src, dst, inrate=48000, outrate=16000, inchannels=1, outchannels=1):
        if not os.path.exists(src):
            print('没有旧音频文件')
            return False

        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))

        try:
            s_read = wave.open(src, 'rb')
            params = s_read.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            # print(nchannels,sampwidth, framerate,nframes)
            s_write = wave.open(dst, 'wb')
        except:
            print('打开旧音频文件失败')
            return False

        n_frames = s_read.getnframes()
        data = s_read.readframes(n_frames)

        try:
            converted = audioop.ratecv(data, 2, inchannels, inrate, outrate, None)
            if outchannels == 1 and inchannels != 1:
                converted = audioop.tomono(converted[0], 2, 1, 0)
        except:
            print('转换格式失败')
            return False

        try:
            s_write.setparams((outchannels, 2, outrate, 0, 'NONE', 'Uncompressed'))
            s_write.writeframes(converted[0])
        except Exception as e:
            print(e)
            print('保存新音频失败')
            return False

        try:
            s_read.close()
            s_write.close()
        except:
            print('无法关闭音频文件')
            return False
        return True

    # 录音file_name路径文件名,TIME录音时间长度
    def my_record(self, TIME, file_name):  # 录音保存到.wav文件
        CHUNK = 2000  # 采样点
        FORMAT = pyaudio.paInt16
        CHANNELS = 1  # 声道
        RATE = 48000  # 采样率
        # RECORD_SECONDS = 2  # 采样宽度2bytes

        self.timeTickStr = str(round(time.time()))
        file_name = audio_path + str(file_name) + self.timeTickStr + '.wav'

        stream = self.p.open(format=FORMAT,
                             channels=CHANNELS,
                             rate=RATE,
                             input=True,
                             frames_per_buffer=CHUNK)

        print("开始录音,请说话......")

        frames = []
        t = time.time()
        while time.time() < t + TIME:
            data = stream.read(CHUNK)
            frames.append(data)

        print("录音结束!")

        stream.stop_stream()
        stream.close()
        # p.terminate()

        wf = wave.open(file_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        file_new_name = audio_path + 'new.wav'
        self.downsampleWav(file_name, file_new_name)
        os.remove(file_name)
        os.rename(file_new_name, file_name)

    # 语音识别返回识别结果字符串   中文普通话识别的免费次数为50000次。
    def stt(self, filename):  # 识别.wav文件中的语音
        try:
            filename = audio_path + str(filename) + self.timeTickStr + '.wav'
            fp = open(filename, 'rb')
            FilePath = fp.read()
            fp.close()
        except:
            print(filename + "音频文件不存在或格式错误")
        finally:
            try:
                # 识别本地文件
                result = self.client.asr(FilePath,
                                         'wav',
                                         16000,
                                         {'dev_pid': 1537, }  # dev_pid参数表示识别的语言类型，1536表示普通话
                                         )
                # 解析返回值，打印语音识别的结果
                if result['err_msg'] == 'success.':
                    word = result['result'][0]  # utf-8编码
                    print('8030')
                    return word  # 返回识别结果值
                else:
                    print("语音识别失败:" + filename)
                    return "语音识别失败"
            except:
                print("没有连接网络")
                return "没有连接网络"

    # 将文本转为音频  语音合成免费额度只有5000次（未认证），认证之后有50000次，在180天内有效
    def tts(self, txt, filename):
        self.timeTickStr = str(round(time.time()))
        if len(txt) != 0:
            word = txt
            # try:
            result = self.client.synthesis(word, 'zh', 1, {
                'vol': self.vol, 'per': self.per, 'spd': self.spd, 'plt': 13
            })
            # 合成正确返回audio.mp3，错误则返回dict
            if not isinstance(result, dict):
                with open(audio_path + str(filename) + self.timeTickStr + '.mp3', 'wb') as f:
                    f.write(result)
                    print('8030')
                    print('文字转音频成功:' + txt)
            else:
                print('文字转音频失败!')

    #         except:
    #             print('没有连接网络')

    def play_bufen(self, filename, play_time):
        pygame.mixer.init(frequency=16000, size=-16, channels=1, buffer=2000)
        track = pygame.mixer.music.load(audio_path + filename)
        pygame.mixer.music.play()
        time.sleep(play_time)
        pygame.mixer.music.stop()

    # 播放音频及音乐
    def play_music(self, filename, type='.mp3', model=1, flag=0, time=0):
        # 只能播放.mp3文件  model=1是播放音乐，=0是播放音频文件  flag=0是播放全部，=1是播放部分。 time是播放音乐多长时间。
        #         try:
        #             try:
        pygame.mixer.init(frequency=16000, size=-16, channels=1, buffer=2000)
        filename = str(filename) + type
        if type == '.wav':
            track = pygame.mixer.Sound(audio_path + filename)
            track.play()  # 循环次数loops，开始时间start

        elif type == '.mp3':
            if model == 0:  # 播放音频
                track = pygame.mixer.music.load(audio_path + filename)
                pygame.mixer.music.play()  # 循环次数loops，开始时间start

            elif model == 1:  # 播放音乐
                track = pygame.mixer.music.load(audio_path + filename)
                if flag == 0:  # 播放全部
                    pygame.mixer.music.play()  # 循环次数loops，开始时间start
                    while pygame.mixer.music.get_busy():  # 等待播放完毕
                        if pygame.mixer.music.get_busy() == 0:
                            break

                else:  # 播放部分
                    self.play_bufen(filename, time)

    # 播放文本
    def play_txt(self, txt):
        tmp = None
        self.tts(txt, tmp)
        self.play_music(tmp)


#             except:
#                 print('没有这个音频文件:'+filename)
#         except:
#             print('没有打开音响')

# 测试录音+语音识别
# '''
# s=Yuyin()
# s.my_record(3,"1")
# txt=s.stt("1")
# print(txt)
# '''
# '''
# #测试文本转语音
# s=Yuyin()
# s.tts('The dog is eating shits!',"c4")  #tts保存为mp3格式
# s.play_music("c4.mp3")
# '''
# '''
# s=Yuyin()
# s.play_music("Build a temporary bridge.mp3")
# '''

if __name__ == "__main__":
    # # 聊天机器人示例
    # audio = None
    # audio2 = None
    # a = 0
    # s = Yuyin()
    # while True:
    #     a += 1
    #     s.my_record(1, audio)
    #     txt = s.stt(audio)
    #     s.chat("你好" + str(a))
    #     s.tts(s.chat_ret, audio2)
    #     s.play_music(audio2)

    # # 循环播报
    # # s = Yuyin()
    # audio = None
    # c4 = None
    # while True:
    #     s = Yuyin()
    #     s.my_record(1, c4)
    #     a = random.randint(1, 20)
    #     b = random.randint(1, 20)
    #     ab = ''.join([str(x) for x in [a, '加', b, '等于']])
    #     print(ab)
    #     s.tts(ab, audio)
    #     s.play_music(audio)

    # # 测试文本转语音
    # c4 = None
    # s = Yuyin()
    # s.tts('你好个头', c4)  #tts保存为mp3格式
    # s.play_music(c4)

    # # 测试录音+语音识别
    # c4 = None
    # s = Yuyin()
    # s.my_record(3, c4)
    # txt = s.stt(c4)
    # print(txt)
    # s.play_music(c4)

    # # 改变语音的语速音量音高
    # c4 = None
    # s = Yuyin()
    # s.change_vol_spd_gender(3, 3, '3')
    # s.tts('你好个头', c4)  #tts保存为mp3格式
    # s.play_music(c4)

    # 播放文本
    s = Yuyin()
    s.change_vol_spd_gender(5, 3, 'woman')
    s.play_txt('雷猴啊哈哈哈')
