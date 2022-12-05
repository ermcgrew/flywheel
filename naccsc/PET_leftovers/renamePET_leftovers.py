##Sessions where study couldn't be determined from Performed Procedure Step Description, compare to indd csv from Dave
##run before with incorrect coding for study, so this version also uses that log

#list of sessions renamed from florbetapir
# cat rename_log_20221108_2.txt | grep -A 2 Florbetapir | sed '/--/d' | 
# 	sed '/No matching performed procedure step description found, making note.../d' | 
# 	sed 's/Renaming //g' | cut -f 3 -d " " >> florbetapir.txt  

# cat renamedflorbetapir.txt | while read line ; do grep -R $line "PET_need_study.txt" ; done | wc -l
#matches--all florbetapir sessions in leftover PET batch


import pandas as pd
import flywheel
fw = flywheel.Client()
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
except flywheel.ApiException as e:
    print(f'Error: {e}')

#Load list from INDD database/Dave
df_study=pd.read_csv('PETSEssionList_with_study.csv') 
df_study['INDDID']=df_study['INDDID'].astype(str)  
df_study.drop(df_study[df_study['INDDID'].str.len()==9].index,inplace=True) ##drop any .01, .02, matching is messy, do manually
df_study['INDDID']=df_study['INDDID'].str.split('.').str[0] #get rid of decimal after Indd #
df_study['PETDate']=df_study['PETDate'].astype(str) 
df_study.drop_duplicates(subset=['INDDID','PETDate'],keep='first',inplace=True)
# df_study.info()

##log of renamed sessions to use for retrieval from flywheel
dfrename=pd.read_csv('renamePetPairs.csv')

#file to record any sessions stil unidentified
o = open('PET_fbprun_not_renamed.txt', 'a')

#loop through each session needing a study ID'ed
needstudy = open('PET_need_study.txt','r') 
for line in needstudy:
    #reset variables to empty strings
    indd=''
    date=''
    study=''
    
    line = line.strip()

    linelist = line.split('x')
    if len(linelist[1]) == 2:
        indd= '.'.join(linelist[0:2]) #to match PET session csv
    else:
        indd=linelist[0]
    
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
    
    dfmatch=df_study.loc[(df_study['INDDID'] == indd) & (df_study['PETDate'] == dateMDY)]
    # print(dfmatch)
    # check that dfmatch has only 1 row
    if len(dfmatch) == 1:
        petprotocol = dfmatch['PETProtocol'].iloc[0]
        tracer = dfmatch['PETTracer'].iloc[0]
        if 'Florbetapir (amyloid)' in tracer:   
            tracershort='FlorbetapirPET'
        elif 'Florbetaben' in tracer:
            tracershort = 'FBBPET'
        elif 'AV1451 (tau)' in tracer:
            tracershort='AV1451PET'
        else:
            tracershort=''

        # print(f'{line} is {petprotocol}')
        if petprotocol == 'ABCD2':
            study = 'ABCD2'
        elif petprotocol == 'LEADS':
            study = "LEADS"
        elif petprotocol == 'REVEAL-SCAN 825741':
            study = "REVEAL"
        elif petprotocol == "Clinical Trial" or petprotocol == "ADNI" or petprotocol == 'IDEAS' or petprotocol == "F-AV-1451 AVID":
            study='Other'
        elif 'NACC' in petprotocol: 
            study='ABC'
        else:
            study = ''    

        if study == '':
            o.write(f"{line}, study\n")
            print(f'{indd},{dateMDY} matched but study not IDed') 
            continue
        if tracershort=='': 
            o.write(f"{line}, scantype\n")
            print(f'{indd},{dateMDY} matched but scantype not IDed')
            continue
        else: 
            newlabel=indd +'x'+ date+'x'+tracershort+'x'+study
        
        dfrenamematch = dfrename.loc[dfrename['old'] == line]
        currentFWname=dfrenamematch['new'].iloc[0]

        try:
            session = project.sessions.find(f'label={currentFWname}')
        except flywheel.ApiException as e:
            print(f'Error: {e}') 
        
        # print(session)
        print(f'Found session: {session[0].label}')
        print(f'Renaming {line} session to: {newlabel}')
        session[0].update({'label': newlabel})

    else:
        o.write(f"{line},no match\n")
        print(f"INDDID, Date {indd}, {dateMDY} not matched")
        continue
    
o.close()