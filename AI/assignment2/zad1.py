from cgi import test
from os import stat
import random
from tkinter.tix import DECREASING
from unittest import result

"""
zawraca minimalna liczbę zmian jaką trzeba wykonać, aby
wiersz row był zgodny z opisem description
"""
def countSwitch(row,description):

    INF = 100000
    n, m = len(row), len(description)
    dp = [[INF for j in range(m+1)] for i in range(n+1)]
    row = row +'0'

    def dfs(i,j):

        if i>=n and j==m : return 0 
        if i>=n and j<m  : return INF
        if dp[i][j]<INF: return dp[i][j]

        if i<n and j>=m : 
            dp[i][j] = row[i:(n-1)].count("1")
            return dp[i][j]
        
        case1 , l= int(row[i]) + dfs(i+1,j), description[j] 
        block = ((1<<l)-1)<<1
        l += 1
        cost  = bin( int( row[i:i+l], 2 ) ^ block ).count('1')
        case2 = cost + dfs(i+l,j+1)

        dp[i][j] = min(case1,case2)
        return dp[i][j]
    
    return dfs(0,0)
        
def testCountSwitch():
    tests  = [ ('1',[1]), ('01101',[2,1]), ("10000",[3]), ("101010",[6]), ('1100111011001100000',[2,3,6]), ('0100111011000100010',[2,6])]
    answer = [0, 0, 2, 3, 2, 4]
    for i in range(len(tests)):
        ans = countSwitch(tests[i][0],tests[i][1])
        if ans!=answer[i] : print(ans)
        else : print(True)  

def convertToHash(row):
    def convertDigitToChar(l):
        if l=='1': return '#'
        return '.' 
    return ''.join([convertDigitToChar(l) for l in row])

class State:
    class Repair:
        def __init__(self,rows,columns):
            self.rows, self.columns = rows, columns
        def __str__(self):
            return f"rows: {self.rows}, columns: {self.columns}"

    def __init__(self,rows,columns,repair):
        self.rows, self.columns, self.repair = rows, columns, repair
    def setToRepair(self,seq):
        self.repair = State.Repair(seq[0],seq[1])
    def __str__(self):
        image = ''
        for row in self.rows:
            image = image + convertToHash(row) + '\n'
        return f"{image}"

class Description:
    def __init__(self,rows,columns):
        self.rows, self.columns, = rows, columns
    def __str__(self):
        return f"rows: {self.rows}, columns: {self.columns}"
    def __repr__(self):
        return f"rows: {self.rows}, columns: {self.columns}"

def findToRepair(state,description):

    def findBlocks(s):
        result, d, last = list(), 0, '?'
        for w in s:
            if w=='0' and last=='1':
                result.append(d)
                d = 0
            if w=='1': d = d+1
            last = w
        if d>0 : result.append(d)
        return result 
    
    badRows = list()
    for i in range(len(state.rows)):
        if findBlocks(state.rows[i]) != description.rows[i]:
            badRows.append(i)

    badCol = list()
    for j in range(len(state.columns)):
        if findBlocks(state.columns[j]) != description.columns[j]:
            badCol.append(j)
    return (badRows,badCol)

def drawStartSate(n,m):
    rows = [ bin(random.randint(0,(1<<m)-1))[2:].zfill(m) for i in range(n)]
    columns = ['' for j in range(m)]
    for j in range(m):
        for i in range(n): columns[j]+=rows[i][j]
    
    # print(f"wylosowane rows:{rows}, columns:{columns}")
    return State(rows,columns,list())


MXSTATES = 51
MXCNT    = 1000
def findSolution(state, description,DEBUG=False):

    def change(s,k):
        s = list(s)
        if s[k] == '1': s[k] ='0'
        else: s[k]='1'
        return ''.join(s)
    def convertRowsToString(rows):
        result = ''
        for row in rows:
            result = result + row + '#'
        return result
    def getOpposite(l):
        if l=='1': return '0'
        return '1'

    n, m = len(state.columns[0]), len(state.rows[0])
    statesAlreadyVisited = set()
    cnt = 0 
    while (len(state.repair.rows)>0 or len(state.repair.columns)>0) and len(statesAlreadyVisited)<MXSTATES and cnt<MXCNT :
        cnt=cnt+1

        if DEBUG : print(f"jestemw whilau \n")
        if DEBUG : print(f"byłem juz w {len(statesAlreadyVisited)} stanach")
        if DEBUG : print(state)
        if DEBUG : print(f"nie zgadza sie : {state.repair}\n\n")

        idx = random.randint(0,len(state.repair.rows) + len(state.repair.columns)-1)
        if DEBUG : print(f"wylosowałem {idx} a range : {len(state.repair.rows) + len(state.repair.columns)-1}\n")

        if idx < len(state.repair.rows):
            rowIdx, colIdx = idx, 0
            minSwitchs = countSwitch(state.rows[rowIdx],description.rows[rowIdx])

            for i in range(m):  
                newRow = change(state.rows[rowIdx],i)

                switchsNow = countSwitch(newRow,description.rows[rowIdx])
                if switchsNow < minSwitchs:
                    minSwitchs, colIdx = switchsNow, i
            if DEBUG : print(f"poprawiam wiersz\n")
        else:
            rowIdx, colIdx = 0, idx -len(state.repair.rows)
            minSwitchs = countSwitch(state.columns[colIdx],description.columns[colIdx])

            for i in range(n):
                newCol = change(state.columns[colIdx],i)

                switchsNow = countSwitch(newCol,description.columns[colIdx])
                if switchsNow < minSwitchs:
                    minSwitchs, rowIdx = switchsNow, i
            if DEBUG : print(f"poprawiam kolumne\n")
        
        nextStateRows = convertRowsToString(state.rows)
        nextStateRows = list(nextStateRows)
        nextStateRows[ rowIdx*(m+1) + colIdx ] = getOpposite(state.rows[rowIdx][colIdx])
        nextStateRows = ''.join(nextStateRows)

        if not nextStateRows in statesAlreadyVisited:
            state.rows[rowIdx] = change(state.rows[rowIdx],colIdx)
            state.columns[colIdx] = change(state.columns[colIdx],rowIdx)
            state.setToRepair( findToRepair(state,description) )
            statesAlreadyVisited.add(convertRowsToString(state.rows))
        else: 
            if DEBUG : print("nic nie zmieniam")
    
    # state.setToRepair( findToRepair(state,description) )


    # print(state)
    # # print(f"koluny obrazka :{state.columns}")
    # print(f"description = {description}")
    # print(findToRepairDEBUG(state,description))
    # print(f"nie zgadza sie : {state.repair}")


    if len(state.repair.rows)==0 and len(state.repair.columns)==0: 
        # print(f"zwracam {state}bo {len(state.repair.rows)} <-- tyle bad rows, {len(state.repair.columns)} <-- tyle bad col \n")
        # print(f"do naprawy jest : {state.repair}")
        return state
    
    # print(f"zwracam FAŁSZ\n")
    return False

def Solve(n,m,description):

    state = drawStartSate(n,m)
    state.setToRepair( findToRepair(state,description) )
    result = findSolution(state,description)

    attempt = 0
    while result==False and  attempt<100:
        state = drawStartSate(n,m)
        state.setToRepair( findToRepair(state,description) )
        result = findSolution(state,description)
        attempt+=1
    
    return state.__str__()


def testSolve( ):

    tests = [ ( 5, 5, Description( [ [5],[1,1,1],[3],[2,2],[5] ], [ [2,2],[1,3],[3,1],[1,3],[2,2] ] ) ), \
         ( 2, 2, Description( [[2],[1]], [[1],[2]] ) ), \
         ( 3, 3, Description( [[3],[3],[3]], [[3],[3],[3]] ) ), \
             ( 3, 3, Description( [[3],[1,1],[1]], [[3],[1],[2]] ) )]

    test_number = 3
    # Solve(tests[test_number][0], tests[test_number][1], tests[test_number][2])
    for test in tests: 
        Solve(test[0],test[1],test[2])

def init(DEBUG=False):
    with open('testcase.txt', 'r') as file:
        lines = file.readlines()
        n, m = int(lines[0].strip().split()[0]), int(lines[0].strip().split()[1])

        rows = list()
        columns = list()
        for i in range(n):
            rows.append( [int(l) for l in lines[i+1].strip().split()] )

        for i in range(m):
            columns.append( [int(l) for l in lines[n+i+1].strip().split()] )
        if DEBUG: print(f"rows : {rows}")
        if DEBUG: print(f"columns: {columns}")

        return (n,m,Description(rows, columns))


def Main(DEBUG=False):

    testcase = init(DEBUG)
    # print(f"test : {testcase}")
    return Solve( testcase[0], testcase[1], testcase[2] )

def run(DEBUG=False):
    if DEBUG:
        print(f"{''.join(Main(DEBUG))}")
    if not DEBUG:   
        with open( 'zad_output.txt', 'w' ) as file:
            file.write(''.join(Main(False)))

run(True)