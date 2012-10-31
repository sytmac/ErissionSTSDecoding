#! /usr/bin/env python
#coding=utf-8
from STSDefinitions  import *
from  settings import *
from  decode import STS_decode
import threading
import os
#调用decode函数
path="D:\\Users\\sytmac\\Desktop\\STS\\STS\\"
file_path ="D:\Users\sytmac\Desktop\STS\STS"
file_list=os.listdir(path)
file_dictionary={}#针对一次性处理的文件进行字典索引，字典的键是每个文件名按照‘_’来分割的第一部分第二部分组成组成键
#将STS定义文件进行字典索引
def Def(DefPath):
    d=DefinitionsToDictiionary(DefPath)
    d.Level_Classify()    
def TheSameFileIntoList(list):
    #首先顺序找到同一份文件的文件名，放进列表进行处理
    global file_list
    global file_dictionary
    for i in range(0,len(file_list)):
        file_dictionary[file_list[i].split('_')[0]+file_list[i].split('_')[1]]=[]
    for i in range(0,len(file_list)):
        file_dictionary[file_list[i].split('_')[0]+file_list[i].split('_')[1]].append(path+file_list[i])
#解析进程，采取循环多线程调用
def decoding_start(filelist):
    decode=STS_decode(filelist)
    decode.decoding()
    decode.ObjectTypeiIntoSameLevelList()
    decode.SameLevelTabelintoOneTable()
    
d=DefinitionsToDictiionary("D:\Users\sytmac\Desktop\STSDefinitions.xls")
d.Level_Classify()
TheSameFileIntoList(file_list)
key_list=file_dictionary.keys()
for i in range(0,len(key_list)):
    decoding_start(file_dictionary[key_list[i]])#给函数传进去一个list，这个list是属于一个文件的 分割文件 名称列表
