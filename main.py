#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import e
import os, sys
import re
import hashlib
import io
import time
import shutil
#自行配置apktool和basksmali-2.4.0.jar路径
basksmali = "path"
apktool = "path"


pattern = re.compile(r'(((file|gopher|news|nntp|telnet|http|ftp|https|ftps|sftp)://)|(www\.))+(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&%_\./-~-]*)?')

#dex 使用basksmali 进行反编译
def Decompile_dex(filepath):
    try:
        
        #获取格式化时间
        # date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # newfile = date.replace(' ','')
        #newfile = "./test"

        str_cmd = "java -jar "+ basksmali +" d "+ filepath +" -o "+tool(filepath)
        print(str_cmd)
        os.system(str_cmd)
        
        return tool(filepath)
    except Exception as e:
        print(e)
        return "decompile excepiton fail"
#dex URL提取
def dex_search(file):
    ret_list = []
    line_num =0
    try:
        with io.open(file, 'r', encoding='utf-8') as smali:
            for line in smali.readlines():
                line_num +=1
                if 'android.com' in line:
                    continue
                if pattern.search(line):
                    ret_list.append('%s [line %d]: %s' % (file, line_num, line))
                    
            
    except Exception as e:
        print(e)
    return ret_list
#dex main
def dex_url_extract(filepath):

    dex_magic  = b'\x64\x65\x78\x0A\x30\x33\x35\x00'
    magic_num = open(filepath, 'rb').read(8)
    if magic_num == dex_magic:
        try:
            dex_path = Decompile_dex(filepath)
            if dex_path == "decompile excepiton fail" :
                exit()
            savefile = dex_path+".md"
            for dirpath, _, filenames in os.walk(dex_path):
                    #跳过original目录
                    if dirpath.endswith("original"):
                        continue
                    for filename in filenames:
                        #如果结尾不是smali活xml就跳出本次循环
                        if (not filename.endswith('smali') and
                            not filename.endswith('xml')):
                            continue
                        file = os.path.join(dirpath, filename)
                        ret = dex_search(file)
                        if len(ret) !=0:
                            #如果找到了url 就以追加的形式写到文件中
                            #使用join 去除list并且添加换行
                            cont_str = '\n'.join(ret)
                            
                            f = io.open(savefile,'a')
                            f.write(cont_str)
        except Exception as e:
            print("fail")
            exit()
        print("url提取结果保存到: "+savefile)
        #删除缓存目录
        shutil.rmtree(dex_path) 
    else :
        print("不是有效的dex文件 请检查")    
#apk 使用apktool 进行反编译
def Decompile_apk(filepath):
    try:

        str_cmd = "apktool" + " d "+ filepath +" -o "+tool(filepath)
        os.system(str_cmd)
        return tool(filepath)
    except Exception as e:
        return "decompile excepiton fail"
#apk URL提取
def apk_search(file):
    ret_list = []
    line_num = 0
    try:
        with io.open(file, 'r', encoding='utf-8') as apkcontent:
            for line in apkcontent.readlines():
                line_num  += 1 
                if 'android.com' in line:
                    continue
                if pattern.search(line):
                    ret_list.append('%s ->: %s' % (file, line))
    except Exception as e:
        print(e)
    return ret_list
#apk main
def apk_url_extract(filepath):
    apk_Decompile_path = Decompile_apk(filepath)
    savefile = apk_Decompile_path+".md"   
    for dirpath, _, filenames in os.walk(apk_Decompile_path):
            #跳过original目录
            if dirpath.endswith("original"):
                continue
            for filename in filenames:
                #如果结尾不是smali活xml就跳出本次循环
                if (not filename.endswith('smali') and
                    not filename.endswith('xml')):
                    continue
                file = os.path.join(dirpath, filename)
                ret = apk_search(file)
                if len(ret) !=0:
                    #如果找到了url 就以追加的形式写到文件中
                    #使用join 去除list并且添加换行
                    cont_str = '\n'.join(ret)
                    f = io.open(savefile,'a')
                    f.write(cont_str)
                
    print("url提取结果保存到: "+savefile)
    #删除缓存文件
    shutil.rmtree(apk_Decompile_path)


# dex目录遍历提取url
# 注意需要遍历一个文件后 进行写入文件
# 反编译一个 搜索一个 结果写入文件
def dirdex_url_extract(filepath):
    new_filepath =filepath.replace("/","_")
    dirResult = new_filepath+"result.md"
    for root,dir,filename in os.walk(filepath) :
        for file in filename:
            Nfile = root +"/"+file
            
            dex_magic  = b'\x64\x65\x78\x0A\x30\x33\x35\x00'
            magic_num = open(Nfile, 'rb').read(8)
            if magic_num == dex_magic:
                dex_Decompile_path = Decompile_dex(Nfile)
                for dirpath, _, filenames in os.walk(dex_Decompile_path):
                #跳过original目录
                    if dirpath.endswith("original"):
                        continue
                    for filename in filenames:
                        #如果结尾不是smali活xml就跳出本次循环
                        if (not filename.endswith('smali') and
                            not filename.endswith('xml')):
                            continue
                        file = os.path.join(dirpath, filename)
                        ret = dex_search(file)
                        if len(ret) !=0:
                            #如果找到了url 就以追加的形式写到文件中
                            #使用join 去除list并且添加换行
                            cont_str = '\n'.join(ret)
                            f = io.open(dirResult,'a')
                            f.write(cont_str)
                #删除缓存目录 
                shutil.rmtree(dex_Decompile_path)

    print("url提取结果保存到: "+dirResult)

def ipa_url_extract(file):
    print(file)
    result = os.popen("strings " +file +" | grep 'http'")
    dirResult = tool(file)

    res = result.read()
    f = io.open(dirResult,'a')
    f.write(res)
    print(dirResult)
def mainswitch(sw):
    sw_dex_apk_dir_ipa = sys.argv[2]
    if sw == "-a": #android
        print("提取字符串") 
        smali_path = os.path.join(sw_dex_apk_dir_ipa, 'smali')
        print(smali_path)
        strlen = len(sw_dex_apk_dir_ipa)
        
        if sw_dex_apk_dir_ipa[strlen-4:strlen] ==".apk":
            print("apk")
            apk_url_extract(sw_dex_apk_dir_ipa)
        elif sw_dex_apk_dir_ipa[strlen-4:strlen] ==".dex":
            print("dex")
            dex_url_extract(sw_dex_apk_dir_ipa)
        elif os.path.isdir(sw_dex_apk_dir_ipa):
            print("目录")
            dirdex_url_extract(sw_dex_apk_dir_ipa)

        else :
            print("不符合提取文件标准，退出")
            exit()
    elif sw =="-i": #ios
            print("ipa")
            print("ipa文件 只能是脱壳后的可执行文件,加固状态下的可执行文件不可以提取url")
            #1. 使用 strings 进行搜索
            ipa_url_extract(sw_dex_apk_dir_ipa)
    elif sw == "-h":
        print("-a/i <path>      :  指定路径提取apk/dex的web资产 ")
    else :
        print("\t\t\t\t\t\t 参数输入错误")
        exit()


def tool(file):
    newfile = file.replace("/","_")
    fstr = newfile.replace(".","_")
    return fstr


# ios
# 使用strings 读取可执行文件

if __name__ == "__main__":
    print("\t\t\t\t\t\t 独立的 dex/apk web资产提取工具 7777777777")
    print("\t\t\t\t\t\t 校验参数ing......[*]")
    if len(sys.argv) == 1 :
        print("\t\t\t\t\t\t 参数输入错误\n \t\t\t\t\t\t 帮助 -h")
        exit()

    sw = sys.argv[1]
    mainswitch(sw)

