from cryptography.hazmat.primitives import serialization

import math
import random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, inverse
from gmpy2 import is_prime
import sys
sys.path.insert(0,'../main/') 
from main.main import get_prime_factors,download_file
public_key = serialization.load_pem_public_key(open("key.pem", "rb").read())

c='249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28'
 # Adjust the path

# 공개 키 구성 요소 가져오기
public_numbers = public_key.public_numbers()
n=public_numbers.n
e=public_numbers.e
p,q=get_prime_factors(n)
print(p,q)
phi=(p-1)*(q-1)
d=pow(e,-1,phi)
key = RSA.construct((n, e, d))
cipher = PKCS1_OAEP.new(key)
message = cipher.decrypt(bytes.fromhex(hex(c)[2:]))
print(message)