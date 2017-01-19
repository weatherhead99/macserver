#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 08:12:45 2017

@author: danw
"""

import schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from contextlib import contextmanager

class MacServer:
    def __init__(self,dbstr,debug=False):
        self.dbengine = create_engine(dbstr,echo=debug)
        self.Session = sessionmaker(bind=self.dbengine)     
#        schema.Base.metadata.create_all(self.dbengine)
    
    @contextmanager
    def dboperation(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            
    