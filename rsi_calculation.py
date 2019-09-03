import pandas as pd
import os
import csv
import sys
from math import log
from math import sqrt
import matplotlib.pyplot as plt 
from collections import defaultdict

read_file=sys.argv[1]
write_file=sys.argv[2]

data = pd.read_csv(read_file)
change={}
upward_movement={}
downward_movement={}
average_upward_movement={}
average_downward_movement={}
relative_strength={}
rsi={}
for index in range(8):
    change[index]=0
    upward_movement[index]=0
    downward_movement[index]=0
    average_upward_movement[index]=0
    average_downward_movement[index]=0
    relative_strength[index]=0
    rsi[index]=0

for index in range(len(data)-1):
    x=0
    y=0
    if(index==0):
        continue
    change[index]=data['Close'][index]-data['Close'][index-1]
    if(change[index]>0):
        upward_movement[index]=change[index]
        downward_movement[index]=0
    else:
        upward_movement[index]=0
        downward_movement[index]=abs(change[index])
    if(index==5):
        x=upward_movement[index-4]+upward_movement[index-3]+upward_movement[index-2]+upward_movement[index-1]+upward_movement[index]
        x=x/5
        y=downward_movement[index-4]+downward_movement[index-3]+downward_movement[index-2]+downward_movement[index-1]+downward_movement[index]
        y=y/5
        average_upward_movement[index]=x
        average_downward_movement[index]=y
        relative_strength[index]=average_upward_movement[index]/average_downward_movement[index]
        rsi[index]=100-(100/(relative_strength[index]+1))
        
    if(index>=6):
        average_upward_movement[index]=(average_upward_movement[index-1]*4+upward_movement[index])/5
        average_downward_movement[index]=(average_downward_movement[index-1]*4+downward_movement[index])/5
        relative_strength[index]=average_upward_movement[index]/average_downward_movement[index]
        rsi[index]=100-100/(relative_strength[index]+1)


list_values = [ v for v in rsi.values() ]
data = data.drop([len(data)-1], axis=0)
data=data.assign(RSI=list_values)
data.to_csv(write_file, index=False)