# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

import pandas as pd
import os
from collections import defaultdict

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
    'Kicking' : 0,
    'Engulfing' : 0,
    'Harami' : 0,
    'Hammer' : 0,
    'Inverted_Hammer' : 0,
    'Piercing_Line' : 0,
    'One_White_Soldier' : 0,
    'Homing_Pigeon' : 0,
    'Meeting_Line' : 0,
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

        identified_candlestick['Kicking']=1

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

        identified_candlestick['Engulfing']=1

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

        identified_candlestick['Harami']=1      

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

        identified_candlestick['Meeting_Line']=1 



    # 2 DAY BEARISH CANDLESTICKS
    # kicking={}
    # engulfing={}
    # harami={}
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

        identified_candlestick['Kicking']=1

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

        identified_candlestick['Engulfing']=1

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

        identified_candlestick['Harami']=1 

    # meeting line

    if(candlestick_cluster[4]['Body']>0.5 and
    candlestick_cluster[5]['Body']<-0.5 and 
    cluster[4]['Close']==cluster[5]['Close']):

        if(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_SHORT'):
            meeting_line['Bearish']='LOW'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_MIDDLE'):
            meeting_line['Bearish']='MEDIUM'

        elif(fuzzified_candlestick_cluster[5]['Fuzzy_Body']=='BLACK_LONG'):
            meeting_line['Bearish']='HIGH'

        else:
            meeting_line['Bearish']='HOLD'

        identified_candlestick['Meeting_Line']=1 

    # hanging man

    if((cluster[5]['High'] > cluster[4]['High'] and 
    cluster[5]['High'] == max(cluster[5]['Open'], cluster[5]['Close'])) or 
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
    cluster[4]['Close']>=cluster[5]['High'] and 
    cluster[4]['Open']<=cluster[5]['Low']):

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
    abs(cluster[4]['Body'])>2*(abs(cluster[4]['High']-cluster[4]['Open']+abs(cluster[4]['Low']-cluster[4]['Close']))) and 
    abs(cluster[5]['Body'])>2*(abs(cluster[5]['High']-cluster[5]['Open']+abs(cluster[5]['Low']-cluster[5]['Close']))) and 
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
    abs(cluster[4]['Body'])>2*(abs(cluster[4]['High']-cluster[4]['Open']+abs(cluster[4]['Low']-cluster[4]['Close']))) and 
    abs(cluster[5]['Body'])>2*(abs(cluster[5]['High']-cluster[5]['Open']+abs(cluster[5]['Low']-cluster[5]['Close']))) and 
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

def divergence(cluster):
    div=''
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
                div='BULLISH'

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
                div='BEARISH'

    return(div)

def swing_rejection(cluster):
    sr=''
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
    z=0
    m=0
    i=0
    for index in range(6):
        if(cluster[index]['RSI']<=30):
            z=1                
        if(cluster[index]['RSI']>30 and y==0 and x==0 and m==0 and z==1 and cluster[index]['RSI']!=maxx):
            x=1
            i=index
        if(cluster[index]['RSI']>30 and x==1 and z==1 and cluster[index]['RSI']>cluster[i]['RSI'] and cluster[index]['RSI']!=maxx):
            continue
        else:
            y=1
        if(cluster[index]['RSI']>30 and y==1 and x==1 and m==0 and z==1 and cluster[index]['RSI']==maxx):
            m=1
        if(x==1 and y==1 and z==1 and m==1):
            sr='BULLISH'

    #bearish swing rejection
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
    m=0
    i=0
    for index in range(6):
        if(cluster[index]['RSI']>=70):
            z=1                
        if(cluster[index]['RSI']<70 and y==0 and x==0 and m==0 and z==1 and cluster[index]['RSI']!=minx):
            x=1
            i=index
        if(cluster[index]['RSI']<70 and x==1 and z==1 and cluster[index]['RSI']<cluster[i]['RSI'] and cluster[index]['RSI']!=minx):
            continue
        else:
            y=1
        if(cluster[index]['RSI']<70 and y==1 and x==1 and m==0 and z==1 and cluster[index]['RSI']==minx):
            m=1
        if(x==1 and y==1 and z==1 and m==1):
            sr='BEARISH'

    return(sr)

        
# MAIN PROGRAM

data = pd.read_csv("bse_data_with_rsi.csv")
data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Change', 'Upward Movement', 'Downward Movement', 'Avg UM', 'Avg DM', 'Relative Strength', 'RSI']
data = data.drop(['Date', 'Change', 'Upward Movement', 'Downward Movement', 'Avg UM', 'Avg DM', 'Relative Strength'], axis = 1)
data = data.drop([0, 1, 2, 3, 4], axis=0)

k = 1
datasheet = {}

for i,j in data.iterrows():
    d = { 'Open' : j.Open, 'High' : j.High, 'Low' : j.Low, 'Close' : j.Close, 'Body': abs(j.Open - j.Close), 'RSI': j.RSI }

    datasheet[k]=d
    k = k+1
datasheet
clusters = {}

y=6
x=0
for index in range(len(datasheet)-6):
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

identified_candlestick_cluster = {
    'Kicking' : 0,
    'Engulfing' : 0,
    'Harami' : 0,
    'Hammer' : 0,
    'Inverted_Hammer' : 0,
    'Piercing_Line' : 0,
    'One_White_Soldier' : 0,
    'Homing_Pigeon' : 0,
    'Meeting_Line' : 0,
    'Hanging_Man' : 0,
    'Descending_Hawk' : 0,
    'One_Black_Crow' : 0,
    'Dark_Cloud_Clover' : 0}


for index in range(len(clusters)):
    if(index==0 or index==1):
        continue

    cluster=clusters[index]    
    candlestick_cluster=candlestick(cluster)
    fuzzified_candlestick_cluster=fuzzify_candlestick(candlestick_cluster)
    identified_candlestick=identify_candlestick(cluster, candlestick_cluster, fuzzified_candlestick_cluster)
    div=divergence(cluster)
    sr=swing_rejection(cluster)
#     print(identified_candlestick)
    if(identified_candlestick['Kicking']!=0):
        identified_candlestick_cluster['Kicking']+=1
    if(identified_candlestick['Engulfing']!=0):
        identified_candlestick_cluster['Engulfing']+=1
    if(identified_candlestick['Harami']!=0):
        identified_candlestick_cluster['Harami']+=1
    if(identified_candlestick['Hammer']!=0):
        identified_candlestick_cluster['Hammer']+=1
    if(identified_candlestick['Inverted_Hammer']!=0):
        identified_candlestick_cluster['Inverted_Hammer']+=1
    if(identified_candlestick['Piercing_Line']!=0):
        identified_candlestick_cluster['Piercing_Line']+=1
    if(identified_candlestick['One_White_Soldier']!=0):
        identified_candlestick_cluster['One_White_Soldier']+=1
    if(identified_candlestick['Homing_Pigeon']!=0):
        identified_candlestick_cluster['Homing_Pigeon']+=1
    if(identified_candlestick['Meeting_Line']!=0):
        identified_candlestick_cluster['Meeting_Line']+=1
    if(identified_candlestick['Hanging_Man']!=0):
        identified_candlestick_cluster['Hanging_Man']+=1
    if(identified_candlestick['One_White_Soldier']!=0):
        identified_candlestick_cluster['One_White_Soldier']+=1
    if(identified_candlestick['Descending_Hawk']!=0):
        identified_candlestick_cluster['Descending_Hawk']+=1
    if(identified_candlestick['One_Black_Crow']!=0):
        identified_candlestick_cluster['One_Black_Crow']+=1
    if(identified_candlestick['Dark_Cloud_Clover']!=0):
        identified_candlestick_cluster['Dark_Cloud_Clover']+=1

# #         identified_candlestick_cluster[index-2]=identified_candlestick

identified_candlestick_cluster
# cluster=clusters[0]
# candlestick_cluster=candlestick(cluster)
# fuzzified_candlestick_cluster=fuzzify_candlestick(candlestick_cluster)
# identified_candlestick=identify_candlestick(cluster, candlestick_cluster, fuzzified_candlestick_cluster)

# candlestick_cluster
# cluster
# fuzzified_candlestick_cluster

