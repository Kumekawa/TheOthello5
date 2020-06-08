import engineBase as oe

class EngineNextMax(oe.OthelloEngine):
    def __init__(self):
        super(EngineNextMax,self).__init__()

    def go(self,s):
        #自分が担当じゃなければ処理をしない
        if(s[1] != self.color):
            print("error")
        #自分が打った後の局面のうち、最も自分の石が多くなる位置を格納。ひとまず(-1,-1)
        best = [-1,-1]
        #自分が打った後の局面のうち、最も自分の石が多くなる場合のその個数を格納。ひとまず-1
        bestCount = -1
        #盤面の全位置を確認
        for i in range(self._Field__xSize):
            for j in range(self._Field__ySize):
                #(i,j)に自分の色が置けるならば、以下の処理を行う
                if(self.getAbleFlip(i,j,self.color)):
                    #(i,j)に石を置いた直後の盤面をfに格納
                    f = self.getNextField(i,j,self.color)
                    #fのうち自分の石の個数を数える
                    count = 0
                    for k in range(len(f)):
                        if(f[k] == self.color):
                            count += 1
                    #もしfにある石がこれまでで一番多かった場合、(i,j)を最適な位置としてbestに格納
                    if(bestCount < count):
                        bestCount = count
                        best = [i,j]
        #bestを返す
        print("put " + str(best[0]) + " " + str(best[1]) + " " + str(self.color))

if __name__ == "__main__":
    o = EngineNextMax()
    o.main()

