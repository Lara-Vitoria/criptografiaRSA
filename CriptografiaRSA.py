import Helper
import threading
from Crypto.Util.number import getPrime

numBits = 4096

class CriaNumero:
    def __init__(self):
        self.resultado = None

    def criaNumero(self):
        self.resultado = getPrime(numBits)

    def getRsultado(self):
        return self.resultado 

def worker(obj):
    obj.criaNumero()

def CriaChaves():
    num = CriaNumero()

    threadP    = threading.Thread(target=worker, args=(num,))
    threadP.start()

    q = getPrime(numBits)

    threadP.join()

    p = num.getRsultado()

    n = Helper.criaN(p, q)
    fiN = Helper.criaFiN(p, q)
    e = Helper.criaE(fiN)
    d = Helper.criaD(e, fiN)

    chavePublica = (e, n)
    chavePrivada = (d, n)
    chaves = [chavePrivada, chavePublica]

    return chaves

def decriptografa(mensagem, chave):
    return int.to_bytes( pow(mensagem, chave[0], chave[1]), length=(mensagem.bit_length() // 8) + 1, byteorder='big').decode()

def encriptografa(mensagem, chave):
    return pow(int.from_bytes(mensagem.encode(), byteorder='big'), chave[0], chave[1])