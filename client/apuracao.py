import socket
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
CLIENTE = "Apuração".encode('utf-8')

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

# enviar mensagem indicando a operação a ser realizada

sock.sendto(CLIENTE, (UDP_IP, UDP_PORT))

# recebe mensagem indicando início da operação

data, addr = sock.recvfrom(1024)
print(data.decode('utf-8'))
print("Lista de candidatos:")

# realiza solicitação da lista de candidatos

sock.sendto(b"Candidatos", addr)

# recebe a lista de candidatos

data, addr = sock.recvfrom(1024)
candidatos = pickle.loads(data)
print(*candidatos)
candidato = input(
    'Para exibir o voto de todos os candidatos digite "Todos", ou o nome do candidato para mostrar os votos individuais.\n')

# envia mensagem solicitando votos de um candidato específico ou todos

sock.sendto(candidato.encode('utf-8'), addr)

# recebe a informação dos votos

data, addr = sock.recvfrom(1024)
try:
    votos = pickle.loads(data)
    votosCandidatos = ""
    for i in votos:
        votosCandidatos += ('\n{} recebeu {} votos!'.format(i, votos[i]))
    print(votosCandidatos)
except:
    votos = data.decode('utf-8')
    print(votos)

# envia mensagem confirmando sucesso em apuração

sock.sendto('Apuração realizada com sucesso!'.encode('utf-8'), addr)
sock.close()
