#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:20:08 2017

@author: dweatherill
"""

import datetime
import schema
from macaddress import *

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

allowed_config_fields = {'opportunistic_add': bool,
                         'timesheet_timeout': datetime.timedelta,
                         }

config_defaults = {'opportunistic_add' : False,
                   'timesheet_timeout' : datetime.timedelta(minutes=30)}
                         
                         
class MACScanner:
    def __init__(self,serverobj, **kwargs):
        self.__serverobj = serverobj
        
        
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
            except MultipleResultsFound:
                raise IndexError('multiple matching devices found for MAC query. This Should never happen')
            except NoResultsFound:
                if self.opportunistic_add:
                    #TODO: add_new_device
                    print('TODO:add_new_device')                
                

    def run_scan(self):
        pass
                    
                    

                
if __name__ =='__main__':
    from api import MacServer
    
    serv = MacServer('sqlite:///:memory:')
    
    ms = MACScanner(serv,opportunistic_add=True)