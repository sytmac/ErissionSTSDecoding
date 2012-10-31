#! /usr/bin/env python
#coding=utf-8
import os
import binascii
import math
from settings import *
from STSDefinitions import DefinitionsToDictiionary
class STS_decode():
    def __init__(self,inputList):
        self.__file=''
        self.__filename=inputList[0]
        print "正在进行解析的文件"
        print"{"
        for i in range(0,len(inputList)):
            binfile=open(inputList[i],"rb")
            print str(inputList[i])
            self.__file=self.__file+binfile.read()
            binfile.close()
        print "}"        
    '''
    decoding规则
    1：objtype开始标识 A2 80 13。
    2：该objtype 包含的counter名称。第一位是标识counter长度，后边几位是counter名称，直到出现00 00 A3 80，才结束counter定义
    3：继续往下读3位，判断该objtype是否定义有数据： 30 80 80是存在数据， 其他是不存在数据，可忽略该objtype。
    4：定义小区。和Counter名称一样，第一位是长度，后边是名称,其中名称是由objtype+Cell来命名
    5：开始取值。标识：A1 80 ， 紧接着的80是表示开始取值，在后一位是值的长度，后边就是具体的数值。
    6：到出现00 00 82 01 00 00 00 表示一行数据取完
    7：接着30 80 80，就开始下一个小区数据
    8：如果出现00 00 82 01 00 00 00，但接着的不是30 80 80，那表示这一objtype数据取完，然后就判断下一个A2 80 13， 重复1-8的过程。
    '''
    def decoding(self):
        fileString=self.__file
        filename=self.__filename
        FileNameWithoutPath=filename.split('\\')[-1]
        sNe=FileNameWithoutPath.split('_')[-2]
        if(len(self.__file)>0):
            sTimeStart=fileString[46:46+12]
            sTimeEnd=fileString[79:79+12]
            sDate=sTimeStart[0:8]
            if(sTimeStart[10:12]=="00" and sTimeEnd[10:12]=="00"):
                #print str(int(sTimeStart[8:10])+8)
                #print str(int(sTimeEnd[8:10])+8)
                sPERIOD=str(int(sTimeStart[8:10])+8)+'00-'+str(int(sTimeEnd[8:10])+8)+'00'
                
                iPos=96
                while(iPos<len(self.__file)):
                    if((binascii.hexlify(fileString[iPos])=="a2")and(binascii.hexlify(fileString[iPos+1])=="80")and(binascii.hexlify(fileString[iPos+2])=="13")):
                        iPos=iPos+3
                        #定义一个字典类型的                        
                        dictionary={}
                        
                        dictionary["ID"]=""
                        
                        dictionary["NE"]=""
                        
                        dictionary["MO"]=""
                        
                        dictionary["DATE"]=""
                        
                        dictionary["PERIOD"]=""
                        
                        dictionary["PERLEN"]=""
                        
                        #在每个OT的字段定义处循环
                        OT_list_columnName=[]
                        counterNameLen=int(binascii.hexlify(fileString[iPos]),16)
                        #将字典的key存入列表中
                        OT_list_columnName.append("ID")
                        
                        OT_list_columnName.append("NE")
                        
                        OT_list_columnName.append("MO")
                        
                        OT_list_columnName.append("DATE")
                        
                        OT_list_columnName.append("PERIOD")
                        
                        OT_list_columnName.append("PERLEN")
                        
                        OT_list_columnName.append(fileString[iPos+1:iPos+1+counterNameLen])
                        iPos=iPos+counterNameLen+2#加一的目的是过滤掉无用的字符
                        while(binascii.hexlify(fileString[iPos-1])!="00"
                            and binascii.hexlify(fileString[iPos])!="00"
                            and binascii.hexlify(fileString[iPos+1])!="a3"
                            and binascii.hexlify(fileString[iPos+2])!="80"):
                            counterNameLen=int(binascii.hexlify(fileString[iPos]),16)
                            OT_list_columnName.append(fileString[iPos+1:iPos+1+counterNameLen])
                            iPos=iPos+counterNameLen+2#加一的目的是过滤掉无用的字符
                        iPos=iPos+3#游标走到OT定义判断
                        sObjLev=""
                        #下边判断该OT是否定义，如定义，开始取数据；如果没有定义，位置加1,判断标志:30 80 80
                        if(binascii.hexlify(fileString[iPos])=="30"and binascii.hexlify(fileString[iPos+1])=="80"and binascii.hexlify(fileString[iPos+2])=="80"):
                            flag_OT=False
                            while(binascii.hexlify(fileString[iPos])=="30"and binascii.hexlify(fileString[iPos+1])=="80"and binascii.hexlify(fileString[iPos+2])=="80" and sObjLev!="NODEF"):
                                iPos=iPos+3
                                sOTMOLen=int(binascii.hexlify(fileString[iPos]),16)
                                sOTMO=fileString[iPos+1:iPos+1+sOTMOLen]
                                sObjtypeName=sOTMO.split('.')[0]
                                sMo=sOTMO.split('.')[1]
                                #如果 ObjType Excel中定义了该 ObjType，那么进行处理
                                if(OBJ_LEVEL_Dictionary.has_key(sObjtypeName)):
                                    sObjLev=OBJ_LEVEL_Dictionary[sObjtypeName]
                                    dictionary["TableName"]=sObjtypeName
                                    dictionary["NameSpace"]=sObjLev    
                                    if(flag_OT==False):
                                        dictionary_OT[dictionary["TableName"]]=[]
                                        flag_OT=True
                                    else:
                                        pass                                 
                                    #try:
                                    dictionary["ID"]=sNe+sMo+"0"+sDate+sPERIOD
                                    dictionary["NE"]=sNe
                                    dictionary["MO"]=sMo
                                    dictionary["DATE"]=sDate
                                    dictionary["PERIOD"]=sPERIOD
                                    dictionary["PERLEN"]="60"
                                    #转到判断是否开始取值处
                                    iPos=iPos+int(binascii.hexlify(fileString[iPos]),16)+1
                                    if(binascii.hexlify(fileString[iPos])=="a1"and binascii.hexlify(fileString[iPos+1])=="80"):
                                        iPos=iPos+2
                                        iData=6
                                       
                                        while(binascii.hexlify(fileString[iPos])!="00"
                                        or binascii.hexlify(fileString[iPos+1])!="00"
                                        or binascii.hexlify(fileString[iPos+2])!="82"
                                        or binascii.hexlify(fileString[iPos+3])!="01"
                                        or binascii.hexlify(fileString[iPos+4])!="00"
                                        or binascii.hexlify(fileString[iPos+5])!="00"
                                        or binascii.hexlify(fileString[iPos+6])!="00"):
                                            
                                            iValue=0
                                            
                                            if(binascii.hexlify(fileString[iPos])=="80"):
                                                iPos=iPos+1;#游标转移到counter的值长度位置上
                                                couterValuelen=int(binascii.hexlify(fileString[iPos]),16)
                                                for i in range(1,couterValuelen+1):
                                                    iValue=iValue+ int(binascii.hexlify(fileString[iPos+i]),16)*pow(16,2*(couterValuelen-i))
                                                dictionary[OT_list_columnName[iData]]=str(iValue)
                                                iPos=iPos+couterValuelen+1  
                                                iData=iData+1
                                            elif(binascii.hexlify(fileString[iPos])=="82"):
                                                dictionary[OT_list_columnName[iData]]="0"
                                                iPos=iPos+2
                                                iData=iData+1
                                            else:
                                                iPos=iPos+1 
                                    if (binascii.hexlify(fileString[iPos])=="00"
                                    and binascii.hexlify(fileString[iPos+1])=="00"
                                    and binascii.hexlify(fileString[iPos+2])=="82"
                                    and binascii.hexlify(fileString[iPos+3])=="01"
                                    and binascii.hexlify(fileString[iPos+4])=="00"
                                    and binascii.hexlify(fileString[iPos+5])=="00"
                                    and binascii.hexlify(fileString[iPos+6])=="00"):
                                        iPos=iPos+7#走到下一行数据
                                        #将数据加入到dictionary_OT
                                        length=len(OT_list_columnName)
                                        List=[]
                                        removed_list=[]
                                        OT_list_columnName_cp=[]
                                        OT_list_columnName_cp.extend(OT_list_columnName[6:])
                                        for i in range(0,length):
                                                #从definition定义的字典中获取存在的counter不存在的counter直接pass掉
                                                if(i<6):
                                                    List.append(dictionary[OT_list_columnName[i]])
                                                elif(i>=6):
                                                    if(Counter_OT_Dictionary[OBJ_LEVEL_Dictionary[sObjtypeName]].has_key(OT_list_columnName[i])==True):
                                                        List.append(dictionary[OT_list_columnName[i]])
                                                    else:
                                                        removed_list.append(OT_list_columnName[i])
                                        #将OT的属性放进OT_list_columnName_cp 以便生成字典 进行搜索,记下当前OT对应的属性属性
                                        for i in range(0,len(removed_list)):
                                                OT_list_columnName_cp.remove(removed_list[i])
                                        #将不同的OT的 属性保存 
                                        if(dictionary_OT_ColumnName[OBJ_LEVEL_Dictionary[sObjtypeName]].has_key(sObjtypeName)==False):
                                            dictionary_OT_ColumnName[OBJ_LEVEL_Dictionary[sObjtypeName]][sObjtypeName]=OT_list_columnName_cp                                         
                                        #dictionary_OT里面包含的是所有的OT类型下面所对应的链表 每一个链表都是这个OT字典所对应的数据                            
                                        dictionary_OT[dictionary["TableName"]].append(List)
                                                                                 
                                else:
                                    sObjLev="NODEF"
                    iPos=iPos+1
    def ObjectTypeiIntoSameLevelList(self):
        
        OT=dictionary_OT.keys()#文件里面所有OT的值,这是一个list
        #每次添加数据的时候让上一次的数据清0
        for i in range(0,len(OT)):
            dictionary_LevelToOTList[OBJ_LEVEL_Dictionary[OT[i]]]=[]
            dictionary_List_OT_Name[OBJ_LEVEL_Dictionary[OT[i]]]=[]
        for i in range(0,len(OT)):
            #dictionary_LevelToOTList 是保存同一类LEVEL的 不同的OT list 的list
            #它里面的每一个列表属于一个OT
            dictionary_LevelToOTList[OBJ_LEVEL_Dictionary[OT[i]]].append(dictionary_OT[OT[i]])
            dictionary_List_OT_Name[OBJ_LEVEL_Dictionary[OT[i]]].append(OT[i])
        #print dictionary_List_OT_Name["STSBSC"]
    #将不同OT表进行合并        
    def SameLevelTabelintoOneTable(self):
        #同一种的OT属性进行输出 ， 为了入数据库
        #STSCELL_Column_List=[]
        LevelTypeLen=len(LevelType_list)
        for i in range (0,LevelTypeLen):
            CounterColumnNameForEachLevel=[]
            CounterColumnNameForEachLevel.append("ID")
            CounterColumnNameForEachLevel.append("NE")
            CounterColumnNameForEachLevel.append("MO")
            CounterColumnNameForEachLevel.append("DATE")
            CounterColumnNameForEachLevel.append("PERIOD")
            CounterColumnNameForEachLevel.append("PERLEN")
            dictionary_CounterColumnNameForEachLevel[LevelType_list[i]].extend(CounterColumnNameForEachLevel)
            for j in range(0,len(dictionary_List_OT_Name[LevelType_list[i]])):           
                    dictionary_CounterColumnNameForEachLevel[LevelType_list[i]].extend(dictionary_OT_ColumnName[LevelType_list[i]][dictionary_List_OT_Name[LevelType_list[i]][j]])
        self.openFile()
        for i in range(0,LevelTypeLen):#遍历有几种LEVEL类型
            if(len(dictionary_LevelToOTList[LevelType_list[i]])>0):            
                    for j in range(0,len(dictionary_LevelToOTList[LevelType_list[i]][0])):#j表示OT里面每张表的长度，同一个OT里面的表的长度是相同的                        
                        counter_data=[]
                        counter_data.append(dictionary_LevelToOTList[LevelType_list[i]][0][j][0])
                        counter_data.append(dictionary_LevelToOTList[LevelType_list[i]][0][j][1])
                        counter_data.append(dictionary_LevelToOTList[LevelType_list[i]][0][j][2])
                        counter_data.append(dictionary_LevelToOTList[LevelType_list[i]][0][j][3])
                        counter_data.append(dictionary_LevelToOTList[LevelType_list[i]][0][j][4])
                        counter_data.append(dictionary_LevelToOTList[LevelType_list[i]][0][j][5])
                        for k in range(0,len(dictionary_LevelToOTList[LevelType_list[i]])):#k指同一个oT的表的个数                       
                            try:
                                counter_data.extend(dictionary_LevelToOTList[LevelType_list[i]][k][j][6:])
                            except:
                                pass
                                #for  m in range(0,len(dictionary_LevelToOTList[LevelType_list[i]])):
                                    #print len(dictionary_LevelToOTList[LevelType_list[i]][m])
                        self.InsertDataIntoFile(LevelType_list[i],counter_data)     
                        
        
        self.closeFile()                
    def openFile(self):
        #第一次的时候将列属性加进去
        if ((os.path.isfile('result_table/STSBSC'))==False): #如果不存在就 将列名写进去
            fp=open('result_table/STSBSC','a')
            fp.write(','.join(dictionary_CounterColumnNameForEachLevel["STSBSC"])+'\n')
            fp.close()
        if ((os.path.isfile('result_table/STSTRA'))==False): #如果不存在就 将列名写进去
            fp=open('result_table/STSTRA','a')
            fp.write(','.join(dictionary_CounterColumnNameForEachLevel["STSTRA"])+'\n')
            fp.close()
        if ((os.path.isfile('result_table/STSCELL'))==False): #如果不存在就 将列名写进去
            fp=open('result_table/STSCELL','a')
            fp.write(','.join(dictionary_CounterColumnNameForEachLevel["STSCELL"])+'\n')
            fp.close()
        if ((os.path.isfile('result_table/STSLAPD'))==False): #如果不存在就 将列名写进去
            fp=open('result_table/STSLAPD','a')
            fp.write(','.join(dictionary_CounterColumnNameForEachLevel["STSLAPD"])+'\n')
            fp.close()
        if ((os.path.isfile('result_table/STSHOEXT'))==False): #如果不存在就 将列名写进去
            fp=open('result_table/STSHOEXT','a')
            fp.write(','.join(dictionary_CounterColumnNameForEachLevel["STSHOEXT"])+'\n')
            fp.close()
        if ((os.path.isfile('result_table/STSMOTS'))==False): #如果不存在就 将列名写进去
            fp=open('result_table/STSMOTS','a')
            fp.write(','.join(dictionary_CounterColumnNameForEachLevel["STSMOTS"])+'\n')
            fp.close()
        if ((os.path.isfile('result_table/STSHOINT'))==False): #如果不存在就 将列名写进去
            fp=open('result_table/STSHOINT','a')
            fp.write(','.join(dictionary_CounterColumnNameForEachLevel["STSHOINT"])+'\n')
            fp.close()
        self.fp_STSBSC=open("result_table/STSBSC","a")
        self.fp_STSTRA=open("result_table/STSTRA","a")
        self.fp_STSCELL=open("result_table/STSCELL","a")
        self.fp_STSLAPD=open("result_table/STSLAPD","a")
        self.fp_STSMOTS=open("result_table/STSMOTS","a")
        self.fp_STSHOINT=open("result_table/STSHOINT","a")
        self.fp_STSHOEXT=open("result_table/STSHOEXT","a")

    def closeFile(self):
        self.fp_STSBSC.close()
        self.fp_STSTRA.close()
        self.fp_STSCELL.close()
        self.fp_STSLAPD.close()
        self.fp_STSMOTS.close()
        self.fp_STSHOINT.close()
        self.fp_STSHOEXT.close()
    def InsertDataIntoFile(self,Level,counter_data):

        if(Level=="STSBSC"):
            self.fp_STSBSC.writelines(','.join(counter_data)+'\n')
        if(Level=="STSTRA"):
            self.fp_STSTRA.writelines(','.join(counter_data)+'\n')
        if(Level=="STSCELL"):            
            self.fp_STSCELL.writelines(','.join(counter_data)+'\n')
        if(Level=="STSLAPD"):   
            self.fp_STSLAPD.writelines(','.join(counter_data)+'\n')
        if(Level=="STSMOTS"):            
            self.fp_STSMOTS.writelines(','.join(counter_data)+'\n')
        if(Level=="STSHOINT"):            
            self.fp_STSHOINT.writelines(','.join(counter_data)+'\n')
        if(Level=="STSHOEXT"):           
            self.fp_STSHOEXT.writelines(','.join(counter_data)+'\n')



