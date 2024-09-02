from copy import deepcopy
import numpy as np

inFileName = 'zad_input.txt'
outFileName = 'zad_output.txt'
Row = 0
Col = 1
Black = 1
White = -1
Grey = 0

class checkType:
    def __init__(self, t) -> None:
        self.t = t

    def rev(self):
        return checkType(0 if self.t else 1)
    
    def val( self ): return self.t
    def __gt__(self, otherT):
        return self.val() > otherT.val()
    

class Picture:
    def __init__(self):
        self.toDeduct = set()    # wiersze i kolumny, które muszę wywnioskować 
                                 # (wywnioskować jak wyglądają)
                                 
        self.stack = []          

        with open(inFileName, 'r') as f:
            rows, cols = [], []
            line = f.readline().split(" ")
            self.size = tuple([int(x) for x in line[:2]])
            self.tab = np.full(self.size, Grey, dtype=int)
            for i in range(self.size[Row]):
                rows.append([int(x) for x in f.readline().split(" ")])
            for i in range(self.size[Col]):
                cols.append([int(x) for x in f.readline().split(" ")])
            self.data = (rows,cols)
    
    def saveOtput(self):
        with open(outFileName, 'w') as file:
            for x in self.tab:
                for y in x:
                    if y == White: file.write('.')
                    elif y == Black: file.write('#')
                    else: raise Exception('Wrong bit on tab')
                file.write('\n')

    def genPerms(self): #GENERUJE DZIEDZINE DLA KAŻDEGO Z WIERSZY I KAŻDEJ KOLUMNY 
                         #TAK ABY WIERSZ SPEŁNIAŁ ZADANY OPIS
        permsRows = []
        for x,y in zip(self.tab, self.data[Row]):
            permsRows.append( genPermForRow(len(x), y) )
        permsCols = []
        for x, y in zip(self.tab.T, self.data[Col]):
            permsCols.append( genPermForRow(len(x), y) )
        self.perms = (permsRows,permsCols)
    
    def deductAll(self): #WNIOSKUJE JAK POWINNY WYGLĄDAĆ WSZYTSKIE KOLUMNY I WIERSZE 
        for i in [Row, Col]:
            for j in range(self.size[i]):
                self.toDeduct.add((checkType(i), j))

        while self.toDeduct:
            (t,i) = self.toDeduct.pop()
            self.deductRow(t,i)

    def deductRow( self, t, index): #SPOSÓB WNIOSKOWANIA:
                                    #Jeżeli we wszytskich kolorowaniach z dziedziny
                                    #jakieś pole ma ten sam kolor to znaczy, że musi mieć taki kolor 
        row = self.tab[index] if t.val()==Row else self.tab[:, index]
        perms = self.perms[t.val()][index]
        acc = (0,) * self.size[t.rev().val()]

        for p in perms:
            acc = tuple(map(sum, zip(acc, p)))

        for i in range(len(acc)):
            if abs(acc[i])==len(perms): #!!!!
                color = White if acc[i] < 0 else Black 
                if color != row[i]:
                    row[i] = color 
                    self.reducePermSet(t.rev(), i, index)
                    self.toDeduct.add((t.rev(), i))

    def reducePermSet(self, t, rowIndex, bitIndex):
        row = self.tab[rowIndex] if t.val() == Row else self.tab[:, rowIndex]
        perms = self.perms[t.val()][rowIndex]
        if row[bitIndex] == 0: raise Exception('reducePermSet row[bitIndex]=0')
        toRemove = [p for p in perms if p[bitIndex]!=row[bitIndex]]
        for p in toRemove: perms.remove(p)
        if len(perms) == 0: raise Exception('IpossibleConstraints')
    
    def domainsSizes(self): #zwraca listę zawierającą rozmiar dziedziny 
                            #dla każdego wiersza i kolumny 
                            #(pamiętam tylko te o rozmiarze większym niż 1) 
        lens = []
        for j in [Row, Col]:
            lens += [(len(x), checkType(j), i)
                    for i, x, in enumerate(self.perms[j]) if len(x) > 1]
        return lens

    def stackPush(self):# wybieram wiersz lub kolumnę, która ma najmniejszą dziedzine
                        # dodaję na stos kopię dziedzin, kopie tablicy, 
                        # kolumnę lub wiersz o min rozmiarze dziedziny 
                        # i jej  lub jego dziedzinę 
        value, t, index = min(self.domainsSizes())
        self.stack.append(
            (deepcopy(self.perms),
            deepcopy(self.tab),
            list(self.perms[t.val()][index]),
            (t,index)))
    
    def stackPop(self): 
        if len(self.stack) == 0: Exception('Out of Domains')
        (perms, tab, domain, id) = self.stack[-1]
        (t, index) = id

        if len(domain) == 0:
            self.stack.pop()
            return self.stackPop()
        
        for i in [Row,Col]: # przywracam dziedziny do stanu z momęntu wrzucenia na stack 
            for j in range(self.size[i]):
                if len(self.perms[i][j]) != len(perms[i][j]):
                    for x in perms[i][j]:
                        self.perms[i][j].add(x)
        self.tab = deepcopy(tab)


        chosenValue = domain.pop()  # zgaduje jak ma wyglądać wybrana kolumna i wiersz
        self.perms[t.val()][index].clear()
        self.perms[t.val()][index].add(chosenValue)
        return id
    
    def permSizes(self):
        return [len(x) for x in self.perms[Row] + self.perms[Col]]

    def isSolved(self):
        for x in self.permSizes():
            if x!=1: return False
        return True

    def backtrack(self):
        self.stackPush()
        t, index = self.stackPop()
        while True:
            try:
                self.deductRow(t, index)
                while self.toDeduct:
                    t, i = self.toDeduct.pop()
                    self.deductRow(t,i)
                if self.isSolved(): return 
                self.stackPush()
                t, index = self.stackPop()
            except Exception as e:
                t, index = self.stackPop()


def genPermForRow(rowLen,data):
    perms = set()
    genPermForInterval([],data,0,rowLen, perms)
    return perms

def genPermForInterval(row,data,startIndex,rowLen,perms):
    if not data:
        perms.add(tuple(row + [White] * (rowLen - startIndex)))
        return None
    if sum(data) + len(data) -1 + startIndex > rowLen:
        return 'TOO_LONG'
    for i in range(startIndex,rowLen-data[0]+1):
        thisBlock = [White] * (i-startIndex) + [Black] * \
            data[0] + ([] if len(data) == 1 else [White])
        temp = genPermForInterval(row + thisBlock, data[1:],
                                startIndex+len(thisBlock), rowLen, perms)
        if temp == 'TOO_LONG':
            return None
    return None


        


