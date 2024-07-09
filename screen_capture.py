#!/usr/bin/env python3

import pyvisa
from siglent import *

def main():
    res_mgr=pyvisa.ResourceManager()
    print('Searching for available instruments...')
    inst=get_instruments(res_mgr)
    enumerate(inst)

    print('----')
    print('Searching for Oscilloscope(s)...')
    oscopes=find_instrument_kind(inst,'OSCOPE')
    if(len(oscopes)>0):
        print('Capturing screen...')
        f=open('capture_oscope.bmp','wb')
        f.write(oscopes[0].screencapbmp())
        f.flush()
        f.close()
    else:
        print('No Oscilloscope(s) found.')
    print('----')
    print()

    print('----')
    print('Searching for Spectrum Analyzer(s)...')
    specans=find_instrument_kind(inst,'SPECAN')
    if(len(specans)>0):
        print('Capturing screen...')
        f=open('capture_specan.bmp','wb')
        f.write(specans[0].screencapbmp())
        f.flush()
        f.close()
    else:
        print('No Spectrum Analyzer(s) found.')
    print('----')
    print()

    close_all(inst)
    print('Done.')

if __name__=='__main__':
    main()
