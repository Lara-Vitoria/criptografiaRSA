from socket import *
import CriptografiaRSA
import pickle

chaves = CriptografiaRSA.CriaChaves()

serverIP = ""
serverPort = 8888
bufferSize = 4096
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((serverIP, serverPort))

print ("UDP server\n")

msgFromServer = "Hello UDP Client"
chaveCliente = None
mensagemDescriptografada = None

while chaveCliente == None:
    message, clientAddress = serverSocket.recvfrom(bufferSize)
    message, chavePublica = pickle.loads(message)

    clientIP = f"Client IP: {clientAddress}"
    print('Received from Client: ', message)

    res = pickle.dumps((msgFromServer, chaves[1]))
    serverSocket.sendto(res, clientAddress)
    chaveCliente = chavePublica

while chaveCliente != None and mensagemDescriptografada != 'exit':
    dados, clientAddress = serverSocket.recvfrom(bufferSize)

    mensagemCriptografada = int.from_bytes(dados, byteorder='big')
    mensagemDescriptografada = CriptografiaRSA.decriptografa(mensagemCriptografada, chaves[0])

    print('\nMensagem criptografada:', mensagemCriptografada)
    print('\nMensagem descriptografada:', mensagemDescriptografada)

    criptografa = CriptografiaRSA.encriptografa(msgFromServer, chaveCliente)
    numBytes = (criptografa.bit_length() + 7) // 8
    resCriptografada = criptografa.to_bytes(numBytes, byteorder='big')

    serverSocket.sendto(resCriptografada, clientAddress)
