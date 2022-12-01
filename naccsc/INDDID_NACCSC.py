import csv
import flywheel
fw = flywheel.Client()
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8')
except flywheel.ApiException as e:
    print(f'Error: {e}')

try:
    sessions = project.sessions.iter_find()
except flywheel.ApiException as e:
    print(f'Error: {e}')

inddlist=[]

for count, session in enumerate(sessions, 1):
    print(f'Loop {count}: {session.label}')
    indd=session.subject.label
    if indd not in inddlist:
        print(f'writing indd {indd} to list')
        inddlist.append(indd)
    else:
        print(f'indd {indd} already captured, skipping')
        continue
 
for x in range(0,len(inddlist)):
    inddlist[x]=inddlist[x].split()

with open(f'inddid_naccsc_list.csv', 'w', newline='') as csvfile:
    csvwriter=csv.writer(csvfile)
    csvwriter.writerows(inddlist)