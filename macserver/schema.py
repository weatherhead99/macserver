#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 06:55:39 2017

@author: danw
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean


Base = declarative_base()

class IntegerPrimaryKeyMixin:
    id = Column(Integer,primary_key=True)

        
UserTagAssociation = Table('users_tags', Base.metadata,
                           Column('user_id',ForeignKey('users.id')),
                                  Column('tag_id',ForeignKey('tags.id')))


DeviceTimeSheetAssociation = Table('devices_timesheets', Base.metadata,
                                   Column('device_id',ForeignKey('devices.id')),
                                   Column('timesheet_id',ForeignKey('timesheets.id')))
    
class User(IntegerPrimaryKeyMixin,Base):
    __tablename__ = 'users'
    name = Column(String)
    tags = relationship('Tag', secondary=UserTagAssociation,
                        back_populates='users')    
    lastseen = Column(DateTime)
    maindevice = Column(Integer,ForeignKey('devices.id'))
    publish = Column(Boolean)

    
class Device(IntegerPrimaryKeyMixin,Base):
    __tablename__ = 'devices'
    name = Column(String)
    mac = Column(String)
    ownerid = Column(Integer,ForeignKey('users.id'))
    owner = relationship('User', back_populates='devices',foreign_keys=ownerid)
    timesheets = relationship('TimeSheet',secondary=DeviceTimeSheetAssociation,
                              back_populates='devices_seen')    
    
User.devices = relationship('Device',order_by=Device.id,back_populates='owner',foreign_keys=Device.ownerid)
    
    
class Tag(IntegerPrimaryKeyMixin,Base):
    __tablename__ = 'tags'
    name = Column(String)
    users = relationship('User',secondary=UserTagAssociation,
                        back_populates='tags')
    


class TimeSheet(IntegerPrimaryKeyMixin,Base):
    __tablename__ = 'timesheets'
    
    personid = Column(Integer,ForeignKey('users.id'))
    person = relationship('User',back_populates='timesheets')
    timein = Column(DateTime)
    timeout = Column(DateTime)
    devices_seen = relationship('Device', secondary=DeviceTimeSheetAssociation,
                                back_populates='timesheets')    
    
User.timesheets = relationship('TimeSheet',order_by=TimeSheet.id,back_populates='person')