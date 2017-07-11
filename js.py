#!/usr/bin/env Python
import os
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
if int(load_stat()['nr_u'])<=4:
    print load_stat()['nr_u'], load_stat()['nr_d'],pro_statm()['resident']

def per_size():
    size=os.popen('df -h /')
    con= size.read().split()
    size.close()
    son=con[11].split('%')
    c=son[0]
    return c

if int(per_size())<700:
    print per_size()
