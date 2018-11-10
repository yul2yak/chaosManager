from socket import socket

from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import threading
import socket
import time


class Yka(QtWidgets.QMainWindow):
    socket: socket
    ui: QtWidgets
    isConnected: bool
    hasRole: bool
    role: str

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.init_status()
        self.init_ui()

    def init_status(self):
        print('init_status')
        self.isConnected = False
        self.hasRole = False
        self.role = ''

    def reset_status(self):
        print('reset_status')
        self.isConnected = False
        if self.role == 'client':
            self.hasRole = False
            self.role = ''

    def init_ui(self):
        self.ui = uic.loadUi("../ui/yka.ui")
        self.ui.show()
        self.ui.startServer.clicked.connect(self.start_server)
        self.ui.connectServer.clicked.connect(self.connect_server)
        self.ui.disconnectServer.clicked.connect(self.disconnect_server)
        self.ui.send.clicked.connect(self.send_msg)

    def start_server(self):
        if not self.hasRole:
            self.hasRole = True
            self.role = 'server'
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind(('localhost', 5000))
            thread = threading.Thread(target=self.socket_listening_thread)
            thread.daemon = True
            thread.start()
            print("서버준비완료")
            self.ui.messageViewer.appendPlainText("서버준비완료")
        else:
            msg = "이미 %s 입니다" % self.role
            print(msg)
            self.ui.messageViewer.appendPlainText(msg)

    def connect_server(self):
        if not self.hasRole:
            self.hasRole = True
            self.role = 'client'
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    def disconnect_server(self):
        if self.role != 'client':
            print('클라이언트가 아닙니다.')
            self.ui.messageViewer.appendPlainText("클라이언트가 아닙니다.")
            return

        if not self.isConnected:
            print('연결이 필요합니다.')
            self.ui.messageViewer.appendPlainText("연결이 필요합니다.")
            return

        self.socket.close()
        self.reset_status()
        print('연결을 종료합니다.')
        self.ui.messageViewer.appendPlainText("연결을 종료합니다.")

    def send_msg(self):
        if not self.isConnected:
            print('연결이 필요합니다.')
            self.ui.messageViewer.appendPlainText("연결이 필요합니다")
            return

        msg = self.ui.inputMessage.text()
        print(msg)
        if self.role == 'client':
            self.socket.sendall(msg.encode())
        else:
            conn, addr = self.socket.accept()
            conn.sendall(msg.encode())

    def socket_listening_thread_client(self):
        while True:
            try:
                msg = self.socket.recv(1024)
            except ConnectionError:
                self.reset_status()
                return
            if msg:
                self.isConnected = True
                self.ui.messageViewer.appendPlainText(msg.decode())
                print(msg.decode())
            time.sleep(0.5)

    def socket_listening_thread(self):
        while True:
            self.socket.listen(1)
            conn, address = self.socket.accept()
            conn.sendall('연결됨'.encode())
            self.isConnected = True
            self.ui.messageViewer.appendPlainText(str(address) + ' 연결됨')
            print(str(address) + ' 연결됨')
            while True:
                try:
                    msg = conn.recv(1024)
                except ConnectionError:
                    print(str(address) + " 클라이언트 연결이 해제됨")
                    self.ui.messageViewer.appendPlainText(str(address) + ' 클라이언트 연결이 해제됨')
                    break
                if not msg:
                    break
                print(msg.decode())
                reply = 'echo: ' + msg.decode()
                conn.sendall(reply.encode())
                self.ui.messageViewer.appendPlainText(str(address) + ' ' + msg.decode())
                time.sleep(0.5)
            conn.close()
            self.reset_status()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    y = Yka()
    app.exec_()
