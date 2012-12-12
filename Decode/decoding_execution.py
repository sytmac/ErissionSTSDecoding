
# -*- coding: utf-8 -*-
'''/
author :SongYang
'''
import json
from  decode import STSdecode
from config.STSDefinitions import DefinitionsToDictionary
from config.settings import LEVELTYPE_LIST, RECORD_COUNTER, EXCEPTION_MESSAGE, WARNING_MESSAGE 
import datetime
import re , sys
encoding = sys.getfilesystemencoding()
def stsdef_operation(s_defpath):
    '''/
     将STS定义文件进行字典索引
    '''
    def_dictionary = DefinitionsToDictionary(s_defpath)
    def_dictionary.levelclassify()    
def samefile_into_list(input_filepath,s_list):
    '''
    首先顺序找到同一份文件的文件名，放进列表进行处理
    针对一次性处理的文件进行字典索引，字典的键是每个文件名按照‘_’来分割的第一部分第二部分组成组成键
    '''
    print "input_filepath:",input_filepath
    file_dictionary = {}
    for i in range(0 , len(s_list)):
        file_dictionary[s_list[i].split('_')[0]+s_list[i].split('_')[1]] = []
    for i in range(0 , len(s_list)):
        s_index = s_list[i].split('_')[0]+s_list[i].split('_')[1]
        file_dictionary[s_index].append(input_filepath+s_list[i])
    return file_dictionary

def decoding_worker(filelist , result_path , guid):
    '''/
    解析进程，调用STSdecode类进行解析作业
    ''' 
    decode = STSdecode(filelist , result_path , guid)
    decode.decoding()
    decode.objtype_into_samelevlist()
    decode.sameleveltableintoonetable()
def computetheday(s_date):
    '''/
    计算输入日期所在周的星期一的日期，输入的格式例如“20130213”
    '''
    regex = '([1][6-9]|[2-9][0-9])[0-9][0-9]([0][1-9]|[1][0-2])([0-2][1-9]|[1-3][0-1])'
    if(re.match(regex , s_date)):
        s_c = int(s_date[:2])
        s_year = int(s_date[2:4])
        s_month = int(s_date[4:6])
        s_day = int(s_date[6:8])
        if s_month == 1 or s_month == 2:
            s_month = s_month+12
            s_year = s_year-1
            if s_year < 0:
                s_year = 99
                s_c = s_c -1
        s_w = s_year+(s_year//4)+(s_c//4)-2*s_c+26*(s_month+1)//10+s_day-1
        l_margin = [-6 , 0 , -1 , -2 , -3 , -4 , -5]
        s_monday = str(datetime.date(int(s_date[:4]) , s_month , s_day)
                       +datetime.timedelta(days = l_margin[s_w%7]))
        s_monday = s_monday[:4]+s_monday[5:7]+s_monday[8:]
        return  str(s_monday) 
def json_packaging(filepath,jsonfile_path):
    '''/
    封装json串返回给前台，输入参数为需要一次性解析的文件路径
    '''
    slevel_dictionary = {}
    levlength = len(LEVELTYPE_LIST)
    for i in range(0 , levlength):
        slevel_dictionary[LEVELTYPE_LIST[i]] = []
        json_dictionary = {}
        filename = filepath.split('\\')[-1]
        filedatetime = filename[1:9]
        monday_date = computetheday(filedatetime)        
        date = monday_date[0:4]+'-'+monday_date[4:6]+'-'+monday_date[6:8]
        json_dictionary["DataStartTime"] = date+' 00:00:00'
        json_dictionary["Interval"] = str(3600*24*7)
        json_dictionary["SaveFileName"] = filepath
        json_dictionary["FileName"] = LEVELTYPE_LIST[i]
        json_dictionary["SuccessCount"] = RECORD_COUNTER[LEVELTYPE_LIST[i]]
        slevel_dictionary[LEVELTYPE_LIST[i]].append(json_dictionary)
        slevel_dictionary["Exception"] = EXCEPTION_MESSAGE
        slevel_dictionary["Warning"] = WARNING_MESSAGE
    fp = open(jsonfile_path , 'w')
    fp.write(json.dumps(slevel_dictionary , indent = 4))
    fp.close()
