import os
import pandas as pd
import json
import sys

system_platform = sys.platform
main_path = '/home/pi/class/'  # 读取和保存文件所用主文件夹
if 'win' in system_platform:
    file_path = os.getcwd()
    # 获取当前文件的位置
    main_path = file_path + '/resources/assets/class/'
f_path = 'file_operation/'


class Common_file:
    # 赋值（f）为txt文件（example.txt），打开方式为【那三个】
    def __init__(self, file_name, mode):
        self.file_name = main_path + f_path + file_name
        self.file = open(self.file_name, mode, encoding='utf-8')
        if mode == 'w':
            print('警告：使用写入模式会清除原文件所有内容！')
            input('请输入任意字符继续：')

    # 关闭文件（f）
    def close(self):
        self.file.close()
        print('文件已关闭')

    # 文件（f）中所有内容
    def read_all(self):
        return self.file.read()

    # 文件（f）中的当前行
    def read_a_line(self):
        return self.file.readline()

    # 文件（f）中的所有行
    def read_all_lines(self):
        return self.file.readlines()

    # 文件（f）跳到下一行
    def nextline(self):
        next(self.file)

    # 文件（f）中当前读取位置
    def tell(self):
        return self.file.tell()

    # 文件（f）回到初始读取位置
    def seek(self):
        self.file.seek(0)

    # 向文件（f）写入内容（message）
    def write(self, message):
        self.file.write(message)

    # 向文件（f）写入序列（line）
    def write_lines(self, lines):
        self.file.writelines(lines)


# 赋值（f）为json文件（example.json），打开方式为【那三个】
class Json(Common_file):
    # json文件（f）中所有内容
    def load(self):
        return json.load(self.file)

    # 向json文件（f）中写入内容（message）
    def dump(self, message):
        json.dump(message,self.file)


class CSV():
    # 赋值（f）为csv文件（example.csv)
    def __init__(self,file_name):
        self.file_name = main_path + f_path + file_name
        self.csv = pd.read_csv(self.file_name, encoding='utf-8')
        # csv文件（f）的形状
        self.shape = self.csv.shape()

    # 打印csv文件（f）中前（数字head，默认5）行
    def print_head(self,head):
        print(self.csv.head(head))

    # 打印csv文件（f）中后（数字tail，默认5）行
    def print_tail(self,tail):
        print(self.csv.tail(tail))

    # 打印csv文件（f）中的汇总统计
    def print_describe(self):
        print(self.csv.describe())

    # csv文件（f）中第（数字row，默认0，下同）行
    def get_a_row(self,row):
        return self.csv.iloc[row,:]

    # csv文件（f）中第（数字column）列
    def get_a_column(self,column):
        return self.csv.iloc[:,column]

    # csv文件（f）中第（数字row）行、第（数字column）列的元素
    def get_directory(self,row,column):
        return self.csv.iloc[row,column]

    # 删除csv文件（f）中的所有空白值
    def dropna(self):
        self.csv.dropna()

    # 用（x）替换csv文件（f）中的所有空白值
    def fillna(self,x):
        self.csv.fillna(x)
