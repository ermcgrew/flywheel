import flywheel
fw = flywheel.Client()

session = fw.get('63615c9a8724cd74af8fbea8')
print(session.label)
if '_' in session.subject.label: 
    indd=session.subject.label.replace('_',"x")
    session.subject.update(label=indd)
else: 
    indd = session.subject.label
    
date = str(session.timestamp)[:10].replace('-','')

labellist=[acquisition.label for acquisition in session.acquisitions()]
if 'Axial MB DTI' in labellist:
    study='LEADS'
elif 'LLASL_m16LC_3.0s_2.0s_bs31_mis' in labellist:
    study='DVCID'

for acquisition in session.acquisitions():
    if acquisition.label == "PhoenixZIPReport" or acquisition.label == "Exam Summary_401_401":
        continue
    else:
        acquisition = acquisition.reload() 
        if acquisition.files[0].type == 'dicom':
            f = acquisition.files[0].info 
            magstrength=f['MagneticFieldStrength']
            if magstrength == 3:
                scantype = '3T'
        break

newlabel = indd + 'x' + date + 'x' + scantype + 'x' + study
print(f'Renaming session to: {newlabel}') 

session.update({'label':newlabel})
print(f'Session name updated to: {session.label}')
