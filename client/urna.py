import socket
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
CLIENTE = b"Urna"

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

# envia mensagem indicando a operação a ser realizada

sock.sendto(CLIENTE, (UDP_IP, UDP_PORT))

# recebe a resposta do servidor de inicio da operação

data, addr = sock.recvfrom(1024)
print(data.decode('utf-8'))
print("Lista de candidatos:")

# realiza a solicitação de lista de candidatos

sock.sendto(b"Candidatos", addr)

# recebe a lista de candidatos

data, addr = sock.recvfrom(1024)
candidatos = pickle.loads(data)
print(*candidatos)
while True:
    candidato = input("Em qual candidato deseja votar?\n")

# envia candidato a ser votado para o servidor

    sock.sendto(candidato.encode('utf-8'), addr)

    # recebe a confirmação do voto
    data, addr = sock.recvfrom(1024)
    mensagem = data.decode('utf-8')
    if 'não está na lista' in mensagem:
        print(mensagem)
    else:
        print(mensagem)
        break

sock.close()
