from csv import field_size_limit
from pprint import pprint
from datetime import datetime
import csv

import flywheel
fw = flywheel.Client()

try:
    project = fw.get_project('6328e43d7be4e9e7d7d5fcfc')
    # project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

try:
    sessions = project.sessions.iter_find()

except flywheel.ApiException as e:
    print(f'Error: {e}')


filename='wecandreamfiles.csv'
headerrow= ['session.label','acquisition.label','f.info["ProtocolName"]', 'Intent', 'Measurement', 'Features']
with open(filename, 'w', newline='') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerow(headerrow)
    for count, session in enumerate(sessions, 1):
        print(f'session loop {count}: {session.label}')
        for acquisition in session.acquisitions():
            acquisition = acquisition.reload()
            for f in acquisition.files:
                    filerow=[]
                    filerow.append(session.label)
                    filerow.append(acquisition.label)
                    
                    try:
                        filerow.append(f.info['ProtocolName'])
                    except KeyError as error:
                        filerow.append('n/a')

                    try:
                        filerow.append(acquisition.files[0].classification['Intent'])
                    except KeyError as error:
                        filerow.append('n/a')

                    try:
                        filerow.append(acquisition.files[0].classification['Measurement'])
                    except KeyError as error:
                        filerow.append('n/a')

                    try:
                        filerow.append(acquisition.files[0].classification['Features'])
                    except KeyError as error:
                        filerow.append('n/a')

                    csvwriter.writerow(filerow)