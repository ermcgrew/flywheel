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
#####use a filter here  so only sessions not matching correct format are pulled?
try:
    sessions = project.sessions.iter_find('created>2022-07-19') #subset to test on
except flywheel.ApiException as e:
    print(f'Error: {e}')

for count, session in enumerate(sessions, 1):
    print(f'***********session loop {count}: {session.label}******************')

        #########how to ID incorrect session labels?
        #SubjectIDxYYYYMMDDxScanType 
        # if session.label != "??????x????????x??": 


#############renaming block
    print(f'Session label: {session.label} is incorrect, renaming...')
    indd = session.subject.label
    date = str(session.created)[:10].replace('-','')
    
    modality = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    if 'MR' in modality:
        print('MRI')
        scantype = '3T'

        classes = [acquisition.files[0].classification for acquisition in session.acquisitions()]
        # print(classes)
        for x in classes:
            if 'Features' in x:
                print('Features found')
        if 'Features' in classes:
            print("Features key found")


        # if 'Features' in acquisition.files[0].classification and acquisition.files[0].classification['Features'] == ['MP2RAGE']:
        #     print('this is a 7T scan' )
        #     scantype = '7T'
        # else: ####need a condition to id 3T scans with
        #     print('this is a 3T scan')
        #     scantype = '3T'


    elif 'PT' in modality:
        petlabels = [acquisition.label for acquisition in session.acquisitions()]
        for petlabel in petlabels:
                if 'Amyloid' in petlabel:
                    scantype = 'FBBPET'
                    break
                elif 'PI2620' in petlabel:
                    scantype = 'PI2620PET'
                    break
                elif 'AV1451' in petlabel:
                    scantype = 'AV1451PET'
                    break
                elif 'FDG' in petlabel:
                    scantype = 'FDGPET'
                    break
        
    # ####study = ???
            #ABC, ABCD2, LEADS, DVCID


    newlabel = indd + 'x' + date + 'x' + scantype + 'x' #+ study
    print(f'Renaming session to: {newlabel}')
#############    

#############################################################
    # session.update(label = newlabel)
    # print(f'Session label is now {session.label}')
#############################################################

print(f'{count} sessions in project {project.label} checked')  