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
# print(df_study.loc[(df_study['INDDID'] == '122152') & (df_study['PETDate'] == '6/8/17')])
# print(df_study.loc[(df_study['PETDate'] == '6/8/17')])

#file to record any sessions stil unidentified
# o = open('PET_need_study_decimals.txt', 'a')

#loop through each session needing a study ID'ed
needstudy = open('PET_need_study.txt','r') 
for line in needstudy:
    # print('*****************************************************************************')
    #reset variables to empty strings
    indd=''
    date=''
    study=''
    
    line = line.strip()

    linelist = line.split('x')
    if len(linelist[1]) == 2:
        indd= '.'.join(linelist[0:2]) ##to match PET session csv
    else:
        indd=linelist[0]
    # print(type(indd))
    
    date=linelist[-3] 
    if date[4] == '0':
        month = date[5]
    else:
        month = date[4:6]
    if date[6] == '0':
        day = date[7]
    else:
        day = date[6:]
    
    dateMDY= month + '/' + day + '/' + date[2:4] ##year is only 2 digits now(?)
    # print(dateMDY)

    scantype=linelist[-2]
    if scantype!='FBBPET':
        # print(f'not an FBB PET scan')
        continue
    elif scantype=="FBBPET":
        dfmatch=df_study.loc[(df_study['INDDID'] == indd) & (df_study['PETDate'] == dateMDY)]
        #check that dfmatch has only 1 row
        # print(dfmatch)
        if len(dfmatch) == 1:
            petprotocol = dfmatch['PETProtocol'].iloc[0]
            tracer = dfmatch['PETTracer'].iloc[0]
            if 'Florbetapir (amyloid)' in tracer:   
                tracershort='FlorbetapirPET'
                # print(f'This session should be FBP, was mis-typed: {scantype}')
            elif 'Florbetaben' in tracer:
                tracershort = 'FBBPET'
            elif 'AV1451 (tau)' in tracer:
                tracershort='AV1451PET'
            else:
                tracershort=''
            # print(f'From spreadsheet: {tracer}, from renamed flywheel: {scantype}')

            # print(f'{line} is {petprotocol}')
            # print(petprotocol)
            if petprotocol == 'ABCD2':
                study = 'ABCD2'
            elif petprotocol == 'LEADS':
                study = "LEADS"
            elif petprotocol == 'REVEAL-SCAN 825741':
                study = "REVEAL"
            elif petprotocol == "Clinical Trial" or petprotocol == "ADNI" or petprotocol == 'IDEAS':
                study='Other'
            elif petprotocol == "NACC_API": 
                study='ABC'
            else:
                study = ''    


            if study == '':
                # o.write(f"{line}, study\n")
                print(f'{indd},{dateMDY} matched but study not IDed') 
                break
            else: 
                # newlabel = line + study
                newlabel=indd +'x'+ date+'x'+tracershort+'x'+study
                # print(newlabel)
            
            # try:
            #     session = project.sessions.find(f'label={line}')
            # except flywheel.ApiException as e:
            #     print(f'Error: {e}') 
            
            # print(f'Found session: {session[0].label}')
            print(f'Renaming {line} session to: {newlabel}')
            # session[0].update({'label': newlabel})

        else:
            # o.write(f"{line}\n")
            # print(f"INDDID, Date {indd}, {dateMDY} not found in Dave's list")
            continue
    
# o.close()