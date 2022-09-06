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
    print(f'session loop {count}: {session.label}')

        #########how to ID incorrect session labels?
        #SubjectIDxYYYYMMDDxScanType 
        # if session.label != "??????x????????x??": 


#############renaming block
    # print(f'Session label: {session.label} is incorrect, renaming...')
    # indd = session.subject.label
    # print(f'Subject indd: {indd}')
    # date = str(session.created)[:10].replace('-','')
    # print(f'Session date: {date}')
    
    # #scantype = acquisition file name (parse)

    # ####study = ???

    # newlabel = indd + 'x' + date + 'x'
    # print(f'Renaming session to: {newlabel}')
#############    

#############################################################
    # session.update(label = newlabel)
    # print(f'Session label is now {session.label}')
#############################################################

print(f'{count} sessions in project {project.label} checked')  