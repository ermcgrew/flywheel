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
        # print(f"{session.label}")

        sessionlabellist = session.label.rsplit("x", 3)
        subject = session.subject.label
        date = str(session.timestamp)[:10].replace("-", "")

        if check_correct(sessionlabellist, subject, date) == [True, True, True, True]:
            print(f"{session.label} is correct")
            continue
        else:
            print(f"{session.label} needs to be renamed")
