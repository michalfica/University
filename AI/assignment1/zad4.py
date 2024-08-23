"""
Rozwiązanie polega na rozpatrzeniu wszytskich możliwych stanów końcowych
(takich ciągów 0/1, w których występuje dokładnie 1 blok 1 długości d) 
i policzeniu na ilu pozycjach różni się dany stan końcowy o stanu początkowego
wynikiem jest najmniejsz możliwa ilość różnych pozycji 
"""

class Case:
    def __init__(self,state,d):
        self.state = state
        self.d = d
    def __str__(self):
        return f"({self.state}, {self.d})"

case = Case(1,1)
case.__doc__
def computeSumPref(state):
    sumPref = [0] * (len(state)+1)
    
    for i in range(len(state)):
        index = i+1 
        sumPref[index] = sumPref[index-1] + int(state[i])
    return sumPref
        
def checkcomputeSumPref():
    state = "101000101110"
    res =[1,1,2,2,2,2,3,3,4,5,6,6]
    print(computeSumPref(state))

def solve(case):
    sumPref = computeSumPref(case.state)
    minAmountofShifts = len(case.state)

    if case.d == 0:
        return sumPref[len(case.state)]

    for i in range(len(case.state)-case.d+1):
        beg, end = i, i+case.d-1
        # liczba zer w przedziale [beg,end]
        swap1 = case.d - (sumPref[end+1] - sumPref[beg])
        #liczba jedynek poza przedziałem [beg,end]
        swap2 = sumPref[len(case.state)] - (sumPref[end+1] - sumPref[beg])

        shiftsTotal = swap1 + swap2 
        minAmountofShifts = min(minAmountofShifts,shiftsTotal)
    return minAmountofShifts

def checkSolve():
    states = [Case("0010001000",5),Case("0010001000",4),Case("0010001000",3),Case("0010001000",2),
                Case("0010001000",1),Case("0010001000",0)]
    results= [3,4,3,2,1,2]

    for i in range(len(states)):
        print(f"{states[i].state} {solve(states[i])}")

checkSolve()
