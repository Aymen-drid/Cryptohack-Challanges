#!/usr/bin/env python3
import sys
from Crypto.Util.number import bytes_to_long, long_to_bytes
from sage.all import *
import json
import math
sys.path.insert(0,'../main/') 
from main.main import decrypt
from pwn import * # pip install pwntools
import json
import requests
from Crypto.Util.number import long_to_bytes
from sympy.ntheory.modular import crt
from sympy import integer_nthroot
from sympy.ntheory.modular import crt
def recover_message(ciphertexts, moduli, e):
    # Combine the congruences using the Chinese Remainder Theorem
    m_e, _ = crt(moduli, ciphertexts)
    
    # Calculate the e-th root of m^e to find m
    m, exact = integer_nthroot(m_e, e)
    
    if not exact:
        raise ValueError("Failed to recover the message. Ensure enough ciphertexts and correct e.")
    
    return m
HOST = "socket.cryptohack.org"
PORT = 13386
# r = remote(HOST, PORT)
def json_recv(r):
    line = r.readline()
    return json.loads(line.decode())

def json_send(hsh,r):
    request = json.dumps(hsh).encode()
    r.sendline(request)

