'''
Created on Sep 18, 2017

@author: pangx
'''
import pandas as pd
import math
import scipy.stats as st
import numpy as np
import pandas as pd
from _pytest.compat import NoneType

##should put into a param list
CWAL = -5; CWAH = 8; CHAL = -5; CHAH = 4; CBMIL = -4; CBMIH = 8 

class CDCCalculator(): 
    #def cal_zscore(self, val, l, m, s, z, p, f):
    def cal_zscore(self, val, age, param, label):
        
        biv = 0
        mdf = 0
        z = 0.0
        out = []
        
        param = self.lms_cal(age, param, label)
        l = param[0]; m = param[1]; s = param[2]

        if  val < 0: 
            print("height or weight must be positive")
            exit(-1)
        elif (val == 0):
            z = f = -50
        else:             
            if abs(l) > 0.01:
                z = (pow((val / m), l) - 1) / (l * s)
            elif (l != None) & (abs(l) < 0.01):
                z = math.log(val/m) / s

            if (val < m ) :
                sdl = (m - m*pow((1 - 2 * l * s), (1/l)))/2
                f = (val - m)/sdl
            else: 
                sdh = (m * pow((1 + 2 * l *s), (1/l)) - m)/2
                f = (val - m)/sdh                
                ### apply cutoff to label biv values
        #print(val, age, param, label, sdl, sdh, f)
                    
        p = 100 * st.norm.cdf(z)   
                   
        q95 = m * (( 1 + l * s * st.norm.ppf(0.95)) ** (1/l))
        qpct95 = 100 *(val/q95)
        q50 =  m * (( 1 + l * s * st.norm.ppf(0.50)) ** (1/l))    
            
            
        if  (label == 'WT'):
            if ( f <= (CWAL -2) ): biv = -3
            elif ( f <= (CWAL - 1) ): biv = -2
            elif ( f <= CWAL ): biv = -1
            elif ( f >= (CWAH + 2) ): biv = 3
            elif ( f >= (CWAH + 1) ): biv = 2
            elif ( f >= CWAH ): biv = 1
            out = [z, p, f,  q95, qpct95, q50, biv ]
            
                
        elif  (label == 'HT'):
            if ( f <= (CHAL -2) ): biv = -3
            elif ( f <= (CHAL - 1) ): biv = -2
            elif ( f <= CHAL ): biv = -1
            elif ( f >= (CHAH + 2) ): biv = 3
            elif ( f >= (CHAH + 1) ): biv = 2
            elif ( f >= CHAH ): biv = 1
            if(biv < -2):
                mdf = val * 2.54
            else: mdf = val 
            if(f < (CHAL - 3)):
                mdf3 = val * 2.54
            else: mdf3 = val 
            if(f < (CHAL - 4)):
                mdf4 = val * 2.54
            else: mdf4 = val 
            out = [z, p, f,  q95, qpct95, q50, biv, mdf, mdf3, mdf4 ]

                     
        elif  (label == 'BMI'):
            if ( f <= (CBMIL -2) ): biv = -3
            elif ( f <= (CBMIL - 1) ): biv = -2
            elif ( f <= CBMIL ): biv = -1
            elif ( f >= (CBMIH + 2 )): biv = 3
            elif ( f >= (CBMIH + 1) ): biv = 2
            elif ( f >= CBMIH ): biv = 1
            out = [z, p, f,  q95, qpct95, q50, biv ]
                                    
        return out

##may not need here
    def age_stat(self, agemon):
        if (agemon > 0 ) & (agemon < 0.5):
            agecat = 0
        elif agemon != None:
            agecat = int(agemon + 0.5) - 0.5
        return agecat
          
    def bmi_cal(self, heightcat, weight, agecat):
        bmi = 0.0
        if ((agecat >= 24) & (weight > 0) & (heightcat > 0)):
            bmi = weight / pow((heightcat/100), 2)   
        return bmi
            
    def height_stat(self, height):
        if (height > 77.5):
            heightcat = int (int (height +0.5) - 0.5)
        elif (height >= 77):
            heightcat = 77
        else: heightcat = height
        print(height, heightcat)
        return heightcat
            
####not needed in who calculations, because age is in days; in cdc parameters are estimated to from those two cloest months
    def lms_cal(self, age,  param, item):
        #ageint = param.loc(param['_AGEMOS2']) - param.loc(param['_AGEMOS1'])
        #print(param)
        ageint = 1
        deltage = age - param[6]
        calparam = []
        
        #print()
        for i in range(3):
            cal = param[i] + deltage * (param[i+3] - param[i]) /ageint
            calparam += [cal]
            
        #print(param0)
        return calparam