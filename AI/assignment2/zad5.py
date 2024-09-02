from queue import Queue
from queue import PriorityQueue
from tokenize import String
from typing import List
from xmlrpc.client import MAXINT

from numpy import result_type

class P:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __eq__(self, other):
        if isinstance(other, P):
            return (self.x==other.x and self.y==other.y)
        return NotImplemented

    def __ne__(self, other):
        x = self.__eq__(other)
        if x is NotImplemented:
            return NotImplemented
        return not x

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def dist(self,other):
        return abs(self.x-other.x) + abs(self.y-other.y)
        
def init():
    board = list()
    with open('zad_input.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            board.append(line.strip())
    return board 

def findPos(t,x): 
    result = list()

    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j] == x: result.append(P(i,j))
    return result

def setPosition(board,path,Ps):
    def moveP(p,move):
        newP = P(p.x,p.y) 

        if move=='U': newP = P(p.x-1,p.y)
        if move=='D': newP = P(p.x+1,p.y)
        if move=='L': newP = P(p.x,p.y-1)
        if move=='R': newP = P(p.x,p.y+1)

        if (not (0<=newP.x and newP.x<len(board))) or (not (0<=newP.y and newP.y<len(board[0]))):
            return p 
        if board[newP.x][newP.y]=='#': return p
        return newP

    newPs = list()
    for p in Ps:
        for move in path:
             p = moveP(p,move)
        newPs.append(p)
    return set(newPs)

class State:
    def __init__(self,ps,dist,sciezka):
        '''
        ps ->      lista pozycji gdzie moze znajdować się komandos po przeyciu ścieżki
        ścieżka -> string 
        '''

        self.ps, self.sciezka = ps, sciezka
        self.dist = dist

    def __lt__(self, other):
        if isinstance(other, State):
            return self.dist < other.dist

    def __gt__(self, other):
        if isinstance(other, State):
            return self.dist > other.dist

    def __str__(self):
        return f"({self.ps} ; {self.sciezka})"
    def __repr__(self):
        return f"(pozycje: {self.ps} ; ścieżka: {self.sciezka})"

def BFS(board,startPs,endPs,initialPath,DEBUG):
    MAXPATHLEN = 55
    Q = PriorityQueue()
    visited = dict()

    def addToQueue(ps,dist,h,path):
        if not str(ps) in visited:
            visited[str(ps)] =  dist
            Q.put( (dist+h, State(ps,dist,path) ) )
        # else:
        #     if visited[str(ps)] > dist:
        #         visited[str(ps)] =  dist
        #         Q.put( (dist+h, State(ps,dist,path) ) )

        
    def check(ps):
        for p in ps:
            czyjestp = False
            for e in endPs:
                if (p.x==e.x and p.y==e.y): czyjestp = True
            if czyjestp==False: return False
        return True 

    def movePs(ps,move):
        newPs = list()
        for p in ps:
            if move=='U': newP = P(p.x-1,p.y)
            if move=='D': newP = P(p.x+1,p.y)
            if move=='L': newP = P(p.x,p.y-1)
            if move=='R': newP = P(p.x,p.y+1)

            if board[newP.x][newP.y]=='#': newP = p 
            newPs.append(newP)
        return set(newPs)
    
    def min_distance_to_any_target(p):
        return min( p.dist(target) for target in endPs )

    def h(ps):
        """
        zwraca max z odległości do najbliżśzego punktu docelowego dla każdej pozycji w stanie 
        """
        return max( min_distance_to_any_target(p) for p in ps  )
    
    #def h(ps)
        # result = MAXINT
        # for p in ps:
        #     result = min( result, min( [p.dist(e) for e in endPs]) )
        # return result 

    # def h(self, state: Poses) -> float:
    #     return max(self.min_distance_to_any_target(guy) for guy in state)

    # def min_distance_to_any_target(self, guy: Pos) -> float:
    #     d = Heuristics.manhattan
    #     return self._d[guy] if guy in self._d \
    #         else min(d(guy, t) for t in self.targets)


    numberOfPs = len(startPs)
    addToQueue(startPs,0,h(startPs),initialPath)

    # if DEBUG:
        # print(f"w kolejce jest : {Q.get()}")



    if DEBUG: result = list()
    while not Q.empty():
        state = Q.get()[1]
        ps, dist, path = state.ps, state.dist, state.sciezka

        # if DEBUG:
            # print(f"stan: ps:{ps}")

        if len(path) > MAXPATHLEN :continue

        if DEBUG:
            if check(ps): result.append(path+"\n")
            if len(result)>1 : return result

        if not DEBUG:
            if check(ps): return path

        if len(ps) < numberOfPs:
            numberOfPs = len(ps)
        
        # if DEBUG: print(f"działąm dalej")

        psL, pathL = movePs(ps,'L') , path + 'L'
        hL = h(psL)

        addToQueue(psL,dist+1,hL,pathL)

        psU, pathU = movePs(ps,'U'), path + 'U'
        hU = h(psU)
        addToQueue(psU,dist+1,hU,pathU)

        psD, pathD = movePs(ps,'D'), path + 'D'
        hD = h(psD)
        addToQueue(psD,dist+1,hD,pathD)

        psR, pathR = movePs(ps,'R'), path + 'R'
        hR = h(psR)
        addToQueue(psR,dist+1,hR,pathR)

    return False

def solve(DEBUG):
    board = init()
    startPos, endPos = findPos(board,'S'), findPos(board,'G')
    startPos = startPos + findPos(board,'B')
    endPos = endPos + findPos(board,'B')

    initialPath = ''
    ps = setPosition(board,initialPath,startPos)

    result = BFS(board,ps,endPos,initialPath,DEBUG)
    if not result==False:
        return result

    return "NIE ZNALAZŁEM\n"

def run():
    with open( 'zad_output.txt', 'w' ) as file:
        file.write(''.join(solve(False)))

run()
    

""" przechodzi 6/21 testów """