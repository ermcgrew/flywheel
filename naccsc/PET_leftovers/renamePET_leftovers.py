##Sessions where study couldn't be determined from Performed Procedure Step Description

import pandas as pd
import flywheel

fw = flywheel.Client()
#select project by project ID
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
except flywheel.ApiException as e:
    print(f'Error: {e}')

#Load list from INDD database/Dave
df_study=pd.read_csv('PETSEssionList_with_study.csv') 
df_study['INDDID']=df_study['INDDID'].astype(int).astype(str) ##lose any .01, .02 subs, do those manually
df_study['PETDate']=df_study['PETDate'].astype(str)
df_study.drop_duplicates(subset=['INDDID','PETDate'],keep='first',inplace=True)

# df_study.info()

#file to record any sessions stil unidentified
o = open('PET_need_study_decimals.txt', 'a')

#loop through each session needing a study ID'ed
needstudy = open('PET_need_study_still.txt','r') 
for line in needstudy:
    # print('*****************************************************************************')
    #reset variables to empty strings
    indd=''
    date=''
    study=''
    
    line = line.strip()

    #fill in INDDID & Date variables
    linelist = line.split('x')
    if len(linelist[1]) == 2:
        indd= '.'.join(linelist[0:2]) ##to match PET session csv
    else:
        indd=linelist[0]
    
    date=linelist[-3] 
    # date, from list: 20140723, YYYYMMDD
    # Year = date[0:4]
    # Month  = date[4:6]
    # Day  = date[6:]

    # needs to match session csv: 7/23/2014, MM/DD/YYYY 
    #if 0th position in MM and DD are 0, drop it
    if date[4] == '0':
        month = date[5]
    else:
        month = date[4:6]

    if date[6] == '0':
        day = date[7]
    else:
        day = date[6:]

    dateMDY= month + '/' + day + '/' + date[0:4]
    
    scantype=linelist[-2]

    dfmatch=df_study.loc[(df_study['INDDID'] == indd) & (df_study['PETDate'] == dateMDY)]
    
    #check that dfmatch has only 1 row
    if len(dfmatch) == 1:
        petprotocol = dfmatch['PETProtocol'].iloc[0]
        tracer = dfmatch['PETTracer'].iloc[0]
        if 'Florbeta' in tracer:   
            tracershort='FBBPET'
        elif 'AV1451 (tau)' in tracer:
            tracershort='AV1451PET'
        else:
            tracershort=''

        if tracershort == scantype:
            # print(f'{line} is {petprotocol}')
            if petprotocol == 'ABCD2':
                study = 'ABCD2'
            elif petprotocol == 'LEADS':
                study = "LEADS"
            elif petprotocol == 'REVEAL-SCAN 825741':
                study = "REVEAL"
            else: 
                study='ABC'
        else:
            o.write(f"{line}, tracer\n")
            print(f'Tracer cannot be matched for {indd},{dateMDY}')
            break

        if study == '':
            o.write(f"{line}, study\n")
            print(f'{indd},{dateMDY} matched but study not IDed') 
            break
        else: 
            newlabel = line + study
        
        try:
            session = project.sessions.find(f'label={line}')
        except flywheel.ApiException as e:
            print(f'Error: {e}') 
        
        print(f'Found session: {session[0].label}')
        print(f'Renaming {line} session to: {newlabel}')
        session[0].update({'label': newlabel})

    else:
        o.write(f"{line}\n")
        print(f"INDDID, Date {indd}, {dateMDY} not found in Dave's list")
  
o.close()