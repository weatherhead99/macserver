#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 06:55:39 2017

@author: danw
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table, Boolean
from macaddress import sanitize, shahash

Base = declarative_base()

class IntegerPrimaryKeyMixin:
    id = Column(Integer,primary_key=True)

class NameMixin:
    name = Column(String,unique=True)
        
class DefaultReprMixin:
    def __repr__(self):
        nm = self.__class__.__name__

        printid = self.id if self.id is not None else -1    
        
        if hasattr(self,'name'):
            return '<%s, name=%s, id=%d>' % (nm, self.name, printid)
        else:
            return '<%s, id=%d>' %(nm,printid)
    
UserTagAssociation = Table('users_tags', Base.metadata,
                           Column('user_id',ForeignKey('users.id')),
                                  Column('tag_id',ForeignKey('tags.id')))


DeviceTimeSheetAssociation = Table('devices_timesheets', Base.metadata,
                                   Column('device_id',ForeignKey('devices.id')),
                                   Column('timesheet_id',ForeignKey('timesheets.id')))
    
class User(IntegerPrimaryKeyMixin, NameMixin, DefaultReprMixin, Base):
    __tablename__ = 'users'
    tags = relationship('Tag', secondary=UserTagAssociation,
                        back_populates='users')    
    lastseen = Column(DateTime)
    maindevice = Column(Integer,ForeignKey('devices.id'))
    publish = Column(Boolean)

    
class Device(IntegerPrimaryKeyMixin,DefaultReprMixin, Base):
    __tablename__ = 'devices'
    name = Column(String)
    #TODO: mac addresses are unique
    hashmac = Column(String)
    ownerid = Column(Integer,ForeignKey('users.id'))
    owner = relationship('User', back_populates='devices',foreign_keys=ownerid)
    timesheets = relationship('TimeSheet',secondary=DeviceTimeSheetAssociation,
                              back_populates='devices_seen')    
    lastseen = Column(DateTime)
    #TODO: how to get SQLalchemy to update this automatically?
    ismaindevice = Column(Boolean)
    
    @classmethod
    def from_plaintext_mac(cls,mac,*args,**kwargs):
        return cls(hashmac=shahash(sanitize(mac)),*args,**kwargs)
    
User.devices = relationship('Device',order_by=Device.id,back_populates='owner',foreign_keys=Device.ownerid)
    

    
class Tag(IntegerPrimaryKeyMixin,NameMixin, DefaultReprMixin, Base):
    __tablename__ = 'tags'
    
    users = relationship('User',secondary=UserTagAssociation,
                        back_populates='tags')
    


class TimeSheet(IntegerPrimaryKeyMixin, DefaultReprMixin, Base):
    __tablename__ = 'timesheets'
    
    personid = Column(Integer,ForeignKey('users.id'))
    person = relationship('User',back_populates='timesheets')
    timein = Column(DateTime)
    timeout = Column(DateTime)
    devices_seen = relationship('Device', secondary=DeviceTimeSheetAssociation,
                                back_populates='timesheets')    
    
User.timesheets = relationship('TimeSheet',order_by=TimeSheet.id,back_populates='person')