from datetime import datetime
import flywheel
#user must be logged into flywheel via CLI to use flywheel.client()
fw = flywheel.Client()

#select project by project ID
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

#create list of sessions
try:
    sessions = project.sessions.iter_find('created>2022-08-19') #subset to test on: created>2022-07-19  label=101628_01_20180508_7T
except flywheel.ApiException as e:
    print(f'Error: {e}')
 
#look at each session and rename as appropriate
for count, session in enumerate(sessions, 1):
    print(f'***********session loop {count}: {session.label}******************')
    ########ID incorrect session labels########    
    #once a session fails an if (fails to match correct format), go to rename block
    if session.label[0:6] == session.subject.label:
        print('subject ID test passed')
        if session.label[7:15] == str(session.timestamp)[:10].replace('-',''): 
            print('date test passed')
            if session.label[16:18] == '3T' or session.label[16:18] =='7T' or session.label[16:25] == 'PI2620PET' or session.label[16:22] == 'FBBPET' or session.label[16:25] == 'AV1451PET':
                print('scantype test passed')
                if session.label[-3:] == 'ABC' or session.label[-5:] =="ABCD2" or session.label[-5:] == 'DVCID':
                    print('study suffix correct')
                    print(f'Session name {session.label} is correct, skipping session.')
                    continue
    #if subject has _01 or x02:
    elif session.label[0:9] == session.subject.label: 
        print('subject ID test passed with x01') 
        if session.label[10:18] == str(session.timestamp)[:10].replace('-',''): 
            print('date test passed')
            if session.label[19:21] == '3T' or session.label[19:21] =='7T' or session.label[16:25] == 'PI2620PET' or session.label[16:22] == 'FBBPET' or session.label[16:25] == 'AV1451PET':  
                print('scantype test passed')
                if session.label[-3:] == 'ABC' or session.label[-5] =="ABCD2" or session.label[-4] == 'VCID':
                    print('study suffix correct')
                    print(f'Session name {session.label} is correct, skipping session.')
                    continue

    #############renaming block################
    print(f'Session label: {session.label} is incorrect, renaming...')

    if '_' in session.subject.label: 
        indd=session.subject.label.replace('_',"x")
        ##add update to session.subject.label? 
    else: 
        indd = session.subject.label
    
    date = str(session.timestamp)[:10].replace('-','')

    for acquisition in session.acquisitions():
        if acquisition.label == "PhoenixZIPReport" or acquisition.label == "Exam Summary_401_401":
            ##those acquisitions don't have the detailed metadata
            continue
        else:
            acquisition = acquisition.reload() 
            if acquisition.files[0].type == 'dicom':
                #only need the dicom file's metadata, dicom file is always first??check that
                f = acquisition.files[0].info #dictionary of metadata info per file
                instname = f['InstitutionName']
                petid = f['PerformedProcedureStepDescription']
                if '829602' in petid:
                    study = "LEADS"

                if 'Amyloid' in acquisition.label:
                    scantype = 'FBBPET'
                    if '844047' in petid:
                        study = 'ABCD2'
                    elif '825943' in petid:
                        study = 'ABC'
                elif 'PI2620' in acquisition.label:
                    scantype = 'PI2620PET'
                    # if '844047' in petid:
                    #     study = 'ABCD2'
                    # elif '829602' in petid:
                    #     study = "LEADS"
                    # elif '825943' in petid:
                    study = 'ABC' ##only abc uses pi?
                elif 'AV1451' in acquisition.label:
                    scantype = 'AV1451PET'
                    if '844403' in petid:
                        study = 'ABCD2'
                    elif '825944' in petid:
                        study = 'ABC'
                elif 'FDG' in acquisition.label:
                    scantype = 'FDGPET'
                    study='LEADS'
                    

        
        
        #this block only for MRIs
        # for f in acquisition.files:
        #     instname = f.info['InstitutionName']
        #     magstrength=[f.info['MagneticFieldStrength'] for f in acquisition.files if 'MagneticFieldStrength' in f.info]
        #     if 7 in magstrength:
        #         scantype="7T"
        #         study = 'ABC'
        #         break
        #     elif 3 in magstrength:
        #         scantype='3T'
        #         if instname == 'HUP':
        #             study='LEADS or DVCID'
        #             break
        #         elif instname == 'SC3T':
        #             if session.timestamp <= datetime.strptime('2021/01/01 12:00:00 +00:00', '%Y/%d/%m %H:%M:%S %z'):
        #                 study='ABC'
        #                 break
        #             else:
        #                 study='ABC or ABCD2'
        #                 break
        #     ###add additional f.info filters to id pet scan type/study        
        #     break        

    
    modality = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    if 'PT' in modality:
        petlabels = [acquisition.label for acquisition in session.acquisitions()]
        for petlabel in petlabels:
            if 'Amyloid' in petlabel:
                scantype = 'FBBPET'
                study='?'
                break
            elif 'PI2620' in petlabel:
                scantype = 'PI2620PET'
                study='?'
                break
            elif 'AV1451' in petlabel:
                scantype = 'AV1451PET'
                study='?'
                break
            elif 'FDG' in petlabel:
                scantype = 'FDGPET'
                study='LEADS'
                break


    newlabel = indd + 'x' + date + 'x' + scantype + 'x' + study
    print(f'Renaming session to: {newlabel}') 

#############################################################
    # session.update({'label': newlabel})
    # print(f'Session label is now {session.label}')
#############################################################

print(f'{count} sessions in project {project.label} checked')  