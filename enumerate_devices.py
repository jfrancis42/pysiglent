#!/usr/bin/env python3

from pysiglent import *

def main():
    res_mgr=pyvisa.ResourceManager()
    inst=get_instruments(res_mgr)
    enumerate(inst)
    close_all(inst)

if __name__=='__main__':
    main()
