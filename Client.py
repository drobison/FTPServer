#!/usr/bin/python
# USAGE: python Client.py [serverPort]

import sys, socket, os


hostName = (sys.argv[1])
controlPort = int(sys.argv[2])

hostAddress = socket.gethostbyname(hostName)

# Directory where client files are stored
ClientFolder = os.getcwd() + "/ClientFolder"

controlConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controlConnection.connect((hostAddress, controlPort))

def GetInput():
    # Prompt to accept and send commands to server
    command = raw_input("ftp> ")
    
    # Before sending to server, validate if it is a put
    # that the file exists.
    if command[0:3] == "put":
        if not os.path.isfile(ClientFolder + "/" + command[4:] ):
            print "This file does not exist."
            command = GetInput()
    return command

# Loop to send commands to the server
while True:
           
    # Get user command
    command = GetInput()
    
    # Send command to server
    controlConnection.send(command)
    
    # Receive response from server
    serverResponse = controlConnection.recv(1024)
    if not serverResponse: break
    
    #print '[Control] Server says "%s"' % serverResponse
    if command == "ls":
        print serverResponse
    
    # Interpret server response and act accordingly.
    
    # Case where request to get a file and it exists
    # if file does not exists nothing happens.  Error is displayed.  
    if command[0:3] == "get" and serverResponse == "File exists." :
        
        targetFile = command[4:]
        
        # Initilize data connection
        dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        dataConnection.bind(('', 0))
        dataConnection.listen(1)
        dataPort = dataConnection.getsockname()[1]
        
        # Send data connection port to server over control connection
        # so server can connect.
        controlConnection.send(str(dataPort))
        
        # Wait for server to connect.
        dataConnection, maddr = dataConnection.accept()
        #print '[Control] Got connection from', maddr
        
        # Used in case the file name needs to be changed.
        # Ex. file already exists.
        newFile = targetFile
        counter = 1
        
        # Determine if the filename already exists
        if os.path.isfile(ClientFolder + "/" + targetFile):        
            while os.path.isfile(ClientFolder + "/"+ str(counter) + targetFile):
                counter = counter + 1
            newFile = str(counter) + targetFile            
        
        # Recieve file from server
        f = open(ClientFolder + "/" + newFile,"wb")
        while 1:
            data = dataConnection.recv(1024)
            if not data: break
            f.write(data)
        f.close()        
        
        # Close data connection
        dataConnection.close()
        
        # Print details
        byteSize = os.path.getsize(ClientFolder + "/" + newFile)
        print "Downloaded - " + targetFile + " (" + str(byteSize) + " bytes)"
        
    # Case where request to upload a file         
    if command[0:3] == "put":
        targetFile = command[4:] 
        
        # Initilize data connection
        dataConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        dataConnection.bind(('', 0))
        dataConnection.listen(1)
        dataPort = dataConnection.getsockname()[1]
        
        # Send data connection port to server over control connection
        # so server can connect.
        controlConnection.send(str(dataPort))
        
        # Wait for server to connect.
        dataConnection, maddr = dataConnection.accept()
        #print '[Control] Got connection from', maddr
        
        # Send file to server
        f = open(ClientFolder + '/' + targetFile, "rb")
        targetFileData = f.read()
        f.close()
        
        dataConnection.send(targetFileData)
        
        # Close data connection
        dataConnection.close()
        
        # Print details
        byteSize = os.path.getsize(ClientFolder + "/" + targetFile)
        print "Uploaded - " + targetFile + " (" + str(byteSize) + " bytes)"                
        
    # If command is quit, exit loop and close program.                
    if command == "quit":
        break        
        
# Close control connection
controlConnection.close()
