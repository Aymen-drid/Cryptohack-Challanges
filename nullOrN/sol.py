import sys
sys.path.insert(0,'../')
from utils.main import utils
from sympy import mod_inverse, cbrt
from Crypto.Util.number  import long_to_bytes,inverse
M=cbrt(M);
print(long_to_bytes(int(M)))