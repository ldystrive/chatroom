import eel
import socket
import threading
import time
import json


class Client:
    def __init__(self, addr):
        self.name = ''
        self.name_list = []
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(addr)
        self.con = threading.Condition()

    def login(self, name):
        print('login', name)
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
                print('Send msg to server failed.')
                self.con.release()

    def chat(self, name, msg):
        self.send('CHAT|' + self.name + '|' + name + '|' + msg)

    def recv(self, room_name, name, msg):
        print(room_name + '|' + name + ': ' + msg)
        eel.recvMsg(room_name, name, msg)
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
            eel.updateNameList(self.name_list)
            print(self.name_list)


addr = ('127.0.0.1', 2333)
client = Client(addr)

eel.init('web')                     # Give folder containing web files


@eel.expose                         # Expose this function to Javascript
def handleinput(x):
    print('%s' % x)


@eel.expose
def handleLogin(x):
    if (client.name == x):
        eel.setLogin(True)
        return
    isLogin = client.login(x)
    eel.setLogin(isLogin)
    if (isLogin):
        main()


@eel.expose
def handleSendMessage(name, msg):
    print(name, msg)
    threading.Thread(target=client.chat, args=(name, msg)).start()


def main():
    threading.Thread(target=client.listen).start()
    # while True:
    #     name_ = input('chat with: ')
    #     msg_ = input('msg: ')
    #     threading.Thread(target=client.chat, args=(name_, msg_)).start()


def portIsUsed(port, ip='localhost'):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, port))
        s.shutdown(2)
        return True
    except:
        return False


_default_options = {
    'mode': 'chrome-app',
    'host': 'localhost',
    'port': 8000
}

while portIsUsed(_default_options['port']):
    _default_options['port'] += 1
    print(_default_options['port'])

eel.start('main.html', size=(800, 600), options=_default_options)    # Start
