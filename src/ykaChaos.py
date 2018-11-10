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
        self.ui.pushButton.clicked.connect(self.serv)
        self.ui.pushButton_2.clicked.connect(self.cli)
        self.ui.pushButton_3.clicked.connect(self.send_msg)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(self):
        self.s.sendall(self.ui.lineEdit_5.Text().encoding())

    def serv(self):

        self.s.bind(('localhost', 5000))
        print("연결완료")
        t1 = threading.Thread(target=self.th1)
        t1.daemon = True
        t1.start()

    def cli(self):
        self.s.connect(('localhost', 5000))

    def th1(self):
        self.s.listen(1)
        conn, addr = self.s.accept()
        while True:
            msg = conn.recv(1024).decode()
            if msg:
                self.ui.plainTextEdit.appendPlainText(msg)
                print(msg)
            time.sleep(1)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    y = Yka()
    app.exec_()
