import numpy as npimport pickle as pkimport arrayfrom itertools import combinationsclass featGetter():        def __init__(self):        #Matrix idxs X feats        self.twoI2F = np.load('I2F/twoI2F.pickle',allow_pickle=True)        self.fiveI2F = np.load('I2F/fiveI2F.pickle',allow_pickle=True)        self.sixI2F = np.load('I2F/sixI2F.pickle',allow_pickle=True)                #Dict        self.twoH2I = np.load('H2I/twoH2I.pickle',allow_pickle=True)        self.fiveH2I = np.load('H2I/fiveH2I.pickle',allow_pickle=True)        self.sixH2I = np.load('H2I/sixH2I.pickle',allow_pickle=True)                #LookupTable        handsDB = open('HandRanks.dat', 'rb')        self.HR = array.array('i')        self.HR.fromfile(handsDB, 32487834)        handsDB.close()        return        def hand2Key(self, hand): #assume array of ints 1-52, first 2 are hole        numCards = len(hand)        hole = sorted(hand[0:2])        table = sorted(hand[2:])                hand = hole+table                key = str(hand[0])        for i in range(1,numCards):            if hand[i]<10: key+= '0'+str(hand[i])            else: key+= str(hand[i])                        return int(key)        def K2I(self, numCards, key):        if numCards==2: return self.twoH2I[key]        elif numCards==5: return self.fiveH2I[key]        else: return self.sixH2I[key]            #returns numpy array    def I2F(self, numCards, index):        if numCards==2: return self.twoI2F[index,:]        elif numCards==5: return self.fiveI2F[index,:]        else: return self.sixI2F[index,:]                    def getScore(self, hand): #given 7-arr of ints, return score        inputScore = self.HR[53 + hand[0]];        for i in range(1,len(hand)):            inputScore = self.HR[inputScore + hand[i]]        return inputScore    def updateScore(self, score,rem): #given 7-arr of ints, return score        for i in range(0,len(rem)):            score = self.HR[score + rem[i]]        return score        def EHS7(self, cards):        s1 = set(cards)                    intersect = list(set([i for i in range(1,53)])-s1)                k = 2        tableScore = self.getScore(cards[2:])        inputScore = self.updateScore(tableScore, cards[0:2])                w,l,t = 0,0,0        for combo in combinations(intersect, k):            temp = self.updateScore(tableScore, combo)            if temp>inputScore: l+=1            elif temp==inputScore: t+=1            else: w+=1        return np.array([round((w+0.5*t)/(w+l+t),2)])            def H2F(self, hand):        if len(hand)<7:            numCards = len(hand)            key = self.hand2Key(hand)            index = self.K2I(numCards, key)            return self.I2F(numCards, index)        else:            return self.EHS7(hand)                                                         