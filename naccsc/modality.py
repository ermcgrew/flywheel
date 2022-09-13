import flywheel
fw = flywheel.Client()

try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

try:
    sessions = project.sessions.iter_find('created>2022-07-19') 
except flywheel.ApiException as e:
    print(f'Error: {e}')

for count, session in enumerate(sessions, 1):
    print(f'session loop {count}: {session.label}')
    test = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    if 'MR' in test:
        print('MRI')
        # for acquisition in session.acquisitions():
        #     acquisition = acquisition.reload()
        #     for f in acquisition.files:
        #         print(f.info)
        #         break
        #     break
    elif 'PT' in test:
        print("PET scan")
        for acquisition in session.acquisitions():
            print(acquisition)
            # acquisition = acquisition.reload()
            # for f in acquisition.files:
            #     print(f.info)
            #     break
            # break

        # if acquisition.files[0].modality == 'MR':
        #     print(acquisition.files[0].classification)
    #     if acquisition.files[0].modality == 'PT':
    #         # print(acquisition)
    #         # print(acquisition.label)