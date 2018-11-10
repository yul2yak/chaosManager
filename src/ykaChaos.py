from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import threading
import socket
import time


class Yka(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.isConnected = False
        self.hasRole = False
        self.role = ''
        self.ui = uic.loadUi("../ui/yka.ui")
        self.ui.show()
        self.ui.startServer.clicked.connect(self.start_server)
        self.ui.connectServer.clicked.connect(self.connect_server)
        self.ui.send.clicked.connect(self.send_msg)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(self):
        if not self.isConnected:
            print('not connected')
            return

        msg = self.ui.inputMessage.text()
        print(msg)
        if self.role == 'client':
            self.socket.sendall(msg.encode())
        else:
            conn, addr = self.socket.accept()
            conn.sendall(msg.encode())

    def start_server(self):
        if not self.hasRole:
            self.hasRole = True
            self.role = 'server'
            self.socket.bind(('localhost', 5000))
            thread = threading.Thread(target=self.socket_listening_thread)
            thread.daemon = True
            thread.start()
            print("서버준비완료")
            self.ui.messageViewer.appendPlainText("서버준비완료")
        else:
            msg = "이미 %s 입니다" %self.role
            print(msg)
            self.ui.messageViewer.appendPlainText(msg)

    def connect_server(self):
        if not self.hasRole:
            self.hasRole = True
            self.role = 'client'
            self.socket.connect(('localhost', 5000))
            print("서버연결시도")
            self.ui.messageViewer.appendPlainText("서버연결시도")
            thread = threading.Thread(target=self.socket_listening_thread_client)
            thread.daemon = True
            thread.start()
        else:
            msg = "이미 %s 입니다" % self.role
            print(msg)
            self.ui.messageViewer.appendPlainText(msg)

    def socket_listening_thread_client(self):
        while True:
            msg = self.socket.recv(1024).decode()
            if msg:
                self.isConnected = True
                self.ui.messageViewer.appendPlainText(msg)
                print(msg)
            time.sleep(0.5)

    def socket_listening_thread(self):
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        conn.sendall('연결됨'.encode())
        self.isConnected = True
        self.ui.messageViewer.appendPlainText('연결됨')
        print('연결됨')
        while True:
            msg = conn.recv(1024).decode()
            if msg:
                print(msg)
                reply = 'reply: ' + msg
                conn.sendall(reply.encode())
                self.ui.messageViewer.appendPlainText(msg)
            time.sleep(0.5)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    y = Yka()
    app.exec_()
