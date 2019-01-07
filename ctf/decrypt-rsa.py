# camsctf-2016 one zero zero
# RSA decryption using the Chinese Remainder Theorem
filename = "RSA.txt"
file = open(filename)
lines = file.readlines()
for i in range(len(lines)):
    lines[i] = lines[i].replace("\n","").split(": ")[1]

#C:0
#P:1
#Q:2
#DP:3
#DQ:4



p = int(lines[1])
q = int(lines[2])
e = 65537

import gmpy2
dp = int(lines[3])
dq = int(lines[4])
qinv = gmpy2.invert(q, p) # 0xaaa636b836bd372367cdf086c55ad88cd7c61e751

def decrypt(c):
  m1 = pow(c, dp, p)
  m2 = pow(c, dq, q)
  h = (qinv * (m1 - m2)) % p
  m = m2 + h * q
  return long_to_bytes(m)

import sys
import os
# from a import long_to_bytes
# from crypto.pct_warnings import PowmInsecureWarning, GetRandomNumber_DeprecationWarning
from Crypto.Util.number import long_to_bytes

m = decrypt(int(lines[0]))
print(m.decode())
