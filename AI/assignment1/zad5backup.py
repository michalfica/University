
import imaplib
from os import stat
from ssl import RAND_bytes
from xmlrpc.client import MAXINT
from numpy import column_stack, zeros
import random

from pyparsing import col

class State:
    def __init__(self,rows,columns,repair):
        self.rows = rows
        self.columns = columns
        self.repair = repair
    def __str__(self):
        #  image = [bin(self.rows[i])[2:].zfill(len(self.columns)) for i in range(len(self.rows))]
        image = [ [0]*len(self.columns) for i in range(len(self.rows))]
        
        for i in range(len(self.rows)):
            row = bin(self.rows[i])[2:].zfill(len(self.columns))
            for j in range(len(self.columns)):
                image[i][j] = row[j]
        return f"{image}\n"

def isOn(a,k): return ((1<<k)&a) > 0
def turnOn(a,k): return ((1<<k)|a)
def turnOff(a,k): return ((~(1<<k))&a) 

def change(a,k): 
    if isOn(a,k): return turnOff(a,k)
    return turnOn(a,k)

def drawStartState(n,m):
    a, b = 0, (1<<m)-1
    rows = [random.randint(a,b) for x in range(n) ]
    columns = [0] * m

    for j in range(m):
        k = m-(j+1)
        for i in range(n):
            power = n-(i+1)

            if isOn(rows[i],k):
                columns[j]+=(1<<power)
    return State(rows,columns,list())

"""
zwraca liczbę całkowitą, która ma zapis binarny dł m 
i wzapisie binarnym ma na początku k jedynek a potem same zera
"""
def fromBinaryToNumber(m,k):
    result = 0 
    for i in range(k):
        result+= turnOn(0,m-(i+1))
    return result 

def getSolutionDescription(n,m,description):
    rows = [0] * n
    columns  = [0] * m

    for i in range(n):
        rows[i] = fromBinaryToNumber(m,description[i])
    for i in range(n,len(description)):
        columns[i-n] = fromBinaryToNumber(n,description[i])
    
    return State(rows,columns,list())

# def testGetSolutionDescription():
#     n, m = 4, 5
#     description = [1,2,3,4, 1,2,3,4,4]
#     print(getSolutionDescription(n,m,description))

"""
przymuje aktualny opis wiersza/kolumny i jak ma docelowo wyglądać 
zwraca min ilość zmian potrzebnych do wykonania 
"""
def countSwitch(a,b):

    # print(f"countSwich a = {a}, b = {b}")
    result = bin(a^b).count("1")
    b= b>>2
    # print(f"chec zaczc while ")
    while b>0 and b%2==0:
        # print(f"zaczynam while")
        # print(f" a = {a} b = {b}")
        # print(f" {a^b}")
        result = min(result,bin(a^b).count("1"))
        # print(f"resukt = {result}")
        b= b>>2
    return result 

def findToRepair(state,targetState):
    ans = list()
    n, m = len(state.rows), len(state.columns)

    for i in range(n):
        if countSwitch(state.rows[i],targetState.rows[i]) > 0:
            ans.append(i+1)
    for j in range(m):
        if countSwitch(state.columns[j],targetState.columns[j]) > 0:
            ans.append(-1*(j+1))
    return ans

def testFindToRepair():
    tests =[(State([3,1],[2,3],list()),State([3,1],[2,3],list()))]
    for test in tests:
        print(len( findToRepair(test[0],test[1])) )

#testFindToRepair()

def check(a,b,k):
    #print(f"check {a},{b},{k}")
    a, b = isOn(a,k), isOn(b,k)
    return (a!=b)

def printSolution(state):
    image = [bin(state.rows[i])[2:].zfill(len(state.columns)) for i in range(len(state.rows))]
    for i in range(len(state.rows)):
            print(image[i])


MXCNT = 20
def findSolution(state,targetState):
    n, m, cnt = len(state.rows), len(state.columns), 0 

    while len(state.repair)>0 and (cnt <MXCNT):
            
            print(f"losuję")
            nr = state.repair[ random.randint(0,len(state.repair)-1) ]
            if nr>0:
                rowIdx, colIdx = nr-1, 0
                moves , switchBefore = 0, 0 
                # countSwitch(state.rows[rowIdx],targetState.rows[rowIdx]) 
                for j in range(m):
                    """
                     zmieniam pole [rowIdx][j] na przeciwne
                    """

                    newRow, newCol = change(state.rows[rowIdx],m-(j+1)), change(state.columns[j],n-(rowIdx-1))
                    switch1 = countSwitch(state.rows[rowIdx],targetState.rows[rowIdx]) + countSwitch(state.columns[j],targetState.columns[j])
                    switch2 = countSwitch(newRow,targetState.rows[rowIdx]) + countSwitch(newCol,targetState.columns[j])
                    #switchBefore+=countSwitch(state.columns[j],targetState.columns[j])
                    #switchAfter = countSwitch(newRow,targetState.rows[rowIdx]) + countSwitch(newCol,targetState.columns[j])

                    #  jexeli row i target row maja różne j bity to dwa razy policze zmiane j bita (najpierw w wierszu potem w kolumnie)
                    if check(state.rows[rowIdx],targetState.rows[rowIdx],m-(j+1)) : switch1-=1
                    else : switch2-=1

                    # if check(state.rows[rowIdx],targetState.rows[rowIdx],m-(j+1)) : switch-=1
                    # else : switch2-=1

                    if moves < (switch1 - switch2):
                        moves, colIdx = (switch1 - switch2), j

                state.rows[rowIdx] = change(state.rows[rowIdx],m-(colIdx+1))
                state.columns[colIdx] = change(state.columns[colIdx],n-(rowIdx+1))
                state.repair = findToRepair(state,targetState)

            else:
                rowIdx, colIdx = 0, -1*(nr) -1
                moves = 0
                #print(f"naprawiam {colIdx} kolumne")

                for i in range(n):
                    # zmieniam pole [i][colIdx] na przeciwne 
                    newRow, newCol = change(state.rows[i],m-(colIdx+1)), change(state.columns[colIdx],n-(i+1))
                    switch1 = countSwitch(state.rows[i],targetState.rows[i]) + countSwitch(state.columns[colIdx],targetState.columns[colIdx])
                    switch2 = countSwitch(newRow,targetState.rows[i]) + countSwitch(newCol,targetState.columns[colIdx])

                    if check(state.columns[colIdx],targetState.columns[colIdx],n-(i+1)) : switch1-=1
                    else : switch2-=1

                    if moves < (switch1 - switch2):
                        moves, rowIdx = (switch1 - switch2), i
                
                #print(f"zmieniam pole {rowIdx},{colIdx}")
                #print(f"k = {m}-{colIdx+1} = {m-(colIdx+1)}")
                state.rows[rowIdx] = change(state.rows[rowIdx],m-(colIdx+1))
                #print(f"k = {n}-{rowIdx+1} = {n-(rowIdx+1)}")
                state.columns[colIdx] = change(state.columns[colIdx],n-(rowIdx+1))

                state.repair = findToRepair(state,targetState)
                cnt+=1
                print(f"znalazłem:")
                printSolution(state)
                print(f"do naprawy : {state.repair}\n")
                

    print(f"wyszedłem z whilea")
    print(f"znalazłem:")
    printSolution(state)
    print(f"do naprawy : {state.repair}")
    if len(state.repair) > 0: return False
    return state

def solve( n, m, description): 
    targetState = getSolutionDescription(n,m,description)

    state = drawStartState(n,m)
    state.repair = findToRepair(state,targetState)

    print(f"state :")
    print(f"{state.rows}")
    print(f"{state.columns}\n")

    print(f"targetstate :")
    print(f"{targetState.rows}")
    print(f"{targetState.columns}")

    result = findSolution(state,targetState)
    # while result==False:
    #     state = drawStartState(n,m)
    #     print(f"state :\n")
    #     print(f"{state.rows}")
    #     print(f"{state.columns}")

    #     print(f"targetstate :\n")
    #     print(f"{targetState.rows}")
    #     print(f"{targetState.columns}")
    #     state.repair = findToRepair(state,targetState)
    #     result = findSolution(state,targetState)
    

    #printSolution(result)


def testSolve():
    # n, m = 2, 2
    # description = [2, 0, 1, 1]
    # solve(n,m,description)

    testst = [(2,2,[2,1,1,2])]
    #(2,2,[2, 0, 1, 1])
    # ,(3,3,[3,2,1,1,2,3]),(4,4,[4,3,2,1,1,2,3,4]),(7,7,[2,2,7,7,2,2,2,4,4,2,2,2,5,5])]
    for test in testst:
        print(test)
        solve(test[0],test[1],test[2]) 


testSolve()