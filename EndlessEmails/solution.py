#!/usr/bin/env python3
from itertools import combinations


def load_output():
    ret = {'n':[], 'c':[]}
    with open("output_0ef6d6343784e59e2f44f61d2d29896f.txt", 'rb') as fd:
        while True:
            line = fd.readline()
            if not line: break
            line = line.strip().decode()
            if not line: continue
            
            k, v = line.split('=')
            k = k.strip()
            if k == 'e':
                continue
            ret[k].append(int(v))

    return ret
from Crypto.Util.number import long_to_bytes, inverse
import gmpy2

def decrypt(grps, e):
    for grp in combinations(zip(grps['n'], grps['c']), e):
        N = 1
        for x in grp: N *= x[0]

        M = 0
        for x in grp:
            M += x[1]*inverse(N//x[0], x[0])*(N//x[0])
        M %= N
        M = gmpy2.mpz(M)
        m = gmpy2.root(M, e)
        if m**3==M:
            print(long_to_bytes(int(m)))
grps = load_output()
decrypt(grps, 3)