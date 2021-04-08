import socket

UDP_IP = "127.0.0.1"
UDP_PORT = 5005 
sock = socket.socket(socket.AF_INET, # Internet 
socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
candidatos= {'Mônica': 0, 'Cebolinha': 0, 'Magali': 0}

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  mensagem = data.decode('utf-8')
  sock.sendto(b"Mensagem recebida!", addr)

  if mensagem == "Candidatos":
    for i in candidatos:
      print(i+ " ")

  if "Votos " in mensagem:
    candidato = mensagem.split()[1]
    print("%s possui %d votos!" % (candidato, candidatos[candidato]))
  if mensagem in candidatos:
    candidatos[mensagem]+=1
    print("Voto em %s registrado!" % mensagem)
  if data==b"close":
    sock.close()
    break