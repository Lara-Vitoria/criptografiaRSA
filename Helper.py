import math
import secrets

def criaN(p , q):
    return p * q

def criaFiN(p, q):
    return (p - 1) * (q - 1)

def criaE(fiN):
    while True:
        e = secrets.randbelow(fiN - 1) + 1
        if math.gcd(e, fiN) == 1:
            return e

def criaD(e, fiN):
    m0, x0, x1 = fiN, 0, 1
    while e > 1: 
        q = e // fiN
        fiN, e = e % fiN, fiN
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1


def criaChavePublica(fiN):
    for i in range(1, 4096):
        if 0 != fiN % i:
            return round(i)
        
def criaChavePrivada(fiN, chavePublica):
    for i in range(0, 4096):
        d = 1 + (i * fiN)
        chave = d / chavePublica
        if 0 == d % chavePublica:
            return round(chave)