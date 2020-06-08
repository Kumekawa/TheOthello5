import engineBase as oe
import random

class EngineRandom(oe.OthelloEngine):
    def __init__(self):
        #親の初期化関数を呼び出す
        super(EngineRandom,self).__init__()

    def go(self,s):
        #もし、自分が思考する番でなければ終了(この処理は実際は不要)
        if(s[1] != str(self.color)):
            print("end")
            return

        #自身が置ける場所を書き出す
        point = []
        for i in range(self._Field__xSize):
            for j in range(self._Field__ySize):
                #(i,j)座標に置けるか確認し、置けるならばpointに追加する
                if self.getAbleFlip(i,j,self.color):
                    point.append([i,j])
        #pointの中からランダムで1箇所選ぶ
        r = random.randint(0,len(point) - 1)

        #上記で選ばれた場所を返す
        print("put " + str(point[r][0]) + " " + str(point[r][1]) + " " + str(self.color))

if __name__ == "__main__":
    er = EngineRandom()
    er.main()
