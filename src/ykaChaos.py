from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
import threading
import socket
import time


class Yka(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("../ui/yka.ui")
        self.ui.show()
        self.ui.startServer.clicked.connect(self.start_server)
        self.ui.connectServer.clicked.connect(self.connect_server)
        self.ui.send.clicked.connect(self.send_msg)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(self):
        print(self.ui.inputMessage.text())
        self.socket.sendall(self.ui.inputMessage.text().encode())

    def start_server(self):
        self.socket.bind(('localhost', 5000))
        t1 = threading.Thread(target=self.socket_listening_thread)
        t1.daemon = True
        t1.start()
        print("서버준비완료")

    def connect_server(self):
        self.socket.connect(('localhost', 5000))
        print("서버연결시도")

    def socket_listening_thread(self):
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        while True:
            msg = conn.recv(1024).decode()
            if msg:
                self.ui.messageViewer.appendPlainText(msg)
                print(msg)
            time.sleep(0.3)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    y = Yka()
    app.exec_()
