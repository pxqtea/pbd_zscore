'''
Created on Sep 18, 2017

@author: pangx
'''
import pandas as pd
import math
import scipy.stats as st
import numpy as np
import pandas as pd
from CDC_Calculator3 import CDCCalculator 
from WHO_Calculator3 import WHOCalculator
from bokeh.layouts import column
from datetime import datetime
from numba.types import none
import math
import csv
from operator import itemgetter
import operator
from blaze import inf




 ## The input file with columns (agemons, agedays, height, weight, dob, measurement date, etc... )
global INPUT, CDCPARAM, WHOPARAM, OUTOUT, WWAL, WWAH, WHAL, WHAH, WBMIL, WBMIH, CWAL, CWAH, CHAL, CHAH, CBMIL, CBMIH, params, outs, variablist 
WWAL = -6; WWAH = 5; WHAL = -6; WHAH = 6; WBMIL = -5; WBMIH = 5  ### WHO Z_value cutoffs
CWAL = -5; CWAH = 8; CHAL = -5; CHAH = 4; CBMIL = -4; CBMIH = 8  ### CDC Z_value cutoffs
outs, cdcouts, whoouts = [], [], []


params = ['L', 'M', 'S']
variablist = ['HT', 'WT', 'BMI']
 
titleline = ['id', 'agemos', 'height',  'date','hz', 'hp', 'hf', \
             'hq95', 'hpct95', 'hq50', 'hbiv', 'hmdf', 'hmdf3', 'hmdf4']
  
cdctitle =  ['id', 'agemos', 'weight', 'hagemos',  'height', 'obmiz', 'sex']
whotitle =  ['id', 'agedays', 'weight', 'hagemos',  'height', 'obmiz', 'sex']

## input data structure: 
# person_id, measurement_id(wt/ht), dob, agemons, agedays, height, weight,  
##output data structure:
#person_id, measurement_id, dob, agemons, agedays, height, weight, bmi, height_z, weight_z, bmi_z, bivh, bivw, bivbmi, bmi50, bmi95
##cdc data structure:
##format of the CDC file (age from 23.5 to 239.5 month ) and weight_for_height with height in (45, 121cm)
#sex, agemos1/2, _L/M/S(HT/WT/BMI/HC)1/2

##WHO data structure:
##format of the WHO file (included age upto 1856, but will be used on kids younger than 2 only, and weight_for_height with height in (45, 110cm)): 
#sex, agedays, _bmi/height/weight/headc/_l/m/s (also have subscapular/triceps skinfold thickness and arm circumference measurments)



def cdc_run(cdc_input, gender, cdcfile):
    ##cdc_input as a list sorted on wagemos
    print("run CDC calculator for age > 24 months for ", len(cdc_input), "measurements")
    cdcparams = pd.read_csv(cdcfile) 
    cdcparams = cdcparams.loc[(cdcparams['SEX'] == gender)]
    cdcparams.reset_index(drop=True, inplace=True)
    ##cdc_input.reset_index(drop=True, inplace=True)
    cdcsize = len(cdcparams)
    if cdcsize == 0: 
        print("parameter file is empty"); exit(-1)
    
    cdcparams = cdcparams.values.tolist()
        
    cdc = CDCCalculator()
    
    wparam, hparam, bparam = [], [], []
    hptr = 0
    
    for row in cdc_input:

        hage = row[1]
        while ( (hage >cdcparams[hptr][6]) & (hptr < cdcsize)):
            hptr +=1
        if(hptr == cdcsize): print("age out of CDC_ref range"); exit(-1)
                
        hparam = cdcparams[hptr][11:17] + [cdcparams[hptr][2]] # + cdcparams.loc[hptr:hptr, 1:1].values.tolist() 

        height = row[2]  #cdc.height_stat(row[4])
        
        #if (height <= 0  ):
        #    print(row); exit(-1)

        htmp = cdc.cal_zscore(height, hage, hparam, 'HT' )
                
        '''
        if (row[5] == 0): bmi = cdc.bmi_cal(height, weight, wage)
        else:  bmi = row[5]
        '''

        outs.append(row + htmp )    ## the new bmi is also calculated with CDC method                

def who_run(who_input, gender, whofile):
    print("run WHO calculator for age <= 24 months for ", len(who_input), "measurements" )

    whoparams = pd.read_csv(whofile) 
    whoparams = whoparams.loc[(whoparams['sex'] == gender)]
    whoparams.reset_index(drop=True, inplace=True)
    ##cdc_input.reset_index(drop=True, inplace=True)
    whosize = len(whoparams)
    if whosize == 0:
        print("parameter file is empty"); exit(-1)
    
    whoparams = whoparams.values.tolist()

    who = WHOCalculator()

    out = []
    bmi = 0.0
    
    wparam, hparam, bparam = [], [], []
    
    for row in who_input:
        #print(wptr, wage, row[0], whoparams[wptr])
        hage = round(row[1] * 30.4)
        if (hage < whosize):
            hparam = whoparams[hage][20:23] + [whoparams[hage][1]] # + cdcparams.loc[hptr:hptr, 1:1].values.tolist() =
        elif(hage == whosize): print("age out of WHO_ref range"); exit(-1)
                
        height = row[2]   # who round up to 0.01  who.height_stat(row[4])
        
        if (height < 0 ):
            print(row); exit(-1)


        htmp = who.cal_zscore(height, hparam, 'HT' )

        outs.append(row + htmp )
        
        
def main(infile, gender, cdcfile, whofile):
    path = '/Users/pangx/Documents/data/project1/codes/'
    
    #input = [person_id, dob, m_date, bmiz, height, weight]
    outfile = infile + '_out_md2_date.csv'
    cdcin = infile + '_cdcin.csv'
    whoin = infile + '_whoin.csv'
    cdcout = infile + '_cdcout_md2_date.csv'
    whoout = infile + '_whoout_md2_date.csv'

    infile = path + infile + '.csv'
    '''
    input = []
    with open(infile, 'r') as f: 
        for line in f: 
            elm = line.split()
            input.append(elm)
     '''   
    if (gender == 'F'):
        gender = 2
    elif (gender == 'M'):
        gender = 1
    else: 
        print("Please enter: input file, gender, cdc_ref file, who_ref file")
        exit()
    
    INPUT=pd.read_csv(infile, skiprows = 0, delimiter = ',')
    #newlines = INPUT['row'].str.strip('()').apply(lambda x: pd.Series(x.split(',')))

    #INPUT = pd.read_csv(infile) 

    INPUT.head(n=5)
    #print(type(INPUT))
    INPUT = INPUT.sort_values(['age_mon_rec'])    #print(INPUT)
    
    colist = INPUT.columns.tolist()
   # print(colist)
    columndic = dict((i, j) for j, i in enumerate(colist) )
    
    #print(columndic)
    
    allinput = INPUT.values.tolist()    #print(input)
    print(len(allinput), " number of measurements read in")

    
    whoinput = []
    cdcinput = []
    tmp = []
    
    #print(columndic['id'])
    #print(allinput)
    
    for element in allinput:
        #print(element)
        '''
        if 'bmiz' in columndic: 
            tmp = [element[columndic[i]] for i in ['id', 'age_mon_rec', 'result', 'hagemos',  'height', 'bmiz']]
        else: 
            tmp = [element[columndic[i]] for i in ['id', 'wagemos', 'weight', 'hagemos',  'height']]
            tmp = tmp + [0]       
        '''
         
        tmp = [element[columndic[i]] for i in ['person_id', 'age_mon_rec', 'result', 'date']]
            
        if(element[columndic['age_mon_rec']] <= 24):
            whoinput.append(tmp)
            #print(tmp[1])
        else:   #if(element[columndic['wagemos']] > 24):
            cdcinput.append(tmp)

    '''
    with open(cdcin, 'w') as f:
        wr = csv.writer(f)
        wr.writerow(cdctitle)
        for row in cdcinput: 
            wr.writerow( row + [gender])
            #print(row)
            
        
    with open(whoin, 'w') as f:
        wr = csv.writer(f)
        wr.writerow(whotitle)
        for row in whoinput: 
            wr.writerow(row + [gender])
    '''
    #print(cdcinput)
    #print(whoinput)
    
    #who_tmp = INPUT.loc[ (INPUT['agemos'] < 24) ].sort_values(['agemos'])
    #cdc_tmp = INPUT.loc[ (INPUT['agemos'] >= 24) ].sort_values(['agemos'])  ##

    #who_tmp.head(n=5)
    #cdc_tmp.head(n=5)
    #print(cdc_tmp)
    
    ##only CDC calculation is work at this moment
    
    if(len(whoinput) >0 ):
        who_run(whoinput, gender, whofile)
    if (len(cdcinput) >0 ):
        cdc_run(cdcinput, gender, cdcfile)
    
    #print(OUTPUT)   
    
    outs.sort(key=operator.itemgetter(0), reverse=False)
    
    
    with open(outfile, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(titleline)
        wr.writerows(outs)
    '''
    with open(cdcout, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(titleline)

        wr.writerows(cdcouts)
        
    with open(whoout, 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(titleline)
        wr.writerows(whoouts)
    '''
    print("The total # of measurements calculated were: ", len(outs))
    #print("The # of measurement with height_biv > 1 is: ", len(OUTPUT.loc[OUTPUT['HTbiv'] > 1]))
    #print("The # of measurement with weight_biv > 1 is: ", len(OUTPUT.loc[OUTPUT['WTbiv'] > 1]))
    
    
    print("done!")

if __name__ == '__main__':
    #main('./heightscreen_8532_3023540', 'F','./cdcref_d.csv', './WHOref_d_pxq.csv')  
    main('./heightscreen_8507_3023540', 'M','./cdcref_d.csv', './WHOref_d_pxq.csv')  
    


    #main('./test3', 'F','./cdcref_d.csv', './WHOref_d_pxq.csv')  
