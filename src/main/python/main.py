from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button
from pynput.keyboard import Key,Listener
from multiprocessing import Process
import socket
import sys
import time

required_clients=2
clients = []
serveroutput=""
HOST = ""
PORT = 0
cnt = True
keyboard = keyboard.Controller()
mouse = mouse.Controller()
s = socket.socket()
s.settimeout(1)
TimeoutException = socket.timeout
listeners=[]
processes=[]


def put_pause_server(key):
    global clients
    try:
        if(key.char=='q'):
            for conn,addr in clients:
                conn.sendall(bytes('pause','utf-8'))
            print("click")
            mouse.press(Button.left)
            mouse.release(Button.left)
            print("paused")
    except AttributeError:
        pass

def put_pause_client(key):
    try:
        if(key.char=='q'):
            s.sendall(bytes('pause','utf-8'))
            mouse.press(Button.left)
            mouse.release(Button.left)
    except AttributeError:
        pass



def server_listen():
    global serveroutput
    global text_box
    while True:
        put_pause=False
        originator=()
        for conn,addr in clients:
            conn.settimeout(0.0001)
            try:
                data=conn.recv(1024)
                print(data)
            except TimeoutException:
                continue
            
            if str(data, "utf-8")=="pause":
                put_pause=True
                originator = addr
                break
        if put_pause:
            print("click")
            mouse.press(Button.left)
            mouse.release(Button.left)
            serveroutput+="client {0} put pause \n".format(originator)
            text_box.setPlainText(serveroutput)
            for conn,addr in clients:
                if addr!=originator:
                    conn.sendall("pause")

def client_listen():
    s.settimeout(0.0001)
    while True:        
        put_pause=False
        try:
            data=s.recv(1024)
            put_pause=str(data, "utf-8")=="pause"
        except TimeoutException:
            print(end='')
        if put_pause:
            print("click")
            mouse.press(Button.left)
            mouse.release(Button.left)
        


class Window(QMainWindow):

    def start_server(self):
        global HOST
        global PORT
        global clients
        global serveroutput
        global required_clients
        global s
        HOST = self.ui.host_input.text()
        PORT = int(self.ui.port_input.text())
        required_clients = int(self.ui.max_clients.text())
        clients = []
        print("starting server on {0} at {1}".format(HOST,PORT))
        serveroutput+="starting server on {0} at {1} \n".format(HOST,PORT)
        try:
            s.bind((HOST, PORT))
        except OSError:
            print("port already used reseting")
            serveroutput+="port already used reseting \n"
        s.settimeout(10000000)
        for i in range(required_clients):
            s.listen(10000000) #dis some shieeeet
            clients.append(s.accept())
            serveroutput+="got client {0} \n".format(i)
        print(clients)
        serveroutput+="got all clients \n"
        for conn,addr in clients:
            print(addr)
        listener=Listener(on_press=put_pause_server)
        listener.start()
        listeners.append(listener)
        server = Process(target=server_listen)
        server.start()
        processes.append(server)
        serveroutput+="started server \n"
        self.ui.textBrowser.setPlainText(serveroutput)
        

    def connect_to_server(self):
        global HOST
        global PORT
        global s
        HOST = self.ui.server_ip.text()
        PORT = int(self.ui.server_port.text())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        listener=Listener(on_press=put_pause_client)
        listener.start()
        server=Process(target=client_listen)
        server.start()
        listeners.append(listener)
        processes.append(server)

    def clear_all_running(self):
        for listener in listeners:
            listener.stop()
        for process in processes:
            process.terminate()
        listeners.clear()
        processes.clear()

    def __init__(self,ui):
        Ui_MainWindow, QtBaseClass = uic.loadUiType(ui)
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global text_box
        text_box = self.ui.textBrowser
        self.ui.restart_button.clicked.connect(self.start_server)
        self.ui.reconnect_button.clicked.connect(self.connect_to_server)
        self.ui.soptButton.clicked.connect(self.clear_all_running)
        self.ui.disconnect_button.clicked.connect(self.clear_all_running)
   
class AppContext(ApplicationContext):           # 1. Subclass ApplicationContext
    def run(self):
        self.ui = self.get_resource("layout.ui")                              # 2. Implement run()
        window = Window(self.ui)
        window.show()
        return self.app.exec_()                 # 3. End run() with this line

if __name__ == '__main__':
    appctxt = AppContext()                      # 4. Instantiate the subclass
    exit_code = appctxt.run()                   # 5. Invoke run()
    sys.exit(exit_code)
