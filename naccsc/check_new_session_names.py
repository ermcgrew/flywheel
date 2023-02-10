#!/usr/bin/python3

import fwgearutils
import flywheel
import sys 
import os 

if __name__ == '__main__':
    CmdName = os.path.basename(sys.argv[0])
    
    fw = fwgearutils.getFW('test')
    if (not fw):
        print(f"{CmdName}: unable to initialize flywheel object", file=sys.stderr)
        sys.exit(1)

    try:
        project = fw.get_project('5c508d5fc2a4ad002d7628d8')
    except flywheel.ApiException as e:
        print(f'Error: {e}')    
    
    #create list of sessions
    try:
        sessions = project.sessions.iter_find("created>2022-12-01")
    except flywheel.ApiException as e:
        print(f'Error: {e}')

    scantypelist=["3T", "7T", "PI2620PET", "FBBPET", "AV1451PET", "FDGPET"]
    studylist=["ABC", "ABCD2", "VCID", "LEADS", "YMTL"]
    
    for session in sessions:
        print(f"{session.label}")
        
        # break into pieces 
        sessionlabellist=session.label.rsplit('x',3)
        check=[False,False,False,False]

        if len(sessionlabellist) == 4:
            if sessionlabellist[0] == session.subject.label:
                check[0]=True
            
            if sessionlabellist[1] == str(session.timestamp)[:10].replace('-',''):
                check[1]=True

            if sessionlabellist[2] in scantypelist:
                check[2]=True    

            if sessionlabellist[3] in studylist:
                check[3]=True    
            
            # if all check items are True
                # continue
            # else:
                # print("needs renaming")
        else:
            print('needs renaming')
            


# if first piece == subject.session.label
# if second piece == timestamp
# if third piece in scantypelist 3T 7T PI2620PET FBBPET AV1451PET FDGPET
# if last piece in study suffix list ABC, ABCD2, VCID, LEADS, YMTL

# if all true
# then true
# else go to rename function