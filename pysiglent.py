#!/usr/bin/env python3

import pyvisa
import time

global query_sleep
global device_timeout
global retry_times

query_sleep=0.2
device_timeout=10000
retry_times=15

class Instrument:
    def __init__(self,res_mgr,res_path):
        global device_timeout
        
        self.delay=0.2
        self.thing=res_mgr.open_resource(res_path)
        self.thing.timeout=device_timeout
        try:
            self.idn=self.query('*IDN?').rstrip()
        except:
            self.idn=False
            self.good=False
            self.thing=False
            self.kind=False
        else:
            self.good=True
            if(self.mfg()=='Siglent Technologies'):
                if(self.model()[0:3]=='SDS'):
                    self.kind='OSCOPE'
                if(self.model()[0:3]=='SDG'):
                    self.kind='SIGGEN'
                if(self.model()[0:3]=='SDM'):
                    self.kind='DVM'
                if(self.model()[0:3]=='SSA'):
                    self.kind='SPECAN'
                if(self.model()[0:3]=='SPD'):
                    self.kind='PSU'

    def query(self,string):
        global query_sleep

        try:
            self.thing.write(string)
            time.sleep(query_sleep)
            res=self.thing.read().rstrip()
        except:
            return(False)
        else:
            return(res)

    def query_bin(self,string):
        global query_sleep

        try:
            self.thing.write(string)
            time.sleep(query_sleep)
            res=self.thing.read_raw()
        except:
            return(False)
        else:
            return(res)

    def valid(self):
        return(self.good)

    def screencapbmp(self):
        return(self.query_bin('SCDP'))

    def mfg(self):
        if(self.idn):
            return(self.idn.split(',')[0])

    def model(self):
        if(self.idn):
            return(self.idn.split(',')[1])

    def serial(self):
        if(self.idn):
            return(self.idn.split(',')[2])

    def ver(self):
        if(self.idn):
            return(self.idn.split(',')[3])

    def done(self):
        if(self.thing):
            self.thing.close()

def enumerate(inst):            
    for i in inst:
        print('mfg:    '+i.mfg())
        print('model:  '+i.model())
        print('serial: '+i.serial())
        print('ver:    '+i.ver())
        print('kind:   '+i.kind)
        print()

def get_instruments(res_mgr):
    inst=list(filter(lambda n: n.valid(),list(map(lambda i: Instrument(res_mgr,i),res_mgr.list_resources()))))

    global retry_times

    i=False
    retry=retry_times
    while(retry>0):
        try:
            i=Instrument(res_mgr,'TCPIP::10.1.1.185::INSTR')
        except:
            retry=retry-1
            time.sleep(0.5)
        else:
            inst.append(i)
            retry=-1

    if(not(i)):
        print('-----------------------------------------')
        print('Failed to find manually-specified device.')
        print('-----------------------------------------')

    return(inst)

def close_all(inst):
    for i in inst:
        print('Closing '+i.idn+'...')
        i.done()

def find_instrument_kind(instruments,kind):
    return(list(filter(lambda i: i.kind==kind,instruments)))

if __name__ == '__main__':
    print("This is a library and is not intended for stand-alone execution.")
