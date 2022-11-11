import pandas as pd
from datetime import datetime
import flywheel

fw = flywheel.Client()
#select project by project ID
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

df_study=pd.read_csv('MRISessionList_with_study.csv')
df_study['INDDID']=df_study['INDDID'].astype(int).astype(str)
df_study['MRIDate']=df_study['MRIDate'].astype(str)

needstudy = open('3T_need_study.txt','r')
for line in needstudy:
    #reset variables to empty strings
    indd=''
    date=''
    study=''
    
    line = line.strip()
    try:
        session = project.sessions.find(f'label={line}')
    except flywheel.ApiException as e:
        print(f'Error: {e}')

    #to find study
    linelist = line.split('x')
    if len(linelist[1]) == 2:
        indd= '.'.join(linelist[0:2]) ##to match MRI session csv
    else:
        indd=linelist[0]
    date=linelist[-3]
    dateYMD=date[4:6] + '/' + date[6:] + '/' + date[0:4]

    dfmatch=df_study.loc[(df_study['INDDID'] == indd) & (df_study['MRIDate'] == dateYMD)]

    #check that dfmatch has only 1 row
    if len(dfmatch) == 1:
        mriprotocol = dfmatch['MRIProtocol'].iloc[0]
        scanner = dfmatch['Scanner'].iloc[0]
    
        if mriprotocol == 'ABCD2' and scanner == 'SC (3T)':
            study = 'ABCD2'
        elif mriprotocol == 'NACC-SC' or mriprotocol == 'Young MTL' and scanner == 'SC (3T)':
            study='ABC'
    
        newlabel = line + study
        print(f'Renaming {line} session to: {newlabel}') 
        # session[0].update({'label': newlabel})
    else:
        print(f'{line} INDD & Date not in MRIsession list')