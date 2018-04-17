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
WWAL = -6; WWAH = 5; WHAL = -6; WHAH = 6; WBMIL = -5; WBMIH = 5  ### WHO Z_value cutoffs

class WHOCalculator(): 
    #def cal_zscore(self, val, l, m, s, z, p, f):
    def cal_zscore(self, val, param, label):
        
        biv = 0
        mdf = 0
        out = []
        
        #param = self.lms_cal(age, param, label)
        
        if val < 0: 
            print("height or weight must be positive")
            exit(-1)
        l = param[0]; m = param[1]; s = param[2]
       
        '''
       ### Who does not use the first adjustment 
        if abs(l) > 0.01:
            z = (pow((val / m), l) - 1) / (l * s)
        elif (l != None) & (abs(l) < 0.01):
            z = math.log(val/m) / s
        p = st.norm.cdf(z)
        '''
        z = (pow((val / m), l) - 1) / (l * s)
        f = z
        
        ### WHO adjustment for bmi and weight
        if (label == 'BMI' or label == 'WT') and (math.fabs(z) > 3): 
            sd2pos = m * (1+l*s*2)**(1/l)
            sd2neg = m * (1+l*s*(-2))**(1/l)
            sd3pos = m * (1+l*s*3)**(1/l)
            sd3neg = m * (1+l*s*(-3))**(1/l)
            sd23pos = sd3pos - sd2pos
            sd23neg = sd2neg - sd3neg
            if ( z > 3):
                f = 3 + (val - sd3pos)/sd23pos
            elif ( z < -3):
                f = -3 + (val - sd3neg)/sd23neg
            
        p = 100 * st.norm.cdf(f)
        
        q95 = m * (( 1 + l * s * st.norm.ppf(0.95)) ** (1/l))
        qpct95 = 100 *(val/q95)
        ##qdif95 = val - q95
        q50 =  m * (( 1 + l * s * st.norm.ppf(0.50)) ** (1/l))
        
        '''
        sdl = (m - m*pow((1 - 2 * l * s), (1/l)))/2
        sdh = (m * pow((1 + 2 * l *s), (1/l)) - m)/2
        if val < m :
            f = (val - m)/sdl
        else: f = (val - m)/sdh       
        '''       
                ### apply cutoff to label biv values
        if  (label == 'WT'):
            if ( f <= WWAL -2 ): biv = -3
            elif ( f <= WWAL - 1 ): biv = -2
            elif ( f <= WWAL ): biv = -1
            elif ( f >= WWAH + 2 ): biv = 3
            elif ( f >= WWAH + 1 ): biv = 2
            elif ( f >= WWAH ): biv = 1
            out = [z, p, f, q95, qpct95, q50, biv]
            
                
        elif  (label == 'HT'):
            if ( f <= WHAL -2 ): biv = -3
            elif ( f <= WHAL - 1 ): biv = -2
            elif ( f <= WHAL ): biv = -1
            elif ( f >= WHAH + 2 ): biv = 3
            elif ( f >= WHAH + 1 ): biv = 2
            elif ( f >= WHAH ): biv = 1
            if(biv < -2):
                mdf = val * 2.54
            else: mdf = val 
            if(f < WHAL -4 ):
                mdf4 = val * 2.54
            else: mdf4 = val 
            if(f < WHAL -3 ):
                mdf3 = val * 2.54
            else: mdf3 = val 
            out = [z, p, f, q95, qpct95, q50, biv, mdf, mdf3,mdf4]

                     
        elif  (label == 'BMI'):
            if ( f <= WBMIL -2 ): biv = -3
            elif ( f <= WBMIL - 1 ): biv = -2
            elif ( f <= WBMIL ): biv = -1
            elif ( f >= WBMIH + 2 ): biv = 3
            elif ( f >= WBMIH + 1 ): biv = 2
            elif ( f >= WBMIH ): biv = 1
            out = [z, p, f, q95, qpct95, q50, biv]
                                    
        return out
          
    def bmi_cal(self, heightcat, weight, agecat):
        bmi = 0.0
        if ((weight > 0) & (heightcat > 0)):
            bmi = weight / pow((heightcat/100), 2)   
        return bmi
            