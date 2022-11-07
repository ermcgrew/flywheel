from csv import field_size_limit
import csv
from pprint import pprint
from datetime import datetime

import flywheel
fw = flywheel.Client()

try:
    # project = fw.get_project('6328e43d7be4e9e7d7d5fcfc') #wecandream
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

try:
    # sessions = project.sessions.iter_find() #wecandream
    sessions = project.sessions.iter_find('created>2022-10-02')  #07-27') 
    # sessions = project.sessions.iter_find('label=128314x20220728x3TxABCD2')
    # sessions = project.sessions.iter_find('label=117870x20220920x3TxABC')
    # sessions = project.sessions.iter_find('label=119202x20220921x3TxVCID')
    # sessions = project.sessions.iter_find('label=123367x20220906xFBBPETxABC') 
    # sessions = project.sessions.iter_find('label=128394x20220907xFBBPETxABCD2')
    # sessions = project.sessions.iter_find('label=128332x20220831xFBBPETxABCD2')
    # sessions = project.sessions.iter_find('label=125111x20220829xPI2620PETxABC')
    # 128387x20220830xAV1451PETxABCD2
    # sessions = project.sessions.iter_find('label=125107x20210609x3T') #LEADS 3t
    # sessions = project.sessions.iter_find('label=124666xAV1451PETx20210915') #LEADS tau
    # sessions = project.sessions.iter_find('label=126886xFlorbetabenx20211110') #LEADS FBB/amy
    # sessions = project.sessions.iter_find('label=124938xAV1451PETx20211208') #ABC tau AV
    # sessions = project.sessions.iter_find('label=122963xPI2620PETx20220221') #ABC tau PI

except flywheel.ApiException as e:
    print(f'Error: {e}')
headerrow=['Session label', 'uploaded by']

for count, session in enumerate(sessions, 1):
        # if session.label[16:25] !="AV1451PET":
        #     continue
        # else:
    print(f'session loop {count}: {session.label}')
    # print(session)
     ########ID incorrect session labels########    
        #once a session fails an if (fails to match correct format), go to rename block
        # if session.label[0:6] == session.subject.label:
        #     print('subject ID test passed')
        #     if session.label[7:15] == str(session.timestamp)[:10].replace('-',''): 
        #         print('date test passed')
        #         if session.label[16:18] == '3T' or session.label[16:18] =='7T' or session.label[16:25] == 'PI2620PET' or session.label[16:22] == 'FBBPET' or session.label[16:25] == 'AV1451PET':
        #             print('scantype test passed')
        #             if session.label[-3:] == 'ABC' or session.label[-5:] =="ABCD2" or session.label[-4:] == 'VCID':
        #                 print('study suffix correct')
        #                 print(f'Session name {session.label} is correct, skipping session.')
        #                 continue
        # #if subject has _01 or x02:
        # elif session.label[0:9] == session.subject.label: 
        #     print('subject ID test passed with x01') 
        #     if session.label[10:18] == str(session.timestamp)[:10].replace('-',''): 
        #         print('date test passed')
        #         if session.label[19:21] == '3T' or session.label[19:21] =='7T' or session.label[16:25] == 'PI2620PET' or session.label[16:22] == 'FBBPET' or session.label[16:25] == 'AV1451PET':  
        #             print('scantype test passed')
        #             if session.label[-3:] == 'ABC' or session.label[-5] =="ABCD2" or session.label[-4] == 'VCID':
        #                 print('study suffix correct')
        #                 print(f'Session name {session.label} is correct, skipping session.')
        #                 continue

        
    # name=session.label
    # namelist=name.split('x')
    # if len(namelist) == 4:
    #     print(f'Session {session.label} is correct')
    #     continue
    # elif namelist[2] == '3T' or namelist[2] == '7T':
    #     print('skip to study id')
    #     ##still verify indd & date are correct??
    # else: 
    #     print('do whole rename')

    # if session.label[-3:] == 'ABC':
    #     study="ABC"
    # if session.label[-5:] =="ABCD2":
    #     study='ABCD2'
    # date = str(session.timestamp)[:10].replace('-','')
    # if date > '2022-07-01':
    #     print(f'{date} is after july 1')
    for acquisition in session.acquisitions():
        print(acquisition.files[0].modality)
        print(acquisition.label)

    test = [acquisition.files[0].modality for acquisition in session.acquisitions()]
    # print(test)
    if 'MR' in test:
        continue    
    # print('MRI')
        # filename=f'{session.label}.csv'
        # headerrow= ['acquisition.label','f.info["ProtocolName"]', 'Intent', 'Measurement', 'Features']
        # with open(filename, 'w', newline='') as csvfile:
        #     csvwriter=csv.writer(csvfile)
        #     csvwriter.writerow(headerrow)
        #     for acquisition in session.acquisitions():
        #         acquisition = acquisition.reload()
        #         for f in acquisition.files:
        #             if f.type == 'dicom' :
        #                 filerow=[]
        #                 filerow.append(acquisition.label)
        #                 try:
        #                     filerow.append(f.info['ProtocolName'])
        #                 except KeyError as error:
        #                     filerow.append('n/a')

        #                 try:
        #                     filerow.append(acquisition.files[0].classification['Intent'])
        #                 except KeyError as error:
        #                     filerow.append('n/a')

        #                 try:
        #                     filerow.append(acquisition.files[0].classification['Measurement'])
        #                 except KeyError as error:
        #                     filerow.append('n/a')

        #                 try:
        #                     filerow.append(acquisition.files[0].classification['Features'])
        #                 except KeyError as error:
        #                     filerow.append('n/a')

        #                 csvwriter.writerow(filerow)
        #             else:
        #                 continue


        # o = open(f'TestLEADS', 'a')
        # for acquisition in session.acquisitions():   
        #     if acquisition.label == "PhoenixZIPReport" or acquisition.label == "Exam Summary_401_401":
        #         continue
        #     else:
        #         acquisition = acquisition.reload() 
        #         if acquisition.files[0].type == 'dicom':
        #             # print(acquisition.files[0].info['InstitutionName'])
        #             # print(acquisition.files[0].info['MagneticFieldStrength'])
        #             f = acquisition.files[0].info
        #             instname = f['InstitutionName']
        #             print(instname)
                
        # # #     print('**********************************')
        # #     # print(f'Acquisition Label: {acquisition.label}')
        # # #     print(f'Classifiction: {acquisition.files[0].classification}')
        # #     o.write('*********New Acquisition******************** \n')
        # #     o.write(f'Acquisition Label: {acquisition.label}\n')
        # #     o.write(f"Classification: {acquisition.files[0].classification} \n")
        #     for f in acquisition.files:
        #         print(f.type)        
        # # print(f.classifier)
        #         try:    
        # #             # print('************************************')
        #             # print(f"\tProtocol name: {f.info['ProtocolName']}")
        #             o.write(f"{f.info['ProtocolName']} \n")
        #         except KeyError as error:
        #             print(f'No protocol name for this file')

        # o.close

#3T file diffs by: 
# cat file.txt | sort -u > save.txt
#diff -y save1.txt save2.txt

                
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
        print("PET scan")
        for acquisition in session.acquisitions():
            acquisition = acquisition.reload()
            
            # pprint(acquisition)
            # for f in acquisition.files:
            #     if f.info['PatientName']:
            #         print('patient name field exists')
            break


        # petlabels = [acquisition.label for acquisition in session.acquisitions()]
        # for petlabel in petlabels:
        #     if 'Amyloid' in petlabel:
        #         scantype = 'FBBPET'
        #         break
        #     elif 'PI2620' in petlabel:
        #         scantype = 'PI2620PET'
        #         break
        #     elif 'AV1451' in petlabel:
        #         scantype = 'AV1451PET'
        #         break
        #     elif 'FDG' in petlabel:
        #         scantype = 'FDGPET'
        #         study='LEADS'
        #         break
        # for acquisition in session.acquisitions():
        #     acquisition = acquisition.reload()
            # print('**********************************')
            # print(f'Acquisition Label: {acquisition.label}')
            # o.write('**********************************\n')
            # o.write(f'Acquisition Label: {acquisition.label}\n')
            # for f in acquisition.files:
            #     try:
            #         # number = f.info['PerformedProcedureStepDescription']
            #         # print(number[:7])
            #         # if '844047' in f.info['PerformedProcedureStepDescription']:
            #         #     print('FBBPETxABCD2')
            #         print(f.info['PerformedProcedureStepDescription'])
            #     except KeyError as error:
            #         print(f"not found for this file")
            #     try:
            #         print(f.info['ProtocolName'])
            #     except KeyError as error:
            #         print('not found')
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