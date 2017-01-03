#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 08:26:01 2017

@author: danw
"""

#Paul's spec
#Just been playing catch up on this (on my phone). A couple of thoughts, 
#mostly to avoid painting ourselves into a corner.
#
#Identification vs names. Some people might be happy to be know as a hacker, 
#or a shedder, but not want detailed information available. There is also the 
#issue of more than 1 MAC address per person (Eg phone vs laptop etc).
#
#It might also be useful to 'tag' other items on the network, even if just to 
#limit the list of 'unknown' mac addresses to work with.
#
#Lastly, timeouts. There are a few places at the shed with poor Wi-Fi coverage.
# It could get confusing to the system if people 'left' every time they went 
#to the loos. Counter to that though, we don't want it to remember people who 
#left hours before. The easiest way might be to use a 'last seen' time stamp.
#
#Paul Hegarty [10:15 AM]  
#My thoughts on what we want it get from it:
#
#* Number of people at the shed.
#* Number of 'hackers' at the shed (number of other groups could also be useful).
#* Number of key holders at the shed.
#* Query if a particular person is at the shed.
#* Query when someone was last seen at the shed (and possibly how long they have been there).



from api import MacServer
from sqlalchemy.sql import func
import schema
import time

def howmanypeopleattheshed(serverobj, since_time):
    pass    
    

