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
#####use a filter here if changing PET to match MRI so only sessions not matching correct format are pulled
try:
    sessions = project.sessions.iter_find('created>2022-07-19') #subset to test on, incl MRI & PET, remove created filter for actual use
except flywheel.ApiException as e:
    print(f'Error: {e}')

for count, session in enumerate(sessions, 1):
    print(f'session loop {count}: {session.label}')
    # for acquisition in session.acquisitions():
    #     print('in acq loop')
    #     print(f'{acquisition.files[0].modality}')
    #     if acquisition.files[0].modality == 'MR':
    #         print('MR found')
        
        #if acquisition.files[0].modality contains MR (vs contains PT)



    #if MRI 
        #if session.label not SubjectIDxYYYYMMDDxScanType
        #########how to ID incorrect session labels? 
        # if session.label != "??????x????????x??": 


#############renaming block
    # print(f'Session label: {session.label} is incorrect, renaming...')
    # indd = session.subject.label
    # print(f'Subject indd: {indd}')
    # date = str(session.created)[:10].replace('-','')
    # print(f'Session date: {date}')
    
    # #scantype = acquisition file name (parse)

    # newlabel = indd + 'x' + date + 'x'
    # print(f'Renaming session to: {newlabel}')

#############################################################
    # session.update(label = newlabel) #in dictionary? test with unsorted first
    # print(f'Session label is now {session.label}')
#############################################################


    #if PET 
        #if session.label not SubjectIDxScanTypexYYYYMMDD
        # if session.label != "??????xPETx????????": 
            #repeat steps from MRI with order change--unless we switch so they match

print(f'{count} sessions in project {project.label} checked')
        