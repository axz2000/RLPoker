def M2B(matchstate):
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
        return [50, 0, 0, 0],[100, 0, 0, 0] 
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
                return ourBets + toFill*[0],theirBets + toFill*[0]
            
            elif act[0]=='c':
                if i==0:
                    continue
                else:
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
    
    return ourBets + toFill*[0],theirBets + toFill*[0]




#(0.5,1,2,all)
def mapBetToAct(rat):
    if rat < 0.2:
        return 0.6
    if rat < 0.55:
        return 1.1
    if rat < 1.1:
        return 2.2
    else:
        return -1 #all-in
    
def mapActToIdx(act):
    if act==0.6:
        return 2
    elif act==1.1:
        return 3
    elif act==2.2:
        return 4
    else:
        return 5
    

numToAlpha = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m',14:'n',15:'o',16:'p',17:'q',18:'r',19:'s',20:'t',21:'u'}
import sys

whichF = numToAlpha[int(sys.argv[1])]

fpi = open(whichF,'r')
fmi = open(whichF+'2','r')

fpo = open(whichF+'_act','w')



#(f,c,0.6,1.1,2.2,all)

count = 0
for line in fpi:
    count+=1
    if count%1000000==0: print(count//1000000, end=' ', flush=True)
    
    probs = [0]*6
    
    line2 = fmi.readline()
    
    line,line2 = line.strip(),line2.strip()
    
    bets = M2B(line2)
    pot = sum(bets[0]) + sum(bets[1])
    
    ll = line
    actact = 0
    amt = 0
    if line[0:2]=='BE':
        amt = int(line[line.index("BET")+3:])
        actact = mapActToIdx(mapBetToAct(abs(amt-pot)/pot))
    elif line[0:2]=='FO':
        actact = 0
    elif line[0:2]=='CA':
        actact = 1
    else:
        1/0
    fpo.write(str(actact)+'\n')

fpi.close()
fmi.close()
fpo.close()
        
       






 
