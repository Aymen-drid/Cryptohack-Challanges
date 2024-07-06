#!/usr/bin/env python3
from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
from utils import listener
import json
r=remote('socket.cryptohack.org','13374')
def json_recv(r):
    line = r.readline()
    return json.loads(line.decode())

def json_send(hsh,r):
    request = json.dumps(hsh).encode()
    r.sendline(request)




class Challenge():
    def __init__(self):
        self.before_input = "Welcome to my signing server. You can get_pubkey, get_secret, or sign.\n"

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_pubkey':
            return {"N": hex(N), "e": hex(E) }

        elif your_input['option'] == 'get_secret':
            secret = bytes_to_long(SECRET_MESSAGE)
            return {"secret": hex(pow(secret, E, N)) }

        elif your_input['option'] == 'sign':
            msg = int(your_input['msg'], 16)
            return {"signature": hex(pow(msg, D, N)) }

        else:
            return {"error": "Invalid option"}

listener.start_server(port=13374)
