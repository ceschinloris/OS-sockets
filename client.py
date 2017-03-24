#!/usr/bin/env python
# coding: utf-8

# http://apprendre-python.com/page-reseaux-sockets-python-port
import os
import socket

def get(args):
    file_name = args[1]
    s.send(file_name.encode())
    file_name = 'data/%s' % (os.path.basename(file_name),)
    r = s.recv(9999999)
    with open(file_name,'wb') as _file:
        _file.write(r)
    print("Le fichier a été correctement copié dans : %s." % file_name)


def put(args):
    pass

    
commands = {
    "get":get,
    "put":put,
}


print("enter the remote adress")
address = input(">> ") # utilisez raw_input() pour les anciennes versions python

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, 1111))

while not s._closed :
    print("Le nom du fichier que vous voulez récupérer:")
    command = input(">> ") # utilisez raw_input() pour les anciennes versions python

    args = command.split(" ")

    commands[args[0]](args)







    