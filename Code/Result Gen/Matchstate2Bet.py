def M2B(matchstate):
    matchstate = matchstate.strip()
    arr = matchstate.split(':')
    actionStr = arr[3]
    rounds = actionStr.split('/')
    if rounds[-1]=='':
        rounds = rounds[:-1]
        
    sb, bb = -1,-1
    
    ourBets = []
    isSBTurn = True
    areweSB = True if matchstate[matchstate.find("|")-1]==':' else False
    if len(rounds)==0:
        if areweSB: return [50, 0, 0, 0]
        else: return [100, 0, 0, 0] 
    for rNum, r in enumerate(rounds):
        charLocs = []
        for i,c in enumerate(r):
            if c.isalpha(): charLocs.append(i)
            
        acts = []
        for i in range(len(charLocs)-1):
            temp = r[charLocs[i]:charLocs[i+1]]
            acts.append(temp)
        acts.append(r[charLocs[-1]:])
        
        if rNum==0:
            isSBTurn = True
            sb, bb = 50, 100
        else: 
            isSBTurn = False
            sb, bb = 0, 0
        
        for i, act in enumerate(acts):
            if act[0]=='f':
                if areweSB: ourBets.append(sb)
                else: ourBets.append(bb)
                toFill = 4-len(ourBets)
                return ourBets + toFill*[0]
            
            elif act[0]=='c':
                if i!=0:
                    if isSBTurn: sb=bb
                    else: bb=sb
            elif act[0]=='r':
                amt = int(act[1:])
                if isSBTurn: sb = amt
                else: bb = amt
            else: return 'ERROR ERROR'
                    
            isSBTurn = not isSBTurn 
            
        if areweSB: ourBets.append(sb)
        else: ourBets.append(bb)
   
    toFill = 4-len(ourBets)
    
    return ourBets + toFill*[0]
'''                    
import numpy as np
import pickle as pk
import sys

numToAlpha = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m',14:'n',15:'o',16:'p',17:'q',18:'r',19:'s',20:'t',21:'u'}
import sys

whichF = numToAlpha[int(sys.argv[1])]

fi = open(whichF+'2','r')
numLines = 0
for line in fi:
    numLines+=1
fi.close()

fi = open(whichF+'2','r')

betMat = np.zeros((numLines,4))

for i,matchstate in enumerate(fi):
    if i%1000000==0: print(i//1000000, end=' ',flush=True)
    betMat[i,:] = M2B(matchstate)
with open(whichF+'_bet.pickle', 'wb') as f:
    pk.dump(betMat, f, protocol=pk.HIGHEST_PROTOCOL) '''
