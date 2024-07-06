FLAG = b'crypto{hhhhhhhhh}'
from Crypto.Util.number import bytes_to_long, getPrime
m = bytes_to_long(FLAG)
print(m)
