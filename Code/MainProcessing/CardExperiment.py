import treys
import itertools

evaluator = treys.Evaluator()

ranks = list(treys.Card.CHAR_RANK_TO_INT_RANK.keys())
suits = list(treys.Card.CHAR_SUIT_TO_INT_SUIT.keys())
cards = []
for i in range(len(ranks)):
    for j in range(len(suits)): cards.append(ranks[i]+suits[j])

cardInts = []
for i in range(len(cards)):
    cardInts.append(treys.Card.new(cards[i]))

cardIntsSet = set(cardInts)

hand = [1065995,1082379]#cardInts[0:2]

allTableCards = itertools.combinations(cardIntsSet - set(hand),5)

count = 1
vec = []
print('Begin:')

for table in allTableCards:
    w,t,l = 0,0,0
    
    allOppCards = itertools.combinations(cardIntsSet - set(hand) - set(table), 2)
    table = list(table)
    for opp in allOppCards:
        opp = list(opp)
        our = evaluator.evaluate(hand, table)
        their = evaluator.evaluate(opp, table)
        
        if our==their:
            t+=1
        elif our>their:
            w+=1
        else:
            l+=1
        
        if count%1000000==0:
            print(str(count/2095452651))
        count+=1
        
    
    

'''
gen all 5/6/7 isomorphism lists: then split those into {2}x{3,4,5} combinations and analyze from there
important: some isomorphisms from the same problem (5/6/7) occur more than others, need to keep that count

'''