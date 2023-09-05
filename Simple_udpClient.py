from socket import *
import CriptografiaRSA
import pickle

chaves = CriptografiaRSA.CriaChaves()

serverAddressPort = ("192.168.0.101", 20001)
clientSocket = socket(AF_INET, SOCK_DGRAM)
bufferSize = 4096

reqChaves = str.encode('Solicitando chave publica do server')
chavePrivada = chaves[0]
chavePublica = chaves[1]
message = None

reqDados = pickle.dumps((reqChaves, chavePublica))
clientSocket.sendto(reqDados, serverAddressPort)
dados, serverAddress = clientSocket.recvfrom(bufferSize)
serverMessage, serverChave = pickle.loads(dados)

print(serverMessage)
print('\nChave publica do server', serverChave)

while 1:
    message = input("\nInput message: ")

    if message == 'exit':
        break

    criptografaMensagem = CriptografiaRSA.encriptografa(message, serverChave)
    numBytes = (criptografaMensagem.bit_length() + 7) // 8
    resCriptografada = criptografaMensagem.to_bytes(numBytes, byteorder='big')

    clientSocket.sendto(resCriptografada, serverAddressPort)

    serverDados, clientAddress = clientSocket.recvfrom(bufferSize)
    mensagemCriptografada = int.from_bytes(serverDados, byteorder='big')
    mensagemDescriptografada = CriptografiaRSA.decriptografa(mensagemCriptografada, chavePrivada)

    print('\nCrypted Message from server:', mensagemCriptografada)
    print('\nDecrypted Message from server:', mensagemDescriptografada)