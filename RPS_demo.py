import numpy as np
import altair as alt 
import pandas as pd
import time
np.random.seed(16)

class RPSTrainer:
    def __init__(self):
        self.ACTIONS = 3
        self.ROCK = 0
        self.PAPER = 1
        self.SCISSORS = 2
        self.regretSum = np.zeros(self.ACTIONS)
        self.strategy = np.zeros(self.ACTIONS)
        self.strategySum = np.zeros(self.ACTIONS)

    def getStrategy(self):
        normalizingSum = 0
        for a in range(self.ACTIONS):
            self.strategy[a] = self.regretSum[a] if self.regretSum[a]>0 else 0
            normalizingSum += self.strategy[a]
        for a in range(self.ACTIONS):
            if(normalizingSum>0):
                self.strategy[a] /= normalizingSum
            else:
                self.strategy[a] = 1.0/self.ACTIONS
            self.strategySum[a] += self.strategy[a]
        return self.strategy

    def getAction(self,strategy):
        r = np.random.random()
        a = 0
        cumulativeProbability = 0
        while(a<self.ACTIONS-1):
            cumulativeProbability+=strategy[a]
            if(r<cumulativeProbability):
                break
            a+=1
        return a

    def train(self,iterations):
        actionUtility = np.zeros(self.ACTIONS)
        results = []

        for i in range(iterations):

            strategy = self.getStrategy()
            myAction = self.getAction(strategy)

            actionUtility = np.zeros(self.ACTIONS)
            if myAction==0:
                actionUtility = np.array([0,-1,1])
            if myAction==1:
                actionUtility = np.array([1,0,-1])
            if myAction==2:
                actionUtility = np.array([-1,1,0])

            for a in range(self.ACTIONS):
                self.regretSum[a]+=actionUtility[a]-actionUtility[myAction]
                
            results.append(self.getAverageStrategy())
            a,b,c = self.getAverageStrategy()
            if len(results)>50:
                if (round(a,2)==0.33 and round(b,2)==0.33) or (round(b,2)==0.33 and round(c,2)==0.33) or (round(a,2)==0.33 and round(c,2)==0.33):
                   break 
        return np.array(results)

    def getAverageStrategy(self):
        avgStrategy = np.zeros(self.ACTIONS)
        normalizingSum = 0
        for a in range(self.ACTIONS):
            normalizingSum+=self.strategySum[a]
        for a in range(self.ACTIONS):
            if(normalizingSum>0):
                avgStrategy[a] = self.strategySum[a] / normalizingSum
            else:
                avgStrategy = [1,0,0]
        return avgStrategy

def norm(array):
	norm = np.sum(array)
	normal_array = array/norm
	return normal_array

def vizLOESS(source):
	alt.renderers.enable('altair_viewer')
	base = alt.Chart(source).mark_circle(opacity=0.5).transform_fold(
    	fold=['Rock', 'Paper', 'Scissor'],
    	as_=['Move', 'Move Probability']
	).encode(
    	alt.X('Iterations:Q'),
    	alt.Y('Move Probability:Q'),
    	alt.Color('Move:N')
	)

	return (base)

def vizWin(source):
	alt.renderers.enable('altair_viewer')
	newdict = pd.DataFrame([norm(np.unique(np.array(source)[i], return_counts = True )[1]) for i in range(len(source))])
	newdict.columns = ['Loss','Draw','Win']
	lenth = len(newdict.Loss.values)
	newnew = pd.DataFrame({'Iteration':np.array(list(range(len(newdict.Loss.values)))*3),'Type':(['Loss']*lenth + ['Draw']*lenth+['Win']*lenth), 'Tie/Loss/Win':np.array(list(newdict.Loss.values) + list(newdict.Draw.values) + list(newdict.Win.values))})
	base = alt.Chart(newnew).mark_bar(opacity=0.85).encode(
    x='Iteration:O',
    y='Tie/Loss/Win:Q',
    order=alt.Order(
      # Sort the segments of the bars by this field
      'Type:N',
      sort='ascending'
    ),
    color=alt.Color('Type:N',
                   scale=alt.Scale(
            domain=['Loss', 'Draw','Win'],
            range=['red', 'grey','green']))
	)
	
	text = alt.Chart(newnew).mark_text(size = 7, dy=8, color='white').encode(
    x=alt.X('Iteration:O'),
    y=alt.Y('Tie/Loss/Win:Q', stack = 'zero'),
    detail='Type:N',
    text=alt.Text('Tie/Loss/Win:Q', format = '0.2f'),
    order=alt.Order(
      'Type:N',
      sort='ascending'
    )
	)

	return base + text

def rps(numSim,myStrat,oppStrat=[0.52,0.29,0.19]):
    ret = []
    for strat in myStrat: 
        i = np.random.choice([0,1,2],numSim,p=strat)
        j = np.random.choice([0,1,2],numSim,p=oppStrat)
        i = i-j
        i = [0 if j==0 else (-1 if j==2 or j==-1 else 1) for j in i]
        ret.append(np.array(i)) 
    return ret

trainer = RPSTrainer()
start = time.time()
res = trainer.train(12000)[1:]
print('Training time:',round((time.time()-start)*1000,1),'ms')
print('Final strategy',[round(i,2) for i in trainer.getAverageStrategy()])



print('Generating Graph...')
start = time.time()
winrate = rps(50000,res)
print('Simulated',50000*len(res)/1000000,'Million Games in',round(time.time()-start,2),'seconds')
vizWin(winrate).show() #just normalize and itll be good to 2 sf 
df = pd.DataFrame({'Iterations':np.array(range(len(res[:,0]))),'Rock':res[:,0],'Paper':res[:,1],'Scissor':res[:,2]})
vizLOESS(df).show()

















