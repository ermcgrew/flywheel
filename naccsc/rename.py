import flywheel

#connect to flywheel
fw = flywheel.Client()

#########add try/excepts  

#select project by project ID
project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC

#create list of sessions
#use a filter here if changing PET to match MRI so only sessions not matching correct format are pulled
sessions = project.sessions.find() 
print(f'{len(sessions)} sessions in project NACC-SC')
# print([session.label for session in sessions])


counter = 0
for session in sessions:
    for acquisition in session.acquisitions():
        #if acquisition.files[0].modality contains MR (vs contains PT)

    #if MRI 
        #if session.label not SubjectIDxYYYYMMDDxScanType
        #########how to ID incorrect session labels? 
        if session.label != "??????x????????x??": 
            counter += 1
            # print(session.label)
            
            #subject.code or subject.label for SubjectID
            indd = session.subject.label
            #date = session.created (datetime conversion)
            #scantype = acquisition file name (parse)
            #save as session.label
            #session.label = indd + 'x' + 'date' + 'x' + 'scantype'
            #record of change--print + log when running script
    #if PET 
        #if session.label not SubjectIDxScanTypexYYYYMMDD
        # if session.label != "??????xPETx????????": 
            #repeat steps from MRI with order change--unless we switch so they match

print(f'{counter} incorrect session names')
        