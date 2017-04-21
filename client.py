#!/usr/bin/env python
# coding: utf-8

# http://apprendre-python.com/page-reseaux-sockets-python-port
import os
import socket
import pickle

class Client:


    CHIFFRE = 9999999

    def __init__(self):
        self.commands = {
            "ls": self.ls,
            "cd": self.cd,
            "mkdir": self.mkdir,
            "get": self.get,
            "put": self.put,
            "exec": self.exec,
            "exit": self.exit,
        }

        # print("enter the remote adress")
        # address = input(">> ")  # utilisez raw_input() pour les anciennes versions python
        self.address = "127.0.0.1"

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.address, 1111))
        self.current_path=''
        self.get_current_path()


    def ls(self, args):
        """ args : void"""
        self.s.send("ls:".encode())
        r = self.s.recv(self.CHIFFRE)

        r = pickle.loads(r)
        print(r)


    def cd(self, args):
        """ args : 0 : path"""
        path = args[0]
        self.s.send(("cd:"+path).encode())
        r = self.s.recv(self.CHIFFRE)

        #error code
        if r.decode() == "1":
            self.get_current_path()
        else:
            print("Error, folder \"" + path + "\" doesn't exist")


    def mkdir(self, args):
        """ args : 0 : folder name"""
        self.s.send(("mkdir:"+args[0]).encode())

        r = self.s.recv(self.CHIFFRE)
        if r.decode() is not "1":
            print(r.decode())


    def get(self, args):
        """ args : 0 : file name
                   1 : save path"""
        file_name = args[0]
        self.s.send(("get:" + file_name).encode())
        file_name = args[1] + '/' + (os.path.basename(file_name))
        r = self.s.recv(self.CHIFFRE)
        with open(file_name, 'wb') as _file:
            _file.write(r)
        print("File saved in " + file_name)


    def put(self, args):
        pass


    def exec(self, args):
        pass


    def exit(self, args):
        self.s.send(("exit:").encode())
        self.s.close()

    def get_current_path(self):
        self.s.send("getpath:".encode())
        r = self.s.recv(self.CHIFFRE)
        self.current_path = r.decode()


    def run(self):
        while not self.s._closed:
            # Faut input les méthodes
            #
            #   ls
            #   cd
            #   mkdir
            #   get server_filename client_savepath
            #   put client_filename server_savepath
            #   run command (exec(command) sur le serveur)

            command = input(self.current_path+">>")  # utilisez raw_input() pour les anciennes versions python

            args = command.split(" ")

            try:
                self.commands[args[0]](args[1:])
            except :
                print("Invalid command")

        print ("bye")

if __name__ == '__main__':
    c = Client()
    c.run()