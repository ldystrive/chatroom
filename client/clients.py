# -*- coding: utf-8 -*-
import socket
import threading
import time

class Client:
    def __init__(self, addr):
        self.name = ''
        self.name_list = []
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(addr)
        self.con = threading.Condition()

    def login(self, name):
        self.name = name
        self.conn.sendall(('LOGIN|' + name).encode('utf-8'))
        try:
            data = self.conn.recv(1024).decode('utf-8')
            if data == 'OK':
                return True
            else:
                print(data)
                return False
        except:
            return False

    def update(self):
        self.send('UPDATE')

    def send(self, msg):
        if self.con.acquire():
            try:
                print(msg)
                self.conn.sendall(msg.encode('utf-8'))
                self.con.release()
            except:
                print('Send msg to ' + name + ' failed.')
                self.con.release()

    def chat(self, name, msg):
        self.send('CHAT|' + self.name + '|' + name + '|' + msg)

    def recv(self, room_name, name, msg):
        print(room_name + '|' + name + ': ' + msg)
        return name, msg

    def logout(self):
        pass

    def listen(self):
        while True:
            data = self.conn.recv(1024).decode('utf-8')
            threading.Thread(target=self.handler, args=(data,)).start()

    def handler(self, data):
        args = data.split('|')
        if args[0] == 'CHAT':
            self.recv(args[1], args[2], '|'.join(args[3:]))
        if args[0] == 'UPDATE':
            self.name_list = [w for w in args[1:] if w != self.name]
            print(self.name_list)


addr = ('127.0.0.1', 2333)
client = Client(addr)


if __name__ == '__main__':
    name = input('please input your name:')
    if client.login(name):
        threading.Thread(target=client.listen).start()
        while True:
            name_ = input('chat with: ')
            msg_ = input('msg: ')
            threading.Thread(target=client.chat, args=(name_, msg_)).start()
