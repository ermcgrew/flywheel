import pandas as pd
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

##Sessions that had study suffix originally and was mistakenely overwritten
#cat rename_log_20221108_2.txt | grep -C 1 manually | sed '/--/d’ | grep ABC | cut -f 3 -d " " >> log_OG_sessionNames.txt
with open('log_OG_sessionNames.txt') as f:
    ognames = f.readlines()
    f.close()
nameDict={}
for x in ognames:
    y=x.split('x')
    if len(y[1]) == 2:
        key=y[0:4]
        key2='x'.join(key)
        key2=key2 + 'x'   
    else:
        key=y[0:3]
        key2='x'.join(key)
        key2=key2 + 'x'   
    value=y[-1]
    value=value.strip()
    nameDict[key2]=value

o = open('3T_need_study_still.txt', 'a')

needstudy = open('after_error.txt','r') #3T_need_study.txt
for line in needstudy:
    #reset variables to empty strings
    indd=''
    date=''
    study=''
    
    line = line.strip()

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
    
        if study == '':
            o.write(f"{line}, something wrong\n")
        else: 
            newlabel = line + study

        ##check against rename_log for existing study label
        if line in nameDict:
            if study == nameDict[line]:
                print(f'Original study {nameDict[line]} matches newly assigned study {study}')
            else:
                print(f'flagging session {line} for review before renaming')
                o.write(f"{line}, something wrong\n")
                break
 
        print(f'Renaming {line} session to: {newlabel}')
        try:
            session = project.sessions.find(f'label={line}')
        except flywheel.ApiException as e:
            print(f'Error: {e}') 
        
        session[0].update({'label': newlabel})

    else:
        o.write(f"{line},not in Dave's list\n")

o.close()


