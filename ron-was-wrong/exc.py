from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import binascii
# msg = "???"
# with open('21.pem') as f:
#     key = RSA.importKey(f.read())
# cipher = PKCS1_OAEP.new(key)
# ciphertext = cipher.encrypt(msg)
# with open('21.ciphertext', 'w') as f:
#     f.write(ciphertext.hex())
from cryptography.hazmat.primitives import serialization
import sys
import requests
def get_prime_factors(n):
    # Step 1: Submit the number to FactorDB
    url = f"http://factordb.com/api?query={n}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Failed to connect to FactorDB")

    data = response.json()

    # Step 2: Check the status and retrieve factors
    if data['status'] not in ['FF', 'CF']:
        return ;

    factors = []
    for factor in data['factors']:
        prime, exponent = factor
        factors.extend([int(prime)] * int(exponent))
    
    # Assuming n is a product of two primes, p and q
    if len(factors) != 2:
        raise Exception(f"Unexpected number of factors for {n}: {factors}")

    return factors[0], factors[1]   
for i in range(1,51):
    public_key = serialization.load_pem_public_key(open(f"./keys/keys_and_messages/{i}.pem", "rb").read())
    with open(f"./keys/keys_and_messages/{i}.ciphertext", 'r') as file:
        hex_string = file.read().strip()
    c = binascii.unhexlify(hex_string)
    public_numbers = public_key.public_numbers()
    n=public_numbers.n
    e=public_numbers.e
    if not get_prime_factors(n):
        continue;
    p,q=get_prime_factors(n)
    print(p,q)
    phi=(p-1)*(q-1)
    d=pow(e,-1,phi)
    key = RSA.construct((n, e, d))
    cipher = PKCS1_OAEP.new(key)
    message = cipher.decrypt(c)
    print(message)