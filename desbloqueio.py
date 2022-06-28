
#pyinstaller --onefile --noupx test.py
#!/bin/python
import pip

try:
    import telnetlib
    import re
    import numpy as np
    import sys
    from time import sleep       
except ImportError:
    pip.main(['install', 'telnetlib'])
    pip.main(['install', 're'])
    pip.main(['install', 'numpy'])
    pip.main(['install', 'sys'])
    pip.main(['install', 'time'])
    import telnetlib
    import re
    import numpy as np
    import sys
    from time import sleep

ip = sys.argv[1]
porta = 23
login = sys.argv[2]
senha = sys.argv[3]

# CRIA CONEXÃO TELNET
telnet = telnetlib.Telnet(ip, porta, timeout=5)

# REALIZA LOGIN NA OLT
telnet.read_until(b"Login: ")
telnet.write(login.encode('ascii') + b"\n")
telnet.read_until(b"Password: ")
telnet.write(senha.encode('ascii') + b"\n")
# ENTRA EM MODO ADMINISTRATIVO
telnet.write(b"enable\n")
telnet.read_until(b"Password: ")
telnet.write(senha.encode('ascii') + b"\n")




telnet.write(b"show version\n") #exibe descrição e versao de todas as placas
sleep(4)
saida = telnet.read_very_eager().decode('utf-8') #decode novamente para string padrão
print(saida)
telnet.close()
texto = saida
texto = re.sub(' +', ' ', texto)


texto = re.findall(r'.* [1-9].*',texto)#encontra somente linhas com ids disponiveis
#texto = re.sub('.*----*.',"",texto)
qtd = len(texto)#conta qtd de elementos
matriz_linha = np.array([])
linha = 0
coluna = 0

for linha in range(qtd):
    matriz_linha = texto[linha].split(" ") #separa a string toda usando espaços como parametro e insere num array cada split
    if (matriz_linha[2]=="GC8B") or (matriz_linha[2]=="GCOB"):
        print(matriz_linha[3])
        telnet = telnetlib.Telnet(ip, porta, timeout=5)

        # REALIZA LOGIN NA OLT
        telnet.read_until(b"Login: ")
        telnet.write(login.encode('ascii') + b"\n")
        telnet.read_until(b"Password: ")
        telnet.write(senha.encode('ascii') + b"\n")
        # ENTRA EM MODO ADMINISTRATIVO
        telnet.write(b"enable\n")
        telnet.read_until(b"Password: ")
        telnet.write(senha.encode('ascii') + b"\n")
        # REALIZA CONEXÃO TELNET COM O CARD

        if('S1B' in matriz_linha[3]) or ('T1A' in matriz_linha[3]):


            telnet.write(b"cd service\n")
            sleep(4)
            slot = int(matriz_linha[1])
            telnet_slot = f"telnet slot {slot}"
            print("Conectando via telnet...")
            telnet.write(telnet_slot.encode('ascii') + b"\n")
            sleep(5)
            #ENVIA COMANDO DE LIBERAR TERCEIROS
            print("Configurando desbloqueio...")
            telnet.write(b"debug\n")
            sleep(1)
            telnet.write(b"set policy param pon-interconnect-switch enable logicsn-auth-mode ctc\n")
            sleep(1)
            telnet.write(b'show policy params\n')
            sleep(1)
            telnet.write(b"exit\n")
            print("Placa ", matriz_linha[1], " Desbloqueada")
            telnet.close()
            sleep(4)
            #print("Script Executado Placa: ",matriz_linha[2])
        elif('R1A' in matriz_linha[3]) or ('R1B' in matriz_linha[3]) or ('R1C' in matriz_linha[3]):
            telnet.write(b"cd service\n")
            sleep(1)
            slot = int(matriz_linha[1])
            telnet_slot = f"telnet slot {slot}"
            print("Conectando via telnet...")
            telnet.write(telnet_slot.encode('ascii') + b"\n")
            sleep(5)
            # telnet.read_until(b"GCOB# ")
            # ENVIA COMANDO DE LIBERAR TERCEIROS
            telnet.write(b"cd omci\n")
            sleep(1)
            telnet.write(b"set omci detecting disable\n")
            sleep(1)
            telnet.write(b"clear\n")
            sleep(1)
            telnet.write(b"show onu_base_capa_whitelist\n")  # exibe descrição e versao de todas as placas
            sleep(4)
            telnet.write(b"\n")
            saida = telnet.read_very_eager().decode('utf-8')  # decode novamente para string padrão
            print(saida)
            texto_omci3 = saida
            texto_omci3 = re.sub(' +', ' ', texto_omci3)
            texto_omci3 = re.findall(r'.*XXXX.*', texto_omci3)  # procura o vendor no show
            if (len(texto_omci3) == 0):  # valida se o vendor esta na whitelist
                print("Desbloqueio não encontrado")
            else:
                print("Placa ja Desbloqueada")
            sleep(1)
            print("Configurando desbloqueio...")
            telnet.write(b"set omci detecting disable\n")
            sleep(1)
            telnet.write(b"clear\n")
            sleep(1)
            telnet.write(b"set onu vendor_id XXXX begin 00000000 end ffffffff policy 2\n")
            sleep(4)
            telnet.write(b"clear\n")
            sleep(1)
            telnet.write(b"show onu_base_capa_whitelist\n\n")  # exibe descrição e versao de todas as placas
            sleep(4)

            saida = telnet.read_very_eager().decode('utf-8')  # decode novamente para string padrão
            print(saida)
            texto_omci4 = saida
            texto_omci4 = re.sub(' +', ' ', texto_omci4)
            texto_omci4 = re.findall(r'.*XXXX.*', texto_omci4)  # procura o vendor no show
            # print(texto_omci2)
            if (len(texto_omci4) == 0):  # valida se o vendor esta na whitelist
                print("Desbloqueio não encontrado")
            else:
                print("Placa ja Desbloqueada")
            sleep(1)
            telnet.write(b"cd ..\n")
            sleep(1)
            telnet.write(b"save\n")
            sleep(5)
            telnet.write(b"exit\n")
            sleep(1)
            telnet.close()
            print("Placa ", matriz_linha[1], " Desbloqueada")
            # print("Script Executado Placa: ", matriz_linha[2])
            sleep(4)
        elif("R1P" in matriz_linha[3]) or ('R2A' in matriz_linha[3]):
            telnet.write(b"cd service\n")
            sleep(1)
            slot = int(matriz_linha[1])
            telnet_slot = f"telnet slot {slot}"
            print("Conectando via telnet...")
            telnet.write(telnet_slot.encode('ascii') + b"\n")
            sleep(5)
            # telnet.read_until(b"GCOB# ")
            # ENVIA COMANDO DE LIBERAR TERCEIROS
            telnet.write(b"cd omci\n")
            sleep(1)
            telnet.write(b"clear\n")
            sleep(1)
            telnet.write(b"show onu_base_capa_whitelist\n")  # exibe descrição e versao de todas as placas
            sleep(4)
            telnet.write(b"\n")
            saida = telnet.read_very_eager().decode('utf-8')  # decode novamente para string padrão
            print(saida)
            texto_omci = saida
            texto_omci = re.sub(' +', ' ', texto_omci)
            texto_omci = re.findall(r'.*ZTEG.*', texto_omci)  # procura o vendor no show
            if(len(texto_omci)==0): #valida se o vendor esta na whitelist
                print("Desbloqueio não encontrado")
            else:
                print("Placa ja Desbloqueada")
            sleep(1)
            print("Configurando desbloqueio...")
            telnet.write(b"set onu vendor_id XXXX begin 00000000 end ffffffff policy 2\n")
            sleep(4)
            telnet.write(b"clear\n")
            sleep(1)
            telnet.write(b"show onu_base_capa_whitelist\n\n")  # exibe descrição e versao de todas as placas
            sleep(4)

            saida = telnet.read_very_eager().decode('utf-8')  # decode novamente para string padrão
            print(saida)
            texto_omci2 = saida
            texto_omci2 = re.sub(' +', ' ', texto_omci2)
            texto_omci2 = re.findall(r'.*XXXX.*', texto_omci2)  # procura o vendor no show
            #print(texto_omci2)
            if (len(texto_omci2) == 0):  # valida se o vendor esta na whitelist
                print("Desbloqueio não encontrado")
            else:
                print("Placa ja Desbloqueada")
            sleep(1)
            telnet.write(b"cd ..\n")
            sleep(1)
            telnet.write(b"save\n")
            sleep(5)
            telnet.write(b"exit\n")
            sleep(1)
            telnet.close()
            print("Placa ", matriz_linha[1], " Desbloqueada")
            #print("Script Executado Placa: ", matriz_linha[2])
            sleep(4)

print("Script executado com sucesso")