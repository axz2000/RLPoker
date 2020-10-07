import numpy as np
import pickle as pk
import time






# 1 for CART, 2 for XGB, 3 for NN
#2: -1 (Full)
#5: 500,1000,2500,10000,50000,-1 
#6: 500,1000,2500,10000,50000,-1
#7: 500, 2500, -1
def trainModel(modelChoice,cNum,numObv,hyperParam=15):
    if modelChoice==1:
        from sklearn.tree import DecisionTreeClassifier
        clf = DecisionTreeClassifier(max_depth=hyperParam)
        
    elif modelChoice==2:
        from sklearn.ensemble import GradientBoostingClassifier
        clf = GradientBoostingClassifier(max_depth=hyperParam)   
    app = 'full' if numObv==-1 else str(numObv)
    x = np.load('FinalData/finalX'+str(cNum)+'_'+app+'.pickle',allow_pickle=True)
    y = np.load('FinalData/finalY'+str(cNum)+'_'+app+'.pickle',allow_pickle=True)
    
    start = time.time()
    model = clf.fit(x,y)
    print("Model Fit in "+str(round(time.time()-start,2))+' seconds')
    
    x = np.load('FinalData/finalX'+str(cNum)+'_full.pickle',allow_pickle=True)
    y = np.load('FinalData/finalY'+str(cNum)+'_full.pickle',allow_pickle=True)
    y = np.reshape(y,(-1,1))
    pred = model.predict(x)
    err = np.reshape(pred,(-1,1))-y
    
    count = 0
    for i in err:
        if i!=0: count+=1
    print('Classification Error: '+str(round(100*count/x.shape[0],3))+'%')
    return clf



import sys

rNum = int(sys.argv[1])
hyp = int(sys.argv[2])

print(rNum)
print(hyp)

clf = trainModel(2,rNum,-1,hyp)
with open('XGB'+str(rNum)+'_'+str(hyp)+'.pickle', 'wb') as f:
    pk.dump(clf, f, protocol=pk.HIGHEST_PROTOCOL)



'''
clf2 = trainModel(1,2,-1,15)
clf5 = trainModel(1,5,-1,16)
clf6 = trainModel(1,6,-1,16)
clf7 = trainModel(1,7,-1,16)

with open('CART2_15.pickle', 'wb') as f:
    pk.dump(clf2, f, protocol=pk.HIGHEST_PROTOCOL)
with open('CART5_16.pickle', 'wb') as f:
    pk.dump(clf5, f, protocol=pk.HIGHEST_PROTOCOL)
with open('CART6_16.pickle', 'wb') as f:
    pk.dump(clf6, f, protocol=pk.HIGHEST_PROTOCOL)
with open('CART7_16.pickle', 'wb') as f:
    pk.dump(clf7, f, protocol=pk.HIGHEST_PROTOCOL)


'''
