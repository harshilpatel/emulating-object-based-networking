Project - 1
Members: __ __
Student ID: __ __
Last Names: __ __

Assignments have been broken into directories
Assignment 1 is in /assignment_01
Assignment 3 & 4 have been combined in /assignment_0304

All assignment require 'python 2'

Assignment 1
    How to run:
        a. Open 2 terminals. The server & client require their individual terminals to read the logs & understand the flow
        b. on terminal 1: `cd assignment_01/ && python server.py`
        c. on terminal 2: `cd assignment_01/ && python client.py`
        d. both server and client have thier respective static dirs -> "static_server" & "static_client"
        e. the client has been designed to accept user inputs if required, you may use enter your choice on terminal 2 & notice the changes in the static dirs [pending]
    
    The workflow:
        a. on upload: file is uploaded from static_client to static_server via udp packets.
        b. on rename: file is renamed using python's system api's
        c. on download: similar to upload, the file is broken depending on the buffer size, and sent to client as packets.
        d. on delete: file is deleted using python's systems api's

Assignment 3
    How to run:
        a: Open 2 terminals.
        b. on terminal 1: `cd assignment_0304/server/ && python server.py`
        c. on terminal 2: `cd assignment_0304/client/ && python client.py`
        d. the logs are streamed to the console & file -> *assignment_0304/server/server.log* && *assignment_0304/server/client.log*

Assignment 4
    How to run:
        a. Navigate the directory -> `cd assignment_0304`
        b. Build the docker images `./build.sh`
        c. Run the images in containers -> `./run.sh`
        d. Two containers with names *rpc-server* *rpc-client* should start and begin communicating as visibile earlier.
        e. The logs, if required are visible for running containers with `./logs.sh`
        f. Stop the containers -> `./stop.sh`