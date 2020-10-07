import array
from itertools import combinations
import math

handsDB = open('HandRanks.dat', 'rb')
HR = array.array('i')
HR.fromfile(handsDB, 32487834)
handsDB.close()

def getScore(hand): #given 7-arr of ints, return score
    inputScore = HR[53 + hand[0]];
    for i in range(1,len(hand)):
        inputScore = HR[inputScore + hand[i]]
    return inputScore

def updateScore(score,rem): #given 7-arr of ints, return score
    for i in range(0,len(rem)):
        score = HR[score + rem[i]]
    return score


def histo56(cards, b, H2I, I2EHS):
    a = len(cards)
    histo = [0]*100
    
    s1 = set(cards)
        
    intersect = list(set([i for i in range(1,53)])-s1)
    
    k = b-a

    if a == 2:
        c = sorted([c for c in cards])+[-1]*k
    elif a == 5:
        c = sorted([c for c in cards[0:2]]) + sorted([c for c in cards[2:]]) +[-1]*k
    
    for combo in combinations(intersect, k):
        c[a:b] = combo
        
        if a==5: cFinal = c[0:2] + sorted([cc for cc in c[2:]])
        else: cFinal = c 
        
        s = str(cFinal[0])
        for card in cFinal[1:]:
            s += '0'+str(card) if card<10 else str(card)
        
        temp = H2I[int(s)]
        s = float(I2EHS[temp])
        
        s = int(math.floor(s*100))
        if s==100: s=99
        histo[s] += 1
        
    return histo

def EHS7(cards):
    s1 = set(cards)
        
    intersect = list(set([i for i in range(1,53)])-s1)
    
    k = 2
    tableScore = getScore(cards[2:])
    inputScore = updateScore(tableScore, cards[0:2])
    
    w,l,t = 0,0,0
    for combo in combinations(intersect, k):
        temp = updateScore(tableScore, combo)
        if temp>inputScore: l+=1
        elif temp==inputScore: t+=1
        else: w+=1
    return (w+0.5*t)/(w+l+t)

def histo7(cards):
    a = len(cards)
    b = 7
    histo = [0]*100
    
    s1 = set(cards)
        
    intersect = list(set([i for i in range(1,53)])-s1)
    
    k = b-a    
    c = [c for c in cards]+[-1]*k
    
    for combo in combinations(intersect, k):
        c[a:b] = combo
        
        s = round(EHS7(c),3)
        
        s = int(math.floor(s*100))
        if s==100: s=99
        histo[s] += 1
        
    return histo

    

import numpy as np
import csv

handlen = 5
outto = 6

if handlen==6: s = 'six'
elif handlen==5: s = 'five'
else: s = 'two'

if outto==5: ss = 'five'
else: ss = 'six'

H2I = np.load("../"+ss+"H2I.pickle",allow_pickle=True)
I2EHS = np.load("../"+ss+"I2EHS.pickle",allow_pickle=True)

holder = np.load(s+'Hands'+'.pickle',allow_pickle=True)

myfile = open(s+'Hands'+str(handlen)+'_'+str(outto)+'.csv','w')
wtr = csv.writer(myfile, delimiter=',', quotechar='"')

cnt = 0
for hand in holder:
    cnt += 1
    if cnt%int(len(holder)/1000)==0:
        print(round(cnt/len(holder),3),end = ' ')
    histo = histo56(hand,outto,H2I,I2EHS)
    wtr.writerow(histo)
    myfile.flush()
myfile.close()