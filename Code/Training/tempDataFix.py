import numpy as np
import pickle as pk

def fixData(fNum):
    
    x = np.load('x'+str(fNum)+'.pickle',allow_pickle=True)
    y = np.load('y'+str(fNum)+'.pickle',allow_pickle=True)
    
    idxsToRem = []
    for i in range(x.shape[0]):
        s = sum(y[i])
        if s!=1: idxsToRem.append(i)
    
    s = set(list([i for i in range(x.shape[0])]))
    s2 = set(idxsToRem)
    
    idxsToKeep = list(s-s2)
    
    x = x[idxsToKeep]
    y = y[idxsToKeep]
    
    if x.shape[0]==y.shape[0]: print('Check Passed')
    
    with open('X'+str(fNum)+'.pickle', 'wb') as f:
        pk.dump(x, f, protocol=pk.HIGHEST_PROTOCOL)
    with open('Y'+str(fNum)+'.pickle', 'wb') as f:
        pk.dump(y, f, protocol=pk.HIGHEST_PROTOCOL)
        
        
def convertY(fNum):
    

    y = np.load('Y'+str(fNum)+'.pickle',allow_pickle=True)
    
    newY = []
    for i in range(y.shape[0]):
        temp = list(y[i])
        s = temp.index(1)
        newY.append(s)
    
    with open('yf'+str(fNum)+'.pickle', 'wb') as f:
        pk.dump(newY, f, protocol=pk.HIGHEST_PROTOCOL)
    
convertY(7)
print('a')
convertY(6)
print('a')
convertY(5)
print('a')
convertY(2)
print('a')
    
