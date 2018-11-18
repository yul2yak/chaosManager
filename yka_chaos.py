from PyQt5 import QtWidgets
from PyQt5 import uic
import sys
from Yka_DBManager import Yka_DBManager
import threading
import socket
import time

class Yka(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("yka.ui")
        self.ui.show()
        self.DBManager=Yka_DBManager()
        self.ui.pushButton.clicked.connect(self.sendData)
        self.ui.pushButton_3.clicked.connect(self.setRank)
        for i in range(6):
            for j in range(7):
                item=QtWidgets.QTableWidgetItem("")
                self.ui.tableWidget.setItem(i,j,item)
        for i in range(6):
            for j in range(8):
                item=QtWidgets.QTableWidgetItem("")
                self.ui.tableWidget_2.setItem(i,j,item)

    def setRank(self):
        player_list=["hjk1000",'yul2ya']
        rank_list=self.DBManager.getRankList(player_list)
        i=0
        for rank in rank_list:
            # d = {"player": player, "turn": turn, "win": win, "draw": draw, "lose": lose, "rate": rate,
            #      "winScore": winScore, "K": K, "D": D, "A": A, "H_win": H_win, "M_win": M_win, "J_win": J_win}
            self.ui.tableWidget_2.item(i,0).setText(str(i+1))
            self.ui.tableWidget_2.item(i,1).setText(rank['player'])
            self.ui.tableWidget_2.item(i, 2).setText(str(rank['turn']))
            self.ui.tableWidget_2.item(i, 3).setText(str(rank['rate']))
            self.ui.tableWidget_2.item(i, 4).setText(str(rank['winScore']))
            self.ui.tableWidget_2.item(i, 5).setText(str(rank['K']))
            self.ui.tableWidget_2.item(i, 6).setText(str(rank['D']))
            self.ui.tableWidget_2.item(i, 7).setText(str(rank['A']))
            i=i+1
    def sendData(self):
        j_list = []
        for i in range(6):
            if(self.ui.tableWidget.item(i,0).text() == ""):
                pass
            else:
                player=self.ui.tableWidget.item(i,0).text()
                result=int(self.ui.tableWidget.item(i,1).text())
                K=int(self.ui.tableWidget.item(i,4).text())
                D=int(self.ui.tableWidget.item(i,5).text())
                A=int(self.ui.tableWidget.item(i, 6).text())
                hero_type=int(self.ui.tableWidget.item(i, 2).text())
                hero_num = int(self.ui.tableWidget.item(i, 3).text())
                j={"player" : player, "result":result, "K":K, "D":D, "A":A, "hero_type": hero_type, "hero_num": hero_num}
                j_list.append(j)
        if(len(j_list)>0):
            self.DBManager.sendResultData(j_list)
            # QtWidgets.QMessageBox.about(self,"DATA가 전송되었습니다.")
            for i in range(6):
                for j in range(7):
                    item = QtWidgets.QTableWidgetItem("")
                    self.ui.tableWidget.setItem(i, j, item)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    y = Yka()
    app.exec_()

