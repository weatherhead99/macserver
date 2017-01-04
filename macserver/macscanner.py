#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:20:08 2017

@author: dweatherill
"""

import datetime
import schema
from macaddress import *
import subprocess
from api import MacServer
import asyncio

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

#def ARP_scan_shell():
#    raw_mac_scan = subprocess.check_output(['arp-scan','-l'])
#    macs = [_.split()[1].decode() for _ in raw_mac_scan.splitlines()[2:-3]]    
#    return macs

class basic_ARP_scan:
    def __init__(self, arpscanargs = None):
        self.arpscanargs = arpscanargs
        
    def __call__(self):
        raw_mac_scan = subprocess.check_output(['arp-scan','-l'] + self.arpscanargs)
        macs = [_.split()[1].decode() for _ in raw_mac_scan.splitlines()[2:-3]]    
        return macs
    
ARP_scan_shell = basic_ARP_scan()

allowed_config_fields = {'opportunistic_add': bool,
                         'timesheet_timeout': datetime.timedelta,
                         'arp_scan_func' : type(ARP_scan_shell)
                         }

config_defaults = {'opportunistic_add' : False,
                   'timesheet_timeout' : datetime.timedelta(minutes=30),
                    'arp_scan_func' : ARP_scan_shell}
                         
                         
class MACScanner:
    def __init__(self,serverobj, **kwargs):
        self.__serverobj = serverobj
        self.new_device_count = 0
        self.updated_devices = 0
        ##general config stuffs move out somewhere
        for k,v in kwargs.items():
            if k not in allowed_config_fields:
                raise ValueError('invalid config option %s passed to %s' %(k, self.__class__))
                
            if not isinstance(v,allowed_config_fields[k]):
                raise TypeError('invalid type for config option %s' % k)
            
            setattr(self,k,v)
            
        for k in allowed_config_fields:
            if not hasattr(self,k):
                setattr(self,k,config_defaults[k])
                
        
    def record_mac_seen(self,macaddr,dt=None):
        #get the current time
        if dt is None:
            dt = datetime.datetime.now()
            
        mac = sanitize(macaddr)
        validate(mac)
        secure_mac = shahash(mac)
        
        
        with self.__serverobj.dboperation() as session:
            try:
                dev = session.query(schema.Device).filter(schema.Device.hashmac==secure_mac).one()
                dev.lastseen = dt
                self.updated_devices += 1
            except MultipleResultsFound:
                raise IndexError('multiple matching devices found for MAC query. This Should never happen')
            except NoResultFound:
                if self.opportunistic_add:
                    #TODO: add_new_device
                    with self.__serverobj.dboperation() as session:
                        dev = schema.Device(hashmac = secure_mac, lastseen=dt)
                        session.add(dev)
                        self.new_device_count +=1
            
    
    @asyncio.coroutine
    def scan(self):
        self.new_device_count = 0
        self.updated_devices = 0
        macs_found = self.arp_scan_func()
        dtnow = datetime.datetime.now()        
        return macs_found,dtnow

@asyncio.coroutine
def scanner_run(interval_seconds,macscan):
    while True:
        print('beginning scan')
        macs, dtfound = yield from macscan.scan()
        print('scan complete')
        print('-------results-----------')
        print(macs)
        print('----- ' + str(dtfound) + '----')
        
        print('updating db state')
        for mac in macs:
            macscan.record_mac_seen(mac,dtfound)
        
        print('%d devices renewed' % macscan.updated_devices)
        print('%d new devices added' % macscan.new_device_count)        
        
        print('sleeping for %d seconds' % interval_seconds)
        yield from asyncio.sleep(interval_seconds)
    
    
    
if __name__ =='__main__':
    #TODO: config
    #TODO: graceful shutdown procedure
    scan_interval_s = 3    
    scan_backend = basic_ARP_scan(['-I wlan0'])    
    
    serv = MacServer('sqlite:///:memory:')
    ms = MACScanner(serv,opportunistic_add=True, arp_scan_func=scan_backend)
        
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    task = asyncio.ensure_future(scanner_run(scan_interval_s,ms))
    
    loop.run_forever()
    
    
    
    
    