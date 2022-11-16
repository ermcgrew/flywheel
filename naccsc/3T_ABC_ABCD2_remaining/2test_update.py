import flywheel

fw = flywheel.Client()
#select project by project ID
try:
    project = fw.get_project('5c508d5fc2a4ad002d7628d8') #NACC-SC
    # project = fw.get_project('5ba2913fe849c300150d02ed')#Unsorted
except flywheel.ApiException as e:
    print(f'Error: {e}')

try:
    session = project.sessions.find('label=128827x20220628x3Tx')
except flywheel.ApiException as e:
    print(f'Error: {e}') 

print(session[0].label)
session[0].update({'label': '128827x20220628x3TxABC'})