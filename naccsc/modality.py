from pprint import pprint
from datetime import datetime

import flywheel
fw = flywheel.Client()

try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

try:
    sessions = project.sessions.iter_find('created>2022-09-01')  #07-27') 
    # sessions = project.sessions.iter_find('label=128314x20220728x3TxABCD2')
    # sessions = project.sessions.iter_find('label=117870x20220920x3TxABC')
    # sessions = project.sessions.iter_find('label=119202x20220921x3TxVCID')
    # sessions = project.sessions.iter_find('label=123367x20220906xFBBPETxABC') 
    # sessions = project.sessions.iter_find('label=128394x20220907xFBBPETxABCD2')
    # sessions = project.sessions.iter_find('label=128332x20220831xFBBPETxABCD2')
    # sessions = project.sessions.iter_find('label=125111x20220829xPI2620PETxABC')
    # 128387x20220830xAV1451PETxABCD2





except flywheel.ApiException as e:
    print(f'Error: {e}')

# idlist =[]

for count, session in enumerate(sessions, 1):
    if session.label[16:25] !="AV1451PET":
        continue
    else:
        print(f'session loop {count}: {session.label}')

    # if session.label[-3:] == 'ABC':
    #     study="ABC"
    # if session.label[-5:] =="ABCD2":
    #     study='ABCD2'
    # date = str(session.timestamp)[:10].replace('-','')
    # if date > '2022-07-01':
    #     print(f'{date} is after july 1')
    
    test = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    if 'MR' in test:
        print('MRI')
        # o = open(f'TestABCmatchtemplate', 'a')
        # for acquisition in session.acquisitions():
        #     acquisition = acquisition.reload()
        #     print('**********************************')
        #     print(f'Acquisition Label: {acquisition.label}')
        #     print(f'Classifiction: {acquisition.files[0].classification}')
        # #     o.write('*********New Acquisition******************** \n')
        # #     o.write(f"Classification: {acquisition.files[0].classification} \n")
        #     for f in acquisition.files:
        # #     #     print(f.classifier)
        #         try:    
        # #             # print('************************************')
        #             print(f"\tProtocol name: {f.info['ProtocolName']}")
        # #             o.write(f"{f.info['ProtocolName']} \n")
        #         except KeyError as error:
        #             print(f'No protocol name for this file')

        # # o.close


                
                # instname = f.info['InstitutionName']
                # magstrength=[f.info['MagneticFieldStrength'] for f in acquisition.files if 'MagneticFieldStrength' in f.info]
                # magstrength = f.info['MagneticFieldStrength']
                # print(magstrength)
                # # if 3 in magstrength:
                # if magstrength == 3:
                #     scantype='3T'
                #     if instname == 'HUP':
                #         study='LEADS or DVCID'
                #     elif instname == 'SC3T':
                #         if session.timestamp <= datetime.strptime('2021/01/01 12:00:00 +00:00', '%Y/%d/%m %H:%M:%S %z'):
                #             study='ABC'
                #         else:
                #             study = 'ABC or ABCD2'
                #     break
                # # elif 7 in magstrength:
                # elif magstrength == 7:
                #     scantype="7T"
                #     study = 'ABC'
                
                # pprint(f.info)
            
                # print(f.info['InstitutionName'])
                # idlist.append(f.info['InstitutionName'])
                # idlist.append(f.info['PerformedProcedureStepID'])
            #     break
            # break
    elif 'PT' in test:
        # print("PET scan")
        # o = open(f'{session.label}', 'a')
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
                study='LEADS'
                break
        for acquisition in session.acquisitions():
            acquisition = acquisition.reload()
            # print('**********************************')
            # print(f'Acquisition Label: {acquisition.label}')
            # o.write('**********************************\n')
            # o.write(f'Acquisition Label: {acquisition.label}\n')
            for f in acquisition.files:
                try:
                    # number = f.info['PerformedProcedureStepDescription']
                    # print(number[:7])
                    # if '844047' in f.info['PerformedProcedureStepDescription']:
                    #     print('FBBPETxABCD2')
                    print(f.info['PerformedProcedureStepDescription'])
                except KeyError as error:
                    print(f"not found for this file")
                try:
                    print(f.info['ProtocolName'])
                except KeyError as error:
                    print('not found')
                # print(f"\tProtocol name: {f.info['ProtocolName']}")
                # o.write('****New file for Acquisition******\n') 
                # keylist=["InstitutionName", "ManufacturerModelName", "PerformedProcedureStepDescription", "PerformedProcedureStepID", "ProtocolName", "SeriesDescription", "SeriesType", "StationName"]
                # for i in keylist:
                #     # print(f'with and f string: {f.info[i]}')
                #     try:
                #         o.write(f'{i}: {f.info[i]}\n')
                #     except KeyError as error:
                #         o.write(f"{i} not found for this file\n")
                # try:
                #     o.write(f'DeviceSerialNumber: {f.info["DeviceSerialNumber"]}\n')
                # except KeyError as error:
                #     o.write("key not found for this file\n")

                # try:
                #     o.write(f'InstitutionName: {f.info["InstitutionName"]}\n')
                #     o.write(f'ManufacturerModelName: {f.info["ManufacturerModelName"]}\n')
                #     o.write(f'PerformedProcedureStepDescription: {f.info["PerformedProcedureStepDescription"]}\n')
                #     o.write(f'PerformedProcedureStepID: {f.info["PerformedProcedureStepID"]}\n')
                #     o.write(f'ProtocolName: {f.info["ProtocolName"]}\n')
                #     o.write(f'SeriesDescription: {f.info["SeriesDescription"]}\n')
                #     o.write(f'SeriesType: {f.info["SeriesType"]}\n')
                #     o.write(f'StationName: {f.info["StationName"]}\n')

                
                # o.write(f.info)


                # pprint(f.info, o)
                # print('**************************')
                # pprint(f.info)
                #     break
                # break
        # o.close()
        # if acquisition.files[0].modality == 'MR':
        #     print(acquisition.files[0].classification)
    #     if acquisition.files[0].modality == 'PT':
    #         # print(acquisition)
    #         # print(acquisition.label)


# idset = set(idlist)
# print(len(idset))
# print(idset)

    # print(study)