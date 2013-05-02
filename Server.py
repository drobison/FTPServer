#!/usr/bin/python
# USAGE: python Server.py [serverPort]

import socket, time, string, sys, urlparse, os
from threading import *

# Directory where server files are stored
ServerFolder = os.getcwd() + "/ServerFolder"

from os import listdir
from os.path import isfile, join

# This port will be used for control.
controlPort = int(sys.argv[1])

# Initilize data connection
controlConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controlConnection.bind(('', controlPort))

# Wait for a client to connect.
controlConnection.listen(1)
print '[Control] FTP server started.  Listening for connections.'

# Accept incoming connection
controlConnection, maddr = controlConnection.accept()
print '[Control] Got connection from', maddr

# Begin accepting commands from client
while 1:
    data = controlConnection.recv(1024)
    if not data: break
    
    # Prompts quit.  Exit loop and close program.
    if data == "quit":
        controlConnection.send("Closing connection.")
        break
    
    # List all files in the Serverfolder    
    elif data == "ls":
        filelist = ""
        files = [ f for f in listdir(ServerFolder) if isfile(join(ServerFolder,f)) ]
        for f in files:
            filelist += f + "   "               
        controlConnection.send(filelist)
        
        #Display confirmation of action
        print "ls - SUCCESS"
    
    # Client is requesting to download a file    
    elif data[0:3] == "get":
        
        # Determine if file exists on server
        targetFile = data[4:]
        fileExists = False
        files = [ f for f in listdir(ServerFolder) if isfile(join(ServerFolder,f)) ]
        for f in files:
            if f == targetFile:
                fileExists = True
                break
        # If file exists, continue
        if fileExists:
            controlConnection.send("File exists.")
            
            # Wait for client to send the port for the data connection
            #print "Waiting for port."
            dataPort = controlConnection.recv(1024)
            #print '[Control] Data port is "%s"' % dataPort
            
            # Connect to the data connection
            dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dataConnection.connect((maddr[0], int(dataPort)))
            
            # Send file to client
            f = open(ServerFolder + '/' + targetFile, "rb")
            targetFileData = f.read()
            f.close()

            dataConnection.send(targetFileData)
            # Finished sending file        
            
            # Close data connection
            dataConnection.close()
            
            #Display confirmation of action
            print data + " - SUCCESS"            
            
        # If file does not exists, wait for the next command.
        else:
            controlConnection.send("File does not exist.")
            #Display failure of action
            print data + " - FAILURE - file did not exist."                      
    
    # Client is requesting to upload a file   
    elif data[0:3] == "put":
        targetFile = data[4:]    
        controlConnection.send("Waiting for port.")
        
        # Wait for client to send the port for the data connection
        #print "Waiting for port."
        dataPort = controlConnection.recv(1024)
        #print '[Control] Data port is "%s"' % dataPort
        
        # Connect to the data connection
        dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dataConnection.connect((maddr[0], int(dataPort)))
        
        # Used in case the file name needs to be changed.
        # Ex. file already exists.
        newFile = targetFile
        counter = 1
        
        # Determine if the filename already exists
        if os.path.isfile(ServerFolder + "/" + targetFile):        
            while os.path.isfile(ServerFolder + "/"+ str(counter) + targetFile):
                counter = counter + 1
            newFile = str(counter) + targetFile                  
        
        # Recieve file from client
        f = open( ServerFolder + "/" + newFile,"wb")
        while 1:
            data1 = dataConnection.recv(1024)
            if not data1: break
            f.write(data1)
        f.close()
        
        #Display confirmation of action
        print data + " - SUCCESS" 
        
    else:
        #Display error message
        print data + " - FAILURE - Unknown command."
        controlConnection.send("Unknown command..")

# Close connections    
controlConnection.close()
controlConnection.close()
