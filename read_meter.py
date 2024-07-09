#!/usr/bin/env python3

import time
from pysiglent import *

def main():
    res_mgr=pyvisa.ResourceManager()
    print('Searching for available instruments...')
    inst=get_instruments(res_mgr)

    dvm=False

    # Enumerate what we found.
    enumerate(inst)

    # Find the first DVM.
    print('Searching for DVM(s)...')
    dvms=find_instrument_kind(inst,'DVM')
    if(len(dvms)>0):
        print('DVM found.')
        dvm=dvms[0]
    else:
        print('No DVM(s) found.')
        
    # Print the voltage ten times.
    if(dvm):
        dvm.query('SENSE:VOLTAGE:DC:RANGE DEF')
        for i in range(0,9):
            dvm_v=float(dvm.query('MEAS:VOLT? (@1)'))
            print('volts: '+str(dvm_v))
            time.sleep(0.1)

    # All done.
    close_all(inst)
    print('Done.')

if __name__=='__main__':
    main()
