#!/usr/bin/env python
##
##  vnc.py - ShowYourDesktop
##
##  Copyright (c) 2011 by William Edwards
##

# This module is used to interface with the VNC client and server using the subprocess module
# as well as interface with plink to create encrypted SSH tunnels. The credentials used to establish
# the tunnels is imported in from the server.py module.
#

from subprocess import Popen, PIPE, STARTUPINFO, STARTF_USESHOWWINDOW
import vnc_hash, os, server

# If running on a Windows-based system, set the startup info to hide any command prompt
# windows that would launch when executing a subprocess.
startupinfo = None
if os.name == 'nt':
    startupinfo = STARTUPINFO()
    startupinfo.dwFlags |= STARTF_USESHOWWINDOW

## View Remote Desktop
def client_tunnel(host=server.sshhost, port="5900", user=server.sshuser, sshport=server.sshport, password=server.sshpass):
    # Create the SSH tunnel to the gateway server
    command = ["plink.exe", "-C", "-N", "-L", "0.0.0.0:" + port + ":localhost:" + port, user + "@" + host, "-P", sshport, "-pw", password]
    return Popen(command, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

def client_connect(host="localhost", port="5900", password="secret"):
    # Convert the password to a 3DES VNC hash
    password = vnc_hash.get_vnc_hash(password)
    print password

    # Generate the connection profile
    profile = "[Connection]\n\
Host=" + host + ":" + port + "\n\
Password=" + password + "\n\
[Options]\n\
UseLocalCursor=1\n\
UseDesktopResize=1\n\
FullScreen=0\n\
FullColour=0\n\
LowColourLevel=2\n\
PreferredEncoding=hextile\n\
AutoSelect=1\n\
Shared=0\n\
SendPtrEvents=1\n\
SendKeyEvents=1\n\
SendCutText=1\n\
AcceptCutText=1\n\
DisableWinKeys=1\n\
Emulate3=0\n\
PointerEventInterval=0\n\
MenuKey=F8\n\
AutoReconnect=1"

    config = open("connect.vnc", "w")
    config.write(profile)

    # Connect to the remote VNC Server through the SSH Tunnel using the connection profile
    return Popen(["vncviewer.exe", "-config", "connect.vnc"], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

# *This function is depreciated and no longer used. It was used to listen for reverse VNC connections.
def client_listen(port="5500"):
    # Listen for VNC requests
    return Popen(["vncviewer.exe", "-listen", port], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

## Share Desktop
def server_tunnel(host=server.sshhost, port="5900", user=server.sshuser, sshport=server.sshport, password=server.sshpass):
    # Create the SSH tunnel to the gateway server
    command = ["plink.exe", "-C", "-N", "-R", "0.0.0.0:" + port + ":localhost:5900", user + "@" + host, "-P", sshport, "-pw", password]
    return Popen(command, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

def server_start(port="5900", password="secret"):
    # Convert the password to a 3DES VNC hash
	password = vnc_hash.get_vnc_hash(password)
	# Launch the VNC Server
	return Popen(["vncserver.exe", "PortNumber=" + port, "SecurityTypes=VncAuth", "Password=" + password], stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)

# *This function is depreciated and no longer used. It was used to make reverse VNC connections.
def server_connect(host="localhost", port="5900"):
    # Connect the remote viewer to the current desktop session
    command = ["vncserver.exe", "-connect", host + ":" + port]
    return Popen(command, stdout=PIPE, stderr=PIPE, startupinfo=startupinfo)