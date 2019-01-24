import sys, hashlib
# import vulnerable_key as vk
from sympy import *
import gmpy2

def sha1(n):
    h = hashlib.sha1()
    h.update(str(n).encode('utf-8'))
    return h.hexdigest()

def M_cf_expansion(n, d):
    e = []

    q = n // d
    r = n % d
    e.append(q)

    while r != 0:
        n, d = d, r
        q = n // d
        r = n % d
        e.append(q)

    return e

def test_get_cf_expansion():
    return cf_expansion(17993, 90581) == [0, 5, 29, 4, 1, 3, 2, 4, 3]

def M_convergents(e):
    n = [] # Nominators
    d = [] # Denominators

    for i in range(len(e)):
        if i == 0:
            ni = e[i]
            di = 1
        elif i == 1:
            ni = e[i]*e[i-1] + 1
            di = e[i]
        else: # i > 1
            ni = e[i]*n[i-1] + n[i-2]
            di = e[i]*d[i-1] + d[i-2]

        n.append(ni)
        d.append(di)
        yield (ni, di)

def decrypt_message(e,p,q,c):
    import gmpy2
    dp = gmpy2.invert(e, (p-1))
    dq = gmpy2.invert(e, (q-1))
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

    m = decrypt(int(c))
    print(m.decode())

def wieners_attack(e,N):
    # N, e, d, p, q = vk.create_keypair(1024)
    # print('[+] Generated an RSA keypair with a short private exponent.')
    # print('[+] For brevity, keypair components are crypto. hashed:')
    # print('[+] ++ SHA1(e):    ', sha1(e))
    # print('[+] -- SHA1(d):    ', sha1(d))
    # print('[+] ++ SHA1(N):    ', sha1(N))
    # print('[+] -- SHA1(p):    ', sha1(p))
    # print('[+] -- SHA1(q):    ', sha1(q))
    # print('[+] -- SHA1(phiN): ', sha1((p - 1)*(q - 1)))
    # print('[+] ------------------')

    cf_expansion = M_cf_expansion(e, N)
    convergents = M_convergents(cf_expansion)
    print('[+] Found the continued fractions expansion convergents of e/N.')

    print('[+] Iterating over convergents; '
            'Testing correctness through factorization.')
    print('[+] ...')
    for pk, pd in convergents: # pk - possible k, pd - possible d
        if pk == 0:
            continue;

        possible_phi = (e*pd - 1)//pk

        p = Symbol('p', integer=True)
        roots = solve(p**2 + (possible_phi - N - 1)*p + N, p)

        if len(roots) == 2:
            pp, pq = roots # pp - possible p, pq - possible q
            if pp*pq == N:
                print('[+] Factored N! :) derived keypair components:')
                # print('[+] ++ SHA1(e):    ', sha1(e))
                # print('[+] ++ SHA1(d):    ', sha1(pd))
                # print('[+] ++ SHA1(N):    ', sha1(N))
                # print('[+] ++ SHA1(p):    ', sha1(pp))
                # print('[+] ++ SHA1(q):    ', sha1(pq))
                # print('[+] ++ SHA1(phiN): ', sha1(possible_phi))
                print("[+] d: " + str(pd))
                print("[+] p: " + str(pp))
                print("[+] q: " + str(pq))
                return(pp,pq)

    print('[-] Wiener\'s Attack failed; Could not factor N')
    return None
def wieners_attack_d(e,N):
    # N, e, d, p, q = vk.create_keypair(1024)
    # print('[+] Generated an RSA keypair with a short private exponent.')
    # print('[+] For brevity, keypair components are crypto. hashed:')
    # print('[+] ++ SHA1(e):    ', sha1(e))
    # print('[+] -- SHA1(d):    ', sha1(d))
    # print('[+] ++ SHA1(N):    ', sha1(N))
    # print('[+] -- SHA1(p):    ', sha1(p))
    # print('[+] -- SHA1(q):    ', sha1(q))
    # print('[+] -- SHA1(phiN): ', sha1((p - 1)*(q - 1)))
    # print('[+] ------------------')

    cf_expansion = M_cf_expansion(e, N)
    convergents = M_convergents(cf_expansion)
    print('[+] Found the continued fractions expansion convergents of e/N.')

    print('[+] Iterating over convergents; '
            'Testing correctness through factorization.')
    print('[+] ...')
    for pk, pd in convergents: # pk - possible k, pd - possible d
        if pk == 0:
            continue;

        possible_phi = (e*pd - 1)//pk

        p = Symbol('p', integer=True)
        roots = solve(p**2 + (possible_phi - N - 1)*p + N, p)

        if len(roots) == 2:
            pp, pq = roots # pp - possible p, pq - possible q
            if pp*pq == N:
                print('[+] Factored N! :) derived keypair components:')
                # print('[+] ++ SHA1(e):    ', sha1(e))
                # print('[+] ++ SHA1(d):    ', sha1(pd))
                # print('[+] ++ SHA1(N):    ', sha1(N))
                # print('[+] ++ SHA1(p):    ', sha1(pp))
                # print('[+] ++ SHA1(q):    ', sha1(pq))
                # print('[+] ++ SHA1(phiN): ', sha1(possible_phi))
                print("[+] d: " + str(pd))
                print("[+] p: " + str(pp))
                print("[+] q: " + str(pq))
                return pd

    print('[-] Wiener\'s Attack failed; Could not factor N')
    return None
