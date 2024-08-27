import time
import hashlib
from Crypto.Util.number import long_to_bytes
current_time = time.time()
print(current_time)
def decrypt(b,current_time):
    key = long_to_bytes(current_time)
    key= hashlib.sha256(key).digest()
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([b[i] ^ key[i]])
    return ciphertext
current_time=int(1724620065.111694)
v=current_time
b="6a6edd4405bb83a2bfdbf42b76a5c328153aaf4fb4bb8f093a3651ab"
b=bytes.fromhex(b)
for i in range(30):
    v+=1;
    print (decrypt(b,v))