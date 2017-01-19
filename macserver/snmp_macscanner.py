# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 21:59:39 2017

@author: danw
"""

from pysnmp.hlapi import *

#E-MSM460
#iso 3.6.1.2.1.17.4.3.1.1.0.12.41.130.42.125
#iso.3.6.1.2.1.17.4.3.1.1
#SNMPv2-SMI::mib-2.17.4.3.1.1

#.1.3.6.1.4.1.8744.5.4.1.5.1.2.5
#.1.3.6.1.4.1.8744.5.4.1.5.1.2.4 

#both .1.3.6.1.4.1.8744.5.4.1.5.1.2
#position 12 != 2

def yield_macaddrs():
    it = nextCmd(SnmpEngine(),
         CommunityData('MiSMK_READ',mpModel=1),
           UdpTransportTarget(('192.168.0.3',161)),
           ContextData(),
           ObjectType(ObjectIdentity('.1.3.6.1.4.1.8744.5.4.1.5.1.2'))
           ) 
    for errIndic, errSt, errIdx, varBinds in it:
        if errIndic:
            print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            raise RuntimeError('SNMP Error %s' % str(errIndic))
        
            #HACK for breaking out if 13th position is not 
        if varBinds[0][0][12] != 2 :
            break
        yield varBinds[0][1]
                        

def snmp_macscan():
    addrs = [_.asOctets() for _ in yield_macaddrs()]
    return [string_from_octets(_) for _ in addrs]

def string_from_octets(octets):
    chrs = ('{:02x}'.format(_) for _ in octets)
    return ":".join(chrs)

if __name__ == '__main__':
    macit = yield_macaddrs()
    macaddrs = list(macit)
