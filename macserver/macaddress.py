#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 13:24:22 2017

@author: dweatherill
"""

from random import randint

import hashlib
import re

mac_regex = re.compile('^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$')



def generate_random():
    return ':'.join('%02x' % randint(0,255) for _ in range(6))  


def validate(mac):
    if mac_regex.match(mac) is None:
        raise ValueError('invalid mac address: %s' % mac)
    
def sanitize(mac):
    #change - separator to :, lowercase, strip whitespace
    mac = mac.replace('-',':').lower().strip()    
    return mac
                
def string_from_octets(octets):
    pass                
                
def shahash(mac):
    #TODO: how do you do this properly in py3k?
    return hashlib.sha256(mac.encode()).hexdigest()
#    return hashlib.sha256(mac).digest()
