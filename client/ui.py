import eel
import socket
import threading
from clients import Client

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


eel.start('main.html', size=(800, 600))    # Start
