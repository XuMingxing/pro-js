# -*- coding: utf-8 -*-
#!/usr/bin/env Python
#-----------1.0.0.002----------#
from __future__ import print_function
from __future__ import with_statement
from collections import OrderedDict 
import ConfigParser 
import os
import sample1
config=ConfigParser.ConfigParser()
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
def pro_statm(pid):
    statm={}
    g=open("/proc/"+str(pid)+"/statm")
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
    memfree=con[16].strip()
    return memfree

#前端打印状态
print(meminfo(),load_stat()['lavg_15'], per_size(),pro_statm(1)['resident'])

#新建计数文件
try :
    count1=config.getint("count","count1")
except ConfigParser.NoSectionError,e:
    js=open('js.conf','w')
    js.write("[count]")
    js.write("count1=0")
    js.write("count2=0")
    js.write("count3=0")
    js.close()
#读取配置文件
config.read("js.cfg")
Corenum=config.getint("option","Corenum")
Hardcapmax=config.getint("option","Hardcapmax")
Residentavg=config.getint("option","Residentavg")
#报警逻辑
config.read("js.conf")
if float(load_stat()['lavg_15'])>Corenum :
    count1=config.getint("count","count1")+1 
    config.set("count","count1",str(count1))
    config.write(open("js.conf","w"))
    if count1>=3:
        sample1.send_msg("进程","数量","超标")
else : 
    config.set("count","count1","0")
    config.write(open("js.conf","w"))
 
if int(meminfo()) != 0:
    count2=config.getint("count","count2")+1
    config.set("count","count2",str(count2))
    config.write(open("js.conf","w"))
    if count2>=3:
        sample1.send_msg("内存","负荷","过大")
else :
    config.set("count","count2","0")
    config.write(open("js.conf","w"))

if int(per_size())>=Hardcapmax:
    sample1.send_msg("硬盘","容量","不足")

if int(pro_statm(1)['resident'])>=Residentavg:
    count4=config.getint("count","count3")+1
    config.set("count","count3",str(count3))
    config.write(open("js.conf","w"))
    if count3>=3:
        sample1.send_msg("进程","resident","泄漏")
else :
    config.set("count","count3","0")
    config.write(open("js.conf","w"))
