#! /usr/bin/env python
#coding=utf-8
'''/
author :SongYang
'''
from config.STSDefinitions import DefinitionsToDictionary
from  decode import STSdecode
import os
#调用decode函数
S_PATH = r"D:\\Users\\sytmac\\Desktop\\STS\\STS\\"
D_DEF_PATH = r'D:\Users\sytmac\Desktop\STSDefinitions.xls'
S_FILELIST = os.listdir(S_PATH)
S_FILE_DICTIONARY = {}#针对一次性处理的文件进行字典索引，字典的键是每个文件名按照‘_’来分割的第一部分第二部分组成组成键

def f_def(s_defpath):
    '''/
     将STS定义文件进行字典索引
    '''
    d_def_dictionary = DefinitionsToDictionary(s_defpath)
    d_def_dictionary.f_level_classify()    
def f_samefileintolist(s_list):
    '''/
    首先顺序找到同一份文件的文件名，放进列表进行处理
    '''
    for i in range(0 , len(s_list)):
        S_FILE_DICTIONARY[s_list[i].split('_')[0]+s_list[i].split('_')[1]] = []
    for i in range(0 , len(s_list)):
        s_index = s_list[i].split('_')[0]+s_list[i].split('_')[1]
        S_FILE_DICTIONARY[s_index].append(S_PATH+s_list[i])

def decoding_start(filelist):
    '''/
    解析进程，采取循环多线程调用
    ''' 
    decode = STSdecode(filelist)
    decode.f_decoding()
    decode.f_objtype_into_samelevlist()
    decode.f_sameleveltableintoonetable()
    

f_def(D_DEF_PATH)
f_samefileintolist(S_FILELIST)
L_KEYLIST = S_FILE_DICTIONARY.keys()
for key in range(0 , len(L_KEYLIST)):
    #给函数传进去一个list，这个list是属于一个文件的 分割文件 名称列表
    decoding_start(S_FILE_DICTIONARY[L_KEYLIST[key]])
