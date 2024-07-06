import sys
from pwn import *
from Crypto.Util.number import bytes_to_long, long_to_bytes
import json
r=remote("socket.cryptohack.org","13374")
def json_recv():
    line = r.readline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)
print(r.readline())
pub={"option":"get_pubkey"}
json_send(pub)
print("public",json_recv())
sec={"option":"get_secret"}
json_send(sec)
a=json_recv()
print("sec",a)
sign={"option":"sign","msg":a["secret"]}
json_send(sign)
b=json_recv()
print("sign",b["signature"])
print(bytes.fromhex(b["signature"][2:]))