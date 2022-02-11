# LAN-Caster

The goal of LAN-Caster is to provide an easy-to-use code base (game engine) for 
developing 2D multiplayer online games.
LAN-Caster originally only supported Local Area Networks (LAN) but now also 
has experimental support for Wide Area Networks (WAN), also known as the Internet.

# How To Run


## Prerequisites

The following items need to be installed to run LAN-Caster.

### Python 3.6 or higher

LAN-Caster uses Python 3.6 or higher (tested on python 3.7.3) which can be installed from [https://www.python.org/downloads/](https://www.python.org/downloads/).

> If multiple versions of python are installed, ensure you are running python 3.6+, not python 3.5 or python 2. The examples in this README use the "python" command assuming python 3.6+ is the default. The command "python3" (Linux) or "py -3" (Windows) may be required to force the correct version.

### Python Modules
LAN-Caster requires two added python moduels to be installed.
1) Pygame is used by the clients to open the game window, render graphics, and collect player input. 
2) Msgpack is used to encode and decode messages between the server and clients.

To install pygame and msgpack on Windows use:
```
py -3 -m pip install pygame msgpack-python
```

To install pygame and msgpack on Linux use:
```
pip3 install pygame msgpack-python
```

Note, if a computer is only running the LAN-Caster server then the pygame module is not required.

### LAN-Caster Code

The LAN-Caster code can be cloned with git from: [https://github.com/dbakewel/lan-caster.git](https://github.com/dbakewel/lan-caster.git) or downloaded in zip form from: [https://github.com/dbakewel/lan-caster/archive/master.zip](https://github.com/dbakewel/lan-caster/archive/master.zip)


## Running the Demo

On windows, **double click "run-demo.bat"** in the root of the LAN-Caster directory.

> If this does not work, open a command window (cmd), cd into the directory containing run-demo.bat and type "rundemo.bat".

The rundemo script will start 4 processes on the local computer: 1 server and 3 clients. Normally, each client would run on a different computer and be used by a different player. The run-demo.bat allows one user to move back and forth between all 3 clients and play all the players at once.

## Running on Separate Computers

By default LAN-Caster only listens on localhost 127.0.0.1 which does not allow messages to be sent or received between computers. To listen on all network interfaces, and allow messages from other computers, use ```-ip 0.0.0.0``` on server and clients. 

> Note, if you want to run LAN-Caster across a network then the ports you choose must be open in the OS and network firewalls for two way UDP traffic. By default, LAN-Caster uses ports of  20000 and above but any available UDP ports can be used.

For example:

Assuming:
*   computer 1 has IP address of 192.168.1.10
*   computer 2 has IP address of 192.168.1.11
*   computer 3 has IP address of 192.168.1.22
*   computer 4 has IP address of 192.168.1.33

The server can be run on computer 1 with: 

```
py -3 src/startserver.py -game "demo" -ip 0.0.0.0
```

The server will listen on 127.0.0.1 and 192.168.1.10

A client can be run on Computer 2, 3, and 4 with: 

```
py -3 src/startclient.py -game "demo" -sip 192.168.1.10
```

## Command Line Help

The server and client allow some customization with command line switches. Use the **-h** switch to display help. For example:

```
D:\lan-caster>py src\startserver.py -h
usage: startserver.py [-h] [-game dir] [-register name] [-ch hostname]
                      [-cp port] [-sip ipaddr] [-sp port] [-fps fps]
                      [-busy secs] [-pause secs] [-test] [-verbose] [-debug]

optional arguments:
  -h, --help      show this help message and exit
  -game dir       Directory to load game from (default: demo)
  -register name  Experimental: Register with connector as name (False == do
                  not register) (default: False)
  -ch hostname    Experimental: Connector hostname or IP address (default:
                  lan-caster.net)
  -cp port        Experimental: Connector port number (default: 20000)
  -sip ipaddr     Server IP address (default: 0.0.0.0)
  -sp port        Server port number (default: 20001)
  -fps fps        Target frames per second (aka steps/sec) (default: 30)
  -busy secs      Seconds between logging percent busy (default: 60)
  -pause secs     Duration to pause in seconds before starting server (for
                  testing) (default: 0)
  -test           Start server in test mode (default: False)
  -verbose        Print VERBOSE level log messages (default: False)
  -debug          Print DEBUG level log messages (includes -verbose) (default:
                  False)
```

```
D:\lan-caster>py src\startclient.py -h
pygame 2.1.2 (SDL 2.0.16, Python 3.6.7)
Hello from the pygame community. https://www.pygame.org/contribute.html
usage: startclient.py [-h] [-game dir] [-player name] [-connect name]
                      [-ch hostname] [-cp port] [-sip ipaddr] [-sp port]
                      [-ip ipaddr] [-p port] [-width width] [-height height]
                      [-fps fps] [-busy secs] [-pause secs] [-verbose]
                      [-debug]

optional arguments:
  -h, --help      show this help message and exit
  -game dir       Directory to load game from (default: demo)
  -player name    Player's name to display in game (default: anonymous)
  -connect name   Experimental: Connect to server using connector. "name" must
                  match server's "-register name" (if False then use -sip and
                  -sp to connect to server) (default: False)
  -ch hostname    Experimental: Connector hostname or IP address (default:
                  lan-caster.net)
  -cp port        Experimental: Connector port number (default: 20000)
  -sip ipaddr     Server IP address (default: 127.0.0.1)
  -sp port        Server port number (default: 20001)
  -ip ipaddr      Client IP address (default: 0.0.0.0)
  -p port         Client port number (client will search for an open port
                  starting with this number.) (default: 20002)
  -width width    Window width (default: 640)
  -height height  Window height (default: 640)
  -fps fps        Target frames per second (default: 30)
  -busy secs      Seconds between logging percent busy (default: 60)
  -pause secs     Duration to pause in seconds before starting client (for
                  testing) (default: 0)
  -verbose        Print VERBOSE level log messages (default: False)
  -debug          Print DEBUG level log messages (includes -verbose) (default:
                  False)
```

---

## Tutorials

The following videos provide an overview of how to use LAN-Caster to build your own game. Also, see comments in the
LAN-Caster code and docs folder.

videos coming soon...

## Additional Information

### Install Connector Systemd Service on Linux (Experimental)
Assuming lan-caster has been installed under a linux user name 'lan-caster' with home dir '/home/lan-caster'
```
cd /home/lan-caster/lan-caster/systemd
sudo cp connector.service /lib/systemd/system/
sudo systemctl enable $f
```

