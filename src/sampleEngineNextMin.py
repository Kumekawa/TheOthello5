import engineBase as oe

class EngineNextMin(oe.OthelloEngine):
    def __init__(self):
        super(EngineNextMin,self).__init__()

    def go(self,s):
        if(s[1] != self.color):
            print("error")
        best = [-1,-1]
        bestCount = 65
        for i in range(self._Field__xSize):
            for j in range(self._Field__ySize):
                if(self.getAbleFlip(i,j,self.color)):
                    f = self.getNextField(i,j,self.color)
                    count = 0
                    for k in range(len(f)):
                        if(f[k] == self.color):
                            count += 1
                    if(bestCount > count):
                        bestCount = count
                        best = [i,j]
        print("put " + str(best[0]) + " " + str(best[1]) + " " + str(self.color))

if __name__ == "__main__":
    o = EngineNextMin()
    o.main()

