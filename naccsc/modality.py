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

mri_values = {}
pet_values = {}


for count, session in enumerate(sessions, 1):
    print(f'session loop {count}: {session.label}')
    test = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    if 'MR' in test:
        print('MRI')
        for acquisition in session.acquisitions():
            acquisition = acquisition.reload()
            for f in acquisition.files:
                print(f.info)
                break
            break
    # elif 'PT' in test:
    #     print("PET scan")
    #     for acquisition in session.acquisitions():
    #         acquisition = acquisition.reload()
    #         for f in acquisition.files:
    #             print(f.info)
    #             break
    #         break


       
    

        # if acquisition.files[0].modality == 'MR':
        #     print(acquisition.files[0].classification)
    #         # mri_values[acquisition.id] = acquisition.files[0].classification


    #         if 'Features' in acquisition.files[0].classification and acquisition.files[0].classification['Features'] == ['MP2RAGE']:
    #             print('this is a 7T scan' )
    #         else: ####need a condition to id 3T scans with
    #             print('this is a 3T scan')
    #     if acquisition.files[0].modality == 'PT':
    #         # print(acquisition)
    #         # pet_values[acquisition.id] = acquisition.files[0].name
    #         # print(acquisition.label)

    #         #works to distinguish type of PET
    #         ####will need to add conditions for other naming for older sessions? 
    #         if 'Amyloid' in acquisition.label:
    #             print('amyloid session')
    #         elif 'AV1451' in acquisition.label:
    #             print('tau session')
    #         elif 'FDG' in acquisition.label:
    #             print('FDG session')

            

        

        #for each session,
        #look through each acquisition #if acquisition.files[0].modality contains MR (vs contains PT)
        #first time MR found
            #go to MRI loop
        #first time PT found
            #go to PET loop
        
        #still doesn't distinguish 3t/7t or pet types
        #use {'classification': {'Intent': ['Localizer'], 'Measurement': ['T2']} to determine?

# print(mri_values['62d845fcaa0594f053f6a385'])
# print(pet_values['62dae2af038cbe7def7d3abf'])