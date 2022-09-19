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
    sessions = project.sessions.iter_find('created>2022-08-19') #subset to test on 07-19
except flywheel.ApiException as e:
    print(f'Error: {e}')

#look at each session and rename as appropriate
for count, session in enumerate(sessions, 1):
    print(f'***********session loop {count}: {session.label}******************')
    ########ID incorrect session labels########    
    #once a session fails an if (fails to match correct format), go to rename block
    if session.label[0:6] == session.subject.label:
        print('subject ID test passed')
        ##add option for x01 subjects
        if session.label[7:15] == str(session.timestamp)[:10].replace('-',''): ##this catches all incorrectly ordered PET scans
            print('date test passed')
            if session.label[16:18] == '3T' or session.label[16:18] =='7T' or session.label[16:25] == 'PI2620PET' or session.label[16:22] == 'FBBPET':
                print('scantype test passed')
                if session.label[-3:] == 'ABC':
                    print('study suffix correct')
                    print(f'Session name {session.label} is correct, skipping session.')
                    continue

    


#############renaming block
#make this a function??
    print(f'Session label: {session.label} is incorrect, renaming...')
    ##fix for if subject.label is wrong e.g. with _
    indd = session.subject.label
    date = str(session.timestamp)[:10].replace('-','')

    for acquisition in session.acquisitions():
        acquisition = acquisition.reload()
        #have to get instituion name for study determination, use it for scan type too?
        magstrength=[f.info['MagneticFieldStrength'] for f in acquisition.files if 'MagneticFieldStrength' in f.info]
        if 3 in magstrength:
            scantype='3T'
            break
        elif 7 in magstrength:
            scantype="7T"
            study = 'ABC'
            break
        break

    
    modality = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    if 'PT' in modality:
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
    # session.update({'label': newlabel})
    # print(f'Session label is now {session.label}')
#############################################################

print(f'{count} sessions in project {project.label} checked')  