#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''/
author:SongYang
'''
import sys,uuid
import os
import binascii
from config.settings import RECORD_COUNTER, EXCEPTION_MESSAGE, WARNING_MESSAGE, FILETABLE
from config.settings import OBJ_LEVEL_DICTIONARY
from config.settings import DICTIONARY_OT
from config.settings import COUNTER_OT_DICTIONARY
from config.settings import DICTIONARY_OT_COLUMNNAME
from config.settings import DICTIONARY_LEVEL_TO_OTLIST
from config.settings import DICTIONARY_LIST_OT_NAME
from config.settings import LEVELTYPE_LIST
from config.settings import DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL

class STSdecode():
    '''/
    解析类
    '''
    def __init__(self , inputlist,result_path ,guid):
        self.__fp_sts_bsc   = None
        self.__fp_sts_tra   = None
        self.__fp_sts_cell  = None
        self.__fp_sts_lapd  = None
        self.__fp_sts_mots  = None
        self.__fp_sts_hoint = None
        self.__fp_sts_hoext = None
        self.__file         = ''
        self.__filename     = inputlist[0]
        self.__result_path  = result_path
        self.__guid         = guid
        print "result_path:" + result_path
        print u"正在进行解析的文件"
        print"{"
        for i in range(0 , len(inputlist)):
            binfile = open(inputlist[i] , "rb")
            print inputlist[i]
            self.__file = self.__file+binfile.read()
            binfile.close()
        print "}"        

    def decoding(self):
        '''/
    decoding规则如下:
        '''
    #1：objtype开始标识 A2 80 13。
    #2：该objtype 包含的counter名称。第一位是标识counter长度，后边几位是counter名称，直到出现00 00 A3 80，才结束counter定义
    #3：继续往下读3位，判断该objtype是否定义有数据： 30 80 80是存在数据， 其他是不存在数据，可忽略该objtype。
    #4：定义小区。和Counter名称一样，第一位是长度，后边是名称,其中名称是由objtype+Cell来命名
    #5：开始取值。标识：A1 80 ， 紧接着的80是表示开始取值，在后一位是值的长度，后边就是具体的数值。
    #6：到出现00 00 82 01 00 00 00 表示一行数据取完
    #7：接着30 80 80，就开始下一个小区数据
    #8：如果出现00 00 82 01 00 00 00，但接着的不是30 80 80，那表示这一objtype数据取完，然后就判断下一个A2 80 13， 重复1-8的过程。
        try:
            filestring = self.__file
            filename = self.__filename
            s_filenamewithoutpath = filename.split('\\')[-1]
            s_ne = s_filenamewithoutpath.split('_')[-2]
            if(len(self.__file)>0):
                s_timestart = filestring[46:46+12]
                s_timeend = filestring[79:79+12]
                s_date = s_timestart[0:8]
                if(s_timestart[10:12] == "00" and s_timeend[10:12] == "00"):
                    #s_period = str(int(s_timestart[8:10])+8)+'00-'+str(int(s_timeend[8:10])+8)+'00'
                    s_period = str(int(s_timestart[8:10])+8)
                    i_pos = 96
                    while(i_pos < len(self.__file)):
                        if((binascii.hexlify(filestring[i_pos]) == "a2")
                           and(binascii.hexlify(filestring[i_pos+1]) == "80")
                           and(binascii.hexlify(filestring[i_pos+2]) == "13")):
                            i_pos = i_pos+3
                            #定义一个字典类型的                        
                            d_dictionary = {}                        
                            d_dictionary["ID"] = ""                       
                            d_dictionary["NE"] = ""                        
                            d_dictionary["MO"] = ""                       
                            d_dictionary["DATE"] = ""                        
                            d_dictionary["PERIOD"] = ""                        
                            d_dictionary["PERLEN"] = "" 
                     
                            #在每个OT的字段定义处循环
                            ot_columnname = []
                            s_counternamelen = int(binascii.hexlify(filestring[i_pos]) , 16)
                            #将字典的key存入列表中
                            ot_columnname.append("ID")                        
                            ot_columnname.append("NE")                        
                            ot_columnname.append("MO")                        
                            ot_columnname.append("DATE")                        
                            ot_columnname.append("PERIOD")                        
                            ot_columnname.append("PERLEN")
                               
                            ot_columnname.append(filestring[i_pos+1:i_pos+1+s_counternamelen])
                            
                            i_pos = i_pos+s_counternamelen+2#加一的目的是过滤掉无用的字符
                            while(binascii.hexlify(filestring[i_pos-1]) != "00"
                                and binascii.hexlify(filestring[i_pos]) != "00"
                                and binascii.hexlify(filestring[i_pos+1]) != "a3"
                                and binascii.hexlify(filestring[i_pos+2]) != "80"):
                                s_counternamelen = int(binascii.hexlify(filestring[i_pos]) , 16)
                                ot_columnname.append(filestring[i_pos+1:i_pos+1+s_counternamelen])
                                i_pos = i_pos+s_counternamelen+2#加一的目的是过滤掉无用的字符
                            i_pos = i_pos+3#游标走到OT定义判断
                            s_objlev = ""
                            #下边判断该OT是否定义，如定义，开始取数据；如果没有定义，位置加1,判断标志:30 80 80
                            if(binascii.hexlify(filestring[i_pos]) == "30"
                               and binascii.hexlify(filestring[i_pos+1]) == "80"
                               and binascii.hexlify(filestring[i_pos+2]) == "80"):
                                s_flag_ot = False
                                while(binascii.hexlify(filestring[i_pos]) == "30"
                                      and binascii.hexlify(filestring[i_pos+1]) == "80"
                                      and binascii.hexlify(filestring[i_pos+2]) == "80" 
                                      and s_objlev != "NODEF"):
                                    i_pos = i_pos+3
                                    s_otmolen = int(binascii.hexlify(filestring[i_pos]) , 16)
                                    s_otmo = filestring[i_pos+1:i_pos+1+s_otmolen]
                                    s_objtypename = s_otmo.split('.')[0]
                                    s_mo = s_otmo.split('.')[1]
                                    #如果 ObjType Excel中定义了该 ObjType，那么进行处理
                                    if(OBJ_LEVEL_DICTIONARY.has_key(s_objtypename)):
                                        s_objlev = OBJ_LEVEL_DICTIONARY[s_objtypename]
                                        d_dictionary["TableName"] = s_objtypename
                                        d_dictionary["NameSpace"] = s_objlev    
                                        if(s_flag_ot == False):
                                            DICTIONARY_OT[d_dictionary["TableName"]] = []
                                            s_flag_ot = True
                                        else:
                                            pass                                 
                                        #try:
                                        #d_dictionary["ID"] = s_ne+s_mo+"0"+s_date+s_period
                                        d_dictionary["ID"]     = str(uuid.uuid4())
                                        d_dictionary["NE"]     = s_ne
                                        d_dictionary["MO"]     = s_mo
                                        d_dictionary["DATE"]   = s_date
                                        d_dictionary["PERIOD"] = s_period
                                        d_dictionary["PERLEN"] = "60"
         
                                        #转到判断是否开始取值处
                                        i_pos = i_pos+int(binascii.hexlify(filestring[i_pos]) , 16)+1
                                        if(binascii.hexlify(filestring[i_pos]) == "a1"
                                           and binascii.hexlify(filestring[i_pos+1]) == "80"):
                                            i_pos  = i_pos+2
                                            i_data = 6                                       
                                            while(binascii.hexlify(filestring[i_pos]) != "00"
                                            or binascii.hexlify(filestring[i_pos+1])  != "00"
                                            or binascii.hexlify(filestring[i_pos+2])  != "82"
                                            or binascii.hexlify(filestring[i_pos+3])  != "01"
                                            or binascii.hexlify(filestring[i_pos+4])  != "00"
                                            or binascii.hexlify(filestring[i_pos+5])  != "00"
                                            or binascii.hexlify(filestring[i_pos+6])  != "00"):                                            
                                                i_value = 0                                            
                                                if(binascii.hexlify(filestring[i_pos]) == "80"):
                                                    i_pos = i_pos+1#游标转移到counter的值长度位置上
                                                    s_coutervaluelen = int(binascii.hexlify(filestring[i_pos]) , 16)
                                                    for i in range(1 , s_coutervaluelen+1):
                                                        i_value = i_value+ int(binascii.hexlify(filestring[i_pos+i]) , 16)*pow(16 , 2*(s_coutervaluelen-i))
                                                    d_dictionary[ot_columnname[i_data]] = str(i_value)
                                                    i_pos = i_pos+s_coutervaluelen+1  
                                                    i_data = i_data+1
                                                elif(binascii.hexlify(filestring[i_pos]) == "82"):
                                                    d_dictionary[ot_columnname[i_data]] = "0"
                                                    i_pos = i_pos+2
                                                    i_data = i_data+1
                                                else:
                                                    i_pos = i_pos+1
                                                    #增加guid
                                        if (binascii.hexlify(filestring[i_pos]) == "00"
                                            and binascii.hexlify(filestring[i_pos+1]) == "00"
                                            and binascii.hexlify(filestring[i_pos+2]) == "82"
                                            and binascii.hexlify(filestring[i_pos+3]) == "01"
                                            and binascii.hexlify(filestring[i_pos+4]) == "00"
                                            and binascii.hexlify(filestring[i_pos+5]) == "00"
                                            and binascii.hexlify(filestring[i_pos+6]) == "00"):
                                            i_pos = i_pos+7#走到下一行数据
                                            #将数据加入到DICTIONARY_OT
                                            length = len(ot_columnname)
                                            templist = []
                                            removed_list = []
                                            ot_columnname_cp = []
                                            ot_columnname_cp.extend(ot_columnname[6:])
                                            for i in range(0 , length):
                                                #从definition定义的字典中获取存在的counter不存在的counter直接pass掉
                                                if(i < 6):
                                                    templist.append(d_dictionary[ot_columnname[i]])
                                                elif(i >= 6):
                                                    if(COUNTER_OT_DICTIONARY[OBJ_LEVEL_DICTIONARY[s_objtypename]].has_key(ot_columnname[i]) == True):
                                                        templist.append(d_dictionary[ot_columnname[i]])
                                                    else:
                                                        removed_list.append(ot_columnname[i])
                                            #将OT的属性放进ot_columnname_cp 以便生成字典 进行搜索,记下当前OT对应的属性属性
                                            for i in range(0 , len(removed_list)):
                                                ot_columnname_cp.remove(removed_list[i])
                                            #将不同的OT的 属性保存 
                                            s_index = OBJ_LEVEL_DICTIONARY[s_objtypename]
                                            if(DICTIONARY_OT_COLUMNNAME[s_index].has_key(s_objtypename) == False):
                                                DICTIONARY_OT_COLUMNNAME[s_index][s_objtypename] = ot_columnname_cp                                         
                                            #DICTIONARY_OT里面包含的是所有的OT类型下面所对应的链表 每一个链表都是这个OT字典所对应的数据                            
                                            DICTIONARY_OT[d_dictionary["TableName"]].append(templist)
                                                                                     
                                    else:
                                        s_objlev = "NODEF"
                        i_pos = i_pos+1
        except:
            EXCEPTION_MESSAGE.append("there exists problems while decoding the data ")
    def objtype_into_samelevlist(self):
        '''
        首先需要调用 self.decode() 进行解析
        之后调用 此函数 进行OT汇总
        '''
        l_ot = DICTIONARY_OT.keys()#文件里面所有OT的值,这是一个list
        #每次添加数据的时候让上一次的数据清0
        for i in range(0 , len(l_ot)):
            DICTIONARY_LEVEL_TO_OTLIST[OBJ_LEVEL_DICTIONARY[l_ot[i]]] = []
            DICTIONARY_LIST_OT_NAME[OBJ_LEVEL_DICTIONARY[l_ot[i]]] = []
        for i in range(0 , len(l_ot)):
            #DICTIONARY_LEVEL_TO_OTLIST 是保存同一类LEVEL的 不同的OT list 的list
            #它里面的每一个列表属于一个OT
            DICTIONARY_LEVEL_TO_OTLIST[OBJ_LEVEL_DICTIONARY[l_ot[i]]].append(DICTIONARY_OT[l_ot[i]])
            DICTIONARY_LIST_OT_NAME[OBJ_LEVEL_DICTIONARY[l_ot[i]]].append(l_ot[i])
    #将不同OT表进行合并        
    def sameleveltableintoonetable(self):
        '''
        首先需要调用 self.decode() 进行解析
    其次调用self.objtype_into_samelevlist()进行OT汇总
    之后调用此函数进行写不同level文件
        '''

        try:
            #同一种的OT属性进行输出 ， 为了入数据库
            leveltype_len = len(LEVELTYPE_LIST)
            
            
            '''
                                     修改日期：2012/12/12 
                                    增加一个字典来关联属性和value之间的关系
            '''
            ######################################
            column_value_map = {}
            for index in range (0 , leveltype_len):
                column_value_map[LEVELTYPE_LIST[index]] = {}
    
            ######################################
            
            for i in range (0 , leveltype_len):
                countercolumnname_for_level = []
                countercolumnname_for_level.append("ID")
                countercolumnname_for_level.append("NE")
                countercolumnname_for_level.append("MO")
                countercolumnname_for_level.append("DATE")
                countercolumnname_for_level.append("PERIOD")
                countercolumnname_for_level.append("PERLEN")
                DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL[LEVELTYPE_LIST[i]].extend(countercolumnname_for_level)
                for j in range(0 , len(DICTIONARY_LIST_OT_NAME[LEVELTYPE_LIST[i]])):           
                    DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL[LEVELTYPE_LIST[i]].extend(DICTIONARY_OT_COLUMNNAME[LEVELTYPE_LIST[i]][DICTIONARY_LIST_OT_NAME[LEVELTYPE_LIST[i]][j]])
                DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL[LEVELTYPE_LIST[i]].append("GUID")
                
            ####################################################################################
            for level in LEVELTYPE_LIST:
                for column_index in  range(0, len(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL[level])):
                    column_value_map[level][DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL[level][column_index]] =  column_index       
            ####################################################################################
            
            self.__openfile()
            for i in range(0 , leveltype_len):#遍历有几种LEVEL类型
                if(len(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]])>0):
                    #j表示OT里面每张表的长度，同一个OT里面的表的长度是相同的             
                    for j in range(0 , len(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][0])):                       
                        counter_data = []
                        counter_data.append(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][0][j][0])
                        counter_data.append(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][0][j][1])
                        counter_data.append(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][0][j][2])
                        counter_data.append(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][0][j][3])
                        counter_data.append(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][0][j][4])
                        counter_data.append(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][0][j][5])
                        for k in range(0 , len(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]])):#k指同一个oT的表的个数                       
                            try:
                                counter_data.extend(DICTIONARY_LEVEL_TO_OTLIST[LEVELTYPE_LIST[i]][k][j][6:])
                            except IndexError:
                                print "index error"
                                WARNING_MESSAGE.append("the same OT tables with different lines numbers ")
                                pass
                        counter_data.append(self.__guid)
                        '''
                                    修改日期：2012/12/12 按照需要针对counter_data进行排列，即按照建表的顺序进行
                        '''
                        ###############################################################################################################
            
                        counter_data_by_order = []
                        counter_data_by_order.append(counter_data[0])
                        counter_data_by_order.append(counter_data[1])
                        counter_data_by_order.append(counter_data[2])
                        counter_data_by_order.append(counter_data[3])
                        counter_data_by_order.append(counter_data[4])
                        counter_data_by_order.append(counter_data[5])
                        
                        for index in range(0, len(FILETABLE[LEVELTYPE_LIST[i]])):     
                            if column_value_map[LEVELTYPE_LIST[i]].has_key(FILETABLE[LEVELTYPE_LIST[i]][index]):
                                couter_index = column_value_map[LEVELTYPE_LIST[i]][FILETABLE[LEVELTYPE_LIST[i]][index]]
                                counter_data_by_order.append(counter_data[couter_index])
                            else:
                                counter_data_by_order.append("")
                        
                        counter_data_by_order.append(counter_data[-1])                       
                        ###############################################################################################################
                                                
                        self.__insertdataintofile(LEVELTYPE_LIST[i], counter_data_by_order)            
            self.__closefile()
        except:
            EXCEPTION_MESSAGE.append("there exists problems in sameleveltableintoonetable() ")                   
    def __openfile(self):
        '''/
        #第一次的时候将列属性加进去
        '''
        #判断是否存在result_table文件夹，不存在的话创建
        if(os.path.isdir(self.__result_path+'/result_table')):
            print "result_table存在"
        else:
            os.mkdir(self.__result_path,'utf-8'+'/result_table')
        
        #如果不存在就 将列名写进去
        if ((os.path.isfile(self.__result_path+'/result_table/STSBSC')) == False): 
            p_fp = open(self.__result_path+'/result_table/STSBSC','a')
            p_fp.write(';'.join(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSBSC"])+'\n')
            p_fp.close()
        if ((os.path.isfile(self.__result_path+'/result_table/STSTRA')) == False):
            p_fp = open(self.__result_path+'/result_table/STSTRA','a')
            p_fp.write(';'.join(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSTRA"])+'\n')
            p_fp.close()
        if ((os.path.isfile(self.__result_path+'/result_table/STSCELL')) == False):
            p_fp = open(self.__result_path+'/result_table/STSCELL','a')
            p_fp.write(';'.join(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSCELL"])+'\n')
            p_fp.close()
        if ((os.path.isfile(self.__result_path+'/result_table/STSLAPD')) == False):
            p_fp = open(self.__result_path+'/result_table/STSLAPD','a')
            p_fp.write(';'.join(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSLAPD"])+'\n')
            p_fp.close()
        if ((os.path.isfile(self.__result_path+'/result_table/STSHOEXT')) == False):
            p_fp = open(self.__result_path+'/result_table/STSHOEXT','a')
            p_fp.write(';'.join(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSHOEXT"])+'\n')
            p_fp.close()
        if ((os.path.isfile(self.__result_path+'/result_table/STSMOTS')) == False):
            p_fp = open(self.__result_path+'/result_table/STSMOTS','a')
            p_fp.write(';'.join(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSMOTS"])+'\n')
            p_fp.close()
        if ((os.path.isfile(self.__result_path+'/result_table/STSHOINT')) == False): 
            p_fp = open(self.__result_path+'/result_table/STSHOINT','a')
            p_fp.write(';'.join(DICTIONARY_COUNTERCOLUMNNAME_FOR_EACHLEVEL["STSHOINT"])+'\n')
            p_fp.close()
        
        self.__fp_sts_bsc = open(self.__result_path+"/result_table/STSBSC","a")
        self.__fp_sts_tra = open(self.__result_path+"/result_table/STSTRA","a")
        self.__fp_sts_cell = open(self.__result_path+"/result_table/STSCELL","a")
        self.__fp_sts_lapd = open(self.__result_path+"/result_table/STSLAPD","a")
        self.__fp_sts_mots = open(self.__result_path+"/result_table/STSMOTS","a")
        self.__fp_sts_hoint = open(self.__result_path+"/result_table/STSHOINT","a")
        self.__fp_sts_hoext = open(self.__result_path+"/result_table/STSHOEXT","a")

    def __closefile(self): 
        '''/
        关闭打开的文件
        '''
        self.__fp_sts_bsc.close()
        self.__fp_sts_tra.close()
        self.__fp_sts_cell.close()
        self.__fp_sts_lapd.close()
        self.__fp_sts_mots.close()
        self.__fp_sts_hoint.close()
        self.__fp_sts_hoext.close()
    def __insertdataintofile(self , s_level , s_counter_data):
        '''/
        '''
        if(s_level == "STSBSC"):
            self.__fp_sts_bsc.writelines(';'.join(s_counter_data)+'\n')
        if(s_level == "STSTRA"):
            self.__fp_sts_tra.writelines(';'.join(s_counter_data)+'\n')
        if(s_level == "STSCELL"):            
            self.__fp_sts_cell.writelines(';'.join(s_counter_data)+'\n')
        if(s_level == "STSLAPD"):   
            self.__fp_sts_lapd.writelines(';'.join(s_counter_data)+'\n')
        if(s_level == "STSMOTS"):            
            self.__fp_sts_mots.writelines(';'.join(s_counter_data)+'\n')
        if(s_level == "STSHOINT"):            
            self.__fp_sts_hoint.writelines(';'.join(s_counter_data)+'\n')
        if(s_level == "STSHOEXT"):           
            self.__fp_sts_hoext.writelines(';'.join(s_counter_data)+'\n')
        
        RECORD_COUNTER[s_level]+=1
