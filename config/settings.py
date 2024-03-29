#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''/
author :SongYang
'''

EXCEPTION_MESSAGE = []
WARNING_MESSAGE   = []
LEVELTYPE_LIST = ["STSBSC" , "STSTRA" , "STSCELL" , "STSHOINT" , "STSHOEXT" , "STSMOTS" , "STSLAPD"]


#记录definition表中counter的顺序，方便按照顺序写入文件 入数据库
FILETABLE = {}
FILETABLE["STSBSC"]   = []
FILETABLE["STSTRA"]   = []
FILETABLE["STSCELL"]  = []
FILETABLE["STSHOINT"] = []
FILETABLE["STSHOEXT"] = []
FILETABLE["STSMOTS"]  = []
FILETABLE["STSLAPD"]  = []
#计数器，每张表成功插入多少条数据
RECORD_COUNTER={}
RECORD_COUNTER["STSBSC"]=0
RECORD_COUNTER["STSTRA"]=0
RECORD_COUNTER["STSCELL"]=0
RECORD_COUNTER["STSHOINT"]=0
RECORD_COUNTER["STSHOEXT"]=0
RECORD_COUNTER["STSMOTS"]=0
RECORD_COUNTER["STSLAPD"]=0

#根据OBJTYPE和Level生成对应的字典
OBJ_LEVEL_DICTIONARY = {}
 
#根据level分成7个不同的字典.字典对应的是counter:ObjectType
STSBSC_DICTIONARY = {}
STSTRA_DICTIONARY = {}
STSCELL_DICTIONARY = {}
STSLAPD_DICTIONARY = {}
STSMOTS_DICTIONARY = {}  
STSHOINT_DICTIONARY = {}
STSHOEXT_DICTIONARY = {}

#COUNTER_OT_DICTIONARY是一个字典它对应的键值是它的key所对应的一个字典，字典里面的是Counter 和 OT对应的索引
COUNTER_OT_DICTIONARY = {}
COUNTER_OT_DICTIONARY["STSBSC"] = STSBSC_DICTIONARY
COUNTER_OT_DICTIONARY["STSTRA"] = STSTRA_DICTIONARY
COUNTER_OT_DICTIONARY["STSCELL"] = STSCELL_DICTIONARY
COUNTER_OT_DICTIONARY["STSHOINT"] = STSHOINT_DICTIONARY
COUNTER_OT_DICTIONARY["STSHOEXT"] = STSHOEXT_DICTIONARY
COUNTER_OT_DICTIONARY["STSMOTS"] = STSMOTS_DICTIONARY
COUNTER_OT_DICTIONARY["STSLAPD"] = STSLAPD_DICTIONARY

#定义表结构 所有相同的LEVEL的数据放到同一个LIST中 之后每个LIST中根据不同的OT在LIST中添加OTLIST。

#根据同一个level的不同OT进行列表分级
DICTIONARY_OT = {}

#链表中的链表是根据OT不同而划分的
DICTIONARY_LEVEL_TO_OTLIST = {}
STSBSC_LIST = []
STSTRA_LIST = []
STSCELL_LIST = []
STSHOINT_LIST = []
STSHOEXT_LIST = []
STSMOTS_LIST = []
STSLAPD_LIST = []

DICTIONARY_LEVEL_TO_OTLIST["STSBSC"] = STSBSC_LIST
DICTIONARY_LEVEL_TO_OTLIST["STSTRA"] = STSTRA_LIST
DICTIONARY_LEVEL_TO_OTLIST["STSCELL"] = STSCELL_LIST
DICTIONARY_LEVEL_TO_OTLIST["STSHOINT"] = STSHOINT_LIST
DICTIONARY_LEVEL_TO_OTLIST["STSHOEXT"] = STSHOEXT_LIST
DICTIONARY_LEVEL_TO_OTLIST["STSMOTS"] = STSMOTS_LIST
DICTIONARY_LEVEL_TO_OTLIST["STSLAPD"] = STSLAPD_LIST

#根据解析文件中的每个level的OT进行记录
DICTIONARY_LIST_OT_NAME = {}
STSBSC_OT_LIST = []
STSTRA_OT_LIST = []
STSCELL_OT_LIST = []
STSHOINT_OT_LIST = []
STSHOEXT_OT_LIST = []
STSMOTS_OT_LIST = []
STSLAPD_OT_LIST = []

DICTIONARY_LIST_OT_NAME["STSBSC"] = STSBSC_OT_LIST
DICTIONARY_LIST_OT_NAME["STSTRA"] = STSTRA_OT_LIST
DICTIONARY_LIST_OT_NAME["STSCELL"] = STSCELL_OT_LIST
DICTIONARY_LIST_OT_NAME["STSHOINT"] = STSHOINT_OT_LIST
DICTIONARY_LIST_OT_NAME["STSHOEXT"] = STSHOEXT_OT_LIST
DICTIONARY_LIST_OT_NAME["STSMOTS"] = STSMOTS_OT_LIST
DICTIONARY_LIST_OT_NAME["STSLAPD"] = STSLAPD_OT_LIST

#记录OT_columnName 每一种OT解析出来的表含有不同的列明 需要将列明跟定义表中的counter进行对比没有的话则不写进组合表中
DICTIONARY_OT_COLUMNNAME = {}
STSBSC_OT_COLUMNNAME = {}
STSTRA_OT_COLUMNNAME = {}
STSCELL_OT_COLUMNNAME = {}
STSHOINT_OT_COLUMNNAME = {}
STSHOEXT_OT_COLUMNNAME = {}
STSMOTS_OT_COLUMNNAME = {}
STSLAPD_OT_COLUMNNAME = {}

DICTIONARY_OT_COLUMNNAME["STSBSC"] = STSBSC_OT_COLUMNNAME
DICTIONARY_OT_COLUMNNAME["STSTRA"] = STSTRA_OT_COLUMNNAME
DICTIONARY_OT_COLUMNNAME["STSCELL"] = STSCELL_OT_COLUMNNAME
DICTIONARY_OT_COLUMNNAME["STSHOINT"] = STSHOINT_OT_COLUMNNAME
DICTIONARY_OT_COLUMNNAME["STSHOEXT"] = STSHOEXT_OT_COLUMNNAME
DICTIONARY_OT_COLUMNNAME["STSMOTS"] = STSMOTS_OT_COLUMNNAME
DICTIONARY_OT_COLUMNNAME["STSLAPD"] = STSLAPD_OT_COLUMNNAME

#
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL = {}
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSBSC"] = []
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSTRA"] = []
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSCELL"] = []
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSHOINT"] = []
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSHOEXT"] = []
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSMOTS"] = []
DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSLAPD"] = []