#!/usr/bin/python


import paramiko
from time import sleep
import datetime


senhas = ['senha1','senha2_opcional','senha3_opcional']
lines = []
with open('banco_de_ips.txt') as f:
    lines = f.readlines()

count = 0

for line in lines:
    count += 1
    ip = line.rstrip()
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.banner_timeout = 15

    print(ip)
    conexao = False

    count2 = 0
    for senha in senhas:
        count2 += 1
        print(senha)
        try:
            ssh.connect(hostname=ip, port=22, username='admin', password=senha, timeout=5)
            sleep(5)
            print("{} Acessivel na porta 22", ip)
            conexao = True


        except Exception:
            error = IOError
            conexao = False
            print(error)
            #print("Tentativa de conectar na porta padrão 22 sem sucesso\n")

        if(conexao==True):
            break

    if(conexao==True):

        stdin, stdout, stderr = ssh.exec_command("cat /tmp/system.cfg")
        print(ip)
        if stderr.channel.recv_exit_status() != 0:
            print("erro\n")
        else:
            config = stdout.read().decode('utf-8')


        stdin, stdout, stderr = ssh.exec_command("sed -n '/^resolv.host.1.name=.*/p' /tmp/system.cfg")
        if stderr.channel.recv_exit_status() != 0:
            print("erro\n")
        else:
            nome = stdout.read().decode('utf-8')
            nome = nome.split('=')
            nome[1] = nome[1].strip()
            titulo = nome[1]
            print(nome[1])
            print("backup executado")

        f = open(f"backup/{titulo}.cfg", "w")
        f.write(config)
        f.close()

    ################################################
ssh.close()



