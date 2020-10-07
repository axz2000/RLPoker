import numpy as np
import pickle as pk

from Matchstate2Bet import M2B
from Matchstate2Card import M2CF
from H2F import featGetter



class M2A:
    def __init__(self, f1,f2,f3,f4):
        self.card2num = {}
        for i,rank in enumerate(['2','3','4','5','6','7','8','9','T','J','Q','K','A']):
            for j,suit in enumerate(['c','d','h','s']):
                self.card2num[rank+suit] = 4*i + j+1
        self.fg = featGetter()
        print('FeatGetter Loaded',flush=True)

        self.m2 = np.load(f1,allow_pickle=True)
        self.m5 = np.load(f2,allow_pickle=True)
        self.m6 = np.load(f3,allow_pickle=True)
        self.m7 = np.load(f4,allow_pickle=True)
        print('Models Loaded',flush=True)

    def retAct(self, matchstate):
        b = M2B(matchstate)
        cf = M2CF(matchstate, self.card2num, self.fg)
    
        feats = list(cf)+b
        feats = np.reshape(feats,(1,-1))
        
        if len(cf)==1:
            return self.m7.predict(feats)[0]
        elif len(cf)==11:
            return self.m6.predict(feats)[0]
        elif len(cf)==21:
            return self.m5.predict(feats)[0]
        else:
            return self.m2.predict(feats)[0]
        
    def getBets(self, matchstate):
        matchstate = matchstate.strip()
        arr = matchstate.split(':')
        actionStr = arr[3]
        rounds = actionStr.split('/')
        if rounds[-1]=='':
            rounds = rounds[:-1]
    
        sb, bb = -1,-1
    
        ourBets = []
        theirBets = []
        isSBTurn = True
        areweSB = True if matchstate[matchstate.find("|")-1]==':' else False
        if len(rounds)==0:
            if areweSB: return [50, 0, 0, 0],[100,0,0,0]
            else: return [100, 0, 0, 0],[50,0,0,0]
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
                    if areweSB:
                        ourBets.append(sb)
                        theirBets.append(bb)
                    else:
                        ourBets.append(bb)
                        theirBets.append(sb)
                    toFill = 4-len(ourBets)
                    return ourBets+toFill*[0],theirBets+toFill*[0]
    
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
    
            if areweSB:
                ourBets.append(sb)
                theirBets.append(bb)
            else:
                ourBets.append(bb)
                theirBets.append(sb)
    
        toFill = 4-len(ourBets)
        return ourBets+toFill*[0],theirBets+toFill*[0]

    def retMoveStr(self, matchstate):
        act = self.retAct(matchstate)
        if act==0:
            return 'f'
        elif act==1:
            return 'c'
        else:
            our,their = self.getBets(matchstate)
            pot = 2 * max(sum(our),sum(their))
            if act==2:
                return 'r'+str(int(0.6*pot + sum(our)))
            elif act==3:
                return 'r'+str(int(1.1*pot + sum(our)))
            elif act==4:
                return 'r'+str(int(2.2*pot + sum(our)))
            elif act==5:
                return 'r20000'
            else: 1/0
