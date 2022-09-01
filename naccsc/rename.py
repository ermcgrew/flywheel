import flywheel
fw = flywheel.Client()

#select project by project ID
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

#create list of sessions
#####use a filter here if changing PET to match MRI so only sessions not matching correct format are pulled
#subset to test on, incl MRI & PET, remove created filter for actual use
try:
    sessions = project.sessions.find('created>2022-07-19') 
except flywheel.ApiException as e:
    print(f'Error: {e}')

print(f'{len(sessions)} sessions in project {project.label}')

for count, session in enumerate(sessions, 1):
    print(f'loop {count}: {session.label}')
    # for acquisition in session.acquisitions():
    #     print('in acq loop')
        #if acquisition.files[0].modality contains MR (vs contains PT)
    #if MRI 
        #if session.label not SubjectIDxYYYYMMDDxScanType
        #########how to ID incorrect session labels? 
        # if session.label != "??????x????????x??": 
            # print(session.label)
            
            #subject.code or subject.label for SubjectID
            # indd = session.subject.label
            #date = session.created (datetime conversion)
            #scantype = acquisition file name (parse)
            #save as session.label
            #session.label = indd + 'x' + 'date' + 'x' + 'scantype'
            #record of change--print + log when running script
    #if PET 
        #if session.label not SubjectIDxScanTypexYYYYMMDD
        # if session.label != "??????xPETx????????": 
            #repeat steps from MRI with order change--unless we switch so they match

print(f'{count} incorrect session names')
        