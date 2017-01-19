#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 10:14:29 2017

@author: weatherill
"""

import schema
import api
from random import randint, sample
from itertools import chain, repeat
from collections import defaultdict
from datetime import datetime
from macaddress import generate_random

import meninsheds

macserver = api.MacServer('sqlite:///:memory:')

MiS_tags = ['shedder', 'hackspace', 'keyholder']
MiS_test_users = ['Mike', 'Steve', 'Gemma', 'Horatio', 'Imhotep', 'Keith',
                      'Abaddon the Despoiler', 'Jeff', 'Ralph', 'Sanjeev', ' Надежда']        
device_types = ['phone', 'tablet', 'laptop', 'CRAY-T94']    
    

                  
def generate_test_user_data():
    #make up some random devices and assign random tags
    users = defaultdict(lambda: {})    
    
    for user in MiS_test_users :
        num_tags = randint(1,2)
        users[user]['tags'] = sample(MiS_tags, num_tags)
        
        num_devices = randint(0,3)    
        users[user]['devices'] = {user+'_'+_:generate_random() for _ in sample(device_types,num_devices)}

    return users
        
    
def populate_database(apiobj, users, tags):
    schema_tags = {_:schema.Tag(name=_) for _ in tags}
    
    schema_users = []
    schema_devices = []
                   
    for username,userdata in users.items():
        thistags = [schema_tags[_] for _ in userdata['tags']]
        u = schema.User(name=username,tags=thistags)
        thisdevices = [schema.Device.from_plaintext_mac(v,name=k, owner = u) for k,v in userdata['devices'].items() ]
        
        schema_users.append(u)
        schema_devices.extend(thisdevices)
        
    
    with apiobj.dboperation() as sesh:
        sesh.add_all(schema_users)
    

if __name__ == '__main__':
    
    macserver = api.MacServer('sqlite:///:memory:')
    users = generate_test_user_data()
    
    populate_database(macserver,users,MiS_tags)
    
    print('---- generated user data-------')
    print(users)
    print('-------------------------------')
    
    
    

    
    
    
    
    
    
        
    