#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 07:16:50 2017

@author: danw
"""

import schema

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

session = Session()
#create schema
schema.Base.metadata.create_all(engine)

member_tag = Tag(name='member')

ed_user = User(name='ed')
ed_phone = Device(name='edph',mac='00:00:11:23:45')
ed_tablet = Device(name='edtab', mac='00:00:12:44:55')
ed_phone.owner = ed_user

ed_user.devices = [ed_phone, ed_tablet]
ed_user.tags = [member_tag]


session.add_all([ed_user,ed_phone,ed_tablet,member_tag])

session.commit()