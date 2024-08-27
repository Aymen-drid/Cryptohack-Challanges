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
chars=list(chars)
ans=[]

for i in range(15000):
    to_send = {"msg": "request"}
    json_send(to_send)
    received=json_recv()
    if received == {'error': 'Leaky ciphertext'}:
        continue
    tt=received['ciphertext']
    print (tt)
    print(i)
    ciphertext = base64.b64decode(tt)
    ans.append([chr(i) for i in ciphertext])
final=[]
temp=[]
for i in range(20):
    final.append([]);
for j in range(20):
    ex=''
    for k in ans:
        ex+=k[j]
    res=list(ex)
    s=''
    
    for i in chars:
        
        if   i not in res :
            print(i)  
            temp.append(i)
    final[j].append(temp)
    temp=[]
with open('final.txt', 'w') as file:
    for item in final:
        file.write(f"{item}\n")