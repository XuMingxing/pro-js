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

#获取硬盘空间大小
def per_size():
    size=os.popen('df -h /')
    con= size.read().split()
    size.close()
    son=con[10].strip('%')
    return son

#获取系统内存剩余情况
def meminfo():
    ''' Return the information in /proc/meminfo
    as a dictionary '''
    f=open('/proc/meminfo')
    con=f.read().split()
    f.close()
    memfree=con[7].strip()
    return memfree

#新建计数文件
try :
    config.read("/home/pi/pro-js/count.conf")
    count1=config.getint("count","count1")
except ConfigParser.NoSectionError,e:
    js=open('/home/pi/pro-js/count.conf','w')
    js.write("[count]\n")
    js.write("count1=0\n")
    js.write("count2=0\n")
    js.write("count3=0\n")
    js.write("count4=0\n")
    js.write("count5=0\n")
    js.write("count6=0\n")
    js.close()


#读取配置文件
config.read("/home/pi/pro-js/js.cfg")
Corenum=config.getint("option","Corenum")
Hardcapmax=config.getint("option","Hardcapmax")
Residentfes=config.getint("option","Residentfes")
Residentmysql=config.getint("option","Residentmysql")
Residentjava1=config.getint("option","Residentjava1")
Residentjava2=config.getint("option","Residentjava2")
memavailable=config.getint("option","memavailable")
#前端打印状态并判断进程有无内存泄漏
pid_fes =os.popen('pidof fes')
pidfes=pid_fes.read().split()
pid_fes.close()

pid_mysql=os.popen('pidof mysqld')
mysql=pid_mysql.read().split()
pid_mysql.close()

pid_java1=os.popen('pgrep -o java')
java1=pid_java1.read().split()
pid_java1.close()

pid_java2=os.popen('pgrep -n java')
java2=pid_java2.read().split()
pid_java2.close()
try :
    fes_mem=pro_statm(pidfes[0])['resident']
    if int(fes_mem)>=Residentfes:
        config.read("/home/pi/pro-js/count.conf")
        count3=config.getint("count","count3")+1
        config.set("count","count3",str(count3))
        config.write(open("/home/pi/pro-js/count.conf","w"))
        if count3>=3:
            sample1.send_msg("进程fes","resident","泄漏")
    else :
        config.read("/home/pi/pro-js/count.conf")
        config.set("count","count3","0")
        config.write(open("/home/pi/pro-js/count.conf","w"))
except IndexError,e:
    fes_mem="noexist"
try :
    mysql_mem=pro_statm(mysql[0])['resident']
    if int(mysql_mem)>=Residentmysql:
        config.read("/home/pi/pro-js/count.conf")
        count4=config.getint("count","count4")+1
        config.set("count","count4",str(count4))
        config.write(open("count.conf","w"))
        if count4>=3:
            sample1.send_msg("进程mysql","resident","泄漏")
    else :
        config.read("/home/pi/pro-js/count.conf")
        config.set("count","count4","0")
        config.write(open("/home/pi/pro-js/count.conf","w"))
except IndexError,e:
    mysql_mem="noexist"
try :
    java1_mem=pro_statm(java1[0])['resident']
except IndexError,e:
    java1_mem="noexist"
try :
    java2_mem=pro_statm(java2[0])['resident']
except IndexError,e:
    java2_mem="noexist"

#java告警
try :
    if int(java1_mem)>int(java2_mem):
        java_mid=java1_mem
        java1_mem=java2_mem
        java2_mem=java_mid
    if int(java1_mem)>=Residentjava1:
        config.read("/home/pi/pro-js/count.conf")
        count5=config.getint("count","count5")+1
        config.set("count","count5",str(count5))
        config.write(open("/home/pi/pro-js/count.conf","w"))
        if count5>=3:
            sample1.send_msg("进程java1","resident","泄漏")
    else :
        config.read("/home/pi/pro-js/count.conf")
        config.set("count","count5","0")
        config.write(open("/home/pi/pro-js/count.conf","w"))
    if int(java2_mem)>=Residentjava2:
        config.read("/home/pi/pro-js/count.conf")
        count6=config.getint("count","count6")+1
        config.set("count","count6",str(count6))
        config.write(open("/home/pi/pro-js/count.conf","w"))
        if count6>=3:
            sample1.send_msg("进程java2","resident","泄漏")
    else :
        config.read("/home/pi/pro-js/count.conf")
        config.set("count","count6","0")
        config.write(open("/home/pi/pro-js/count.conf","w"))
except ValueError,e:
    print("one of java is not existing")

#报警逻辑
config.read("/home/pi/pro-js/count.conf")
if float(load_stat()['lavg_15'])>Corenum :
    count1=config.getint("count","count1")+1 
    config.set("count","count1",str(count1))
    config.write(open("/home/pi/pro-js/count.conf","w"))
    if count1>=3:
        sample1.send_msg("进程","数量","超标")
else : 
    config.set("count","count1","0")
    config.write(open("/home/pi/pro-js/count.conf","w"))
 
if int(meminfo()) <memavailable:
    count2=config.getint("count","count2")+1
    config.set("count","count2",str(count2))
    config.write(open("/home/pi/pro-js/count.conf","w"))
    if count2>=3:
        sample1.send_msg("内存","负荷","过大")
else :
    config.set("count","count2","0")
    config.write(open("/home/pi/pro-js/count.conf","w"))

if int(per_size())>=Hardcapmax:
    sample1.send_msg("硬盘","容量","不足")
print(meminfo(),load_stat()['lavg_15'], str(per_size())+"%" ,fes_mem,mysql_mem,java1_mem,java2_mem)
