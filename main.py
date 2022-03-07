#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from math import e
import os , re,io,shutil
import sys

bask = "./Tools/baksmali-2.4.0.jar"
pattern = re.compile(r'(((file|gopher|news|nntp|telnet|http|ftp|https|ftps|sftp)://)|(www\.))+(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(/[a-zA-Z0-9\&%_\./-~-]*)?')
# '    const-string v1, "123.196.118.23"\n'
pattern1 = re.compile(r'(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)\.(25[0-5]|2[0-4]\d|[0-1]\d{2}|[1-9]?\d)')
#pattern2 = re.compile(r'(?<=//|)(((\w)+\.)+\w+)(\:(\d+))')

pattern2 = re.compile('(file|gopher|news|nntp|telnet|http|ftp|https|ftps|sftp)://([^/:]+)(:\d*)?')
# 多重规则去匹配数据
#dex 使用basksmali 进行反编译
def Decompile_dex(filepath):
    try:
        
        str_cmd = "java -jar "+ bask +" d "+ filepath +" -o "+tool(filepath)
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
                if 'android.com' in line:
                    continue
                if pattern.search(line):
                    newstr = pattern.search(line)
                    ip = newstr[0]
                    # newstr1 =pattern2.search(line)
                    # ip1 =  newstr1[0]
                    #pattern2.search()
                    ret_list.append(' %s ' % (ip))
                elif pattern1.search(line):
                    newstr = pattern1.search(line)
                    ip = newstr[0]
                    # newstr1 =pattern2.search(line)
                    # ip1 =  newstr1[0]

                    ret_list.append(' %s ' % (ip))    
# # 存在 ip
# 存在 http
            
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
                    if dirpath.count("original") > 0:
                        continue
                    for filename in filenames:
                        #如果结尾不是smali活xml就跳出本次循环
                        # if (not filename.endswith('smali') and
                        #     not filename.endswith('xml') ):
                        #     continue
                        file = os.path.join(dirpath, filename)
                        print(dirpath)
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

def so_search(file):

    try:
    
        result = os.popen("strings " +file +" | grep 'http'")
        
        dirResult = tool(file)
        dirResult =dirResult +".md"
        res = result.read()
        f = io.open(dirResult,'a')
        f.write(res)
        f.close()
        result =so_url_filter(dirResult)
        #删除缓存文件
        os.remove(dirResult)
        return result
    except Exception as e:
        print(e)


#因为so使用的是strings 所以要筛选一下  
def so_url_filter(file):
    print(file)
    ret_list = []
    try:
        with io.open(file, 'rt', encoding='utf-8') as so:
            result = so.readlines()
            
            for line in result:
                print(line)
                if 'android' in line:
                    continue
                if 'umeng' in line:
                    continue
                if 'adobe' in line:
                    continue
                if pattern.search(line):
                    #print(line)
                    ret_list.append('%s' % (line))
                    
                elif pattern1.search(line):
                    ret_list.append('%s' %(line))    
                    
        return ret_list  
    except Exception as e:
        print(e)
    
#apk main
def apk_url_extract(filepath):
    try:
        apk_Decompile_path = Decompile_apk(filepath)
        savefile = apk_Decompile_path+".md"   
        for dirpath, _, filenames in os.walk(apk_Decompile_path):
                #跳过original目录
                if dirpath.count("original") > 0:
                    continue
                for filename in filenames:
                    
                    #如果结尾不是smali或xml就跳出本次循环
                    # if (not filename.endswith('smali') and
                    #     not filename.endswith('xml')):
                    #     continue

                    file = os.path.join(dirpath, filename)
                    if filename.endswith('so'):
                        ret = so_search(file)
                    else :
                        ret = dex_search(file)
                    if len(ret) !=0:
                        #如果找到了url 就以追加的形式写到文件中
                        #使用join 去除list并且添加换行
                        cont_str = '\n'.join(ret)
                        f = io.open(savefile,'a')
                        f.write(cont_str)
                        f.close()
                    
        print("url提取结果保存到: "+savefile)
        #删除缓存文件
        shutil.rmtree(apk_Decompile_path)
    except Exception as e:
            print(e)

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
                    if dirpath.count("original") > 0:
                        continue
                    for filename in filenames:
                        #如果结尾不是smali活xml就跳出本次循环
                        # if filename.endswith('smali'):
                        #     continue
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
    try:
        print(file)
        result = os.popen("strings " +file +" | grep 'http'")
        dirResult = tool(file)
        dirResult =dirResult +".md"
        res = result.read()
        f = io.open(dirResult,'a')
        f.write(res)
        result =ipa_url_filter(dirResult)
        
        new_str =result
        result_f = io.open(dirResult,'w')
        cont_str = '\n'.join(new_str)
        result_f.write(cont_str)
        print("url提取结果保存到: "+dirResult)
    except Exception as e:
        print(e)
#因为ios使用的是strings 所以要筛选一下  
def ipa_url_filter(file):
   
    print(file)
    ret_list = []
    try:
        with io.open(file, 'r', encoding='utf-8') as ipa:
            for line in ipa.readlines():
               
                if 'apple' in line:
                    continue
                if 'umeng' in line:
                    continue
                if 'adobe' in line:
                    continue
                if pattern.search(line):
                    ret_list.append('%s' % (line))
                    
                elif pattern1.search(line):
                    ret_list.append('%s' %(line))    
                    
        return ret_list     
    except Exception as e:
        print(e)
    
def mainswitch(sw):
    
    if sw == "-a": #android
        sw_dex_apk_dir_ipa = sys.argv[2]
        print("Android") 
        smali_path = os.path.join(sw_dex_apk_dir_ipa, 'smali')
        print(smali_path)
        strlen = len(sw_dex_apk_dir_ipa)
        #通过截取后缀来判断是文件/目录(虽然有些不太对 应该去判断魔术) 但是先用这个 后面完善了在去判断魔术标识头
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
            sw_dex_apk_dir_ipa = sys.argv[2]
            print("iOS")
            print("ipa文件 只能是脱壳后的可执行文件,加固状态下的可执行文件不可以提取url")
            #1. 使用 strings 进行搜索
            ipa_url_extract(sw_dex_apk_dir_ipa)
    elif sw == "-h":
        print("\t\t\t\t\t\t-s <path>      :  指定路径提取apk/dex的web资产 ")
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
    print("\t\t\t\t\t\t 使用前请阅读readme.md")
    print("\t\t\t\t\t\t 独立的 dex/apk web资产提取工具")
    print("\t\t\t\t\t\t 校验参数ing......[*]")
    if len(sys.argv) == 1 :
        print("\t\t\t\t\t\t 参数输入错误\n \t\t\t\t\t\t 帮助 -h")
        exit()

    sw = sys.argv[1]
    mainswitch(sw)

