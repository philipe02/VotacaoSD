import socket
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP
sock.bind((UDP_IP, UDP_PORT))
candidatos = {'Mônica': 0, 'Cebolinha': 0, 'Magali': 0}

while True:
    # recebe qual cliente está realizando a operação

    data, addr = sock.recvfrom(1024)
    mensagem = data.decode('utf-8')

    # caso seja urna inicia a votação

    if mensagem == "Urna":
        # envia uma mensagem de volta pro cliente indicando início da votação

        sock.sendto("Iniciando votação!".encode('utf-8'), addr)
        print("Votação sendo iniciada.")

        # recebe solicitação da lista de candidatos

        data, addr = sock.recvfrom(1024)
        mensagem = data.decode('utf-8')

        # envia lista de candidatos para o cliente

        listaCandidatos = pickle.dumps(list(candidatos.keys()))
        sock.sendto(listaCandidatos, addr)

        # recebe candidado a ser votado
        while True:
            data, addr = sock.recvfrom(1024)
            mensagem = data.decode('utf-8')

            if mensagem in candidatos:
                candidatos[mensagem] += 1

                # enviando confirmação que voto foi realizado para o cliente

                sock.sendto(("Voto em {} registrado!".format(
                    mensagem)).encode('utf-8'), addr)
                print("Voto com sucesso.")
                break
            else:
                sock.sendto(("{} não está na lista!".format(
                    mensagem)).encode('utf-8'), addr)
                print("Voto falhou.")

    if mensagem == "Apuração":
        # envia uma mensagem de volta pro cliente indicando início da votação

        sock.sendto("Iniciando apuração!".encode('utf-8'), addr)
        print("Apuração sendo iniciada.")

        # recebe solicitação da lista de candidatos

        data, addr = sock.recvfrom(1024)
        mensagem = data.decode('utf-8')

        # envia lista de candidatos para o cliente

        listaCandidatos = pickle.dumps(list(candidatos.keys()))
        sock.sendto(listaCandidatos, addr)

        # recebe solicitação de apuração de votos de um candidato individual ou todos
        while True:
            data, addr = sock.recvfrom(1024)
            mensagem = data.decode('utf-8')
            if mensagem == "Todos":
                # envia informações de todos os candidatos para o cliente

                sock.sendto(pickle.dumps(candidatos), addr)
                break
            elif mensagem in candidatos:
                # envia informação de um candidato

                sock.sendto(("{} recebeu {} votos!".format(
                    mensagem, candidatos[mensagem])).encode('utf-8'), addr)
                break
            else:
                sock.sendto(("Opção inválida!").encode('utf-8'), addr)
                print('Opção inválida!')
        data, addr = sock.recvfrom(1024)
        mensagem = data.decode('utf-8')
        print(mensagem)
