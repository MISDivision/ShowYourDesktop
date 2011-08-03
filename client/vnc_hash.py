#!/usr/bin/env python
##
##  vnc_hash.py - ShowYourDesktop
## 
## Written by Gringo Suave
## http://www.geekademy.com/2010/10/creating-hashed-password-for-vnc.html
## 

# This module is used to generate a 3des VNC hash used to store in the 
# VNC connection profile.
#

import d3des as d

def get_vnc_hash(password):
    passpadd = (password + '\x00'*8)[:8]
    strkey = ''.join([ chr(x) for x in d.vnckey ])
    ekey = d.deskey(strkey, False)

    hashed = d.desfunc(passpadd, ekey)
    return hashed.encode('hex')
    
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print get_vnc_hash(sys.argv[1])
    else:
        print 'usage: %s ' % sys.argv[0]