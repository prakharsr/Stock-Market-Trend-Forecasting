import pandas as pd
import os
from math import log
from math import sqrt
import matplotlib.pyplot as plt 
from collections import defaultdict

def candlestick(cluster):
    candlestick_cluster = {}
    
    for day in range(len(cluster)):
        
        if(day==0):
            continue
        upper = 100*(cluster[day]['High'] - max(cluster[day]['Open'], cluster[day]['Close']))/cluster[day]['Open']
        lower = 100*(min(cluster[day]['Open'], cluster[day]['Close']) - cluster[day]['Low'])/cluster[day]['Open']
        body = 100*(cluster[day]['Close']- cluster[day]['Open'])/cluster[day]['Close']
        if(cluster[day]['Low'] <= cluster[day-1]['High']):
            gap=0
        else:
            gap=100*(cluster[day]['Low']- cluster[day-1]['High'])/cluster[day]['Low']
        trend = 100*(cluster[day]['Close']- cluster[day-1]['Close'])/cluster[day]['Close']
        if(cluster[day-1]['Low'] <= cluster[day]['Open']):
            difopen=0
        else:
            difopen=100*(cluster[day-1]['Low']- cluster[day]['Open'])/cluster[day-1]['Low']
        if(cluster[day-1]['High'] >= cluster[day]['Close']):
            difclose=0
        else:
            difclose=100*(cluster[day]['Close']- cluster[day-1]['High'])/cluster[day]['Close']
        if(cluster[day]['Close'] <= (cluster[day-1]['Open']+cluster[day-1]['Close'])/2):
            difcentral=0
        else:
            difcentral=100*(cluster[day]['Close'] - (cluster[day-1]['Open']+cluster[day-1]['Close'])/2)/cluster[day]['Close']
        rsi=cluster[day]['RSI']
        
        data={'Upper': upper, 'Lower': lower, 'Body': body, 'Gap': gap, 'Trend':trend, 'Difopen': difopen, 'Difclose': difclose, 'Difcentral': difcentral, 'RSI': rsi}
        candlestick_cluster[day]=data
        
    return candlestick_cluster

#membership function
def fuzzify_candlestick(data):
    
    fuzzified_candlestick_cluster={}
    
    for day in range(6):
        
        if(day==0):
            continue

        Fuzzy_Lower=''
        Fuzzy_Upper=''
        Fuzzy_Body=''
        Fuzzy_Trend=''
        Fuzzy_Gap=''
        Fuzzy_Difopen=''
        Fuzzy_Difclose=''
        Fuzzy_Difcentral=''
        RSI=''

        #lower
        fuzzy_lower={}
        if(data[day]['Upper']>=0 and data[day]['Upper']<=0.5):
            fuzzy_lower['NULL']=-2*data[day]['Upper']+1
            fuzzy_lower['SHORT']=2*data[day]['Upper']
            fuzzy_lower['MIDDLE']=0
            fuzzy_lower['LONG']=0

            if(max(fuzzy_lower['NULL'], fuzzy_lower['SHORT'])==fuzzy_lower['NULL']):
                Fuzzy_Lower='NULL'
            else:
                Fuzzy_Lower='SHORT'

        elif(data[day]['Upper']>0.5 and data[day]['Upper']<=1.5):
            fuzzy_lower['NULL']=0
            fuzzy_lower['SHORT']=1
            fuzzy_lower['MIDDLE']=0
            fuzzy_lower['LONG']=0

            Fuzzy_Lower='SHORT'

        elif(data[day]['Upper']>1.5 and data[day]['Upper']<=2.5):
            fuzzy_lower['NULL']=0
            fuzzy_lower['SHORT']=-data[day]['Upper']+2.5
            fuzzy_lower['MIDDLE']=data[day]['Upper']-1.5
            fuzzy_lower['LONG']=0

            if(max(fuzzy_lower['MIDDLE'], fuzzy_lower['SHORT'])==fuzzy_lower['MIDDLE']):
                Fuzzy_Lower='MIDDLE'
            else:
                Fuzzy_Lower='SHORT'

        elif(data[day]['Upper']>2.5 and data[day]['Upper']<=3.5):
            fuzzy_lower['NULL']=0
            fuzzy_lower['SHORT']=0
            fuzzy_lower['MIDDLE']=1
            fuzzy_lower['LONG']=0

            Fuzzy_Lower='MIDDLE'

        elif(data[day]['Upper']>3.5 and data[day]['Upper']<=5):
            fuzzy_lower['NULL']=0
            fuzzy_lower['SHORT']=0
            fuzzy_lower['MIDDLE']=(-2*data[day]['Upper']+10)/3
            fuzzy_lower['LONG']=(2*data[day]['Upper']-7)/3

            if(max(fuzzy_lower['MIDDLE'], fuzzy_lower['LONG'])==fuzzy_lower['MIDDLE']):
                Fuzzy_Lower='MIDDLE'
            else:
                Fuzzy_Lower='LONG'

        elif(data[day]['Upper']>5):
            fuzzy_lower['NULL']=0
            fuzzy_lower['SHORT']=0
            fuzzy_lower['MIDDLE']=0
            fuzzy_lower['LONG']=1

            Fuzzy_Lower='LONG'
            
        #upper
        fuzzy_upper={}
        if(data[day]['Upper']>=0 and data[day]['Upper']<=0.5):
            fuzzy_upper['NULL']=-2*data[day]['Upper']+1
            fuzzy_upper['SHORT']=2*data[day]['Upper']
            fuzzy_upper['MIDDLE']=0
            fuzzy_upper['LONG']=0

            if(max(fuzzy_upper['NULL'], fuzzy_upper['SHORT'])==fuzzy_upper['NULL']):
                Fuzzy_Upper='NULL'
            else:
                Fuzzy_Upper='SHORT'

        elif(data[day]['Upper']>0.5 and data[day]['Upper']<=1.5):
            fuzzy_upper['NULL']=0
            fuzzy_upper['SHORT']=1
            fuzzy_upper['MIDDLE']=0
            fuzzy_upper['LONG']=0

            Fuzzy_Upper='SHORT'

        elif(data[day]['Upper']>1.5 and data[day]['Upper']<=2.5):
            fuzzy_upper['NULL']=0
            fuzzy_upper['SHORT']=-data[day]['Upper']+2.5
            fuzzy_upper['MIDDLE']=data[day]['Upper']-1.5
            fuzzy_upper['LONG']=0

            if(max(fuzzy_upper['SHORT'], fuzzy_upper['MIDDLE'])==fuzzy_upper['MIDDLE']):
                Fuzzy_Upper='MIDDLE'
            else:
                Fuzzy_Upper='SHORT'

        elif(data[day]['Upper']>2.5 and data[day]['Upper']<=3.5):
            fuzzy_upper['NULL']=0
            fuzzy_upper['SHORT']=0
            fuzzy_upper['MIDDLE']=1
            fuzzy_upper['LONG']=0

            Fuzzy_Upper='MIDDLE'

        elif(data[day]['Upper']>3.5 and data[day]['Upper']<=5):
            fuzzy_upper['NULL']=0
            fuzzy_upper['SHORT']=0
            fuzzy_upper['MIDDLE']=(-2*data[day]['Upper']+10)/3
            fuzzy_upper['LONG']=(2*data[day]['Upper']-7)/3

            if(max(fuzzy_upper['MIDDLE'], fuzzy_upper['LONG'])==fuzzy_upper['LONG']):
                Fuzzy_Upper='LONG'
            else:
                Fuzzy_Upper='MIDDLE'

        elif(data[day]['Upper']>5):
            fuzzy_upper['NULL']=0
            fuzzy_upper['SHORT']=0
            fuzzy_upper['MIDDLE']=0
            fuzzy_upper['LONG']=1

            Fuzzy_Upper='LONG'

        #body
        fuzzy_body={}
        if(data[day]['Body']<=-5):
            fuzzy_body['BLACK_LONG']=1
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            if(max(fuzzy_body['BLACK_LONG'],
            fuzzy_body['BLACK_MIDDLE'],
            fuzzy_body['BLACK_SHORT'],
            fuzzy_body['EQUAL'],
            fuzzy_body['WHITE_SHORT'],
            fuzzy_body['WHITE_MIDDLE'],
            fuzzy_body['WHITE_LONG'])==fuzzy_body['BLACK_LONG']):
                Fuzzy_Body='BLACK_LONG'
            
        if(data[day]['Body']>-5 and data[day]['Body']<=-3.5):
            fuzzy_body['BLACK_LONG']=(-2*data[day]['Body']-7)/3
            fuzzy_body['BLACK_MIDDLE']=(2*data[day]['Body']+10)/3
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            if(max(fuzzy_body['BLACK_LONG'],
            fuzzy_body['BLACK_MIDDLE'],
            fuzzy_body['BLACK_SHORT'],
            fuzzy_body['EQUAL'],
            fuzzy_body['WHITE_SHORT'],
            fuzzy_body['WHITE_MIDDLE'],
            fuzzy_body['WHITE_LONG'])==fuzzy_body['BLACK_LONG']):
                Fuzzy_Body='BLACK_LONG'
            
            else:
                Fuzzy_Body='BLACK_MIDDLE'
        
        if(data[day]['Body']>-3.5 and data[day]['Body']<=-2.5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=1
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            Fuzzy_Body='BLACK_MIDDLE'

        if(data[day]['Body']>-2.5 and data[day]['Body']<=-1.5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=-data[day]['Body']-1.5
            fuzzy_body['BLACK_SHORT']=data[day]['Body']+2.5
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            if(max(fuzzy_body['BLACK_LONG'],
            fuzzy_body['BLACK_MIDDLE'],
            fuzzy_body['BLACK_SHORT'],
            fuzzy_body['EQUAL'],
            fuzzy_body['WHITE_SHORT'],
            fuzzy_body['WHITE_MIDDLE'],
            fuzzy_body['WHITE_LONG'])==fuzzy_body['BLACK_MIDDLE']):
                Fuzzy_Body='BLACK_MIDDLE'
            
            else:
                Fuzzy_Body='BLACK_SHORT'
        
        if(data[day]['Body']>-1.5 and data[day]['Body']<=-0.5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=1
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            Fuzzy_Body='BLACK_SHORT'

        if(data[day]['Body']>-0.5 and data[day]['Body']<=0):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=-2*data[day]['Body']
            fuzzy_body['EQUAL']=2*data[day]['Body']
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            if(max(fuzzy_body['BLACK_LONG'],
            fuzzy_body['BLACK_MIDDLE'],
            fuzzy_body['BLACK_SHORT'],
            fuzzy_body['EQUAL'],
            fuzzy_body['WHITE_SHORT'],
            fuzzy_body['WHITE_MIDDLE'],
            fuzzy_body['WHITE_LONG'])==fuzzy_body['BLACK_SHORT']):
                Fuzzy_Body='BLACK_SHORT'
            
            else:
                Fuzzy_Body='EQUAL'

        if(data[day]['Body']>0 and data[day]['Body']<=0.5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=-2*data[day]['Body']+1
            fuzzy_body['WHITE_SHORT']=2*data[day]['Body']
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            if(max(fuzzy_body['BLACK_LONG'],
            fuzzy_body['BLACK_MIDDLE'],
            fuzzy_body['BLACK_SHORT'],
            fuzzy_body['EQUAL'],
            fuzzy_body['WHITE_SHORT'],
            fuzzy_body['WHITE_MIDDLE'],
            fuzzy_body['WHITE_LONG'])==fuzzy_body['EQUAL']):
                Fuzzy_Body='EQUAL'
            
            else:
                Fuzzy_Body='WHITE_SHORT'

        if(data[day]['Body']>0.5 and data[day]['Body']<=1.5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=1
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=0

            Fuzzy_Body='WHITE_SHORT'

        if(data[day]['Body']>1.5 and data[day]['Body']<=2.5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=-data[day]['Body'] + 2.5
            fuzzy_body['WHITE_MIDDLE']=data[day]['Body'] - 1.5
            fuzzy_body['WHITE_LONG']=0

            if(max(fuzzy_body['BLACK_LONG'],
            fuzzy_body['BLACK_MIDDLE'],
            fuzzy_body['BLACK_SHORT'],
            fuzzy_body['EQUAL'],
            fuzzy_body['WHITE_SHORT'],
            fuzzy_body['WHITE_MIDDLE'],
            fuzzy_body['WHITE_LONG'])==fuzzy_body['WHITE_SHORT']):
                Fuzzy_Body='WHITE_SHORT'
            
            else:
                Fuzzy_Body='WHITE_MIDDLE'            

        if(data[day]['Body']>2.5 and data[day]['Body']<=3.5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=1
            fuzzy_body['WHITE_LONG']=0

            Fuzzy_Body='WHITE_MIDDLE' 

        if(data[day]['Body']>3.5 and data[day]['Body']<=5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=(-2*data[day]['Body']+10)/3
            fuzzy_body['WHITE_LONG']=(2*data[day]['Body']-7)/3

            if(max(fuzzy_body['BLACK_LONG'],
            fuzzy_body['BLACK_MIDDLE'],
            fuzzy_body['BLACK_SHORT'],
            fuzzy_body['EQUAL'],
            fuzzy_body['WHITE_SHORT'],
            fuzzy_body['WHITE_MIDDLE'],
            fuzzy_body['WHITE_LONG'])==fuzzy_body['WHITE_MIDDLE']):
                Fuzzy_Body='WHITE_MIDDLE'
            
            else:
                Fuzzy_Body='WHITE_LONG' 

        if(data[day]['Body']>5):
            fuzzy_body['BLACK_LONG']=0
            fuzzy_body['BLACK_MIDDLE']=0
            fuzzy_body['BLACK_SHORT']=0
            fuzzy_body['EQUAL']=0
            fuzzy_body['WHITE_SHORT']=0
            fuzzy_body['WHITE_MIDDLE']=0
            fuzzy_body['WHITE_LONG']=1

            Fuzzy_Body='WHITE_LONG' 

        #trend
        fuzzy_trend={}

        if(data[day]['Trend']<=-5):
            fuzzy_trend['LONG_BEARISH']=1
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            Fuzzy_Trend='LONG_BEARISH'          
            
        if(data[day]['Trend']>-5 and data[day]['Trend']<=-3.5):
            fuzzy_trend['LONG_BEARISH']=(-2*data[day]['Trend']-7)/3
            fuzzy_trend['MIDDLE_BEARISH']=(2*data[day]['Trend']+10)/3
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            if(max(fuzzy_trend['LONG_BEARISH'],
            fuzzy_trend['MIDDLE_BEARISH'],
            fuzzy_trend['SHORT_BEARISH'],
            fuzzy_trend['NULL'],
            fuzzy_trend['SHORT_BULLISH'],
            fuzzy_trend['MIDDLE_BULLISH'],
            fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['LONG_BEARISH']):
                Fuzzy_Trend='LONG_BEARISH'
            
            else:
                Fuzzy_Trend='MIDDLE_BEARISH'
        
        if(data[day]['Trend']>-3.5 and data[day]['Trend']<=-2.5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=1
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            Fuzzy_Trend='MIDDLE_BEARISH'

        if(data[day]['Trend']>-2.5 and data[day]['Trend']<=-1.5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=-data[day]['Trend']-1.5
            fuzzy_trend['SHORT_BEARISH']=data[day]['Trend']+2.5
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            if(max(fuzzy_trend['LONG_BEARISH'],
            fuzzy_trend['MIDDLE_BEARISH'],
            fuzzy_trend['SHORT_BEARISH'],
            fuzzy_trend['NULL'],
            fuzzy_trend['SHORT_BULLISH'],
            fuzzy_trend['MIDDLE_BULLISH'],
            fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['MIDDLE_BEARISH']):
                Fuzzy_Trend='MIDDLE_BEARISH'
            
            else:
                Fuzzy_Trend='SHORT_BEARISH'
        
        if(data[day]['Trend']>-1.5 and data[day]['Trend']<=-0.5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=1
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            Fuzzy_Trend='SHORT_BEARISH'

        if(data[day]['Trend']>-0.5 and data[day]['Trend']<=0):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=-2*data[day]['Trend']
            fuzzy_trend['NULL']=2*data[day]['Trend']
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            if(max(fuzzy_trend['LONG_BEARISH'],
            fuzzy_trend['MIDDLE_BEARISH'],
            fuzzy_trend['SHORT_BEARISH'],
            fuzzy_trend['NULL'],
            fuzzy_trend['SHORT_BULLISH'],
            fuzzy_trend['MIDDLE_BULLISH'],
            fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['SHORT_BEARISH']):
                Fuzzy_Trend='SHORT_BEARISH'
            
            else:
                Fuzzy_Trend='NULL'

        if(data[day]['Trend']>0 and data[day]['Trend']<=0.5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=-2*data[day]['Trend']+1
            fuzzy_trend['SHORT_BULLISH']=2*data[day]['Trend']
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            if(max(fuzzy_trend['LONG_BEARISH'],
            fuzzy_trend['MIDDLE_BEARISH'],
            fuzzy_trend['SHORT_BEARISH'],
            fuzzy_trend['NULL'],
            fuzzy_trend['SHORT_BULLISH'],
            fuzzy_trend['MIDDLE_BULLISH'],
            fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['SHORT_BULLISH']):
                Fuzzy_Trend='SHORT_BULLISH'
            
            else:
                Fuzzy_Trend='NULL'

        if(data[day]['Trend']>0.5 and data[day]['Trend']<=1.5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=1
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=0

            Fuzzy_Trend='SHORT_BULLISH'

        if(data[day]['Trend']>1.5 and data[day]['Trend']<=2.5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=-data[day]['Trend'] + 2.5
            fuzzy_trend['MIDDLE_BULLISH']=data[day]['Trend'] - 1.5
            fuzzy_trend['LONG_BULLISH']=0

            if(max(fuzzy_trend['LONG_BEARISH'],
            fuzzy_trend['MIDDLE_BEARISH'],
            fuzzy_trend['SHORT_BEARISH'],
            fuzzy_trend['NULL'],
            fuzzy_trend['SHORT_BULLISH'],
            fuzzy_trend['MIDDLE_BULLISH'],
            fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['SHORT_BULLISH']):
                Fuzzy_Trend='SHORT_BULLISH'
            
            else:
                Fuzzy_Trend='MIDDLE_BULLISH'

        if(data[day]['Trend']>2.5 and data[day]['Trend']<=3.5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=1
            fuzzy_trend['LONG_BULLISH']=0

            Fuzzy_Trend='MIDDLE_BULLISH'

        if(data[day]['Trend']>3.5 and data[day]['Trend']<=5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=(-2*data[day]['Trend']+10)/3
            fuzzy_trend['LONG_BULLISH']=(2*data[day]['Trend']-7)/3

            if(max(fuzzy_trend['LONG_BEARISH'],
            fuzzy_trend['MIDDLE_BEARISH'],
            fuzzy_trend['SHORT_BEARISH'],
            fuzzy_trend['NULL'],
            fuzzy_trend['SHORT_BULLISH'],
            fuzzy_trend['MIDDLE_BULLISH'],
            fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['LONG_BULLISH']):
                Fuzzy_Trend='LONG_BULLISH'
            
            else:
                Fuzzy_Trend='MIDDLE_BULLISH'

        if(data[day]['Trend']>5):
            fuzzy_trend['LONG_BEARISH']=0
            fuzzy_trend['MIDDLE_BEARISH']=0
            fuzzy_trend['SHORT_BEARISH']=0
            fuzzy_trend['NULL']=0
            fuzzy_trend['SHORT_BULLISH']=0
            fuzzy_trend['MIDDLE_BULLISH']=0
            fuzzy_trend['LONG_BULLISH']=1

            Fuzzy_Trend='LONG_BULLISH'


        #gap
        fuzzy_gap={}

        if(data[day]['Gap']>=0 and data[day]['Gap']<=0.5):
            fuzzy_gap['NULL']=-2*data[day]['Gap']+1
            fuzzy_gap['SHORT']=2*data[day]['Gap']
            fuzzy_gap['MIDDLE']=0
            fuzzy_gap['LONG']=0

            if(max(fuzzy_gap['NULL'],
            fuzzy_gap['SHORT'],
            fuzzy_gap['MIDDLE'],
            fuzzy_gap['LONG'])==fuzzy_gap['NULL']):
                Fuzzy_Gap='NULL'
            
            else:
                Fuzzy_Gap='SHORT'

        if(data[day]['Gap']>0.5 and data[day]['Gap']<=1):
            fuzzy_gap['NULL']=0
            fuzzy_gap['SHORT']=1
            fuzzy_gap['MIDDLE']=0
            fuzzy_gap['LONG']=0

            Fuzzy_Gap='SHORT'

        if(data[day]['Gap']>1 and data[day]['Gap']<=1.5):
            fuzzy_gap['NULL']=0
            fuzzy_gap['SHORT']=-2*data[day]['Gap']+3
            fuzzy_gap['MIDDLE']=2*data[day]['Gap']-2
            fuzzy_gap['LONG']=0

            if(max(fuzzy_gap['NULL'],
            fuzzy_gap['SHORT'],
            fuzzy_gap['MIDDLE'],
            fuzzy_gap['LONG'])==fuzzy_gap['MIDDLE']):
                Fuzzy_Gap='MIDDLE'
            
            else:
                Fuzzy_Gap='SHORT'

        if(data[day]['Gap']>1.5 and data[day]['Gap']<=2):
            fuzzy_gap['NULL']=0
            fuzzy_gap['SHORT']=0
            fuzzy_gap['MIDDLE']=1
            fuzzy_gap['LONG']=0

            Fuzzy_Gap='MIDDLE'

        if(data[day]['Gap']>2 and data[day]['Gap']<=2.5):
            fuzzy_gap['NULL']=0
            fuzzy_gap['SHORT']=0
            fuzzy_gap['MIDDLE']=-2*data[day]['Gap']+5
            fuzzy_gap['LONG']=2*data[day]['Gap']-4

            if(max(fuzzy_gap['NULL'],
            fuzzy_gap['SHORT'],
            fuzzy_gap['MIDDLE'],
            fuzzy_gap['LONG'])==fuzzy_gap['MIDDLE']):
                Fuzzy_Gap='MIDDLE'
            
            else:
                Fuzzy_Gap='LONG'

        if(data[day]['Gap']>2.5):
            fuzzy_gap['NULL']=0
            fuzzy_gap['SHORT']=0
            fuzzy_gap['MIDDLE']=0
            fuzzy_gap['LONG']=1

            Fuzzy_Gap='LONG'

        #difopen

        fuzzy_difopen={}

        if(data[day]['Difopen']>=0 and data[day]['Difopen']<=0.5):
            fuzzy_difopen['NULL']=-2*data[day]['Difopen']+1
            fuzzy_difopen['SHORT']=2*data[day]['Difopen']
            fuzzy_difopen['MIDDLE']=0
            fuzzy_difopen['LONG']=0

            if(max(fuzzy_difopen['NULL'],
            fuzzy_difopen['SHORT'],
            fuzzy_difopen['MIDDLE'],
            fuzzy_difopen['LONG'])==fuzzy_difopen['NULL']):
                Fuzzy_Difopen='NULL'
            
            else:
                Fuzzy_Difopen='SHORT'

        if(data[day]['Difopen']>0.5 and data[day]['Difopen']<=1.5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=1
            fuzzy_difopen['MIDDLE']=0
            fuzzy_difopen['LONG']=0

            Fuzzy_Difopen='SHORT'

        if(data[day]['Difopen']>1.5 and data[day]['Difopen']<=2.5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=-data[day]['Difopen']+2.5
            fuzzy_difopen['MIDDLE']=data[day]['Difopen']-1.5
            fuzzy_difopen['LONG']=0

            if(max(fuzzy_difopen['NULL'],
            fuzzy_difopen['SHORT'],
            fuzzy_difopen['MIDDLE'],
            fuzzy_difopen['LONG'])==fuzzy_difopen['SHORT']):
                Fuzzy_Difopen='SHORT'
            
            else:
                Fuzzy_Difopen='MIDDLE'

        if(data[day]['Difopen']>2.5 and data[day]['Difopen']<=3.5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=0
            fuzzy_difopen['MIDDLE']=1
            fuzzy_difopen['LONG']=0

            Fuzzy_Difopen='MIDDLE'

        if(data[day]['Difopen']>3.5 and data[day]['Difopen']<=5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=0
            fuzzy_difopen['MIDDLE']=(-2*data[day]['Difopen']+10)/3
            fuzzy_difopen['LONG']=(2*data[day]['Difopen']-7)/3

            if(max(fuzzy_difopen['NULL'],
            fuzzy_difopen['SHORT'],
            fuzzy_difopen['MIDDLE'],
            fuzzy_difopen['LONG'])==fuzzy_difopen['LONG']):
                Fuzzy_Difopen='LONG'
            
            else:
                Fuzzy_Difopen='MIDDLE'

        if(data[day]['Difopen']>5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=0
            fuzzy_difopen['MIDDLE']=0
            fuzzy_difopen['LONG']=1

            Fuzzy_Difopen='LONG'

        #difclose

        fuzzy_difclose={}

        if(data[day]['Difclose']>=0 and data[day]['Difclose']<=0.5):
            fuzzy_difclose['NULL']=-2*data[day]['Difclose']+1
            fuzzy_difclose['SHORT']=2*data[day]['Difclose']
            fuzzy_difclose['MIDDLE']=0
            fuzzy_difclose['LONG']=0

            if(max(fuzzy_difclose['NULL'],
            fuzzy_difclose['SHORT'],
            fuzzy_difclose['MIDDLE'],
            fuzzy_difclose['LONG'])==fuzzy_difclose['NULL']):
                Fuzzy_Difclose='NULL'
            
            else:
                Fuzzy_Difclose='SHORT'

        if(data[day]['Difclose']>0.5 and data[day]['Difclose']<=1.5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=1
            fuzzy_difclose['MIDDLE']=0
            fuzzy_difclose['LONG']=0

            Fuzzy_Difclose='SHORT'

        if(data[day]['Difclose']>1.5 and data[day]['Difclose']<=2.5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=-data[day]['Difclose']+2.5
            fuzzy_difclose['MIDDLE']=data[day]['Difclose']-1.5
            fuzzy_difclose['LONG']=0

            if(max(fuzzy_difclose['NULL'],
            fuzzy_difclose['SHORT'],
            fuzzy_difclose['MIDDLE'],
            fuzzy_difclose['LONG'])==fuzzy_difclose['SHORT']):
                Fuzzy_Difclose='SHORT'
            
            else:
                Fuzzy_Difclose='MIDDLE'

        if(data[day]['Difclose']>2.5 and data[day]['Difclose']<=3.5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=0
            fuzzy_difclose['MIDDLE']=1
            fuzzy_difclose['LONG']=0

            Fuzzy_Difclose='MIDDLE'

        if(data[day]['Difclose']>3.5 and data[day]['Difclose']<=5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=0
            fuzzy_difclose['MIDDLE']=(-2*data[day]['Difclose']+10)/3
            fuzzy_difclose['LONG']=(2*data[day]['Difclose']-7)/3

            if(max(fuzzy_difclose['NULL'],
            fuzzy_difclose['SHORT'],
            fuzzy_difclose['MIDDLE'],
            fuzzy_difclose['LONG'])==fuzzy_difclose['LONG']):
                Fuzzy_Difclose='LONG'
            
            else:
                Fuzzy_Difclose='MIDDLE'

        if(data[day]['Difclose']>5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=0
            fuzzy_difclose['MIDDLE']=0
            fuzzy_difclose['LONG']=1

            Fuzzy_Difclose='LONG'
            
        #difcentral

        fuzzy_difcentral={}

        if(data[day]['Difcentral']>=0 and data[day]['Difcentral']<=0.5):
            fuzzy_difcentral['NULL']=-2*data[day]['Difcentral']+1
            fuzzy_difcentral['SHORT']=2*data[day]['Difcentral']
            fuzzy_difcentral['MIDDLE']=0
            fuzzy_difcentral['LONG']=0

            if(max(fuzzy_difcentral['NULL'],
            fuzzy_difcentral['SHORT'],
            fuzzy_difcentral['MIDDLE'],
            fuzzy_difcentral['LONG'])==fuzzy_difcentral['NULL']):
                Fuzzy_Difcentral='NULL'
            
            else:
                Fuzzy_Difcentral='SHORT'

        if(data[day]['Difcentral']>0.5 and data[day]['Difcentral']<=1.5):
            fuzzy_difcentral['NULL']=0
            fuzzy_difcentral['SHORT']=1
            fuzzy_difcentral['MIDDLE']=0
            fuzzy_difcentral['LONG']=0

            Fuzzy_Difcentral='SHORT'

        if(data[day]['Difcentral']>1.5 and data[day]['Difcentral']<=2.5):
            fuzzy_difcentral['NULL']=0
            fuzzy_difcentral['SHORT']=-data[day]['Difcentral']+2.5
            fuzzy_difcentral['MIDDLE']=data[day]['Difcentral']-1.5
            fuzzy_difcentral['LONG']=0

            if(max(fuzzy_difcentral['NULL'],
            fuzzy_difcentral['SHORT'],
            fuzzy_difcentral['MIDDLE'],
            fuzzy_difcentral['LONG'])==fuzzy_difcentral['MIDDLE']):
                Fuzzy_Difcentral='MIDDLE'
            
            else:
                Fuzzy_Difcentral='SHORT'

        if(data[day]['Difcentral']>2.5 and data[day]['Difcentral']<=3.5):
            fuzzy_difcentral['NULL']=0
            fuzzy_difcentral['SHORT']=0
            fuzzy_difcentral['MIDDLE']=1
            fuzzy_difcentral['LONG']=0

            Fuzzy_Difcentral='MIDDLE'

        if(data[day]['Difcentral']>3.5 and data[day]['Difcentral']<=5):
            fuzzy_difcentral['NULL']=0
            fuzzy_difcentral['SHORT']=0
            fuzzy_difcentral['MIDDLE']=(-2*data[day]['Difcentral']+10)/3
            fuzzy_difcentral['LONG']=(2*data[day]['Difcentral']-7)/3

            if(max(fuzzy_difcentral['NULL'],
            fuzzy_difcentral['SHORT'],
            fuzzy_difcentral['MIDDLE'],
            fuzzy_difcentral['LONG'])==fuzzy_difcentral['MIDDLE']):
                Fuzzy_Difcentral='MIDDLE'
            
            else:
                Fuzzy_Difcentral='LONG'

        if(data[day]['Difcentral']>5):
            fuzzy_difcentral['NULL']=0
            fuzzy_difcentral['SHORT']=0
            fuzzy_difcentral['MIDDLE']=0
            fuzzy_difcentral['LONG']=1

            Fuzzy_Difcentral='LONG'

        # RSI

        if(data[day]['RSI']<=55 and data[day]['RSI']>45):
            RSI='NULL'
        if(data[day]['RSI']<=65 and data[day]['RSI']>55):
            RSI='LOW_BULLISH'
        if(data[day]['RSI']<=75 and data[day]['RSI']>65):
            RSI='MEDIUM_BULLISH'
        if(data[day]['RSI']<=85 and data[day]['RSI']>75):
            RSI='HIGH_BULLISH'
        if(data[day]['RSI']<=100 and data[day]['RSI']>85):
            RSI='VERY_HIGH_BULLISH'
        if(data[day]['RSI']<=45 and data[day]['RSI']>35):
            RSI='LOW_BEARISH'
        if(data[day]['RSI']<=35 and data[day]['RSI']>25):
            RSI='MEDIUM_BEARISH'
        if(data[day]['RSI']<=25 and data[day]['RSI']>=0):
            RSI='HIGH_BEARISH'
        if(data[day]['RSI']<=85 and data[day]['RSI']>75):
            RSI='VERY_HIGH_BEARISH'
        
            
        fuzzified_candlestick_cluster[day]={'Fuzzy_Lower': Fuzzy_Lower, 'Fuzzy_Upper': Fuzzy_Upper, 'Fuzzy_Body': Fuzzy_Body, 'Fuzzy_Trend': Fuzzy_Trend, 'Fuzzy_Gap': Fuzzy_Gap, 'Fuzzy_Difopen': Fuzzy_Difopen, 'Fuzzy_Difclose': Fuzzy_Difclose,  'Fuzzy_Difcentral': Fuzzy_Difcentral, 'RSI': RSI}
    return fuzzified_candlestick_cluster

def identify_candlestick(cluster, candlestick_cluster, fuzzified_candlestick_cluster):
    
    identified_candlestick = {
    'Kicking_Bullish' : 0,
    'Kicking_Bearish' : 0,
    'Engulfing_Bullish' : 0,
    'Engulfing_Bearish' : 0,
    'Harami_Bullish' : 0,
    'Harami_Bearish' : 0,
    'Meeting_Line_Bullish' : 0,
    'Meeting_Line_Bearish' : 0,
    'Hammer' : 0,
    'Inverted_Hammer' : 0,
    'Piercing_Line' : 0,
    'One_White_Soldier' : 0,
    'Homing_Pigeon' : 0,
    'Hanging_Man' : 0,
    'Descending_Hawk' : 0,
    'One_Black_Crow' : 0,
    'Dark_Cloud_Clover' : 0}

    # 2 DAY BULLISH CANDLESTICKS
    kicking={}
    engulfing={}
    harami={}
    hammer={}
    inverted_hammer={}
    piercing_line={}
    one_white_soldier={}
    homing_pigeon={}
    meeting_line={}

    # 3 DAY BULLISH CANDLESTICKS
    # morning_star={}
    # threee_white_soldiers={}

    #kicking
    if(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
    fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
    fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
    fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
    cluster[5]['Low'] > cluster[4]['High'] and 
    candlestick_cluster[4]['Body']<-0.5 and
    candlestick_cluster[5]['Body']>0.5):

        if(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Gap']=='LONG'):
            kicking['Bullish']='HIGH'

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Gap']=='MIDDLE'):
            kicking['Bullish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Gap']=='SHORT'):
            kicking['Bullish']='MEDIUM'

        else:
            kicking['Bullish']='HOLD'

        identified_candlestick['Kicking_Bullish']=1

    #hammer

    if(cluster[5]['Low'] < cluster[4]['Low'] and 
    fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and
    cluster[5]['High'] - max(cluster[5]['Open'], cluster[5]['Close']) < cluster[5]['Body']/5 and 
    min(cluster[5]['Open'], cluster[5]['Close']) - cluster[5]['Low'] >  2*abs(cluster[5]['Open']-cluster[5]['Close']) ):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BEARISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hammer['Bullish']='HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='SHORT' and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BEARISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hammer['Bullish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='SHORT' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BEARISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hammer['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BEARISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hammer['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='SHORT') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BEARISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hammer['Bullish']='MEDIUM_LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='SHORT' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BEARISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hammer['Bullish']='LOW'

        else:
            hammer['Bullish']='HOLD'

        identified_candlestick['Hammer']=1

    # piercing line

    if(candlestick_cluster[4]['Body']<-0.5 and 
    candlestick_cluster[5]['Body']>0.5 and 
    cluster[5]['Open']<cluster[4]['Low'] and 
    cluster[5]['Close']>cluster[4]['Body']/2 and 
    cluster[5]['Close']<cluster[4]['Open'] and 
    (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='SHORT' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='SHORT' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='MEDIUM_LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='SHORT' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='MIDDLE' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='MEDIUM_LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='MIDDLE' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='MIDDLE' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='LONG' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='LONG' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difopen']=='LONG' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            piercing_line['Bullish']='HIGH'

        else:
            piercing_line['Bullish']='HOLD'

        identified_candlestick['Piercing_Line']=1

    # engulfing

    if(candlestick_cluster[4]['Body']<-0.5 and
    candlestick_cluster[5]['Body']>0.5 and 
    cluster[4]['High']<=cluster[5]['Close'] and 
    cluster[4]['Low']>=cluster[5]['Open']):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT'):
            engulfing['Bullish']='LOW'      

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_MIDDLE'):
            engulfing['Bullish']='MEDIUM'   

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_LONG'):
            engulfing['Bullish']='HIGH' 

        else:
            engulfing['Bullish']='HOLD'

        identified_candlestick['Engulfing_Bullish']=1

    # harami

    if(candlestick_cluster[4]['Body']<-0.5 and
    candlestick_cluster[5]['Body']>0.5 and 
    cluster[4]['Open']>=cluster[5]['High'] and 
    cluster[4]['Close']<=cluster[5]['Low']):

        if(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_SHORT'):
            harami['Bullish']='LOW'      

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE'):
            harami['Bullish']='MEDIUM'   

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG'):
            harami['Bullish']='HIGH' 

        else:
            harami['Bullish']='HOLD'

        identified_candlestick['Harami_Bullish']=1      

    # inverted hammer

    if(cluster[5]['Low'] < cluster[4]['Low'] and 
    fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and candlestick_cluster[4]['Body']<-0.5 and (cluster[5]['Low'] - min(cluster[5]['Open'], cluster[5]['Close'])) < cluster[5]['Body']/5 and 
    (cluster[5]['High'] - max(cluster[5]['Open'], cluster[5]['Close'])) >  2*abs(cluster[5]['Open']-cluster[5]['Close']) ):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='MIDDLE') and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BEARISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            inverted_hammer['Bullish']='HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='SHORT' and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BEARISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            inverted_hammer['Bullish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='SHORT' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='MIDDLE') and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BEARISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            inverted_hammer['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='MIDDLE') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BEARISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            inverted_hammer['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='SHORT') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BEARISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            inverted_hammer['Bullish']='MEDIUM_LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='SHORT' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='MIDDLE') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BEARISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            inverted_hammer['Bullish']='LOW'

        else:
            inverted_hammer['Bullish']='HOLD'

        identified_candlestick['Inverted_Hammer']=1  

    # one white soldier

    if(candlestick_cluster[4]['Body']<-0.5 and 
    candlestick_cluster[5]['Body']>0.5 and 
    cluster[5]['Open']>cluster[4]['Close'] and 
    cluster[5]['Close']>cluster[4]['Open'] and 
    (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='SHORT' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='SHORT' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='MEDIUM_LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='SHORT' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='MIDDLE' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='MEDIUM_LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='MIDDLE' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='MIDDLE' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='LONG' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='LONG' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Difclose']=='LONG' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Difcentral']=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG')):
            one_white_soldier['Bullish']='HIGH'

        else:
            one_white_soldier['Bullish']='HOLD'

        identified_candlestick['One_White_Soldier']=1

    # homing pigeon

    if(candlestick_cluster[4]['Body']<-0.5 and
    candlestick_cluster[5]['Body']<-0.5 and 
    cluster[4]['High']>cluster[5]['High'] and 
    cluster[4]['Low']<cluster[5]['Low']):

        if(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_SHORT'):
            homing_pigeon['Bullish']='LOW'      

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_MIDDLE'):
            homing_pigeon['Bullish']='MEDIUM'   

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='BLACK_LONG'):
            homing_pigeon['Bullish']='HIGH' 

        else:
            homing_pigeon['Bullish']='HOLD'

        identified_candlestick['Homing_Pigeon']=1  

    # meeting line

    if(candlestick_cluster[4]['Body']<-0.5 and
    candlestick_cluster[5]['Body']>0.5 and 
    ((cluster[4]['Close']-cluster[5]['Close'])/cluster[4]['Close']) <= 0.5 and 
    ((cluster[4]['Close']-cluster[5]['Close'])/cluster[4]['Close']) >= 0):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_SHORT'):
            meeting_line['Bullish']='LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_MIDDLE'):
            meeting_line['Bullish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='WHITE_LONG'):
            meeting_line['Bullish']='HIGH'

        else:
            meeting_line['Bullish']='HOLD'

        identified_candlestick['Meeting_Line_Bullish']=1 



    # 2 DAY BEARISH CANDLESTICKS
    # kicking={}
    # engulfing={}
    # harami={}_Bullish
    # meeting_line={}
    hanging_man={}
    descending_hawk={}
    one_black_crow={}
    dark_cloud_clover={}
   
    #kicking
    if(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
    fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
    fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
    fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
    cluster[4]['Low'] > cluster[5]['High'] and 
    candlestick_cluster[4]['Body']>0.5 and
    candlestick_cluster[5]['Body']<-0.5):

        if(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Gap']=='LONG'):
            kicking['Bearish']='HIGH'

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Gap']=='MIDDLE'):
            kicking['Bearish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[4]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Gap']=='SHORT'):
            kicking['Bearish']='MEDIUM'

        else:
            kicking['Bearish']='HOLD'

        identified_candlestick['Kicking_Bearish']=1

    # engulfing

    if(candlestick_cluster[4]['Body']>0.5 and
    candlestick_cluster[5]['Body']<-0.5 and 
    cluster[4]['High']<=cluster[5]['Open'] and 
    cluster[4]['Low']>=cluster[5]['Close']):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT'):
            engulfing['Bearish']='LOW'      

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_MIDDLE'):
            engulfing['Bearish']='MEDIUM'   

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_LONG'):
            engulfing['Bearish']='HIGH' 

        else:
            engulfing['Bearish']='HOLD'

        identified_candlestick['Engulfing_Bearish']=1

    # harami

    if(candlestick_cluster[4]['Body']>0.5 and
    candlestick_cluster[5]['Body']<-0.5 and 
    cluster[4]['Close']>=cluster[5]['High'] and 
    cluster[4]['Open']<=cluster[5]['Low']):

        if(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_SHORT'):
            harami['Bearish']='LOW'      

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE'):
            harami['Bearish']='MEDIUM'   

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG'):
            harami['Bearish']='HIGH' 

        else:
            harami['Bearish']='HOLD'

        identified_candlestick['Harami_Bearish']=1 

    # meeting line

    if(candlestick_cluster[4]['Body']>0.5 and
    candlestick_cluster[5]['Body']<-0.5 and 
    ((cluster[5]['Close']-cluster[4]['Close'])/cluster[5]['Close']) <= 0.5 and 
    ((cluster[5]['Close']-cluster[4]['Close'])/cluster[5]['Close']) >= 0):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT'):
            meeting_line['Bearish']='LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_MIDDLE'):
            meeting_line['Bearish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_LONG'):
            meeting_line['Bearish']='HIGH'

        else:
            meeting_line['Bearish']='HOLD'

        identified_candlestick['Meeting_Line_Bearish']=1 

    # hanging man

    if(cluster[5]['High'] > cluster[4]['High'] and 
    fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
    (cluster[5]['High'] - max(cluster[5]['Open'], cluster[5]['Close']) < cluster[5]['Body']/5) and 
    (min(cluster[5]['Open'], cluster[5]['Close']) - cluster[5]['Low'] >  2*abs(cluster[5]['Open']-cluster[5]['Close'])) ):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BULLISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hanging_man['Bearish']='HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='SHORT' and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BULLISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hanging_man['Bearish']='MEDIUM_HIGH'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='SHORT' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='SHORT_BULLISH' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hanging_man['Bearish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BULLISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hanging_man['Bearish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='NULL' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='SHORT') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BULLISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hanging_man['Bearish']='MEDIUM_LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Upper']=='SHORT' and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='LONG' or fuzzified_candlestick_cluster[5]['Fuzzy_Lower']=='MIDDLE') and  
        (fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='MIDDLE' or fuzzified_candlestick_cluster[5]['Fuzzy_Trend']=='LONG_BULLISH') and 
        (fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT' or fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='EQUAL') ):
            hanging_man['Bearish']='LOW'

        else:
            hanging_man['Bearish']='HOLD'

        identified_candlestick['Hanging_Man']=1 

    # descending hawk

    if(candlestick_cluster[4]['Body']>0.5 and
    candlestick_cluster[5]['Body']>0.5 and 
    cluster[4]['Close']>cluster[5]['High'] and 
    cluster[4]['Open']<cluster[5]['Low']):

        if(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_SHORT'):
            descending_hawk['Bearish']='LOW'      

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE'):
            descending_hawk['Bearish']='MEDIUM'   

        elif(fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG'):
            descending_hawk['Bearish']='HIGH' 

        else:
            descending_hawk['Bearish']='HOLD'

        identified_candlestick['Descending_Hawk']=1 

    # one black crow 

    if(candlestick_cluster[4]['Body']>0.5 and 
    candlestick_cluster[5]['Body']<-0.5 and 
    (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG') and 
    cluster[5]['Close']<cluster[4]['Low'] and 
    cluster[5]['Open']>cluster[4]['Body']/2):

        difopen=0
        Fuzzy_Difopen=''

        if(cluster[4]['Close'] <= cluster[5]['High']):
            difopen=0
        else:
            difopen=100*(cluster[4]['Close']- cluster[5]['High'])/cluster[4]['Close']

        fuzzy_difopen={}

        if(difopen>=0 and difopen<=0.5):
            fuzzy_difopen['NULL']=-2*difopen+1
            fuzzy_difopen['SHORT']=2*difopen
            fuzzy_difopen['MIDDLE']=0
            fuzzy_difopen['LONG']=0

            if(max(fuzzy_difopen['NULL'],
            fuzzy_difopen['SHORT'],
            fuzzy_difopen['MIDDLE'],
            fuzzy_difopen['LONG'])==fuzzy_difopen['NULL']):
                Fuzzy_Difopen='NULL'

            else:
                Fuzzy_Difopen='SHORT'

        if(difopen>0.5 and difopen<=1.5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=1
            fuzzy_difopen['MIDDLE']=0
            fuzzy_difopen['LONG']=0

            Fuzzy_Difopen='SHORT'

        if(difopen>1.5 and difopen<=2.5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=-difopen+2.5
            fuzzy_difopen['MIDDLE']=difopen-1.5
            fuzzy_difopen['LONG']=0

            if(max(fuzzy_difopen['NULL'],
            fuzzy_difopen['SHORT'],
            fuzzy_difopen['MIDDLE'],
            fuzzy_difopen['LONG'])==fuzzy_difopen['SHORT']):
                Fuzzy_Difopen='SHORT'

            else:
                Fuzzy_Difopen='MIDDLE'

        if(difopen>2.5 and difopen<=3.5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=0
            fuzzy_difopen['MIDDLE']=1
            fuzzy_difopen['LONG']=0

            Fuzzy_Difopen='MIDDLE'

        if(difopen>3.5 and difopen<=5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=0
            fuzzy_difopen['MIDDLE']=(-2*difopen+10)/3
            fuzzy_difopen['LONG']=(2*difopen-7)/3

            if(max(fuzzy_difopen['NULL'],
            fuzzy_difopen['SHORT'],
            fuzzy_difopen['MIDDLE'],
            fuzzy_difopen['LONG'])==fuzzy_difopen['LONG']):
                Fuzzy_Difopen='LONG'

            else:
                Fuzzy_Difopen='MIDDLE'

        if(difopen>5):
            fuzzy_difopen['NULL']=0
            fuzzy_difopen['SHORT']=0
            fuzzy_difopen['MIDDLE']=0
            fuzzy_difopen['LONG']=1

            Fuzzy_Difopen='LONG'

        if(Fuzzy_Difopen=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG')):
            one_black_crow['Bearish']='LOW'

        elif(Fuzzy_Difopen=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG')):
            one_black_crow['Bearish']='MEDIUM'

        elif(Fuzzy_Difopen=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG')):
            one_black_crow['Bearish']='HIGH'

        else:
            one_black_crow['Bearish']='HOLD'

        identified_candlestick['One_Black_Crow']=1

    # dark cloud clover

    if(candlestick_cluster[4]['Body']>0.5 and 
    candlestick_cluster[5]['Body']<-0.5 and 
    (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG') and 
    cluster[5]['Open']>cluster[4]['Close'] and 
    cluster[5]['Close']>cluster[4]['Open']):

        difclose=0
        Fuzzy_Difclose=''

        if(cluster[4]['High'] >= cluster[5]['Open']):
            difclose=0
        else:
            difclose=100*(cluster[5]['Open']- cluster[4]['High'])/cluster[5]['Open']

        fuzzy_difclose={}

        if(difclose>=0 and difclose<=0.5):
            fuzzy_difclose['NULL']=-2*difclose+1
            fuzzy_difclose['SHORT']=2*difclose
            fuzzy_difclose['MIDDLE']=0
            fuzzy_difclose['LONG']=0

            if(max(fuzzy_difclose['NULL'],
            fuzzy_difclose['SHORT'],
            fuzzy_difclose['MIDDLE'],
            fuzzy_difclose['LONG'])==fuzzy_difclose['NULL']):
                Fuzzy_Difclose='NULL'

            else:
                Fuzzy_Difclose='SHORT'

        if(difclose>0.5 and difclose<=1.5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=1
            fuzzy_difclose['MIDDLE']=0
            fuzzy_difclose['LONG']=0

            Fuzzy_Difclose='SHORT'

        if(difclose>1.5 and difclose<=2.5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=-difclose+2.5
            fuzzy_difclose['MIDDLE']=difclose-1.5
            fuzzy_difclose['LONG']=0

            if(max(fuzzy_difclose['NULL'],
            fuzzy_difclose['SHORT'],
            fuzzy_difclose['MIDDLE'],
            fuzzy_difclose['LONG'])==fuzzy_difclose['SHORT']):
                Fuzzy_Difclose='SHORT'

            else:
                Fuzzy_Difclose='MIDDLE'

        if(difclose>2.5 and difclose<=3.5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=0
            fuzzy_difclose['MIDDLE']=1
            fuzzy_difclose['LONG']=0

            Fuzzy_Difclose='MIDDLE'

        if(difclose>3.5 and difclose<=5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=0
            fuzzy_difclose['MIDDLE']=(-2*difclose+10)/3
            fuzzy_difclose['LONG']=(2*difclose-7)/3

            if(max(fuzzy_difclose['NULL'],
            fuzzy_difclose['SHORT'],
            fuzzy_difclose['MIDDLE'],
            fuzzy_difclose['LONG'])==fuzzy_difclose['LONG']):
                Fuzzy_Difclose='LONG'

            else:
                Fuzzy_Difclose='MIDDLE'

        if(difclose>5):
            fuzzy_difclose['NULL']=0
            fuzzy_difclose['SHORT']=0
            fuzzy_difclose['MIDDLE']=0
            fuzzy_difclose['LONG']=1

            Fuzzy_Difclose='LONG'

        if(Fuzzy_Difclose=='SHORT' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG')):
            dark_cloud_clover['Bearish']='LOW'

        elif(Fuzzy_Difclose=='MIDDLE' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG')):
            dark_cloud_clover['Bearish']='MEDIUM'

        elif(Fuzzy_Difclose=='LONG' and 
        (fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_MIDDLE' or fuzzified_candlestick_cluster[4]['Fuzzy_Body']=='WHITE_LONG')):
            dark_cloud_clover['Bearish']='HIGH'

        else:
            dark_cloud_clover['Bearish']='HOLD'

        identified_candlestick['Dark_Cloud_Clover']=1

    return identified_candlestick

def divergence(cluster):
    div='No_Divergence'
    #bullish divergence
    minx=min(cluster[0]['RSI'], 
    cluster[1]['RSI'], 
    cluster[2]['RSI'], 
    cluster[3]['RSI'], 
    cluster[4]['RSI'],
    cluster[5]['RSI'],
    )
    y=0
    x=0
    z=0
    if(minx<=30):
        for index in range(6):
            if(cluster[index]['RSI']==minx):
                z=1                
            if(cluster[index]['RSI']>30 and y==0 and z==1):
                x=1
            if(cluster[index]['RSI']<30 and x==1 and z==1):
                y=1
            if(x==1 and y==1):
                div='Bullish_Divergence'

    #bearish divergence
    maxx=max(cluster[0]['RSI'], 
    cluster[1]['RSI'], 
    cluster[2]['RSI'], 
    cluster[3]['RSI'], 
    cluster[4]['RSI'],
    cluster[5]['RSI'],
    )
    y=0
    x=0
    z=0
    if(maxx>=70):
        for index in range(6):
            if(cluster[index]['RSI']==maxx):
                z=1                
            if(cluster[index]['RSI']<70 and y==0 and z==1):
                x=1
            if(cluster[index]['RSI']>70 and x==1 and z==1):
                y=1
            if(x==1 and y==1):
                div='Bearish_Divergence'

    return(div)

def swing_rejection(cluster):
    sr='No_Swing_Rejection'
    #bullish swing rejection
    maxx=max(cluster[0]['RSI'], 
    cluster[1]['RSI'], 
    cluster[2]['RSI'], 
    cluster[3]['RSI'], 
    cluster[4]['RSI'],
    cluster[5]['RSI'],
    )
    y=0
    x=0
    l=0
    z=0
    m=0
    i=0
    for index in range(6):
        if(cluster[index]['RSI']<=30):
            z=1                
        if(cluster[index]['RSI']>30 and y==0 and x==0 and m==0 and z==1 and cluster[index]['RSI']!=maxx):
            x=1
            i=index
        if(cluster[index]['RSI']>30 and x==1 and z==1 and m==0 and y==0 and cluster[index]['RSI']>cluster[i]['RSI'] and cluster[index]['RSI']!=maxx):
            y=1
            i=index
        if(cluster[index]['RSI']>30 and x==1 and z==1 and m==0 and y==1 and l==0 and cluster[index]['RSI']<cluster[i]['RSI'] and cluster[index]['RSI']!=maxx):
            l=1
        if(cluster[index]['RSI']>30 and y==1 and x==1 and m==0 and z==1 and l==1 and cluster[index]['RSI']==maxx):
            m=1
        if(x==1 and y==1 and z==1 and m==1 and l==1):
            sr='Bullish_Swing_Rejection'

    #bearish swing rejection
    minx=min(cluster[0]['RSI'], 
    cluster[1]['RSI'], 
    cluster[2]['RSI'], 
    cluster[3]['RSI'], 
    cluster[4]['RSI'],
    cluster[5]['RSI'],
    )
    y=0
    l=0
    x=0
    z=0
    m=0
    i=0
    for index in range(6):
        if(cluster[index]['RSI']>=70):
            z=1                
        if(cluster[index]['RSI']<70 and y==0 and x==0 and m==0 and z==1 and cluster[index]['RSI']!=minx):
            x=1
            i=index
        if(cluster[index]['RSI']<70 and x==1 and z==1 and m==0 and y==0 and cluster[index]['RSI']<cluster[i]['RSI'] and cluster[index]['RSI']!=minx):
            y=1
            i=index
        if(cluster[index]['RSI']<70 and x==1 and z==1 and m==0 and y==1 and l==0 and cluster[index]['RSI']>cluster[i]['RSI'] and cluster[index]['RSI']!=minx):
            l=1
        if(cluster[index]['RSI']<70 and y==1 and x==1 and m==0 and z==1 and l==1 and cluster[index]['RSI']==minx):
            m=1
        if(x==1 and y==1 and z==1 and m==1 and l==1):
            sr='Bearish_Swing_Rejection'

    return(sr)

def Query(Previous_Trend, identified_candlestick_cluster, RSI_Trend, div, sr):
    tf1 = 0
    tf2 = 0
    tf3 = 0
    tf4 = 0
    tf5 = 0
    tf6 = 0
    tf7 = 0
    tf8 = 0
    tf9 = 0
    tf10 = 0
    tf11 = 0
    tf12 = 0
    tf13 = 0
    tf14 = 0
    tf15 = 0
    tf16 = 0
    tf17 = 0

    f1 = open(os.getcwd()+"/documents/BULLISH.txt", "r")
    f2 = open(os.getcwd()+"/documents/BEARISH.txt", "r")
    f3 = open(os.getcwd()+"/documents/NEUTRAL.txt", "r")

    for x in f1:
        prtr, cs, rsitr, divergence, swingrejection = x.strip().split(' ')
        if(prtr == Previous_Trend):
            tf1 = tf1+1
        if(cs == identified_candlestick_cluster):
            tf2 = tf2+1
        if(rsitr == RSI_Trend):
            tf3 = tf3+1
        if(divergence == div):
            tf4 = tf4+1
        if(swingrejection == sr):
            tf5 = tf5+1


    for x in f2:
        prtr, cs, rsitr, divergence, swingrejection = x.strip().split(' ')
        if(prtr == Previous_Trend):
            tf6 = tf6+1
        if(cs == identified_candlestick_cluster):
            tf7 = tf7+1
        if(rsitr == RSI_Trend):
            tf8 = tf8+1
        if(divergence == div):
            tf9 = tf9+1
        if(swingrejection == sr):
            tf10 = tf10+1


    for x in f3:
        prtr, cs, rsitr, divergence, swingrejection = x.strip().split(' ')
        if(prtr == Previous_Trend):
            tf11 = tf11+1
        if(cs == identified_candlestick_cluster):
            tf12 = tf12+1
        if(rsitr == RSI_Trend):
            tf13 = tf13+1
        if(divergence == div):
            tf14 = tf14+1
        if(swingrejection == sr):
            tf15 = tf15+1

    idf1 = log((41483/(1+tf6+tf11)),10)
    idf2 = log((41483/(1+tf7+tf12)),10)
    idf3 = log((41483/(1+tf8+tf13)),10)
    idf4 = log((41483/(1+tf9+tf14)),10)
    idf5 = log((41483/(1+tf10+tf15)),10)
    idf6 = log((41483/(1+tf11+tf1)),10)
    idf7 = log((41483/(1+tf2+tf12)),10)
    idf8 = log((41483/(1+tf13+tf3)),10)
    idf9 = log((41483/(1+tf4+tf14)),10)
    idf10 = log((41483/(1+tf15+tf5)),10)
    idf11 = log((41483/(1+tf6+tf1)),10)
    idf12 = log((41483/(1+tf7+tf2)),10)
    idf13 = log((41483/(1+tf8+tf3)),10)
    idf14 = log((41483/(1+tf9+tf4)),10)
    idf15 = log((41483/(1+tf10+tf5)),10)

    idf1l = idf1/sqrt(pow(idf1,2)+pow(idf6,2)+pow(idf11,2))
    idf2l = idf2/sqrt(pow(idf2,2)+pow(idf7,2)+pow(idf12,2))
    idf3l = idf3/sqrt(pow(idf3,2)+pow(idf8,2)+pow(idf13,2))
    idf4l = idf4/sqrt(pow(idf4,2)+pow(idf9,2)+pow(idf14,2))
    idf5l = idf5/sqrt(pow(idf5,2)+pow(idf10,2)+pow(idf15,2))
    idf6l = idf6/sqrt(pow(idf6,2)+pow(idf11,2)+pow(idf1,2))
    idf7l = idf7/sqrt(pow(idf7,2)+pow(idf12,2)+pow(idf12,2))
    idf8l = idf8/sqrt(pow(idf8,2)+pow(idf13,2)+pow(idf3,2))
    idf9l = idf9/sqrt(pow(idf9,2)+pow(idf14,2)+pow(idf14,2))
    idf10l = idf10/sqrt(pow(idf10,2)+pow(idf15,2)+pow(idf5,2))
    idf11l = idf11/sqrt(pow(idf11,2)+pow(idf6,2)+pow(idf1,2))
    idf12l = idf12/sqrt(pow(idf12,2)+pow(idf7,2)+pow(idf2,2))
    idf13l = idf13/sqrt(pow(idf13,2)+pow(idf8,2)+pow(idf3,2))
    idf14l = idf14/sqrt(pow(idf14,2)+pow(idf9,2)+pow(idf4,2))
    idf15l = idf15/sqrt(pow(idf15,2)+pow(idf10,2)+pow(idf5,2))

    tf1 = 1+log(tf1,10) if (tf1 > 0) else 0 
    tf2 = 1+log(tf2,10) if (tf2 > 0) else 0 
    tf3 = 1+log(tf3,10) if (tf3 > 0) else 0 
    tf4 = 1+log(tf4,10) if (tf4 > 0) else 0 
    tf5 = 1+log(tf5,10) if (tf5 > 0) else 0 
    tf6 = 1+log(tf6,10) if (tf6 > 0) else 0 
    tf7 = 1+log(tf7,10) if (tf7 > 0) else 0 
    tf8 = 1+log(tf8,10) if (tf8 > 0) else 0 
    tf9 = 1+log(tf9,10) if (tf9 > 0) else 0 
    tf10 = 1+log(tf10,10) if (tf10 > 0) else 0 
    tf11 = 1+log(tf11,10) if (tf11 > 0) else 0 
    tf12 = 1+log(tf12,10) if (tf12 > 0) else 0 
    tf13 = 1+log(tf13,10) if (tf13 > 0) else 0 
    tf14 = 1+log(tf14,10) if (tf14 > 0) else 0 
    tf15 = 1+log(tf15,10) if (tf15 > 0) else 0 

    tf1l = tf1/sqrt(pow(tf1,2)+pow(tf6,2)+pow(tf11,2))
    tf2l = tf2/sqrt(pow(tf2,2)+pow(tf7,2)+pow(tf12,2))
    tf3l = tf3/sqrt(pow(tf3,2)+pow(tf8,2)+pow(tf13,2))
    tf4l = tf4/sqrt(pow(tf4,2)+pow(tf9,2)+pow(tf14,2))
    tf5l = tf5/sqrt(pow(tf5,2)+pow(tf10,2)+pow(tf15,2))
    tf6l = tf6/sqrt(pow(tf6,2)+pow(tf11,2)+pow(tf1,2))
    tf7l = tf7/sqrt(pow(tf7,2)+pow(tf12,2)+pow(tf12,2))
    tf8l = tf8/sqrt(pow(tf8,2)+pow(tf13,2)+pow(tf3,2))
    tf9l = tf9/sqrt(pow(tf9,2)+pow(tf14,2)+pow(tf14,2))
    tf10l = tf10/sqrt(pow(tf10,2)+pow(tf15,2)+pow(tf5,2))
    tf11l = tf11/sqrt(pow(tf11,2)+pow(tf6,2)+pow(tf1,2))
    tf12l = tf12/sqrt(pow(tf12,2)+pow(tf7,2)+pow(tf2,2))
    tf13l = tf13/sqrt(pow(tf13,2)+pow(tf8,2)+pow(tf3,2))
    tf14l = tf14/sqrt(pow(tf14,2)+pow(tf9,2)+pow(tf4,2))
    tf15l = tf15/sqrt(pow(tf15,2)+pow(tf10,2)+pow(tf5,2))

    score1 = tf1l * idf1l + tf2l * idf2l + 	tf3l * idf3l + tf4l * idf4l + tf5l * idf5l
    score2 = tf6l * idf6l + tf7l * idf7l + 	tf8l * idf8l + tf9l * idf9l + tf10l * idf10l
    score3 = tf11l * idf11l + tf12l * idf12l + tf13l * idf13l + tf14l * idf14l + tf15l * idf15l

    if(max(score1, score2, score3)==score1):
        return "Bullish"
    elif(max(score1, score2, score3)==score2):
        return "Bearish"
    else:
        return "Neutral"

# MAIN PROGRAM

# # for main
# data = pd.read_csv("bse_data_with_rsi.csv")
# # f1=open('./doc2.txt', 'w+')
# f2=open('./doc.txt', 'w+')
# query=0


#for query
data = pd.read_csv("query_data_with_rsi.csv")
# # f1=open('./query_doc2.txt', 'w+')
f2=open('./query_doc.txt', 'w+')
query=1



data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Change', 'Upward Movement', 'Downward Movement', 'Avg UM', 'Avg DM', 'Relative Strength', 'RSI']
data = data.drop(['Date', 'Change', 'Upward Movement', 'Downward Movement', 'Avg UM', 'Avg DM', 'Relative Strength'], axis = 1)
data = data.drop([0, 1, 2, 3, 4], axis=0)

k = 1
datasheet = {}

for i,j in data.iterrows():
    d = { 'Open' : j.Open, 'High' : j.High, 'Low' : j.Low, 'Close' : j.Close, 'Body': abs(j.Open - j.Close), 'RSI': j.RSI }

    datasheet[k]=d
    k = k+1

clusters = {}

y=6
x=0
for index in range(len(datasheet)-5):
    if(index==0):
        continue
    while(y>0):
        d={0 : datasheet[index], 
         1 : datasheet[index+1],
         2 : datasheet[index+2],
         3 : datasheet[index+3],
         4 : datasheet[index+4],
         5 : datasheet[index+5]}
        clusters[x] = d
        y-=1
        x+=1
    y=6    

count_of_identified_candlestick_cluster = {
'Kicking_Bullish' : 0,
    'Kicking_Bearish' : 0,
    'Engulfing_Bullish' : 0,
    'Engulfing_Bearish' : 0,
    'Harami_Bullish' : 0,
    'Harami_Bearish' : 0,
    'Meeting_Line_Bullish' : 0,
    'Meeting_Line_Bearish' : 0,
    'Hammer' : 0,
    'Inverted_Hammer' : 0,
    'Piercing_Line' : 0,
    'One_White_Soldier' : 0,
    'Homing_Pigeon' : 0,
    'Hanging_Man' : 0,
    'Descending_Hawk' : 0,
    'One_Black_Crow' : 0,
    'Dark_Cloud_Clover' : 0}


div_count=0
sr_count=0
data_for_future_trend={}

for index in range(len(clusters)-1):
    
    identified_candlestick_cluster=""
    
    cluster=clusters[index]    
    candlestick_cluster=candlestick(cluster)
    fuzzified_candlestick_cluster=fuzzify_candlestick(candlestick_cluster)
    identified_candlestick=identify_candlestick(cluster, candlestick_cluster, fuzzified_candlestick_cluster)
    div=divergence(cluster)
    sr=swing_rejection(cluster)
    
    if(identified_candlestick['Kicking_Bullish']!=0):
        count_of_identified_candlestick_cluster['Kicking_Bullish']+=1
        identified_candlestick_cluster+="Kicking_Bullish"

    if(identified_candlestick['Engulfing_Bullish']!=0):
        count_of_identified_candlestick_cluster['Engulfing_Bullish']+=1
        identified_candlestick_cluster+="Engulfing_Bullish"

    if(identified_candlestick['Harami_Bullish']!=0):
        count_of_identified_candlestick_cluster['Harami_Bullish']+=1
        identified_candlestick_cluster+="Harami_Bullish"

    if(identified_candlestick['Meeting_Line_Bullish']!=0):
        count_of_identified_candlestick_cluster['Meeting_Line_Bullish']+=1
        identified_candlestick_cluster+="Meeting_Line_Bullish"

    if(identified_candlestick['Kicking_Bearish']!=0):
        count_of_identified_candlestick_cluster['Kicking_Bearish']+=1
        identified_candlestick_cluster+="Kicking_Bearish"

    if(identified_candlestick['Engulfing_Bearish']!=0):
        count_of_identified_candlestick_cluster['Engulfing_Bearish']+=1
        identified_candlestick_cluster+="Engulfing_Bearish"

    if(identified_candlestick['Harami_Bearish']!=0):
        count_of_identified_candlestick_cluster['Harami_Bearish']+=1
        identified_candlestick_cluster+="Harami_Bearish"

    if(identified_candlestick['Meeting_Line_Bearish']!=0):
        count_of_identified_candlestick_cluster['Meeting_Line_Bearish']+=1
        identified_candlestick_cluster+="Meeting_Line_Bearish"

    if(identified_candlestick['Hammer']!=0):
        count_of_identified_candlestick_cluster['Hammer']+=1
        identified_candlestick_cluster+="Hammer"

    if(identified_candlestick['Inverted_Hammer']!=0):
        count_of_identified_candlestick_cluster['Inverted_Hammer']+=1
        identified_candlestick_cluster+="Inverted_Hammer"

    if(identified_candlestick['Piercing_Line']!=0):
        count_of_identified_candlestick_cluster['Piercing_Line']+=1
        identified_candlestick_cluster+="Piercing_Line"

    if(identified_candlestick['Homing_Pigeon']!=0):
        count_of_identified_candlestick_cluster['Homing_Pigeon']+=1
        identified_candlestick_cluster+="Homing_Pigeon"

    if(identified_candlestick['Hanging_Man']!=0):
        count_of_identified_candlestick_cluster['Hanging_Man']+=1
        identified_candlestick_cluster+="Hanging_Man"

    if(identified_candlestick['One_White_Soldier']!=0):
        count_of_identified_candlestick_cluster['One_White_Soldier']+=1
        identified_candlestick_cluster+="One_White_Soldier"

    if(identified_candlestick['Descending_Hawk']!=0):
        count_of_identified_candlestick_cluster['Descending_Hawk']+=1
        identified_candlestick_cluster+="Descending_Hawk"

    if(identified_candlestick['One_Black_Crow']!=0):
        count_of_identified_candlestick_cluster['One_Black_Crow']+=1
        identified_candlestick_cluster+="One_Black_Crow"
        
    if(identified_candlestick['Dark_Cloud_Clover']!=0):
        count_of_identified_candlestick_cluster['Dark_Cloud_Clover']+=1
        identified_candlestick_cluster+="Dark_Cloud_Clover"
    
    if(
    identified_candlestick['Kicking_Bullish'] == 0 and 
    identified_candlestick['Kicking_Bearish'] == 0 and 
    identified_candlestick['Engulfing_Bullish'] == 0 and 
    identified_candlestick['Engulfing_Bearish'] == 0 and 
    identified_candlestick['Harami_Bullish'] == 0 and 
    identified_candlestick['Harami_Bearish'] == 0 and 
    identified_candlestick['Meeting_Line_Bullish'] == 0 and 
    identified_candlestick['Meeting_Line_Bearish'] == 0 and 
    identified_candlestick['Hammer'] == 0 and 
    identified_candlestick['Inverted_Hammer'] == 0 and 
    identified_candlestick['Piercing_Line'] == 0 and 
    identified_candlestick['One_White_Soldier'] == 0 and 
    identified_candlestick['Homing_Pigeon'] == 0 and 
    identified_candlestick['Hanging_Man'] == 0 and 
    identified_candlestick['Descending_Hawk'] == 0 and 
    identified_candlestick['One_Black_Crow'] == 0 and 
    identified_candlestick['Dark_Cloud_Clover'] == 0 ):
        identified_candlestick_cluster+="No_Candlestick_Found"
        
    

    if(div=='Bullish_Divergence'):
        div_count+=1
    if(div=='Bearish_Divergence'):
        div_count+=1
    if(sr=='Bullish_Swing_Rejection'):
        sr_count+=1
    if(sr=='Bearish_Swing_Rejection'):
        sr_count+=1
        
    Previous_Trend=''
    tr1=candlestick_cluster[1]['Trend']
    tr2=candlestick_cluster[2]['Trend']
    tr3=candlestick_cluster[3]['Trend']
    x=(tr1+tr2+tr3)/3
    
    fuzzy_trend={}

    if(x<=-5):
        fuzzy_trend['LONG_BEARISH']=1
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        Previous_Trend='BEARISH'          

    if(x>-5 and x<=-3.5):
        fuzzy_trend['LONG_BEARISH']=(-2*x-7)/3
        fuzzy_trend['MIDDLE_BEARISH']=(2*x+10)/3
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        if(max(fuzzy_trend['LONG_BEARISH'],
        fuzzy_trend['MIDDLE_BEARISH'],
        fuzzy_trend['SHORT_BEARISH'],
        fuzzy_trend['NULL'],
        fuzzy_trend['SHORT_BULLISH'],
        fuzzy_trend['MIDDLE_BULLISH'],
        fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['LONG_BEARISH']):
            Previous_Trend='BEARISH'

        else:
            Previous_Trend='BEARISH'

    if(x>-3.5 and x<=-2.5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=1
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        Previous_Trend='BEARISH'

    if(x>-2.5 and x<=-1.5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=-x-1.5
        fuzzy_trend['SHORT_BEARISH']=x+2.5
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        if(max(fuzzy_trend['LONG_BEARISH'],
        fuzzy_trend['MIDDLE_BEARISH'],
        fuzzy_trend['SHORT_BEARISH'],
        fuzzy_trend['NULL'],
        fuzzy_trend['SHORT_BULLISH'],
        fuzzy_trend['MIDDLE_BULLISH'],
        fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['MIDDLE_BEARISH']):
            Previous_Trend='BEARISH'

        else:
            Previous_Trend='BEARISH'

    if(x>-1.5 and x<=-0.5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=1
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        Previous_Trend='BEARISH'

    if(x>-0.5 and x<=0):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=-2*x
        fuzzy_trend['NULL']=2*x
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        if(max(fuzzy_trend['LONG_BEARISH'],
        fuzzy_trend['MIDDLE_BEARISH'],
        fuzzy_trend['SHORT_BEARISH'],
        fuzzy_trend['NULL'],
        fuzzy_trend['SHORT_BULLISH'],
        fuzzy_trend['MIDDLE_BULLISH'],
        fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['SHORT_BEARISH']):
            Previous_Trend='BEARISH'

        else:
            Previous_Trend='NEUTRAL'

    if(x>0 and x<=0.5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=-2*x+1
        fuzzy_trend['SHORT_BULLISH']=2*x
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        if(max(fuzzy_trend['LONG_BEARISH'],
        fuzzy_trend['MIDDLE_BEARISH'],
        fuzzy_trend['SHORT_BEARISH'],
        fuzzy_trend['NULL'],
        fuzzy_trend['SHORT_BULLISH'],
        fuzzy_trend['MIDDLE_BULLISH'],
        fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['SHORT_BULLISH']):
            Previous_Trend='BULLISH'

        else:
            Previous_Trend='NEUTRAL'

    if(x>0.5 and x<=1.5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=1
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=0

        Previous_Trend='BULLISH'

    if(x>1.5 and x<=2.5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=-x + 2.5
        fuzzy_trend['MIDDLE_BULLISH']=x - 1.5
        fuzzy_trend['LONG_BULLISH']=0

        if(max(fuzzy_trend['LONG_BEARISH'],
        fuzzy_trend['MIDDLE_BEARISH'],
        fuzzy_trend['SHORT_BEARISH'],
        fuzzy_trend['NULL'],
        fuzzy_trend['SHORT_BULLISH'],
        fuzzy_trend['MIDDLE_BULLISH'],
        fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['SHORT_BULLISH']):
            Previous_Trend='BULLISH'

        else:
            Previous_Trend='BULLISH'

    if(x>2.5 and x<=3.5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=1
        fuzzy_trend['LONG_BULLISH']=0

        Previous_Trend='BULLISH'

    if(x>3.5 and x<=5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=(-2*x+10)/3
        fuzzy_trend['LONG_BULLISH']=(2*x-7)/3

        if(max(fuzzy_trend['LONG_BEARISH'],
        fuzzy_trend['MIDDLE_BEARISH'],
        fuzzy_trend['SHORT_BEARISH'],
        fuzzy_trend['NULL'],
        fuzzy_trend['SHORT_BULLISH'],
        fuzzy_trend['MIDDLE_BULLISH'],
        fuzzy_trend['LONG_BULLISH'])==fuzzy_trend['LONG_BULLISH']):
            Previous_Trend='BULLISH'

        else:
            Previous_Trend='BULLISH'

    if(x>5):
        fuzzy_trend['LONG_BEARISH']=0
        fuzzy_trend['MIDDLE_BEARISH']=0
        fuzzy_trend['SHORT_BEARISH']=0
        fuzzy_trend['NULL']=0
        fuzzy_trend['SHORT_BULLISH']=0
        fuzzy_trend['MIDDLE_BULLISH']=0
        fuzzy_trend['LONG_BULLISH']=1

        Previous_Trend='BULLISH'
        
    r1=candlestick_cluster[1]['RSI']
    r2=candlestick_cluster[2]['RSI']
    r3=candlestick_cluster[3]['RSI']
    y=(r1+r2+r3)/3

    RSI_Trend=''
    
    if(y<=55 and y>45):
            RSI_Trend='NULL'
    if(y<=65 and y>55):
        RSI_Trend='OVERBOUGHT'
    if(y<=75 and y>65):
        RSI_Trend='OVERBOUGHT'
    if(y<=85 and y>75):
        RSI_Trend='OVERBOUGHT'
    if(y<=100 and y>85):
        RSI_Trend='OVERBOUGHT'
    if(y<=45 and y>35):
        RSI_Trend='OVERSOLD'
    if(y<=35 and y>25):
        RSI_Trend='OVERSOLD'
    if(y<=25 and y>=0):
        RSI_Trend='OVERSOLD'
    if(y<=85 and y>75):
        RSI_Trend='OVERSOLD'
    
    data_for_f_t={'Previous_Trend': Previous_Trend, 'identified_candlestick_cluster': identified_candlestick_cluster, 'RSI_Trend': RSI_Trend, 'div': div, 'sr': sr}

    f2.write(Previous_Trend + " " + 
        identified_candlestick_cluster+ " " +
        RSI_Trend + " " + 
        div + " " +
        sr + "\n"
        )
    data_for_future_trend[index]=data_for_f_t

f2.close()

doc=''

if(query==0):
    for index in range(len(clusters)-2):
        doc=data_for_future_trend[index+1]['Previous_Trend']
        filename = os.getcwd()+ "/documents/"+doc+".txt"

        f3 = open(filename, "a+")
        f3.write(data_for_future_trend[index]['Previous_Trend'] + " " + 
        data_for_future_trend[index]['identified_candlestick_cluster'] + " " +
        data_for_future_trend[index]['RSI_Trend'] + " " + 
        data_for_future_trend[index]['div'] + " " +
        data_for_future_trend[index]['sr'] + "\n"
        )
        f3.close()

if(query==1):
            
    for index in range(len(data_for_future_trend)-2):
        q=Query(data_for_future_trend[index]['Previous_Trend'], 
            data_for_future_trend[index]['identified_candlestick_cluster'], 
            data_for_future_trend[index]['RSI_Trend'], 
            data_for_future_trend[index]['div'], 
            data_for_future_trend[index]['sr'])
        print(q)
    