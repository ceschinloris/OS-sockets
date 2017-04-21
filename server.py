#!/usr/bin/env python
# coding: utf-8
import os
import socket
import threading
import pickle
from pathlib import Path


class ClientThread(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

        self.is_running = True
        self.commands = {
            "ls": self.ls,
            "cd": self.cd,
            "mkdir": self.mkdir,
            "get": self.get,
            "put": self.put,
            "exec": self.exec,
            "exit": self.exit,
            "getpath": self.get_current_path,
        }
        self.current_path = Path(os.getcwd())

    def run(self):
        print("Connection de %s %s" % (self.ip, self.port,))

        while self.is_running:
            command = self.clientsocket.recv(2048).decode()
            if command is not '':
                command_name, command_args = command.split(":", 1)

                self.commands[command_name](command_args)

        print("Client déconnecté...")

    def ls(self, args):
        """ args : void"""
        file_list = os.listdir(self.current_path.absolute())
        self.clientsocket.send(pickle.dumps(file_list))

    def cd(self, args):
        """ args : 0 : path"""
        if os.path.isdir(str(self.current_path) + '/' + args):

            self.current_path = Path(os.path.join(self.current_path, args)).resolve()

            self.clientsocket.send("1".encode())
        else:
            self.clientsocket.send("2".encode())

    def mkdir(self, args):
        try:
            os.mkdir(os.path.join(self.current_path.absolute(), args))
            self.clientsocket.send("1".encode())
        except FileExistsError as e:
            self.clientsocket.send(str(e).encode())

    def get(self, args):
        """ args : 0 : file name
                   1 : save path"""

        fp = open(args, 'rb')
        self.clientsocket.send(fp.read())

    def put(self, args):
        pass

    def exec(self, args):
        pass

    def exit(self, args):
        self.is_running = False

    def get_current_path(self, args):
        """ args : void"""
        self.clientsocket.send(str(self.current_path.absolute()).encode())


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 1111))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
