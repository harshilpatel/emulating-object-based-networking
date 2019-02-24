5306 - Spring 2019
Project - 1
Members: Patel Harshilkumar, Timmaiahgari Sreenidhi
Student ID: 1001717222, 1001721679
Last Names: Patel, Timmaiahgari

Assignments have been broken into directories
Assignment 1 is in /assignment_01
Assignment 3 & 4 have been combined in /assignment_0304

All assignment require 'python 2'

Environment requirements:
    - python2 as the default runtime for `python` command
    - optionally, running docker in the system

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
        b: Navigate into the projects directory.
        c: on terminal 1: `cd assignment_0304/server/ && python server.py`
        d: on termi nal 2: `cd assignment_0304/client/ && python client.py`
        e: the logs are streamed to the console & file -> *assignment_0304/server/server.log* && *assignment_0304/server/client.log*
        f: inspect the logs/console ouput to understand the behaviour

Assignment 4
    How to run:
        A. To run locally:
            a. Open two terminals and navigate to the project directory.
            b. Run `cd assignment_0304/server` and `cd assignment_0304/client` on the terminals.
            c. Run the following `./build.sh` and `./run.sh` on both terminals.
        B. To run remotely:
            a. Open two terminals and navigate to the project directory.
            b. Navigate to the directory -> `cd assignment_0304`
            c. Build the docker images for both client and server -> `./build.sh`
            d. Run the images in containers -> `./run.sh`
            e. Two containers with names *rpc-server* *rpc-client* should start and begin communicating as visibile earlier.
            f. The logs, if required are visible for running containers with `./logs.sh`
            g. Stop/Terminate the containers -> `./stop.sh`