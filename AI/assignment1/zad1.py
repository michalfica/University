from operator import add
from os import stat
from pdb import post_mortem
from queue import Queue
from unittest import result

"""
Rozpatruję wszystkie kolejne możliwe stany gry zaczynając od stanu początkowego 
dopóki nie trafię na mat, figury poruszają się zgodnie z regułami, dodatkowo 
mogą wchodzić tylko na wolne pola
"""

global kingmoves 
kingmoves = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (-1,-1), (-1,1), (1,-1)]

class State:
    def __init__(self, turn, wk, wt, bk):
        self.turn = turn
        self.wk = wk
        self.wt = wt
        self.bk = bk
    
    def eq(self,other):
        return (self.turn==other.turn and self.wk==other.wk and self.wt==other.wt and self.bk==other.bk)
    
    def whiteTurn(self):
        return self.turn == 1

    def __str__(self):
        return f"({self.turn}, {self.wk}, {self.wt}, {self.bk})"

class Position:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return (self.x==other.x and self.y==other.y)

    def inBoard(self):
        return 0<self.x and self.x<9 and 0<self.x and self.y<9 

    def __str__(self):
        return f"[{self.x}, {self.y}]"

def checkBeat( state ):
    """
    Czy bialy bije czarnego w obecnym układzie pionków?
    """
    if state.wt.x==state.bk.x or state.wt.y==state.bk.y:
        return True
    
    for i in kingmoves:
        wkmove = Position(state.wk.x+i[0],state.wk.y+i[1])
        if wkmove.inBoard() and wkmove==state.bk:
            return True
    return False

def testCheckBeat():
    states = [State(1,Position(5,5),Position(3,7),Position(6,6)),State(-1,Position(5,5),Position(3,7),Position(6,6)),
              State(1,Position(5,5),Position(3,7),Position(6,7)),State(1,Position(5,5),Position(3,7),Position(7,6))]
    answers= [True,True,True,False]

    for i in range(len(states)):
        print(f"{checkBeat(states[i])==answers[i]} ")

def checkMat( state ):
    """
    Czy jest tura czarnego, czy biały może w obecnym układzie zbić czarnego i czy czarny nie może uciec przed biciem?
    """
    if not checkBeat(state) or state.whiteTurn():
        return False
    for i in kingmoves:
        bkmove = Position(state.bk.x+i[0],state.bk.y+i[1])
        if bkmove.inBoard() and (not checkBeat(State(1,state.wk,state.wt,bkmove))):
            return False
    return True

def testCheckMat():
    states = [State(-1,Position(1,2),Position(2,3),Position(3,4))]
    answers= [False]

    for i in range(len(states)): 
        print(f"{checkMat(states[i])==answers[i]} ")

def BFS(startState):
    visited = dict()
    Q = Queue() 
    predecessor = dict()

    def addToQueue(prevstate,state,d):
        if not state in visited:
            visited[state] = True
            predecessor[state] = prevstate
            Q.put((state,d))

    def printPath(state):
        path = [state]
        while not state.eq(startState):  
            prevState = predecessor[state]
            path.append(prevState)
            state = prevState

        for i in range(len(path)):
            idx = len(path) - (i+1)
            print(path[idx])

    addToQueue(startState,startState,0)

    global result 
    global finalstate 
    result = -1 
    while not Q.empty():
        item = Q.get()
        state, distance = item[0], item[1]

        if checkMat(state):
            result = distance 
            finalstate = state 
            break 
        
        if state.whiteTurn():
            for i in kingmoves:
                wkmove = Position(state.wk.x+i[0],state.wk.y+i[0])
                newstate = State(-1,wkmove,state.wt,state.bk)

                if wkmove.inBoard() and  (not wkmove==state.wt):
                    addToQueue(state,newstate,distance+1)

            for i in range(2):
                for j in range(8):
                    if i==0 : wtmove = Position(state.wt.x,j+1)
                    else :    wtmove = Position(j+1,state.wt.y)

                    newstate = State(-1,state.wk,wtmove,state.bk)
                    if not wtmove==state.wk:
                        addToQueue(state,newstate,distance+1)
        else:
            for i in kingmoves:
                bkmove = Position(state.bk.x+i[0],state.bk.y+i[1])
                newstate = State(1,state.wk,state.wt,bkmove)

                if bkmove.inBoard() and (not bkmove==state.wk) and (not bkmove==state.wt):
                    addToQueue(state,newstate,distance+1)

    if result == -1:
        return 'INF'
    else:
        print(f"from {startState} to mat {result}")
        printPath(finalstate)
        return result 

def solve(state):
    if checkMat(state) or (state.whiteTurn() and checkBeat(state)):
        return 0

    return BFS(state)

def testSolve():
    states = [State(-1,Position(1,1),Position(2,2),Position(3,3)),State(-1,Position(7,8),Position(8,1),Position(3,4)),
              State(-1,Position(2,4),Position(6,3),Position(5,8)),State(-1,Position(1,2),Position(5,4),Position(1,4))]
    #for state in states:
    #    print(f"{solve(state)} ")
    solve(states[3])

testSolve()

'black g8 h1 c4' '10'
'black b4 f3 e8' '6'
'black a2 e4 a4' '8'







