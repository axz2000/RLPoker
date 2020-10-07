import numpy as np
import pickle as pk
import sys
import random

argMap = {1:[-1],2:[500,1000,2500,10000,50000,-1],3:[500,1000,2500,10000,50000,-1],4:[500,2500,-1]}
nameMap = {1:2,2:5,3:6,4:7}
whichAmts = argMap[int(sys.argv[1])]
whichF = nameMap[int(sys.argv[1])]

x = np.load('finalX'+str(whichF)+'.pickle',allow_pickle=True)
y = np.load('finalY'+str(whichF)+'.pickle',allow_pickle=True)

for amt in whichAmts:
	if amt!=-1:
		idxs = random.sample(range(1, x.shape[0]), amt)
		xTemp,yTemp = x[idxs],y[idxs]
	else: xTemp,yTemp = x,y
	app = str(amt) if amt!=-1 else 'full'
	with open('finalY'+str(whichF)+'_'+app+'.pickle', 'wb') as f:
		pk.dump(yTemp, f, protocol=pk.HIGHEST_PROTOCOL)
	with open('finalX'+str(whichF)+'_'+app+'.pickle', 'wb') as f:
		pk.dump(xTemp, f, protocol=pk.HIGHEST_PROTOCOL)


