#!/usr/bin/python3

import fwgearutils
import flywheel
import logging
from datetime import datetime


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
    scantype = ""
    study = ""
    datadict = {
        "MagneticFieldStrength": "",
        "InstitutionName": "",
        "InstitutionAddress": "",
        "PerformedProcedureStepDescription": "",
        "ProtocolName": "",
    }

    for acquisition in session.acquisitions():
        modality = acquisition.files[0].modality
        if modality == "CT" or modality == "SR":
            # those acquisitions don't have detailed metadata
            continue
        else:
            acquisition = acquisition.reload()

            # all acq.labels into 1 string to be partial-matched to
            labels = " ".join(
                [acquisition.label for acquisition in session.acquisitions()]
            )

            # only need the dicom file's metadata
            dicom_file_index = [
                x
                for x in range(0, len(acquisition.files))
                if acquisition.files[x].type == "dicom"
            ][0]
            file_info = acquisition.files[dicom_file_index].info
            # populate datadict with info, error if key not found
            for key in datadict:
                try:
                    datadict[key] = file_info[key]
                except KeyError:
                    pass

            if modality == "PT":
                if "Amyloid" in labels or "AV45" in labels:
                    scantype = "FBBPET"
                    if (
                        "844047" in datadict["PerformedProcedureStepDescription"]
                        or "844047" in datadict["ProtocolName"]
                    ):
                        study = "ABCD2"
                        break
                    elif (
                        "825943" in datadict["PerformedProcedureStepDescription"]
                        or "825943" in datadict["ProtocolName"]
                    ):
                        study = "ABC"
                        break
                    elif (
                        "829602" in datadict["PerformedProcedureStepDescription"]
                        or "829602" in datadict["ProtocolName"]
                    ):
                        study = "LEADS"
                        break
                    else:
                        continue
                elif "2620" in labels:
                    # PI2620 sometimes listed with space--PI 2620
                    scantype = "PI2620PET"
                    study = "ABC"
                    break
                elif "AV1451" in labels:
                    scantype = "AV1451PET"
                    if (
                        "844403" in datadict["PerformedProcedureStepDescription"]
                        or "844403" in datadict["ProtocolName"]
                    ):
                        study = "ABCD2"
                        break
                    elif (
                        "825944" in datadict["PerformedProcedureStepDescription"]
                        or "833864" in datadict["PerformedProcedureStepDescription"]
                        or "825944" in datadict["ProtocolName"]
                        or "833864" in datadict["ProtocolName"]
                    ):
                        study = "ABC"
                        break
                    elif (
                        "829602" in datadict["PerformedProcedureStepDescription"]
                        or "829602" in datadict["ProtocolName"]
                    ):
                        study = "LEADS"
                        break
                    else:
                        continue
                elif "FDG" in labels:
                    scantype = "FDGPET"
                    study = "LEADS"
                    break
                else:
                    break

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
                            continue
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
                            logging.warning(f"{session.label}; ABC or ABCD2")
                            break
                    else:
                        continue
                else:
                    continue

    return subject + "x" + date + "x" + scantype + "x" + study


def main():
    fw = fwgearutils.getFW("")
    if not fw:
        logging.critical("Unable to establish flywheel client")

    # get NACC-SC flywheel project
    try:
        project = fw.get_project("5c508d5fc2a4ad002d7628d8")
    except flywheel.ApiException:
        logging.exception("Exception occurred")

    # get list of sessions
    try:
        sessions = project.sessions.iter_find("created>2022-12-01")
    except flywheel.ApiException:
        logging.exception("Exception occurred")

    for session in sessions:
        sessionlabellist = session.label.rsplit("x", 3)
        subject = session.subject.label
        if "." in subject or "_" in subject:
            logging.warning(f"Subejct label {subject} incorrect")

        date = str(session.timestamp)[:10].replace("-", "")

        if check_correct(sessionlabellist, subject, date):
            logging.debug(f"Session label {session.label} is correct")
            continue
        else:
            new_session_label = rename_session(session, subject, date)
            logging.info(
                f"Session label renamed from:{session.label}:{new_session_label}"
            )
            if new_session_label[-1:] == "x":
                logging.warning(
                    f"{session.label}:{new_session_label}; insufficient information for scantype and/or study"
                )
            # session.update({'label': new_session_label})


current_time = datetime.now().strftime("%Y-%m-%dT%H_%M_%S")
# logging.basicConfig(filename=f"log_check_new_session_names_{current_time}.txt", filemode='w', format='%(levelname)s: %(message)s', level=logging.DEBUG)
logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.DEBUG)
# Debug level: correct session label
# Info level: renamed session label
# Warning level: incorrectly formatted subject label & insufficient information for full renaming
# get list of renamed sessions with:
# cat log_check_new_session_names_2023-02-13T16_27_33.txt | grep INFO | cut -d ":" -f 3,4
# get list of items needing attention with:
# cat log_check_new_session_names_2023-02-13T16_27_33.txt | grep WARNING

scantypelist = ["3T", "7T", "PI2620PET", "FBBPET", "AV1451PET", "FDGPET"]
studylist = ["ABC", "ABCD2", "VCID", "LEADS", "YMTL"]

main()
# after main, send log file to email--how?
