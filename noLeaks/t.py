from pwn import * # pip install pwntools
import json

r = remote('socket.cryptohack.org', 13370)
r.recvline()
def json_recv():
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_-+=}{[]:;'<>,.?/|\\`~"
ans=[]
while True:
    to_send = {"msg": "request"}
    json_send(to_send)
    received=json_recv()
    if received == {'error': 'Leaky ciphertext'}:
        print(received)
        continue
    tt=received['ciphertext']
    ciphertext = base64.b64decode(tt)
    print(ciphertext)
# with open('outputff.txt', 'w') as file:
#     for item in ans:
#         file.write(f"{item}\n")