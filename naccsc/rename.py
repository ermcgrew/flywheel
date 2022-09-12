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
        #########ID incorrect session labels
        #SubjectIDxYYYYMMDDxScanType 
        
        #once a session fails an if (fails to match correct format), go to rename block

        #if first 6 chars == subject.label 
            #if it's a x01 
                #if chars 7-14 == date #this will catch all the PET scans in the old order
                    #if last 2 chars == 3T or 7T
                        #if last chars are study suffix, 
                            #this session is correctly named
                            #continue
        #else go to rename 

    # print(session.label[0:6]) #subject ID
    print(session.label[6]) #x
    print(session.label[7:15]) #date
    print(session.label[16:18]) #3T/7T
    if session.label[0:6] == session.subject.label:
        print('subject ID test passed')
        ##add option for x01 subjects
        if session.label[7:15] == str(session.created)[:10].replace('-',''):
            print('date test passed')
            if session.label[16:18] == '3T' or session.label[16:18] =='7T':  ##need something else here to catch new correct PET scans
                print('scantype test passed')

    


#############renaming block
#make this a function??
    print(f'Session label: {session.label} is incorrect, renaming...')
    indd = session.subject.label
    date = str(session.created)[:10].replace('-','')
    
    for acquisition in session.acquisitions():
        acquisition = acquisition.reload()
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
    # session.update(label = newlabel)
    # print(f'Session label is now {session.label}')
#############################################################

print(f'{count} sessions in project {project.label} checked')  