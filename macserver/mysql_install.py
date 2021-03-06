# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 00:43:56 2017

@author: danw
"""

import schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def mysql_install(connstr,debug=False):
    dbengine = create_engine(connstr,echo=debug)
    session = sessionmaker(dbengine)
    schema.Base.metadata.create_all(dbengine)


if __name__ == '__main__':
    connstr = 'mysql+pymysql://dan:8Rr2%ynRAm%ng*K4@localhost/macserver'
    mysql_install(connstr,True)    
