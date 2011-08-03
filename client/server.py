#!/usr/bin/env python
##
##  server.py - ShowYourDesktop
##
##  Copyright (c) 2011 by William Edwards
##

# This module is used to communicate to the authentication server over https
# to request creating new sessions, closing existing sessions, and getting the
# port number for an existing session. It also contains the tunnel login information.
#

import urllib

# The server URL used for authentication
server_url = "https://<server-url>/check.php?"

# The SSH credentials used to establish the encrypted tunnels in vnc.py
sshhost = "yourhost.com"
sshuser = "remote"
sshpass = ""
sshport = "22"

def communicate(request, key):
    data = urllib.urlopen(server_url + 'key=' + key + '&request=' + request).read()
    
    return data

def view(key):
    port = communicate("view", key)
    
    if port != "":
        return port
    else:
        return False
    
def share(key):
    port = communicate("share", key)
    
    if port != "":
        return port
    else:
        return False
    
def close(key):
    result = communicate("close", key)
    
    if result == "Closed":
        return True
    else:
        return False
