# Hermes - A terminal based chat system.
Hermes is terminal based messenger app utilising sockets and threading allowing users to have fun conversations. 

## Context
This project was developed as a fun project over my summer break, so that anyone at my university can have conversations over the Uni's network. 
Working on Hermes has helped me learn more about:
    - Communication Systems
    - Network Architecture
    - Socket Programming in Python


The naming was a pretty obvious choice. Hermes, the messenger of the Olympic gods.

## How to use Hermes
There are two main programs: 
    1. The Server: server.py
    2. The Client: client.py
### The Server
1. Run the ```server.py```
    ```cmd
    $ python server.py
    ```
2. The machine's name and ip address will be displayed. The ip address should be shared with others who want to connect to the chat.
3. You might be prompted to Allow Network Access Permissions for Python3. Click on Allow.
4. The server is now up and running.

### The Client
1. Run the ```client.py```
    ```cmd
    $ python server.py
    ```
2. Enter the server ip address. 
3. Select your nickname. (This will be displayed to everyone in the chat.)
4. You are now connected to the chat.