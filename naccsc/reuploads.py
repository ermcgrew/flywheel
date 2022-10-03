import flywheel
fw = flywheel.Client()

try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
except flywheel.ApiException as e:
    print(f'Error: {e}')

try:
    sessions = project.sessions.iter_find('created>2022-07-22') 
except flywheel.ApiException as e:
    print(f'Error: {e}')

o = open('pet_reuploads.txt', 'a')

for count, session in enumerate(sessions, 1):
    print(f'session loop {count}: {session.label}')
    test = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    if 'PT' in test:
        for acquisition in session.acquisitions():
            if acquisition.label == "PhoenixZIPReport" or acquisition.label == "Exam Summary_401_401":
                continue
            else:
                acquisition = acquisition.reload()
                if acquisition.files[0].type == 'dicom':
                    f = acquisition.files[0].info
                    try:
                        testval = f['PatientName']
                        print(f'{session.label} includes Patient Name field')
                        o.write(f'{session.label}\n')
                    except KeyError as error:
                        print(f'{session.label} has been de-identified')
                else:
                    continue
            break
o.close()