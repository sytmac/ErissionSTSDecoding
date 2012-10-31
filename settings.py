#! /usr/bin/env python
#coding=utf-8

LevelType_list=["STSBSC","STSTRA","STSCELL","STSHOINT","STSHOEXT","STSMOTS","STSLAPD"]
#根据OBJTYPE和Level生成对应的字典
OBJ_LEVEL_Dictionary={}

#根据level分成7个不同的字典.字典对应的是counter:ObjectType
STSBSC_Dictionary={}
STSTRA_Dictionary={}
STSCELL_Dictionary={}
STSLAPD_Dictionary={}
STSMOTS_Dictionary={}
STSHOINT_Dictionary={}
STSHOEXT_Dictionary={}


#Counter_OT_Dictionary是一个字典它对应的键值是它的key所对应的一个字典，字典里面的是Counter 和 OT对应的索引
Counter_OT_Dictionary={}
Counter_OT_Dictionary["STSBSC"]=STSBSC_Dictionary
Counter_OT_Dictionary["STSTRA"]=STSTRA_Dictionary
Counter_OT_Dictionary["STSCELL"]=STSCELL_Dictionary
Counter_OT_Dictionary["STSHOINT"]=STSHOINT_Dictionary
Counter_OT_Dictionary["STSHOEXT"]=STSHOEXT_Dictionary
Counter_OT_Dictionary["STSMOTS"]=STSMOTS_Dictionary
Counter_OT_Dictionary["STSLAPD"]=STSLAPD_Dictionary

#定义表结构 所有相同的LEVEL的数据放到同一个list中 之后每个list中根据不同的OT在list中添加OTlist。

#根据同一个level的不同OT进行列表分级
dictionary_OT={}
dictionary_OT_Attr={}

#链表中的链表是根据OT不同而划分的
dictionary_LevelToOTList={}
STSBSC_list=[]
STSTRA_list=[]
STSCELL_list=[]
STSHOINT_list=[]
STSHOEXT_list=[]
STSMOTS_list=[]
STSLAPD_list=[]

dictionary_LevelToOTList["STSBSC"]=STSBSC_list
dictionary_LevelToOTList["STSTRA"]=STSTRA_list
dictionary_LevelToOTList["STSCELL"]=STSCELL_list
dictionary_LevelToOTList["STSHOINT"]=STSHOINT_list
dictionary_LevelToOTList["STSHOEXT"]=STSHOEXT_list
dictionary_LevelToOTList["STSMOTS"]=STSMOTS_list
dictionary_LevelToOTList["STSLAPD"]=STSLAPD_list



#根据解析文件中的每个level的OT进行记录
dictionary_List_OT_Name={}
STSBSC_OT_list=[]
STSTRA_OT_list=[]
STSCELL_OT_list=[]
STSHOINT_OT_list=[]
STSHOEXT_OT_list=[]
STSMOTS_OT_list=[]
STSLAPD_OT_list=[]

dictionary_List_OT_Name["STSBSC"]=STSBSC_OT_list
dictionary_List_OT_Name["STSTRA"]=STSTRA_OT_list
dictionary_List_OT_Name["STSCELL"]=STSCELL_OT_list
dictionary_List_OT_Name["STSHOINT"]=STSHOINT_OT_list
dictionary_List_OT_Name["STSHOEXT"]=STSHOEXT_OT_list
dictionary_List_OT_Name["STSMOTS"]=STSMOTS_OT_list
dictionary_List_OT_Name["STSLAPD"]=STSLAPD_OT_list

#记录OT_columnName 每一种OT解析出来的表含有不同的列明 需要将列明跟定义表中的counter进行对比没有的话则不写进组合表中
dictionary_OT_ColumnName={}
STSBSC_OT_ColumnName=  {}
STSTRA_OT_ColumnName=  {}
STSCELL_OT_ColumnName= {}
STSHOINT_OT_ColumnName={}
STSHOEXT_OT_ColumnName={}
STSMOTS_OT_ColumnName= {}
STSLAPD_OT_ColumnName= {}

dictionary_OT_ColumnName["STSBSC"]=STSBSC_OT_ColumnName
dictionary_OT_ColumnName["STSTRA"]=STSTRA_OT_ColumnName
dictionary_OT_ColumnName["STSCELL"]=STSCELL_OT_ColumnName
dictionary_OT_ColumnName["STSHOINT"]=STSHOINT_OT_ColumnName
dictionary_OT_ColumnName["STSHOEXT"]=STSHOEXT_OT_ColumnName
dictionary_OT_ColumnName["STSMOTS"]=STSMOTS_OT_ColumnName
dictionary_OT_ColumnName["STSLAPD"]=STSLAPD_OT_ColumnName

#
dictionary_CounterColumnNameForEachLevel={}
dictionary_CounterColumnNameForEachLevel["STSBSC"]=[]
dictionary_CounterColumnNameForEachLevel["STSTRA"]=[]
dictionary_CounterColumnNameForEachLevel["STSCELL"]=[]
dictionary_CounterColumnNameForEachLevel["STSHOINT"]=[]
dictionary_CounterColumnNameForEachLevel["STSHOEXT"]=[]
dictionary_CounterColumnNameForEachLevel["STSMOTS"]=[]
dictionary_CounterColumnNameForEachLevel["STSLAPD"]=[]