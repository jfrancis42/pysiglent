#!/usr/bin/env python3

import time
from pysiglent import *

global csv_out
csv_out=True

def main():
    res_mgr=pyvisa.ResourceManager()
    print('Searching for available instruments...')
    inst=get_instruments(res_mgr)

    dvm=False
    psu=False

    global csv_out

    # Enumerate what we found.
    for i in inst:
        print('mfg:    '+i.mfg())
        print('model:  '+i.model())
        print('serial: '+i.serial())
        print('ver:    '+i.ver())
        print('kind:   '+i.kind)
        print()

    print('Searching for PSU(s)...')
    psus=find_instrument_kind(inst,'PSU')
    if(len(psus)>0):
        print('PSU found.')
        psu=psus[0]
    else:
        print('No PSU(s) found.')
    print()

    print('Searching for DVM(s)...')
    dvms=find_instrument_kind(inst,'DVM')
    if(len(dvms)>0):
        print('DVM found.')
        dvm=dvms[0]
    else:
        print('No DVM(s) found.')
    print()
        
    if(dvm and psu):
        print('Setting DVM to read DC voltage...')
        psu.query('VOLTAGE:DC:RANGE DEF')
        print('Setting PSU Channel 2 active...')
        psu.query('INST CH2')
        print('Setting PSU Channel 2 to 1.5A max...')
        psu.query('CH2:CURRENT 1.5')
        print('Setting PSU Channel 2 to 1.0VDC...')
        psu.query('CH2:VOLTAGE 1.0')
        print('Turning PSU Channel 2 On...')
        psu.query('OUTPUT CH2,ON')
        print()
        time.sleep(1.0)

        f=open('out.csv','w')
        f.write('dvm_v,dvm_a,dvm_w,psu_v,psu_a,psu_w\n')

        v=1.0
        for i in range(0,25):
            psu.query('CH2:VOLTAGE '+str(v))
            v=v+1
            if(v>20):
                v=20
            dvm_v=float(dvm.query('MEAS:VOLT? (@1)'))
            psu_v=float(psu.query('MEASURE:VOLTAGE? CH2'))
            psu_a=float(psu.query('MEASURE:CURRENT? CH2'))
            psu_w=float(psu.query('MEASURE:POWER? CH2'))
            dvm_a=dvm_v/1.03
            dvm_w=dvm_a*psu_v
            if(csv_out):
                s=str(dvm_v)+','+str(dvm_a)+','+str(dvm_w)+','+str(psu_v)+','+str(psu_a)+','+str(psu_w)+'\n'
                f.write(s)
            print('dvm_v: '+str(dvm_v))
            print('dvm_a: '+str(dvm_a))
            print('dvm_w: '+str(dvm_w))
            print('psu_v: '+str(psu_v))
            print('psu_a: '+str(psu_a))
            print('psu_w: '+str(psu_w))
            print()
            time.sleep(0.1)

        print('Turning PSU Channel 2 Off...')
        psu.query('OUTPUT CH2,OFF')
        print('Setting PSU Channel 2 to 1.0VDC...')
        psu.query('CH2:VOLTAGE 1.0')
        time.sleep(1.0)

    if(csv_out):
        f.flush()
        f.close()

    close_all(inst)
    print('Done.')

if __name__=='__main__':
    main()
