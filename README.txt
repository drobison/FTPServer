– Names and email addresses of all partners.
David Robison       davidrobison@csu.fullerton.edu
Chris Gudea         pulala@gmail.com

– The programming language you use (e.g. C++, Java, or Python)
Python

– How to execute your program.
Server:
    python Server.py <ServerPort>
    Example:
        python Server.py 50000
    
Client:
    python Client.py <ServerURL> <ServerPort>
    Note: When running locally, ServerURL is localhost
    Example:
        python Client.py localhost 50000
        
    Available client commands:
    
    ls
        Description - will list all files in the servers folder
        
    get <filename>
        Description - will attempt to get the file with name 'filename'
        from the ServerFolder.  If file does not exist, server will say so.
        If it does, the file is downloaded to the ClientFolder.  If the 
        filename already exists in the ClientFolder it will add an integer
        value to the filename until a spot is found to prevent overwritting files.
        
    put <filename>
        Description - will attempt to put the file with name 'filename'
        into the ServerFolder.  If file does not exist, client will say so.
        If it does, the file is uploaded to the ServerFolder.  If the 
        filename already exists in the ServerFolder it will add an integer
        value to the filename until a spot is found to prevent overwritting files.        

– Whether you implemented the extra credit.
    No

– Anything special about your submission that we should take note of.
    N/A
