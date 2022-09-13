import flywheel
fw = flywheel.Client()

session = fw.get('631a35c680fcd66d1fe77a21')
print(session.label)

newlabel = '125111x20220829xPI2620PETxABC'

session.update({'label':newlabel})
print(f'Session name updated to: {session.label}')
