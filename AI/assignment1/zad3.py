import random

from numpy import nested_iters, sort

class Card:
    def __init__(self,value,col):
        self.value = value
        self.col = col

    def __eq__(self,other):
        return (self.value==other.value and self.col==other.col)

    def __str__(self):
        return f"[{self.value},{self.col}]"
    
    def __repr__(self):
        return str(self)

"""
zakładam, że karty w ręce są posortowane rosnąco 
"""
class Hand:
    def __init__(self,st,nd,rd,rth,fth):
        cards = [st,nd,rd,rth,fth]
        cards.sort(key=lambda card: card.value)

        self.st, self.nd, self.rd, self.rth, self.fth = cards[0], cards[1], cards[2], cards[3], cards[4]

    def __str__(self):
        return f"({self.st},{self.nd},{self.rd},{self.rth},{self.fth})"


def checkPoker(hand):
    return checkStrit(hand) and checkKolor(hand)

def checkKareta(hand):
    if hand.nd.value==hand.rd.value and hand.rd.value==hand.rth.value :
        if hand.st.value==hand.nd.value or hand.rth.value==hand.fth.value:
            return True
    return False

def checkFul(hand):
    return checkTrojka(hand) and (checkPara(hand)!="None")

def checkKolor(hand):
    return hand.st.col==hand.nd.col and hand.nd.col==hand.rd.col and hand.rd.col==hand.rth.col and hand.rth.col==hand.fth.col

def checkStrit(hand):
    return hand.st.value +1 ==hand.nd.value and hand.nd.value +1 ==hand.rd.value and hand.rd.value +1 ==hand.rth.value and hand.rth.value +1 ==hand.fth.value

def checkTrojka(hand):
    if hand.st.value==hand.nd.value and hand.nd.value==hand.rd.value:
        if hand.rd.value!=hand.rth.value: 
            return True

    if hand.nd.value==hand.rd.value and hand.rd.value==hand.rth.value:
        if hand.st.value!=hand.nd.value: 
            return True
    
    if hand.rd.value==hand.rth.value and hand.rth.value==hand.fth.value:
        if hand.nd.value!=hand.rd.value: 
            return True
    
    return False

def checkDwiePary(hand):
    para = checkPara(hand)

    if para=="None":
        return False
    if para=="st":
        return checkPara(Hand(Card(-1,0),Card(0,0),hand.rd,hand.rth,hand.fth))!="None"
    if para=="nd":
        return checkPara(Hand(hand.st,Card(-1,0),Card(0,0),hand.rth,hand.fth))!="None"
    if para=="rd":
        return checkPara(Hand(hand.st,hand.nd,Card(-1,0),Card(0,0),hand.fth))!="None"
    if para=="rth":
        return checkPara(Hand(hand.st,hand.nd,hand.rd,Card(-1,0),Card(0,0)))!="None"

def checkPara(hand):
    if hand.st.value==hand.nd.value and hand.nd.value!=hand.rd.value:
        return "st"
    if hand.nd.value==hand.rd.value and (hand.rd.value!=hand.rth.value and hand.st.value!=hand.nd.value):
        return "nd"
    if hand.rd.value==hand.rth.value and (hand.nd.value!=hand.rd.value and hand.rth.value!=hand.fth.value):
        return "rd"
    if hand.rth.value==hand.fth.value and hand.rd.value!=hand.rth.value:
        return "rth"

    return "None"

def evaluate(hand):
    if checkPoker(hand):
        return 8 
    if checkKareta(hand):
        return 7
    if checkFul(hand):
        return 6
    if checkKolor(hand):
        return 5
    if checkStrit(hand):
        return 4
    if checkTrojka(hand):
        return 3
    if checkDwiePary(hand):
        return 2
    if checkPara(hand)!="None":
        return 1
    return 0
    

def checkEvaluate():
    hand = Hand(Card(6,2),Card(6,1),Card(3,1),Card(6,3),Card(5,1))
    print(hand)
    print(evaluate(hand))

def getStPlayerDeck():
    deck = []
    for i in range(11,15):
        for j in range(1,5):
            deck.append(Card(i,j))
    return deck

def getNdPlayerDeck():
    deck = []
    for i in range(2,11):
        for j in range(1,5):
            deck.append(Card(i,j))
    return deck

def drawHand(deck):
    hand = random.sample(deck, 5)
    return Hand(hand[0],hand[1],hand[2],hand[3],hand[4])

def computeChance(rounds,ndDeck):
    stPlayerDeck = getStPlayerDeck()
    ndPlayerDeck = ndDeck

    n, ndWin = rounds, 0
    while n>0:
        stPlayerHand = drawHand(stPlayerDeck)
        ndPlayerHand = drawHand(ndPlayerDeck)

        stResult = evaluate(stPlayerHand)
        ndResult = evaluate(ndPlayerHand)

        if ndResult > stResult:
            ndWin+=1

        n-=1
    
    return ndWin/rounds

def solve():
    amountOfRounds ,attempt = 1000, 100
    result = 0 
    for i in range(attempt):
        result+=computeChance(amountOfRounds,getNdPlayerDeck())
    chance = result/attempt * 100
    print(f"Szanse na wygraną drugiego gracza przy standardowej tali {amountOfRounds} rozgrywkach to {chance}%")

    amountOfRounds ,attempt = 1000, 100
    result = 0 

    specialDeck = [Card(8,1), Card(8,2), Card(8,3), Card(8,4), Card(9,1), Card(9,2), Card(9,3), Card(9,4), Card(10,1), Card(10,2), Card(10,3), Card(10,4)]
    for i in range(attempt):
        result+=computeChance(amountOfRounds,specialDeck)
    chance = result/attempt * 100

    print(f"Szanse na wygraną drugiego gracza przy tali {specialDeck} \ni przy {amountOfRounds} rozgrywkach to {chance}%")

solve()