from datetime import datetime
from operator import mod
import flywheel

def mknote(indd,date,scantype):
    newlabel = indd + 'x' + date + 'x' + scantype + 'x'
    o.write(f'{newlabel}\n')
    return 

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
    sessions = project.sessions.iter_find('created>2022-07-14')  #label=125107x20210609x3T   label=125590x10202022x7T    
    #subset to test on mris:created>2022-10-01   pet: created>2022-07-14  125081xFDGx20220720 label=127794xAV1451PETx20220719
except flywheel.ApiException as e:
    print(f'Error: {e}')

#document to track sessions that can't be completely renamed:
time=datetime.now().strftime("%Y%m%d_%H%M")
o = open(f'sessions_no_study_{time}', 'a')

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
        # print('for loop working')
        if modality == 'CT' or modality == 'SR': #those acquisitions don't have detailed metadata
            continue
        else:
            # print('hit the else')
            # print(acquisition.files[1].type) ###how to handle when dicom is not the [0] file...
            if acquisition.files[0].type == 'dicom': #only need the dicom file's metadata
                # print("is dicom")
                labels=' '.join([acquisition.label for acquisition in session.acquisitions()]) #all acq.labels into 1 string to be partial-matched to
                # print(labels)
                acquisition = acquisition.reload() 
                f = acquisition.files[0].info #dictionary of metadata info per file
                if 'MagneticFieldStrength' in f:
                    magstrength=f['MagneticFieldStrength']

                try:
                    instname = f['InstitutionName']
                except KeyError as e:
                    print(f'No key {e} exists')
                
                try:
                    instaddress = f['InstitutionAddress']
                except KeyError as e:
                    print(f'No key {e} exists')
                
                petid = f['PerformedProcedureStepDescription']

                ##PET scans 
                if modality == 'PT':
                    if 'Amyloid' in labels: 
                        scantype = 'FBBPET'
                        if '844047' in petid:
                            study = 'ABCD2'
                            break
                        elif '825943' in petid:
                            study = 'ABC'
                            # print('study ABC assigned line 90')
                            break
                        elif '829602' in petid:
                            study = "LEADS"
                            break
                        else: ##if no matching petid
                            print('No matching performed procedure step description found')
                            mknote(indd,date,scantype)
                            break
                    elif '2620' in labels: #PI2620 sometimes listed with space--PI 2620
                        scantype = 'PI2620PET'
                        study = 'ABC'
                        # print('study ABC assigned line 98')
                        break
                    elif 'AV1451' in labels: 
                        scantype = 'AV1451PET'
                        if '844403' in petid:
                            study = 'ABCD2'
                            break
                        elif '825944' in petid or '833864' in petid:
                            study = 'ABC'
                            # print('study ABC assigned line 108')
                            break
                        elif '829602' in petid:
                            study = "LEADS"
                            break
                        else: ##if no matching petid
                            print('No matching performed procedure step description found')
                            mknote(indd,date,scantype)
                            break
                    elif 'FDG' in labels: 
                        scantype = 'FDGPET'
                        study='LEADS'
                        break
                ##MRIs        
                elif modality == "MR":
                    if magstrength == 7:
                        scantype="7T"
                        study = 'ABC'
                        break
                    elif magstrength == 3:
                        # print('magstrength is 3')
                        scantype='3T'
                        if instname == 'HUP' or 'Spruce' in instaddress:
                            if 'Axial' in labels:
                                # print('study is LEADS')
                                study='LEADS'
                                break
                            elif 'LLASL' in labels:
                                study='VCID'
                                # print('study is VCID')
                                break
                        elif instname == 'SC3T' or 'Curie' in instaddress:
                            # print('instname is sc3t')
                            if session.timestamp <= datetime.strptime('2022/02/01 12:00:00 +00:00', '%Y/%d/%m %H:%M:%S %z'):
                                study='ABC'
                                break
                            else:
                                print('ABC or ABCD2--determine manually')
                                mknote(indd,date,scantype)
                                break        
                    

    newlabel = indd + 'x' + date + 'x' + scantype + 'x' + study
    print(f'Renaming session to: {newlabel}') 

#############################################################
    # session.update({'label': newlabel})
    # session.reload()
    # print(f'Session label is now {session.label}')
#############################################################
o.close()
print(f'{count} sessions in project {project.label} checked')  