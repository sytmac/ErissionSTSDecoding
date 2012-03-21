#! /usr/bin/env python
#coding=utf-8
'''/
author :SongYang
''' 
import xlrd
from config.settings import D_STSBSC_DICTIONARY , D_STSTRA_DICTIONARY , D_STSCELL_DICTIONARY , D_STSLAPD_DICTIONARY , D_STSMOTS_DICTIONARY , D_STSHOINT_DICTIONARY , D_STSHOEXT_DICTIONARY
from config.settings import D_OBJ_LEVEL_DICTIONARY
class DefinitionsToDictionary(object):
    '''/
    '''
    def __init__(self , filename):
        self.__fname = filename
        s_bk = xlrd.open_workbook(self.__fname)
        try:
            s_sh = s_bk.sheet_by_name("Sheet1")
        except IndexError:
            print "no sheet in %s named Sheet1" % self.__fname 
        self.__nrows = s_sh.nrows        
        self.__row_list = []
        row_data = s_sh.row_values(0)
        self.__row_list.append(row_data)  
        #针对第一行进行判断是否是数据还是属性        
        if (s_sh.row_values(0)[0] != "LEVEL"):
            row_data = s_sh.row_values(0)
            self.__row_list.append(row_data)
        for i in range(1 , self.__nrows):
            row_data = s_sh.row_values(i)
            self.__row_list.append(row_data)
                    
    def levelclassify(self): 
        '''/ 
        '''        
        for i in range(0 , self.__nrows):
            if (self.__row_list[i][0] == "STSBSC"):
                s_index = self.__row_list[i][2]
                D_STSBSC_DICTIONARY[s_index] = self.__row_list[i][1]
            elif (self.__row_list[i][0] == "STSTRA"):
                s_index = self.__row_list[i][2]
                D_STSTRA_DICTIONARY[s_index] = self.__row_list[i][1]
            elif (self.__row_list[i][0] == "STSCELL"):
                s_index = self.__row_list[i][2]
                D_STSCELL_DICTIONARY[s_index] = self.__row_list[i][1]
            elif (self.__row_list[i][0] == "STSLAPD"):
                s_index = self.__row_list[i][2]
                D_STSLAPD_DICTIONARY[s_index] = self.__row_list[i][1]
            elif (self.__row_list[i][0] == "STSMOTS"):
                s_index = self.__row_list[i][2]
                D_STSMOTS_DICTIONARY[s_index] = self.__row_list[i][1]
            elif (self.__row_list[i][0] == "STSHOINT"):
                s_index = self.__row_list[i][2]
                D_STSHOINT_DICTIONARY[s_index] = self.__row_list[i][1]
            elif (self.__row_list[i][0] == "STSHOEXT"):
                s_index = self.__row_list[i][2]
                D_STSHOEXT_DICTIONARY[s_index] = self.__row_list[i][1]              
        #根据OBJTYPE和Level生成对应的字典
        for i in range(1 , self.__nrows):
            D_OBJ_LEVEL_DICTIONARY[self.__row_list[i][1]] = self.__row_list[i][0]
