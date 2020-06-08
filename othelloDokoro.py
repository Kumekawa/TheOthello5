from src import logic as ol
from src import getFilePathWithGUI as gfp
import subprocess as sp
import time
import tkinter as tk
import threading

class OthelloDokoro(ol.Field):
    def __init__(self):
        super(OthelloDokoro,self).__init__()
        self.__start()
        self.interval = 1

    def main(self):
        #開始時の挨拶
        self.p1.communicate("SOP")
        self.p2.communicate("SOP")

        #先行後攻の設定
        self.p1.communicate("setcolor b")
        self.p2.communicate("setcolor w")

        turnCount = 0

        #ターンプレイヤーに従って、決着がつくまで対局させる
        while(True):
            #局面の送信
            self.p1.communicate(self.getFieldSOP())
            self.p2.communicate(self.getFieldSOP())


            r = ""
            s = []
            while(True):
                #ターンプレイヤーが"put"を返して来るまで"go"を送り続ける
                if self._Field__turnPlayer == "b":
                    r = self.p1.communicate("go b")
                elif self._Field__turnPlayer == "w":
                    r = self.p2.communicate("go w")
                s = r.split(" ")
                #if(s[0] == "put"):
                if(True):
                    break

            put = self.putStone(int(s[1]),int(s[2]),s[3])
            if(put == "putok"):
                oppoment = self.getOppomentColor(self._Field__turnPlayer)
                #相手が置けるので、相手に手番を渡す
                if(self.isAblePut(oppoment)):
                    self._Field__turnPlayer = oppoment
                elif(self.isAblePut(self._Field__turnPlayer)):
                    #相手が置けないが、ターンプレイヤーは置けるのでそのまま続ける
                    pass
                else:
                    #お互い置けなくなったので、勝ち負けを決定する
                    sop = self.getFieldSOP()
                    #石の数を数えて勝者を出す
                    wn = 0
                    bn = 0
                    for i in range(len(sop)):
                        if(sop[i] == "w"):
                            wn += 1
                        elif(sop[i] == "b"):
                            bn += 1
                    if(wn > bn):
                        #白勝ち
                        self.p1.communicate("result you lose")
                        self.p2.communicate("result you win")
                        break
                    elif(bn > wn):
                        #黒勝ち
                        self.p1.communicate("result you win")
                        self.p2.communicate("result you lose")
                        break
                    else:
                        #引き分け
                        self.p1.communicate("result you draw")
                        self.p2.communicate("result you draw")
                        break

            else:
                #正しく置けなかったので、ターンプレイヤーを敗北とする
                if self._Field__turnPlayer == "b":
                    self.p1.communicate("result you lose")
                    self.p2.communicate("result you win")
                    break
                elif self._Field__turnPlayer == "w":
                    self.p1.communicate("result you win")
                    self.p2.communicate("result you lose")
                    break

            self.printField()
            turnCount += 1
            print(turnCount)
            time.sleep(self.interval)
            
            if(self.th.isAlive() == False):
                break

        self.printField()
        turnCount += 1
        print(turnCount)
        time.sleep(0)

        self.p1.communicate("quit")
        self.p2.communicate("quit")
        
        self.th.join()

    def __start(self):
        print("先手を選んで下さい")
        ps = gfp.getFilePath()
        #ps = "c:\\Users\\kumek\\Documents\\VisualStudioCode\\python\\othello\\src\\engineNextMax.py"
        print(ps)
        print("後手を選んで下さい")
        pg = gfp.getFilePath()
        #pg = "c:\\Users\\kumek\\Documents\\VisualStudioCode\\python\\othello\\src\\engineNextMin.py"
        print(pg)

        #self.__drawWindow()
        
        self.p1 = Player(ps,"p1")
        self.p2 = Player(pg,"p2")

        self.th = threading.Thread(target=self.__drawWindow)
        self.th.start()


    def __drawWindow(self):
        square = 80
        h = square * self._Field__ySize
        w = square * self._Field__xSize

        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window,bg = "green",height = h,width = w)
        self.__refleshWindow()
        self.canvas.pack()
        self.window.mainloop()

    def __refleshWindow(self):
        square = 80
        h = square * self._Field__ySize
        w = square * self._Field__xSize

        self.canvas.delete("stones")

        for j in range(self._Field__ySize):
            for i in range(self._Field__xSize):
                c = self._Field__fieldArray[i][j]
                if c == "w":
                    self.canvas.create_oval(square * i,square * j,square * (i + 1),square * (j + 1),fill = "white",tags = "stones")
                elif c == "b":
                    self.canvas.create_oval(square * i,square * j,square * (i + 1),square * (j + 1),fill = "black",tags = "stones")
                self.canvas.create_rectangle(square * i,square * j,square * (i + 1),square * (j + 1),tags = "stones")

        self.window.after(1000 // 30,self.__refleshWindow)
        

    def __quit(self):
        pass
    
    def setInterval(self,interval):
        self.interval = interval

#https://qiita.com/tanabe13f/items/8d5e4e5350d217dec8f5
class Player:
    def __init__(self,path,name = "no name"):
        self.path = path
        self.name = name

        t = self.path.split('.')
        s = t[-1]
        e = self.path
        if(s == "py"):
            e = ["python",self.path]
        
        self.process = sp.Popen(e,stdin=sp.PIPE,stdout=sp.PIPE,encoding="UTF-8")

    def communicate(self,inText):
        print(self.name + " < " + inText)
        self.process.stdin.write(inText)
        self.process.stdin.write("\n")
        self.process.stdin.flush()
        out = self.process.stdout.readline().strip()
        print(self.name + " > " + out)
        return out


if __name__ == "__main__":
    o = OthelloDokoro();
    #一個置くごとの間隔を設定する
    o.setInterval(0)
    o.main()

