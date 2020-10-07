import numpy as np
import pickle as pk
import sys
import time

#(f,c,0.6,1.1,2.2,all)
def trainNN(cNum,numObv,numLayer,nodePerLayer):
    from keras.layers import Dense, Input
    from keras import Model
    from keras.utils import to_categorical    
    from keras.callbacks import EarlyStopping
    
    app = 'full' if numObv==-1 else str(numObv)
    x = np.load('FinalData/finalX'+str(cNum)+'_'+app+'.pickle',allow_pickle=True)
    y = np.load('FinalData/finalY'+str(cNum)+'_'+app+'.pickle',allow_pickle=True)
    y = to_categorical(y)
    
    model = 0
    if numLayer==3:
        inputs = Input(shape=(x.shape[1],))
        hidden1 = Dense(nodePerLayer, activation='relu')(inputs)
        hidden2 = Dense(nodePerLayer, activation='relu')(hidden1)
        hidden3 = Dense(nodePerLayer, activation='relu')(hidden2)
        outputs = Dense(6,activation='softmax')(hidden3)
        model = Model(inputs,outputs)
        
    elif numLayer==5:
        inputs = Input(shape=(x.shape[1],))
        hidden1 = Dense(nodePerLayer, activation='relu')(inputs)
        hidden2 = Dense(nodePerLayer, activation='relu')(hidden1)
        hidden3 = Dense(nodePerLayer, activation='relu')(hidden2)
        hidden4 = Dense(nodePerLayer, activation='relu')(hidden3)
        hidden5 = Dense(nodePerLayer, activation='relu')(hidden4)
        outputs = Dense(6,activation='softmax')(hidden5)
        model = Model(inputs,outputs)
    elif numLayer==7:
        inputs = Input(shape=(x.shape[1],))
        hidden1 = Dense(nodePerLayer, activation='relu')(inputs)
        hidden2 = Dense(nodePerLayer, activation='relu')(hidden1)
        hidden3 = Dense(nodePerLayer, activation='relu')(hidden2)
        hidden4 = Dense(nodePerLayer, activation='relu')(hidden3)
        hidden5 = Dense(nodePerLayer, activation='relu')(hidden4)
        hidden6 = Dense(nodePerLayer, activation='relu')(hidden5)
        hidden7 = Dense(nodePerLayer, activation='relu')(hidden6)
        outputs = Dense(6,activation='softmax')(hidden7)
        model = Model(inputs,outputs)
    
    model.compile(optimizer='adam',loss='categorical_crossentropy', metrics=['accuracy'])
    usualCallback = EarlyStopping()
    overfitCallback = EarlyStopping(monitor='loss', min_delta=0.0001, patience = 50)
    
    start = time.time()
    model.fit(x,y,epochs=100000,callbacks=[overfitCallback],verbose= 2)
    print("Model Fit in "+str(round(time.time()-start,2))+' seconds')
    
    x = np.load('FinalData/finalX'+str(cNum)+'_full.pickle',allow_pickle=True)
    y = np.load('FinalData/finalY'+str(cNum)+'_full.pickle',allow_pickle=True)
    y = to_categorical(y)
    y = [np.argmax(i) for i in y]
    y = np.reshape(y,(-1,1))
    
    pred = model.predict(x)
    pred = [np.argmax(i) for i in pred]
    
    err = np.reshape(pred,(-1,1))-y
    
    count = 0
    for i in err:
        if i!=0: count+=1
    print('Classification Error: '+str(round(100*count/x.shape[0],3))+'%')
    return model


m={1: (2, 3, 16),2: (2, 5, 16),3: (2, 7, 16),4: (2, 3, 64),5: (2, 5, 64),6: (2, 7, 64),
 7: (2, 3, 128),8: (2, 5, 128),9: (2, 7, 128),10: (2, 3, 512),11: (2, 5, 512),12: (2, 7, 512),
 13: (2, 3, 1024),14: (2, 5, 1024),15: (2, 7, 1024),25: (2, 3, 4096),26: (2, 5, 4096),
 27: (2, 7, 4096),16: (5, 3, 16),17: (5, 5, 16),18: (5, 7, 16),19: (5, 3, 64),20: (5, 5, 64),
 21: (5, 7, 64),22: (5, 3, 128),23: (5, 5, 128),24: (5, 7, 128),28: (5, 3, 512),29: (5, 5, 512),30: (5, 7, 512),
 31: (5, 3, 1024),32: (5, 5, 1024),33: (5, 7, 1024),34: (5, 3, 4096),35: (5, 5, 4096),
 36: (5, 7, 4096),37: (6, 3, 16),38: (6, 5, 16),39: (6, 7, 16),40: (6, 3, 64),41: (6, 5, 64),
 42: (6, 7, 64),43: (6, 3, 128),44: (6, 5, 128),45: (6, 7, 128),46: (6, 3, 512),
 47: (6, 5, 512),48: (6, 7, 512),49: (6, 3, 1024),50: (6, 5, 1024),51: (6, 7, 1024),
 52: (6, 3, 4096),53: (6, 5, 4096),54: (6, 7, 4096),55: (7, 3, 16),56: (7, 5, 16),
 57: (7, 7, 16),58: (7, 3, 64),59: (7, 5, 64),60: (7, 7, 64),61: (7, 3, 128),
 62: (7, 5, 128),63: (7, 7, 128),64: (7, 3, 512),65: (7, 5, 512),66: (7, 7, 512),
 67: (7, 3, 1024),68: (7, 5, 1024),69: (7, 7, 1024),70: (7, 3, 4096),71: (7, 5, 4096),72: (7, 7, 4096)}


params = m[int(sys.argv[1])]
rNum,nLayers,nNodes = params

print(rNum)
print(nLayers)
print(nNodes)

clf = trainNN(rNum, -1, nLayers, nNodes)
with open('NN'+str(rNum)+'_'+str(nLayers)+'_'+str(nNodes)+'.pickle', 'wb') as f:
    pk.dump(clf, f, protocol=pk.HIGHEST_PROTOCOL)
