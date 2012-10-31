#! /usr/bin/env python
#coding=utf-8
import xlrd
from settings import *
class DefinitionsToDictiionary(object):
    def __init__(self,filename):
        self.__fname=filename
        bk=xlrd.open_workbook(self.__fname)
        shxrange=range(bk.nsheets)
        try:
            sh=bk.sheet_by_name("Sheet1")
        except:
            print "no sheet in %s named Sheet1" % self.__fname 
        self.__nrows=sh.nrows        
        self.__row_list = []
        row_data = sh.row_values(0)
        self.__row_list.append(row_data)  
        #针对第一行进行判断是否是数据还是属性        
        if (sh.row_values(0)[0]!="LEVEL"):
            row_data = sh.row_values(0)
            self.__row_list.append(row_data)
        for i in range(1,self.__nrows):
            row_data = sh.row_values(i)
            self.__row_list.append(row_data)
        #print self.__row_list
        
    def Level_Classify(self):        
        for i in range(0,self.__nrows):
            if (self.__row_list[i][0]=="STSBSC"):
                STSBSC_Dictionary[self.__row_list[i][2]]=self.__row_list[i][1]
            elif (self.__row_list[i][0]=="STSTRA"):
                STSTRA_Dictionary[self.__row_list[i][2]]=self.__row_list[i][1]
            elif (self.__row_list[i][0]=="STSCELL"):
                STSCELL_Dictionary[self.__row_list[i][2]]=self.__row_list[i][1]
            elif (self.__row_list[i][0]=="STSLAPD"):
                STSLAPD_Dictionary[self.__row_list[i][2]]=self.__row_list[i][1]
            elif (self.__row_list[i][0]=="STSMOTS"):
                STSMOTS_Dictionary[self.__row_list[i][2]]=self.__row_list[i][1]
            elif (self.__row_list[i][0]=="STSHOINT"):
                STSHOINT_Dictionary[self.__row_list[i][2]]=self.__row_list[i][1]
            elif (self.__row_list[i][0]=="STSHOEXT"):
                STSHOEXT_Dictionary[self.__row_list[i][2]]=self.__row_list[i][1]              
        #根据OBJTYPE和Level生成对应的字典
        for i in range(1,self.__nrows):
            OBJ_LEVEL_Dictionary[self.__row_list[i][1]]=self.__row_list[i][0]
