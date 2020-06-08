#戦いの流れ
# 盤面を用意
# 先手後手の決定
#   石が置かれようとする
#   そこに置けるか確認する
#   置けるならば置く
#   次のプレイヤーが置けるか確認する
#   次のプレイヤーが置けなければ順番をスキップする
#   お互いが置けなくなったら終了

class Field:
    #色の設定
    C_NONE = "0"
    C_BLACK = "b"
    C_WHITE = "w"
    #相手の色を取得する
    def getOppomentColor(self,color):
        if color == self.C_BLACK:
            return self.C_WHITE
        if color == self.C_WHITE:
            return self.C_BLACK
        return self.C_NONE

    #初期化時に呼び出される(最初に呼び出される)
    def __init__(self):
        #盤面の大きさ
        self.__xSize = 8
        self.__ySize = 8
        #盤面そのもの
        self.__fieldArray = [[0 for j in range(self.__ySize)] for i in range(self.__xSize)]
        #ターンプレイヤー
        self.__turnPlayer = self.C_BLACK
        #初期盤面を設定
        self.setStartPosition()
        
    #初期局面を設定
    def setStartPosition(self):
        #全体を何もない状態に
        for y in range(self.__ySize):
            for x in range(self.__xSize):
                self.__fieldArray[x][y] = self.C_NONE
        left = self.__xSize // 2 - 1
        top = self.__ySize // 2 - 1
        right = self.__xSize // 2
        bottom = self.__ySize // 2
        #中央に四個の石を配置
        self.__fieldArray[left][top] = self.C_BLACK
        self.__fieldArray[left][bottom] = self.C_WHITE
        self.__fieldArray[right][top] = self.C_WHITE
        self.__fieldArray[right][bottom] = self.C_BLACK

    #x,yに石を置く。置けたら"putok"、置けなかったら"putfault"が返ってくる
    def putStone(self,x,y,color):
        x = int(x)
        y = int(y)

        pf = "putfault"
        po = "putok"
        #置きたい場所に既に石があるので配置失敗
        if self.__fieldArray[x][y] != self.C_NONE:
            return pf
        #盤面の外に出てしまっているので終了
        if self.isOut(x,y):
            return pf

        isPutOk = False
        #全方向にひっくりかえせるか確認し、置けたら置く
        for i in range(-1,2):
            for j in range(-1,2):
                #print(isPutOk)
                isPutOk = (self.__flip(x,y,i,j,color) or isPutOk)

        #無事置けたかどうかを返す
        if isPutOk:
            self.__setColor(x,y,color)
            return po
        else :
            return pf

    #あるマスに石が置けるかどうか確認する
    def getAbleFlip(self,x,y,color):
        for j in range(-1,2):
            for i in range(-1,2):
                if self.__getAbleFlip(x,y,i,j,color):
                    return True #置ける場所が1箇所でもあった
        return False
    
    

    #盤面外の座標を指定しているかどうか
    def isOut(self,x,y):               
        if 0 <= x < self.__xSize and 0 <= y < self.__ySize :
            return False
        else :
            return True

    #指定座標の色を取得
    def getColor(self,x,y):
        return self.__fieldArray[x][y]

    #盤面を描画
    def printField(self):
        for y in range(self.__ySize):
            for x in range(self.__xSize):                
                print(" ",end = "")
                if(self.__fieldArray[x][y] == str(0)):
                    print("_",end = "")
                else:
                    print(self.__fieldArray[x][y],end = "")

            print("")
        return self.__fieldArray

    #現在の局面において指定された側の色が置けるかどうかを判定する
    def isAblePut(self,color):
        for y in range(self.__ySize):
            for x in range(self.__xSize):
                if self.getAbleFlip(x,y,color) :
                    return True #置ける場所がある
        return False    #置ける場所がない


    #現在の局面をSOP(特別オセロプロトコル)形式で出力
    def getFieldSOP(self):
        s = "position "
        for y in range(self.__ySize):
            for x in range(self.__xSize):
                s += self.getColor(x,y)
        
        s += " " + self.__turnPlayer
        return s

    #現在の局面のうち、置けるところを返す
    def getAblePutPoint(self,color):
        f = [[0 for j in range(self.__ySize)] for i in range(self.__xSize)]
        s = ""
        for y in range(self.__ySize):
            for x in range(self.__xSize):
                if self.getAbleFlip(x,y,color):
                    s += str(color)
                else:
                    s += "0"
        return s

    #SOPからfieldArrayを設定する
    def setFieldArray(self,SOP):
        for i in range(self.__xSize):
            for j in range(self.__ySize):
                self.__fieldArray[i][j] = SOP[i + j * self.__xSize]


    #現在の局面において、指定された位置に置かれた場合の局面を返す
    def getNextField(self,x,y,color):
        o = Field()
        o.setFieldArray(self.getFieldSOP().split(' ')[1])
        o.putStone(x,y,color)
        return o.getFieldSOP()

    #指定された方向がひっくりかえせるか確認する
    #x,y:石を置きたい場所
    #dx,dy:石を置けるか探索する方向
    #      -1,-1ならば左上がひっくりかえせるかどうかを確認する
    def __getAbleFlip(self,x,y,dx,dy,color):
        #ひっくりかえせるかどうかの方向が無いので終了
        if dx == 0 and dy == 0:
            return False
        #置きたい場所に既に置かれていれば終了
        if self.getColor(x,y) != self.C_NONE:
            return False

        #x,yの初期位置
        fx = x
        fy = y
        status = 2 #0:正常終了、1:相手の石を数えてる途中、2:初期状態
        #ひっくりかえしに行く
        while(status > 0):
            #指定された方向へ移動
            x += dx
            y += dy
            #盤面内にあるか確認
            if self.isOut(x,y):
                return False
            #移動した先が空欄ではないかどうか確認
            if self.getColor(x,y) == self.C_NONE:
                return False
            #移動した方向が相手の石かどうか調べる
            if self.getColor(x,y) == self.getOppomentColor(color):
                #相手の石がある
                status = 1
            elif status == 1:
                #自分の石があったのでひっくりかえす
                status = 0
            else :
                #行った方向が最初から自分の石だったので終了
                return False
        #ここまで来たと言うことはひっくりかえせる
        return True

    #指定された方向にひっくりかえしに行く
    def __flip (self,x,y,dx,dy,color):
        if self.__getAbleFlip(x,y,dx,dy,color):
            #無事ひっくりかえせるのでひっくりかえす
            x += dx
            y += dy
            while(self.getColor(x,y) != color):
                self.__setColor(x,y,color)
                x += dx
                y += dy
            #ひっくりかえし成功
            return True
        else :
            #ひっくりかえし失敗
            return False

    #指定座標に色を置く。勝手に色を置かれると困るのでプライベート
    def __setColor(self,x,y,color):
        self.__fieldArray[x][y] = color

if __name__ == "__main__":
    print("hello world!")
    f = Field()
    f.setFieldArray("bwwwwwwbwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwbwwwwww0")
    f.printField()
    print("")
    f.putStone(7,7,"b")
    f.printField()
