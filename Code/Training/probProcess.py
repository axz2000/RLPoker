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
    if rat < 1.1:
        return 0.5
    if rat < 2.2:
        return 1
    if rat < 5.25:
        return 2.5
    else:
        return -1 #all-in
    
def mapActToIdx(act):
    if act==0.5:
        return 2
    elif act==1:
        return 3
    elif act==2.5:
        return 4
    else:
        return 5
    

numToAlpha = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m',14:'n',15:'o',16:'p',17:'q',18:'r',19:'s',20:'t',21:'u'}
import sys

whichF = numToAlpha[int(sys.argv[1])]

fpi = open(whichF,'r')
fmi = open(whichF+'2','r')

fpo = open(whichF+'_labelProbs','w')



#(f,c,0.5,1,2.5,all)

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
    line = line.split("|")
    if line[-1]=='': line=line[:-1]
    
    for act in line:
        form, p, amt = '',-1,-1
        
        act = act.split(",")
        for j,info in enumerate(act):
            info = info.strip()
            
            found = False
            for i,c in enumerate(info):
                if c.isnumeric():
                    info = info[i:]
                    found=True
                    break
            if not found: info = info[-1]
            if j==0:
                if info=='102' or info=='f': form='f'
                elif info=='98' or info=='b': form='b'
                elif info=='99' or info=='c': form='c'
                else: 
                    print(info)
                    2/0
                
            elif j==1:
                p = float(info)
    
            elif j==2:
                amt = int(info)
                
            else: 1/0
        if form=='f':
            probs[0] += p
        elif form=='b':
            actToTake = mapBetToAct(amt/pot)
            probs[mapActToIdx(actToTake)] += p
        else:
            probs[1] += p
    if probs==[0,0,0,0,0,0]:
        print(ll)
	print(line2)
        break
    for val in probs[:-1]:
        fpo.write(str(val)+',')
    fpo.write(str(probs[-1])+'\n')

fpi.close()
fmi.close()
fpo.close()
        
        
