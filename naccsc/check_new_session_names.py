#!/usr/bin/python3

import fwgearutils
import flywheel
import sys
import os


def check_correct(sessionlabellist, subject, date):
    check = [False, False, False, False]
    # for x in range(0,len(sessionlabellist)):

    if len(sessionlabellist) == 4:
        if sessionlabellist[0] == subject:
            check[0] = True

        if sessionlabellist[1] == date:
            check[1] = True

        if sessionlabellist[2] in scantypelist:
            check[2] = True

        if sessionlabellist[3] in studylist:
            check[3] = True

    return check


def rename_session(session, subject, date):
    # print('in renaming function')
    # print(session.label)
    scantype=''
    study=''
    for acquisition in session.acquisitions(): 
        if scantype == '': #keeps from looping through every acq 
            modality = acquisition.files[0].modality
            if modality == 'CT' or modality == 'SR': #those acquisitions don't have detailed metadata
                continue
            else:
                for x in range(len(acquisition.files)): 
                    if acquisition.files[x].type == 'dicom': #only need the dicom file's metadata
                        labels=' '.join([acquisition.label for acquisition in session.acquisitions()]) #all acq.labels into 1 string to be partial-matched to
                        acquisition = acquisition.reload() 
                        f = acquisition.files[x].info #dictionary of metadata info per file
                                                
                        if 'MagneticFieldStrength' in f:
                            magstrength=f['MagneticFieldStrength']

                        try:
                            instname = f['InstitutionName']
                        except KeyError as e:
                            instname =''
                        
                        try:
                            instaddress = f['InstitutionAddress']
                        except KeyError as e:
                            instaddress = ''
                        
                        try:
                            petid = f['PerformedProcedureStepDescription']
                        except KeyError as e:
                            petid=''

                        try:
                            protocolName = f['ProtocolName']
                        except KeyError as e:
                            protocolName=''

                        if modality == 'PT':
                            if 'Amyloid' in labels or 'AV45' in labels: 
                                scantype = 'FBBPET'
                                if '844047' in petid or '844047' in protocolName:
                                    study = 'ABCD2'
                                    break
                                elif '825943' in petid or '825943' in protocolName:
                                    study = 'ABC'
                                    break
                                elif '829602' in petid or '829602' in protocolName:
                                    study = "LEADS"
                                    break
                                else: 
                                    print('No matching performed procedure step description found, making note...')
                                    # mknote(indd,date,scantype)
                                    break                                                    
                            elif '2620' in labels: #PI2620 sometimes listed with space--PI 2620
                                scantype = 'PI2620PET'
                                study = 'ABC'
                                break
                            elif 'AV1451' in labels: 
                                scantype = 'AV1451PET'
                                if '844403' in petid or '844403' in protocolName:
                                    study = 'ABCD2'
                                    break
                                elif '825944' in petid or '833864' in petid or '825944' in protocolName or '833864' in protocolName:
                                    study = 'ABC'
                                    break
                                elif '829602' in petid or '829602' in protocolName:
                                    study = "LEADS"
                                    break
                                else: 
                                    print('No matching performed procedure step description found, making note...')
                                    # mknote(indd,date,scantype)
                                    break
                            elif 'FDG' in labels: 
                                scantype = 'FDGPET'
                                study='LEADS'
                                break
                            else: 
                                print(f'{session.label} PET scan needs scantype')        
                        
                        elif modality == "MR":
                            if round(magstrength) == 7:
                                scantype="7T"
                                if session.label[-4:] == "YMTL":
                                    study = 'YMTL'
                                    break
                                else:
                                    study = 'ABC'
                                    break
                            elif magstrength == 3:
                                scantype='3T'
                                if instname == 'HUP' or 'Spruce' in instaddress:
                                    if 'Axial' in labels:
                                        study='LEADS'
                                        break
                                    elif 'LLASL' in labels:
                                        study='VCID'
                                        break
                                    else:
                                        print('HUP 3T scan labels insufficient to id study, making note...')
                                        # mknote(indd,date,scantype)
                                        break
                                elif instname == 'SC3T' or 'Curie' in instaddress:
                                    if session.label[-4:] == "YMTL":
                                        study = 'YMTL'
                                        break
                                    elif session.label[-5:] == "ABCD2":
                                        study = 'ABCD2'
                                        break
                                    elif session.label[-3:] == "ABC":
                                        study = 'ABC'
                                        break
                                    else:
                                        print('ABC or ABCD2--determine manually')
                                        # mknote(indd,date,scantype)
                                        break
                                else:
                                    print('3T scan does not have inst. name or address to ID study, making note...')
                                    # mknote(indd,date,scantype)
                                    break
                            else:
                                print(f'{session.label} MRI needs a scan strength')
                    else:
                        continue #not a dicom file, skip it        

    return subject + "x" + date + "x" + scantype + "x" + study


if __name__ == "__main__":
    CmdName = os.path.basename(sys.argv[0])

    fw = fwgearutils.getFW("test")
    if not fw:
        print(f"{CmdName}: unable to initialize flywheel object", file=sys.stderr)
        sys.exit(1)

    # get NACC-SC flywheel project
    try:
        project = fw.get_project("5c508d5fc2a4ad002d7628d8")
    except flywheel.ApiException as e:
        print(f"Error: {e}")

    # get list of sessions
    try:
        sessions = project.sessions.iter_find("created>2022-12-01")
    except flywheel.ApiException as e:
        print(f"Error: {e}")

    # accepted options for scantypes and studies
    scantypelist = ["3T", "7T", "PI2620PET", "FBBPET", "AV1451PET", "FDGPET"]
    studylist = ["ABC", "ABCD2", "VCID", "LEADS", "YMTL"]

    # review each session
    for session in sessions:
        print('\n')
        print(f"{session.label}")

        sessionlabellist = session.label.rsplit("x", 3)
        subject = session.subject.label
        if '.' in subject or "_" in subject:
            print(f"Subejct label {subject} incorrect")
        date = str(session.timestamp)[:10].replace("-", "")

        if check_correct(sessionlabellist, subject, date) == [True, True, True, True]:
            print(f"{session.label} is correct")
            continue
        else:
            # print(f"{session.label} needs to be renamed")
            new_session_label=rename_session(session, subject, date)
            print(f"New label: {new_session_label}")
            # log session.label, new_session_label
            # session.update({'label': new_session_label})
