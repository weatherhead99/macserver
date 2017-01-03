#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 06:55:39 2017

@author: danw
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table


Base = declarative_base()

class IntegerPrimaryKeyMixin:
    id = Column(Integer,primary_key=True)

        
UserTagAssociation = Table('users_tags', Base.metadata,
                           Column('user_id',ForeignKey('users.id')),
                                  Column('tag_id',ForeignKey('tags.id')))
    
class User(IntegerPrimaryKeyMixin,Base):
    __tablename__ = 'users'
    name = Column(String)
    tags = relationship('Tag', secondary=UserTagAssociation,
                        back_populates='users')    

class Device(IntegerPrimaryKeyMixin,Base):
    __tablename__ = 'devices'
    name = Column(String)
    mac = Column(String)
    ownerid = Column(Integer,ForeignKey('users.id'))
    owner = relationship('User', back_populates='devices')
    
User.devices = relationship('Device',order_by=Device.id,back_populates='owner')
    
    
class Tag(IntegerPrimaryKeyMixin,Base):
    __tablename__ = 'tags'
    name = Column(String)
    users = relationship('User',secondary=UserTagAssociation,
                        back_populates='tags')
    
    
