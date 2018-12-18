# -*- coding: utf-8 -*-
import socket
import threading
import sys


class Server:
    def __init__(self, addr):
        self.conn_dict = {}
        self.addr_dict = {'group': '0'}
        self.ban_list = ['group', 'failed']
        self.con_dict = {}
        #self.con = threading.Condition()
        #self.client_conns = []
        # noinspection PyBroadException
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print('Failed to create socket.')
            sys.exit()
        self.socket.bind(addr)
        self.socket.listen(5)
        print('Socket listening')

    def login(self, name, conn, addr):
        if (name.lower() in self.addr_dict.keys() and addr[0] != self.addr_dict[name.lower()][0]) \
                or name.lower() in self.ban_list:
            conn.sendall('Failed,name exists.'.encode('utf-8'))
            return

        con = threading.Condition()
        if con.acquire():
            self.con_dict[name.lower()] = [con, ]
            self.conn_dict[name.lower()] = [conn, ]
            self.addr_dict[name.lower()] = addr
            try:
                conn.sendall('OK'.encode('utf-8'))
                con.release()
            except:
                con.release()
        self.update()

    def update(self):
        names = 'UPDATE|' + '|'.join(self.addr_dict.keys())
        print(names)
        for name in self.conn_dict.keys():
            self.send(name, names)

    def logout(self, name):
        if name.lower() not in self.conn_dict.keys():
            return
        con = self.con_dict[name.lower()][0]
        if con.acquire():
            try:
                self.addr_dict.pop(name.lower())
                self.conn_dict.pop(name.lower())
                self.con_dict.pop(name.lower())
                con.release()
            except:
                con.release()
        self.update()

    def send(self, name, msg):

        if name in self.con_dict.keys():
            con = self.con_dict[name][0]
        else:
            print('send ' + msg.split('|')[0] + ' to ' + name + ' failed.')
            return False
        if con.acquire():
            try:
                conn = self.conn_dict[name][0]
                conn.sendall(msg.encode('utf-8'))
                con.release()
                return True
            except:
                print('send ' + msg.split('|')[0] + ' to ' + name + ' failed.')
                con.release()
                return False

    def chat(self, name_a, name_b, msg):
        print('chat: from ' + name_a + ' to ' + name_b + ': ' + msg)
        if name_b not in self.addr_dict.keys():
            pass
        if name_b.lower() == 'group':
            msg = 'CHAT|' + name_a + '|' + name_a + '|' + msg
            for name in self.conn_dict.keys():
                if name != name_a:
                    self.send(name, msg)
        else:
            msg = 'CHAT|' + 'group' + '|' + name_a + '|' + msg
            self.send(name_b, msg)

    def handler(self, data, conn, addr):
        args = data.split('|')
        if args[0] == 'LOGIN':
            self.login('|'.join(args[1:]), conn, addr)
        if args[0] == 'LOGOUT':
            self.logout('|'.join(args[1:]))
        if args[0] == 'CHAT':
            self.chat(args[1], args[2], '|'.join(args[3:]))
        if args[0] == 'UPDATE':
            self.update()

    def keep_conn(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    return
                threading.Thread(target=self.handler, args=(data, conn, addr)).start()
            except:
                print('a connection break.')

    def listen(self):
        while True:
            conn, addr = self.socket.accept()
            print('Connected with ' + addr[0] + ':' + str(addr[1]))
            data = conn.recv(1024).decode('utf-8')
            threading.Thread(target=self.handler, args=(data, conn, addr)).start()
            threading.Thread(target=self.keep_conn, args=(conn,addr)).start()


addr = ('127.0.0.1', 2333)
server = Server(addr)


if __name__ == '__main__':
    server.listen()

