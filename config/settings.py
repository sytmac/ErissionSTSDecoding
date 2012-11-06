#! /usr/bin/env python
#coding=utf-8
'''/
author :SongYang
'''
L_LEVELTYPE_LIST = ["STSBSC" , "STSTRA" , "STSCELL" , "STSHOINT" , "STSHOEXT" , "STSMOTS" , "STSLAPD"]
#根据OBJTYPE和Level生成对应的字典
D_OBJ_LEVEL_DICTIONARY = {}
 
#根据level分成7个不同的字典.字典对应的是counter:ObjectType
D_STSBSC_DICTIONARY = {}
D_STSTRA_DICTIONARY = {}
D_STSCELL_DICTIONARY = {}
D_STSLAPD_DICTIONARY = {}
D_STSMOTS_DICTIONARY = {} 
D_STSHOINT_DICTIONARY = {}
D_STSHOEXT_DICTIONARY = {}

#D_COUNTER_OT_DICTIONARY是一个字典它对应的键值是它的key所对应的一个字典，字典里面的是Counter 和 OT对应的索引
D_COUNTER_OT_DICTIONARY = {}
D_COUNTER_OT_DICTIONARY["STSBSC"] = D_STSBSC_DICTIONARY
D_COUNTER_OT_DICTIONARY["STSTRA"] = D_STSTRA_DICTIONARY
D_COUNTER_OT_DICTIONARY["STSCELL"] = D_STSCELL_DICTIONARY
D_COUNTER_OT_DICTIONARY["STSHOINT"] = D_STSHOINT_DICTIONARY
D_COUNTER_OT_DICTIONARY["STSHOEXT"] = D_STSHOEXT_DICTIONARY
D_COUNTER_OT_DICTIONARY["STSMOTS"] = D_STSMOTS_DICTIONARY
D_COUNTER_OT_DICTIONARY["STSLAPD"] = D_STSLAPD_DICTIONARY

#定义表结构 所有相同的LEVEL的数据放到同一个LIST中 之后每个LIST中根据不同的OT在LIST中添加OTLIST。

#根据同一个level的不同OT进行列表分级
D_DICTIONARY_OT = {}

#链表中的链表是根据OT不同而划分的
D_DICTIONARY_LEVEL_TO_OTLIST = {}
L_STSBSC_LIST = []
L_STSTRA_LIST = []
L_STSCELL_LIST = []
L_STSHOINT_LIST = []
L_STSHOEXT_LIST = []
L_STSMOTS_LIST = []
L_STSLAPD_LIST = []

D_DICTIONARY_LEVEL_TO_OTLIST["STSBSC"] = L_STSBSC_LIST
D_DICTIONARY_LEVEL_TO_OTLIST["STSTRA"] = L_STSTRA_LIST
D_DICTIONARY_LEVEL_TO_OTLIST["STSCELL"] = L_STSCELL_LIST
D_DICTIONARY_LEVEL_TO_OTLIST["STSHOINT"] = L_STSHOINT_LIST
D_DICTIONARY_LEVEL_TO_OTLIST["STSHOEXT"] = L_STSHOEXT_LIST
D_DICTIONARY_LEVEL_TO_OTLIST["STSMOTS"] = L_STSMOTS_LIST
D_DICTIONARY_LEVEL_TO_OTLIST["STSLAPD"] = L_STSLAPD_LIST

#根据解析文件中的每个level的OT进行记录
D_DICTIONARY_LIST_OT_NAME = {}
L_STSBSC_OT_LIST = []
L_STSTRA_OT_LIST = []
L_STSCELL_OT_LIST = []
L_STSHOINT_OT_LIST = []
L_STSHOEXT_OT_LIST = []
L_STSMOTS_OT_LIST = []
L_STSLAPD_OT_LIST = []

D_DICTIONARY_LIST_OT_NAME["STSBSC"] = L_STSBSC_OT_LIST
D_DICTIONARY_LIST_OT_NAME["STSTRA"] = L_STSTRA_OT_LIST
D_DICTIONARY_LIST_OT_NAME["STSCELL"] = L_STSCELL_OT_LIST
D_DICTIONARY_LIST_OT_NAME["STSHOINT"] = L_STSHOINT_OT_LIST
D_DICTIONARY_LIST_OT_NAME["STSHOEXT"] = L_STSHOEXT_OT_LIST
D_DICTIONARY_LIST_OT_NAME["STSMOTS"] = L_STSMOTS_OT_LIST
D_DICTIONARY_LIST_OT_NAME["STSLAPD"] = L_STSLAPD_OT_LIST

#记录OT_columnName 每一种OT解析出来的表含有不同的列明 需要将列明跟定义表中的counter进行对比没有的话则不写进组合表中
D_DICTIONARY_OT_COLUMNNAME = {}
S_STSBSC_OT_COLUMNNAME = {}
S_STSTRA_OT_COLUMNNAME = {}
S_STSCELL_OT_COLUMNNAME = {}
S_STSHOINT_OT_COLUMNNAME = {}
S_STSHOEXT_OT_COLUMNNAME = {}
S_STSMOTS_OT_COLUMNNAME = {}
S_STSLAPD_OT_COLUMNNAME = {}

D_DICTIONARY_OT_COLUMNNAME["STSBSC"] = S_STSBSC_OT_COLUMNNAME
D_DICTIONARY_OT_COLUMNNAME["STSTRA"] = S_STSTRA_OT_COLUMNNAME
D_DICTIONARY_OT_COLUMNNAME["STSCELL"] = S_STSCELL_OT_COLUMNNAME
D_DICTIONARY_OT_COLUMNNAME["STSHOINT"] = S_STSHOINT_OT_COLUMNNAME
D_DICTIONARY_OT_COLUMNNAME["STSHOEXT"] = S_STSHOEXT_OT_COLUMNNAME
D_DICTIONARY_OT_COLUMNNAME["STSMOTS"] = S_STSMOTS_OT_COLUMNNAME
D_DICTIONARY_OT_COLUMNNAME["STSLAPD"] = S_STSLAPD_OT_COLUMNNAME

#
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL = {}
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSBSC"] = []
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSTRA"] = []
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSCELL"] = []
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSHOINT"] = []
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSHOEXT"] = []
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSMOTS"] = []
D_DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSLAPD"] = []