##Sessions where study couldn't be determined from Performed Procedure Step Description

import pandas as pd
import flywheel

fw = flywheel.Client()
#select project by project ID
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

#Load list from INDD database/Dave
df_study=pd.read_csv('PETSEssionList_with_study.csv') 
df_study['INDDID']=df_study['INDDID'].astype(int).astype(str)
df_study['PETDate']=df_study['PETDate'].astype(str)
# df_study.info()

#file to record any sessions stil unidentified
# o = open('PET_need_study_still.txt', 'a')

#loop through each session needing a study ID'ed
needstudy = open('PET_need_study.txt','r') 
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
    dateDMY=date[4:6] + '/' + date[6:] + '/' + date[0:4]
    scantype=linelist[-2]
    # print(scantype)

    dfmatch=df_study.loc[(df_study['INDDID'] == indd) & (df_study['PETDate'] == dateDMY)]
    
    #check that dfmatch has only 1 row
    if len(dfmatch) == 1:
        petprotocol = dfmatch['PETProtocol'].iloc[0]
        # print(petprotocol)
        tracer = dfmatch['PETTracer'].iloc[0]
        if 'Florbeta' in tracer:
            tracershort='FBBPET'
        elif 'AV1451 (tau)' in tracer:
            tracershort='AV1451PET'
        else:
            tracershort=''

        if tracershort == scantype:
            # print(f'Confirm tracer {tracer} and scantype {scantype} match')
            if petprotocol == 'ABCD2':
                study = 'ABCD2'
            elif petprotocol == 'LEADS':
                study = "LEADS"
            else:
                study='ABC'
        else:
            print(f'Tracer cannot be matched for {indd},{dateDMY}')
            break

        if study == '':
            # o.write(f"{line}, something wrong\n")
            print(f'{indd},{dateDMY} matched but study not IDed') 
            break
        else: 
            newlabel = line + study
 
        print(f'Renaming {line} session to: {newlabel}')
#         try:
#             session = project.sessions.find(f'label={line}')
#         except flywheel.ApiException as e:
#             print(f'Error: {e}') 
        
#         session[0].update({'label': newlabel})

    else:
        # o.write(f"{line}\n")
        print(f"INDDID, Date {indd}, {dateDMY} not found in Dave's list")

# o.close()


