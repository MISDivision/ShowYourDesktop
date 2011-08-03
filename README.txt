
ShowYourDesktop Client
==============================================

Copyright (C) 2011 William Edwards  All Rights Reserved.

This software is distributed under the GNU General Public Licence as published
by the Free Software Foundation.  See the file LICENCE.TXT for the conditions
under which this software is made available.  ShowYourDesktop also contains code from other
sources. 


Summary
===========================

The ShowYourDesktop client is a small application written in Python used to share your 
desktop with anyone in the world. It does this by creating a reverse SSH tunnel to an
intermediary server for NAT traversal and encryption and tunneling VNC traffic using
RealVNC. The server component is required to establish SSH tunnels for both the sharer
and the viewer as well as handle the ports that are currently in use by existing sessions.

You can create your custom deployment using your own SSH server by installing the server
components and modifying the ShowYourDesktop client to use your server details. This can
be easily done by changing the server variables in "server.py" and importing your server's
host key into the "sshhostkeys" directory.


Requirements
===========================

* Py2exe (to compile into a Windows executable)
  http://sourceforge.net/projects/py2exe/files/


Custom Deployment
===========================

You can create your own custom deployment using your own server by following these steps:

- 	Install the server components as dictated in "server/README.txt".

- 	Modify "server.py" to include your server's details. The variables you will need to modify
	are:
		server_url
		sshhost
		sshuser
		sshpass
		sshport

-	Import your server's SSH host key into the "sshhostkeys" directory. This can be easily done
	by making a connection using the included "plink.exe". Note that regular versions of plink
	will store the host key in the registry thus making it not portable and will fail to connect
	on desktops that do not have the key in their registry:
		plink.exe <user>@<host>
		
-	Compile your new client using py2exe:
		python setup.py install
		python setup.py py2exe
		
-	This will create the needed files in the "dist" folder. In order for the newly compiled
	ShowYourDesktop executable to work, you will need to copy the following files/folders to the "dist"
	folder:
		sshhostkeys/
		logmessages.dll
		plink.exe
		showyourdesktop.ico
		vncserver.exe
		vncviewer.exe
		wm_hooks.dll

-	You can then use a 3rd party utility such as 7zip or WinRAR to create a self-extracting archive 
	that will extract the archive to a temporary directory and automatically launch "main.exe".