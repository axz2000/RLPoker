import numpy as np
import pickle as pk
import sys

numToAlpha = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m',14:'n',15:'o',16:'p',17:'q',18:'r',19:'s',20:'t',21:'u'}
numToFNum = {1:2,2:5,3:6,4:7}
def process(num):
	num = numToFNum[int(num)]
	matList, labelList = [],[]
	for f in list(numToAlpha.values()):
		print(len(matList),flush=True,end=' ')
		matList.append(np.load(f+'_x'+str(num)+'.pickle',allow_pickle=True))
		labelList.append(np.load(f+'_y'+str(num)+'.pickle',allow_pickle=True))		
	print('\nAll Files Loaded',flush=True)
	
	fullMat = np.vstack(matList)
	fullLab = np.concatenate(labelList)
	matList, labelList = [],[]
	print('Concatenated',flush=True)
	
	fullMat, idxs = np.unique(fullMat, axis=0, return_index=True)
	fullLab = fullLab[idxs]
	if (fullLab.shape[0]!=fullMat.shape[0]): 1/0
	print('Uniques Found, Check Passed',flush=True)
	
	with open('finalX'+str(num)+'.pickle','wb') as f:
		pk.dump(fullMat, f, protocol=pk.HIGHEST_PROTOCOL)
	print('X Written',flush=True)

	with open('finalY'+str(num)+'.pickle','wb') as f:
		pk.dump(fullLab, f, protocol=pk.HIGHEST_PROTOCOL)
	print('Y Written',flush=True)

process(sys.argv[1])
