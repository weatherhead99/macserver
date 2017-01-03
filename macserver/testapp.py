#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 07:16:50 2017

@author: danw
"""

import api
from schema import Tag, User, Device

member_tag = Tag(name='member')

ed_user = User(name='ed')
ed_phone = Device(name='edph',mac='00:00:11:23:45')
ed_tablet = Device(name='edtab', mac='00:00:12:44:55')
ed_phone.owner = ed_user

ed_user.devices = [ed_phone, ed_tablet]
ed_user.tags = [member_tag]


a = api.MacServer('sqlite:///:memory:',True)

#with a.dboperation() as sesh:
#    sesh.add(ed_user)
#
#with a.dboperation() as sesh:
#    sesh.que