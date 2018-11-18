import sqlite3
import json
import datetime

class Yka_DBManager():

    def __init__(self):
        self.conn=sqlite3.connect("yka_chaos.db")
        self.c=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS results(player text, date_time text, result integer, K integer, D integer,A integer, hero_type integer, hero_num integer)")

    def __del__(self):
        self.conn.close()

    def requestDatabyPlayer(self,player,s_data="2017-01-01",e_date="2020-12-31"):
        json_list=[]
        for l in self.c.execute("SELECT * FROM results WHERE player=? AND date_time BETWEEN ? AND ?",(player,s_data,e_date)):
            l=list(l)
            d={"player" :l[0], "date_time" : l[1], "result":l[2], "K":l[3], "D":l[4], "A":l[5], "hero_type": l[6], "hero_num": l[7]}
            j=json.dumps(d)
            json_list.append(d)
        return json_list

    def getPlayerScore(self,player,s_data="2017-01-01",e_date="2020-12-31"):
        # turn - 총게임수, win- 이긴게임수, draw- 비긴게임수, lose- 진게임수, rate -승률, winScore-승점, K-총킬수, D-총데스, A-총어시
        # H_rate -힘승률, M_rate-민첩승률, J_rate-지능승률
        turn=0
        win=0
        draw=0
        lose=0
        rate=0.
        winScore=0
        K=0
        D=0
        A=0
        H_win=0
        M_win=0
        J_win=0

        lists=self.requestDatabyPlayer(player,s_data,e_date)

        for l in lists:

            turn=turn+1
            K=K+l["K"]
            D=D+l["D"]
            A=A+l["A"]
            if(l["result"]==1):
                win=win+1
                winScore=winScore+1
                if(l["hero_type"]==0):
                    H_win=H_win+1
                if (l["hero_type"]==1):
                    M_win = M_win + 1
                if (l["hero_type"]==2):
                    J_win = J_win + 1
            if (l["result"] == 0):
                draw = draw + 1
            if (l["result"] == -1):
                lose=lose+1
                winScore=winScore-1
        rate=win/turn
        # turn - 총게임수, win- 이긴게임수, draw- 비긴게임수, lose- 진게임수, rate -승률, winScore-승점, K-총킬수, D-총데스, A-총어시
        # H_win -힘승률, M_win-민첩승률, J_win-지능승률
        d={"player":player,"turn":turn,"win":win,"draw":draw,"lose": lose,"rate":rate,"winScore":winScore,"K":K,"D":D,"A":A,"H_win":H_win,"M_win":M_win,"J_win":J_win}
        j=json.dumps(d)
        return d

    def requestDatabyHero(self,hero_type,hero_num,s_data="2017-01-01",e_date="2020-12-31"):
        json_list = []
        for l in self.c.execute("SELECT * FROM results WHERE hero_type=? AND hero_num=? AND date_time BETWEEN ? AND ?",
                                   (hero_type, hero_num, s_data, e_date)):
            l = list(l)
            d = {"player": l[0], "date_time": l[1], "result": l[2], "K": l[3], "D": l[4], "A": l[5], "hero_type": l[6],"hero_num": l[7]}
            j = json.dumps(d)
            json_list.append(d)
        return json_list

    def sendResultData(self,json_list):
        now=datetime.datetime.now()
        nowDateTime=now.strftime("%Y-%m-%d")
        for j in json_list:
            t=(j["player"],nowDateTime,j["result"],j["K"],j["D"],j["A"],j["hero_type"],j["hero_num"])
            self.c.execute("INSERT INTO results VALUES(?,?,?,?,?,?,?,?)",t)
        self.conn.commit()

    def getRankList(self,player_list,s_data="2017-01-01",e_date="2020-12-31"):
        rank=[]
        for player in player_list:
            l=self.getPlayerScore(player,s_data,e_date)
            rank.append(l)
        new_rank=sorted(rank,key=lambda l:(l['winScore'],l['rate'],l['K']),reverse=True)
        return new_rank

# a=Yka_DBManager()
# j_list=[]
# j1={"player" : "hjk1000", "result":1, "K":10, "D":0, "A":10, "hero_type": 2, "hero_num": 5}
# j2={"player" : "yul2ya", "result":1, "K":10, "D":0, "A":10, "hero_type": 2, "hero_num": 5}
# j_list.append(j1)
# j_list.append(j2)
# # a.sendResultData(j_list)
# # results=a.requestDatabyPlayer("hjk1000")
# j=a.getPlayerScore("hjk1000")
# rank=a.getRankList(["hjk1000","yul2ya"])
# print (rank)