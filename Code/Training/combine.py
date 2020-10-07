import numpy as np
import pickle as pk
import sys

numToAlpha = {1:'a',2:'b',3:'c',4:'d',5:'e',6:'f',7:'g',8:'h',9:'i',10:'j',11:'k',12:'l',13:'m',14:'n',15:'o',16:'p',17:'q',18:'r',19:'s',20:'t',21:'u'}

whichF = numToAlpha[int(sys.argv[1])]

x2 = np.load(whichF+"_cardfeat.pickle",allow_pickle=True)
xBet = np.load(whichF+"_bet.pickle",allow_pickle=True)
print('1')
xnp = np.asarray(x2)
print('2')

x2, x5, x6, x7 = [],[],[],[]

count = 0
for arr in xnp:
    if count%1000000==0: print(count//1000000, end=' ')
    l = len(arr)
    
    if l==31:
        x2.append(count)
    elif l==21:
        x5.append(count)
    elif l==11:
        x6.append(count)
    else: 
        x7.append(count)
        
    count+=1

fi = open(whichF+'_act','r')
labels = []
for line in fi:
    labels.append(int(line.strip()))
labels = np.asarray(labels)



    
print('\nhere',flush=True)
x2x = np.stack(xnp[x2],axis=0)
x2x = np.hstack([x2x,xBet[x2]])
y2y = labels[x2]
if x2x.shape[1]!=35 or x2x.shape[0]!=y2y.shape[0]:
    print('erra',flush=True)
    1/0
x2x, idxs = np.unique(x2x, axis=0, return_index=True)
y2y = y2y[idxs]
if (x2x.shape[0]!=y2y.shape[0]): 1/0
with open(whichF+'_y2.pickle', 'wb') as f:
    pk.dump(y2y, f, protocol=pk.HIGHEST_PROTOCOL)
with open(whichF+'_x2.pickle', 'wb') as f:
    pk.dump(x2x, f, protocol=pk.HIGHEST_PROTOCOL)
print('done2',flush=True)



x2x = np.stack(xnp[x5],axis=0)
x2x = np.hstack([x2x,xBet[x5]])
y2y = labels[x5]
if x2x.shape[1]!=25 or x2x.shape[0]!=y2y.shape[0]:
    print('errb',flush=True)
    1/0
x2x, idxs = np.unique(x2x, axis=0, return_index=True)
y2y = y2y[idxs]
if (x2x.shape[0]!=y2y.shape[0]): 1/0
with open(whichF+'_y5.pickle', 'wb') as f:
    pk.dump(y2y, f, protocol=pk.HIGHEST_PROTOCOL)
with open(whichF+'_x5.pickle', 'wb') as f:
    pk.dump(x2x, f, protocol=pk.HIGHEST_PROTOCOL)
print('done5',flush=True)





x2x = np.stack(xnp[x6],axis=0)
x2x = np.hstack([x2x,xBet[x6]])
y2y = labels[x6]
if x2x.shape[1]!=15 or x2x.shape[0]!=y2y.shape[0]:
    print('errc',flush=True)
    1/0
x2x, idxs = np.unique(x2x, axis=0, return_index=True)
y2y = y2y[idxs]
if (x2x.shape[0]!=y2y.shape[0]): 1/0
with open(whichF+'_y6.pickle', 'wb') as f:
    pk.dump(y2y, f, protocol=pk.HIGHEST_PROTOCOL)
with open(whichF+'_x6.pickle', 'wb') as f:
    pk.dump(x2x, f, protocol=pk.HIGHEST_PROTOCOL)
print('done6',flush=True)




x2x = np.stack(xnp[x7],axis=0)
x2x = np.hstack([x2x,xBet[x7]])
y2y = labels[x7]
if x2x.shape[1]!=5 or x2x.shape[0]!=y2y.shape[0]:
    print('errd',flush=True)
    1/0
x2x, idxs = np.unique(x2x, axis=0, return_index=True)
y2y = y2y[idxs]
if (x2x.shape[0]!=y2y.shape[0]): 1/0
with open(whichF+'_y7.pickle', 'wb') as f:
    pk.dump(y2y, f, protocol=pk.HIGHEST_PROTOCOL)
with open(whichF+'_x7.pickle', 'wb') as f:
    pk.dump(x2x, f, protocol=pk.HIGHEST_PROTOCOL)
print('done7',flush=True)

