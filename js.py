# -*- coding: utf-8 -*-
#!/usr/bin/env Python
#-----------1.0.0.002----------#
from __future__ import print_function
from collections import OrderedDict
import os

#获取loadavg值大小
def load_stat():
    loadavg={}
    f=open("/proc/loadavg")
    con=f.read().split()
    f.close()
    loadavg['lavg_1']=con[0]
    loadavg['lavg_5']=con[1]
    loadavg['lavg_15']=con[2]
    loadavg['nr']=con[3]
    loadavg['last_pid']=con[4]
    son=con[3].split('/')
    loadavg['nr_u']=son[0]
    loadavg['nr_d']=son[1]
    return loadavg

#获取进程statm内存情况
def pro_statm():
    statm={}
    g=open("/proc/1/statm")
    con=g.read().split()
    g.close()
    statm['size']=con[0]
    statm['resident']=con[1]
    statm['shared']=con[2]
    statm['Trs']=con[3]
    statm['Lrs']=con[4]
    statm['Drs']=con[5]
    statm['dt']=con[6]
    return statm

#获取硬盘内存大小
def per_size():
    size=os.popen('df -h /')
    con= size.read().split()
    size.close()
    son=con[11].strip('%')
    return son

#获取系统内存剩余情况
def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    f=open('/proc/meminfo')
    con=f.read().split()
    f.close()
    memfree=con[4].strip()
    return memfree

#前端打印状态
print("剩余物理内存(Kb):",meminfo())
print("正在运行的进程数:", load_stat()['nr_u'])
print("总进程数:",load_stat()['nr_d'])
print("硬盘占用率(%):", per_size())
print("Resident:",pro_statm()['resident'])

#报警逻辑
if int(load_stat()['nr_u'])>4:
    print("warning:系统进程数超标")
if int(meminfo()) <= 189104:
    print("warning:剩余内存过低")
if int(per_size())>=90:
    print("warning:硬盘内存即将耗尽")
if int(pro_statm()['resident'])>=1000:
    print("warning:程序占用内存异常")
