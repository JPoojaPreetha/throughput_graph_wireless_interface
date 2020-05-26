import copy
import re
import datetime
import copy
import configuration as conf
import re

import matplotlib.dates as md
import matplotlib.pyplot as plt
from datetime import datetime
import math
import time
import copy


def graph(dates,oput,title,stfile):
    plt.subplots_adjust(bottom=0.3)
    plt.xticks( rotation=30, horizontalalignment='right' )
    
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.plot(dates,oput)
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Mbps')
    plt.savefig(stfile)
    plt.show()

def throughput(fname):
    print(" Throughput Graphs \n") 
    infile=open(fname,"r")
    lines=infile.readlines()
    txfile=open("txfile.txt","w+")
    rxfile=open("rxfile.txt","w+")
    #gather lines Tx Databytes and Rx Databytes into seperate files 
    for line in lines:
        if "Tx Data Bytes" in line:
            txfile.write(line)
        elif "Rx Data Bytes" in line:
            rxfile.write(line)

    txb=[]
    txt=[]
    txfile=open("txfile.txt","r")
    tl=txfile.readlines()

    #separate Databytes and time_series on given line
    for i in tl:
        txb.append(i.split('=')[1].split('|')[0])
        txt.append(i.split('|')[1].split('.')[0])

    #throughput calculation for Tx
    txt1=copy.deepcopy(txt)  
    txb = [int(i) for i in txb]
    txt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in txt]
    
    
    tdelb = [txb[i + 1] - txb[i] for i in range(len(txb)-1)]
    tdelt = [(txt[i + 1] - txt[i]).total_seconds() for i in range(len(txt)-1)]

    
    
    tput=[((tdelb[i])*8)/(tdelt[i]*math.pow(10,6)) for i in range(0,len(tdelb))]
    

    txt1 = [datetime.strptime(txt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(txt1)-1)]
        
    dates = md.date2num(txt1)

    graph(dates,tput,"Througput graph for tx databytes","txtput.png")


    rxb=[]
    rxt=[]
    rxfile=open("rxfile.txt","r")
    rl=rxfile.readlines()

    for i in rl:
        rxb.append(i.split('=')[1].split('|')[0])
        rxt.append(i.split('|')[1].split('.')[0])
    rxt1=copy.deepcopy(rxt)  
    rxb = [int(i) for i in rxb]
    rxt = [datetime.strptime(x,'%Y-%m-%d %H:%M:%S') for x in rxt]
    

    rdelb = [rxb[i + 1] - rxb[i] for i in range(len(rxb)-1)]
    rdelt = [(rxt[i + 1] - rxt[i]).total_seconds() for i in range(len(rxt)-1)]

    rtput=[((rdelb[i])*8)/(rdelt[i]*math.pow(10,6)) for i in range(0,len(rdelb))]
    

    ttput=[(tput[i]+rtput[i]) for i in range(len(tput))] 
    #print(" check : ",tput[0]," ",rtput[0] ," is " ,ttput[0])
    
    rxt1 = [datetime.strptime(rxt1[x],'%Y-%m-%d %H:%M:%S') for x in range(len(rxt1)-1)]
        
    dates = md.date2num(rxt1)
    
    graph(dates,rtput,"Througput graph for rx databytes","rxtput.png")
    graph(dates,ttput,"Througput graph for tx+rx databytes","tot_throughput_1.png")
    

    
    

