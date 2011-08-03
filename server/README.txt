
ShowYourDesktop Server
==============================================

Copyright (C) 2011 William Edwards  All Rights Reserved.

This software is distributed under the GNU General Public Licence as published
by the Free Software Foundation.  See the file LICENCE.TXT for the conditions
under which this software is made available.  ShowYourDesktop also contains 
code from other sources. 


Summary
===========================

The ShowYourDesktop server is a simple script that uses Apache, PHP, and MySQL 
to handle the creation of VNC sessions and manage SSH tunnels. It works by 
receiving a request from the ShowYourDesktop client via HTTP(s) with a VNC 
password and generates a random port that is available on the server to 
establish an SSH tunnel on. Once it generates the port, it inserts a record 
into the database with the password, port, and client information and returns 
the port number to the ShowYourDesktop client.

Once the client has received the port, it establishes a reverse SSH tunnel to 
the server over that port and waits for a connection. The person attempting to 
view the desktop also launches the client and it queries the server with the 
VNC password provided by the sharer. The server then looks up the port 
associated with the VNC password and returns it to the viewer so that it can 
establish a tunnel to the server and launch a VNC viewer session.


Requirements
===========================

* Apache/Lighttpd
* PHP
* MySQL
* SSHD


Installation
===========================

-	Create a database in MySQL to store the client sessions:
		mysql -u root -p -e "CREATE DATABASE showyourdesktop;"
	
-	Create a database user:
		mysql -u root -p -e "GRANT ALL ON showyourdesktop.* TO 'showyourdesktop'@'localhost' IDENTIFIED BY 'password';"
		
-	Create the client table structure using the db.sql file included:
		mysql -u root -p showyourdesktop < db.sql

-	Copy "check.php" and the "includes" folder to the desired web directory and modify the "includes/config.inc.php" 
	file to the desired configuration.
	
-	Enable the GatewayPorts option in your SSH configuration:
		echo "GatewayPorts yes" >> /etc/ssh/sshd_config
		
-	Create a new user to be used for the SSH tunnels:
		adduser remote
		passwd remote
		
-	Change the user's shell so it does not have login privileges:
		chsh -s /sbin/nologin remote