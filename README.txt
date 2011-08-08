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
* cx-freeze (to compile into a Linux executable)
  http://cx-freeze.sourceforge.net/


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

WINDOWS 
To create a Windows compatible binary, complete these steps:
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


LINUX
To create a Linux compatible binary, follow these steps:
-	Import your server's SSH host key into the "sshhostkeys/sshhostkeys" file. This can be easily
	done by making an initial connection using the included "plink_i386" or "plink_x86_64" binary
	and importing the hostkey:
		./plink_i386 <user>@<host>
		cat ~/.putty/sshhostkeys > sshhostkeys/sshhostkeys

-	Compile your new client using cx-freeze:
	cxfreeze main.py

-	This will create the needed files in the "dist" folder. You will then need to copy the following
	files/folders into the "dist" directory":
		sshhostkeys/
		plink_[i386][x86_64]
		x11vncserver_[i386][x86_64]
		xvnc4viewer_[i386][x86_64]

-	You can then crate a self-extracting binary using a third party utility or using the following steps:

	1. Copy the following scripts into their own files.
		decompress.sh
			#!/bin/bash
			export TMPDIR=`mktemp -d /tmp/.selfextract.XXXXXX`

			ARCHIVE=`awk '/^__ARCHIVE_BELOW__/ {print NR + 1; exit 0; }' $0`

			tail -n+$ARCHIVE $0 | tar xz -C $TMPDIR

			CDIR=`pwd`
			cd $TMPDIR
			./main

			cd $CDIR
			rm -rf $TMPDIR

			exit 0

			__ARCHIVE_BELOW__

		build.sh
			#!/bin/bash
			cd payload
			tar cf ../payload.tar ./*
			cd ..

			if [ -e "payload.tar" ]; then
			    gzip payload.tar

			    if [ -e "payload.tar.gz" ]; then
			        cat decompress.sh payload.tar.gz > showyourdesktop.bsx
			    else
			        echo "payload.tar.gz does not exist"
			        exit 1
			    fi
			else
			    echo "payload.tar does not exist"
			    exit 1
			fi

			echo "showyourdesktop.bsx created"
			exit 0

	2. Create the payload directory and copy the compiled files inside.
		mkdir payload
		cp -r client/dist/* ./payload

	3. Run the build script to create the self-extracting archive:
		chmod +x build.sh && ./build.sh

	You should now have a self-extracting binary with the ShowYourDesktop client included.
