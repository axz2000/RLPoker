from H2F import featGetter


card2num = {}
for i,rank in enumerate(['2','3','4','5','6','7','8','9','T','J','Q','K','A']):
    for j,suit in enumerate(['c','d','h','s']):
        card2num[rank+suit] = 4*i + j+1

def M2CF(matchstate, card2num, fg):
    cardInfo = matchstate.strip().split(':')[-1]
    
    if cardInfo[0]=='|': cardInfo = cardInfo[1:]
    else: cardInfo = cardInfo[0:4] + cardInfo[5:]
    
    cardInfo = cardInfo.split('/')
    
    cards = ''
    for s in cardInfo:
        cards+=s
    
    hand = []
    for i in range(0,len(cards),2):
        currCard = cards[i:i+2]
        hand.append(card2num[currCard])
    return fg.H2F(hand)
    
'''
numToAlpha = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m',14:'n',15:'o',16:'p',17:'q',18:'r',19:'s',20:'t',21:'u'}
import sys
import numpy as np
import pickle as pk

whichF = numToAlpha[int(sys.argv[1])]

x = featGetter()
print('FG Loaded',flush=True)            
fi = open(whichF+'2','r')

featList = []

for i,matchstate in enumerate(fi):
    if i%100000==0: print(i//100000, end = ' ', flush=True)
    featList.append(M2CF(matchstate, card2num, x))

with open(whichF + '_cardfeat.pickle', 'wb') as f:
    pk.dump(featList, f, protocol=pk.HIGHEST_PROTOCOL)'''
