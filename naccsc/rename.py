#Reviews all sessions in NACC-SC flywheel project and renames them in correct syntax: INDDxDATExSCANTYPExSTUDY
#Run from terminal: python rename.py >> rename_log_DATE.txt

from datetime import datetime
import flywheel

#notes sessions where study cannot be ID'ed
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
    sessions = project.sessions.iter_find('label=124738x20220906x3T')      
except flywheel.ApiException as e:
    print(f'Error: {e}')

#document to track sessions that can't be completely renamed:
time=datetime.now().strftime("%Y%m%d_%H%M")
o = open(f'sessions_no_study_{time}.txt', 'a')

#look at each session and rename as appropriate
for count, session in enumerate(sessions, 1):
    print(f'***********session loop {count}: {session.label}******************')
    
    #reset variables to empty strings
    indd=''
    date=''
    scantype=''
    study=''

    if 'Duplicate' in session.tags or 'Misc.' in session.tags: #skip duplicate and Misc. sessions
        print(f'{session.label} has tags {session.tags}, not renaming')
        continue
    else:
        print(f'Session label: {session.label} is incorrect, renaming...')

        if '_' in session.subject.label: 
            indd=session.subject.label.replace('_',"x")
            print(f'Updating subject label to {indd}')
            session.subject.update(label=indd) ##updates subject label to correct version
        else: 
            indd = session.subject.label
        
        date = str(session.timestamp)[:10].replace('-','')

        for count2, acquisition in enumerate(session.acquisitions(), 1): 
            if scantype == '': #keeps from looping through every acq 
                modality = acquisition.files[0].modality
                if modality == 'CT' or modality == 'SR': #those acquisitions don't have detailed metadata
                    continue
                else:
                    for x in range(len(acquisition.files)): 
                        if acquisition.files[x].type == 'dicom': #only need the dicom file's metadata
                            labels=' '.join([acquisition.label for acquisition in session.acquisitions()]) #all acq.labels into 1 string to be partial-matched to
                            acquisition = acquisition.reload() 
                            f = acquisition.files[x].info #dictionary of metadata info per file
                                                    
                            if 'MagneticFieldStrength' in f:
                                magstrength=f['MagneticFieldStrength']

                            try:
                                instname = f['InstitutionName']
                            except KeyError as e:
                                print(f'No key {e} exists')
                                instname =''
                            
                            try:
                                instaddress = f['InstitutionAddress']
                            except KeyError as e:
                                print(f'No key {e} exists')
                                instaddress = ''
                            
                            try:
                                petid = f['PerformedProcedureStepDescription']
                            except KeyError as e:
                                print(f'No key {e} exists')
                                petid=''

                            try:
                                protocolName = f['ProtocolName']
                            except KeyError as e:
                                print(f'No key {e} exists')
                                protocolName=''
 
                            if modality == 'PT':
                                if 'Amyloid' in labels or 'AV45' in labels: 
                                    scantype = 'FBBPET'
                                    if '844047' in petid or '844047' in protocolName:
                                        study = 'ABCD2'
                                        break
                                    elif '825943' in petid or '825943' in protocolName:
                                        study = 'ABC'
                                        break
                                    elif '829602' in petid or '829602' in protocolName:
                                        study = "LEADS"
                                        break
                                    else: 
                                        print('No matching performed procedure step description found, making note...')
                                        mknote(indd,date,scantype)
                                        break                                                    
                                elif '2620' in labels: #PI2620 sometimes listed with space--PI 2620
                                    scantype = 'PI2620PET'
                                    study = 'ABC'
                                    break
                                elif 'AV1451' in labels: 
                                    scantype = 'AV1451PET'
                                    if '844403' in petid or '844403' in protocolName:
                                        study = 'ABCD2'
                                        break
                                    elif '825944' in petid or '833864' in petid or '825944' in protocolName or '833864' in protocolName:
                                        study = 'ABC'
                                        break
                                    elif '829602' in petid or '829602' in protocolName:
                                        study = "LEADS"
                                        break
                                    else: 
                                        print('No matching performed procedure step description found, making note...')
                                        mknote(indd,date,scantype)
                                        break
                                elif 'FDG' in labels: 
                                    scantype = 'FDGPET'
                                    study='LEADS'
                                    break       
                            elif modality == "MR":
                                if magstrength == 7 or magstrength == 6.98094: #some 2020 7T scans have this number instead of 7
                                    scantype="7T"
                                    study = 'ABC'
                                    break
                                elif magstrength == 3:
                                    scantype='3T'
                                    if instname == 'HUP' or 'Spruce' in instaddress:
                                        if 'Axial' in labels:
                                            study='LEADS'
                                            break
                                        elif 'LLASL' in labels:
                                            study='VCID'
                                            break
                                        else:
                                            print('HUP 3T scan labels insufficient to id study, making note...')
                                            mknote(indd,date,scantype)
                                            break
                                    elif instname == 'SC3T' or 'Curie' in instaddress:
                                        if session.timestamp <= datetime.strptime('2022/02/01 12:00:00 +00:00', '%Y/%d/%m %H:%M:%S %z'):
                                            study='ABC'
                                            break
                                        else:
                                            print('ABC or ABCD2--determine manually')
                                            mknote(indd,date,scantype)
                                            break
                                    else:
                                        print('3T scan does not have inst. name or address to ID study, making note...')
                                        mknote(indd,date,scantype)
                                        break
                        else:
                            continue #not a dicom file, skip it        

        newlabel = indd + 'x' + date + 'x' + scantype + 'x' + study
        print(f'Renaming session to: {newlabel}') 
        session.update({'label': newlabel})

o.close()
print(f'{count} sessions in project {project.label} checked')  