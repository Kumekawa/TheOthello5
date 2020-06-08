import logic as ol
import random
from abc import ABCMeta,abstractmethod

class OthelloEngine(ol.Field):
    def __init__(self):
        super(OthelloEngine,self).__init__()
        self.color = self.C_BLACK
        self.turnPlayer = self.C_BLACK

    def main(self):
        while(True):
            s = input().split(' ')
            if(s[0] == "SOP"):
                self.SOP()
            elif(s[0] == "setcolor"):
                self.setColor(s)
            elif(s[0] == "position"):
                self.position(s)
            elif(s[0] == "go"):
                self.go(s)
            elif(s[0] == "quit"):
                self.quit()
                return
            else:
                print("command ready:" + s[0])

    def SOP(self):
        print("SOP ok")

    def setColor(self,s):
        self.color = s[1]
        print("setcolor ok:" + self.color)

    def position(self,s):
        self.setFieldArray(s[1])
        self.turnPlayer = s[2]
        print("position ok")

    @abstractmethod
    def go(self,s):
        if(s[1] != str(self.color)):
            print("end")
            return

        point = []
        for i in range(self._Field__xSize):
            for j in range(self._Field__ySize):
                if self.getAbleFlip(i,j,self.color):
                    point.append([i,j])
        r = random.randint(0,len(point) - 1)

        print("put " + str(point[r][0]) + " " + str(point[r][1]) + " " + str(self.color))

    def quit(self):
        print("quit")
        

if __name__ == "__main__":
    o = OthelloEngine()
    o.main()
