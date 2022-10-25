from datetime import datetime
from operator import mod
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
    sessions = project.sessions.iter_find('created>2022-07-14') #subset to test on    125081xFDGx20220720 label=127794xAV1451PETx20220719
except flywheel.ApiException as e:
    print(f'Error: {e}')

#look at each session and rename as appropriate
for count, session in enumerate(sessions, 1):
    print(f'***********session loop {count}: {session.label}******************')
    
    #reset variables to empty strings
    indd=''
    date=''
    scantype=''
    study=''

    ########ID incorrect session labels########    
    #once a session fails an if (fails to match correct format), go to rename block
    if session.label[0:6] == session.subject.label:
        print('subject ID test passed')
        if session.label[7:15] == str(session.timestamp)[:10].replace('-',''): 
            print('date test passed')
            if session.label[16:18] == '3T' or session.label[16:18] =='7T' or session.label[16:25] == 'PI2620PET' or session.label[16:22] == 'FBBPET' or session.label[16:25] == 'AV1451PET':
                print('scantype test passed')
                if session.label[-3:] == 'ABC' or session.label[-5:] =="ABCD2" or session.label[-4:] == 'VCID':
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
        ######add update to session.subject.label? 
    else: 
        indd = session.subject.label
    
    date = str(session.timestamp)[:10].replace('-','')

    for acquisition in session.acquisitions():
        modality = acquisition.files[0].modality
        if modality == 'CT' or modality == 'SR': 
            #those acquisitions don't have detailed metadata
            continue
        else:
            if acquisition.files[0].type == 'dicom':
                #only need the dicom file's metadata, 
                ######dicom file is always first??check
                
                labellist=[acquisition.label for acquisition in session.acquisitions()]
                # print(labellist)
                
                magstrength=[f.info['MagneticFieldStrength'] for f in acquisition.files if 'MagneticFieldStrength' in f.info]
                #does this need to be a list comp? goes here before reload??



                acquisition = acquisition.reload() 
                f = acquisition.files[0].info #dictionary of metadata info per file
                instname = f['InstitutionName'] ##add inst.address as another field to match if instname doesn't exist
                petid = f['PerformedProcedureStepDescription'] #fine here, try as listcomp??
                #print(petid)
                

                ##PET scans 
                if modality == 'PT':
                    print(acquisition.label)

                    if 'Amyloid' in acquisition.label:
                        scantype = 'FBBPET'
                        if '844047' in petid:
                            study = 'ABCD2'
                            break
                        elif '825943' in petid:
                            study = 'ABC'
                            print('study ABC assigned line 90')
                            break
                        elif '829602' in petid:
                            study = "LEADS"
                            break
                    elif '2620' in acquisition.label: #PI2620 sometimes listed with space--PI 2620
                        scantype = 'PI2620PET'
                        study = 'ABC'
                        print('study ABC assigned line 98')

                        break
                    elif 'AV1451' in acquisition.label:
                        scantype = 'AV1451PET'
                        if '844403' in petid:
                            study = 'ABCD2'
                            break
                        elif '825944' in petid or '833864' in petid:
                            study = 'ABC'
                            print('study ABC assigned line 108')

                            break
                        elif '829602' in petid:
                            study = "LEADS"
                            break
                    elif 'FDG' in acquisition.label:
                        scantype = 'FDGPET'
                        study='LEADS'
                        break
                ##MRIs        
                elif modality == "MR":
                    if 7 in magstrength:
                        scantype="7T"
                        study = 'ABC'
                        print('study ABC assigned line 123')

                        break
                    elif 3 in magstrength:
                        print('magstrength is 3')
                        scantype='3T'
                        if instname == 'HUP':
                            if 'Axial 3TE T2 Star' in labellist:  # MB DTI
                                ##### if axial in any x of labellist
                                print('study is LEADS')
                                study='LEADS'
                                break
                            elif 'LLASL_m16LC_3.0s_2.0s_bs31_mis' in labellist:
                                study='VCID'
                                print('study is VCID')
                                break
                        elif instname == 'SC3T':
                            print('instname is sc3t')
                            if session.timestamp <= datetime.strptime('2022/02/01 12:00:00 +00:00', '%Y/%d/%m %H:%M:%S %z'):
                                study='ABC'
                                print('study is ABC assigned line 143')

                                break
                            else:
                                ######add this session to list for review
                                study=''
                                print('ABC or ABCD2--determine manually')
                                break        
                    

    newlabel = indd + 'x' + date + 'x' + scantype + 'x' + study
    print(f'Renaming session to: {newlabel}') 

#############################################################
    # session.update({'label': newlabel})
    # session.reload()
    # print(f'Session label is now {session.label}')
#############################################################

print(f'{count} sessions in project {project.label} checked')  