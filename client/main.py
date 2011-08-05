#!/usr/bin/env python
##
##  main.py - ShowYourDesktop
##
##  Copyright (c) 2011 by William Edwards
##

# This module is used as the primary graphical user interface to create
# reverse SSH tunnel sessions, start the VNC server, and view an existing
# VNC server session by querying the authentication server.
#

from Tkinter import *
import vnc, time, os, random, string, tksimpledialog, server

# Create a list for any subprocesses so we can loop through and kill all child processes
processes = []
shared = False

class App:

    # Creates the main tkinter window
    def __init__(self, master):

        self.frame = Frame(master)
        self.frame.pack()
        
        self.password = StringVar()
        self.password.set("")
        self.textbox = Entry(self.frame, relief=SUNKEN, textvar=self.password, state="readonly", takefocus=True, width=15)
        self.textbox.pack(side=BOTTOM, pady=15, padx=5)
        
        self.status = Label(master, text="", bd=1, relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
        
        self.share_desktop = Button(self.frame, text="Share My Desktop", command=self.share_desktop)
        self.share_desktop.pack(side=LEFT, pady=15, padx=5)

        self.view_desktop = Button(self.frame, text="View Remote Desktop", command=self.view_desktop)
        self.view_desktop.pack(side=LEFT, pady=15, padx=5)
        
        self.button = Button(self.frame, text="Quit", command=self.frame.quit)
        self.button.pack(side=LEFT, pady=15, padx=5)

    def view_desktop(self):
        global processes
	
	    # Get the password from the user
        password = tksimpledialog.askstring('Authentication', 'Password:')
        
        # If the password is blank or the user presses cancel, break out of the function
        if (password == "" or password == None):
            return None
        
        try:
            # Connect to the server to query the correct port number
            port = server.view(password.strip())
        except:
            self.status.config(text="Error connecting to server.")
            self.status.update_idletasks()
            return None
        
        # If no port was returned, break out of the function.
        if not port:
            self.status.config(text="Requested session not found.")
            self.status.update_idletasks()
            return None

        # Disable the view desktop button
        self.view_desktop.config(state=DISABLED)
        self.share_desktop.config(state=DISABLED)
        
        self.status.config(text="Creating Secure Tunnel...")
        self.status.update_idletasks()
        ## Append the process object to the list of processes so we can end all child processes upon exit
        processes.append(vnc.client_tunnel(port=port)) 
        time.sleep(2)

        # Connect to the remote session
        self.status.config(text="Connecting to remote desktop...")
        self.status.update_idletasks()
        processes.append(vnc.client_connect(port=port, password=password))
        #self.status.config(text="Waiting for client desktop to be shared...")
        #self.status.update_idletasks()
        #processes.append(vnc.client_listen(port=port))
        
    def share_desktop(self):
        global processes
        global shared

        # Update status bar
        self.status.config(text="Generating password...")
        self.status.update_idletasks()

		# Generate a random 10 digit password
        password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))
        
        try:
            # Fetch the port from the server
            port = server.share(password)
        except:
            self.status.config(text="Error connecting to server.")
            self.status.update_idletasks()
            return None            
        
        # If the server returned false, break out of the function
        if not port:
            self.status.config(text="Unable to create session. Please try again.")
            self.status.update_idletasks()
            return None

        # Set shared to the password so we can close out the session
        shared = password

        # Show the port in the password field
        self.password.set(password)

        # Disable the share desktop button
        self.share_desktop.config(state=DISABLED)
        self.view_desktop.config(state=DISABLED)

        # Create the secure tunnel
        self.status.config(text="Creating Secure Tunnel...")
        self.status.update_idletasks()
        # Append the process object to the list of processes so we can end all child processes upon exit
        processes.append(vnc.server_tunnel(port=port)) 
        time.sleep(2)
        
        # Start the VNC Server
        self.status.config(text="Starting VNC Server...")
        self.status.update_idletasks()
        processes.append(vnc.server_start(password=password))
        time.sleep(2)

        self.status.config(text="Waiting for remote client...")
        self.status.update_idletasks()
        #vncprocess = vnc.server_connect(port=port) # Attempt to connect to the VNC viewer
        #output = vncprocess.communicate() # Retrieve the command output
        #print output
        #processes.append(vncprocess) # Append to the list of processes

root = Tk()
root.title("ShowYourDesktop")
if os.name == "nt": root.wm_iconbitmap("showyourdesktop.ico")
app = App(root)
root.mainloop()

# End any extra processes
for process in processes:
    try:
        print "Killed", process.pid
        process.kill()
    except:
        print "Unexpected error:", sys.exc_info()[0]

# Remove the session from the server's database if it was shared.
if shared:
    server.close(shared)
