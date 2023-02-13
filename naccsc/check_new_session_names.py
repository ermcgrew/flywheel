#!/usr/bin/python3

import fwgearutils
import flywheel
import sys
import os


def check_correct(sessionlabellist, subject, date):
    if (
        len(sessionlabellist) == 4
        and sessionlabellist[0] == subject
        and sessionlabellist[1] == date
        and sessionlabellist[2] in scantypelist
        and sessionlabellist[3] in studylist
    ):
        return True
    else:
        return False


def rename_session(session, subject, date):
    # print('in renaming function')
    # print(session.label)
    scantype = ""
    study = ""

    for acquisition in session.acquisitions():
        # print(f"acqq label: {acquisition.label}")
        if scantype == "":  # keeps from looping through every acq
            modality = acquisition.files[0].modality
            if (modality == "CT" or modality == "SR"):  
            # those acquisitions don't have detailed metadata
                continue
            else:
                dicom_file_index=[x for x in range(0,len(acquisition.files)) if acquisition.files[x].type == "dicom"]
                acquisition = acquisition.reload()
                file_info = acquisition.files[dicom_file_index[0]].info
                # only need the dicom file's metadata
                labels = " ".join([acquisition.label for acquisition in session.acquisitions()])
                # all acq.labels into 1 string to be partial-matched to

                # dictionary of metadata info per file
                datadict = {
                    "MagneticFieldStrength": "",
                    "InstitutionName": "",
                    "InstitutionAddress": "",
                    "PerformedProcedureStepDescription": "",
                    "ProtocolName": "",
                }
                # populate datadict with info, error if key not found
                for key in datadict:
                    try:
                        datadict[key] = file_info[key]
                    except KeyError as error:
                        print(f"Key {error} not found")

                if modality == "PT":
                    if "Amyloid" in labels or "AV45" in labels:
                        scantype = "FBBPET"
                        if (
                            "844047"
                            in datadict["PerformedProcedureStepDescription"]
                            or "844047" in datadict["ProtocolName"]
                        ):
                            study = "ABCD2"
                            break
                        elif (
                            "825943"
                            in datadict["PerformedProcedureStepDescription"]
                            or "825943" in datadict["ProtocolName"]
                        ):
                            study = "ABC"
                            break
                        elif (
                            "829602"
                            in datadict["PerformedProcedureStepDescription"]
                            or "829602" in datadict["ProtocolName"]
                        ):
                            study = "LEADS"
                            break
                        else:
                            print(
                                "No matching performed procedure step description found, making note..."
                            )
                            # mknote(indd,date,scantype)
                            break
                    elif "2620" in labels:
                        # PI2620 sometimes listed with space--PI 2620
                        scantype = "PI2620PET"
                        study = "ABC"
                        break
                    elif "AV1451" in labels:
                        scantype = "AV1451PET"
                        if (
                            "844403"
                            in datadict["PerformedProcedureStepDescription"]
                            or "844403" in datadict["ProtocolName"]
                        ):
                            study = "ABCD2"
                            break
                        elif (
                            "825944"
                            in datadict["PerformedProcedureStepDescription"]
                            or "833864"
                            in datadict["PerformedProcedureStepDescription"]
                            or "825944" in datadict["ProtocolName"]
                            or "833864" in datadict["ProtocolName"]
                        ):
                            study = "ABC"
                            break
                        elif (
                            "829602"
                            in datadict["PerformedProcedureStepDescription"]
                            or "829602" in datadict["ProtocolName"]
                        ):
                            study = "LEADS"
                            break
                        else:
                            print(
                                "No matching performed procedure step description found, making note..."
                            )
                            # mknote(indd,date,scantype)
                            break
                    elif "FDG" in labels:
                        scantype = "FDGPET"
                        study = "LEADS"
                        break
                    else:
                        print(f"{session.label} PET scan needs scantype")

                elif modality == "MR":
                    if round(datadict["MagneticFieldStrength"]) == 7:
                        scantype = "7T"
                        if session.label[-4:] == "YMTL":
                            study = "YMTL"
                            break
                        else:
                            study = "ABC"
                            break
                    elif datadict["MagneticFieldStrength"] == 3:
                        scantype = "3T"
                        if (
                            datadict["InstitutionName"] == "HUP"
                            or "Spruce" in datadict["InstitutionAddress"]
                        ):
                            if "Axial" in labels:
                                study = "LEADS"
                                break
                            elif "LLASL" in labels:
                                study = "VCID"
                                break
                            else:
                                print(
                                    "HUP 3T scan labels insufficient to id study, making note..."
                                )
                                # mknote(indd,date,scantype)
                                break
                        elif (
                            datadict["InstitutionName"] == "SC3T"
                            or "Curie" in datadict["InstitutionAddress"]
                        ):
                            if session.label[-4:] == "YMTL":
                                study = "YMTL"
                                break
                            elif session.label[-5:] == "ABCD2":
                                study = "ABCD2"
                                break
                            elif session.label[-3:] == "ABC":
                                study = "ABC"
                                break
                            else:
                                print("ABC or ABCD2--determine manually")
                                # mknote(indd,date,scantype)
                                break
                        else:
                            print(
                                "3T scan does not have inst. name or address to ID study, making note..."
                            )
                            # mknote(indd,date,scantype)
                            break
                    else:
                        print(f"{session.label} MRI needs a scan strength")

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
        print("")
        print(f"{session.label}")

        sessionlabellist = session.label.rsplit("x", 3)
        subject = session.subject.label
        if "." in subject or "_" in subject:
            print(f"Subejct label {subject} incorrect")
        date = str(session.timestamp)[:10].replace("-", "")

        if check_correct(sessionlabellist, subject, date):
            print(f"{session.label} is correct")
            continue
        else:
            # print(f"{session.label} needs to be renamed")
            new_session_label = rename_session(session, subject, date)
            print(f"New label: {new_session_label}")
            # log session.label, new_session_label
            # session.update({'label': new_session_label})
